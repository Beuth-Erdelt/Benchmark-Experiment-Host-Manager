"""Focused tests for the agent's validation and submission boundary."""
from __future__ import annotations

import fcntl
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from agent.harness import prompts, submit as submit_adapter
from agent.harness.agent import (
    Trajectory,
    _carry_forward,
    _phase_number,
    _write_reports,
    main as agent_main,
    run_interpret,
)
from agent.harness.model_client import ChatModel, Reply, ToolCall
from agent.harness.tools import (
    FOLLOWUP_AUTHOR_TOOLS,
    FOLLOWUP_DECISION_TOOLS,
    INTERPRET_TOOLS,
    Workspace,
)


_SPEC = """\
mode: run
title: comparison
hypothesis: one system is faster under concurrency
discriminates: [system, concurrency]
workload:
  name: tpch
  params: {scaling_factor: 1, active_queries: [5]}
  rounds: [1, 2]
  repetitions: 3
systems:
  - {name: PostgreSQL, profile: analytical-ssd}
  - {name: PgDuckDB, profile: analytical-ssd}
resources:
  cpu: {request: 4, limit: 4}
  memory: {request: 8Gi, limit: 8Gi}
  storage: {size: 10Gi}
"""


class _Process:
    pid = 4242

    def poll(self):
        return None


class _Model:
    model = "fake"
    temperature = 0.0
    max_tokens = 1000

    def __init__(self, replies: list[Reply]) -> None:
        self.replies = replies
        self.tool_sets: list[set[str]] = []

    def reply(self, _messages, tools=None):
        self.tool_sets.append({tool["function"]["name"] for tool in (tools or [])})
        return self.replies.pop(0)


def _tool_reply(*calls: ToolCall) -> Reply:
    return Reply("", "", list(calls), {"role": "assistant", "content": ""}, {})


def _text_reply(text: str) -> Reply:
    return Reply(text, "", [], {"role": "assistant", "content": text}, {})


class WorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "contracts").mkdir()
        (self.root / "results").mkdir()
        self.run = self.root / "trajectory"
        self.run.mkdir()
        for name in ("contract_catalog.yml", "contract_result.yml"):
            shutil.copyfile(Path("contracts") / name, self.root / "contracts" / name)
        self.workspace = Workspace(
            root=str(self.root), inbox="inbox",
            catalog_path="contracts/contract_catalog.yml",
            results_root=str(self.root / "results"), run_directory=self.run,
        )
        self.path = "inbox/followup.yml"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _validate(self) -> None:
        self.workspace.write_file(self.path, _SPEC)
        self.assertTrue(self.workspace.validate(self.path)["valid"])

    def test_submit_requires_unchanged_validated_bytes(self) -> None:
        self._validate()
        self.workspace.write_file(self.path, _SPEC + "# changed\n")
        self.assertIn("changed since validate", self.workspace.call("submit", {"path": self.path})["error"])

    def test_submit_is_bound_to_the_validated_contract(self) -> None:
        self._validate()
        catalog = self.root / "contracts" / "contract_catalog.yml"
        catalog.write_text(catalog.read_text() + "\n# changed\n")
        self.assertIn("validation inputs changed", self.workspace.call("submit", {"path": self.path})["error"])

    def test_an_oversized_file_is_cut_and_says_so(self) -> None:
        # bexhoma's report pages run to hundreds of thousands of tokens, so a
        # whole-file read would end the run with a context-length error.
        path = self.root / "results" / "big.log"
        path.write_text("x" * 40_000)
        result = self.workspace.read_file(str(path))
        self.assertEqual(result["bytes"], 40_000)
        self.assertEqual(len(result["text"]), 24_000)
        self.assertIn("only the first", result["truncated"])

    def test_a_small_file_is_returned_whole(self) -> None:
        self.workspace.write_file(self.path, _SPEC)
        result = self.workspace.read_file(self.path)
        self.assertEqual(result["text"], _SPEC)
        self.assertNotIn("truncated", result)

    def test_a_markdown_section_past_the_file_limit_is_addressable(self) -> None:
        text = "# Front\n" + "x" * 30_000 + "\n### Errors\nimportant evidence\n### Provenance\nlinks\n"
        path = self.root / "results" / "report.md"
        path.write_text(text)
        self.assertIn("request a section", self.workspace.read_file(str(path))["error"])
        result = self.workspace.read_file(str(path), "### Errors")
        self.assertEqual(result["text"], "### Errors\nimportant evidence\n")

    def test_a_long_markdown_section_can_be_continued(self) -> None:
        section = "### Latency\n" + "x" * 14_000 + "\n"
        path = self.root / "results" / "report.md"
        path.write_text("# Report\n" + section + "### Provenance\nlinks\n")

        first = self.workspace.read_file(str(path), "### Latency")
        self.assertEqual(first["next_offset"], 12_000)
        self.assertIn("Continue with offset=12000", first["truncated"])
        second = self.workspace.read_file(
            str(path), "### Latency", first["next_offset"]
        )

        self.assertEqual(first["text"] + second["text"], section)
        self.assertNotIn("truncated", second)

    def test_read_offset_requires_a_section_and_valid_range(self) -> None:
        path = self.root / "results" / "report.md"
        path.write_text("### Evidence\nshort\n")
        self.assertIn("together with", self.workspace.read_file(str(path), offset=1)["error"])
        self.assertIn(
            "past the selected section",
            self.workspace.read_file(str(path), "### Evidence", 10_000)["error"],
        )

    def test_query_latency_comparison_uses_phase_means_then_run_medians(self) -> None:
        header = (
            "| Queries | PgDuckDB-1-1-1-1-1 | PgDuckDB-1-1-2-1-1 | "
            "PgDuckDB-1-1-2-1-2 | PgDuckDB-1-2-1-1-1 | "
            "PgDuckDB-1-2-2-1-1 | PgDuckDB-1-2-2-1-2 |\n"
            "|:--|--:|--:|--:|--:|--:|--:|\n"
        )
        left = self.root / "results" / "left.md"
        right = self.root / "results" / "right.md"
        left.write_text(
            "### Latency of Timer Execution [ms]\n" + header
            + "| First (TPC-H Q1) | 10 | 20 | 24 | 14 | 30 | 34 |\n"
            + "| Second (TPC-H Q2) | 40 | 50 | 54 | 44 | 60 | 64 |\n"
        )
        right.write_text(
            "### Latency of Timer Execution [ms]\n" + header
            + "| First (TPC-H Q1) | 5 | 10 | 14 | 7 | 20 | 24 |\n"
            + "| Second (TPC-H Q2) | 80 | 90 | 94 | 84 | 100 | 104 |\n"
        )

        result = self.workspace.compare_query_latency(
            str(left), str(right), "forced", "default"
        )

        self.assertEqual(
            result["winner_counts"]["1"]["default_faster_queries"], ["Q1"]
        )
        self.assertEqual(
            result["winner_counts"]["1"]["forced_faster_queries"], ["Q2"]
        )
        q1_client2 = next(
            row for row in result["queries"]
            if row["query"] == "Q1" and row["client"] == 2
        )
        self.assertEqual(q1_client2["forced_median_ms"], 27.0)
        self.assertEqual(q1_client2["default_median_ms"], 17.0)
        self.assertEqual(q1_client2["parallel_connections"], 2)

    def test_file_reads_have_a_cumulative_context_limit(self) -> None:
        path = self.root / "results" / "big.log"
        path.write_text("x" * 40_000)
        for _ in range(3):
            self.assertIn("text", self.workspace.read_file(str(path)))
        last = self.workspace.read_file(str(path))
        self.assertEqual(last["returned_characters"], 8_000)
        self.assertIn("budget is exhausted", self.workspace.read_file(str(path))["error"])

    def test_a_fresh_model_context_resets_only_the_read_allowance(self) -> None:
        path = self.root / "results" / "big.log"
        path.write_text("x" * 40_000)
        for _ in range(3):
            self.workspace.read_file(str(path))
        self.workspace.reset_read_context()
        result = self.workspace.read_file(str(path))
        self.assertEqual(result["returned_characters"], 24_000)
        self.assertEqual(result["context_characters_remaining"], 56_000)

    def test_yaml_does_not_accept_markdown_sections(self) -> None:
        self.workspace.write_file(self.path, "# Comment\nvalue: true\n")
        result = self.workspace.read_file(self.path, "# Comment")
        self.assertIn("only supported for Markdown", result["error"])

    def test_authoritative_files_are_whole_or_error(self) -> None:
        catalog = self.root / "contracts" / "contract_catalog.yml"
        catalog.write_text(catalog.read_text() + "\n# growth\n" + "x" * 2_000)
        result = self.workspace.read_file("contracts/contract_catalog.yml")
        self.assertEqual(len(result["text"]), len(catalog.read_text()))
        self.assertNotIn("truncated", result)

        catalog.write_text("x" * 49_000)
        result = self.workspace.read_file("contracts/contract_catalog.yml")
        self.assertIn("whole-file limit", result["error"])
        self.assertNotIn("text", result)

    def test_invalid_shapes_return_verdicts(self) -> None:
        self.workspace.write_file(self.path, "hello\n")
        self.assertFalse(self.workspace.validate(self.path)["valid"])
        self.workspace.write_file(self.path, _SPEC + "invented: true\n")
        result = self.workspace.validate(self.path)
        self.assertFalse(result["valid"])
        self.assertIn("unknown field", result["errors"][0]["message"])

    def test_resource_sweep_must_be_declared_as_a_factor(self) -> None:
        sweep = _SPEC.replace(
            "memory: {request: 8Gi, limit: 8Gi}",
            "memory:\n    - {request: 4Gi, limit: 4Gi}\n    - {request: 8Gi, limit: 8Gi}",
        )
        self.workspace.write_file(self.path, sweep)
        self.assertFalse(self.workspace.validate(self.path)["valid"])
        sweep = sweep.replace("[system, concurrency]", "[system, concurrency, memory]")
        self.workspace.write_file(self.path, sweep)
        result = self.workspace.validate(self.path)
        self.assertTrue(result["valid"])
        self.assertEqual(result["estimate"]["runs"], 24)

    def test_repeated_system_treatments_are_rejected_before_runtime_collapse(self) -> None:
        """One experiment cannot encode two knob variants with the same DBMS name."""
        repeated = yaml.safe_load(_SPEC)
        repeated["systems"] = [
            {
                "name": "PgDuckDB",
                "profile": "analytical-ssd",
                "override": {"duckdb_force_execution": True},
            },
            {
                "name": "PgDuckDB",
                "profile": "analytical-ssd",
                "override": {"duckdb_force_execution": False},
            },
        ]
        self.workspace.write_file(self.path, yaml.safe_dump(repeated))

        result = self.workspace.validate(self.path)

        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["stage"], "methodology")
        self.assertIn("use a follow-up experiment", result["errors"][0]["message"])

    def _rejection(self, spec_text: str) -> str:
        self.workspace.write_file(self.path, spec_text)
        result = self.workspace.validate(self.path)
        self.assertFalse(result["valid"], spec_text)
        return result["errors"][0]["message"]

    def test_values_are_checked_against_declared_bounds(self) -> None:
        for original, broken, expected in (
            ("scaling_factor: 1", "scaling_factor: 0", "below the declared minimum"),
            ("active_queries: [5]", "active_queries: [99]", "above the declared maximum"),
            ("active_queries: [5]", "active_queries: []", "must not be empty"),
            ("rounds: [1, 2]", "rounds: [0, 2]", "below the declared minimum"),
            ("repetitions: 3", "repetitions: 0", "below the declared minimum"),
            ("scaling_factor: 1", "scaling_factor: two", "must be an integer"),
            ("active_queries: [5]", "active_queries: 5", "must be a list of integers"),
            ("cpu: {request: 4, limit: 4}", "cpu: {request: 9, limit: 4}", "exceeds its own limit"),
        ):
            with self.subTest(broken):
                self.assertIn(expected, self._rejection(_SPEC.replace(original, broken)))

    def test_declared_primitive_types_and_enums_are_checked(self) -> None:
        for original, broken, expected in (
            ("mode: run", "mode: nonsense", "is not one of"),
            ("title: comparison", "title: 42", "must be a string"),
            ("discriminates: [system, concurrency]",
             "discriminates: [system, 2]", "must be a string"),
            ("resources:", "observe:\n  monitoring_sut: not-a-bool\nresources:",
             "must be a boolean"),
        ):
            with self.subTest(broken):
                self.assertIn(expected, self._rejection(_SPEC.replace(original, broken)))

    def test_malformed_nested_shape_returns_a_verdict(self) -> None:
        broken = yaml.safe_load(_SPEC)
        broken["workload"] = ["tpch"]
        self.workspace.write_file(self.path, yaml.safe_dump(broken))
        result = self.workspace.validate(self.path)
        self.assertFalse(result["valid"])
        self.assertIsNone(result["estimate"]["runs"])
        self.assertIn("workload must be an object", result["errors"][0]["message"])

    def test_updated_catalog_bounds_are_applied_without_code_changes(self) -> None:
        catalog = self.root / "contracts" / "contract_catalog.yml"
        changed = yaml.safe_load(catalog.read_text())
        changed["workloads"]["tpch"]["params"]["scaling_factor"]["min"] = 2
        catalog.write_text(yaml.safe_dump(changed))
        self.assertIn("declared minimum of 2", self._rejection(_SPEC))

    def test_workload_bounds_apply_to_the_loading_block(self) -> None:
        self.assertIn("below the declared minimum",
                      self._rejection(_SPEC + "loading:\n  pods: 0\n"))

    def test_a_restructured_catalog_yields_a_verdict_not_a_crash(self) -> None:
        catalog = self.root / "contracts" / "contract_catalog.yml"
        broken = yaml.safe_load(catalog.read_text())
        broken["experiment_schema"]["fields"]["workload"].pop("fields")
        catalog.write_text(yaml.safe_dump(broken))
        self.assertIn("catalog is missing the structure", self._rejection(_SPEC))

    def test_a_mistyped_contract_type_is_reported_not_ignored(self) -> None:
        catalog = self.root / "contracts" / "contract_catalog.yml"
        broken = yaml.safe_load(catalog.read_text())
        broken["experiment_schema"]["fields"]["title"]["type"] = "string"
        catalog.write_text(yaml.safe_dump(broken))
        self.assertIn("unrecognised type", self._rejection(_SPEC))

    def test_submit_preassigns_code_and_archives_provenance(self) -> None:
        self._validate()

        def launch(argv, **_kwargs):
            self.assertEqual(argv[1:3], ["-m", "agent.harness.submit"])
            code = argv[argv.index("--experiment-code") + 1]
            (self.root / "results" / code).mkdir()
            return _Process()

        with mock.patch("agent.harness.tools.subprocess.Popen", side_effect=launch):
            result = self.workspace.submit(self.path)

        result_dir = self.root / "results" / result["code"]
        self.assertEqual((result_dir / "experiment.yml").read_text(), _SPEC)
        self.assertTrue((result_dir / "contract_catalog.yml").is_file())
        self.assertTrue((result_dir / "contract_result.yml").is_file())
        self.assertEqual((self.run / "submitted-experiment.yml").read_text(), _SPEC)

    def test_agent_side_submit_adapter_uses_bexhoma_resolver(self) -> None:
        specification = self.root / "submitted.yml"
        specification.write_text(_SPEC)
        parsed = object()
        parser = mock.Mock()
        parser.parse_args.return_value = parsed
        with (
            mock.patch.object(submit_adapter.catalog_spec, "load_catalog", return_value={}),
            mock.patch.object(
                submit_adapter.catalog_spec, "build_argv", return_value=["-dbms", "PostgreSQL"]
            ) as build,
            mock.patch.object(submit_adapter.tpch, "build_parser", return_value=parser),
            mock.patch.object(submit_adapter.tpch, "run") as run,
        ):
            submit_adapter.run(str(specification), "catalog.yml", "123")

        build.assert_called_once()
        parser.parse_args.assert_called_once_with(
            ["-dbms", "PostgreSQL", "-e", "123", "-rp"]
        )
        run.assert_called_once_with(parsed)

    def test_list_results_persists_a_derived_finished_state(self) -> None:
        code = "42"
        report = self.root / "results" / code / "report" / "index.md"
        report.parent.mkdir(parents=True)
        report.write_text("finished\n")
        status = self.workspace.status_dir / f"{code}.json"
        status.write_text(json.dumps({
            "code": code,
            "state": "running",
            "results": str(report.parent.parent),
            "pid": 99999999,
        }))

        listing = self.workspace.list_results()["experiments"]

        self.assertEqual(listing[0]["state"], "finished")
        self.assertEqual(json.loads(status.read_text())["state"], "finished")

    def test_submit_refuses_while_run_lock_is_held(self) -> None:
        self._validate()
        lock = (self.root / "results" / ".bexhoma-agent.lock").open("w")
        self.addCleanup(lock.close)
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        result = self.workspace.call("submit", {"path": self.path})
        self.assertIn("still running", result["error"])

    def test_interpretation_can_submit_one_followup(self) -> None:
        assessment = {
            "question": "what causes degradation?", "status": "unresolved",
            "conclusion": "CPU contention is possible", "evidence": "latency rises",
            "missing": "a controlled CPU intervention",
        }
        decision = {
            "action": "followup", "rationale": "the catalog exposes a CPU sweep",
            "unresolved_question": "what causes degradation?",
            "experiment_goal": "vary CPU at fixed memory and compare the concurrency slope",
        }
        model = _Model([
            _tool_reply(ToolCall("record", "record_interpretation",
                                 {"questions": [assessment]})),
            _text_reply("The comparison is settled, but the mechanism is not."),
            _tool_reply(
                ToolCall("read-catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("decide", "record_followup_decision", decision),
            ),
            _text_reply("A CPU sweep is warranted."),
            _tool_reply(
                ToolCall("read-catalog-again", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("write", "write_file", {"path": self.path, "text": _SPEC}),
                ToolCall("validate", "validate", {"path": self.path}),
                ToolCall("submit", "submit", {"path": self.path}),
            ),
            _text_reply("Follow-up submitted."),
        ])

        def launch(argv, **_kwargs):
            code = argv[argv.index("--experiment-code") + 1]
            (self.root / "results" / code).mkdir()
            return _Process()

        with mock.patch("agent.harness.tools.subprocess.Popen", side_effect=launch):
            outcome = run_interpret(
                task="question", report_path="results/old/report/index.md",
                specification=_SPEC, workspace=self.workspace, model=model,
                trajectory=Trajectory(self.run),
                result_contract_path="contracts/contract_result.yml",
                followups=1, environment_path=None, attempts=1,
            )
        self.assertIsNotNone(outcome["code"])
        self.assertTrue(outcome["phase_complete"])
        self.assertEqual(outcome["followups_remaining"], 0)
        self.assertEqual(outcome["followup_decision"]["action"], "followup")
        self.assertEqual(outcome["question_assessments"], [assessment])
        self.assertNotIn("write_file", model.tool_sets[0])
        self.assertNotIn("write_file", model.tool_sets[2])
        self.assertIn("write_file", model.tool_sets[4])

    def test_followup_decision_must_read_catalog_before_finishing(self) -> None:
        assessment = {
            "question": "mechanism?", "status": "partial", "conclusion": "CPU indicated",
            "evidence": "same memory slopes", "missing": "controlled intervention",
        }
        finish = {
            "action": "finish", "rationale": "no safe supported intervention exists",
            "unresolved_question": "", "experiment_goal": "",
        }
        model = _Model([
            _tool_reply(ToolCall("record", "record_interpretation",
                                 {"questions": [assessment]})),
            _text_reply("The mechanism is only indicated."),
            _tool_reply(ToolCall("too-early", "record_followup_decision", finish)),
            _tool_reply(
                ToolCall("read-catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("finish", "record_followup_decision", finish),
            ),
            _text_reply("No feasible follow-up exists."),
        ])

        outcome = run_interpret(
            task="question", report_path="results/old/report/index.md",
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path="contracts/contract_result.yml",
            followups=1, environment_path=None, attempts=1,
        )

        self.assertIsNone(outcome["code"])
        self.assertTrue(outcome["phase_complete"])
        self.assertEqual(outcome["followup_decision"]["action"], "finish")
        events = [json.loads(line) for line in (self.run / "trajectory.jsonl").read_text().splitlines()]
        rejected = [event for event in events
                    if event.get("tool") == "record_followup_decision"
                    and "error" in event.get("result", {})]
        self.assertEqual(len(rejected), 1)

    def test_interpretation_dry_run_validates_without_submit(self) -> None:
        assessment = {
            "question": "mechanism?", "status": "partial",
            "conclusion": "CPU indicated", "evidence": "same memory slopes",
            "missing": "controlled intervention",
        }
        decision = {
            "action": "followup", "rationale": "a CPU sweep is feasible",
            "unresolved_question": "mechanism?",
            "experiment_goal": "vary CPU at fixed memory",
        }
        model = _Model([
            _tool_reply(ToolCall("record", "record_interpretation",
                                 {"questions": [assessment]})),
            _text_reply("The mechanism is partial."),
            _tool_reply(
                ToolCall("catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("decision", "record_followup_decision", decision),
            ),
            _text_reply("A follow-up is warranted."),
            _tool_reply(
                ToolCall("catalog-again", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("write", "write_file", {"path": self.path, "text": _SPEC}),
                ToolCall("validate", "validate", {"path": self.path}),
            ),
            _text_reply("The proposed follow-up validates."),
        ])

        outcome = run_interpret(
            task="question", report_path="results/old/report/index.md",
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path="contracts/contract_result.yml",
            followups=1, environment_path=None, attempts=1, dry_run=True,
        )

        self.assertTrue(outcome["phase_complete"])
        self.assertIsNone(outcome["code"])
        self.assertEqual(outcome["validated_path"], self.path)
        self.assertNotIn("submit", model.tool_sets[4])

    def test_interpretation_cannot_finish_without_question_coverage(self) -> None:
        assessment = {
            "question": "is it faster?", "status": "settled", "conclusion": "no",
            "evidence": "latency is higher", "missing": "",
        }
        model = _Model([
            _text_reply("A premature answer."),
            _tool_reply(ToolCall("record", "record_interpretation",
                                 {"questions": [assessment]})),
            _text_reply("The supported answer."),
        ])

        outcome = run_interpret(
            task="question", report_path="results/old/report/index.md",
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path="contracts/contract_result.yml",
            followups=0, environment_path=None, attempts=1,
        )

        self.assertEqual(outcome["summary"], "The supported answer.")
        self.assertTrue(outcome["phase_complete"])
        events = [json.loads(line) for line in (self.run / "trajectory.jsonl").read_text().splitlines()]
        self.assertTrue(any(event["type"] == "completion_rejected" for event in events))

    def test_settled_interpretation_cannot_list_missing_evidence(self) -> None:
        invalid = {
            "question": "what causes degradation?", "status": "settled",
            "conclusion": "memory starvation", "evidence": "throughput falls",
            "missing": "direct memory measurements",
        }
        corrected = {**invalid, "status": "partial"}
        model = _Model([
            _tool_reply(ToolCall("invalid", "record_interpretation",
                                 {"questions": [invalid]})),
            _tool_reply(ToolCall("corrected", "record_interpretation",
                                 {"questions": [corrected]})),
            _text_reply("Memory starvation is indicated but not established."),
        ])

        outcome = run_interpret(
            task="question", report_path="results/old/report/index.md",
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path="contracts/contract_result.yml",
            followups=0, environment_path=None, attempts=1,
        )

        self.assertEqual(outcome["question_assessments"], [corrected])
        events = [json.loads(line) for line in
                  (self.run / "trajectory.jsonl").read_text().splitlines()]
        rejected = [event for event in events
                    if event.get("tool") == "record_interpretation"
                    and "error" in event.get("result", {})]
        self.assertEqual(len(rejected), 1)

    def test_followup_decision_also_requires_present_environment(self) -> None:
        (self.root / "environment.yml").write_text("usable_nodes: []\n")
        workspace = Workspace(
            root=str(self.root), inbox="inbox",
            catalog_path="contracts/contract_catalog.yml",
            environment_path="environment.yml",
            results_root=str(self.root / "results"), run_directory=self.run,
        )
        assessment = {
            "question": "mechanism?", "status": "partial", "conclusion": "uncertain",
            "evidence": "a directional pattern", "missing": "an intervention",
        }
        finish = {
            "action": "finish", "rationale": "no feasible intervention exists",
            "unresolved_question": "", "experiment_goal": "",
        }
        model = _Model([
            _tool_reply(ToolCall("record", "record_interpretation",
                                 {"questions": [assessment]})),
            _text_reply("The mechanism remains uncertain."),
            _tool_reply(
                ToolCall("catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("too-early", "record_followup_decision", finish),
            ),
            _tool_reply(
                ToolCall("environment", "read_file", {"path": "environment.yml"}),
                ToolCall("finish", "record_followup_decision", finish),
            ),
            _text_reply("No follow-up."),
        ])

        outcome = run_interpret(
            task="question", report_path="results/old/report/index.md",
            specification=_SPEC, workspace=workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path="contracts/contract_result.yml",
            followups=1, environment_path="environment.yml", attempts=1,
        )

        self.assertTrue(outcome["phase_complete"])
        events = [json.loads(line) for line in (self.run / "trajectory.jsonl").read_text().splitlines()]
        rejected = [event for event in events
                    if event.get("tool") == "record_followup_decision"
                    and "error" in event.get("result", {})]
        self.assertEqual(rejected[0]["result"]["missing"], [str(self.root / "environment.yml")])


class PhaseTest(unittest.TestCase):
    def test_cli_reuses_one_investigation_and_writes_final_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "contracts").mkdir()
            (root / "contracts" / "contract_catalog.yml").write_text("version: 1\n")
            results = root / "results"
            results.mkdir()

            def design_phase(**kwargs):
                trajectory = kwargs["trajectory"]
                trajectory.record("meta", phase="design", budgets={"followups": 1})
                trajectory.record("task", text="question")
                outcome = {
                    "summary": "design account", "code": "42",
                    "submitted_spec": None, "followups_remaining": 1,
                }
                trajectory.record("outcome", **outcome)
                return outcome

            design_argv = [
                "agent", "--model", "fake", "--root", str(root),
                "--trajectories", "investigations", "--results", str(results),
                "--environment", "", "--task", "question",
            ]
            with (
                mock.patch("sys.argv", design_argv),
                mock.patch("agent.harness.agent.model_client.ChatModel"),
                mock.patch("agent.harness.agent.run_design", side_effect=design_phase),
            ):
                self.assertEqual(agent_main(), 0)

            investigations = list((root / "investigations").iterdir())
            self.assertEqual(len(investigations), 1)
            investigation = investigations[0]
            self.assertFalse((investigation / "answer.md").exists())

            report = results / "42" / "report" / "index.md"
            report.parent.mkdir(parents=True)
            report.write_text("finished\n")
            (root / "status" / "42.json").write_text(json.dumps({
                "code": "42", "state": "running", "results": str(results / "42"),
            }))

            def interpret_phase(**kwargs):
                trajectory = kwargs["trajectory"]
                trajectory.record("meta", phase="interpret", report=str(report))
                trajectory.record("task", text="question")
                outcome = {
                    "summary": "# Benchmark Study Result\n\nFinal aggregate",
                    "code": None, "followups_remaining": 1,
                    "phase_complete": True,
                }
                trajectory.record("outcome", **outcome)
                return outcome

            interpret_argv = [
                "agent", "--phase", "interpret", "--model", "fake",
                "--root", str(root), "--trajectories", "investigations",
                "--results", str(results), "--environment", "",
                "--run", str(investigation),
            ]
            with (
                mock.patch("sys.argv", interpret_argv),
                mock.patch("agent.harness.agent.model_client.ChatModel"),
                mock.patch("agent.harness.agent.run_interpret", side_effect=interpret_phase),
            ):
                self.assertEqual(agent_main(), 0)

            self.assertEqual(list((root / "investigations").iterdir()), [investigation])
            self.assertTrue((investigation / "reports" / "01-design.md").is_file())
            self.assertTrue((investigation / "reports" / "02-interpret.md").is_file())
            self.assertEqual(
                (investigation / "answer.md").read_text(),
                "# Benchmark Study Result\n\nFinal aggregate\n",
            )
            phases = [
                json.loads(line).get("phase")
                for line in (investigation / "trajectory.jsonl").read_text().splitlines()
                if json.loads(line).get("type") == "meta"
            ]
            self.assertEqual(phases, ["design", "interpret"])

    def test_only_final_phase_creates_aggregated_answer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            investigation = Path(directory)
            trajectory = Trajectory(investigation)

            first_report, first_answer = _write_reports(
                investigation, trajectory, 1, "design", "design account", False
            )
            self.assertEqual(first_report.read_text(), "design account\n")
            self.assertIsNone(first_answer)
            self.assertFalse((investigation / "answer.md").exists())

            final_report, final_answer = _write_reports(
                investigation, trajectory, 2, "interpret", "full study", True
            )
            self.assertEqual(final_report.read_text(), "full study\n")
            self.assertEqual(final_answer, investigation / "answer.md")
            self.assertEqual(final_answer.read_text(), "full study\n")

    def test_phase_number_counts_all_phases_in_one_trajectory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            investigation = Path(directory)
            (investigation / "trajectory.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in (
                    {"type": "meta", "phase": "design"},
                    {"type": "outcome", "code": "41"},
                    {"type": "meta", "phase": "interpret"},
                    {"type": "outcome", "code": "42"},
                )),
                encoding="utf-8",
            )

            self.assertEqual(_phase_number(investigation), 3)

    def test_stages_expose_only_the_tools_they_need(self) -> None:
        names = lambda schemas: {tool["function"]["name"] for tool in schemas}
        self.assertEqual(
            names(INTERPRET_TOOLS),
            {"read_file", "compare_query_latency", "list_results", "record_interpretation"},
        )
        self.assertEqual(
            names(FOLLOWUP_DECISION_TOOLS),
            {"read_file", "record_followup_decision"},
        )
        self.assertEqual(
            names(FOLLOWUP_AUTHOR_TOOLS),
            {"read_file", "write_file", "validate", "submit"},
        )

    def test_carry_forward_prefers_immutable_submitted_spec(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            (run / "submitted-experiment.yml").write_text("immutable\n")
            events = [
                {"type": "meta", "budgets": {"followups": 1}},
                {"type": "task", "text": "question"},
                {"type": "outcome", "validated_path": "inbox/mutable.yml", "code": "42"},
            ]
            (run / "trajectory.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in events))
            task, specification, code, followups, previous = _carry_forward(
                run, Path(directory)
            )
            self.assertEqual((task, specification, code, followups, previous),
                             ("question", "immutable\n", "42", 1, None))

    def test_followup_carries_a_bounded_previous_experiment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run = root / "run"
            run.mkdir()
            (run / "submitted-experiment.yml").write_text("followup\n")
            previous = root / "results" / "41"
            (previous / "report").mkdir(parents=True)
            (previous / "experiment.yml").write_text("original\n")
            events = [
                {"type": "meta", "phase": "design",
                 "budgets": {"followups": 1}},
                {"type": "task", "text": "question"},
                {"type": "outcome", "code": "41",
                 "summary": "initial experiment submitted",
                 "followups_remaining": 1},
                {"type": "meta", "phase": "interpret",
                 "report": str(previous / "report" / "index.md"),
                 "budgets": {"followups": 1}},
                {"type": "outcome", "code": "42", "followups_remaining": 0,
                 "summary": "changed CPU to distinguish contention",
                 "followup_decision": {
                     "action": "followup",
                     "rationale": "separate CPU contention from routing",
                     "unresolved_question": "is CPU contention causal?",
                     "experiment_goal": "repeat with controlled CPU limits",
                 }},
            ]
            (run / "trajectory.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in events))

            task, specification, code, followups, handoff = _carry_forward(run, root)

            self.assertEqual((task, specification, code, followups),
                             ("question", "followup\n", "42", 0))
            self.assertEqual(handoff, {
                "report": str(previous / "report" / "index.md"),
                "specification": "original\n",
                "summary": "changed CPU to distinguish contention",
                "followup_decision": {
                    "action": "followup",
                    "rationale": "separate CPU contention from routing",
                    "unresolved_question": "is CPU contention causal?",
                    "experiment_goal": "repeat with controlled CPU limits",
                },
            })

    def test_interpret_prompt_requires_a_self_contained_study_report(self) -> None:
        messages = prompts.interpret_messages(
            task="Which configuration is faster?",
            report_path="results/42/report/index.md",
            result_contract_path="results/42/contract_result.yml",
            specification=_SPEC,
            previous_experiment={
                "followup_decision": {
                    "action": "followup",
                    "rationale": "the baseline was missing",
                }
            },
        )

        system = messages[0]["content"]
        for heading in (
            "# Benchmark Study Result",
            "## Original question",
            "## Hypothesis",
            "## Experiments performed",
            "## Validity",
            "## Results",
            "## Interpretation",
            "## Follow-up experiment",
            "## Final verdict",
        ):
            self.assertIn(heading, system)
        self.assertIn("the baseline was missing", messages[1]["content"])


class ChatModelTest(unittest.TestCase):
    def test_current_reasoning_field_is_logged_but_not_replayed(self) -> None:
        message = mock.Mock()
        message.content = "answer"
        message.tool_calls = []
        message.model_dump.return_value = {
            "role": "assistant", "content": "answer", "reasoning": "hidden",
        }
        usage = mock.Mock()
        usage.model_dump.return_value = {"completion_tokens": 12}
        response = mock.Mock(choices=[mock.Mock(message=message)], usage=usage)
        model = ChatModel.__new__(ChatModel)
        model.model = "fake"
        model.temperature = 0.0
        model.max_tokens = 100
        model._client = mock.Mock()
        model._client.chat.completions.create.return_value = response

        reply = model.reply([{"role": "user", "content": "question"}])

        self.assertEqual(reply.reasoning, "hidden")
        self.assertNotIn("reasoning", reply.message)
        request = model._client.chat.completions.create.call_args.kwargs
        self.assertNotIn("extra_body", request)


if __name__ == "__main__":
    unittest.main()
