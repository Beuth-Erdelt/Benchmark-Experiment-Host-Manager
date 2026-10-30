"""
Tests for cluster SUT settings: worker placement (-rnw), per-component sizing,
placeholder SUT pods, scripts on all workers, always-run check scripts and
storage metrics of volumes bexhoma did not create.

Manifest tests run ``LifecycleManager.start_sut()`` against the shipped
TiDB and CockroachDB templates with the stub cluster of
:class:`tests.test_naming_conformance.SutManifestPerRunTest`.

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

import yaml

from bexhoma.benchmarks.tpch import resolve_indexing_key
from bexhoma.cli_args import make_base_parser, resource_cells, split_worker_nodes
from bexhoma.configurations.base import SutConfiguration
from bexhoma.configurations.lifecycle import pin_pods_to_nodes, sum_requested_resources
from bexhoma.configurations.loading import LoadingCoordinator

from . import test_naming_conformance as naming

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_config(filename):
    with open(os.path.join(_REPO, filename), encoding='utf-8') as f:
        return ast.literal_eval(f.read())


class SplitWorkerNodesTest(unittest.TestCase):
    """``-rnw``: '+' joins nodes of a cell, ',' separates cells, 'sut' is the -rnn node."""

    def test_no_value(self):
        self.assertEqual(split_worker_nodes(None), [None])
        self.assertEqual(split_worker_nodes(''), [None])

    def test_one_cell(self):
        self.assertEqual(split_worker_nodes('a+b+c'), [['a', 'b', 'c']])

    def test_sweep_and_sut(self):
        self.assertEqual(split_worker_nodes('sut+b,c', sut_node='a'), [['a', 'b'], ['c']])

    def test_duplicates_removed(self):
        self.assertEqual(split_worker_nodes('a+sut', sut_node='a'), [['a']])

    def test_errors(self):
        with self.assertRaises(ValueError):
            split_worker_nodes('sut+b')
        with self.assertRaises(ValueError):
            split_worker_nodes('a++b')

    def test_paired_with_resource_cells(self):
        cells = resource_cells(['4'], ['0'], ['16Gi', '32Gi'], ['0'], None, split_worker_nodes('a+b,c'))
        self.assertEqual([c['worker_nodes'] for c in cells], [['a', 'b'], ['c']])
        self.assertEqual([c['memory'] for c in cells], ['16Gi', '32Gi'])
        cells = resource_cells(['4'], ['0'], ['16Gi', '32Gi'], ['0'], None, split_worker_nodes('a+b'))
        self.assertEqual([c['worker_nodes'] for c in cells], [['a', 'b'], ['a', 'b']])
        with self.assertRaisesRegex(ValueError, 'must share one length'):
            resource_cells(['4'], ['0'], ['16Gi', '32Gi'], ['0'], None, split_worker_nodes('a,b,c'))

    def test_parser_knows_rnw(self):
        args = make_base_parser().parse_args(['-rnw', 'a+b'])
        self.assertEqual(args.request_node_worker, 'a+b')


class PinPodsToNodesTest(unittest.TestCase):
    """Node affinity plus an even spread; the template's own anti-affinity stays."""

    def test_pin(self):
        pod_spec = {'affinity': {'podAntiAffinity': {'x': 1}},
                    'topologySpreadConstraints': [{'topologyKey': 'zone'}]}
        pin_pods_to_nodes(pod_spec, ['a', 'b'], {'component': 'tikv'})
        terms = pod_spec['affinity']['nodeAffinity']['requiredDuringSchedulingIgnoredDuringExecution']
        self.assertEqual(terms['nodeSelectorTerms'][0]['matchExpressions'][0]['values'], ['a', 'b'])
        self.assertEqual(pod_spec['affinity']['podAntiAffinity'], {'x': 1})
        spread = pod_spec['topologySpreadConstraints']
        self.assertEqual(len(spread), 2)
        self.assertEqual(spread[1]['maxSkew'], 1)
        self.assertEqual(spread[1]['whenUnsatisfiable'], 'DoNotSchedule')
        self.assertEqual(spread[1]['labelSelector'], {'matchLabels': {'component': 'tikv'}})
        # idempotent: a second call replaces, not appends
        pin_pods_to_nodes(pod_spec, ['c'], {'component': 'tikv'})
        self.assertEqual(len(pod_spec['topologySpreadConstraints']), 2)


