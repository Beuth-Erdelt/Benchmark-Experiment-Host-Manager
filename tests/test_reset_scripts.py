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
from bexhoma.configurations.loading import LoadingCoordinator, script_failed
from bexhoma.experiments.base import ExperimentBase

from .test_load_mode_workload import _FakeExperiment
from .test_resource_sweep import _AnyDockers, _AnyVolumes, _dbms_choices, _SweepStubCluster

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: DBMS without reset scripts (plan decision D1).
NO_RESET = {'DatabaseService'}

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
        'CedarDB': ['reset-ycsb.sql'],
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
        'CedarDB': ['reset-benchbase.sql'],
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
        'CedarDB': ['reset-tpch.sql'],
        'ClickHouse': [_FLUSH],
        'ClickHouseCluster': ['reset-tpch.sql', _FLUSH],
    },
    'tpcds.py': {
        'PostgreSQL': ['reset-tpcds.sql'],
        'MonetDB': ['reset-tpcds.sql'],
        'MySQL': ['reset-tpcds.sql', _FLUSH],
        'MariaDB': ['reset-tpcds.sql', _FLUSH],
        'ClickHouse': [_FLUSH],
        'ClickHouseCluster': ['reset-tpcds.sql', _FLUSH],
    },
    'ssb.py': {
        'PostgreSQL': ['reset-ssb.sql'],
        'MonetDB': ['reset-ssb.sql'],
        'ClickHouse': [_FLUSH],
        'ClickHouseCluster': ['reset-ssb.sql', _FLUSH],
        'PgDuckDB': ['reset-ssb.sql'],
        'Citus': ['reset-ssb.sql'],
        'CedarDB': ['reset-ssb.sql'],
        'MySQL': ['reset-ssb.sql', _FLUSH],
        'MariaDB': ['reset-ssb.sql', _FLUSH],
    },
}

