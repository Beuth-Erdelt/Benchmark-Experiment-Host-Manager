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


if __name__ == '__main__':
    unittest.main()
