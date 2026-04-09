"""
:Date: 2022-10-01
:Version: 0.6.0
:Authors: Patrick K. Erdelt

    Classes for managing an experiment.
    This is plugged into a cluster object.
    It collects some configuation objects.
    Two examples are included, dealing with TPC-H and TPC-DS tests.
    Another example concerns TSBS experiment.
    Each experiment also should have an own folder having:

    * a query file
    * a subfolder for each dbms, that may run this experiment, including schema files

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
from dbmsbenchmarker import parameter, inspector
import logging
import urllib3
from os import makedirs, path
import time
from timeit import default_timer
#import datetime
import os
from datetime import datetime, timedelta
import re
import pandas as pd
import json
import ast
from types import SimpleNamespace
from importlib.metadata import version
from pathlib import Path
import platform
import math
from typing import List, Tuple, Optional

from bexhoma import evaluators
from .default import default

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)


"""
############################################################################
Benchbase
############################################################################
"""

class benchbase(default):
    """
    Class for defining a Benchbase experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor), i.e. number of rows divided by 10.000
    """
    def __init__(self,
            cluster,
            code=None,
            #queryfile = 'queries-tpch.config',
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.SF = SF
        self.set_experiment(volume='benchbase')
        self.set_experiment(script='Schema')
        self.set_experiment(indexing='Checks')
        self.cluster.set_experiments_configfolder('experiments/benchbase')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'Benchbase Queries SF='+str(SF),
            info = 'This experiment performs some Benchbase workloads.',
            type = 'benchbase',
            )
        self.storage_label = 'benchbase-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-benchbase.yml"
        self.evaluator = evaluators.benchbase(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
        self.benchmark = 'tpcc'                                                          # Benchbase knows several benchmarks. Here we store, which one to use, default tpcc
        self.components = {
            "loader": {
                "sensor": True
             },
            "benchmarker": {
                "dbmsbenchmarker": True
            }
        }
    def set_benchmark_type(self, benchmark='tpcc'):
        self.benchmark = benchmark
        self.storage_label = 'benchbase-{benchmark}-{SF}'.format(benchmark=self.benchmark, SF=self.SF)
        self.cluster.set_experiments_configfolder('experiments/benchbase/'+benchmark)
    def prepare_testbed(self, parameter):
        args = SimpleNamespace(**parameter)
        self.args = args
        self.args_dict = parameter
        mode = str(parameter['mode'])
        if mode=='load' or mode=='start':
            self.benchmarking_active = False
        if mode=='start':
            self.loading_deactivated = True
        SF = str(self.SF)
        SD = int(args.scaling_duration)*60
        target_base = int(args.target_base)
        type_of_benchmark = args.benchmark
        workload = args.workload
        extra_keying = int(args.extra_keying)
        extra_new_connection = int(args.extra_new_connection)
        num_benchmarking_target_factors = self.get_parameter_as_list('num_benchmarking_target_factors')
        if mode == 'run':
            self.set_workload(
                name = 'Benchbase Workload {} SF={}'.format(type_of_benchmark, SF),
                info = 'This experiment compares run time and resource consumption of Benchbase queries in different DBMS.',
                type = 'benchbase',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'load':
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'Benchbase Data {} Loading SF={}'.format(type_of_benchmark, SF),
                info = 'This imports a Benchbase data set.',
                type = 'benchbase',
                defaultParameters = {'SF': SF}
            )
        else:
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'Benchbase Start DBMS',
                info = 'This just starts a SUT.',
                intro = 'Start DBMS and do not load data.',
                type = 'benchbase',
                defaultParameters = {'SF': SF}
            )
        self.loading_active = True
        self.jobtemplate_loading = "jobtemplate-loading-benchbase.yml"
        self.set_experiment(script='Schema')
        # note more infos about experiment in workload description
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nBenchbase data is generated and loaded using several threads."
        if self.benchmarking_is_active():
            if len(type_of_benchmark):
                self.workload['info'] = self.workload['info']+"\nBenchmark is '{}'.".format(type_of_benchmark)
                if type_of_benchmark == "ycsb":
                    self.workload['info'] = self.workload['info']+" Workload is '{}'.".format(workload)
        if self.loading_is_active() or self.benchmarking_is_active():
            if SF:
                #self.workload['info'] = self.workload['info']+" Scaling factor (e.g., number of warehouses for TPC-C) is {}.".format(SF)
                self.workload['info'] = self.workload['info']+" Scaling factor is {}.".format(SF)
            self.workload['info'] = self.workload['info']+" Target is based on multiples of '{}'.".format(target_base)
        if self.benchmarking_is_active():
            self.workload['info'] = self.workload['info']+" Factors for benchmarking are {}.".format(num_benchmarking_target_factors)
            if extra_keying:
                self.workload['info'] = self.workload['info']+" Benchmarking has keying and thinking times activated."
            if extra_new_connection:
                self.workload['info'] = self.workload['info']+" There is a reconnect for each transaction."
            if SD:
                self.workload['info'] = self.workload['info']+" Benchmarking runs for {} minutes.".format(int(SD/60))
        default.prepare_testbed(self, parameter)
    def log_to_df(self, filename):
        self.cluster.logger.debug('benchbase.log_to_df({})'.format(filename))
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)
            log = re.findall('####BEXHOMA####(.+?)####BEXHOMA####', stdout, re.DOTALL)
            if len(log) > 0:
                result = json.loads(log[0])
                df = pd.json_normalize(result)
                df.index.name = connection_name[0]
                self.cluster.logger.debug(df)
                #print(df)
                return df
            else:
                print("no results found in log file {}".format(filename))
                return pd.DataFrame()
        except Exception as e:
            print(e)
            return pd.DataFrame()
    def DEPRECATED_get_parts_of_name(self, name):
        parts_name = re.findall('{(.+?)}', self.name_format)
        parts_values = re.findall('-(.+?)-', "-"+name.replace("-","--")+"--")
        return dict(zip(parts_name, parts_values))
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('benchbase.test_results()')
        self.evaluator.test_results()
        workflow = self.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
    def OLD_evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to Benchbase.
        """
        self.cluster.logger.debug('benchbase.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        self.workload['workflow_errors'] = self.evaluator.workflow_errors
        # download results
        if len(pod_dashboard) == 0:
            pod_dashboard = self.get_dashboard_pod()
        if self.monitoring_active:
            cmd = {}
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loading -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct stream -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loader -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct benchmarker -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            for component_type in self.workload['monitoring_components']:
                cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct {} -e {}'.format(component_type, self.code)
                stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
                self.cluster.logger.debug(stdout)
        print("{:30s}: downloading partial results".format("Experiment"))
        self.experimentfile_download(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.experimentfile_upload(filename='')
    def show_summary(self):
        #print('benchbase.show_summary()')
        connections_sorted, monitoring_applications = self.show_summary_header()
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        #####################
        warehouses = 0
        df = self.evaluator.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            print("\n### Execution")
            print("\n#### Per Pod\n")
            warehouses = int(df['sf'].max())
            columns = ["experiment_run","terminals","target","client", "child", "time", "num_errors", "Throughput (requests/second)","Goodput (requests/second)","efficiency", "Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]
            df.fillna(0, inplace=True)
            df_plot = self.evaluator.benchmarking_set_datatypes(df)
            #print(df_plot)
            df_plot_filtered = pd.DataFrame()
            for col in columns:
                if col in df_plot.columns:
                    df_plot_filtered[col] = df_plot.loc[:,col]
            df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(['experiment_run', 'client', 'child'])
            print(df_plot_filtered.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Aggregated Parallel\n")
            if self.workload['tenant_per'] == "container":
                # we want to aggregate containers of DBMS running in parallel
                #print(type(df_plot))
                df_plot['connection'] = df_plot['experiment_run'].astype(str)+"-"+df_plot['client'].astype(str)
            df_aggregated = self.evaluator.benchmarking_aggregate_by_parallel_pods(df_plot)
            #print(df_aggregated)
            #print(df_aggregated.T)
            df_aggregated = df_aggregated.sort_values(['experiment_run','target','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"terminals","target","pod_count"]].copy()
            #columns = ["[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)","[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)","[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)","[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)"]
            columns = ["time", "num_errors", "Throughput (requests/second)","Goodput (requests/second)","efficiency", "Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            df_aggregated_reduced = df_aggregated_reduced.reindex(index=evaluators.natural_sort(df_aggregated_reduced.index))
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
            print(df_aggregated_reduced.to_markdown(index=True, floatfmt=".2f"))
        #print("\nWarehouses:", warehouses)
        #####################
        if self.benchmarking_is_active():
            print("\n### Workflow")
            workflow_actual = self.evaluator.reconstruct_workflow(df)
            workflow_planned = self.workload['workflow_planned']
            if len(workflow_actual) > 0:
                print("\n#### Actual\n")
                for c in workflow_actual:
                    print("* DBMS", c, "- Pods", workflow_actual[c])
            if len(workflow_planned) > 0:
                print("\n#### Planned\n")
                for c in workflow_planned:
                    print("* DBMS", c, "- Pods", workflow_planned[c])
        #####################
        if self.loading_is_active():
            print("\n### Loading\n")
            #connections_sorted = sorted(connections, key=lambda c: c['name']) 
            result = dict()
            for c in connections_sorted:
                result[c['name']] = {
                    'time_load': c['timeIngesting'],
                    'terminals': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS'],
                    #'target': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TARGET'],
                    'pods': c['parameter']['parallelism'],
                }
                #result[c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS']] = c['timeIngesting']
            df = pd.DataFrame(result)#, index=['time_load'])#, index=result.keys())
            #print(df)
            #df = df.T.pivot(columns='terminals', index='target', values='time_load')
            df_connections = df.copy().T
            #print(df_connections)
            df_tpx = (warehouses*3600.0)/df_connections.sort_index()
            #print(df_tpx)
            #df_loading_tpx = df_tpx['time_load']
            #df_connections['Imported warehouses [1/h]'] = df_tpx['time_load']
            df_connections['Throughput [SF/h]'] = df_tpx['time_load']
            df_connections = df_connections.reindex(index=evaluators.natural_sort(df_connections.index))
            df_connections = df_connections.rename_axis(index="DBMS")
            print(df_connections.to_markdown(index=True, floatfmt=".2f"))
            #pd.DataFrame(df_tpx['time_load']).plot.bar(title="Imported warehouses [1/h]")
        #####################
        test_results_monitoring = self.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            #print(monitoring_applications)#df_monitoring_app)
            for title, metrics in monitoring_applications.items():
                print("\n#### "+title+"\n")
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        print("\n### Tests")
        self.evaluator.test_results_column(df_aggregated_reduced, "Throughput (requests/second)")
        if len(test_results_monitoring) > 0:
            print(test_results_monitoring)
        if self.benchmarking_is_active():
            if self.test_workflow(workflow_actual, workflow_planned):
                print("* TEST passed: Workflow as planned")
            else:
                print("* TEST failed: Workflow not as planned")


