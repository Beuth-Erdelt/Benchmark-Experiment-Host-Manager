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

from bexhoma import environment
from bexhoma import spec as catalog_spec
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


if __name__ == '__main__':
    unittest.main()
