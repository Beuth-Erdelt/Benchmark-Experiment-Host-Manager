"""Tests for dev/plan-silent-malfunctions.md: malfunctions of a run must leave a failed test."""
from __future__ import annotations

import glob
import os
import tempfile
import unittest
from unittest import mock

import pandas as pd

from bexhoma import clusters, test_status
from bexhoma.benchmarks.benchbase.evaluator import BenchbaseEvaluator
from bexhoma.benchmarks.dbmsbenchmarker.evaluator import DbmsBenchmarkerEvaluator
from bexhoma.benchmarks.hardware.evaluator import HardwareEvaluator
from bexhoma.benchmarks.ycsb.evaluator import YcsbEvaluator
from bexhoma.clusters import Kubernetes, exit_code_line, script_end_line, wrap_script
from bexhoma.configurations.loading import script_failed
from bexhoma.evaluators.base import natural_sort_rows
from bexhoma.evaluators.logger import LogEvaluator
from bexhoma.experiments.base import ExperimentBase
from bexhoma.loading_checks import check_benchmarker_pods

__all__ = []

#: kubectl's own messages when the connection breaks; real outputs (#1793360424 and others)
BROKEN_STREAM_OUTPUTS = (
    'error: unable to upgrade connection: container not found ("dbms")\n',
    'Unable to connect to the server: net/http: TLS handshake timeout\n',
    '',  # a stream cut without any message
)

POD_EVICTED = """Name:             bexhoma-benchmarker-pgduckdb-1-1790852331-2-3-1-gdjd8
Status:           Failed
Reason:           Evicted
Message:          The node was low on resource: ephemeral-storage.
Containers:
  dbmsbenchmarker:
    State:          Terminated
      Reason:       Error
      Exit Code:    137
    Ready:          False
"""
POD_OK = POD_EVICTED.replace('Status:           Failed', 'Status:           Succeeded').replace(
    'Exit Code:    137', 'Exit Code:    0').replace('Reason:       Error', 'Reason:       Completed')


def experiment(folder: str = '') -> ExperimentBase:
    """An experiment that only records tests."""
    e = ExperimentBase.__new__(ExperimentBase)
    e.path, e.appname, e.code = folder, 'bexhoma', '42'
    e._test_results = []
    e._runtime_test_results = []
    return e


class ScriptOutcomeTest(unittest.TestCase):
    """S1/S8: a script counts as failed by kubectl's exit code and by sqlplus SP2 errors."""

    def test_exit_code_line(self) -> None:
        self.assertEqual(exit_code_line(0), '')
        self.assertEqual(exit_code_line(None), '')
        self.assertEqual(exit_code_line(mock.Mock()), '')
        self.assertIn('bexhoma: kubectl exit code 1', exit_code_line(1))

    def test_broken_stream_counts_as_failed(self) -> None:
        for output in BROKEN_STREAM_OUTPUTS:
            with self.subTest(output=output):
                self.assertFalse(script_failed('', output))
                self.assertTrue(script_failed('', output + exit_code_line(1)))

    def test_end_marker(self) -> None:
        """A script cut off by a vanished pod or stream has no end marker; a failed one prints failed."""
        self.assertEqual(wrap_script('psql < x.sql'),
                         '( psql < x.sql ) && echo BEXHOMA_SCRIPT_END:ok || echo BEXHOMA_SCRIPT_END:failed')
        self.assertEqual(wrap_script(''), '')
        cut = 'CREATE INDEX\nCREATE INDEX\n'
        self.assertFalse(script_failed(cut, ''))
        self.assertTrue(script_failed(cut, script_end_line('psql < x.sql', cut)))
        self.assertFalse(script_failed(cut + 'BEXHOMA_SCRIPT_END:ok\n', ''))
        self.assertTrue(script_failed('BEXHOMA_SCRIPT_END:failed\n', ''))
        self.assertEqual(script_end_line('', ''), '')

    def test_sqlplus_sp2_error(self) -> None:
        # real output of the instant client (2026-11-24): sqlplus goes on and exits 0
        stdout = 'SP2-0734: unknown command beginning "SELEC 1 FR..." - rest of line ignored.\nAFTER_SP2_ERROR\n'
        self.assertTrue(script_failed(stdout, ''))
        self.assertFalse(script_failed('Table created.\n', ''))

    def test_pod_command_reports_exit_code(self) -> None:
        cluster = Kubernetes.__new__(Kubernetes)
        cluster.context, cluster.logger = 'test', mock.Mock()
        process = mock.Mock(returncode=1)
        process.communicate.return_value = (b'', b'error: unable to upgrade connection\n')
        with mock.patch.object(clusters.subprocess, 'Popen', return_value=process):
            _, _, stderr = cluster.execute_command_in_pod('sh -e x.sh', pod='sut', retry_interrupted=False,
                                                          report_exit=True)
        self.assertTrue(script_failed('', stderr))
        with mock.patch.object(clusters.subprocess, 'Popen', return_value=process):
            _, _, stderr = cluster.execute_command_in_pod('ls', pod='sut', retry_interrupted=False)
        self.assertNotIn('bexhoma: kubectl exit code', stderr)


