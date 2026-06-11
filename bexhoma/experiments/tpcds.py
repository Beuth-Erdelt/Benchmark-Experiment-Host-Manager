"""
Experiment class for TPC-DS benchmarks.

Provides :class:`tpcds`, which extends :class:`dbmsbenchmarker` to orchestrate
TPC-DS data generation, loading, and query execution via the DBMSBenchmarker
tool inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3

from bexhoma import benchmarks
from .dbmsbenchmarker import dbmsbenchmarker

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["tpcds"]


class tpcds(dbmsbenchmarker):
    """
    TPC-DS experiment: orchestrates data generation, loading, and
    DBMSBenchmarker query execution inside a Kubernetes cluster.

    Registers a :class:`~bexhoma.benchmarks.tpcds.TPCDS` benchmark object and
    pre-populates the experiment dict template.  Workload configuration
    (modes, info strings, indexing strategies) is delegated to
    :meth:`~bexhoma.benchmarks.tpcds.TPCDS.configure_workload`.
    """

    def __init__(self,
                 cluster,
                 code=None,
                 queryfile='queries-tpcds.config',
                 SF='100',
                 num_experiment_to_apply=1,
                 timeout=7200,
                 script=None):
        """
        :param cluster: Cluster object.
        :param code: Experiment identifier; auto-generated if ``None``.
        :param queryfile: DBMSBenchmarker query config file name.
        :param SF: Scaling factor — data size in GB.
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        :param script: Init-script collection name; defaults to ``'SF{SF}-index'``.
        """
        dbmsbenchmarker.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)
        self.SF = SF
        self.use_distributed_datasource = False
        if script is None:
            script = 'SF' + str(SF) + '-index'
        self.set_experiment(volume='tpcds')
        self.cluster.set_experiments_configfolder('experiments/tpcds')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_additional_labels(SF=SF)
        self.set_workload(
            name='TPC-DS Queries SF=' + str(SF),
            info='This experiment performs some TPC-DS inspired queries.',
            type='tpcds',
        )
        self.storage_label = 'tpcds-' + str(SF)
        self.add_benchmark(benchmarks.TPCDS(SF=SF))
        self.experiment_dict_template = {
            "loader": [
                {
                    "name":        "tpcds-loader",
                    "benchmarker": "dbmsbenchmarker",
                    "template":    "jobtemplate-loading-tpcds-PostgreSQL.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ],
            "benchmarker": [[
                {
                    "name":        "tpcds",
                    "benchmarker": "dbmsbenchmarker",
                    "template":    "jobtemplate-benchmarking-dbmsbenchmarker.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ]],
        }

    def set_queries_full(self) -> None:
        """Switch to the full TPC-DS query file covering all 99 queries."""
        self.set_queryfile('queries-tpcds.config')

    def set_queries_profiling(self) -> None:
        """Switch to the abbreviated profiling query file for import validation."""
        self.set_queryfile('queries-tpcds-profiling.config')

