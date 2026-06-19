"""
Logger evaluator: reads benchmark log files into DataFrames.

Provides :class:`logger`, which extends :class:`base` by parsing
bexhoma benchmarker log files produced by Kubernetes pods and
transforming them into structured pandas DataFrames. All
benchmark-specific evaluators inherit from :class:`logger`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
import pickle
import json
import traceback
import ast
from dbmsbenchmarker import monitor
from datetime import datetime
import glob
from pathlib import Path

from .base import base, natural_sort


class logger(base):
    """
    Evaluator base that reads benchmark log files into DataFrames.

    Extends :class:`base` by implementing :meth:`end_benchmarking` and
    :meth:`end_loading` to parse pod log files, pickle the resulting DataFrames,
    and collect them into a single combined pickle per phase.
    All benchmark-specific evaluators (``benchbase``, ``ycsb``, ``tpcc``,
    ``dbmsbenchmarker``) inherit from this class.
    """
    def end_benchmarking(self, jobname):
        """
        Parses all benchmarker log files for a job and caches results as pickle files.

        Scans the result folder for files matching
        ``bexhoma-benchmarker-<jobname>*.dbmsbenchmarker.log``, calls
        :meth:`log_to_df` on each, and writes non-empty results to a
        ``<filename>.df.pickle`` side-car file.

        :param jobname: Job name used to filter matching log files.
        :type jobname: str
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker-" + jobname) and filename.endswith(".dbmsbenchmarker.log"):
                df = self.log_to_df(self.path + "/" + filename)
                if df.empty:
                    self.num_missing_benchmarking_dfs += 1
                else:
                    with open(self.path + "/" + filename + ".df.pickle", "wb") as f:
                        pickle.dump(df, f)
    def end_loading(self, jobname):
        """
        Parses all loader sensor log files for a job and caches results as pickle files.

        Scans the result folder for files matching
        ``bexhoma-loading-<jobname>*.sensor.log``, calls :meth:`log_to_df` on
        each, prints a message when errors are detected, and writes non-empty
        results to a ``<filename>.df.pickle`` side-car file.

        :param jobname: Job name used to filter matching log files.
        :type jobname: str
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-loading-" + jobname) and filename.endswith(".sensor.log"):
                full_path = self.path + "/" + filename
                df = self.log_to_df_loading(full_path)
                if df.empty:
                    self.num_missing_loading_dfs += 1
                    if full_path in self.workflow_errors:
                        print("Error in " + filename)
                        print(self.workflow_errors)
                else:
                    with open(self.path + "/" + filename + ".df.pickle", "wb") as f:
                        pickle.dump(df, f)
    def _collect_dfs(self, filename_result='', filename_source_start='', filename_source_end='', num_missing=0):
        """
        Collects all per-pod pickle DataFrames for one phase and writes a combined pickle.

        Scans the result folder for files matching
        ``<filename_source_start>*<filename_source_end>``, concatenates their
        DataFrames, sets ``connection`` as the index, adds a ``missing_dfs`` column
        with the count of absent pod DataFrames, and writes the result to
        ``<filename_result>``.

        :param filename_result: Name of the combined output pickle file.
        :type filename_result: str
        :param filename_source_start: Filename prefix used to match source pickle files.
        :type filename_source_start: str
        :param filename_source_end: Filename suffix used to match source pickle files.
        :type filename_source_end: str
        :param num_missing: Number of per-pod DataFrames that failed to parse and are absent from the union.
        :type num_missing: int
        """
        df_collected = None
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith(filename_source_start) and filename.endswith(filename_source_end):
                try:
                    df = pd.read_pickle(self.path + "/" + filename)
                except Exception:
                    num_missing += 1
                    continue
                if not df.empty:
                    df_collected = df.copy() if df_collected is None else pd.concat([df_collected, df])
                else:
                    num_missing += 1
        if df_collected is not None and not df_collected.empty:
            df_collected['missing_dfs'] = num_missing
            df_collected.set_index('connection', inplace=True, drop=False)
            with open(self.path + "/" + filename_result, "wb") as f:
                pickle.dump(df_collected, f)
    def _pickle_name_benchmarking(self) -> str:
        """
        Return the combined benchmarking pickle filename for this evaluator.

        Always returns ``bexhoma-benchmarker.{N}.all.df.pickle``, where ``N``
        is ``benchmark_run`` when set, or ``1`` when unset.

        :return: Pickle filename (basename only, not full path).
        :rtype: str
        """
        run = self.benchmark_run if self.benchmark_run > 0 else 1
        return f"bexhoma-benchmarker.{run}.all.df.pickle"

    def _pickle_name_loading(self) -> str:
        """
        Return the combined loading pickle filename for this evaluator.

        Loading is performed once per experiment, shared across all benchmark
        runs, so the name is always ``bexhoma-loading.all.df.pickle``.

        :return: Pickle filename (basename only, not full path).
        :rtype: str
        """
        return "bexhoma-loading.all.df.pickle"

    def evaluate_results(self, pod_dashboard=''):
        """
        Parses all pod log files and persists the results as pickled DataFrames.

        Calls :meth:`transform_all_logs_benchmarking` and :meth:`_collect_dfs` for the
        benchmarking phase when ``include_benchmarking`` is set, and analogously
        for the loading phase.  When ``benchmark_run > 0``, each phase writes a
        per-benchmark pickle file rather than the shared ``*.all.df.pickle``.
        """
        if self.include_benchmarking:
            self.num_missing_benchmarking_dfs = 0
            self.transform_all_logs_benchmarking()
            self._collect_dfs(
                filename_result=self._pickle_name_benchmarking(),
                filename_source_start="bexhoma-benchmarker",
                filename_source_end=".log.df.pickle",
                num_missing=self.num_missing_benchmarking_dfs)
        if self.include_loading:
            self.num_missing_loading_dfs = 0
            self.transform_all_logs_loading()
            self._collect_dfs(
                filename_result=self._pickle_name_loading(),
                filename_source_start="bexhoma-loading",
                filename_source_end=".log.df.pickle",
                num_missing=self.num_missing_loading_dfs)

    def get_df_benchmarking(self):
        """
        Returns the DataFrame containing all benchmarking-phase results.

        Reads from the combined pickle file, triggering :meth:`evaluate_results`
        to generate it on first access if it does not yet exist.

        Ensures a ``pods`` column is present: when the pickle was written before
        this column was added (older runs), it is derived from ``pod_count``.

        :return: DataFrame of benchmarking results, or empty DataFrame when unavailable.
        :rtype: pandas.DataFrame
        """
        pickle_path = self.path + "/" + self._pickle_name_benchmarking()
        if not os.path.isfile(pickle_path):
            self.evaluate_results()
        if os.path.isfile(pickle_path):
            df = pd.read_pickle(pickle_path)
            if 'pods' not in df.columns and 'pod_count' in df.columns:
                df['pods'] = df['pod_count']
            return df
        return pd.DataFrame()

    def get_df_loading(self):
        """
        Returns the DataFrame containing all loading-phase results.

        Reads from the combined pickle file if it exists.

        :return: DataFrame of loading results, or empty DataFrame when unavailable.
        :rtype: pandas.DataFrame
        """
        pickle_path = self.path + "/" + self._pickle_name_loading()
        if os.path.isfile(pickle_path):
            return pd.read_pickle(pickle_path)
        return pd.DataFrame()
    def plot(self, df, column, x, y, plot_by=None, kind='line', dict_colors=None, figsize=(12,8)):
        """
        Plots one or more line (or other) charts from a DataFrame.

        When ``plot_by`` is ``None``, a single chart is produced with one line
        per value in ``column``.  When ``plot_by`` is given, a grid of sub-plots
        is created — one per group defined by ``plot_by`` — with lines split by
        ``column`` within each sub-plot.

        :param df: DataFrame containing the data to plot.
        :type df: pandas.DataFrame
        :param column: Column whose unique values define individual lines.
        :type column: str
        :param x: Column to use as the x-axis.
        :type x: str
        :param y: Column to use as the y-axis.
        :type y: str
        :param plot_by: Optional column whose values define separate sub-plots.
        :type plot_by: str or None
        :param kind: Plot kind passed to ``DataFrame.plot`` (e.g. ``'line'``, ``'bar'``).
        :type kind: str
        :param dict_colors: Optional colour mapping for the ``kind`` keyword.
        :type dict_colors: dict or None
        :param figsize: Figure size as ``(width, height)`` in inches.
        :type figsize: tuple
        :return: Matplotlib axes object (single axes when ``plot_by`` is ``None``).
        """
        if plot_by is None:
            fig, ax = plt.subplots()
            for key, grp in df.groupby(column):
                labels = "{} {}".format(key, column)
                ax = grp.plot(ax=ax, kind=kind, x=x, y=y, title=y, label=labels, figsize=figsize)
                ax.set_ylim(0,df[y].max())
            plt.legend(loc='best')
            return ax
        else:
            row_idx = 0
            col_idx = 0
            groups = df.groupby(plot_by)
            num_rows = (len(groups) + 1) // 2
            fig, axes = plt.subplots(nrows=num_rows, ncols=2, sharex=True, squeeze=False, figsize=(figsize[0], figsize[1] * num_rows))
            for key1, grp in groups:
                for key2, grp2 in grp.groupby(column):
                    labels = "{} {}, {} {}".format(key1, plot_by, key2, column)
                    if dict_colors is not None and len(dict_colors):
                        ax = grp2.plot(ax=axes[row_idx, col_idx], kind=kind, x=x, y=y, label=labels, title=y, figsize=figsize, layout=(num_rows, 2), color=dict_colors)
                    else:
                        ax = grp2.plot(ax=axes[row_idx, col_idx], kind=kind, x=x, y=y, label=labels, title=y, figsize=figsize, layout=(num_rows, 2))
                    ax.set_ylim(0, df[y].max())
                col_idx += 1
                if col_idx > 1:
                    row_idx += 1
                    col_idx = 0
            plt.legend(loc='best')
            plt.tight_layout()
            plt.show()
    def test_results(self):
        """
        Validates results by loading and reconstructing the workflow.

        :return: ``0`` on success, ``1`` if an exception is raised.
        :rtype: int
        """
        try:
            if self.include_benchmarking:
                df = self.get_df_benchmarking()
                self.workflow = self.reconstruct_workflow(df)
            if self.include_loading:
                self.get_df_loading()
            return 0
        except Exception as exc:
            print(exc)
            return 1
    def transform_monitoring_results(self, component="loading"):
        """
        Combines per-connection monitoring CSV files into a single wide-format CSV.

        For example, per-connection files like::

            query_datagenerator_metric_total_cpu_util_MonetDB-NIL-1-1.csv
            query_datagenerator_metric_total_cpu_util_MonetDB-NIL-1-2.csv

        are merged into::

            query_datagenerator_metric_total_cpu_util.csv

        :param component: Component label used in the metric filename prefix
                          (e.g. ``'loading'``, ``'stream'``).
        :type component: str
        """
        connections_sorted = self.get_connection_config()
        metric_keys = self.get_monitoring_metrics()
        for metric_key in metric_keys:
            df_all = None
            for connection in connections_sorted:
                conn_name = connection['orig_name'] if 'orig_name' in connection else connection['name']
                filename = "query_{component}_metric_{metric}_{connection}.csv".format(
                    component=component, metric=metric_key, connection=conn_name
                )
                df = monitor.metrics.loadMetricsDataframe(self.path + "/" + filename)
                if df is None:
                    continue
                df.columns = [conn_name]
                df_all = df if df_all is None else df_all.merge(df, how='outer', left_index=True, right_index=True)
            out_filename = "query_{component}_metric_{metric}.csv".format(component=component, metric=metric_key)
            monitor.metrics.saveMetricsDataframe(self.path + "/" + out_filename, df_all)
    def get_monitoring_metric(self, metric, component="loading"):
        """
        Returns a wide-format DataFrame of a single monitoring metric for a component.

        Reads the pre-combined CSV produced by :meth:`transform_monitoring_results`
        and returns it transposed so that rows are timestamps and columns are connections.

        :param metric: Metric key (e.g. ``'cpu_throttled_seconds_total'``).
        :type metric: str
        :param component: Component label used in the metric filename prefix.
        :type component: str
        :return: Wide-format DataFrame, or empty DataFrame if the file does not exist.
        :rtype: pandas.DataFrame
        """
        filename = '/query_{component}_metric_{metric}.csv'.format(component=component, metric=metric)
        if os.path.isfile(self.path+"/"+filename):
            df = pd.read_csv(self.path+"/"+filename).T
            df = df.reindex(index=natural_sort(df.index))
            return df.T
        else:
            return pd.DataFrame()
    def get_monitoring_metrics(self):
        """
        Returns the list of metric keys defined in the first connection's monitoring block.

        :return: List of metric key strings, or empty list when no metrics are configured.
        :rtype: list[str]
        """
        connections_sorted = self.get_connection_config()
        for conn in connections_sorted:
            if 'monitoring' in conn and 'metrics' in conn['monitoring']:
                return list(conn['monitoring']['metrics'].keys())
            return []
        return []

    def get_connection_config(self):
        """
        Returns the parsed ``connections.config`` as a list of connection dicts,
        sorted by connection name.

        :return: List of connection configuration dicts.
        :rtype: list[dict]
        """
        with open(self.path + "/connections.config", 'r') as f:
            connections = ast.literal_eval(f.read())
        return sorted(connections, key=lambda conn: conn['name'])

    def record_tests(self, experiment, df_loading: pd.DataFrame, df_reduced: pd.DataFrame,
                     workflow_actual: dict, workflow_planned: dict, **extra) -> None:
        """
        Record pass/fail test results for this benchmark.

        Default: tests only that the workflow matches the plan. Override in
        benchmark-specific evaluator subclasses to test metric columns.

        :param experiment: The owning experiment object.
        :param df_loading: Per-run loading DataFrame.
        :param df_reduced: Per-phase execution DataFrame.
        :param workflow_actual: Reconstructed actual workflow dict.
        :param workflow_planned: Planned workflow dict from workload config.
        """
        if experiment.benchmarking_is_active():
            experiment._record_test(
                experiment.test_workflow(workflow_actual, workflow_planned),
                "Workflow as planned"
            )


