"""Tests for batched, parallel metric fetching after a loop pass.

Covers that a :class:`MetricFetchBatch` runs fetches side by side, registers
components in the calling thread, repeats failed ``metrics.py`` runs one by
one, uploads ``connections.config`` once, and runs its after-actions last; that
``MetricsCollector.fetch`` honours ``register``/``upload``; that loading metrics
are fetched once per repetition and copied for later connections; and that the
copy script rewrites the header line.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest import mock

from bexhoma.configurations.benchmarking import BenchmarkRunner
from bexhoma.configurations.metrics import MetricsCollector
from bexhoma.experiments.base import ExperimentBase
from bexhoma.metric_fetching import MetricFetchBatch, fetch_failed

__all__ = []

_SH_CANDIDATES = [shutil.which('sh'), r'C:\Program Files\SmartGit\git\usr\bin\sh.exe',
                  r'C:\Program Files\Git\usr\bin\sh.exe']
_SH = next((c for c in _SH_CANDIDATES if c and os.path.isfile(c)), None)


class _FakeMetrics:
    """Records calls; ``fetch`` sleeps so that parallel runs overlap."""

    def __init__(self, outputs=None, delay=0.2):
        self.registered = []
        self.calls = []
        self.outputs = list(outputs or [])
        self.delay = delay
        self.active = 0
        self.max_active = 0
        self.lock = threading.Lock()
        self.register_threads = set()

    def register(self, component_type, title, optional=False):
        self.registered.append(component_type)
        self.register_threads.add(threading.get_ident())

    def fetch(self, register=True, upload=True, **kwargs):
        with self.lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)
            self.calls.append((kwargs['connection'], register, upload))
            output = self.outputs.pop(0) if self.outputs else 'ok'
        time.sleep(self.delay)
        with self.lock:
            self.active -= 1
        return output


def _config(metrics):
    return SimpleNamespace(metrics=metrics, upload_experiment_file=mock.Mock())


def _task(connection, component_type='benchmarking'):
    return dict(connection=connection, component_type=component_type, title='t')


class MetricFetchBatchTest(unittest.TestCase):

    def run_batch(self, batch, workers=4):
        with mock.patch('builtins.print'):
            batch.run(workers)

    def test_fetches_run_side_by_side_and_upload_once(self):
        metrics = _FakeMetrics()
        config = _config(metrics)
        batch = MetricFetchBatch()
        for tenant in range(8):
            batch.add_fetch(config, **_task(f'postgresql-{tenant}-1-1-1'))
        started = time.monotonic()
        self.run_batch(batch, workers=4)
        self.assertEqual(metrics.max_active, 4)
        self.assertLess(time.monotonic() - started, 8 * 0.2 * 0.75)
        self.assertEqual(len(metrics.calls), 8)
        self.assertTrue(all(not register and not upload for _, register, upload in metrics.calls))
        config.upload_experiment_file.assert_called_once_with('connections.config')
        self.assertEqual(len(batch), 0)

    def test_registration_happens_when_queuing(self):
        metrics = _FakeMetrics()
        batch = MetricFetchBatch()
        batch.add_fetch(_config(metrics), **_task('a', 'loading'))
        self.assertEqual(metrics.registered, ['loading'])
        self.assertEqual(metrics.register_threads, {threading.get_ident()})

    def test_one_worker_runs_one_by_one(self):
        metrics = _FakeMetrics(delay=0.01)
        batch = MetricFetchBatch()
        for tenant in range(3):
            batch.add_fetch(_config(metrics), **_task(str(tenant)))
        self.run_batch(batch, workers=1)
        self.assertEqual(metrics.max_active, 1)

    def test_failed_fetch_is_repeated_and_actions_run_last(self):
        metrics = _FakeMetrics(outputs=['ok', 'Traceback (most recent call last):\nSyntaxError'], delay=0.01)
        config = _config(metrics)
        order = []
        batch = MetricFetchBatch()
        batch.add_fetch(config, **_task('a'))
        batch.add_fetch(config, **_task('b'))
        batch.add_after(lambda: order.append(len(metrics.calls)))
        self.run_batch(batch, workers=2)
        self.assertEqual(len(metrics.calls), 3)
        self.assertEqual(order, [3])

    def test_empty_batch_does_nothing(self):
        with mock.patch('builtins.print') as printed:
            MetricFetchBatch().run(4)
        printed.assert_not_called()

    def test_fetch_failed(self):
        self.assertTrue(fetch_failed('x\nTraceback (most recent call last):\n'))
        self.assertFalse(fetch_failed('Metrics missing for CPU'))
        self.assertFalse(fetch_failed(None))


class CollectorFetchSwitchesTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        cluster = SimpleNamespace(execute_command_in_pod=mock.Mock(return_value=('', 'out', '')))
        self.cfg = SimpleNamespace(
            code='1', path=self.tmp, logger=mock.Mock(), upload_experiment_file=mock.Mock(),
            experiment=SimpleNamespace(workload={}, cluster=cluster),
            benchmark=SimpleNamespace(dbms={'c': SimpleNamespace(connectiondata={
                'monitoring': {'metrics': {'total_cpu_memory': {'query': 'q'}}}})}))
        self.collector = MetricsCollector(self.cfg)

    def fetch(self, **switches):
        with mock.patch('builtins.print'):
            return self.collector.fetch(
                connection='c', connection_file='c.config', container='dbms', component='sut',
                component_type='benchmarking', title='Benchmarking phase', experiment='1',
                time_start=0, time_end=1, metrics_type='metrics', pod_dashboard='dash', **switches)

    def test_default_registers_and_uploads(self):
        self.assertEqual(self.fetch(), 'out')
        self.assertEqual(self.cfg.experiment.workload['monitoring_components'], {'benchmarking': 'Benchmarking phase'})
        self.cfg.upload_experiment_file.assert_called_once_with('connections.config')

    def test_batch_mode_neither_registers_nor_uploads(self):
        self.fetch(register=False, upload=False)
        self.assertNotIn('monitoring_components', self.cfg.experiment.workload)
        self.cfg.upload_experiment_file.assert_not_called()


class LoadingMetricsOncePerRepetitionTest(unittest.TestCase):

    def runner(self):
        self.metrics = mock.Mock()
        cluster = SimpleNamespace(get_service_endpoints=lambda service_name: ['x'], monitor_cluster_exists=True)
        self.cfg = SimpleNamespace(
            num_experiment_to_apply_done=0, loading_metrics_fetched={}, monitoring_sut=True,
            deployment_infos={'deployment': {'sut': {'containers': ['dbms']}}},
            experiment=SimpleNamespace(cluster=cluster, components={'loader': {'sensor': True}}),
            code='1', time_loading_start=10, time_loading_end=20, metrics=self.metrics)
        return BenchmarkRunner(self.cfg)

    def load(self, runner, connection, batch):
        with mock.patch('builtins.print'):
            runner._loading_metrics(connection, connection + '.config', 'dash', batch)

    def test_first_connection_fetches_later_ones_copy(self):
        runner = self.runner()
        batch = MetricFetchBatch()
        self.load(runner, 'pg-1-1-1', batch)
        self.assertEqual([kw['component_type'] for _, kw in batch.fetches], ['loading', 'loader'])
        self.assertEqual(self.cfg.loading_metrics_fetched[1], ('pg-1-1-1', ['loading', 'loader']))
        self.load(runner, 'pg-1-2-1', batch)
        self.assertEqual(len(batch.fetches), 2)
        self.assertEqual(len(batch.after), 1)
        batch.after[0]()
        self.metrics.copy_fetched.assert_called_once_with('pg-1-1-1', 'pg-1-2-1', ['loading', 'loader'], 'dash')

    def test_next_repetition_fetches_again(self):
        runner = self.runner()
        self.load(runner, 'pg-1-1-1', None)
        self.cfg.num_experiment_to_apply_done = 1
        self.load(runner, 'pg-2-1-1', None)
        self.assertEqual(self.metrics.fetch.call_count, 4)
        self.metrics.copy_fetched.assert_not_called()


@unittest.skipIf(_SH is None, 'no sh available')
class CopyMetricsScriptTest(unittest.TestCase):

    def test_copies_csvs_of_given_types_and_renames_header(self):
        folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        files = {
            'query_loading_metric_cpu_pg-1-1-1.csv': 'pg-1-1-1\n1\n2\n',
            'query_loader_metric_cpu_pg-1-1-1.csv': 'pg-1-1-1\n3\n',
            'query_benchmarking_metric_cpu_pg-1-1-1.csv': 'pg-1-1-1\n9\n',
            'query_loading_metric_cpu_pg-1-1-11.csv': 'pg-1-1-11\n7\n',
        }
        for name, content in files.items():
            with open(os.path.join(folder, name), 'w', newline='\n') as f:
                f.write(content)
        script = os.path.join(folder, 'copy.sh')
        with open(script, 'w', newline='\n') as f:
            f.write(ExperimentBase.COPY_METRICS_SCRIPT)
        # the script uses tail and mv; on Windows they sit next to Git's sh
        env = dict(os.environ, PATH=os.path.dirname(_SH) + os.pathsep + os.environ.get('PATH', ''))
        subprocess.run([_SH, script, folder.replace('\\', '/'), 'pg-1-1-1', 'pg-1-2-1', 'loading', 'loader'],
                       check=True, env=env)
        with open(os.path.join(folder, 'query_loading_metric_cpu_pg-1-2-1.csv')) as f:
            self.assertEqual(f.read(), 'pg-1-2-1\n1\n2\n')
        self.assertTrue(os.path.isfile(os.path.join(folder, 'query_loader_metric_cpu_pg-1-2-1.csv')))
        self.assertFalse(os.path.isfile(os.path.join(folder, 'query_benchmarking_metric_cpu_pg-1-2-1.csv')))
        self.assertEqual(len(os.listdir(folder)), len(files) + 1 + 2)


if __name__ == '__main__':
    unittest.main()
