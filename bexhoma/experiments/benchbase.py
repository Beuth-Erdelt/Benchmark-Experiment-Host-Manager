"""
Experiment class for Benchbase benchmarks.

Provides :class:`benchbase`, which extends :class:`mixed` to orchestrate
Benchbase workloads (e.g., TPC-C, SEATS, Twitter) inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3

from bexhoma import benchmarks
from .mixed import mixed

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["benchbase"]


class benchbase(mixed):
    """
    Benchbase experiment: orchestrates Benchbase loading and benchmarking
    inside a Kubernetes cluster.

    Registers a :class:`~bexhoma.benchmarks.benchbase.Benchbase` benchmark
    object and pre-populates the experiment dict template with Benchbase-specific
    job templates.
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
        :param SF: Scaling factor (rows ÷ 10 000 for most workloads).
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        """
        mixed.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.SF = SF
        self.set_experiment(volume='benchbase')
        self.set_experiment(script='Schema')
        self.set_experiment(indexing='Checks')
        self.cluster.set_experiments_configfolder('experiments/benchbase')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name='Benchbase Queries SF=' + str(SF),
            info='This experiment performs some Benchbase workloads.',
            type='benchbase',
        )
        self.storage_label = 'benchbase-' + str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-benchbase.yml"
        self.jobtemplate_benchmarking = "jobtemplate-benchmarking-benchbase.yml"
        self.benchmark_type = 'tpcc'
        self.components = {
            "loader": {"sensor": True},
            "benchmarker": {"dbmsbenchmarker": True},
        }
        self.add_benchmark(benchmarks.Benchbase(SF=SF))
        self.experiment_dict_template = {
            "loader": [
                {
                    "name":        "benchbase-loader",
                    "benchmarker": "benchbase",
                    "template":    "jobtemplate-loading-benchbase.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ],
            "benchmarker": [[
                {
                    "name":        "benchbase",
                    "benchmarker": "benchbase",
                    "template":    "jobtemplate-benchmarking-benchbase.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ]],
        }

    def set_benchmark_type(self, benchmark: str = 'tpcc') -> None:
        """
        Select the Benchbase workload to run and update the storage label and config folder accordingly.

        :param benchmark: Benchbase benchmark name, e.g. 'tpcc', 'ycsb', 'seats'.
        """
        self.benchmark_type = benchmark
        self.storage_label = f'benchbase-{benchmark}-{self.SF}'
        self.cluster.set_experiments_configfolder(f'experiments/benchbase/{benchmark}')

    def OLD_evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to Benchbase.
        """
        self.cluster.logger.debug('benchbase.evaluate_results()')
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
        print("{:30s}: downloading partial results".format("Experiment"))
        self.experimentdownload_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.experimentupload_file(filename='')
