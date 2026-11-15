"""
Collector for mixed-benchmark experiments.

Provides :class:`mixed`, which reads the ``benchmark_sequence`` persisted in
``queries.config`` by :meth:`~bexhoma.experiments.base.base.store_workflow_results`
and dispatches to the correct typed sub-collector for each benchmark-run index.

Use this collector when a single experiment code contains results from more than
one benchmark tool.  For experiments that use
only one benchmark tool, use the corresponding typed collector directly.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import CollectorBase

__all__ = ["MixedCollector"]


def collector_class_for_type(bm_type: str) -> type:
    """
    The collector class of the benchmark that a ``benchmark_sequence`` entry names.

    :param bm_type: ``'type'`` of the entry.
    :return: Collector class registered for that benchmark.
    :raises KeyError: If no benchmark is registered for ``bm_type``, or it has no collector.
    """
    # imported here: the registry's descriptors import the collectors of this package
    from bexhoma.benchmarks import registry
    descriptor = registry.descriptor_for_type(bm_type)
    if descriptor is None or descriptor.collector is None:
        raise KeyError(bm_type)
    return descriptor.collector


class MixedCollector(CollectorBase):
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
        CollectorBase.__init__(self, path, codes)
        workload = self.get_workload(codes[0])
        self.benchmark_sequence: list[dict] = workload.get('benchmark_sequence', [])

    def get_typed_collector(self, benchmark_run: int) -> CollectorBase:
        """
        Returns a typed sub-collector scoped to a single benchmark-run index.

        The collector class is resolved by :func:`collector_class_for_type` from the
        ``'type'`` field of the matching entry in :attr:`benchmark_sequence`.

        :param benchmark_run: 1-based benchmark-run index.
        :type benchmark_run: int
        :return: Typed collector instance filtered to ``benchmark_run``.
        :rtype: CollectorBase
        :raises StopIteration: If ``benchmark_run`` is not found in
            :attr:`benchmark_sequence`.
        :raises KeyError: If no benchmark with a collector is registered for the type.
        """
        entry = next(e for e in self.benchmark_sequence if e['index'] == benchmark_run)
        bm_type = entry['type']
        collector_cls = collector_class_for_type(bm_type)
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
