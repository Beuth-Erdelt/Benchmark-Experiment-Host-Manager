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



class ycsb(logger):
    """
    Class for evaluating an YCSB experiment.
    Constructor sets

      1. `path`: path to result folders
      1. `code`: Id of the experiment (name of result folder)
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True):
        super().__init__(code, path, True, True)
    def log_to_df(self, filename):
        """
        Transforms a log file in text format into a pandas DataFrame.

        :param filename: Name of the log file 
        :return: DataFrame of results
        """
        # test for known errors
        logger.log_to_df(self, filename)
        #print("Exceptions", filename)
        # extract status and result fields
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            pod_name = filename[filename.rindex("-")+1:-len(".log")]
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)[0]
            configuration_name = re.findall('BEXHOMA_CONFIGURATION:(.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            code = re.findall('BEXHOMA_EXPERIMENT:(.+?)\n', stdout)[0]
            experiment_run = re.findall('BEXHOMA_EXPERIMENT_RUN:(.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            target = re.findall('YCSB_TARGET (.+?)\n', stdout)[0]
            threads = re.findall('YCSB_THREADCOUNT (.+?)\n', stdout)[0]
            workload = re.findall('YCSB_WORKLOAD (.+?)\n', stdout)[0]
            operations = re.findall('YCSB_OPERATIONS (.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD (.+?)\n', stdout)[0]
            batchsize = re.findall('YCSB_BATCHSIZE:(.+?)\n', stdout)
            if len(batchsize)>0:
                # information found
                batchsize = int(batchsize[0])
            else:
                batchsize = -1
            exceptions = re.findall('site.ycsb.DBException:(.+?)\n', stdout)
            if len(exceptions)>0:
                # information found
                exceptions = len(exceptions)
            else:
                exceptions = 0
            #workload = "A"
            pod_count = re.findall('BEXHOMA_NUM_PODS (.+?)\n', stdout)[0]
            result = []
            #for line in s.split("\n"):
            for line in lines:
                line = line.strip('\n')
                cells = line.split(", ")
                #print(cells)
                if len(cells[0]) and cells[0][0] == "[":
                    result.append(line.split(", "))
            #print(result)
            #return
            # test len of values, because of [ WARN]
            phase = connection_name
            connection = connection_name + '-' + child
            list_columns = [value[0]+"."+value[1] for value in result if len(value) > 1]
            list_values = [code, phase, connection, configuration_name, experiment_run, client, pod_name, pod_count, threads, target, sf, workload, operations, batchsize, exceptions, child]
            list_measures = [value[2] for value in result if len(value) > 1]
            #list_values = [connection_name, configuration_name, experiment_run, pod_name].append([value[2] for value in result])
            #print(list_columns)
            #print(list_values)
            #print(list_measures)
            #exit()
            list_values.extend(list_measures)
            #print(list_values)
            df = pd.DataFrame(list_values)
            df = df.T
            columns = ['code', 'phase', 'connection', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'threads', 'target', 'SF', 'workload', 'operations', 'batchsize', 'exceptions', 'child']
            columns.extend(list_columns)
            #print(columns)
            df.columns = columns
            df.index.name = connection
            # number of inserts must be integer - otherwise conversion will fail
            #if '[INSERT].Return=OK' in columns and df['[INSERT].Return=OK'] == 'NaN':
            #    df['[INSERT].Return=OK'] = 0
            #print(df.T)
            #exit()
            #print(df.T)
            return df
        except Exception as e:
            print(e)
            #print(list_columns)
            return pd.DataFrame()
    def benchmarking_set_datatypes(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to suitable data types.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        try:
            df.fillna(0, inplace=True)
            df_typed = df.astype({
                'code':'int',
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
                #'[TOTAL_GCS_PS_Scavenge].Count':'int',
                #'[TOTAL_GC_TIME_PS_Scavenge].Time(ms)':'float',
                #'[TOTAL_GC_TIME_%_PS_Scavenge].Time(%)':'float',
                #'[TOTAL_GCS_PS_MarkSweep].Count':'int',
                #'[TOTAL_GC_TIME_PS_MarkSweep].Time(ms)':'float',
                #'[TOTAL_GC_TIME_%_PS_MarkSweep].Time(%)':'float',
                #'[TOTAL_GCs].Count':'int',
                #'[TOTAL_GC_TIME].Time(ms)':'float',
                #'[TOTAL_GC_TIME_%].Time(%)':'float',
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
        except Exception as e:
            print(e)
            #print(list_columns)
            return df
    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        #column = ["connection","experiment_run"]
        df_aggregated = pd.DataFrame()
        #for key, grp in df.groupby(columns):
        for key, grp in df.groupby([df[col] for col in columns]):
            #print(key, len(grp.index))
            #print(grp)
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
                #'[TOTAL_GCS_PS_Scavenge].Count':'sum',
                #'[TOTAL_GC_TIME_PS_Scavenge].Time(ms)':'max',
                #'[TOTAL_GC_TIME_%_PS_Scavenge].Time(%)':'max',
                #'[TOTAL_GCS_PS_MarkSweep].Count':'sum',
                #'[TOTAL_GC_TIME_PS_MarkSweep].Time(ms)':'max',
                #'[TOTAL_GC_TIME_%_PS_MarkSweep].Time(%)':'max',
                #'[TOTAL_GCs].Count':'sum',
                #'[TOTAL_GC_TIME].Time(ms)':'max',
                #'[TOTAL_GC_TIME_%].Time(%)':'max',
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
            #print(grp.agg(aggregate))
            dict_grp = dict()
            dict_grp['connection'] = key[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            #dict_grp['client'] = grp['client'][0]
            #dict_grp['pod'] = grp['pod'][0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            df_grp = pd.DataFrame(dict_grp, index=[key[0]])#columns=list(dict_grp.keys()))
            #df_grp = df_grp.T
            #df_grp.set_index('connection', inplace=True)
            #print(df_grp)
            df_aggregated = pd.concat([df_aggregated, df_grp])
        return df_aggregated
    def loading_set_datatypes(self, df):
        """
        Transforms a pandas DataFrame collection of loading results to suitable data types.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        #df = evaluation.get_df_loading()
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
            #'[TOTAL_GCS_PS_Scavenge].Count':'int',
            #'[TOTAL_GC_TIME_PS_Scavenge].Time(ms)':'float',
            #'[TOTAL_GC_TIME_%_PS_Scavenge].Time(%)':'float',
            #'[TOTAL_GCS_PS_MarkSweep].Count':'float',
            #'[TOTAL_GC_TIME_PS_MarkSweep].Time(ms)':'float',
            #'[TOTAL_GC_TIME_%_PS_MarkSweep].Time(%)':'float',
            #'[TOTAL_GCs].Count':'int',
            #'[TOTAL_GC_TIME].Time(ms)':'float',
            #'[TOTAL_GC_TIME_%].Time(%)':'float',
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
        Transforms a pandas DataFrame collection of loading results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        #column = ["connection","experiment_run"]
        df_aggregated = pd.DataFrame()
        #for key, grp in df.groupby(column):
        for key, grp in df.groupby([df[col] for col in columns]):
            #print(key, len(grp.index))
            #print(grp)
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
                #'[TOTAL_GCS_PS_Scavenge].Count':'sum',
                #'[TOTAL_GC_TIME_PS_Scavenge].Time(ms)':'max',
                #'[TOTAL_GC_TIME_%_PS_Scavenge].Time(%)':'max',
                #'[TOTAL_GCS_PS_MarkSweep].Count':'sum',
                #'[TOTAL_GC_TIME_PS_MarkSweep].Time(ms)':'max',
                #'[TOTAL_GC_TIME_%_PS_MarkSweep].Time(%)':'max',
                #'[TOTAL_GCs].Count':'sum',
                #'[TOTAL_GC_TIME].Time(ms)':'max',
                #'[TOTAL_GC_TIME_%].Time(%)':'max',
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
            #print(grp.agg(aggregate))
            dict_grp = dict()
            dict_grp['connection'] = key[0]
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            #dict_grp['client'] = grp['client'][0]
            #dict_grp['pod'] = grp['pod'][0]
            #dict_grp['pod_count'] = grp['pod_count'][0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            #print(dict_grp)
            df_grp = pd.DataFrame(dict_grp, index=[key[0]])#columns=list(dict_grp.keys()))
            #print(df_grp)
            #df_grp = df_grp.T
            #df_grp.set_index('connection', inplace=True)
            #print(df_grp)
            df_aggregated = pd.concat([df_aggregated, df_grp])
        return df_aggregated
    def get_df_loading(self):
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
    def benchmark_logs_to_timeseries_df(self, list_logs, metric="current_ops_per_sec", aggregate=True):
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
            matching_files = glob.glob(os.path.join(directory, pattern))
            return matching_files
        if not aggregate:
            df_total = []
        else:
            df_total = pd.DataFrame()
        num_logs = 0
        for file_logs in list_logs:
            pattern = 'bexhoma-benchmarker-*-{}.log'.format(file_logs)
            #print("Scan for files in "+self.path+'/'+self.code)
            matching_files = find_matching_files(self.path, pattern)
            for file in matching_files:
                num_logs = num_logs + 1
                #print("Extract data from log file "+file)
                parsed_results = self.parse_ycsb_log_file(file)
                data = []
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
                    data.append(d)
                data.pop()  # remove the last measure as it is not reliable
                #print(data)
                df = pd.DataFrame(data)
                df = df.set_index('sec')
                #df.fillna(0) # we need NaN for missing values (e.g., average computation)
                df = df.groupby(df.index).last() # in case of duplicate indexes (i.e., times)
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
                            # compute average or sum
                            df_total = df_total.add(df, fill_value=0)
        if aggregate:
            if not metric == "current_ops_per_sec" and not "9" in metric and not "Max" in metric and not "Min" in metric:
                df_total = df_total / num_logs
            df_total['avg'] = int(df_total[column].mean())
        return df_total
    def get_benchmark_logs_timeseries_df_aggregated(self, metric="current_ops_per_sec", configuration="", client='1', experiment_run='1'):
        """
        Returns a dataframes of time series of a metric, aggregated all pods per second.
        Gets result from self.get_df_benchmarking().
        This is all raw data as a time series.
        Restricts to a configuration, a client and an experiment run.
        Aggregates given metrics per second (!) over all pods.
        Percentiles and maximum are aggregated by max.
        Minimum is aggregated by min.
        Average is aggregated by average.
        Aggregation is summation otherwise.

        :param metric: Metric like 'current_ops_per_sec'
        :param configuration: Name of configuration like 'PostgreSQL-64-8-196608'
        :param client: Number of client like 1
        :param experiment_run: Numer of experiment run like 1
        :return: Dataframe, index is number of second, column is (constant) value of aggregated metric
        """
        client = str(client)
        #configuration = 'configuration'
        df = self.get_df_benchmarking()
        #print(df)
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=True)
        #print("get_benchmark_logs_timeseries_df_aggregated", df_total)
        return df_total
    def get_benchmark_logs_timeseries_df_single(self, metric="current_ops_per_sec", configuration="", client='1', experiment_run='1'):
        """
        Returns list of dataframes of time series of a metric, one for each pod.
        Gets result from self.get_df_benchmarking().
        This is all raw data as a time series.
        Restricts to a configuration, a client and an experiment run.

        :param metric: Metric like 'current_ops_per_sec'
        :param configuration: Name of configuration like 'PostgreSQL-64-8-196608'
        :param client: Number of client like 1
        :param experiment_run: Numer of experiment run like 1
        :return: List of dataframes, index is number of second, column is value of aggregated metric
        """
        client = str(client)
        #configuration = 'configuration'
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].tolist()
        #print(list_logs)
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)
        #print("get_benchmark_logs_timeseries_df_single", df_total)
        return df_total

    def get_loading_per_connection(self):
        df = self.get_df_loading()
        df_connections = self.get_connections_of_experiment()
        #print(df, df_connections)
        cols_loading = ['code', 'configuration', 'experiment_run']
        check_loading = all(set(cols_loading).issubset(d.columns) for d in [df, df_connections])
        #print("combine on columns " + " ".join(cols_loading))
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
        # no pod_count means there has not been a logged loading phase
        result = result.dropna(subset=['pod_count'])
        workload_properties = self.get_workload()
        #print(workload_properties['defaultParameters']['SF'])
        result['SF'] = int(workload_properties['defaultParameters']['SF'])
        return result
        #return df_ycsb
        # workload_properties = self.get_workload()
        # #print(workload_properties['defaultParameters']['SF'])
        # df = self.get_connections_of_experiment()
        # df['SF'] = int(workload_properties['defaultParameters']['SF'])
        # #sf = 1
        # df_load = df['time_load'].copy()
        # df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        # #print(df_tpx)
        # df['Throughput [SF/h]'] = df_tpx#['time_load']
        # df = df[['code','SF','configuration','connection','phase','experiment_run','client','time_load','time_ingest','time_check','pods', 'type_tenants', 'num_tenants', 'vol_tenants','Throughput [SF/h]']].copy()
        # return df

    def get_loading_per_pod(self):
        return self.get_df_loading()
        workload_properties = self.get_workload()
        #print(workload_properties['defaultParameters']['SF'])
        df = self.get_connections_of_experiment()
        df['SF'] = int(workload_properties['defaultParameters']['SF'])
        #sf = 1
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        #print(df_tpx)
        df['Throughput [SF/h]'] = df_tpx#['time_load']
        df = df[['code','SF','configuration','connection','phase','experiment_run','client','time_load','time_ingest','time_check','pods', 'type_tenants', 'num_tenants', 'vol_tenants','Throughput [SF/h]']].copy()
        df.index.name = 'pod'
        return df




