"""
Evaluator for Benchbase experiments.

Provides :class:`benchbase`, which extends :class:`logger` to parse and
aggregate throughput and latency results produced by the Benchbase
benchmarking tool.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import os
import re
import matplotlib.pyplot as plt

from bexhoma import evaluators
pd.set_option("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
import pickle
import json
import traceback
import ast
from dbmsbenchmarker import monitor
from datetime import datetime
import glob
from pathlib import Path

from .base import natural_sort
from .logger import logger



class benchbase(logger):
    """
    Evaluator for a Benchbase experiment.

    Parses per-pod log files to extract throughput, goodput, and latency
    distribution results produced by the Benchbase benchmarking tool.
    Also provides time-series access to per-second throughput metrics via
    :meth:`get_benchmark_logs_timeseries_df_aggregated` and
    :meth:`get_benchmark_logs_timeseries_df_single`.

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Whether loading-phase results are expected.
    :param include_benchmarking: Whether benchmarking-phase results are expected.
    """
    def log_to_df(self, filename):
        """
        Transforms a log file in text format into a pandas DataFrame.

        :param filename: Name of the log file 
        :return: DataFrame of results
        """
        # test for known errors
        logger.log_to_df(self, filename)
        # extract status and result fields
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            pod_name = filename[filename.rindex("-")+1:-len(".log")]
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)[0]
            duration = re.findall('BEXHOMA_DURATION:(.+?)\n', stdout)[0]
            configuration_name = re.findall('BEXHOMA_CONFIGURATION:(.+?)\n', stdout)[0]
            experiment_run = re.findall('BEXHOMA_EXPERIMENT_RUN:(.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            code = re.findall('BEXHOMA_EXPERIMENT:(.+?)\n', stdout)[0]
            error_timesynch = re.findall('start time has already passed', stdout)
            if len(error_timesynch) > 0:
                # log is incomplete
                return pd.DataFrame()
            pod_count = re.findall('BEXHOMA_NUM_PODS (.+?)\n', stdout)[0]
            bench = re.findall('BENCHBASE_BENCH (.+?)\n', stdout)[0]
            profile = re.findall('BENCHBASE_PROFILE (.+?)\n', stdout)[0]
            target = re.findall('BENCHBASE_TARGET (.+?)\n', stdout)[0]
            time = re.findall('BENCHBASE_TIME (.+?)\n', stdout)[0]
            batchsize = re.findall('BENCHBASE_BATCHSIZE (.+?)\n', stdout)[0]
            keyandthink = re.findall('BENCHBASE_KEY_AND_THINK (.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD (.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            errors = re.findall('error code', stdout)
            num_errors = len(errors)
            header = {
                'connection': connection_name + '-' + child,
                'phase': connection_name,
                'configuration': configuration_name,
                'experiment_run': experiment_run,
                'code': code,
                'client': client,
                'pod': pod_name,
                'pod_count': pod_count,
                'bench': bench,
                'profile': profile,
                'target': target,
                'time': time,
                'batchsize': batchsize,
                'sf': int(sf),
                'num_errors': num_errors,
                'duration': duration,
                'efficiency': 0.0,
                'child': child,
            }
            df_header = pd.DataFrame(header, index=[0])
            if True: # num_errors == 0:
                log = re.findall('####BEXHOMA####(.+?)####BEXHOMA####', stdout, re.DOTALL)
                if len(log) > 0:
                    result = json.loads(log[0])
                    df = pd.json_normalize(result)
                    #self.cluster.logger.debug(df)
                    df = pd.concat([df_header, df], axis=1)
                    df.index.name = connection_name
                    #print(df, keyandthink)
                    if keyandthink == "true" and bench == "tpcc":
                        df["efficiency"] = 0.45 * 60. * 100. * df['Goodput (requests/second)'] / 12.86 / df['sf']
                    #print(df)
                    return df
                else:
                    print("no results found in log file {}".format(filename))
                    return df_header
            else:
                return df_header#pd.DataFrame()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(stdout)
            return df_header
    def benchmarking_set_datatypes(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to suitable data types.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        df_typed = df.astype({
            'connection':'str',
            'phase':'str',
            'configuration':'str',
            'experiment_run':'int',
            'duration':'int',
            'client':'int',
            'code': 'int',
            'pod':'str',
            'pod_count':'int',
            'bench':'str',
            'profile':'str',
            'target':'int',
            'time':'float',
            #'terminals':'int',
            'batchsize':'int',
            'sf':'int',
            'num_errors':'int',
            'scalefactor':'int',
            'Current Timestamp (milliseconds)':'str',
            'Benchmark Type':'str',
            'isolation':'str',
            'DBMS Version':'str',
            'Goodput (requests/second)':'float',
            'terminals':'int',
            'DBMS Type':'str',
            'Throughput (requests/second)':'float',
            'Latency Distribution.95th Percentile Latency (microseconds)':'float',
            'Latency Distribution.Maximum Latency (microseconds)':'float',
            'Latency Distribution.Median Latency (microseconds)':'float',
            'Latency Distribution.Minimum Latency (microseconds)':'float',
            'Latency Distribution.25th Percentile Latency (microseconds)':'float',
            'Latency Distribution.90th Percentile Latency (microseconds)':'float',
            'Latency Distribution.99th Percentile Latency (microseconds)':'float',
            'Latency Distribution.75th Percentile Latency (microseconds)':'float',
            'Latency Distribution.Average Latency (microseconds)':'float',
            'efficiency': 'float',
            'child': 'int',
        })
        return df_typed
    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(columns):
            aggregate = {
                'connection':'max',
                'client':'max',
                'code':'max',
                'pod':'sum',
                'pod_count':'count',
                'duration':'max',
                'bench':'max',
                'profile':'max',
                'target':'sum',
                'time':'max',
                'batchsize':'mean',
                'sf':'max',
                'num_errors':'sum',
                'scalefactor':'max',
                'Current Timestamp (milliseconds)':'max',
                'Benchmark Type':'max',
                'isolation':'max',
                'DBMS Version':'max',
                'Goodput (requests/second)':'sum',
                'terminals':'sum',
                'DBMS Type':'max',
                'Throughput (requests/second)':'sum',
                'Latency Distribution.95th Percentile Latency (microseconds)':'max',
                'Latency Distribution.Maximum Latency (microseconds)':'max',
                'Latency Distribution.Median Latency (microseconds)':'max',
                'Latency Distribution.Minimum Latency (microseconds)':'min',
                'Latency Distribution.25th Percentile Latency (microseconds)':'max',
                'Latency Distribution.90th Percentile Latency (microseconds)':'max',
                'Latency Distribution.99th Percentile Latency (microseconds)':'max',
                'Latency Distribution.75th Percentile Latency (microseconds)':'max',
                'Latency Distribution.Average Latency (microseconds)':'mean',
                'efficiency': 'sum',
                'child': 'count',
            }
            dict_grp = dict()
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            key_index = "_".join(map(str, key))
            df_grp = pd.DataFrame(dict_grp, index=[key_index])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        mask = (df_aggregated['sf'] * 10 == df_aggregated['terminals']) & (df_aggregated['efficiency'] != 0.) & (df_aggregated['bench'] == "tpcc")
        #df_masked = df_aggregated[~mask]
        #print(mask, df_aggregated.loc[mask])
        df_aggregated['efficiency'] = 0.  # Default all rows to 0
        df_aggregated.loc[mask, 'efficiency'] = (
            0.45 * 60. * 100. * df_aggregated['Goodput (requests/second)'] / 12.86 / df_aggregated['sf']
        )
        return df_aggregated
    def parse_benchbase_log_file(self, file_path):
        """
        Scans the lines of a Benchbase log file.
        Extracts relevant performance infos for time series analysis.
        Each line starting with a time stamp is converted into a dict containing measurements (Throughput: txn/sec)

        :param file_path: Full path of log file
        :return: List of dicts of measures, one entry per line
        """
        datetime_first_measure = 0
        def parse_string(log):
            nonlocal datetime_first_measure
            #log = re.sub(r'Avg=�', 'Avg=0', log)
            try:
                # Extract the date and time
                pattern = r'\[INFO\s*\]\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s*\[([\w-]+)\].*?Throughput:\s*([\d\.]+) txn/sec'
                #print(pattern)
                #print(log)
                match = re.match(pattern, log)
                date_time, thread_id, throughput = match.groups()
                #print(date_time, thread_id, throughput)
                #print("----match")
                fmt = '%Y-%m-%d %H:%M:%S,%f'
                dt = datetime.strptime(date_time, fmt)
                if datetime_first_measure == 0:
                    datetime_first_measure = dt
                #print(datetime_first_measure, dt)
                second = int((dt - datetime_first_measure).total_seconds())
                return {
                    #"date_time": date_time,
                    "second": second, #date_time,
                    #"thread_id": thread_id,
                    "throughput": float(throughput),
                }
            except Exception as e:
                # Log or handle any parsing errors (optional)
                #print("----no match")
                #print(e)
                return None
        results = []
        with open(file_path, 'r') as file:
            for line in file:
                parsed_data = parse_string(line.strip())
                if parsed_data:
                    results.append(parsed_data)
        return results
    def benchmark_logs_to_timeseries_df(self, list_logs, metric="throughput", aggregate=True):
        """
        Parses Benchbase log files for the given pod IDs and assembles a time-series DataFrame.

        Each pod ID in ``list_logs`` is resolved to matching log files via a glob pattern.
        When ``aggregate`` is ``True`` the per-second metric values from all pods are
        combined into a single DataFrame: percentile/max metrics use the element-wise
        maximum, minimum metrics use the element-wise minimum, and all others are summed.
        When ``aggregate`` is ``False`` a list of per-pod DataFrames is returned instead.

        :param list_logs: Pod IDs (short suffixes) used to locate matching log files.
        :type list_logs: list[str]
        :param metric: Metric column to extract (default ``'throughput'``).
        :type metric: str
        :param aggregate: Whether to aggregate all pod DataFrames into one.
        :type aggregate: bool
        :return: Aggregated DataFrame indexed by ``'second'`` (with an ``'avg'`` column
                 appended) when ``aggregate`` is ``True``, or a list of per-pod DataFrames.
        :rtype: pandas.DataFrame or list[pandas.DataFrame]
        """
        column = metric
        remove_first = 0
        remove_last = 0
        def flatten_dict(d, parent_key='', sep='_'):
            """
            Flattens a nested dictionary so that nested keys are concatenated with a separator.

            :param d: Dictionary to flatten.
            :param parent_key: String to prepend to the keys (used during recursion).
            :param sep: Separator for concatenating keys.
            :return: Flattened dictionary.
            """
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k  # Concatenate parent and child keys
                if isinstance(v, dict):  # If value is a dictionary, recurse
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                else:  # Otherwise, add the key-value pair
                    items.append((new_key, v))
            return dict(items)
        def find_matching_files(directory, pattern):
            """
            Finds files in the specified directory that match the given pattern.

            :param directory: The path to the directory where the search is performed.
            :param pattern: The file pattern to match (e.g., "*.txt" for all text files).
            :return: A list of file paths that match the pattern.
            """
            # Use glob to find files matching the pattern
            matching_files = glob.glob(os.path.abspath(os.path.normpath(os.path.join(directory, pattern))))
            return matching_files
        if not aggregate:
            df_total = []
        else:
            df_total = pd.DataFrame()
        num_logs = 0
        for file_logs in list_logs:
            pattern = 'bexhoma-benchmarker-*-{}.log'.format(file_logs)
            matching_files = find_matching_files(self.path, pattern)
            for file in matching_files:
                num_logs = num_logs + 1
                parsed_results = self.parse_benchbase_log_file(file)
                df = pd.DataFrame(parsed_results)
                df = df.set_index('second')
                df = df.groupby(df.index).last()  # collapse duplicate timestamps
                if remove_first > 0:
                    df = df.iloc[remove_first:]
                if remove_last > 0:
                    df = df.iloc[:-remove_last]
                if not aggregate:
                    df_total.append(df.copy())
                else:
                    if df_total.empty:
                        df_total = df.copy()
                    else:
                        if "9" in metric or "Max" in metric:
                            df_total[column] = df_total[column].combine(df[column], lambda x, y: x if (x > y and pd.notna(x) and pd.notna(y)) or (pd.notna(x) and not pd.notna(y)) else y)
                        elif "Min" in metric:
                            df_total[column] = df_total[column].combine(df[column], lambda x, y: x if (x < y and pd.notna(x) and pd.notna(y)) or (pd.notna(x) and not pd.notna(y)) else y)
                        else:
                            df_total = df_total.add(df, fill_value=0)
        if aggregate:
            df_total['avg'] = int(df_total[column].mean())
        return df_total
    def get_benchmark_logs_timeseries_df_aggregated(self, metric="throughput", configuration="", client='1', experiment_run='1'):
        """
        Returns a DataFrame of time series of a metric for the benchmarking phase,
        aggregated over all pods per second.

        Retrieves pod IDs from :meth:`get_df_benchmarking` filtered by the given
        ``configuration``, ``client``, and ``experiment_run``, then delegates to
        :meth:`benchmark_logs_to_timeseries_df` with ``aggregate=True``.

        :param metric: Metric column to extract (default ``'throughput'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-64-8-65536'``).
        :type configuration: str
        :param client: Client number (default ``'1'``).
        :type client: str or int
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: DataFrame indexed by ``'second'`` with the metric and an ``'avg'`` column.
        :rtype: pandas.DataFrame
        """
        client = str(client)
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=True)
        return df_total
    def get_benchmark_logs_timeseries_df_single(self, metric="throughput", configuration="", client='1', experiment_run='1'):
        """
        Returns a list of DataFrames of time series of a metric for the benchmarking
        phase, one per pod.

        Retrieves pod IDs from :meth:`get_df_benchmarking` filtered by the given
        ``configuration``, ``client``, and ``experiment_run``, then delegates to
        :meth:`benchmark_logs_to_timeseries_df` with ``aggregate=False``.

        :param metric: Metric column to extract (default ``'throughput'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-64-8-65536'``).
        :type configuration: str
        :param client: Client number (default ``'1'``).
        :type client: str or int
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: List of DataFrames, one per pod, each indexed by ``'second'``.
        :rtype: list[pandas.DataFrame]
        """
        client = str(client)
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)
        return df_total
    def get_summary_benchmark_per_connection(self):
        df = self.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            #print("\n### Execution")
            #print("\n#### Per Pod\n")
            #warehouses = int(df['sf'].max())
            columns = ["experiment_run","terminals","target","client", "child", "time", "num_errors", "Throughput (requests/second)","Goodput (requests/second)","efficiency", "Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]
            df.fillna(0, inplace=True)
            df_plot = self.benchmarking_set_datatypes(df)
            #print(df_plot)
            df_plot_filtered = pd.DataFrame()
            for col in columns:
                if col in df_plot.columns:
                    df_plot_filtered[col] = df_plot.loc[:,col]
            df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(['experiment_run', 'client', 'child'])
            #print(df_plot_filtered.to_markdown(index=True, floatfmt=".2f"))
            return df_plot_filtered
    def get_summary_benchmark_per_phase(self):
        df = self.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            columns = ["experiment_run","terminals","target","client", "child", "time", "num_errors", "Throughput (requests/second)","Goodput (requests/second)","efficiency", "Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]
            df.fillna(0, inplace=True)
            df_plot = self.benchmarking_set_datatypes(df)
            #print("\n#### Aggregated Parallel\n")
            #if self.workload['tenant_per'] == "container":
            #    # we want to aggregate containers of DBMS running in parallel
            #    #print(type(df_plot))
            #    df_plot['connection'] = df_plot['experiment_run'].astype(str)+"-"+df_plot['client'].astype(str)
            df_aggregated = self.benchmarking_aggregate_by_parallel_pods(df_plot)
            #print(df_aggregated)
            #print(df_aggregated.T)
            df_aggregated = df_aggregated.sort_values(['experiment_run','target','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"terminals","target","pod_count"]].copy()
            #columns = ["[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)","[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)","[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)","[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)"]
            columns = ["time", "num_errors", "Throughput (requests/second)","Goodput (requests/second)","efficiency", "Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            df_aggregated_reduced = df_aggregated_reduced.reindex(index=evaluators.natural_sort(df_aggregated_reduced.index))
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
            #print(df_aggregated_reduced.to_markdown(index=True, floatfmt=".2f"))
            return df_aggregated_reduced
    def get_summary_loading_per_run(self):
        df = self.get_loading_per_run()
        return df