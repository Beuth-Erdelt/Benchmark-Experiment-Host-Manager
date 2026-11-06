"""
Tests for multi-tenancy (``-mtn``/``-mtb``) as a declared capability of a DBMS.

A DBMS lists the tenancy modes it supports in the ``multi_tenancy`` of its benchmark entry in
``cluster.config``. A multi-tenant run is refused, before anything starts, for a DBMS that does
not list the requested mode; otherwise it would join the tenant machinery without tenant
storage, parameters or scripts. A declared ``schema`` mode must have its tenant scripts.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import contextlib
import io
import os
import runpy
import sys
import tempfile
import types
import unittest
from unittest import mock

import benchbase
import tpch
from bexhoma import system_descriptors as sd
from bexhoma.experiments import system_builder as builder

from .test_reset_scripts import _AnyVolumes, _run_script
from .test_resource_sweep import _SweepStubCluster

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#: Placeholders the loader replaces by the durability scripts of the DBMS folder.
_PLACEHOLDERS = {'durability.sql', 'restoredurability.sql'}


def _config() -> dict:
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as file:
        return ast.literal_eval(file.read())


def _dockers() -> dict:
    return {
        'A': {'benchmarks': {'x': {'multi_tenancy': ['container', 'schema']}}},
        'B': {'benchmarks': {'x': {'multi_tenancy': ['schema']}}},
        'C': {'benchmarks': {'x': {}}},
    }


class UnsupportedTenancyTest(unittest.TestCase):

    def check(self, dbms, number, mode, dockers=None):
        return sd.unsupported_tenancy(dockers or _dockers(), 'x', dbms, number, mode)

    def test_no_tenancy_is_never_refused(self) -> None:
        self.assertEqual(self.check(['A', 'C'], 0, ''), '')
        self.assertEqual(self.check(['C'], '0', 'schema'), '')

    def test_a_listed_mode_is_fine(self) -> None:
        self.assertEqual(self.check(['A', 'B'], 2, 'schema'), '')
        self.assertEqual(self.check(['A'], 2, 'container'), '')

    def test_an_unlisted_mode_is_refused_naming_who_supports_it(self) -> None:
        message = self.check(['A', 'B'], 2, 'container')
        self.assertIn('-mtn 2 -mtb container: B does not support this tenancy in x', message)
        self.assertIn('supported: A: container, schema; B: schema', message)

    def test_a_dbms_without_multi_tenancy_is_refused(self) -> None:
        self.assertIn('C does not support', self.check(['A', 'C'], 2, 'schema'))
        self.assertIn('A, C do not support', self.check(['A', 'C'], 2, 'database'))

    def test_a_missing_mode_is_refused(self) -> None:
        self.assertIn('-mtb (missing)', self.check(['A'], 2, ''))

    def test_no_dbms_supports_it(self) -> None:
        dockers = {'C': {'benchmarks': {'x': {}}}}
        self.assertIn('no DBMS supports multi-tenancy in x', self.check(['C'], 2, 'schema', dockers))

    def test_validation_rejects_unknown_modes(self) -> None:
        dockers = {'A': {'storage_prefix': 'a', 'template': {'alias': 'a'},
                         'benchmarks': {'x': {'multi_tenancy': ['schema', 'tablespace']}}}}
        problems = sd.validate_descriptors(dockers, {'x'})
        self.assertEqual(len(problems), 1)
        self.assertIn("unknown mode 'tablespace'", problems[0])


class SelectionTest(unittest.TestCase):
    """:func:`~bexhoma.experiments.system_builder.selected_dockers` refuses before any configuration exists."""

    def args(self, number, mode):
        return types.SimpleNamespace(multi_tenant_num=number, multi_tenant_by=mode)

    def test_refused_with_the_message(self) -> None:
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, 'B does not support this tenancy'):
            builder.selected_dockers(_dockers(), 'x', ['A', 'B'], self.args('2', 'container'))

    def test_supported_and_without_args(self) -> None:
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', ['A', 'B'], self.args('2', 'schema')), ['A', 'B'])
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', ['A', 'C']), ['A', 'C'])
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', ['C'], self.args(0, '')), ['C'])


def _refused(script: str, *argv: str) -> tuple:
    """Run the script's ``__main__`` and return the exit code and what it printed to stderr."""
    stderr = io.StringIO()
    with (
        mock.patch.object(sys, 'argv', [script, 'run', *argv]),
        contextlib.redirect_stdout(io.StringIO()),
        contextlib.redirect_stderr(stderr),
    ):
        try:
            runpy.run_path(os.path.join(_REPO, script), run_name='__main__')
        except SystemExit as exit_:
            return exit_.code, stderr.getvalue()
    return None, stderr.getvalue()


