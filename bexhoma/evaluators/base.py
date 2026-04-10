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
from datetime import datetime
import glob
from pathlib import Path

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

class base:
    """
    Basis class for evaluating an experiment.
    Constructor sets

      1. `path`: path to result folders
      1. `code`: Id of the experiment (name of result folder)
      1. `include_loading`: Bool if loading is included
      1. `include_benchmarking`: Bool if benchmarking is included
      1. `workflow`: Dict for storing actual workload (set later)
      1. `workflow_errors`: Dict for storing errors during workflow (set later)
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True):
        """
        Initializes object by setting code and path to result folder.

        :param path: path to result folders
        :param code: Id of the experiment (name of result folder)
        :param include_loading: Are there results about the loading phase?
        :param include_benchmarking: Are there results about the benchmarking phase?
        """
        self.path = (path+"/"+code)#.replace("\\", "/").replace("C:", "")
        self.code = code
        self.include_loading = include_loading
        self.include_benchmarking = include_benchmarking
        self.workflow = dict()
        self.workflow_errors = dict()
    def log_to_df(self, filename):
        """
        Transforms a log file in text format into a pandas DataFrame.

        :param filename: Name of the log file 
        :return: DataFrame of results
        """
        self.workflow_errors[filename] = dict()
        # test for known errors
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            def test_for_known_errors(text, error_message):
                error = re.findall('(.+?)'+error_message, text)
                #print(type(error), len(error))
                if len(error) > 0:
                    self.workflow_errors[filename][error_message] = list()
                    for e in error:
                        self.workflow_errors[filename][error_message].append(e)
                        #print(i)
            error_message = 'Temporary failure in name resolution'
            test_for_known_errors(stdout, error_message)
            #print(errors)
            #exit()
        except Exception as e:
            pass
        if len(self.workflow_errors[filename]) == 0:
            # no errors found
            del self.workflow_errors[filename]
        return pd.DataFrame()
    def transform_all_logs_benchmarking(self):
        """
        Collects all pandas DataFrames from the same phase (loading or benchmarking) and combines them into a single DataFrame.
        This DataFrame is stored as a pickled file.
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker") and filename.endswith(".dbmsbenchmarker.log"):
                #print("filename:", filename)
                pod_name = filename[filename.rindex("-")+1:-len(".log")]
                #print("pod_name:", pod_name)
                jobname = filename[len("bexhoma-benchmarker-"):-len("-"+pod_name+".dbmsbenchmarker.log")]
                #print("jobname:", jobname)
                self.end_benchmarking(jobname)
    def transform_all_logs_loading(self):
        """
        Collects all pandas DataFrames from the same phase (loading or benchmarking) and combines them into a single DataFrame.
        This DataFrame is stored as a pickled file.
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-loading") and filename.endswith(".sensor.log"):
                #print("filename:", filename)
                pod_name = filename[filename.rindex("-")+1:-len(".log")]
                #print("pod_name:", pod_name)
                jobname = filename[len("bexhoma-loading-"):-len("-"+pod_name+".sensor.log")]
                #print("jobname:", jobname)
                self.end_loading(jobname)
    def end_benchmarking(self, jobname):
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.
        The results are stored in a pandas DataFrame.

        :param jobname: Name of the job to clean
        """
        path = self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker-"+jobname) and filename.endswith(".dbmsbenchmarker.log"):
                #print(filename)
                df = self.log_to_df(path+"/"+filename)
                #print(df)
                """
                if df.empty:
                    print("Error in "+filename)
                    print(self.workflow_errors)
                else:
                    filename_df = path+"/"+filename+".df.pickle"
                    f = open(filename_df, "wb")
                    pickle.dump(df, f)
                    f.close()
                """
    def end_loading(self, jobname):
        """
        Ends a loading job.
        This is for storing or cleaning measures.
        The results are stored in a pandas DataFrame.

        :param jobname: Name of the job to clean
        """
        path = self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-loading-"+jobname) and filename.endswith(".sensor.log"):
                #print(filename)
                df = self.log_to_df(path+"/"+filename)
                #print(df)
                """
                if df.empty:
                    print("Error in "+filename)
                    print(self.workflow_errors)
                else:
                    filename_df = path+"/"+filename+".df.pickle"
                    f = open(filename_df, "wb")
                    pickle.dump(df, f)
                    f.close()
                """
    def _collect_dfs(self, filename_result='', filename_source_start='', filename_source_end=''):
        """
        This method does nothing and must be overloaded.
        In principle: Collects all pandas DataFrames from the same phase (loading or benchmarking) and combines them into a single DataFrame.
        This DataFrame is stored as a pickled file.
        Source files are identifies by a pattern "filename_source_start*filename_source_end"

        :param filename_result: Name of the pickled result file 
        :param filename_source_start: Begin of name pattern for source files
        :param filename_source_end: End of name pattern for source files
        """
        pass
    def evaluate_results(self, pod_dashboard=''):
        """
        Scans all log files and grabs some information.
        In this class basically it scans for errors.
        """
        if self.include_benchmarking:
            self.transform_all_logs_benchmarking()
            # only sensible for logger classes:
            self._collect_dfs(filename_result="bexhoma-benchmarker.all.df.pickle" , filename_source_start="bexhoma-benchmarker", filename_source_end=".log.df.pickle")
        if self.include_loading:
            self.transform_all_logs_loading()
            # only sensible for logger classes:
            self._collect_dfs(filename_result="bexhoma-loading.all.df.pickle" , filename_source_start="bexhoma-loading", filename_source_end=".log.df.pickle")
    def get_df_benchmarking(self):
        """
        Returns the DataFrame that containts all information about the benchmarking phase.

        :return: DataFrame of benchmarking results
        """
        return pd.DataFrame()
    def get_df_loading(self):
        """
        Returns the DataFrame that containts all information about the loading phase.

        :return: DataFrame of loading results
        """
        return pd.DataFrame()
    def reconstruct_workflow(self, df):
        """
        Constructs the workflow out of the results (reverse engineer workflow).
        This for example looks like this:
        {'MySQL-24-4-1024': [[1, 2], [1, 2]], 'MySQL-24-4-2048': [[1, 2], [1, 2]], 'PostgreSQL-24-4-1024': [[1, 2], [1, 2]], 'PostgreSQL-24-4-2048': [[1, 2], [1, 2]]}

        * 4 configurations
        * each 2 experiment runs
        * consisting of [1,2] benchmarker (first 1 pod, then 2 pods in parallel)

        :param df: DataFrame of benchmarking results - time format (pods already aggregated)
        :return: Dict of connections
        """
        # Tree of elements of the workflow
        #workflow = dict()
        #return workflow
        # Tree of elements of the workflow
        #print(df)
        def remove_after_last_dash(s):
            index = s.rfind('-')
            if index != -1:
                return s[:index]
            return s  # return the original string if "-" is not found
        configs = dict()
        for index, row in df.iterrows():
            #print(row['experiment_run'], row['configuration'])
            # strip experiment run number
            #configuration_name = remove_after_last_dash(row['orig_name']) # row['configuration']
            client_name_pattern = "{}-{}".format(row['num_experiment'], row['num_client'])
            if row['orig_name'].endswith(client_name_pattern):
                configuration_name = row['orig_name'][:-len(client_name_pattern)-1]
            else:
                configuration_name = remove_after_last_dash(row['orig_name']) # row['configuration']
            if configuration_name not in configs:
                configs[configuration_name] = dict()
                #configs[row['configuration']]
            if row['num_experiment'] not in configs[configuration_name]:
                configs[configuration_name][row['num_experiment']] = dict()
            if row['num_client'] not in configs[configuration_name][row['num_experiment']]:
                configs[configuration_name][row['num_experiment']][row['num_client']] = dict()
                configs[configuration_name][row['num_experiment']][row['num_client']]['pods'] = dict()
                configs[configuration_name][row['num_experiment']][row['num_client']]['result_count'] = 0
                #configs[row['configuration']][row['experiment_run']][row['client']]['run'] = dict()
            configs[configuration_name][row['num_experiment']][row['num_client']]['pods'][row['pods']] = True
            configs[configuration_name][row['num_experiment']][row['num_client']]['result_count'] = configs[configuration_name][row['num_experiment']][row['num_client']]['result_count'] + 1
            #configs[row['configuration']][row['experiment_run']][row['client']]['run'][row['run']] = dict()
            #configs[row['configuration']][row['experiment_run']][row['client']]['run'][row['run']]['vusers'] = row['vusers']
        #print(configs)
        #pretty_configs = json.dumps(configs, indent=2)
        #print(pretty_configs)
        # Flat version of workflow
        workflow = dict()
        for index, row in configs.items():
            workflow[index] = []
            for i, v in row.items():
                l = []
                for j, w in v.items():
                    #l.append(len(w['pods']))
                    l.append(w['result_count'])
                workflow[index].append(l)
        #print(workflow)
        #pretty_workflow = json.dumps(workflow, indent=2)
        #print(pretty_workflow)
        return workflow
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        return 0
    def test_results_column(self, df, test_column, silent=False, title=''):
            #test_column = 'x'
            if len(title) > 0:
                title = f"{title} {test_column}"
            else:
                title = test_column
            if not df is None and not df.empty:
                # Check if test_column contains 0 or NaN
                contains_zero_or_nan = df[test_column].isin([0]) | df[test_column].isna()
                # Print result (True for rows where 0 or NaN is found)
                #print(contains_zero_or_nan)
                if contains_zero_or_nan.any():
                    if not silent:
                        print("* TEST failed: {} contains 0 or NaN".format(title))
                    return False
                else:
                    if not silent:
                        print("* TEST passed: {} contains no 0 or NaN".format(title))
                    return True
            return False

