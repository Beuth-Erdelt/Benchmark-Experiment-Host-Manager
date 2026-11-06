"""
Tests for :mod:`bexhoma.experiments.system_builder` and the placeholder expansion of the
descriptors (:func:`bexhoma.system_descriptors.expand`).

The configurations the entry scripts build with it are covered by ``test_dbms_snapshots``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import types
import unittest

import tpch

from bexhoma import system_descriptors as sd
from bexhoma.experiments import system_builder as builder


def _dockers() -> dict:
    return {
        'B': {'benchmarks': {'x': {'default': True}, 'y': {}}},
        'A': {'benchmarks': {'x': {}, 'y': {'default': True}}},
        'C': {'benchmarks': {'x': {'default': True}}},
        'D': {'benchmarks': {'y': {}}},
    }


class ExpandTest(unittest.TestCase):

    context = {'n': 3, 'name': 'abc', 'flag': True}

    def test_a_whole_placeholder_keeps_the_type(self) -> None:
        self.assertEqual(sd.expand('{n}', self.context), 3)
        self.assertIs(sd.expand('{flag}', self.context), True)

    def test_mixed_text_is_formatted(self) -> None:
        self.assertEqual(sd.expand('{name}-{n}', self.context), 'abc-3')
        self.assertEqual(sd.expand('no placeholder', self.context), 'no placeholder')

    def test_containers_are_expanded_recursively(self) -> None:
        self.assertEqual(sd.expand({'a': ['{n}', 'x{n}'], 'b': {'c': '{name}'}, 'd': 5}, self.context),
                         {'a': [3, 'x3'], 'b': {'c': 'abc'}, 'd': 5})

    def test_reset_script_names_follow_the_benchmark_context(self) -> None:
        scripts = ['reset-ssb{schema_suffix}.sql', 'reset-flush.sh']
        self.assertEqual(sd.expand(scripts, {'schema_suffix': ''}), ['reset-ssb.sql', 'reset-flush.sh'])
        self.assertEqual(sd.expand(scripts, {'schema_suffix': '-flat'}), ['reset-ssb-flat.sql', 'reset-flush.sh'])

    def test_unknown_placeholder_raises(self) -> None:
        with self.assertRaises(KeyError):
            sd.expand('{missing}', self.context)


class SelectionTest(unittest.TestCase):

    def test_default_set_in_config_order(self) -> None:
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', []), ['B', 'C'])
        self.assertEqual(builder.selected_dockers(_dockers(), 'y', None), ['A'])

    def test_named_dbms_in_config_order_not_argument_order(self) -> None:
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', ['C', 'A']), ['A', 'C'])

    def test_incompatible_dbms_is_refused(self) -> None:
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, r"D is not compatible with benchmark 'x'"):
            builder.selected_dockers(_dockers(), 'x', ['B', 'D'])


class ContextTest(unittest.TestCase):

    def test_worker_counts_are_integers(self) -> None:
        args = types.SimpleNamespace(num_worker='2', num_worker_replicas=1, num_worker_shards='3', other='x')
        context = builder.context_of(args)
        self.assertEqual((context['num_worker'], context['num_worker_replicas'], context['num_worker_shards']), (2, 1, 3))
        self.assertEqual(context['other'], 'x')

    def test_entry_parameters_are_expanded(self) -> None:
        dockers = {'A': {'benchmarks': {'x': {'sut_parameters': {'N': '{num_worker}', 'T': 'fixed'}}}}}
        args = types.SimpleNamespace(num_worker='2')
        self.assertEqual(builder.entry_parameters(dockers, 'A', 'x', 'sut_parameters', args), {'N': 2, 'T': 'fixed'})
        self.assertEqual(builder.entry_parameters(dockers, 'A', 'x', 'eval_parameters', args), {})


class LoadingPodsTest(unittest.TestCase):

    def test_no_limit(self) -> None:
        self.assertEqual(builder.limit_loading_pods({}, 'A', 4, 2), (4, 2))

    def test_within_the_limit(self) -> None:
        self.assertEqual(builder.limit_loading_pods({'max_loading_pods': 2}, 'A', 2, 1), (2, 1))

    def test_capped_with_a_message(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(builder.limit_loading_pods({'max_loading_pods': 1}, 'A', 4, 2), (1, 1))
        self.assertEqual(out.getvalue().strip(), 'A: loads with 1 pod, ignoring -nlp 4')

    def test_parallel_only_capped_without_a_message(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(builder.limit_loading_pods({'max_loading_pods': 1}, 'A', 1, 3), (1, 1))
        self.assertEqual(out.getvalue(), '')


class LoadingVariantsTest(unittest.TestCase):

    def test_one_without_declaration(self) -> None:
        self.assertEqual(builder.loading_variants({}, [1, 8]), [{}])

    def test_one_per_thread_count(self) -> None:
        entry = {'per_loading_threads': {'T': '{threads}', 'P': 1}}
        self.assertEqual(builder.loading_variants(entry, [1, '8']), [{'T': 1, 'P': 1}, {'T': 8, 'P': 1}])


class TenantTest(unittest.TestCase):
    """The multi-tenant variants of tpch.py, for a DBMS that declares ``multi_tenancy``."""

    entry = {'multi_tenancy': True}

    def experiment(self, by: str, number: int = 2):
        return types.SimpleNamespace(tenant_per=by, num_tenants=number)

    def test_a_dbms_without_the_flag_has_no_tenants(self) -> None:
        experiment = self.experiment('container')
        self.assertEqual(tpch.tenant_ids(experiment, {}), [None])
        self.assertEqual(tpch.tenant_parameters(experiment, {}, None, 'p'), {})

    def test_container_tenancy_is_one_configuration_per_tenant(self) -> None:
        experiment = self.experiment('container', 3)
        self.assertEqual(tpch.tenant_ids(experiment, self.entry), [0, 1, 2])
        result = tpch.tenant_parameters(experiment, self.entry, 1, 'p')
        self.assertEqual(result['storage'], 'p-1-3')
        self.assertEqual(result['loading'], {'BEXHOMA_TENANT_BY': 'container', 'BEXHOMA_TENANT_NUM': 3, 'BEXHOMA_TENANT_ID': 1})
        self.assertEqual(result['eval'], {'TENANT_BY': 'container', 'TENANT_NUM': 3, 'TENANT': 1})
        self.assertNotIn('experiment', result)

    def test_schema_tenancy_switches_scripts(self) -> None:
        experiment = self.experiment('schema')
        self.assertEqual(tpch.tenant_ids(experiment, self.entry), [None])
        result = tpch.tenant_parameters(experiment, self.entry, None, 'p')
        self.assertEqual(result['storage'], 'p-schema-2')
        self.assertEqual(result['experiment']['script'], 'Schema_tenant')
        self.assertEqual(result['benchmarking']['BEXHOMA_TENANT_ID'], 0)

    def test_no_tenancy_keeps_the_storage_but_still_sets_the_parameters(self) -> None:
        result = tpch.tenant_parameters(self.experiment('', 0), self.entry, None, 'p')
        self.assertNotIn('storage', result)
        self.assertEqual(result['loading']['BEXHOMA_TENANT_BY'], '')
        self.assertEqual(result['eval'], {'TENANT_BY': '', 'TENANT_NUM': 0})


if __name__ == '__main__':
    unittest.main()
