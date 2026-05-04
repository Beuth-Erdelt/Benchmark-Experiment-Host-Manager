"""
Evaluator for HammerDB TPC-C experiments.

Provides :class:`tpcc`, which extends :class:`logger` to parse and aggregate
transactions-per-minute (TPM) and throughput results produced by HammerDB.

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


from .base import natural_sort
from .logger import logger


class tpcc(logger):
    """
    Evaluator for a HammerDB TPC-C experiment.

    Parses per-pod log files to extract NOPM, TPM, and optional latency statistics
    (CALLS, MIN, AVG, MAX, TOTAL, P99, P95, P50, SD, RATIO) and assembles them into
    DataFrames.  Aggregation over parallel pods follows the same pattern as the other
    logger-based evaluators.

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
            # extract "wz4bp" from "./1672716717/bexhoma-benchmarker-mariadb-bht-10-9-4-1672716717-1-1-wz4bp.log"
            #print(filename, filename.rindex("-"))
            pod_name = filename[filename.rindex("-")+1:-len(".log")]
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)[0]
            configuration_name = re.findall('BEXHOMA_CONFIGURATION:(.+?)\n', stdout)[0]
            code = re.findall('BEXHOMA_EXPERIMENT:(.+?)\n', stdout)[0]
            experiment_run = re.findall('BEXHOMA_EXPERIMENT_RUN:(.+?)\n', stdout)[0]
            iterations = re.findall('HAMMERDB_ITERATIONS (.+?)\n', stdout)[0]
            duration = re.findall('HAMMERDB_DURATION (.+?)\n', stdout)[0]
            rampup = re.findall('HAMMERDB_RAMPUP (.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            vusers_loading = re.findall('HAMMERDB_NUM_VU (.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            timeprofile = re.findall('HAMMERDB_TIMEPROFILE (.+?)\n', stdout)[0]
            allwarehouses = re.findall('HAMMERDB_ALLWAREHOUSES (.+?)\n', stdout)[0]
            keyandthink = re.findall('HAMMERDB_KEYANDTHINK (.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD (.+?)\n', stdout)[0]
            error_timesynch = re.findall('start time has already passed', stdout)
            if len(error_timesynch) > 0:
                # log is incomplete
                print(filename, "log is incomplete")
                return pd.DataFrame()
            pod_count = re.findall('BEXHOMA_NUM_PODS (.+?)\n', stdout)[0]
            errors = re.findall('Error ', stdout)
            if len(errors) > 0:
                # something went wrong
                print(filename, "something went wrong")
            num_errors = len(errors)
            #print("connection_name:", connection_name)
            results = re.findall("Vuser 1:TEST RESULT : System achieved (.+?) NOPM from (.+?) (.+?) TPM", stdout)
            vusers = re.findall("Vuser 1:(.+?) Active", stdout)
            result_tupels = list(zip(results, vusers))
            # Create a dictionary to store the latency results
            extracted_data = {}
            # Find the section that starts with 'SUMMARY OF <number> ACTIVE VIRTUAL USERS'
            pattern = r'SUMMARY OF (\d+) ACTIVE VIRTUAL USERS'
            # Search for the pattern in the text
            match = re.search(pattern, stdout)
            # If a match is found, extract the relevant section
            if match:
                start_index = match.start()
                relevant_text = stdout[start_index:]
                match = re.search('>>>>> PROC: NEWORD', relevant_text)
                # If a match is found, extract the relevant section
                start_index = match.start()
                relevant_text = relevant_text[start_index:]
                # Optional: If you want to stop after the "SUMMARY OF 250 ACTIVE VIRTUAL USERS" section, 
                # you can cut off the text after this part by looking for the next occurrence of '>>>>> PROC'
                end_index = relevant_text.find('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
                if end_index != -1:
                    relevant_text = relevant_text[:end_index]
                # Match label-number pairs (e.g., "CALLS: 5426322", "MIN: 2.990ms")
                pattern = r'(\w+):\s*([\d\.]+)'
                matches = re.findall(pattern, relevant_text)
                for label, value in matches:
                    # only take first occurrence; suffix time labels with " [ms]"
                    if not label in extracted_data and not label + " [ms]" in extracted_data:
                        if 'ms' in value or label in ['MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50']:
                            label = label + " [ms]"
                            extracted_data[label] = float(value.replace('ms', '').strip())
                        else:
                            extracted_data[label] = float(value.strip())
            # compute efficiency — only valid when keying time is enabled

            if keyandthink == "true":
                efficiency = round(100.*float(result_tupels[0][0][0])/float(result_tupels[0][1])/1.286, 2)
            else:
                efficiency = 0
            connection = connection_name + '-' + child
            phase = connection_name
            # this finds ['CALLS', 'MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50', 'SD', 'RATIO']
            # if latencies are logged
            list_latencies = list(extracted_data.values())
            result_list = [(connection, phase, configuration_name, experiment_run, client, pod_name, pod_count, code, iterations, duration, rampup, sf, i, num_errors, vusers_loading, vuser, efficiency, result[0], result[1], result[2]) + tuple(list_latencies) for i, (result, vuser) in enumerate(result_tupels)]
            df = pd.DataFrame(result_list)
            column_names = ['connection', 'phase', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'code', 'iterations', 'duration', 'rampup', 'sf', 'run', 'errors', 'vusers_loading', 'vusers', 'efficiency', 'NOPM', 'TPM', 'dbms']
            column_names.extend(list(extracted_data.keys()))
            df.columns = column_names
            df.index.name = connection_name
            return df
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return pd.DataFrame()
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        try:
            directory = os.fsencode(self.path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".pickle"):
                    df = pd.read_pickle(self.path+"/"+filename)
                    list(df['vusers'])
            return super().test_results()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return 1
    def benchmarking_set_datatypes(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to suitable data types.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        # {'CALLS': 5426322.0, 'MIN': 2.99, 'AVG': 48.146, 'MAX': 22834.486, 'TOTAL': 261256185.492, 'P99': 975.119, 'P95': 279.771, 'P50': 5.818, 'SD': 201562.961, 'RATIO': 82.539}
        if 'CALLS' in df:
            df_typed = df.astype({
                'connection':'str',
                'configuration':'str',
                'experiment_run':'int',
                'code':'int',
                'client':'int',
                'pod':'str',
                'pod_count':'int',
                'iterations':'int',
                'duration':'int',
                'rampup':'int',
                'sf':'int',
                'run':'int',
                'errors':'int',
                'vusers_loading':'int',
                'vusers':'int',
                'NOPM':'int',
                'TPM':'int',
                'efficiency':'float',
                'dbms':'str',
                'CALLS':'float',
                'MIN [ms]':'float',
                'AVG [ms]':'float',
                'MAX [ms]':'float',
                'TOTAL [ms]':'float',
                'P99 [ms]':'float',
                'P95 [ms]':'float',
                'P50 [ms]':'float',
            })
        else:
            df_typed = df.astype({
                'connection':'str',
                'configuration':'str',
                'experiment_run':'int',
                'code':'int',
                'client':'int',
                'pod':'str',
                'pod_count':'int',
                'iterations':'int',
                'duration':'int',
                'rampup':'int',
                'sf':'int',
                'run':'int',
                'errors':'int',
                'vusers_loading':'int',
                'vusers':'int',
                'NOPM':'int',
                'TPM':'int',
                'efficiency':'float',
                'dbms':'str',
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
        for key, grp in df.groupby([df[col] for col in columns]):
            if 'CALLS' in grp:
                aggregate = {
                    'connection':'max',
                    'client':'max',
                    'code':'max',
                    'pod':'sum',
                    'pod_count':'count',
                    'iterations':'max',
                    'duration':'max',
                    'sf':'max',
                    'run':'max',
                    'errors':'sum',
                    'vusers_loading':'max',
                    'vusers':'sum',
                    'NOPM':'mean',
                    'TPM':'mean',
                    'efficiency':'min',
                    'dbms':'max',
                    'CALLS':'max',
                    'MIN [ms]':'max',
                    'AVG [ms]':'mean',
                    'MAX [ms]':'max',
                    'TOTAL [ms]':'max',
                    'P99 [ms]':'max',
                    'P95 [ms]':'max',
                    'P50 [ms]':'max',
                }
            else:
                aggregate = {
                    'code':'max',
                    'client':'max',
                    'pod':'sum',
                    'pod_count':'count',
                    'iterations':'max',
                    'duration':'max',
                    'sf':'max',
                    'run':'max',
                    'errors':'sum',
                    'vusers_loading':'max',
                    'vusers':'sum',
                    'NOPM':'mean',
                    'TPM':'mean',
                    'efficiency':'min',
                    'dbms':'max',
                }
            dict_grp = dict()
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            df_grp = pd.DataFrame(dict_grp, index=[key[0]])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        df_aggregated['efficiency'] = 0.
        mask = df_aggregated['sf'] * 10 == df_aggregated['vusers']
        df_aggregated.loc[mask, 'efficiency'] = (
            100. * df_aggregated['NOPM'] / 12.86 / df_aggregated['sf']
        )
        return df_aggregated


