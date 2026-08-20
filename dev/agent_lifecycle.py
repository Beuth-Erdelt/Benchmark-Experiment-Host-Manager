#!/usr/bin/env python3
"""Run the prototype agent while lending its GPU back during benchmarks.

This is an operator-side wrapper, not part of :mod:`agent`.  It invokes the
agent's public CLI as a child process and observes only the durable investigation
trajectory and result files. Neither the agent nor a submitted experiment
imports it, so both continue to work unchanged when this module is absent.

Lifecycle:

1. start vLLM and invoke the design phase;
2. after a successful submission, stop vLLM and wait for the report on disk;
3. restart vLLM for interpretation;
4. repeat steps 2-3 for an approved follow-up; and
5. stop vLLM after the final verdict, or after any failure/interruption.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence


class LifecycleError(RuntimeError):
    """Raised when an agent phase or benchmark cannot complete."""


@dataclass(frozen=True)
class LifecycleConfig:
    """Paths and timing used by :class:`AgentLifecycle`."""

    root: Path
    trajectories: Path
    results: Path
    status: Path
    server_script: Path
    poll_seconds: float = 30.0
    benchmark_timeout_seconds: float = 0.0
    server_retry_seconds: float = 60.0
    server_start_attempts: int = 0


class ModelServer:
    """Small adapter around the independently usable server switch."""

    def __init__(
        self,
        script: Path,
        run_command: Callable[..., subprocess.CompletedProcess[Any]] = subprocess.run,
    ) -> None:
        self.script = script
        self._run_command = run_command

    def switch(self, state: str) -> None:
        """Bring the server ``up`` or ``down``, failing on operator errors."""
        if state not in {"up", "down"}:
            raise ValueError(f"unsupported model-server state: {state}")
        result = self._run_command(["bash", str(self.script), state], check=False)
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
    ) -> None:
        self.config = config
        self.agent_command = list(agent_command)
        self.server = server
        self._sleep = sleep

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
                    # Submission waits until the exact result directory exists,
                    # so reaching this point means the benchmark is running.
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

    @staticmethod
    def _is_final(phase: str, outcome: dict[str, Any]) -> bool:
        if phase == "interpret":
            return outcome.get("phase_complete") is True
        # A dry-run design is complete without a submission and has no benchmark
        # to wait for. Normal design completion always has a code.
        return bool(outcome.get("summary")) and outcome.get("code") is None

    def _wait_for_report(self, code: str) -> Path:
        report = self.config.results / code / "report" / "index.md"
        status_file = self.config.status / f"{code}.json"
        deadline = (
            time.monotonic() + self.config.benchmark_timeout_seconds
            if self.config.benchmark_timeout_seconds > 0 else None
        )
        print(f"model server down; waiting for benchmark {code}", flush=True)
        while not report.is_file():
            if status_file.is_file():
                status = json.loads(status_file.read_text(encoding="utf-8"))
                if status.get("state") == "failed":
                    raise LifecycleError(f"benchmark {code} is marked failed")
                pid = status.get("pid")
                if isinstance(pid, int) and pid > 0 and not _pid_alive(pid):
                    raise LifecycleError(
                        f"benchmark {code} process {pid} exited before producing {report}"
                    )
            if deadline is not None and time.monotonic() >= deadline:
                raise LifecycleError(f"timed out waiting for benchmark {code}: {report}")
            self._sleep(self.config.poll_seconds)
        return report


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


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
    parser.add_argument("--base-url", default=os.environ.get(
        "AGENT_BASE_URL", "http://localhost:8001/v1"))
    parser.add_argument("--api-key", default=os.environ.get("AGENT_API_KEY", "EMPTY"))
    parser.add_argument("--root", default=os.getcwd())
    parser.add_argument("--results", default=os.environ.get(
        "AGENT_RESULTS", "/home/ll/benchmarks"))
    parser.add_argument("--trajectories", default="agent/trajectories")
    parser.add_argument("--status", default="status")
    parser.add_argument("--server-script", default="dev/model_server.sh")
    parser.add_argument("--poll-seconds", type=float, default=30.0)
    parser.add_argument("--benchmark-timeout-seconds", type=float, default=0.0,
                        help="zero waits indefinitely")
    parser.add_argument("--server-retry-seconds", type=float, default=60.0)
    parser.add_argument(
        "--server-start-attempts", type=int, default=0,
        help="model-server start attempts; zero retries until capacity returns",
    )
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--followups", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=16384)
    parser.add_argument("--catalog", default="contracts/contract_catalog.yml")
    parser.add_argument("--environment", default="dev/catalog/environment.yml")
    parser.add_argument("--inbox", default="inbox")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
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
    config = LifecycleConfig(
        root=root,
        trajectories=_path_from_root(root, args.trajectories),
        results=Path(args.results).resolve(),
        status=_path_from_root(root, args.status),
        server_script=_path_from_root(root, args.server_script),
        poll_seconds=args.poll_seconds,
        benchmark_timeout_seconds=args.benchmark_timeout_seconds,
        server_retry_seconds=args.server_retry_seconds,
        server_start_attempts=args.server_start_attempts,
    )
    agent_command = [
        sys.executable, "-m", "agent.harness.agent",
        "--model", args.model,
        "--base-url", args.base_url,
        "--api-key", args.api_key,
        "--root", str(root),
        "--results", str(config.results),
        "--trajectories", str(config.trajectories),
        "--attempts", str(args.attempts),
        "--followups", str(args.followups),
        "--temperature", str(args.temperature),
        "--max-tokens", str(args.max_tokens),
        "--catalog", args.catalog,
        "--environment", args.environment,
        "--inbox", args.inbox,
    ]
    if args.dry_run:
        agent_command.append("--dry-run")

    lifecycle = AgentLifecycle(config, agent_command, ModelServer(config.server_script))
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
    print("model server is down")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
