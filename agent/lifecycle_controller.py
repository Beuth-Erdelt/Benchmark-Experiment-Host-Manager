"""Start or resume one durable agent lifecycle inside Kubernetes.

The controller prepares an in-cluster kubeconfig and a runtime copy of
``cluster.config``, refreshes the environment descriptor, and then delegates to
the existing lifecycle wrapper. Persistent state lets a replacement Job pod
resume a submitted experiment without submitting it again.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import fcntl
import json
import os
import pprint
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

__all__ = ["main"]

_IN_CLUSTER_CONTEXT = "agent-in-cluster"
_SERVICE_ACCOUNT_DIRECTORY = Path("/var/run/secrets/kubernetes.io/serviceaccount")
_DEFAULT_ROOT = Path("/opt/bexhoma")
_DEFAULT_STATE_ROOT = Path("/state")
_DEFAULT_INPUT_DIRECTORY = Path("/input")
_RUN_LOCK = ".agent-run.lock"


class ControllerError(RuntimeError):
    """Report an invalid or incomplete lifecycle-controller setup."""


def _required_environment(name: str) -> str:
    """Return one required, non-empty environment variable."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise ControllerError(f"required environment variable {name} is empty")
    return value


def _write_in_cluster_kubeconfig(
    destination: Path,
    namespace: str,
    host: str,
    port: str,
    service_account_directory: Path = _SERVICE_ACCOUNT_DIRECTORY,
) -> None:
    """Write a kubeconfig that follows the pod's rotating service-account token."""
    certificate = service_account_directory / "ca.crt"
    token = service_account_directory / "token"
    if not certificate.is_file() or not token.is_file():
        raise ControllerError(
            f"service-account credentials are missing from {service_account_directory}"
        )
    configuration = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [{
            "name": _IN_CLUSTER_CONTEXT,
            "cluster": {
                "server": f"https://{host}:{port}",
                "certificate-authority": str(certificate),
            },
        }],
        "contexts": [{
            "name": _IN_CLUSTER_CONTEXT,
            "context": {
                "cluster": _IN_CLUSTER_CONTEXT,
                "namespace": namespace,
                "user": _IN_CLUSTER_CONTEXT,
            },
        }],
        "current-context": _IN_CLUSTER_CONTEXT,
        "users": [{
            "name": _IN_CLUSTER_CONTEXT,
            "user": {"tokenFile": str(token)},
        }],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.safe_dump(configuration), encoding="utf-8")


def _select_source_context(
    contexts: dict[str, Any], requested: str | None,
) -> dict[str, Any]:
    """Select the cluster-specific BeXhoma settings copied into pod context."""
    if requested:
        if requested not in contexts:
            raise ControllerError(
                f"AGENT_SOURCE_CONTEXT {requested!r} is absent from cluster.config"
            )
        return dict(contexts[requested])
    if len(contexts) != 1:
        raise ControllerError(
            "cluster.config contains multiple contexts; set AGENT_SOURCE_CONTEXT"
        )
    return dict(next(iter(contexts.values())))


def _write_runtime_cluster_config(
    source: Path,
    destination: Path,
    namespace: str,
    results: Path,
    source_context: str | None,
) -> None:
    """Write a pod-local BeXhoma configuration using in-cluster credentials."""
    try:
        configuration = ast.literal_eval(source.read_text(encoding="utf-8"))
        contexts = configuration["credentials"]["k8s"]["context"]
    except (KeyError, SyntaxError, ValueError) as error:
        raise ControllerError(f"cannot read BeXhoma configuration {source}: {error}") from error
    if not isinstance(contexts, dict):
        raise ControllerError("credentials.k8s.context must be a mapping")
    selected = _select_source_context(contexts, source_context)
    selected["namespace"] = namespace
    configuration["credentials"]["k8s"]["context"] = {
        _IN_CLUSTER_CONTEXT: selected,
    }
    configuration["benchmarker"]["resultfolder"] = str(results)
    destination.write_text(
        pprint.pformat(configuration, sort_dicts=False, width=100) + "\n",
        encoding="utf-8",
    )


