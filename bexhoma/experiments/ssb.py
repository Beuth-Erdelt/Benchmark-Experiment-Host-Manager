"""
Experiment class for Star Schema Benchmark (SSB) experiments.

Provides :class:`SsbExperiment`, which extends :class:`DbmsBenchmarkerExperiment`
to orchestrate SSB data generation, loading, and query execution via the
DBMSBenchmarker tool inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3

from bexhoma import benchmarks
from .dbmsbenchmarker import DbmsBenchmarkerExperiment

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["SsbExperiment"]


class SsbExperiment(DbmsBenchmarkerExperiment):
    """
    SSB experiment: orchestrates data generation, loading, and DBMSBenchmarker
    query execution inside a Kubernetes cluster.

    Registers a :class:`~bexhoma.benchmarks.ssb.SSB` benchmark object and
    pre-populates the experiment dict template. Workload configuration (modes,
    schema and query variants, info strings, post-load scripts) is delegated to
    :meth:`~bexhoma.benchmarks.ssb.SSB.configure_workload`.

    Extends :class:`DbmsBenchmarkerExperiment`.
    """

    #: Every DBMS may be swept across CPU, RAM and storage class.
    supports_storage_sweep = True
    #: ``bexhoma summary`` rebuilds it from workload type ``ssb``.
    summary_from_type = True

    def __init__(self,
                 cluster,
                 code=None,
                 queryfile='queries-ssb.config',
                 SF='1',
                 num_experiment_to_apply=1,
                 timeout=7200):
        """
        :param cluster: Cluster object.
        :param code: Experiment identifier; auto-generated if ``None``.
        :param queryfile: DBMSBenchmarker query config file name.
        :param SF: Scaling factor — data size in GB.
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        """
        DbmsBenchmarkerExperiment.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)
        self.SF = SF
        self.use_distributed_datasource = False
        self.set_experiment(volume='ssb')
        self.cluster.set_experiments_configfolder('experiments/ssb')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_additional_labels(SF=SF)
        self.set_workload(
            name='SSB Queries SF=' + str(SF),
            info='This experiment performs the Star Schema Benchmark queries.',
            type='ssb',
        )
        self.storage_label = 'ssb-' + str(SF)
        self.add_benchmark(benchmarks.SSB(SF=SF))
        self.experiment_dict_template = {
            "loader": [
                {
                    "name":        "ssb-loader",
                    "benchmarker": "dbmsbenchmarker",
                    "template":    "jobtemplate-loading-ssb-PostgreSQL.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ],
            "benchmarker": [[
                {
                    "name":        "ssb",
                    "benchmarker": "dbmsbenchmarker",
                    "template":    "jobtemplate-benchmarking-dbmsbenchmarker.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ]],
        }
