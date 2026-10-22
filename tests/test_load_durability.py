"""
Tests for the import durability option ``-xld/--load-durability`` (dev/plan-oltp-storage-dbms.md, WP10).

The init script lists of the cluster config carry the placeholders
``durability.sql`` / ``restoredurability.sql``; bexhoma replaces them by the
level's scripts the DBMS folder has. Copies of a script in different
benchmarks must be identical (apart from the header line naming their
folder), unless the deviation is declared in :data:`ALLOWED_DEVIATIONS`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import contextlib
import glob
import io
import os
import types
import unittest

from bexhoma.cli_args import make_base_parser
from bexhoma.configurations.base import SutConfiguration
from bexhoma.load_durability import LEVELS, PLACEHOLDERS, expand_durability_placeholders

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXPERIMENTS = os.path.join(_REPO, 'experiments')

#: Copy that all other copies of a DBMS's durability scripts are compared with.
REFERENCE_BENCHMARK = {'PostgreSQL': 'tpch', 'MySQL': 'tpcds', 'Citus': 'tpch', 'MariaDB': 'tpch'}

#: (benchmark, DBMS, script) -> why this copy differs from the reference copy.
ALLOWED_DEVIATIONS = {
    ('tpch', 'MySQL', 'durability-relaxed.sql'): 'also autocommit 0 (the TPC-H loaders commit), as before -xld',
    ('tpcc', 'MySQL', 'durability-relaxed.sql'): 'flush 0 and 1G log buffer for the HammerDB build, as before -xld',
    ('ycsb', 'MySQL', 'durability-relaxed.sql'): 'flush 0 and 1G log buffer for the YCSB load, as before -xld',
}


def _body(path):
    """Script text without its first line (the header naming the folder)."""
    with open(path, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n').split('\n', 1)[1]


class ExpandTest(unittest.TestCase):
    """Placeholders become the level's scripts the folder has; other entries stay."""

    folder = os.path.join(_EXPERIMENTS, 'tpch', 'PostgreSQL')

    def test_in_place(self):
        scripts = ['initindexes-tpch.sql', 'restoredurability.sql', 'checkschema-tpch.sql']
        self.assertEqual(expand_durability_placeholders(scripts, 'relaxed', self.folder),
                         ['initindexes-tpch.sql', 'restoredurability-relaxed.sql', 'checkschema-tpch.sql'])
        # the list from the cluster config is not changed
        self.assertIn('restoredurability.sql', scripts)

    def test_list_without_placeholder(self):
        self.assertEqual(expand_durability_placeholders(['initschema-tpch.sql'], 'unsafe', self.folder),
                         ['initschema-tpch.sql'])

    def test_every_level_defined(self):
        for placeholder in PLACEHOLDERS.values():
            self.assertEqual(set(placeholder), set(LEVELS))


class ClusterConfigTest(unittest.TestCase):
    """Every pre-load list starts with durability.sql, every post-load list has
    restoredurability.sql right before its check script."""

    def test_placeholders_in_benchmark_lists(self):
        with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as f:
            volumes = ast.literal_eval(f.read())['volumes']
        for volume in ('tpch', 'tpcds', 'tpcc', 'ycsb', 'benchbase'):
            for key, scripts in volumes[volume]['initscripts'].items():
                if not scripts:
                    continue
                with self.subTest(volume=volume, key=key):
                    checks = [i for i, s in enumerate(scripts) if s.startswith('checkschema-')]
                    if checks:
                        self.assertEqual(scripts[checks[-1] - 1], 'restoredurability.sql')
                        self.assertNotIn('durability.sql', scripts)
                    else:
                        self.assertEqual(scripts[0], 'durability.sql')
                        self.assertNotIn('restoredurability.sql', scripts)