def _events(run: Path) -> list[dict[str, Any]]:
    """Read valid JSON events from one investigation trajectory."""
    trajectory = run / "trajectory.jsonl"
    if not trajectory.is_file():
        return []
    events = []
    for line in trajectory.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def _has_submitted_outcome(run: Path) -> bool:
    """Return whether an investigation durably names a submitted benchmark."""
    return any(
        event.get("type") == "outcome" and event.get("code")
        for event in _events(run)
    )


def _recover_submitted_outcome(run: Path, status_directory: Path) -> bool:
    """Recover the narrow post-submit/pre-outcome crash window from status state."""
    if _has_submitted_outcome(run):
        return True
    phase = next(
        (
            event.get("phase")
            for event in reversed(_events(run))
            if event.get("type") == "meta" and event.get("phase")
        ),
        None,
    )
    if phase not in {"design", "interpret"}:
        return False
    for status_file in sorted(status_directory.glob("*.json"), reverse=True):
        try:
            status = json.loads(status_file.read_text(encoding="utf-8"))
            specification = Path(status["spec"]).resolve()
        except (KeyError, json.JSONDecodeError, OSError):
            continue
        if run.resolve() not in specification.parents:
            continue
        recovered = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "type": "outcome",
            "code": str(status["code"]),
            "summary": "Recovered a durable submission after controller restart.",
            "recovered_after_restart": True,
        }
        with (run / "trajectory.jsonl").open("a", encoding="utf-8") as trajectory:
            trajectory.write(json.dumps(recovered) + "\n")
        return True
    return False


