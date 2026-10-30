"""
Tests for DDL parameters (:mod:`bexhoma.ddl_parameters`) and the volumes that store them.

Covers the pure functions (parsing, declarations, filling, labels, comparison
with a reused volume), the declaration files in ``experiments/``, the upload
of filled scripts, the resolution and sweep per configuration through
``tpch.run``/``ycsb.run`` against :class:`~tests.stubs.StubCluster`
(``process()`` patched out, its two steps called as it would), short volume
and worker names, the shape check and the summary's test of reused volumes.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import glob
import os
import re
import tempfile
import types
import unittest
from unittest import mock

import tpch
import ycsb
from bexhoma import ddl_parameters
from bexhoma.cli_args import MAX_STATEFULSET_NAME, abbreviate_storage_name, limit_name
from bexhoma.configurations.base import SutConfiguration
from bexhoma.configurations.loading import LoadingCoordinator
from bexhoma.experiments.base import ExperimentBase
from bexhoma.experiments.tpch import TpchExperiment
from bexhoma.experiments.ycsb import YcsbExperiment

from .test_resource_sweep import _AnyDockers, _AnyVolumes, _SweepStubCluster

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXPERIMENTS = os.path.join(_REPO, 'experiments')

#: Kubernetes label name (without prefix) and value syntax.
_LABEL_NAME = re.compile(r'^[A-Za-z0-9]([A-Za-z0-9_.-]{0,61}[A-Za-z0-9])?$')
_LABEL_VALUE = re.compile(r'^([A-Za-z0-9]([A-Za-z0-9_.-]{0,61}[A-Za-z0-9])?)?$')


class ParseTest(unittest.TestCase):

    def test_single_and_swept_values(self):
        self.assertEqual(
            ddl_parameters.parse_assignments(['num_worker_shards=16,64', 'engine=Aria']),
            {'num_worker_shards': ['16', '64'], 'engine': ['Aria']})

    def test_none_given(self):
        self.assertEqual(ddl_parameters.parse_assignments([]), {})
        self.assertEqual(ddl_parameters.parse_assignments(None), {})

    def test_values_must_be_label_values(self):
        for entry in ('engine', '=Aria', 'engine=', 'engine=Aria,', "engine=Aria'; DROP", 'engine=a b',
                      'shards=-1', 'shards=+32', 'engine=Aria.', 'engine=' + 'a' * 64):
            with self.subTest(entry):
                with self.assertRaises(ValueError):
                    ddl_parameters.parse_assignments([entry])

    def test_combinations(self):
        self.assertEqual(ddl_parameters.combinations({}), [{}])
        self.assertEqual(
            ddl_parameters.combinations({'a': ['1', '2'], 'b': ['x', 'y']}),
            [{'a': '1', 'b': 'x'}, {'a': '1', 'b': 'y'}, {'a': '2', 'b': 'x'}, {'a': '2', 'b': 'y'}])


class DeclarationTest(unittest.TestCase):

    def setUp(self):
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        self.folder = tmp_dir.name
        os.makedirs(os.path.join(self.folder, 'Citus', 'distributed'))
        os.makedirs(os.path.join(self.folder, 'PostgreSQL'))
        self.write('Citus', "# comment\n{'num_worker_shards': {'default': 32, 'type': 'int', 'description': 'shards'}}\n")

    def write(self, folder, text):
        with open(os.path.join(self.folder, folder, ddl_parameters.FILENAME), 'w') as f:
            f.write(text)

    def test_folder_parent_and_none(self):
        expected = {'num_worker_shards': {'default': '32', 'type': 'int', 'description': 'shards'}}
        self.assertEqual(ddl_parameters.load_declarations(self.folder, 'Citus'), expected)
        self.assertEqual(ddl_parameters.load_declarations(self.folder, 'Citus/distributed'), expected)
        self.assertEqual(ddl_parameters.load_declarations(self.folder, 'PostgreSQL'), {})

    def test_bad_declarations_are_refused(self):
        for text, message in (
                ("{'fillfactor': {'description': 'no default'}}", 'default'),
                ("{'fill_': {'default': 100}}", 'label name'),
                ("{'_fill': {'default': 100}}", 'label name'),
                ("{'unlogged': {'default': True}}", 'string or an int'),
                ("{'ratio': {'default': 0.5}}", 'string or an int'),
                ("{'limit': {'default': -1}}", 'not a valid label value'),
                ("{'mode': {'default': 'a', 'values': ['a', 'b c']}}", 'not a valid label value'),
                ("{'mode': {'default': 'a', 'type': 'float'}}", 'type'),
        ):
            with self.subTest(text):
                self.write('PostgreSQL', text)
                with self.assertRaisesRegex(ValueError, message):
                    ddl_parameters.load_declarations(self.folder, 'PostgreSQL')


class ValueTest(unittest.TestCase):

    declarations = {
        'engine': {'default': 'InnoDB', 'values': ['InnoDB', 'Aria']},
        'pk': {'default': 'hash', 'values': ['hash', 'asc'], 'sql': {'hash': 'HASH', 'asc': 'ASC'}},
        'shards': {'default': '32', 'type': 'int'},
    }

    def test_validate_normalises(self):
        self.assertEqual(
            ddl_parameters.validate(self.declarations, {'engine': ['InnoDB', 'Aria'], 'shards': '032'}, 'x'),
            {'engine': ['InnoDB', 'Aria'], 'shards': '32'})

    def test_validate_refuses(self):
        for given, message in (({'engine': 'MyISAM'}, 'engine=MyISAM'),
                               ({'engine': 'innodb'}, 'engine=innodb'),
                               ({'shards': 'many'}, 'not an integer')):
            with self.subTest(given):
                with self.assertRaisesRegex(ValueError, message):
                    ddl_parameters.validate(self.declarations, given, 'x')

    def test_resolve_and_sql_mapping(self):
        values = ddl_parameters.resolve(self.declarations, {'pk': 'asc', 'other': 'ignored'})
        self.assertEqual(values, {'engine': 'InnoDB', 'pk': 'asc', 'shards': '32'})
        self.assertEqual(ddl_parameters.fill_values(self.declarations, values),
                         {'engine': 'InnoDB', 'pk': 'ASC', 'shards': '32'})

    def test_only_known_keys_are_replaced(self):
        text = ("SET citus.shard_count = {shards};\n"
                "ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}', '{replica}');\n"
                "WITH (replica_placement='{\"num_replicas\": 3}');\n")
        self.assertEqual(ddl_parameters.fill(text, {'shards': '64'}), text.replace('{shards}', '64'))

    def test_labels_round_trip(self):
        values = {'engine': 'Aria', 'shards': '8'}
        labels = ddl_parameters.volume_labels(values)
        self.assertEqual(labels, {'ddl_engine': 'Aria', 'ddl_shards': '8'})
        effective, _ = ddl_parameters.compare_with_volume(
            {'engine': 'InnoDB', 'shards': '32'}, set(), labels, {})
        self.assertEqual(effective, values)

    def test_values_that_are_no_label_are_left_out(self):
        self.assertEqual(ddl_parameters.volume_labels({'a': 'ok', 'b': 'not ok', 'c': ''}, prefix='load_'),
                         {'load_a': 'ok'})


class CompareWithVolumeTest(unittest.TestCase):
    """The volume's values win; given values that differ are reported, missing labels assumed."""

    def compare(self, requested, given, labels):
        defaults = {'engine': 'InnoDB', 'shards': '32'}
        return ddl_parameters.compare_with_volume(requested, given, labels, defaults)

    def test_not_given_is_taken_from_the_volume(self):
        effective, report = self.compare({'engine': 'InnoDB', 'shards': '32'}, set(),
                                         {'ddl_engine': 'Aria', 'ddl_shards': '8'})
        self.assertEqual(effective, {'engine': 'Aria', 'shards': '8'})
        self.assertEqual(report['from_volume'], {'engine': 'Aria', 'shards': '8'})
        self.assertEqual(report['differences'], {})

    def test_given_and_equal_matches(self):
        _, report = self.compare({'engine': 'Aria', 'shards': '32'}, {'engine'},
                                 {'ddl_engine': 'Aria', 'ddl_shards': '32'})
        self.assertEqual(report['matching'], ['engine'])
        self.assertEqual(report['differences'], {})

    def test_given_and_other_differs_but_volume_wins(self):
        effective, report = self.compare({'engine': 'InnoDB', 'shards': '64'}, {'shards'},
                                         {'ddl_engine': 'InnoDB', 'ddl_shards': '8'})
        self.assertEqual(effective['shards'], '8')
        self.assertEqual(report['differences'], {'shards': ['64', '8']})

    def test_missing_label_is_assumed_and_unknown_listed(self):
        effective, report = self.compare({'engine': 'Aria', 'shards': '32'}, {'engine'},
                                         {'loaded': 'True', 'ddl_dropped_key': 'x'})
        self.assertEqual(effective, {'engine': 'InnoDB', 'shards': '32'})
        self.assertEqual(report['assumed'], ['engine', 'shards'])
        self.assertEqual(report['unknown'], ['dropped_key'])


