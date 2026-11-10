"""
Unit tests for :mod:`bexhoma.experiments.tpch_builder`, against a stub cluster
object (no live Kubernetes cluster needed).

``TpchExperiment.process()`` is patched to a no-op in the full-build test:
it is the seam where a live cluster would actually deploy pods, and is out
of scope for these tests — everything before it (cluster construction,
``prepare_testbed()``, per-system configuration, provenance copying) runs
for real against :class:`~tests.stubs.StubCluster`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import os
import tempfile
import unittest
from unittest import mock

import yaml

from bexhoma.experiments import tpch_builder as experiment_builder
from bexhoma.experiments.tpch import TpchExperiment
from bexhoma.system_descriptors import IncompatibleBenchmark

from .stubs import StubCluster

_BASE_SPEC = {
    'workload': 'tpch',
    'mode': 'run',
    'experiment': {'code': None, 'num_config': 1, 'timeout': 600, 'scaling_factor': '1'},
    'cluster': {'aws': False, 'context': None},
    'monitoring': {'sut': True, 'cluster': False, 'app': False},
    'rounds': [1],
    'loading': {'pods': [1], 'threads': [1], 'split': 1},
    'tpch': {
        'recreate_parameter': False, 'shuffle_queries': False,
        'init_indexes': False, 'init_constraints': False, 'init_statistics': False,
        'init_columns': False, 'datatransfer': False, 'active_queries': [],
        'refresh_streams': 0, 'refresh_stream_offset': 0, 'duckdb_force_execution': False,
    },
    'systems': [
        {
            'dbms': 'PostgreSQL', 'configuration': '', 'alias': 'DBMS A2',
            'resources': {'cpu': {'request': '4', 'limit': '4'}, 'memory': {'request': '16Gi', 'limit': '16Gi'}},
        },
        {
            'dbms': 'PgDuckDB',
            'resources': {'cpu': {'request': '4', 'limit': '4'}, 'memory': {'request': '16Gi', 'limit': '16Gi'}},
            'sut_parameters': {'DUCKDB_FORCE_EXECUTION': 'true'},
        },
    ],
}


class BuildExperimentTest(unittest.TestCase):
    """End-to-end (minus ``process()``) test of :func:`build_experiment`."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.stub_cluster = StubCluster(resultfolder=self.tmp_dir.name)

        self.spec_path = os.path.join(self.tmp_dir.name, 'experiment.yaml')
        with open(self.spec_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(_BASE_SPEC, f)

        kubernetes_patch = mock.patch.object(
            experiment_builder.clusters, 'Kubernetes', return_value=self.stub_cluster
        )
        process_patch = mock.patch.object(TpchExperiment, 'process', lambda self: None)
        kubernetes_patch.start()
        process_patch.start()
        self.addCleanup(kubernetes_patch.stop)
        self.addCleanup(process_patch.stop)

    def _build(self, spec: dict) -> TpchExperiment:
        return experiment_builder.build_experiment(spec, self.spec_path)

    def test_builds_one_configuration_per_system(self) -> None:
        """Every ``systems:`` entry becomes exactly one SutConfiguration, in order."""
        experiment = self._build(copy.deepcopy(_BASE_SPEC))
        self.assertEqual(len(experiment.configurations), 2)
        self.assertEqual(experiment.configurations[0].docker, 'PostgreSQL')
        self.assertEqual(experiment.configurations[1].docker, 'PgDuckDB')

    def test_dbms_defaults_applied(self) -> None:
        """dialect, jobtemplate_loading, and path_experiment_docker come from the DBMS's tpch entry and template in the cluster config."""
        experiment = self._build(copy.deepcopy(_BASE_SPEC))
        postgres, pgduckdb = experiment.configurations
        self.assertEqual(postgres.dialect, 'PostgreSQL')
        self.assertEqual(postgres.jobtemplate_loading, 'jobtemplate-loading-tpch-PostgreSQL.yml')
        self.assertEqual(pgduckdb.dialect, 'PostgreSQL')
        self.assertEqual(pgduckdb.path_experiment_docker, 'PostgreSQL')

    def test_resources_from_yaml(self) -> None:
        """Per-system resource requests/limits are read from the YAML block."""
        experiment = self._build(copy.deepcopy(_BASE_SPEC))
        postgres = experiment.configurations[0]
        self.assertEqual(postgres.resources['requests']['cpu'], '4')
        self.assertEqual(postgres.resources['requests']['memory'], '16Gi')
        self.assertEqual(postgres.resources['limits']['memory'], '16Gi')

    def test_storage_configuration_falls_back_to_storage_prefix(self) -> None:
        """No 'configuration:' override means storageConfiguration uses the DBMS's storage_prefix of the cluster config."""
        experiment = self._build(copy.deepcopy(_BASE_SPEC))
        postgres, pgduckdb = experiment.configurations
        self.assertEqual(postgres.storage['storageConfiguration'], 'postgresql')
        self.assertEqual(pgduckdb.storage['storageConfiguration'], 'PgDuckDB')

    def test_sut_parameters_override_wins_over_global_duckdb_default(self) -> None:
        """A system's own sut_parameters.DUCKDB_FORCE_EXECUTION beats the global tpch: default."""
        experiment = self._build(copy.deepcopy(_BASE_SPEC))
        postgres, pgduckdb = experiment.configurations
        self.assertEqual(postgres.sut_parameters, {})
        self.assertEqual(pgduckdb.sut_parameters, {'DUCKDB_FORCE_EXECUTION': 'true'})

    def test_global_duckdb_force_execution_default_used_when_system_silent(self) -> None:
        """With no per-system override, PgDuckDB falls back to the global tpch: default."""
        spec = copy.deepcopy(_BASE_SPEC)
        spec['tpch']['duckdb_force_execution'] = True
        del spec['systems'][1]['sut_parameters']
        experiment = self._build(spec)
        pgduckdb = experiment.configurations[1]
        self.assertEqual(pgduckdb.sut_parameters, {'DUCKDB_FORCE_EXECUTION': 'true'})

    def test_loading_and_rounds_applied(self) -> None:
        """Loading pod/split counts and the -ne round sweep reach the configuration."""
        spec = copy.deepcopy(_BASE_SPEC)
        spec['rounds'] = [1, 2]
        experiment = self._build(spec)
        postgres = experiment.configurations[0]
        self.assertEqual(postgres.num_loading, 1)
        self.assertEqual(postgres.num_loading_pods, 1)
        self.assertEqual(postgres.benchmark_list_template, [1, 2])

    def test_top_level_loading_pods_reach_every_configuration(self) -> None:
        """loading.pods: [4] at the top used to stay in the info text only, the loader started 1 pod."""
        spec = copy.deepcopy(_BASE_SPEC)
        spec['loading'] = {'pods': [4], 'threads': [1], 'split': 2}
        experiment = self._build(spec)
        for config in experiment.configurations:
            self.assertEqual((config.num_loading_pods, config.num_loading), (4, 2))
            self.assertEqual(config.loading_parameters['PODS_TOTAL'], '4')
            self.assertEqual(config.loading_parameters['PODS_PARALLEL'], '2')

    def test_a_system_loading_block_wins_over_the_top_level_one(self) -> None:
        spec = copy.deepcopy(_BASE_SPEC)
        spec['loading'] = {'pods': [4]}
        spec['systems'][1]['loading'] = {'pods': [2]}
        postgres, pgduckdb = self._build(spec).configurations
        self.assertEqual(postgres.num_loading_pods, 4)
        self.assertEqual(pgduckdb.num_loading_pods, 2)

    def test_loading_threads_reach_a_dbms_with_thread_variants(self) -> None:
        """MySQL declares per_loading_threads: the YAML's threads fill MYSQL_LOADING_THREADS."""
        spec = copy.deepcopy(_BASE_SPEC)
        spec['loading'] = {'pods': [1], 'threads': [8]}
        spec['systems'] = [{'dbms': 'MySQL'}]
        mysql = self._build(spec).configurations[0]
        self.assertEqual(str(mysql.loading_parameters['MYSQL_LOADING_THREADS']), '8')

    def test_unknown_dbms_raises_key_error(self) -> None:
        """A dbms with no tpch entry raises — validation is expected to have caught this earlier."""
        spec = copy.deepcopy(_BASE_SPEC)
        spec['systems'][0]['dbms'] = 'Oracle'
        with self.assertRaises(IncompatibleBenchmark):
            self._build(spec)

    def test_provenance_experiment_yaml_copied(self) -> None:
        """The experiment.yaml that was actually loaded is copied into the result folder."""
        experiment = self._build(copy.deepcopy(_BASE_SPEC))
        copied_path = os.path.join(experiment.path, 'experiment.yaml')
        self.assertTrue(os.path.isfile(copied_path))
        with open(copied_path, 'r', encoding='utf-8') as f:
            self.assertEqual(yaml.safe_load(f), _BASE_SPEC)

    def test_provenance_catalog_and_environment_copied_when_present(self) -> None:
        """catalog:/environment: pointers, when present and resolvable, are copied too."""
        catalog_path = os.path.join(self.tmp_dir.name, 'catalog.yaml')
        with open(catalog_path, 'w', encoding='utf-8') as f:
            f.write("workloads: {}\n")
        spec = copy.deepcopy(_BASE_SPEC)
        spec['catalog'] = 'catalog.yaml'
        spec['environment'] = 'does-not-exist.yml'  # missing on purpose: must be silently skipped

        experiment = self._build(spec)

        self.assertTrue(os.path.isfile(os.path.join(experiment.path, 'catalog.yaml')))
        self.assertFalse(os.path.isfile(os.path.join(experiment.path, 'environment.yml')))


class BuildPrepareTestbedParameterTest(unittest.TestCase):
    """Tests for :func:`bexhoma.experiments.tpch_builder._build_prepare_testbed_parameter`."""

    def test_overlays_yaml_fields_onto_parser_dest_names(self) -> None:
        tpch_module = experiment_builder._import_tpch_module()
        spec = copy.deepcopy(_BASE_SPEC)
        spec['rounds'] = [1, 2, 4]
        parameter = experiment_builder._build_prepare_testbed_parameter(spec, tpch_module)
        self.assertEqual(parameter['mode'], 'run')
        self.assertEqual(parameter['num_query_executors'], '1,2,4')
        self.assertEqual(parameter['num_loading_pods'], '1')
        self.assertEqual(parameter['monitoring'], True)
        self.assertEqual(parameter['dbms'], ['PostgreSQL', 'PgDuckDB'])

    def test_baseline_defaults_survive_when_yaml_omits_a_section(self) -> None:
        """A YAML with no 'loading:' block still gets tpch.py's own argparse defaults."""
        tpch_module = experiment_builder._import_tpch_module()
        spec = copy.deepcopy(_BASE_SPEC)
        del spec['loading']
        parameter = experiment_builder._build_prepare_testbed_parameter(spec, tpch_module)
        self.assertEqual(parameter['num_loading_pods'], '1')
        self.assertEqual(parameter['num_loading_threads'], '1')


if __name__ == '__main__':
    unittest.main()