def _latest_resumable(
    trajectories: Path, status_directory: Path,
) -> Path | None:
    """Return the newest unfinished investigation with a durable submission."""
    if not trajectories.is_dir():
        return None
    runs = sorted(
        (path for path in trajectories.iterdir() if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for run in runs:
        if (run / "answer.md").is_file():
            continue
        if _recover_submitted_outcome(run, status_directory):
            return run
    return None


def _status_for_run(run: Path, status_directory: Path) -> tuple[Path, dict[str, Any]]:
    """Return the durable status record whose submitted spec belongs to a run."""
    for status_file in sorted(status_directory.glob("*.json"), reverse=True):
        try:
            status = json.loads(status_file.read_text(encoding="utf-8"))
            specification = Path(status["spec"]).resolve()
        except (KeyError, json.JSONDecodeError, OSError):
            continue
        if run.resolve() in specification.parents:
            return status_file, status
    raise ControllerError(f"no submitted benchmark status belongs to {run}")


def _resume_benchmark_orchestrator(
    run: Path,
    status_directory: Path,
    results: Path,
    root: Path,
) -> None:
    """Resume BeXhoma after Kubernetes replaced its former controller Pod."""
    status_file, status = _status_for_run(run, status_directory)
    report = Path(status["results"]) / "report" / "index.md"
    if report.is_file():
        return
    provenance = status.get("provenance", {})
    catalog = provenance.get("contract_catalog.yml")
    if not catalog:
        raise ControllerError(f"benchmark {status.get('code')} has no archived catalog")

    lock_descriptor = os.open(results / _RUN_LOCK, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(lock_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        os.close(lock_descriptor)
        raise ControllerError(
            "another agent experiment holds the shared benchmark lock"
        ) from error

    log_path = Path(status["log"])
    try:
        with log_path.open("a", encoding="utf-8") as log:
            log.write("\nController Pod restarted; resuming BeXhoma orchestration.\n")
            log.flush()
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m", "agent.harness.submit",
                    status["spec"],
                    "--catalog", catalog,
                    "--experiment-code", str(status["code"]),
                ],
                cwd=root,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                pass_fds=(lock_descriptor,),
            )
    except (OSError, ValueError):
        os.close(lock_descriptor)
        raise
    os.close(lock_descriptor)
    status["pid"] = process.pid
    status["state"] = "running"
    status["resumed_after_controller_restart"] = True
    status_file.write_text(json.dumps(status, indent=2), encoding="utf-8")


def _refresh_environment(root: Path, destination: Path) -> None:
    """Capture current cluster facts before the design phase starts."""
    subprocess.run(
        [sys.executable, "-m", "bexhoma.environment", "--output", str(destination)],
        cwd=root,
        check=True,
    )


def main() -> int:
    """Prepare in-cluster state and replace this process with the lifecycle.

    :return: Zero only if process replacement unexpectedly returns.
    :rtype: int
    """
    root = Path(os.environ.get("AGENT_ROOT", _DEFAULT_ROOT)).resolve()
    state_root = Path(os.environ.get("AGENT_STATE_ROOT", _DEFAULT_STATE_ROOT)).resolve()
    input_directory = Path(
        os.environ.get("AGENT_INPUT_DIRECTORY", _DEFAULT_INPUT_DIRECTORY)
    ).resolve()
    lifecycle_id = _required_environment("AGENT_LIFECYCLE_ID")
    namespace = _required_environment("POD_NAMESPACE")
    host = _required_environment("KUBERNETES_SERVICE_HOST")
    port = os.environ.get("KUBERNETES_SERVICE_PORT_HTTPS", "443")

    lifecycle_state = state_root / "investigations" / lifecycle_id
    trajectories = lifecycle_state / "trajectories"
    statuses = lifecycle_state / "status"
    inbox = lifecycle_state / "inbox"
    results = state_root / "results"
    for directory in (trajectories, statuses, inbox, results):
        directory.mkdir(parents=True, exist_ok=True)

    kubeconfig = lifecycle_state / "kubeconfig.yml"
    _write_in_cluster_kubeconfig(kubeconfig, namespace, host, port)
    os.environ["KUBECONFIG"] = str(kubeconfig)
    os.environ["MODEL_SERVER_CONTEXT"] = _IN_CLUSTER_CONTEXT
    os.environ["MODEL_SERVER_NAMESPACE"] = namespace
    os.environ["MODEL_SERVER_IN_CLUSTER"] = "1"
    os.environ["KUBE_LOGIN_SCRIPT"] = "/bin/true"

    _write_runtime_cluster_config(
        source=input_directory / "cluster.config",
        destination=root / "cluster.config",
        namespace=namespace,
        results=results,
        source_context=os.environ.get("AGENT_SOURCE_CONTEXT") or None,
    )
    environment = lifecycle_state / "environment.yml"
    _refresh_environment(root, environment)

    command = [
        sys.executable,
        str(root / "dev" / "agent_lifecycle.py"),
        "--root", str(root),
        "--model", _required_environment("AGENT_MODEL"),
        "--base-url", os.environ.get(
            "AGENT_BASE_URL", "http://vllm-qwen38-service/v1"
        ),
        "--results", str(results),
        "--trajectories", str(trajectories),
        "--status", str(statuses),
        "--inbox", str(inbox),
        "--environment", str(environment),
        "--followups", os.environ.get("AGENT_FOLLOWUPS", "1"),
    ]
    resumable = _latest_resumable(trajectories, statuses)
    if resumable is not None:
        _resume_benchmark_orchestrator(resumable, statuses, results, root)
        command.extend(["--resume", str(resumable)])
    else:
        task_file = Path(
            os.environ.get("AGENT_TASK_FILE", input_directory / "task.txt")
        )
        task = task_file.read_text(encoding="utf-8").strip()
        if not task:
            raise ControllerError(f"benchmark question is empty in {task_file}")
        command.extend(["--task", task])

    os.environ.setdefault(
        "MODEL_SERVER_BASE_URL", "http://vllm-qwen38-service/v1"
    )
    os.execv(sys.executable, command)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ControllerError, OSError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