class _FakeLogEvaluator(LogEvaluator):
    """A log evaluator with given per-pod rows."""

    RESULTS_PER_POD = True

    def __init__(self, rows: list, benchmark_run: int = 1) -> None:
        self.rows = pd.DataFrame(rows)
        self.benchmark_run = benchmark_run

    def get_df_benchmarking(self):
        return self.rows


def planned(*connections: str, benchmark_run: int = 1) -> pd.DataFrame:
    return pd.DataFrame([{'connection': c, 'benchmark_run': benchmark_run, 'job': c.rsplit('-', 1)[0], 'pods': 2}
                         for c in connections])


class ResultsCompleteTest(unittest.TestCase):
    """S2: every planned benchmarker pod leaves exactly one result."""

    def test_complete(self) -> None:
        e = experiment()
        _FakeLogEvaluator([{'connection': 'x-1-1-1-1', 'pod': 'a'}, {'connection': 'x-1-1-1-2', 'pod': 'b'}]
                          ).record_results_complete_test(e, planned('x-1-1-1-1', 'x-1-1-1-2'))
        self.assertEqual(e._test_results, [(True, 'Results of all benchmarker pods')])

    def test_missing_pod(self) -> None:
        e = experiment()
        _FakeLogEvaluator([{'connection': 'x-1-1-1-2', 'pod': 'b'}]
                          ).record_results_complete_test(e, planned('x-1-1-1-1', 'x-1-1-1-2'))
        self.assertFalse(e._test_results[0][0])
        self.assertIn('missing: x-1-1-1-1', e._test_results[0][1])

    def test_same_child_twice(self) -> None:
        """A pod retried by Kubernetes ran with the child of another pod (1790852331)."""
        e = experiment()
        _FakeLogEvaluator([{'connection': 'x-1-1-1-1', 'pod': 'a'}, {'connection': 'x-1-1-1-1', 'pod': 'c'},
                           {'connection': 'x-1-1-1-2', 'pod': 'b'}]
                          ).record_results_complete_test(e, planned('x-1-1-1-1', 'x-1-1-1-2'))
        self.assertFalse(e._test_results[0][0])
        self.assertIn('same child twice: x-1-1-1-1', e._test_results[0][1])

    def test_several_rows_of_one_pod(self) -> None:
        """HammerDB writes one row per iteration of a pod: that is no duplicate."""
        e = experiment()
        _FakeLogEvaluator([{'connection': 'x-1-1-1-1', 'pod': 'a'}, {'connection': 'x-1-1-1-1', 'pod': 'a'}]
                          ).record_results_complete_test(e, planned('x-1-1-1-1'))
        self.assertTrue(e._test_results[0][0])

    def test_other_benchmark_is_left_out(self) -> None:
        e = experiment()
        connections = pd.concat([planned('x-1-1-1-1'), planned('x-1-1-2-1', benchmark_run=2)])
        _FakeLogEvaluator([{'connection': 'x-1-1-1-1', 'pod': 'a'}]).record_results_complete_test(e, connections)
        self.assertTrue(e._test_results[0][0])

    def test_rows_without_results(self) -> None:
        benchbase, ycsb, hardware = (cls.__new__(cls) for cls in (BenchbaseEvaluator, YcsbEvaluator, HardwareEvaluator))
        df = pd.DataFrame([{'connection': 'a', 'scalefactor': '16'}, {'connection': 'b', 'scalefactor': None}])
        self.assertEqual(list(benchbase.rows_with_results(df)['connection']), ['a'])
        df = pd.DataFrame([{'connection': 'a', '[OVERALL].Throughput(ops/sec)': '5'},
                           {'connection': 'b', '[OVERALL].Throughput(ops/sec)': None}])
        self.assertEqual(list(ycsb.rows_with_results(df)['connection']), ['a'])
        self.assertTrue(ycsb.rows_with_results(pd.DataFrame([{'connection': 'a'}])).empty)
        df = pd.DataFrame([{'connection': 'a', 'hardware_fio_read_iops': '100'},
                           {'connection': 'b', 'hardware_fio_read_iops': ''}])
        self.assertEqual(list(hardware.rows_with_results(df)['connection']), ['a'])

    def test_dbmsbenchmarker_pod_entries(self) -> None:
        evaluator = DbmsBenchmarkerEvaluator.__new__(DbmsBenchmarkerEvaluator)
        evaluator.benchmark_run = 1
        e = experiment()
        evaluator.record_results_complete_test(e, planned('x-1-1-1-1', 'x-1-1-1-2'))
        self.assertEqual(e._test_results, [(True, 'Results of all benchmarker pods')])
        e = experiment()
        evaluator.record_results_complete_test(e, planned('x-1-1-1-1'))
        self.assertFalse(e._test_results[0][0])
        self.assertIn('x-1-1-1 (1 of 2)', e._test_results[0][1])

    def test_sort_keeps_rows_with_the_same_index(self) -> None:
        df = pd.DataFrame({'v': [1, 2, 3]}, index=['a-10', 'a-2', 'a-2'])
        self.assertEqual(list(natural_sort_rows(df)['v']), [2, 3, 1])


