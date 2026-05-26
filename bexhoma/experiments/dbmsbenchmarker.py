"""
Experiment class for DBMSBenchmarker benchmarks.

Provides :class:`dbmsbenchmarker`, which extends :class:`base` to orchestrate
the DBMSBenchmarker tool inside a Kubernetes cluster, including loading,
benchmarking, and result collection phases.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import logging
import urllib3
import pandas as pd

from bexhoma import evaluators
from .base import base

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["dbmsbenchmarker"]

# DBMSBenchmarker experiment class


class dbmsbenchmarker(base):
    """
    Class for defining an DBMSBenchmarker experiment.
    This
    
    * merges results for different connections into one
    """
    def __init__(self,
            cluster,
            code=None,
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            ):
        base.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)
        self.evaluator = evaluators.dbmsbenchmarker(                    # evaluator specific to DBMSBenchmarker result format
            code=self.code, path=self.cluster.resultfolder, include_loading=True, include_benchmarking=True)
    def evaluate_results(self,
                         pod_dashboard: str = '') -> None:
        """
        Let the dashboard pod build the evaluations.
        This is specific to dbmsbenchmarker.

        1) All local logs are copied to the pod.
        2) Benchmarker in the dashboard pod is updated (dev channel)
        3) All results of all DBMS are joined (merge.py of benchmarker) in dashboard pod
        4) Evaluation cube is built (python benchmark.py read -e yes) in dashboard pod
        """
        self.cluster.logger.debug('dbmsbenchmarker.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        self.workload['workflow_errors'] = self.evaluator.workflow_errors
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
        # specific to dbmsbenchmarker
        cmd = {}
        cmd['update_dbmsbenchmarker'] = 'git pull'#/'+str(self.code)
        self.cluster.execute_command_in_pod(command=cmd['update_dbmsbenchmarker'], pod=pod_dashboard, container="dashboard")
        if self.benchmarking_is_active():
            #print("Join results ", end="", flush=True)
            print("{:30s}: join results...".format("Experiment"), end="", flush=True)
            cmd['merge_results'] = 'python merge.py -r /results/ -c '+str(self.code)
            self.cluster.execute_command_in_pod(command=cmd['merge_results'], pod=pod_dashboard, container="dashboard")
            print("done!")
        #print("Build evaluation cube ", end="", flush=True)
        print("{:30s}: build evaluation cube...".format("Experiment"), end="", flush=True)
        cmd['evaluate_results'] = 'python benchmark.py read -e yes -r /results/'+str(self.code)
        self.cluster.execute_command_in_pod(command=cmd['evaluate_results'], pod=pod_dashboard, container="dashboard")
        print("done!")
        # download evaluation cubes
        print("{:30s}: downloading partial results".format("Experiment"))
        self.experimentdownload_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.experimentupload_file(filename='')
    def show_summary(self) -> None:
        """
        Print a Markdown-formatted summary of a DBMSBenchmarker experiment.

        Covers workflow, loading times, per-connection and per-phase execution stats,
        query latencies, SQL errors, SQL warnings, monitoring metrics, and
        pass/fail test assertions.
        """
        self._test_results = []
        self.evaluator.load_inspector()
        connections_sorted, monitoring_applications = self.show_summary_header()
        #####################
        df = self.evaluator.get_df_benchmarking()
        if self.benchmarking_is_active():
            print("\n### Workflow")
            df = self.evaluator.get_summary_benchmark_per_connection()
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
            df.drop('configuration', axis=1, inplace=True, errors='ignore')
            df.drop('pod', axis=1, inplace=True, errors='ignore')
            print(df.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Phase\n")
            df = self.evaluator.get_summary_benchmark_per_phase()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            df_aggregated_reduced = df.copy()
            print("\n### Latency of Timer Execution [ms]")
            num_of_queries = 0
            df = self.evaluator.get_query_latencies(query_titles=True)
            if not df is None:
                df = df.sort_index().T.round(2)
                df.index.names = ["Queries"]
                print(df.to_markdown(index=True, floatfmt=".2f"))
                num_of_queries = len(df.index)
            print("\n### Errors (failed queries)\n")
            df = self.evaluator.get_total_errors(query_titles=True)
            num_errors = df.sum().sum()
            if num_errors > 0:
                df_errors = df.copy()
                df_errors = df_errors[~(df_errors == False).all(axis=1)]
                list_error_queries = list(df_errors.index)
                # remove only False rows
                df = df[~(df == False).all(axis=1)]
                print(df.to_markdown(index=True, floatfmt=".2f"))
                for error in list_error_queries:
                    numQuery = error[1:]        # remove the leading "Q"
                    list_errors = self.evaluator.evaluation.get_error(numQuery)
                    list_errors = {k:v for k,v in list_errors.items() if len(v) > 0}
                    print("* "+error)
                    for k,v in list_errors.items():
                        print("  * {}: {}".format(k,v))
            else:
                print("No errors")
            print("\n### Warnings (result mismatch)\n")
            df = self.evaluator.get_total_warnings(query_titles=True)
            num_warnings = df.sum().sum()
            if num_warnings > 0:
                # remove only False rows
                df = df[~(df == False).all(axis=1)]
                print(df.to_markdown(index=True, floatfmt=".2f"))
            else:
                print("No warnings")
        else:
            df_aggregated_reduced = pd.DataFrame()
        #####################
        self.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            for title, metrics in monitoring_applications.items():
                print("\n#### "+title+"\n")
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        if self.benchmarking_is_active():
            self._test_column(df_aggregated_reduced, "Geo Times [s]")
            self._test_column(df_aggregated_reduced, "Power@Size [~Q/h]")
            self._test_column(df_aggregated_reduced, "Throughput@Size")
            passed_errors = num_errors == 0
            self._record_test(passed_errors, "No SQL errors" if passed_errors else "SQL errors")
            passed_warnings = num_warnings == 0
            self._record_test(passed_warnings, "No SQL warnings" if passed_warnings else "SQL warnings (result mismatch)")
            self._record_test(self.test_workflow(workflow_actual, workflow_planned), "Workflow as planned")
        self._print_test_summary()