class ApplyTest(unittest.TestCase):
    """apply_load_durability() includes the level's scripts the folder has, once."""

    def apply(self, docker, level, path=None):
        cfg = types.SimpleNamespace(
            load_durability=level, load_durability_scripts=None, configuration=docker + '-1',
            path_experiment_docker=path or docker,
            initscript=['durability.sql', 'initschema-ycsb.sql'],
            indexscript=['restoredurability.sql', 'checkschema-ycsb.sql'], connection_parameter={},
            experiment=types.SimpleNamespace(cluster=types.SimpleNamespace(
                experiments_configfolder=os.path.join(_EXPERIMENTS, 'ycsb'))))
        with contextlib.redirect_stdout(io.StringIO()):
            SutConfiguration.apply_load_durability(cfg)
            SutConfiguration.apply_load_durability(cfg)
        return cfg

    def test_mysql_unsafe(self):
        cfg = self.apply('MySQL', 'unsafe')
        self.assertEqual(cfg.initscript, ['durability-relaxed.sql', 'durability-unsafe.sql', 'initschema-ycsb.sql'])
        self.assertEqual(cfg.indexscript, ['restoredurability-unsafe.sql', 'restoredurability-relaxed.sql',
                                           'checkschema-ycsb.sql'])
        self.assertEqual(cfg.connection_parameter['load_durability'], 'unsafe')
        self.assertEqual(cfg.load_durability_scripts, ['durability-relaxed.sql', 'durability-unsafe.sql',
                                                       'restoredurability-unsafe.sql', 'restoredurability-relaxed.sql'])

    def test_postgresql_unsafe_has_sync(self):
        cfg = self.apply('PGBouncer', 'unsafe', path='PostgreSQL')
        self.assertEqual(cfg.indexscript[:3], ['restoredurability-unsafe.sql', 'restoredurability-unsafe.sh',
                                               'restoredurability-relaxed.sql'])

    def test_citus_unsafe_only_relaxed_scripts(self):
        cfg = self.apply('Citus', 'unsafe')
        self.assertEqual(cfg.initscript, ['durability-relaxed.sql', 'initschema-ycsb.sql'])

    def test_mariadb_shell_scripts(self):
        cfg = self.apply('MariaDB', 'unsafe')
        self.assertEqual(cfg.initscript, ['durability-relaxed.sh', 'durability-unsafe.sh', 'initschema-ycsb.sql'])
        self.assertEqual(cfg.indexscript, ['restoredurability-unsafe.sh', 'restoredurability-relaxed.sh',
                                           'checkschema-ycsb.sql'])

    def test_durable(self):
        cfg = self.apply('PGBouncer', 'durable', path='PostgreSQL')
        self.assertEqual(cfg.initscript, ['durability-durable.sql', 'initschema-ycsb.sql'])
        self.assertEqual(cfg.indexscript, ['restoredurability-durable.sql', 'checkschema-ycsb.sql'])
        cfg = self.apply('MariaDB', 'durable')
        self.assertEqual(cfg.initscript, ['durability-durable.sh', 'initschema-ycsb.sql'])

    def test_dbms_without_scripts(self):
        for level in ('durable', 'relaxed', 'unsafe'):
            cfg = self.apply('TiDB', level)
            self.assertEqual((cfg.initscript, cfg.indexscript), (['initschema-ycsb.sql'], ['checkschema-ycsb.sql']))


class CliTest(unittest.TestCase):

    def test_default_and_choices(self):
        parser = make_base_parser()
        self.assertEqual(parser.parse_args([]).load_durability, 'relaxed')
        self.assertEqual(parser.parse_args(['-xld', 'unsafe']).load_durability, 'unsafe')
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(['-xld', 'off'])


class RepositoryScriptsTest(unittest.TestCase):
    """Shipped scripts: copies without undeclared deviations, no braces, init scripts relax nothing."""

    def scripts(self):
        # filled_* are by-products of runs (str.format() output, gitignored)
        return sorted(p for p in glob.glob(os.path.join(_EXPERIMENTS, '**', '*durability-*'), recursive=True)
                      if not os.path.basename(p).startswith('filled_'))

    def test_copies_do_not_deviate(self):
        used = set()
        for path in self.scripts():
            folder, script = os.path.split(path)
            dbms = os.path.basename(folder)
            benchmark = os.path.relpath(os.path.dirname(folder), _EXPERIMENTS).replace(os.sep, '/')
            key = (benchmark, dbms, script)
            with self.subTest(copy='/'.join(key)):
                reference = os.path.join(_EXPERIMENTS, REFERENCE_BENCHMARK[dbms], dbms, script)
                same = _body(path) == _body(reference)
                if key in ALLOWED_DEVIATIONS:
                    used.add(key)
                    self.assertFalse(same, 'declared deviation is identical: remove it from ALLOWED_DEVIATIONS')
                else:
                    self.assertTrue(same, f'differs from {REFERENCE_BENCHMARK[dbms]}/{dbms}/{script}; '
                                          'align it or declare it in ALLOWED_DEVIATIONS')
                with open(path, encoding='utf-8') as f:
                    self.assertTrue(f.readline().rstrip().endswith(f'| experiments/{benchmark}/{dbms}'))
        self.assertEqual(used, set(ALLOWED_DEVIATIONS))

    def test_no_curly_braces(self):
        """Scripts may be filled with str.format() (ddl_parameters, tenants)."""
        for path in self.scripts():
            with open(path, encoding='utf-8') as f:
                text = f.read()
            with self.subTest(path=os.path.relpath(path, _REPO)):
                self.assertNotRegex(text, r'[{}]')

    def test_init_scripts_no_longer_relax(self):
        """The relaxations moved out of the init and check scripts into the durability scripts."""
        for path in glob.glob(os.path.join(_EXPERIMENTS, '*', '*', '*schema*.sql')):
            if os.sep + 'PgDuckDB' + os.sep in path:
                continue  # unused folder (needs MotherDuck)
            with open(path, encoding='utf-8') as f:
                text = f.read()
            with self.subTest(path=os.path.relpath(path, _REPO)):
                self.assertNotIn('saved_settings', text)
                self.assertNotIn('synchronous_commit = off', text)


if __name__ == '__main__':
    unittest.main()