class SumRequestedResourcesTest(unittest.TestCase):
    def test_sum(self):
        docs = [
            {'kind': 'Deployment', 'metadata': {'labels': {'component': 'sut'}},
             'spec': {'replicas': 1, 'template': {'spec': {'containers': [
                 {'name': 'dbms', 'resources': {'requests': {'cpu': '500m', 'memory': '512Mi'}}},
                 {'name': 'exporter', 'resources': {'requests': {'cpu': 1, 'memory': '1Gi'}}}]}}}},
            {'kind': 'StatefulSet', 'metadata': {'labels': {'component': 'tikv'}},
             'spec': {'replicas': 3, 'template': {'spec': {'containers': [
                 {'name': 'dbms', 'resources': {'requests': {'cpu': 4, 'memory': '16Gi'}}}]}}}},
            {'kind': 'Service'},
        ]
        total = sum_requested_resources(docs)
        self.assertEqual(total['cpu'], 12.5)
        self.assertEqual(total['memory_gib'], 48.5)
        self.assertEqual(total['pods'], 4)
        self.assertEqual(total['components']['tikv'], {'replicas': 3, 'cpu': 12.0, 'memory_gib': 48.0})


class ConfigurationSettersTest(unittest.TestCase):
    def test_setters(self):
        ns = types.SimpleNamespace(data_components=None, sut_role='data', script_target='sut')
        self.assertTrue(SutConfiguration.receives_experiment_resources(ns, 'pd'))
        SutConfiguration.set_data_components(ns, ['tikv'])
        self.assertFalse(SutConfiguration.receives_experiment_resources(ns, 'pd'))
        self.assertTrue(SutConfiguration.receives_experiment_resources(ns, 'tikv'))
        SutConfiguration.set_sut_role(ns, 'placeholder')
        self.assertEqual(ns.sut_role, 'placeholder')
        SutConfiguration.set_script_target(ns, 'workers')
        self.assertEqual(ns.script_target, 'workers')
        with self.assertRaises(ValueError):
            SutConfiguration.set_sut_role(ns, 'helper')
        with self.assertRaises(ValueError):
            SutConfiguration.set_script_target(ns, 'all')


class SplitWorkerScriptsTest(unittest.TestCase):
    """With script target 'workers', shell scripts go to the workers, SQL stays with the SUT."""

    def test_split(self):
        scripts = ['checkschema-ycsb.sql', 'save-snapshot.sh']
        sut = LoadingCoordinator(types.SimpleNamespace(script_target='sut'))
        self.assertEqual(sut.split_worker_scripts(scripts), (scripts, []))
        workers = LoadingCoordinator(types.SimpleNamespace(script_target='workers'))
        self.assertEqual(workers.split_worker_scripts(scripts),
                         (['checkschema-ycsb.sql'], ['save-snapshot.sh']))


