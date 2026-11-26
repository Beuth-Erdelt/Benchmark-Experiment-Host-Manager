"""Tests for scoping monitoring queries by pod (``dev/plan-metrics-pod-scope.md``, M2).

Covers the cAdvisor templates with ``{pods}``, ``{namespace}`` and the 90 s
stale-series filter; the job pod patterns built from the job names; the job
query sets in the connection file and the fetch that picks them; and the job
counting rule (first value + growth) for scoped connections.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import math
import os
import re
import shutil
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd

from bexhoma import missing_metrics
from bexhoma.configurations.base import SutConfiguration
from bexhoma.configurations.metrics import MetricsCollector
from bexhoma.experiments.base import ExperimentBase
from bexhoma.monitoring_math import counter_total, read_connections, scoped_job_connections

__all__ = []

_ROOT = Path(__file__).resolve().parent.parent
_FORMAT_KEYS = dict(host='n1', gpuid='', configuration='pg-1', experiment='123', schema='', database='',
                    pods='POD', namespace='NS', storage_class='', pool='', rbd_images='')


def _templates() -> dict:
    config = ast.literal_eval((_ROOT / 'k8s-cluster.config').read_text(encoding='utf-8'))
    return config['credentials']['k8s']['monitor']['metrics']


def _cadvisor(templates: dict) -> dict:
    return {key: metric for key, metric in templates.items() if 'container_' in metric['query']}


def _configuration() -> SutConfiguration:
    cfg = object.__new__(SutConfiguration)
    cfg.storage = {}
    cfg.storage_monitoring = None
    cfg.experiment = types.SimpleNamespace(cluster=types.SimpleNamespace(contextdata={'namespace': 'perdelt'}))
    cfg.deployment_infos = {"deployment": {"sut": {"pvc": []}}, "statefulset": {}}
    cfg.configuration = "PostgreSQL-1"
    cfg.code = "1792334082"
    cfg.appname = "bexhoma"
    return cfg


class TemplateTest(unittest.TestCase):
    """The shipped cAdvisor templates select by {pods} and {namespace}; instant ones drop stale series."""

    def test_cadvisor_templates(self) -> None:
        templates = _cadvisor(_templates())
        self.assertEqual(len(templates), 14)
        for key, metric in templates.items():
            with self.subTest(key):
                query = metric['query']
                self.assertNotIn('{configuration}-{experiment}', query)
                selectors = re.findall(r'container_[a-z_]+\{\{(.*?)\}\}', query)
                self.assertTrue(selectors)
                for selector in selectors:
                    self.assertEqual(selector.count('pod=~"{pods}"'), 1)
                    self.assertEqual(selector.count('namespace="{namespace}"'), 1)
                if 'irate(' in query:
                    self.assertEqual(len(selectors), 1)
                    self.assertNotIn('timestamp(', query)
                else:
                    self.assertEqual(len(selectors), 2)
                    self.assertIn(' and (time() - timestamp(', query)
                    self.assertIn(')) < 90)', query)
                self.assertEqual(query.count('('), query.count(')'))

    def test_all_templates_format(self) -> None:
        for key, metric in _templates().items():
            with self.subTest(key):
                formatted = metric['query'].format(**_FORMAT_KEYS)
                self.assertNotIn('{pods}', formatted)

    def test_old_template_formats_with_the_new_keys(self) -> None:
        old = 'sum(container_cpu_usage_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}})'
        self.assertEqual(old.format(**_FORMAT_KEYS),
                         'sum(container_cpu_usage_seconds_total{pod=~"(.*)pg-1-123(.*)", container="dbms"})')


class FormattingTest(unittest.TestCase):
    """{pods} defaults to the pattern the templates had literally; jobs pass their own."""

    query = 'm{{pod=~"{pods}", namespace="{namespace}"}}'

    def test_default_is_the_sut_pattern(self) -> None:
        cfg = _configuration()
        self.assertEqual(cfg.set_metric_of_config_default(self.query, host='', gpuid='', schema='', database=''),
                         'm{pod=~"bexhoma-[a-z0-9]+-postgresql-1-1792334082-.*", namespace="perdelt"}')

    def test_sut_pattern_excludes_configurations_ending_with_this_one(self) -> None:
        """#940: PG-1 and XPG-1 in one experiment."""
        pattern = SutConfiguration.sut_pods_pattern('bexhoma', 'pg-1', '1792334082')
        for pod in ('bexhoma-sut-pg-1-1792334082-6d9f7c8b5-x7k2p', 'bexhoma-pool-pg-1-1792334082-5f8d9-qp9nt'):
            with self.subTest(pod):
                self.assertTrue(re.fullmatch(pattern, pod))
        for pod in ('bexhoma-sut-xpg-1-1792334082-6d9f7c8b5-x7k2p', 'bexhoma-sut-x-pg-1-1792334082-6d9f7c8b5-x7k2p',
                    'bexhoma-sut-pg-1-17923340821-6d9f7c8b5-x7k2p', 'bx-w-pg-1-1792334082-0'):
            with self.subTest(pod):
                self.assertFalse(re.fullmatch(pattern, pod))

    def test_job_pods(self) -> None:
        cfg = _configuration()
        self.assertEqual(cfg.set_metric_of_config_default(self.query, host='', gpuid='', schema='', database='',
                                                          pods='job-[a-z0-9]{5}'),
                         'm{pod=~"job-[a-z0-9]{5}", namespace="perdelt"}')

    def test_workers_keep_their_pattern(self) -> None:
        cfg = _configuration()
        cfg.worker_metric_strip_container = False
        cfg.num_worker = 2
        cfg.get_worker_name = lambda component: f'bexhoma-{component}-postgresql-1-1792334082'
        self.assertEqual(
            cfg.set_metric_of_config(self.query, host='', gpuid='', schema='', database='', component='worker'),
            'm{pod=~"(.*)bexhoma-worker-postgresql-1-1792334082-(.*)", namespace="perdelt"}')

    def test_strip_container_branch(self) -> None:
        cfg = _configuration()
        cfg.worker_metric_strip_container = True
        self.assertEqual(
            cfg.set_metric_of_config(self.query, host='', gpuid='', schema='', database='', component='yb-tserver'),
            'm{pod=~"(.*)yb-tserver-(.*)", namespace="perdelt"}')


