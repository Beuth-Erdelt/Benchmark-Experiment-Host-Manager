"""
Unit tests for DBMSBenchmarker query completion: the per-phase completion
matrix, the complete-phases table, the notes that explain the pooled
totals, and the per-phase failure events.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest
from unittest import mock

import pandas as pd

from bexhoma import report_writer
from bexhoma.benchmarks.tpch import TPCH
from bexhoma.evaluators.dbmsbenchmarker import DbmsBenchmarkerEvaluator

_PHASES = {"c-1-1-1-1": "c-1-1", "c-1-2-1-1": "c-1-2", "c-1-2-1-2": "c-1-2"}
#: Inspector query indices (0-based) each connection completed: Q1 and Q18 are
#: active; one pod of phase c-1-2 failed Q18.
_SUCCESSFUL = {"c-1-1-1-1": [0, 17], "c-1-2-1-1": [0, 17], "c-1-2-1-2": [0]}


def _completion() -> pd.DataFrame:
    return pd.DataFrame(
        {"phase": ["c-1-1", "c-1-2", "c-1-2"], "Q1": [True, True, True], "Q18": [True, True, False]},
        index=list(_PHASES),
    )


def _evaluator() -> DbmsBenchmarkerEvaluator:
    evaluator = DbmsBenchmarkerEvaluator.__new__(DbmsBenchmarkerEvaluator)
    evaluator.evaluation = mock.Mock()
    evaluator.evaluation.get_survey_successful.side_effect = (
        lambda timername, dbms_filter=(): _SUCCESSFUL[dbms_filter[0]] if dbms_filter else []
    )
    evaluator.get_connection_phases = mock.Mock(return_value=dict(_PHASES))
    evaluator.get_total_errors = mock.Mock(return_value=pd.DataFrame(columns=["Q1", "Q18"]))
    return evaluator


class EvaluatorCompletionTest(unittest.TestCase):
    """Completion is judged per connection, then counted per phase."""

    def test_completion_per_connection(self) -> None:
        completion = _evaluator().get_query_completion()
        pd.testing.assert_frame_equal(completion, _completion())

    def test_completion_per_phase_counts_pods(self) -> None:
        counts = DbmsBenchmarkerEvaluator.get_query_completion_per_phase(_evaluator(), _completion())
        self.assertEqual(counts.loc["c-1-2"].to_dict(), {"pods": 2, "Q1": 2, "Q18": 1})

    def test_complete_phases_pool_only_their_connections(self) -> None:
        evaluator = _evaluator()
        evaluator.get_df_benchmarking = mock.Mock(return_value=pd.DataFrame())
        evaluator.get_summary_benchmark_per_phase_complete(_completion())
        evaluator.get_df_benchmarking.assert_called_once_with(dbms_filter=["c-1-1-1-1"])

    def test_no_complete_phase_gives_empty_table(self) -> None:
        evaluator = _evaluator()
        evaluator.get_df_benchmarking = mock.Mock()
        completion = _completion().assign(Q18=False)
        self.assertTrue(evaluator.get_summary_benchmark_per_phase_complete(completion).empty)
        evaluator.get_df_benchmarking.assert_not_called()

    def test_pooled_queries_are_labels(self) -> None:
        evaluator = _evaluator()
        self.assertEqual(evaluator.get_pooled_queries(), [])
        evaluator.evaluation.get_survey_successful.side_effect = None
        evaluator.evaluation.get_survey_successful.return_value = [0]
        self.assertEqual(evaluator.get_pooled_queries(), ["Q1"])


def _benchmark(pooled: list[str]) -> TPCH:
    benchmark = TPCH(SF="1")
    evaluator = mock.Mock()
    evaluator.get_query_completion.return_value = _completion()
    evaluator.get_query_completion_per_phase.side_effect = (
        lambda completion: DbmsBenchmarkerEvaluator.get_query_completion_per_phase(None, completion)
    )
    evaluator.get_pooled_queries.return_value = pooled
    evaluator.get_total_errors.side_effect = lambda query_titles=False: pd.DataFrame(
        columns=["Title 1", "Title 18"] if query_titles else ["Q1", "Q18"])
    evaluator.get_summary_benchmark_per_phase_complete.return_value = pd.DataFrame(
        {"phase": ["c-1-1"], "Geo Times [s]": [1.0]}, index=["c-1-1"])
    benchmark.evaluator = evaluator
    return benchmark


class ResultsNotesTest(unittest.TestCase):
    """The pooled tables say what they leave out instead of staying silent."""

    def test_empty_table_names_the_failed_queries(self) -> None:
        note = _benchmark(pooled=[])._results_notes(is_empty=True)[0]
        self.assertTrue(note.startswith("No rows:"))
        self.assertIn("Q18 failed in 1 of 3 connections", note)
        self.assertIn("Per Phase (Complete Phases Only)", note)

    def test_partial_pool_is_stated(self) -> None:
        note = _benchmark(pooled=["Q1"])._results_notes(is_empty=False)[0]
        self.assertIn("cover 1 of 2 active queries", note)

    def test_full_pool_needs_no_note(self) -> None:
        self.assertEqual(_benchmark(pooled=["Q1", "Q18"])._results_notes(is_empty=False), [])

    def test_note_follows_a_table_after_a_blank_line(self) -> None:
        benchmark = _benchmark(pooled=["Q1"])
        per_connection, per_phase = benchmark._results_sections(pd.DataFrame(), pd.DataFrame({"a": [1]}))
        # Some queries are pooled, so an empty table is empty for another reason: no claim.
        self.assertIsNone(per_connection.lines)
        self.assertEqual(per_phase.lines[0], "")
        self.assertIn("cover 1 of 2", per_phase.lines[1])


class CompletionSectionsTest(unittest.TestCase):
    """Matrix always, complete-phases table only when some phase is incomplete."""

    def test_matrix_and_complete_phases(self) -> None:
        matrix, complete = _benchmark(pooled=["Q1"])._build_completion_sections(is_multitenant=False)
        self.assertEqual(matrix.heading, "Query Completion per Phase")
        self.assertEqual(matrix.dataframe.loc["c-1-2"].to_dict(),
                         {"pods": 2, "Title 1": "2/2", "Title 18": "1/2", "complete": "no"})
        self.assertEqual(complete.heading, "Per Phase (Complete Phases Only)")
        self.assertIn("Left out: c-1-2", complete.lines[-1])

    def test_all_complete_shows_matrix_only(self) -> None:
        benchmark = _benchmark(pooled=["Q1", "Q18"])
        benchmark.evaluator.get_query_completion.return_value = _completion().assign(Q18=True)
        sections = benchmark._build_completion_sections(is_multitenant=False)
        self.assertEqual([s.heading for s in sections], ["Query Completion per Phase"])

    def test_failure_events_per_incomplete_phase(self) -> None:
        events = _benchmark(pooled=["Q1"])._failure_events()
        self.assertEqual([(e.phase, e.text) for e in events], [("c-1-2", "queries failed: Q18 in 1 of 2 pods")])


class HealthSummaryCompletionTest(unittest.TestCase):
    """index.md points to the complete phases when some phase failed."""

    def test_incomplete_phases_are_pointed_to(self) -> None:
        lines = report_writer._build_health_summary_lines(
            0, {"num_errors": 1, "num_warnings": 0, "phases_complete": 9, "phases_total": 12})
        line = next(line for line in lines if line.startswith("- Phases"))
        self.assertIn("9 of 12", line)
        self.assertIn("Per Phase (Complete Phases Only)", line)


if __name__ == "__main__":
    unittest.main()
