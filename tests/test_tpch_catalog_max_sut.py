"""
Tests for the concurrent-SUT caps (``max_sut`` / ``max_sut_experiment``).

The default benchmarking situation is one system-under-test at a time (see
``catalog_concepts.sut_isolation``). This covers:

* ``bexhoma/cli_args.py``: both ``-ms`` and ``-mse`` default to 1, and ``0``
  is normalised to ``None`` ("no limit") so the entry scripts' existing
  ``is not None`` guards leave the cap unset;
* ``bexhoma/experiments/tpch_catalog.py::build_tpch_argv``: the caps are
  emitted only when the experiment.yml actually sets them, and ``0`` is
  passed through verbatim;
* ``bexhoma/spec.py::validate_experiment``: a negative or non-integer cap
  is rejected.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import unittest

import tpch
from bexhoma import spec as catalog_spec

_CATALOG_FILE = 'contracts/contract_catalog.yml'

_BASE_SPEC = {
    'mode': 'run',
    'title': 'concurrent-SUT cap test',
    'hypothesis': 'the caps reach tpch.py only when set',
    'discriminates': ['system'],
    'workload': {'name': 'tpch', 'params': {'scaling_factor': 10}, 'rounds': [1], 'repetitions': 1},
    'loading': {'pods': 1, 'threads': 1},
    'systems': [{'name': 'PostgreSQL', 'profile': 'analytical-ssd'}],
    'placement': {'sut': 'cl-worker36'},
    'resources': {
        'cpu': {'request': 16, 'limit': 16},
        'memory': {'request': '64G', 'limit': '64G'},
        'storage': {'size': '50Gi'},
    },
}


def _flag_value(argv, flag):
    """The token right after ``flag`` in ``argv``, or ``None`` when absent."""
    return argv[argv.index(flag) + 1] if flag in argv else None


class MaxSutCliDefaultTest(unittest.TestCase):
    """``-ms``/``-mse`` default to 1; ``0`` means "no limit" (``None``)."""

    def _parse(self, extra):
        return tpch.build_parser().parse_args(['run', '-dbms', 'PostgreSQL', *extra])

    def test_both_caps_default_to_one(self):
        args = self._parse([])
        self.assertEqual(args.max_sut, 1)
        self.assertEqual(args.max_sut_experiment, 1)

    def test_zero_is_normalised_to_no_limit(self):
        args = self._parse(['-ms', '0', '-mse', '0'])
        self.assertIsNone(args.max_sut)
        self.assertIsNone(args.max_sut_experiment)

    def test_positive_value_passes_through(self):
        args = self._parse(['-ms', '4', '-mse', '2'])
        self.assertEqual(args.max_sut, 4)
        self.assertEqual(args.max_sut_experiment, 2)

    def test_non_integer_is_rejected(self):
        with self.assertRaises(SystemExit):
            self._parse(['-ms', 'lots'])


class MaxSutArgvEmissionTest(unittest.TestCase):
    """``build_tpch_argv`` emits ``-ms``/``-mse`` only when the spec sets them."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _argv(self, **overrides):
        spec = copy.deepcopy(_BASE_SPEC)
        spec.update(overrides)
        return catalog_spec.build_argv(self.catalog, spec)

    def test_absent_fields_emit_nothing(self):
        argv = self._argv()
        self.assertNotIn('-ms', argv)
        self.assertNotIn('-mse', argv)

    def test_zero_is_emitted_verbatim(self):
        argv = self._argv(max_sut=0)
        self.assertEqual(_flag_value(argv, '-ms'), '0')
        self.assertNotIn('-mse', argv)

    def test_both_caps_emitted_when_set(self):
        argv = self._argv(max_sut=3, max_sut_experiment=2)
        self.assertEqual(_flag_value(argv, '-ms'), '3')
        self.assertEqual(_flag_value(argv, '-mse'), '2')

    def test_emitted_value_survives_a_round_trip_through_tpch_parser(self):
        argv = self._argv(max_sut=0, max_sut_experiment=5)
        args = tpch.build_parser().parse_args(argv)
        self.assertIsNone(args.max_sut)          # 0 -> no limit
        self.assertEqual(args.max_sut_experiment, 5)


class MaxSutValidationTest(unittest.TestCase):
    """A negative or non-integer cap fails validation before any argv is built."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _build(self, **overrides):
        spec = copy.deepcopy(_BASE_SPEC)
        spec.update(overrides)
        return catalog_spec.build_argv(self.catalog, spec)

    def test_negative_cap_rejected(self):
        with self.assertRaises(catalog_spec.SpecError):
            self._build(max_sut=-1)

    def test_non_integer_cap_rejected(self):
        with self.assertRaises(catalog_spec.SpecError):
            self._build(max_sut_experiment='two')

    def test_bool_cap_rejected(self):
        with self.assertRaises(catalog_spec.SpecError):
            self._build(max_sut=True)

    def test_zero_and_positive_caps_accepted(self):
        self._build(max_sut=0, max_sut_experiment=4)  # must not raise


if __name__ == '__main__':
    unittest.main()
