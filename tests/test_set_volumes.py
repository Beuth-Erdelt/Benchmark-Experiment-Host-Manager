"""
Tests for ``--set`` on ``emptyDir`` volumes of the SUT.

``--set KIND[NAME](@CONFIG).volume[V].FIELD=VALUE`` changes ``sizeLimit`` or
``medium`` of an ``emptyDir`` volume, e.g. the RAM-backed tmpdir of MySQL.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import types
import unittest

import yaml

from bexhoma.configurations.manifest import (
    ManifestBuilder, find_volume, memory_volume_exceeds_limit, patch_volume)
from bexhoma.experiments.base import parse_set_arg


def _load(template):
    with open('k8s/' + template) as f:
        return [d for d in yaml.safe_load_all(f) if isinstance(d, dict)]


def _workload(docs, kind, name):
    return next(d for d in docs if d.get('kind') == kind and d['metadata']['name'] == name)


def _patch(docs, set_args, configuration='MySQL-1', memory_limit=None):
    """Apply ``--set`` strings like an experiment does and return what was printed."""
    resources = {'limits': {'memory': memory_limit}} if memory_limit else {}
    builder = ManifestBuilder(types.SimpleNamespace(configuration=configuration, resources=resources))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        builder.patch_dbms_args(docs, [parse_set_arg(s) for s in set_args])
    return out.getvalue()


MYSQL_TMP = 'deployment[bexhoma-deployment-mysql].volume[mysqltmp]'


class ParseVolumeSelectorTest(unittest.TestCase):
    """The volume form of the selector and its checks."""

    def test_size_limit(self):
        sel, val = parse_set_arg(MYSQL_TMP + '.sizeLimit=64Gi')
        self.assertEqual(sel['target'], 'volume')
        self.assertEqual((sel['kind'], sel['workload'], sel['volume'], sel['field'], sel['config']),
                         ('deployment', 'bexhoma-deployment-mysql', 'mysqltmp', 'sizeLimit', ''))
        self.assertEqual(val, '64Gi')

    def test_field_case_insensitive(self):
        sel, _ = parse_set_arg(MYSQL_TMP + '.sizelimit=64Gi')
        self.assertEqual(sel['field'], 'sizeLimit')

    def test_scope_and_statefulset(self):
        sel, val = parse_set_arg('statefulset[bexhoma-worker]@Citus-2.volume[dshm].medium=')
        self.assertEqual((sel['kind'], sel['config'], sel['field'], val), ('statefulset', 'Citus-2', 'medium', ''))

    def test_container_selector_unchanged(self):
        sel, val = parse_set_arg('deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G')
        self.assertEqual(sel['target'], 'container')
        self.assertEqual((sel['container'], sel['param'], val), ('dbms', 'innodb_buffer_pool_size', '10G'))

    def test_rejects(self):
        for bad in (MYSQL_TMP + '.sizeLimit=64GB',     # not a Kubernetes quantity
                    MYSQL_TMP + '.sizeLimit=',
                    MYSQL_TMP + '.medium=disk',
                    MYSQL_TMP + '.hostPath=/tmp',      # not an allowed field
                    'deployment[x].volume[v]=1'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    parse_set_arg(bad)


class PatchVolumeTest(unittest.TestCase):
    """``patch_volume`` on single volume dicts."""

    def test_replace_size_limit(self):
        vol = {'name': 'v', 'emptyDir': {'medium': 'Memory', 'sizeLimit': '32Gi'}}
        self.assertTrue(patch_volume(vol, 'sizeLimit', '64Gi'))
        self.assertEqual(vol['emptyDir'], {'medium': 'Memory', 'sizeLimit': '64Gi'})

    def test_add_size_limit_to_empty_empty_dir(self):
        for empty in ({}, None):
            with self.subTest(empty=empty):
                vol = {'name': 'v', 'emptyDir': empty}
                self.assertTrue(patch_volume(vol, 'sizeLimit', '1Gi'))
                self.assertEqual(vol['emptyDir'], {'sizeLimit': '1Gi'})

    def test_remove_medium(self):
        vol = {'name': 'v', 'emptyDir': {'medium': 'Memory', 'sizeLimit': '32Gi'}}
        self.assertTrue(patch_volume(vol, 'medium', ''))
        self.assertEqual(vol['emptyDir'], {'sizeLimit': '32Gi'})

    def test_unchanged(self):
        vol = {'name': 'v', 'emptyDir': {'sizeLimit': '32Gi'}}
        self.assertFalse(patch_volume(vol, 'sizeLimit', '32Gi'))
        self.assertFalse(patch_volume(vol, 'medium', ''))

    def test_not_empty_dir(self):
        vol = {'name': 'v', 'persistentVolumeClaim': {'claimName': 'c'}}
        with self.assertRaises(ValueError):
            patch_volume(vol, 'sizeLimit', '1Gi')
        self.assertNotIn('emptyDir', vol)


class MemoryLimitWarningTest(unittest.TestCase):
    """A RAM-backed volume larger than the memory limit is flagged."""

    def test_exceeds(self):
        vol = {'emptyDir': {'medium': 'Memory', 'sizeLimit': '200Gi'}}
        self.assertTrue(memory_volume_exceeds_limit(vol, '128Gi'))
        self.assertFalse(memory_volume_exceeds_limit(vol, '256Gi'))

    def test_not_flagged(self):
        self.assertFalse(memory_volume_exceeds_limit({'emptyDir': {'sizeLimit': '200Gi'}}, '128Gi'))   # on disk
        self.assertFalse(memory_volume_exceeds_limit({'emptyDir': {'medium': 'Memory'}}, '128Gi'))    # no size
        vol = {'emptyDir': {'medium': 'Memory', 'sizeLimit': '200Gi'}}
        self.assertFalse(memory_volume_exceeds_limit(vol, None))
        self.assertFalse(memory_volume_exceeds_limit(vol, '0'))


class TemplateVolumeTest(unittest.TestCase):
    """``patch_dbms_args`` with volume operations on the real templates."""

    def _mysqltmp(self, docs):
        return find_volume(_workload(docs, 'Deployment', 'bexhoma-deployment-mysql'), 'mysqltmp')

    def test_mysql_tmpdir_size(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        out = _patch(docs, [MYSQL_TMP + '.sizeLimit=64Gi'], memory_limit='128Gi')
        self.assertEqual(self._mysqltmp(docs)['emptyDir'], {'medium': 'Memory', 'sizeLimit': '64Gi'})
        self.assertIn('updated deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit = 64Gi', out)
        self.assertNotIn('warning', out)

    def test_mysql_tmpdir_on_disk(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        _patch(docs, [MYSQL_TMP + '.medium=', MYSQL_TMP + '.sizeLimit=500Gi'])
        self.assertEqual(self._mysqltmp(docs)['emptyDir'], {'sizeLimit': '500Gi'})

    def test_warning_beyond_memory_limit(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        out = _patch(docs, [MYSQL_TMP + '.sizeLimit=200Gi'], memory_limit='128Gi')
        self.assertIn('warning: volume[mysqltmp] is in RAM', out)

    def test_already_set(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        out = _patch(docs, [MYSQL_TMP + '.sizeLimit=32Gi'])
        self.assertIn('already set to desired value', out)

    def test_postgresql_dshm(self):
        docs = _load('deploymenttemplate-PostgreSQL.yml')
        workload = next(d for d in docs if d.get('kind') == 'Deployment')['metadata']['name']
        _patch(docs, ['deployment[{}].volume[dshm].sizeLimit=16Gi'.format(workload)], configuration='PostgreSQL-1')
        dshm = find_volume(_workload(docs, 'Deployment', workload), 'dshm')
        self.assertEqual(dshm['emptyDir'], {'medium': 'Memory', 'sizeLimit': '16Gi'})

    def test_volume_not_found(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        out = _patch(docs, ['deployment[bexhoma-deployment-mysql].volume[nonexistent].sizeLimit=1Gi'])
        self.assertIn('volume[nonexistent] not found in deployment[bexhoma-deployment-mysql]', out)

    def test_not_an_empty_dir(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        before = yaml.safe_dump(docs)
        out = _patch(docs, ['deployment[bexhoma-deployment-mysql].volume[benchmark-storage-volume].sizeLimit=1Gi'])
        self.assertIn('is not an emptyDir, not changed', out)
        self.assertEqual(yaml.safe_dump(docs), before)

    def test_scope(self):
        op = '{}@MySQL-2.volume[mysqltmp].sizeLimit=64Gi'.format('deployment[bexhoma-deployment-mysql]')
        docs = _load('deploymenttemplate-MySQL.yml')
        _patch(docs, [op], configuration='MySQL-1')
        self.assertEqual(self._mysqltmp(docs)['emptyDir']['sizeLimit'], '32Gi')
        _patch(docs, [op], configuration='MySQL-2')
        self.assertEqual(self._mysqltmp(docs)['emptyDir']['sizeLimit'], '64Gi')

    def test_mixed_with_container_ops(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        _patch(docs, ['deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G',
                      MYSQL_TMP + '.sizeLimit=64Gi'])
        dep = _workload(docs, 'Deployment', 'bexhoma-deployment-mysql')
        dbms = next(c for c in dep['spec']['template']['spec']['containers'] if c['name'] == 'dbms')
        self.assertIn('--innodb-buffer-pool-size=10G', dbms['args'])
        self.assertEqual(self._mysqltmp(docs)['emptyDir']['sizeLimit'], '64Gi')


if __name__ == '__main__':
    unittest.main()