class CheckScriptsAlwaysRunTest(unittest.TestCase):
    """TPC-H/TPC-DS always get a post-load list that ends with the check script."""

    def test_no_flags_is_checks(self):
        self.assertEqual(resolve_indexing_key(False, False, False), 'Checks')

    def test_every_post_load_list_ends_with_the_check_script(self):
        for config_file in ('k8s-cluster.config', 'cluster.config'):
            volumes = _load_config(config_file)['volumes']
            for benchmark in ('tpch', 'tpcds'):
                scripts = volumes[benchmark]['initscripts']
                self.assertIn('Checks', scripts)
                post_load = [key for key in scripts
                             if key == 'Checks' or key.startswith(('Index', 'Constraints', 'Statistics'))]
                for key in post_load:
                    self.assertTrue(scripts[key][-1].startswith(f'checkschema-{benchmark}'),
                                    f'{config_file} {benchmark} {key}: {scripts[key]}')
            # every key resolve_indexing_key() can return exists for TPC-H
            for flags in [(i, c, s) for i in (False, True) for c in (False, True) for s in (False, True)]:
                self.assertIn(resolve_indexing_key(*flags), volumes['tpch']['initscripts'])

    def test_check_scripts_exist_without_braces(self):
        for benchmark in ('tpch', 'tpcds'):
            for dbms in ('PostgreSQL', 'MySQL', 'MariaDB', 'Citus', 'MonetDB', 'ClickHouse', 'ClickHouseCluster'):
                path = os.path.join(_REPO, 'experiments', benchmark, dbms, f'checkschema-{benchmark}.sql')
                self.assertTrue(os.path.isfile(path), path)
                with open(path, encoding='utf-8') as f:
                    text = f.read()
                # bexhoma may fill scripts with str.format()
                self.assertNotRegex(text, r'[{}]', path)
                text.format()

    def test_relaxed_settings_are_restored(self):
        """Every MySQL durability-relaxed.sql (-xld, WP10) saves what it relaxes, and its restore restores it.

        The init scripts relax nothing themselves any more.
        """
        for benchmark in ('tpch', 'tpcds', 'tpcc', 'ycsb', 'benchbase/tpcc'):
            folder = os.path.join(_REPO, 'experiments', benchmark, 'MySQL')
            path = os.path.join(folder, 'durability-relaxed.sql')
            with open(os.path.join(folder, 'restoredurability-relaxed.sql'), encoding='utf-8') as f:
                restore_text = f.read()
            with open(path, encoding='utf-8') as f:
                relax_text = f.read()
            relaxed = set(re.findall(r'^SET GLOBAL (\w+) =', relax_text, re.M))
            self.assertTrue(relaxed, path)
            for setting in relaxed:
                self.assertIn(f"('{setting}', @@GLOBAL.{setting})", relax_text, f'{path}: {setting} not saved')
                self.assertIn(f'SET GLOBAL {setting} = @v;', restore_text, f'{setting} not restored')
        for benchmark in ('tpch', 'tpcc', 'ycsb', 'tpcds'):
            init = os.path.join(_REPO, 'experiments', benchmark, 'MySQL', f'initschema-{benchmark}.sql')
            with open(init, encoding='utf-8') as f:
                init_text = f.read()
            self.assertEqual(set(re.findall(r'^SET GLOBAL (\w+) ?=', init_text, re.M)) - {'local_infile', 'sql_mode'},
                             set(), init)
            # memory sizes come from the template or --set, not from the init scripts
            self.assertNotRegex(init_text, r'(?m)^SET GLOBAL (innodb_buffer_pool_size|tmp_table_size|max_heap_table_size)\b')


