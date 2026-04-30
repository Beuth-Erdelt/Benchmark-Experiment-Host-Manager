"""
Base evaluator class for bexhoma experiments.

Provides :func:`natural_sort` and :class:`base`, which loads an experiment
result folder, parses workflow state and connection configuration, and
exposes monitoring data. All other evaluators inherit from :class:`base`
via :class:`logger`.

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
    def get_workload(self):
        """
        Returns the workload configuration of an experiment.

        Reads the ``queries.config`` file for the given experiment code and
        returns its contents as a dictionary.  The ``tenant_per`` key is
        normalised to the string ``'None'`` when absent or empty.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: Workload properties dictionary.
        :rtype: dict
        """
        with open(self.path + "/" + "/queries.config", 'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
            return workload_properties
    def add_connection_to_result(self, c, connection_id, result):
        result[connection_id] = {
            'code': c['parameter']['code'],
            'connection': c['name'],
            'configuration': c['configuration'] if 'configuration' in c else '',
            'phase': c['phase'],
            'experiment_run': c['parameter']['numExperiment'],
            'client': int(c['parameter']['client']),
            #'SF': c['defaultParameters']['SF'],
            'dockerimage': c['parameter']['dockerimage'],
            'time_load': float(c['timeLoad']),
            'time_ingest': float(c['timeIngesting']),
            'time_check': float(c['timeIndex']),
            'terminals': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS']
                if 'BENCHBASE_TERMINALS' in c['parameter']['connection_parameter']['loading_parameters'] else 0,
            'pods': c['parameter']['parallelism'],
            'tenant': c['parameter']['TENANT'] if 'TENANT' in c['parameter'] else '',
            'num_worker': int(c['parameter']['num_worker']),
            'type_tenants': c['parameter']['TENANT_BY'] if 'TENANT_BY' in c['parameter'] else 'None',
            'num_tenants': int(c['parameter']['TENANT_NUM']) if 'TENANT_NUM' in c['parameter'] else 0,
            'vol_tenants': c['parameter']['TENANT_VOL'] if 'TENANT_VOL' in c['parameter'] else 'False',
            'datadisk': c['hostsystem']['datadisk'],
        }
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
    def get_connections_of_experiment(self):
        """
        Returns connection metadata for a single experiment.

        Reads ``connections.config`` and builds a row per pod/client with the
        following key columns: ``phase``, ``code``, ``connection``, ``configuration``,
        ``experiment_run``, ``client``, ``type_tenants``, ``num_tenants``,
        ``vol_tenants``, plus flattened host-system, loading-parameter,
        benchmarking-parameter, and SUT-parameter fields.

        When a connection entry carries ``orig_name``, the entry represents an
        individual pod; otherwise a synthetic row is generated for each parallel
        client.

        :param evaluation: Evaluator instance. Defaults to the first code's evaluator.
        :type evaluation: object
        :return: DataFrame of connection metadata, one row per pod/client.
        :rtype: pandas.DataFrame
        """
        with open(self.path + "/" +  "/connections.config", 'r') as inf:
            connections = ast.literal_eval(inf.read())
            connections_sorted = sorted(connections, key=lambda c: c['name'])
            result = dict()
            for c in connections_sorted:
                if 'orig_name' in c:
                    # entry represents an individual pod — use the pod name as connection id
                    name = c['name']
                    c['phase'] = "{code}-{connection}".format(code=c['parameter']['code'], connection=c['orig_name'])
                    connection_id = "{code}-{connection}".format(code=c['parameter']['code'], connection=name)
                    #add_connection_to_result(c, connection_id, result)
                    self.add_connection_to_result(c, connection_id, result)
                else:
                    # no per-pod entries — synthesise one row per parallel client
                    clients = int(c['parameter']['parallelism'])
                    name = c['name']
                    for i in range(1, clients + 1):
                        c['name'] = "{code}-{phase}-{client}".format(code=c['parameter']['code'], phase=name, client=i)
                        c['phase'] = "{code}-{phase}".format(code=c['parameter']['code'], phase=name)
                        connection_id = "{code}-{phase}-{client}".format(code=c['parameter']['code'], phase=name, client=i)
                        #add_connection_to_result(c, connection_id, result)
                        self.add_connection_to_result(c, connection_id, result)
            return pd.DataFrame(result).T
    def get_loading_per_connection(self):
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
        return df
    def get_loading_per_run(self):
        df = self.get_loading_per_connection()
        df = df.groupby(['code', 'configuration', 'experiment_run']).max()
        df = df.reset_index()
        df.index = df['code'].astype(str) + "-" + \
                   df['configuration'].astype(str) + "-" + \
                   df['experiment_run'].astype(str)
        #df.index = df.index.map(lambda x: '-'.join(map(str, x)))
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        #print(df_tpx)
        df['Throughput [SF/h]'] = df_tpx#['time_load']
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('client', axis=1, inplace=True, errors='ignore')
        return df
    def get_loading_per_run_multitenant(self):
        df = self.get_loading_per_connection()
        df = df.groupby(["code", "experiment_run", "type_tenants", 'vol_tenants', "num_tenants"]).max()
        df = df.reset_index()
        df.index = df['code'].astype(str) + "-" + \
                   df['configuration'].astype(str) + "-" + \
                   df['experiment_run'].astype(str)
        #df.index = df.index.map(lambda x: '-'.join(map(str, x)))
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        #print(df_tpx)
        df['Throughput [SF/h]'] = df_tpx#['time_load']
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('client', axis=1, inplace=True, errors='ignore')
        return df
