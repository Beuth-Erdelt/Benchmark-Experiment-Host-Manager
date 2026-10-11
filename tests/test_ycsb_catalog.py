"""
Tests for the ``ycsb`` half of the catalog-contract translator.

``bexhoma/spec.py::build_argv`` dispatches a ``workload.name == 'ycsb'``
experiment.yml to :func:`bexhoma.experiments.ycsb_catalog.build_ycsb_argv`,
which turns it into a ``ycsb.py`` argument vector. These tests check that:

* the emitted argv parses back cleanly through ``ycsb.build_parser()``;
* catalog params/loading/rounds/observe/placement/resources map to the right
  ``ycsb.py`` flags;
* the contract's default-1 SUT isolation is applied (``-mse``), same
  as the tpch builder;
* a profile's resolved knobs become ``--set`` deployment patches;
* a resources: sweep becomes comma lists with per-cell scoped knobs;
* an unsupported system is rejected.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import unittest

import ycsb
from bexhoma import spec as catalog_spec

_CATALOG_FILE = 'contracts/contract_catalog.yml'

_BASE_SPEC = {
    'mode': 'run',
    'title': 'YCSB workload A on PostgreSQL',
    'hypothesis': 'baseline throughput scales with concurrent clients',
    'discriminates': ['concurrency'],
    'workload': {
        'name': 'ycsb',
        'params': {
            'workload': 'a',
            'scaling_factor': 1,
            'operations_scale': 5,
            'target_base': 0,
            'logging_interval': 10,
            'insert_order': 'hashed',
        },
        'rounds': [1, 2, 4],
        'repetitions': 3,
    },
    'loading': {'pods': 1, 'threads': 8},
    'systems': [{'name': 'PostgreSQL'}],
    'observe': {'monitoring_sut': True, 'metrics': ['total_cpu_util']},
    'placement': {'sut': 'cl-worker36', 'loading': 'cl-worker19'},
    'resources': {
        'cpu': {'request': 8, 'limit': 8},
        'memory': {'request': '32Gi', 'limit': '32Gi'},
        'storage': {'size': '50Gi'},
    },
}


def _flag_value(argv, flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


class BuildYcsbArgvTest(unittest.TestCase):
    """``build_ycsb_argv`` maps the catalog spec onto ``ycsb.py`` flags."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _argv(self, **overrides):
        spec = copy.deepcopy(_BASE_SPEC)
        spec.update(overrides)
        return catalog_spec.build_argv(self.catalog, spec)

    def test_argv_parses_back_through_ycsb(self):
        args = ycsb.build_parser().parse_args(self._argv())
        self.assertEqual(args.mode, 'run')
        self.assertEqual(args.dbms, ['PostgreSQL'])
        self.assertEqual(args.scaling_factor, '1')
        self.assertEqual(args.scaling_factor_operations, '5')
        self.assertEqual(args.workload, 'a')
        self.assertEqual(args.target_base, '0')
        self.assertEqual(args.num_query_executors, '1,2,4')
        self.assertEqual(args.num_config, '3')
        self.assertEqual(args.num_loading_pods, '1')
        self.assertEqual(args.num_loading_threads, '8')

    def test_benchmarking_pods_and_threads_are_optional(self):
        args = ycsb.build_parser().parse_args(self._argv())
        self.assertEqual(args.num_benchmarking_pods, '1')
        self.assertEqual(args.num_benchmarking_threads, '1')

    def test_benchmarking_pods_and_threads_map_to_nbp_nbt(self):
        argv = self._argv(benchmarking={'pods': 4, 'threads': 128})
        args = ycsb.build_parser().parse_args(argv)
        self.assertEqual(args.num_benchmarking_pods, '4')
        self.assertEqual(args.num_benchmarking_threads, '128')

    def test_reset_between_rounds_is_always_activated(self):
        """Skipping the CHECKPOINT/VACUUM ANALYZE reset is never a valid choice."""
        args = ycsb.build_parser().parse_args(self._argv())
        self.assertTrue(args.activate_reset)

    def test_loading_timeout_is_translated(self):
        argv = self._argv(loading={'pods': 1, 'threads': 8, 'timeout_minutes': 15})
        args = ycsb.build_parser().parse_args(argv)
        self.assertEqual(args.loading_timeout, 15)

    def test_loading_timeout_is_optional(self):
        args = ycsb.build_parser().parse_args(self._argv())
        self.assertIsNone(args.loading_timeout)

    def test_verify_result_is_off_by_default(self):
        args = ycsb.build_parser().parse_args(self._argv())
        self.assertFalse(args.test_result)

    def test_verify_result_maps_to_tr(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['workload']['params']['verify_result'] = True
        argv = catalog_spec.build_argv(self.catalog, spec)
        args = ycsb.build_parser().parse_args(argv)
        self.assertTrue(args.test_result)

    def test_observe_and_placement_and_resources(self):
        argv = self._argv()
        self.assertIn('-m', argv)
        self.assertEqual(_flag_value(argv, '-rnn'), 'cl-worker36')
        self.assertEqual(_flag_value(argv, '-rnl'), 'cl-worker19')
        self.assertEqual(_flag_value(argv, '-rc'), '8')
        self.assertEqual(_flag_value(argv, '-lr'), '32Gi')
        self.assertEqual(_flag_value(argv, '-rss'), '50Gi')

    def test_default_sut_isolation_cap_emitted(self):
        argv = self._argv()
        self.assertNotIn('-ms', argv)
        self.assertEqual(_flag_value(argv, '-mse'), '1')

    def test_zero_cap_drops_the_flag(self):
        argv = self._argv(max_sut=0)
        self.assertNotIn('-ms', argv)
        self.assertEqual(_flag_value(argv, '-mse'), '1')

    def test_profile_knobs_become_set_patches(self):
        argv = self._argv(systems=[{'name': 'PostgreSQL', 'profile': 'analytical-ssd'}])
        set_patches = [argv[i + 1] for i, tok in enumerate(argv) if tok == '--set']
        self.assertTrue(any('.container[dbms].shared_buffers=' in p for p in set_patches))
        self.assertTrue(all(p.startswith('deployment[bexhoma-deployment-postgres]') for p in set_patches))

    def test_unsupported_system_rejected(self):
        with self.assertRaises(catalog_spec.SpecError):
            self._argv(systems=[{'name': 'Redis'}])

    def test_memory_sweep_becomes_comma_lists(self):
        argv = self._argv(resources={
            'cpu': {'request': 8, 'limit': 8},
            'memory': [
                {'request': '32Gi', 'limit': '32Gi'},
                {'request': '16Gi', 'limit': '16Gi'},
            ],
        })
        args = ycsb.build_parser().parse_args(argv)
        self.assertEqual(args.request_ram, '32Gi,16Gi')
        self.assertEqual(args.limit_ram, '32Gi,16Gi')
        self.assertEqual(args.request_cpu, '8,8')

    def test_sweep_scopes_derived_knobs_per_cell(self):
        argv = self._argv(
            systems=[{'name': 'PostgreSQL', 'profile': 'analytical-ssd'}],
            resources={
                'cpu': {'request': 8, 'limit': 8},
                'memory': [
                    {'request': '32Gi', 'limit': '32Gi'},
                    {'request': '16Gi', 'limit': '16Gi'},
                ],
            })
        shared_buffers = {
            patch.split('.container')[0].split('@')[1]: patch.split('=')[1]
            for i, token in enumerate(argv) if token == '--set'
            for patch in [argv[i + 1]] if '.shared_buffers=' in patch
        }
        self.assertEqual(sorted(shared_buffers), ['PostgreSQL-1', 'PostgreSQL-2'])
        self.assertNotEqual(shared_buffers['PostgreSQL-1'], shared_buffers['PostgreSQL-2'])

    def test_storage_sweep_becomes_a_comma_list(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['resources']['storage_class'] = ['cephcsi', None]
        argv = catalog_spec.build_argv(self.catalog, spec)
        self.assertEqual(_flag_value(argv, '-rst'), 'cephcsi,')
        self.assertIn('-rsr', argv)

    def test_sweep_lists_of_different_lengths_are_rejected(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['resources']['memory'] = [{'request': '8Gi', 'limit': '8Gi'}, {'request': '16Gi', 'limit': '16Gi'}]
        spec['resources']['storage_class'] = ['cephcsi', 'shared', None]
        with self.assertRaisesRegex(catalog_spec.SpecError, 'must share one length'):
            catalog_spec.build_argv(self.catalog, spec)

    def test_sweep_with_several_loading_target_factors_is_rejected(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['workload']['params']['loading_target_factors'] = [1, 2]
        spec['resources']['memory'] = [{'request': '8Gi', 'limit': '8Gi'}, {'request': '16Gi', 'limit': '16Gi'}]
        with self.assertRaisesRegex(catalog_spec.SpecError, 'loading_target_factors'):
            catalog_spec.build_argv(self.catalog, spec)

    def test_optional_blocks_may_be_absent(self):
        spec = copy.deepcopy(_BASE_SPEC)
        del spec['observe']
        del spec['placement']
        del spec['resources']
        argv = catalog_spec.build_argv(self.catalog, spec)
        args = ycsb.build_parser().parse_args(argv)  # must not raise
        self.assertEqual(args.workload, 'a')


if __name__ == '__main__':
    unittest.main()