class JobPatternTest(unittest.TestCase):
    """Job pod patterns match exactly the pods Kubernetes names after the job."""

    def setUp(self) -> None:
        self.cfg = _configuration()

    def benchmarker(self, run='1', client='1', benchmark_run='1') -> str:
        return self.cfg.generate_component_name(
            component='benchmarker', configuration='PostgreSQL-1', experiment=self.cfg.code,
            experiment_run=run, client=client, benchmark_run=benchmark_run)

    def test_benchmarker_of_one_connection(self) -> None:
        pattern = self.cfg.job_pods_pattern(self.benchmarker())
        self.assertEqual(pattern, 'bexhoma-benchmarker-postgresql-1-1792334082-1-1-1-[a-z0-9]{5}')
        self.assertTrue(re.fullmatch(pattern, self.benchmarker() + '-qp9nt'))
        for other in (self.benchmarker(benchmark_run='10'), self.benchmarker(client='2'),
                      self.benchmarker(run='2')):
            with self.subTest(other):
                self.assertFalse(re.fullmatch(pattern, other + '-qp9nt'))

    def test_without_benchmark_index(self) -> None:
        jobname = self.benchmarker(benchmark_run='')
        self.assertEqual(jobname, 'bexhoma-benchmarker-postgresql-1-1792334082-1-1')
        pattern = self.cfg.job_pods_pattern(jobname)
        self.assertTrue(re.fullmatch(pattern, jobname + '-abcde'))
        self.assertFalse(re.fullmatch(pattern, jobname + '-1-abcde'))

    def test_loading_jobs_of_the_repetition(self) -> None:
        pattern = self.cfg.job_pods_pattern(
            self.cfg.generate_component_name(component='loading', experiment_run='1'), all_jobs_with_prefix=True)
        for data_job in ('1', '2'):
            name = self.cfg.generate_component_name(component='loading', experiment_run='1', client='1',
                                                    benchmark_run=data_job)
            self.assertTrue(re.fullmatch(pattern, name + '-x7k2p'))
        for run in ('2', '10'):
            name = self.cfg.generate_component_name(component='loading', experiment_run=run, client='1',
                                                    benchmark_run='1')
            self.assertFalse(re.fullmatch(pattern, name + '-x7k2p'))

    def test_longest_job_name_is_not_cut(self) -> None:
        jobname = 'bexhoma-benchmarker-' + 'a' * 31 + '-1-1-1'
        self.assertEqual(len(jobname), SutConfiguration.MAX_JOB_NAME)
        pattern = self.cfg.job_pods_pattern(jobname)
        self.assertTrue(re.fullmatch(pattern, jobname + '-qp9nt'))
        self.assertEqual(len(jobname + '-qp9nt'), 63)


