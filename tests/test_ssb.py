"""
Tests for the Star Schema Benchmark (SSB, dev/plan-ssb.md).

- The query files parse, the spec files hold the constants of the
  specification, and every random query fills from its parameter tables with
  values that keep the query's shape (two cities of one nation, a brand range
  within one decade, a 7-day week).
- The script lists in ``k8s-cluster.config`` (``volumes.ssb``) cover every key
  ``SSB.configure_workload`` can select, and every script they name exists in
  the DBMS folders.
- ``ssb.py`` selects schema, post-load list, query file, volume label and
  loader ENV per variant, and rejects multi-tenancy.
- ``bexhoma summary`` rebuilds exactly the experiment classes that declare
  ``summary_from_type``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import contextlib
import copy
import datetime
import io
import itertools
import os
import random
import re
import runpy
import sys
import tempfile
import unittest
from unittest import mock

from dbmsbenchmarker import parameter

from bexhoma import experiments
from bexhoma.benchmarks.ssb import (DIMENSION_DBMS, QUERY_VARIANTS, SCHEMA_VARIANTS,
                                    resolve_dimension_folder, resolve_indexing_key,
                                    resolve_queryfile)
from bexhoma.experiments.base import ExperimentBase

from .test_resource_sweep import _AnyDockers, _SweepStubCluster

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXP = os.path.join(_REPO, 'experiments', 'ssb')
#: DBMS of the default -dbms set.
_DBMS_FOLDERS = ('PostgreSQL', 'MonetDB', 'ClickHouse')
#: Every script folder, including the -xdim distributed scripts.
_ALL_FOLDERS = _DBMS_FOLDERS + ('ClickHouseCluster', 'ClickHouseCluster/distributed', 'Citus', 'Citus/distributed',
                                'MySQL', 'MariaDB', 'CedarDB')
#: Placeholders the loading code replaces by the durability scripts the folder has.
_PLACEHOLDERS = {'durability.sql', 'restoredurability.sql'}


def _load_config(name: str) -> dict:
    with open(os.path.join(_EXP, name), encoding='utf-8') as f:
        return ast.literal_eval(f.read())


def _ssb_volume() -> dict:
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as f:
        return ast.literal_eval(f.read())['volumes']['ssb']


class QueryFilesTest(unittest.TestCase):
    """The six query files and their parameter tables."""

    def test_files_are_generated(self):
        """The committed query files are what make_queries.py writes."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(
                    sys, 'argv', ['make_queries.py', tmp_dir]):
                runpy.run_path(os.path.join(_EXP, 'make_queries.py'), run_name='__main__')
            for name in sorted(os.listdir(tmp_dir)):
                with self.subTest(name), open(os.path.join(tmp_dir, name), encoding='utf-8') as new, \
                        open(os.path.join(_EXP, name), encoding='utf-8') as committed:
                    self.assertEqual(new.read(), committed.read())

    def test_files_parse(self):
        for schema, query in itertools.product(SCHEMA_VARIANTS, QUERY_VARIANTS):
            with self.subTest(schema=schema, query=query):
                cfg = _load_config(resolve_queryfile(schema, query))
                self.assertEqual(len(cfg['queries']), 13)
                for order in cfg['stream_ordering'].values():
                    self.assertEqual(sorted(order), list(range(1, 14)))
        self.assertEqual(len(_load_config('queries-ssb-empty.config')['queries']), 1)
        normal = {q['query'].rsplit(' from ', 1)[1] for q in _load_config('queries-ssb-profiling.config')['queries']}
        flat = {q['query'].rsplit(' from ', 1)[1] for q in _load_config('queries-ssb-flat-profiling.config')['queries']}
        # each profiling file reads only the tables of its schema variant
        self.assertEqual(normal, {'customer', 'supplier', 'part', 'dates', 'lineorder'})
        self.assertEqual(flat, {'lineorder_flat'})

    def test_mysql_variants(self):
        """The flat queries have a MySQL variant without CAST(... AS INTEGER), otherwise equal."""
        for query_variant in QUERY_VARIANTS:
            for q in _load_config(resolve_queryfile('flat', query_variant))['queries']:
                sql = q['query']
                with self.subTest(query_variant=query_variant, title=q['title']):
                    if 'as integer' not in sql:
                        self.assertNotIn('DBMS', q)
                        continue
                    self.assertEqual(set(q['DBMS']), {'MySQL'})
                    self.assertNotIn('as integer', q['DBMS']['MySQL'])
                    self.assertEqual(q['DBMS']['MySQL'], sql.replace(
                        'cast(extract(year from lo_orderdate) as integer)', 'extract(year from lo_orderdate)'))
        for q in _load_config(resolve_queryfile('normal', 'spec'))['queries']:
            self.assertNotIn('DBMS', q)

    def test_variants_share_titles(self):
        titles = {(s, q): [x['title'] for x in _load_config(resolve_queryfile(s, q))['queries']]
                  for s, q in itertools.product(SCHEMA_VARIANTS, QUERY_VARIANTS)}
        self.assertEqual(len({tuple(t) for t in titles.values()}), 1)

    def test_spec_constants(self):
        for schema in SCHEMA_VARIANTS:
            queries = [q['query'] for q in _load_config(resolve_queryfile(schema, 'spec'))['queries']]
            for sql in queries:
                self.assertNotIn('{', sql)
                self.assertNotIn('parameter', sql)
            self.assertIn("lo_discount between 1 and 3", queries[0])
            self.assertIn("p_brand1 between 'MFGR#2221' and 'MFGR#2228'", queries[4])
            self.assertIn("p_brand1 = 'MFGR#2239'", queries[5])
            self.assertIn("c_city = 'UNITED KI1'", queries[8])
            self.assertIn("p_category = 'MFGR#14'", queries[12])
        flat = [q['query'] for q in _load_config(resolve_queryfile('flat', 'spec'))['queries']]
        # week 6 of 1994 in dbgen's numbering (day of year / 7 + 1)
        self.assertIn("between date '1994-02-04' and date '1994-02-10'", flat[2])
        for sql in flat:
            self.assertNotRegex(sql, r'\bdates\b')

    def test_random_queries_fill(self):
        random.seed(348)
        for schema in SCHEMA_VARIANTS:
            for i, q in enumerate(_load_config(resolve_queryfile(schema, 'random'))['queries'], 1):
                self.assertTrue(q.get('parameter'), (schema, i))
                for _ in range(200):
                    values = parameter.generateParameters(copy.deepcopy(q['parameter']), 1)[0]
                    sql = q['query'].format(**values)
                    with self.subTest(schema=schema, query=i):
                        self.assertNotRegex(sql, r'[{}]')
                        self._check_shape(sql)

    def _check_shape(self, sql: str) -> None:
        cities = re.findall(r"c_city = '([^']*)'", sql)
        if cities:
            self.assertEqual(len(set(cities)), 2, sql)
            # same nation: same 9-character prefix
            self.assertEqual(cities[0][:9], cities[1][:9], sql)
        brands = re.search(r"between 'MFGR#(\d\d)(\d\d)' and 'MFGR#(\d\d)(\d\d)'", sql)
        if brands:
            first, last = int(brands.group(2)), int(brands.group(4))
            self.assertEqual(brands.group(1), brands.group(3))
            self.assertEqual((last - first, first // 10), (7, last // 10), sql)
        week = re.search(r"lo_orderdate between date '([\d-]+)' and date '([\d-]+)'", sql)
        if week:
            start, end = (datetime.date.fromisoformat(d) for d in week.groups())
            self.assertEqual((end - start).days, 6)
            self.assertEqual(start.timetuple().tm_yday % 7, 0)


class ScriptListsTest(unittest.TestCase):
    """``volumes.ssb`` in the cluster config and the DBMS folders agree."""

    def setUp(self):
        self.lists = _ssb_volume()['initscripts']

    def test_every_selectable_key_exists(self):
        keys = {'Schema', 'Schema_flat'}
        for schema in SCHEMA_VARIANTS:
            for flags in itertools.product((False, True), repeat=3):
                keys.add(resolve_indexing_key(*flags, schema_variant=schema))
        self.assertEqual(keys, set(self.lists))

    def test_scripts_exist(self):
        for key, scripts in self.lists.items():
            for script in scripts:
                if script in _PLACEHOLDERS:
                    continue
                with self.subTest(key=key, script=script):
                    self.assertTrue(os.path.isfile(os.path.join(_EXP, 'PostgreSQL', script)))
                    self.assertTrue(os.path.isfile(os.path.join(_EXP, 'MonetDB', script)))
                    self.assertTrue(os.path.isfile(os.path.join(_EXP, 'Citus', script)))
                    self.assertTrue(os.path.isfile(os.path.join(_EXP, 'MySQL', script)))
                    self.assertTrue(os.path.isfile(os.path.join(_EXP, 'MariaDB', script)))
                    if not script.endswith('-flat.sql'):
                        self.assertTrue(os.path.isfile(os.path.join(_EXP, 'Citus', 'distributed', script)))
                    # ClickHouse has no secondary indexes, constraints or statistics scripts
                    if script.startswith(('initschema', 'checkschema')):
                        self.assertTrue(os.path.isfile(os.path.join(_EXP, 'ClickHouse', script)))
                        self.assertTrue(os.path.isfile(os.path.join(_EXP, 'ClickHouseCluster', script)))
                        # -xdim distributed changes the star schema only
                        if not script.endswith('-flat.sql'):
                            self.assertTrue(os.path.isfile(
                                os.path.join(_EXP, 'ClickHouseCluster', 'distributed', script)))

    def test_post_load_lists_end_with_check(self):
        for key, scripts in self.lists.items():
            if not key.startswith('Schema'):
                self.assertTrue(scripts[-1].startswith('checkschema-ssb'), key)
                self.assertEqual(scripts[-1].endswith('-flat.sql'), key.endswith('_flat'), key)

    def test_distributed_copies_are_identical(self):
        """The files of <DBMS>/distributed that do not depend on the dimensions are copies of the default ones."""
        own = {
            'ClickHouseCluster': {'initschema-ssb.sql', 'checkschema-ssb.sql', 'reset-ssb.sql'},
            'Citus': {'initschema-ssb.sql', 'initconstraints-ssb.sql'},
        }
        self.assertEqual(set(own), set(DIMENSION_DBMS))
        for docker in DIMENSION_DBMS:
            folder = os.path.join(_EXP, docker, 'distributed')
            for name in sorted(set(os.listdir(folder)) - own[docker]):
                with self.subTest(docker=docker, name=name), open(os.path.join(folder, name), encoding='utf-8') as copy, \
                        open(os.path.join(_EXP, docker, name), encoding='utf-8') as original:
                    self.assertEqual(copy.read().replace(f'experiments/ssb/{docker}/distributed', f'experiments/ssb/{docker}'),
                                     original.read())

    def test_no_braces(self):
        """No braces except the DDL parameters the folder declares (ddl-parameters.config)."""
        from bexhoma import ddl_parameters
        for folder in _ALL_FOLDERS:
            declared = ddl_parameters.load_declarations(_EXP, folder)
            for name in os.listdir(os.path.join(_EXP, folder)):
                if os.path.isdir(os.path.join(_EXP, folder, name)) or name == ddl_parameters.FILENAME:
                    continue
                with self.subTest(folder=folder, name=name):
                    with open(os.path.join(_EXP, folder, name), encoding='utf-8') as f:
                        text = f.read()
                    for key in declared:
                        text = text.replace('{' + key + '}', '')
                    self.assertNotRegex(text, r'[{}]')


class EntryScriptTest(unittest.TestCase):
    """``ssb.py`` up to ``process()`` against a stub cluster with the real ``volumes.ssb``."""

    def run_script(self, *argv: str):
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        cluster = _SweepStubCluster(resultfolder=tmp_dir.name)
        cluster.volumes['ssb'] = _ssb_volume()
        cluster.dockers = _AnyDockers(cluster.dockers)
        captured = []
        with (
            mock.patch('bexhoma.clusters.Kubernetes', return_value=cluster),
            mock.patch.object(ExperimentBase, 'process', lambda self: captured.append(self)),
            mock.patch.object(sys, 'argv', ['ssb.py', *argv]),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            try:
                runpy.run_path(os.path.join(_REPO, 'ssb.py'), run_name='__main__')
            except SystemExit as exit_:
                if exit_.code not in (None, 0):
                    return exit_.code
        self.assertEqual(len(captured), 1)
        return captured[0]

    def test_defaults(self):
        experiment = self.run_script('run', '-sf', '1')
        self.assertEqual(experiment.script, 'Schema')
        self.assertEqual(experiment.indexing, 'Checks')
        self.assertEqual(experiment.queryfile, 'queries-ssb.config')
        self.assertEqual({c.docker for c in experiment.configurations}, set(_DBMS_FOLDERS))
        for config in experiment.configurations:
            self.assertEqual(config.storage_label, 'ssb-1')
            self.assertEqual(config.loading_parameters['SSB_SCHEMA_VARIANT'], 'normal')
            self.assertEqual(config.jobtemplate_loading, f'jobtemplate-loading-ssb-{config.docker}.yml')
            self.assertTrue(os.path.isfile(os.path.join(_REPO, 'k8s', config.jobtemplate_loading)))

    def test_flat_random(self):
        experiment = self.run_script('run', '-sf', '10', '-xsv', 'flat', '-xqv', 'random', '-xii', '-xic', '-xis')
        self.assertEqual(experiment.script, 'Schema_flat')
        self.assertEqual(experiment.indexing, 'Index_and_Statistics_flat')
        self.assertEqual(experiment.queryfile, 'queries-ssb-flat-random.config')
        self.assertIn('Constraints (-xic) are ignored', experiment.workload['info'])
        for config in experiment.configurations:
            self.assertEqual(config.storage_label, 'ssb-flat-10')
            self.assertEqual(config.loading_parameters['SSB_SCHEMA_VARIANT'], 'flat')

    def test_normal_post_load_combination(self):
        experiment = self.run_script('load', '-xic', '-xis')
        self.assertEqual(experiment.indexing, 'Constraints_and_Statistics')

    def test_profiling_file_per_variant(self):
        self.assertEqual(self.run_script('profiling').queryfile, 'queries-ssb-profiling.config')
        self.assertEqual(self.run_script('profiling', '-xsv', 'flat').queryfile, 'queries-ssb-flat-profiling.config')

    def test_multi_tenancy_rejected(self):
        self.assertEqual(self.run_script('run', '-mtn', '2', '-mtb', 'schema'), 2)

    def _cluster_config(self, experiment):
        configs = [c for c in experiment.configurations if c.docker == 'ClickHouseCluster']
        self.assertEqual(len(configs), 1)
        return configs[0]

    def test_clickhouse_cluster_replicated_default(self):
        experiment = self.run_script('run', '-dbms', 'PostgreSQL', 'ClickHouseCluster', '-nw', '2')
        config = self._cluster_config(experiment)
        self.assertEqual(config.path_experiment_docker, 'ClickHouseCluster')
        self.assertEqual(config.storage_label, 'ssb-1')
        self.assertEqual(config.num_worker, 2)
        self.assertEqual(config.script_target, 'workers')
        self.assertEqual(config.jobtemplate_loading, 'jobtemplate-loading-ssb-ClickHouse.yml')
        self.assertIn('Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated)',
                      experiment.workload['info'])
        resets = {e.get('resetscript') and tuple(e['resetscript'])
                  for r in config.experiment_dict['benchmarker'] for e in r}
        self.assertEqual(resets, {('reset-ssb.sql', 'reset-flush.sh')})

    def test_clickhouse_cluster_distributed(self):
        experiment = self.run_script('run', '-dbms', 'PostgreSQL', 'ClickHouseCluster', '-xdim', 'distributed')
        config = self._cluster_config(experiment)
        self.assertEqual(config.path_experiment_docker, 'ClickHouseCluster/distributed')
        self.assertEqual(config.storage_label, 'ssb-distributed-1')
        self.assertIn('spread over the nodes like lineorder (-xdim distributed)', experiment.workload['info'])
        # single-node DBMS ignore -xdim
        postgresql = [c for c in experiment.configurations if c.docker == 'PostgreSQL'][0]
        self.assertEqual((postgresql.path_experiment_docker, postgresql.storage_label), ('PostgreSQL', 'ssb-1'))

    def test_clickhouse_cluster_flat_ignores_dimensions(self):
        experiment = self.run_script('run', '-dbms', 'ClickHouseCluster', '-xsv', 'flat', '-xdim', 'distributed')
        config = self._cluster_config(experiment)
        self.assertEqual((config.path_experiment_docker, config.storage_label), ('ClickHouseCluster', 'ssb-flat-1'))
        self.assertNotIn('-xdim', experiment.workload['info'])
        resets = {e.get('resetscript') and tuple(e['resetscript'])
                  for r in config.experiment_dict['benchmarker'] for e in r}
        self.assertEqual(resets, {('reset-ssb-flat.sql', 'reset-flush.sh')})
        self.assertTrue(os.path.isfile(os.path.join(_EXP, 'ClickHouseCluster', 'reset-ssb-flat.sql')))

    def test_pgduckdb_reuses_postgresql(self):
        experiment = self.run_script('run', '-dbms', 'PgDuckDB', '-xdfe')
        config = experiment.configurations[0]
        self.assertEqual(config.docker, 'PgDuckDB')
        self.assertEqual(config.path_experiment_docker, 'PostgreSQL')
        self.assertEqual(config.jobtemplate_loading, 'jobtemplate-loading-ssb-PostgreSQL.yml')
        self.assertEqual(config.sut_parameters['DUCKDB_FORCE_EXECUTION'], 'true')
        self.assertIn('forced through the DuckDB execution engine', experiment.workload['info'])
        self.assertEqual(self.run_script('run', '-dbms', 'PgDuckDB').configurations[0]
                         .sut_parameters['DUCKDB_FORCE_EXECUTION'], 'false')

    def test_citus(self):
        experiment = self.run_script('run', '-dbms', 'Citus', '-nw', '3')
        config = experiment.configurations[0]
        self.assertEqual((config.docker, config.num_worker, config.path_experiment_docker, config.storage_label),
                         ('Citus', 3, 'Citus', 'ssb-1'))
        self.assertEqual(config.jobtemplate_loading, 'jobtemplate-loading-ssb-PostgreSQL.yml')
        self.assertIn('Dimensions of Citus are a full copy on every node', experiment.workload['info'])
        config = self.run_script('run', '-dbms', 'Citus', '-xdim', 'distributed').configurations[0]
        self.assertEqual((config.path_experiment_docker, config.storage_label), ('Citus/distributed', 'ssb-distributed-1'))
        config = self.run_script('run', '-dbms', 'Citus', '-xsv', 'flat', '-xdim', 'distributed').configurations[0]
        self.assertEqual((config.path_experiment_docker, config.storage_label), ('Citus', 'ssb-flat-1'))
        resets = {e.get('resetscript') and tuple(e['resetscript'])
                  for r in config.experiment_dict['benchmarker'] for e in r}
        self.assertEqual(resets, {('reset-ssb-flat.sql',)})

    def test_mysql_mariadb(self):
        experiment = self.run_script('run', '-dbms', 'MySQL', 'MariaDB', '-xsv', 'flat')
        configs = {c.docker: c for c in experiment.configurations}
        self.assertEqual(set(configs), {'MySQL', 'MariaDB'})
        for docker, config in configs.items():
            self.assertEqual(config.jobtemplate_loading, f'jobtemplate-loading-ssb-{docker}.yml')
            self.assertTrue(os.path.isfile(os.path.join(_REPO, 'k8s', config.jobtemplate_loading)))
            resets = {e.get('resetscript') and tuple(e['resetscript'])
                      for r in config.experiment_dict['benchmarker'] for e in r}
            self.assertEqual(resets, {('reset-ssb-flat.sql', 'reset-flush.sh')})
        self.assertEqual(configs['MariaDB'].sut_parameters['MARIADB_DATABASE'], 'ssb')

    def test_mysql_loaders_share_the_script(self):
        loaders = os.path.join(_REPO, 'images', 'ssb')
        with open(os.path.join(loaders, 'loader_mysql', 'loader.sh'), encoding='utf-8') as mysql, \
                open(os.path.join(loaders, 'loader_mariadb', 'loader.sh'), encoding='utf-8') as mariadb:
            self.assertEqual(mysql.read(), mariadb.read())

    def test_dimension_folder(self):
        for docker in DIMENSION_DBMS:
            self.assertEqual(resolve_dimension_folder(docker, 'normal', 'replicated'), docker)
            self.assertEqual(resolve_dimension_folder(docker, 'normal', 'distributed'), docker + '/distributed')
            self.assertEqual(resolve_dimension_folder(docker, 'flat', 'distributed'), docker)
        self.assertEqual(resolve_dimension_folder('PostgreSQL', 'normal', 'distributed'), 'PostgreSQL')
        for folder in ('ClickHouseCluster', 'ClickHouseCluster/distributed'):
            for name in ('reset-ssb.sql', 'reset-flush.sh'):
                self.assertTrue(os.path.isfile(os.path.join(_EXP, folder, name)), (folder, name))


class SummaryDispatchTest(unittest.TestCase):
    """``bexhoma summary`` maps a workload type to its class only where the class allows it."""

    def test_classes_with_summary_from_type(self):
        classes = {name for name in experiments.__all__
                   if isinstance(getattr(experiments, name), type) and name.islower()
                   and getattr(experiments, name).summary_from_type}
        self.assertEqual(classes, {'tpch', 'tpcds', 'ssb', 'ycsb', 'tpcc', 'benchbase'})

    def test_workload_type_names_the_alias(self):
        self.assertIs(experiments.ssb, experiments.SsbExperiment)
        for alias in ('tpch', 'tpcds', 'ssb', 'ycsb', 'tpcc', 'benchbase'):
            self.assertTrue(issubclass(getattr(experiments, alias), ExperimentBase), alias)


if __name__ == '__main__':
    unittest.main()
