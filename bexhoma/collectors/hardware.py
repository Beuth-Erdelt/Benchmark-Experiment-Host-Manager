"""
Collector for Hardware (fio/sysbench) experiments.

Provides :class:`HardwareCollector`, a subclass of :class:`CollectorBase` that wires up
:class:`evaluators.hardware` as the evaluator and overrides the performance aggregation
methods to handle the hardware evaluator's column layout.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd

from bexhoma import evaluators
from .base import CollectorBase

__all__ = ["HardwareCollector"]

#: fio result columns shown in the default summary view.
_SUMMARY_COLS = [
    'hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
    'hardware_fio_engine', 'hardware_fio_numjobs',
    'hardware_fio_read_iops', 'hardware_fio_write_iops',
    'hardware_fio_read_bw_kbps', 'hardware_fio_write_bw_kbps',
    'hardware_fio_read_lat_p95_ms', 'hardware_fio_write_lat_p95_ms',
    'hardware_fio_read_lat_p99_ms', 'hardware_fio_write_lat_p99_ms',
    'errors',
]


class HardwareCollector(CollectorBase):
    """
    Collector for Hardware (fio/sysbench) experiments.

    Overrides :meth:`get_evaluator` to return a :class:`evaluators.hardware` instance and
    overrides the performance aggregation methods because the hardware evaluator's
    :meth:`~bexhoma.evaluators.hardware.HardwareEvaluator.benchmarking_aggregate_by_parallel_pods`
    does not produce a ``connection`` column (unlike the base class expectation).
    """

    def get_evaluator(self, code: str = '') -> evaluators.hardware:
        """
        Returns a :class:`evaluators.hardware` instance for the given experiment code.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: Hardware evaluator for the specified experiment.
        :rtype: evaluators.hardware
        """
        if code == '':
            code = self.codes[0]
        return evaluators.hardware(code=code, path=self.path)

    def get_performance_aggregated_per_phase(self) -> pd.DataFrame:
        """
        Combines aggregated fio performance results per phase from all experiment codes.

        Groups by the ``phase`` column (``configuration-experiment_run-client``),
        aggregating all parallel benchmark pods within the same phase into a single row.
        The result index is the code-prefixed phase identifier
        (``<code>-<configuration>-<experiment_run>-<client>``).

        :return: Combined DataFrame of aggregated fio performance metrics, one row per phase.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = self.get_performance_single(evaluation)
            if df.empty:
                continue
            df = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(
                df, columns=['phase']
            )
            if df_aggregated.empty:
                continue
            df_aggregated.index = evaluation.code + '-' + df_aggregated.index.astype(str)
            df_aggregated['phase'] = evaluation.code + '-' + df_aggregated['phase'].astype(str)
            df_aggregated['configuration'] = (
                evaluation.code + '-' + df_aggregated['configuration'].astype(str)
            )
            df_aggregated.drop('connection', axis=1, inplace=True, errors='ignore')
            df_aggregated.drop('job', axis=1, inplace=True, errors='ignore')
            df_aggregated['code'] = df_aggregated['code'].astype(str)
            df_aggregated = df_aggregated.drop(columns=['pod'])
            df_performance = pd.concat([df_performance, df_aggregated])
        return df_performance

    def get_performance_aggregated_per_job(self) -> pd.DataFrame:
        """
        Combines aggregated fio performance results per job from all experiment codes.

        Groups by the ``job`` column
        (``configuration-experiment_run-client-benchmark_run``), keeping parallel
        benchmark jobs within the same phase as separate rows.  The result index is the
        code-prefixed job identifier.

        :return: Combined DataFrame of aggregated fio performance metrics, one row per job.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = self.get_performance_single(evaluation)
            if df.empty:
                continue
            df = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(
                df, columns=['job']
            )
            if df_aggregated.empty:
                continue
            df_aggregated.index = evaluation.code + '-' + df_aggregated.index.astype(str)
            df_aggregated['phase'] = evaluation.code + '-' + df_aggregated['phase'].astype(str)
            df_aggregated['job'] = evaluation.code + '-' + df_aggregated['job'].astype(str)
            df_aggregated['configuration'] = (
                evaluation.code + '-' + df_aggregated['configuration'].astype(str)
            )
            df_aggregated.drop('connection', axis=1, inplace=True, errors='ignore')
            df_aggregated['code'] = df_aggregated['code'].astype(str)
            df_aggregated = df_aggregated.drop(columns=['pod'])
            df_performance = pd.concat([df_performance, df_aggregated])
        return df_performance

    def get_summary(self) -> pd.DataFrame:
        """
        Returns a focused comparison table of key fio metrics across all experiment codes.

        Calls :meth:`get_performance_aggregated_per_phase` and filters to the workload
        parameter and key IOPS / bandwidth / tail-latency columns defined in
        :data:`_SUMMARY_COLS`.  Columns absent from the aggregated result are silently skipped.

        :return: DataFrame with one row per phase and the key fio comparison columns,
                 or an empty DataFrame when no results are available.
        :rtype: pandas.DataFrame
        """
        df = self.get_performance_aggregated_per_phase()
        if df.empty:
            return df
        visible = [col for col in _SUMMARY_COLS if col in df.columns]
        return df[visible]
