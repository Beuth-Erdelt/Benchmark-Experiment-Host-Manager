"""
Unit tests for :mod:`bexhoma.missing_metrics`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bexhoma import missing_metrics, report_writer

_URL = "http://bexhoma-service-monitoring-default.perdelt.svc.cluster.local:9090/api/v1/query_range"
_LINE = ('ERROR:root:Metrics missing for CPU Memory (sum(container_memory_working_set_bytes{container="dbms"}))'
         f': {_URL}')
_LINE_CONNECTION = ('ERROR:root:Metrics missing for CPU Throttle (sum(rate(x[1m]))) for connection '
                    f'postgresql-1-1-1-1-1: {_URL}')


class ParseMissingMetricsTest(unittest.TestCase):
    """The dbmsbenchmarker log line is split into title, query and connection."""

    def test_title_and_query(self) -> None:
        [entry] = missing_metrics.parse_missing_metrics("noise\n" + _LINE + "\n" + _URL + "\n", "a.log")
        self.assertEqual(entry.title, "CPU Memory")
        self.assertEqual(entry.query, 'sum(container_memory_working_set_bytes{container="dbms"})')
        self.assertEqual(entry.connection, "")
        self.assertEqual(entry.source, "a.log")

    def test_connection(self) -> None:
        [entry] = missing_metrics.parse_missing_metrics(_LINE_CONNECTION)
        self.assertEqual((entry.title, entry.query, entry.connection), ("CPU Throttle", "sum(rate(x[1m]))", "postgresql-1-1-1-1-1"))

    def test_repeated_message_counts_once(self) -> None:
        self.assertEqual(len(missing_metrics.parse_missing_metrics(_LINE + "\n" + _LINE)), 1)

    def test_label_without_query_is_kept_whole(self) -> None:
        [entry] = missing_metrics.parse_missing_metrics("ERROR:root:Metrics missing for CPU")
        self.assertEqual(entry.title, "CPU")

    def test_clean_log(self) -> None:
        self.assertEqual(missing_metrics.parse_missing_metrics("Fetch metric interval 1 to 2 = 1 s span\n"), [])

    def test_title_with_parentheses(self) -> None:
        line = ('ERROR:root:Metrics missing for Max Transaction Duration (WAL Wait) '
                '(max(pg_stat_activity_max_tx_duration{wait_event=~"WALWrite|WalSync"})) '
                f'for connection pgduckdb-1-1-1-1: {_URL}')
        [entry] = missing_metrics.parse_missing_metrics(line)
        self.assertEqual(entry.title, "Max Transaction Duration (WAL Wait)")
        self.assertEqual(entry.query, 'max(pg_stat_activity_max_tx_duration{wait_event=~"WALWrite|WalSync"})')
        self.assertEqual(entry.connection, "pgduckdb-1-1-1-1")

    def test_component_comes_from_the_log_name(self) -> None:
        fetch_log = missing_metrics.fetch_log_name("pgduckdb-1-1-1-1", "datagenerator")
        [entry] = missing_metrics.parse_missing_metrics(_LINE, fetch_log)
        self.assertEqual(entry.component, "datagenerator")
        [entry] = missing_metrics.parse_missing_metrics(_LINE, "bexhoma-benchmarker-x-1-abc.dbmsbenchmarker.log")
        self.assertEqual(entry.component, "benchmarking")


class CollectMissingMetricsTest(unittest.TestCase):
    """Both the dashboard-pod fetch logs and the benchmarker pod logs are scanned."""

    def test_both_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            (result_dir / missing_metrics.fetch_log_name("PostgreSQL-1-1-1", "benchmarking")).write_text(_LINE)
            (result_dir / "bexhoma-benchmarker-postgresql-1-123-1-1-1-qp9nt.dbmsbenchmarker.log").write_text(_LINE_CONNECTION)
            (result_dir / "bexhoma-sut-postgresql-1-123-1-abc.dbms.log").write_text(_LINE)
            missing = missing_metrics.collect_missing_metrics(result_dir)
        self.assertEqual([entry.source for entry in missing], [
            "bexhoma-benchmarker-postgresql-1-123-1-1-1-qp9nt.dbmsbenchmarker.log",
            "bexhoma-metrics-PostgreSQL-1-1-1-benchmarking.log",
        ])

    def test_gap_logged_by_both_processes_counts_once(self) -> None:
        def line(connection: str) -> str:
            return ('ERROR:root:Metrics missing for Locks (sum(x{wait_event_type="Lock"})) '
                    f'for connection {connection}: {_URL}')
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            (result_dir / missing_metrics.fetch_log_name("pgduckdb-1-1-1-1", "benchmarking")).write_text(
                line("pgduckdb-1-1-1-1"))
            (result_dir / "bexhoma-benchmarker-pgduckdb-1-123-1-1-1-cwkhp.dbmsbenchmarker.log").write_text(
                line("pgduckdb-1-1-1-1-1"))
            missing = missing_metrics.collect_missing_metrics(result_dir)
        self.assertEqual([entry.source for entry in missing], ["bexhoma-metrics-pgduckdb-1-1-1-1-benchmarking.log"])

    def test_same_metric_in_two_phases_is_kept_twice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            for component in ("loading", "benchmarking"):
                (result_dir / missing_metrics.fetch_log_name("PostgreSQL-1-1-1", component)).write_text(_LINE)
            missing = missing_metrics.collect_missing_metrics(result_dir)
        self.assertEqual(sorted(entry.component for entry in missing), ["benchmarking", "loading"])

    def test_expected_gaps_carry_their_reason(self) -> None:
        connections = [{"name": "pg", "monitoring": {"metrics": {
            "throttle": {"title": "CPU Throttle", "sparse": True},
            "memory": {"title": "CPU Memory"},
        }}}]
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            (result_dir / "connections.config").write_text(repr(connections))
            (result_dir / missing_metrics.fetch_log_name("pg-1", "datagenerator")).write_text(_LINE)
            (result_dir / missing_metrics.fetch_log_name("pg-1", "loader")).write_text(_LINE_CONNECTION)
            (result_dir / missing_metrics.fetch_log_name("pg-1", "benchmarking")).write_text(_LINE)
            missing = missing_metrics.collect_missing_metrics(result_dir, ["datagenerator"])
        expected = {(entry.component, entry.title): entry.expected for entry in missing}
        self.assertEqual(expected, {
            ("datagenerator", "CPU Memory"): missing_metrics.EXPECTED_DATA_PREEXISTING,
            ("loader", "CPU Throttle"): missing_metrics.EXPECTED_SPARSE,
            ("benchmarking", "CPU Memory"): "",
        })

    def test_fetch_logs_have_their_own_files_md_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            (result_dir / missing_metrics.fetch_log_name("PostgreSQL-1-1-1", "benchmarking")).write_text("x")
            groups = report_writer._group_result_files(result_dir)
        self.assertEqual([path.name for path in groups["metrics-fetch"]], ["bexhoma-metrics-PostgreSQL-1-1-1-benchmarking.log"])


class HealthSummaryTest(unittest.TestCase):
    """index.md's Health Summary names missing metrics, or says there are none."""

    def test_missing_metrics_are_named(self) -> None:
        missing = missing_metrics.parse_missing_metrics(_LINE + "\n" + _LINE_CONNECTION, "a.log")
        lines = report_writer._build_health_summary_lines(0, {}, None, missing)
        line = next(line for line in lines if "Missing monitoring metrics" in line)
        self.assertIn(": 2 (CPU Memory, CPU Throttle)", line)
        self.assertIn("monitoring.md", line)

    def test_expected_gaps_get_their_own_line(self) -> None:
        missing = [missing_metrics.MissingMetric("a.log", "CPU Memory", component="datagenerator",
                                                 expected=missing_metrics.EXPECTED_DATA_PREEXISTING)]
        lines = report_writer._build_health_summary_lines(0, {}, None, missing)
        self.assertIn("- Missing monitoring metrics: none", lines)
        self.assertTrue(any(line.startswith("- Expected monitoring gaps: 1 (data pre-existing)") for line in lines))

    def test_none_missing(self) -> None:
        self.assertIn("- Missing monitoring metrics: none", report_writer._build_health_summary_lines(0, {}, None, []))

    def test_no_line_without_monitoring(self) -> None:
        lines = report_writer._build_health_summary_lines(0, {})
        self.assertFalse(any("monitoring metrics" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
