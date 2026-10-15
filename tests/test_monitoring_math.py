"""Tests for reducing counter time series to a phase total (``bexhoma.monitoring_math``).

The series shapes are taken from the storage probes of 2026-10-14/15
(experiments 1792023056, 1792029787), where ``max - min`` reported the
previous repetition's SUT total for the first phase after a restart.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import math
import unittest

import pandas as pd

from bexhoma.monitoring_math import JOB_COMPONENTS, counter_increase, counter_total

__all__ = []


def _frame(**columns) -> pd.DataFrame:
    return pd.DataFrame(columns)


class CounterIncreaseTest(unittest.TestCase):
    """Growth only: drops (a vanishing pod, a reset, zero padding) are not counted."""

    def test_dead_pod_of_the_previous_repetition_is_not_counted(self):
        """TPC-C 1792023056 rep 2 loading: old SUT flat at 4205 until it vanishes."""
        df = _frame(c=[4206.0, 4206.0, 4242.0, 4353.0, 148.0, 148.0])
        self.assertAlmostEqual(counter_increase(df)['c'], 147.0)
        self.assertAlmostEqual((df.max() - df.min())['c'], 4205.0)  # what was reported

    def test_plain_counter_equals_max_minus_min(self):
        df = _frame(c=[10.0, 12.5, 20.0, 20.0, 31.0])
        self.assertAlmostEqual(counter_increase(df)['c'], 21.0)

    def test_reset_counts_both_segments(self):
        df = _frame(c=[100.0, 150.0, 0.0, 30.0])
        self.assertAlmostEqual(counter_increase(df)['c'], 80.0)

    def test_zero_padding_at_the_end_is_ignored(self):
        df = _frame(c=[50.0, 60.0, 0.0, 0.0])
        self.assertAlmostEqual(counter_increase(df)['c'], 10.0)

    def test_gaps_are_bridged(self):
        df = _frame(c=[1.0, float('nan'), float('nan'), 4.0])
        self.assertAlmostEqual(counter_increase(df)['c'], 3.0)

    def test_empty_and_single_value_columns(self):
        df = _frame(empty=[float('nan')] * 3, single=[float('nan'), 7.0, float('nan')])
        result = counter_increase(df)
        self.assertTrue(math.isnan(result['empty']))
        self.assertEqual(result['single'], 0.0)

    def test_one_value_per_connection_sorted(self):
        df = _frame(b=[0.0, 2.0], a=[0.0, 1.0])
        self.assertEqual(list(counter_increase(df).index), ['a', 'b'])


class CounterTotalTest(unittest.TestCase):
    """SUT components use the growth; job components keep max - min until they are scoped."""

    def test_sut_components_use_the_growth(self):
        """TPC-H 1792029787 run 3 benchmarking: run 2's SUT leaves at sample 2."""
        df = _frame(c=[526.7, 621.0, 94.8, 487.7])
        for component in ('loading', 'benchmarking', 'workerloading', 'poolbenchmarking'):
            with self.subTest(component):
                self.assertAlmostEqual(counter_total(df, component)['c'], 487.2)

    def test_job_components_keep_max_minus_min(self):
        """TPC-C 1792023056 loader: first scrape already shows the job's CPU, then padding."""
        df = _frame(c=[190.9, 190.9, 0.0, 0.0])
        self.assertEqual(JOB_COMPONENTS, {'loader', 'datagenerator', 'benchmarker'})
        for component in JOB_COMPONENTS:
            with self.subTest(component):
                self.assertAlmostEqual(counter_total(df, component)['c'], 190.9)
        self.assertAlmostEqual(counter_increase(df)['c'], 0.0)  # why jobs keep max - min


if __name__ == '__main__':
    unittest.main()
