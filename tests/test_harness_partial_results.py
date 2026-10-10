"""
Tests for how the agent harness treats a result whose queries failed in some
phases: claims from complete phases only (conservative), phase-local validity
scope, the disclosure rule, and the repair turn for a record refused on the
last turn.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent.harness import agent as agent_module
from agent.harness import tools
from agent.harness.agent import Trajectory, _converse, _InterpretationGate
from agent.harness.model_client import Reply, ToolCall

_SPEC = """\
mode: run
title: concurrency
hypothesis: throughput rises with concurrency
discriminates: [concurrency]
workload:
  name: tpch
  params: {scaling_factor: 1, active_queries: [1, 18]}
  rounds: [1, 2]
  repetitions: 3
systems:
  - {name: PgDuckDB, profile: analytical-ssd}
resources:
  cpu: {request: 4, limit: 4}
  memory: {request: 8Gi, limit: 8Gi}
"""

_Q1 = "Pricing Summary Report (TPC-H Q1)"
_Q18 = "Large Volume Customer (TPC-H Q18)"


def _report(incomplete: dict[str, int]) -> str:
    """A benchmarking.md of 3 runs × 2 levels; ``incomplete`` maps a phase to
    how many of its pods failed Q18."""
    phases = [(run, client, pods) for run in (1, 2, 3) for client, pods in ((1, 1), (2, 2))]
    completion = [
        "#### Query Completion per Phase", "",
        f"| phase | pods | {_Q1} | {_Q18} | complete |", "|:--|--:|:--|:--|:--|",
    ]
    complete_rows = []
    errors = []
    for run, client, pods in phases:
        phase = f"pgduckdb-1-{run}-{client}"
        failed = incomplete.get(phase, 0)
        completion.append(
            f"| {phase} | {pods} | {pods}/{pods} | {pods - failed}/{pods} | {'no' if failed else 'yes'} |")
        if failed:
            errors.append(f"| {phase}-1-1 | 0.00 | 1.00 |")
        else:
            geo, throughput = (10.0, 100.0) if pods == 1 else (12.0, 180.0)
            complete_rows.append(
                f"| {phase} | {phase} | {run} | {client} | {pods} | {geo} | {throughput} |")
    complete_connections = [
        f"pgduckdb-1-{run}-{client}-1-{pod}"
        for run, client, pods in phases if not incomplete.get(f"pgduckdb-1-{run}-{client}")
        for pod in range(1, pods + 1)
    ]
    latency = [
        "### Latency of Timer Execution [ms] (Complete Phases Only)",
        "| Queries | " + " | ".join(complete_connections) + " |",
        "|:--|" + "--:|" * len(complete_connections),
        f"| {_Q1} | " + " | ".join("100.0" if c.split("-")[3] == "1" else "150.0" for c in complete_connections) + " |",
        f"| {_Q18} | " + " | ".join("200.0" if c.split("-")[3] == "1" else "400.0" for c in complete_connections) + " |",
    ]
    lines = [
        "### Benchmarking", "", "#### Per Connection", "", "No rows: queries failed.", "",
        "#### Per Phase", "", "No rows: queries failed.", "",
    ] + completion + ["", "#### Per Phase (Complete Phases Only)", "",
                      "| | phase | experiment_run | client | pod_count | Geo Times [s] | Throughput@Size |",
                      "|:--|:--|--:|--:|--:|--:|--:|"] + complete_rows + [
        "", "### Latency of Timer Execution [ms]", "No rows: queries failed.", ""] + latency + [
        "", "### Errors (failed queries)", "", f"| | {_Q1} | {_Q18} |", "|:--|--:|--:|"] + errors
    return "\n".join(lines) + "\n"


_INDEX = """\
### Tests