#: Benchbase benchmarks other than tpcc have folders (and resets) only for these DBMS (R4).
BENCHBASE_NON_TPCC = {'PostgreSQL', 'PGBouncer', 'CedarDB'}


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

    def test_ssb(self):
        self.assert_complete('ssb.py')

    def test_benchbase(self):
        for benchmark in ('tpcc', 'twitter', 'ycsb', 'chbenchmark'):
            self.assert_complete('benchbase.py', '-xbt', benchmark, benchmark=benchmark)

    def test_yugabytedb_tpcc_uses_its_own_database(self):
        """initschema creates the database; later scripts and BenchBase connect to it, other benchmarks do not."""
        _, configurations = _run_script('benchbase.py', '-xbt', 'tpcc')
        config = next(c for c in configurations if c.docker == 'YugabyteDB')
        self.assertEqual(config.loading_parameters['BEXHOMA_DATABASE'], 'benchbase')
        for entry in (e for client_round in config.experiment_dict['benchmarker'] for e in client_round):
            self.assertEqual(entry['parameters']['BEXHOMA_DATABASE'], 'benchbase')
        folder = os.path.join(_REPO, 'experiments', 'benchbase', 'tpcc', 'YugabyteDB')
        for name in ('initschema-benchbase.sql', 'checkschema-benchbase.sql', 'reset-benchbase.sql'):
            with self.subTest(name), open(os.path.join(folder, name), encoding='utf-8') as f:
                self.assertIn('\\c benchbase\n', f.read())
        _, configurations = _run_script('benchbase.py', '-xbt', 'twitter')
        config = next(c for c in configurations if c.docker == 'YugabyteDB')
        self.assertEqual(config.loading_parameters['BEXHOMA_DATABASE'], 'yugabyte')

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
        self.assertIn("reset scripts not in folder, skipped: nope.sql", out.getvalue())

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

    def test_newline_in_load_data_is_escaped(self):
        """MonetDB's loadData holds a newline; a raw one breaks the sh -c command."""
        os.makedirs(os.path.join(self.cfg.experiment.cluster.experiments_configfolder, 'MonetDB'))
        open(os.path.join(self.cfg.experiment.cluster.experiments_configfolder, 'MonetDB', 'reset-tpch.sql'), 'w').close()
        sent = []
        cluster = self.cfg.experiment.cluster
        cluster.namespace = 'ns'
        cluster.get_pods = lambda **kw: ['sut-pod']
        cluster.kubectl = lambda command: None
        self.cfg.experiment.path = self.cfg.experiment.cluster.experiments_configfolder
        self.cfg.__dict__.update(
            path_experiment_docker='MonetDB', appname='bexhoma', code='1', num_tenants=0, tenant_per='',
            script_target='sut', dockertemplate={
                'loadData': "cd /home/monetdb;printf 'user=monetdb\npassword=monetdb\n' > .monetdb;mclient demo < {scriptname}",
                'template': {'JDBC': {'database': 'demo'}}},
            get_service_sut=lambda configuration: 'svc',
            execute_command_in_pod_sut=lambda cmd, retry_interrupted=True: sent.append(cmd) or ('', '', ''))
        with (
            mock.patch.object(LoadingCoordinator, 'prepare_init_dbms'),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            LoadingCoordinator(self.cfg).exec_reset_script('reset_1_1_1', ['reset-tpch.sql'])
        self.assertEqual(len(sent), 1)
        self.assertNotIn('\n', sent[0])
        self.assertIn("printf 'user=monetdb\\npassword=monetdb\\n'", sent[0])

    def _sent_with_tenants(self, tenant_per: str) -> list:
        """Commands of a reset with 3 tenants."""
        sent = []
        cluster = self.cfg.experiment.cluster
        cluster.namespace = 'ns'
        cluster.get_pods = lambda **kw: ['sut-pod']
        cluster.kubectl = lambda command: None
        self.cfg.experiment.path = cluster.experiments_configfolder
        self.cfg.__dict__.update(
            appname='bexhoma', code='1', num_tenants=3, tenant_per=tenant_per, script_target='sut',
            dockertemplate={'loadData': 'psql -d {database} < {scriptname}',
                            'template': {'JDBC': {'database': 'postgres'}}},
            get_service_sut=lambda configuration: 'svc',
            execute_command_in_pod_sut=lambda cmd, retry_interrupted=True: sent.append(cmd) or ('', '', ''))
        with (
            mock.patch.object(LoadingCoordinator, 'prepare_init_dbms'),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            LoadingCoordinator(self.cfg).exec_reset_script('reset_1_1_1', ['reset-ycsb.sql'])
        return sent

    def test_schema_tenancy_runs_once(self):
        """A reset covers the whole database, so it does not repeat per schema."""
        self.assertEqual(self._sent_with_tenants('schema'), ['psql -d postgres < /tmp/0-reset-ycsb.sql'])

    def test_database_tenancy_runs_per_tenant(self):
        self.assertEqual(self._sent_with_tenants('database'),
                         [f'psql -d tenant_{tenant} < /tmp/reset-ycsb.sql' for tenant in range(3)])


class SchemaTenancyScriptsTest(unittest.TestCase):
    """What schema tenancy needs of its scripts."""

    def test_alter_database_is_serialized(self):
        """Tenants run the statistics script in parallel and update the same catalog row."""
        with open(os.path.join(_REPO, 'experiments', 'tpch', 'PostgreSQL', 'initstatistics-tpch-schema.sql'),
                  encoding='utf-8') as f:
            text = f.read()
        positions = [text.index(statement) for statement in
                     ('BEGIN;', 'pg_advisory_xact_lock', 'ALTER DATABASE postgres', 'COMMIT;')]
        self.assertEqual(positions, sorted(positions))

    def test_benchbase_mysql_refused(self):
        """Only the PostgreSQL folder has -schema scripts; no -dbms includes MySQL."""
        for dbms in (['-dbms', 'MySQL'], ['-dbms', 'PostgreSQL', 'MySQL'], []):
            stderr = io.StringIO()
            with (
                self.subTest(dbms),
                mock.patch.object(sys, 'argv', ['benchbase.py', 'run', *dbms, '-mtb', 'schema', '-mtn', '2']),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
                self.assertRaises(SystemExit) as exit_,
            ):
                runpy.run_path(os.path.join(_REPO, 'benchbase.py'), run_name='__main__')
            self.assertEqual(exit_.exception.code, 2)
            self.assertIn('-mtb schema is not supported for MySQL', stderr.getvalue())


class ScriptFailedTest(unittest.TestCase):
    """Failure detection from the output the cluster runs produced."""

    def test_failed(self):
        cases = {
            'TiDB, wrong database': ("", "ERROR 1146 (42S02) at line 14: Table 'benchbase.customer' doesn't exist\n"
                                         "command terminated with exit code 1\n"),
            'MonetDB, missing procedure': ("", "SELECT: no such operator 'sys'.'flush_log'()\n"
                                               "command terminated with exit code 1\n"),
            'psql error, exit 0': ("", "psql:/tmp/reset-ycsb.sql:14: ERROR:  relation \"usertable\" does not exist\n"),
            'cockroach': ("", "ERROR: relation \"usertable\" does not exist\nSQLSTATE: 42P01\n"),
            'flush timeout': ("dirty pages: 3 after 600 s\n",
                              "flush timeout: 3 dirty pages left after 600 s\ncommand terminated with exit code 1\n"),
            'redis error reply': ("invoking CONFIG RESETSTAT\nERR unknown subcommand 'RESETSTAT'\n", ""),
        }
        for name, (stdout, stderr) in cases.items():
            with self.subTest(name):
                self.assertTrue(script_failed(stdout, stderr))

    def test_ok(self):
        cases = {
            'no output': ("", ""),
            'psql VERBOSE notices': ("Timing is on.\nCHECKPOINT\n",
                                     "INFO:  vacuuming \"postgres.public.usertable\"\n"
                                     "INFO:  finished vacuuming \"postgres.public.usertable\": index scans: 0\n"
                                     "NOTICE:  table \"x\" does not exist, skipping\n"),
            'mariadb password warning': ("dirty pages: 0 after 3 s\nFLUSH STATUS done\n",
                                         "Warning: Using a password on the command line interface can be insecure.\n"),
            'redis OK': ("invoking SAVE\nOK\ninvoking CONFIG RESETSTAT\nOK\n", ""),
            'citus success rows': ("nodename | nodeport | success | result\n w1 | 5432 | t | CHECKPOINT\n", ""),
        }
        for name, (stdout, stderr) in cases.items():
            with self.subTest(name):
                self.assertFalse(script_failed(stdout, stderr))


class ResetFailedRecordedTest(unittest.TestCase):
    """exec_reset_script names the failed and missing scripts in last_reset_failed."""

    def test_failed_and_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.makedirs(os.path.join(tmp_dir, 'MySQL'))
            for name in ('reset-ycsb.sql', 'reset-flush.sh'):
                open(os.path.join(tmp_dir, 'MySQL', name), 'w').close()
            outputs = {'reset-ycsb.sql': ('', ''),
                       'reset-flush.sh': ('', 'flush timeout\ncommand terminated with exit code 1\n')}
            cluster = types.SimpleNamespace(
                experiments_configfolder=tmp_dir, namespace='ns',
                get_pods=lambda **kw: ['sut-pod'], kubectl=lambda command: None)
            cfg = types.SimpleNamespace(
                configuration='MySQL-1', path_experiment_docker='MySQL', appname='bexhoma', code='1',
                num_tenants=0, tenant_per='', script_target='sut',
                dockertemplate={'loadData': 'mysql < {scriptname}', 'template': {'JDBC': {'database': 'ycsb'}}},
                experiment=types.SimpleNamespace(cluster=cluster, path=tmp_dir, volume='ycsb'),
                get_service_sut=lambda configuration: 'svc',
                execute_command_in_pod_sut=lambda cmd, retry_interrupted=True: (
                    '', *outputs['reset-flush.sh' if 'reset-flush.sh' in cmd else 'reset-ycsb.sql']))
            loader = LoadingCoordinator(cfg)
            with mock.patch.object(LoadingCoordinator, 'prepare_init_dbms'), \
                    contextlib.redirect_stdout(io.StringIO()) as out:
                loader.exec_reset_script('reset_1_1_1', ['reset-ycsb.sql', 'reset-flush.sh', 'gone.sql'])
        # a script not in the folder is skipped, not failed (as in loading)
        self.assertEqual(loader.last_reset_failed, ['reset-flush.sh'])
        self.assertIn('not in folder, skipped: gone.sql', out.getvalue())
        self.assertIn('FAILED: reset-flush.sh', out.getvalue())


class ResetSummaryTest(unittest.TestCase):
    """The Reset table shows the failed scripts; a test line says whether all resets ran fine."""

    def _df(self, failed):
        import pandas as pd
        rows = []
        for job, (seconds, value) in failed.items():
            for pod in (1, 2):                     # one row per pod of the job
                rows.append({'phase': job[:-2], 'job': job, 'experiment_run': 1, 'client': 1,
                             'benchmark_run': 1, 'time_reset': seconds, 'reset_failed': value})
        return pd.DataFrame(rows)

    def _record(self, df):
        from bexhoma.benchmarks.base import Benchmark
        recorded = []
        experiment = types.SimpleNamespace(_record_test=lambda passed, label: recorded.append((passed, label)))
        Benchmark._record_reset_test(Benchmark.__new__(Benchmark), experiment, df)
        return recorded

    def test_table_shows_failed_and_fast_resets(self):
        from bexhoma.benchmarks.base import Benchmark
        df = self._df({'pg-1-1-1': (0, ''), 'pg-1-2-1': (40, 'reset-flush.sh'), 'pg-1-3-1': (0, None)})
        rows = Benchmark._reset_rows(df)
        self.assertEqual(list(rows['job']), ['pg-1-1-1', 'pg-1-2-1'])  # 0 s reset shown, no-reset row not
        self.assertEqual(list(rows['reset_failed']), ['', 'reset-flush.sh'])

    def test_test_line(self):
        self.assertEqual(self._record(self._df({'pg-1-1-1': (3, '')})),
                         [(True, 'Reset scripts ran without errors')])
        passed, label = self._record(self._df({'pg-1-1-1': (3, ''), 'pg-1-2-1': (40, 'reset-flush.sh')}))[0]
        self.assertFalse(passed)
        self.assertIn('pg-1-2-1: reset-flush.sh', label)
        self.assertEqual(self._record(self._df({'pg-1-1-1': (0, None)})), [])   # no reset ran


class ResetInAgentReportTest(unittest.TestCase):
    """The agent report explains a failed reset and links the reset logs."""

    def test_validity_rule(self):
        from bexhoma import report_writer
        self.assertIn('| `Reset scripts ran without errors` |', report_writer._VALIDITY_RULES_MD)

    def test_reset_logs_have_their_own_group(self):
        from pathlib import Path
        from bexhoma import report_writer
        with tempfile.TemporaryDirectory() as tmp_dir:
            names = ['bexhoma-reset_1_1_1-mysql-1-reset-flush-mysql.sh.stdout.log',
                     'bexhoma-reset_1_2_1-mysql-1-reset-ycsb-ycsb.sql.stderr.log',
                     'bexhoma-loading-mysql-1-reset-flush-mysql.sh.log']   # uploaded script, not output
            for name in names:
                open(os.path.join(tmp_dir, name), 'w').close()
            groups = report_writer._group_result_files(Path(tmp_dir))
        self.assertEqual(sorted(p.name for p in groups['reset-output']), sorted(names[:2]))
        self.assertEqual([p.name for p in groups['loading-scripts']], names[2:])


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
                                config('none', 'DatabaseService', []),
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


class ResetSectionTest(unittest.TestCase):
    """The Reset table has one row per job, although the connections have one row per pod."""

    def test_one_row_per_job(self):
        import pandas as pd
        df_connections = pd.DataFrame([
            dict(phase='pg-1-1-1', job='pg-1-1-1-1', experiment_run=1, client=1, benchmark_run=1, time_reset=4.0),
            dict(phase='pg-1-1-2', job='pg-1-1-2-1', experiment_run=1, client=2, benchmark_run=1, time_reset=13.0),
            dict(phase='pg-1-1-2', job='pg-1-1-2-1', experiment_run=1, client=2, benchmark_run=1, time_reset=13.0),
            dict(phase='pg-1-1-3', job='pg-1-1-3-1', experiment_run=1, client=3, benchmark_run=1, time_reset=0.0),
        ])
        section = TPCH(SF='1')._build_reset_section(df_connections)
        self.assertEqual(section.dataframe['job'].tolist(), ['pg-1-1-1-1', 'pg-1-1-2-1'])
        self.assertEqual(section.dataframe['time_reset'].tolist(), [4.0, 13.0])


if __name__ == '__main__':
    unittest.main()