class NameTest(unittest.TestCase):

    dockers = {'PostgreSQL': {'abbreviation': 'pg'}, 'PGBouncer': {}, 'ClickHouse': {'abbreviation': 'ch'},
               'ClickHouseCluster': {'abbreviation': 'chc'}, 'Dragonfly': {'abbreviation': 'df'},
               'DragonflyCluster': {}, 'PgDuckDB': {'abbreviation': 'pgd'}}

    def test_abbreviation_by_storage_name(self):
        for name, expected in (('postgresql', 'pg'), ('postgresql-schema-16', 'pg-schema-16'),
                               ('PostgreSQL-1', 'pg-1'), ('PgDuckDB', 'pgd'),
                               ('clickhousecluster', 'chc'), ('clickhouse-2', 'ch-2'),
                               ('dragonfly', 'df'), ('dfr', 'dfr'), ('postgresqlx', 'postgresqlx'),
                               ('cedardb', 'cedardb'), ('dbs', 'dbs')):
            with self.subTest(name):
                self.assertEqual(abbreviate_storage_name(name, self.dockers), expected)

    def test_without_dockers_nothing_changes(self):
        self.assertEqual(abbreviate_storage_name('postgresql', None), 'postgresql')

    def test_limit_name(self):
        short = 'bx-w-ci-cephcsi-tpch-100'
        self.assertEqual(limit_name(short), short)
        long_names = ['bx-w-cockroachdb-12-cephcsi-benchbase-tpcc-16000-' + suffix for suffix in 'ab']
        limited = [limit_name(name) for name in long_names]
        for name in limited:
            self.assertLessEqual(len(name), MAX_STATEFULSET_NAME)
            self.assertRegex(name, r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$')
        self.assertNotEqual(limited[0], limited[1])

    def config(self, storage_configuration, storage_class=None, num_worker=3, storage_label='tpch-100'):
        config = types.SimpleNamespace(
            configuration='Citus-1', appname='bexhoma', code='1793', storage_label=storage_label,
            num_worker=num_worker,
            storage={'storageConfiguration': storage_configuration, 'storageClassName': storage_class},
            experiment=types.SimpleNamespace(cluster=types.SimpleNamespace(
                dockers={'Citus': {'abbreviation': 'ci'}, 'TiDB': {'abbreviation': 'ti'}})))
        for method in ('get_storage_configuration', 'generate_component_name', 'get_worker_name', 'use_storage'):
            setattr(config, method, getattr(SutConfiguration, method).__get__(config))
        return config

    def test_volume_and_worker_names(self):
        config = self.config('citus', 'cephcsi')
        self.assertEqual(config.get_storage_configuration(), 'ci-cephcsi')
        self.assertEqual(config.get_worker_name(), 'bx-w-ci-cephcsi-tpch-100')
        tidb = self.config('tidb', 'nvme', storage_label='benchbase-tpcc-1600')
        self.assertEqual(tidb.get_worker_name(component='tikv'), 'bx-tikv-ti-nvme-benchbase-tpcc-1600')
        self.assertEqual(tidb.get_worker_name(component='pd'), 'bx-pd-ti-nvme-benchbase-tpcc-1600')

    def test_ephemeral_worker_names_are_per_configuration_and_experiment(self):
        """Without a volume, the name is by configuration and code: a sweep (Citus-1, Citus-2) gets two."""
        config = self.config('citus')
        config.storage = {}
        self.assertEqual(config.get_worker_name(), 'bx-w-ci-1-1793')
        config.configuration = 'Citus-2'
        self.assertEqual(config.get_worker_name(), 'bx-w-ci-2-1793')
        self.assertEqual(config.get_worker_name(component='pd'), 'bx-pd-ci-2-1793')

    def test_worker_name_never_exceeds_the_limit(self):
        config = self.config('citus-' + 'x' * 40, 'cephcsi', storage_label='benchbase-tpcc-1600')
        self.assertLessEqual(len(config.get_worker_name()), MAX_STATEFULSET_NAME)


class ShapeTest(unittest.TestCase):

    def config(self, num_worker):
        config = types.SimpleNamespace(configuration='Citus-1', num_worker=num_worker)
        config.check_volume_shape = SutConfiguration.check_volume_shape.__get__(config)
        return config

    def test_same_or_unknown_shape_passes(self):
        self.config(4).check_volume_shape('v', {'shape_num_worker': '4', 'shape_state': 'stable'})
        self.config(4).check_volume_shape('v', {'loaded': 'True'})

    def test_other_shape_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'loaded with 2 workers, but 4'):
            self.config(4).check_volume_shape('v', {'shape_num_worker': '2'})
        with self.assertRaisesRegex(ValueError, 'shape_state=changing'):
            self.config(4).check_volume_shape('v', {'shape_num_worker': '4', 'shape_state': 'changing'})


