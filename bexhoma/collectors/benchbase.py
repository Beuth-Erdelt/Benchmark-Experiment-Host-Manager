"""
Collector for Benchbase experiments.

Provides :class:`benchbase`, a thin subclass of :class:`base` that wires up
:class:`evaluators.benchbase` as the evaluator. All data collection and
aggregation logic is inherited from :class:`base`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import seaborn as sns
from math import floor
import ast
import json
import re
import numpy as np
from scipy.stats import gmean
import pprint

from dbmsbenchmarker import parameter, inspector

from bexhoma import evaluators
from .base import base


class benchbase(base):
    """
    Collector for Benchbase experiments.

    Overrides :meth:`get_evaluator` to return a :class:`evaluators.benchbase` instance.
    All data collection and aggregation methods are inherited from :class:`base`.
    """
    def __init__(self, path, codes):
        """
        :param path: Base filesystem path that contains the experiment directories.
        :type path: str
        :param codes: List of experiment codes to collect results for.
        :type codes: list[str]
        """
        base.__init__(self, path, codes)

    def get_evaluator(self, code=''):
        """
        Returns a :class:`evaluators.benchbase` instance for the given experiment code.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: Benchbase evaluator for the specified experiment.
        :rtype: evaluators.benchbase
        """
        if code == '':
            code = self.codes[0]
        return evaluators.benchbase(code=code, path=self.path)

    def get_benchmark_timeseries_per_phase(self, metric="throughput"):
        """
        Combines aggregated Benchbase time-series per phase from all experiment codes into a wide-format DataFrame.

        For each code and each unique ``(configuration, client, experiment_run)`` combination,
        calls :meth:`evaluators.benchbase.get_benchmark_logs_timeseries_df_aggregated` and
        places the metric column as one column in the result.  Each column is labelled
        ``{code}-{configuration}-{client}-{experiment_run}``.

        :param metric: Benchbase metric to retrieve (default ``'throughput'``).
        :type metric: str
        :return: Wide-format DataFrame indexed by second with one column per phase,
                 or an empty DataFrame when no data is available.
        :rtype: pandas.DataFrame
        """
        df_result = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df_benchmarking = self.get_performance_single(evaluation)
            if df_benchmarking.empty:
                continue
            df_benchmarking = evaluation.benchmarking_set_datatypes(df_benchmarking)
            for (configuration, client, experiment_run), _ in df_benchmarking.groupby(
                ['configuration', 'client', 'experiment_run']
            ):
                df_ts = evaluation.get_benchmark_logs_timeseries_df_aggregated(
                    metric=metric,
                    configuration=configuration,
                    client=client,
                    experiment_run=experiment_run
                )
                if isinstance(df_ts, pd.DataFrame) and not df_ts.empty and metric in df_ts.columns:
                    col_label = f"{code}-{configuration}-{client}-{experiment_run}"
                    df_result[col_label] = df_ts[metric]
        return df_result

    def get_benchmark_timeseries_all(self, metric="throughput"):
        """
        Collects long-format Benchbase time-series data for a given metric across all experiment codes.

        For each code and each unique ``(configuration, client, experiment_run)`` combination,
        calls :meth:`evaluators.benchbase.get_benchmark_logs_timeseries_df_aggregated`, reshapes
        the result to long format, and annotates each row with its identifying fields.
        Connection metadata (e.g. ``type_tenants``, ``num_tenants``, ``vol_tenants``) is joined
        in from :meth:`get_connections` for each code.

        :param metric: Benchbase metric to retrieve (default ``'throughput'``).
        :type metric: str
        :return: Long-format DataFrame with columns ``second``, ``code``, ``configuration``,
                 ``client``, ``experiment_run``, ``metric``, ``value``, plus connection
                 metadata columns.
        :rtype: pandas.DataFrame
        """
        df_timeseries = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df_connections = self.get_connections(evaluation)
            df_benchmarking = self.get_performance_single(evaluation)
            if df_benchmarking.empty:
                continue
            df_benchmarking = evaluation.benchmarking_set_datatypes(df_benchmarking)
            df_code = pd.DataFrame()
            for (configuration, client, experiment_run), _ in df_benchmarking.groupby(
                ['configuration', 'client', 'experiment_run']
            ):
                df_ts = evaluation.get_benchmark_logs_timeseries_df_aggregated(
                    metric=metric,
                    configuration=configuration,
                    client=client,
                    experiment_run=experiment_run
                )
                if isinstance(df_ts, pd.DataFrame) and not df_ts.empty and metric in df_ts.columns:
                    index_col = df_ts.index.name or 'second'
                    df_long = df_ts[[metric]].reset_index().rename(
                        columns={index_col: 'second', metric: 'value'}
                    )
                    df_long['metric'] = metric
                    df_long['code'] = code
                    df_long['configuration'] = configuration
                    df_long['client'] = str(client)
                    df_long['experiment_run'] = str(experiment_run)
                    df_code = pd.concat([df_code, df_long])
            if not df_code.empty:
                join_keys = ['code', 'configuration', 'client', 'experiment_run']
                extra_cols = [
                    c for c in df_connections.columns
                    if c not in join_keys and c not in ['connection', 'phase']
                ]
                df_meta = df_connections[join_keys + extra_cols].drop_duplicates(subset=join_keys).copy()
                df_meta['client'] = df_meta['client'].astype(str)
                df_meta['experiment_run'] = df_meta['experiment_run'].astype(str)
                df_code = df_code.merge(df_meta, on=join_keys, how='left')
                df_timeseries = pd.concat([df_timeseries, df_code])
        df_timeseries = df_timeseries.sort_values(["second", "configuration", "experiment_run", "client"])
        return df_timeseries
