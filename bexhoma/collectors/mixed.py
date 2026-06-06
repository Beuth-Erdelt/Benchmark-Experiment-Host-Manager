"""
Collector for mixed-benchmark experiments.

Provides :class:`mixed`, which reads the ``benchmark_sequence`` persisted in
``queries.config`` by :meth:`~bexhoma.experiments.base.base.store_workflow_results`
and dispatches to the correct typed sub-collector for each benchmark-run index.

Use this collector when a single experiment code contains results from more than
one benchmark tool (e.g. Benchbase followed by YCSB).  For experiments that use
only one benchmark tool, use the corresponding typed collector directly.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import base
from .benchbase import benchbase as benchbase_collector
from .ycsb import ycsb as ycsb_collector
from .tpcc import tpcc as tpcc_collector
from .dbmsbenchmarker import dbmsbenchmarker as dbmsbenchmarker_collector

__all__ = ["mixed"]

# Maps the benchmark tool name stored in queries.config to its collector class.
_COLLECTOR_FOR_TYPE: dict = {
    'benchbase':       benchbase_collector,
    'ycsb':            ycsb_collector,
    'tpcc':            tpcc_collector,
    'hammerdb':        tpcc_collector,
    'dbmsbenchmarker': dbmsbenchmarker_collector,
    'tpch':            dbmsbenchmarker_collector,
    'tpcds':           dbmsbenchmarker_collector,
}


class mixed(base):
    """
    Collector for experiments that contain multiple benchmark types.

    Reads the ``benchmark_sequence`` key from ``queries.config`` — written by
    :meth:`~bexhoma.experiments.base.base.store_workflow_results` — to determine
    which benchmark tool ran at each ``benchmark_run`` index.  Exposes one typed
    sub-collector per benchmark-run index via :meth:`get_typed_collector`, and a
    convenience method :meth:`get_performance_per_benchmark` that returns a dict
    of aggregated-performance DataFrames keyed by benchmark type name.

    :param path: Base filesystem path that contains the experiment directories.
    :param codes: List of experiment codes to collect results for.
    """

    def __init__(self, path: str, codes: list[str]) -> None:
        """
        :param path: Base filesystem path that contains the experiment directories.
        :type path: str
        :param codes: List of experiment codes to collect results for.
        :type codes: list[str]
        :raises KeyError: If ``queries.config`` for the first code does not contain
            ``'benchmark_sequence'``.
        """
        base.__init__(self, path, codes)
        workload = self.get_workload(codes[0])
        self.benchmark_sequence: list[dict] = workload.get('benchmark_sequence', [])

    def get_typed_collector(self, benchmark_run: int) -> base:
        """
        Returns a typed sub-collector scoped to a single benchmark-run index.

        The collector class is resolved from :data:`_COLLECTOR_FOR_TYPE` using the
        ``'type'`` field of the matching entry in :attr:`benchmark_sequence`.

        :param benchmark_run: 1-based benchmark-run index.
        :type benchmark_run: int
        :return: Typed collector instance filtered to ``benchmark_run``.
        :rtype: base
        :raises StopIteration: If ``benchmark_run`` is not found in
            :attr:`benchmark_sequence`.
        :raises KeyError: If the benchmark type is not registered in
            :data:`_COLLECTOR_FOR_TYPE`.
        """
        entry = next(e for e in self.benchmark_sequence if e['index'] == benchmark_run)
        bm_type = entry['type']
        collector_cls = _COLLECTOR_FOR_TYPE[bm_type]
        return collector_cls(self.path, self.codes, benchmark_run=benchmark_run)

    def get_performance_per_benchmark(self) -> dict:
        """
        Returns aggregated performance results separated by benchmark type.

        Iterates over :attr:`benchmark_sequence`, creates a typed sub-collector
        for each entry via :meth:`get_typed_collector`, and calls
        :meth:`~base.get_performance_aggregated_per_phase` on it.

        :return: Dict mapping benchmark type name to its aggregated-performance
                 DataFrame.  When two entries share the same type (parallel
                 runs of the same tool), both DataFrames are concatenated under
                 that key.
        :rtype: dict[str, pandas.DataFrame]
        """
        import pandas as pd
        result: dict = {}
        for entry in self.benchmark_sequence:
            bm_type = entry['type']
            collector = self.get_typed_collector(entry['index'])
            df = collector.get_performance_aggregated_per_phase()
            if bm_type in result:
                result[bm_type] = pd.concat([result[bm_type], df])
            else:
                result[bm_type] = df
        return result
