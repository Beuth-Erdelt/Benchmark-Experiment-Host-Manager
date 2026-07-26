"""
Experiment class for DBMSBenchmarker benchmarks.

Provides :class:`DbmsBenchmarkerExperiment`, which extends
:class:`MixedExperiment` to orchestrate the DBMSBenchmarker tool inside a
Kubernetes cluster, including loading, benchmarking, and result collection
phases.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import logging
import urllib3
import pandas as pd

from bexhoma import evaluators
from .mixed import MixedExperiment

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["DbmsBenchmarkerExperiment"]


class DbmsBenchmarkerExperiment(MixedExperiment):
    """
    Experiment class for DBMSBenchmarker-based benchmarks.

    Provides ``evaluate_results`` (which joins per-connection results on a
    dashboard pod and builds the evaluation cube) and ``show_summary`` (which
    presents per-query latencies, errors, and warnings).

    TPC-H and TPC-DS subclass this to add their own benchmark registration and
    experiment dict template.

    Subclasses: :class:`TpchExperiment`, :class:`TpcdsExperiment`.
    """

    def __init__(self,
                 cluster,
                 code=None,
                 SF='1',
                 num_experiment_to_apply=1,
                 timeout=7200):
        """
        :param cluster: Cluster object.
        :param code: Experiment identifier; auto-generated if ``None``.
        :param SF: Scaling factor (forwarded to sub-class templates).
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        """
        MixedExperiment.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)
        self.evaluator = evaluators.dbmsbenchmarker(
            code=self.code, path=self.cluster.resultfolder, include_loading=True, include_benchmarking=True)
        self.active_queries: list[int] | None = None
    def set_active_queries(self,
                           active_queries: list[int] | None) -> None:
        """
        Restrict the query workload to a set of query numbers.

        Only affects the per-experiment query config copy written to the
        result folder and uploaded to the cluster; the query config file in
        the corresponding ``experiments/`` folder is never modified. Query
        numbers are 1-based positions within the query config's ``queries``
        list. Queries not listed are marked inactive (``'active': False``)
        for this experiment.

        :param active_queries: 1-based query numbers to keep active, or
            ``None`` to leave every query's ``active`` flag as defined in the
            query config file.
        :type active_queries: list[int] | None
        """
        self.active_queries = active_queries
    def evaluate_results(self,
                         pod_dashboard: str = '') -> None:
        """
        Let the dashboard pod build the evaluations.
        This is specific to dbmsbenchmarker.

        1) All local logs are copied to the pod.
        2) Benchmarker in the dashboard pod is updated (dev channel)
        3) All results of all DBMS are joined (merge.py of benchmarker) in dashboard pod
        4) Evaluation cube is built (python benchmark.py read -e yes -scm) in dashboard
           pod; its stdout/stderr is persisted to ``evaluate_results.log`` in the result
           folder so the cube-building step can be inspected/timed after the fact.
           ``-scm`` skips dbmsbenchmarker's per-component (loading/streaming/loader/
           benchmarker/datagenerator) hardware metric aggregates, since bexhoma's own
           evaluators never read them (they are only consumed by dbmsbenchmarker's
           interactive evaluation notebooks).
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
        cmd['evaluate_results'] = 'python benchmark.py read -e yes -scm -r /results/'+str(self.code)
        _, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['evaluate_results'], pod=pod_dashboard, container="dashboard")
        self.cluster.logger.debug(stdout)
        filename_log = f"{self.cluster.resultfolder}/{self.code}/evaluate_results.log"
        with open(filename_log, "w") as f:
            f.write(stdout)
            if stderr:
                f.write(stderr)
        print("done!")
        # download evaluation cubes
        print("{:30s}: downloading partial results".format("Experiment"))
        self.download_experiment_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.upload_experiment_file(filename='')
    def show_summary(self, write_report: bool = False) -> None:
        """
        Print the experiment summary by delegating to the primary benchmark.

        Finds the benchmark with ``benchmark_index == 1`` and calls its
        :meth:`~bexhoma.benchmarks.base.Benchmark.show_summary` template method,
        passing this experiment as the context object.

        :param write_report: When ``True``, also write a tiered Markdown report
            (``report/index.md`` + detail files) to the result folder.
        """
        primary = next(bm for bm in self.benchmarks if bm.benchmark_index == 1)
        primary.show_summary(self, write_report=write_report)


