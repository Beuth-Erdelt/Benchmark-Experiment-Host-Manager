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


if __name__ == "__main__":
    unittest.main()
