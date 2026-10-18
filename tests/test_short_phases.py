"""Tests for phases shorter than the scrape interval (dev/plan-metrics-pod-scope.md, M1b).

A phase whose window cannot hold the scrapes its component needs is not
measurable: the summary shows ``n/a`` for its ``CPU [CPUs]`` and leaves it out
of the CPU test; the test is skipped only when no phase of the component is
measurable.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from bexhoma import missing_metrics
from bexhoma.evaluators.base import EvaluatorBase
from bexhoma.experiments.base import ExperimentBase
from bexhoma.monitoring_math import min_measurable_window

__all__ = []


class _Evaluator:
    """Monitoring series per (metric, component); the CPU counter grows by ``cpu`` per connection."""

    test_results_column = EvaluatorBase.test_results_column

    def __init__(self, path: str, cpu: dict) -> None:
        self.path = path
        self.cpu = cpu

    def get_monitoring_metric(self, metric: str, component: str) -> pd.DataFrame:
        if metric == 'total_cpu_util_s':
            return pd.DataFrame({connection: [100.0, 100.0 + growth] for connection, growth in self.cpu.items()})
        return pd.DataFrame({connection: [1.0, 2.0] for connection in self.cpu})


class MinMeasurableWindowTest(unittest.TestCase):
    """SUT and workers need one scrape inside the window, jobs counted by max - min two."""

    def test_rule_per_component(self) -> None:
        self.assertEqual(min_measurable_window('benchmarking', 30), 36)
        self.assertEqual(min_measurable_window('tikvloading', 30), 36)
        self.assertEqual(min_measurable_window('benchmarker', 30), 60)
        self.assertEqual(min_measurable_window('loader', 30), 60)
        self.assertEqual(min_measurable_window('benchmarker', 30, jobs_scoped=True), 36)


class ShortPhaseSummaryTest(unittest.TestCase):
    """show_summary_monitoring(): n/a for short phases, test over the measurable ones."""

    def summary(self, component: str, windows: dict, cpu: dict, scrape_interval=30):
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        for connection, window in windows.items():
            text = "### python metrics.py\n" + (f"Interval length {window}s\n" if window is not None else "")
            (Path(tmp_dir.name) / missing_metrics.fetch_log_name(connection, component)).write_text(text)
        experiment = ExperimentBase.__new__(ExperimentBase)
        experiment.monitoring_active = True
        experiment.cluster = SimpleNamespace(
            monitor_cluster_active=False,
            config={'credentials': {'k8s': {'monitor': {'scrape_interval': scrape_interval}}}})
        experiment.workload = {'monitoring_components': {component: 'Phase'}, 'optional_monitoring_components': []}
        experiment.evaluator = _Evaluator(tmp_dir.name, cpu)
        experiment._test_results = []
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            experiment.show_summary_monitoring()
        cpu_test = next(result for result in experiment._test_results if 'CPU [CPUs]' in result[1])
        return cpu_test, output.getvalue()

    def test_short_sut_phase_is_skipped_and_shown_as_na(self) -> None:
        (passed, label), table = self.summary('benchmarking', {'pg-1-1-1-1': 11}, {'pg-1-1-1-1': 0.0})
        self.assertIsNone(passed)
        self.assertIn('phase shorter than monitoring scrape interval', label)
        self.assertIn('n/a', table)

    def test_long_sut_phase_with_zeros_fails(self) -> None:
        (passed, label), table = self.summary('benchmarking', {'pg-1-1-1-1': 600}, {'pg-1-1-1-1': 0.0})
        self.assertFalse(passed)
        self.assertNotIn('n/a', table)

    def test_sut_phase_of_45_s_is_measured(self) -> None:
        (passed, _), table = self.summary('benchmarking', {'pg-1-1-1-1': 45}, {'pg-1-1-1-1': 12.5})
        self.assertTrue(passed)
        self.assertIn('12.50', table)

    def test_job_of_45_s_counted_by_max_minus_min_is_skipped(self) -> None:
        (passed, _), _ = self.summary('benchmarker', {'pg-1-1-1-1': 45}, {'pg-1-1-1-1': 0.0})
        self.assertIsNone(passed)

    def test_short_phase_is_left_out_of_a_passing_test(self) -> None:
        """Round 1 too short, round 2 measured: the test passes on round 2."""
        (passed, _), table = self.summary(
            'benchmarking', {'pg-1-1-1-1': 11, 'pg-1-1-2-1': 300},
            {'pg-1-1-1-1': 0.0, 'pg-1-1-2-1': 640.0})
        self.assertTrue(passed)
        row = next(line for line in table.splitlines() if 'pg-1-1-1-1' in line)
        self.assertIn('n/a', row)
        self.assertIn('640.00', table)

    def test_old_logs_without_window_keep_the_old_test(self) -> None:
        (passed, _), table = self.summary('benchmarking', {'pg-1-1-1-1': None}, {'pg-1-1-1-1': 0.0})
        self.assertFalse(passed)
        self.assertNotIn('n/a', table)

    def test_scrape_interval_from_cluster_config(self) -> None:
        """At a scrape interval of 5 s, a 11 s SUT phase is measurable."""
        (passed, _), _ = self.summary('benchmarking', {'pg-1-1-1-1': 11}, {'pg-1-1-1-1': 0.0}, scrape_interval=5)
        self.assertFalse(passed)


if __name__ == '__main__':
    unittest.main()
