"""Tests for #848: no loader pod, loading script or load fails silently."""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from bexhoma.configurations.base import SutConfiguration
from bexhoma.configurations.loading import LoadingCoordinator, loading_script_errors
from bexhoma.experiments.base import LOADING_UNSCHEDULABLE_TIMEOUT_MINUTES, ExperimentBase
from bexhoma.loading_checks import (check_loader_pods, parse_ingest_markers,
                                    parse_job_failed_pods, parse_pod_description)

__all__ = []

POD_FAILED = """Name:             bexhoma-loading-dbms-1-42-1-1-1-abcde
Status:           Failed
Init Containers:
  datagenerator:
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
    Ready:          True
Containers:
  sensor:
    State:          Terminated
      Reason:       Error
      Exit Code:    1
    Ready:          False
    Restart Count:  0
"""

POD_OK = POD_FAILED.replace("Failed", "Succeeded").replace("Error", "Completed").replace("Exit Code:    1", "Exit Code:    0")

JOB_FAILED = "Completions:      2\nPods Statuses:    0 Active (0 Ready) / 0 Succeeded / 3 Failed\n"


class ParserTest(unittest.TestCase):
    """The result-folder parsers."""

    def test_pod_description(self) -> None:
        self.assertEqual(parse_pod_description(POD_FAILED), ('Failed', [('sensor', 'Error', '1')]))
        self.assertEqual(parse_pod_description(POD_OK), ('Succeeded', []))

    def test_job_description(self) -> None:
        self.assertEqual(parse_job_failed_pods(JOB_FAILED), 3)
        self.assertEqual(parse_job_failed_pods("Pods Statuses: 0 Active / 1 Succeeded / 0 Failed"), 0)
        self.assertEqual(parse_job_failed_pods(""), 0)

    def test_ingest_markers(self) -> None:
        units = parse_ingest_markers(
            "x\nBEXHOMA_INGEST:lineitem:100:100:ok\nBEXHOMA_INGEST:orders:10:9:failed\n"
            "BEXHOMA_INGEST:usertable:::ok\r\n", pod='p', container='sensor')
        self.assertEqual([(u.unit, u.expected, u.reported, u.ok) for u in units],
                         [('lineitem', '100', '100', True), ('orders', '10', '9', False), ('usertable', '', '', True)])


