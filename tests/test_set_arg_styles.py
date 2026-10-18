"""
Tests for ``--set`` arg styles and environment targets.

``--set`` writes PostgreSQL ``-c key=value`` pairs, MySQL/MariaDB
``--key=value`` elements (style from the ``bexhoma/arg-style`` annotation or
detected from the args), and container environment variables via
``container[C].env.NAME``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import types
import unittest

import yaml

from bexhoma import spec as catalog_spec
from bexhoma.configurations.manifest import (
    ARG_STYLE_FLAG, ARG_STYLE_PG, ManifestBuilder, detect_arg_style, ensure_arg_flags, ensure_env,
    patch_container)
from bexhoma.experiments.base import parse_set_arg
from bexhoma.experiments.tpch_catalog import _env_set_arg


def _load(template):
    with open('k8s/' + template) as f:
        return [d for d in yaml.safe_load_all(f) if isinstance(d, dict)]


def _workload(docs, kind, name):
    return next(d for d in docs if d.get('kind') == kind and d['metadata']['name'] == name)


def _container(doc, name='dbms'):
    return next(c for c in doc['spec']['template']['spec']['containers'] if c['name'] == name)


def _env_value(container, name):
    return next(e.get('value') for e in container['env'] if e['name'] == name)


class EnsureArgFlagsTest(unittest.TestCase):
    """``--key=value`` elements: replace in place, append, hyphen/underscore."""

    def test_replace_keeps_template_spelling(self):
        args = ensure_arg_flags(['--max_connections=1500', '--innodb-buffer-pool-size=96G'],
                                [('innodb_buffer_pool_size', '10G')])
        self.assertEqual(args, ['--max_connections=1500', '--innodb-buffer-pool-size=10G'])

    def test_append_when_missing(self):
        args = ensure_arg_flags(['--max_connections=1500'], [('innodb_log_buffer_size', '1G')])
        self.assertEqual(args, ['--max_connections=1500', '--innodb_log_buffer_size=1G'])

    def test_valueless_flag_untouched(self):
        args = ensure_arg_flags(['--skip-log-bin'], [('max_connections', '10')])
        self.assertEqual(args, ['--skip-log-bin', '--max_connections=10'])

    def test_second_update_of_appended_key_replaces(self):
        args = ensure_arg_flags([], [('a_b', '1'), ('a-b', '2')])
        self.assertEqual(args, ['--a_b=2'])


class EnsureEnvTest(unittest.TestCase):
    """``env`` list: set, replace, valueFrom entries."""

    def test_append(self):
        self.assertEqual(ensure_env([{'name': 'A', 'value': '1'}], 'B', 2),
                         [{'name': 'A', 'value': '1'}, {'name': 'B', 'value': '2'}])

    def test_replace(self):
        self.assertEqual(ensure_env([{'name': 'A', 'value': '1'}], 'A', '3'), [{'name': 'A', 'value': '3'}])

    def test_replace_value_from(self):
        env = ensure_env([{'name': 'A', 'valueFrom': {'fieldRef': {'fieldPath': 'x'}}}], 'A', 'v')
        self.assertEqual(env, [{'name': 'A', 'value': 'v'}])

    def test_input_not_mutated(self):
        original = [{'name': 'A', 'value': '1'}]
        ensure_env(original, 'A', '2')
        self.assertEqual(original, [{'name': 'A', 'value': '1'}])


class DetectArgStyleTest(unittest.TestCase):
    """Annotation wins; otherwise the args decide; default is PostgreSQL style."""

    def test_annotation(self):
        doc = {'metadata': {'annotations': {'bexhoma/arg-style': 'flag'}}}
        self.assertEqual(detect_arg_style(doc, ['-c', 'a=1']), ARG_STYLE_FLAG)

    def test_detect_pg(self):
        self.assertEqual(detect_arg_style({}, ['-c', 'a=1']), ARG_STYLE_PG)

    def test_detect_flag(self):
        self.assertEqual(detect_arg_style({}, ['--a=1']), ARG_STYLE_FLAG)

    def test_default_pg(self):
        self.assertEqual(detect_arg_style({}, []), ARG_STYLE_PG)
        self.assertEqual(detect_arg_style({'metadata': {'annotations': None}}, None), ARG_STYLE_PG)


class TemplatePatchTest(unittest.TestCase):
    """``--set`` on the shipped templates."""

    def test_mysql_template_flag_style(self):
        docs = _load('deploymenttemplate-MySQL.yml')
        sel, val = parse_set_arg(
            'deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G')
        dep = _workload(docs, 'Deployment', 'bexhoma-deployment-mysql')
        self.assertTrue(patch_container(dep, sel['container'], sel['param'], val))
        args = _container(dep)['args']
        self.assertIn('--innodb-buffer-pool-size=10G', args)
        self.assertNotIn('--innodb-buffer-pool-size=96G', args)
        self.assertNotIn('-c', args)
        self.assertNotIn('--mysql-native-password=ON', args)

    def test_mariadb_template_flag_style_append(self):
        docs = _load('deploymenttemplate-MariaDB.yml')
        dep = _workload(docs, 'Deployment', 'bexhoma-deployment-mariadb')
        self.assertTrue(patch_container(dep, 'dbms', 'innodb_flush_log_at_trx_commit', '1'))
        args = _container(dep)['args']
        self.assertIn('--innodb-flush-log-at-trx-commit=1', args)
        self.assertNotIn('--innodb-buffer-pool-chunk-size=2G', args)

    def test_postgresql_template_unaffected(self):
        docs = _load('deploymenttemplate-PostgreSQL.yml')
        dep = _workload(docs, 'Deployment', 'bexhoma-deployment-postgres')
        self.assertTrue(patch_container(dep, 'dbms', 'shared_buffers', '4GB'))
        args = _container(dep)['args']
        self.assertIn('shared_buffers=4GB', args)
        self.assertFalse(any(a.startswith('--shared_buffers') for a in args))

    def test_env_on_statefulset(self):
        docs = _load('deploymenttemplate-DragonflyCluster.yml')
        sel, val = parse_set_arg(
            'statefulset[bexhoma-worker].container[dbms].env.DFLY_snapshot_cron=* * * * *')
        self.assertEqual(sel['param'], 'env.DFLY_snapshot_cron')
        sts = _workload(docs, 'StatefulSet', 'bexhoma-worker')
        args_before = _container(sts).get('args')
        self.assertTrue(patch_container(sts, sel['container'], sel['param'], val))
        c = _container(sts)
        self.assertEqual(_env_value(c, 'DFLY_snapshot_cron'), '* * * * *')
        self.assertEqual(c.get('args'), args_before)
        # replace the template default
        self.assertTrue(patch_container(sts, 'dbms', 'env.DFLY_maxmemory', '12GiB'))
        self.assertEqual(_env_value(_container(sts), 'DFLY_maxmemory'), '12GiB')

    def test_dragonfly_maxmemory_not_on_command_line(self):
        for template in ('deploymenttemplate-Dragonfly.yml', 'deploymenttemplate-DragonflyCluster.yml',
                         'deploymenttemplate-DragonflyReplica.yml'):
            for doc in _load(template):
                if doc.get('kind') not in ('Deployment', 'StatefulSet'):
                    continue
                c = _container(doc)
                self.assertNotIn('--maxmemory', ' '.join(c.get('command') or []), template)
                self.assertTrue(_env_value(c, 'DFLY_maxmemory'), template)


class PatchDbmsArgsScopeTest(unittest.TestCase):
    """``@CONFIG`` scope applies to env targets as to args."""

    def _builder(self, configuration):
        return ManifestBuilder(types.SimpleNamespace(configuration=configuration))

    def test_scope(self):
        op = parse_set_arg('deployment[bexhoma-deployment-mysql]@MySQL-2.container[dbms].env.X=1')
        docs = _load('deploymenttemplate-MySQL.yml')
        self._builder('MySQL-1').patch_dbms_args(docs, [op])
        dep = _workload(docs, 'Deployment', 'bexhoma-deployment-mysql')
        self.assertNotIn('X', [e['name'] for e in _container(dep)['env']])
        self._builder('MySQL-2').patch_dbms_args(docs, [op])
        self.assertEqual(_env_value(_container(dep), 'X'), '1')


class CatalogArgStyleTest(unittest.TestCase):
    """Catalog knobs: mysql-flag goes through plain ``--set``, env-var through ``env.NAME``."""

    def test_styles(self):
        self.assertIn(catalog_spec.ARG_STYLE_MYSQL_FLAG, catalog_spec.ARG_STYLES_VIA_SET)
        self.assertIn(catalog_spec.DEFAULT_ARG_STYLE, catalog_spec.ARG_STYLES_VIA_SET)

    def test_env_set_arg(self):
        resolved = types.SimpleNamespace(name='Dragonfly', deployment='bexhoma-deployment-dragonfly')
        knob = catalog_spec.ResolvedKnob(name='snapshot', value='* * * * *', arg_style='env-var',
                                         env_var='DFLY_snapshot_cron')
        s = _env_set_arg(resolved, '@Dragonfly-1', knob)
        sel, val = parse_set_arg(s)
        self.assertEqual(sel['param'], 'env.DFLY_snapshot_cron')
        self.assertEqual(sel['config'], 'Dragonfly-1')
        self.assertEqual(val, '* * * * *')

    def test_env_set_arg_requires_env_var(self):
        resolved = types.SimpleNamespace(name='X', deployment='d')
        knob = catalog_spec.ResolvedKnob(name='k', value=1, arg_style='env-var')
        with self.assertRaises(catalog_spec.SpecError):
            _env_set_arg(resolved, '', knob)


if __name__ == '__main__':
    unittest.main()