class VolumeParametersTest(unittest.TestCase):
    """Labels written at load time and taken back on reuse."""

    def config(self, ddl_parameters_, given=(), script='Schema', indexing='Index', data=None):
        config = types.SimpleNamespace(
            configuration='MariaDB-1', num_worker=0, script=script, indexing=indexing,
            ddl_parameters=dict(ddl_parameters_), ddl_given=set(given), eval_parameters={},
            ddl_declarations={'engine': {'default': 'InnoDB'}},
            experiment=types.SimpleNamespace(data_parameters=data or {}))
        for method in ('load_parameters', 'volume_parameter_labels', 'apply_volume_parameters',
                       'set_eval_parameters'):
            setattr(config, method, getattr(SutConfiguration, method).__get__(config))
        return config

    def test_labels_written_at_load_time(self):
        config = self.config({'engine': 'Aria'}, data={'insert_order': 'ordered'})
        labels = config.volume_parameter_labels()
        self.assertEqual(labels, {
            'ddl_engine': 'Aria', 'load_script': 'Schema', 'load_indexing': 'Index',
            'load_insert_order': 'ordered', 'shape_num_worker': '0', 'shape_state': 'stable'})
        for name, value in labels.items():
            self.assertRegex(name, _LABEL_NAME)
            self.assertRegex(value, _LABEL_VALUE)

    def test_reuse_takes_the_volume_values(self):
        loaded = self.config({'engine': 'Aria'}).volume_parameter_labels()
        config = self.config({'engine': 'InnoDB'}, given={'engine'}, indexing='Checks')
        with mock.patch('builtins.print'):
            check = config.apply_volume_parameters(loaded)
        self.assertEqual(config.ddl_parameters, {'engine': 'Aria'})
        self.assertEqual(config.eval_parameters, {'ddl_engine': 'Aria'})
        self.assertEqual(check['ddl']['differences'], {'engine': ['InnoDB', 'Aria']})
        self.assertEqual(check['ddl_requested'], {'engine': 'InnoDB'})
        self.assertEqual(check['load']['differences'], {'indexing': ['Checks', 'Index']})