class BenchmarkerPodsTest(unittest.TestCase):
    """S3: a retried pod fails; a failed benchmarker pod is a failed test."""

    def test_no_child_fallback_in_benchmarker_scripts(self) -> None:
        files = glob.glob('images/**/benchmarker.sh', recursive=True)
        self.assertTrue(files)
        for path in files:
            with open(path, encoding='utf-8') as file:
                text = file.read()
            if 'lpop bexhoma-benchmarker' not in text:
                continue
            with self.subTest(script=path):
                self.assertNotIn('BEXHOMA_CHILD=1\n', text)
                self.assertIn('FATAL: no child number in message queue', text)

    def test_evicted_pod(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            prefix = os.path.join(folder, 'bexhoma-benchmarker-pgduckdb-1-42-2-3-1-')
            with open(prefix + 'gdjd8.describe.log', 'w') as file:
                file.write(POD_EVICTED)
            with open(prefix + 'abcde.describe.log', 'w') as file:
                file.write(POD_OK)
            checks = check_benchmarker_pods(folder, 'bexhoma', '42', ['PgDuckDB-1'])
            self.assertEqual(len(checks['PgDuckDB-1'].pods), 2)
            self.assertEqual(len(checks['PgDuckDB-1'].failures), 1)
            self.assertIn('exit 137', checks['PgDuckDB-1'].failures[0])
            e = experiment(folder)
            e._show_benchmarker_pod_checks([{'name': 'PgDuckDB-1-2-3', 'configuration': 'PgDuckDB-1'}])
            self.assertFalse(e._test_results[0][0])
            # a loader check does not read benchmarker pods
            e = experiment(folder)
            e._show_loader_pod_checks([{'name': 'PgDuckDB-1-2-3', 'configuration': 'PgDuckDB-1'}])
            self.assertEqual(e._test_results, [])


class GeneratorMarkerTest(unittest.TestCase):
    """S4: raw data is reused only with the completion marker, written after a successful generation."""

    def test_marker_written_after_the_checks(self) -> None:
        for path in ('images/tpch/generator/generator.sh', 'images/tpcds/generator/generator.sh'):
            with open(path, encoding='utf-8') as file:
                text = file.read()
            with self.subTest(script=path):
                self.assertIn('no completion marker', text)
                written = text.index('> "${destination_raw%/}/.bexhoma_generated"'
                                     if 'tpcds' in path else '> "$destination_raw/.bexhoma_generated"')
                self.assertLess(text.rindex('FATAL:'), written)
                self.assertLess(text.index('I do nothing'), written)


class RuntimeGapsTest(unittest.TestCase):
    """S5: gaps found while running become failed tests."""

    def test_runtime_failure_once(self) -> None:
        e = experiment()
        e._record_runtime_failure('x')
        e._record_runtime_failure('x')
        self.assertEqual(e._runtime_test_results, [(False, 'x')])

    def test_logs_not_stored(self) -> None:
        e = experiment()
        e.cluster = mock.Mock(logs_not_stored=['b.log', 'a.log', 'a.log'])
        e._record_runtime_gaps()
        self.assertEqual(e._runtime_test_results, [(False, 'Pod log stored: a.log'), (False, 'Pod log stored: b.log')])

    def test_store_pod_log_gives_up(self) -> None:
        cluster = Kubernetes.__new__(Kubernetes)
        cluster.code, cluster.logger = '42', mock.Mock()
        with tempfile.TemporaryDirectory() as folder:
            os.makedirs(os.path.join(folder, '42'))
            cluster.config = {'benchmarker': {'resultfolder': folder}}
            with mock.patch.object(Kubernetes, 'pod_log', return_value=None), \
                    mock.patch.object(Kubernetes, '_pod_label', return_value='bexhoma-loading-x'):
                cluster.store_pod_log('bexhoma-loading-x', 'sensor')
            self.assertEqual(cluster.logs_not_stored, ['bexhoma-loading-x.sensor.log'])
            # an empty log (a container that prints nothing) is no gap
            with mock.patch.object(Kubernetes, 'pod_log', return_value=''), \
                    mock.patch.object(Kubernetes, '_pod_label', return_value='bexhoma-sut-x'):
                cluster.store_pod_log('bexhoma-sut-x', 'exporter')
        self.assertEqual(cluster.logs_not_stored, ['bexhoma-loading-x.sensor.log'])


class AbortedSummaryScriptsTest(unittest.TestCase):
    """An experiment aborted before its first result still names the loading scripts that failed (1795559036)."""

    def test_failed_index_script(self) -> None:
        from types import SimpleNamespace
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as folder:
            prefix = os.path.join(folder, 'bexhoma-loading-postgresql-1-initindexes-tpch-postgres.sql')
            with open(prefix + '.stdout.log', 'w') as file:
                file.write('CREATE INDEX\nBEXHOMA_SCRIPT_END:failed\n')
            with open(prefix + '.stderr.log', 'w') as file:
                file.write('FATAL:  terminating connection due to administrator command\n')
            e = experiment(folder)
            e.workload = {'name': 'TPC-H'}
            e.configurations = [SimpleNamespace(configuration='PostgreSQL-1')]
            with contextlib.redirect_stdout(io.StringIO()):
                e.show_summary_aborted()
        self.assertFalse(e._test_results[0][0])
        self.assertIn('initindexes-tpch-postgres.sql', e._test_results[0][1])


class SutPodsTest(unittest.TestCase):
    """S6 and S9: a replaced SUT pod and incomplete host information are seen."""

    HOST = {'RAM': 1, 'CPU': 'x', 'Cores': 2, 'node': 'n'}

    def connection(self, uid: str, run: int = 1, loading: str = 'u1', **host) -> dict:
        return {'name': f'PG-1-{run}-1', 'configuration': 'PG-1', 'parameter': {'numExperiment': run},
                'sut_pod_uid_loading': loading, 'hostsystem': {**self.HOST, 'pod_uid': uid, **host}}

    def test_not_replaced(self) -> None:
        e = experiment()
        e._test_sut_pods_not_replaced([self.connection('u1'), self.connection('u1'),
                                       self.connection('u2', run=2, loading='u2')])
        self.assertEqual(e._test_results, [(True, 'SUT pods not replaced')])

    def test_replaced_during_loading(self) -> None:
        e = experiment()
        e._test_sut_pods_not_replaced([self.connection('u2', loading='u1')])
        self.assertFalse(e._test_results[0][0])

    def test_worker_replaced(self) -> None:
        e = experiment()
        first, second = self.connection('u1'), self.connection('u1')
        first['worker'] = {'worker': [{'pod_uid': 'w1'}]}
        second['worker'] = {'worker': [{'pod_uid': 'w2'}]}
        e._test_sut_pods_not_replaced([first, second])
        self.assertIn('worker 0', e._test_results[0][1])

    def test_older_results_without_uids(self) -> None:
        e = experiment()
        e._test_sut_pods_not_replaced([{'name': 'PG-1-1-1', 'hostsystem': {'RAM': 1}}])
        self.assertEqual(e._test_results, [])

    def test_replaced_during_last_round(self) -> None:
        """P2: the end-of-repetition snapshot has a UID no earlier reading saw."""
        e = experiment()
        e._test_sut_pods_not_replaced([self.connection('u1')], {('pg-1', '1'): {'sut-a': 'u9'}})
        self.assertFalse(e._test_results[0][0])
        self.assertIn('pg-1 repetition 1 sut-a (after the last round started)', e._test_results[0][1])

    def test_snapshot_same_pods(self) -> None:
        e = experiment()
        first = self.connection('u1')
        first['worker'] = {'worker': [{'pod_uid': 'w1'}]}
        e._test_sut_pods_not_replaced([first], {('pg-1', '1'): {'sut-a': 'u1', 'worker-0': 'w1'}})
        self.assertEqual(e._test_results, [(True, 'SUT pods not replaced')])

    def test_snapshot_of_a_repetition_without_readings(self) -> None:
        e = experiment()
        e._test_sut_pods_not_replaced([self.connection('u1')], {('pg-1', '2'): {'sut-a': 'u9'}})
        self.assertEqual(e._test_results, [(True, 'SUT pods not replaced')])

    def test_read_snapshot_uids(self) -> None:
        import json
        from bexhoma import sut_restarts
        entry = sut_restarts.restart_snapshot_entry('0 0', {'dbms': 0, 'exporter': 0}, uid='u1')
        self.assertEqual(entry['uid'], 'u1')
        self.assertNotIn('uid', sut_restarts.restart_snapshot_entry('0', {'dbms': 0}))
        with tempfile.TemporaryDirectory() as folder:
            with open(os.path.join(folder, 'bexhoma-sut-pg-1-42-2-restarts.json'), 'w') as file:
                json.dump({'sut-a': entry, 'sut-b': {'counts': '0', 'containers': {}}, 'old': '0'}, file)
            uids = sut_restarts.read_snapshot_uids(folder, '42')
        self.assertEqual(uids, {('pg-1', '2'): {'sut-a': 'u1'}})

    def test_host_info(self) -> None:
        e = experiment()
        e._test_host_info_complete([self.connection('u1')])
        self.assertEqual(e._test_results, [(True, 'Host information complete')])
        e = experiment()
        e._test_host_info_complete([self.connection('u1', CPU='', Cores=0)])
        self.assertEqual(e._test_results[0][0], test_status.WARNING)
        self.assertIn('CPU, Cores', e._test_results[0][1])


class ConfiguredAmountTest(unittest.TestCase):
    """S7: a run shorter than configured fails."""

    def test_ycsb_operations_with_read_modify_write(self) -> None:
        # workload F: 100 reads and 50 read-modify-writes; YCSB counts each RMW as READ, UPDATE and RMW
        row = pd.Series({'[READ].Operations': '150', '[UPDATE].Operations': '50',
                         '[READ-MODIFY-WRITE].Operations': '50', '[CLEANUP].Operations': '8'})
        self.assertEqual(YcsbEvaluator.operations_done(row), 150)
        row = pd.Series({'[READ].Operations': '187666', '[UPDATE].Operations': '187334'})
        self.assertEqual(YcsbEvaluator.operations_done(row), 375000)

    def test_ycsb_test(self) -> None:
        evaluator = YcsbEvaluator.__new__(YcsbEvaluator)
        rows = pd.DataFrame([{'connection': 'a', 'operations': '100', '[OVERALL].Throughput(ops/sec)': '1',
                              '[READ].Operations': '100'},
                             {'connection': 'b', 'operations': '100', '[OVERALL].Throughput(ops/sec)': '1',
                              '[READ].Operations': '60'}])
        e = experiment()
        with mock.patch.object(YcsbEvaluator, 'get_df_benchmarking', return_value=rows):
            evaluator._test_operations_complete(e)
        self.assertFalse(e._test_results[0][0])
        self.assertIn('b (60 of 100)', e._test_results[0][1])

    def test_benchbase_duration(self) -> None:
        evaluator = BenchbaseEvaluator.__new__(BenchbaseEvaluator)
        rows = pd.DataFrame([{'connection': 'a', 'time': '300', 'scalefactor': '16',
                              'Elapsed Time (nanoseconds)': 300000013266},
                             {'connection': 'b', 'time': '300', 'scalefactor': '16',
                              'Elapsed Time (nanoseconds)': 120000000000}])
        e = experiment()
        with mock.patch.object(BenchbaseEvaluator, 'get_df_benchmarking', return_value=rows):
            evaluator._test_duration_complete(e)
        self.assertFalse(e._test_results[0][0])
        self.assertIn('b (120s of 300s)', e._test_results[0][1])
        self.assertNotIn('a (', e._test_results[0][1])

    HAMMERDB_LOG = ("HAMMERDB_DURATION:5\nHAMMERDB_RAMPUP:2\nStart 0 seconds\n16 VU TEST\n"
                    "Vuser 1:Rampup complete, Taking start Transaction Count.\n"
                    "Vuser 1:Test complete, Taking end Transaction Count.\n"
                    "Vuser 1:FINISHED SUCCESS\nEnd 429 seconds\nDuration 429 seconds\n"
                    "Benchmarking done\nDuration 470 seconds\n")

    def test_hammerdb_markers(self) -> None:
        from bexhoma.benchmarks.hammerdb.evaluator import HammerdbEvaluator
        markers = HammerdbEvaluator.run_markers(self.HAMMERDB_LOG)
        self.assertEqual(markers, {'seconds': 429, 'started': 1, 'completed': 1, 'failed': [],
                                   'rampup': 2.0, 'duration': 5.0})
        failed = self.HAMMERDB_LOG.replace('Vuser 1:FINISHED SUCCESS', 'Vuser 3:FINISHED FAILED')
        self.assertEqual(HammerdbEvaluator.run_markers(failed)['failed'], ['3'])

    def test_hammerdb_tests(self) -> None:
        """P5: a short run and a failed virtual user fail; transaction errors are not looked at."""
        from bexhoma.benchmarks.hammerdb.evaluator import HammerdbEvaluator
        logs = {
            'ok': self.HAMMERDB_LOG.replace('FINISHED SUCCESS', 'FINISHED SUCCESS\nError in Virtual User 2: deadlock'),
            'short': self.HAMMERDB_LOG.replace('429 seconds', '200 seconds'),
            'cut': self.HAMMERDB_LOG.replace('Vuser 1:Test complete, Taking end Transaction Count.\n', ''),
            'vufail': self.HAMMERDB_LOG.replace('Vuser 1:FINISHED SUCCESS', 'Vuser 4:FINISHED FAILED'),
            'old': 'HAMMERDB_DURATION:5\nHAMMERDB_RAMPUP:2\n',
        }
        with tempfile.TemporaryDirectory() as folder:
            for pod, text in logs.items():
                with open(os.path.join(folder, f'bexhoma-benchmarker-pg-1-42-1-1-1-{pod}.dbmsbenchmarker.log'), 'w') as file:
                    file.write(text)
            evaluator = HammerdbEvaluator.__new__(HammerdbEvaluator)
            evaluator.path = folder
            rows = pd.DataFrame([{'connection': f'pg-{pod}', 'pod': f'{pod}.dbmsbenchmarker'} for pod in logs])
            e = experiment()
            with mock.patch.object(HammerdbEvaluator, 'get_df_benchmarking', return_value=rows):
                evaluator._test_runs_complete(e)
        (vu_passed, vu_label), (time_passed, time_label) = e._test_results
        self.assertFalse(vu_passed)
        self.assertEqual(vu_label, 'Virtual users FINISHED FAILED: pg-vufail (Vuser 4)')
        self.assertFalse(time_passed)
        self.assertIn('pg-short (200s of 420s)', time_label)
        self.assertIn('pg-cut (0 of 1 VU tests completed)', time_label)
        self.assertNotIn('pg-ok', time_label + vu_label)
        self.assertNotIn('pg-old', time_label + vu_label)


class ExitCodeTest(unittest.TestCase):
    """P1: a failed test of any summary makes the run exit 1; there is no -tr."""

    def outcome(self, *blocks: list) -> tuple[int, str]:
        import contextlib
        import io
        e = experiment()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            for block in blocks:
                e._test_results = list(block)
                e._print_test_summary()
            code = e.tests_outcome()
        return code, out.getvalue()

    def test_all_passed(self) -> None:
        code, out = self.outcome([(True, 'a'), (True, 'b')])
        self.assertEqual(code, 0)
        self.assertIn('Test successful!', out)

    def test_failed(self) -> None:
        code, out = self.outcome([(True, 'a'), (False, 'b')])
        self.assertEqual(code, 1)
        self.assertIn('Tests failed: 1 of 2', out)
        self.assertNotIn('Test successful!', out)

    def test_skipped_and_warning_do_not_fail(self) -> None:
        code, _ = self.outcome([(True, 'a'), (None, 'b'), (test_status.WARNING, 'c')])
        self.assertEqual(code, 0)

    def test_failure_in_a_later_benchmark_counts(self) -> None:
        """A mixed experiment resets _test_results per benchmark; the count is kept."""
        code, out = self.outcome([(True, 'a')], [(False, 'b')], [(True, 'c')])
        self.assertEqual(code, 1)
        self.assertIn('Tests failed: 1 of 3', out)

    def test_no_summary_fails(self) -> None:
        """P12: a workload type no benchmark claims is a failed test, not a silent exit 0."""
        import contextlib
        import io
        e = experiment()
        e.workload = {'type': 'tpcc'}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ExperimentBase.show_summary(e)
            code = e.tests_outcome()
        self.assertEqual(code, 1)
        self.assertIn("* TEST failed: No summary: workload type 'tpcc' belongs to no benchmark", out.getvalue())

    def test_no_tests_printed(self) -> None:
        code, out = self.outcome()
        self.assertEqual(code, 0)
        self.assertEqual(out, '')

    def test_no_tr_flag(self) -> None:
        import argparse
        import contextlib
        import io
        from bexhoma.cli_args import make_base_parser
        parser = argparse.ArgumentParser(parents=[make_base_parser()])
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            parser.parse_args(['-tr'])


if __name__ == "__main__":
    unittest.main()
