"""
Conformance checks tying ``contracts/contract_result.yml``'s documented
result-folder naming contract to the actual naming code that produces it.

These exist so a future naming change (e.g. reintroducing camelCase, or
forgetting to lowercase a segment) is caught by a failing test instead of
silently drifting the on-disk contract away from what the doc promises an
agent. Built against :class:`~tests.stubs.StubCluster` (no live Kubernetes
cluster needed), the same fixture :mod:`tests.test_experiment_builder` uses.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import copy
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from bexhoma import experiment_builder, report_writer, spec
from bexhoma.experiments.tpch import TpchExperiment

from .stubs import StubCluster

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONTRACT_PATH = os.path.join(_REPO_ROOT, 'contracts', 'contract_result.yml')
_CATALOG_CONTRACT_PATH = os.path.join(_REPO_ROOT, 'contracts', 'contract_catalog.yml')

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
        {'dbms': 'PostgreSQL'},
    ],
}


class ContractSelfConsistencyTest(unittest.TestCase):
    """The contract file and the code that implements it must not drift apart."""

    def setUp(self) -> None:
        with open(_CONTRACT_PATH, 'r', encoding='utf-8') as f:
            self.contract = yaml.safe_load(f)

    def test_contract_version_matches_report_writer_schema_version(self) -> None:
        """``result_contract_version`` must equal ``report_writer.SCHEMA_VERSION``."""
        self.assertEqual(self.contract['result_contract_version'], report_writer.SCHEMA_VERSION)

    def test_tier2_files_do_not_reference_retired_names(self) -> None:
        """The old 'execution.md' filename must not resurface once renamed to 'benchmarking.md'."""
        tier2_files = self.contract['tiers']['2_evidence']['files']
        self.assertIn('report/benchmarking.md', tier2_files)
        self.assertNotIn('report/execution.md', tier2_files)

    def test_provenance_has_no_stale_execution_key(self) -> None:
        """The provenance map's key must be 'benchmarking', not the retired 'execution'."""
        self.assertIn('benchmarking', self.contract['provenance'])
        self.assertNotIn('execution', self.contract['provenance'])

    def test_no_dangling_identifier_terms_references(self) -> None:
        """Any 'identifier_terms.<name>' cross-reference in a string value must
        point at a key that actually exists under identifier_terms -- guards
        against the kind of copy-paste drift that left a 'see
        identifier_terms.component_note' pointing at a field that was never
        added."""
        identifier_terms = self.contract['structure']['identifier_terms']

        def walk(value):
            if isinstance(value, str):
                for name in re.findall(r'identifier_terms\.(\w+)', value):
                    self.assertIn(
                        name, identifier_terms,
                        f"dangling reference to identifier_terms.{name}, which doesn't exist",
                    )
            elif isinstance(value, dict):
                for v in value.values():
                    walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)

        walk(self.contract)


class CatalogContractSelfConsistencyTest(unittest.TestCase):
    """contract_catalog.yml (also loaded in production as the live catalog.yaml,
    see spec.load_catalog()) must not drift from the code that resolves it."""

    def setUp(self) -> None:
        with open(_CATALOG_CONTRACT_PATH, 'r', encoding='utf-8') as f:
            self.catalog_contract = yaml.safe_load(f)

    def test_catalog_contract_version_matches_spec_module_constant(self) -> None:
        """``catalog_contract_version`` must equal ``spec.CATALOG_CONTRACT_VERSION``."""
        self.assertEqual(self.catalog_contract['catalog_contract_version'], spec.CATALOG_CONTRACT_VERSION)

    def test_follow_up_of_is_documented_as_optional(self) -> None:
        """follow_up_of must exist in the schema and not be a required header field,
        matching validate_experiment()'s treatment of it as optional."""
        follow_up_of_field = self.catalog_contract['experiment_schema']['fields']['follow_up_of']
        self.assertEqual(follow_up_of_field['required'], False)


