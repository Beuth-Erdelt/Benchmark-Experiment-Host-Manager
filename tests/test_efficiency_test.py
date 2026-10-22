"""Tests for the TPC-C efficiency TEST line of Benchbase and HammerDB experiments.

Efficiency is only computed with key-and-think time and terminals/vusers = 10 x SF;
everywhere else it is 0 by design, so the test is skipped instead of failed.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from types import SimpleNamespace
import unittest

import pandas as pd

from bexhoma.evaluators.base import EvaluatorBase
from bexhoma.evaluators.benchbase import BenchbaseEvaluator
from bexhoma.evaluators.tpcc import TpccEvaluator
from bexhoma.experiments.base import ExperimentBase

__all__ = []


def _experiment(sf=4, benchmark_type='tpcc', **parameters):
    """Bare stand-in with the ExperimentBase test helpers bound to it."""
    exp = SimpleNamespace(SF=sf, benchmark_type=benchmark_type, _test_results=[],
                          default_benchmarking_parameters=parameters)
    exp.evaluator = SimpleNamespace(test_results_column=lambda df, col: EvaluatorBase.test_results_column(None, df, col))
    for name in ('_record_test', '_record_skipped_test', '_test_column', '_test_efficiency'):
        setattr(exp, name, getattr(ExperimentBase, name).__get__(exp))
    exp.benchmarking_is_active = lambda: True
    exp.test_workflow = lambda actual, planned: True
    return exp


def _labels(exp, prefix='efficiency'):
    return [(passed, label) for passed, label in exp._test_results if label.startswith(prefix)]


class EfficiencyTestHelperTest(unittest.TestCase):
    """ExperimentBase._test_efficiency skips where efficiency is 0 by design."""

    def test_not_computed_is_skipped(self):
        exp = _experiment()
        df = pd.DataFrame({'terminals': [40], 'efficiency': [0.0]})
        exp._test_efficiency(df, 'terminals', computed=False, reason="needs key-and-think time (-xkey)")
        self.assertEqual(_labels(exp), [(None, "efficiency (not computed: needs key-and-think time (-xkey))")])

    def test_no_phase_with_ten_times_sf_is_skipped(self):
        exp = _experiment(sf=4)
        df = pd.DataFrame({'vusers': [4, 8], 'efficiency': [0.0, 0.0]})
        exp._test_efficiency(df, 'vusers', computed=True, reason='')
        self.assertEqual(_labels(exp), [(None, "efficiency (not computed: no phase with vusers = 10 x SF = 40)")])

    def test_only_eligible_phases_are_tested(self):
        exp = _experiment(sf=4)
        df = pd.DataFrame({'terminals': [40, 8], 'efficiency': [87.5, 0.0]})
        exp._test_efficiency(df, 'terminals', computed=True, reason='')
        self.assertEqual(_labels(exp), [(True, "efficiency contains no 0 or NaN")])

    def test_zero_in_eligible_phase_fails(self):
        exp = _experiment(sf=4)
        df = pd.DataFrame({'terminals': [40], 'efficiency': [0.0]})
        exp._test_efficiency(df, 'terminals', computed=True, reason='')
        self.assertEqual(_labels(exp), [(False, "efficiency contains 0 or NaN")])


class EvaluatorRecordTestsTest(unittest.TestCase):
    """Benchbase and HammerDB record_tests decide from key-and-think and the benchmark."""

    def test_benchbase_without_keying_skips(self):
        exp = _experiment(BENCHBASE_KEY_AND_THINK="false")
        df = pd.DataFrame({'terminals': [40], 'Throughput (requests/second)': [1024.0], 'efficiency': [0.0]})
        BenchbaseEvaluator.record_tests(None, exp, pd.DataFrame(), df, {}, {})
        self.assertEqual(_labels(exp)[0][0], None)

    def test_benchbase_twitter_with_keying_skips(self):
        exp = _experiment(benchmark_type='twitter', BENCHBASE_KEY_AND_THINK="true")
        df = pd.DataFrame({'terminals': [40], 'Throughput (requests/second)': [1024.0], 'efficiency': [0.0]})
        BenchbaseEvaluator.record_tests(None, exp, pd.DataFrame(), df, {}, {})
        self.assertEqual(_labels(exp)[0][0], None)

    def test_benchbase_tpcc_with_keying_tests(self):
        exp = _experiment(BENCHBASE_KEY_AND_THINK="true")
        df = pd.DataFrame({'terminals': [40], 'Throughput (requests/second)': [10.0], 'efficiency': [0.0]})
        BenchbaseEvaluator.record_tests(None, exp, pd.DataFrame(), df, {}, {})
        self.assertEqual(_labels(exp), [(False, "efficiency contains 0 or NaN")])

    def test_hammerdb_without_keying_skips(self):
        exp = _experiment(HAMMERDB_KEYANDTHINK="false")
        df = pd.DataFrame({'vusers': [40], 'NOPM': [1000], 'efficiency': [50.0]})
        TpccEvaluator.record_tests(None, exp, pd.DataFrame(), df, {}, {})
        self.assertEqual(_labels(exp)[0][0], None)

    def test_hammerdb_with_keying_tests(self):
        exp = _experiment(HAMMERDB_KEYANDTHINK="true")
        df = pd.DataFrame({'vusers': [40], 'NOPM': [500], 'efficiency': [97.2]})
        TpccEvaluator.record_tests(None, exp, pd.DataFrame(), df, {}, {})
        self.assertEqual(_labels(exp), [(True, "efficiency contains no 0 or NaN")])


def _hammerdb_pods(keyandthink=None, vusers=(20, 20), sf=4, nopm=500):
    """Typed per-pod HammerDB rows of one phase, as benchmarking_set_datatypes returns them."""
    rows = []
    for child, vuser in enumerate(vusers, start=1):
        row = {'connection': f'mysql-1-1-1-{child}', 'phase': 'mysql-1-1', 'job': 'mysql-1-1-1',
               'configuration': 'MySQL-1', 'experiment_run': 1, 'code': 1, 'client': 1,
               'benchmark_run': 1, 'pod': str(child), 'pod_count': len(vusers), 'iterations': 1,
               'duration': 2, 'rampup': 0, 'sf': sf, 'run': 0, 'errors': 0, 'vusers_loading': 1,
               'vusers': vuser, 'NOPM': nopm, 'TPM': 2 * nopm, 'efficiency': 0.0, 'dbms': 'MySQL',
               'tenant_id': -1}
        if keyandthink is not None:
            row['keyandthink'] = keyandthink
        rows.append(row)
    return pd.DataFrame(rows)


class HammerdbPhaseEfficiencyTest(unittest.TestCase):
    """The per-phase efficiency of HammerDB needs key-and-think time, like the per-pod one."""

    def _phase_efficiency(self, df):
        return float(TpccEvaluator.benchmarking_aggregate_by_parallel_pods(None, df)['efficiency'].iloc[0])

    def test_with_keying_and_ten_times_sf(self):
        self.assertAlmostEqual(self._phase_efficiency(_hammerdb_pods("true")), 100. * 500 / 12.86 / 4)

    def test_without_keying_is_zero(self):
        self.assertEqual(self._phase_efficiency(_hammerdb_pods("false")), 0.)

    def test_other_vusers_is_zero(self):
        self.assertEqual(self._phase_efficiency(_hammerdb_pods("true", vusers=(2, 2))), 0.)

    def test_results_without_the_column_keep_the_old_rule(self):
        self.assertAlmostEqual(self._phase_efficiency(_hammerdb_pods(None)), 100. * 500 / 12.86 / 4)


if __name__ == '__main__':
    unittest.main()
