"""
Tests for CedarDB (issues #513, #830).

CedarDB refuses weak passwords, has no trust authentication and no psql in its
image, so the password and the client are wired in several places that must
stay in step. Its scripts avoid what CedarDB does not implement.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import glob
import os
import re
import unittest

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_NOT_IN_CEDARDB = ('CHECKPOINT;', 'query_to_xml', 'pg_stat_wal', 'pg_stat_bgwriter', 'pg_stat_reset')


def _config():
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as f:
        return ast.literal_eval(f.read())


def _deployment():
    with open(os.path.join(_REPO, 'k8s', 'deploymenttemplate-CedarDB.yml'), encoding='utf-8') as f:
        return [d for d in yaml.safe_load_all(f) if d['kind'] == 'Deployment'][0]


class CedarDBWiringTest(unittest.TestCase):
    def setUp(self):
        self.docker = _config()['dockers']['CedarDB']
        self.pod = _deployment()['spec']['template']['spec']
        self.dbms = [c for c in self.pod['containers'] if c['name'] == 'dbms'][0]
        self.env = {e['name']: e['value'] for e in self.dbms['env']}

    def test_password_is_the_same_everywhere(self):
        password = self.docker['template']['JDBC']['auth'][1]
        self.assertEqual(self.env['CEDAR_PASSWORD'], password)
        self.assertEqual(self.env['PGPASSWORD'], password)
        self.assertEqual(self.docker['client_env']['PGPASSWORD'], password)

    def test_password_passes_the_image_and_sed(self):
        password = self.docker['template']['JDBC']['auth'][1]
        self.assertGreaterEqual(len(password), 20)
        self.assertRegex(password, r'^[A-Za-z0-9]+$')

    def test_image_is_pinned_to_the_configured_version(self):
        self.assertEqual(self.dbms['image'], 'cedardb/cedardb:' + self.docker['template']['version'])

    def test_load_client_comes_from_the_init_container(self):
        mounts = {m['name']: m['mountPath'] for m in self.dbms['volumeMounts']}
        self.assertEqual(mounts['pgclient'], '/pgclient')
        self.assertIn('pgclient', [v['name'] for v in self.pod['volumes']])
        self.assertIn('include-client', [c['name'] for c in self.pod['initContainers']])
        self.assertTrue(self.docker['loadData'].startswith('/pgclient/psql '))

    def test_load_client_stays_without_a_storage_volume(self):
        from bexhoma.configurations.lifecycle import init_containers_without_storage
        self.assertEqual(init_containers_without_storage(self.pod['initContainers']), self.pod['initContainers'])

    def test_only_the_load_client_stays_without_a_storage_volume(self):
        from bexhoma.configurations.lifecycle import init_containers_without_storage
        with open(os.path.join(_REPO, 'k8s', 'deploymenttemplate-PostgreSQL.yml'), encoding='utf-8') as f:
            pod = [d for d in yaml.safe_load_all(f) if d['kind'] == 'Deployment'][0]['spec']['template']['spec']
        self.assertEqual(init_containers_without_storage(pod['initContainers']), [])

    def test_server_binds_to_ipv4(self):
        self.assertIn('-address=0.0.0.0', self.dbms['command'][-1])


class CedarDBScriptsTest(unittest.TestCase):
    def test_scripts_use_only_what_cedardb_has(self):
        scripts = glob.glob(os.path.join(_REPO, 'experiments', '**', 'CedarDB', '*.sql'), recursive=True)
        self.assertTrue(scripts)
        for script in scripts:
            with self.subTest(script=script), open(script, encoding='utf-8') as f:
                sql = re.sub(r'--.*', '', f.read())
                for word in _NOT_IN_CEDARDB:
                    self.assertNotIn(word, sql)

    def test_no_script_beyond_the_size_limit(self):
        """Community Edition: read-only above 64 GiB, so SF100 cannot load."""
        self.assertEqual(glob.glob(os.path.join(_REPO, 'experiments', 'tpch', 'CedarDB', '*SF100*')), [])

    def test_tpch_queries_of_the_cedardb_dialect_have_no_date_function(self):
        """CedarDB runs its variant or else the main text; no date('...') there."""
        with open(os.path.join(_REPO, 'experiments', 'tpch', 'queries-tpch.config'), encoding='utf-8') as f:
            queries = ast.literal_eval(f.read())['queries']
        for query in queries:
            with self.subTest(query=query['title']):
                self.assertNotIn("date('", query.get('DBMS', {}).get('CedarDB', query['query']))

    def test_cedardb_variants_differ_from_postgresql_only_in_the_date_form(self):
        with open(os.path.join(_REPO, 'experiments', 'tpch', 'queries-tpch.config'), encoding='utf-8') as f:
            queries = ast.literal_eval(f.read())['queries']
        variants = [q for q in queries if 'CedarDB' in q.get('DBMS', {})]
        self.assertEqual([queries.index(q) + 1 for q in variants], [8, 10, 15])
        for query in variants:
            with self.subTest(query=query['title']):
                postgresql = query['DBMS'].get('PostgreSQL', query['query'])
                self.assertEqual(query['DBMS']['CedarDB'], re.sub(r"date\('([^']+)'\)", r"date '\1'", postgresql))

    def test_tpch_uses_the_cedardb_dialect(self):
        from bexhoma.experiments.tpch import DBMS_DEFAULTS
        self.assertEqual(DBMS_DEFAULTS['CedarDB']['dialect'], 'CedarDB')


if __name__ == '__main__':
    unittest.main()