class SummaryTest(unittest.TestCase):
    """The test ``Data parameters as requested`` from the connections' ``volume_check``."""

    def results(self, *checks):
        experiment = ExperimentBase.__new__(ExperimentBase)
        experiment._test_results = []
        connections = [{'name': f'c{i}', 'configuration': f'C-{i}', 'volume_check': check}
                       for i, check in enumerate(checks)]
        with mock.patch('builtins.print'):
            experiment._show_volume_checks(connections)
        return experiment._test_results

    @staticmethod
    def report(**kwargs):
        return {'from_volume': {}, 'differences': {}, 'matching': [], 'assumed': [], 'unknown': [], **kwargs}

    def test_no_reuse_passes(self):
        self.assertEqual(self.results({}), [(True, 'Data parameters as requested')])

    def test_old_results_record_nothing(self):
        experiment = ExperimentBase.__new__(ExperimentBase)
        experiment._test_results = []
        experiment._show_volume_checks([{'name': 'c'}])
        self.assertEqual(experiment._test_results, [])

    def test_difference_fails(self):
        check = {'ddl': self.report(from_volume={'engine': 'Aria'}, differences={'engine': ['InnoDB', 'Aria']}),
                 'load': self.report()}
        [(passed, label)] = self.results(check)
        self.assertFalse(passed)
        self.assertIn('C-0 engine: requested InnoDB, volume Aria', label)

    def test_assumed_is_skipped(self):
        check = {'ddl': self.report(assumed=['engine']), 'load': self.report(assumed=['script'])}
        [(passed, label)] = self.results(check)
        self.assertIsNone(passed)
        self.assertIn('C-0 engine, C-0 script', label)

    def test_volume_loading_errors_are_kept(self):
        config = VolumeParametersTest().config({'engine': 'InnoDB'})
        with mock.patch('builtins.print'):
            check = config.apply_volume_parameters({'ddl_engine': 'InnoDB', 'errors_schema': '0', 'errors_index': '2'})
        self.assertEqual(check['loading_errors'], {'index': 2})
        with mock.patch('builtins.print'):
            check = config.apply_volume_parameters({'ddl_engine': 'InnoDB'})
        self.assertNotIn('loading_errors', check)


class InitScriptsTest(unittest.TestCase):
    """The test ``Init scripts without errors`` from the loading logs and reused volumes."""

    def results(self, logs, connections=None):
        with tempfile.TemporaryDirectory() as folder:
            for name, text in logs.items():
                with open(os.path.join(folder, name), 'w', encoding='utf-8') as file:
                    file.write(text)
            experiment = ExperimentBase.__new__(ExperimentBase)
            experiment._test_results = []
            experiment.path = folder
            experiment.appname = 'bexhoma'
            connections = connections or [{'name': 'c1', 'configuration': 'PostgreSQL-1'},
                                          {'name': 'c10', 'configuration': 'PostgreSQL-10'}]
            with mock.patch('builtins.print'):
                experiment._show_init_script_checks(connections)
            return experiment._test_results

    def test_clean_logs_pass(self):
        logs = {'bexhoma-loading-postgresql-1-initschema-tpch-postgres.sql.log': 'CREATE TABLE ...',
                'bexhoma-loading-postgresql-1-initindexes-tpch-postgres.sql.stderr.log': 'NOTICE:  table exists\n'}
        self.assertEqual(self.results(logs), [(True, 'Init scripts without errors')])

    def test_errors_fail_per_configuration(self):
        logs = {'bexhoma-loading-postgresql-10-checkschema-tpch-postgres.sql.stderr.log': 'ERROR:  relation "x" does not exist\n',
                'bexhoma-loading-postgresql-1-initschema-tpch-postgres.sql.stderr.log':
                    'bash: line 1: /tmp/initschema-tpch.sql: No such file or directory\ncommand terminated with exit code 1\n',
                'bexhoma-index-postgresql-1-initworkers-pod-0.sh.stderr.log': 'FATAL: no\n'}
        [(passed, label)] = self.results(logs)
        self.assertFalse(passed)
        self.assertIn('PostgreSQL-1: initschema-tpch-postgres.sql, initworkers-pod-0.sh', label)
        self.assertIn('PostgreSQL-10: checkschema-tpch-postgres.sql', label)

    def test_redis_error_replies_on_stdout(self):
        logs = {'bexhoma-loading-postgresql-1-initschema-ycsb-ycsb.sql.stdout.log': '(error) ERR unknown command\n'}
        [(passed, _)] = self.results(logs)
        self.assertFalse(passed)

    def test_skipped_scripts_are_listed_not_failed(self):
        logs = {'bexhoma-loading-postgresql-1-initschema-tpch-postgres.sql.log': 'CREATE TABLE ...'}
        connections = [{'name': 'c1', 'configuration': 'PostgreSQL-1', 'loading_skipped': ['checkschema-tpch.sql']}]
        with mock.patch('builtins.print') as printed:
            with tempfile.TemporaryDirectory() as folder:
                for name, text in logs.items():
                    with open(os.path.join(folder, name), 'w', encoding='utf-8') as file:
                        file.write(text)
                experiment = ExperimentBase.__new__(ExperimentBase)
                experiment._test_results, experiment.path, experiment.appname = [], folder, 'bexhoma'
                experiment._show_init_script_checks(connections)
        self.assertEqual(experiment._test_results, [(True, 'Init scripts without errors')])
        self.assertIn(mock.call('* PostgreSQL-1: skipped checkschema-tpch.sql'), printed.call_args_list)

    def test_nothing_loaded_records_nothing(self):
        self.assertEqual(self.results({}), [])

    def test_reused_volume_with_errors_fails(self):
        connections = [{'name': 'c1', 'configuration': 'PostgreSQL-1', 'storage_reused': True,
                        'volume_check': {'loading_errors': {'index': 2}}}]
        [(passed, label)] = self.results({}, connections)
        self.assertFalse(passed)
        self.assertIn('PostgreSQL-1: volume index 2', label)

    def test_reused_volume_clean_or_unknown(self):
        clean = [{'name': 'c1', 'configuration': 'PostgreSQL-1', 'storage_reused': True,
                  'volume_check': {'loading_errors': {}}}]
        self.assertEqual(self.results({}, clean), [(True, 'Init scripts without errors')])
        unknown = [{'name': 'c1', 'configuration': 'PostgreSQL-1', 'storage_reused': True, 'volume_check': {}}]
        [(passed, label)] = self.results({}, unknown)
        self.assertIsNone(passed)
        self.assertIn('PostgreSQL-1', label)


