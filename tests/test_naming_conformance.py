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
import os
import re
import tempfile
import unittest
from unittest import mock

import yaml

from bexhoma import experiment_builder, report_writer
from bexhoma.experiments.tpch import TpchExperiment

from .stubs import StubCluster

_CONTRACT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'contracts', 'contract_result.yml',
)

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
        """The SUT is the persistent, one-per-configuration exception: no experiment_run/client/benchmark_run."""
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


if __name__ == '__main__':
    unittest.main()
