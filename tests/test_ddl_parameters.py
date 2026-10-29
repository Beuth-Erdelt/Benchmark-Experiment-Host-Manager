"""
Tests for DDL parameters (:mod:`bexhoma.ddl_parameters`).

Covers the pure functions (parsing, declarations, filling, volume names), the
declaration files in ``experiments/``, the upload of filled scripts, and the
resolution and sweep per configuration through ``tpch.run``/``ycsb.run``
against :class:`~tests.stubs.StubCluster` (``process()`` patched out, its two
steps called as it would).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
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
from bexhoma.configurations.loading import LoadingCoordinator
from bexhoma.experiments.tpch import TpchExperiment
from bexhoma.experiments.ycsb import YcsbExperiment

from .test_resource_sweep import _AnyDockers, _AnyVolumes, _SweepStubCluster

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXPERIMENTS = os.path.join(_REPO, 'experiments')


class ParseTest(unittest.TestCase):

    def test_single_and_swept_values(self):
        self.assertEqual(
            ddl_parameters.parse_assignments(['num_worker_shards=16,64', 'engine=Aria']),
            {'num_worker_shards': ['16', '64'], 'engine': ['Aria']})

    def test_none_given(self):
        self.assertEqual(ddl_parameters.parse_assignments([]), {})
        self.assertEqual(ddl_parameters.parse_assignments(None), {})

    def test_malformed_entries_are_refused(self):
        for entry in ('engine', '=Aria', 'engine=', 'engine=Aria,', "engine=Aria'; DROP", 'engine=a b'):
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
        with open(os.path.join(self.folder, 'Citus', ddl_parameters.FILENAME), 'w') as f:
            f.write("# comment\n{'num_worker_shards': {'default': 32, 'description': 'shards'}}\n")

    def test_folder_parent_and_none(self):
        expected = {'num_worker_shards': {'default': 32, 'description': 'shards'}}
        self.assertEqual(ddl_parameters.load_declarations(self.folder, 'Citus'), expected)
        self.assertEqual(ddl_parameters.load_declarations(self.folder, 'Citus/distributed'), expected)
        self.assertEqual(ddl_parameters.load_declarations(self.folder, 'PostgreSQL'), {})

    def test_entry_without_default_is_refused(self):
        with open(os.path.join(self.folder, 'PostgreSQL', ddl_parameters.FILENAME), 'w') as f:
            f.write("{'fillfactor': {'description': 'no default'}}")
        with self.assertRaisesRegex(ValueError, 'default'):
            ddl_parameters.load_declarations(self.folder, 'PostgreSQL')


class FillTest(unittest.TestCase):

    declarations = {
        'engine': {'default': 'InnoDB', 'values': ['InnoDB', 'Aria']},
        'pk': {'default': 'hash', 'values': ['hash', 'asc'], 'sql': {'hash': 'HASH', 'asc': 'ASC'}},
        'shards': {'default': 32},
    }

    def test_validate(self):
        ddl_parameters.validate(self.declarations, {'engine': ['InnoDB', 'Aria'], 'shards': '7'}, 'x')
        with self.assertRaisesRegex(ValueError, 'engine=MyISAM'):
            ddl_parameters.validate(self.declarations, {'engine': 'MyISAM'}, 'x')

    def test_resolve_and_sql_mapping(self):
        values = ddl_parameters.resolve(self.declarations, {'pk': 'asc', 'other': 'ignored'})
        self.assertEqual(values, {'engine': 'InnoDB', 'pk': 'asc', 'shards': 32})
        self.assertEqual(ddl_parameters.fill_values(self.declarations, values),
                         {'engine': 'InnoDB', 'pk': 'ASC', 'shards': '32'})

    def test_only_known_keys_are_replaced(self):
        text = ("SET citus.shard_count = {shards};\n"
                "ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}', '{replica}');\n"
                "WITH (replica_placement='{\"num_replicas\": 3}');\n")
        self.assertEqual(
            ddl_parameters.fill(text, {'shards': '64'}),
            text.replace('{shards}', '64'))

    def test_storage_suffix(self):
        defaults = ddl_parameters.resolve(self.declarations, {})
        self.assertEqual(ddl_parameters.storage_suffix(self.declarations, defaults), '')
        # a value given as text equal to the default is still the default
        self.assertEqual(ddl_parameters.storage_suffix(self.declarations, {**defaults, 'shards': '32'}), '')
        first = ddl_parameters.storage_suffix(self.declarations, {**defaults, 'shards': '64'})
        second = ddl_parameters.storage_suffix(self.declarations, {**defaults, 'shards': '16'})
        self.assertRegex(first, r'^ddl[0-9a-f]{6}$')
        self.assertNotEqual(first, second)
        self.assertEqual(first, ddl_parameters.storage_suffix(self.declarations, {**defaults, 'shards': '64'}))


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

    def test_defaults_are_allowed_values(self):
        for folder in self.folders():
            declarations = ddl_parameters.load_declarations(folder, '.')
            with self.subTest(os.path.relpath(folder, _REPO)):
                ddl_parameters.validate(
                    declarations, {key: declaration['default'] for key, declaration in declarations.items()}, folder)

    def test_no_filled_files_in_the_source_tree(self):
        self.assertEqual(glob.glob(os.path.join(_EXPERIMENTS, '**', 'filled_*'), recursive=True), [])


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
            f.write("{'num_worker_shards': {'default': 32}}")

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
        self.assertEqual(citus.ddl_parameters, {'num_worker_shards': 32})
        self.assertEqual(mariadb.ddl_parameters, {'engine': 'InnoDB'})
        self.assertEqual(monetdb.ddl_parameters, {})
        for config in configs.values():
            self.assertEqual(config.ddl_storage_suffix, '')
            self.assertNotIn('ddl_engine', config.eval_parameters)

    def test_nws_sets_the_shards_of_citus_only(self):
        configs = self.configs('-dbms', 'Citus', 'MonetDB', '-nws', '48', '-nw', '2')
        citus = next(c for c in configs.values() if c.docker == 'Citus')
        monetdb = next(c for c in configs.values() if c.docker == 'MonetDB')
        self.assertEqual(citus.ddl_parameters, {'num_worker_shards': '48'})
        self.assertRegex(citus.ddl_storage_suffix, r'^ddl[0-9a-f]{6}$')
        self.assertEqual(monetdb.ddl_parameters, {})

    def test_single_value_names_the_volume_and_is_evaluated(self):
        configs = self.configs('-dbms', 'MariaDB', '-xddl', 'engine=Aria', '-rst', 'cephcsi', '-rss', '10Gi')
        (mariadb,) = configs.values()
        self.assertEqual(mariadb.ddl_parameters, {'engine': 'Aria'})
        self.assertEqual(mariadb.eval_parameters['ddl_engine'], 'Aria')
        self.assertRegex(mariadb.get_storage_configuration(), r'^mariadb-ddl[0-9a-f]{6}-cephcsi$')

    def test_sweep_clones_declaring_dbms_only(self):
        configs = self.configs('-dbms', 'MariaDB', 'MonetDB', '-xddl', 'engine=InnoDB,Aria,MyISAM',
                               '-rst', 'cephcsi', '-rss', '10Gi')
        self.assertEqual(sorted(name for name, c in configs.items() if c.docker == 'MariaDB'),
                         ['MariaDB-1', 'MariaDB-2', 'MariaDB-3'])
        monetdb = [c for c in configs.values() if c.docker == 'MonetDB']
        self.assertEqual(len(monetdb), 1)
        self.assertEqual(monetdb[0].ddl_parameters, {})
        self.assertEqual([configs[f'MariaDB-{n}'].ddl_parameters['engine'] for n in (1, 2, 3)],
                         ['InnoDB', 'Aria', 'MyISAM'])
        self.assertEqual([configs[f'MariaDB-{n}'].eval_parameters['ddl_engine'] for n in (1, 2, 3)],
                         ['InnoDB', 'Aria', 'MyISAM'])
        volumes = [configs[f'MariaDB-{n}'].get_storage_configuration() for n in (1, 2, 3)]
        self.assertEqual(volumes[0], 'mariadb-cephcsi')    # the default keeps the plain volume
        self.assertEqual(len(set(volumes)), 3)
        self.assertEqual(configs['MariaDB-2'].alias, 'MariaDB@2')

    def test_sweep_times_resource_cells(self):
        configs = self.configs('-dbms', 'MariaDB', '-xddl', 'engine=InnoDB,Aria',
                               '-rr', '32Gi,64Gi', '-rst', 'cephcsi', '-rss', '10Gi')
        self.assertEqual(
            [(name, config.resources['requests']['memory'], config.ddl_parameters['engine'])
             for name, config in sorted(configs.items())],
            [('MariaDB-1', '32Gi', 'InnoDB'), ('MariaDB-2', '32Gi', 'Aria'),
             ('MariaDB-3', '64Gi', 'InnoDB'), ('MariaDB-4', '64Gi', 'Aria')])
        volumes = [config.get_storage_configuration() for config in configs.values()]
        self.assertEqual(len(set(volumes)), 4)
        self.assertEqual(configs['MariaDB-3'].get_storage_configuration(), 'mariadb-2-cephcsi')

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
        self.assertEqual(by_docker['Citus'].ddl_parameters, {'num_worker_shards': 32, 'num_worker_replicas': 1})
        self.assertEqual(by_docker['CockroachDB'].ddl_parameters, {'num_worker_replicas': 3})
        self.assertEqual(by_docker['TiDB'].ddl_parameters, {'num_worker_replicas': 3})
        self.assertEqual(by_docker['PostgreSQL'].ddl_parameters, {})

    def test_shard_sweep(self):
        configs = self.configs('-dbms', 'Citus', '-nw', '3', '-xddl', 'num_worker_shards=16,64')
        self.assertEqual(sorted((name, config.ddl_parameters['num_worker_shards'])
                                for name, config in configs.items()),
                         [('Citus-1', '16'), ('Citus-2', '64')])


if __name__ == '__main__':
    unittest.main()