class EntryScriptsTest(unittest.TestCase):
    """The real scripts. A refusal is a usage error right after parsing: no cluster is needed."""

    def test_postgresql_runs_every_mode_of_tpch(self) -> None:
        for mode in sd.TENANCY_MODES:
            with self.subTest(mode=mode):
                _, configurations = _run_script('tpch.py', '-dbms', 'PostgreSQL', '-mtn', '2', '-mtb', mode, '-nlp', '2')
                self.assertEqual({c.docker for c in configurations}, {'PostgreSQL'})
                self.assertEqual(len(configurations), 2 if mode == 'container' else 1)

    def test_other_dbms_are_refused_by_tpch(self) -> None:
        for docker in ('MySQL', 'MariaDB', 'MonetDB', 'ClickHouse', 'CedarDB', 'Citus'):
            with self.subTest(docker=docker):
                code, stderr = _refused('tpch.py', '-dbms', docker, '-mtn', '2', '-mtb', 'database', '-nlp', '2')
                self.assertEqual(code, 2)
                self.assertIn(f'{docker} does not support this tenancy in tpch', stderr)

    def test_a_mixed_selection_is_refused_as_a_whole(self) -> None:
        code, stderr = _refused('tpch.py', '-dbms', 'PostgreSQL', 'MySQL', '-mtn', '2', '-mtb', 'schema', '-nlp', '2')
        self.assertEqual(code, 2)
        self.assertIn('MySQL does not support', stderr)
        self.assertNotIn('PostgreSQL does not support', stderr)

    def test_benchmarks_without_tenancy_refuse_it(self) -> None:
        for script in ('tpcds.py', 'hammerdb.py'):
            with self.subTest(script=script):
                code, stderr = _refused(script, '-dbms', 'PostgreSQL', '-mtn', '2', '-mtb', 'schema')
                self.assertEqual(code, 2)
                self.assertIn('no DBMS supports multi-tenancy', stderr)

    def test_the_in_process_run_refuses_too(self) -> None:
        """``experiment.py`` calls ``tpch.run`` without the command line parser."""
        args = tpch.build_parser().parse_args(['run', '-dbms', 'MySQL', '-mtn', '2', '-mtb', 'database', '-nlp', '2'])
        with tempfile.TemporaryDirectory() as tmp_dir:
            cluster = _SweepStubCluster(resultfolder=tmp_dir)
            cluster.volumes = _AnyVolumes(cluster.volumes)
            with (
                mock.patch('bexhoma.clusters.Kubernetes', return_value=cluster),
                contextlib.redirect_stdout(io.StringIO()),
                self.assertRaisesRegex(sd.IncompatibleBenchmark, 'MySQL does not support this tenancy in tpch'),
            ):
                tpch.run(args)

    def test_benchbase_supports_the_modes_it_declares(self) -> None:
        for mode, dbms in (('database', ['PostgreSQL', 'MySQL']), ('container', ['PostgreSQL', 'MySQL']),
                           ('schema', ['PostgreSQL'])):
            with self.subTest(mode=mode):
                _, configurations = _run_script('benchbase.py', '-dbms', *dbms, '-mtn', '2', '-mtb', mode)
                self.assertEqual({c.docker for c in configurations}, set(dbms))

    def test_no_tenancy_is_unaffected(self) -> None:
        _, configurations = _run_script('tpch.py', '-dbms', 'MySQL')
        self.assertEqual({c.docker for c in configurations}, {'MySQL'})


class DeclaredModesTest(unittest.TestCase):
    """What a DBMS declares has to exist."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = _config()

    def declared(self):
        for docker, spec in self.config['dockers'].items():
            for benchmark, entry in (spec.get('benchmarks') or {}).items():
                if entry.get('multi_tenancy'):
                    yield docker, benchmark, entry['multi_tenancy']

    def test_modes_are_known(self) -> None:
        for docker, benchmark, modes in self.declared():
            with self.subTest(docker=docker, benchmark=benchmark):
                self.assertTrue(set(modes) <= set(sd.TENANCY_MODES), modes)

    def test_the_schema_mode_has_its_tenant_scripts(self) -> None:
        """Schema tenancy switches to the tenant script collections of the benchmark's volume; the
        DBMS's script folder has to hold every file of them."""
        helpers = {'tpch': lambda modes: tpch.tenant_parameters(
                       types.SimpleNamespace(tenant_per='schema', num_tenants=2), {'multi_tenancy': modes}, None, 'p'),
                   'benchbase': lambda modes: benchbase.tenant_parameters(
                       types.SimpleNamespace(tenant_per='schema', num_tenants=2, multi_tenant_volume=False),
                       {'multi_tenancy': modes}, None, 'p')}
        checked = set()
        for docker, benchmark, modes in self.declared():
            if 'schema' not in modes:
                continue
            with self.subTest(docker=docker, benchmark=benchmark):
                self.assertIn(benchmark, helpers, 'add the script collections of this benchmark to this test')
                scripts = helpers[benchmark](modes)['experiment']
                initscripts = self.config['volumes'][benchmark]['initscripts']
                # Benchbase keeps its scripts per benchmark type (tpcc is the default of -xbt)
                path = ('experiments', benchmark, *(('tpcc',) if benchmark == 'benchbase' else ()),
                        sd.base_system(self.config['dockers'], docker))
                folder = os.path.join(_REPO, *path)
                for collection in scripts.values():
                    self.assertIn(collection, initscripts)
                    for name in initscripts[collection]:
                        if name not in _PLACEHOLDERS:
                            self.assertTrue(os.path.isfile(os.path.join(folder, name)), f'{name} missing in {folder}')
                checked.add(benchmark)
        self.assertEqual(checked, {'tpch', 'benchbase'})

    def test_postgresql_supports_all_modes_in_tpch(self) -> None:
        entry = self.config['dockers']['PostgreSQL']['benchmarks']['tpch']
        self.assertEqual(entry['multi_tenancy'], list(sd.TENANCY_MODES))


if __name__ == '__main__':
    unittest.main()
