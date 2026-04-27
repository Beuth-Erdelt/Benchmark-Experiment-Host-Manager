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
pd.set_option("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
# Some nice output
#from IPython.display import display, Markdown
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
    Class for evaluating a Benchbase experiment.
    Constructor sets

      1. `path`: path to result folders
      1. `code`: Id of the experiment (name of result folder)
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
            #terminals = re.findall('BENCHBASE_TERMINALS (.+?)\n', stdout)[0]
            batchsize = re.findall('BENCHBASE_BATCHSIZE (.+?)\n', stdout)[0]
            keyandthink = re.findall('BENCHBASE_KEY_AND_THINK (.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD (.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            #errors = re.findall('Exception in thread ', stdout)
            errors = re.findall('error code', stdout)
            #print(errors)
            num_errors = len(errors)
            #if keyandthink == "true":
            #    efficiency = round(100.*/1.286, 2)
            #else:
            #    efficiency = 0
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
                #'terminals': terminals,
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
        #column = "connection"
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(columns):
            #print(key, len(grp.index))
            #print(grp.columns)
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
                #'terminals':'sum',
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
            #print(grp.agg(aggregate))
            dict_grp = dict()
            #dict_grp['connection'] = key
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            #dict_grp['client'] = grp['client'][0]
            #dict_grp['pod'] = grp['pod'][0]
            #print(dict_grp)
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            #print(key)
            key_index = "_".join(map(str, key))
            #print(key_index)
            df_grp = pd.DataFrame(dict_grp, index=[key_index])#columns=list(dict_grp.keys()))
            #df_grp = df_grp.T
            #df_grp.set_index('connection', inplace=True)
            #print(df_grp)
            df_aggregated = pd.concat([df_aggregated, df_grp])
        #print(df_aggregated)
        #mask = df_aggregated['sf'] * 10 == df_aggregated['terminals']  # Condition
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
        #column = "current_ops_per_sec"
        #column = "READ_Avg"
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
        def safe_glob(pattern, recursive=True, return_paths=False):
            try:
                # Normalize and absolute path
                pattern = os.path.abspath(os.path.normpath(pattern))
                #print(f"[safe_glob] Using pattern: {pattern}")

                # Run glob
                matches = glob.glob(pattern, recursive=recursive)
                #print(f"[safe_glob] Found {len(matches)} file(s)")

                # Print found files
                #for m in matches:
                #    print(f" - {m}")

                # Optional: return Path objects
                if return_paths:
                    return [Path(m) for m in matches]
                return matches

            except Exception as e:
                print(f"[safe_glob] ERROR: {e}")
                return []
        if not aggregate:
            df_total = []
        else:
            df_total = pd.DataFrame()
        num_logs = 0
        for file_logs in list_logs:
            pattern = 'bexhoma-benchmarker-*-{}.log'.format(file_logs)
            #pattern = "*.log"
            #pattern = "bexhoma-benchmarker-*-qhrlt.dbmsbenchmarker.log"
            #print("Scan for files like {pattern} in {path}".format(pattern=pattern, path=self.path))
            #print(f'Current Working Directory: {os.getcwd()}')
            #print(safe_glob(os.path.join(self.path, pattern)))
            #matching_files = glob.glob(os.path.abspath(os.path.normpath(os.path.join(self.path, pattern))))#find_matching_files(self.path, pattern)
            matching_files = find_matching_files(self.path, pattern)
            #matching_files = safe_glob(os.path.join(self.path, pattern))
            for file in matching_files:
                num_logs = num_logs + 1
                #print("Extract data from log file "+file)
                parsed_results = self.parse_benchbase_log_file(file)
                #print(parsed_results)
                """data = []
                for result in parsed_results:
                    #print(result)
                    if not column in result:
                        result_metrics = flatten_dict(result['metrics'])
                        #print(result_metrics)
                        d = {
                            'sec': result['sec'],
                            column: result_metrics[column]
                        }
                    else:
                        d = {
                            'sec': result['sec'],
                            column: result[column]
                        }
                    data.append(d)"""
                #data.pop()  # remove the last measure as it is not reliable
                #print(data)
                df = pd.DataFrame(parsed_results)
                df = df.set_index('second')
                #df.fillna(0) # we need NaN for missing values (e.g., average computation)
                df = df.groupby(df.index).last() # in case of duplicate indexes (i.e., times)
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
                            # compute average or sum
                            #print(df_total)
                            #print(df)
                            df_total = df_total.add(df, fill_value=0)
        if aggregate:
            #if not metric == "current_ops_per_sec" and not "9" in metric and not "Max" in metric and not "Min" in metric:
            #    df_total = df_total / num_logs
            #print(df_total[column])
            df_total['avg'] = int(df_total[column].mean())
        return df_total
    def get_benchmark_logs_timeseries_df_aggregated(self, metric="throughput", configuration="", client='1', experiment_run='1'):
        #code = "1737365651"
        #code = "1737110896"
        #path = "/home/perdelt/benchmarks"
        #evaluation = evaluator.ycsb(code=code, path=path)
        client = str(client)#'49'
        #configuration = 'configuration'
        df = self.get_df_benchmarking()
        #print(df)
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        #print(list_logs)
        #list_logs = df[df['client'] == client]['pod'].tolist()
        #list_logs = df[df['client'] == client]['pod_count'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=True)
        return df_total
    def get_benchmark_logs_timeseries_df_single(self, metric="throughput", configuration="", client='1', experiment_run='1'):
        #code = "1737365651"
        #code = "1737110896"
        #path = "/home/perdelt/benchmarks"
        #evaluation = evaluator.ycsb(code=code, path=path)
        client = str(client)#'49'
        #configuration = 'configuration'
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        #print(list_logs)
        #list_logs = df[df['client'] == client]['pod'].tolist()
        #list_logs = df[df['client'] == client]['pod_count'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)
        return df_total




