"""
Unit tests for :mod:`bexhoma.hardware_baseline`.

Schedule-computation tests run against plain node-name lists (no cluster
needed). The setup-phase tests construct a real ``HardwareExperiment``
against a stub cluster (:class:`tests.stubs.StubCluster`, extended here with
the ``hardware`` volume / ``Hardware`` docker entries
``HardwareExperiment.__init__``/``SutConfiguration.__init__`` require) and
patch ``HardwareExperiment.process()``/``remove_experiment()`` to no-ops --
the same seam ``tests/test_experiment_builder.py`` uses for ``TpchExperiment``.
Everything up to ``process()`` (cluster/config bootstrap, per-node pinning,
per-round parameter/``BEXHOMA_HOST`` overrides, round counts) runs for real,
without a live cluster or submitting any Kubernetes object.

The ``_collect_results`` tests exercise result-parsing against a fake
evaluator returning realistic ``client``-column values -- this is the class
of test the setup-phase tests above do *not* cover, since they patch
``process()`` to a no-op before any result ever gets parsed. That gap let a
real bug through once already: ``client`` values here are 1-indexed (the
first round a config runs -- the sysbench CPU/RAM self-test -- is logged as
``client == 1``), confirmed against a real multi-node run's pickled results;
see the comment on ``hardware_baseline._CPU_BASELINE_ROUND`` for why (a
``cfg.client - 1`` write in ``ManifestBuilder.create_manifest_job()`` looks
0-indexed in isolation, but ``work_benchmark_list()`` already increments
``config.client`` before that write happens, cancelling it back out).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import itertools
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

import pandas as pd

from bexhoma import hardware_baseline
from bexhoma.experiments.hardware import HardwareExperiment

from .stubs import StubCluster


class _HardwareStubCluster(StubCluster):
    """``StubCluster`` extended with the ``hardware`` volume / ``Hardware``
    docker entries ``HardwareExperiment.__init__``/``SutConfiguration.__init__``
    unconditionally index (see ``HardwareExperiment.__init__``'s own comment
    on ``cluster.config['volumes']['hardware']``)."""

    def __init__(self, resultfolder: str) -> None:
        super().__init__(resultfolder)
        self.volumes['hardware'] = {'id': 'hardware', 'initscripts': {'Schema': []}}
        self.dockers['Hardware'] = {}


class ComputeRoundRobinScheduleTest(unittest.TestCase):
    """Tests for :func:`bexhoma.hardware_baseline.compute_round_robin_schedule`."""

    def _assert_valid_schedule(self, nodes: list) -> dict:
        """Assert full-coverage, disjoint-per-round, reciprocated pairing; return the schedule."""
        schedule = hardware_baseline.compute_round_robin_schedule(nodes)
        self.assertEqual(set(schedule), set(nodes))
        round_lengths = {len(targets) for targets in schedule.values()}
        self.assertEqual(len(round_lengths), 1, "every node must have the same round count")
        rounds = round_lengths.pop()
        all_pairs = set()
        for round_index in range(rounds):
            targets_this_round = [
                targets[round_index] for targets in schedule.values() if targets[round_index] is not None
            ]
            self.assertEqual(
                len(targets_this_round), len(set(targets_this_round)),
                f"round {round_index} reuses a node as more than one target",
            )
            for node, targets in schedule.items():
                target = targets[round_index]
                if target is not None:
                    self.assertEqual(
                        schedule[target][round_index], node,
                        f"round {round_index}: {node}->{target} is not reciprocated",
                    )
                    all_pairs.add(frozenset((node, target)))
        expected_pairs = {frozenset(pair) for pair in itertools.combinations(nodes, 2)}
        self.assertEqual(all_pairs, expected_pairs)
        return schedule

    def test_even_node_count_covers_every_pair_exactly_once(self) -> None:
        schedule = self._assert_valid_schedule(['n1', 'n2', 'n3', 'n4'])
        self.assertEqual(len(schedule['n1']), 3)

    def test_odd_node_count_pads_with_bye_and_covers_every_pair(self) -> None:
        schedule = self._assert_valid_schedule(['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(len(schedule['a']), 5)
        for node, targets in schedule.items():
            self.assertEqual(targets.count(None), 1, f"{node} should have exactly one bye round")

    def test_three_nodes(self) -> None:
        self._assert_valid_schedule(['x', 'y', 'z'])

    def test_single_node_has_no_rounds(self) -> None:
        self.assertEqual(hardware_baseline.compute_round_robin_schedule(['only']), {'only': []})

    def test_empty_node_list(self) -> None:
        self.assertEqual(hardware_baseline.compute_round_robin_schedule([]), {})


class ComputeStarScheduleTest(unittest.TestCase):
    """Tests for :func:`bexhoma.hardware_baseline.compute_star_schedule`."""

    def test_every_spoke_targets_the_hub(self) -> None:
        schedule = hardware_baseline.compute_star_schedule(['n1', 'n2', 'n3'], 'n1')
        self.assertEqual(schedule['n2'], ['n1'])
        self.assertEqual(schedule['n3'], ['n1'])

    def test_hub_gets_a_self_test_round_not_zero_rounds(self) -> None:
        """The hub must still have one round (target None), so every node's
        benchmark_list stays the same length for round-indexed lockstep."""
        schedule = hardware_baseline.compute_star_schedule(['n1', 'n2', 'n3'], 'n1')
        self.assertEqual(schedule['n1'], [None])
        self.assertEqual({len(targets) for targets in schedule.values()}, {1})

    def test_hub_not_in_nodes_raises(self) -> None:
        with self.assertRaises(hardware_baseline.HardwareBaselineError):
            hardware_baseline.compute_star_schedule(['n1', 'n2'], 'not-a-node')


class SanitizeNodeIdTest(unittest.TestCase):
    """Tests for :func:`bexhoma.hardware_baseline._sanitize_node_id`."""

    def test_lowercases_and_replaces_invalid_characters(self) -> None:
        self.assertEqual(
            hardware_baseline._sanitize_node_id('Node_01.cluster.LOCAL'), 'node-01-cluster-loca')

    def test_truncates_to_max_length(self) -> None:
        result = hardware_baseline._sanitize_node_id('a' * 40)
        self.assertLessEqual(len(result), hardware_baseline._MAX_NODE_ID_LENGTH)

    def test_strips_leading_and_trailing_dashes(self) -> None:
        self.assertEqual(hardware_baseline._sanitize_node_id('--node--'), 'node')


class BuildParsedArgsTest(unittest.TestCase):
    """Tests for :func:`bexhoma.hardware_baseline._build_parsed_args`."""

    def test_overrides_expected_fields(self) -> None:
        args = hardware_baseline._build_parsed_args(timeout_minutes=7, hardware_duration=20)
        self.assertEqual(args.mode, 'run')
        self.assertEqual(args.dbms, ['Hardware'])
        self.assertIsNone(args.request_storage_type)
        self.assertEqual(args.multi_tenant_by, 'container')
        self.assertEqual(args.experiment_timeout, 7)
        self.assertFalse(args.monitoring)
        self.assertFalse(args.monitoring_cluster)
        self.assertFalse(args.monitoring_app)
        self.assertEqual(args.hardware_duration, 20)

    def test_base_parser_defaults_survive_untouched_fields(self) -> None:
        """Fields this feature doesn't override keep make_base_parser()'s own defaults."""
        args = hardware_baseline._build_parsed_args(timeout_minutes=None, hardware_duration=15)
        self.assertEqual(args.timeout, 600)
        self.assertEqual(args.sets, [])
        self.assertIsNone(args.experiment_timeout)


class RunHardwareBaselineSetupTest(unittest.TestCase):
    """Exercises :func:`run_hardware_baseline` up to (not including)
    ``experiment.process()``, against a stub cluster."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.stub_cluster = _HardwareStubCluster(resultfolder=self.tmp_dir.name)
        self.captured_experiment = None

        def _capture_and_noop(experiment_self) -> None:
            self.captured_experiment = experiment_self

        process_patch = mock.patch.object(HardwareExperiment, 'process', _capture_and_noop)
        remove_patch = mock.patch.object(HardwareExperiment, 'remove_experiment', lambda self: None)
        process_patch.start()
        remove_patch.start()
        self.addCleanup(process_patch.stop)
        self.addCleanup(remove_patch.stop)

    def _run(self, nodes, **kwargs):
        return hardware_baseline.run_hardware_baseline(self.stub_cluster, nodes, **kwargs)

    def test_one_configuration_per_node(self) -> None:
        self._run(['n1', 'n2', 'n3'], network_topology='none')
        self.assertEqual(len(self.captured_experiment.configurations), 3)

    def test_each_configuration_pinned_to_its_own_node(self) -> None:
        self._run(['n1', 'n2'], network_topology='none')
        for config in self.captured_experiment.configurations:
            node = config.alias
            self.assertEqual(config.resources['nodeSelector']['kubernetes.io/hostname'], node)
            self.assertIn(f'kubernetes.io/hostname: {node}', config.benchmarking_patch)

    def test_baseline_only_gives_two_rounds_per_configuration(self) -> None:
        self._run(['n1', 'n2'], network_topology='none')
        for config in self.captured_experiment.configurations:
            self.assertEqual(config.benchmark_list_template, [1, 1])

    def test_star_topology_gives_three_rounds_including_the_hubs_self_test(self) -> None:
        self._run(['n1', 'n2', 'n3'], network_topology='star', hub='n1')
        for config in self.captured_experiment.configurations:
            self.assertEqual(config.benchmark_list_template, [1, 1, 1])

    def test_full_topology_round_count_matches_schedule(self) -> None:
        self._run(['n1', 'n2', 'n3', 'n4'], network_topology='full')
        # 4 nodes -> 3 round-robin rounds, plus the 2 baseline rounds
        for config in self.captured_experiment.configurations:
            self.assertEqual(config.benchmark_list_template, [1, 1, 1, 1, 1])

    def test_network_round_overrides_bexhoma_host_to_targets_own_service(self) -> None:
        self._run(['n1', 'n2', 'n3'], network_topology='star', hub='n1')
        configs_by_alias = {config.alias: config for config in self.captured_experiment.configurations}
        spoke, hub = configs_by_alias['n2'], configs_by_alias['n1']
        # round index 2 (0-based): sysbench, fio, then the network round
        network_round_params = spoke.benchmarking_parameters_list[2]
        self.assertEqual(network_round_params['HARDWARE_TYPE'], 'sockperf')
        self.assertEqual(network_round_params['BEXHOMA_HOST'], hub.get_service_sut(hub.configuration))

    def test_hub_network_round_is_a_self_test_with_no_host_override(self) -> None:
        self._run(['n1', 'n2', 'n3'], network_topology='star', hub='n1')
        configs_by_alias = {config.alias: config for config in self.captured_experiment.configurations}
        hub_network_round_params = configs_by_alias['n1'].benchmarking_parameters_list[2]
        self.assertEqual(hub_network_round_params['HARDWARE_TYPE'], 'sysbench')
        self.assertNotIn('BEXHOMA_HOST', hub_network_round_params)

    def test_baseline_rounds_target_the_nodes_own_sut(self) -> None:
        self._run(['n1', 'n2'], network_topology='none')
        for config in self.captured_experiment.configurations:
            cpu_round, fio_round = config.benchmarking_parameters_list[:2]
            self.assertEqual(cpu_round['HARDWARE_TYPE'], 'sysbench')
            self.assertEqual(fio_round['HARDWARE_TYPE'], 'fio')
            self.assertNotIn('BEXHOMA_HOST', cpu_round)
            self.assertNotIn('BEXHOMA_HOST', fio_round)

    def test_no_schedulable_nodes_raises(self) -> None:
        with self.assertRaises(hardware_baseline.HardwareBaselineError):
            self._run([])

    def test_invalid_topology_raises(self) -> None:
        with self.assertRaises(hardware_baseline.HardwareBaselineError):
            self._run(['n1'], network_topology='bogus')