class CatalogCapabilityTest(unittest.TestCase):
    """``systems.<name>.ddl.<workload>`` of the contract catalog mirrors the declaration files."""

    def test_catalog_equals_declarations(self):
        from bexhoma import spec
        catalog = spec.load_catalog(os.path.join(os.path.dirname(_EXPERIMENTS), 'contracts', 'contract_catalog.yml'))
        for workload, contract in catalog['workloads'].items():
            for system in contract.get('supports', []):
                with self.subTest(workload=workload, system=system):
                    # PgDuckDB runs PostgreSQL's scripts (path_experiment_docker) and inherits its ddl (extends)
                    folder = 'PostgreSQL' if system == 'PgDuckDB' else system
                    declared = ddl_parameters.load_declarations(_EXPERIMENTS, f'{workload}/{folder}')
                    capability = spec.ddl_declarations(catalog, system, workload)
                    self.assertEqual(sorted(capability), sorted(declared))
                    for key, declaration in declared.items():
                        self.assertEqual(str(capability[key]['default']), declaration['default'])
                        self.assertEqual(capability[key].get('type', 'token'), declaration.get('type', 'token'))
                        if declaration.get('values'):
                            self.assertEqual([str(v) for v in capability[key]['values']], declaration['values'])


class RepositoryDeclarationsTest(unittest.TestCase):
    """The declaration files of ``experiments/`` and the scripts that use them."""

    def folders(self):
        return sorted(os.path.dirname(path) for path in
                      glob.glob(os.path.join(_EXPERIMENTS, '**', ddl_parameters.FILENAME), recursive=True))

    def scripts(self, folder):
        """Scripts of the folder and of its variant subfolders without an own file."""
        found = []
        for root, _, files in os.walk(folder):
            if root != folder and os.path.isfile(os.path.join(root, ddl_parameters.FILENAME)):
                continue
            found += [os.path.join(root, name) for name in files
                      if name.endswith(('.sql', '.sh')) and not name.startswith('filled_')]
        return found

    def test_every_key_is_in_the_dbms_docs(self):
        """docs/DBMS.md lists every key in the section of its DBMS, with default and values."""
        with open(os.path.join(_REPO, 'docs', 'DBMS.md'), encoding='utf-8') as f:
            sections = re.split(r'^## ', f.read(), flags=re.M)
        for folder in self.folders():
            relative = os.path.relpath(folder, _EXPERIMENTS).replace(os.sep, '/')
            if relative == 'tpch/CockroachDB':
                continue  # tpch.py has no CockroachDB
            dbms = os.path.basename(folder)
            section = next(s for s in sections if s.startswith(dbms + '\n'))
            for key, declaration in ddl_parameters.load_declarations(os.path.dirname(folder), dbms).items():
                with self.subTest(folder=relative, key=key):
                    row = next(line for line in section.splitlines() if line.startswith(f'| `{key}` |'))
                    self.assertIn(f"| `{declaration['default']}` |", row)
                    for value in declaration.get('values') or []:
                        self.assertIn(f'`{value}`', row)

    def test_every_key_is_used_and_every_placeholder_declared(self):
        self.assertTrue(self.folders())
        for folder in self.folders():
            declarations = ddl_parameters.load_declarations(folder, '.')
            with self.subTest(os.path.relpath(folder, _REPO)):
                used = set()
                for path in self.scripts(folder):
                    with open(path, encoding='utf-8') as f:
                        names = set(re.findall(r'\{([A-Za-z_][A-Za-z0-9_]*)\}', f.read()))
                    self.assertEqual(names - set(declarations) - {'BEXHOMA_SCHEMA'}, set(),
                                     f'{os.path.basename(path)} has undeclared placeholders')
                    used |= names
                self.assertEqual(set(declarations) - used, set(), 'declared but not used')

    def test_every_value_round_trips_as_a_label(self):
        for folder in self.folders():
            declarations = ddl_parameters.load_declarations(folder, '.')
            for key, declaration in declarations.items():
                for value in declaration.get('values', [declaration['default']]):
                    with self.subTest(folder=os.path.relpath(folder, _REPO), key=key, value=value):
                        labels = ddl_parameters.volume_labels({key: value})
                        [(name, label)] = labels.items()
                        self.assertRegex(name, _LABEL_NAME)
                        self.assertRegex(label, _LABEL_VALUE)
                        effective, _ = ddl_parameters.compare_with_volume({key: 'x'}, set(), labels, {})
                        self.assertEqual(effective[key], ddl_parameters.normalize(declaration, value))

    def test_no_filled_files_in_the_source_tree(self):
        self.assertEqual(glob.glob(os.path.join(_EXPERIMENTS, '**', 'filled_*'), recursive=True), [])


