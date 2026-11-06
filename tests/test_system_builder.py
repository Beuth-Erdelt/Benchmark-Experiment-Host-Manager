"""
Tests for :mod:`bexhoma.experiments.system_builder` and the placeholder expansion of the
descriptors (:func:`bexhoma.system_descriptors.expand`).

The configurations the entry scripts build with it are covered by ``test_dbms_snapshots``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import types
import unittest

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


if __name__ == '__main__':
    unittest.main()
