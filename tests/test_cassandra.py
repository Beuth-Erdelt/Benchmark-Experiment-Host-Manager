"""
Tests for Cassandra (issue #824).

Cassandra has no JDBC driver: YCSB uses its cassandra-cql binding, selected by
BEXHOMA_DBMS_TYPE in the shell scripts of both images. Scripts are CQL, run by
cqlsh. Single node and cluster are two docker keys, since application metrics
are fetched per component.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import os
import re
import types
import unittest

import pandas as pd
import yaml

from bexhoma import ddl_parameters
from bexhoma.configurations.loading import script_failed
from bexhoma.evaluators.ycsb import YcsbEvaluator

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _config():
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as f:
        return ast.literal_eval(f.read())


def _manifests(template):
    with open(os.path.join(_REPO, 'k8s', template), encoding='utf-8') as f:
        return list(yaml.safe_load_all(f))


def _dbms_container(manifests, kind):
    pod = [d for d in manifests if d['kind'] == kind][0]['spec']['template']['spec']
    return [c for c in pod['containers'] if c['name'] == 'dbms'][0]


def _read(*path):
    with open(os.path.join(_REPO, *path), encoding='utf-8') as f:
        return f.read()


class CassandraTemplateTest(unittest.TestCase):
    def setUp(self):
        self.dockers = _config()['dockers']
        self.single = _manifests('deploymenttemplate-Cassandra.yml')
        self.cluster = _manifests('deploymenttemplate-CassandraCluster.yml')

    def test_image_is_pinned_to_the_configured_version(self):
        version = self.dockers['Cassandra']['template']['version']
        self.assertEqual(self.dockers['CassandraCluster']['template']['version'], version)
        self.assertRegex(version, r'^\d+\.\d+\.\d+$')
        image = 'cassandra:' + version
        self.assertEqual(_dbms_container(self.single, 'Deployment')['image'], image)
        self.assertEqual(_dbms_container(self.cluster, 'Deployment')['image'], image)
        self.assertEqual(_dbms_container(self.cluster, 'StatefulSet')['image'], image)

    def test_data_is_on_the_volume(self):
        mounts = {m['name']: m['mountPath'] for m in _dbms_container(self.single, 'Deployment')['volumeMounts']}
        self.assertEqual(mounts['benchmark-storage-volume'], self.dockers['Cassandra']['datadir'])
        mounts = {m['name']: m['mountPath'] for m in _dbms_container(self.cluster, 'StatefulSet')['volumeMounts']}
        self.assertEqual(mounts['bxw'], self.dockers['CassandraCluster']['datadir'])

    def test_cluster_nodes_join_one_after_the_other(self):
        """Parallel bootstrap is refused, and readiness has to mean: joined."""
        statefulset = [d for d in self.cluster if d['kind'] == 'StatefulSet'][0]
        self.assertEqual(statefulset['spec']['podManagementPolicy'], 'OrderedReady')
        self.assertEqual(_dbms_container(self.cluster, 'StatefulSet')['readinessProbe']['tcpSocket']['port'], 9042)

    def test_seed_comes_from_the_first_worker(self):
        self.assertIn('CASSANDRA_SEEDS="$BEXHOMA_WORKER_FIRST"', _dbms_container(self.cluster, 'StatefulSet')['command'][-1])

    def test_cluster_has_no_data_in_the_placeholder(self):
        self.assertNotIn('volumeMounts', _dbms_container(self.cluster, 'Deployment'))
        self.assertLessEqual(len(_dbms_container(self.cluster, 'Deployment')['resources']), 2)

    def test_heap_follows_the_limit_of_the_container(self):
        """cassandra-env.sh sees the RAM of the node; HEAP_NEWSIZE must stay unset with G1."""
        for container in (_dbms_container(self.single, 'Deployment'), _dbms_container(self.cluster, 'StatefulSet')):
            self.assertIn('MAX_HEAP_SIZE', container['command'][-1])
            self.assertNotIn('HEAP_NEWSIZE', container['command'][-1])
            memory = [e for e in container['env'] if e['name'] == 'MEMORY_LIMIT_MIB'][0]
            self.assertEqual(memory['valueFrom']['resourceFieldRef']['resource'], 'limits.memory')

    def test_load_command_runs_cqlsh_on_the_service(self):
        for docker in ('Cassandra', 'CassandraCluster'):
            load = self.dockers[docker]['loadData']
            self.assertTrue(load.startswith('cqlsh {service_name} 9091 '))
            self.assertIn('-f {scriptname}', load)

    def test_service_port_is_the_cql_port(self):
        for manifests in (self.single, self.cluster):
            service = [d for d in manifests if d['kind'] == 'Service' and d['metadata']['name'] == 'bexhoma-service'][0]
            ports = {p['name']: p for p in service['spec']['ports']}
            self.assertEqual((ports['port-dbms']['port'], ports['port-dbms']['targetPort']), (9091, 9042))

    def test_exporter_runs_where_the_data_is(self):
        for manifests, kind in ((self.single, 'Deployment'), (self.cluster, 'StatefulSet')):
            pod = [d for d in manifests if d['kind'] == kind][0]['spec']['template']['spec']
            exporter = [c for c in pod['containers'] if c['name'] == 'monitor-application'][0]
            self.assertRegex(exporter['image'], r':\d+\.\d+\.\d+$')
            self.assertEqual(exporter['ports'][0]['containerPort'], 8080)

    def test_exporter_heap_stays_below_its_limit(self):
        """Without -Xmx its JVM takes the RAM of the node and is OOMKilled at the limit of 1 GiB."""
        for manifests, kind in ((self.single, 'Deployment'), (self.cluster, 'StatefulSet')):
            pod = [d for d in manifests if d['kind'] == kind][0]['spec']['template']['spec']
            exporter = [c for c in pod['containers'] if c['name'] == 'monitor-application'][0]
            env = {e['name']: e['value'] for e in exporter['env']}
            self.assertEqual(env['JVM_OPTS'], '-Xmx512m')
            self.assertEqual(exporter['resources']['limits']['memory'], '1Gi')


class CassandraMonitoringTest(unittest.TestCase):
    def setUp(self):
        self.config = _config()
        self.dockers = self.config['dockers']

    def test_metrics_are_tagged_with_the_component_that_fetches_them(self):
        """monitor.py skips a metric whose component is not the one fetched."""
        self.assertEqual(list(self.dockers['Cassandra']['monitor']), ['sut'])
        self.assertEqual(list(self.dockers['CassandraCluster']['monitor']), ['worker'])

    def test_discovery_selects_the_pods_that_have_the_exporter(self):
        single = self.dockers['Cassandra']['monitor']['sut']['discovery_config']
        cluster = self.dockers['CassandraCluster']['monitor']['worker']['discovery_config']
        self.assertIn('regex: bexhoma;sut;Cassandra\n', single)
        self.assertIn('regex: bexhoma;worker;CassandraCluster\n', cluster)
        for discovery_config in (single, cluster):
            self.assertIn("replacement: '$1:8080'", discovery_config)

    def test_discovery_can_be_filled(self):
        for docker, component in (('Cassandra', 'sut'), ('CassandraCluster', 'worker')):
            text = self.dockers[docker]['monitor'][component]['discovery_config'].format(
                namespace='n', master='m', prometheus_interval='30s', prometheus_timeout='30s')
            self.assertIn('names: ["n"]', text)

    def test_metric_queries_survive_format(self):
        metrics = self.config['credentials']['k8s']['monitor']['cassandra']['metrics']
        self.assertTrue(metrics)
        for name, metric in metrics.items():
            with self.subTest(metric=name):
                query = metric['query'].format()
                self.assertRegex(query, r'cassandra_stats\{name=~?"org:apache:cassandra:metrics:')

    def test_request_rates_come_from_the_counters(self):
        """The one-minute average of the JMX meter lags behind a benchmark of seconds."""
        metrics = self.config['credentials']['k8s']['monitor']['cassandra']['metrics']
        for name in ('cassandra_read_rate', 'cassandra_write_rate'):
            self.assertIn('irate(', metrics[name]['query'])
            self.assertIn(':latency:count"', metrics[name]['query'])


class CassandraScriptsTest(unittest.TestCase):
    def test_replication_factor_is_the_ddl_parameter(self):
        declarations = ddl_parameters.load_declarations(os.path.join(_REPO, 'experiments', 'ycsb'), 'Cassandra')
        values = ddl_parameters.fill_values(declarations, ddl_parameters.resolve(declarations, {'num_worker_replicas': '3'}))
        text = ddl_parameters.fill(_read('experiments', 'ycsb', 'Cassandra', 'initschema-ycsb.sql'), values)
        self.assertIn("{'class': 'SimpleStrategy', 'replication_factor': 3}", text)

    def test_default_replication_factor_runs_on_a_single_node(self):
        declarations = ddl_parameters.load_declarations(os.path.join(_REPO, 'experiments', 'ycsb'), 'Cassandra')
        self.assertEqual(declarations['num_worker_replicas']['default'], '1')

    def test_table_has_the_columns_of_the_binding(self):
        text = _read('experiments', 'ycsb', 'Cassandra', 'initschema-ycsb.sql')
        self.assertIn('CREATE KEYSPACE ycsb', text)
        self.assertIn('CREATE TABLE ycsb.usertable', text)
        self.assertRegex(text, r'y_id\s+varchar PRIMARY KEY')
        for field in range(10):
            self.assertRegex(text, rf'field{field}\s+varchar')

    def test_check_script_does_not_scan_the_table(self):
        sql = re.sub(r'--.*', '', _read('experiments', 'ycsb', 'Cassandra', 'checkschema-ycsb.sql'))
        self.assertNotIn('usertable', sql)
        self.assertNotIn('count(', sql.lower())

    def test_snapshot_script_follows_the_reset_contract(self):
        text = _read('experiments', 'ycsb', 'Cassandra', 'save-snapshot.sh')
        self.assertNotIn('{', text)
        self.assertIn('nodetool flush ycsb usertable', text)
        self.assertIn('step 1 (statistics): n/a', text)
        self.assertIn('step 3 (counters): n/a', text)

    def test_failed_cqlsh_counts_as_failed_script(self):
        stderr = "/tmp/initschema-ycsb.sql:9:SyntaxException: line 1:0 no viable alternative\ncommand terminated with exit code 2\n"
        self.assertTrue(script_failed('', stderr))


class RowsLoadedTest(unittest.TestCase):
    """A YCSB load can end with rows missing and no other sign of it (first seen with Cassandra)."""

    @staticmethod
    def _results(inserted, pods=8, num_tenants=0, columns=('sf', 'pod_count', '[INSERT].Return=OK')):
        experiment = types.SimpleNamespace(num_tenants=num_tenants, results=[])
        experiment._record_test = lambda passed, title: experiment.results.append((passed, title))
        df_loading = pd.DataFrame({'sf': [1], 'pod_count': [pods], '[INSERT].Return=OK': [inserted]})
        YcsbEvaluator._test_rows_loaded(None, experiment, df_loading[list(columns)])
        return experiment.results

    def test_complete_load_passes(self):
        self.assertEqual(self._results(1000000), [(True, 'Loading Phase: all rows inserted')])

    def test_missing_rows_fail(self):
        [(passed, title)] = self._results(584562)
        self.assertFalse(passed)
        self.assertEqual(title, 'Loading Phase: 415438 of 1000000 rows not inserted')

    def test_remainder_of_the_split_is_no_failure(self):
        self.assertEqual(self._results(999999, pods=7)[0][0], True)

    def test_multi_tenant_is_left_out(self):
        self.assertEqual(self._results(10, num_tenants=2), [])

    def test_summary_without_the_columns_is_left_out(self):
        self.assertEqual(self._results(10, columns=('sf', 'pod_count')), [])


class CassandraImageScriptsTest(unittest.TestCase):
    def _scripts(self):
        return (_read('images', 'ycsb', 'generator', 'generator.sh'),
                _read('images', 'ycsb', 'benchmarker', 'benchmarker.sh'))

    def test_both_images_use_the_cql_binding(self):
        generator, benchmarker = self._scripts()
        self.assertEqual(generator.count('bin/ycsb load cassandra-cql '), 2)
        self.assertEqual(benchmarker.count('bin/ycsb run cassandra-cql '), 2)

    def test_cluster_is_reached_through_its_workers(self):
        """The driver uses one port for all nodes it discovers, so not the service port."""
        for script in self._scripts():
            self.assertIn('hosts=$BEXHOMA_WORKER_LIST\nport=9042', script)
            self.assertIn('hosts=$BEXHOMA_HOST\nport=$BEXHOMA_PORT', script)

    def test_failed_inserts_are_retried(self):
        """A loader thread ends at its first failed insert, its remaining rows would be missing."""
        generator, _ = self._scripts()
        branch = generator[generator.index('"$BEXHOMA_DBMS_TYPE" == "cassandra"'):generator.index('db.driver=')]
        self.assertIn('core_workload_insertion_retry_limit=10', branch)

    def test_type_is_set_in_loading_and_benchmarking(self):
        source = _read('ycsb.py')
        branch = source[source.index('if ("Cassandra" in args.dbms)'):source.index('if ("Citus" in args.dbms)')]
        self.assertEqual(branch.count('BEXHOMA_DBMS_TYPE = "cassandra"'), 2)


if __name__ == '__main__':
    unittest.main()