class JobTimingTest(unittest.TestCase):
    """The timing of a job reads the logs of its own pods only (issue #939)."""

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.experiment = types.SimpleNamespace(
            path=self.tmp, cluster=types.SimpleNamespace(logger=mock.Mock()),
            result_filename_local=lambda name: os.path.join(self.tmp, name),
            _record_runtime_failure=mock.Mock())

    def log(self, filename: str, start: int, end: int) -> None:
        with open(os.path.join(self.tmp, filename), 'w') as f:
            f.write(f"BEXHOMA_START:{start}\nBEXHOMA_END:{end}\n")

    def timing(self, jobname: str, container: str) -> list:
        return ExperimentBase.extract_job_timing(self.experiment, jobname, container)

    def test_job_1_does_not_take_the_logs_of_job_10(self) -> None:
        job = 'bexhoma-loading-postgresql-1-1792334082-1-1'
        self.log(f'{job}-1-x7k2p.sensor.log', 100, 200)
        self.log(f'{job}-1-a1b2c.sensor.log', 110, 210)
        self.log(f'{job}-10-qp9nt.sensor.log', 500, 900)
        self.log(f'{job}-1-x7k2p.datagenerator.log', 50, 90)
        self.log(f'{job}-1-x7k2p.sensor.previous.log', 1, 2)
        self.log(f'{job}-1.describe.job.log', 1, 2)
        self.assertEqual(sorted(self.timing(f'{job}-1', 'sensor')), [(100, 200), (110, 210)])
        self.assertEqual(self.timing(f'{job}-10', 'sensor'), [(500, 900)])
        self.assertEqual(self.timing(f'{job}-1', 'datagenerator'), [(50, 90)])
        self.experiment._record_runtime_failure.assert_not_called()

    def test_benchmarker_of_one_round(self) -> None:
        job = 'bexhoma-benchmarker-postgresql-1-1792334082-1-1'
        self.log(f'{job}-1-qp9nt.dbmsbenchmarker.log', 100, 200)
        self.log(f'{job}-11-abcde.dbmsbenchmarker.log', 300, 400)
        self.assertEqual(self.timing(f'{job}-1', 'dbmsbenchmarker'), [(100, 200)])

    def test_longest_job_name(self) -> None:
        job = 'bexhoma-benchmarker-' + 'a' * 31 + '-1-1-1'
        self.log(f'{job}-qp9nt.dbmsbenchmarker.log', 100, 200)
        self.assertEqual(self.timing(job, 'dbmsbenchmarker'), [(100, 200)])


class JobNameLengthTest(unittest.TestCase):
    """Job names longer than Kubernetes keeps in pod names are refused before the experiment starts (#938)."""

    def setUp(self) -> None:
        self.cfg = _configuration()
        self.cfg.num_experiment_to_apply = 1
        self.cfg.experiment_dict = {'loader': [], 'benchmarker': [[{'name': 'tpch'}]]}

    def test_longest_names_take_the_last_numbers(self) -> None:
        self.cfg.num_experiment_to_apply = 3
        self.cfg.experiment_dict = {'loader': [{}] * 12, 'benchmarker': [[{}], [{}] * 10, [{}]]}
        self.assertEqual(self.cfg.longest_job_names(), [
            'bexhoma-loading-postgresql-1-1792334082-3-1-12',
            'bexhoma-benchmarker-postgresql-1-1792334082-3-3-10'])

    def test_without_rounds_only_the_loading_job(self) -> None:
        self.cfg.experiment_dict['benchmarker'] = []
        self.assertEqual(self.cfg.longest_job_names(), ['bexhoma-loading-postgresql-1-1792334082-1-1-1'])

    def test_names_of_the_test_logs_pass(self) -> None:
        self.cfg.configuration = 'ClickHouseCluster-1'
        self.cfg.check_job_name_lengths()

    def test_long_configuration_name_is_refused(self) -> None:
        self.cfg.configuration = 'ClickHouseCluster-1-abcd'
        with self.assertRaisesRegex(ValueError, r'ClickHouseCluster-1-abcd: job name '
                                    r'bexhoma-benchmarker-clickhousecluster-1-abcd-1792334082-1-1-1 has 61 '
                                    r'characters, at most 57 .* by at least 4 characters'):
            self.cfg.check_job_name_lengths()

    def test_loading_alone(self) -> None:
        self.cfg.configuration = 'ClickHouseCluster-1-abcd'
        self.cfg.check_job_name_lengths(benchmarking=False)
        self.cfg.configuration = 'ClickHouseCluster-1-abcdefg'
        with self.assertRaisesRegex(ValueError, 'bexhoma-loading-'):
            self.cfg.check_job_name_lengths(benchmarking=False)

    def test_experiment_checks_by_mode(self) -> None:
        self.cfg.configuration = 'ClickHouseCluster-1-abcd'
        for mode, refused in (('run', True), ('load', False), ('start', False), ('summary', False)):
            with self.subTest(mode):
                experiment = types.SimpleNamespace(args=types.SimpleNamespace(mode=mode), configurations=[self.cfg])
                if refused:
                    with self.assertRaises(ValueError):
                        ExperimentBase.check_job_name_lengths(experiment)
                else:
                    ExperimentBase.check_job_name_lengths(experiment)


