"""
Experiment class for TPC-H benchmarks.

Provides :class:`TpchExperiment`, which extends
:class:`DbmsBenchmarkerExperiment` to orchestrate TPC-H data generation,
loading, and query execution via the DBMSBenchmarker tool inside a Kubernetes
cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
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

__all__ = ["TpchExperiment"]


class TpchExperiment(DbmsBenchmarkerExperiment):
    """
    TPC-H experiment: orchestrates data generation, loading, and
    DBMSBenchmarker query execution inside a Kubernetes cluster.

    Registers a :class:`~bexhoma.benchmarks.tpch.TPCH` benchmark object and
    pre-populates the experiment dict template.  Workload configuration
    (modes, info strings, indexing strategies) is delegated to
    :meth:`~bexhoma.benchmarks.tpch.TPCH.configure_workload`.

    Extends :class:`DbmsBenchmarkerExperiment`.
    """

    def __init__(self,
                 cluster,
                 code=None,
                 queryfile='queries-tpch.config',
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
        DbmsBenchmarkerExperiment.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)
        self.SF = SF
        self.use_distributed_datasource = False
        if script is None:
            script = 'SF' + str(SF) + '-index'
        self.set_experiment(volume='tpch')
        self.cluster.set_experiments_configfolder('experiments/tpch')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_additional_labels(SF=SF)
        self.set_queryfile(queryfile)
        self.set_workload(
            name='TPC-H Queries SF=' + str(SF),
            info='This experiment performs some TPC-H inspired queries.',
            type='tpch',
        )
        self.storage_label = 'tpch-' + str(SF)
        self.add_benchmark(benchmarks.TPCH(SF=SF))
        self.experiment_dict_template = {
            "loader": [
                {
                    "name":        "tpch-loader",
                    "benchmarker": "dbmsbenchmarker",
                    "template":    "jobtemplate-loading-tpch-PostgreSQL.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ],
            "benchmarker": [[
                {
                    "name":        "tpch",
                    "benchmarker": "dbmsbenchmarker",
                    "template":    "jobtemplate-benchmarking-dbmsbenchmarker.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
                #{
                #    "name":        "tpch",
                #    "benchmarker": "dbmsbenchmarker",
                #    "template":    "jobtemplate-benchmarking-dbmsbenchmarker.yml",
                #    "parallelism": 1,
                #    "num_pods":    1,
                #    "target":      "sut",
                #    "parameters":  {},
                #},
            ]],
        }

    def enable_refresh_stream(self, template: str = "jobtemplate-benchmarking-tpch-refresh-PostgreSQL.yml") -> None:
        """
        Add a TPC-H RF1/RF2 refresh stream that runs in parallel with the query stream.

        The refresh stream becomes ``benchmark_run=2`` within each client round.
        Call :meth:`set_default_benchmarking_parameters` with ``TPCH_REFRESH_STREAMS``
        and ``TPCH_REFRESH_STREAM_OFFSET`` before calling this method so those values
        reach both the generator initContainer and the loader main container.

        :param template: k8s job-template file for the refresh benchmarker job.
            Choose the variant matching the target DBMS
            (``jobtemplate-benchmarking-tpch-refresh-PostgreSQL.yml`` or
            ``jobtemplate-benchmarking-tpch-refresh-MySQL.yml``).
        """
        self.experiment_dict_template["benchmarker"][0].append({
            "name":             "tpch-refresh",
            "benchmarker":      "tpch_refresh",
            "template":         template,
            "parallelism":      1,
            "num_pods":         1,
            "fixed_parallelism": True,
            "target":           "sut",
            "parameters":       {},
        })
        self.add_benchmark(benchmarks.RefreshStreamBenchmark(name='tpch_refresh', SF=self.SF))

    def show_summary(self) -> None:
        """
        Print the TPC-H experiment summary, including the refresh stream section.

        When :meth:`enable_refresh_stream` was called during the live run,
        :class:`~bexhoma.benchmarks.RefreshStreamBenchmark` is already in
        ``self.benchmarks`` and the generic loop inside
        :meth:`dbmsbenchmarker.show_summary` places the section right after
        ``### Execution → Per Phase``.

        When called post-hoc via ``bexperiments summary`` (no
        :meth:`enable_refresh_stream`), a temporary
        :class:`~bexhoma.benchmarks.RefreshStreamBenchmark` is appended to
        ``self.benchmarks`` before delegating to ``super()``, so the same loop
        positions it identically.  The temporary entry is removed afterwards.
        """
        refresh_added = False
        if not any(isinstance(bm, benchmarks.RefreshStreamBenchmark) for bm in self.benchmarks):
            refresh_bm = benchmarks.RefreshStreamBenchmark(name='tpch_refresh', SF=str(self.SF))
            refresh_bm.benchmark_index = 2
            refresh_bm.evaluator = refresh_bm.create_evaluator(
                self.code, self.cluster.resultfolder, 2
            )
            self.benchmarks.append(refresh_bm)
            refresh_added = True
        super().show_summary()
        if refresh_added:
            self.benchmarks.pop()

    def set_queries_full(self) -> None:
        """Switch to the full TPC-H query file covering all 22 queries."""
        self.set_queryfile('queries-tpch.config')

    def set_queries_profiling(self) -> None:
        """Switch to the abbreviated profiling query file for import validation."""
        self.set_queryfile('queries-tpch-profiling.config')