class StartSutClusterManifestTest(naming.SutManifestPerRunTest):
    """start_sut() on the TiDB and CockroachDB templates."""

    def _start(self, template, num_worker=3):
        self.cfg.sut_template = template
        self.cfg.num_worker = num_worker
        self.cfg.storage = {'storageClassName': 'nvme', 'storageSize': '50Gi', 'keep': True}
        self.cfg.experiment.cluster.storage_classes = ['nvme']
        self.cfg.experiment.cluster.get_pvc_storage_class = lambda *a, **kw: None
        self.cfg.resources['requests'] = {'cpu': '8', 'memory': '16Gi', 'gpu': 0}
        self.cfg.resources['limits'] = {'cpu': '8', 'memory': '16Gi'}
        self.cfg.num_experiment_to_apply_done = 0
        self.cfg.lifecycle.start_sut()
        path = os.path.join(self.tmp_dir.name, next(
            p for p in os.listdir(self.tmp_dir.name) if re.match(r'bexhoma-sut-.*-1\.yml$', p)))
        with open(path, encoding='utf-8') as f:
            return [d for d in yaml.safe_load_all(f) if isinstance(d, dict)]

    @staticmethod
    def _workload(docs, kind, component):
        return next(d for d in docs if d['kind'] == kind and d['metadata']['labels']['component'] == component)

    @staticmethod
    def _dbms(doc):
        return next(c for c in doc['spec']['template']['spec']['containers'] if c['name'] == 'dbms')

    def test_all_statefulsets_get_resources_by_default(self):
        docs = self._start('deploymenttemplate-TiDB.yml')
        pd = self._workload(docs, 'StatefulSet', 'pd')
        self.assertEqual(self._dbms(pd)['resources']['requests']['memory'], '16Gi')
        self.assertEqual(pd['spec']['volumeClaimTemplates'][0]['spec']['resources']['requests']['storage'], '50Gi')

    def test_data_components_only(self):
        self.cfg.set_data_components(['tikv'])
        self.cfg.set_resources(requests_pd={'cpu': '500m'}, storage_pd='20Gi')
        docs = self._start('deploymenttemplate-TiDB.yml')
        pd = self._workload(docs, 'StatefulSet', 'pd')
        tikv = self._workload(docs, 'StatefulSet', 'tikv')
        self.assertEqual(self._dbms(pd)['resources']['requests'], {'cpu': '500m', 'memory': '512Mi'})
        self.assertEqual(self._dbms(pd)['resources']['limits'], {'cpu': '1', 'memory': '2Gi'})
        self.assertEqual(self._dbms(tikv)['resources']['requests']['memory'], '16Gi')
        claim_pd = pd['spec']['volumeClaimTemplates'][0]['spec']
        claim_tikv = tikv['spec']['volumeClaimTemplates'][0]['spec']
        self.assertEqual(claim_pd['resources']['requests']['storage'], '20Gi')
        self.assertEqual(claim_tikv['resources']['requests']['storage'], '50Gi')
        self.assertEqual(claim_pd['storageClassName'], 'nvme')
        self.assertEqual(claim_tikv['storageClassName'], 'nvme')
        total = self.cfg.connection_parameter['resources_total']
        self.assertEqual(total['components']['tikv']['replicas'], 3)
        self.assertEqual(total['components']['pd']['cpu'], 1.5)

    def test_worker_nodes(self):
        self.cfg.set_resources(nodes_worker=['a', 'b', 'c'])
        docs = self._start('deploymenttemplate-TiDB.yml')
        for component in ('pd', 'tikv'):
            spec = self._workload(docs, 'StatefulSet', component)['spec']['template']['spec']
            terms = spec['affinity']['nodeAffinity']['requiredDuringSchedulingIgnoredDuringExecution']
            self.assertEqual(terms['nodeSelectorTerms'][0]['matchExpressions'][0]['values'], ['a', 'b', 'c'])
            self.assertIn('podAntiAffinity', spec['affinity'])
            self.assertEqual(spec['topologySpreadConstraints'][-1]['labelSelector']['matchLabels']['component'],
                             component)
        sut = self._workload(docs, 'Deployment', 'sut')['spec']['template']['spec']
        self.assertNotIn('nodeAffinity', sut.get('affinity') or {})

    def test_placeholder_keeps_template_resources_but_gets_node(self):
        self.cfg.set_sut_role('placeholder')
        self.cfg.set_resources(nodeSelector={'cpu': '', 'gpu': '', 'kubernetes.io/hostname': 'n1'})
        docs = self._start('deploymenttemplate-CockroachDB.yml')
        sut = self._workload(docs, 'Deployment', 'sut')
        self.assertEqual(self._dbms(sut)['resources']['requests'], {'cpu': '250m', 'memory': '512Mi'})
        self.assertEqual(self._dbms(sut)['resources']['limits'], {'cpu': '1000m', 'memory': '1Gi'})
        self.assertEqual(sut['spec']['template']['spec']['nodeSelector']['kubernetes.io/hostname'], 'n1')
        worker = self._workload(docs, 'StatefulSet', 'worker')
        self.assertEqual(self._dbms(worker)['resources']['requests']['memory'], '16Gi')

    def test_data_sut_gets_experiment_resources(self):
        docs = self._start('deploymenttemplate-CockroachDB.yml')
        sut = self._workload(docs, 'Deployment', 'sut')
        self.assertEqual(self._dbms(sut)['resources']['requests']['memory'], '16Gi')