| status | label |
|---|---|
| failed | No SUT container restarts |
| failed | SQL errors |
| failed | Geo Times [s] contains 0 or NaN |
"""


def _assess(incomplete: dict[str, int], report: str | None = None) -> dict:
    return tools._assess_comparison_quality(report or _report(incomplete), _SPEC, _INDEX, None)


class CompletePhaseClaimsTest(unittest.TestCase):
    """Claims from complete phases only, when every level kept two repetitions."""

    def test_one_failed_run_per_level_still_yields_scoped_claims(self) -> None:
        quality = _assess({"pgduckdb-1-3-2": 1})
        characterization = quality["result_characterization"]
        self.assertEqual(characterization["scope"], "complete_phases_only")
        sweeps = characterization["ordered_sweeps"]
        self.assertEqual({sweep["metric"] for sweep in sweeps}, {"Geo Times [s]", "Throughput@Size"})
        for sweep in sweeps:
            self.assertEqual(sweep["scope"], "complete_phases_only")
            self.assertEqual(sweep["completion_by_level"], {"1": "3/3", "2": "2/3"})
            self.assertEqual([value["repetitions"] for value in sweep["values"]], [3, 2])
        self.assertEqual(characterization["excluded_phases"], ["pgduckdb-1-3-2"])
        self.assertEqual(characterization["incomplete_phases"],
                         [{"phase": "pgduckdb-1-3-2", "failed_queries": [_Q18]}])

    def test_a_level_left_with_one_repetition_yields_no_claim(self) -> None:
        quality = _assess({"pgduckdb-1-2-2": 1, "pgduckdb-1-3-2": 1})
        characterization = quality["result_characterization"]
        self.assertEqual(characterization["ordered_sweeps"], [])
        self.assertIn("concurrency", characterization["unsupported_factors"])
        self.assertIn("Fewer than 2 complete repetitions", characterization["unusable_reason"])

    def test_a_report_without_completion_table_keeps_the_old_rule(self) -> None:
        report = _report({"pgduckdb-1-3-2": 1}).replace("#### Query Completion per Phase", "#### Something Else")
        characterization = _assess({}, report)["result_characterization"]
        self.assertEqual(characterization["ordered_sweeps"], [])
        self.assertNotIn("scope", characterization)
        self.assertIn("Planned queries failed", characterization["unusable_reason"])

    def test_query_evidence_places_failures_without_pooled_table(self) -> None:
        evidence = _assess({"pgduckdb-1-3-2": 1})["query_evidence"]
        self.assertEqual(evidence["failures"], [{
            "phase": "pgduckdb-1-3-2", "configuration": "pgduckdb-1",
            "concurrency": 2, "query": 18, "errors": 1.0,
        }])


class CompletePhaseQueryEvidenceTest(unittest.TestCase):
    """Per-query timings come from the complete phases when the pooled table is empty."""

    def test_timings_per_level_with_completion(self) -> None:
        evidence = _assess({"pgduckdb-1-3-2": 1})["query_evidence"]
        self.assertEqual(evidence["source_section"], "### Latency of Timer Execution [ms] (Complete Phases Only)")
        self.assertEqual(evidence["evidence_scope"], "complete_phases_only")
        self.assertEqual(evidence["queries"], [1, 18])
        self.assertEqual(evidence["excluded_phases"], ["pgduckdb-1-3-2"])
        by_level = {entry["concurrency"]: entry for entry in evidence["latency_by_context"]}
        self.assertEqual(by_level[1]["completion"], "3/3")
        self.assertEqual(by_level[2]["completion"], "2/3")
        self.assertEqual(by_level[2]["queries"]["18"]["mean_ms"], 400.0)
        self.assertEqual(by_level[2]["queries"]["18"]["repetitions"], 2)

    def test_a_level_with_one_complete_repetition_is_dropped(self) -> None:
        evidence = _assess({"pgduckdb-1-2-2": 1, "pgduckdb-1-3-2": 1})["query_evidence"]
        self.assertEqual([entry["concurrency"] for entry in evidence["latency_by_context"]], [1])
        self.assertEqual(evidence["thin_contexts"],
                         [{"configuration": "pgduckdb-1", "concurrency": 2, "completion": "1/3"}])

    def test_without_complete_latency_table_no_timings(self) -> None:
        report = _report({"pgduckdb-1-3-2": 1}).replace("(Complete Phases Only)\n| Queries", "(Other)\n| Queries")
        evidence = _assess({}, report)["query_evidence"]
        self.assertEqual(evidence["latency_by_context"], [])
        self.assertNotIn("evidence_scope", evidence)


class PhaseLocalValidityTest(unittest.TestCase):
    """Query-failure checks are located; every other failure stays global."""

    def test_query_failures_are_located_restarts_are_not(self) -> None:
        scope = _assess({"pgduckdb-1-3-2": 1})["validity_scope"]
        self.assertEqual(scope["benchmark_phase_count"], 6)
        self.assertEqual(scope["incomplete_phases"], ["pgduckdb-1-3-2"])
        self.assertEqual(len(scope["complete_phases"]), 5)
        details = {detail["failed_check"]: detail for detail in scope["details"]}
        self.assertEqual(details["SQL errors"]["affected_phases"], ["pgduckdb-1-3-2"])
        self.assertEqual(details["Geo Times [s] contains 0 or NaN"]["affected_phases"], ["pgduckdb-1-3-2"])
        self.assertEqual(details["No SUT container restarts"]["affected_phases"], [])
        self.assertTrue(scope["performance_metrics_affected"])


class DisclosureGateTest(unittest.TestCase):
    """A record using complete-phase claims must name the incomplete phases."""

    def _gate(self) -> _InterpretationGate:
        gate = _InterpretationGate.__new__(_InterpretationGate)
        gate.failed_checks = 3
        gate.report = Path("/r/report/index.md")
        gate._unread = mock.Mock(return_value=[])
        gate._cited = mock.Mock(return_value=gate.report)
        gate.comparison_quality = _assess({"pgduckdb-1-3-2": 1})
        return gate

    def _validity(self, scope: str) -> dict:
        return {"validity": {"scope": scope, "evidence_paths": ["report/index.md"]}}

    def test_unnamed_incomplete_phase_is_refused(self) -> None:
        error = self._gate()._validity_error(self._validity("Queries failed in run 3."))
        self.assertEqual(error["missing"], ["pgduckdb-1-3-2"])

    def test_named_incomplete_phase_passes(self) -> None:
        self.assertIsNone(self._gate()._validity_error(
            self._validity("Q18 failed in phase pgduckdb-1-3-2; claims use the other phases.")))

    def test_claims_carry_scope_into_the_record(self) -> None:
        claims = agent_module._checkable_result_claims(
            self._gate().comparison_quality["result_characterization"])
        self.assertTrue(all(c["scope"] == "complete_phases_only" for c in claims["ordered_sweeps"]))
        self.assertEqual(claims["ordered_sweeps"][0]["completion_by_level"], {"1": "3/3", "2": "2/3"})


class _Model:
    model = "fake"

    def __init__(self, replies: list[Reply]) -> None:
        self.replies = replies

    def reply(self, _messages, tools=None):
        return self.replies.pop(0)


def _call(identifier: str) -> Reply:
    return Reply("", "", [ToolCall(identifier, "record", {})], {"role": "assistant", "content": ""}, {})


class RepairTurnTest(unittest.TestCase):
    """A record refused on the last turn gets a bounded turn to repair it."""

    _SCHEMAS = [{"type": "function", "function": {"name": "record", "parameters": {}}}]

    def _run(self, results: list[dict], replies: list[Reply], repair_turns: int) -> tuple[str, Path]:
        directory = Path(tempfile.mkdtemp())
        handler = mock.Mock(side_effect=results)
        summary, _, _ = _converse(
            [], _Model(replies), workspace=None, trajectory=Trajectory(directory),
            tool_schemas=self._SCHEMAS, max_turns=1,
            done_when=lambda name, result: result.get("recorded") is True,
            tool_handler=handler, require_done=True,
            repair_tool="record", repair_turns=repair_turns,
        )
        return summary, directory

    @staticmethod
    def _events(directory: Path) -> list[dict]:
        return [json.loads(line) for line in (directory / "trajectory.jsonl").read_text().splitlines()]

    def test_refusal_on_last_turn_is_repaired(self) -> None:
        summary, directory = self._run(
            [{"error": "malformed"}, {"recorded": True}],
            [_call("a"), _call("b"), Reply("done", "", [], {"role": "assistant", "content": "done"}, {})],
            repair_turns=4,
        )
        self.assertEqual(summary, "done")
        self.assertEqual([e["type"] for e in self._events(directory)].count("repair_turn_granted"), 1)

    def test_repair_turns_are_bounded(self) -> None:
        summary, directory = self._run(
            [{"error": "malformed"}] * 3, [_call("a"), _call("b"), _call("c")], repair_turns=2)
        self.assertEqual(summary, "")
        self.assertEqual([e["type"] for e in self._events(directory)].count("repair_turn_granted"), 2)

    def test_without_repair_turns_the_phase_ends(self) -> None:
        summary, directory = self._run([{"error": "malformed"}], [_call("a")], repair_turns=0)
        self.assertEqual(summary, "")
        self.assertNotIn("repair_turn_granted", [e["type"] for e in self._events(directory)])


if __name__ == "__main__":
    unittest.main()
