"""
Tests for the reset scripts of ``-ar`` (dev/plan-reset-scripts.md).

The completeness test runs every entry script with all its ``-dbms`` choices
against the stub cluster of :mod:`tests.test_resource_sweep` and checks that
every DBMS in scope gets the expected reset list and that every file of it is
in the configuration's experiment folder. A DBMS added to a CLI fails here
until it gets a reset (or is listed in ``NO_RESET``).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import glob
import io
import os
import re
import runpy
import sys
import tempfile
import types
import unittest
from unittest import mock

from bexhoma.benchmarks.tpcds import TPCDS
from bexhoma.benchmarks.tpch import TPCH
from bexhoma.configurations.loading import LoadingCoordinator
from bexhoma.experiments.base import ExperimentBase

from .test_load_mode_workload import _FakeExperiment
from .test_resource_sweep import _AnyDockers, _AnyVolumes, _dbms_choices, _SweepStubCluster

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: DBMS without reset scripts (plan decision D1).
NO_RESET = {'CedarDB', 'DatabaseService'}

_FLUSH = 'reset-flush.sh'
_COUNTERS = 'reset-counters.sh'

#: Entry script -> DBMS (``config.docker``) -> expected reset list.
EXPECTED = {
    'ycsb.py': {
        'PostgreSQL': ['reset-ycsb.sql'],
        'PGBouncer': ['reset-ycsb.sql'],
        'MySQL': ['reset-ycsb.sql', _FLUSH],
        'MariaDB': ['reset-ycsb.sql', _FLUSH],
        'YugabyteDB': ['reset-ycsb.sql', _COUNTERS],
        'CockroachDB': ['reset-ycsb.sql'],
        'TiDB': ['reset-ycsb.sql'],
        'Citus': ['reset-ycsb.sql'],
        'Dragonfly': ['save-snapshot.sh'],
        'Redis': ['save-snapshot.sh'],
    },
    'benchbase.py': {
        'PostgreSQL': ['reset-benchbase.sql'],
        'PGBouncer': ['reset-benchbase.sql'],
        'MySQL': ['reset-benchbase.sql', _FLUSH],
        'MariaDB': ['reset-benchbase.sql', _FLUSH],
        'YugabyteDB': ['reset-benchbase.sql', _COUNTERS],
        'CockroachDB': ['reset-benchbase.sql'],
        'TiDB': ['reset-benchbase.sql'],
        'Citus': ['reset-benchbase.sql'],
    },
    'hammerdb.py': {
        'PostgreSQL': ['reset-tpcc.sql'],
        'MySQL': ['reset-tpcc.sql', _FLUSH],
        'MariaDB': ['reset-tpcc.sql', _FLUSH],
        'Citus': ['reset-tpcc.sql'],
    },
    'tpch.py': {
        'PostgreSQL': ['reset-tpch.sql'],
        'PgDuckDB': ['reset-tpch.sql'],
        'MonetDB': ['reset-tpch.sql'],
        'MySQL': ['reset-tpch.sql', _FLUSH],
        'MariaDB': ['reset-tpch.sql', _FLUSH],
        'Citus': ['reset-tpch.sql'],
    },
    'tpcds.py': {
        'PostgreSQL': ['reset-tpcds.sql'],
        'MonetDB': ['reset-tpcds.sql'],
        'MySQL': ['reset-tpcds.sql', _FLUSH],
        'MariaDB': ['reset-tpcds.sql', _FLUSH],
    },
}

#: Benchbase benchmarks other than tpcc have folders (and resets) only for these DBMS (R4).
BENCHBASE_NON_TPCC = {'PostgreSQL', 'PGBouncer'}


def _run_script(script: str, *argv: str) -> tuple:
    """Run an entry script with all its ``-dbms`` choices up to ``process()``.

    :return: ``(experiment configfolder, configurations)``.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        cluster = _SweepStubCluster(resultfolder=tmp_dir)
        cluster.volumes = _AnyVolumes(cluster.volumes)
        cluster.dockers = _AnyDockers(cluster.dockers)
        captured = []
        command = [script, 'run', '-dbms', *_dbms_choices(script), *argv]
        with (
            mock.patch('bexhoma.clusters.Kubernetes', return_value=cluster),
            mock.patch.object(ExperimentBase, 'process', lambda self: captured.append(self)),
            mock.patch.object(sys, 'argv', command),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                runpy.run_path(os.path.join(_REPO, script), run_name='__main__')
            except SystemExit:
                pass
    assert len(captured) == 1, f'{script} did not reach process()'
    return cluster.experiments_configfolder, captured[0].configurations


def _resets(config) -> dict:
    """Reset list per benchmarker entry name, over all client rounds."""
    resets = {}
    for client_round in config.experiment_dict.get('benchmarker') or []:
        for entry in client_round:
            resets.setdefault(entry['name'], entry.get('resetscript') or [])
    return resets


class ResetCompletenessTest(unittest.TestCase):
    """Every DBMS of every benchmark CLI has a reset list whose files exist (M9)."""

    def assert_complete(self, script: str, *argv: str, benchmark: str = None) -> None:
        folder, configurations = _run_script(script, *argv)
        expected = EXPECTED[script]
        self.assertEqual(set(_dbms_choices(script)) - NO_RESET, set(expected),
                         f'{script}: -dbms choices without an entry in EXPECTED')
        seen = set()
        for config in configurations:
            with self.subTest(script=script, benchmark=benchmark, configuration=config.configuration):
                resets = _resets(config)
                lists = [r for r in resets.values() if r]
                if config.docker in NO_RESET or (
                        benchmark not in (None, 'tpcc') and config.docker not in BENCHBASE_NON_TPCC):
                    self.assertEqual(lists, [], config.docker)
                    continue
                seen.add(config.docker)
                self.assertEqual(lists, [expected[config.docker]], config.docker)
                for name in expected[config.docker]:
                    path = os.path.join(_REPO, folder, config.path_experiment_docker, name)
                    self.assertTrue(os.path.isfile(path), path)
        wanted = set(expected) if benchmark in (None, 'tpcc') else BENCHBASE_NON_TPCC
        self.assertEqual(seen, wanted, script)

    def test_ycsb(self):
        self.assert_complete('ycsb.py')

    def test_hammerdb(self):
        self.assert_complete('hammerdb.py')

    def test_tpch(self):
        self.assert_complete('tpch.py')

    def test_tpcds(self):
        self.assert_complete('tpcds.py')

    def test_benchbase(self):
        for benchmark in ('tpcc', 'twitter', 'ycsb', 'chbenchmark'):
            self.assert_complete('benchbase.py', '-xbt', benchmark, benchmark=benchmark)

    def test_tpch_refresh_stream_gets_no_second_reset(self):
        """The reset runs once per round, before the query stream, not again before the refresh stream."""
        _, configurations = _run_script('tpch.py', '-xrs', '1')
        for config in configurations:
            resets = _resets(config)
            self.assertIn('tpch_refresh', resets)
            self.assertEqual(resets['tpch_refresh'], [], config.configuration)


class ResetScriptContentTest(unittest.TestCase):
    """Reset scripts follow the contract and survive ``str.format()``."""

    def _scripts(self):
        paths = []
        for pattern in ('reset-*.sql', 'reset-*.sh', 'save-snapshot.sh'):
            paths += glob.glob(os.path.join(_REPO, 'experiments', '**', pattern), recursive=True)
        return sorted(p for p in paths if 'SingleStore' not in p)

    def test_no_braces(self):
        for path in self._scripts():
            with self.subTest(path), open(path, encoding='utf-8') as f:
                text = f.read()
                # bexhoma may fill scripts with str.format()
                self.assertNotRegex(text, r'[{}]', path)
                text.format()

    def test_steps_in_order(self):
        """Statistics -> persist -> counters; a missing step is an n/a line, not left out."""
        for path in self._scripts():
            if os.path.basename(path) in (_FLUSH, _COUNTERS):
                continue  # later steps only, after the statistics script
            with self.subTest(path), open(path, encoding='utf-8') as f:
                text = f.read()
                if 'reset-flush.sh' in text:
                    continue  # MySQL/MariaDB .sql: step 1 only
                positions = [text.find(f'step {n} (') for n in (1, 2, 3)]
                self.assertTrue(all(p >= 0 for p in positions), path)
                self.assertEqual(positions, sorted(positions), path)

    def test_postgresql_checkpoint_after_vacuum(self):
        for path in glob.glob(os.path.join(_REPO, 'experiments', '**', 'PostgreSQL', 'reset-*.sql'),
                              recursive=True):
            with self.subTest(path), open(path, encoding='utf-8') as f:
                text = f.read()
                vacuum, checkpoint, counters = (
                    re.search(pattern, text, re.M).start()
                    for pattern in (r'^VACUUM', r'^CHECKPOINT;', r'^SELECT pg_stat_reset\(\);'))
                self.assertLess(vacuum, checkpoint, path)
                self.assertLess(checkpoint, counters, path)

    def test_citus_reaches_the_workers(self):
        for path in glob.glob(os.path.join(_REPO, 'experiments', '**', 'Citus', 'reset-*.sql'), recursive=True):
            with self.subTest(path), open(path, encoding='utf-8') as f:
                text = f.read()
                self.assertIn('run_command_on_workers($cmd$CHECKPOINT$cmd$)', text, path)
                self.assertIn('run_command_on_workers($cmd$SELECT pg_stat_reset()$cmd$)', text, path)

    def test_shell_scripts_are_identical(self):
        """The duplicated reset-flush.sh and reset-counters.sh files differ only in their folder line."""
        for dbms, name in (('MySQL', _FLUSH), ('MariaDB', _FLUSH), ('YugabyteDB', _COUNTERS)):
            texts = []
            for path in glob.glob(os.path.join(_REPO, 'experiments', '**', dbms, name), recursive=True):
                with open(path, encoding='utf-8') as f:
                    texts.append(re.sub(r'^# Benchmark-Experiment-Host-Manager \| .*$', '', f.read(), count=1, flags=re.M))
            self.assertGreater(len(texts), 1, dbms)
            self.assertEqual(len(set(texts)), 1, dbms)

    def test_yugabytedb_counters_on_every_tserver(self):
        """The counters are reset per tserver, not once through the service."""
        for path in glob.glob(os.path.join(_REPO, 'experiments', '**', 'YugabyteDB', 'reset-*'), recursive=True):
            with self.subTest(path), open(path, encoding='utf-8') as f:
                text = f.read()
                if path.endswith(_COUNTERS):
                    self.assertIn('yb-tserver-$i.yb-tservers', text)
                else:
                    self.assertNotRegex(text, r'(?m)^SELECT pg_stat_reset', path)


class ExecResetScriptTest(unittest.TestCase):
    """A reset script missing in the experiment folder is skipped with a message (M1.1)."""

    def setUp(self):
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        os.makedirs(os.path.join(tmp_dir.name, 'PostgreSQL'))
        with open(os.path.join(tmp_dir.name, 'PostgreSQL', 'reset-ycsb.sql'), 'w') as f:
            f.write('CHECKPOINT;\n')
        self.cfg = types.SimpleNamespace(
            dockertemplate={'loadData': 'psql < {scriptname}'}, configuration='PostgreSQL-1',
            path_experiment_docker='PostgreSQL',
            experiment=types.SimpleNamespace(cluster=types.SimpleNamespace(experiments_configfolder=tmp_dir.name)))

    def test_all_missing(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(LoadingCoordinator(self.cfg).exec_reset_script('reset_1_1_1', ['nope.sql']), 0)
        self.assertIn("reset scripts ['nope.sql'] not found", out.getvalue())

    def test_missing_one_is_dropped(self):
        class Stop(Exception):
            pass
        with (
            mock.patch.object(LoadingCoordinator, 'split_worker_scripts', side_effect=Stop) as split,
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaises(Stop),
        ):
            LoadingCoordinator(self.cfg).exec_reset_script('reset_1_1_1', ['reset-ycsb.sql', 'reset-flush.sh'])
        split.assert_called_once_with(['reset-ycsb.sql'])


class WarnMissingResetScriptsTest(unittest.TestCase):
    """``-ar`` on a configuration without (existing) reset scripts warns once at start (M1.2)."""

    def test_warnings(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.makedirs(os.path.join(tmp_dir, 'PostgreSQL'))
            open(os.path.join(tmp_dir, 'PostgreSQL', 'reset-ycsb.sql'), 'w').close()

            def config(name, docker, scripts, legacy=None):
                return types.SimpleNamespace(
                    configuration=name, path_experiment_docker=docker, resetscript=legacy or [],
                    experiment_dict={'benchmarker': [[{'name': 'b', 'resetscript': scripts}],
                                                     [{'name': 'b', 'resetscript': scripts}]]})
            experiment = types.SimpleNamespace(
                resetscript_active=True, cluster=types.SimpleNamespace(experiments_configfolder=tmp_dir),
                configurations=[config('ok', 'PostgreSQL', ['reset-ycsb.sql']),
                                config('none', 'CedarDB', []),
                                config('missing', 'PostgreSQL', ['reset-ycsb.sql', 'gone.sh']),
                                config('legacy', 'PostgreSQL', [], legacy=['reset-ycsb.sql'])])
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                warned = ExperimentBase.warn_missing_reset_scripts(experiment)
            self.assertEqual(warned, ['none', 'missing'])
            self.assertIn("['gone.sh'] not found", out.getvalue())
            self.assertEqual(out.getvalue().count('WARNING'), 2)
            experiment.resetscript_active = False
            self.assertEqual(ExperimentBase.warn_missing_reset_scripts(experiment), [])


class ResetInfoLineTest(unittest.TestCase):
    """TPC-H and TPC-DS name the reset in the workload info, as the OLTP benchmarks do (M1.3)."""

    def _info(self, benchmark, activate_reset):
        parameter = dict(
            mode='run', recreate_parameter=False, shuffle_queries=False, limit_import_table='',
            init_indexes=False, init_constraints=False, init_statistics=False, init_columns=False,
            datatransfer=False, num_loading_split='1', num_refresh_streams=0, num_refresh_stream_offset=0,
            duckdb_force_execution=False, verbose_explain=False, store_explain=False, timeout=600,
            activate_reset=activate_reset,
        )
        experiment = _FakeExperiment()
        benchmark.configure_workload(experiment, parameter)
        return experiment.workload['info']

    def test_info(self):
        for benchmark in (TPCH(SF='1'), TPCDS(SF='1')):
            with self.subTest(type(benchmark).__name__):
                self.assertIn('A reset script', self._info(benchmark, True))
                self.assertNotIn('A reset script', self._info(benchmark, False))


if __name__ == '__main__':
    unittest.main()
