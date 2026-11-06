"""
Tests for the per-DBMS, per-benchmark descriptors in the cluster configuration.

* :mod:`bexhoma.system_descriptors` accessors and validation, on a small neutral dict.
* The real ``k8s-cluster.config`` (and the local ``cluster.config``, when present)
  hold valid descriptors, and both declare the same ones.
* Until the entry scripts read the descriptors (they still carry the per-DBMS
  blocks), the data must say exactly what the scripts do: the DBMS with an entry
  are the ``-dbms`` choices, the ``default`` ones are what runs without ``-dbms``,
  and alias, dialect, loading template and script folder equal what each script
  configures (the committed snapshots of ``test_dbms_snapshots``).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import json
import os
import unittest

from bexhoma import system_descriptors as sd

from .test_dbms_snapshots import SCRIPTS, build_snapshot
from .test_resource_sweep import _dbms_choices

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SNAPSHOT_DIR = os.path.join(_REPO, 'tests', 'snapshots')

#: Entry script -> benchmark key of ``dockers.<x>.benchmarks`` (the key of ``volumes``).
BENCHMARK_OF_SCRIPT = {'hammerdb.py': 'tpcc', 'tpch.py': 'tpch', 'tpcds.py': 'tpcds',
                       'ssb.py': 'ssb', 'benchbase.py': 'benchbase', 'ycsb.py': 'ycsb'}


def _load(name: str) -> dict:
    with open(os.path.join(_REPO, name), encoding='utf-8') as file:
        return ast.literal_eval(file.read())


def _small() -> dict:
    return {
        'A': {'benchmarks': {'x': {'default': True, 'alias': 'A1'}, 'y': {'alias': 'A2', 'dialect': 'd'}}},
        'B': {'base_system': 'A', 'benchmarks': {'x': {'alias': 'B1'}}},
        'C': {},
    }


class AccessorsTest(unittest.TestCase):

    def test_compatible_is_the_set_of_entries(self) -> None:
        self.assertEqual(sd.compatible_dockers(_small(), 'x'), ['A', 'B'])
        self.assertEqual(sd.compatible_dockers(_small(), 'y'), ['A'])
        self.assertEqual(sd.compatible_dockers(_small(), 'z'), [])

    def test_default_needs_the_flag(self) -> None:
        self.assertEqual(sd.default_dockers(_small(), 'x'), ['A'])
        self.assertEqual(sd.default_dockers(_small(), 'y'), [])

    def test_entry_and_missing_entry(self) -> None:
        self.assertEqual(sd.benchmark_entry(_small(), 'A', 'y')['dialect'], 'd')
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, r"B is not compatible with benchmark 'y' \(compatible: A\)"):
            sd.benchmark_entry(_small(), 'B', 'y')
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, 'unknown DBMS'):
            sd.benchmark_entry(_small(), 'Q', 'x')

    def test_base_system(self) -> None:
        self.assertEqual(sd.base_system(_small(), 'B'), 'A')
        self.assertEqual(sd.base_system(_small(), 'A'), 'A')


class ValidationTest(unittest.TestCase):

    def check(self, dockers: dict) -> list:
        return sd.validate_descriptors(dockers, {'x', 'y'})

    def test_valid(self) -> None:
        self.assertEqual(self.check(_small()), [])

    def test_problems_are_named(self) -> None:
        dockers = _small()
        dockers['B']['base_system'] = 'Q'
        dockers['A']['benchmarks']['z'] = {'alias': 'a'}
        dockers['A']['benchmarks']['x']['colour'] = 'red'
        dockers['A']['benchmarks']['y']['default'] = 'yes'
        dockers['C'] = {'benchmarks': {'x': {'alias': ''}, 'y': 'not a dict'}}
        problems = '\n'.join(self.check(dockers))
        for expected in ("B: base_system 'Q'", 'A.benchmarks.z: unknown benchmark', "A.benchmarks.x: unknown key 'colour'",
                         'A.benchmarks.y.default: must be bool', 'C.benchmarks.x.alias: must not be empty',
                         'C.benchmarks.y: must be a dict'):
            self.assertIn(expected, problems)

    def test_template_must_exist(self) -> None:
        dockers = {'A': {'benchmarks': {'x': {'loading_template': 'no-such-template.yml'}}}}
        problems = sd.validate_descriptors(dockers, {'x'}, template_folder=os.path.join(_REPO, 'k8s'))
        self.assertEqual(len(problems), 1)
        self.assertIn('no-such-template.yml not found', problems[0])


class ConfigFilesTest(unittest.TestCase):

    def test_main_config_is_valid(self) -> None:
        config = _load('k8s-cluster.config')
        self.assertEqual(sd.validate_descriptors(config['dockers'], set(config['volumes']),
                                                 os.path.join(_REPO, 'k8s')), [])

    @unittest.skipUnless(os.path.exists(os.path.join(_REPO, 'cluster.config')), 'cluster.config is local (git-ignored)')
    def test_local_config_declares_the_same(self) -> None:
        main, local = _load('k8s-cluster.config')['dockers'], _load('cluster.config')['dockers']
        for name in main:
            for key in ('benchmarks', 'base_system'):
                with self.subTest(docker=name, key=key):
                    self.assertEqual(main[name].get(key), local.get(name, {}).get(key))


class DescriptorsMatchScriptsTest(unittest.TestCase):
    """The data equals what the entry scripts still hard-code."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.dockers = _load('k8s-cluster.config')['dockers']

    def test_compatible_dockers_are_the_dbms_choices(self) -> None:
        for script, benchmark in BENCHMARK_OF_SCRIPT.items():
            with self.subTest(script=script):
                self.assertEqual(set(sd.compatible_dockers(self.dockers, benchmark)), set(_dbms_choices(script)))

    def test_default_dockers_are_what_runs_without_dbms(self) -> None:
        for script, benchmark in BENCHMARK_OF_SCRIPT.items():
            with self.subTest(script=script):
                snapshot = build_snapshot(script, [], dbms=[])
                ran = {c['docker'] for c in snapshot['configurations']}
                self.assertEqual(set(sd.default_dockers(self.dockers, benchmark)), ran)

    def test_entries_equal_the_configurations_the_scripts_build(self) -> None:
        for script in SCRIPTS:
            benchmark = BENCHMARK_OF_SCRIPT[script]
            with open(os.path.join(_SNAPSHOT_DIR, f'{script[:-3]}-default.json'), encoding='utf-8') as file:
                snapshot = json.load(file)
            for config in snapshot['configurations']:
                docker = config['docker']
                with self.subTest(script=script, docker=docker):
                    entry = sd.benchmark_entry(self.dockers, docker, benchmark)
                    self.assertEqual(entry['alias'], config['alias'])
                    self.assertEqual(entry.get('dialect', ''), config['dialect'])
                    self.assertEqual(entry.get('loading_template', ''), config['_jobtemplate_loading'])
                    self.assertEqual(sd.base_system(self.dockers, docker), config['path_experiment_docker'])


if __name__ == '__main__':
    unittest.main()