class ClusterConfigTest(unittest.TestCase):
    """Abbreviations in both cluster configs: the same, unique and short."""

    def dockers(self, filename):
        path = os.path.join(_REPO, filename)
        if not os.path.isfile(path):
            self.skipTest(f'{filename} not present')
        with open(path, encoding='utf-8') as f:
            return ast.literal_eval(f.read())['dockers']

    def test_abbreviations(self):
        abbreviations = {dbms: entry.get('abbreviation')
                         for dbms, entry in self.dockers('k8s-cluster.config').items()}
        given = [a for a in abbreviations.values() if a]
        self.assertEqual(len(given), len(set(given)), 'abbreviations must be unique')
        for abbreviation in given:
            self.assertRegex(abbreviation, r'^[a-z][a-z0-9]{1,2}$')
        local = os.path.join(_REPO, 'cluster.config')
        if os.path.isfile(local):
            self.assertEqual({dbms: entry.get('abbreviation') for dbms, entry in self.dockers('cluster.config').items()
                              if dbms in abbreviations}, abbreviations)


class UploadTest(unittest.TestCase):
    """``LoadingCoordinator`` fills scripts of declaring folders and copies the others unchanged."""

    def setUp(self):
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        self.tmp = tmp_dir.name
        self.experiments = os.path.join(self.tmp, 'experiments')
        for dbms in ('Citus', 'PostgreSQL'):
            os.makedirs(os.path.join(self.experiments, dbms))
            with open(os.path.join(self.experiments, dbms, 'init.sql'), 'w') as f:
                f.write("SET citus.shard_count = {num_worker_shards}; -- {shard}\n")
        with open(os.path.join(self.experiments, 'Citus', ddl_parameters.FILENAME), 'w') as f:
            f.write("{'num_worker_shards': {'default': 32, 'type': 'int'}}")

    def coordinator(self, dbms, ddl):
        cluster = types.SimpleNamespace(experiments_configfolder=self.experiments, upload_file=mock.Mock())
        cfg = types.SimpleNamespace(
            path_experiment_docker=dbms, ddl_parameters=ddl, pod_sut='pod',
            experiment=types.SimpleNamespace(cluster=cluster), execute_command_in_pod_sut=mock.Mock())
        return LoadingCoordinator(cfg), cluster

    def upload(self, dbms, ddl):
        coordinator, cluster = self.coordinator(dbms, ddl)
        target = os.path.join(self.tmp, f'{dbms}.log')
        self.assertTrue(coordinator.upload_script('init.sql', coordinator.ddl_fill_values(), '/tmp/init.sql', target))
        cluster.upload_file.assert_called_once_with(
            filename_remote='/tmp/init.sql', filename_local=target, pod='pod', container='dbms')
        with open(target) as f:
            return f.read()

    def test_declaring_folder_is_filled(self):
        self.assertEqual(self.upload('Citus', {}), "SET citus.shard_count = 32; -- {shard}\n")
        self.assertEqual(self.upload('Citus', {'num_worker_shards': '64'}),
                         "SET citus.shard_count = 64; -- {shard}\n")

    def test_other_folder_is_unchanged(self):
        self.assertEqual(self.upload('PostgreSQL', {'num_worker_shards': '64'}),
                         "SET citus.shard_count = {num_worker_shards}; -- {shard}\n")

    def test_missing_script_is_skipped(self):
        coordinator, cluster = self.coordinator('Citus', {})
        self.assertFalse(coordinator.upload_script('missing.sql', {}, '/tmp/x', os.path.join(self.tmp, 'x')))
        cluster.upload_file.assert_not_called()


