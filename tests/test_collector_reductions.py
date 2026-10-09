"""
Unit tests for how :class:`bexhoma.collectors.base.CollectorBase` reduces monitoring metrics.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import types
import unittest

import pandas as pd

from bexhoma.collectors.base import CollectorBase


def _collector(metrics: dict) -> CollectorBase:
    collector = object.__new__(CollectorBase)
    collector.with_monitoring = True
    collector.df_metrics = pd.DataFrame(metrics).T
    return collector


class NodeLevelCounterTest(unittest.TestCase):
    """The node-level I/O wait counter is found by key, whatever its title."""

    def test_current_and_old_title(self) -> None:
        for title in ("Node I/O Wait CPU Time [s]", "Total I/O Wait Time [s]"):
            collector = _collector({"io_wait_total": {"title": title, "active": True, "type": "cluster", "metric": "counter"}})
            self.assertEqual(collector._node_level_counter_titles(), [title])

    def test_absent_metric(self) -> None:
        collector = _collector({"total_cpu_util": {"title": "CPU", "active": True, "type": "cluster", "metric": "gauge"}})
        self.assertEqual(collector._node_level_counter_titles(), [])


class SummaryReductionTest(unittest.TestCase):
    """show_summary_monitoring_table: counter -> max-min, ratio -> max, gauge -> mean."""

    def test_reduction_per_kind(self) -> None:
        series = pd.DataFrame({"conn": [1.0, 4.0, 2.0]})
        collector = _collector({
            "c": {"title": "Counter", "active": True, "type": "cluster", "metric": "counter"},
            "r": {"title": "Ratio", "active": True, "type": "cluster", "metric": "ratio"},
            "g": {"title": "Gauge", "active": True, "type": "cluster", "metric": "gauge"},
        })
        evaluation = types.SimpleNamespace(code="1", get_monitoring_metric=lambda metric, component: series.copy())
        summary = collector.show_summary_monitoring_table(evaluation, "benchmarking")
        self.assertEqual(summary.loc["conn"].to_dict(), {"Counter": 3.0, "Ratio": 4.0, "Gauge": 2.33})


_METRICS = {
    "cpu_s": {"title": "CPU Time [s]", "active": True, "type": "cluster", "metric": "counter"},
    "mem": {"title": "Memory [MiB]", "active": True, "type": "cluster", "metric": "gauge"},
    "peak": {"title": "Peak [%]", "active": True, "type": "cluster", "metric": "ratio"},
    "io_wait_total": {"title": "Node I/O Wait CPU Time [s]", "active": True, "type": "cluster", "metric": "counter"},
}
_COLUMNS = ["CPU Time [s]", "Memory [MiB]", "Peak [%]", "Node I/O Wait CPU Time [s]"]


def _jobs(rows: dict, tenancy: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per-job values and their metadata; rows maps job -> (configuration, values)."""
    per_job = pd.DataFrame({job: values for job, (_, values) in rows.items()}, index=_COLUMNS).T
    meta = per_job.copy()
    meta["configuration"] = [configuration for configuration, _ in rows.values()]
    for column, value in (("code", "1"), ("experiment_run", 1), ("client", 1),
                          ("type_tenants", tenancy), ("num_tenants", 2)):
        meta[column] = value
    return per_job, meta


class PhaseAggregationTest(unittest.TestCase):
    """Parallel jobs of one configuration are copies of one measurement, so counters take max."""

    def test_counter_is_not_summed_over_parallel_jobs(self) -> None:
        per_job, meta = _jobs({
            "1-pg-1-1-1": ("pg", [100.0, 50.0, 80.0, 10.0]),
            "1-pg-1-1-2": ("pg", [101.0, 52.0, 90.0, 10.0]),
        }, "schema")
        collector = _collector(_METRICS)
        collector.get_monitoring_aggregated_per_job = lambda type: per_job
        collector.add_metadata = lambda df: meta
        phase = collector.get_monitoring_aggregated_per_phase("benchmarking")
        row = phase.iloc[0]
        self.assertEqual((row["CPU Time [s]"], row["Memory [MiB]"], row["Peak [%]"]), (101.0, 51.0, 90.0))


class MultitenantAggregationTest(unittest.TestCase):
    """Within a configuration take max/mean; across configurations (container tenants) sum."""

    def _aggregate(self, rows: dict, tenancy: str) -> pd.Series:
        per_job, meta = _jobs(rows, tenancy)
        collector = _collector(_METRICS)
        collector.get_monitoring_aggregated_per_job = lambda type: per_job
        collector.add_metadata = lambda df: meta
        return collector.get_monitoring_aggregated_per_phase_multitenant("benchmarking").iloc[0]

    def test_schema_tenants_share_one_sut(self) -> None:
        row = self._aggregate({
            "1-pg-1-1-1": ("pg", [100.0, 50.0, 80.0, 10.0]),
            "1-pg-1-1-2": ("pg", [101.0, 52.0, 90.0, 10.0]),
        }, "schema")
        self.assertEqual(row[_COLUMNS].tolist(), [101.0, 51.0, 90.0, 10.0])

    def test_container_tenants_are_separate_suts(self) -> None:
        row = self._aggregate({
            "1-pg-0-1-1-1": ("pg-0", [100.0, 50.0, 80.0, 10.0]),
            "1-pg-1-1-1-1": ("pg-1", [101.0, 52.0, 90.0, 10.0]),
        }, "container")
        self.assertEqual(row[_COLUMNS].tolist(), [201.0, 102.0, 90.0, 10.0])


class SummaryWithoutActiveMetricsTest(unittest.TestCase):
    """No active metric gives an empty summary instead of a concat error."""

    def test_all_inactive(self) -> None:
        collector = _collector({"g": {"title": "Gauge", "active": False, "type": "cluster", "metric": "gauge"}})
        evaluation = types.SimpleNamespace(code="1", get_monitoring_metric=lambda metric, component: pd.DataFrame())
        self.assertTrue(collector.show_summary_monitoring_table(evaluation, "benchmarking").empty)


class TimeseriesComponentTest(unittest.TestCase):
    """The long-format time series read the requested component, not always benchmarking."""

    def test_component_is_passed_through(self) -> None:
        collector = _collector({"g": {"title": "Gauge", "active": True, "type": "cluster", "metric": "gauge"}})
        collector.codes = ["1"]
        requested = []

        def single(code, metric, component):
            requested.append(component)
            return pd.DataFrame({"job-a": [1.0]})

        collector.get_monitoring_timeseries_single = single
        collector.get_evaluator = lambda code: types.SimpleNamespace(code=code)
        collector.get_connections = lambda evaluation: pd.DataFrame({
            "job": ["job-a"], "code": ["1"], "phase": ["p"], "experiment_run": [1], "client": [1],
            "benchmark_run": [1], "type_tenants": ["None"], "vol_tenants": [False], "num_tenants": [0],
            "configuration": ["c"],
        })
        collector.get_workload = lambda code: {"tenant_per": "None", "num_tenants": 0, "multi_tenant_volume": False}
        collector.get_monitoring_timeseries_all(metric="g", component="loading")
        collector.get_monitoring_timeseries_all_multitenant(metric="g", component="loader")
        self.assertEqual(requested, ["loading", "loader"])


if __name__ == "__main__":
    unittest.main()
