"""
Experiment class for HammerDB TPC-C benchmarks.

Provides :class:`TpccExperiment`, which extends :class:`MixedExperiment` to
orchestrate HammerDB TPC-C workloads inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3

from bexhoma import benchmarks
from .mixed import MixedExperiment

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["TpccExperiment"]


class TpccExperiment(MixedExperiment):
    """
    TPC-C experiment: orchestrates HammerDB TPC-C loading and benchmarking
    inside a Kubernetes cluster.

    Registers a :class:`~bexhoma.benchmarks.tpcc.TPCC` benchmark object and
    pre-populates the experiment dict template with HammerDB-specific job templates.
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
        :param SF: Scaling factor — number of TPC-C warehouses.
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        """
        MixedExperiment.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.SF = SF
        self.set_experiment(volume='tpcc')
        self.set_experiment(script='Schema')
        self.set_experiment(indexing='Checks')
        self.cluster.set_experiments_configfolder('experiments/tpcc')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name='TPC-C Queries SF=' + str(SF),
            info='This experiment performs some TPC-C inspired workloads.',
            type='tpcc',
        )
        self.storage_label = 'hammerdb-' + str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-hammerdb.yml"
        self.jobtemplate_benchmarking = "jobtemplate-benchmarking-hammerdb.yml"
        self.components = {
            "loader": {"sensor": True},
            "benchmarker": {"dbmsbenchmarker": True},
        }
        self.add_benchmark(benchmarks.TPCC(SF=SF))
        self.experiment_dict_template = {
            "loader": [
                {
                    "name":        "tpcc-loader",
                    "benchmarker": "hammerdb",
                    "template":    "jobtemplate-loading-hammerdb.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ],
            "benchmarker": [[
                {
                    "name":        "tpcc",
                    "benchmarker": "hammerdb",
                    "template":    "jobtemplate-benchmarking-hammerdb.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ]],
        }

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
        self.download_experiment_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.upload_experiment_file(filename='')
