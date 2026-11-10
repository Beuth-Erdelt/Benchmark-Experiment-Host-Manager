"""
Tests for the per-DBMS, per-benchmark descriptors in the cluster configuration.

* :mod:`bexhoma.system_descriptors` accessors and validation, on a small neutral dict.
* The real ``k8s-cluster.config`` (and the local ``cluster.config``, when present)
  hold valid descriptors, and both declare the same ones.
* Until the entry scripts read the descriptors (they still carry the per-DBMS
  blocks), the data must say exactly what the scripts do: the DBMS with an entry
  are the ``-dbms`` choices, the ``default`` ones are what runs without ``-dbms``,
  and alias and dialect (the DBMS's own), loading template and script folder equal what each script
  configures (the committed snapshots of ``test_dbms_snapshots``).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import json
import os
import types
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
        'A': {'storage_prefix': 'a', 'template': {'alias': 'Alias-A', 'dialect': 'd'},
              'benchmarks': {'x': {'default': True}, 'y': {}}},
        'B': {'base_system': 'A', 'storage_prefix': 'b', 'template': {'alias': 'Alias-B'}, 'benchmarks': {'x': {}}},
        'C': {},
        'D': {'storage_prefix': 'd', 'template': {'alias': 'Alias-D'}, 'benchmarks': {'x': {'dimensions': True, 'unsupported_dimensions': {'wide': 'too slow'}},
                             'y': {'dimensions': False}}},
    }


class AccessorsTest(unittest.TestCase):

    def test_compatible_is_the_set_of_entries(self) -> None:
        self.assertEqual(sd.compatible_dockers(_small(), 'x'), ['A', 'B', 'D'])
        self.assertEqual(sd.compatible_dockers(_small(), 'y'), ['A', 'D'])
        self.assertEqual(sd.compatible_dockers(_small(), 'z'), [])

    def test_default_needs_the_flag(self) -> None:
        self.assertEqual(sd.default_dockers(_small(), 'x'), ['A'])
        self.assertEqual(sd.default_dockers(_small(), 'y'), [])

    def test_entry_and_missing_entry(self) -> None:
        self.assertEqual(sd.dialect(_small(), 'A'), 'd')
        self.assertEqual(sd.dialect(_small(), 'B'), '')
        self.assertEqual(sd.dialect(_small(), 'Q'), '')
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, r"B is not compatible with benchmark 'y' \(compatible: A, D\)"):
            sd.benchmark_entry(_small(), 'B', 'y')
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, 'unknown DBMS'):
            sd.benchmark_entry(_small(), 'Q', 'x')

    def test_dimensions(self) -> None:
        self.assertEqual(sd.dimension_dockers(_small(), 'x'), ['D'])
        self.assertEqual(sd.dimension_dockers(_small(), 'y'), [])

    def test_unsupported_dimension(self) -> None:
        self.assertEqual(sd.unsupported_dimension(_small(), 'D', 'x', 'wide'), 'too slow')
        self.assertEqual(sd.unsupported_dimension(_small(), 'D', 'x', 'narrow'), '')
        self.assertEqual(sd.unsupported_dimension(_small(), 'A', 'x', 'wide'), '')
        self.assertEqual(sd.unsupported_dimension(_small(), 'Q', 'x', 'wide'), '')

    def test_load_dockers_falls_back_to_the_main_config(self) -> None:
        dockers = sd.load_dockers(os.path.join(_REPO, 'no-such-cluster.config'))
        self.assertEqual(dockers, _load('k8s-cluster.config')['dockers'])

    def test_notes_selected_flag_and_always(self) -> None:
        dockers = {
            'A': {'benchmarks': {'x': {'notes': [{'text': 'A runs {n} pods.', 'when': 'selected'}]}}},
            'B': {'benchmarks': {'x': {'notes': [{'text': 'B is forced.', 'when': 'force'},
                                                 {'text': 'B always.'}]}}},
        }
        args = types.SimpleNamespace(dbms=[], n=3, force=False)
        # -dbms not given: the 'selected' note shows, the flag note does not
        self.assertEqual(sd.notes(dockers, 'x', args), '\nA runs 3 pods.\nB always.')
        args = types.SimpleNamespace(dbms=['B'], n=3, force=True)
        self.assertEqual(sd.notes(dockers, 'x', args), '\nB is forced.\nB always.')
        self.assertEqual(sd.notes(dockers, 'other', args), '')

    def test_notes_flag_does_not_need_the_dbms_selected(self) -> None:
        dockers = {'A': {'benchmarks': {'x': {'notes': [{'text': 'forced', 'when': 'force'}]}}}}
        self.assertEqual(sd.notes(dockers, 'x', types.SimpleNamespace(dbms=['Z'], force=True)), '\nforced')
        self.assertEqual(sd.notes(dockers, 'x', types.SimpleNamespace(dbms=['Z'])), '')

    def test_alias_is_the_templates_one_per_dbms(self) -> None:
        self.assertEqual(sd.alias(_small(), 'A'), 'Alias-A')
        self.assertEqual(sd.alias(_small(), 'C'), '')
        self.assertEqual(sd.alias(_small(), 'Q'), '')

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
        dockers['A']['benchmarks']['z'] = {}
        dockers['A']['benchmarks']['x']['colour'] = 'red'
        dockers['A']['benchmarks']['y']['default'] = 'yes'
        dockers['C'] = {'benchmarks': {'x': {'loading_template': ''}, 'y': 'not a dict'}}
        dockers['D']['benchmarks']['x']['unsupported_dimensions'] = ['wide']
        dockers['D']['benchmarks']['y']['notes'] = [{'when': 'f'}]
        problems = '\n'.join(self.check(dockers))
        for expected in ("B: base_system 'Q'", 'A.benchmarks.z: unknown benchmark', "A.benchmarks.x: unknown key 'colour'",
                         'A.benchmarks.y.default: must be bool', 'C.benchmarks.x.loading_template: must not be empty', 'C: has benchmarks but no template.alias',
                         'C.benchmarks.y: must be a dict', 'D.benchmarks.x.unsupported_dimensions: must be dict',
                         "D.benchmarks.y.notes: every note needs a non-empty 'text'"):
            self.assertIn(expected, problems)

    def test_variant_keys_are_type_checked_like_the_entry(self) -> None:
        dockers = _small()
        dockers['A']['benchmarks']['x']['variants'] = [
            {'when': 'num_worker > 0', 'loading_parameters': 'not a dict', 'worker_count': '', 'colour': 'red'},
            {'when': 'num_worker > 1', 'variants': []},
        ]
        problems = '\n'.join(self.check(dockers))
        for expected in ('A.benchmarks.x.variants[1].loading_parameters: must be dict',
                         'A.benchmarks.x.variants[1].worker_count: must not be empty',
                         "A.benchmarks.x.variants[1]: unknown key 'colour'",
                         "A.benchmarks.x.variants[2]: unknown key 'variants'"):
            self.assertIn(expected, problems)

    def test_sut_attributes_keys_are_known(self) -> None:
        dockers = _small()
        dockers['A']['sut_attributes'] = {'sut_rolle': 'placeholder', 'monitoring_sut': False}
        dockers['A']['benchmarks']['x']['sut_attributes'] = {'statefulsets': {'s': 1}, 'resource_swep': False}
        dockers['A']['benchmarks']['y']['variants'] = [{'when': 'num_worker > 0', 'sut_attributes': {'scripttarget': 'workers'}}]
        problems = self.check(dockers)
        self.assertEqual(len(problems), 3, problems)
        for expected, problem in zip(("A.sut_attributes: unknown key 'sut_rolle'",
                                      "A.benchmarks.x.sut_attributes: unknown key 'resource_swep'",
                                      "A.benchmarks.y.variants[1].sut_attributes: unknown key 'scripttarget'"), problems):
            self.assertIn(expected, problem)

    def test_sut_attribute_keys_exist_on_the_configuration(self) -> None:
        from bexhoma import configurations
        # the setters are methods of the configuration, the attributes are set in its __init__
        for setter in sd.SUT_SETTERS.values():
            with self.subTest(setter=setter):
                self.assertTrue(callable(getattr(configurations.default, setter, None)))
        with open(os.path.join(_REPO, 'bexhoma', 'configurations', 'base.py'), encoding='utf-8') as file:
            assigned = {node.attr for node in ast.walk(ast.parse(file.read()))
                        if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store)
                        and isinstance(node.value, ast.Name) and node.value.id == 'self'}
        for attribute in sd.SUT_ATTRIBUTES:
            with self.subTest(attribute=attribute):
                self.assertIn(attribute, assigned)

    def test_template_must_exist(self) -> None:
        dockers = {'A': {'storage_prefix': 'a', 'template': {'alias': 'a'},
                         'benchmarks': {'x': {'loading_template': 'no-such-template.yml'}}}}
        problems = sd.validate_descriptors(dockers, {'x'}, template_folder=os.path.join(_REPO, 'k8s'))
        self.assertEqual(len(problems), 1)
        self.assertIn('no-such-template.yml not found', problems[0])


class ConfigFilesTest(unittest.TestCase):

    def test_main_config_is_valid(self) -> None:
        config = _load('k8s-cluster.config')
        self.assertEqual(sd.validate_descriptors(config['dockers'], set(config['volumes']),
                                                 os.path.join(_REPO, 'k8s')), [])

    def test_catalog_option_flags_exist_in_tpch(self) -> None:
        """An env-var knob of an experiment.yaml that is a tpch.py option is passed as that option's flag."""
        import tpch
        from bexhoma.experiments.tpch_catalog import option_flags
        destinations = {option: action.dest for action in tpch.build_parser()._actions for option in action.option_strings}
        dockers = _load('k8s-cluster.config')['dockers']
        checked = 0
        for name, docker in dockers.items():
            declared = ((docker.get('benchmarks') or {}).get('tpch') or {}).get('option_parameters') or {}
            for env_var, flag in option_flags(name).items():
                with self.subTest(docker=name, env_var=env_var):
                    self.assertEqual(destinations.get(flag), declared[env_var])
                    checked += 1
        self.assertGreater(checked, 0)

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

    def test_storage_prefix_is_what_the_scripts_set(self) -> None:
        for script in SCRIPTS:
            with open(os.path.join(_SNAPSHOT_DIR, f'{script[:-3]}-default.json'), encoding='utf-8') as file:
                snapshot = json.load(file)
            for config in snapshot['configurations']:
                with self.subTest(script=script, docker=config['docker']):
                    self.assertEqual(sd.storage_prefix(self.dockers, config['docker']),
                                     config['storage']['storageConfiguration'])

    def test_experiment_yaml_dockers_are_the_former_defaults_table(self) -> None:
        """The declarative builder handled exactly these DBMS when they were a table in Python."""
        self.assertEqual(set(sd.experiment_yaml_dockers(self.dockers, 'tpch')),
                         {'PostgreSQL', 'PgDuckDB', 'MonetDB', 'MariaDB', 'MariaDBCS', 'MySQL', 'CedarDB', 'ClickHouse'})

    def test_refresh_template_resolution(self) -> None:
        dockers = {
            'A': {'benchmarks': {'x': {'refresh_template': 'r1.yml'}}},
            'B': {'benchmarks': {'x': {'refresh_template': 'r1.yml'}}},
            'C': {'benchmarks': {'x': {'refresh_template': 'r2.yml'}}},
            'D': {'benchmarks': {'x': {}}},
        }
        self.assertEqual(sd.refresh_template(dockers, ['A', 'B'], 'x'), 'r1.yml')
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, r'D has no refresh job .*\(DBMS with one: A, B, C\)'):
            sd.refresh_template(dockers, ['A', 'D'], 'x')
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, 'need different ones: A: r1.yml, C: r2.yml'):
            sd.refresh_template(dockers, ['A', 'C'], 'x')

    def test_refresh_templates_are_the_former_table(self) -> None:
        pg = 'jobtemplate-benchmarking-tpch-refresh-PostgreSQL.yml'
        former = {'PostgreSQL': pg, 'PgDuckDB': pg,
                  'MySQL': 'jobtemplate-benchmarking-tpch-refresh-MySQL.yml',
                  'MariaDB': 'jobtemplate-benchmarking-tpch-refresh-MariaDB.yml',
                  'MariaDBCS': 'jobtemplate-benchmarking-tpch-refresh-MariaDB.yml',
                  'MonetDB': 'jobtemplate-benchmarking-tpch-refresh-MonetDB.yml'}
        for docker, template in former.items():
            with self.subTest(docker=docker):
                self.assertEqual(sd.benchmark_entry(self.dockers, docker, 'tpch').get('refresh_template'), template)
        # every other DBMS of the benchmark declares a job as well (test_refresh_loaders): no code fallback
        for docker in sd.compatible_dockers(self.dockers, 'tpch'):
            with self.subTest(declared=docker):
                self.assertTrue(sd.benchmark_entry(self.dockers, docker, 'tpch').get('refresh_template'))

    def test_builder_defaults_are_the_former_special_cases(self) -> None:
        entry = lambda docker: sd.benchmark_entry(self.dockers, docker, 'tpch')
        self.assertEqual(entry('MariaDBCS')['max_loading_pods'], 1)
        self.assertNotIn('max_loading_pods', entry('MariaDB'))
        for docker in ('MariaDB', 'MariaDBCS'):
            self.assertEqual(entry(docker)['sut_parameters'], {'MARIADB_DATABASE': 'tpch'})
        self.assertEqual(entry('PgDuckDB')['option_parameters'], {'DUCKDB_FORCE_EXECUTION': 'duckdb_force_execution'})
        self.assertNotIn('option_parameters', entry('PostgreSQL'))

    def test_entries_equal_the_configurations_the_scripts_build(self) -> None:
        for script in SCRIPTS:
            benchmark = BENCHMARK_OF_SCRIPT[script]
            with open(os.path.join(_SNAPSHOT_DIR, f'{script[:-3]}-default.json'), encoding='utf-8') as file:
                snapshot = json.load(file)
            for config in snapshot['configurations']:
                docker = config['docker']
                with self.subTest(script=script, docker=docker):
                    entry = sd.benchmark_entry(self.dockers, docker, benchmark)
                    self.assertEqual(sd.alias(self.dockers, docker), config['alias'])
                    self.assertEqual(sd.dialect(self.dockers, docker), config['dialect'])
                    self.assertEqual(entry.get('loading_template', ''), config['_jobtemplate_loading'])
                    self.assertEqual(sd.base_system(self.dockers, docker), config['path_experiment_docker'])


if __name__ == '__main__':
    unittest.main()
