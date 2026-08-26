"""
Tests for the concurrent-SUT caps (``max_sut`` / ``max_sut_experiment``).

The catalog contract's default benchmarking situation is one
system-under-test at a time (see ``catalog_concepts.sut_isolation``). Because
``tpch.py``'s own ``-ms``/``-mse`` CLI defaults are "no limit", the default
of 1 has to be applied by the argv builder, not inherited. This covers:

* ``bexhoma/experiments/tpch_catalog.py::build_tpch_argv``: ``-ms``/``-mse``
  are always emitted -- an absent field becomes ``-ms 1``/``-mse 1``; a
  field set to 0 ("no limit") drops the flag so ``tpch.py`` inherits its own
  no-limit default; an explicit N is passed through;
* ``bexhoma/spec.py::validate_experiment``: a negative or non-integer cap
  is rejected before any argv is built.

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
    'hypothesis': 'the caps reach tpch.py with the contract default of 1',
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


class MaxSutArgvEmissionTest(unittest.TestCase):
    """``build_tpch_argv`` applies the contract's default-1 SUT isolation."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _argv(self, **overrides):
        spec = copy.deepcopy(_BASE_SPEC)
        spec.update(overrides)
        return catalog_spec.build_argv(self.catalog, spec)

    def test_absent_fields_emit_the_default_of_one(self):
        argv = self._argv()
        self.assertEqual(_flag_value(argv, '-ms'), '1')
        self.assertEqual(_flag_value(argv, '-mse'), '1')

    def test_zero_means_no_limit_and_drops_the_flag(self):
        argv = self._argv(max_sut=0)
        self.assertNotIn('-ms', argv)
        self.assertEqual(_flag_value(argv, '-mse'), '1')  # the other cap is untouched

    def test_explicit_values_pass_through(self):
        argv = self._argv(max_sut=3, max_sut_experiment=2)
        self.assertEqual(_flag_value(argv, '-ms'), '3')
        self.assertEqual(_flag_value(argv, '-mse'), '2')

    def test_emitted_argv_parses_back_through_tpch(self):
        argv = self._argv(max_sut=5)
        args = tpch.build_parser().parse_args(argv)
        self.assertEqual(args.max_sut, '5')
        self.assertEqual(args.max_sut_experiment, '1')


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