class StartSutClickHouseManifestTest(naming.SutManifestPerRunTest):
    """start_sut() on the ClickHouse (standalone) and ClickHouseCluster templates."""

    _start = StartSutClusterManifestTest._start
    _workload = staticmethod(StartSutClusterManifestTest._workload)
    _dbms = staticmethod(StartSutClusterManifestTest._dbms)

    @staticmethod
    def _env(container):
        return {e['name']: e.get('value') for e in container.get('env') or []}

    def test_standalone(self):
        docs = self._start('deploymenttemplate-ClickHouse.yml', num_worker=0)
        self.assertEqual([d['kind'] for d in docs if d['kind'] == 'StatefulSet'], [])
        sut = self._workload(docs, 'Deployment', 'sut')
        self.assertRegex(sut['metadata']['name'], r'^bexhoma-sut-')
        dbms = self._dbms(sut)
        self.assertEqual(dbms['resources']['requests']['memory'], '16Gi')
        self.assertEqual(self._env(dbms)['CLICKHOUSE_SKIP_USER_SETUP'], '1')
        self.assertNotIn('privileged', dbms.get('securityContext') or {})
        pvc = next(d for d in docs if d['kind'] == 'PersistentVolumeClaim')
        self.assertEqual(pvc['spec']['storageClassName'], 'nvme')
        claim = next(v for v in sut['spec']['template']['spec']['volumes'] if v['name'] == 'benchmark-storage-volume')
        self.assertEqual(claim['persistentVolumeClaim']['claimName'], pvc['metadata']['name'])
        service = next(d for d in docs if d['kind'] == 'Service')
        ports = {p['name'] for p in service['spec']['ports']}
        self.assertTrue({'port-dbms', 'port-sut-native'} <= ports)

    def test_cluster(self):
        docs = self._start('deploymenttemplate-ClickHouseCluster.yml', num_worker=3)
        sut = self._workload(docs, 'Deployment', 'sut')
        worker = self._workload(docs, 'StatefulSet', 'worker')
        self.assertEqual(worker['spec']['replicas'], 3)
        self.assertEqual(worker['spec']['serviceName'], worker['metadata']['name'])
        self.assertEqual(self._dbms(worker)['resources']['requests']['memory'], '16Gi')
        claim = worker['spec']['volumeClaimTemplates'][0]['spec']
        self.assertEqual(claim['storageClassName'], 'nvme')
        self.assertEqual(claim['resources']['requests']['storage'], '50Gi')
        # the startup scripts build remote_servers from the worker list and find the
        # coordinator's Keeper by the SUT service name
        for workload in (sut, worker):
            env = self._env(self._dbms(workload))
            hosts = env['BEXHOMA_WORKER_LIST_SPACE'].split()
            self.assertEqual(hosts, [f"{worker['metadata']['name']}-{i}.{worker['metadata']['name']}"
                                     for i in range(3)])
            self.assertEqual(env['BEXHOMA_SUT_NAME'], sut['metadata']['name'])
        services = {d['metadata']['labels']['component']: d for d in docs if d['kind'] == 'Service'}
        self.assertEqual(services['sut']['metadata']['name'], sut['metadata']['name'])
        self.assertIn('port-sut-keeper', {p['name'] for p in services['sut']['spec']['ports']})
        self.assertEqual(services['worker']['metadata']['name'], worker['metadata']['name'])
        self.assertEqual(services['worker']['spec']['clusterIP'], 'None')
        # a worker is ready only with a Keeper session: init scripts (ON CLUSTER) wait for it
        probe = self._dbms(worker)['readinessProbe']['exec']['command']
        self.assertIn('system.zookeeper', ' '.join(probe))
        self.assertEqual(self._env(self._dbms(worker))['BEXHOMA_WORKER_SERVICE'], worker['metadata']['name'])

    def test_init_scripts_match_the_cluster_name_and_tables(self):
        """The cluster scripts address cluster 'bexhoma' of the template and the standalone tables.

        A table is distributed (``<name>_local`` per shard, Distributed table on the shards
        and the coordinator, flushed by the reset) or replicated (ReplicatedMergeTree on
        the shards and the coordinator, synced by the reset); TPC-H has both placements
        (-xdim).
        """
        for benchmark, folders in (('tpch', ('ClickHouseCluster', 'ClickHouseCluster/distributed')),
                                   ('tpcds', ('ClickHouseCluster',))):
            path = os.path.join(_REPO, 'experiments', benchmark)
            with open(os.path.join(path, 'ClickHouse', f'initschema-{benchmark}.sql'), encoding='utf-8') as f:
                tables = re.findall(r'CREATE TABLE (\w+) \(', f.read())
            for folder in folders:
                with self.subTest(benchmark=benchmark, folder=folder):
                    with open(os.path.join(path, folder, f'initschema-{benchmark}.sql'), encoding='utf-8') as f:
                        cluster = f.read()
                    distributed = re.findall(r'CREATE TABLE (\w+)_local ON CLUSTER bexhoma \(', cluster)
                    # Distributed tables on the shards (ON CLUSTER) and on the coordinator (not a shard)
                    self.assertEqual(re.findall(r'CREATE TABLE (\w+)( ON CLUSTER bexhoma)? \([^;]*\) ENGINE = Distributed\(bexhoma, currentDatabase\(\), \1_local,', cluster),
                                     [(t, on_cluster) for t in distributed for on_cluster in (' ON CLUSTER bexhoma', '')])
                    replicated = re.findall(r'CREATE TABLE (\w+) ON CLUSTER bexhoma \([^;]*\) ENGINE = ReplicatedMergeTree ', cluster)
                    self.assertEqual(re.findall(r'CREATE TABLE (\w+) \([^;]*\) ENGINE = ReplicatedMergeTree ', cluster), replicated)
                    self.assertEqual(sorted(distributed + replicated), sorted(tables))
                    with open(os.path.join(path, folder, f'reset-{benchmark}.sql'), encoding='utf-8') as f:
                        reset = f.read()
                    self.assertEqual(sorted(re.findall(r'SYSTEM FLUSH DISTRIBUTED (\w+);', reset)), sorted(distributed))
                    self.assertEqual(sorted(re.findall(r'SYSTEM SYNC REPLICA ON CLUSTER bexhoma (\w+);', reset)), sorted(replicated))
        with open(os.path.join(_REPO, 'k8s', 'deploymenttemplate-ClickHouseCluster.yml'), encoding='utf-8') as f:
            self.assertIn('<bexhoma>$shards</bexhoma>', f.read())


