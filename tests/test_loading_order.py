"""
Tests for the order of Schema scripts and loading jobs.

The loop calls ``start_pod()`` right after ``start_exec()``, which runs the
Schema scripts in a background thread. ``start_pod()`` first waits until the
scripts have labeled the SUT pod ``schema=True``
(:meth:`~bexhoma.configurations.loading.LoadingCoordinator.wait_for_schema`):
the scripts create what the loaders need, e.g. the MySQL user ``root@'%'`` with
its password. Before, HammerDB on MySQL connected before the password was set.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import types
import unittest
from unittest import mock

from bexhoma.configurations.loading import LoadingCoordinator


class WaitForSchemaTest(unittest.TestCase):

    def _loader(self, labels_sequence, loading_finished=False, max_loading_minutes=None):
        calls = []

        def get_pods_labels(**kwargs):
            calls.append(kwargs)
            return labels_sequence[min(len(calls), len(labels_sequence)) - 1]
        cluster = types.SimpleNamespace(get_pods_labels=get_pods_labels)
        cfg = types.SimpleNamespace(
            experiment=types.SimpleNamespace(cluster=cluster, max_loading_minutes=max_loading_minutes),
            loading_finished=loading_finished, loading_started_at=None)
        return LoadingCoordinator(cfg), calls

    def test_polls_until_label_is_set(self):
        loader, calls = self._loader([
            {'sut': {'schema': 'False'}}, {'sut': {'schema': 'False'}}, {'sut': {'schema': 'True'}}])
        with mock.patch('bexhoma.configurations.loading.time.sleep') as sleep, \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertTrue(loader.wait_for_schema(app='bexhoma', experiment='1', configuration='MySQL-1'))
        self.assertEqual(len(calls), 3)
        self.assertEqual(sleep.call_args_list, [mock.call(2), mock.call(2)])
        self.assertEqual(calls[0], {'app': 'bexhoma', 'component': 'sut', 'experiment': '1',
                                    'configuration': 'MySQL-1'})
        self.assertIn('waits for the Schema scripts', out.getvalue())
        self.assertIn('Schema scripts done', out.getvalue())

    def test_no_wait_when_label_is_set(self):
        loader, calls = self._loader([{'sut': {'schema': 'True'}}])
        with mock.patch('bexhoma.configurations.loading.time.sleep') as sleep, \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertTrue(loader.wait_for_schema(app='a', experiment='1', configuration='c'))
        sleep.assert_not_called()
        self.assertEqual(out.getvalue(), '')

    def test_stops_when_scripts_could_not_be_uploaded(self):
        loader, calls = self._loader([{}], loading_finished=True)
        with mock.patch('bexhoma.configurations.loading.time.sleep') as sleep, \
                contextlib.redirect_stdout(io.StringIO()):
            loader.wait_for_schema(app='a', experiment='1', configuration='c')
        sleep.assert_not_called()

    def test_loading_timeout(self):
        """With --loading-timeout, the wait gives up and hands the abort to the loop's timeout."""
        loader, calls = self._loader([{'sut': {'schema': 'False'}}], max_loading_minutes=0)
        with mock.patch('bexhoma.configurations.loading.time.sleep'), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertFalse(loader.wait_for_schema(app='a', experiment='1', configuration='c'))
        self.assertIn('WARNING', out.getvalue())
        self.assertIsNotNone(loader._config.loading_started_at)

    def test_no_jobs_after_timeout(self):
        cfg = mock.Mock()
        cfg.appname, cfg.code, cfg.configuration = 'bexhoma', '1', 'MySQL-1'
        cfg.num_experiment_to_apply_done = 0
        with mock.patch.object(LoadingCoordinator, 'wait_for_schema', return_value=False):
            LoadingCoordinator(cfg).start_pod()
        cfg.experiment.cluster.create_object_from_file.assert_not_called()
        cfg.experiment.cluster.set_pod_counter.assert_not_called()

    def test_start_pod_waits_before_creating_jobs(self):
        order = []
        cfg = mock.Mock()
        cfg.appname, cfg.code, cfg.configuration = 'bexhoma', '1', 'MySQL-1'
        cfg.num_experiment_to_apply_done = 0
        cfg.experiment_dict = {'loader': [{'parallelism': 1, 'num_pods': 1}]}
        cfg.manifest.create_manifest_loading.return_value = 'loading-job.yml'
        cfg.experiment.cluster.set_pod_counter.side_effect = lambda **kw: order.append('counter')
        cfg.experiment.cluster.create_object_from_file.side_effect = lambda job: order.append('job')
        with mock.patch.object(LoadingCoordinator, 'wait_for_schema',
                               side_effect=lambda **kw: order.append('wait') or True):
            LoadingCoordinator(cfg).start_pod()
        self.assertEqual(order[0], 'wait')
        self.assertIn('job', order)


if __name__ == '__main__':
    unittest.main()