class FetchQuerySetTest(unittest.TestCase):
    """Job components are fetched with their connection's own query set when it has one."""

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.exec = mock.Mock(return_value=('', 'out', ''))

    def fetch(self, monitoring: dict, component_type: str) -> str:
        cfg = types.SimpleNamespace(
            code='1', path=self.tmp, logger=mock.Mock(), upload_experiment_file=mock.Mock(),
            experiment=types.SimpleNamespace(workload={}, cluster=types.SimpleNamespace(execute_command_in_pod=self.exec)),
            benchmark=types.SimpleNamespace(dbms={'c': types.SimpleNamespace(connectiondata={'monitoring': monitoring})}))
        with mock.patch('builtins.print'):
            MetricsCollector(cfg).fetch(
                connection='c', connection_file='c.config', container='x', component='x',
                component_type=component_type, title='t', experiment='1', time_start=0, time_end=1,
                metrics_type='metrics', pod_dashboard='dash')
        return self.exec.call_args.kwargs['command']

    def test_query_set_per_component(self) -> None:
        metric = {'total_cpu_memory': {'query': 'q'}}
        monitoring = {'metrics': metric, 'metrics_benchmarker': metric, 'metrics_loading': metric}
        for component_type, expected in (('benchmarker', 'metrics_benchmarker'), ('loader', 'metrics_loading'),
                                         ('datagenerator', 'metrics_loading'), ('benchmarking', 'metrics'),
                                         ('loading', 'metrics')):
            with self.subTest(component_type):
                self.assertIn(f'-mt {expected} ', self.fetch(monitoring, component_type))

    def test_connection_without_job_sets(self) -> None:
        self.assertIn('-mt metrics ', self.fetch({'metrics': {'total_cpu_memory': {'query': 'q'}}}, 'benchmarker'))


def _connection(name: str, scoped: bool) -> dict:
    default = {'cpu': {'query': 'sum(x{pod=~"(.*)pg-1-123(.*)"})'}, 'node': {'query': 'node{host="n1"}'}}
    job = {'cpu': {'query': 'sum(x{pod=~"job-1-[a-z0-9]{5}"})' if scoped else default['cpu']['query']},
           'node': default['node']}
    return {'name': name, 'monitoring': {'metrics': default, 'metrics_benchmarker': job, 'metrics_loading': job}}


