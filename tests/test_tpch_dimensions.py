"""
Tests for ``-xdim`` in TPC-H (dev/plan-ddl-parameters.md, item 14).

- ``tpch.py`` selects the script folder and the volume per placement for
  ClickHouseCluster, refuses Citus with distributed dimensions, and the other
  DBMS ignore it.
- Every script of the ClickHouseCluster folder is also in its ``distributed``
  folder, and the ones that do not depend on the placement are copies.
- The scripts contain no braces except the declared DDL parameters.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import os
import runpy
import sys
import unittest
from unittest import mock

from bexhoma import ddl_parameters
from bexhoma.benchmarks.base import dimension_folder
from bexhoma.benchmarks.tpch import DIMENSION_DBMS

from .test_reset_scripts import _run_script

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXP = os.path.join(_REPO, 'experiments', 'tpch')
#: Files of <DBMS>/distributed that depend on the placement.
_OWN = {
    'ClickHouseCluster': {'initschema-tpch.sql', 'checkschema-tpch.sql', 'reset-tpch.sql'},
}


def _scripts(folder: str) -> set:
    path = os.path.join(_EXP, folder)
    return {name for name in os.listdir(path)
            if os.path.isfile(os.path.join(path, name)) and name != ddl_parameters.FILENAME}


class EntryScriptTest(unittest.TestCase):
    """``tpch.py`` up to ``process()``."""

    def _configs(self, *argv: str) -> dict:
        _, configurations = _run_script('tpch.py', *argv)
        return {config.docker: config for config in configurations}

    def test_replicated_default(self):
        configs = self._configs()
        for docker, config in configs.items():
            with self.subTest(docker):
                self.assertEqual((config.path_experiment_docker, config.storage_label),
                                 ('PostgreSQL' if docker == 'PgDuckDB' else docker, 'tpch-1'))
        self.assertIn('Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated)',
                      configs['Citus'].experiment.workload['info'])

    def test_distributed(self):
        # the later -dbms replaces the full list _run_script passes
        configs = self._configs('-dbms', 'PostgreSQL', 'ClickHouseCluster', '-xdim', 'distributed')
        self.assertEqual(set(configs), {'PostgreSQL', 'ClickHouseCluster'})
        self.assertEqual((configs['ClickHouseCluster'].path_experiment_docker, configs['ClickHouseCluster'].storage_label),
                         ('ClickHouseCluster/distributed', 'tpch-distributed-1'))
        # single-node DBMS ignore -xdim
        self.assertEqual((configs['PostgreSQL'].path_experiment_docker, configs['PostgreSQL'].storage_label),
                         ('PostgreSQL', 'tpch-1'))
        self.assertIn('Dimensions of ClickHouseCluster are spread over the nodes like orders and lineitem '
                      '(-xdim distributed)', configs['ClickHouseCluster'].experiment.workload['info'])

    def test_citus_distributed_refused(self):
        stderr = io.StringIO()
        with (
            mock.patch.object(sys, 'argv', ['tpch.py', 'run', '-dbms', 'Citus', '-xdim', 'distributed']),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(stderr),
            self.assertRaises(SystemExit) as exit_,
        ):
            runpy.run_path(os.path.join(_REPO, 'tpch.py'), run_name='__main__')
        self.assertEqual(exit_.exception.code, 2)
        self.assertIn('-xdim distributed is not supported for Citus', stderr.getvalue())
        self.assertFalse(os.path.exists(os.path.join(_EXP, 'Citus', 'distributed')))


class ScriptFolderTest(unittest.TestCase):
    """The ``distributed`` folder holds every script, and copies where the placement does not matter."""

    def test_dimension_folder(self):
        self.assertEqual(dimension_folder('ClickHouseCluster', 'replicated'), 'ClickHouseCluster')
        self.assertEqual(dimension_folder('ClickHouseCluster', 'distributed'), 'ClickHouseCluster/distributed')
        self.assertEqual(dimension_folder('PostgreSQL', 'distributed'), 'PostgreSQL')

    def test_same_scripts(self):
        self.assertEqual(set(_OWN), set(DIMENSION_DBMS))
        for docker in DIMENSION_DBMS:
            with self.subTest(docker):
                self.assertEqual(_scripts(docker + '/distributed'), _scripts(docker))
                self.assertLessEqual(_OWN[docker], _scripts(docker))

    def test_copies_are_identical(self):
        for docker in DIMENSION_DBMS:
            for name in sorted(_scripts(docker + '/distributed') - _OWN[docker]):
                with self.subTest(docker=docker, name=name), \
                        open(os.path.join(_EXP, docker, 'distributed', name), encoding='utf-8') as copy, \
                        open(os.path.join(_EXP, docker, name), encoding='utf-8') as original:
                    self.assertEqual(copy.read().replace(f'experiments/tpch/{docker}/distributed',
                                                         f'experiments/tpch/{docker}'),
                                     original.read())

    def test_no_braces(self):
        """No braces except the DDL parameters the folder declares (ddl-parameters.config)."""
        for docker in DIMENSION_DBMS:
            for folder in (docker, docker + '/distributed'):
                declared = ddl_parameters.load_declarations(_EXP, folder)
                for name in sorted(_scripts(folder)):
                    with self.subTest(folder=folder, name=name), \
                            open(os.path.join(_EXP, folder, name), encoding='utf-8') as f:
                        text = f.read()
                        for key in declared:
                            text = text.replace('{' + key + '}', '')
                        self.assertNotRegex(text, r'[{}]')


if __name__ == '__main__':
    unittest.main()
