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
    def test_results_column(self, df, test_column, silent=False):
            #test_column = 'x'
            if not df is None and not df.empty:
                # Check if test_column contains 0 or NaN
                contains_zero_or_nan = df[test_column].isin([0]) | df[test_column].isna()
                # Print result (True for rows where 0 or NaN is found)
                #print(contains_zero_or_nan)
                if contains_zero_or_nan.any():
                    if not silent:
                        print("TEST failed: {} contains 0 or NaN".format(test_column))
                    return False
                else:
                    if not silent:
                        print("TEST passed: {} contains no 0 or NaN".format(test_column))
                    return True
            return False


class logger(base):
    """
    Basis class for evaluating an experiment.
    The transforms log files into DataFrames.
    """
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
                if df.empty:
                    print("Error in "+filename)
                    print(self.workflow_errors)
                else:
                    filename_df = path+"/"+filename+".df.pickle"
                    f = open(filename_df, "wb")
                    pickle.dump(df, f)
                    #print("WRITTEN", filename_df, df.T)
                    f.close()
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
                if df.empty:
                    print("Error in "+filename)
                    print(self.workflow_errors)
                else:
                    filename_df = path+"/"+filename+".df.pickle"
                    f = open(filename_df, "wb")
                    pickle.dump(df, f)
                    f.close()
    def _collect_dfs(self, filename_result='', filename_source_start='', filename_source_end=''):
        """
        Collects all pandas DataFrames from the same phase (loading or benchmarking) and combines them into a single DataFrame.
        This DataFrame is stored as a pickled file.
        Source files are identifies by a pattern "filename_source_start*filename_source_end"

        :param filename_result: Name of the pickled result file 
        :param filename_source_start: Begin of name pattern for source files
        :param filename_source_end: End of name pattern for source files
        """
        df_collected = None
        path = self.path
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith(filename_source_start) and filename.endswith(filename_source_end):
                #print(filename)
                df = pd.read_pickle(path+"/"+filename)
                if not df.empty:
                    #df['configuration'] = df.index.name
                    if df_collected is not None:
                        df_collected = pd.concat([df_collected, df])
                    else:
                        df_collected = df.copy()
        if not df_collected is None and not df_collected.empty:
            df_collected['index'] = df_collected.groupby('connection')['connection'].cumcount() + 1#df_collected.index.map(str)
            df_collected['connection_pod'] = df_collected['connection']+"-"+df_collected['index'].astype(str)
            #df_collected['connection_pod'] = df_collected.groupby('connection')['connection'].cumcount() + 1#.transform('count')
            #print(df_collected)
            df_collected.drop('index', axis=1, inplace=True)
            df_collected.set_index('connection_pod', inplace=True)
            filename_df = path+"/"+filename_result
            #print(filename_df)
            #print(df_collected.info())
            f = open(filename_df, "wb")
            pickle.dump(df_collected, f)
            f.close()
            #self.cluster.logger.debug(df_collected)
    def evaluate_results(self, pod_dashboard=''):
        """
        Collects all pandas DataFrames from the same phase (loading or benchmarking) and combines them into a single DataFrame.
        This DataFrame is stored as a pickled file.
        """
        if self.include_benchmarking:
            self.transform_all_logs_benchmarking()
            self._collect_dfs(filename_result="bexhoma-benchmarker.all.df.pickle" , filename_source_start="bexhoma-benchmarker", filename_source_end=".log.df.pickle")
        if self.include_loading:
            self.transform_all_logs_loading()
            self._collect_dfs(filename_result="bexhoma-loading.all.df.pickle" , filename_source_start="bexhoma-loading", filename_source_end=".log.df.pickle")
    def get_df_benchmarking(self):
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
    def plot(self, df, column, x, y, plot_by=None, kind='line', dict_colors=None, figsize=(12,8)):
        if plot_by is None:
            fig, ax = plt.subplots()
            for key, grp in df.groupby(column):
                labels = "{} {}".format(key, column)
                ax = grp.plot(ax=ax, kind=kind, x=x, y=y, title=y, label=labels, figsize=figsize)
                ax.set_ylim(0,df[y].max())
            plt.legend(loc='best')
            #plt.show()
            return ax
        else:
            row=0
            col=0
            groups = df.groupby(plot_by)
            #print(len(groups))
            rows = (len(groups)+1)//2
            #print(rows, "rows")
            fig, axes = plt.subplots(nrows=rows, ncols=2, sharex=True, squeeze=False, figsize=(figsize[0],figsize[1]*rows))
            #print(axes)
            for key1, grp in groups:#df3.groupby(col1):
                #print(len(axs))
                for key2, grp2 in grp.groupby(column):
                    #print(grp2)
                    labels = "{} {}, {} {}".format(key1, plot_by, key2, column)
                    #print(row,col)
                    if not dict_colors is None and len(dict_colors):
                        ax = grp2.plot(ax=axes[row,col], kind=kind, x=x, y=y, label=labels, title=y, figsize=figsize, layout=(rows,2), color=dict_colors)
                    else:
                        ax = grp2.plot(ax=axes[row,col], kind=kind, x=x, y=y, label=labels, title=y, figsize=figsize, layout=(rows,2))
                    ax.set_ylim(0, df[y].max())
                col = col + 1
                if col > 1:
                    row = row + 1
                    col = 0
            plt.legend(loc='best')
            plt.tight_layout()
            plt.show()
    def reconstruct_workflow(self, df):
        """
        Constructs the workflow out of the results (reverse engineer workflow).
        This for example looks like this:
        {'MySQL-24-4-1024': [[1, 2], [1, 2]], 'MySQL-24-4-2048': [[1, 2], [1, 2]], 'PostgreSQL-24-4-1024': [[1, 2], [1, 2]], 'PostgreSQL-24-4-2048': [[1, 2], [1, 2]]}

        * 4 configurations
        * each 2 experiment runs
        * consisting of [1,2] benchmarker (first 1 pod, then 2 pods in parallel)

        :param df: DataFrame of benchmarking results 
        :return: Dict of connections
        """
        # Tree of elements of the workflow
        configs = dict()
        for index, row in df.iterrows():
            #print(row['experiment_run'], row['configuration'])
            if row['configuration'] not in configs:
                configs[row['configuration']] = dict()
                #configs[row['configuration']]
            if row['experiment_run'] not in configs[row['configuration']]:
                configs[row['configuration']][row['experiment_run']] = dict()
            if row['client'] not in configs[row['configuration']][row['experiment_run']]:
                configs[row['configuration']][row['experiment_run']][row['client']] = dict()
                configs[row['configuration']][row['experiment_run']][row['client']]['pods'] = dict()
                configs[row['configuration']][row['experiment_run']][row['client']]['result_count'] = 0
                #configs[row['configuration']][row['experiment_run']][row['client']]['run'] = dict()
            configs[row['configuration']][row['experiment_run']][row['client']]['pods'][row['pod']] = True
            configs[row['configuration']][row['experiment_run']][row['client']]['result_count'] = configs[row['configuration']][row['experiment_run']][row['client']]['result_count'] + 1
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
                    l.append(len(w['pods']))
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
        try:
            if self.include_benchmarking:
                df = self.get_df_benchmarking()
                if not df.empty:
                    #print("Benchmarking", df)
                    pass
                self.workflow = self.reconstruct_workflow(df)
                if not len(self.workflow) == 0:
                    #print("Workflow", self.workflow)
                    pass
            if self.include_loading:
                df = self.get_df_loading()
                if not df.empty:
                    #print("Loading", df)
                    pass
            return 0
        except Exception as e:
            print(e)
            return 1
    def transform_monitoring_results(self, component="loading"):
        """
        Creates combined metrics.csv.
        For example
            query_datagenerator_metric_total_cpu_util_MonetDB-NIL-1-1.csv
            query_datagenerator_metric_total_cpu_util_MonetDB-NIL-1-2.csv
        are combined to
            query_datagenerator_metric_total_cpu_util.csv
        """
        connections_sorted = self.get_connection_config()
        list_metrics = self.get_monitoring_metrics()
        #print(c['name'], list_metrics)
        for m in list_metrics:
            df_all = None
            for connection in connections_sorted:
                if 'orig_name' in connection:
                    connectionname = connection['orig_name']
                else:
                    connectionname = connection['name']
                filename = "query_{component}_metric_{metric}_{connection}.csv".format(component=component, metric=m, connection=connectionname)
                #print(self.path++"/"+filename)
                df = monitor.metrics.loadMetricsDataframe(self.path+"/"+filename)
                if df is None:
                    continue
                #print(df)
                df.columns=[connectionname]
                if df_all is None:
                    df_all = df
                else:
                    df_all = df_all.merge(df, how='outer', left_index=True,right_index=True)
            #print(df_all)
            filename = '/query_{component}_metric_{metric}.csv'.format(component=component, metric=m)
            #print(self.path+filename)
            monitor.metrics.saveMetricsDataframe(self.path+"/"+filename, df_all)
    def get_monitoring_metric(self, metric, component="loading"):
        """
        Returns DataFrame containing metrics measured from a specific component.

        :return: DataFrame of monitoring metrics
        """
        filename = '/query_{component}_metric_{metric}.csv'.format(component=component, metric=metric)
        #print("Looking for {}".format(filename))
        if os.path.isfile(self.path+"/"+filename):
            df = pd.read_csv(self.path+"/"+filename).T
            #print(df)
            df = df.reindex(index=natural_sort(df.index))
            return df.T
        else:
            return pd.DataFrame()
    def get_monitoring_metrics(self):
        """
        Returns list of names of metrics using during monitoring.

        :return: List of monitoring metrics
        """
        connections_sorted = self.get_connection_config()
        for c in connections_sorted:
            if 'monitoring' in c and 'metrics' in c['monitoring']:
                list_metrics = list(c['monitoring']['metrics'].keys())
            else:
                list_metrics = []
            break
        return list_metrics
    def get_connection_config(self):
        """
        Returns connection.config as Python dict.
        Items are sorted by connection name.

        :return: Python dict of all connection informations
        """
        with open(self.path+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
        connections_sorted = sorted(connections, key=lambda c: c['name']) 
        return connections_sorted



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
        base.log_to_df(self, filename)
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
            experiment_run = re.findall('BEXHOMA_EXPERIMENT_RUN:(.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            target = re.findall('YCSB_TARGET (.+?)\n', stdout)[0]
            threads = re.findall('YCSB_THREADCOUNT (.+?)\n', stdout)[0]
            workload = re.findall('YCSB_WORKLOAD (.+?)\n', stdout)[0]
            operations = re.findall('YCSB_OPERATIONS (.+?)\n', stdout)[0]
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
            list_columns = [value[0]+"."+value[1] for value in result if len(value) > 1]
            list_values = [connection_name, configuration_name, experiment_run, client, pod_name, pod_count, threads, target, sf, workload, operations, batchsize, exceptions]
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
            columns = ['connection', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'threads', 'target', 'sf', 'workload', 'operations', 'batchsize', 'exceptions']
            columns.extend(list_columns)
            #print(columns)
            df.columns = columns
            df.index.name = connection_name
            # number of inserts must be integer - otherwise conversion will fail
            #if '[INSERT].Return=OK' in columns and df['[INSERT].Return=OK'] == 'NaN':
            #    df['[INSERT].Return=OK'] = 0
            #print(df.T)
            #exit()
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
                'connection':'str',
                'configuration':'str',
                'experiment_run':'int',
                'client':'int',
                'pod':'str',
                'pod_count':'int',
                'threads':'int',
                'target':'int',
                'sf':'int',
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
    def benchmarking_aggregate_by_parallel_pods(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        column = ["connection","experiment_run"]
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(column):
            #print(key, len(grp.index))
            #print(grp)
            aggregate = {
                'client':'max',
                'pod':'sum',
                'pod_count':'count',
                'threads':'sum',
                'target':'sum',
                'sf':'max',
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
            'connection':'str',
            'configuration':'str',
            'experiment_run':'int',
            'client':'int',
            'pod':'str',
            'pod_count':'int',
            'threads':'int',
            'target':'int',
            'sf':'int',
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
    def loading_aggregate_by_parallel_pods(self, df):
        """
        Transforms a pandas DataFrame collection of loading results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        column = ["connection","experiment_run"]
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(column):
            #print(key, len(grp.index))
            #print(grp)
            aggregate = {
                'client':'max',
                'pod':'sum',
                'pod_count':'count',
                'threads':'sum',
                'target':'sum',
                'sf':'max',
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
        df_total = self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)
        #print("get_benchmark_logs_timeseries_df_single", df_total)
        return df_total





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
        base.log_to_df(self, filename)
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
                'connection': connection_name,
                'configuration': configuration_name,
                'experiment_run': experiment_run,
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
            'configuration':'str',
            'experiment_run':'int',
            'duration':'int',
            'client':'int',
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
    def benchmarking_aggregate_by_parallel_pods(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        column = "connection"
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(column):
            #print(key, len(grp.index))
            #print(grp.columns)
            aggregate = {
                'client':'max',
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
            dict_grp['connection'] = key
            dict_grp['configuration'] = grp['configuration'].iloc[0]
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
        base.log_to_df(self, filename)
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
            result_list = [(connection_name, configuration_name, experiment_run, client, pod_name, pod_count, iterations, duration, rampup, sf, i, num_errors, vusers_loading, vuser, efficiency, result[0], result[1], result[2]) + tuple(list_latencies) for i, (result, vuser) in enumerate(result_tupels)]#.extend(list_latencies)
            #print(result_list)
            df = pd.DataFrame(result_list)
            #print(list(extracted_data.keys()))
            column_names = ['connection', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'iterations', 'duration', 'rampup', 'sf', 'run', 'errors', 'vusers_loading', 'vusers', 'efficiency', 'NOPM', 'TPM', 'dbms']
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
    def benchmarking_aggregate_by_parallel_pods(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to a new DataFrame.
        All result lines belonging to pods being run in parallel will be aggregated.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
        column = ["connection","run"]
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby(column):
            #print(key, len(grp.index))
            #print(grp)
            if 'CALLS' in grp:
                aggregate = {
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



# grep "start time has already passed" ../benchmarks/1672653866/*
