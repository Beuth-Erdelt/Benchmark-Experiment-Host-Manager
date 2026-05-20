"""
Evaluator for DBMSBenchmarker experiments.

Provides :class:`dbmsbenchmarker`, which extends :class:`logger` to parse
and aggregate per-query performance results, warnings, errors, and latency
statistics produced by the DBMSBenchmarker tool.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
import pickle
import json
import traceback
import ast
from dbmsbenchmarker import monitor
from dbmsbenchmarker import parameter, inspector
from datetime import datetime
import glob
from pathlib import Path
from scipy.stats import gmean
import numpy as np

from .base import natural_sort
from .logger import logger

def map_index_to_queryname(numQuery):
    """
    Maps a query index string (e.g., ``'q1'``) to a human-readable title from the
    global ``query_properties`` dictionary.

    If the title cannot be resolved, the original input string is returned unchanged.

    :param numQuery: A query index string, typically a letter followed by a number (e.g., ``'q1'``).
    :type numQuery: str
    :return: The query title from ``query_properties``, or ``numQuery`` if not found.
    :rtype: str
    """
    global query_properties
    if (
        numQuery[1:] in query_properties
        and 'config' in query_properties[numQuery[1:]]
        and 'title' in query_properties[numQuery[1:]]['config']
    ):
        return query_properties[numQuery[1:]]['config']['title']
    return numQuery


class dbmsbenchmarker(logger):
    """
    Evaluator for a DBMSBenchmarker experiment.

    Wraps a :class:`dbmsbenchmarker.inspector.inspector` instance and exposes
    loading times, per-query latency statistics, throughput metrics, warning and
    error counts, and aggregation over parallel pods.

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Unused; loading is always enabled for this evaluator.
    :param include_benchmarking: Unused; benchmarking is always enabled.
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True):
        """
        Initialises the inspector before delegating to the parent constructor.

        :param code: Experiment identifier.
        :param path: Root path that contains the result folders.
        :param include_loading: Ignored; always ``True``.
        :param include_benchmarking: Ignored; always ``True``.
        """
        self.evaluation = None
        self.path_base = path
        super().__init__(code, path, True, True)
        self.load_inspector()
    def load_inspector(self):
        """
        Loads the DBMSBenchmarker inspector for this experiment.

        Creates an :class:`inspector.inspector` rooted at ``self.path_base``,
        loads the experiment identified by ``self.code``, and stores the result
        in ``self.evaluation``.
        """
        try:
            self.evaluation = inspector.inspector(self.path_base)
            self.evaluation.load_experiment(code=self.code, silent=True)
            self.evaluation.code = self.code
        except Exception as e:
            # it fails silently - experiment not completed
            pass
    def get_df_loading(self):
        """
        Returns the DataFrame containing all loading-phase timing results.

        Reads loading time fields (``timeGenerate``, ``timeIngesting``, ``timeSchema``,
        ``timeIndex``, ``timeLoad``) from the inspector's connection data.

        :return: DataFrame with one row per DBMS connection indexed as ``"DBMS"``.
        :rtype: pandas.DataFrame
        """
        if self.evaluation is None:
            self.load_inspector()
        loading_times = {}
        for conn_name, connection in self.evaluation.benchmarks.dbms.items():
            loading_times[conn_name] = {}
            for time_key in ('timeGenerate', 'timeIngesting', 'timeSchema', 'timeIndex', 'timeLoad'):
                if time_key in connection.connectiondata:
                    loading_times[conn_name][time_key] = connection.connectiondata[time_key]
        df = pd.DataFrame(loading_times)
        df = df.reindex(sorted(df.columns), axis=1)
        df = df.round(2).T
        df = df.rename_axis(index="DBMS")
        return df
    def test_results(self):
        """
        Validates results by loading and reconstructing the workflow.

        :return: ``0`` on success, ``1`` if an exception is raised.
        :rtype: int
        """
        try:
            self.load_inspector()
            if self.include_benchmarking:
                df = self.get_df_benchmarking()
                self.workflow = self.reconstruct_workflow(df)
            if self.include_loading:
                self.get_df_loading()
            return 0
        except Exception as exc:
            print(exc)
            return 1
    def get_df_benchmarking(self):
        """
        Returns the DataFrame containing all benchmarking-phase results.

        Combines per-query latency statistics, geo-mean execution times, and per-connection
        timing data from the DBMSBenchmarker inspector into a single DataFrame.

        :return: DataFrame with one row per connection/pod, or empty DataFrame on failure.
        :rtype: pandas.DataFrame
        """
        if self.evaluation is None:
            self.load_inspector()
        global query_properties
        query_properties = self.evaluation.get_experiment_query_properties()
        num_of_queries = 0
        df_stats = self.evaluation.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
        if df_stats is not None:
            df_stats = df_stats.sort_index().T.round(2)
            df_stats.index = df_stats.index.map(map_index_to_queryname)
            num_of_queries = len(df_stats.index)
        df = self.evaluation.get_aggregated_experiment_statistics(type='timer', name='execution', query_aggregate='Median', total_aggregate='Geo')
        df = (df / 1000.0).sort_index().astype('float')
        if df.empty:
            return pd.DataFrame()
        df['Power@Size [~Q/h]'] = float(parameter.defaultParameters['SF']) * 3600. / df
        df_power = df.copy()
        df = self.evaluation.get_aggregated_experiment_statistics(type='timer', name='run', query_aggregate='Median', total_aggregate='Geo')
        df = (df / 1000.0).sort_index()
        df.columns = ['Geo Times [s]']
        df_geo_mean_runtime = df.copy()
        df = pd.concat([df_power, df_geo_mean_runtime], axis=1)
        df_timing_rows = pd.DataFrame()
        for pod_idx, (_conn_nr, connection) in enumerate(self.evaluation.benchmarks.dbms.items(), start=1):
            connection_data = connection.connectiondata
            conn_name = connection_data['name']
            orig_name = connection_data['orig_name']
            configuration = connection_data.get('configuration', '-')
            connection_props = self.evaluation.get_experiment_connection_properties(conn_name)
            df_row = pd.DataFrame(index=[conn_name])
            df_row['phase'] = orig_name
            df_row['connection'] = conn_name
            df_row['configuration'] = configuration
            df_row['SF'] = float(connection_data['parameter']['connection_parameter']['loading_parameters']['SF'])
            df_row['pods'] = int(connection_data['parameter']['connection_parameter']['loading_parameters']['PODS_PARALLEL'])
            df_row['experiment_run'] = int(connection_data['parameter']['numExperiment'])
            df_row['client'] = int(connection_data['parameter']['client'])
            df_row['code'] = int(connection_data['parameter']['code'])
            df_row['pod'] = pod_idx
            df_row['benchmark_start'] = connection_props['times']['total'][conn_name]['time_start']
            if 'time_end' not in connection_props['times']['total'][conn_name]:
                return pd.DataFrame()
            df_row['benchmark_end'] = connection_props['times']['total'][conn_name]['time_end']
            df_timing_rows = pd.concat([df_timing_rows, df_row])
        df_timing = df_timing_rows.sort_index()
        group_keys = ['configuration', 'connection', 'phase', 'SF', 'experiment_run', 'client']
        benchmark_start = df_timing.groupby(group_keys)['benchmark_start'].min()
        benchmark_end = df_timing.groupby(group_keys)['benchmark_end'].max()
        df_benchmark = (benchmark_end - benchmark_start).to_frame(name='time [s]').round(2)
        df_benchmark['pod_count'] = df_timing.groupby(group_keys)['benchmark_end'].count()
        df_benchmark['SF2'] = df_benchmark.index.get_level_values('SF')
        df_benchmark['num_of_queries'] = num_of_queries
        df_benchmark['Throughput@Size'] = (
            num_of_queries * 3600. * df_benchmark['pod_count'] / df_benchmark['time [s]'] * df_benchmark['SF2']
        ).round(2)
        df_benchmark = df_benchmark.reset_index(level=group_keys)
        df_benchmark = df_benchmark.set_index("connection", drop=False)
        df_benchmark['pod'] = df_benchmark['connection']
        df = pd.concat([df, df_benchmark], axis=1)
        df.drop('SF2', axis=1, inplace=True)
        df['Power@Size [~Q/h]'] = df['SF'] * 3600. / df['total_timer_execution']
        df.drop('total_timer_execution', axis=1, inplace=True)
        df['code'] = self.evaluation.code
        df = df.sort_values(['experiment_run', 'client'])
        df = df[['code', 'configuration', 'phase', 'connection', 'experiment_run', 'client',
                  'pod_count', 'SF', 'num_of_queries', 'time [s]', 'Geo Times [s]',
                  'Power@Size [~Q/h]', 'Throughput@Size', 'pod']]
        return df
    def benchmarking_set_datatypes(self, df):
        """
        Returns the DataFrame unchanged.

        DBMSBenchmarker results are already typed by the inspector; no conversion
        is needed.

        :param df: DataFrame of results.
        :type df: pandas.DataFrame
        :return: The same DataFrame, unmodified.
        :rtype: pandas.DataFrame
        """
        return df
    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Aggregates parallel-pod DBMSBenchmarker result rows into one row per phase.

        Groups by ``columns`` and applies geo-mean for timing/power metrics and
        max/sum for count metrics. Recomputes ``Throughput@Size`` from the aggregated
        values.

        :param df: Benchmarking DataFrame (output of :meth:`get_df_benchmarking`).
        :type df: pandas.DataFrame
        :param columns: Grouping columns (default ``['phase']``).
        :type columns: list[str]
        :return: Aggregated DataFrame with one row per group.
        :rtype: pandas.DataFrame
        """
        def safe_gmean(x):
            """Return the geometric mean of ``x``, or NaN for empty input."""
            if len(x) == 0:
                return np.nan
            res = gmean(x)
            return float(res) if np.isscalar(res) or res.size == 1 else float(res[0])
        if self.evaluation is None:
            self.load_inspector()
        global query_properties
        query_properties = self.evaluation.get_experiment_query_properties()
        num_of_queries = 0
        df_stats = self.evaluation.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
        if not df_stats is None:
            df_stats = df_stats.sort_index().T.round(2)
            df_stats.index = df_stats.index.map(map_index_to_queryname)
            num_of_queries = len(df_stats.index)
        df_aggregated = pd.DataFrame()
        for group_key, grp in df.groupby([df[col] for col in columns]):
            aggregate = {
                'connection': 'max',
                'Geo Times [s]': safe_gmean,
                'Power@Size [~Q/h]': safe_gmean,
                'code': 'max',
                'pod_count': 'count',
                'SF': 'max',
                'experiment_run': 'max',
                'time [s]': 'max',
                'client': 'max',
                'Throughput@Size': 'max',
                'num_of_queries': 'sum',
            }
            dict_grp = {
                'configuration': grp['configuration'].iloc[0],
                'experiment_run': grp['experiment_run'].iloc[0],
                'phase': grp['phase'].iloc[0],
            }
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            group_key_str = "_".join(map(str, group_key))
            df_grp = pd.DataFrame(dict_grp, index=[group_key_str])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        df_aggregated['Throughput@Size'] = (df_aggregated['num_of_queries']*3600./df_aggregated['time [s]']*df_aggregated['SF']).round(2)
        df_aggregated['pod'] = "-"
        df_aggregated = df_aggregated[['code', 'configuration', 'phase', 'connection', 'experiment_run', 'client', 'pod_count', 'SF', 'num_of_queries', 'time [s]', 'Geo Times [s]', 'Power@Size [~Q/h]', 'Throughput@Size', 'pod']]
        return df_aggregated
    def get_total_warnings(self, query_titles=False):
        """
        Returns the per-query warning counts for this experiment.

        :param query_titles: When ``True``, replaces query index labels with
                             human-readable titles from ``queries.config``.
        :type query_titles: bool
        :return: DataFrame of warning counts with queries as columns and DBMS as rows.
        :rtype: pandas.DataFrame
        """
        global query_properties
        df = self.evaluation.get_total_warnings().T
        if query_titles:
            query_properties = self.evaluation.get_experiment_query_properties()
            df.index = df.index.map(map_index_to_queryname)
        return df.T
    def get_total_errors(self, query_titles=False):
        """
        Returns the per-query error counts for this experiment.

        :param query_titles: When ``True``, replaces query index labels with
                             human-readable titles from ``queries.config``.
        :type query_titles: bool
        :return: DataFrame of error counts with queries as columns and DBMS as rows.
        :rtype: pandas.DataFrame
        """
        global query_properties
        df = self.evaluation.get_total_errors().T
        if query_titles:
            query_properties = self.evaluation.get_experiment_query_properties()
            df.index = df.index.map(map_index_to_queryname)
        return df.T
    def get_query_latencies(self, query_titles=False):
        """
        Returns the mean execution latency per query and DBMS.

        :param query_titles: When ``True``, replaces query index labels with
                             human-readable titles from ``queries.config``.
        :type query_titles: bool
        :return: DataFrame of mean latencies (ms) with queries as columns and DBMS as rows.
        :rtype: pandas.DataFrame
        """
        global query_properties
        df = self.evaluation.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean').T
        if query_titles:
            if not df is None:
                query_properties = self.evaluation.get_experiment_query_properties()
                df = df.round(2)
                df.index = df.index.map(map_index_to_queryname)
        return df.T
    def get_summary_benchmark_per_phase(self):
        """
        Returns benchmarking results aggregated over parallel pods, one row per phase.

        Applies :meth:`benchmarking_set_datatypes`, aggregates via
        :meth:`benchmarking_aggregate_by_parallel_pods`, and selects the columns
        used for the per-phase summary table (experiment run, terminals, target,
        pod count, time, errors, throughput, goodput, efficiency, and latency
        percentiles), sorted by ``(experiment_run, target, pod_count)``.

        :return: DataFrame indexed as ``"DBMS"`` with one row per phase, or an
                 empty DataFrame if there are no benchmarking results.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            df.fillna(0, inplace=True)
            df_plot = self.benchmarking_set_datatypes(df)
            df_aggregated = self.benchmarking_aggregate_by_parallel_pods(df_plot)
            df_aggregated = df_aggregated.sort_values(['experiment_run','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated.copy()
            df_aggregated_reduced.drop('code', axis=1, inplace=True, errors='ignore')
            df_aggregated_reduced.drop('connection', axis=1, inplace=True, errors='ignore')
            df_aggregated_reduced.drop('configuration', axis=1, inplace=True, errors='ignore')
            df_aggregated_reduced.drop('phase', axis=1, inplace=True, errors='ignore')
            df_aggregated_reduced.drop('pod', axis=1, inplace=True, errors='ignore')
            return df_aggregated_reduced
    def get_summary_benchmark_per_connection(self):
        """
        Returns benchmarking results with one row per pod, filtered to the key
        display columns.

        Applies :meth:`benchmarking_set_datatypes` and selects the columns used
        for the per-connection summary table (experiment run, terminals, target,
        client, child, time, errors, throughput, goodput, efficiency, and
        latency percentiles), then sorts by ``(experiment_run, client, child)``.

        :return: DataFrame indexed as ``"DBMS"`` with one row per pod, or ``None``
                 if there are no benchmarking results.
        :rtype: pandas.DataFrame or None
        """
        df = self.get_df_benchmarking()
        df.drop('code', axis=1, inplace=True, errors='ignore')
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        return df
    def get_summary_loading_per_run(self):
        """
        Returns loading metrics aggregated per experiment run.

        Delegates to :meth:`get_loading_per_run` (defined in :class:`base`),
        which reduces the per-connection loading DataFrame to one row per
        ``(code, configuration, experiment_run)`` and adds a
        ``'Throughput [SF/h]'`` column.

        :return: DataFrame with one row per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_loading_per_run()
        df.drop('code', axis=1, inplace=True, errors='ignore')
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('configuration', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('pod', axis=1, inplace=True, errors='ignore')
        return df