class PvcSelectorTest(unittest.TestCase):
    """PVCs of a label selector join the volumes of the storage metrics."""

    def test_selector_adds_pvcs(self):
        calls = {}
        cluster = types.SimpleNamespace(
            get_pvc_by_selector=lambda selector: calls.setdefault('selector', selector) and ['yb-1', 'yb-2'],
            get_pvc_storage_class=lambda pvc: 'cephcsi',
            get_storage_class_info=lambda name: {'provisioner': 'rbd.csi.ceph.com', 'pool': 'p', 'kind': 'rbd'},
            get_pvc_rbd_image=lambda pvc: {'helper': 'csi-vol-a', 'yb-1': 'csi-vol-b', 'yb-2': 'csi-vol-c'}[pvc],
            get_ceph_metrics_support=lambda pool: {'pool_metrics': True, 'volume_metrics': True},
        )
        cfg = types.SimpleNamespace(
            experiment=types.SimpleNamespace(cluster=cluster), pvc_selector='app=yb-tserver',
            get_list_of_pvc=lambda: ['helper'])
        record = SutConfiguration._resolve_ceph_storage(cfg, 'cephcsi')
        self.assertEqual(calls['selector'], 'app=yb-tserver')
        for image in ('csi-vol-a', 'csi-vol-b', 'csi-vol-c'):
            self.assertIn(image, record['rbd_images'])


if __name__ == '__main__':
    unittest.main()
