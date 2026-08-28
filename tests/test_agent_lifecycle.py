"""Tests for the optional operator-side vLLM lifecycle wrapper."""
from __future__ import annotations

import ast
import json
import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from agent.lifecycle_controller import (
    _events,
    _latest_resumable,
    _resume_benchmark_orchestrator,
    _write_in_cluster_kubeconfig,
    _write_runtime_cluster_config,
)
from dev.agent_lifecycle import (
    AgentLifecycle,
    LifecycleConfig,
    LifecycleError,
    ModelServer,
    _install_signal_handlers,
    _parser,
)

__all__: list[str] = []

MANIFEST = Path(__file__).parents[1] / "agent" / "k8s" / "vllm-qwen38-27b.yml"
CONTROLLER_MANIFEST = (
    Path(__file__).parents[1] / "agent" / "k8s" / "lifecycle-controller.yml"
)


def _model_pod() -> dict:
    """Return the model server Pod document from the shipped manifest."""
    documents = list(yaml.safe_load_all(MANIFEST.read_text(encoding="utf-8")))
    return next(document for document in documents if document.get("kind") == "Pod")


def _watchdog_script() -> str:
    """Return the exact watchdog function and loop embedded in the pod."""
    startup = _model_pod()["spec"]["containers"][0]["args"][0]
    return startup[startup.index("probe_activity() {"):]


