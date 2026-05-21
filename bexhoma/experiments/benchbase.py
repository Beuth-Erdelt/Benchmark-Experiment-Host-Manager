"""
Experiment class for Benchbase benchmarks.

Provides :class:`benchbase`, which extends :class:`base` to orchestrate
Benchbase workloads (e.g., TPC-C, SEATS, Twitter) inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3
import re
import pandas as pd
import json
from types import SimpleNamespace

from bexhoma import evaluators
from .base import base

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["benchbase"]

# Benchbase experiment class

class benchbase(base):
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
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            ):
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.SF = SF                                                    # Benchbase scaling factor (e.g. number of warehouses / 10 000 rows)
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
        self.storage_label = 'benchbase-'+str(SF)                      # label used to match persistent storage to this experiment
        self.jobtemplate_loading = "jobtemplate-loading-benchbase.yml"  # K8s job template for the Benchbase loading container
        self.evaluator = evaluators.benchbase(                          # evaluator specific to Benchbase result format
            code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
        self.benchmark = 'tpcc'                                         # active Benchbase workload; changed via set_benchmark_type()
        self.components = {                                             # maps component types to required sub-components (no datagenerator for Benchbase)
            "loader": {
                "sensor": True
             },
            "benchmarker": {
                "dbmsbenchmarker": True
            }
        }
    def set_benchmark_type(self, benchmark: str = 'tpcc') -> None:
        """
        Select the Benchbase workload to run and update the storage label and config folder accordingly.

        :param benchmark: Benchbase benchmark name, e.g. 'tpcc', 'ycsb', 'seats'.
        """
        self.benchmark = benchmark
        self.storage_label = f'benchbase-{self.benchmark}-{self.SF}'
        self.cluster.set_experiments_configfolder(f'experiments/benchbase/{benchmark}')
    def prepare_testbed(self, parameter: dict) -> None:
        """
        Configure the experiment from CLI-style parameter dict and delegate to base.

        Sets workload metadata, loading job template, and appends human-readable
        info lines about SF, benchmark type, duration, and target throughput factors.

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
            self.set_workload(
                name = 'Benchbase Data {} Loading SF={}'.format(type_of_benchmark, SF),
                info = 'This imports a Benchbase data set.',
                type = 'benchbase',
                defaultParameters = {'SF': SF}
            )
        else:
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
        base.prepare_testbed(self, parameter)
    def log_to_df(self, filename: str) -> pd.DataFrame:
        """
        Parse a Benchbase container log file and return its JSON result as a DataFrame.

        Looks for a ``####BEXHOMA####...####BEXHOMA####`` block in the log and decodes
        the embedded JSON.  Returns an empty DataFrame when the block is absent or the
        file cannot be read.

        :param filename: Absolute path to the log file.
        :return: Normalised DataFrame of the JSON result, or empty DataFrame on failure.
        """
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
    def DEPRECATED_get_parts_of_name(self, name: str) -> dict:
        parts_name = re.findall('{(.+?)}', self.name_format)
        parts_values = re.findall('-(.+?)-', "-"+name.replace("-","--")+"--")
        return dict(zip(parts_name, parts_values))
    def test_results(self) -> None:
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
        Print a Markdown-formatted summary of loading and benchmarking results for this Benchbase experiment.

        Covers workflow (actual vs. planned), loading times, execution throughput per
        connection and phase, application metrics, and pass/fail test assertions.
        """
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
        if self.loading_is_active():
            print("\n### Loading")
            print("\n#### Per Run\n")
            df = self.evaluator.get_summary_loading_per_run()
            print(df.to_markdown(index=True, floatfmt=".2f"))
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
        #####################
        test_results_monitoring = self.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
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


