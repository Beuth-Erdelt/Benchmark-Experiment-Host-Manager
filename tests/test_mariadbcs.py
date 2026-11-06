"""
Tests for MariaDB ColumnStore (issue #827).

The template runs the official MariaDB image and installs the plugin at every
start, so the image tag, the plugin version and the start script must stay in
step. The tables are those of MariaDB without keys, in the ColumnStore engine.

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
_SCHEMAS = (('tpch', 'initschema-tpch.sql'), ('tpcds', 'initschema-tpcds.sql'),
            ('ssb', 'initschema-ssb.sql'), ('ssb', 'initschema-ssb-flat.sql'))


def _config():
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as f:
        return ast.literal_eval(f.read())


def _deployment():
    with open(os.path.join(_REPO, 'k8s', 'deploymenttemplate-MariaDBCS.yml'), encoding='utf-8') as f:
        return [d for d in yaml.safe_load_all(f) if d['kind'] == 'Deployment'][0]


def _columns(benchmark, dbms, script):
    """Column definitions per table, without keys and the storage engine."""
    with open(os.path.join(_REPO, 'experiments', benchmark, dbms, script), encoding='utf-8') as f:
        sql = re.sub(r'--.*', '', f.read())
    tables = {}
    for name, body in re.findall(r'CREATE TABLE (\S+)\s*\((.*?)\n\)', sql, re.S):
        lines = [' '.join(line.strip().rstrip(',').split()) for line in body.splitlines()]
        tables[name] = [line for line in lines if line and not line.startswith('PRIMARY KEY')]
    return tables


class MariaDBCSTemplateTest(unittest.TestCase):
    def setUp(self):
        self.docker = _config()['dockers']['MariaDBCS']
        self.pod = _deployment()['spec']['template']['spec']
        self.dbms = [c for c in self.pod['containers'] if c['name'] == 'dbms'][0]
        self.script = self.dbms['command'][2]

    def test_stock_image_of_the_configured_server_version(self):
        server = self.docker['template']['version'].split('-')[0]
        self.assertEqual(self.dbms['image'], 'mariadb:' + server)

    def test_same_server_as_mariadb(self):
        with open(os.path.join(_REPO, 'k8s', 'deploymenttemplate-MariaDB.yml'), encoding='utf-8') as f:
            mariadb = [d for d in yaml.safe_load_all(f) if d['kind'] == 'Deployment'][0]
        self.assertEqual(self.dbms['image'], mariadb['spec']['template']['spec']['containers'][0]['image'])

    def test_args_reach_the_server(self):
        # bash -c script NAME args: "--" is $0, so "$@" holds the args of the container
        self.assertEqual(self.dbms['command'][3:], ['--'])
        self.assertIn('docker-entrypoint.sh mariadbd "$@"', self.script)

    def test_catalog_and_data_share_the_volume(self):
        mounts = {m['mountPath']: m for m in self.dbms['volumeMounts']}
        for path, sub_path in (('/var/lib/columnstore', 'columnstore'), ('/var/lib/mysql', 'mysql')):
            self.assertEqual(mounts[path]['name'], 'benchmark-storage-volume')
            self.assertEqual(mounts[path]['subPath'], sub_path)

    def test_probes_need_the_daemons(self):
        for probe in ('startupProbe', 'readinessProbe'):
            self.assertIn('calpontsys.systable', self.dbms[probe]['exec']['command'][-1])

    def test_memory_follows_the_pod_limit_and_all_cores_stay(self):
        self.assertIn('mcsSetConfig SystemConfig CGroup ../../..$MCS_CGROUP', self.script)
        # the cgroup of the container has an empty cpuset.cpus, which means one core to ColumnStore
        self.assertNotIn('mcsSetConfig SystemConfig CGroup .\n', self.script)
        self.assertIn('$(nproc)', self.script)

    def test_daemons_start_before_the_server_and_stop_after_it(self):
        self.assertLess(self.script.index('DDLProc\n'), self.script.index('docker-entrypoint.sh'))
        self.assertLess(self.script.index('kill -TERM $SERVER'), self.script.index('mcs-savebrm.py'))
        self.assertLess(self.script.index('mcs-loadbrm.py'), self.script.index('workernode DBRM_Worker1'))

    def test_primproc_is_restarted_but_not_at_shutdown(self):
        self.assertIn('if ! pgrep -x PrimProc', self.script)
        self.assertLess(self.script.index('kill $WATCHDOG'), self.script.index('pkill PrimProc'))

    def test_functions_are_created_with_the_root_login(self):
        self.assertLess(self.script.index('rm -f /etc/mysql/debian.cnf'), self.script.index('/usr/sbin/install_mcs_mysql.sh'))


class MariaDBCSScriptsTest(unittest.TestCase):
    def test_tables_are_those_of_mariadb(self):
        for benchmark, script in _SCHEMAS:
            with self.subTest(script=script):
                columns = _columns(benchmark, 'MariaDBCS', script)
                self.assertTrue(columns)
                self.assertEqual(columns, _columns(benchmark, 'MariaDB', script))

    def test_every_table_is_columnar(self):
        for benchmark, script in _SCHEMAS:
            with self.subTest(script=script):
                with open(os.path.join(_REPO, 'experiments', benchmark, 'MariaDBCS', script), encoding='utf-8') as f:
                    sql = re.sub(r'--.*', '', f.read())
                self.assertEqual(len(re.findall(r'CREATE TABLE', sql)), len(re.findall(r'ENGINE = ColumnStore;', sql)))

    def test_no_keys_or_innodb(self):
        scripts = glob.glob(os.path.join(_REPO, 'experiments', '*', 'MariaDBCS', '*.sql'))
        self.assertTrue(scripts)
        for script in scripts:
            if os.path.basename(script).startswith('initdata'):
                continue
            with self.subTest(script=script), open(script, encoding='utf-8') as f:
                sql = re.sub(r'--.*', '', f.read())
                for word in ('PRIMARY KEY', 'FOREIGN KEY', 'CREATE INDEX', 'Innodb_', 'innodb_', 'TABLE_CONSTRAINTS'):
                    self.assertNotIn(word, sql)

    def test_scripts_of_every_list_exist(self):
        volumes = _config()['volumes']
        for benchmark, schemas in (('tpch', ['Schema']), ('tpcds', ['Schema']), ('ssb', ['Schema', 'Schema_flat'])):
            scripts = volumes[benchmark]['initscripts']
            names = ['Checks', 'Index', 'Index_and_Constraints_and_Statistics'] + schemas
            for name in names:
                for script in scripts[name]:
                    if script not in ('durability.sql', 'restoredurability.sql'):
                        with self.subTest(benchmark=benchmark, script=script):
                            self.assertTrue(os.path.isfile(os.path.join(_REPO, 'experiments', benchmark, 'MariaDBCS', script)))

    def test_query_variants_come_on_top_of_the_mysql_dialect(self):
        from bexhoma.experiments.tpch import DBMS_DEFAULTS
        self.assertEqual(DBMS_DEFAULTS['MariaDBCS']['dialect'], 'MySQL')
        with open(os.path.join(_REPO, 'experiments', 'tpch', 'queries-tpch.config'), encoding='utf-8') as f:
            queries = ast.literal_eval(f.read())['queries']
        self.assertEqual(len([q for q in queries if 'MariaDBCS' in q.get('DBMS', {})]), 4)

    def test_loads_with_one_pod(self):
        """Concurrent LOAD DATA into a table fails and the loader goes on, so rows would be missing."""
        for script in ('tpch.py', 'tpcds.py', 'ssb.py'):
            with self.subTest(script=script), open(os.path.join(_REPO, script), encoding='utf-8') as f:
                block = f.read().split('if ("MariaDBCS" in args.dbms):')[1].split('if ("')[0]
            self.assertIn('config.set_loading(parallel=1, num_pods=1)', block)
            self.assertIn('PODS_TOTAL = "1"', block)
            self.assertIn('PODS_PARALLEL = "1"', block)

    def test_rollup_queries_of_tpcds_are_emulated(self):
        """WITH ROLLUP kills PrimProc on a table and gives wrong results on a derived table."""
        with open(os.path.join(_REPO, 'experiments', 'tpcds', 'queries-tpcds.config'), encoding='utf-8') as f:
            queries = ast.literal_eval(f.read())['queries']
        variants = {q['title']: q['DBMS'] for q in queries if 'MariaDBCS' in q.get('DBMS', {})}
        rollups = {f'TPC-DS Q{n}' for n in (18, 22, 27, 36, 67, 70, 86)}
        refused = {f'TPC-DS Q{n}' for n in (6, 8, 9, 10, 28, 35, 38, 44, 45, 61, 77, 87, 88, 90)} | {'TPC-DS Q14a+b', 'TPC-DS Q23a+b'}
        self.assertEqual(set(variants), rollups | refused | {f'TPC-DS Q{n}' for n in (47, 57, 72, 93)})
        for title in refused:
            with self.subTest(query=title):
                self.assertEqual(list(variants[title])[-1], 'MariaDBCS')
                text = variants[title]['MariaDBCS']
                text = ' '.join(text if isinstance(text, list) else [text]).lower()
                for word in ('intersect', ' except ', 'with rollup '):
                    self.assertNotIn(word, text)
        for title in rollups:
            dbms = variants[title]
            with self.subTest(query=title):
                # a mariadbcs connection also matches the key MariaDB, the last match wins
                self.assertEqual(list(dbms)[-1], 'MariaDBCS')
                text = dbms['MariaDBCS'].lower()
                self.assertNotRegex(text, r'with\s+rollup\b')
                self.assertIn('union all', text)

    def test_q33_q56_are_the_reference_query_with_nulls_first_where_needed(self):
        with open(os.path.join(_REPO, 'experiments', 'tpcds', 'queries-tpcds.config'), encoding='utf-8') as f:
            queries = {q['title']: q for q in ast.literal_eval(f.read())['queries']}
        for title in ('TPC-DS Q33', 'TPC-DS Q56'):
            with self.subTest(query=title):
                query = queries[title]
                self.assertNotIn('is not null', query['query'].lower())
                self.assertEqual(sorted(query['DBMS']), ['Clickhouse', 'PostgreSQL'])
                for text in query['DBMS'].values():
                    self.assertIn('nulls first', text.lower())

    def test_variants_avoid_what_gives_wrong_results(self):
        with open(os.path.join(_REPO, 'experiments', 'tpcds', 'queries-tpcds.config'), encoding='utf-8') as f:
            queries = {q['title']: q for q in ast.literal_eval(f.read())['queries']}
        for n in (47, 57):
            text = queries[f'TPC-DS Q{n}']['DBMS']['MariaDBCS'].lower()
            self.assertNotIn('v1_lag', text)
            self.assertIn('having', text)
        self.assertNotIn('off.k', queries['TPC-DS Q72']['DBMS']['MariaDBCS'])
        self.assertNotIn('left outer join', queries['TPC-DS Q93']['DBMS']['MariaDBCS'].lower())
        for title in ('TPC-DS Q47', 'TPC-DS Q57', 'TPC-DS Q72', 'TPC-DS Q93'):
            self.assertEqual(list(queries[title]['DBMS'])[-1], 'MariaDBCS')

    def test_not_part_of_the_default_runs(self):
        for script in ('tpch.py', 'tpcds.py', 'ssb.py'):
            with self.subTest(script=script), open(os.path.join(_REPO, script), encoding='utf-8') as f:
                self.assertIn('if ("MariaDBCS" in args.dbms):', f.read())


if __name__ == '__main__':
    unittest.main()
