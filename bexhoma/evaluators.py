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
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True):
        """
        Initializes object by setting code and path to result folder.

        :param path: path to result folders
        :param code: Id of the experiment (name of result folder)
        :param include_loading: Are there results about the loading phase?
        :param include_benchmarking: Are there results about the benchmarking phase?
        """
        self.path = path+"/"+code
        self.code = code
        self.include_loading = include_loading
        self.include_benchmarking = include_benchmarking
        self.workflow = dict()
    def end_benchmarking(self, jobname):
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.
        The results are stored in a pandas DataFrame.

        :param jobname: Name of the job to clean
        """
        pass
    def end_loading(self, jobname):
        """
        Ends a loading job.
        This is for storing or cleaning measures.
        The results are stored in a pandas DataFrame.

        :param jobname: Name of the job to clean
        """
        pass
    def evaluate_results(self, pod_dashboard=''):
        """
        Collects all pandas DataFrames from the same phase (loading or benchmarking) and combines them into a single DataFrame.
        This DataFrame is stored as a pickled file.
        """
        pass
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
    Constructor sets

      1. `path`: path to result folders
      1. `code`: Id of the experiment (name of result folder)
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
                df, errors = self.log_to_df(path+"/"+filename)
                #print(df)
                if df.empty:
                    print("Error in "+filename)
                    print(errors)
                else:
                    filename_df = path+"/"+filename+".df.pickle"
                    f = open(filename_df, "wb")
                    pickle.dump(df, f)
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
                df, errors = self.log_to_df(path+"/"+filename)
                #print(df)
                if df.empty:
                    print("Error in "+filename)
                    print(errors)
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
            #print(df_collected)
            filename_df = path+"/"+filename_result
            f = open(filename_df, "wb")
            pickle.dump(df_collected, f)
            f.close()
            #self.cluster.logger.debug(df_collected)
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
        df = pd.read_pickle(self.path+"/"+filename)
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
    def log_to_df(self, filename):
        """
        Transforms a log file in text format into a pandas DataFrame.

        :param filename: Name of the log file 
        :return: DataFrame of results
        """
        errors_general = {filename: dict()}
        return pd.DataFrame(), errors_general
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
                    print("Benchmarking", df)
                self.workflow = self.reconstruct_workflow(df)
                if not len(self.workflow) == 0:
                    print("Workflow", self.workflow)
            if self.include_loading:
                df = self.get_df_loading()
                if not df.empty:
                    print("Loading", df)
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
        errors_general = {filename: dict()}
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
            #workload = "A"
            pod_count = re.findall('NUM_PODS (.+?)\n', stdout)[0]
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
            list_columns = [value[0]+"."+value[1] for value in result]
            list_values = [connection_name, configuration_name, experiment_run, client, pod_name, pod_count, threads, target, sf, workload, operations, batchsize]
            list_measures = [value[2] for value in result]
            #list_values = [connection_name, configuration_name, experiment_run, pod_name].append([value[2] for value in result])
            #print(list_columns)
            #print(list_values)
            #print(list_measures)
            #exit()
            list_values.extend(list_measures)
            #print(list_values)
            df = pd.DataFrame(list_values)
            df = df.T
            columns = ['connection', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'threads', 'target', 'sf', 'workload', 'operations', 'batchsize']
            columns.extend(list_columns)
            #print(columns)
            df.columns = columns
            df.index.name = connection_name
            # number of inserts must be integer - otherwise conversion will fail
            #if '[INSERT].Return=OK' in columns and df['[INSERT].Return=OK'] == 'NaN':
            #    df['[INSERT].Return=OK'] = 0
            return df, errors_general
        except Exception as e:
            print(e)
            return pd.DataFrame(), errors_general
    def benchmarking_set_datatypes(self, df):
        """
        Transforms a pandas DataFrame collection of benchmarking results to suitable data types.

        :param df: DataFrame of results 
        :return: DataFrame of results
        """
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
        return df_typed
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
            }
            if '[READ].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[READ].Operations':'sum',
                    '[READ].AverageLatency(us)':'mean',
                    '[READ].MinLatency(us)':'min',
                    '[READ].MaxLatency(us)':'max',
                    '[READ].95thPercentileLatency(us)':'mean',
                    '[READ].99thPercentileLatency(us)':'mean',
                    '[READ].Return=OK': 'sum',
                }}
            if '[INSERT].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[INSERT].Operations':'sum',
                    '[INSERT].AverageLatency(us)':'mean',
                    '[INSERT].MinLatency(us)':'min',
                    '[INSERT].MaxLatency(us)':'max',
                    '[INSERT].95thPercentileLatency(us)':'mean',
                    '[INSERT].99thPercentileLatency(us)':'mean',
                    '[INSERT].Return=OK': 'sum',
                }}
            if '[UPDATE].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[UPDATE].Operations':'sum',
                    '[UPDATE].AverageLatency(us)':'mean',
                    '[UPDATE].MinLatency(us)':'min',
                    '[UPDATE].MaxLatency(us)':'max',
                    '[UPDATE].95thPercentileLatency(us)':'mean',
                    '[UPDATE].99thPercentileLatency(us)':'mean',
                    '[UPDATE].Return=OK': 'sum',
                }}
            if '[SCAN].Operations' in grp.columns:
                aggregate = {**aggregate, **{
                    '[SCAN].Operations':'sum',
                    '[SCAN].AverageLatency(us)':'mean',
                    '[SCAN].MinLatency(us)':'min',
                    '[SCAN].MaxLatency(us)':'max',
                    '[SCAN].95thPercentileLatency(us)':'mean',
                    '[SCAN].99thPercentileLatency(us)':'mean',
                    '[SCAN].Return=OK':'sum',
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
        stdout = ""
        df_header = pd.DataFrame()
        errors_general = {filename: dict()}
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            error_message = 'Temporary failure in name resolution'
            error = re.findall('(.+?)'+error_message, stdout)
            #print(type(error), len(error))
            if len(error) > 0:
                errors_general[filename][error_message] = list()
                for e in error:
                    errors_general[filename][error_message].append(e)
                    #print(i)
            #print(errors)
            #exit()
        except Exception as e:
            pass
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
            pod_count = re.findall('NUM_PODS (.+?)\n', stdout)[0]
            bench = re.findall('BENCHBASE_BENCH (.+?)\n', stdout)[0]
            profile = re.findall('BENCHBASE_PROFILE (.+?)\n', stdout)[0]
            target = re.findall('BENCHBASE_TARGET (.+?)\n', stdout)[0]
            time = re.findall('BENCHBASE_TIME (.+?)\n', stdout)[0]
            #terminals = re.findall('BENCHBASE_TERMINALS (.+?)\n', stdout)[0]
            batchsize = re.findall('BENCHBASE_BATCHSIZE (.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            errors = re.findall('Exception in thread ', stdout)
            num_errors = len(errors)
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
                'sf': sf,
                'num_errors': num_errors,
                'duration': duration,
            }
            df_header = pd.DataFrame(header, index=[0])
            if num_errors == 0:
                log = re.findall('####BEXHOMA####(.+?)####BEXHOMA####', stdout, re.DOTALL)
                if len(log) > 0:
                    result = json.loads(log[0])
                    df = pd.json_normalize(result)
                    #self.cluster.logger.debug(df)
                    df = pd.concat([df_header, df], axis=1)
                    df.index.name = connection_name
                    #print(df)
                    return df, errors_general
                else:
                    print("no results found in log file {}".format(filename))
                    return df_header, errors_general
            else:
                return df_header, errors_general#pd.DataFrame()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(stdout)
            return df_header, errors_general
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
        return df_aggregated





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
        errors_general = {filename: dict()}
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
            vusers_loading = re.findall('PARALLEL (.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            #client = "1"
            error_timesynch = re.findall('start time has already passed', stdout)
            if len(error_timesynch) > 0:
                # log is incomplete
                print(filename, "log is incomplete")
                return pd.DataFrame(), errors_general
            pod_count = re.findall('NUM_PODS (.+?)\n', stdout)[0]
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
            #for (result, vuser) in result_tupels:
            #    print(result, vuser)
            #print(result)
            result_list = [(connection_name, configuration_name, experiment_run, client, pod_name, pod_count, iterations, duration, rampup, sf, i, num_errors, vusers_loading, vuser, result[0], result[1], result[2]) for i, (result, vuser) in enumerate(result_tupels)]
            df = pd.DataFrame(result_list)
            df.columns = ['connection', 'configuration', 'experiment_run', 'client', 'pod', 'pod_count', 'iterations', 'duration', 'rampup', 'sf', 'run', 'errors', 'vusers_loading', 'vusers', 'NOPM', 'TPM', 'dbms']
            df.index.name = connection_name
            return df, errors_general
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return pd.DataFrame(), errors_general
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
                    print(df)
                    print(df.index.name)
                    list_vusers = list(df['vusers'])
                    print(list_vusers)
                    print("vusers", " ".join(list_vusers))
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
        return df_aggregated



# grep "start time has already passed" ../benchmarks/1672653866/*
