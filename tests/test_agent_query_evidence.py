"""Verify compact evidence for query-specific benchmark conclusions."""

from __future__ import annotations

import unittest

from agent.harness.tools import _assess_comparison_quality

__all__ = ["QueryEvidenceTest"]


def _report() -> str:
    """Build a synthetic report with a query crossover and localized failures."""
    phase_rows = []
    connections = []
    query_times = {1: [], 13: []}
    error_rows = []
    for configuration in ("pg-duck-1", "pg-duck-2", "postgres-1", "postgres-2"):
        for repetition in (1, 2):
            for client, concurrency in ((1, 1), (3, 2)):
                phase = f"{configuration}-{repetition}-{client}"
                phase_rows.append(f"| {phase} | {repetition} | {client} | {concurrency} | 10 |")
                for stream in range(1, concurrency + 1):
                    connection = f"{phase}-1-{stream}"
                    connections.append(connection)
                    fast_query = 7 if configuration == "postgres-2" else 12
                    query_times[1].append(str(fast_query + repetition))
                    query_times[13].append("2" if configuration.startswith("pg-duck") else "10")
                    if configuration.startswith("postgres") and client == 3:
                        error_rows.append(f"| {connection} | 0 | 0 | 1 |")
    return "\n".join([
        "#### Per Phase", "",
        "| phase | experiment_run | client | pod_count | Geo Times [s] |",
        "|---|---|---|---|---|", *phase_rows, "",
        "### Latency of Timer Execution [ms]",
        "| Queries | " + " | ".join(connections) + " |",
        "|---|" + "---|" * len(connections),
        *(f"| Query (TPC-H Q{query}) | " + " | ".join(values) + " |"
          for query, values in query_times.items()), "",
        "### Errors (failed queries)", "",
        "| connection | Query (TPC-H Q1) | Query (TPC-H Q13) | Query (TPC-H Q18) |",
        "|---|---|---|---|", *error_rows,
    ])


class QueryEvidenceTest(unittest.TestCase):
    """Keep configurations, workload subsets, and failure locations explicit."""

    def test_component_evidence_preserves_crossover_and_repetitions(self) -> None:
        """An overall ranking must not erase opposite query-level rankings."""
        assessment = _assess_comparison_quality(_report())
        evidence = assessment["query_evidence"]
        self.assertEqual(evidence["queries"], [1, 13])
        contexts = {
            (row["configuration"], row["concurrency"]): row
            for row in evidence["latency_by_context"]
        }
        self.assertEqual(len(contexts), 8)
        postgres = contexts[("postgres-2", 2)]["queries"]
        duck = contexts[("pg-duck-2", 2)]["queries"]
        self.assertLess(postgres["1"]["mean_ms"], duck["1"]["mean_ms"])
        self.assertGreater(postgres["13"]["mean_ms"], duck["13"]["mean_ms"])
        self.assertEqual(postgres["1"], {
            "mean_ms": 8.5, "min_ms": 8.0, "max_ms": 9.0, "repetitions": 2,
        })
        self.assertEqual(assessment["whole_workload_throughput"], "not_comparable")
        self.assertEqual(assessment["result_characterization"]["ordered_sweeps"], [])

    def test_failures_keep_the_actual_concurrency_and_phase(self) -> None:
        """A failure at one load must not be reported at every load."""
        failures = _assess_comparison_quality(_report())["query_evidence"]["failures"]
        self.assertEqual(len(failures), 4)
        self.assertEqual({row["concurrency"] for row in failures}, {2})
        self.assertEqual({row["query"] for row in failures}, {18})
        self.assertEqual(sum(row["errors"] for row in failures), 8)
        self.assertIn("postgres-1-1-3", {row["phase"] for row in failures})

    def test_invalid_or_failed_query_is_not_summarized_as_successful(self) -> None:
        """Reject a partial numeric row and an inconsistent success/error row."""
        for invalid in ("NaN", "inf", "0", "-1", "missing"):
            with self.subTest(invalid=invalid):
                report = _report().replace("| 13 |", f"| {invalid} |", 1)
                evidence = _assess_comparison_quality(report)["query_evidence"]
                self.assertEqual(evidence["queries"], [13])
                self.assertEqual(evidence["omitted_queries"], [1])
        report = _report().replace("| 0 | 0 | 1 |", "| 1 | 0 | 1 |", 1)
        evidence = _assess_comparison_quality(report)["query_evidence"]
        self.assertEqual(evidence["queries"], [13])
        self.assertEqual(evidence["omitted_queries"], [1])

    def test_missing_connection_prevents_a_partial_phase_mean(self) -> None:
        """One surviving stream must not stand in for an entire phase."""
        report = _report().replace("pg-duck-1-1-3-1-2", "unrecognized", 1)
        evidence = _assess_comparison_quality(report)["query_evidence"]
        self.assertEqual(evidence["latency_by_context"], [])
        self.assertIn("unavailable", evidence["reason"])

    def test_no_query_table_leaves_existing_assessment_available(self) -> None:
        """A benchmark without per-query timings needs no invented breakdown."""
        report = _report().split("### Latency")[0]
        evidence = _assess_comparison_quality(report)["query_evidence"]
        self.assertEqual(evidence["latency_by_context"], [])
        self.assertEqual(evidence["queries"], [])


if __name__ == "__main__":
    unittest.main()