class _FakeHardwareEvaluator:
    """Stands in for :class:`bexhoma.evaluators.hardware.HardwareEvaluator`,
    returning a pre-built already-aggregated DataFrame directly instead of
    reading log files off disk -- ``_collect_results`` only cares about the
    evaluator's public shape (``get_df_benchmarking``/
    ``benchmarking_set_datatypes``/``benchmarking_aggregate_by_parallel_pods``),
    not how it got there."""

    def __init__(self, df_aggregated: pd.DataFrame) -> None:
        self._df_aggregated = df_aggregated

    def get_df_benchmarking(self) -> pd.DataFrame:
        return pd.DataFrame({'placeholder': [1]})  # only emptiness is checked; content is unused

    def benchmarking_set_datatypes(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def benchmarking_aggregate_by_parallel_pods(self, df: pd.DataFrame, columns=None) -> pd.DataFrame:
        del df, columns
        return self._df_aggregated


def _fake_experiment(df_aggregated: pd.DataFrame) -> SimpleNamespace:
    """Minimal experiment stand-in exposing only ``benchmarks[0].evaluator``,
    the one attribute :func:`_collect_results` reads off ``experiment``."""
    evaluator = _FakeHardwareEvaluator(df_aggregated)
    return SimpleNamespace(benchmarks=[SimpleNamespace(evaluator=evaluator)])


class CollectResultsTest(unittest.TestCase):
    """Tests for :func:`bexhoma.hardware_baseline._collect_results`.

    Exercises the ``client``-column round-index convention directly against
    realistic (1-indexed -- see ``hardware_baseline._CPU_BASELINE_ROUND``'s
    comment) values, matching what a real run's pickled results actually
    contain (verified 2026-07-31 against a 16-node cluster run: every
    completed round logged ``client == 1``, ``hardware_type == 'sysbench'``).
    """

    def _collect(self, df_aggregated: pd.DataFrame, configs_by_node: dict, network_targets: dict) -> hardware_baseline.HardwareBaselineResult:
        result = hardware_baseline.HardwareBaselineResult(code='test-code')
        hardware_baseline._collect_results(
            cluster=None, experiment=_fake_experiment(df_aggregated),
            configs_by_node=configs_by_node, network_targets=network_targets, result=result)
        return result

    def test_cpu_baseline_round_is_client_one(self) -> None:
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 1, 'hardware_type': 'sysbench', 'value': 111},
        ])
        configs_by_node = {'n1': SimpleNamespace(configuration='hw-n1')}
        result = self._collect(df, configs_by_node, {'n1': []})
        self.assertEqual(result.per_node['n1']['cpu_mem']['value'], 111)

    def test_fio_baseline_round_is_client_two(self) -> None:
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 2, 'hardware_type': 'fio', 'value': 222},
        ])
        configs_by_node = {'n1': SimpleNamespace(configuration='hw-n1')}
        result = self._collect(df, configs_by_node, {'n1': []})
        self.assertEqual(result.per_node['n1']['fio']['value'], 222)

    def test_both_baseline_rounds_together(self) -> None:
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 1, 'hardware_type': 'sysbench', 'value': 111},
            {'configuration': 'hw-n1', 'client': 2, 'hardware_type': 'fio', 'value': 222},
        ])
        configs_by_node = {'n1': SimpleNamespace(configuration='hw-n1')}
        result = self._collect(df, configs_by_node, {'n1': []})
        self.assertEqual(result.per_node['n1']['cpu_mem']['value'], 111)
        self.assertEqual(result.per_node['n1']['fio']['value'], 222)

    def test_network_round_starts_at_client_three_and_resolves_target_by_schedule(self) -> None:
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 1, 'hardware_type': 'sysbench', 'value': 1},
            {'configuration': 'hw-n1', 'client': 2, 'hardware_type': 'fio', 'value': 2},
            {'configuration': 'hw-n1', 'client': 3, 'hardware_type': 'sockperf', 'value': 3},
        ])
        configs_by_node = {
            'n1': SimpleNamespace(configuration='hw-n1'),
            'n2': SimpleNamespace(configuration='hw-n2'),
        }
        result = self._collect(df, configs_by_node, {'n1': ['n2'], 'n2': ['n1']})
        self.assertEqual(result.network_matrix['n1->n2']['value'], 3)

    def test_bye_round_within_network_schedule_is_not_recorded_as_a_pair(self) -> None:
        """A self-test filler round (hardware_type sysbench, at a network-round
        client index) must not be mistaken for the primary cpu_mem round nor
        turned into a network_matrix entry."""
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 1, 'hardware_type': 'sysbench', 'value': 1},
            {'configuration': 'hw-n1', 'client': 2, 'hardware_type': 'fio', 'value': 2},
            {'configuration': 'hw-n1', 'client': 3, 'hardware_type': 'sysbench', 'value': 999},
        ])
        configs_by_node = {'n1': SimpleNamespace(configuration='hw-n1')}
        # network_targets[node][0] is None: this node's only network round was a bye
        result = self._collect(df, configs_by_node, {'n1': [None]})
        self.assertEqual(result.per_node['n1']['cpu_mem']['value'], 1)
        self.assertEqual(result.network_matrix, {})

    def test_unrecognized_configuration_is_skipped_not_erroring(self) -> None:
        df = pd.DataFrame([
            {'configuration': 'not-one-of-ours', 'client': 1, 'hardware_type': 'sysbench', 'value': 1},
        ])
        result = self._collect(df, configs_by_node={}, network_targets={})
        self.assertEqual(result.per_node, {})
        self.assertEqual(result.network_matrix, {})

    def test_empty_dataframe_leaves_result_empty(self) -> None:
        result = self._collect(pd.DataFrame(), configs_by_node={}, network_targets={})
        self.assertEqual(result.per_node, {})
        self.assertEqual(result.network_matrix, {})


if __name__ == '__main__':
    unittest.main()