class _ExperimentTestBase(unittest.TestCase):
    experiment_class = TpchExperiment
    module = tpch

    def setUp(self):
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        self.cluster = _SweepStubCluster(resultfolder=tmp_dir.name)
        self.cluster.volumes = _AnyVolumes(self.cluster.volumes)
        self.cluster.dockers = _AnyDockers(self.cluster.dockers)
        self.captured = None

        def capture(experiment_self):
            self.captured = experiment_self

        for patch in (
            mock.patch.object(self.module.clusters, 'Kubernetes', return_value=self.cluster),
            mock.patch.object(self.experiment_class, 'process', capture),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    def configs(self, *argv):
        """Build the experiment and run the two steps of ``process()`` before anything starts."""
        self.module.run(self.module.build_parser().parse_args(['run', *argv]))
        self.captured.resolve_ddl_parameters()
        self.captured.expand_resource_cells()
        return {config.configuration: config for config in self.captured.configurations}


class TpchExperimentTest(_ExperimentTestBase):

    def test_defaults_without_flags(self):
        configs = self.configs('-dbms', 'Citus', 'MonetDB', 'MariaDB')
        citus, monetdb, mariadb = (next(c for c in configs.values() if c.docker == d)
                                   for d in ('Citus', 'MonetDB', 'MariaDB'))
        self.assertEqual(citus.ddl_parameters, {'num_worker_shards': '32', 'columnar_compression': 'default'})
        self.assertEqual(mariadb.ddl_parameters, {'engine': 'InnoDB', 'histograms': 'off'})
        self.assertEqual(monetdb.ddl_parameters, {})
        for config in configs.values():
            self.assertNotIn('ddl_engine', config.eval_parameters)

    def test_nws_sets_the_shards_of_citus_only(self):
        configs = self.configs('-dbms', 'Citus', 'MonetDB', '-nws', '48', '-nw', '2')
        citus = next(c for c in configs.values() if c.docker == 'Citus')
        monetdb = next(c for c in configs.values() if c.docker == 'MonetDB')
        self.assertEqual(citus.ddl_parameters, {'num_worker_shards': '48', 'columnar_compression': 'default'})
        self.assertEqual(citus.ddl_given, {'num_worker_shards'})
        self.assertEqual(monetdb.ddl_parameters, {})

    def test_single_value_keeps_the_volume_name(self):
        configs = self.configs('-dbms', 'MariaDB', '-xddl', 'engine=Aria', '-rst', 'cephcsi', '-rss', '10Gi')
        (mariadb,) = configs.values()
        self.assertEqual(mariadb.ddl_parameters, {'engine': 'Aria', 'histograms': 'off'})
        self.assertEqual(mariadb.eval_parameters['ddl_engine'], 'Aria')
        self.assertEqual(mariadb.get_storage_configuration(), 'mariadb-cephcsi')

    def test_sweep_clones_declaring_dbms_only(self):
        configs = self.configs('-dbms', 'MariaDB', 'MonetDB', '-xddl', 'engine=InnoDB,Aria,MyISAM')
        self.assertEqual(sorted(name for name, c in configs.items() if c.docker == 'MariaDB'),
                         ['MariaDB-1', 'MariaDB-2', 'MariaDB-3'])
        monetdb = [c for c in configs.values() if c.docker == 'MonetDB']
        self.assertEqual(len(monetdb), 1)
        self.assertEqual(monetdb[0].ddl_parameters, {})
        self.assertEqual([configs[f'MariaDB-{n}'].ddl_parameters['engine'] for n in (1, 2, 3)],
                         ['InnoDB', 'Aria', 'MyISAM'])
        self.assertEqual([configs[f'MariaDB-{n}'].eval_parameters['ddl_engine'] for n in (1, 2, 3)],
                         ['InnoDB', 'Aria', 'MyISAM'])
        self.assertEqual(configs['MariaDB-2'].alias, 'MariaDB@2')

    def test_sweep_times_resource_cells(self):
        configs = self.configs('-dbms', 'MariaDB', '-xddl', 'engine=InnoDB,Aria', '-rr', '32Gi,64Gi')
        self.assertEqual(
            [(name, config.resources['requests']['memory'], config.ddl_parameters['engine'])
             for name, config in sorted(configs.items())],
            [('MariaDB-1', '32Gi', 'InnoDB'), ('MariaDB-2', '32Gi', 'Aria'),
             ('MariaDB-3', '64Gi', 'InnoDB'), ('MariaDB-4', '64Gi', 'Aria')])

    def test_sweep_with_persistent_storage_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'persistent storage'):
            self.configs('-dbms', 'MariaDB', '-xddl', 'engine=InnoDB,Aria', '-rst', 'cephcsi', '-rss', '10Gi')

    def test_unknown_key_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'fillfactor'):
            self.configs('-dbms', 'MariaDB', '-xddl', 'fillfactor=80')

    def test_value_not_allowed_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'engine=ColumnStore'):
            self.configs('-dbms', 'MariaDB', '-xddl', 'engine=InnoDB,ColumnStore')