class FolderTest(unittest.TestCase):
    """check_loader_pods() on a result folder."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, text: str) -> None:
        with open(os.path.join(self.folder, name), 'w', encoding='utf-8') as file:
            file.write(text)

    def test_clean_load(self) -> None:
        self.write('bexhoma-loading-dbms-1-42-1-1-1-abcde.describe.log', POD_OK)
        self.write('bexhoma-loading-dbms-1-42-1-1-1-abcde.sensor.log', 'BEXHOMA_INGEST:t:1:1:ok\n')
        self.write('bexhoma-loading-dbms-1-42-1-1-1.describe.job.log', 'Pods Statuses: 0 Active / 1 Succeeded / 0 Failed')
        # a script log of the SUT pod is no loader pod
        self.write('bexhoma-loading-dbms-1-initschema-db.sql.stderr.log', 'ERROR: x')
        checks = check_loader_pods(self.folder, 'bexhoma', '42', ['DBMS-1'])
        self.assertEqual(list(checks), ['DBMS-1'])
        self.assertEqual(checks['DBMS-1'].failures, [])
        self.assertEqual(len(checks['DBMS-1'].units), 1)

    def test_failed_pod_job_and_unit(self) -> None:
        self.write('bexhoma-loading-dbms-1-42-1-1-1-abcde.describe.log', POD_FAILED)
        self.write('bexhoma-loading-dbms-1-42-1-1-1-fghij.sensor.log', 'BEXHOMA_INGEST:orders:10:9:failed\n')
        self.write('bexhoma-loading-dbms-1-42-1-1-1.describe.job.log', JOB_FAILED)
        failures = check_loader_pods(self.folder, 'bexhoma', '42', ['DBMS-1'])['DBMS-1'].failures
        self.assertEqual(len(failures), 3)
        self.assertIn('sensor exit 1 (Error)', failures[0])
        self.assertIn('unit orders failed (expected 10, reported 9)', failures[1])
        # 3 failed pods in the job, 1 with a description
        self.assertIn('2 failed pods without stored description', failures[2])

    def test_longest_configuration_name_wins(self) -> None:
        self.write('bexhoma-loading-dbms-1-0-42-1-1-1-abcde.describe.log', POD_FAILED)
        checks = check_loader_pods(self.folder, 'bexhoma', '42', ['DBMS-1', 'DBMS-1-0'])
        self.assertEqual(list(checks), ['DBMS-1-0'])

    def test_no_loader_pods(self) -> None:
        self.assertEqual(check_loader_pods(self.folder, 'bexhoma', '42', ['DBMS-1']), {})
        self.assertEqual(check_loader_pods('', 'bexhoma', '42', ['DBMS-1']), {})


def experiment(folder: str = '') -> ExperimentBase:
    e = ExperimentBase.__new__(ExperimentBase)
    e.path, e.appname, e.code = folder, 'bexhoma', '42'
    e._test_results = []
    return e


class SummaryTest(unittest.TestCase):
    """The summary tests."""

    def test_loader_pods_test(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            e = experiment(folder)
            connections = [{'name': 'DBMS-1-1', 'configuration': 'DBMS-1'}]
            e._show_loader_pod_checks(connections)
            self.assertEqual(e._test_results, [])
            with open(os.path.join(folder, 'bexhoma-loading-dbms-1-42-1-1-1-abcde.describe.log'), 'w') as file:
                file.write(POD_OK)
            e._show_loader_pod_checks(connections)
            self.assertEqual(e._test_results[-1], (True, 'Loader pods without errors'))
            with open(os.path.join(folder, 'bexhoma-loading-dbms-1-42-1-1-1-abcde.describe.log'), 'w') as file:
                file.write(POD_FAILED)
            e._show_loader_pod_checks(connections)
            self.assertFalse(e._test_results[-1][0])
            self.assertIn('Loader pods without errors (failed: DBMS-1: 1)', e._test_results[-1][1])

    def test_loading_failed_test(self) -> None:
        e = experiment()
        e._show_loading_failures([{'name': 'DBMS-1-1'}])
        self.assertEqual(e._test_results, [])
        e._show_loading_failures([{'name': 'DBMS-1-1', 'configuration': 'DBMS-1', 'loading_failed': []}])
        self.assertEqual(e._test_results[-1], (True, 'Loading completed without failures'))
        e._show_loading_failures([
            {'name': 'DBMS-1-1', 'configuration': 'DBMS-1', 'loading_failed': ['SUT restarted 1 time during loading']},
            {'name': 'DBMS-1-2', 'configuration': 'DBMS-1', 'loading_failed': ['SUT restarted 1 time during loading']}])
        self.assertEqual(e._test_results[-1], (
            False, 'Loading completed without failures (failed: DBMS-1: SUT restarted 1 time during loading)'))

    def test_fatal_loading_failure_aborts(self) -> None:
        e = experiment()
        config = SimpleNamespace(configuration='DBMS-1', loading_failed_fatal='index scripts could not be uploaded: x',
                                 loading_started=True, loading_finished=True)
        self.assertIn('index scripts could not be uploaded', e._loading_abort_reason(config, None))


class ScriptFailedTest(unittest.TestCase):
    """Client error formats beyond ERROR/FATAL lines and exit codes."""

    def test_more_client_errors(self) -> None:
        from bexhoma.configurations.loading import script_failed
        self.assertTrue(script_failed('', 'psql: error: could not translate host name "x"'))
        self.assertTrue(script_failed('', 'Code: 60. DB::Exception: Table default.x does not exist.'))
        self.assertTrue(script_failed('', '<stdin>:3:InvalidRequest: Error from server: code=2200'))
        self.assertTrue(script_failed('', 'ERROR:  load durability: fsync is on, not off'))
        self.assertFalse(script_failed('ok', 'NOTICE:  table "x" does not exist, skipping'))

    def test_clients_that_go_on_after_an_error(self) -> None:
        """Real outputs (2026-11-10, Dec2025-SP3 / Cassandra 5.0.9) of a script with a failing statement.

        Both clients run the rest of the script, but exit non-zero: mclient with 1 and a message
        without ERROR, cqlsh -f with 2 and an 'Error from server' message.
        """
        from bexhoma.configurations.loading import script_failed
        mclient = "SELECT: no such table 'bexhoma_no_such_table'\n"
        self.assertFalse(script_failed('', mclient))
        self.assertTrue(script_failed('', mclient + 'command terminated with exit code 1\n'))
        cqlsh = ('/tmp/bx_fail.cql:3:InvalidRequest: Error from server: code=2200 [Invalid query] '
                 'message="keyspace bexhoma_no_such_keyspace does not exist"\n')
        self.assertTrue(script_failed('', cqlsh))
        self.assertTrue(script_failed('', cqlsh + 'command terminated with exit code 2\n'))
        # the restore check of the MySQL/MariaDB durability scripts
        self.assertTrue(script_failed('', 'ERROR 1644 (45000) at line 64: load durability: '
                                          'innodb_log_buffer_size is 1048576, not the saved 1048577\n'))

    def test_restore_scripts_check_the_restored_values(self) -> None:
        """Every MySQL/MariaDB restore checks the saved values before deleting them."""
        import glob
        files = [f for f in glob.glob('experiments/**/restoredurability-*.*', recursive=True)
                 if 'saved_settings' in open(f, encoding='utf-8').read()
                 and 'DELETE FROM bexhoma.saved_settings' in open(f, encoding='utf-8').read()]
        self.assertTrue(files)
        for path in files:
            text = open(path, encoding='utf-8').read()
            with self.subTest(script=path):
                self.assertIn('CALL bexhoma.check_restored();', text)
                self.assertLess(text.index('CALL bexhoma.check_restored();'),
                                text.index('DELETE FROM bexhoma.saved_settings'))


#: Pipes in ``experiments/**/*.sh`` that were checked: a failing command in
#: front of the pipe does not stop ``sh -e``, so each one must fail some other
#: way. Collapsed whitespace, as :func:`script_pipes` returns them.
ALLOWED_PIPES = {
    # empty value, not 0: loops until the flush timeout, then exit 1
    'dirty=$($MYSQL -e "SHOW GLOBAL STATUS LIKE \'Innodb_buffer_pool_pages_dirty\'" | cut -f2)',
    # empty value, not 0: loops until the timeout, then exit 1
    "pending=$(nodetool compactionstats | grep '^pending tasks' | tr -s ' ' | cut -d' ' -f3)",
    'pending=$(cockroach sql --insecure --host "$HOST" --format=csv -e "$QUERY" | tail -n 1)',
    # reply=$(redis-cli SAVE) before it already stops sh -e on a failure
    'if ! echo "$reply" | grep -q "checkpoint already in progress"; then',
    # a failing client ends the wait; the redis-cli SAVE after it fails or prints ERR
    'while redis-cli INFO persistence | grep -q "rdb_bgsave_in_progress:1"; do',
    'while valkey-cli INFO persistence | grep -q "rdb_bgsave_in_progress:1"; do',
}


def script_pipes(text: str) -> list:
    """Lines of a shell script with a pipe outside quotes and comments.

    :param text: Content of the script.
    :return: The lines, stripped and with collapsed whitespace.
    """
    import re
    pipes = []
    for line in text.splitlines():
        code = re.sub(r"'[^']*'", "''", line)
        code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
        code = '' if code.lstrip().startswith('#') else code.split(' #', 1)[0]
        if re.search(r'(?<!\|)\|(?!\|)', code):
            pipes.append(re.sub(r'\s+', ' ', line.strip()))
    return pipes


class ScriptPipesTest(unittest.TestCase):
    """A new pipe in a loading, index or reset script is checked before it is allowed (experiments/README.md)."""

    def test_detection(self) -> None:
        self.assertEqual(script_pipes('psql -c "x" | cut -f2\n'), ['psql -c "x" | cut -f2'])
        self.assertEqual(script_pipes("bcp t in f.dat -t \"|\" -c\na || b\n# x | y\necho '|'\n"), [])

    def test_only_checked_pipes(self) -> None:
        import glob
        files = sorted(glob.glob('experiments/**/*.sh', recursive=True))
        self.assertTrue(files)
        found = set()
        for path in files:
            for pipe in script_pipes(open(path, encoding='utf-8', errors='replace').read()):
                found.add(pipe)
                with self.subTest(script=path, pipe=pipe):
                    self.assertIn(pipe, ALLOWED_PIPES,
                                  "a failing command in front of a pipe does not stop sh -e; check the "
                                  "result instead (experiments/README.md) and add the line to ALLOWED_PIPES")
        # no stale entries
        self.assertEqual(ALLOWED_PIPES - found, set())
        for path in glob.glob('experiments/**/MySQL/restoredurability-unsafe.sql', recursive=True):
            with self.subTest(script=path):
                self.assertIn('CALL bexhoma.check_redo_log();', open(path, encoding='utf-8').read())

    def test_shell_scripts_run_with_errexit(self) -> None:
        import inspect
        from bexhoma.configurations import loading
        source = inspect.getsource(loading)
        self.assertNotIn('then sh {', source)
        self.assertNotIn("'sh {}'", source)
        self.assertEqual(source.count('sh -e {'), 3)


class LoadStatusTest(unittest.TestCase):
    """Volume labels and reuse after a failed load."""

    def test_loading_script_errors(self) -> None:
        self.assertEqual(loading_script_errors({'errors_schema': '0', 'errors_index': '2', 'index': 'True'}),
                         {'index': 2})

    def test_sut_restart_during_loading(self) -> None:
        cluster = mock.Mock()
        cfg = SimpleNamespace(sut_restarts_at_loading_start=1, loading_failed=[],
                              experiment=SimpleNamespace(cluster=cluster))
        coordinator = LoadingCoordinator(cfg)
        cluster.get_pod_restart_counts.return_value = {'dbms': 1}
        coordinator.check_sut_restarts_during_loading('pod')
        self.assertEqual(cfg.loading_failed, [])
        cluster.get_pod_restart_counts.return_value = {'dbms': 2, 'exporter': 1}
        coordinator.check_sut_restarts_during_loading('pod')
        self.assertEqual(cfg.loading_failed, ['SUT restarted 2 times during loading'])
        cfg.sut_restarts_at_loading_start = None
        cfg.loading_failed = []
        coordinator.check_sut_restarts_during_loading('pod')
        self.assertEqual(cfg.loading_failed, [])

    def test_volume_reuse(self) -> None:
        cfg = SutConfiguration.__new__(SutConfiguration)
        cfg.configuration = 'DBMS-1'
        cfg.num_experiment_to_apply_done, cfg.loading_started, cfg.loading_finished = 0, False, False
        cfg.check_volume_loaded('pvc', {'loaded': 'True'})
        cfg.check_volume_loaded('pvc', {})                                  # before the label existed
        with self.assertRaisesRegex(ValueError, 'unfinished load'):
            cfg.check_volume_loaded('pvc', {'loaded': 'False'})
        with self.assertRaisesRegex(ValueError, 'failed load'):
            cfg.check_volume_loaded('pvc', {'loaded': 'False', 'loading_failed': 'True'})
        # a later repetition finds the volume this experiment loaded
        cfg.num_experiment_to_apply_done = 1
        cfg.check_volume_loaded('pvc', {'loaded': 'False', 'loading_failed': 'True'})


class AbortedSummaryTest(unittest.TestCase):
    """An experiment aborted before its first result gets a short summary, not a traceback."""

    def test_summary_without_result_files(self) -> None:
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as folder:
            e = experiment(folder)
            e.args = SimpleNamespace(write_report=False)
            e.workload = {'name': 'TPC-H Queries SF=1', 'info': 'This experiment ...\nLoad durability is unsafe.'}
            e._runtime_test_results = [(False, 'Loading of PostgreSQL-1 failed: -xld unsafe cannot take effect')]
            e.show_summary = mock.Mock()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                e._show_summary_or_abort_note()
            e.show_summary.assert_not_called()
            self.assertIn('No results: the experiment ended before its first result was written', out.getvalue())
            self.assertIn('TEST failed: Loading of PostgreSQL-1 failed', out.getvalue())
            # the loader pods stored before the abort are judged as well
            e.configurations = [SimpleNamespace(configuration='DBMS-1')]
            with open(os.path.join(folder, 'bexhoma-loading-dbms-1-42-1-1-1-abcde.describe.log'), 'w') as file:
                file.write(POD_FAILED)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                e._show_summary_or_abort_note()
            self.assertIn('TEST failed: Loader pods without errors (failed: DBMS-1: 1)', out.getvalue())
            os.remove(os.path.join(folder, 'bexhoma-loading-dbms-1-42-1-1-1-abcde.describe.log'))
            # with the result files the full summary runs
            for name in ('queries.config', 'connections.config'):
                with open(os.path.join(folder, name), 'w') as file:
                    file.write('{}')
            e._show_summary_or_abort_note()
            e.show_summary.assert_called_once_with(write_report=False)


class RefusedSutTest(unittest.TestCase):
    """A refused volume aborts the experiment with a failed test, not with a traceback."""

    def test_refused_volume_aborts(self) -> None:
        e = experiment()
        e._runtime_test_results = []
        e.remove_experiment = mock.Mock()
        e.cluster = mock.Mock()
        cfg = SimpleNamespace(configuration='DBMS-1', loading_failed=[], loading_failed_fatal='',
                              loading_started=False, loading_finished=False, loading_active=True,
                              lifecycle=mock.Mock())
        cfg.loader = LoadingCoordinator(cfg)
        cfg.lifecycle.start_sut.side_effect = ValueError(
            'DBMS-1: existing storage pvc holds an unfinished load (loaded=False); remove it (-rsr)')
        self.assertFalse(e._start_sut_or_abort(cfg))
        e.remove_experiment.assert_called_once()
        self.assertEqual(e._runtime_test_results, [(False, 'Loading of DBMS-1 failed: existing storage pvc holds '
                                                           'an unfinished load (loaded=False); remove it (-rsr)')])
        cfg.lifecycle.start_sut.side_effect = None
        self.assertTrue(e._start_sut_or_abort(cfg))


class LoadDurabilityTest(unittest.TestCase):
    """-xld with --set: database-level synchronous_commit, server-wide conflicts refused."""

    def test_conflicting_set_args(self) -> None:
        from bexhoma.load_durability import conflicting_set_args
        required = {'fsync': 'off', 'full_page_writes': 'off'}
        ops = [({'target': 'container', 'param': 'fsync', 'config': ''}, 'on'),
               ({'target': 'container', 'param': 'fsync', 'config': 'Other-1'}, 'on'),        # other configuration
               ({'target': 'container', 'param': 'full_page_writes', 'config': ''}, 'false'),  # same as off
               ({'target': 'container', 'param': 'synchronous_commit', 'config': ''}, 'on'),  # per database: no conflict
               ({'target': 'volume', 'field': 'sizeLimit', 'config': ''}, '64Gi')]
        self.assertEqual(conflicting_set_args(required, ops, 'DBMS-1'), ['fsync=on (--set), the load needs off'])
        self.assertEqual(conflicting_set_args({}, ops, 'DBMS-1'), [])

    def test_server_wide_declarations_match_the_scripts(self) -> None:
        """Every script that sets a server-wide value by ALTER SYSTEM declares it, and vice versa."""
        import glob
        import re
        from bexhoma.load_durability import server_wide_settings
        files = glob.glob('experiments/**/durability-*.sql', recursive=True)
        self.assertTrue(files)
        for path in files:
            folder, name = os.path.split(path)
            text = open(path, encoding='utf-8').read()
            set_values = dict(re.findall(r'^ALTER SYSTEM SET (fsync|full_page_writes) = (\w+);$', text, re.M))
            with self.subTest(script=path):
                self.assertEqual(server_wide_settings([name], folder), set_values)
                if re.search(r'^ALTER SYSTEM SET synchronous_commit', text, re.M):
                    # wins over --set (command line) only per database
                    self.assertIn("format('ALTER DATABASE %I SET synchronous_commit", text)

    def test_restore_scripts_reset_the_database_setting(self) -> None:
        import glob
        for path in glob.glob('experiments/**/restoredurability-*.sql', recursive=True):
            text = open(path, encoding='utf-8').read()
            if 'ALTER SYSTEM RESET synchronous_commit' in text:
                with self.subTest(script=path):
                    self.assertIn("format('ALTER DATABASE %I RESET synchronous_commit'", text)

    def test_conflict_ends_loading_before_it_starts(self) -> None:
        cluster = mock.Mock()
        cluster.get_pods.return_value = ['sut-pod']
        cluster.get_pod_status.return_value = 'Running'
        cluster.get_pod_restart_counts.return_value = {}
        cfg = SimpleNamespace(
            appname='bexhoma', configuration='DBMS-1', load_durability='unsafe',
            experiment=SimpleNamespace(code='42', cluster=cluster), logger=mock.Mock(),
            loading_started=False, loading_finished=False, loading_active=True,
            loading_failed=[], loading_failed_fatal='',
            apply_load_durability=mock.Mock(),
            load_durability_conflicts=mock.Mock(return_value=['fsync=on (--set), the load needs off']))
        coordinator = LoadingCoordinator(cfg)
        coordinator.check = mock.Mock()
        coordinator.load_data = mock.Mock()
        self.assertFalse(coordinator.start_exec())
        coordinator.load_data.assert_not_called()
        self.assertIn('fsync=on', cfg.loading_failed_fatal)
        self.assertTrue(cfg.loading_finished)
        # the experiment loop aborts in its next pass
        self.assertIn('fsync=on', experiment()._loading_abort_reason(cfg, None))

    def _coordinator(self, uid_now: str, uid_first: str):
        cluster = mock.Mock()
        cluster.get_pods.return_value = ['sut-pod']
        cluster.get_pod_status.return_value = 'Running'
        cluster.get_pod_restart_counts.return_value = {}
        cluster.get_pod_uid.return_value = uid_now
        cfg = SimpleNamespace(
            appname='bexhoma', configuration='DBMS-1',
            experiment=SimpleNamespace(code='42', cluster=cluster), logger=mock.Mock(),
            loading_started=False, loading_finished=False, loading_active=True,
            loading_failed=[], loading_failed_fatal='', sut_pod_uid_at_loading_start=uid_first,
            apply_load_durability=mock.Mock(), load_durability_conflicts=mock.Mock(return_value=[]))
        coordinator = LoadingCoordinator(cfg)
        coordinator.check = mock.Mock()
        coordinator.load_data = mock.Mock()
        coordinator.load_data_asynch = mock.Mock()
        return coordinator, cfg

    def test_replaced_sut_pod_is_not_loaded_again(self) -> None:
        """P10: a SUT pod replaced after its loading started aborts the repetition (1795557106)."""
        import contextlib
        import io
        coordinator, cfg = self._coordinator(uid_now='uid-new', uid_first='uid-old')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(coordinator.start_exec())
        coordinator.load_data.assert_not_called()
        self.assertIn('replaced during loading (UID uid-old -> uid-new)', cfg.loading_failed_fatal)
        self.assertEqual(cfg.sut_pod_uid_at_loading_start, 'uid-old')
        self.assertIn('replaced', experiment()._loading_abort_reason(cfg, None))

    def test_replaced_sut_pod_during_benchmarking(self) -> None:
        """The labels of the new pod are gone during benchmarking as well; the message names the phase."""
        coordinator, cfg = self._coordinator(uid_now='uid-new', uid_first='uid-old')
        cfg.client = 3
        with contextlib_quiet():
            self.assertFalse(coordinator.start_exec())
        coordinator.load_data.assert_not_called()
        self.assertIn('replaced during benchmarking (2 rounds submitted) (UID uid-old -> uid-new)',
                      cfg.loading_failed_fatal)

    def test_replaced_sut_pod_snapshot(self) -> None:
        """The repetition ends with the abort: its snapshot names the new pod with its UID (run 1795612329)."""
        import json
        from bexhoma import sut_restarts
        coordinator, cfg = self._coordinator(uid_now='uid-new', uid_first='uid-old')
        cfg.code, cfg.num_experiment_to_apply_done = '42', 0
        cfg.experiment.cluster.get_pod_restart_counts.return_value = {'dbms': 0, 'monitor': 0}
        with tempfile.TemporaryDirectory() as folder:
            cfg.experiment.result_filename_local = lambda name: os.path.join(folder, name)
            with contextlib_quiet():
                self.assertFalse(coordinator.start_exec())
            with open(os.path.join(folder, 'bexhoma-sut-dbms-1-42-1-restarts.json')) as handle:
                self.assertEqual(json.load(handle)['sut-pod']['uid'], 'uid-new')
            self.assertEqual(sut_restarts.read_snapshot_uids(folder, '42'), {('dbms-1', '1'): {'sut-pod': 'uid-new'}})
        # without a result folder (stand-ins) the abort still happens
        coordinator, cfg = self._coordinator(uid_now='uid-new', uid_first='uid-old')
        with contextlib_quiet():
            self.assertFalse(coordinator.start_exec())
        self.assertIn('replaced', cfg.loading_failed_fatal)

    def test_first_load_records_the_uid(self) -> None:
        for uid_first in ('', 'uid-1'):
            # '': the first load; 'uid-1': the same pod again, no replacement
            coordinator, cfg = self._coordinator(uid_now='uid-1', uid_first=uid_first)
            cfg.initscript = []
            # loading goes on: stop the test where the scripts would run
            coordinator.load_data.side_effect = InterruptedError
            with self.subTest(uid_first=uid_first), contextlib_quiet(), self.assertRaises(InterruptedError):
                coordinator.start_exec()
            self.assertEqual(cfg.sut_pod_uid_at_loading_start, 'uid-1')
            self.assertEqual(cfg.loading_failed_fatal, '')


def contextlib_quiet():
    """Swallow what the code under test prints."""
    import contextlib
    import io
    return contextlib.redirect_stdout(io.StringIO())


class UnschedulableLoaderTest(unittest.TestCase):
    """A loading pod the scheduler cannot place aborts the load instead of blocking the barrier forever."""

    NOW = datetime(2026, 11, 23, 12, 0, 0)

    def abort_reason(self, minutes_unschedulable, message='0/5 nodes are available: 1 Too many pods.'):
        e = experiment()
        e.max_loading_minutes = None
        e.cluster = mock.Mock()
        e.cluster.get_jobs.return_value = ['job-1']
        e.cluster.get_job_failed.return_value = False
        e.cluster.get_pods.return_value = ['loader-pod-16'] if minutes_unschedulable is not None else []
        since = (self.NOW - timedelta(minutes=minutes_unschedulable or 0)).replace(tzinfo=timezone.utc)
        e.cluster.get_pod_unschedulable.return_value = (since, message)
        cfg = SimpleNamespace(configuration='DBMS-1', appname='bexhoma', code='42', loading_failed_fatal='',
                              loading_started=True, loading_finished=False, loading_started_at=None)
        reason = e._loading_abort_reason(cfg, self.NOW)
        if minutes_unschedulable is not None:
            e.cluster.get_pods.assert_called_once_with(app='bexhoma', component='loading', experiment='42',
                                                       configuration='DBMS-1', status='Pending')
        return reason

    def test_unschedulable_for_the_timeout_aborts(self) -> None:
        self.assertEqual(self.abort_reason(LOADING_UNSCHEDULABLE_TIMEOUT_MINUTES),
                         'Loading pod loader-pod-16 of DBMS-1 could not be scheduled for 15 minutes '
                         '(0/5 nodes are available: 1 Too many pods.); the other loading pods wait for it')

    def test_shorter_wait_continues(self) -> None:
        self.assertIsNone(self.abort_reason(LOADING_UNSCHEDULABLE_TIMEOUT_MINUTES - 1))

    def test_no_pending_pod_continues(self) -> None:
        self.assertIsNone(self.abort_reason(None))

    def test_pending_but_scheduled_continues(self) -> None:
        e = experiment()
        e.max_loading_minutes = None
        e.cluster = mock.Mock()
        e.cluster.get_jobs.return_value = []
        e.cluster.get_pods.return_value = ['loader-pod-1']   # e.g. pulling its image
        e.cluster.get_pod_unschedulable.return_value = None
        cfg = SimpleNamespace(configuration='DBMS-1', appname='bexhoma', code='42', loading_failed_fatal='',
                              loading_started=True, loading_finished=False, loading_started_at=None)
        self.assertIsNone(e._loading_abort_reason(cfg, self.NOW))

    def test_cluster_reads_the_pod_scheduled_condition(self) -> None:
        from bexhoma.clusters import Kubernetes
        cluster = Kubernetes.__new__(Kubernetes)
        since = datetime(2026, 11, 23, 11, 0, tzinfo=timezone.utc)
        unschedulable = SimpleNamespace(type='PodScheduled', status='False', reason='Unschedulable',
                                        last_transition_time=since, message='Too many pods')
        pod = SimpleNamespace(status=SimpleNamespace(conditions=[unschedulable]))
        with mock.patch.object(Kubernetes, '_read_pod', return_value=pod):
            self.assertEqual(cluster.get_pod_unschedulable('p'), (since, 'Too many pods'))
        scheduled = SimpleNamespace(type='PodScheduled', status='True', reason=None,
                                    last_transition_time=since, message=None)
        pod.status.conditions = [scheduled]
        with mock.patch.object(Kubernetes, '_read_pod', return_value=pod):
            self.assertIsNone(cluster.get_pod_unschedulable('p'))
        with mock.patch.object(Kubernetes, '_read_pod', return_value=None):
            self.assertIsNone(cluster.get_pod_unschedulable('p'))


if __name__ == '__main__':
    unittest.main()
