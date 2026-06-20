"""
Collector for DBMSBenchmarker experiments.

Provides :func:`map_index_to_queryname` and :class:`DbmsBenchmarkerCollector`, which
extends :class:`CollectorBase` with query-level aggregation methods for warnings,
errors, and execution latencies across multiple experiment codes.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import seaborn as sns
from math import floor
import ast
import json
import re
import numpy as np
from scipy.stats import gmean
import pprint

from dbmsbenchmarker import parameter, inspector

from bexhoma import evaluators
from .base import CollectorBase

__all__ = ["DbmsBenchmarkerCollector", "map_index_to_queryname"]


def map_index_to_queryname(numQuery):
    """
    Maps a query index string (e.g., ``'q1'``) to a human-readable title from the
    global ``query_properties`` dictionary.

    If the title cannot be resolved, the original input string is returned unchanged.

    :param numQuery: A query index string, typically a letter followed by a number (e.g., ``'q1'``).
    :type numQuery: str
    :return: The query title from ``query_properties``, or ``numQuery`` if not found.
    :rtype: str
    """
    global query_properties
    if (
        numQuery[1:] in query_properties
        and 'config' in query_properties[numQuery[1:]]
        and 'title' in query_properties[numQuery[1:]]['config']
    ):
        return query_properties[numQuery[1:]]['config']['title']
    return numQuery


class DbmsBenchmarkerCollector(CollectorBase):
    """
    Collector for DBMSBenchmarker experiments.

    Extends :class:`CollectorBase` with query-level aggregation methods for warnings,
    errors, and latencies. Overrides :meth:`get_evaluator` to return a
    :class:`evaluators.dbmsbenchmarker` instance.
    """
    def __init__(self, path, codes, benchmark_run: int = 0):
        """
        :param path: Base filesystem path that contains the experiment directories.
        :type path: str
        :param codes: List of experiment codes to collect results for.
        :type codes: list[str]
        :param benchmark_run: 1-based benchmark index to filter results to; 0 means all runs.
        :type benchmark_run: int
        """
        self.benchmark_run = benchmark_run
        CollectorBase.__init__(self, path, codes)

    def get_evaluator(self, code=''):
        """
        Returns a :class:`evaluators.dbmsbenchmarker` instance for the given experiment code.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: DBMSBenchmarker evaluator for the specified experiment.
        :rtype: evaluators.dbmsbenchmarker
        """
        if code == '':
            code = self.codes[0]
        return evaluators.dbmsbenchmarker(code=code, path=self.path, benchmark_run=self.benchmark_run)

    def get_total_warnings(self, query_titles=False):
        """
        Aggregates warning counts (result mismatches) across all experiment codes.

        For each code, retrieves the per-query warning DataFrame from the evaluator
        and prefixes its index with the experiment code before concatenating.

        :param query_titles: If ``True``, use human-readable query titles as index labels.
        :type query_titles: bool
        :return: A combined DataFrame of warning counts for all experiments.
        :rtype: pandas.DataFrame
        """
        df_result = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_total_warnings(query_titles)
            df.index = evaluation.code + '-' + df.index.astype(str)
            df_result = pd.concat([df_result, df])
        return df_result

    def get_total_errors(self, query_titles=False):
        """
        Aggregates error counts (failed queries) across all experiment codes.

        For each code, retrieves the per-query error DataFrame from the evaluator
        and prefixes its index with the experiment code before concatenating.

        .. note::
            The current implementation delegates to ``evaluation.get_total_warnings``.

        :param query_titles: If ``True``, use human-readable query titles as index labels.
        :type query_titles: bool
        :return: A combined DataFrame of error counts for all experiments.
        :rtype: pandas.DataFrame
        """
        df_result = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_total_errors(query_titles)
            df.index = evaluation.code + '-' + df.index.astype(str)
            df_result = pd.concat([df_result, df])
        return df_result

    def get_query_latencies(self, query_titles=False):
        """
        Aggregates query latency metrics across all experiment codes.

        For each code, retrieves the per-query latency DataFrame from the evaluator
        and prefixes its index with the experiment code before concatenating.

        :param query_titles: If ``True``, use human-readable query titles as index labels.
        :type query_titles: bool
        :return: A combined DataFrame of query latencies for all experiments.
        :rtype: pandas.DataFrame
        """
        df_result = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_query_latencies(query_titles)
            df.index = evaluation.code + '-' + df.index.astype(str)
            df_result = pd.concat([df_result, df])
        return df_result