class YcsbExperimentTest(_ExperimentTestBase):
    experiment_class = YcsbExperiment
    module = ycsb

    def test_dbms_with_placeholders_get_defaults(self):
        configs = self.configs('-dbms', 'Citus', 'CockroachDB', 'TiDB', 'PostgreSQL', '-nw', '3')
        by_docker = {config.docker: config for config in configs.values()}
        self.assertEqual(by_docker['Citus'].ddl_parameters,
                         {'num_worker_shards': '32', 'num_worker_replicas': '1', 'fillfactor': '100'})
        self.assertEqual(by_docker['CockroachDB'].ddl_parameters,
                         {'num_worker_replicas': '3', 'pk_hash': 'hash', 'bucket_count': 'default',
                          'range_max_bytes': 'default', 'column_families': 'one', 'pre_split': 'none'})
        self.assertEqual(by_docker['TiDB'].ddl_parameters,
                         {'num_worker_replicas': '3', 'clustered': 'default', 'split_regions': 'none',
                          'shard_row_id_bits': 'none', 'pre_split_regions': 'none'})
        self.assertEqual(by_docker['PostgreSQL'].ddl_parameters, {'fillfactor': '100', 'autovacuum_scale': '0.2'})

    def test_defaults_reproduce_the_scripts(self):
        """With the defaults, the filled scripts equal the scripts before the placeholders."""
        expected = {
            'PostgreSQL': ('initschema-ycsb.sql', ') WITH (fillfactor = 100, autovacuum_vacuum_scale_factor = 0.2);'),
            'Citus': ('initschema-ycsb.sql', ') WITH (fillfactor = 100);'),
            'CockroachDB': ('initschema-ycsb.sql', 'YCSB_KEY  VARCHAR(255) PRIMARY KEY USING HASH,'),
            'YugabyteDB': ('initschema-ycsb.sql', 'PRIMARY KEY (YCSB_KEY HASH)\n) ;'),
            'TiDB': ('initschema-ycsb.sql', 'YCSB_KEY  VARCHAR(255) PRIMARY KEY ,'),
            'MySQL': ('initschema-ycsb.sql',
                      ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;'),
            'MariaDB': ('initschema-ycsb.sql', '    PRIMARY KEY (`YCSB_KEY`)\n)  ;'),
        }
        for dbms, (script, line) in expected.items():
            with self.subTest(dbms):
                folder = os.path.join(_EXPERIMENTS, 'ycsb', dbms)
                declarations = ddl_parameters.load_declarations(os.path.join(_EXPERIMENTS, 'ycsb'), dbms)
                with open(os.path.join(folder, script), encoding='utf-8') as f:
                    filled = ddl_parameters.fill(f.read(), ddl_parameters.fill_values(
                        declarations, ddl_parameters.resolve(declarations, {})))
                self.assertIn(line, filled)
                self.assertNotRegex(filled, r'\{(' + '|'.join(declarations) + r')\}')

    def test_requirements_are_checked_before_start(self):
        with self.assertRaisesRegex(ValueError, 'split_regions=16 requires clustered'):
            self.configs('-dbms', 'TiDB', '-nw', '3', '-xddl', 'clustered=nonclustered', '-xddl', 'split_regions=16')
        with self.assertRaisesRegex(ValueError, 'num_tablets=8 requires pk_sharding'):
            self.configs('-dbms', 'YugabyteDB', '-xddl', 'pk_sharding=hash,asc', '-xddl', 'num_tablets=8')

    def test_requirements_allow_valid_combinations(self):
        configs = self.configs('-dbms', 'TiDB', '-nw', '3', '-xddl', 'clustered=default,clustered',
                               '-xddl', 'split_regions=16')
        self.assertEqual(len(configs), 2)

    def test_cockroachdb_without_hash(self):
        declarations = ddl_parameters.load_declarations(os.path.join(_EXPERIMENTS, 'ycsb'), 'CockroachDB')
        values = ddl_parameters.fill_values(declarations, ddl_parameters.resolve(declarations, {'pk_hash': 'none'}))
        self.assertEqual(values['pk_hash'], '')

    def test_shard_sweep_normalises(self):
        configs = self.configs('-dbms', 'Citus', '-nw', '3', '-xddl', 'num_worker_shards=016,64')
        self.assertEqual(sorted((name, config.ddl_parameters['num_worker_shards'])
                                for name, config in configs.items()),
                         [('Citus-1', '16'), ('Citus-2', '64')])

    def test_insert_order_is_a_load_parameter(self):
        configs = self.configs('-dbms', 'PostgreSQL', '-xio', 'ordered')
        (config,) = configs.values()
        self.assertEqual(config.load_parameters()['insert_order'], 'ordered')

    def test_dragonfly_replica_mode_has_its_own_volume(self):
        modes = {}
        for argv in (('-nw', '3'), ('-nw', '3', '-nwr', '1')):
            configs = self.configs('-dbms', 'Dragonfly', *argv)
            (config,) = configs.values()
            modes[argv] = config.storage['storageConfiguration']
        self.assertEqual(modes, {('-nw', '3'): 'dragonfly', ('-nw', '3', '-nwr', '1'): 'dfr'})


if __name__ == '__main__':
    unittest.main()
