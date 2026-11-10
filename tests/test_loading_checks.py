"""Tests for #848: no loader pod, loading script or load fails silently."""
from __future__ import annotations

import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from bexhoma.configurations.base import SutConfiguration
from bexhoma.configurations.loading import LoadingCoordinator, loading_script_errors
from bexhoma.experiments.base import ExperimentBase
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


if __name__ == '__main__':
    unittest.main()
