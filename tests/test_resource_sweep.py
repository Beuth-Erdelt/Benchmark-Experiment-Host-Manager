"""
Tests for resource sweeps across every DBMS of a workload.

``-rc/-lc/-rr/-lr/-rst`` may each carry a comma list. The entry scripts build
each DBMS once, and :meth:`~bexhoma.experiments.base.ExperimentBase.expand_resource_cells`
(called by ``process()``) clones every configuration once per resource cell.
These tests build real experiments through ``tpch.run`` and ``ycsb.run``
against :class:`~tests.stubs.StubCluster`, with ``process()`` patched out, and
then expand the cells as ``process()`` would.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import tempfile
import unittest
from unittest import mock

import tpch
import ycsb
from bexhoma.experiments.tpch import TpchExperiment
from bexhoma.experiments.ycsb import YcsbExperiment
from bexhoma.experiments.base import ExperimentBase

from .stubs import StubCluster


class _SweepStubCluster(StubCluster):
    """``StubCluster`` with the storage classes, ``ycsb`` volume and dockers these tests use."""

    def __init__(self, resultfolder: str) -> None:
        super().__init__(resultfolder)
        self.contextdata = {'clustername': 'stub'}
        self.storage_classes = ['cephcsi', 'shared']
        self.volumes['ycsb'] = {'id': 'ycsb', 'initscripts': {'Schema': [], 'SchemaTenant': [], 'Checks': []}}
        for dbms in ('DatabaseService', 'PGBouncer', 'Dragonfly', 'Redis'):
            self.dockers[dbms] = {}


class _SweepTestBase(unittest.TestCase):
    experiment_class = TpchExperiment
    module = tpch

    def setUp(self) -> None:
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        self.cluster = _SweepStubCluster(resultfolder=tmp_dir.name)
        self.captured = None

        def capture(experiment_self):
            self.captured = experiment_self

        for patch in (
            mock.patch.object(self.module.clusters, 'Kubernetes', return_value=self.cluster),
            mock.patch.object(self.experiment_class, 'process', capture),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    def _build(self, *argv):
        args = self.module.build_parser().parse_args(['run', *argv])
        self.module.run(args)
        return self.captured

    def _expanded(self, *argv):
        experiment = self._build(*argv)
        experiment.expand_resource_cells()
        return {config.configuration: config for config in experiment.configurations}


class TpchSweepTest(_SweepTestBase):
    """Every TPC-H DBMS is swept, not only PostgreSQL and PgDuckDB."""

    def test_every_dbms_gets_one_configuration_per_cell(self):
        configs = self._expanded('-dbms', 'PostgreSQL', 'MonetDB', 'MySQL', 'MariaDB',
                                 '-rr', '32Gi,64Gi', '-lr', '32Gi,64Gi', '-rc', '8')
        self.assertEqual(sorted(configs), [
            'MariaDB-1', 'MariaDB-2', 'MonetDB-1', 'MonetDB-2',
            'MySQL-1', 'MySQL-2', 'PostgreSQL-1', 'PostgreSQL-2'])
        for name, memory in (('MonetDB-1', '32Gi'), ('MonetDB-2', '64Gi')):
            self.assertEqual(configs[name].resources['requests'], {'cpu': '8', 'memory': memory, 'gpu': 0})
            self.assertEqual(configs[name].resources['limits'], {'cpu': '0', 'memory': memory})
        self.assertEqual(configs['MonetDB-2'].alias, 'MonetDB@2')
        self.assertEqual(configs['MonetDB-2'].storage['storageConfiguration'], 'monetdb-2')

    def test_names_match_the_catalog_scopes_of_before(self):
        """``build_tpch_argv`` scopes ``--set`` to ``PostgreSQL-{cell}`` and ``PgDuckDB-{cell}``."""
        configs = self._expanded('-dbms', 'PostgreSQL', 'PgDuckDB', '-rc', '8,16', '-lc', '8,16')
        self.assertEqual(sorted(configs), ['PgDuckDB-1', 'PgDuckDB-2', 'PostgreSQL-1', 'PostgreSQL-2'])
        self.assertEqual(configs['PostgreSQL-2'].storage['storageConfiguration'], 'postgresql-2')
        self.assertEqual(configs['PgDuckDB-1'].storage['storageConfiguration'], 'PgDuckDB-1')
        self.assertEqual(configs['PostgreSQL-1'].alias, 'PostgreSQL@1')

    def test_storage_sweep_sets_the_class_per_cell(self):
        configs = self._expanded('-dbms', 'MonetDB', '-rst', 'cephcsi,shared,', '-rss', '50Gi')
        self.assertEqual(
            [(name, config.storage['storageClassName'], config.get_storage_configuration())
             for name, config in sorted(configs.items())],
            [('MonetDB-1', 'cephcsi', 'monetdb-1-cephcsi'),
             ('MonetDB-2', 'shared', 'monetdb-2-shared'),
             ('MonetDB-3', None, 'monetdb-3')])
        self.assertEqual({config.storage['storageSize'] for config in configs.values()}, {'50Gi'})

    def test_clones_do_not_share_state(self):
        configs = self._expanded('-dbms', 'MonetDB', '-rr', '32Gi,64Gi')
        first, second = configs['MonetDB-1'], configs['MonetDB-2']
        self.assertIsNot(first.loading_parameters, second.loading_parameters)
        self.assertIsNot(first.experiment_dict, second.experiment_dict)
        self.assertIs(first.experiment, second.experiment)
        self.assertIs(second.lifecycle._config, second)
        self.assertEqual(first.loading_parameters, second.loading_parameters)
        self.assertEqual(first.benchmark_list, second.benchmark_list)

    def test_several_configurations_of_one_dbms_keep_their_names(self):
        """A loading-pods sweep gives MonetDB twice; each is swept on its own.

        Both already share the volume ``monetdb``; per cell they still share
        one (``monetdb-1``, ``monetdb-2``), but never across cells."""
        experiment = self._build('-dbms', 'MonetDB', '-nlp', '1,2', '-rr', '32Gi,64Gi')
        originals = [config.configuration for config in experiment.configurations]
        experiment.expand_resource_cells()
        names = [config.configuration for config in experiment.configurations]
        self.assertEqual(names, [f'{original}-{cell}' for original in originals for cell in (1, 2)])
        self.assertEqual(
            [(config.storage['storageConfiguration'], config.resources['requests']['memory'])
             for config in experiment.configurations],
            [('monetdb-1', '32Gi'), ('monetdb-2', '64Gi')] * 2)

    def test_database_service_is_kept_once(self):
        configs = self._expanded('-dbms', 'MonetDB', 'DatabaseService', '-rr', '32Gi,64Gi')
        services = [config for config in configs.values() if config.docker == 'DatabaseService']
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].resources['requests']['memory'], '32Gi')

    def test_without_sweep_nothing_changes(self):
        experiment = self._build('-dbms', 'PostgreSQL', 'MonetDB', '-rr', '32Gi')
        before = [(config.configuration, config.alias) for config in experiment.configurations]
        experiment.expand_resource_cells()
        self.assertEqual([(config.configuration, config.alias) for config in experiment.configurations], before)
        self.assertEqual(experiment.configurations[0].storage['storageConfiguration'], 'postgresql')
        self.assertEqual(experiment.configurations[0].resources['requests']['memory'], '32Gi')

    def test_experiment_default_is_the_first_cell(self):
        experiment = self._build('-dbms', 'MonetDB', '-rr', '32Gi,64Gi', '-rst', 'cephcsi,shared')
        self.assertEqual(experiment.resources['requests']['memory'], '32Gi')
        self.assertEqual(experiment.storage['storageClassName'], 'cephcsi')

    def test_expanding_twice_does_nothing(self):
        experiment = self._build('-dbms', 'MonetDB', '-rr', '32Gi,64Gi')
        experiment.expand_resource_cells()
        experiment.expand_resource_cells()
        self.assertEqual(len(experiment.configurations), 2)

    def test_length_mismatch_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'must share one length'):
            self._build('-dbms', 'MonetDB', '-rr', '32Gi,64Gi', '-rst', 'cephcsi,shared,')


class YcsbSweepTest(_SweepTestBase):
    """YCSB sweeps its DBMS the same way."""

    experiment_class = YcsbExperiment
    module = ycsb

    def test_every_dbms_gets_one_configuration_per_cell(self):
        configs = self._expanded('-dbms', 'PostgreSQL', 'MySQL', '-rc', '4,8', '-lc', '4,8',
                                 '-rst', 'cephcsi', '-rss', '10Gi')
        self.assertEqual(sorted(configs), ['MySQL-1', 'MySQL-2', 'PostgreSQL-1', 'PostgreSQL-2'])
        self.assertEqual(configs['PostgreSQL-2'].resources['requests']['cpu'], '8')
        self.assertEqual(configs['MySQL-1'].resources['limits']['cpu'], '4')
        self.assertEqual(configs['MySQL-2'].storage['storageConfiguration'], 'mysql-2')
        self.assertEqual(configs['MySQL-2'].storage['storageClassName'], 'cephcsi')
        self.assertEqual(configs['MySQL-2'].get_storage_configuration(), 'mysql-2-cephcsi')

    def test_catalog_scopes_name_the_expanded_configurations(self):
        """The ``--set`` scopes ``build_ycsb_argv`` emits land on real cells."""
        import copy
        import re
        from bexhoma import spec as catalog_spec
        from tests.test_ycsb_catalog import _BASE_SPEC
        spec = copy.deepcopy(_BASE_SPEC)
        del spec['observe']  # the stub cluster has no monitoring config
        spec['systems'] = [{'name': 'PostgreSQL', 'profile': 'analytical-ssd'}]
        spec['resources']['memory'] = [{'request': '16Gi', 'limit': '16Gi'}, {'request': '32Gi', 'limit': '32Gi'}]
        spec['resources']['storage_class'] = None
        argv = catalog_spec.build_argv(catalog_spec.load_catalog('contracts/contract_catalog.yml'), spec)
        scopes = {match.group(1) for token in argv for match in [re.search(r'@([A-Za-z0-9-]+)\.container', token)] if match}
        self.module.run(self.module.build_parser().parse_args(argv))
        self.captured.expand_resource_cells()
        names = {config.configuration for config in self.captured.configurations}
        self.assertEqual(scopes, {'PostgreSQL-1', 'PostgreSQL-2'})
        self.assertEqual(names, scopes)


class SupportTest(unittest.TestCase):
    """Only experiments that opt in accept a sweep."""

    def test_the_database_workloads_opt_in(self):
        from bexhoma.experiments.tpcds import TpcdsExperiment
        from bexhoma.experiments.tpcc import TpccExperiment
        from bexhoma.experiments.benchbase import BenchbaseExperiment
        self.assertFalse(ExperimentBase.supports_storage_sweep)
        for experiment_class in (TpchExperiment, TpcdsExperiment, YcsbExperiment, TpccExperiment, BenchbaseExperiment):
            with self.subTest(experiment_class.__name__):
                self.assertTrue(experiment_class.supports_storage_sweep)


if __name__ == '__main__':
    unittest.main()
