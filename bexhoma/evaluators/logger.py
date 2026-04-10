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

from .base import base, natural_sort


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
                    # dbmsbenchmarker never returns a non-empty dataframe
                    #print("Error in "+filename)
                    #print(self.workflow_errors)
                    pass
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
                path_and_filename = path+"/"+filename
                df = self.log_to_df(path_and_filename)
                #print(df)
                if df.empty and path_and_filename in self.workflow_errors:
                    # there has been an error
                    print("Error in "+filename)
                    print(self.workflow_errors)
                elif not df.empty:
                    # there is no resulting df in log file
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


