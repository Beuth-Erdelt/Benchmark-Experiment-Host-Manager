"""Tests for the optional operator-side vLLM lifecycle wrapper."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from dev.agent_lifecycle import AgentLifecycle, LifecycleConfig, LifecycleError


class _Server:
    def __init__(self) -> None:
        self.actions: list[str] = []

    def switch(self, state: str) -> None:
        self.actions.append(state)


class _FlakyServer(_Server):
    def __init__(self, failed_starts: int) -> None:
        super().__init__()
        self.failed_starts = failed_starts

    def switch(self, state: str) -> None:
        super().switch(state)
        if state == "up" and self.failed_starts:
            self.failed_starts -= 1
            raise LifecycleError("no GPU capacity")


class _Lifecycle(AgentLifecycle):
    def __init__(self, *args, runs: list[Path], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.runs = runs
        self.invocations: list[tuple[str, Path | None]] = []

    def _invoke_agent(self, phase, task=None, source=None):
        self.invocations.append((phase, source))
        staged = self.runs.pop(0)
        if phase == "design":
            return staged
        if source is None:
            raise AssertionError("interpretation requires an investigation")
        with (source / "trajectory.jsonl").open("a", encoding="utf-8") as destination:
            destination.write((staged / "trajectory.jsonl").read_text(encoding="utf-8"))
        return source


def _trajectory(directory: Path, phase: str, **outcome) -> Path:
    directory.mkdir(parents=True)
    events = [
        {"type": "meta", "phase": phase},
        {"type": "outcome", **outcome},
    ]
    (directory / "trajectory.jsonl").write_text(
        "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
    (directory / "answer.md").write_text(outcome.get("summary", ""), encoding="utf-8")
    return directory


class AgentLifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.trajectories = self.root / "trajectories"
        self.results = self.root / "results"
        self.status = self.root / "status"
        for path in (self.trajectories, self.results, self.status):
            path.mkdir()
        self.config = LifecycleConfig(
            root=self.root,
            trajectories=self.trajectories,
            results=self.results,
            status=self.status,
            server_script=self.root / "server.sh",
            poll_seconds=0.001,
        )
        self.server = _Server()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _report(self, code: str) -> None:
        report = self.results / code / "report" / "index.md"
        report.parent.mkdir(parents=True)
        report.write_text("done\n", encoding="utf-8")

    def test_server_is_off_during_benchmark_and_after_final_verdict(self) -> None:
        design = _trajectory(
            self.trajectories / "1", "design", code="101", summary="submitted")
        final = _trajectory(
            self.trajectories / "2", "interpret", code=None,
            summary="final answer", phase_complete=True)
        self._report("101")
        lifecycle = _Lifecycle(
            self.config, ["agent"], self.server, runs=[design, final])

        result = lifecycle.run("question")

        self.assertEqual(result, design)
        self.assertEqual(self.server.actions, ["up", "down", "up", "down"])
        self.assertEqual(lifecycle.invocations, [("design", None), ("interpret", design)])

    def test_followup_repeats_the_off_wait_on_cycle(self) -> None:
        design = _trajectory(
            self.trajectories / "1", "design", code="101", summary="submitted")
        followup = _trajectory(
            self.trajectories / "2", "interpret", code="102",
            summary="follow-up submitted", phase_complete=True)
        final = _trajectory(
            self.trajectories / "3", "interpret", code=None,
            summary="final answer", phase_complete=True)
        self._report("101")
        self._report("102")
        lifecycle = _Lifecycle(
            self.config, ["agent"], self.server, runs=[design, followup, final])

        lifecycle.run("question")

        self.assertEqual(
            self.server.actions, ["up", "down", "up", "down", "up", "down"])
        self.assertEqual(lifecycle.invocations[-1], ("interpret", design))

    def test_resume_does_not_start_model_before_waiting_for_active_benchmark(self) -> None:
        design = _trajectory(
            self.trajectories / "1", "design", code="101", summary="submitted")
        final = _trajectory(
            self.trajectories / "2", "interpret", code=None,
            summary="final answer", phase_complete=True)
        self._report("101")
        lifecycle = _Lifecycle(
            self.config, ["agent"], self.server, runs=[final])

        lifecycle.run(None, resume=design)

        self.assertEqual(self.server.actions, ["down", "up", "down"])

    def test_failed_benchmark_still_leaves_server_down(self) -> None:
        design = _trajectory(
            self.trajectories / "1", "design", code="101", summary="submitted")
        (self.status / "101.json").write_text(
            json.dumps({"state": "failed"}), encoding="utf-8")
        lifecycle = _Lifecycle(
            self.config, ["agent"], self.server, runs=[], sleep=lambda _: None)

        with self.assertRaisesRegex(LifecycleError, "marked failed"):
            lifecycle.run(None, resume=design)

        self.assertEqual(self.server.actions, ["down", "down"])

    def test_incomplete_final_phase_is_an_error_and_cleans_up(self) -> None:
        incomplete = _trajectory(
            self.trajectories / "1", "interpret", code=None,
            summary="partial", phase_complete=False)
        lifecycle = _Lifecycle(self.config, ["agent"], self.server, runs=[])

        with self.assertRaisesRegex(LifecycleError, "neither a submitted benchmark"):
            lifecycle.run(None, resume=incomplete)

        self.assertEqual(self.server.actions, ["down"])

    def test_server_start_retries_until_shared_gpu_is_available(self) -> None:
        design = _trajectory(
            self.trajectories / "1", "design", code="101", summary="submitted")
        final = _trajectory(
            self.trajectories / "2", "interpret", code=None,
            summary="final answer", phase_complete=True)
        self._report("101")
        server = _FlakyServer(failed_starts=2)
        lifecycle = _Lifecycle(
            self.config, ["agent"], server, runs=[design, final], sleep=lambda _: None)

        lifecycle.run("question")

        self.assertEqual(
            server.actions, ["up", "up", "up", "down", "up", "down"])

    def test_finite_server_start_attempts_fail_and_clean_up(self) -> None:
        config = LifecycleConfig(
            **{
                **self.config.__dict__,
                "server_start_attempts": 2,
            }
        )
        server = _FlakyServer(failed_starts=2)
        lifecycle = _Lifecycle(
            config, ["agent"], server, runs=[], sleep=lambda _: None)

        with self.assertRaisesRegex(LifecycleError, "no GPU capacity"):
            lifecycle.run("question")

        self.assertEqual(server.actions, ["up", "up", "down"])

    def test_real_invoker_appends_interpretation_to_same_investigation(self) -> None:
        investigation = _trajectory(
            self.trajectories / "one", "design", code="101", summary="submitted"
        )
        lifecycle = AgentLifecycle(self.config, ["agent"], self.server)

        def append_phase(*args, **kwargs):
            with (investigation / "trajectory.jsonl").open("a", encoding="utf-8") as log:
                log.write(json.dumps({"type": "meta", "phase": "interpret"}) + "\n")
                log.write(json.dumps({
                    "type": "outcome", "code": None,
                    "summary": "aggregated verdict", "phase_complete": True,
                }) + "\n")
            return mock.Mock(returncode=0)

        with mock.patch("dev.agent_lifecycle.subprocess.run", side_effect=append_phase):
            result = lifecycle._invoke_agent("interpret", source=investigation)

        self.assertEqual(result, investigation)
        phases = [
            json.loads(line).get("phase")
            for line in (investigation / "trajectory.jsonl").read_text().splitlines()
            if json.loads(line).get("type") == "meta"
        ]
        self.assertEqual(phases, ["design", "interpret"])


if __name__ == "__main__":
    unittest.main()
