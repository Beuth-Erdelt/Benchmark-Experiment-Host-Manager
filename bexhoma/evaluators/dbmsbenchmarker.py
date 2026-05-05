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
    Maps a query index string (e.g., 'q1', 'q2', etc.) to a human-readable query title 
    from the global `query_properties` dictionary.

    If the title is not found in `query_properties`, the input string is returned as-is.

    Parameters
    ----------
    numQuery : str
        A string representing the query index, typically starting with a letter followed by a number (e.g., 'q1').

    Returns
    -------
    str
        The title of the query if available in `query_properties`, otherwise the original input string.
    """
    global query_properties
    if numQuery[1:] in query_properties and 'config' in query_properties[numQuery[1:]] and 'title' in query_properties[numQuery[1:]]['config']:
        return query_properties[numQuery[1:]]['config']['title']
    else:
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
        print(self.path_base)
        self.get_inspector()
    def get_inspector(self):
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
        Returns the DataFrame that containts all information about the loading phase.

        :return: DataFrame of loading results
        """
        if self.evaluation is None:
            self.get_inspector()
        times = {}
        for c, connection in self.evaluation.benchmarks.dbms.items():
            times[c]={}
            if 'timeGenerate' in connection.connectiondata:
                times[c]['timeGenerate'] = connection.connectiondata['timeGenerate']
            if 'timeIngesting' in connection.connectiondata:
                times[c]['timeIngesting'] = connection.connectiondata['timeIngesting']
            if 'timeSchema' in connection.connectiondata:
                times[c]['timeSchema'] = connection.connectiondata['timeSchema']
            if 'timeIndex' in connection.connectiondata:
                times[c]['timeIndex'] = connection.connectiondata['timeIndex']
            if 'timeLoad' in connection.connectiondata:
                times[c]['timeLoad'] = connection.connectiondata['timeLoad']
        df = pd.DataFrame(times)
        df = df.reindex(sorted(df.columns), axis=1)
        df = df.round(2).T
        #df.index.names = ["DBMS"]
        df = df.rename_axis(index="DBMS")
        return df
    def get_df_benchmarking(self):
        """
        Returns the DataFrame that containts all information about the benchmarking phase.

        :return: DataFrame of benchmarking results
        """
        if self.evaluation is None:
            self.get_inspector()
        global query_properties
        query_properties = self.evaluation.get_experiment_query_properties()
        num_of_queries = 0
        df = self.evaluation.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
        if not df is None:
            df = df.sort_index().T.round(2)
            df.index = df.index.map(map_index_to_queryname)
            num_of_queries = len(df.index)
        df = self.evaluation.get_aggregated_experiment_statistics(type='timer', name='execution', query_aggregate='Median', total_aggregate='Geo')
        df = (df/1000.0).sort_index().astype('float')
        if df.empty:
            return pd.DataFrame()
        df['Power@Size [~Q/h]'] = float(parameter.defaultParameters['SF'])*3600./df
        df_power = df.copy()
        df = self.evaluation.get_aggregated_experiment_statistics(type='timer', name='run', query_aggregate='Median', total_aggregate='Geo')
        df = (df/1000.0).sort_index()
        df.columns = ['Geo Times [s]']
        df_geo_mean_runtime = df.copy()
        #print(df_geo_mean_runtime.index)
        df = pd.concat([df_power, df_geo_mean_runtime], axis=1)
        #print(df)
        df_merged_time = pd.DataFrame()
        for connection_nr, connection in self.evaluation.benchmarks.dbms.items():
            df_time = pd.DataFrame()
            c = connection.connectiondata
            connection_name = c['name']
            orig_name = c['orig_name']
            configuration = c['configuration'] if 'configuration' in c else '-'
            eva = self.evaluation.get_experiment_connection_properties(c['name'])
            df_time.index = [connection_name]
            df_time['phase'] = orig_name #self.evaluation.code + '-' + orig_name
            df_time['connection'] = connection_name #self.evaluation.code + '-' + connection_name
            df_time['configuration'] = configuration
            df_time['SF'] = float(c['parameter']['connection_parameter']['loading_parameters']['SF'])
            df_time['pods'] = int(c['parameter']['connection_parameter']['loading_parameters']['PODS_PARALLEL'])
            df_time['experiment_run'] = int(c['parameter']['numExperiment'])
            df_time['client'] = int(c['parameter']['client'])
            df_time['code'] = int(c['parameter']['code'])
            df_time['benchmark_start'] = eva['times']['total'][c['name']]['time_start']
            if not 'time_end' in eva['times']['total'][c['name']]:
                return pd.DataFrame()
            df_time['benchmark_end'] = eva['times']['total'][c['name']]['time_end']
            df_merged_time = pd.concat([df_merged_time, df_time])
        df_time = df_merged_time.sort_index()
        benchmark_start = df_time.groupby(['configuration', 'connection', 'phase', 'SF', 'experiment_run', 'client'])['benchmark_start'].min()
        benchmark_end = df_time.groupby(['configuration', 'connection', 'phase', 'SF', 'experiment_run', 'client'])['benchmark_end'].max()
        duration = benchmark_end - benchmark_start
        df_benchmark = duration.to_frame(name='duration')
        df_benchmark.columns = ['time [s]']
        benchmark_count = df_time.groupby(['configuration', 'connection', 'phase', 'SF', 'experiment_run', 'client']).count()
        df_benchmark['pod_count'] = benchmark_count['benchmark_end']
        df_benchmark['SF2'] = df_benchmark.index.get_level_values('SF')
        df_benchmark['num_of_queries'] = num_of_queries
        df_benchmark['Throughput@Size'] = (num_of_queries*3600.*df_benchmark['pod_count']/df_benchmark['time [s]']*df_benchmark['SF2']).round(2)
        df_benchmark = df_benchmark.reset_index(level=['configuration', 'connection', 'phase', 'SF', 'experiment_run', 'client'])
        df_benchmark = df_benchmark.set_index("connection", drop=False)
        df = pd.concat([df, df_benchmark], axis=1)
        df.drop('SF2', axis=1, inplace=True)
        df['Power@Size [~Q/h]'] = df['SF']*3600./df['total_timer_execution']
        df['code'] = self.evaluation.code
        df = df.sort_values(['experiment_run', 'client'])
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
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        def safe_gmean(x):
            if len(x) == 0: return np.nan
            res = gmean(x)
            return float(res) if np.isscalar(res) or res.size == 1 else float(res[0])
        if self.evaluation is None:
            self.get_inspector()
        global query_properties
        query_properties = self.evaluation.get_experiment_query_properties()
        num_of_queries = 0
        df_stats = self.evaluation.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
        if not df_stats is None:
            df_stats = df_stats.sort_index().T.round(2)
            df_stats.index = df_stats.index.map(map_index_to_queryname)
            num_of_queries = len(df_stats.index)
        #num_of_queries=22
        #df=df_performance.copy()
        #column = "connection"
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby([df[col] for col in columns]):
            aggregate = {
                'connection':'max',
                'total_timer_execution':safe_gmean,
                'Power@Size [~Q/h]':safe_gmean,
                'code':'max',
                'pod_count':'count',
                'SF':'max',
                'experiment_run':'max',
                'time [s]':'max',
                'client':'max',
                'Throughput@Size':'max',
                'num_of_queries':'sum',
            }
            dict_grp = dict()
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            key_index = "_".join(map(str, key))
            df_grp = pd.DataFrame(dict_grp, index=[key_index])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        df_aggregated['Throughput@Size'] = (df_aggregated['num_of_queries']*3600./df_aggregated['time [s]']*df_aggregated['SF']).round(2)
        df_aggregated['pod'] = "-"
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