class ScopedConnectionsTest(unittest.TestCase):
    """A connection is scoped when its job query differs from metrics' (the template had {pods})."""

    connections = [_connection('new', True), _connection('old', False), {'name': 'older', 'monitoring': {}}]

    def test_per_component_and_metric(self) -> None:
        self.assertEqual(scoped_job_connections(self.connections, 'benchmarker', 'cpu'), {'new'})
        self.assertEqual(scoped_job_connections(self.connections, 'loader'), {'new'})
        self.assertEqual(scoped_job_connections(self.connections, 'loader', 'node'), set())
        self.assertEqual(scoped_job_connections(self.connections, 'benchmarking', 'cpu'), set())

    def test_read_connections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.assertEqual(read_connections(tmp_dir), [])
            (Path(tmp_dir) / 'connections.config').write_text(repr(self.connections))
            self.assertEqual([c['name'] for c in read_connections(tmp_dir)], ['new', 'old', 'older'])

    def test_per_connection_files_when_connections_config_was_rewritten(self) -> None:
        """test_parallel_tpch_ycsb 1792366946: DBMSBenchmarker left one connection, renamed with its client."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            folder = Path(tmp_dir)
            renamed = dict(_connection('pg-1-1-1-1', True), name='pg-1-1-1-1-1')
            (folder / 'connections.config').write_text(repr([renamed]))
            for name in ('pg-1-1-1-1', 'pg-1-1-1-2'):
                (folder / f'{name}.config').write_text(repr([_connection(name, True)]))
            (folder / 'queries.config').write_text(repr({'name': 'q', 'queries': []}))
            connections = read_connections(folder)
            self.assertEqual(scoped_job_connections(connections, 'benchmarker', 'cpu'),
                             {'pg-1-1-1-1-1', 'pg-1-1-1-1', 'pg-1-1-1-2'})
            # a changed file is read again
            (folder / 'pg-1-1-1-2.config').write_text(repr([_connection('pg-1-1-1-2', False)]))
            os.utime(folder / 'pg-1-1-1-2.config', ns=(1, 1))
            self.assertNotIn('pg-1-1-1-2', scoped_job_connections(read_connections(folder), 'benchmarker', 'cpu'))


class ScopedCounterTest(unittest.TestCase):
    """Scoped job counters: first value + positive steps; unscoped ones keep max - min."""

    def total(self, values, scoped=True) -> float:
        df = pd.DataFrame({'c': values})
        return counter_total(df, 'loader', {'c'} if scoped else ())['c']

    def test_single_scrape_counts(self) -> None:
        """tenancy_2 1792334082: a 45 s loader with one sample and zero padding."""
        self.assertAlmostEqual(self.total([158.0, 158.0, 0.0, 0.0]), 158.0)
        self.assertAlmostEqual(self.total([158.0, 158.0, 0.0, 0.0], scoped=False), 158.0)

    def test_first_value_is_growth(self) -> None:
        self.assertAlmostEqual(self.total([151.0, 160.0, 167.0]), 167.0)
        self.assertAlmostEqual(self.total([151.0, 160.0, 167.0], scoped=False), 16.0)

    def test_gap_counts_only_the_step(self) -> None:
        self.assertAlmostEqual(self.total([100.0, 110.0, float('nan'), 125.0]), 125.0)

    def test_finished_pod_leaving_the_sum_is_not_subtracted_or_recounted(self) -> None:
        # two pods of one job: 50 + 30, the first finishes and drops out, the second grows
        self.assertAlmostEqual(self.total([80.0, 90.0, 40.0, 45.0]), 95.0)

    def test_leading_gap_and_empty_column(self) -> None:
        self.assertAlmostEqual(self.total([float('nan'), 20.0, 30.0]), 30.0)
        self.assertTrue(math.isnan(self.total([float('nan'), float('nan')])))

    def test_sut_components_ignore_scoping(self) -> None:
        df = pd.DataFrame({'c': [526.7, 621.0, 94.8, 487.7]})
        self.assertAlmostEqual(counter_total(df, 'loading', {'c'})['c'], 487.2)

    def test_mixed_columns(self) -> None:
        df = pd.DataFrame({'new': [151.0, 167.0], 'old': [151.0, 167.0]})
        result = counter_total(df, 'benchmarker', {'new'})
        self.assertEqual(result.to_dict(), {'new': 167.0, 'old': 16.0})


class ShortWindowTest(unittest.TestCase):
    """A scoped job needs one scrape (1.2 x I), an unscoped one two (2 x I)."""

    def test_missing_metrics_threshold_per_connection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            (result_dir / 'connections.config').write_text(repr([_connection('new', True), _connection('old', False)]))
            for connection in ('new', 'old'):
                (result_dir / missing_metrics.fetch_log_name(connection, 'benchmarker')).write_text(
                    "### python metrics.py\nInterval length 45s\n"
                    f"ERROR:root:Metrics missing for CPU (sum(x)) for connection {connection}: http://p\n")
            missing = missing_metrics.collect_missing_metrics(result_dir, scrape_interval=30)
        self.assertEqual({entry.connection: entry.expected for entry in missing},
                         {'new': '', 'old': missing_metrics.EXPECTED_SHORT_PHASE})


if __name__ == '__main__':
    unittest.main()
