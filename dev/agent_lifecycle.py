#!/usr/bin/env python3
"""Run the prototype agent while lending its GPU back during benchmarks.

This is an operator-side wrapper, not part of :mod:`agent`.  It invokes the
agent's public CLI as a child process and observes only the durable investigation
trajectory and result files -- including the status file in which the agent
records where each submitted run landed, which is how the two stay agreed on
that without a second setting. Neither the agent nor a submitted experiment
imports it, so both continue to work unchanged when this module is absent.

Lifecycle:

1. start vLLM and invoke the design phase;
2. after a successful submission, stop vLLM and wait for the report on disk;
3. restart vLLM for interpretation;
4. repeat steps 2-3 for an approved follow-up; and
5. stop vLLM after the final verdict, or after any failure/interruption.

An endpoint this machine does not own -- a hosted API, or an Ollama already
running -- has nothing to start or stop, so ``AGENT_MODEL_SERVER=external`` in
:file:`.env` keeps the same phase chain and drops steps 1, 3 and 5.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from collections.abc import Callable, Sequence

from dotenv import load_dotenv

# This runs as a script (``python dev/agent_lifecycle.py``), so the repository
# root is not already importable. Add it for the one trajectory-location helper
# below, which the wrapper shares with the agent CLI so both agree on where an
# investigation lands without a second setting.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.harness.tools import default_result_root


#: How often the wait for a benchmark says that it is still waiting. A run takes
#: hours, and polling silently is indistinguishable from having died.
_WAIT_NOTICE_SECONDS = 600.0

#: How much of a refusal, or of the agent's own account, a failure message keeps.
_REASON_CHARS = 400

#: Validation calls passed to each design and follow-up authoring phase.
_DEFAULT_ATTEMPTS = 3

#: Subdirectory of Bexhoma's result folder that holds investigation
#: trajectories when ``--trajectories`` is not given, matching the agent CLI's
#: own default.
_TRAJECTORY_SUBDIR = "agent"

#: The only two answers to who owns the model endpoint. ``bundled`` is started
#: and stopped by this wrapper; ``external`` is already running.
_BUNDLED_SERVER = "bundled"
_SERVER_OWNERS = frozenset({_BUNDLED_SERVER, "external"})

#: Runs Bexhoma's experiment manager (the ``bexperiments`` console script) with
#: ``python -c`` rather than by locating the installed wrapper, whose name and
#: directory differ between POSIX and Windows.
_MANAGER_ENTRY = "from bexhoma.scripts.experimentsmanager import manage; manage()"


class LifecycleError(RuntimeError):
    """Raised when an agent phase or benchmark cannot complete."""


@dataclass(frozen=True)
class LifecycleConfig:
    """Paths and timing used by :class:`AgentLifecycle`."""

    root: Path
    trajectories: Path
    status: Path
    server_script: Path
    #: Only set when an operator overrode it; otherwise each run's directory is
    #: read from the status file the agent wrote at submission.
    results: Path | None = None
    poll_seconds: float = 30.0
    benchmark_timeout_seconds: float = 0.0
    server_retry_seconds: float = 60.0
    server_start_attempts: int = 0


class ModelServer:
    """Small adapter around the independently usable server switch.

    ``bundled`` says who owns the endpoint. The vLLM server in
    :file:`dev/model_server.sh`, or its PowerShell port
    :file:`dev/model_server.ps1` on Windows, is this wrapper's to start and
    stop; a hosted API or an Ollama that is already running answers on its
    own, so switching it does nothing and the phase chain is all that is left
    to do.
    """

    def __init__(
        self,
        script: Path,
        bundled: bool = True,
        run_command: Callable[..., subprocess.CompletedProcess[Any]] = subprocess.run,
    ) -> None:
        self.script = script
        self.bundled = bundled
        self._run_command = run_command

    def _command(self, state: str) -> list[str]:
        """Return the interpreter and switch-script call for this platform.

        The switch ships as a POSIX shell script and a PowerShell port with
        the same behaviour. A Windows workstation has no ``bash`` but always
        has ``powershell``, so the interpreter follows the script's suffix
        rather than being fixed.

        :param state: ``up`` or ``down``.
        :return: the argument vector for :func:`subprocess.run`.
        :rtype: list[str]
        """
        if self.script.suffix == ".ps1":
            return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", str(self.script), state]
        return ["bash", str(self.script), state]

    def switch(self, state: str) -> None:
        """Bring the server ``up`` or ``down``, failing on operator errors."""
        if state not in {"up", "down"}:
            raise ValueError(f"unsupported model-server state: {state}")
        if not self.bundled:
            return
        result = self._run_command(self._command(state), check=False)
        if result.returncode:
            raise LifecycleError(
                f"model-server command {state!r} failed with exit code {result.returncode}"
            )


class AgentLifecycle:
    """Coordinate server availability around otherwise unchanged agent runs."""

    def __init__(
        self,
        config: LifecycleConfig,
        agent_command: Sequence[str],
        server: ModelServer,
        sleep: Callable[[float], None] = time.sleep,
        interpret_model: str | None = None,
    ) -> None:
        self.config = config
        self.agent_command = list(agent_command)
        self.server = server
        self._sleep = sleep
        self.interpret_model = interpret_model

    def run(self, task: str | None, resume: Path | None = None) -> Path:
        """Run through the final verdict and return its investigation directory.

        ``resume`` may identify an investigation with a successfully submitted
        design or follow-up. This makes the wrapper restartable without re-submitting an
        experiment after a terminal disconnect.
        """
        current: Path | None = None
        try:
            if resume is None:
                if not task:
                    raise LifecycleError("a task is required when not resuming a run")
                self._start_server()
                current = self._invoke_agent("design", task=task)
            else:
                current = resume.resolve()
                self._read_phase_state(current)

            while True:
                phase, outcome = self._read_phase_state(current)
                code = outcome.get("code")
                if code:
                    # Submission may return while the exact result directory is
                    # still starting, but the assigned code is already durable.
                    self.server.switch("down")
                    report = self._wait_for_report(str(code))
                    print(f"benchmark {code} finished: {report}", flush=True)
                    self._start_server()
                    current = self._invoke_agent("interpret", source=current)
                    continue

                if self._is_final(phase, outcome):
                    return current
                raise LifecycleError(
                    f"agent {phase} phase produced neither a submitted benchmark "
                    "nor a complete final verdict"
                )
        finally:
            # Resource safety wins even when the model, benchmark, login, or the
            # wrapper itself fails. down is idempotent and preserves the PVC.
            primary_error = sys.exc_info()[0] is not None
            try:
                self.server.switch("down")
            except Exception as error:
                if not primary_error:
                    raise
                print(f"warning: could not stop model server during cleanup: {error}",
                      file=sys.stderr)

    def _start_server(self) -> None:
        """Start the model server, retrying while shared GPU capacity is unavailable."""
        attempt = 0
        while True:
            attempt += 1
            try:
                self.server.switch("up")
                return
            except LifecycleError as error:
                if (
                    self.config.server_start_attempts > 0
                    and attempt >= self.config.server_start_attempts
                ):
                    raise
                print(
                    f"warning: model server start attempt {attempt} failed: {error}; "
                    f"retrying in {self.config.server_retry_seconds:g}s",
                    file=sys.stderr,
                    flush=True,
                )
                self._sleep(self.config.server_retry_seconds)

    def _invoke_agent(
        self, phase: str, task: str | None = None, source: Path | None = None,
    ) -> Path:
        before = set(self._trajectory_runs())
        command = [*self.agent_command, "--phase", phase]
        if phase == "design":
            command.extend(["--task", task or ""])
        else:
            if source is None:
                raise LifecycleError("interpretation needs the current investigation")
            command.extend(["--run", str(source)])
            if self.interpret_model:
                # Judging a finished result is harder than designing one, so the
                # verdict may run on a stronger model. argparse keeps the last
                # --model it parses, so this overrides the base command's.
                command.extend(["--model", self.interpret_model])

        print(f"starting the {phase} phase", flush=True)
        log = source / "trajectory.jsonl" if source is not None else None
        previous_size = log.stat().st_size if log is not None and log.is_file() else None
        result = subprocess.run(command, cwd=self.config.root, check=False)
        if phase == "design":
            created = sorted(set(self._trajectory_runs()) - before)
            if not created:
                raise LifecycleError(
                    f"agent design phase created no investigation "
                    f"(exit code {result.returncode})"
                )
            investigation = created[-1]
        else:
            if source is None:
                raise LifecycleError("interpretation needs an investigation")
            investigation = source.resolve()
            current_log = investigation / "trajectory.jsonl"
            if (
                previous_size is None
                or not current_log.is_file()
                or current_log.stat().st_size <= previous_size
            ):
                raise LifecycleError(
                    f"agent interpret phase did not append to {current_log} "
                    f"(exit code {result.returncode})"
                )
        if result.returncode:
            raise LifecycleError(
                f"agent {phase} phase failed with exit code {result.returncode}; "
                f"investigation: {investigation}"
                f"{_failure_reason(investigation)}"
            )
        return investigation

    def _trajectory_runs(self) -> list[Path]:
        if not self.config.trajectories.is_dir():
            return []
        return [
            path.resolve() for path in self.config.trajectories.iterdir()
            if path.is_dir() and (path / "trajectory.jsonl").is_file()
        ]

    def _read_phase_state(self, run: Path) -> tuple[str, dict[str, Any]]:
        log = run / "trajectory.jsonl"
        if not log.is_file():
            raise LifecycleError(f"trajectory log not found: {log}")
        phase: str | None = None
        outcome: dict[str, Any] | None = None
        for line in log.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            if event.get("type") == "meta" and event.get("phase"):
                phase = str(event["phase"])
            elif event.get("type") == "outcome":
                outcome = event
        if phase not in {"design", "interpret"} or outcome is None:
            raise LifecycleError(f"trajectory has no complete phase outcome: {log}")
        return phase, outcome

    def _is_final(self, phase: str, outcome: dict[str, Any]) -> bool:
        if phase == "interpret":
            return outcome.get("phase_complete") is True
        # Only a dry run ends at design: it validates and stops, with no
        # benchmark to wait for. Any other design that reaches here submitted
        # nothing -- it ran out of validation attempts or turns -- and saying
        # "final verdict" of it would name an answer file that was never written.
        return "--dry-run" in self.agent_command and bool(outcome.get("summary"))

    def _result_directory(self, code: str, status_file: Path) -> Path:
        """Return where a submitted benchmark is writing its results.

        Read from the status file the agent wrote at submission, so the wrapper
        cannot disagree with the agent about where a run landed. ``--results``
        remains a fallback for a status file written before that field existed.

        :param code: Experiment code of the submitted benchmark.
        :param status_file: The agent's status file for that code.
        :return: The run's result directory.
        :rtype: Path
        :raises LifecycleError: When neither source can name the directory.
        """
        if status_file.is_file():
            recorded = json.loads(status_file.read_text(encoding="utf-8")).get("results")
            if recorded:
                return Path(recorded)
        if self.config.results is None:
            raise LifecycleError(
                f"cannot locate results for benchmark {code}: no directory recorded "
                f"in {status_file}, and no --results given"
            )
        return self.config.results / code

    def _wait_for_report(self, code: str) -> Path:
        status_file = self.config.status / f"{code}.json"
        report = self._result_directory(code, status_file) / "report" / "index.md"
        deadline = (
            time.monotonic() + self.config.benchmark_timeout_seconds
            if self.config.benchmark_timeout_seconds > 0 else None
        )
        # The switch script announces the shutdown itself when there is one.
        print(f"waiting for benchmark {code}", flush=True)
        started = time.monotonic()
        next_notice = started + _WAIT_NOTICE_SECONDS
        while not report.is_file():
            if time.monotonic() >= next_notice:
                minutes = (time.monotonic() - started) / 60
                print(f"benchmark {code} still running after {minutes:.0f} min",
                      flush=True)
                next_notice += _WAIT_NOTICE_SECONDS
            if status_file.is_file():
                status = json.loads(status_file.read_text(encoding="utf-8"))
                if status.get("state") == "failed":
                    self._cleanup_failed_benchmark(code)
                    raise LifecycleError(f"benchmark {code} is marked failed")
                pid = status.get("pid")
                if isinstance(pid, int) and pid > 0 and not _pid_alive(pid):
                    self._cleanup_failed_benchmark(code)
                    raise LifecycleError(
                        f"benchmark {code} process {pid} exited before producing {report}"
                    )
            if deadline is not None and time.monotonic() >= deadline:
                raise LifecycleError(f"timed out waiting for benchmark {code}: {report}")
            self._sleep(self.config.poll_seconds)
        return report

    def _cleanup_failed_benchmark(self, code: str) -> None:
        """Remove live Kubernetes objects for one definitively failed run."""
        print(f"benchmark {code} failed; removing its cluster resources", flush=True)
        result = subprocess.run(
            [sys.executable, "-c", _MANAGER_ENTRY, "stop", "-e", code],
            cwd=self.config.root,
            check=False,
        )
        if result.returncode:
            print(
                f"warning: cleanup for benchmark {code} exited with "
                f"status {result.returncode}",
                file=sys.stderr,
            )


def _failure_reason(run: Path) -> str:
    """Read from the trajectory why a phase stopped, to report it where it failed.

    The agent explains itself on the way out, but that scrolls past during a long
    run, and an exit code and a directory tell an operator nothing about why a
    question could not be answered. The refusal that ended the attempt and the
    agent's own closing account are both durable, so they are repeated here.

    :param run: Investigation directory of the phase that failed.
    :return: Indented lines to append to the error message, empty when the
        trajectory says nothing useful.
    :rtype: str
    """
    log = run / "trajectory.jsonl"
    if not log.is_file():
        return ""
    refusal = ""
    summary = ""
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            # A killed process can leave its last line half written.
            continue
        if event.get("type") == "tool_call":
            result = event.get("result") or {}
            refusals = result.get("errors") or []
            if refusals:
                refusal = str(refusals[0].get("message", "")).strip()
            elif result.get("error"):
                refusal = str(result["error"]).strip()
        elif event.get("type") == "outcome":
            summary = str(event.get("summary") or "").strip()
    parts = []
    if refusal:
        parts.append(f"last refusal: {refusal[:_REASON_CHARS]}")
    if summary:
        parts.append(f"the agent reported: {summary[:_REASON_CHARS]}")
    return "".join(f"\n  {part}" for part in parts)


def _pid_alive(pid: int) -> bool:
    """Report whether a process ID is currently running.

    ``os.kill(pid, 0)`` is a POSIX liveness probe; on Windows signal 0 instead
    triggers a console-control event, so that platform is probed through the
    Win32 API directly.

    :param pid: Process ID to probe.
    :return: ``True`` if the process exists (including when its liveness
        cannot be determined because it belongs to another user), ``False``
        otherwise.
    :rtype: bool
    """
    if os.name == "nt":
        import ctypes
        process_query_limited_information = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(
            process_query_limited_information, False, pid
        )
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _raise_on_signal(number: int, _frame: Any) -> None:
    """Turn a termination signal into the exception the cleanup path expects.

    :param number: Signal number delivered to this process.
    :param _frame: Interrupted stack frame, unused.
    :raises LifecycleError: Always, so that :meth:`AgentLifecycle.run` stops the
        model server on its way out.
    """
    raise LifecycleError(f"received {signal.Signals(number).name}")


def _install_signal_handlers() -> None:
    """Make polite termination and terminal hangup run the cleanup path.

    Python's defaults end the process outright, which would leave the GPU held
    by a server nobody is going to use. Raising instead unwinds through
    ``subprocess.run``, which kills the agent child, and then through the
    ``finally`` block that shuts the server down.
    """
    for name in ("SIGTERM", "SIGHUP"):
        number = getattr(signal, name, None)
        if number is not None:
            signal.signal(number, _raise_on_signal)


def _path_from_root(root: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the agent with vLLM off while submitted benchmarks execute.")
    start = parser.add_mutually_exclusive_group(required=True)
    start.add_argument("--task", help="question for a new design run")
    start.add_argument("--resume", help="submitted investigation to resume")
    parser.add_argument("--model", default=os.environ.get("AGENT_MODEL"))
    parser.add_argument("--interpret-model",
                        default=os.environ.get("AGENT_INTERPRET_MODEL"),
                        help="model for the interpretation phase; defaults to "
                             "--model, so the verdict can run on a stronger "
                             "model than the design")
    parser.add_argument("--base-url", default=os.environ.get(
        "AGENT_BASE_URL", "http://localhost:8001/v1"))
    parser.add_argument("--api-key", default=os.environ.get("AGENT_API_KEY", "EMPTY"))
    parser.add_argument("--root", default=os.getcwd())
    parser.add_argument("--results", default=os.environ.get("AGENT_RESULTS"),
                        help="bexhoma's result folder; defaults to the resultfolder "
                             "declared in cluster.config")
    parser.add_argument("--trajectories", default=None,
                        help="directory holding investigation trajectories; "
                             "defaults to the 'agent' subdirectory of the "
                             "result folder declared in cluster.config")
    parser.add_argument("--status", default="status")
    parser.add_argument(
        "--server-script",
        default="dev/model_server.ps1" if sys.platform == "win32"
        else "dev/model_server.sh",
    )
    parser.add_argument("--poll-seconds", type=float, default=30.0)
    parser.add_argument("--benchmark-timeout-seconds", type=float, default=0.0,
                        help="zero waits indefinitely")
    parser.add_argument("--server-retry-seconds", type=float, default=60.0)
    parser.add_argument(
        "--server-start-attempts", type=int, default=0,
        help="model-server start attempts; zero retries until capacity returns",
    )
    parser.add_argument("--attempts", type=int, default=_DEFAULT_ATTEMPTS)
    parser.add_argument("--followups", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=16384)
    parser.add_argument("--catalog", default="contracts/contract_catalog.yml")
    parser.add_argument("--environment", default="dev/catalog/environment.yml")
    parser.add_argument("--method",
                        default=os.environ.get(
                            "AGENT_METHOD", "agent/experiment_design_handbook.md"),
                        help="experiment design handbook; set AGENT_METHOD empty, or "
                             "pass an empty string, to design without one")
    parser.add_argument("--inbox", default="inbox")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    # Same .env as the agent CLI reads, so the wrapper and its child phase agree
    # on which model server is meant without exporting anything by hand.
    load_dotenv()
    _install_signal_handlers()
    args = _parser().parse_args()
    if not args.model:
        print("error: no model given; pass --model or set AGENT_MODEL", file=sys.stderr)
        return 2
    if (
        args.poll_seconds <= 0
        or args.benchmark_timeout_seconds < 0
        or args.server_retry_seconds <= 0
        or args.server_start_attempts < 0
    ):
        print(
            "error: polling/retry intervals must be positive and "
            "timeouts/attempts cannot be negative",
            file=sys.stderr,
        )
        return 2

    root = Path(args.root).resolve()
    # Checked here as well as in the phase itself, so a mistyped handbook path
    # is reported before a model server is started for a run that cannot use it.
    if args.method and not _path_from_root(root, args.method).is_file():
        print(f"error: no experiment design handbook at "
              f"{_path_from_root(root, args.method)}. Pass an existing --method, "
              "or an empty one (set AGENT_METHOD empty) to design without a "
              "handbook.", file=sys.stderr)
        return 2

    results = Path(args.results).resolve() if args.results else None
    if args.trajectories:
        trajectories = _path_from_root(root, args.trajectories)
    else:
        result_root = results or default_result_root(root)
        if result_root is None:
            print("error: no result folder. Bexhoma reads one from cluster.config "
                  "(cp k8s-cluster.config cluster.config), or pass --results, set "
                  "AGENT_RESULTS, or pass --trajectories", file=sys.stderr)
            return 2
        trajectories = result_root / _TRAJECTORY_SUBDIR

    config = LifecycleConfig(
        root=root,
        trajectories=trajectories,
        results=results,
        status=_path_from_root(root, args.status),
        server_script=_path_from_root(root, args.server_script),
        poll_seconds=args.poll_seconds,
        benchmark_timeout_seconds=args.benchmark_timeout_seconds,
        server_retry_seconds=args.server_retry_seconds,
        server_start_attempts=args.server_start_attempts,
    )
    # Keep credentials out of the child process command line, where tools such
    # as ps expose them. The agent already reads this inherited environment
    # variable, including when --api-key supplied the wrapper's override.
    os.environ["AGENT_API_KEY"] = args.api_key
    agent_command = [
        sys.executable, "-m", "agent.harness.agent",
        "--model", args.model,
        "--base-url", args.base_url,
        "--root", str(root),
        "--trajectories", str(config.trajectories),
        "--status", str(config.status),
        "--attempts", str(args.attempts),
        "--followups", str(args.followups),
        "--temperature", str(args.temperature),
        "--max-tokens", str(args.max_tokens),
        "--catalog", args.catalog,
        "--environment", args.environment,
        # Forwarded even when empty: an empty value is how a run is asked to
        # design without the handbook, which is what the ablation compares.
        "--method", args.method,
        "--inbox", args.inbox,
    ]
    # Only forwarded when the operator overrode it; otherwise the agent reads
    # the result folder from Bexhoma's own configuration.
    if config.results is not None:
        agent_command.extend(["--results", str(config.results)])
    if args.dry_run:
        agent_command.append("--dry-run")

    # .env says who owns the endpoint: bundled means the vLLM server is started
    # and stopped here, external means it is already running and is left alone.
    # Anything else is a typo, and guessing at one would quietly change which
    # lifecycle a run gets.
    owner = os.environ.get("AGENT_MODEL_SERVER", _BUNDLED_SERVER)
    if owner not in _SERVER_OWNERS:
        print(
            f"error: AGENT_MODEL_SERVER is {owner!r}; it must be "
            f"{' or '.join(sorted(_SERVER_OWNERS))}",
            file=sys.stderr,
        )
        return 2
    bundled = owner == _BUNDLED_SERVER
    lifecycle = AgentLifecycle(
        config, agent_command, ModelServer(config.server_script, bundled),
        interpret_model=args.interpret_model)
    try:
        final_run = lifecycle.run(
            task=args.task,
            resume=_path_from_root(root, args.resume) if args.resume else None,
        )
    except (LifecycleError, KeyboardInterrupt) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    answer = final_run / "answer.md"
    print(f"final verdict: {answer}")
    if bundled:
        print("model server is down")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
