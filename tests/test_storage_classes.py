"""
Tests for which storage classes an experiment may use.

The cluster may list storage classes bexhoma cannot provision on (legacy
provisioners, classes meant for other workloads). ``environment.yml`` marks
each class ``usable`` -- declared in the cluster config -- and
``resources.storage_class`` must name a usable one.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import types
import unittest

import tpch
from bexhoma import environment
from bexhoma import spec as catalog_spec
from bexhoma.cli_args import format_storage_types, split_storage_types
from bexhoma.experiments.base import ExperimentBase
from bexhoma.experiments.tpch import TpchExperiment
from tests.test_ycsb_catalog import _BASE_SPEC


def _storage_class(name):
    return types.SimpleNamespace(
        metadata=types.SimpleNamespace(name=name), provisioner='p',
        parameters={}, reclaim_policy='Delete', volume_binding_mode='Immediate',
    )


def _with_storage_class(storage_class):
    spec = copy.deepcopy(_BASE_SPEC)
    # The minimal environments below have no nodes and no monitoring section.
    del spec['placement']
    del spec['observe']
    spec['resources']['storage_class'] = storage_class
    return spec


class CollectorTest(unittest.TestCase):
    """The collector marks exactly the classes declared in the cluster config."""

    def test_declared_class_is_usable(self):
        info = environment.StorageClassInfo.from_v1storageclass(_storage_class('cephcsi'), {'cephcsi': 'cephcsi'})
        self.assertTrue(info.usable)

    def test_undeclared_class_is_listed_but_not_usable(self):
        info = environment.StorageClassInfo.from_v1storageclass(_storage_class('cephxfs'), {'cephcsi': 'cephcsi'})
        self.assertEqual(info.name, 'cephxfs')
        self.assertFalse(info.usable)


class UsableStorageClassesTest(unittest.TestCase):
    """``spec.usable_storage_classes`` reads the flag, or the alias of an older file."""

    def test_reads_the_usable_flag(self):
        environment_yml = {'storage_classes': [
            {'name': 'shared', 'usable': True},
            {'name': 'ceph', 'usable': False},
            {'name': 'cephcsi', 'usable': True},
        ]}
        self.assertEqual(catalog_spec.usable_storage_classes(environment_yml), ['cephcsi', 'shared'])

    def test_older_file_falls_back_to_the_alias(self):
        environment_yml = {'storage_classes': [
            {'name': 'cephcsi', 'alias': 'cephcsi'},
            {'name': 'cephxfs', 'alias': None},
        ]}
        self.assertEqual(catalog_spec.usable_storage_classes(environment_yml), ['cephcsi'])

    def test_no_section_means_none(self):
        self.assertEqual(catalog_spec.usable_storage_classes({}), [])


class ValidateEnvironmentTest(unittest.TestCase):
    """``spec.validate_environment`` refuses a listed but unusable class."""

    _ENVIRONMENT = {'nodes': [], 'storage_classes': [
        {'name': 'cephcsi', 'usable': True},
        {'name': 'cephxfs', 'usable': False},
    ]}

    def test_usable_class_passes(self):
        catalog_spec.validate_environment(self._ENVIRONMENT, _with_storage_class('cephcsi'))

    def test_unset_class_passes(self):
        catalog_spec.validate_environment(self._ENVIRONMENT, _with_storage_class(None))

    def test_unusable_class_is_refused_with_the_usable_ones_named(self):
        with self.assertRaisesRegex(catalog_spec.SpecError, "'cephxfs' is not a usable.*usable: cephcsi"):
            catalog_spec.validate_environment(self._ENVIRONMENT, _with_storage_class('cephxfs'))

    def test_unknown_class_is_refused(self):
        with self.assertRaisesRegex(catalog_spec.SpecError, "'ssd' is not a usable"):
            catalog_spec.validate_environment(self._ENVIRONMENT, _with_storage_class('ssd'))


class StorageTypeListTest(unittest.TestCase):
    """``-rst`` keeps its single-value meaning and adds a comma list."""

    def test_single_values_are_unchanged(self):
        for value in (None, '', 'ramdisk', 'cephcsi'):
            with self.subTest(value):
                self.assertEqual(split_storage_types(value), [value])

    def test_list_maps_empty_entries_to_ephemeral(self):
        self.assertEqual(split_storage_types('cephcsi,shared,'), ['cephcsi', 'shared', None])

    def test_format_round_trips_a_sweep(self):
        storage_types = [None, 'cephcsi', 'shared']
        self.assertEqual(split_storage_types(format_storage_types(storage_types)), storage_types)

    def test_only_tpch_supports_a_sweep(self):
        self.assertFalse(ExperimentBase.supports_storage_sweep)
        self.assertTrue(TpchExperiment.supports_storage_sweep)


class TpchStorageCellTest(unittest.TestCase):
    """``tpch.py`` pairs the storage class with the other resource lists."""

    def test_storage_sweep_makes_one_cell_per_class(self):
        cells = tpch._resource_cells(['8'], ['8'], ['32Gi'], ['32Gi'], ['cephcsi', 'shared', None])
        self.assertEqual([cell['storage_type'] for cell in cells], ['cephcsi', 'shared', None])
        self.assertEqual({cell['memory'] for cell in cells}, {'32Gi'})

    def test_storage_is_paired_with_memory_by_position(self):
        cells = tpch._resource_cells(['8'], ['8'], ['32Gi', '64Gi'], ['32Gi', '64Gi'], ['cephcsi', 'shared'])
        self.assertEqual([(cell['memory'], cell['storage_type']) for cell in cells],
                         [('32Gi', 'cephcsi'), ('64Gi', 'shared')])

    def test_length_mismatch_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'must share one length'):
            tpch._resource_cells(['8'], ['8'], ['32Gi', '64Gi'], ['32Gi', '64Gi'], ['cephcsi', 'shared', None])

    def test_without_storage_list_cells_are_unchanged(self):
        cells = tpch._resource_cells(['8'], ['8'], ['32Gi', '64Gi'], ['32Gi', '64Gi'])
        self.assertEqual(len(cells), 2)
        self.assertEqual({cell['storage_type'] for cell in cells}, {None})

    def test_storage_suffix_is_a_dns_label(self):
        self.assertEqual(tpch._storage_suffix('cephcsi'), 'cephcsi')
        self.assertEqual(tpch._storage_suffix(None), 'ephemeral')
        self.assertEqual(tpch._storage_suffix('Ceph_CSI'), 'ceph-csi')

    def _configured(self, storage_type, storage_varies):
        config = types.SimpleNamespace(storage={'storageClassName': 'cephcsi', 'storageSize': '50Gi'})
        config.set_storage = lambda **kwargs: config.storage.update(kwargs)
        tpch._set_cell_storage(config, 'postgresql-2', {'storage_type': storage_type}, storage_varies)
        return config.storage

    def test_sweep_cell_gets_its_class_and_a_volume_named_after_it(self):
        storage = self._configured('shared', storage_varies=True)
        self.assertEqual(storage['storageConfiguration'], 'postgresql-2-shared')
        self.assertEqual(storage['storageClassName'], 'shared')
        self.assertEqual(storage['storageSize'], '50Gi')

    def test_ephemeral_sweep_cell_gets_no_volume(self):
        storage = self._configured(None, storage_varies=True)
        self.assertEqual(storage['storageConfiguration'], 'postgresql-2-ephemeral')
        self.assertIsNone(storage['storageClassName'])

    def test_without_sweep_the_experiment_class_stays(self):
        storage = self._configured(None, storage_varies=False)
        self.assertEqual(storage['storageConfiguration'], 'postgresql-2')
        self.assertEqual(storage['storageClassName'], 'cephcsi')


_TPCH_SPEC = {
    'mode': 'run',
    'title': 'storage backends',
    'hypothesis': 'ephemeral disk loads faster than network storage',
    'discriminates': ['storage_class'],
    'workload': {'name': 'tpch', 'params': {'scaling_factor': 10}, 'rounds': [1], 'repetitions': 3},
    'loading': {'pods': 8},
    'systems': [{'name': 'PostgreSQL'}],
    'placement': {'sut': 'cl-worker13'},
    'resources': {
        'cpu': {'request': 8, 'limit': 8},
        'memory': {'request': '8Gi', 'limit': '8Gi'},
        'storage': {'size': '100Gi'},
    },
}


def _flag(argv, flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


class TpchArgvTest(unittest.TestCase):
    """``build_tpch_argv`` emits ``-rst`` from resources, as a list when swept, and ``-rsr``."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog('contracts/contract_catalog.yml')

    def _argv(self, storage_class=..., **storage):
        spec = copy.deepcopy(_TPCH_SPEC)
        if storage_class is not ...:
            spec['resources']['storage_class'] = storage_class
        spec['resources']['storage'].update(storage)
        return catalog_spec.build_argv(self.catalog, spec)

    def test_a_class_without_a_profile_reaches_tpch(self):
        """It used to be emitted only from a profile's requires:, so this ran ephemeral."""
        argv = self._argv('cephcsi')
        self.assertEqual(_flag(argv, '-rst'), 'cephcsi')
        self.assertIn('-rsr', argv)

    def test_remove_existing_false_keeps_the_volume(self):
        argv = self._argv('cephcsi', remove_existing=False)
        self.assertEqual(_flag(argv, '-rst'), 'cephcsi')
        self.assertNotIn('-rsr', argv)

    def test_ephemeral_emits_neither_flag(self):
        argv = self._argv()
        self.assertNotIn('-rst', argv)
        self.assertNotIn('-rsr', argv)

    def test_a_sweep_becomes_a_comma_list_tpch_reads_back(self):
        argv = self._argv(['cephcsi', 'shared', None])
        self.assertEqual(_flag(argv, '-rst'), 'cephcsi,shared,')
        self.assertIn('-rsr', argv)
        args = tpch.build_parser().parse_args(argv)
        self.assertEqual(split_storage_types(args.request_storage_type), ['cephcsi', 'shared', None])

    def test_a_sweep_pairs_with_memory_by_position(self):
        spec = copy.deepcopy(_TPCH_SPEC)
        spec['resources']['memory'] = [{'request': '8Gi', 'limit': '8Gi'}, {'request': '16Gi', 'limit': '16Gi'}]
        spec['resources']['storage_class'] = ['cephcsi', 'shared', None]
        with self.assertRaisesRegex(catalog_spec.SpecError, 'must share one length'):
            catalog_spec.build_argv(self.catalog, spec)

    def test_a_profile_requires_is_checked_per_cell(self):
        spec = copy.deepcopy(_TPCH_SPEC)
        spec['systems'] = [{'name': 'PostgreSQL', 'profile': 'analytical-ssd'}]
        spec['resources']['storage_class'] = [None, 'cephcsi']
        with self.assertRaisesRegex(catalog_spec.SpecError, "got 'cephcsi'"):
            catalog_spec.build_argv(self.catalog, spec)

    def test_ycsb_refuses_a_sweep_and_gets_fresh_volumes(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['resources']['storage_class'] = ['cephcsi', 'shared']
        with self.assertRaisesRegex(catalog_spec.SpecError, 'does not support storage sweeps'):
            catalog_spec.build_argv(self.catalog, spec)
        spec['resources']['storage_class'] = 'cephcsi'
        argv = catalog_spec.build_argv(self.catalog, spec)
        self.assertEqual(_flag(argv, '-rst'), 'cephcsi')
        self.assertIn('-rsr', argv)


class StorageShapeTest(unittest.TestCase):
    """``spec.validate_experiment`` checks the shape of the storage fields."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog('contracts/contract_catalog.yml')

    def test_malformed_storage_class_is_refused(self):
        for value in (5, [], ['cephcsi', 3], ''):
            spec = copy.deepcopy(_TPCH_SPEC)
            spec['resources']['storage_class'] = value
            with self.subTest(value), self.assertRaisesRegex(catalog_spec.SpecError, 'storage_class must be'):
                catalog_spec.validate_experiment(self.catalog, spec)

    def test_remove_existing_must_be_a_boolean(self):
        spec = copy.deepcopy(_TPCH_SPEC)
        spec['resources']['storage']['remove_existing'] = 'yes'
        with self.assertRaisesRegex(catalog_spec.SpecError, 'remove_existing must be true or false'):
            catalog_spec.validate_experiment(self.catalog, spec)

    def test_every_listed_class_is_checked_against_the_environment(self):
        spec = _with_storage_class(['cephcsi', None, 'cephxfs'])
        with self.assertRaisesRegex(catalog_spec.SpecError, "'cephxfs' is not a usable"):
            catalog_spec.validate_environment(ValidateEnvironmentTest._ENVIRONMENT, spec)

    def test_removes_existing_storage_defaults(self):
        self.assertFalse(catalog_spec.removes_existing_storage({}))
        self.assertFalse(catalog_spec.removes_existing_storage({'storage_class': [None, None]}))
        self.assertTrue(catalog_spec.removes_existing_storage({'storage_class': [None, 'shared']}))
        self.assertFalse(catalog_spec.removes_existing_storage(
            {'storage_class': 'shared', 'storage': {'remove_existing': False}}))


class StorageReusedTest(unittest.TestCase):
    """A reused volume shows in the evaluated connections; older results stay unknown."""

    def _row(self, **extra):
        from bexhoma.evaluators.base import EvaluatorBase
        connection = {
            'name': 'postgresql-1-1-1-1', 'configuration': 'PostgreSQL-1', 'phase': 'postgresql-1-1-1',
            'job': 'postgresql-1-1-1-1',
            'parameter': {'code': '1', 'numExperiment': 1, 'client': 1, 'dockerimage': 'postgres',
                          'parallelism': 1, 'num_worker': 0, 'connection_parameter': {}},
            'hostsystem': {'datadisk': 0},
            'time_loading': 10, 'time_schema': 1, 'time_generated': 0, 'time_ingested': 0, 'time_index': 0,
            'storage': {'storageClassName': 'shared', 'storageConfiguration': 'postgresql-1-shared'},
            **extra,
        }
        result = {}
        evaluator = types.SimpleNamespace(get_terminals=lambda parameters: 0)
        EvaluatorBase.add_connection_to_result(evaluator, connection, 'c', result)
        return result['c']

    def test_reuse_is_a_column(self):
        row = self._row(storage_reused=True)
        self.assertTrue(row['storage_reused'])
        self.assertEqual(row['sut_storage_storageClassName'], 'shared')

    def test_older_results_leave_it_unknown(self):
        self.assertNotIn('storage_reused', self._row())


if __name__ == '__main__':
    unittest.main()
