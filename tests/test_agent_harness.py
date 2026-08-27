"""Focused tests for the agent's validation and submission boundary."""
from __future__ import annotations

import contextlib
import fcntl
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import yaml

from agent.harness import prompts, submit as submit_adapter
from agent.harness.agent import (
    Trajectory,
    _carry_forward,
    _phase_number,
    _write_reports,
    main as agent_main,
    run_design,
    run_interpret,
)
from openai import RateLimitError

from agent.harness.model_client import (
    ChatModel, ContextWindowExhausted, ModelUnreachable, Reply, ToolCall,
)
from agent.harness.tools import (
    DESIGN_TOOLS,
    FOLLOWUP_AUTHOR_TOOLS,
    INTERPRET_TOOLS,
    ToolError,
    Workspace,
    default_result_root,
    without_submit,
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

_ENVIRONMENT = """\
resource_limits:
  max_allocatable_cpu: 64
  max_allocatable_memory: 128Gi
"""

_REPORT_PATH = "results/old/report/index.md"
_RESULT_CONTRACT_PATH = "contracts/contract_result.yml"
_REPORT = """\
---
overall_status:
  passed: 7
  failed: 0
  skipped: 0
---
### Tests

| status | label |
|---|---|
| passed | Workflow as planned |

[Benchmarking](benchmarking.md)
[Execution](execution.md)
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
        self.messages: list[list[dict[str, Any]]] = []

    def reply(self, _messages, tools=None):
        self.messages.append(list(_messages))
        self.tool_sets.append({tool["function"]["name"] for tool in (tools or [])})
        return self.replies.pop(0)


def _tool_reply(*calls: ToolCall) -> Reply:
    return Reply("", "", list(calls), {"role": "assistant", "content": ""}, {})


def _text_reply(text: str) -> Reply:
    return Reply(text, "", [], {"role": "assistant", "content": text}, {})


def _interpretation_text() -> str:
    """Return one result-contract-shaped answer for scripted model tests."""
    return """\
# Result interpretation

## Hypothesis

The benchmark question.

## Verdict

The validity checks support the stated scope.

## Evidence

The decisive measured result.

## Follow-up

No follow-up is needed.
"""


def _followup_spec(query: int = 5, code: str = "old") -> str:
    """Return a lineage-correct specification with one controlled change."""
    specification = _SPEC.replace(
        "discriminates: [system, concurrency]",
        f"discriminates: [system, concurrency]\nfollow_up_of: \"{code}\"",
    )
    specification = specification.replace(
        "active_queries: [5]", f"active_queries: [{query}]"
    )
    return specification.replace(
        "cpu: {request: 4, limit: 4}", "cpu: {request: 8, limit: 8}"
    )


def _record_arguments(
    questions: list[dict[str, Any]], failed_checks: int = 0, scope: str = "",
    comparison_quality: dict[str, Any] | None = None,
    follow_up: dict[str, Any] | None = None,
    hypothesis_verdict: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one complete interpretation record for scripted model tests."""
    normalized = [
        {
            **question,
            "validity": question.get("validity", "supported"),
            "evidence_paths": question.get("evidence_paths", [_REPORT_PATH]),
        }
        for question in questions
    ]
    return {
        "hypothesis_verdict": hypothesis_verdict or {
            "status": "inconclusive",
            "conclusion": "The current experiment does not settle the hypothesis.",
            "evidence_paths": [_REPORT_PATH],
        },
        "validity": {
            "failed_checks": failed_checks,
            "scope": scope,
            "evidence_paths": [_REPORT_PATH],
        },
        "comparison_quality": comparison_quality or {
            "query_coverage": "not_applicable",
            "whole_workload_throughput": "not_applicable",
            "suspect_repetitions": [],
        },
        "questions": normalized,
        "follow_up": follow_up or {
            "action": "finish",
            "rationale": "the current result is sufficient",
            "unresolved_question": "",
            "experiment_goal": "",
            "target_queries": [],
            "full_workload_required": False,
            "cost_rationale": "No additional cluster time is needed.",
        },
    }


def _evidence_record_reply(identifier: str, arguments: dict) -> Reply:
    """Read the required evidence and submit one interpretation record."""
    return _tool_reply(
        ToolCall(f"{identifier}-report", "read_file", {"path": _REPORT_PATH}),
        ToolCall(
            f"{identifier}-contract", "read_file", {"path": _RESULT_CONTRACT_PATH}
        ),
        ToolCall(identifier, "record_interpretation", arguments),
    )


class WorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "contracts").mkdir()
        (self.root / "results").mkdir()
        (self.root / "environment.yml").write_text(_ENVIRONMENT)
        self.run = self.root / "trajectory"
        self.run.mkdir()
        for name in ("contract_catalog.yml", "contract_result.yml"):
            shutil.copyfile(Path("contracts") / name, self.root / "contracts" / name)
        report = self.root / _REPORT_PATH
        report.parent.mkdir(parents=True)
        report.write_text(_REPORT)
        self.workspace = Workspace(
            root=str(self.root), inbox="inbox",
            catalog_path="contracts/contract_catalog.yml",
            environment_path="environment.yml",
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

    def test_interpretation_reads_only_files_reachable_from_one_report(self) -> None:
        """A selected report must not expose unlinked or sibling-result files."""
        linked = self.root / "results" / "old" / "report" / "benchmarking.md"
        linked.write_text("linked evidence\n")
        unlinked = self.root / "results" / "old" / "report" / "secret.md"
        unlinked.write_text("unlinked evidence\n")
        sibling = self.root / "results" / "other" / "report" / "index.md"
        sibling.parent.mkdir(parents=True)
        sibling.write_text("other result\n")

        self.workspace.restrict_to_result(_REPORT_PATH, _RESULT_CONTRACT_PATH)

        self.assertIn("text", self.workspace.read_file(_REPORT_PATH))
        self.assertEqual(self.workspace.read_file(str(linked))["text"], "linked evidence\n")
        self.assertIn("not reachable", self.workspace.call(
            "read_file", {"path": str(unlinked)}
        )["error"])
        self.assertIn("not reachable", self.workspace.call(
            "read_file", {"path": str(sibling)}
        )["error"])

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

    def test_comparison_quality_separates_coverage_and_flags_anomalies(self) -> None:
        report = self.root / "results" / "quality.md"
        report.write_text("""\
#### Per Phase

| phase | experiment_run | client | Geo Times [s] |
|:--|--:|--:|--:|
| pgduckdb-1-1-1 | 1 | 1 | 9.0 |
| pgduckdb-1-2-1 | 2 | 1 | 9.2 |
| pgduckdb-1-3-1 | 3 | 1 | 9.1 |
| postgresql-1-1-1 | 1 | 1 | 6.0 |
| postgresql-1-2-1 | 2 | 1 | 6.2 |
| postgresql-1-3-1 | 3 | 1 | 1.0 |

### Latency of Timer Execution [ms]
| Queries | pgduckdb-1-1-1-1-1 | postgresql-1-1-1-1-1 |
|:--|--:|--:|
| First (TPC-H Q1) | 10 | 8 |
| Third (TPC-H Q3) | 30 | 20 |

### Errors (failed queries)
| | First (TPC-H Q1) | Second (TPC-H Q2) | Third (TPC-H Q3) |
|:--|--:|--:|--:|
| postgresql-1-1-1-1-1 | 0 | 1 | 0 |
""")

        result = self.workspace.assess_comparison_quality(str(report))

        self.assertEqual(result["query_coverage"], "partial")
        self.assertEqual(result["unresolved_queries"], [2])
        self.assertEqual(result["whole_workload_throughput"], "not_comparable")
        self.assertEqual(
            result["systems"]["postgresql-1"]["completed_queries"], [1, 3]
        )
        self.assertEqual(
            result["suspect_repetitions"][0]["phase"], "postgresql-1-3-1"
        )
        self.assertEqual(
            result["suspect_repetitions"][0]["status"], "suspect_not_invalid"
        )

    def test_validation_estimates_the_declared_timeout_budget(self) -> None:
        self.workspace.write_file(self.path, _SPEC)

        estimate = self.workspace.validate(self.path)["estimate"]

        self.assertEqual(estimate["runs"], 12)
        self.assertEqual(estimate["query_timeout_budget_min"], 120.0)
        self.assertEqual(estimate["declared_timeout_budget_min"], 120.0)
        self.assertIn("not a runtime prediction", estimate["basis"])

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

    def test_cpu_only_sweep_has_distinct_resource_cell_identities(self) -> None:
        """Every CPU treatment must address a different runtime configuration."""
        experiment = yaml.safe_load(_SPEC)
        experiment["discriminates"].append("cpu")
        experiment["resources"]["cpu"] = [
            {"request": cpu, "limit": cpu} for cpu in (8, 16, 32)
        ]

        catalog = submit_adapter.catalog_spec.load_catalog(self.workspace.catalog_path)
        argv = submit_adapter.catalog_spec.build_argv(catalog, experiment)
        scoped_configurations = {
            argument.split("@", 1)[1].split(".container", 1)[0]
            for argument in argv
            if argument.startswith("deployment[") and "@" in argument
        }

        self.assertEqual(scoped_configurations, {
            f"{system}-resources-{cell}"
            for system in ("PostgreSQL", "PgDuckDB")
            for cell in (1, 2, 3)
        })

    def test_loading_timeout_is_validated_and_translated(self) -> None:
        """The agent contract must expose Bexhoma's load-only deadline."""
        experiment = yaml.safe_load(_SPEC)
        catalog = submit_adapter.catalog_spec.load_catalog(self.workspace.catalog_path)
        self.assertNotIn(
            "--loading-timeout",
            submit_adapter.catalog_spec.build_argv(catalog, experiment),
        )
        experiment["loading"] = {"timeout_minutes": 15}
        self.workspace.write_file(self.path, yaml.safe_dump(experiment))

        verdict = self.workspace.validate(self.path)
        argv = submit_adapter.catalog_spec.build_argv(catalog, experiment)

        self.assertTrue(verdict["valid"])
        self.assertEqual(argv[argv.index("--loading-timeout") + 1], "15")

        experiment["loading"]["timeout_minutes"] = 0
        self.workspace.write_file(self.path, yaml.safe_dump(experiment))
        invalid = self.workspace.validate(self.path)
        self.assertFalse(invalid["valid"])
        self.assertIn("minimum of 1", invalid["errors"][0]["message"])

    def test_benchmarker_peak_limits_must_fit_its_pinned_node(self) -> None:
        """Concurrent benchmarker Pods must not hide an unsafe memory peak."""
        experiment = yaml.safe_load(_SPEC)
        experiment["placement"] = {
            "sut": "database-node",
            "benchmarking": "benchmark-node",
        }
        environment = {
            "nodes": [
                {
                    "name": "database-node",
                    "allocatable": {"cpu": 64, "memory": "64Gi"},
                },
                {
                    "name": "benchmark-node",
                    "allocatable": {"cpu": 128, "memory": "384Gi"},
                },
            ],
        }
        (self.root / "environment.yml").write_text(yaml.safe_dump(environment))
        self.workspace.write_file(self.path, yaml.safe_dump(experiment))

        fitting = self.workspace.validate(self.path)

        self.assertTrue(fitting["valid"])

        experiment["workload"]["rounds"] = [1, 2, 4]
        self.workspace.write_file(self.path, yaml.safe_dump(experiment))
        oversized = self.workspace.validate(self.path)

        self.assertFalse(oversized["valid"])
        self.assertEqual(oversized["errors"][0]["stage"], "environment")
        self.assertIn("4 benchmarker pod(s)", oversized["errors"][0]["message"])
        self.assertIn("512Gi", oversized["errors"][0]["message"])

    def test_co_located_sut_limits_are_added_to_benchmarker_limits(self) -> None:
        """A shared node must fit resident databases as well as benchmarkers."""
        experiment = yaml.safe_load(_SPEC)
        experiment["placement"] = {
            "sut": "shared-node",
            "benchmarking": "benchmark-node",
        }
        environment = {
            "nodes": [
                {
                    "name": "shared-node",
                    "allocatable": {"cpu": 128, "memory": "64Gi"},
                },
                {
                    "name": "benchmark-node",
                    "allocatable": {"cpu": 128, "memory": "256Gi"},
                },
            ],
        }
        (self.root / "environment.yml").write_text(yaml.safe_dump(environment))
        self.workspace.write_file(self.path, yaml.safe_dump(experiment))
        self.assertTrue(self.workspace.validate(self.path)["valid"])

        experiment["placement"]["sut"] = "benchmark-node"
        self.workspace.write_file(self.path, yaml.safe_dump(experiment))
        co_located = self.workspace.validate(self.path)

        self.assertFalse(co_located["valid"])
        message = co_located["errors"][0]["message"]
        self.assertIn("one active SUT pod and 2 benchmarker pod(s)", message)
        self.assertIn("264Gi", message)

    def test_submit_requires_environment_checked_validation(self) -> None:
        """Catalog-only validation is useful for dry runs but cannot reach Kubernetes."""
        unchecked = Workspace(
            root=str(self.root), inbox="unchecked-inbox",
            catalog_path="contracts/contract_catalog.yml",
            results_root=str(self.root / "results"), run_directory=self.run,
        )
        path = "unchecked-inbox/experiment.yml"
        unchecked.write_file(path, _SPEC)

        verdict = unchecked.validate(path)
        result = unchecked.call("submit", {"path": path})

        self.assertTrue(verdict["valid"])
        self.assertFalse(verdict["environment_checked"])
        self.assertIn("full catalog and environment validation", result["error"])

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

    def test_submit_names_a_run_it_launched_but_could_not_confirm(self) -> None:
        """A slow start must be reported as a live run, not as nothing having happened."""
        self._validate()

        with (
            mock.patch("agent.harness.tools.subprocess.Popen", return_value=_Process()),
            mock.patch("agent.harness.tools._CODE_WAIT_SECONDS", 0),
        ):
            result = self.workspace.submit(self.path)

        self.assertEqual(result["state"], "starting")
        self.assertEqual(result["pid"], 4242)
        self.assertTrue(result["code"])

        result_directory = self.root / "results" / result["code"]
        report = result_directory / "report" / "index.md"
        report.parent.mkdir(parents=True)
        report.write_text("finished\n")

        listing = self.workspace.list_results()["experiments"]

        self.assertEqual(listing[0]["code"], result["code"])
        self.assertEqual(listing[0]["state"], "finished")
        self.assertEqual((result_directory / "experiment.yml").read_text(), _SPEC)
        self.assertTrue((result_directory / "contract_catalog.yml").is_file())
        self.assertTrue((result_directory / "contract_result.yml").is_file())
        self.assertEqual(
            (result_directory / "environment.yml").read_text(), _ENVIRONMENT
        )

    def test_submit_reports_a_child_that_died_before_starting(self) -> None:
        """A dead child is a different failure from a slow one and reads differently."""
        self._validate()

        class _Dead(_Process):
            returncode = 3

            def poll(self):
                return 3

        with (
            mock.patch("agent.harness.tools.subprocess.Popen", return_value=_Dead()),
            self.assertRaises(ToolError) as refused,
        ):
            self.workspace.submit(self.path)

        self.assertIn("exited with status 3", str(refused.exception))

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
            [
                "-dbms", "PostgreSQL", "-e", "123",
                "--max-sut-experiment", "1", "-rp",
            ]
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
            "target_queries": [], "full_workload_required": True,
            "cost_rationale": "The mechanism requires the complete concurrency workload.",
        }
        model = _Model([
            _evidence_record_reply(
                "record", _record_arguments([assessment], follow_up=decision)
            ),
            _text_reply(_interpretation_text()),
            _tool_reply(
                ToolCall("read-catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("write", "write_file", {
                    "path": self.path, "text": _followup_spec(),
                }),
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
                task="question", report_path=_REPORT_PATH,
                specification=_SPEC, workspace=self.workspace, model=model,
                trajectory=Trajectory(self.run),
                result_contract_path=_RESULT_CONTRACT_PATH,
                followups=1, environment_path=None, attempts=1,
            )
        self.assertIsNotNone(outcome["code"])
        self.assertTrue(outcome["phase_complete"])
        self.assertEqual(outcome["followups_remaining"], 0)
        self.assertEqual(outcome["followup_decision"]["action"], "followup")
        self.assertEqual(
            outcome["question_assessments"], _record_arguments([assessment])["questions"]
        )
        self.assertNotIn("write_file", model.tool_sets[0])
        self.assertIn("write_file", model.tool_sets[2])

    def test_interpretation_persists_a_portable_scientific_summary(self) -> None:
        """Keep the lineage handoff structured and local to the result folder."""
        assessment = {
            "question": "is the hypothesis supported?", "status": "settled",
            "conclusion": "yes", "evidence": "the measured result supports it",
            "missing": "",
        }
        verdict = {
            "status": "supported",
            "conclusion": "The measured result supports the hypothesis.",
            "evidence_paths": [_REPORT_PATH],
        }
        model = _Model([
            _evidence_record_reply(
                "record", _record_arguments(
                    [assessment], hypothesis_verdict=verdict,
                ),
            ),
            _text_reply(_interpretation_text()),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH,
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH,
            followups=0, environment_path=None,
        )

        summary_path = self.root / "results" / "old" / "agent_summary.yml"
        summary = yaml.safe_load(summary_path.read_text())
        self.assertEqual(summary["agent_summary_version"], "1.0.0")
        self.assertEqual(summary["experiment_code"], "old")
        self.assertIsNone(summary["follow_up_of"])
        self.assertEqual(
            summary["hypothesis"], "one system is faster under concurrency",
        )
        self.assertEqual(summary["verdict"]["status"], "supported")
        self.assertEqual(
            summary["verdict"]["evidence_paths"], ["report/index.md"],
        )
        self.assertEqual(outcome["agent_summary_path"], str(summary_path))

    def test_followup_author_receives_only_compact_ancestor_summaries(self) -> None:
        """Use lineage memory without reopening an ancestor's report."""
        parent_directory = self.root / "results" / "123"
        parent_directory.mkdir()
        parent_summary = {
            "agent_summary_version": "1.0.0",
            "experiment_code": "123",
            "follow_up_of": None,
            "hypothesis": "CPU is the limiting factor.",
            "verdict": {
                "status": "refuted",
                "conclusion": "Additional CPU did not improve throughput.",
                "evidence_paths": ["report/index.md"],
            },
            "technical_validity": {"failed_checks": 0, "scope": ""},
            "unresolved_question": "Is memory bandwidth limiting throughput?",
        }
        (parent_directory / "agent_summary.yml").write_text(
            yaml.safe_dump(parent_summary, sort_keys=False), encoding="utf-8",
        )
        specification = _SPEC.replace(
            "discriminates: [system, concurrency]",
            'discriminates: [system, concurrency]\nfollow_up_of: "123"',
        )
        assessment = {
            "question": "what causes degradation?", "status": "unresolved",
            "conclusion": "the cause remains unknown", "evidence": "latency rises",
            "missing": "a controlled memory intervention",
        }
        decision = {
            "action": "followup", "rationale": "a memory sweep is feasible",
            "unresolved_question": "is memory bandwidth limiting throughput?",
            "experiment_goal": "vary memory while holding CPU fixed",
            "target_queries": [], "full_workload_required": True,
            "cost_rationale": "The complete workload exposes the concurrency slope.",
        }
        model = _Model([
            _evidence_record_reply(
                "record", _record_arguments([assessment], follow_up=decision),
            ),
            _text_reply(_interpretation_text()),
            _tool_reply(
                ToolCall(
                    "catalog", "read_file",
                    {"path": "contracts/contract_catalog.yml"},
                ),
                ToolCall("write", "write_file", {
                    "path": self.path, "text": _followup_spec(),
                }),
                ToolCall("validate", "validate", {"path": self.path}),
            ),
            _text_reply("The follow-up validates."),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH,
            specification=specification, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH,
            followups=1, environment_path=None, attempts=1, dry_run=True,
        )

        author_prompt = "\n".join(
            str(message.get("content", ""))
            for exchange in model.messages
            for message in exchange
            if "Earlier ancestor summaries" in str(message.get("content", ""))
        )
        self.assertIn("CPU is the limiting factor", author_prompt)
        self.assertIn("Additional CPU did not improve throughput", author_prompt)
        self.assertEqual(outcome["ancestor_summaries_loaded"], 1)

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
            "target_queries": [], "full_workload_required": True,
            "cost_rationale": "The concurrency slope needs the full workload.",
        }
        model = _Model([
            _evidence_record_reply(
                "record", _record_arguments([assessment], follow_up=decision)
            ),
            _text_reply(_interpretation_text()),
            _tool_reply(
                ToolCall("catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("write", "write_file", {
                    "path": self.path, "text": _followup_spec(),
                }),
                ToolCall("validate", "validate", {"path": self.path}),
            ),
            _text_reply("The proposed follow-up validates."),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH,
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH,
            followups=1, environment_path=None, attempts=1, dry_run=True,
        )

        self.assertTrue(outcome["phase_complete"])
        self.assertIsNone(outcome["code"])
        self.assertEqual(outcome["validated_path"], self.path)
        self.assertNotIn("submit", model.tool_sets[2])

    def test_cost_aware_followup_rejects_a_broader_query_set(self) -> None:
        assessment = {
            "question": "why did Q2 time out?", "status": "unresolved",
            "conclusion": "the timeout is unexplained", "evidence": "Q2 failed",
            "missing": "a focused longer-timeout run",
        }
        decision = {
            "action": "followup", "rationale": "Q2 needs a controlled retry",
            "unresolved_question": "why did Q2 time out?",
            "experiment_goal": "retry only Q2 with a longer timeout",
            "target_queries": [2], "full_workload_required": False,
            "cost_rationale": "The other queries cannot resolve the Q2 timeout.",
        }
        focused_spec = _followup_spec(query=2)
        model = _Model([
            _evidence_record_reply(
                "record", _record_arguments([assessment], follow_up=decision)
            ),
            _text_reply(_interpretation_text()),
            _tool_reply(
                ToolCall("catalog", "read_file", {"path": "contracts/contract_catalog.yml"}),
                ToolCall("write-broad", "write_file", {
                    "path": self.path, "text": _followup_spec(query=5),
                }),
                ToolCall("validate-broad", "validate", {"path": self.path}),
            ),
            _tool_reply(
                ToolCall("write-focused", "write_file", {
                    "path": self.path, "text": focused_spec,
                }),
                ToolCall("validate-focused", "validate", {"path": self.path}),
            ),
            _text_reply("The focused follow-up validates."),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH, specification=_SPEC,
            workspace=self.workspace, model=model, trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH, followups=1,
            environment_path=None, attempts=2, dry_run=True,
        )

        self.assertEqual(outcome["validated_path"], self.path)
        validate_results = [
            event["result"] for event in map(
                json.loads,
                (self.run / "trajectory.jsonl").read_text().splitlines(),
            )
            if event.get("tool") == "validate"
        ]
        self.assertFalse(validate_results[0]["valid"])
        self.assertTrue(validate_results[1]["valid"])

    def test_followup_requires_exact_lineage_and_a_controlled_change(self) -> None:
        """Lineage metadata alone must not turn a repeated run into a follow-up."""
        assessment = {
            "question": "what causes degradation?", "status": "unresolved",
            "conclusion": "the cause is unknown", "evidence": "latency rises",
            "missing": "a controlled CPU intervention",
        }
        decision = {
            "action": "followup", "rationale": "a CPU intervention is feasible",
            "unresolved_question": "what causes degradation?",
            "experiment_goal": "vary CPU while holding the workload fixed",
            "target_queries": [], "full_workload_required": True,
            "cost_rationale": "The full workload is needed for its concurrency slope.",
        }
        wrong_lineage = _followup_spec(code="different")
        repeated = _SPEC.replace(
            "discriminates: [system, concurrency]",
            'discriminates: [system, concurrency]\nfollow_up_of: "old"',
        )
        model = _Model([
            _evidence_record_reply(
                "record", _record_arguments([assessment], follow_up=decision)
            ),
            _text_reply("The current result leaves the cause unresolved."),
            _tool_reply(
                ToolCall("catalog", "read_file", {
                    "path": "contracts/contract_catalog.yml",
                }),
                ToolCall("write-wrong", "write_file", {
                    "path": self.path, "text": wrong_lineage,
                }),
                ToolCall("validate-wrong", "validate", {"path": self.path}),
            ),
            _tool_reply(
                ToolCall("write-repeat", "write_file", {
                    "path": self.path, "text": repeated,
                }),
                ToolCall("validate-repeat", "validate", {"path": self.path}),
            ),
            _tool_reply(
                ToolCall("write-changed", "write_file", {
                    "path": self.path, "text": _followup_spec(),
                }),
                ToolCall("validate-changed", "validate", {"path": self.path}),
            ),
            _text_reply("The controlled follow-up validates."),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH, specification=_SPEC,
            workspace=self.workspace, model=model, trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH, followups=1,
            environment_path=None, attempts=3, dry_run=True,
        )

        self.assertEqual(outcome["validated_path"], self.path)
        validations = [
            event["result"] for event in map(
                json.loads, (self.run / "trajectory.jsonl").read_text().splitlines()
            ) if event.get("tool") == "validate"
        ]
        self.assertIn("follow_up_of must equal", validations[0]["errors"][0]["message"])
        self.assertIn("repeats its parent", validations[1]["errors"][0]["message"])
        self.assertTrue(validations[2]["valid"])

    def test_design_dry_run_withholds_submit_without_disarming_later_runs(self) -> None:
        """The withheld tool must be scoped to this run, not to the imported module."""
        model = _Model([
            _tool_reply(
                ToolCall("catalog", "read_file",
                         {"path": "contracts/contract_catalog.yml"}),
                ToolCall("write", "write_file", {"path": self.path, "text": _SPEC}),
                ToolCall("validate", "validate", {"path": self.path}),
            ),
            _text_reply("The design validates."),
        ])

        outcome = run_design(
            task="question", workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run), catalog_path="contracts/contract_catalog.yml",
            catalog_sha256="0" * 64, environment_path=None, attempts=1, dry_run=True,
        )

        self.assertIsNone(outcome["code"])
        self.assertEqual(outcome["validated_path"], self.path)
        self.assertNotIn("submit", model.tool_sets[0])
        # The module's own lists must be exactly as they were before this run.
        self.assertIn(
            "submit", {tool["function"]["name"] for tool in DESIGN_TOOLS})
        self.assertIn(
            "submit", {tool["function"]["name"] for tool in FOLLOWUP_AUTHOR_TOOLS})

    def test_initial_design_reads_the_catalog_before_writing(self) -> None:
        """Initial authoring must enforce the same contract boundary as a follow-up."""
        model = _Model([
            _tool_reply(ToolCall(
                "too-early", "write_file", {"path": self.path, "text": _SPEC}
            )),
            _tool_reply(
                ToolCall(
                    "catalog", "read_file",
                    {"path": "contracts/contract_catalog.yml"},
                ),
                ToolCall("write", "write_file", {"path": self.path, "text": _SPEC}),
                ToolCall("validate", "validate", {"path": self.path}),
            ),
            _text_reply("The design validates."),
        ])

        outcome = run_design(
            task="question", workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            catalog_path="contracts/contract_catalog.yml",
            catalog_sha256="0" * 64, environment_path=None,
            attempts=1, dry_run=True,
        )

        self.assertEqual(outcome["validated_path"], self.path)
        events = [
            json.loads(line)
            for line in (self.run / "trajectory.jsonl").read_text().splitlines()
        ]
        rejected = [
            event for event in events
            if event.get("tool") == "write_file"
            and "error" in event.get("result", {})
        ]
        self.assertEqual(len(rejected), 1)
        self.assertIn("complete catalog", rejected[0]["result"]["error"])

    def test_interpretation_cannot_finish_without_question_coverage(self) -> None:
        assessment = {
            "question": "is it faster?", "status": "settled", "conclusion": "no",
            "evidence": "latency is higher", "missing": "",
        }
        model = _Model([
            _text_reply("A premature answer."),
            _evidence_record_reply("record", _record_arguments([assessment])),
            _text_reply(_interpretation_text()),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH,
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH,
            followups=0, environment_path=None, attempts=1,
        )

        self.assertEqual(outcome["summary"], _interpretation_text())
        self.assertTrue(outcome["phase_complete"])
        events = [json.loads(line) for line in (self.run / "trajectory.jsonl").read_text().splitlines()]
        self.assertTrue(any(event["type"] == "completion_rejected" for event in events))

    def test_interpretation_requires_deterministic_comparison_quality(self) -> None:
        benchmarking = self.root / "results" / "old" / "report" / "benchmarking.md"
        benchmarking.write_text("""\
#### Per Phase
| phase | experiment_run | client | Geo Times [s] |
|:--|--:|--:|--:|
| postgresql-1-1-1 | 1 | 1 | 2.0 |
| postgresql-1-2-1 | 2 | 1 | 2.1 |
| postgresql-1-3-1 | 3 | 1 | 2.2 |

### Latency of Timer Execution [ms]
| Queries | postgresql-1-1-1-1-1 |
|:--|--:|
| First (TPC-H Q1) | 10 |
""")
        assessment = {
            "question": "is it stable?", "status": "settled",
            "conclusion": "yes", "evidence": "three similar repetitions",
            "missing": "", "evidence_paths": [_REPORT_PATH, str(benchmarking)],
        }
        quality = {
            "query_coverage": "complete",
            "whole_workload_throughput": "comparable",
            "suspect_repetitions": [],
        }
        accepted = _record_arguments([assessment], comparison_quality=quality)
        model = _Model([
            _evidence_record_reply("too-early", accepted),
            _tool_reply(ToolCall(
                "quality", "assess_comparison_quality", {"path": str(benchmarking)}
            )),
            _tool_reply(ToolCall("record", "record_interpretation", accepted)),
            _text_reply(_interpretation_text()),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH, specification=_SPEC,
            workspace=self.workspace, model=model, trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH, followups=0,
            environment_path=None,
        )

        self.assertEqual(outcome["comparison_quality"]["query_coverage"], "complete")
        events = [
            json.loads(line)
            for line in (self.run / "trajectory.jsonl").read_text().splitlines()
        ]
        rejected = [
            event for event in events
            if event.get("tool") == "record_interpretation"
            and "error" in event.get("result", {})
        ]
        self.assertEqual(len(rejected), 1)

    def test_interpretation_requires_report_contract_and_read_evidence(self) -> None:
        assessment = {
            "question": "is it faster?", "status": "settled", "conclusion": "yes",
            "evidence": "the measured latency is lower", "missing": "",
        }
        unread_path = "results/old/report/execution.md"
        (self.root / unread_path).write_text("### Per Phase\n\nMeasured evidence.\n")
        arguments = _record_arguments([{
            **assessment, "evidence_paths": [unread_path],
        }])
        model = _Model([
            _tool_reply(ToolCall(
                "too-early", "record_interpretation", arguments
            )),
            _tool_reply(
                ToolCall("report", "read_file", {"path": _REPORT_PATH}),
                ToolCall("still-early", "record_interpretation", arguments),
            ),
            _tool_reply(
                ToolCall(
                    "contract", "read_file", {"path": _RESULT_CONTRACT_PATH}
                ),
                ToolCall("unread", "record_interpretation", arguments),
            ),
            _tool_reply(
                ToolCall("evidence", "read_file", {"path": unread_path}),
                ToolCall("record", "record_interpretation", arguments),
            ),
            _text_reply(_interpretation_text()),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH, specification=_SPEC,
            workspace=self.workspace, model=model, trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH, followups=0,
            environment_path=None, attempts=1,
        )

        self.assertTrue(outcome["phase_complete"])
        events = [
            json.loads(line)
            for line in (self.run / "trajectory.jsonl").read_text().splitlines()
        ]
        rejected = [
            event for event in events
            if event.get("tool") == "record_interpretation"
            and "error" in event.get("result", {})
        ]
        self.assertEqual(len(rejected), 3)

    def test_failed_validity_checks_require_exact_count_and_scope(self) -> None:
        report = _REPORT.replace("failed: 0", "failed: 1")
        (self.root / _REPORT_PATH).write_text(report)
        assessment = {
            "question": "is latency usable?", "status": "settled",
            "conclusion": "yes", "evidence": "latency is present", "missing": "",
        }
        wrong_count = _record_arguments([assessment])
        missing_scope = _record_arguments([assessment], failed_checks=1)
        invalid_question = _record_arguments(
            [{**assessment, "validity": "invalid"}],
            failed_checks=1, scope="Monitoring failed; latency remained valid.",
        )
        accepted = _record_arguments(
            [assessment], failed_checks=1,
            scope="Monitoring failed; the latency check passed and is unaffected.",
        )
        model = _Model([
            _tool_reply(
                ToolCall("report", "read_file", {"path": _REPORT_PATH}),
                ToolCall(
                    "contract", "read_file", {"path": _RESULT_CONTRACT_PATH}
                ),
                ToolCall("wrong-count", "record_interpretation", wrong_count),
            ),
            _tool_reply(ToolCall(
                "missing-scope", "record_interpretation", missing_scope
            )),
            _tool_reply(ToolCall(
                "invalid-question", "record_interpretation", invalid_question
            )),
            _tool_reply(ToolCall("record", "record_interpretation", accepted)),
            _text_reply(_interpretation_text()),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH, specification=_SPEC,
            workspace=self.workspace, model=model, trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH, followups=0,
            environment_path=None, attempts=1,
        )

        self.assertEqual(outcome["validity_assessment"], accepted["validity"])
        events = [
            json.loads(line)
            for line in (self.run / "trajectory.jsonl").read_text().splitlines()
        ]
        rejected = [
            event for event in events
            if event.get("tool") == "record_interpretation"
            and "error" in event.get("result", {})
        ]
        self.assertEqual(len(rejected), 3)

    def test_settled_interpretation_cannot_list_missing_evidence(self) -> None:
        invalid = {
            "question": "what causes degradation?", "status": "settled",
            "conclusion": "memory starvation", "evidence": "throughput falls",
            "missing": "direct memory measurements",
        }
        corrected = {**invalid, "status": "partial"}
        model = _Model([
            _tool_reply(
                ToolCall("report", "read_file", {"path": _REPORT_PATH}),
                ToolCall(
                    "contract", "read_file", {"path": _RESULT_CONTRACT_PATH}
                ),
                ToolCall(
                    "invalid", "record_interpretation", _record_arguments([invalid])
                ),
            ),
            _tool_reply(ToolCall(
                "corrected", "record_interpretation", _record_arguments([corrected])
            )),
            _text_reply(_interpretation_text()),
        ])

        outcome = run_interpret(
            task="question", report_path=_REPORT_PATH,
            specification=_SPEC, workspace=self.workspace, model=model,
            trajectory=Trajectory(self.run),
            result_contract_path=_RESULT_CONTRACT_PATH,
            followups=0, environment_path=None, attempts=1,
        )

        self.assertEqual(
            outcome["question_assessments"], _record_arguments([corrected])["questions"]
        )
        events = [json.loads(line) for line in
                  (self.run / "trajectory.jsonl").read_text().splitlines()]
        rejected = [event for event in events
                    if event.get("tool") == "record_interpretation"
                    and "error" in event.get("result", {})]
        self.assertEqual(len(rejected), 1)

class PhaseTest(unittest.TestCase):
    def test_completed_design_labels_investigation_with_scale_and_model(self) -> None:
        """A validated design gains readable metadata without breaking resume."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "contracts").mkdir()
            (root / "contracts" / "contract_catalog.yml").write_text("version: 1\n")
            results = root / "results"
            results.mkdir()

            def design_phase(**kwargs):
                trajectory = kwargs["trajectory"]
                workspace = kwargs["workspace"]
                submitted = workspace.run_directory / "submitted-experiment.yml"
                submitted.write_text(_SPEC)
                workspace.status_dir.joinpath("42.json").write_text(json.dumps({
                    "code": "42",
                    "spec": str(submitted),
                    "log": str(workspace.run_directory / "bexhoma.log"),
                    "provenance": {
                        "contract_catalog.yml": str(
                            workspace.run_directory / "submitted-contract_catalog.yml"
                        ),
                    },
                }))
                trajectory.record(
                    "meta", phase="design", model="Qwen/Qwen3.8-27B-FP8",
                    budgets={"followups": 1},
                )
                trajectory.record("task", text="question")
                outcome = {
                    "summary": "design account", "code": "42",
                    "submitted_spec": str(submitted), "followups_remaining": 1,
                }
                trajectory.record("outcome", **outcome)
                return outcome

            argv = [
                "agent", "--model", "Qwen/Qwen3.8-27B-FP8",
                "--root", str(root), "--trajectories", "investigations",
                "--results", str(results), "--environment", "",
                "--status", "durable-status",
                "--task", "question",
            ]
            with (
                mock.patch("sys.argv", argv),
                mock.patch("agent.harness.agent.model_client.ChatModel"),
                mock.patch(
                    "agent.harness.agent.run_design", side_effect=design_phase
                ),
            ):
                self.assertEqual(agent_main(), 0)

            investigation = next((root / "investigations").iterdir())
            self.assertTrue(
                investigation.name.endswith("-sf1-Qwen-Qwen3.8-27B-FP8")
            )
            events = [
                json.loads(line)
                for line in (investigation / "trajectory.jsonl").read_text().splitlines()
            ]
            self.assertEqual(events[-2]["type"], "investigation_relocated")
            task, specification, code, followups = _carry_forward(
                investigation, root
            )
            self.assertEqual((task, specification, code, followups), (
                "question", _SPEC, "42", 1,
            ))
            status = json.loads(
                (root / "durable-status" / "42.json").read_text()
            )
            self.assertEqual(
                Path(status["spec"]),
                investigation / "phases" / "01-design" / "submitted-experiment.yml",
            )
            self.assertTrue(Path(status["log"]).is_relative_to(investigation))
            self.assertTrue(
                Path(status["provenance"]["contract_catalog.yml"]).is_relative_to(
                    investigation
                )
            )

    def test_an_unreachable_endpoint_reads_like_the_other_setup_errors(self) -> None:
        """A wrong --base-url is a misconfiguration, not a crash to decipher."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "contracts").mkdir()
            (root / "contracts" / "contract_catalog.yml").write_text("version: 1\n")
            (root / "results").mkdir()

            argv = [
                "agent", "--model", "fake", "--root", str(root),
                "--trajectories", "investigations", "--results", str(root / "results"),
                "--environment", "", "--task", "question",
                "--base-url", "http://127.0.0.1:9/v1",
            ]
            unreachable = ModelUnreachable("no answer from http://127.0.0.1:9/v1")
            stderr = io.StringIO()
            with (
                mock.patch("sys.argv", argv),
                mock.patch("agent.harness.agent.model_client.ChatModel"),
                mock.patch("agent.harness.agent.run_design", side_effect=unreachable),
                contextlib.redirect_stderr(stderr),
            ):
                # Exit 2 is what every other misconfiguration in main() returns.
                self.assertEqual(agent_main(), 2)

            self.assertIn("no answer from the model endpoint", stderr.getvalue())
            self.assertIn("http://127.0.0.1:9/v1", stderr.getvalue())
            # The abandoned phase stays auditable rather than vanishing.
            log = next((root / "investigations").glob("*/trajectory.jsonl"))
            events = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(events[-1]["type"], "aborted")

    def test_an_exhausted_context_window_is_reported_and_recorded(self) -> None:
        """A phase that outgrew the window must say so, not die mid-turn."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "contracts").mkdir()
            (root / "contracts" / "contract_catalog.yml").write_text("version: 1\n")
            (root / "results").mkdir()

            argv = [
                "agent", "--model", "fake", "--root", str(root),
                "--trajectories", "investigations", "--results", str(root / "results"),
                "--environment", "", "--task", "question", "--max-tokens", "32768",
            ]
            exhausted = ContextWindowExhausted("0 of 65536 tokens left for an answer")
            stderr = io.StringIO()
            with (
                mock.patch("sys.argv", argv),
                mock.patch("agent.harness.agent.model_client.ChatModel"),
                mock.patch("agent.harness.agent.run_design", side_effect=exhausted),
                contextlib.redirect_stderr(stderr),
            ):
                self.assertEqual(agent_main(), 2)

            self.assertIn("context window", stderr.getvalue())
            self.assertIn("32768", stderr.getvalue())
            log = next((root / "investigations").glob("*/trajectory.jsonl"))
            events = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(events[-1]["type"], "aborted")
            self.assertEqual(events[-1]["reason"], "context window exhausted")

    def test_cli_reuses_one_investigation_and_writes_one_result_answer(self) -> None:
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

            def interpret_phase(**kwargs):
                trajectory = kwargs["trajectory"]
                trajectory.record("meta", phase="interpret", report=str(report))
                trajectory.record("task", text="question")
                outcome = {
                    "summary": "# Result interpretation\n\nCurrent result only",
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
                "# Result interpretation\n\nCurrent result only\n",
            )
            phases = [
                json.loads(line).get("phase")
                for line in (investigation / "trajectory.jsonl").read_text().splitlines()
                if json.loads(line).get("type") == "meta"
            ]
            self.assertEqual(phases, ["design", "interpret"])

    def test_cli_interprets_an_exact_report_without_local_run_state(self) -> None:
        """The portable path needs only one result folder and model endpoint."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contracts = root / "contracts"
            contracts.mkdir()
            shutil.copyfile(
                Path("contracts/contract_catalog.yml"),
                contracts / "contract_catalog.yml",
            )
            results = root / "results"
            report = results / "42" / "report" / "index.md"
            report.parent.mkdir(parents=True)
            report.write_text("finished\n")
            (results / "42" / "experiment.yml").write_text(_SPEC)
            shutil.copyfile(
                Path("contracts/contract_result.yml"),
                results / "42" / "contract_result.yml",
            )

            def interpret_phase(**kwargs):
                self.assertEqual(kwargs["report_path"], str(report))
                self.assertEqual(
                    kwargs["task"], "one system is faster under concurrency"
                )
                self.assertEqual(kwargs["specification"], _SPEC)
                trajectory = kwargs["trajectory"]
                trajectory.record("meta", phase="interpret", report=str(report))
                return {
                    "summary": "One-result answer", "code": None,
                    "phase_complete": True,
                }

            argv = [
                "agent", "--phase", "interpret", "--model", "fake",
                "--root", str(root), "--trajectories", "investigations",
                "--environment", "", "--report", str(report),
            ]
            with (
                mock.patch("sys.argv", argv),
                mock.patch("agent.harness.agent.model_client.ChatModel"),
                mock.patch(
                    "agent.harness.agent.run_interpret", side_effect=interpret_phase
                ),
            ):
                self.assertEqual(agent_main(), 0)

            investigation = next((root / "investigations").iterdir())
            self.assertEqual(
                (investigation / "answer.md").read_text(), "One-result answer\n"
            )

    def test_only_completed_interpretation_creates_answer(self) -> None:
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
                investigation, trajectory, 2, "interpret", "one result", True
            )
            self.assertEqual(final_report.read_text(), "one result\n")
            self.assertEqual(final_answer, investigation / "answer.md")
            self.assertEqual(final_answer.read_text(), "one result\n")

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
            {
                "read_file", "assess_comparison_quality", "record_interpretation",
            },
        )
        self.assertEqual(
            names(FOLLOWUP_AUTHOR_TOOLS),
            {"read_file", "write_file", "validate", "submit"},
        )

    def test_concise_question_keeps_operational_context_out_of_user_message(self) -> None:
        question = "At SF10, which system handles concurrent reporting better?"

        messages = prompts.design_messages(
            task=question, catalog_path="contracts/contract_catalog.yml",
            environment_path="environment.yml", inbox="inbox",
            attempts=3, followups=1,
        )

        self.assertEqual(messages[1], {"role": "user", "content": question})
        self.assertIn("contracts/contract_catalog.yml", messages[0]["content"])
        self.assertIn("environment.yml", messages[0]["content"])
        self.assertIn("no shell", messages[0]["content"])

    def test_withholding_submit_leaves_every_phase_tool_list_intact(self) -> None:
        """A dry run must not take submit away from the phases that still need it."""
        def names(schemas):
            return {tool["function"]["name"] for tool in schemas}

        # Two names for one list would let a dry run disarm a later real run.
        self.assertIsNot(FOLLOWUP_AUTHOR_TOOLS, DESIGN_TOOLS)

        withheld = without_submit(DESIGN_TOOLS)

        self.assertNotIn("submit", names(withheld))
        self.assertIn("submit", names(DESIGN_TOOLS))
        self.assertIn("submit", names(FOLLOWUP_AUTHOR_TOOLS))

    def test_result_root_comes_from_the_config_bexhoma_reads(self) -> None:
        """Agent and Bexhoma must agree on the folder without a second setting."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "cluster.config"

            config.write_text("{'benchmarker': {'resultfolder': 'benchmarks'}}")
            self.assertEqual(default_result_root(root), root / "benchmarks")

            config.write_text("{'benchmarker': {'resultfolder': '/srv/benchmarks'}}")
            self.assertEqual(default_result_root(root), Path("/srv/benchmarks"))

            # Bexhoma normalises Windows paths, so this side has to as well.
            config.write_text("{'benchmarker': {'resultfolder': 'C:\\\\bench'}}")
            self.assertEqual(default_result_root(root), Path("/bench"))

    def test_result_root_is_absent_rather_than_guessed(self) -> None:
        """No configuration must not silently become somebody's home directory."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIsNone(default_result_root(root))

            (root / "cluster.config").write_text("{'benchmarker': {}}")
            self.assertIsNone(default_result_root(root))

            (root / "cluster.config").write_text("not a python literal {")
            self.assertIsNone(default_result_root(root))

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
            task, specification, code, followups = _carry_forward(
                run, Path(directory)
            )
            self.assertEqual(
                (task, specification, code, followups),
                ("question", "immutable\n", "42", 1),
            )

    def test_interpret_prompt_is_scoped_to_one_result(self) -> None:
        messages = prompts.interpret_messages(
            task="Which configuration is faster?",
            report_path="results/42/report/index.md",
            result_contract_path="results/42/contract_result.yml",
            specification=_SPEC,
        )

        system = messages[0]["content"]
        self.assertIn("read this one result", system)
        self.assertIn("answer_contract", system)
        self.assertIn("Discuss only this experiment", system)
        self.assertNotIn("previous experiment", messages[1]["content"])


class ChatModelTest(unittest.TestCase):
    @staticmethod
    def _model(max_tokens: int = 100, window: Any = None, usage: Any = None) -> ChatModel:
        """Build a client whose server answers with one canned completion.

        :param max_tokens: Configured per-turn ceiling.
        :param window: ``max_model_len`` the served model publishes, or ``None``
            to publish none at all.
        :param usage: Usage payload the server reports, if any.
        """
        message = mock.Mock()
        message.content = "answer"
        message.tool_calls = []
        message.model_dump.return_value = {
            "role": "assistant", "content": "answer", "reasoning": "hidden",
        }
        reported = mock.Mock()
        reported.model_dump.return_value = usage or {"completion_tokens": 12}
        response = mock.Mock(choices=[mock.Mock(message=message)], usage=reported)
        model = ChatModel.__new__(ChatModel)
        model.model = "fake"
        model.base_url = "http://fake/v1"
        model.temperature = 0.0
        model.max_tokens = max_tokens
        model._context_window = None
        model._context_window_asked = False
        model._counted_messages = 0
        model._counted_prompt_tokens = 0
        model._sleep = mock.Mock()
        model._client = mock.Mock()
        model._client.chat.completions.create.return_value = response
        served = mock.Mock(id="fake")
        if window is None:
            del served.max_model_len
        else:
            served.max_model_len = window
        model._client.models.list.return_value = mock.Mock(data=[served])
        return model

    @staticmethod
    def _rate_limited() -> RateLimitError:
        """Build the refusal a metered endpoint raises, with no retry-after header."""
        response = mock.Mock(headers={})
        return RateLimitError("rate limit exceeded", response=response, body=None)

    def test_a_metered_endpoint_refusing_a_turn_is_waited_out(self) -> None:
        """A per-minute quota clears on its own; losing the phase to it does not."""
        model = self._model()
        answer = model._client.chat.completions.create.return_value
        model._client.chat.completions.create.side_effect = [
            self._rate_limited(), self._rate_limited(), answer,
        ]

        reply = model.reply([{"role": "user", "content": "question"}])

        self.assertEqual(reply.text, "answer")
        self.assertEqual(model._sleep.call_count, 2)
        first, second = (call.args[0] for call in model._sleep.call_args_list)
        self.assertGreater(second, first)

    def test_an_endpoint_that_never_stops_refusing_is_reported_as_unreachable(self) -> None:
        """Waiting forever would hide a quota that is exhausted, not merely busy."""
        model = self._model()
        model._client.chat.completions.create.side_effect = self._rate_limited()

        with self.assertRaises(ModelUnreachable):
            model.reply([{"role": "user", "content": "question"}])

    def test_a_window_published_under_the_hosted_name_is_honoured(self) -> None:
        """vLLM calls it max_model_len; a hosted API calls it max_context_length."""
        model = self._model(max_tokens=32768)
        served = model._client.models.list.return_value.data[0]
        served.max_context_length = 2000

        model.reply([{"role": "user", "content": "question"}])

        reserved = model._client.chat.completions.create.call_args.kwargs["max_tokens"]
        self.assertLessEqual(reserved, 2000)

    def test_current_reasoning_field_is_logged_but_not_replayed(self) -> None:
        model = self._model()

        reply = model.reply([{"role": "user", "content": "question"}])

        self.assertEqual(reply.reasoning, "hidden")
        self.assertNotIn("reasoning", reply.message)
        request = model._client.chat.completions.create.call_args.kwargs
        self.assertNotIn("extra_body", request)

    def test_a_turn_reserves_only_what_the_context_window_leaves(self) -> None:
        """Asking for a fixed ceiling on a full conversation is what overflows."""
        model = self._model(max_tokens=32768, window=2000)

        model.reply([{"role": "user", "content": "question"}])

        reserved = model._client.chat.completions.create.call_args.kwargs["max_tokens"]
        self.assertLess(reserved, model.max_tokens)
        self.assertLessEqual(reserved, 2000)
        self.assertGreater(reserved, 0)

    def test_a_server_without_a_published_window_keeps_the_configured_ceiling(self) -> None:
        """Only a server that states its window may narrow the per-turn ceiling."""
        model = self._model(max_tokens=256)

        model.reply([{"role": "user", "content": "question"}])

        request = model._client.chat.completions.create.call_args.kwargs
        self.assertEqual(request["max_tokens"], 256)

    def test_a_conversation_with_no_room_left_stops_before_the_server_refuses(self) -> None:
        """A refused request would end the phase with no record of why."""
        model = self._model(max_tokens=32768, window=2000)

        with self.assertRaises(ContextWindowExhausted):
            model.reply([{"role": "user", "content": "filler " * 1000}])

        model._client.chat.completions.create.assert_not_called()

    def test_the_next_turn_is_sized_from_the_count_the_server_reported(self) -> None:
        """A local estimate of a long conversation would drift; the server's count does not."""
        model = self._model(max_tokens=32768, window=8000,
                            usage={"prompt_tokens": 6000, "completion_tokens": 12})
        messages: list[dict[str, Any]] = [{"role": "user", "content": "question"}]

        model.reply(messages)
        messages.append({"role": "assistant", "content": "answer"})
        model.reply(messages)

        reserved = model._client.chat.completions.create.call_args.kwargs["max_tokens"]
        self.assertLess(reserved, 8000 - 6000)


if __name__ == "__main__":
    unittest.main()
