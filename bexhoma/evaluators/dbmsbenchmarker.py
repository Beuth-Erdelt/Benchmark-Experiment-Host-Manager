"""
:Date: 2023-01-05
:Version: 0.6.1
:Authors: Patrick K. Erdelt

    Module to evaluate results obtained using bexhoma.

    Copyright (C) 2020  Patrick K. Erdelt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
# Some nice output
#from IPython.display import display, Markdown
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
    Class for evaluating a DBMSBenchmarker experiment.
    Constructor sets

      1. `path`: path to result folders
      1. `code`: Id of the experiment (name of result folder)
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True):
        self.evaluation = None
        self.path_base = path
        super().__init__(code, path, True, True)
    def get_inspector(self):
        self.evaluation = inspector.inspector(self.path_base)
        self.evaluation.load_experiment(code=self.code, silent=True)
        self.evaluation.code = self.code
    def OLD_get_df_benchmarking(self):
        """
        Returns the DataFrame that containts all information about the benchmarking phase.

        :return: DataFrame of benchmarking results
        """
        filename = "bexhoma-benchmarker.all.df.pickle"
        filename_full = self.path+"/"+filename
        if os.path.isfile(filename_full):
            df = pd.read_pickle(filename_full)
        else:
            self.evaluate_results()
            if os.path.isfile(filename_full):
                df = pd.read_pickle(filename_full)
            else:
                df = pd.DataFrame()
        #df#.sort_values(["configuration", "pod"])
        return df
    def OLD_get_df_loading(self):
        """
        Returns the DataFrame that containts all information about the loading phase.

        :return: DataFrame of loading results
        """
        filename = "bexhoma-loading.all.df.pickle"
        if os.path.isfile(self.path+"/"+filename):
            df = pd.read_pickle(self.path+"/"+filename)
        else:
            df = pd.DataFrame()
        #df#.sort_values(["configuration", "pod"])
        return df
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
        df = pd.concat([df_power, df_geo_mean_runtime], axis=1)
        df_merged_time = pd.DataFrame()
        for connection_nr, connection in self.evaluation.benchmarks.dbms.items():
            df_time = pd.DataFrame()
            c = connection.connectiondata
            connection_name = c['name']
            orig_name = c['orig_name']
            eva = self.evaluation.get_experiment_connection_properties(c['name'])
            df_time.index = [connection_name]
            df_time['orig_name'] = orig_name
            df_time['connection_name'] = connection_name
            df_time['SF'] = float(c['parameter']['connection_parameter']['loading_parameters']['SF'])
            df_time['pods'] = int(c['parameter']['connection_parameter']['loading_parameters']['PODS_PARALLEL'])
            df_time['num_experiment'] = int(c['parameter']['numExperiment'])
            df_time['num_client'] = int(c['parameter']['client'])
            df_time['code'] = int(c['parameter']['code'])
            df_time['benchmark_start'] = eva['times']['total'][c['name']]['time_start']
            if not 'time_end' in eva['times']['total'][c['name']]:
                return pd.DataFrame()
            df_time['benchmark_end'] = eva['times']['total'][c['name']]['time_end']
            df_merged_time = pd.concat([df_merged_time, df_time])
        df_time = df_merged_time.sort_index()
        # aggregate per parallel pods per dbms - not valid for model=container?
        #benchmark_start = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client']).min('benchmark_start')
        #benchmark_end = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client']).max('benchmark_end')
        #print(df_time)
        benchmark_start = df_time.groupby(['connection_name', 'orig_name', 'SF', 'num_experiment', 'num_client'])['benchmark_start'].min()
        benchmark_end = df_time.groupby(['connection_name', 'orig_name', 'SF', 'num_experiment', 'num_client'])['benchmark_end'].max()
        duration = benchmark_end - benchmark_start
        df_benchmark = duration.to_frame(name='duration')
        #df_benchmark = pd.DataFrame(benchmark_end['benchmark_end'] - benchmark_start['benchmark_start'])
        df_benchmark.columns = ['time [s]']
        benchmark_count = df_time.groupby(['connection_name', 'orig_name', 'SF', 'num_experiment', 'num_client']).count()
        df_benchmark['count'] = benchmark_count['benchmark_end']
        df_benchmark['connection'] = df_benchmark.index.get_level_values('orig_name')
        df_benchmark['SF2'] = df_benchmark.index.get_level_values('SF')
        #df_benchmark['connection'] = df_benchmark.index.map(lambda x: x[1])
        #df_benchmark['SF2'] = df_benchmark.index.map(lambda x: x[2])
        df_benchmark['num_of_queries'] = num_of_queries
        df_benchmark['Throughput@Size'] = (num_of_queries*3600.*df_benchmark['count']/df_benchmark['time [s]']*df_benchmark['SF2']).round(2)
        index_names = list(df_benchmark.index.names)
        index_names[0] = "connection_pod"
        df_benchmark.rename_axis(index_names, inplace=True)
        df_benchmark = df_benchmark.reset_index(level=['orig_name', 'SF', 'num_experiment', 'num_client'])
        df = pd.concat([df, df_benchmark], axis=1)
        df.drop('SF2', axis=1, inplace=True)
        df.rename(columns={'num_experiment': 'experiment_run'}, inplace=True)
        df.rename(columns={'num_client': 'client'}, inplace=True)
        df['Power@Size [~Q/h]'] = df['SF']*3600./df['total_timer_execution']
        df['code'] = self.evaluation.code
        df = df.sort_values(['experiment_run', 'client'])
        return df
    def benchmarking_set_datatypes(self, df):
        return df
    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["connection"]):
        """
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
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
        column = "connection"
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(column):
            #print(key, len(grp.index))
            #print(grp.columns)
            aggregate = {
                'total_timer_execution':gmean,
                'Power@Size [~Q/h]':gmean,
                'code':'max',
                'orig_name':'max',
                'SF':'max',
                'experiment_run':'max',
                'time [s]':'max',
                'count':'count',
                'client':'max',
                'Throughput@Size':'max',
                'num_of_queries':'sum',
            }
            dict_grp = dict()
            dict_grp['connection'] = key
            #dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            #dict_grp['client'] = grp['client'][0]
            #dict_grp['pod'] = grp['pod'][0]
            #print(dict_grp)
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            df_grp = pd.DataFrame(dict_grp, index=[key])#columns=list(dict_grp.keys()))
            #df_grp = df_grp.T
            #df_grp.set_index('connection', inplace=True)
            #print(df_grp)
            df_aggregated = pd.concat([df_aggregated, df_grp])
        df_aggregated['Throughput@Size'] = (df_aggregated['num_of_queries']*3600./df_aggregated['time [s]']*df_aggregated['SF']).round(2)
        df_aggregated['pod'] = "-"
        #df_aggregated['Throughput@Size'] = (df_aggregated['num_of_queries']*3600.*df_aggregated['count']/df_aggregated['time [s]']*df_aggregated['SF']).round(2)
        df_aggregated
        return df_aggregated