class FollowUpOfValidationTest(unittest.TestCase):
    """spec.validate_experiment()'s handling of the optional follow_up_of field."""

    def _catalog(self) -> dict:
        return {'workloads': {'tpch': {'supports': []}}}

    def _experiment(self, **overrides) -> dict:
        experiment = {
            'title': 't', 'hypothesis': 'h', 'discriminates': ['system'],
            'workload': {'name': 'tpch'}, 'systems': [],
        }
        experiment.update(overrides)
        return experiment

    def test_missing_follow_up_of_is_valid(self) -> None:
        spec.validate_experiment(self._catalog(), self._experiment())

    def test_string_follow_up_of_is_valid(self) -> None:
        spec.validate_experiment(self._catalog(), self._experiment(follow_up_of='1785578016'))

    def test_non_string_follow_up_of_is_rejected(self) -> None:
        with self.assertRaises(spec.SpecError):
            spec.validate_experiment(self._catalog(), self._experiment(follow_up_of=1785578016))


class GenerateComponentNameConformanceTest(unittest.TestCase):
    """generate_component_name() output must match the contract's raw_filenames rules."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        stub_cluster = StubCluster(resultfolder=self.tmp_dir.name)
        spec_path = os.path.join(self.tmp_dir.name, 'experiment.yaml')
        with open(spec_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(_BASE_SPEC, f)
        kubernetes_patch = mock.patch.object(
            experiment_builder.clusters, 'Kubernetes', return_value=stub_cluster
        )
        process_patch = mock.patch.object(TpchExperiment, 'process', lambda self: None)
        kubernetes_patch.start()
        process_patch.start()
        self.addCleanup(kubernetes_patch.stop)
        self.addCleanup(process_patch.stop)
        self.experiment = experiment_builder.build_experiment(copy.deepcopy(_BASE_SPEC), spec_path)
        self.cfg = self.experiment.configurations[0]

    def test_sut_name_has_no_run_segment_and_is_lowercase(self) -> None:
        """The SUT's live k8s object name is the one persistent, one-per-configuration
        exception: no experiment_run/client/benchmark_run baked into generate_component_name()'s
        output, since the same Deployment is restarted in place across every -nc repeat rather
        than recreated. (Its *archived manifest filename* does carry experiment_run -- see
        SutManifestPerRunTest -- but that's a separate, per-run file copy, not the object's
        own identity.)"""
        name = self.cfg.generate_component_name(
            component='sut', experiment='1784910886', configuration=self.cfg.configuration,
        )
        self.assertEqual(name, name.lower())
        expected_suffix = self.cfg.configuration.lower() + '-1784910886'
        self.assertTrue(name.endswith(expected_suffix), f"{name!r} does not end with {expected_suffix!r}")
        # No trailing numeric run/client/benchmark_run segments beyond the code itself.
        self.assertEqual(name.count('-'), expected_suffix.count('-') + 2)  # + app-component + component-configuration separators

    def test_benchmarker_name_has_full_run_segments_and_is_lowercase(self) -> None:
        """A per-round benchmarker Job name carries experiment_run/client/benchmark_run, all lowercase."""
        name = self.cfg.generate_component_name(
            component='benchmarker', experiment='1784910886', configuration=self.cfg.configuration,
            experiment_run='2', client='3', benchmark_run='1',
        )
        self.assertEqual(name, name.lower())
        self.assertTrue(name.endswith('-1784910886-2-3-1'), f"{name!r} does not end with the expected run/client/benchmark_run segments")


class SutManifestPerRunTest(unittest.TestCase):
    """start_sut() must archive one manifest file per experiment_run (even when
    the SUT is already running and nothing new is actually submitted to the
    cluster), while the live Deployment object itself keeps one stable,
    run-independent name across every repeat run."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.stub_cluster = StubCluster(resultfolder=self.tmp_dir.name)
        self.stub_cluster.yamlfolder = os.path.join(repo_root, 'k8s') + os.sep
        self.stub_cluster.namespace = 'bexhoma'
        self.stub_cluster.contextdata = {
            'namespace': 'bexhoma', 'service_sut': '{service}.{namespace}.svc.cluster.local',
        }
        self.stub_cluster.monitor_cluster_active = False
        self.stub_cluster.monitor_cluster_exists = False
        self.already_running_deployments: list = []
        self.created_objects: list = []
        self.stub_cluster.get_deployments = lambda *a, **kw: self.already_running_deployments
        self.stub_cluster.create_object_from_file = lambda path: self.created_objects.append(path)
        self.stub_cluster.get_pvc = lambda *a, **kw: []
        self.stub_cluster.get_pvc_labels = lambda *a, **kw: []
        self.stub_cluster.pvc_exists = lambda *a, **kw: False
        self.stub_cluster.delete_pvc = lambda *a, **kw: None

        spec_path = os.path.join(self.tmp_dir.name, 'experiment.yaml')
        with open(spec_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(_BASE_SPEC, f)
        kubernetes_patch = mock.patch.object(
            experiment_builder.clusters, 'Kubernetes', return_value=self.stub_cluster
        )
        process_patch = mock.patch.object(TpchExperiment, 'process', lambda self: None)
        kubernetes_patch.start()
        process_patch.start()
        self.addCleanup(kubernetes_patch.stop)
        self.addCleanup(process_patch.stop)
        self.experiment = experiment_builder.build_experiment(copy.deepcopy(_BASE_SPEC), spec_path)
        self.cfg = self.experiment.configurations[0]
        self.cfg.experiment.path = self.tmp_dir.name

    def _deployment_name(self, manifest_path: str) -> str:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            docs = list(yaml.safe_load_all(f))
        return next(d['metadata']['name'] for d in docs if isinstance(d, dict) and d.get('kind') == 'Deployment')

    def test_manifest_written_and_deployed_on_first_run(self) -> None:
        self.cfg.num_experiment_to_apply_done = 0
        result = self.cfg.lifecycle.start_sut()
        manifests = sorted(
            p for p in os.listdir(self.tmp_dir.name) if re.match(r'bexhoma-sut-.*\.yml$', p)
        )
        self.assertTrue(result)
        self.assertEqual(len(self.created_objects), 1)
        self.assertEqual(len(manifests), 1)
        self.assertTrue(manifests[0].endswith('-1.yml'))

    def test_second_run_archives_a_new_manifest_without_redeploying(self) -> None:
        self.cfg.num_experiment_to_apply_done = 0
        self.cfg.lifecycle.start_sut()
        self.already_running_deployments = ['some-existing-deployment']
        self.cfg.num_experiment_to_apply_done = 1
        result = self.cfg.lifecycle.start_sut()
        manifests = sorted(
            p for p in os.listdir(self.tmp_dir.name) if re.match(r'bexhoma-sut-.*\.yml$', p)
        )
        self.assertFalse(result)
        self.assertEqual(len(self.created_objects), 1, "create_object_from_file must not be called again")
        self.assertEqual(len(manifests), 2)
        self.assertTrue(any(m.endswith('-2.yml') for m in manifests))

    def test_deployment_name_is_stable_across_runs(self) -> None:
        self.cfg.num_experiment_to_apply_done = 0
        self.cfg.lifecycle.start_sut()
        run1_manifest = os.path.join(
            self.tmp_dir.name,
            next(p for p in os.listdir(self.tmp_dir.name) if p.endswith('-1.yml')),
        )
        name_run1 = self._deployment_name(run1_manifest)

        self.already_running_deployments = ['some-existing-deployment']
        self.cfg.num_experiment_to_apply_done = 1
        self.cfg.lifecycle.start_sut()
        run2_manifest = os.path.join(
            self.tmp_dir.name,
            next(p for p in os.listdir(self.tmp_dir.name) if p.endswith('-2.yml')),
        )
        name_run2 = self._deployment_name(run2_manifest)

        self.assertEqual(name_run1, name_run2)


class SutRestartsPerRunTest(unittest.TestCase):
    """bexhoma-sut-*-restarts.json is archived one-per-experiment_run like the
    manifest, but restartCount is cumulative across runs (same pod, not
    recreated) -- readers must aggregate by max per pod, not by summing every
    file, or the same restarts get counted once per run."""

    def test_report_writer_takes_max_per_pod_not_sum_across_runs(self) -> None:
        from bexhoma import report_writer

        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, 'bexhoma-sut-postgresql-1-1-restarts.json'), 'w') as f:
                json.dump({'pod-a': '2'}, f)
            with open(os.path.join(tmp_dir, 'bexhoma-sut-postgresql-1-2-restarts.json'), 'w') as f:
                json.dump({'pod-a': '5'}, f)
            total, per_pod = report_writer._count_sut_restarts(Path(tmp_dir))
        self.assertEqual(total, 5, "cumulative restartCount across 2 runs must be maxed, not summed to 7")
        self.assertEqual(per_pod['pod-a'], '5')


