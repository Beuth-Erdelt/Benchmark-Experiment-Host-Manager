"""
Evaluator for YCSB experiments.

Provides :class:`ycsb`, which extends :class:`logger` to parse and aggregate
operation throughput and latency results produced by the Yahoo Cloud Serving
Benchmark (YCSB) tool.

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
from datetime import datetime
import glob
from pathlib import Path
from bexhoma import evaluators

from .base import natural_sort
from .logger import logger



class ycsb(logger):
    """
    Evaluator for a YCSB experiment.

    Parses per-pod log files to extract operation counts, throughput, and per-operation
    latency statistics produced by the Yahoo Cloud Serving Benchmark (YCSB) tool.
    Provides time-series access to per-second throughput for both the benchmarking and
    loading phases via :meth:`get_benchmark_logs_timeseries_df_aggregated`,
    :meth:`get_loading_logs_timeseries_df_aggregated`, and their ``*_single`` variants.

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Ignored; loading is always enabled for this evaluator.
    :param include_benchmarking: Ignored; benchmarking is always enabled.
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True, benchmark_run: int = 0):
        """
        :param code: Experiment identifier — also the name of the result sub-folder.
        :param path: Root path that contains the result folders.
        :param include_loading: Ignored; loading is always enabled for this evaluator.
        :param include_benchmarking: Ignored; benchmarking is always enabled.
        :param benchmark_run: 1-based position in the benchmark sequence; 0 means unset.
        :type benchmark_run: int
        """
        super().__init__(code, path, True, True, benchmark_run=benchmark_run)
    def log_to_df(self, filename):
        """
        Parses a YCSB pod log file into a single-row DataFrame.

        Extracts connection metadata, benchmark parameters, and per-operation
        metrics (throughput, latency percentiles) from the YCSB summary output.

        :param filename: Absolute path to the YCSB log file.
        :type filename: str
        :return: Single-row DataFrame of YCSB results, or empty on parse failure.
        :rtype: pandas.DataFrame
        """
        logger.log_to_df(self, filename)
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            pod_name = filename[filename.rindex("-") + 1:-len(".log")]
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)[0]
            configuration_name = re.findall('BEXHOMA_CONFIGURATION:(.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            code = re.findall('BEXHOMA_EXPERIMENT:(.+?)\n', stdout)[0]
            experiment_run = re.findall('BEXHOMA_EXPERIMENT_RUN:(.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            benchmark_run = re.findall('BEXHOMA_BENCHMARK_RUN:(.+?)\n', stdout)
            benchmark_run = benchmark_run[0] if benchmark_run else '1'
            target = re.findall('YCSB_TARGET (.+?)\n', stdout)[0]
            threads = re.findall('YCSB_THREADCOUNT (.+?)\n', stdout)[0]
            workload = re.findall('YCSB_WORKLOAD (.+?)\n', stdout)[0]
            operations = re.findall('YCSB_OPERATIONS (.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD (.+?)\n', stdout)[0]
            batchsize_matches = re.findall('YCSB_BATCHSIZE:(.+?)\n', stdout)
            batchsize = int(batchsize_matches[0]) if batchsize_matches else -1
            exception_matches = re.findall('site.ycsb.DBException:(.+?)\n', stdout)
            exceptions = len(exception_matches)
            pod_count = re.findall('BEXHOMA_NUM_PODS (.+?)\n', stdout)[0]
            # collect lines starting with "[" — YCSB summary rows; skip "[ WARN]" lines
            parsed_rows = []
            for line in lines:
                line = line.strip('\n')
                cells = line.split(", ")
                if cells[0] and cells[0][0] == "[":
                    parsed_rows.append(line.split(", "))
            phase = connection_name
            #connection = configuration_name + '-' + experiment_run + '-' + child
            connection = configuration_name + '-' + experiment_run + '-' + client + '-' + benchmark_run + '-' + child
            #connection = connection_name + '-' + child
            col_names = [value[0] + "." + value[1] for value in parsed_rows if len(value) > 1]
            measure_values = [value[2] for value in parsed_rows if len(value) > 1]
            row_values = [code, phase, connection, configuration_name, experiment_run, client,
                          benchmark_run, pod_name, pod_count, threads, target, sf, workload,
                          operations, batchsize, exceptions, child]
            row_values.extend(measure_values)
            df = pd.DataFrame(row_values).T
            columns = ['code', 'phase', 'connection', 'configuration', 'experiment_run', 'client',
                       'benchmark_run', 'pod', 'pod_count', 'threads', 'target', 'SF', 'workload',
                       'operations', 'batchsize', 'exceptions', 'child']
            columns.extend(col_names)
            df.columns = columns
            # only works for benchmarking
            df.index.name = connection
            # should also work for loading without PVC
            #df.index = df['configuration'].astype(str) + "-" + df['experiment_run'].astype(str)  + "-" + df['child'].astype(str)
            #print("NEW INDEX", df)
            #df.index.name = connection
            return df
        except Exception as exc:
            print(exc)
            return pd.DataFrame()
    def benchmarking_set_datatypes(self, df):
        """
        Casts all YCSB benchmarking result columns to their appropriate data types.

        Only casts operation-specific columns when they are present in the DataFrame.

        :param df: DataFrame of raw YCSB benchmarking results.
        :type df: pandas.DataFrame
        :return: DataFrame with columns cast to correct types, or original ``df`` on error.
        :rtype: pandas.DataFrame
        """
        try:
            df.fillna(0, inplace=True)
            df_typed = df.astype({
                'code':'int',
                'connection':'str',
                'configuration':'str',
                'experiment_run':'int',
                'client':'int',
                'benchmark_run':'int',
                'pod':'str',
                'pod_count':'int',
                'threads':'int',
                'target':'int',
                'SF':'int',
                'workload':'str',
                'operations':'int',
                'exceptions':'int',
                '[OVERALL].RunTime(ms)':'float',
                '[OVERALL].Throughput(ops/sec)':'float',
            })
            if '[CLEANUP].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[CLEANUP].Operations':'int',
                    '[CLEANUP].AverageLatency(us)':'float',
                    '[CLEANUP].MinLatency(us)':'float',
                    '[CLEANUP].MaxLatency(us)':'float',
                    '[CLEANUP].95thPercentileLatency(us)':'float',
                    '[CLEANUP].99thPercentileLatency(us)':'float',
            })
            if '[READ].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[READ].Operations':'int',
                    '[READ].AverageLatency(us)':'float',
                    '[READ].MinLatency(us)':'float',
                    '[READ].MaxLatency(us)':'float',
                    '[READ].95thPercentileLatency(us)':'float',
                    '[READ].99thPercentileLatency(us)':'float',
                    '[READ].Return=OK':'int',
            })
            if '[UPDATE].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[UPDATE].Operations':'int',
                    '[UPDATE].AverageLatency(us)':'float',
                    '[UPDATE].MinLatency(us)':'float',
                    '[UPDATE].MaxLatency(us)':'float',
                    '[UPDATE].95thPercentileLatency(us)':'float',
                    '[UPDATE].99thPercentileLatency(us)':'float',
                    '[UPDATE].Return=OK': 'int',
            })
            if '[INSERT].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[INSERT].Operations':'int',
                    '[INSERT].AverageLatency(us)':'float',
                    '[INSERT].MinLatency(us)':'float',
                    '[INSERT].MaxLatency(us)':'float',
                    '[INSERT].95thPercentileLatency(us)':'float',
                    '[INSERT].99thPercentileLatency(us)':'float',
                    '[INSERT].Return=OK': 'int',
            })
            if '[SCAN].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[SCAN].Operations':'int',
                    '[SCAN].AverageLatency(us)':'float',
                    '[SCAN].MinLatency(us)':'float',
                    '[SCAN].MaxLatency(us)':'float',
                    '[SCAN].95thPercentileLatency(us)':'float',
                    '[SCAN].99thPercentileLatency(us)':'float',
                    '[SCAN].Return=OK':'int',
                })
            if '[READ-MODIFY-WRITE].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[READ-MODIFY-WRITE].Operations':'int',
                    '[READ-MODIFY-WRITE].AverageLatency(us)':'float',
                    '[READ-MODIFY-WRITE].MinLatency(us)':'float',
                    '[READ-MODIFY-WRITE].MaxLatency(us)':'float',
                    '[READ-MODIFY-WRITE].95thPercentileLatency(us)':'float',
                    '[READ-MODIFY-WRITE].99thPercentileLatency(us)':'float',
                })
            if '[CLEANUP-FAILED].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[CLEANUP-FAILED].Operations':'int',
                    '[CLEANUP-FAILED].AverageLatency(us)':'float',
                    '[CLEANUP-FAILED].MinLatency(us)':'float',
                    '[CLEANUP-FAILED].MaxLatency(us)':'float',
                    '[CLEANUP-FAILED].95thPercentileLatency(us)':'float',
                    '[CLEANUP-FAILED].99thPercentileLatency(us)':'float',
            })
            if '[READ-FAILED].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[READ-FAILED].Operations':'int',
                    '[READ-FAILED].AverageLatency(us)':'float',
                    '[READ-FAILED].MinLatency(us)':'float',
                    '[READ-FAILED].MaxLatency(us)':'float',
                    '[READ-FAILED].95thPercentileLatency(us)':'float',
                    '[READ-FAILED].99thPercentileLatency(us)':'float',
            })
            if '[UPDATE-FAILED].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[UPDATE-FAILED].Operations':'int',
                    '[UPDATE-FAILED].AverageLatency(us)':'float',
                    '[UPDATE-FAILED].MinLatency(us)':'float',
                    '[UPDATE-FAILED].MaxLatency(us)':'float',
                    '[UPDATE-FAILED].95thPercentileLatency(us)':'float',
                    '[UPDATE-FAILED].99thPercentileLatency(us)':'float',
            })
            if '[INSERT-FAILED].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[INSERT-FAILED].Operations':'int',
                    '[INSERT-FAILED].AverageLatency(us)':'float',
                    '[INSERT-FAILED].MinLatency(us)':'float',
                    '[INSERT-FAILED].MaxLatency(us)':'float',
                    '[INSERT-FAILED].95thPercentileLatency(us)':'float',
                    '[INSERT-FAILED].99thPercentileLatency(us)':'float',
            })
            if '[SCAN-FAILED].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[SCAN-FAILED].Operations':'int',
                    '[SCAN-FAILED].AverageLatency(us)':'float',
                    '[SCAN-FAILED].MinLatency(us)':'float',
                    '[SCAN-FAILED].MaxLatency(us)':'float',
                    '[SCAN-FAILED].95thPercentileLatency(us)':'float',
                    '[SCAN-FAILED].99thPercentileLatency(us)':'float',
                })
            if '[READ-MODIFY-WRITE-FAILED].Operations'in df_typed.columns:
                df_typed = df_typed.astype({
                    '[READ-MODIFY-WRITE-FAILED].Operations':'int',
                    '[READ-MODIFY-WRITE-FAILED].AverageLatency(us)':'float',
                    '[READ-MODIFY-WRITE-FAILED].MinLatency(us)':'float',
                    '[READ-MODIFY-WRITE-FAILED].MaxLatency(us)':'float',
                    '[READ-MODIFY-WRITE-FAILED].95thPercentileLatency(us)':'float',
                    '[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)':'float',
                })
            return df_typed
        except Exception as exc:
            print(exc)
            return df
    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Aggregates parallel-pod YCSB benchmarking rows into one row per job.

        Groups by ``columns`` and sums counts/throughput, takes mean for average
        latencies, and max for percentile/max latencies.

        The default ``columns=['phase']`` groups by the job identifier stored in the
        ``phase`` column, producing one row per benchmark job.

        :param df: Typed YCSB benchmarking DataFrame.
        :type df: pandas.DataFrame
        :param columns: Grouping columns (default ``['phase']``).
        :type columns: list[str]
        :return: Aggregated DataFrame with one row per group.
        :rtype: pandas.DataFrame
        """
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby([df[col] for col in columns]):
            aggregate = {
                'code':'max',
                'client':'max',
                'benchmark_run':'max',
                'pod':'sum',
                'pod_count':'count',
                'threads':'sum',
                'target':'sum',
                'SF':'max',
                'workload':'max',
                'operations':'sum',
                'exceptions':'sum',
                '[OVERALL].RunTime(ms)':'max',
                '[OVERALL].Throughput(ops/sec)':'sum',
            }
            if '[CLEANUP].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                '[CLEANUP].Operations':'sum',
                '[CLEANUP].AverageLatency(us)':'mean',
                '[CLEANUP].MinLatency(us)':'min',
                '[CLEANUP].MaxLatency(us)':'max',
                '[CLEANUP].95thPercentileLatency(us)':'max',
                '[CLEANUP].99thPercentileLatency(us)':'max',
                }}
            if '[READ].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[READ].Operations':'sum',
                    '[READ].AverageLatency(us)':'mean',
                    '[READ].MinLatency(us)':'min',
                    '[READ].MaxLatency(us)':'max',
                    '[READ].95thPercentileLatency(us)':'max',
                    '[READ].99thPercentileLatency(us)':'max',
                    '[READ].Return=OK': 'sum',
                }}
            if '[INSERT].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[INSERT].Operations':'sum',
                    '[INSERT].AverageLatency(us)':'mean',
                    '[INSERT].MinLatency(us)':'min',
                    '[INSERT].MaxLatency(us)':'max',
                    '[INSERT].95thPercentileLatency(us)':'max',
                    '[INSERT].99thPercentileLatency(us)':'max',
                    '[INSERT].Return=OK': 'sum',
                }}
            if '[UPDATE].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[UPDATE].Operations':'sum',
                    '[UPDATE].AverageLatency(us)':'mean',
                    '[UPDATE].MinLatency(us)':'min',
                    '[UPDATE].MaxLatency(us)':'max',
                    '[UPDATE].95thPercentileLatency(us)':'max',
                    '[UPDATE].99thPercentileLatency(us)':'max',
                    '[UPDATE].Return=OK': 'sum',
                }}
            if '[SCAN].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[SCAN].Operations':'sum',
                    '[SCAN].AverageLatency(us)':'mean',
                    '[SCAN].MinLatency(us)':'min',
                    '[SCAN].MaxLatency(us)':'max',
                    '[SCAN].95thPercentileLatency(us)':'max',
                    '[SCAN].99thPercentileLatency(us)':'max',
                    '[SCAN].Return=OK':'sum',
                }}
            if '[READ-MODIFY-WRITE].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[READ-MODIFY-WRITE].Operations':'sum',
                    '[READ-MODIFY-WRITE].AverageLatency(us)':'mean',
                    '[READ-MODIFY-WRITE].MinLatency(us)':'min',
                    '[READ-MODIFY-WRITE].MaxLatency(us)':'max',
                    '[READ-MODIFY-WRITE].95thPercentileLatency(us)':'max',
                    '[READ-MODIFY-WRITE].99thPercentileLatency(us)':'max',
                }}
            if '[CLEANUP-FAILED].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                '[CLEANUP-FAILED].Operations':'sum',
                '[CLEANUP-FAILED].AverageLatency(us)':'mean',
                '[CLEANUP-FAILED].MinLatency(us)':'min',
                '[CLEANUP-FAILED].MaxLatency(us)':'max',
                '[CLEANUP-FAILED].95thPercentileLatency(us)':'max',
                '[CLEANUP-FAILED].99thPercentileLatency(us)':'max',
                }}
            if '[READ-FAILED].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[READ-FAILED].Operations':'sum',
                    '[READ-FAILED].AverageLatency(us)':'mean',
                    '[READ-FAILED].MinLatency(us)':'min',
                    '[READ-FAILED].MaxLatency(us)':'max',
                    '[READ-FAILED].95thPercentileLatency(us)':'max',
                    '[READ-FAILED].99thPercentileLatency(us)':'max',
                }}
            if '[INSERT-FAILED].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[INSERT-FAILED].Operations':'sum',
                    '[INSERT-FAILED].AverageLatency(us)':'mean',
                    '[INSERT-FAILED].MinLatency(us)':'min',
                    '[INSERT-FAILED].MaxLatency(us)':'max',
                    '[INSERT-FAILED].95thPercentileLatency(us)':'max',
                    '[INSERT-FAILED].99thPercentileLatency(us)':'max',
                }}
            if '[UPDATE-FAILED].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[UPDATE-FAILED].Operations':'sum',
                    '[UPDATE-FAILED].AverageLatency(us)':'mean',
                    '[UPDATE-FAILED].MinLatency(us)':'min',
                    '[UPDATE-FAILED].MaxLatency(us)':'max',
                    '[UPDATE-FAILED].95thPercentileLatency(us)':'max',
                    '[UPDATE-FAILED].99thPercentileLatency(us)':'max',
                }}
            if '[SCAN-FAILED].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[SCAN-FAILED].Operations':'sum',
                    '[SCAN-FAILED].AverageLatency(us)':'mean',
                    '[SCAN-FAILED].MinLatency(us)':'min',
                    '[SCAN-FAILED].MaxLatency(us)':'max',
                    '[SCAN-FAILED].95thPercentileLatency(us)':'max',
                    '[SCAN-FAILED].99thPercentileLatency(us)':'max',
                }}
            if '[READ-MODIFY-WRITE-FAILED].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[READ-MODIFY-WRITE-FAILED].Operations':'sum',
                    '[READ-MODIFY-WRITE-FAILED].AverageLatency(us)':'mean',
                    '[READ-MODIFY-WRITE-FAILED].MinLatency(us)':'min',
                    '[READ-MODIFY-WRITE-FAILED].MaxLatency(us)':'max',
                    '[READ-MODIFY-WRITE-FAILED].95thPercentileLatency(us)':'max',
                    '[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)':'max',
                }}
            dict_grp = dict()
            dict_grp['connection'] = key[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            key_index = "-".join(map(str, key))
            df_grp = pd.DataFrame(dict_grp, index=[key_index])
            #df_grp = pd.DataFrame(dict_grp, index=[key[0]])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        return df_aggregated
    def loading_set_datatypes(self, df):
        """
        Casts all YCSB loading result columns to their appropriate data types.

        :param df: DataFrame of raw YCSB loading results.
        :type df: pandas.DataFrame
        :return: DataFrame with columns cast to correct types.
        :rtype: pandas.DataFrame
        """
        df.fillna(0, inplace=True)
        df_typed = df.astype({
            'code':'str',
            'connection':'str',
            'configuration':'str',
            'experiment_run':'int',
            'client':'int',
            'pod':'str',
            'pod_count':'int',
            'threads':'int',
            'target':'int',
            'SF':'int',
            'workload':'str',
            'operations':'int',
            'exceptions':'int',
            '[OVERALL].RunTime(ms)':'float',
            '[OVERALL].Throughput(ops/sec)':'float',
            '[CLEANUP].Operations':'int',
            '[CLEANUP].AverageLatency(us)':'float',
            '[CLEANUP].MinLatency(us)':'float',
            '[CLEANUP].MaxLatency(us)':'float',
            '[CLEANUP].95thPercentileLatency(us)':'float',
            '[CLEANUP].99thPercentileLatency(us)':'float',
            '[INSERT].Operations':'int',
            '[INSERT].AverageLatency(us)':'float',
            '[INSERT].MinLatency(us)':'float',
            '[INSERT].MaxLatency(us)':'float',
            '[INSERT].95thPercentileLatency(us)':'float',
            '[INSERT].99thPercentileLatency(us)':'float',
            '[INSERT].Return=OK':'int',
        })
        return df_typed
    def loading_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Aggregates parallel-pod YCSB loading rows into one row per job.

        The default ``columns=['phase']`` groups by the job identifier stored in
        the ``phase`` column, producing one row per loading job.

        :param df: Typed YCSB loading DataFrame.
        :type df: pandas.DataFrame
        :param columns: Grouping columns (default ``['phase']``).
        :type columns: list[str]
        :return: Aggregated DataFrame with one row per group.
        :rtype: pandas.DataFrame
        """
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby([df[col] for col in columns]):
            aggregate = {
                'code':'max',
                'client':'max',
                'pod':'sum',
                'pod_count':'count',
                'threads':'sum',
                'target':'sum',
                'SF':'max',
                'workload':'max',
                'operations':'sum',
                'exceptions':'sum',
                '[OVERALL].RunTime(ms)':'max',
                '[OVERALL].Throughput(ops/sec)':'sum',
                '[CLEANUP].Operations':'sum',
                '[CLEANUP].AverageLatency(us)':'mean',
                '[CLEANUP].MinLatency(us)':'min',
                '[CLEANUP].MaxLatency(us)':'max',
                '[CLEANUP].95thPercentileLatency(us)':'mean',
                '[CLEANUP].99thPercentileLatency(us)':'mean',
                '[INSERT].Operations':'sum',
                '[INSERT].AverageLatency(us)':'mean',
                '[INSERT].MinLatency(us)':'min',
                '[INSERT].MaxLatency(us)':'max',
                '[INSERT].95thPercentileLatency(us)':'mean',
                '[INSERT].99thPercentileLatency(us)':'mean',
                '[INSERT].Return=OK':'sum',
            }
            dict_grp = dict()
            dict_grp['connection'] = key[0]
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            key_index = "-".join(map(str, key))
            df_grp = pd.DataFrame(dict_grp, index=[key_index])
            #df_grp = pd.DataFrame(dict_grp, index=[key[0]])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        return df_aggregated
    def get_df_loading(self):
        """
        Returns the DataFrame containing all loading-phase results.

        :return: DataFrame of loading results, or empty DataFrame when unavailable.
        :rtype: pandas.DataFrame
        """
        pickle_path = self.path + "/bexhoma-loading.all.df.pickle"
        if os.path.isfile(pickle_path):
            return pd.read_pickle(pickle_path)
        return pd.DataFrame()
    def parse_ycsb_log_file(self, file_path):
        """
        Scans the lines of a YCSB log file.
        Extracts relevant performance infos for time series analysis.
        Each line starting with a time stamp is converted into a dict containing measurements (operations, sec of measurement, READ latency, ...)-

        :param file_path: Full path of log file
        :return: List of dicts of measures, one entry per line
        """
        def parse_string(log):
            log = re.sub(r'Avg=�', 'Avg=0', log)
            try:
                # Extract the date and time
                date_time_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{3})", log)
                date_time_str = date_time_match.group(1) if date_time_match else None
                date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S:%f") if date_time_str else None
                # Extract metrics from sections like [READ: ...] or [UPDATE: ...]
                # Match the pattern for operations and ops/sec
                match = re.search(r"(\d+)\s+operations", log)
                if match:
                    total_operations = int(match.group(1))  # First captured group
                # Match the pattern for operations and ops/sec
                match = re.search(r"(\d+)\s+sec:", log)
                if match:
                    sec = int(match.group(1))  # First captured group
                # Match the pattern for operations and ops/sec
                match = re.search(r";\s+([\d.]+)\s+current ops/sec", log)
                if match:
                    current_ops_per_sec = float(match.group(1))  # First captured group
                sections = re.findall(r"\[(\w+): ([^\]]+)\]", log)
                metrics = {}
                for section, content in sections:
                    # Extract key-value pairs
                    metrics[section] = {}
                    for key_value in content.split(", "):
                        key, value = key_value.split("=")
                        metrics[section][key] = float(value) if "." in value else int(value)
                return {
                    "date_time": date_time,
                    "sec": sec,
                    "total_operations": total_operations,
                    "current_ops_per_sec": current_ops_per_sec,
                    #"all_numbers": list(map(float, all_numbers)),  # Convert all numbers to float
                    "metrics": metrics,
                }
            except Exception as e:
                # Log or handle any parsing errors (optional)
                return None
        results = []
        with open(file_path, 'r') as file:
            for line in file:
                parsed_data = parse_string(line.strip())
                if parsed_data:
                    results.append(parsed_data)
        return results
    def benchmark_logs_to_timeseries_df(self, list_logs, metric="current_ops_per_sec", aggregate=True, filetype="benchmarker"):
        """
        Parses benchmarker log files for the given pod IDs and assembles a time-series DataFrame.

        Delegates to :meth:`logs_to_timeseries_df` with ``filetype='benchmarker'``.

        :param list_logs: Pod IDs used to locate matching log files.
        :type list_logs: list[str]
        :param metric: Metric to extract (default ``'current_ops_per_sec'``).
        :type metric: str
        :param aggregate: Whether to aggregate all pod DataFrames into one.
        :type aggregate: bool
        :return: Aggregated DataFrame or list of per-pod DataFrames.
        :rtype: pandas.DataFrame or list[pandas.DataFrame]
        """
        return self.logs_to_timeseries_df(list_logs=list_logs, metric=metric, aggregate=aggregate, filetype="benchmarker")
    def loading_logs_to_timeseries_df(self, list_logs, metric="current_ops_per_sec", aggregate=True, filetype="benchmarker"):
        """
        Parses loader log files for the given pod IDs and assembles a time-series DataFrame.

        Delegates to :meth:`logs_to_timeseries_df` with ``filetype='loading'``.

        :param list_logs: Pod IDs used to locate matching log files.
        :type list_logs: list[str]
        :param metric: Metric to extract (default ``'current_ops_per_sec'``).
        :type metric: str
        :param aggregate: Whether to aggregate all pod DataFrames into one.
        :type aggregate: bool
        :return: Aggregated DataFrame or list of per-pod DataFrames.
        :rtype: pandas.DataFrame or list[pandas.DataFrame]
        """
        return self.logs_to_timeseries_df(list_logs=list_logs, metric=metric, aggregate=aggregate, filetype="loading")
    def logs_to_timeseries_df(self, list_logs, metric="current_ops_per_sec", aggregate=True, filetype="benchmarker"):
        """
        Parses YCSB log files for the given pod IDs and assembles a time-series DataFrame.

        Each pod ID in ``list_logs`` is resolved to matching log files via a glob pattern
        that uses ``filetype`` to distinguish benchmarker from loading logs.
        When ``aggregate`` is ``True`` the per-second values from all pods are combined:
        percentile/max metrics use element-wise maximum, minimum metrics use element-wise
        minimum, and all others are summed.  When ``aggregate`` is ``False`` a list of
        per-pod DataFrames is returned instead.

        :param list_logs: Pod IDs used to locate matching log files.
        :type list_logs: list[str]
        :param metric: Metric column to extract (default ``'current_ops_per_sec'``).
        :type metric: str
        :param aggregate: Whether to aggregate all pod DataFrames into one.
        :type aggregate: bool
        :param filetype: Log file prefix: ``'benchmarker'`` or ``'loading'``.
        :type filetype: str
        :return: Aggregated DataFrame indexed by ``'sec'`` (with an ``'avg'`` column
                 appended) when ``aggregate`` is ``True``, or a list of per-pod DataFrames.
        :rtype: pandas.DataFrame or list[pandas.DataFrame]
        """
        column = metric
        remove_first = 0
        remove_last = 0

        def flatten_dict(d, parent_key='', sep='_'):
            """Recursively flatten a nested dict, joining keys with ``sep``."""
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        def find_matching_files(directory, pattern):
            return glob.glob(os.path.join(directory, pattern))
        if not aggregate:
            df_total = []
        else:
            df_total = pd.DataFrame()
        num_logs = 0
        for file_logs in list_logs:
            pattern = 'bexhoma-{}-*-{}.log'.format(filetype, file_logs)
            matching_files = find_matching_files(self.path, pattern)
            for file in matching_files:
                num_logs = num_logs + 1
                parsed_results = self.parse_ycsb_log_file(file)
                data = []
                for result in parsed_results:
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
                    data.append(d)
                data.pop()  # last measurement is partial; discard it
                df = pd.DataFrame(data)
                df = df.set_index('sec')
                df = df.groupby(df.index).last()
                if remove_first > 0:
                    df = df.iloc[remove_first:]
                if remove_last > 0:
                    df = df.iloc[:-remove_last]
                #print("total for aggregation", df) # index: second, column: metric value
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
            if not metric == "current_ops_per_sec" and not "9" in metric and not "Max" in metric and not "Min" in metric:
                df_total = df_total / num_logs
            df_total['avg'] = int(df_total[column].mean())
        return df_total
    def get_benchmark_logs_timeseries_df_aggregated(self, metric="current_ops_per_sec", configuration="", client='1', experiment_run='1'):
        """
        Returns a DataFrame of per-second benchmarking time-series, aggregated across pods.

        Retrieves pod IDs from :meth:`get_df_benchmarking` and delegates to
        :meth:`benchmark_logs_to_timeseries_df` with ``aggregate=True``.

        :param metric: YCSB metric to retrieve (default ``'current_ops_per_sec'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-64-8-196608'``).
        :type configuration: str
        :param client: Client number (default ``'1'``).
        :type client: str or int
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: DataFrame indexed by second with one metric column and an ``'avg'`` column.
        :rtype: pandas.DataFrame
        """
        client = str(client)
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=True)
        return df_total
    def get_benchmark_logs_timeseries_df_single(self, metric="current_ops_per_sec", configuration="", client='1', experiment_run='1'):
        """
        Returns a list of per-pod benchmarking time-series DataFrames (one per pod).

        :param metric: YCSB metric to retrieve (default ``'current_ops_per_sec'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-64-8-196608'``).
        :type configuration: str
        :param client: Client number (default ``'1'``).
        :type client: str or int
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: List of DataFrames, one per pod, each indexed by second.
        :rtype: list[pandas.DataFrame]
        """
        client = str(client)
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)
        return df_total

    def get_loading_logs_timeseries_df_aggregated(self, metric="current_ops_per_sec", configuration="", experiment_run='1'):
        """
        Returns a DataFrame of time series of a metric for the loading phase, aggregated over all pods per second.

        Uses :meth:`get_df_loading` to retrieve the pod list and
        :meth:`benchmark_logs_to_timeseries_df` to parse and aggregate the log files.
        Restricts to a configuration and an experiment run.
        Aggregation follows the same strategy as for the benchmarking phase:
        percentiles and maximum by max, minimum by min, average by average,
        ``'current_ops_per_sec'`` and all others by sum.

        :param metric: Metric to retrieve (default ``'current_ops_per_sec'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-64-8-196608'``).
        :type configuration: str
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: DataFrame indexed by second with one column for the aggregated metric
                 plus an ``'avg'`` column, or an empty DataFrame when no files are found.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_loading()
        list_logs = df[
            (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))
        ]['pod'].tolist()
        return self.loading_logs_to_timeseries_df(list_logs, metric=metric, aggregate=True)

    def get_loading_logs_timeseries_df_single(self, metric="current_ops_per_sec", configuration="", experiment_run='1'):
        """
        Returns a list of DataFrames of time series of a metric for the loading phase, one per pod.

        Uses :meth:`get_df_loading` to retrieve the pod list and
        :meth:`benchmark_logs_to_timeseries_df` to parse the log files without aggregation.
        Restricts to a configuration and an experiment run.

        :param metric: Metric to retrieve (default ``'current_ops_per_sec'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-64-8-196608'``).
        :type configuration: str
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: List of DataFrames, one per pod, each indexed by second with one metric column.
        :rtype: list[pandas.DataFrame]
        """
        df = self.get_df_loading()
        list_logs = df[
            (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))
        ]['pod'].tolist()
        return self.loading_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)

    def get_loading_per_connection(self):
        """
        Returns loading metrics for each individual connection, merged with connection
        metadata and enriched with the scale factor.

        Combines the aggregated loading DataFrame (from :meth:`get_df_loading`) with
        connection metadata (from :meth:`get_connections_of_experiment`) on
        ``(code, configuration, experiment_run)``, then normalises the index.
        Rows for which no loading log was recorded (missing ``pod_count``) are dropped.

        :return: DataFrame with one row per loading run, indexed as
                 ``{code}-{configuration}-{experiment_run}``.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_loading()
        df_connections = self.get_connections_of_experiment()
        cols_loading = ['code', 'configuration', 'experiment_run']
        df = self.loading_set_datatypes(df)
        df = self.loading_aggregate_by_parallel_pods(df)
        indexname = df.index.name
        df_connections = df_connections.drop_duplicates(subset=cols_loading, keep='first')
        df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
        df = df.set_index(cols_loading, drop=False)
        df_connections = df_connections.set_index(cols_loading, drop=False)
        # normalise index tuples to strings for consistent matching
        df.index = pd.MultiIndex.from_tuples(
            [tuple(map(str, t)) for t in df.index],
            names=df.index.names
        )
        df_connections.index = pd.MultiIndex.from_tuples(
            [tuple(map(str, t)) for t in df_connections.index],
            names=df_connections.index.names
        )
        result = df.combine_first(df_connections)
        result.index = ['-'.join(map(str, i)) for i in result.index]
        #result.index.name = indexname
        # rows without pod_count have no recorded loading phase
        result = result.dropna(subset=['pod_count'])
        workload_properties = self.get_workload()
        result['SF'] = int(workload_properties['defaultParameters']['SF'])
        return result

    def get_loading_per_pod(self):
        """
        Returns the raw loading DataFrame with one row per pod.

        :return: DataFrame from :meth:`get_df_loading` — one row per loading pod.
        :rtype: pandas.DataFrame
        """
        return self.get_df_loading()
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
        if not df.empty:
            columns = [
            'configuration', 'experiment_run', 'client', 'benchmark_run', 'child',"threads","target","pod_count","exceptions",
            "[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)",
            "[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)",
            "[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)",
            "[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)",
            "[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)",
            "[READ-MODIFY-WRITE].Operations","[READ-MODIFY-WRITE].99thPercentileLatency(us)","[READ-MODIFY-WRITE].99thPercentileLatency(us)",
            "[INSERT-FAILED].Operations","[INSERT-FAILED].99thPercentileLatency(us)","[INSERT-FAILED].99thPercentileLatency(us)",
            "[READ-FAILED].Operations","[READ-FAILED].99thPercentileLatency(us)","[READ-FAILED].99thPercentileLatency(us)",
            "[UPDATE-FAILED].Operations","[UPDATE-FAILED].99thPercentileLatency(us)","[UPDATE-FAILED].99thPercentileLatency(us)",
            "[SCAN-FAILED].Operations","[SCAN-FAILED].99thPercentileLatency(us)","[SCAN-FAILED].99thPercentileLatency(us)",
            "[READ-MODIFY-WRITE-FAILED].Operations","[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)","[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)",
            ]
            df.fillna(0, inplace=True)
            df_plot = self.benchmarking_set_datatypes(df)
            df_plot_filtered = pd.DataFrame()
            for col in columns:
                if col in df_plot.columns:
                    df_plot_filtered[col] = df_plot.loc[:,col]
            #df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(['experiment_run', 'client', 'child'])
            #df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(by=['DBMS', 'experiment_run', 'client', 'child'], key=natural_sort) #sort_values(['experiment_run'])
            #print(df_plot_filtered)
            df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(by=['configuration', 'experiment_run', 'client', 'child'], key=natural_sort) #sort_values(['experiment_run'])
            #df_plot_filtered = df_plot_filtered.reindex(index=evaluators.natural_sort(df_plot_filtered.index))
            return df_plot_filtered
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
            df_aggregated = df_aggregated.sort_values(['experiment_run','target','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"threads","target","benchmark_run","pod_count","exceptions"]].copy()
            columns = [
            "[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)",
            "[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)",
            "[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)",
            "[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)",
            "[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)",
            "[READ-MODIFY-WRITE].Operations","[READ-MODIFY-WRITE].99thPercentileLatency(us)","[READ-MODIFY-WRITE].99thPercentileLatency(us)",
            "[INSERT-FAILED].Operations","[INSERT-FAILED].99thPercentileLatency(us)","[INSERT-FAILED].99thPercentileLatency(us)",
            "[READ-FAILED].Operations","[READ-FAILED].99thPercentileLatency(us)","[READ-FAILED].99thPercentileLatency(us)",
            "[UPDATE-FAILED].Operations","[UPDATE-FAILED].99thPercentileLatency(us)","[UPDATE-FAILED].99thPercentileLatency(us)",
            "[SCAN-FAILED].Operations","[SCAN-FAILED].99thPercentileLatency(us)","[SCAN-FAILED].99thPercentileLatency(us)",
            "[READ-MODIFY-WRITE-FAILED].Operations","[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)","[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)",
            ]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            df_aggregated_reduced = df_aggregated_reduced.reindex(index=evaluators.natural_sort(df_aggregated_reduced.index))
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
            return df_aggregated_reduced
    def get_summary_loading_per_connection(self):
        """
        Returns loading metrics aggregated per experiment run.

        Delegates to :meth:`get_df_loading` (defined in :class:`base`),
        which reduces the per-connection loading DataFrame to one row per
        ``(code, configuration, experiment_run)`` and adds a
        ``'Throughput [SF/h]'`` column.

        :return: DataFrame with one row per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_loading()
        if not df.empty:
            columns = ['experiment_run','connection', "threads","target","pod_count","exceptions","[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)"]
            df.fillna(0, inplace=True)
            df_plot = self.loading_set_datatypes(df)
            df_plot_filtered = pd.DataFrame()
            for col in columns:
                if col in df_plot.columns:
                    df_plot_filtered[col] = df_plot.loc[:,col]
            #df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(by=['DBMS', 'experiment_run'], key=natural_sort) #sort_values(['experiment_run'])
            df_plot_filtered = df_plot_filtered.reindex(index=evaluators.natural_sort(df_plot_filtered.index))
            df_plot_filtered.drop('connection', axis=1, inplace=True, errors='ignore')
            return df_plot_filtered
        else:
            return df


    def get_summary_loading_per_run(self):
        """
        Returns loading metrics aggregated per experiment run.

        Delegates to :meth:`get_df_loading` (defined in :class:`base`),
        which reduces the per-connection loading DataFrame to one row per
        ``(code, configuration, experiment_run)`` and adds a
        ``'Throughput [SF/h]'`` column.

        :return: DataFrame with one row per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_loading()
        if not df.empty:
            df_plot = self.loading_set_datatypes(df)
            df_aggregated = self.loading_aggregate_by_parallel_pods(df_plot, columns=['configuration', 'experiment_run'])
            df_aggregated.sort_values(['experiment_run','target','pod_count'], inplace=True)
            df_plot_filtered = df_aggregated[['experiment_run',"threads","target","pod_count","exceptions","[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)"]]
            df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(by=['DBMS', 'experiment_run'], key=natural_sort) #sort_values(['experiment_run'])
            df_plot_filtered = df_plot_filtered.reindex(index=evaluators.natural_sort(df_plot_filtered.index))
            df_plot_filtered.drop('connection', axis=1, inplace=True, errors='ignore')
            return df_plot_filtered
        else:
            return df



