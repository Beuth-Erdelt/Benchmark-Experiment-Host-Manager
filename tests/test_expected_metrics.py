"""Tests of the expected-metrics list and its check against a result folder (bexhoma.expected_metrics).

The check must give the same answer on the run's folder, on one cleaned by
``-rp`` (per-connection CSVs merged into aggregates and deleted) and on a
published copy that keeps only the needed files; it never judges values.
"""
import csv
import os
import shutil
import tempfile
import threading
import types
import unittest
from pathlib import Path

from bexhoma import expected_metrics as em
from bexhoma.configurations.metrics import MetricsCollector
from bexhoma.experiments.base import ExperimentBase


def _row(connection, component_type, metric, configuration="PostgreSQL-1", source="fetch"):
    return dict(connection=connection, configuration=configuration, component_type=component_type,
                metrics_type="metrics", metric=metric, time_start=100, time_end=400, source=source)


def _write_metric(folder, component_type, metric, connection, values=("0.5", "0.7")):
    path = Path(folder) / em.metric_filename(component_type, metric, connection)
    path.write_text(connection + "\n" + "".join(v + "\n" for v in values), encoding="utf-8")


def _connections_config(folder, connections):
    (Path(folder) / "connections.config").write_text(str(connections), encoding="utf-8")


def _connection(name, configuration="PostgreSQL-1", time_loading=120.0, benchmarked=True, **extra):
    c = dict(name=name, configuration=configuration, time_loading=time_loading, monitoring={},
             hostsystem=dict(benchmarking_timespans={'benchmarker': [(1, 2)]} if benchmarked else {}))
    c.update(extra)
    return c


def _transform(folder):
    """What -rp's transform_monitoring_results() does: merge per-connection files, delete them."""
    folder = Path(folder)
    groups = {}
    for path in folder.glob("query_*_metric_*_*.csv"):
        for row in em.read(folder) or []:
            if path.name == em.metric_filename(row['component_type'], row['metric'], row['connection']):
                groups.setdefault(em.aggregate_filename(row['component_type'], row['metric']), []).append(
                    (row['connection'], path))
    for aggregate, members in groups.items():
        columns = [[line for line in p.read_text(encoding="utf-8").splitlines()] for _, p in members]
        length = max(len(c) for c in columns)
        lines = []
        for i in range(length):
            lines.append(",".join(c[i] if i < len(c) else "" for c in columns))
        (folder / aggregate).write_text("\n".join(lines) + "\n", encoding="utf-8")
        for _, p in members:
            p.unlink()


class ExpectedMetricNamesTest(unittest.TestCase):
    """The rows follow DBMSBenchmarker's fetchMetric(): no row for a file it does not write."""

    def _connectiondata(self, **metrics):
        return dict(active=True, monitoring=dict(prometheus_url="http://p", metrics=metrics))

    def test_inactive_metric_and_other_component_left_out(self):
        data = self._connectiondata(
            cpu=dict(query="q"), off=dict(query="q", active=False),
            app=dict(query="q", component="pool"))
        self.assertEqual(em.expected_metric_names(data, "metrics", "sut", "benchmarking"), ["cpu"])
        self.assertEqual(em.expected_metric_names(data, "metrics", "pool", "benchmarking"), ["cpu", "app"])

    def test_application_metric_only_for_loading_and_benchmarking(self):
        data = self._connectiondata(cpu=dict(query="q"), tps=dict(query="q", type="application"))
        data['monitoring']['prometheus_url_application'] = "http://app"
        self.assertEqual(em.expected_metric_names(data, "metrics", "", "loading"), ["cpu", "tps"])
        self.assertEqual(em.expected_metric_names(data, "metrics", "", "loader"), ["cpu"])
        # without an application endpoint it is queried at the generic URL, so a file is written
        del data['monitoring']['prometheus_url_application']
        self.assertEqual(em.expected_metric_names(data, "metrics", "", "loader"), ["cpu", "tps"])

    def test_job_query_set_and_fallback(self):
        data = self._connectiondata(cpu=dict(query="q"))
        data['monitoring']['metrics_benchmarker'] = dict(cpu_job=dict(query="q"))
        self.assertEqual(em.expected_metric_names(data, "metrics", "benchmarker", "benchmarker"), ["cpu_job"])
        self.assertEqual(em.expected_metric_names(data, "metrics_missing", "", "loading"), ["cpu"])

    def test_no_prometheus_or_inactive_connection(self):
        data = self._connectiondata(cpu=dict(query="q"))
        data['monitoring']['prometheus_url'] = ""
        self.assertEqual(em.expected_metric_names(data, "metrics", "", "loading"), [])
        data = self._connectiondata(cpu=dict(query="q"))
        data['active'] = False
        self.assertEqual(em.expected_metric_names(data, "metrics", "", "loading"), [])


class RecordTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_rows_deduplicated_and_parallel_writes_kept(self):
        em.record(self.folder, [_row("pg-1", "loading", "cpu")])
        self.assertEqual(em.record(self.folder, [_row("pg-1", "loading", "cpu", source="copy")]), 1)
        threads = [threading.Thread(target=em.record, args=(self.folder, [_row(f"pg-{i}", "loader", "cpu")]))
                   for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        rows = em.read(self.folder)
        self.assertEqual(len(rows), 21)
        self.assertEqual(rows[0]['source'], "copy")
        self.assertFalse(any(name.endswith('.tmp') for name in os.listdir(self.folder)))


class CheckTest(unittest.TestCase):
    """Presence per row, before and after -rp, on a published copy."""

    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.rows = [_row(c, t, m) for c in ("pg-1", "pg-2") for t in ("loading", "loader", "benchmarking")
                     for m in ("cpu", "vacuums")]
        em.record(self.folder, self.rows)
        _connections_config(self.folder, [_connection("pg-1"), _connection("pg-2")])
        for row in self.rows:
            _write_metric(self.folder, row['component_type'], row['metric'], row['connection'])

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def _statuses(self):
        result = em.check(self.folder, expected_count=len(self.rows))
        return result, {(m.connection, m.component_type, m.metric, m.status) for m in result.misses}

    def _both(self, expected):
        """Check, then clean the folder like -rp and check again: the same misses both times."""
        result, misses = self._statuses()
        self.assertEqual(misses, expected)
        _transform(self.folder)
        self.assertFalse(list(Path(self.folder).glob("query_*_metric_*_pg-*.csv")))
        result_after, misses_after = self._statuses()
        self.assertEqual(misses_after, expected)
        return result_after

    def test_clean_folder_passes(self):
        self.assertTrue(self._both(set()).passed)

    def test_zero_nan_and_header_only_are_present(self):
        _write_metric(self.folder, "loading", "vacuums", "pg-1", values=("0", "0", "0"))
        _write_metric(self.folder, "loader", "vacuums", "pg-1", values=("", ""))
        _write_metric(self.folder, "benchmarking", "vacuums", "pg-1", values=())
        self.assertTrue(self._both(set()).passed)

    def test_deleted_file_missing(self):
        os.remove(Path(self.folder) / em.metric_filename("loader", "cpu", "pg-2"))
        result = self._both({("pg-2", "loader", "cpu", em.STATUS_MISSING)})
        self.assertFalse(result.passed)
        self.assertEqual(em.describe(result), [("pg-2", "loader", "1 of 2 metrics missing (cpu)")])

    def test_failed_fetch_of_a_repetition(self):
        for metric in ("cpu", "vacuums"):
            os.remove(Path(self.folder) / em.metric_filename("benchmarking", metric, "pg-2"))
        self._both({("pg-2", "benchmarking", "cpu", em.STATUS_MISSING),
                    ("pg-2", "benchmarking", "vacuums", em.STATUS_MISSING)})

    def test_published_copy_with_only_the_needed_files(self):
        _transform(self.folder)
        copy = tempfile.mkdtemp()
        try:
            for name in os.listdir(self.folder):
                if name in ("connections.config", em.FILENAME) or name.startswith("query_"):
                    shutil.copy(Path(self.folder) / name, copy)
            self.assertTrue(em.check(copy, expected_count=len(self.rows)).passed)
            os.remove(Path(copy) / em.FILENAME)
            result = em.check(copy, expected_count=len(self.rows))
            self.assertTrue(result.list_missing)
            self.assertFalse(result.passed)
        finally:
            shutil.rmtree(copy, ignore_errors=True)

    def test_older_result_skipped(self):
        os.remove(Path(self.folder) / em.FILENAME)
        result = em.check(self.folder, expected_count=None)
        self.assertTrue(result.skipped)
        self.assertTrue(result.passed)

    def test_orig_name_column_after_merge(self):
        """Entries DBMSBenchmarker expands per pod: the aggregate column is the job-level orig_name."""
        _connections_config(self.folder, [_connection("pg-1"), _connection("pg-2"),
                                          _connection("pg-2-1", orig_name="pg-2")])
        em.record(self.folder, [_row("pg-2-1", "loader", "cpu")])
        _transform(self.folder)
        # transform_monitoring_results() names the column after orig_name
        aggregate = Path(self.folder) / em.aggregate_filename("loader", "cpu")
        self.assertNotIn("pg-2-1", aggregate.read_text(encoding="utf-8").splitlines()[0].split(","))
        self.assertTrue(em.check(self.folder, expected_count=len(self.rows) + 1).passed)
        aggregate.write_text("pg-1\n0.5\n", encoding="utf-8")
        misses = {(m.connection, m.metric) for m in em.check(self.folder, len(self.rows) + 1).misses}
        self.assertEqual(misses, {("pg-2", "cpu"), ("pg-2-1", "cpu")})


class NotFetchedTest(unittest.TestCase):
    """A fetch that was never queued: the phase times of connections.config are the second source."""

    def setUp(self):
        self.folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def _misses(self, connections, rows):
        em.record(self.folder, rows)
        for row in rows:
            _write_metric(self.folder, row['component_type'], row['metric'], row['connection'])
        _connections_config(self.folder, connections)
        return {(m.connection, m.component_type, m.status) for m in em.check(self.folder, len(rows)).misses}

    def test_repetition_without_rows(self):
        rows = [_row("pg-1", t, "cpu") for t in ("loading", "loader", "benchmarking", "benchmarker")]
        misses = self._misses([_connection("pg-1"), _connection("pg-2")], rows)
        self.assertEqual(misses, {("pg-2", t, em.STATUS_NOT_FETCHED)
                                  for t in ("loading", "loader", "benchmarking", "benchmarker")})

    def test_inherited_or_deactivated_loading_and_no_benchmarking_not_required(self):
        rows = [_row("pg-1", t, "cpu") for t in ("loading", "loader", "benchmarking")]
        connections = [_connection("pg-1"),
                       _connection("pg-2", loading_inherited=True, benchmarked=False),
                       _connection("pg-3", loading_deactivated=True, benchmarked=False),
                       _connection("pg-4", time_loading=0, benchmarked=False)]
        self.assertEqual(self._misses(connections, rows), set())

    def test_type_not_fetched_by_the_configuration_not_required(self):
        # MySQL-1 without SUT monitoring: no 'benchmarking' rows anywhere in that configuration
        rows = [_row("pg-1", "benchmarking", "cpu"), _row("my-1", "benchmarker", "cpu", configuration="MySQL-1")]
        connections = [_connection("pg-1", time_loading=0),
                       _connection("my-1", configuration="MySQL-1", time_loading=0)]
        self.assertEqual(self._misses(connections, rows), set())

    def test_copy_rows_count(self):
        rows = [_row("pg-1", "loading", "cpu"), _row("pg-2", "loading", "cpu", source="copy")]
        connections = [_connection("pg-1", benchmarked=False), _connection("pg-2", benchmarked=False)]
        self.assertEqual(self._misses(connections, rows), set())


class CollectorTest(unittest.TestCase):
    """MetricsCollector writes rows when a fetch is registered and when it copies a fetch."""

    def setUp(self):
        self.folder = tempfile.mkdtemp()
        monitoring = dict(prometheus_url="http://p", metrics=dict(cpu=dict(query="q"), ram=dict(query="q")))
        dbms = {name: types.SimpleNamespace(connectiondata=dict(active=True, monitoring=monitoring))
                for name in ("pg-1", "pg-2")}
        self.workload = {}
        self.cfg = types.SimpleNamespace(
            path=self.folder, code="1", configuration="PostgreSQL-1", benchmark=types.SimpleNamespace(dbms=dbms),
            experiment=types.SimpleNamespace(workload=self.workload))
        self.collector = MetricsCollector(self.cfg)

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_expect_and_copy(self):
        self.collector.expect("pg-1", "loader", "loader", "metrics", 1, 2)
        self.collector.expect("pg-1", "sut", "loading", "metrics", 1, 2)
        self.cfg.experiment.ensure_copy_metrics_script = lambda: "copy.sh"
        self.cfg.experiment.cluster = types.SimpleNamespace(
            execute_command_in_pod=lambda **kwargs: ("", "", ""))
        self.cfg.logger = types.SimpleNamespace(debug=lambda *a: None)
        self.collector.copy_fetched("pg-1", "pg-2", ["loading"], "dashboard")
        rows = em.read(self.folder)
        self.assertEqual(len(rows), 6)
        self.assertEqual(self.workload[em.WORKLOAD_KEY], 6)
        self.assertEqual({(r['connection'], r['component_type'], r['source']) for r in rows if r['connection'] == 'pg-2'},
                         {("pg-2", "loading", "copy")})

    def test_unknown_connection_writes_nothing(self):
        self.collector.expect("other", "sut", "loading", "metrics", 1, 2)
        self.assertIsNone(em.read(self.folder))


class SummaryTest(unittest.TestCase):
    """The test line of the summary, on a stand-in experiment."""

    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.experiment = ExperimentBase.__new__(ExperimentBase)
        self.experiment._test_results = []
        self.experiment.evaluator = types.SimpleNamespace(path=self.folder)
        self.experiment.workload = {'monitoring_components': {'loading': 'Loading phase: SUT deployment'}}

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_older_result_skipped(self):
        self.experiment._show_expected_metrics_check()
        self.assertEqual(self.experiment._test_results,
                         [(None, "All expected metrics present (no expected-metrics list (older result))")])

    def test_monitoring_off_no_test(self):
        self.experiment.workload = {'monitoring_components': {}}
        self.experiment._show_expected_metrics_check()
        self.assertEqual(self.experiment._test_results, [])

    def test_missing_file_fails_with_log_lines(self):
        em.record(self.folder, [_row("pg-1", "loading", "cpu"), _row("pg-1", "loading", "ram")])
        _write_metric(self.folder, "loading", "cpu", "pg-1")
        _connections_config(self.folder, [_connection("pg-1", benchmarked=False)])
        (Path(self.folder) / "bexhoma-metrics-pg-1-loading.log").write_text(
            "### python metrics.py\nTraceback (most recent call last)\nKeyError: 'ram'\n", encoding="utf-8")
        self.experiment.workload[em.WORKLOAD_KEY] = 2
        self.experiment._show_expected_metrics_check()
        passed, label = self.experiment._test_results[-1]
        self.assertIs(passed, False)
        self.assertEqual(label, "All expected metrics present (missing: 1 of 2; pg-1 loading)")

    def test_list_missing_fails(self):
        self.experiment.workload[em.WORKLOAD_KEY] = 12
        self.experiment._show_expected_metrics_check()
        self.assertIs(self.experiment._test_results[-1][0], False)
        self.assertIn("list missing", self.experiment._test_results[-1][1])

    def test_report_file(self):
        em.record(self.folder, [_row("pg-1", "loading", "cpu"), _row("pg-1", "loading", "ram")])
        _write_metric(self.folder, "loading", "cpu", "pg-1")
        _connections_config(self.folder, [_connection("pg-1", benchmarked=False)])
        result = em.check(self.folder, 2)
        target = Path(self.folder) / "metrics-check.csv"
        em.write_check(target, result)
        with open(target, newline='', encoding='utf-8') as f:
            statuses = {(r['metric'], r['status']) for r in csv.DictReader(f)}
        self.assertEqual(statuses, {("cpu", "present"), ("ram", em.STATUS_MISSING)})


if __name__ == "__main__":
    unittest.main()
