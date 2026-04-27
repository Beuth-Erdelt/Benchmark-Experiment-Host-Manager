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


class tpcc(logger):
    """
    Class for evaluating an TPC-C experiment (in the HammerDB version).
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
            # extract "wz4bp" from "./1672716717/bexhoma-benchmarker-mariadb-bht-10-9-4-1672716717-1-1-wz4bp.log"
            #print(filename, filename.rindex("-"))
            pod_name = filename[filename.rindex("-")+1:-len(".log")]
            #print("pod_name:", pod_name)
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
            #client = "1"
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
            #print(results)
            vusers = re.findall("Vuser 1:(.+?) Active", stdout)
            #print(vusers)
            result_tupels = list(zip(results, vusers))
            # Find the section that starts with 'SUMMARY OF 250 ACTIVE VIRTUAL USERS'
            #start_index = stdout.find('SUMMARY OF 250 ACTIVE VIRTUAL USERS')
            # Extract the text from that point onward
            #if start_index != -1:
            # Create a dictionary to store the results latencies
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
                # Regex pattern to match the labels and numbers (e.g., CALLS: 5426322, MIN: 2.990ms)
                pattern = r'(\w+):\s*([\d\.]+)'
                # Find all label-number pairs in the relevant text
                matches = re.findall(pattern, relevant_text)
                # Convert matches into dictionary form
                for label, value in matches:
                    #print(label)
                    # only take first occurence
                    if not label in extracted_data and not label + " [ms]" in extracted_data:
                        # If the value ends with 'ms', strip it and convert it to float
                        if 'ms' in value or label in ['MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50']:
                            label = label + " [ms]"
                            extracted_data[label] = float(value.replace('ms', '').strip())
                        else:
                            extracted_data[label] = float(value.strip())
                # Output the dictionary
                #print(extracted_data)
            else:
                pass
                #print("No latencies found.")
            #for (result, vuser) in result_tupels:
            #    print(result, vuser)
            #print(result)
            # compute efficiency, only valid for keying time
            #print(result_tupels[0][0][0], result_tupels[0][1])
            if keyandthink == "true":
                efficiency = round(100.*float(result_tupels[0][0][0])/float(result_tupels[0][1])/1.286, 2)
            else:
                efficiency = 0
            # this finds ['CALLS', 'MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50', 'SD', 'RATIO']
            # if latencies are logged
            list_latencies = list(extracted_data.values())
            #print(list_latencies)
            result_list = [(connection_name, configuration_name, experiment_run, client, pod_name, pod_count, code, iterations, duration, rampup, sf, i, num_errors, vusers_loading, vuser, efficiency, result[0], result[1], result[2]) + tuple(list_latencies) for i, (result, vuser) in enumerate(result_tupels)]#.extend(list_latencies)
            #print(result_list)
            df = pd.DataFrame(result_list)
            #print(list(extracted_data.keys()))
            column_names = ['connection', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'code', 'iterations', 'duration', 'rampup', 'sf', 'run', 'errors', 'vusers_loading', 'vusers', 'efficiency', 'NOPM', 'TPM', 'dbms']
            column_names.extend(list(extracted_data.keys()))
            #print(column_names)
            df.columns = column_names
            df.index.name = connection_name
            #print(df)
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
            #path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
            #path = '../benchmarks/1669163583'
            directory = os.fsencode(self.path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".pickle"): 
                    df = pd.read_pickle(self.path+"/"+filename)
                    #print(df)
                    #print(df.index.name)
                    list_vusers = list(df['vusers'])
                    #print(list_vusers)
                    #print("vusers", " ".join(list_vusers))
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
        #column = ["connection","run"]
        df_aggregated = pd.DataFrame()
        #for key, grp in df.groupby(column):
        for key, grp in df.groupby([df[col] for col in columns]):
            #print(key, len(grp.index))
            #print(grp)
            if 'CALLS' in grp:
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
                    #'vusers':'max',
                    #'NOPM':'sum',
                    'NOPM':'mean',
                    #'TPM':'sum',
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
                    #'vusers':'max',
                    #'NOPM':'sum',
                    'NOPM':'mean',
                    #'TPM':'sum',
                    'TPM':'mean',
                    'efficiency':'min',
                    'dbms':'max',
                }
            #print(grp.agg(aggregate))
            dict_grp = dict()
            dict_grp['connection'] = key[0]
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
        #print(df_aggregated['sf'], df_aggregated['vusers'], df_aggregated['NOPM'])
        #print(df_aggregated['sf']*10 == df_aggregated['vusers'])
        #print(df_aggregated['efficiency'])
        df_aggregated['efficiency'] = 0.  # Default all rows to 0
        mask = df_aggregated['sf'] * 10 == df_aggregated['vusers']  # Condition
        #print(mask, df_aggregated.loc[mask])
        df_aggregated.loc[mask, 'efficiency'] = (
            100. * df_aggregated['NOPM'] / 12.86 / df_aggregated['sf']
        )
        #print(df_aggregated['efficiency'])
        return df_aggregated


