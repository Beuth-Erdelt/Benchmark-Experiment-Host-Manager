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
YCSB
############################################################################
"""

class ycsb(default):
    """
    Class for defining an YCSB experiment.
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
        self.set_experiment(volume='ycsb')
        self.set_experiment(script='Schema')#SF'+str(SF)+'-index')
        self.set_experiment(indexing='Checks')
        self.cluster.set_experiments_configfolder('experiments/ycsb')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'YCSB Queries SF='+str(SF),
            info = 'This experiment performs some YCSB inspired workloads.',
            type = 'ycsb',
            )
        self.storage_label = 'ycsb-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-ycsb.yml"
        self.evaluator = evaluators.ycsb(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
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
        SFO = str(args.scaling_factor_operations)
        if SFO == 'None':
            SFO = SF
        ycsb_rows = int(SF)*1000000 # 1kb each, that is SF is size in GB
        ycsb_operations = int(SFO)*1000000
        target_base = int(args.target_base)
        extra_insert_order = args.extra_insert_order                 # insert keys by ordering or by hashed value
        batchsize = args.scaling_batchsize
        num_loading_target_factors = self.get_parameter_as_list('num_loading_target_factors')
        num_benchmarking_target_factors = self.get_parameter_as_list('num_benchmarking_target_factors')
        if mode == 'run':
            self.set_workload(
                name = 'YCSB SF='+str(SF),
                info = 'This experiment compares run time and resource consumption of YCSB queries.',
                type = 'ycsb',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'load':
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'YCSB Data Loading SF='+str(SF),
                info = 'This imports YCSB data sets.',
                type = 'ycsb',
                defaultParameters = {'SF': SF}
            )
        else:
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'YCSB Start DBMS',
                info = 'This just starts a SUT.',
                intro = 'Start DBMS and do not load data.',
                type = 'ycsb',
                defaultParameters = {'SF': SF}
            )
        self.loading_active = True
        self.jobtemplate_loading = "jobtemplate-loading-ycsb.yml"
        self.set_experiment(script='Schema')
        # note more infos about experiment in workload description
        self.workload['info'] = self.workload['info']+"\nWorkload is '{}'.".format(args.workload.upper())
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nNumber of rows to insert is {}.".format(ycsb_rows)
            self.workload['info'] = self.workload['info']+"\nOrdering of inserts is {}.".format(extra_insert_order)
        if self.benchmarking_is_active():
            self.workload['info'] = self.workload['info']+"\nNumber of operations is {}.".format(ycsb_operations)
            self.workload['info'] = self.workload['info']+"\nBatch size is '{}'.".format(batchsize)
        #self.workload['info'] = self.workload['info']+"\nYCSB is performed using several threads and processes."
        if self.loading_is_active() or self.benchmarking_is_active():
            self.workload['info'] = self.workload['info']+"\nTarget is based on multiples of '{}'.".format(target_base)
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nFactors for loading are {}.".format(num_loading_target_factors)
        if self.benchmarking_is_active():
            self.workload['info'] = self.workload['info']+"\nFactors for benchmarking are {}.".format(num_benchmarking_target_factors)
        default.prepare_testbed(self, parameter)
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('ycsb.test_results()')
        self.evaluator.test_results()
        workflow = self.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
    def OLD_evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to YCSB.
        """
        self.cluster.logger.debug('ycsb.evaluate_results()')
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
        #print('ycsb.show_summary()')
        connections_sorted, monitoring_applications = self.show_summary_header()
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        #####################
        test_loading = False
        df = self.evaluator.get_df_loading()
        if not df.empty:
            print("\n### Loading\n")
            df = df.sort_values(['configuration','experiment_run','client'])
            df = df[df.columns.drop(list(df.filter(regex='FAILED')))]
            #print(df)
            #print(df.columns)
            df_plot = self.evaluator.loading_set_datatypes(df)
            df_aggregated = self.evaluator.loading_aggregate_by_parallel_pods(df_plot)
            df_aggregated.sort_values(['experiment_run','target','pod_count'], inplace=True)
            df_aggregated_loaded = df_aggregated[['experiment_run',"threads","target","pod_count","exceptions","[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)"]]
            df_aggregated_loaded = df_aggregated_loaded.rename_axis(index="DBMS")
            print(df_aggregated_loaded.to_markdown(index=True, floatfmt=".2f"))
            test_loading = True
        #####################
        contains_failed = False
        df = self.evaluator.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            print("\n### Execution\n")
            df.fillna(0, inplace=True)
            #print(df.T)
            #exit()
            df_plot = self.evaluator.benchmarking_set_datatypes(df)
            df_aggregated = self.evaluator.benchmarking_aggregate_by_parallel_pods(df_plot)
            df_aggregated = df_aggregated.sort_values(['experiment_run','target','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"threads","target","pod_count","exceptions"]].copy()
            columns = [
            "[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)",
            "[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)",
            "[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)",
            "[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)",
            "[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)",
            "[READ-MODIFY-WRITE].Operations","[READ-MODIFY-WRITE].99thPercentileLatency(us)","[READ-MODIFY-WRITE].99thPercentileLatency(us)",
            "[INSERT-FAILED].Operations","[INSERT-FAILED].99thPercentileLatency(us)","[INSERT-FAILED].99thPercentileLatency(us)",
            "[READ-FAILED].Operations","[READ-FAILED].99thPercentileLatency(us)","[READ-FAILED].99thPercentileLatency(us)",
            "[UPDATE-FAILED].Operations","[UPDATE-FAILED].99thPercentileLatency(us)","[UPDATE-FAILED].99thPercentileLatency(us)",
            "[SCAN-FAILED].Operations","[SCAN-FAILED].99thPercentileLatency(us)","[SCAN-FAILED].99thPercentileLatency(us)",
            "[READ-MODIFY-WRITE-FAILED].Operations","[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)","[READ-MODIFY-WRITE-FAILED].99thPercentileLatency(us)",
            ]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
            print(df_aggregated_reduced.to_markdown(index=True, floatfmt=".2f"))
            contains_failed = any('FAILED' in col for col in df_aggregated_reduced.columns)
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
        test_results_monitoring = self.show_summary_monitoring()
        #if not df_monitoring_app.empty:
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            #print(monitoring_applications)#df_monitoring_app)
            for title, metrics in monitoring_applications.items():
                print("\n#### "+title+"\n")
                metrics.index.names = ["DBMS"]
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        print("\n### Tests")
        if test_loading:
            self.evaluator.test_results_column(df_aggregated_loaded, "[OVERALL].Throughput(ops/sec)", title="Loading Phase:")
        self.evaluator.test_results_column(df_aggregated_reduced, "[OVERALL].Throughput(ops/sec)", title="Execution Phase:")
        if len(test_results_monitoring) > 0:
            print(test_results_monitoring)
        if self.benchmarking_is_active():
            if self.test_workflow(workflow_actual, workflow_planned):
                print("* TEST passed: Workflow as planned")
            else:
                print("* TEST failed: Workflow not as planned")
        silent = False
        if contains_failed:
            if not silent:
                print("* TEST failed: {} contains FAILED column".format("Execution Phase:"))
            return False
        else:
            if not silent:
                print("* TEST passed: {} contains no FAILED column".format("Execution Phase:"))
            return True

