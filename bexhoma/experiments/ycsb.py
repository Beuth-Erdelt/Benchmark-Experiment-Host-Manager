"""
Experiment class for YCSB benchmarks.

Provides :class:`ycsb`, which extends :class:`base` to orchestrate
Yahoo Cloud Serving Benchmark (YCSB) workloads inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3
import pandas as pd
from types import SimpleNamespace

from bexhoma import evaluators
from .base import base

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["ycsb"]

# YCSB experiment class

class ycsb(base):
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
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            ):
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.SF = SF                                                    # YCSB scaling factor (dataset size in GB; 1 SF = 1 000 000 rows of ~1 kB)
        self.set_experiment(volume='ycsb')
        self.set_experiment(script='Schema')
        self.set_experiment(indexing='Checks')
        self.cluster.set_experiments_configfolder('experiments/ycsb')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'YCSB Queries SF='+str(SF),
            info = 'This experiment performs some YCSB inspired workloads.',
            type = 'ycsb',
            )
        self.storage_label = 'ycsb-'+str(SF)                           # label used to match persistent storage to this experiment
        self.jobtemplate_loading = "jobtemplate-loading-ycsb.yml"             # K8s job template for the YCSB loading container
        self.jobtemplate_benchmarking = "jobtemplate-benchmarking-ycsb.yml"      # K8s job template for the YCSB benchmarking container
        self.evaluator = evaluators.ycsb(                               # evaluator specific to YCSB result format
            code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
        self.components = {                                             # maps component types to required sub-components (no datagenerator for YCSB)
            "loader": {
                "sensor": True
             },
            "benchmarker": {
                "dbmsbenchmarker": True
            }
        }
    def prepare_testbed(self, parameter: dict) -> None:
        """
        Configure the YCSB experiment from a CLI parameter dict and delegate to base.

        Sets workload metadata and appends info lines about the YCSB workload letter,
        number of rows, operations, batch size, and throughput target factors.

        :param parameter: Dict of CLI arguments as produced by argparse.
        """
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
            self.set_workload(
                name = 'YCSB Data Loading SF='+str(SF),
                info = 'This imports YCSB data sets.',
                type = 'ycsb',
                defaultParameters = {'SF': SF}
            )
        else:
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
        base.prepare_testbed(self, parameter)
    def test_results(self) -> None:
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
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct stream -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loader -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct benchmarker -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            for component_type in self.workload['monitoring_components']:
                cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct {} -e {}'.format(component_type, self.code)
                _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
                self.cluster.logger.debug(stdout)
        print("{:30s}: downloading partial results".format("Experiment"))
        self.experimentdownload_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.experimentupload_file(filename='')
    def show_summary(self) -> None:
        """
        Print a Markdown-formatted summary of a YCSB experiment.

        Covers workflow (actual vs. planned), per-connection and per-run loading stats,
        execution throughput and latency by operation type, application metrics, and
        pass/fail test assertions including a check for FAILED columns.
        """
        self._test_results = []
        connections_sorted, monitoring_applications = self.show_summary_header()
        #####################
        df = self.evaluator.get_df_benchmarking()
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
        df = self.evaluator.get_summary_loading_per_connection()
        if self.loading_is_active() and not df.empty:
            print("\n### Loading")
            print("\n#### Per Connection\n")
            df = self.evaluator.get_summary_loading_per_connection()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Run\n")
            df = self.evaluator.get_summary_loading_per_run()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            df_aggregated_loaded = df.copy()
            test_loading = True
        else:
            df_aggregated_loaded = pd.DataFrame()
            test_loading = False
        if self.benchmarking_is_active():
            print("\n### Execution")
            print("\n#### Per Connection\n")
            df = self.evaluator.get_summary_benchmark_per_connection()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Phase\n")
            df = self.evaluator.get_summary_benchmark_per_phase()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            df_aggregated_reduced = df.copy()
        else:
            df_aggregated_reduced = pd.DataFrame()
        contains_failed = any('FAILED' in col for col in df_aggregated_reduced.columns)
        self.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            for title, metrics in monitoring_applications.items():
                print("\n#### "+title+"\n")
                metrics.index.names = ["DBMS"]
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        if test_loading:
            self._test_column(df_aggregated_loaded, "[OVERALL].Throughput(ops/sec)", title="Loading Phase:")
        self._test_column(df_aggregated_reduced, "[OVERALL].Throughput(ops/sec)", title="Execution Phase:")
        if self.benchmarking_is_active():
            self._record_test(self.test_workflow(workflow_actual, workflow_planned), "Workflow as planned")
        self._record_test(not contains_failed, "Execution Phase: contains no FAILED column" if not contains_failed else "Execution Phase: contains FAILED column")
        self._print_test_summary()
        return not contains_failed

