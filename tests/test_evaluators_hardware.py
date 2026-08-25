"""
Unit tests for :mod:`bexhoma.evaluators.hardware`.

Covers a real bug found while validating the hardware-baseline sweep
(:mod:`bexhoma.hardware_baseline`) against a live cluster: an experiment that
mixes multiple ``HARDWARE_TYPE`` rounds under one configuration (e.g. a
sysbench round then a fio round for the same node) caused
``HardwareEvaluator.record_tests()`` to report a false "0 CPU events/sec"
failure for the fio rounds, since it gated its sysbench check on the single
experiment-wide ``args.hardware_type`` and then scanned *every* row --
including fio rows, where the sysbench-only column is legitimately zero.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import unittest
from types import SimpleNamespace

import pandas as pd

from bexhoma import evaluators


def _make_evaluator() -> evaluators.hardware:
    """Build a HardwareEvaluator with no disk access needed for these tests."""
    return evaluators.hardware(code='test-code', path='/nonexistent', include_loading=False,
                                include_benchmarking=True, benchmark_run=1, name='hardware')


def _make_experiment(records: list) -> SimpleNamespace:
    """Minimal experiment stand-in: records every (passed, label) via _record_test."""
    return SimpleNamespace(
        args=SimpleNamespace(hardware_type='sysbench'),
        benchmarking_is_active=lambda: True,
        test_workflow=lambda actual, planned: True,
        _record_test=lambda passed, label: records.append((passed, label)),
    )


class RowsOfHardwareTypeTest(unittest.TestCase):
    """Tests for :meth:`HardwareEvaluator._rows_of_hardware_type`."""

    def test_filters_by_column_when_present(self) -> None:
        df = pd.DataFrame([
            {'hardware_type': 'sysbench', 'value': 1},
            {'hardware_type': 'fio', 'value': 2},
            {'hardware_type': 'sysbench', 'value': 3},
        ])
        selected = evaluators.hardware._rows_of_hardware_type(df, 'sysbench', 'sysbench')
        self.assertEqual(sorted(selected['value']), [1, 3])

    def test_falls_back_to_experiment_wide_type_when_column_absent(self) -> None:
        df = pd.DataFrame([{'value': 1}, {'value': 2}])
        matching = evaluators.hardware._rows_of_hardware_type(df, 'sysbench', 'sysbench')
        self.assertEqual(len(matching), 2)
        not_matching = evaluators.hardware._rows_of_hardware_type(df, 'fio', 'sysbench')
        self.assertEqual(len(not_matching), 0)


class BenchmarkingAggregateHardwareTypeTest(unittest.TestCase):
    """Tests for hardware_type survival through
    :meth:`HardwareEvaluator.benchmarking_aggregate_by_parallel_pods`."""

    def test_hardware_type_is_preserved_as_a_constant_per_group_column(self) -> None:
        evaluator = _make_evaluator()
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 1, 'hardware_type': 'sysbench',
             'code': 1, 'job': 'j1', 'experiment_run': 1, 'phase': 'p1',
             'pod': 'a', 'pod_count': 1, 'errors': 0, 'benchmark_run': 1,
             'tenant_id': -1, 'duration': 1},
        ])
        df_aggregated = evaluator.benchmarking_aggregate_by_parallel_pods(df, columns=['configuration', 'client'])
        self.assertIn('hardware_type', df_aggregated.columns)
        self.assertEqual(df_aggregated['hardware_type'].iloc[0], 'sysbench')

    def test_absent_hardware_type_column_does_not_raise(self) -> None:
        evaluator = _make_evaluator()
        df = pd.DataFrame([
            {'configuration': 'hw-n1', 'client': 1,
             'code': 1, 'job': 'j1', 'experiment_run': 1, 'phase': 'p1',
             'pod': 'a', 'pod_count': 1, 'errors': 0, 'benchmark_run': 1,
             'tenant_id': -1, 'duration': 1},
        ])
        df_aggregated = evaluator.benchmarking_aggregate_by_parallel_pods(df, columns=['configuration', 'client'])
        self.assertNotIn('hardware_type', df_aggregated.columns)


class RecordTestsMixedHardwareTypeTest(unittest.TestCase):
    """Tests for :meth:`HardwareEvaluator.record_tests` against a ``df_reduced``
    that mixes multiple hardware types under one experiment -- the scenario
    :mod:`bexhoma.hardware_baseline` introduces."""

    def _df_reduced(self, sysbench_cpu_events: float, fio_read_iops: float, fio_write_iops: float) -> pd.DataFrame:
        return pd.DataFrame([
            {'hardware_type': 'sysbench', 'hardware_sysbench_cpu_events_per_sec': sysbench_cpu_events},
            {'hardware_type': 'fio', 'hardware_fio_read_iops': fio_read_iops, 'hardware_fio_write_iops': fio_write_iops},
        ])

    def test_healthy_mixed_rounds_both_pass(self) -> None:
        evaluator = _make_evaluator()
        df_reduced = self._df_reduced(sysbench_cpu_events=300.0, fio_read_iops=100.0, fio_write_iops=100.0)
        records = []
        evaluator.record_tests(_make_experiment(records), pd.DataFrame(), df_reduced, {}, {})
        results = {label: passed for passed, label in records}
        self.assertTrue(results.get("Execution Phase: every round has non-zero CPU events/sec"))
        self.assertTrue(results.get("Execution Phase: every round has non-zero read or write IOPS"))

    def test_fio_round_with_zero_sysbench_column_does_not_fail_sysbench_check(self) -> None:
        """This is the exact bug: a fio round's own hardware_sysbench_cpu_events_per_sec
        is legitimately 0 (sysbench never ran that round) and must not trip the
        sysbench zero-events check."""
        evaluator = _make_evaluator()
        df_reduced = self._df_reduced(sysbench_cpu_events=300.0, fio_read_iops=100.0, fio_write_iops=100.0)
        records = []
        evaluator.record_tests(_make_experiment(records), pd.DataFrame(), df_reduced, {}, {})
        labels = [label for passed, label in records]
        self.assertNotIn("Execution Phase: at least one round has 0 CPU events/sec", labels)

    def test_genuinely_broken_sysbench_round_is_still_caught(self) -> None:
        evaluator = _make_evaluator()
        df_reduced = self._df_reduced(sysbench_cpu_events=0.0, fio_read_iops=100.0, fio_write_iops=100.0)
        records = []
        evaluator.record_tests(_make_experiment(records), pd.DataFrame(), df_reduced, {}, {})
        results = {label: passed for passed, label in records}
        self.assertFalse(results.get("Execution Phase: every round has non-zero CPU events/sec"))
        # the fio round is unaffected
        self.assertTrue(results.get("Execution Phase: every round has non-zero read or write IOPS"))

    def test_genuinely_broken_fio_round_does_not_fail_sysbench_check(self) -> None:
        evaluator = _make_evaluator()
        df_reduced = self._df_reduced(sysbench_cpu_events=300.0, fio_read_iops=0.0, fio_write_iops=0.0)
        records = []
        evaluator.record_tests(_make_experiment(records), pd.DataFrame(), df_reduced, {}, {})
        results = {label: passed for passed, label in records}
        self.assertTrue(results.get("Execution Phase: every round has non-zero CPU events/sec"))
        self.assertFalse(results.get("Execution Phase: every round has non-zero read or write IOPS"))


if __name__ == '__main__':
    unittest.main()
