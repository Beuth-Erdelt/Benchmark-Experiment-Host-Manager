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

    def test_default_is_the_old_pattern(self) -> None:
        cfg = _configuration()
        self.assertEqual(cfg.set_metric_of_config_default(self.query, host='', gpuid='', schema='', database=''),
                         'm{pod=~"(.*)postgresql-1-1792334082(.*)", namespace="perdelt"}')

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

    def test_long_job_names_are_cut_like_kubernetes(self) -> None:
        jobname = 'bexhoma-benchmarker-' + 'a' * 50 + '-1-1-1'
        pattern = self.cfg.job_pods_pattern(jobname)
        self.assertTrue(re.fullmatch(pattern, (jobname + '-')[:58] + 'qp9nt'))
        self.assertLessEqual(len((jobname + '-')[:58] + 'qp9nt'), 63)


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
