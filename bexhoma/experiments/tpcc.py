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
from .base import base

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)



"""
############################################################################
TPC-C
############################################################################
"""

class tpcc(base):
    """
    Class for defining an TPC-C experiment (in the HammerDB version).
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor), i.e. number of warehouses
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
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.SF = SF
        self.set_experiment(volume='tpcc')
        self.set_experiment(script='Schema')#SF'+str(SF)+'-index')
        self.set_experiment(indexing='Checks')
        self.cluster.set_experiments_configfolder('experiments/tpcc')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'TPC-C Queries SF='+str(SF),
            info = 'This experiment performs some TPC-C inspired workloads.',
            type = 'tpcc',
            )
        self.storage_label = 'hammerdb-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-hammerdb.yml"
        self.evaluator = evaluators.tpcc(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
        self.components = {
            "loader": {
                "sensor": True
             },
            "benchmarker": {
                "dbmsbenchmarker": True
            }
        }
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
        SD = int(args.scaling_duration)
        extra_latency = int(args.extra_latency)
        extra_keying = int(args.extra_keying)
        if mode == 'run':
            self.set_workload(
                name = 'HammerDB Workload SF={} (warehouses for TPC-C)'.format(SF),
                info = 'This experiment compares run time and resource consumption of TPC-C queries in different DBMS.',
                type = 'tpcc',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'load':
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'HammerDB Data Loading SF={} (warehouses for TPC-C)'.format(SF),
                info = 'This imports TPC-C data sets.',
                type = 'tpcc',
                defaultParameters = {'SF': SF}
            )
        else:
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'HammerDB Start DBMS',
                info = 'This just starts a SUT.',
                intro = 'Start DBMS and do not load data.',
                type = 'tpcc',
                defaultParameters = {'SF': SF}
            )
        self.loading_active = True
        self.jobtemplate_loading = "jobtemplate-loading-hammerdb.yml"
        self.set_experiment(script='Schema')
        # note more infos about experiment in workload description
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nTPC-C data is generated and loaded using several threads."
        if self.loading_is_active() or self.benchmarking_is_active():
            if SF:
                self.workload['info'] = self.workload['info']+"\nScaling factor (i.e., number of warehouses) is {}.".format(SF)
        if self.benchmarking_is_active():
            if SD:
                self.workload['info'] = self.workload['info']+" Benchmarking runs for {} minutes.".format(SD)
            if extra_keying:
                self.workload['info'] = self.workload['info']+" Benchmarking has keying and thinking times activated."
            if extra_latency:
                self.workload['info'] = self.workload['info']+" Benchmarking also logs latencies."
        default.prepare_testbed(self, parameter)
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('tpcc.test_results()')
        self.evaluator.test_results()
        workflow = self.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
    def OLD_evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to HammerDB.
        """
        self.cluster.logger.debug('tpcc.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        self.workload['workflow_errors'] = self.evaluator.workflow_errors
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
        # copy logs and yamls to result folder
        print("{:30s}: downloading partial results".format("Experiment"))
        self.experimentfile_download(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.experimentfile_upload(filename='')
    def show_summary(self):
        #print('tpcc.show_summary()')
        connections_sorted, monitoring_applications = self.show_summary_header()
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        #####################
        if self.loading_is_active():
            df = self.evaluator.get_df_loading()
            if not df.empty:
                print("\n### Loading\n")
                #print(df)
                print(df.to_markdown(index=True, floatfmt=".2f"))
        #####################
        warehouses = 0
        if self.benchmarking_is_active():
            df = self.evaluator.get_df_benchmarking()
            if not df.empty:
                print("\n### Execution\n")
                #print(df)
                warehouses = int(df['sf'].max())
                df.fillna(0, inplace=True)
                df_plot = self.evaluator.benchmarking_set_datatypes(df)
                df_aggregated = self.evaluator.benchmarking_aggregate_by_parallel_pods(df_plot)
                df_aggregated = df_aggregated.sort_values(['experiment_run','client','pod_count']).round(2)
                if "P95 [ms]" in df_aggregated:
                    # we have latencies
                    aggregated_list = ['experiment_run',"vusers","client","pod_count","P95 [ms]","P99 [ms]", "efficiency"]
                    columns = ["NOPM", "TPM", "efficiency", "duration", "errors","P95 [ms]","P99 [ms]"]
                else:
                    aggregated_list = ['experiment_run',"vusers","client","pod_count", "efficiency"]
                    columns = ["NOPM", "TPM", "efficiency", "duration", "errors"]
                df_aggregated_reduced = df_aggregated[aggregated_list].copy()
                for col in columns:
                    if col in df_aggregated.columns:
                        df_aggregated_reduced[col] = df_aggregated.loc[:,col]
                #print(df_aggregated_reduced)
                df_aggregated_reduced.index.names = ["DBMS"]
                print(df_aggregated_reduced.to_markdown(index=True, floatfmt=".2f"))
            print("\n* Warehouses:", warehouses)
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
                    #'terminals': c['parameter']['connection_parameter']['loading_parameters']['HAMMERDB_VUSERS'], # these are the benchmark clients
                    'terminals': c['parameter']['connection_parameter']['loading_parameters']['HAMMERDB_NUM_VU'],
                    #'target': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TARGET'],
                    'pods': c['parameter']['parallelism'],
                }
                #result[c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS']] = c['timeIngesting']
            df = pd.DataFrame(result)#, index=['time_load'])#, index=result.keys())
            #print(df)
            #df = df.T.pivot(columns='terminals', index='target', values='time_load')
            df_connections = df.copy().T
            #print(df_connections)
            df_time_load = pd.DataFrame(df_connections['time_load'], columns=['time_load'])
            df_tpx = (warehouses*3600.0)/df_time_load.sort_index()
            #print(df_tpx)
            #df_loading_tpx = df_tpx['time_load']
            df_connections['Imported warehouses [1/h]'] = df_tpx['time_load']
            df_connections.index.names = ["DBMS"]
            print(df_connections.to_markdown(index=True, floatfmt=".2f"))
            #print(df_connections)
        #####################
        test_results_monitoring = self.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            #print(df_monitoring_app)
            for title, metrics in monitoring_applications.items():
                print("\n#### "+title+"\n")
                #print(metrics)
                metrics.index.names = ["DBMS"]
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        print("\n### Tests")
        if len(test_results_monitoring) > 0:
            print(test_results_monitoring)
        if self.benchmarking_is_active():
            self.evaluator.test_results_column(df_aggregated_reduced, "NOPM")
            if self.test_workflow(workflow_actual, workflow_planned):
                print("* TEST passed: Workflow as planned")
            else:
                print("* TEST failed: Workflow not as planned")