def _probe_program() -> str:
    """Return the embedded Python metric parser with a local-file input."""
    startup = _model_pod()["spec"]["containers"][0]["args"][0]
    start = startup.index("import sys\n", startup.index("probe_activity()"))
    end = startup.index("\nPY\n", start)
    program = startup[start:end]
    reader_start = program.index("    with urllib.request.urlopen(")
    reader_end = program.index("except OSError", reader_start)
    file_reader = """\
    with open(sys.argv[1], "rb") as response:
        body = response.read().decode("utf-8", "replace")
"""
    return program[:reader_start] + file_reader + program[reader_end:]


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
        self.cleaned_codes: list[str] = []

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

    def _cleanup_failed_benchmark(self, code: str) -> None:
        """Record deterministic cleanup without calling a real cluster."""
        self.cleaned_codes.append(code)


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
    def test_controller_job_has_durable_state_and_retry_semantics(self) -> None:
        documents = list(yaml.safe_load_all(
            CONTROLLER_MANIFEST.read_text(encoding="utf-8")
        ))
        job = next(document for document in documents if document.get("kind") == "Job")
        pod = job["spec"]["template"]["spec"]

        self.assertEqual(pod["restartPolicy"], "OnFailure")
        self.assertEqual(pod["serviceAccountName"], "agent-lifecycle")
        self.assertNotIn("activeDeadlineSeconds", job["spec"])
        self.assertEqual(
            pod["volumes"][0]["persistentVolumeClaim"]["claimName"],
            "agent-lifecycle-state",
        )

    def test_controller_writes_rotating_in_cluster_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            account = root / "account"
            account.mkdir()
            (account / "ca.crt").write_text("certificate", encoding="utf-8")
            (account / "token").write_text("token", encoding="utf-8")
            destination = root / "kubeconfig.yml"

            _write_in_cluster_kubeconfig(
                destination, "research", "kubernetes.default.svc", "443", account
            )

            configuration = yaml.safe_load(destination.read_text(encoding="utf-8"))
            self.assertEqual(
                configuration["contexts"][0]["context"]["namespace"], "research"
            )
            self.assertEqual(
                configuration["users"][0]["user"]["tokenFile"],
                str(account / "token"),
            )

    def test_controller_injects_namespace_context_and_result_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.config"
            destination = root / "cluster.config"
            source.write_text(
                repr({
                    "benchmarker": {"resultfolder": "/old"},
                    "credentials": {"k8s": {"context": {
                        "portable": {
                            "namespace": "old",
                            "port": 9091,
                            "storage_classes": ["shared"],
                        },
                    }}},
                }),
                encoding="utf-8",
            )

            _write_runtime_cluster_config(
                source, destination, "research", root / "results", "portable"
            )

            configuration = ast.literal_eval(destination.read_text(encoding="utf-8"))
            context = configuration["credentials"]["k8s"]["context"]
            self.assertEqual(list(context), ["agent-in-cluster"])
            self.assertEqual(context["agent-in-cluster"]["namespace"], "research")
            self.assertEqual(
                configuration["benchmarker"]["resultfolder"], str(root / "results")
            )

    def test_controller_recovers_submission_recorded_before_phase_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            trajectories = root / "trajectories"
            statuses = root / "status"
            run = trajectories / "run"
            phase = run / "phases" / "01-design"
            phase.mkdir(parents=True)
            statuses.mkdir()
            (run / "trajectory.jsonl").write_text(
                json.dumps({"type": "meta", "phase": "design"}) + "\n",
                encoding="utf-8",
            )
            specification = phase / "submitted-experiment.yml"
            specification.write_text("mode: run\n", encoding="utf-8")
            (statuses / "42.json").write_text(json.dumps({
                "code": "42",
                "spec": str(specification),
            }), encoding="utf-8")

            resumable = _latest_resumable(trajectories, statuses)

            self.assertEqual(resumable, run)
            recovered = _events(run)[-1]
            self.assertEqual(recovered["code"], "42")
            self.assertTrue(recovered["recovered_after_restart"])

    def test_controller_resumes_bexhoma_with_same_code_after_pod_restart(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / "trajectories" / "run"
            phase = run / "phases" / "01-design"
            statuses = root / "status"
            results = root / "results"
            phase.mkdir(parents=True)
            statuses.mkdir()
            results.mkdir()
            specification = phase / "submitted-experiment.yml"
            catalog = phase / "submitted-contract_catalog.yml"
            log = phase / "bexhoma.log"
            specification.write_text("mode: run\n", encoding="utf-8")
            catalog.write_text("catalog_contract_version: 1.0.0\n", encoding="utf-8")
            log.write_text("first process\n", encoding="utf-8")
            (run / "trajectory.jsonl").write_text(
                json.dumps({"type": "meta", "phase": "design"}) + "\n"
                + json.dumps({"type": "outcome", "code": "42"}) + "\n",
                encoding="utf-8",
            )
            status_file = statuses / "42.json"
            status_file.write_text(json.dumps({
                "code": "42",
                "state": "running",
                "pid": 99,
                "spec": str(specification),
                "results": str(results / "42"),
                "log": str(log),
                "provenance": {"contract_catalog.yml": str(catalog)},
            }), encoding="utf-8")
            process = mock.Mock(pid=1234)

            with mock.patch(
                "agent.lifecycle_controller.subprocess.Popen", return_value=process
            ) as launch:
                _resume_benchmark_orchestrator(run, statuses, results, root)

            command = launch.call_args.args[0]
            self.assertEqual(command[-2:], ["--experiment-code", "42"])
            self.assertEqual(command[command.index("--catalog") + 1], str(catalog))
            persisted = json.loads(status_file.read_text(encoding="utf-8"))
            self.assertEqual(persisted["pid"], 1234)
            self.assertTrue(persisted["resumed_after_controller_restart"])
            self.assertIn("resuming BeXhoma", log.read_text(encoding="utf-8"))

    def test_the_handbook_is_one_switch_from_the_wrapper_to_the_agent(self) -> None:
        """The ablation needs the handbook off without editing any file."""
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AGENT_METHOD", None)
            default = _parser().parse_args(["--task", "q"])
        self.assertEqual(default.method, "agent/experiment_design_handbook.md")

        without = _parser().parse_args(["--task", "q", "--method", ""])
        self.assertEqual(without.method, "")

        with mock.patch.dict(os.environ, {"AGENT_METHOD": ""}):
            from_environment = _parser().parse_args(["--task", "q"])
        self.assertEqual(from_environment.method, "")

    def test_model_manifest_accepts_h100_or_h200(self) -> None:
        expressions = _model_pod()["spec"]["affinity"]["nodeAffinity"][
            "requiredDuringSchedulingIgnoredDuringExecution"
        ]["nodeSelectorTerms"][0]["matchExpressions"]

        self.assertIn(
            {"key": "gpu", "operator": "In", "values": ["h100", "h200"]},
            expressions,
        )

    def test_model_pod_releases_the_gpu_when_it_is_left_idle(self) -> None:
        """The GPU must come back even when no wrapper is there to hand it back."""
        pod = _model_pod()
        container = pod["spec"]["containers"][0]
        environment = {entry["name"]: entry["value"] for entry in container["env"]}

        # Always would restart the pod the moment the watchdog ended it.
        self.assertEqual(pod["spec"]["restartPolicy"], "OnFailure")
        self.assertEqual(
            pod["metadata"]["annotations"]["bexhoma.local/model-server-generation"],
            "idle-watchdog-v2",
        )
        self.assertGreater(int(environment["IDLE_SHUTDOWN_SECONDS"]), 0)
        self.assertGreater(int(environment["IDLE_POLL_SECONDS"]), 0)
        # The shell has to survive the server launch to be able to watch it.
        self.assertIn("VLLM_PID=$!", container["args"][0])

    def test_model_pod_startup_script_is_valid_shell(self) -> None:
        """This script only ever runs in-cluster, so syntax is checked here."""
        script = _model_pod()["spec"]["containers"][0]["args"][0]
        with tempfile.NamedTemporaryFile("w", suffix=".sh") as handle:
            handle.write(script)
            handle.flush()
            checked = subprocess.run(
                ["bash", "-n", handle.name], capture_output=True, text=True)

        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_exact_pod_watchdog_stops_only_after_observed_activity_goes_idle(self) -> None:
        """Exercise the shipped loop with long and between-poll request signals."""
        watchdog = _watchdog_script()
        loop = watchdog[watchdog.index("idle_seconds=0"):]
        readings = self.root / "readings.txt"
        readings.write_text("0 0.000\n1 0.000\n0 1.000\n0 1.000\n0 1.000\n")
        position = self.root / "position.txt"
        position.write_text("1\n")
        script = f"""\
set -euo pipefail
IDLE_SHUTDOWN_SECONDS=2
IDLE_POLL_SECONDS=1
SHUTDOWN_GRACE_SECONDS=1
sleep() {{ :; }}
python3 -c 'import time; time.sleep(30)' &
VLLM_PID=$!
probe_activity() {{
    position=$(cat {position})
    sed -n "${{position}}p" {readings}
    echo $((position + 1)) > {position}
}}
{loop}
"""

        result = subprocess.run(
            ["bash", "-c", script], capture_output=True, text=True, timeout=10)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreaterEqual(int(position.read_text()), 6)
        self.assertIn("releasing the GPU", result.stdout)
        self.assertIn("kill -KILL", _watchdog_script())

    def test_watchdog_fails_open_without_both_metric_classes(self) -> None:
        """Incomplete telemetry must not be treated as proof that the pod is idle."""
        metrics = self.root / "metrics.txt"
        metrics.write_text(
            'vllm:num_requests_running{model_name="test"} 0\n'
            'vllm:num_requests_waiting{model_name="test"} 0\n')

        result = subprocess.run(
            ["python3", "-c", _probe_program(), str(metrics)],
            capture_output=True, text=True, timeout=10)

        self.assertEqual(result.returncode, 1)
        self.assertIn("incomplete vLLM request metrics", result.stderr)

    def test_termination_signal_still_stops_the_model_server(self) -> None:
        """A polite kill must release the GPU, not strand it as the default would."""
        class _Signalled(_Lifecycle):
            def _invoke_agent(self, phase, task=None, source=None):
                os.kill(os.getpid(), signal.SIGTERM)
                raise AssertionError("the signal did not interrupt the phase")

        lifecycle = _Signalled(self.config, ["agent"], self.server, runs=[])
        previous = signal.getsignal(signal.SIGTERM)
        _install_signal_handlers()
        try:
            with self.assertRaisesRegex(LifecycleError, "SIGTERM"):
                lifecycle.run("question")
        finally:
            signal.signal(signal.SIGTERM, previous)

        self.assertEqual(self.server.actions, ["up", "down"])

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

    def test_an_endpoint_we_do_not_host_is_chained_without_being_switched(self) -> None:
        """A hosted API or a running Ollama needs the phase chain, not a server switch."""
        design = _trajectory(
            self.trajectories / "1", "design", code="101", summary="submitted")
        final = _trajectory(
            self.trajectories / "2", "interpret", code=None,
            summary="final answer", phase_complete=True)
        self._report("101")
        server = ModelServer(self.config.server_script, bundled=False)
        lifecycle = _Lifecycle(self.config, ["agent"], server, runs=[design, final])

        with mock.patch("dev.agent_lifecycle.subprocess.run") as run_command:
            result = lifecycle.run("question")

        self.assertEqual(result, design)
        self.assertEqual(
            lifecycle.invocations, [("design", None), ("interpret", design)])
        run_command.assert_not_called()

    def test_who_owns_the_endpoint_decides_whether_the_switch_runs(self) -> None:
        """.env chooses the backend, so it also decides whether a server is switched."""
        commands: list[list[str]] = []

        def record(command: list[str], check: bool) -> subprocess.CompletedProcess:
            commands.append(command)
            return subprocess.CompletedProcess(command, 0)

        ModelServer(self.config.server_script, run_command=record).switch("up")
        ModelServer(
            self.config.server_script, bundled=False, run_command=record).switch("up")

        self.assertEqual(
            commands, [["bash", str(self.config.server_script), "up"]])

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

    def test_result_directory_comes_from_what_the_agent_recorded(self) -> None:
        """The wrapper must not need its own copy of where results land."""
        elsewhere = self.root / "somewhere-else" / "101"
        (self.status / "101.json").write_text(
            json.dumps({"code": "101", "results": str(elsewhere)}), encoding="utf-8")
        config = LifecycleConfig(**{**self.config.__dict__, "results": None})
        lifecycle = _Lifecycle(config, ["agent"], self.server, runs=[])

        located = lifecycle._result_directory("101", self.status / "101.json")

        self.assertEqual(located, elsewhere)

    def test_result_directory_without_any_source_is_an_error(self) -> None:
        """Silence here would mean polling a path nobody ever writes to."""
        config = LifecycleConfig(**{**self.config.__dict__, "results": None})
        lifecycle = _Lifecycle(config, ["agent"], self.server, runs=[])

        with self.assertRaisesRegex(LifecycleError, "cannot locate results"):
            lifecycle._result_directory("101", self.status / "missing.json")

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
        self.assertEqual(lifecycle.cleaned_codes, ["101"])

    def test_failed_benchmark_cleanup_uses_the_exact_experiment_code(self) -> None:
        lifecycle = AgentLifecycle(self.config, ["agent"], self.server)

        with mock.patch(
            "dev.agent_lifecycle.subprocess.run",
            return_value=mock.Mock(returncode=0),
        ) as run:
            lifecycle._cleanup_failed_benchmark("101")

        run.assert_called_once_with(
            [str(Path(sys.executable).with_name("bexperiments")), "stop", "-e", "101"],
            cwd=self.root,
            check=False,
        )

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