class YcsbLogToDfCasingTest(unittest.TestCase):
    """YcsbEvaluator.log_to_df() must lowercase phase/connection even when
    BEXHOMA_CONFIGURATION (sourced from the mixed-case DBMS config name) is not."""

    def test_phase_and_connection_are_lowercased(self) -> None:
        from bexhoma.evaluators.ycsb import YcsbEvaluator

        with tempfile.TemporaryDirectory() as tmp_dir:
            log_content = (
                "BEXHOMA_CONNECTION:PgDuckDB-1-1-1-1\n"
                "BEXHOMA_CONFIGURATION:PgDuckDB-1\n"
                "SF:1\n"
                "BEXHOMA_EXPERIMENT:1784910886\n"
                "BEXHOMA_EXPERIMENT_RUN:1\n"
                "BEXHOMA_CLIENT:1\n"
                "BEXHOMA_BENCHMARK_RUN:1\n"
                "YCSB_TARGET:0\n"
                "YCSB_THREADCOUNT:4\n"
                "YCSB_WORKLOAD:a\n"
                "YCSB_OPERATIONS:1000\n"
                "BEXHOMA_CHILD:1\n"
                "BEXHOMA_NUM_PODS:1\n"
                "[OVERALL], Throughput(ops/sec), 123.4\n"
            )
            log_path = os.path.join(tmp_dir, 'bexhoma-benchmarker-pgduckdb-1-1784910886-1-1-1-abcde.log')
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            evaluator = YcsbEvaluator(code='1784910886', path=tmp_dir)
            df = evaluator.log_to_df(log_path)
        self.assertFalse(df.empty)
        row = df.iloc[0]
        self.assertEqual(row['phase'], 'pgduckdb-1-1-1')
        self.assertEqual(row['connection'], 'pgduckdb-1-1-1-1-1')
        # The standalone 'configuration' column is a display field and keeps its
        # original case — only the compound phase/connection tokens are lowercased.
        self.assertEqual(row['configuration'], 'PgDuckDB-1')


class NoLegacyStreamFallbackTest(unittest.TestCase):
    """Only the "benchmarking" naming convention is supported — no fallback to
    the retired "stream" filenames. Guards against reintroducing legacy-read
    compatibility code the user explicitly did not want."""

    def test_old_style_stream_file_is_not_picked_up(self) -> None:
        from bexhoma.evaluators.logger import LogEvaluator

        with tempfile.TemporaryDirectory() as tmp_dir:
            code = '1784910886'
            os.makedirs(os.path.join(tmp_dir, code))
            legacy = os.path.join(tmp_dir, code, 'query_stream_metric_cpu_util.csv')
            with open(legacy, 'w', encoding='utf-8') as f:
                f.write('postgresql-1-1-1-1\n1.5\n2.5\n')
            evaluator = LogEvaluator(code=code, path=tmp_dir)
            df = evaluator.get_monitoring_metric('cpu_util', component='benchmarking')
        self.assertTrue(df.empty)


if __name__ == '__main__':
    unittest.main()
