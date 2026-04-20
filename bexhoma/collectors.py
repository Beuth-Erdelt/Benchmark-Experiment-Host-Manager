"""
:Date: 2025-07-22
:Version: 0.8.10
:Authors: Patrick K. Erdelt

    Classes for collecting and aggregating results from several experiments.

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


def get_non_constant(df):
    def is_not_constant(s):
        return s.nunique(dropna=False) > 1
    df = df.loc[:, df.apply(is_not_constant)]
    return df

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




class default():
    """
    :Date: 2025-07-22
    :Version: 0.8.10
    :Authors: Patrick K. Erdelt

        Class for collecting and aggregating results from several experiments.

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
    def __init__(self, path, codes):
        self.path = path
        self.codes = codes
        self.with_monitoring = True
        code = codes[0]
        evaluate = self.get_evaluator(code)
        self.df_metrics = self.get_metrics(evaluate)
    def get_workload(self, code=''):
        """
        Returns the workload data of an experiment given by its code.

        This function reads the 'queries.config' file associated with the specified experiment code,
        parses its contents, and returns the workload properties as a dictionary.

        :param code: The unique identifier of the experiment.
        :type code: str
        :return: A dictionary containing the workload properties.
        :rtype: dict
        """
        if code == '':
            code = self.codes[0]
        with open(self.path+"/"+code+"/queries.config",'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
            if 'tenant_per' not in workload_properties or workload_properties['tenant_per'] == '':
                workload_properties['tenant_per'] = 'None'
            return workload_properties

    def get_monitored_components(self, code=''):
        if not self.with_monitoring:
            return pd.DataFrame()
        monitoring_components  = self.get_workload(code=code)['monitoring_components']
        #print(monitoring_components)
        df = pd.DataFrame.from_dict(monitoring_components, orient='index', columns=['description'])
        return df

    def get_performance_single(self, evaluation=None):
        """
        Reads the performance metrics and returns them without any aggregation across clients.

        This function retrieves benchmarking data from the given evaluation object,
        sorts it by experiment run and client, and returns the resulting DataFrame.

        :param evaluation: The evaluation object containing benchmarking data.
        :type evaluation: object
        :return: A DataFrame containing unaggregated performance metrics per client.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            evaluation = self.get_evaluator()
        df = evaluation.get_df_benchmarking()
        if not df.empty:
            df = df.sort_values(['code', 'experiment_run', 'client'])
        else:
            print(evaluation.code, "is empty")
        return df

        
    def OLD_get_performance(self, evaluation):
        """
        Reads and aggregates the performance metrics across clients.

        This function retrieves benchmarking data from the given evaluation object,
        sorts it by experiment run and client, and performs aggregation by client.
        It sums throughput and error counts, calculates the mean average latency, 
        and determines the maximum 99th percentile latency per client.

        :param evaluation: The evaluation object containing benchmarking data.
        :type evaluation: object
        :return: A DataFrame with aggregated performance metrics per client.
        :rtype: pandas.DataFrame
        """
        df = self.get_performance_single(evaluation)
        df = evaluation.benchmarking_set_datatypes(df)
        df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df)
        df_aggregated.index = evaluation.code + '-' + df_aggregated.index.astype(str)
        df_aggregated['phase'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['phase'].astype(str)
        df_aggregated['configuration'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['configuration'].astype(str)
        df_aggregated.drop('connection', axis=1, inplace=True)
        #print(df_aggregated)
        return df_aggregated

    def OLD_get_performance_single(self, evaluate):
        """
        Reads the performance metrics and returns them without any aggregation across clients.
        Computes performance metrics for a single experiment run, including latency, execution power,
        throughput, and timing details for each connection/client.

        This function uses benchmarking results from a given evaluator instance, maps query indices
        to human-readable names, and calculates a set of performance indicators such as:
        - Power@Size: estimated performance at a given scale factor
        - Geo Times: geometric mean of execution runtimes
        - Throughput@Size: estimated throughput per hour at a given scale factor, is number of queries executed per hour scaled by SF and number of clients

        :param evaluate: An evaluator object containing benchmarking and experiment data.
        :type evaluate: object
        :return: A DataFrame containing various aggregated performance metrics including runtime, throughput,
                 number of queries, and associated configuration like client count and SF.
        :rtype: pandas.DataFrame
        """
        global query_properties
        query_properties = evaluate.get_experiment_query_properties()
        num_of_queries = 0
        df = evaluate.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
        if not df is None:
            df = df.sort_index().T.round(2)
            df.index = df.index.map(map_index_to_queryname)
            num_of_queries = len(df.index)
        df = evaluate.get_aggregated_experiment_statistics(type='timer', name='execution', query_aggregate='Median', total_aggregate='Geo')
        df = (df/1000.0).sort_index().astype('float')
        if df.empty:
            return pd.DataFrame()
        df['Power@Size [~Q/h]'] = float(parameter.defaultParameters['SF'])*3600./df
        df_power = df.copy()
        df = evaluate.get_aggregated_experiment_statistics(type='timer', name='run', query_aggregate='Median', total_aggregate='Geo')
        df = (df/1000.0).sort_index()
        df.columns = ['Geo Times [s]']
        df_geo_mean_runtime = df.copy()
        df = pd.concat([df_power, df_geo_mean_runtime], axis=1)
        df_merged_time = pd.DataFrame()
        for connection_nr, connection in evaluate.benchmarks.dbms.items():
            df_time = pd.DataFrame()
            c = connection.connectiondata
            connection_name = c['name']
            orig_name = c['orig_name']
            eva = evaluate.get_experiment_connection_properties(c['name'])
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
        benchmark_start = df_time.groupby(['connection_name', 'SF', 'num_experiment', 'num_client']).min('benchmark_start')
        benchmark_end = df_time.groupby(['connection_name', 'SF', 'num_experiment', 'num_client']).max('benchmark_end')
        df_benchmark = pd.DataFrame(benchmark_end['benchmark_end'] - benchmark_start['benchmark_start'])
        df_benchmark.columns = ['time [s]']
        benchmark_count = df_time.groupby(['connection_name', 'SF', 'num_experiment', 'num_client']).count()
        df_benchmark['count'] = benchmark_count['benchmark_end']
        df_benchmark['SF2'] = df_benchmark.index.map(lambda x: x[1])
        df_benchmark['num_of_queries'] = num_of_queries
        df_benchmark['Throughput@Size'] = (num_of_queries*3600.*df_benchmark['count']/df_benchmark['time [s]']*df_benchmark['SF2']).round(2)
        index_names = list(df_benchmark.index.names)
        index_names[0] = "DBMS"
        df_benchmark.rename_axis(index_names, inplace=True)
        df_benchmark = df_benchmark.reset_index(level=['SF', 'num_experiment', 'num_client'])
        df = pd.concat([df, df_benchmark], axis=1)
        df.drop('SF2', axis=1, inplace=True)
        df.rename(columns={'num_experiment': 'experiment_run'}, inplace=True)
        df.rename(columns={'num_client': 'client'}, inplace=True)
        df['Power@Size [~Q/h]'] = df['SF']*3600./df['total_timer_execution']
        df = df.sort_values(['experiment_run', 'client'])
        return df


    def OLD_get_performance(self, evaluation):
        """
        Aggregates performance metrics from a single experiment evaluation across parallel clients.

        This function retrieves detailed metrics using `get_performance_single()`, sorts the data,
        and groups it by client to compute throughput, execution time, and power metrics. The 
        throughput is recomputed based on the total number of queries, count, and execution time.

        :param evaluation: The evaluation object containing benchmarking data.
        :type evaluation: object
        :return: A DataFrame with aggregated performance metrics per client.
        :rtype: pandas.DataFrame
        """
        df = self.get_performance_single(evaluation)
        if df.empty:
            return pd.DataFrame()
        result = df.groupby(['experiment_run', 'client']).agg({
            'Throughput@Size': 'sum',
            'time [s]': 'max',
            'num_of_queries': 'max',
            'SF': 'max',
            'count': 'sum',
            'Power@Size [~Q/h]': lambda x: gmean(x.dropna()), # 'prod',
            #'num_errors': 'sum',
            #'Latency Distribution.Average Latency (microseconds)': 'mean'
        }).reset_index()
        result['Throughput@Size'] = (result['num_of_queries']*3600.*result['count']/result['time [s]']*result['SF']).round(2)
        return result


    def OLD_get_performance_all(self):
        """
        Loops over multiple experiments and combines their aggregated performance results into a single DataFrame.

        For each experiment code, this function:
        - Initializes a benchmarking evaluator
        - Retrieves the corresponding workload configuration
        - Extracts aggregated performance metrics per client
        - Annotates the results with workload metadata (`type` and `num_tenants`)
        - Concatenates the results into a single DataFrame

        :return: A combined DataFrame containing aggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_performance(evaluation)
            if df.empty:
                continue
            #print(df)
            df['type']=workload['tenant_per']
            df['num_tenants']=workload['num_tenants']
            df['vol_tenants']=workload['multi_tenant_volume']
            df['code']=code
            #print(df)
            df_performance = pd.concat([df_performance, df])
        df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance

    def get_performance_aggregated_per_phase(self, type="stream"):
        """
        Loops over multiple experiments and combines their aggregated performance results into a single DataFrame.

        For each experiment code, this function:
        - Initializes a benchmarking evaluator
        - Retrieves the corresponding workload configuration
        - Extracts aggregated performance metrics per client
        - Annotates the results with workload metadata (`type` and `num_tenants`)
        - Concatenates the results into a single DataFrame

        :return: A combined DataFrame containing aggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_performance_single(evaluation)
            df = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df, columns=['phase'])
            #print(df_aggregated)
            df_aggregated.index = evaluation.code + '-' + df_aggregated.index.astype(str)
            df_aggregated['phase'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['phase'].astype(str)
            df_aggregated['configuration'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['configuration'].astype(str)
            df_aggregated.drop('connection', axis=1, inplace=True)
            #df = self.get_performance(evaluation)
            if df_aggregated.empty:
                continue
            #print(df)
            #df['type']=workload['tenant_per']
            #df['num_tenants']=workload['num_tenants']
            #df['vol_tenants']=workload['multi_tenant_volume']
            #df['code']=code
            df_aggregated['code'] = df_aggregated['code'].astype(str)
            df_aggregated = df_aggregated.drop(columns=['pod'])
            #print(df)
            df_performance = pd.concat([df_performance, df_aggregated])
        #df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance

    def get_performance_aggregated_per_phase_multitenant(self, type="stream"):
        """
        Loops over multiple experiments and combines their aggregated performance results into a single DataFrame.

        For each experiment code, this function:
        - Initializes a benchmarking evaluator
        - Retrieves the corresponding workload configuration
        - Extracts aggregated performance metrics per client
        - Annotates the results with workload metadata (`type` and `num_tenants`)
        - Concatenates the results into a single DataFrame

        :return: A combined DataFrame containing aggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_performance_single(evaluation)
            df = evaluation.benchmarking_set_datatypes(df)
            df['type_tenants'] = workload['tenant_per']
            df['num_tenants'] = workload['num_tenants']
            df['vol_tenants'] = workload['multi_tenant_volume']
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df, columns=['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants'])
            #df_aggregated.index = evaluation.code + '-' + df_aggregated.index.astype(str)
            df_aggregated['phase'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['phase'].astype(str)
            df_aggregated['configuration'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['configuration'].astype(str)
            #df_aggregated.drop('connection', axis=1, inplace=True)
            #df = self.get_performance(evaluation)
            if df_aggregated.empty:
                continue
            #print(df)
            df_aggregated['type_tenants'] = workload['tenant_per']
            df_aggregated['num_tenants'] = workload['num_tenants']
            df_aggregated['vol_tenants'] = workload['multi_tenant_volume']
            #df['code']=code
            df_aggregated['code'] = df_aggregated['code'].astype(str)
            df_aggregated = df_aggregated.drop(columns=['pod', 'connection', 'phase'], errors='ignore')
            #print(df)
            df_performance = pd.concat([df_performance, df_aggregated])
        #df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance

    def get_monitoring_aggregated_per_phase_multitenant(self, type="stream"):
        df = self.get_monitoring_aggregated_per_phase(type)
        df_metadata = self.add_metadata(df)
        agg_dict = df.columns
        # Filter aggregation dictionary to only include columns present in df
        filtered_agg_dict = {col: 'max' if self.df_metrics.loc[self.df_metrics['title'] == col, 'metric'].item() == 'ratio' else 'sum' for col in agg_dict if col in df.columns}
        if 'Total I/O Wait Time [s]' in filtered_agg_dict:
            filtered_agg_dict['Total I/O Wait Time [s]'] = 'max'
        #print(filtered_agg_dict)
        # Apply groupby with filtered aggregation
        cols = ['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
        df_metadata = df_metadata.groupby(cols).agg(filtered_agg_dict)#.reset_index()
        df_metadata[cols] = pd.DataFrame(df_metadata.index.tolist(), index=df_metadata.index)
        df_metadata.index = ['_'.join(map(str, i)) for i in df_metadata.index]
        #df_metadata = self.add_metadata(df_metadata)
        return df_metadata

    def get_performance_per_connection(self):
        """
        Loops over multiple experiments and combines their unaggregated performance results into a single DataFrame.

        For each experiment code, this function:
        - Initializes a benchmarking evaluator
        - Retrieves the corresponding workload configuration
        - Extracts unaggregated performance metrics per client
        - Annotates the results with workload metadata (`type` and `num_tenants`)
        - Concatenates the results into a single DataFrame

        :return: A combined DataFrame containing unaggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_performance_single(evaluation)
            #df['type']=workload['tenant_per']
            #df['num_tenants']=workload['num_tenants']
            #df['vol_tenants']=workload['multi_tenant_volume']
            #df['code']=code
            #print(df)
            df['phase'] = df['code'].astype(str) + "-" + df['phase'].astype(str)
            df['connection'] = df['code'].astype(str) + "-" + df['connection'].astype(str)
            df['configuration'] = df['code'].astype(str) + "-" + df['configuration'].astype(str)
            df.index = evaluation.code + '-' + df.index.astype(str)
            #print(df)
            df_performance = pd.concat([df_performance, df])
        #df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance

    def OLD_get_performance_all_single(self):
        """
        Loops over multiple experiments and combines their unaggregated performance results into a single DataFrame.

        For each experiment code, this function:
        - Initializes a benchmarking evaluator
        - Retrieves the corresponding workload configuration
        - Extracts unaggregated performance metrics per client
        - Annotates the results with workload metadata (`type` and `num_tenants`)
        - Concatenates the results into a single DataFrame

        :return: A combined DataFrame containing unaggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_performance_single(evaluation)
            #df['type']=workload['tenant_per']
            #df['num_tenants']=workload['num_tenants']
            #df['vol_tenants']=workload['multi_tenant_volume']
            #df['code']=code
            #print(df)
            df_performance = pd.concat([df_performance, df])
        #df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance


    def get_metrics(self, evaluation=None):
        """
        Returns information about hardware metrics that were collected during the experiment.

        This function reads the `connections.config` file associated with the given evaluation,
        extracts and organizes the monitored hardware metrics, and returns them in a structured DataFrame.

        The resulting DataFrame includes, for each metric:
        - `title`: A descriptive name
        - `active`: Whether the metric was active during monitoring
        - `type`: The type/category of the metric (e.g., 'cluster')
        - `metric`: The raw metric name or identifier

        :param evaluation: The evaluation object containing the experiment code.
        :type evaluation: object
        :return: A DataFrame listing hardware metrics and their metadata.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            evaluation = self.get_evaluator()
        with open(self.path+"/"+evaluation.code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
            pretty_connections = json.dumps(connections, indent=2)
            #print(pretty_connections)
            connections_sorted = sorted(connections, key=lambda c: c['name'])
            result = dict()
            for c in connections_sorted:
                if not 'metrics' in c['monitoring']:
                    # no monitoring
                    self.with_monitoring = False
                    return pd.DataFrame()
                #print(c)
                for m, metric in c['monitoring']['metrics'].items():
                    if m in result:
                        continue
                    result[m] = {
                        'title': metric['title'],
                        'active': metric['active'] if 'active' in metric else 'True',
                        'type': metric['type'] if 'type' in metric else 'cluster',
                        'metric': metric['metric'] if 'metric' in metric else '',
                    }
            df = pd.DataFrame(result).T
            return df


    def get_connections_of_experiment(self, evaluation=None):
        """
        Returns info about all connections in the collection.
        Makes a loop over all codes and calls get_connections_of_experiment(evaluation).
        If evaluation is given, calls get_connections_of_experiment(evaluation).
        Important columns:
        df[['phase', 'code', 'connection', 'configuration', 'experiment_run', 'client', 'type_tenants', 'num_tenants', 'vol_tenants']]
        Code is added to phase and connection.

        :param evaluation: The evaluation object containing the experiment code.
        :type evaluation: object
        :return: A DataFrame listing connection infos.
        :rtype: pandas.DataFrame
        """
        def add_connection_to_result(c, connection_id, result):
            result[connection_id] = {
                'code': c['parameter']['code'],
                'connection': c['name'],
                'configuration': c['configuration'] if 'configuration' in c else '',
                'phase': c['phase'],
                'experiment_run': c['parameter']['numExperiment'],
                'client': int(c['parameter']['client']),
                'dockerimage': c['parameter']['dockerimage'],
                'time_load': c['timeLoad'],
                'time_ingest': c['timeIngesting'],
                'time_check': c['timeIndex'],
                'terminals': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS'] if 'BENCHBASE_TERMINALS' in c['parameter']['connection_parameter']['loading_parameters'] else 0,
                'pods': c['parameter']['parallelism'],
                'tenant': c['parameter']['TENANT'] if 'TENANT' in c['parameter'] else '',
                'num_worker': int(c['parameter']['num_worker']),
                'type_tenants': c['parameter']['TENANT_BY'] if 'TENANT_BY' in c['parameter'] else 'None',
                'num_tenants': int(c['parameter']['TENANT_NUM']) if 'TENANT_NUM' in c['parameter'] else 0,
                'vol_tenants': c['parameter']['TENANT_VOL'] if 'TENANT_VOL' in c['parameter'] else 'False',
                'datadisk': c['hostsystem']['datadisk'],
            }
            #df['type']=workload['tenant_per']
            #df['num_tenants']=workload['num_tenants']
            #df['vol_tenants']=workload['multi_tenant_volume']
            for key, hostdata in c['hostsystem'].items():
                if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                    result[connection_id][f'host_{key}'] = hostdata
            if 'loading_parameters' in c['parameter']['connection_parameter']:
                for key, hostdata in c['parameter']['connection_parameter']['loading_parameters'].items():
                    if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                        result[connection_id][f'loading_parameters_{key}'] = hostdata
            if 'benchmarking_parameters' in c['parameter']['connection_parameter']:
                for key, hostdata in c['parameter']['connection_parameter']['benchmarking_parameters'].items():
                    if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                        result[connection_id][f'benchmarking_parameters_{key}'] = hostdata
            if 'sut_parameters' in c['parameter']['connection_parameter']:
                for key, hostdata in c['parameter']['connection_parameter']['sut_parameters'].items():
                    if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                        result[connection_id][f'sut_parameters_{key}'] = hostdata
            if 'args' in c['hostsystem']:
                for key, arg in enumerate(c['hostsystem']['args']):
                    if "=" in arg:
                        key = arg.split("=")[0]
                        value = arg.split("=")[1]
                        result[connection_id][f'arg_{key}'] = value
        if evaluation is None:
            evaluation = self.get_evaluator()
        with open(self.path+"/"+evaluation.code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
            pretty_connections = json.dumps(connections, indent=2)
            #print(pretty_connections)
            connections_sorted = sorted(connections, key=lambda c: c['name'])
            result = dict()
            for c in connections_sorted:
                #pprint.pp(c)
                if 'orig_name' in c:
                    # go from pod identifier to connection identifier
                    name = c['orig_name']
                    c['phase'] = "{code}-{connection}".format(code=c['parameter']['code'], connection=name)
                    connection_id = "{code}-{connection}".format(code=c['parameter']['code'], connection=name)
                    add_connection_to_result(c, connection_id, result)
                else:
                    # simulate having connection (per pod)
                    clients = int(c['parameter']['parallelism'])
                    name = c['name']
                    for i in range(1, clients+1):
                        c['name'] = "{code}-{phase}-{client}".format(code=c['parameter']['code'], phase=name, client=i)
                        c['phase'] = "{code}-{phase}".format(code=c['parameter']['code'], phase=name)
                        connection_id = "{code}-{phase}-{client}".format(code=c['parameter']['code'], phase=name, client=i)
                        add_connection_to_result(c, connection_id, result)
            df = pd.DataFrame(result).T
            return df

    def get_connections(self, evaluation=None):
        """
        Returns info about all connections in the collection.
        Makes a loop over all codes and calls get_connections_of_experiment(evaluation).
        If evaluation is given, calls get_connections_of_experiment(evaluation).
        Important columns:
        df[['phase', 'code', 'connection', 'configuration', 'experiment_run', 'client', 'type_tenants', 'num_tenants', 'vol_tenants']]
        Code is added to phase and connection.

        :param evaluation: The evaluation object containing the experiment code.
        :type evaluation: object
        :return: A DataFrame listing connection infos.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            df_connections = pd.DataFrame()
            for code in self.codes:
                evaluation = self.get_evaluator(code)
                df_connection = self.get_connections_of_experiment(evaluation)
                df_connections = pd.concat([df_connections, df_connection])
            return df_connections
        else:
            #evaluation = self.get_evaluator()
            df_connection = self.get_connections_of_experiment(evaluation)
            return df_connection



    def OLD_get_loading_time_max(self, evaluation=None):
        """
        Collects information about the loading processes from the experiment configuration.

        This function reads the `connections.config` file associated with the given evaluation,
        extracts metadata related to data loading operations for each connection, and returns
        the results as a DataFrame.

        The resulting DataFrame includes, for each connection:
        - `time_load`: Total time taken for the load phase
        - `time_ingest`: Time spent ingesting data
        - `time_check`: Time spent indexing or verifying the data
        - `terminals`: Number of BenchBase terminals used
        - `pods`: Degree of parallelism (e.g., number of pods or workers)
        - `tenant`: Tenant identifier (if applicable)
        - `client`: Client name or identifier
        - `datadisk`: Size of the data disk used on the host system (in MB)

        :param evaluation: The evaluation object containing the experiment code.
        :type evaluation: object
        :return: A DataFrame with loading-related metrics and parameters for each connection.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            evaluation = self.get_evaluator()
        with open(self.path+"/"+evaluation.code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
            pretty_connections = json.dumps(connections, indent=2)
            #print(pretty_connections)
            connections_sorted = sorted(connections, key=lambda c: c['name'])
            result = dict()
            for c in connections_sorted:
                #print(c)
                result[c['name']] = {
                    'time_load': c['timeLoad'],
                    'time_ingest': c['timeIngesting'],
                    'time_check': c['timeIndex'],
                    'terminals': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS'] if 'BENCHBASE_TERMINALS' in c['parameter']['connection_parameter']['loading_parameters'] else 0,
                    'pods': c['parameter']['parallelism'],
                    'tenant': c['parameter']['TENANT'] if 'TENANT' in c['parameter'] else '',
                    'client': int(c['parameter']['client']),
                    'num_worker': int(c['parameter']['num_worker']),
                    'datadisk': c['hostsystem']['datadisk'],
                }
            df = pd.DataFrame(result).T
            return df


    def OLD_get_loading_time_max_all(self):
        """
        Collects loading process information for a list of experiments and combines the results into a single DataFrame.

        For each experiment code in the input list, this function:
        - Initializes a benchmarking evaluator
        - Retrieves workload metadata
        - Extracts loading-related metrics for each connection
        - Annotates the data with workload attributes (`type`, `num_tenants`)
        - Appends the result to a cumulative DataFrame

        The resulting DataFrame provides a consolidated view of the loading phase across multiple experiments,
        including timings, configuration parameters, and hardware context.

        :return: A combined DataFrame containing loading metrics and metadata for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_loading_time_max(evaluation)
            df['type_tenants']=workload['tenant_per']
            df['num_tenants']=workload['num_tenants']
            df['vol_tenants']=workload['multi_tenant_volume']
            df['code']=code
            #print(df)
            df_performance = pd.concat([df_performance, df])
        df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type_tenants'])
        return df_performance


    def OLD_show_summary_monitoring_table(self, evaluate, component):
        """
        Collects hardware and application monitoring metrics for a specified component without aggregation.

        This function retrieves multiple monitoring metrics from the evaluation object related to
        CPU usage, memory, PostgreSQL activity, cache statistics, and background writer performance.
        Each metric is processed (e.g., max-min differences, means, or max values) and combined into a single DataFrame.

        Aggregation is defined here manually per metric.

        :param evaluate: The evaluation object containing monitoring data and methods to retrieve metrics.
        :type evaluate: object
        :param component: The component name for which to retrieve metrics (e.g., 'database', 'worker').
        :type component: str
        :return: A DataFrame combining all monitored metrics indexed by monitored entities.
        :rtype: pandas.DataFrame
        """
        # Define metrics with the processing method and resulting column name
        metrics_info = [
            ('total_cpu_util_s', 'diff', 'CPU [CPUs]'),
            ('total_cpu_throttled', 'max', 'CPU Throttled'),
            ('total_cpu_util', 'max', 'Max CPU'),
            ('total_cpu_memory', 'max', 'Max RAM [Gb]', 1./1024.),
            ('total_cpu_memory_cached', 'max', 'Max RAM Cached [Gb]', 1./1024.),
            ('pg_locks_count', 'mean', 'Locks'),
            ('pg_locks_count_accessexclusivelock', 'mean', 'Access Exclusive'),
            ('pg_locks_count_accesssharelock', 'mean', 'Access Share'),
            ('pg_locks_count_exclusivelock', 'mean', 'Exclusive'),
            ('pg_locks_count_rowexclusivelock', 'mean', 'Row Exclusive'),
            ('pg_locks_count_rowsharelock', 'mean', 'Row Share'),
            ('pg_locks_count_sharelock', 'mean', 'Share'),
            ('pg_locks_count_sharerowexclusivelock', 'mean', 'Share Row Exclusive'),
            ('pg_locks_count_shareupdateexclusivelock', 'mean', 'Share Update Exclusive'),
            ('pg_locks_count_sireadlock', 'mean', 'SI Read'),
            ('pg_stat_activity_count_active', 'mean', 'Active'),
            ('pg_stat_activity_count_idle', 'mean', 'Idle'),
            ('pg_stat_activity_count_idle_transaction', 'mean', 'Transactions Idle'),
            ('pg_stat_activity_count_idle_transaction_aborted', 'max', 'Transactions Aborted'),
            ('pg_stat_database_blks_hit', 'diff', 'Block Hits'),
            ('pg_stat_database_blks_read', 'diff', 'Block Reads'),
            ('pg_statio_user_tables_heap_blocks_read', 'diff', 'Heap Reads'),
            ('pg_statio_user_tables_heap_blocks_hit', 'diff', 'Heap Hits'),
            ('pg_stat_bgwriter_checkpoint_sync_time_total', 'diff', 'Sync Time'),
            ('pg_stat_bgwriter_checkpoint_write_time_total', 'diff', 'Write Time'),
            ('cache_hit_ratio', 'mean', 'Cache Hit Ratio [%]', 100.0),
            ('pg_stat_user_tables_autoanalyze_count', 'diff', 'Number Autoanalyze'),
            ('pg_stat_user_tables_autovacuum_count', 'diff', 'Number Autovacuum'),
            ('core_variance', 'mean', 'Variance of Core Util [%]'),
        ]
        results = []
        for metric in metrics_info:
            metric_name = metric[0]
            method = metric[1]
            col_name = metric[2]
            scale = metric[3] if len(metric) > 3 else 1
            df = evaluate.get_monitoring_metric(metric=metric_name, component=component)
            # Apply scaling if needed
            if scale != 1:
                df = df * scale
            # Process dataframe according to method
            if method == 'diff':
                processed = df.max().sort_index() - df.min().sort_index()
            elif method == 'max':
                processed = df.max().sort_index()
            elif method == 'mean':
                processed = df.mean().sort_index()
            else:
                raise ValueError(f"Unknown processing method: {method}")
            df_cleaned = pd.DataFrame(processed)
            df_cleaned.columns = [col_name]
            results.append(df_cleaned)
        # Combine all dataframes horizontally (join on index)
        summary_df = pd.concat(results, axis=1).round(2)
        summary_df = summary_df.reindex(index=evaluators.natural_sort(summary_df.index))
        return summary_df

    def show_summary_monitoring_table(self, evaluation, type='stream'):
        """
        Collects hardware and application monitoring metrics for a specified component without aggregation.

        This function retrieves multiple monitoring metrics from the evaluation object related to
        CPU usage, memory, PostgreSQL activity, cache statistics, and background writer performance.
        Each metric is processed (e.g., max-min differences, means, or max values) and combined into a single DataFrame.

        :param evaluate: The evaluation object containing monitoring data and methods to retrieve metrics.
        :type evaluate: object
        :param component: The component name for which to retrieve metrics (e.g., 'database', 'worker').
        :type component: str
        :return: A DataFrame combining all monitored metrics indexed by monitored entities.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        #scale = 1
        results = []
        for idx, row in self.df_metrics.iterrows():
            if row["active"] == False:
                continue
            metric_name = idx
            method = 'diff' if row["metric"] == 'counter' else 'mean'
            #method = 'diff' if row["metric"] == 'counter' else 'max' if row["metric"] == 'ratio' else 'mean'
            col_name = row["title"]
            #print(idx, row["title"], method)
            #scale = metric[3] if len(metric) > 3 else 1
            df = evaluation.get_monitoring_metric(metric=metric_name, component=type)
            # Apply scaling if needed
            #if scale != 1:
            #    df = df * scale
            # Process dataframe according to method
            if method == 'diff':
                processed = df.max().sort_index() - df.min().sort_index()
            elif method == 'max':
                processed = df.max().sort_index()
            elif method == 'mean':
                processed = df.mean().sort_index()
            else:
                raise ValueError(f"Unknown processing method: {method}")
            df_cleaned = pd.DataFrame(processed)
            df_cleaned.columns = [col_name]
            #df_cleaned.index = evaluation.code + '-' + df_cleaned.index.astype(str)
            results.append(df_cleaned)
            #print(results)
        # Combine all dataframes horizontally (join on index)
        summary_df = pd.concat(results, axis=1).round(2)
        #summary_df = summary_df.reindex(index=evaluators.natural_sort(summary_df.index))
        return summary_df

    def get_monitoring_timeseries_single(self, code, metric='pg_locks_count', component="stream"):
        """
        Retrieves a single monitoring metric as a time series DataFrame for a given experiment code and component.

        The function initializes the evaluation object for the specified experiment,
        then fetches the time series data for the specified metric and component.

        :param code: The experiment identifier code.
        :type code: str
        :param metric: The name of the monitoring metric to retrieve (default is 'pg_locks_count').
        :type metric: str, optional
        :param component: The component name to filter metrics (default is 'stream').
        :type component: str, optional
        :return: A DataFrame containing the time series of the requested metric indexed by timestamps or monitoring targets.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        evaluate = self.get_evaluator(code)
        df = evaluate.get_monitoring_metric(metric=metric, component=component)
        return df


    def OLD_get_monitoring(self, evaluation, type="stream"):
        """
        Retrieves and aggregates monitoring metrics for a specified component type, grouped by client.

        This function obtains detailed monitoring data using `show_summary_monitoring_table` for the
        specified component type (default "stream"). It adds connection columns.
        then aggregates various hardware and application metrics by code, experiment_run and client using sum or mean as appropriate.

        Aggregation is by summation except for type "ratio", which aggregates via max.

        :param evaluation: The evaluation object containing monitoring data.
        :type evaluation: object
        :param type: The component type to filter monitoring metrics (default is "stream").
        :type type: str, optional
        :return: A DataFrame with aggregated monitoring metrics grouped by client. If no data is available, returns None.
        :rtype: pandas.DataFrame or None
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_monitoring = self.show_summary_monitoring_table(evaluation, type)
        if len(df_monitoring) > 0:
            #print(df_monitoring)
            df = df_monitoring.copy()  # avoid modifying original
            df_connections = self.get_connections(evaluation)
            df = df.join(df_connections)
            #print(df)
            #df['client'] = df.index.str.rsplit('-', n=1).str[-1]
            #print(df)
            agg_dict = df_monitoring.columns
            # Filter aggregation dictionary to only include columns present in df
            filtered_agg_dict = {col: 'max' if self.df_metrics.loc[self.df_metrics['title'] == col, 'metric'].item() == 'ratio' else 'sum' for col in agg_dict if col in df.columns}
            if 'Total I/O Wait Time [s]' in filtered_agg_dict:
                filtered_agg_dict['Total I/O Wait Time [s]'] = 'max'
            #print(filtered_agg_dict)
            # Apply groupby with filtered aggregation
            result = df.groupby(['experiment_run', 'client']).agg(filtered_agg_dict).reset_index()
            return result



    def OLD_get_monitoring(self, evaluation, type="stream"):
        """
        Retrieves and aggregates monitoring metrics for a specified component type, grouped by client.

        This function obtains detailed monitoring data using `show_summary_monitoring_table` for the
        specified component type (default "stream"). It adds a 'client' column extracted from the DataFrame index,
        then aggregates various hardware and application metrics by client using sum or mean as appropriate.

        Aggregation is defined here manually per metric.

        :param evaluation: The evaluation object containing monitoring data.
        :type evaluation: object
        :param type: The component type to filter monitoring metrics (default is "stream").
        :type type: str, optional
        :return: A DataFrame with aggregated monitoring metrics grouped by client. If no data is available, returns None.
        :rtype: pandas.DataFrame or None
        """
        df_monitoring = self.show_summary_monitoring_table(evaluation, type)
        if len(df_monitoring) > 0:
            df = df_monitoring.copy()  # avoid modifying original
            df['client'] = int(df.index.str.rsplit('-', n=1).str[-1])
            agg_dict = {
                'CPU [CPUs]': 'sum',
                'Max RAM [Gb]': 'sum',
                'Max RAM Cached [Gb]': 'sum',
                'Max CPU': 'sum',
                'CPU Throttled': 'sum',
                'Locks': 'sum',
                'Access Exclusive': 'sum',
                'Access Share': 'sum',
                'Exclusive': 'sum',
                'Row Exclusive': 'sum',
                'Row Share': 'sum',
                'Share': 'sum',
                'Share Row Exclusive': 'sum',
                'Share Update Exclusive': 'sum',
                'SI Read': 'sum',
                'Active': 'sum',
                'Idle': 'sum',
                'Transactions Idle': 'sum',
                'Transactions Aborted': 'sum',
                'Block Hits': 'sum',
                'Block Reads': 'sum',
                'Heap Reads': 'sum',
                'Heap Hits': 'sum',
                'Sync Time': 'sum',
                'Write Time': 'sum',
                'Number Autoanalyze': 'sum',
                'Number Autovacuum': 'sum',
                'Cache Hit Ratio [%]': 'mean',
                'Variance of Core Util [%]': 'max',
            }
            # Filter aggregation dictionary to only include columns present in df
            filtered_agg_dict = {col: func for col, func in agg_dict.items() if col in df.columns}
            # Apply groupby with filtered aggregation
            result = df.groupby(['experiment_run', 'client']).agg(filtered_agg_dict).reset_index()
            return result


    def OLD_get_monitoring_all(self, type="stream"):
        """
        Aggregates monitoring metrics across multiple experiments for a specified component type.

        For each experiment code provided, this function:
        - Initializes the evaluation object,
        - Retrieves workload metadata,
        - Collects aggregated monitoring metrics for the specified component type,
        - Adds workload-related metadata columns ('type' and 'num_tenants'),
        - Concatenates the results into a single DataFrame.

        :param type: The component type to filter monitoring metrics (default is "stream").
        :type type: str, optional
        :return: A concatenated DataFrame containing aggregated monitoring metrics for all experiments,
                 enriched with workload metadata.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_monitoring(evaluation, type)
            if df is None:
                print(code, df)
                continue
            df['type'] = workload['tenant_per']
            df['num_tenants'] = workload['num_tenants']
            df['vol_tenants'] = workload['multi_tenant_volume']
            df['code']=code
            df_performance = pd.concat([df_performance, df])
        df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance


    def OLD_get_monitoring_single_all(self, type="stream"):
        """
        Retrieves non-aggregated monitoring metrics for multiple experiments and combines them into a single DataFrame.

        For each experiment code, this function:
        - Initializes the evaluation object,
        - Retrieves workload metadata,
        - Collects detailed monitoring metrics for the specified component type without aggregation across clients,
        - Adds workload-related metadata columns ('type' and 'num_tenants'),
        - Concatenates the results into a single DataFrame.

        :param type: The component type to filter monitoring metrics (default is "stream").
        :type type: str, optional
        :return: A DataFrame containing detailed (non-aggregated) monitoring metrics for all experiments,
                 enriched with workload metadata.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df_monitoring = self.show_summary_monitoring_table(evaluation, type)
            if len(df_monitoring) > 0:
                df = df_monitoring.copy()  # avoid modifying original
                #df_connections = self.get_connections(evaluation)
                #df = df.join(df_connections)
                #df['client'] = df.index.str.rsplit('-', n=1).str[-1]
                #df['type'] = workload['tenant_per']
                #df['num_tenants'] = workload['num_tenants']
                #df['vol_tenants']=workload['multi_tenant_volume']
                #df['code']=code
                df_performance = pd.concat([df_performance, df])
        df_performance = df_performance.sort_values(['num_tenants', 'vol_tenants', 'type'])
        return df_performance

    def get_monitoring_aggregated_per_phase(self, type="stream"):
        """
        Retrieves aggregated monitoring metrics for multiple experiments and combines them into a single DataFrame.
        Drops column "connection" if exists, since it is not sensible anymore.

        :param type: The component type to filter monitoring metrics (default is "stream").
        :type type: str, optional
        :return: A DataFrame containing detailed (aggregated) monitoring metrics for all experiments
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            #workload = self.get_workload(code)
            df_monitoring = self.show_summary_monitoring_table(evaluation, type)
            if len(df_monitoring) > 0:
                df = df_monitoring.copy()  # avoid modifying original
                df_performance = pd.concat([df_performance, df])
        df_performance.drop('connection', axis=1, inplace=True, errors='ignore')
        return df_performance

    def get_monitoring_timeseries_per_phase(self, code, metric='pg_locks_count', component="stream"):
        """
        Retrieves a single monitoring metric as a time series DataFrame for a given experiment code and component.

        The function initializes the evaluation object for the specified experiment,
        then fetches the time series data for the specified metric and component.

        :param code: The experiment identifier code.
        :type code: str
        :param metric: The name of the monitoring metric to retrieve (default is 'pg_locks_count').
        :type metric: str, optional
        :param component: The component name to filter metrics (default is 'stream').
        :type component: str, optional
        :return: A DataFrame containing the time series of the requested metric indexed by timestamps or monitoring targets.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        evaluate = self.get_evaluator(code)
        df = evaluate.get_monitoring_metric(metric=metric, component=component)
        return df.T

    def add_metadata(self, df):
        """
        Retrieves non-aggregated monitoring metrics for multiple experiments and combines them into a single DataFrame.

        For each experiment code, this function:
        - Initializes the evaluation object,
        - Retrieves workload metadata,
        - Collects detailed monitoring metrics for the specified component type without aggregation across clients,
        - Adds workload-related metadata columns ('type' and 'num_tenants'),
        - Concatenates the results into a single DataFrame.

        :param type: The component type to filter monitoring metrics (default is "stream").
        :type type: str, optional
        :return: A DataFrame containing detailed (non-aggregated) monitoring metrics for all experiments,
                 enriched with workload metadata.
        :rtype: pandas.DataFrame
        """
        df_connections = self.get_connections()
        intersection = df.index.intersection(df_connections['phase'])
        if not intersection.empty:
            phase_dropped = False
            # index of df is per phase
            print("combine on index and column 'phase'")
            if 'phase' in df.columns:
                #print("drop duplicate column 'phase'")
                df.drop('phase', axis=1, inplace=True)
                phase_dropped = True
            #df_phases = df_connections.drop_duplicates(subset=['phase'], keep='first')
            #result = df.merge(df_phases, left_index=True, right_on='phase', how='inner').set_index('phase')
            cols_to_use = [c for c in df_connections.columns if c not in df.columns or c == 'phase']
            #print(cols_to_use)
            result = df.merge(
                df_connections[cols_to_use].drop_duplicates('phase'),
                left_index=True,
                right_on='phase',
                how='inner'
            ).set_index('phase').copy()
            #if phase_dropped:
            result['phase'] = result.index
            result.drop('connection', axis=1, inplace=True, errors='ignore')
            return result
        cols_phase = ['phase']
        cols_multi_tenant = ['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
        check_phase = all(set(cols_phase).issubset(d.columns) for d in [df, df_connections])
        check_multi_tenant = all(set(cols_multi_tenant).issubset(d.columns) for d in [df, df_connections])
        #df_connections = df_connections.drop_duplicates(subset=cols, keep='first')
        #df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
        #df = df.set_index(cols, drop=False)
        #df_connections = df_connections.set_index(cols, drop=False)
        #df_connections = df_connections.drop_duplicates('phase'),
        #print(df.head())
        #print(df_connections.head())
        # 2. Kombinieren (df hat Vorrang, df_connections füllt NaN auf)
        #print(df)
        #print(df_connections)
        #result = df.combine_first(df_connections)#.reindex(columns=df.columns)
        #result
        intersection = df.index.intersection(df_connections.index)
        if not intersection.empty:
            print("combine on index")
            #result = df.combine_first(df_connections).reindex(columns=df.columns)
            # 1. Spalten finden, die NUR in df_connections existieren
            cols_to_use = [c for c in df_connections.columns if c not in df.columns]
            # 2. Diese Spalten rechts an df hängen
            result = df.join(df_connections[cols_to_use], how='inner')
            #result = pd.concat([df, df_connections[cols_to_use]], axis=1)
            #result = result.sort_values(['code', 'experiment_run', 'client'])
            return result
        elif check_phase:
            print("combine on columns " + " ".join(cols_phase))
            #df = df.rename_axis('phase').reset_index()
            indexname = df.index.name
            df_connections = df_connections.drop_duplicates(subset=cols_phase, keep='first')
            df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
            df = df.set_index(cols_phase, drop=False)
            df_connections = df_connections.set_index(cols_phase, drop=False)
            #df_connections = df_connections.drop_duplicates('phase'),
            #print(df.head())
            #print(df_connections.head())
            # 2. Kombinieren (df hat Vorrang, df_connections füllt NaN auf)
            #print(df)
            #print(df_connections)
            result = df.combine_first(df_connections)#.reindex(columns=df.columns)
            result.index.name = indexname
            # 1. Spalten finden, die NUR in df_connections existieren
            #cols_to_use = [c for c in df_connections.columns if c not in df.columns]
            # 2. Diese Spalten rechts an df hängen
            #print(f"df Duplikate: {df.index.duplicated().any()}")
            #print(f"df_connections Duplikate: {df_connections.index.duplicated().any()}")
            #result = pd.concat([df, df_connections[cols_to_use]], axis=1)
            #print(result.index)
            # 3. Spalten aus dem Index zurückholen
            #result = result.reset_index()
            #result = result.set_index('phase')
            #result = result.sort_values(['code', 'experiment_run', 'client'])
            return result
        elif check_multi_tenant:
            print("combine on columns " + " ".join(cols_multi_tenant))
            #df = df.rename_axis('phase').reset_index()
            indexname = df.index.name
            df_connections = df_connections.drop_duplicates(subset=cols_multi_tenant, keep='first')
            df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
            df = df.set_index(cols_multi_tenant, drop=False)
            df_connections = df_connections.set_index(cols_multi_tenant, drop=False)
            df.index = pd.MultiIndex.from_tuples(
                [tuple(map(str, t)) for t in df.index], 
                names=df.index.names
            )
            df_connections.index = pd.MultiIndex.from_tuples(
                [tuple(map(str, t)) for t in df_connections.index], 
                names=df_connections.index.names
            )
            #print(df.index)
            #print(df_connections.index)
            #df_connections = df_connections.drop_duplicates('phase'),
            #print(df.head())
            #print(df_connections.head())
            # 2. Kombinieren (df hat Vorrang, df_connections füllt NaN auf)
            #print(df)
            #print(df_connections)
            result = df.combine_first(df_connections)#.reindex(columns=df.columns)
            result.index = ['_'.join(map(str, i)) for i in result.index]
            #result.index.name = indexname
            # 1. Spalten finden, die NUR in df_connections existieren
            #cols_to_use = [c for c in df_connections.columns if c not in df.columns]
            # 2. Diese Spalten rechts an df hängen
            #print(f"df Duplikate: {df.index.duplicated().any()}")
            #print(f"df_connections Duplikate: {df_connections.index.duplicated().any()}")
            #result = pd.concat([df, df_connections[cols_to_use]], axis=1)
            #print(result.index)
            # 3. Spalten aus dem Index zurückholen
            #result = result.reset_index()
            #result = result.set_index('phase')
            #result = result.sort_values(['code', 'experiment_run', 'client'])
            return result
        else:
            print("combine failed!")            
        #for code in self.codes:
        #    evaluation = self.get_evaluator(code)
        #    df_connections = self.get_connections(evaluation)
        #    df = df.combine_first(df_connections)#, lsuffix='_left', rsuffix='_right')
        #    print(df_connections)
        #df = df.sort_values(['code', 'experiment_run', 'client'])
        #return df


    def get_monitoring_timeseries_all(self, metric='pg_locks_count', component="stream"):
        if not self.with_monitoring:
            #print("no monitoring")
            return pd.DataFrame()
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df_connections = self.get_connections(evaluation)
            df_monitoring = self.get_monitoring_timeseries_single(code, metric=metric)
            df_monitoring.index.name="timestamp"
            #print(df_monitoring.head())
            #print(df_connections.head())
            df_long = df_monitoring.reset_index().melt(
                id_vars="timestamp",     # keep timestamp
                var_name="series",       # column name for former column headers
                value_name="value"       # column name for the numbers
            )
            #df_long['client'] = df_long['series'].str.rsplit('-', n=1).str[-1]
            df_long['metric'] = metric
            df_long['component'] = component
            #print(df_long['series'].head())
            #print(df_connections['phase'].head())
            df_long = pd.merge(df_long, df_connections, left_on='series', right_on='phase', how='left')
            #print(df_long.head())
            #if workload['tenant_per'] == 'container':
            #    # 1 time series per tenant
            #    pass
            #else:
            #    # 1 time series for all tenants (it is 1 DBMS)
            #    df_long['tenant'] = "0"
            #df_long['type_tenants'] = workload['tenant_per']
            #df_long['num_tenants'] = workload['num_tenants']
            #df_long['vol_tenants'] = workload['multi_tenant_volume']
            df_performance = pd.concat([df_performance, df_long])
        #print(df_performance)
        df_sum = (
            df_performance
            #.groupby(["timestamp", "code", "experiment_run", "client", "type_tenants", 'vol_tenants', "num_tenants", "metric", "component"], as_index=False)["value"]
            .groupby(["timestamp", "code", "phase", "experiment_run", "client", "type_tenants", 'vol_tenants', "num_tenants", "metric", "component"], as_index=False)["value"]
            #.groupby(["timestamp", "code", "phase", "experiment_run", "client", "metric", "component"], as_index=False)["value"]
            .sum()
        )
        #df_sum.drop(columns=['timestamp'], inplace=True)
        #print(df_performance.head())
        #print(df_sum.head())
        return df_sum

    def get_monitoring_timeseries_all_multitenant(self, metric='pg_locks_count', component="stream"):
        if not self.with_monitoring:
            return pd.DataFrame()
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df_connections = self.get_connections(evaluation)
            df_monitoring = self.get_monitoring_timeseries_single(code, metric=metric)
            df_monitoring.index.name="timestamp"
            df_long = df_monitoring.reset_index().melt(
                id_vars="timestamp",     # keep timestamp
                var_name="series",       # column name for former column headers
                value_name="value"       # column name for the numbers
            )
            #df_long['client'] = df_long['series'].str.rsplit('-', n=1).str[-1]
            df_long['metric'] = metric
            df_long['component'] = component
            df_long = pd.merge(df_long, df_connections, left_on='series', right_on='phase', how='left')
            if workload['tenant_per'] == 'container':
                # 1 time series per tenant
                pass
            else:
                # 1 time series for all tenants (it is 1 DBMS)
                df_long['tenant'] = "0"
            df_long['type_tenants'] = workload['tenant_per']
            df_long['num_tenants'] = workload['num_tenants']
            df_long['vol_tenants'] = workload['multi_tenant_volume']
            df_performance = pd.concat([df_performance, df_long])
        df_sum = (
            df_performance
            .groupby(["timestamp", "code", "experiment_run", "client", "type_tenants", 'vol_tenants', "num_tenants", "metric", "component"], as_index=False)["value"]
            #.groupby(["timestamp", "code", "phase", "experiment_run", "client", "type_tenants", 'vol_tenants', "num_tenants", "metric", "component"], as_index=False)["value"]
            .sum()
        )
        #df_sum.drop(columns=['timestamp'], inplace=True)
        #print(df_performance.head())
        #print(df_sum.head())
        return df_sum


    def OLD_get_evaluator(self, code=''):
        if code == '':
            code = self.codes[0]
        evaluation = inspector.inspector(self.path)
        evaluation.load_experiment(code=code, silent=True)
        evaluation.code = code
        return evaluation
        #return evaluators.base(code=code, path=self.path)

    def get_evaluator(self, code=''):
        if code == '':
            code = self.codes[0]
        return evaluators.dbmsbenchmarker(code=code, path=self.path)







"""
############################################################################
Benchbase
############################################################################
"""

class benchbase(default):
    """
    Class for evaluating Benchbase experiments.
    """
    def __init__(self,
            path,
            codes
            ):
        default.__init__(self, path, codes)


    def get_evaluator(self, code=''):
        if code == '':
            code = self.codes[0]
        return evaluators.benchbase(code=code, path=self.path)


