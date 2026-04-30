"""
Base collector class for aggregating results from multiple bexhoma experiments.

Provides :func:`get_non_constant` and :class:`base`, which handles reading
workload and connection configurations, collecting performance metrics per
client and per phase, and aggregating monitoring time-series data across
experiment codes — including multi-tenant variants. Subclasses override
:meth:`base.get_evaluator` to supply the benchmark-specific evaluator.

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


def get_non_constant(df):
    """
    Filters a DataFrame to keep only columns whose values vary across rows.

    :param df: Input DataFrame.
    :type df: pandas.DataFrame
    :return: DataFrame containing only non-constant columns.
    :rtype: pandas.DataFrame
    """
    def is_not_constant(s):
        return s.nunique(dropna=False) > 1
    return df.loc[:, df.apply(is_not_constant)]


class base():
    """
    Base class for collecting and aggregating results from several experiments.

    Subclasses override :meth:`get_evaluator` to return a benchmark-specific
    evaluator. All data retrieval and aggregation methods are defined here.

    :Date: 2025-07-22
    :Version: 0.8.10
    """
    def __init__(self, path, codes):
        """
        :param path: Base filesystem path that contains the experiment directories.
        :type path: str
        :param codes: List of experiment codes to collect results for.
        :type codes: list[str]
        """
        self.path = path
        self.codes = codes
        self.with_monitoring = True
        evaluation = self.get_evaluator(codes[0])
        self.df_metrics = self.get_metrics(evaluation)

    def get_metrics_metadata(self):
        """
        Returns the metrics metadata DataFrame built during initialisation.

        :return: DataFrame listing monitored hardware metrics and their metadata.
        :rtype: pandas.DataFrame
        """
        return self.df_metrics

    def get_workload(self, code=''):
        """
        Returns the workload configuration of an experiment.

        Reads the ``queries.config`` file for the given experiment code and
        returns its contents as a dictionary.  The ``tenant_per`` key is
        normalised to the string ``'None'`` when absent or empty.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: Workload properties dictionary.
        :rtype: dict
        """
        if code == '':
            code = self.codes[0]
        with open(self.path + "/" + code + "/queries.config", 'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
            if 'tenant_per' not in workload_properties or workload_properties['tenant_per'] == '':
                workload_properties['tenant_per'] = 'None'
            return workload_properties

    def get_monitored_components(self, code=''):
        """
        Returns a DataFrame of monitored components defined in the workload configuration.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: DataFrame indexed by component key with a ``description`` column,
                 or an empty DataFrame when monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        monitoring_components = self.get_workload(code=code)['monitoring_components']
        return pd.DataFrame.from_dict(monitoring_components, orient='index', columns=['description'])

    def get_performance_single(self, evaluation=None):
        """
        Returns unaggregated benchmarking performance metrics per client.

        Retrieves the benchmarking DataFrame from the evaluator, sorts it by
        experiment run and client, and returns the result without further aggregation.

        :param evaluation: Evaluator instance. Defaults to the first code's evaluator.
        :type evaluation: object
        :return: DataFrame of per-client performance metrics sorted by
                 ``code``, ``experiment_run``, and ``client``.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            evaluation = self.get_evaluator()
        df = evaluation.get_df_benchmarking()
        if not df.empty:
            df = df.sort_values(['code', 'experiment_run', 'client'])
        else:
            print(evaluation.code, "is empty")
        return df

    def get_performance_aggregated_per_phase(self, type="stream"):
        """
        Combines aggregated performance results from all experiment codes into one DataFrame.

        For each code:

        - initialises the evaluator and reads the workload configuration,
        - retrieves and types the per-client performance data,
        - aggregates across parallel pods grouped by phase,
        - prefixes ``phase``, ``configuration``, and the DataFrame index with the experiment code.

        :param type: Component type passed to the aggregation call (currently unused in this method).
        :type type: str
        :return: Combined DataFrame of aggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = self.get_performance_single(evaluation)
            df = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df, columns=['phase'])
            df_aggregated.index = evaluation.code + '-' + df_aggregated.index.astype(str)
            df_aggregated['phase'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['phase'].astype(str)
            df_aggregated['configuration'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['configuration'].astype(str)
            df_aggregated.drop('connection', axis=1, inplace=True)
            if df_aggregated.empty:
                continue
            df_aggregated['code'] = df_aggregated['code'].astype(str)
            df_aggregated = df_aggregated.drop(columns=['pod'])
            df_performance = pd.concat([df_performance, df_aggregated])
        return df_performance

    def get_performance_aggregated_per_phase_multitenant(self, type="stream"):
        """
        Combines aggregated multi-tenant performance results from all experiment codes into one DataFrame.

        Extends :meth:`get_performance_aggregated_per_phase` by annotating each row with
        tenant metadata (``type_tenants``, ``num_tenants``, ``vol_tenants``) read from the
        workload configuration before aggregation.

        :param type: Component type passed to the aggregation call (currently unused in this method).
        :type type: str
        :return: Combined DataFrame of aggregated multi-tenant performance metrics.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df = self.get_performance_single(evaluation)
            df = evaluation.benchmarking_set_datatypes(df)
            df['type_tenants'] = workload['tenant_per']
            df['num_tenants'] = workload['num_tenants']
            df['vol_tenants'] = workload['multi_tenant_volume']
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(
                df, columns=['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
            )
            df_aggregated['phase'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['phase'].astype(str)
            df_aggregated['configuration'] = df_aggregated['code'].astype(str) + "-" + df_aggregated['configuration'].astype(str)
            if df_aggregated.empty:
                continue
            df_aggregated['type_tenants'] = workload['tenant_per']
            df_aggregated['num_tenants'] = workload['num_tenants']
            df_aggregated['vol_tenants'] = workload['multi_tenant_volume']
            df_aggregated['code'] = df_aggregated['code'].astype(str)
            df_aggregated = df_aggregated.drop(columns=['pod', 'connection', 'phase'], errors='ignore')
            df_performance = pd.concat([df_performance, df_aggregated])
        return df_performance

    def get_monitoring_aggregated_per_phase_multitenant(self, type="stream"):
        """
        Combines aggregated multi-tenant monitoring metrics from all experiment codes into one DataFrame.

        Calls :meth:`get_monitoring_aggregated_per_phase` to collect the raw monitoring data,
        enriches it with connection metadata via :meth:`add_metadata`, then groups by
        ``(code, experiment_run, client, type_tenants, num_tenants)`` and reduces each
        metric column using ``'max'`` for ratio metrics and ``'sum'`` for counter metrics.
        ``'Total I/O Wait Time [s]'`` is always reduced with ``'max'``.

        :param type: Component type forwarded to :meth:`get_monitoring_aggregated_per_phase`.
        :type type: str
        :return: DataFrame of grouped multi-tenant monitoring metrics indexed by the
                 underscore-joined group key.
        :rtype: pandas.DataFrame
        """
        df = self.get_monitoring_aggregated_per_phase(type)
        df_metadata = self.add_metadata(df)
        metric_cols = df.columns
        filtered_agg_dict = {
            col: 'max' if self.df_metrics.loc[self.df_metrics['title'] == col, 'metric'].item() == 'ratio' else 'sum'
            for col in metric_cols if col in df.columns
        }
        if 'Total I/O Wait Time [s]' in filtered_agg_dict:
            filtered_agg_dict['Total I/O Wait Time [s]'] = 'max'
        cols = ['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
        #cols = ['code', 'configuration', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
        df_metadata = df_metadata.groupby(cols).agg(filtered_agg_dict)
        df_metadata[cols] = pd.DataFrame(df_metadata.index.tolist(), index=df_metadata.index)
        df_metadata.index = ['_'.join(map(str, i)) for i in df_metadata.index]
        return df_metadata

    def get_performance_per_connection(self):
        """
        Combines unaggregated performance results per connection from all experiment codes.

        For each code, retrieves the per-client performance data and prefixes the
        ``phase``, ``connection``, ``configuration``, and DataFrame index with the
        experiment code before concatenating.

        :return: Combined DataFrame of unaggregated performance metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_performance = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = self.get_performance_single(evaluation)
            df['phase'] = df['code'].astype(str) + "-" + df['phase'].astype(str)
            df['connection'] = df['code'].astype(str) + "-" + df['connection'].astype(str)
            df['configuration'] = df['code'].astype(str) + "-" + df['configuration'].astype(str)
            df.index = evaluation.code + '-' + df.index.astype(str)
            df_performance = pd.concat([df_performance, df])
        return df_performance

    def get_metrics(self, evaluation=None):
        """
        Returns metadata for the hardware metrics collected during the experiment.

        Reads ``connections.config`` for the given evaluation and extracts the
        monitoring metric definitions.  The returned DataFrame has one row per
        metric and the following columns:

        - ``title``: human-readable metric name,
        - ``active``: whether the metric was active (defaults to ``'True'``),
        - ``type``: metric category, e.g. ``'cluster'`` (default),
        - ``metric``: raw metric identifier.

        Sets ``self.with_monitoring = False`` and returns an empty DataFrame when
        no ``'metrics'`` key is found in the first connection's monitoring block.

        :param evaluation: Evaluator instance. Defaults to the first code's evaluator.
        :type evaluation: object
        :return: DataFrame of metric metadata indexed by metric key.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            evaluation = self.get_evaluator()
        with open(self.path + "/" + evaluation.code + "/connections.config", 'r') as inf:
            connections = ast.literal_eval(inf.read())
            connections_sorted = sorted(connections, key=lambda c: c['name'])
            result = dict()
            for c in connections_sorted:
                if 'metrics' not in c['monitoring']:
                    self.with_monitoring = False
                    return pd.DataFrame()
                for m, metric in c['monitoring']['metrics'].items():
                    if m in result:
                        continue
                    result[m] = {
                        'title': metric['title'],
                        'active': metric['active'] if 'active' in metric else 'True',
                        'type': metric['type'] if 'type' in metric else 'cluster',
                        'metric': metric['metric'] if 'metric' in metric else '',
                    }
            return pd.DataFrame(result).T


    def get_connections(self, evaluation=None):
        """
        Returns connection metadata for all experiments in the collection.

        When called without arguments, iterates over ``self.codes`` and concatenates
        the result of :meth:`get_connections_of_experiment` for each code.  When an
        ``evaluation`` is provided, returns only the connections for that experiment.

        Key columns in the returned DataFrame:
        ``phase``, ``code``, ``connection``, ``configuration``,
        ``experiment_run``, ``client``, ``type_tenants``, ``num_tenants``,
        ``vol_tenants``.

        :param evaluation: Evaluator instance. If provided, only that experiment is queried.
        :type evaluation: object, optional
        :return: DataFrame of connection metadata.
        :rtype: pandas.DataFrame
        """
        if evaluation is None:
            df_connections = pd.DataFrame()
            for code in self.codes:
                evaluation = self.get_evaluator(code)
                df_connection = evaluation.get_connections_of_experiment()
                df_connections = pd.concat([df_connections, df_connection])
            return df_connections
        else:
            return evaluation.get_connections_of_experiment()

    def show_summary_monitoring_table(self, evaluation, type='stream'):
        """
        Collects all active monitoring metrics for a given component without aggregation.

        Iterates over ``self.df_metrics``, skipping inactive metrics, and fetches the
        time-series data for each metric via the evaluator.  Counter metrics are reduced
        by ``max - min``; ratio metrics by ``max``; all others by ``mean``.
        Results are combined column-wise into a summary DataFrame.

        :param evaluation: Evaluator instance providing the monitoring data.
        :type evaluation: object
        :param type: Component name to retrieve metrics for (e.g. ``'stream'``, ``'database'``).
        :type type: str
        :return: Summary DataFrame of monitoring metrics rounded to two decimal places,
                 or an empty DataFrame when monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        results = []
        for idx, row in self.df_metrics.iterrows():
            if row["active"] == False:
                continue
            metric_name = idx
            method = 'diff' if row["metric"] == 'counter' else 'mean'
            col_name = row["title"]
            df = evaluation.get_monitoring_metric(metric=metric_name, component=type)
            if method == 'diff':
                processed = df.max().sort_index() - df.min().sort_index()
            elif method == 'max':
                processed = df.max().sort_index()
            elif method == 'mean':
                processed = df.mean().sort_index()
            else:
                raise ValueError(f"Unknown processing method: {method}")
            df_cleaned = pd.DataFrame(processed)
            df_cleaned.columns = [col_name]
            results.append(df_cleaned)
        return pd.concat(results, axis=1).round(2)

    def get_monitoring_timeseries_single(self, code, metric='pg_locks_count', component="stream"):
        """
        Returns a single monitoring metric as a wide-format time-series DataFrame.

        Rows are timestamps; columns are monitored component instances (e.g. pods).

        :param code: Experiment identifier.
        :type code: str
        :param metric: Monitoring metric name (default ``'pg_locks_count'``).
        :type metric: str
        :param component: Component name to filter metrics (default ``'stream'``).
        :type component: str
        :return: Wide-format time-series DataFrame, or empty if monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        evaluate = self.get_evaluator(code)
        return evaluate.get_monitoring_metric(metric=metric, component=component)

    def get_monitoring_aggregated_per_phase(self, type="stream"):
        """
        Combines aggregated monitoring metrics from all experiment codes into one DataFrame.

        For each code, calls :meth:`show_summary_monitoring_table` and concatenates the
        results.  The ``connection`` column is dropped from the combined result because
        it is no longer meaningful across experiments.

        :param type: Component type to filter monitoring metrics (default ``'stream'``).
        :type type: str
        :return: Combined DataFrame of aggregated monitoring metrics for all experiments,
                 or an empty DataFrame when monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_monitoring_all = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df_monitoring = self.show_summary_monitoring_table(evaluation, type)
            if len(df_monitoring) > 0:
                df_monitoring_all = pd.concat([df_monitoring_all, df_monitoring.copy()])
        df_monitoring_all.drop('connection', axis=1, inplace=True, errors='ignore')
        return df_monitoring_all

    def get_monitoring_timeseries_per_phase(self, code, metric='pg_locks_count', component="stream"):
        """
        Returns a single monitoring metric as a transposed time-series DataFrame.

        Compared to :meth:`get_monitoring_timeseries_single`, the result is transposed so
        that rows are monitored component instances and columns are timestamps.

        :param code: Experiment identifier.
        :type code: str
        :param metric: Monitoring metric name (default ``'pg_locks_count'``).
        :type metric: str
        :param component: Component name to filter metrics (default ``'stream'``).
        :type component: str
        :return: Transposed time-series DataFrame, or empty if monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        evaluate = self.get_evaluator(code)
        df = evaluate.get_monitoring_metric(metric=metric, component=component)
        return df.T

    def add_metadata(self, df):
        """
        Joins connection metadata from :meth:`get_connections` onto a monitoring DataFrame.

        Attempts to merge ``df`` with the connection metadata using one of several
        strategies, tried in order:

        1. **Index × phase column** — when ``df``'s index intersects
           ``df_connections['phase']``.
        2. **Shared index** — when both DataFrames share common index values.
        3. **Phase column join** — when both DataFrames have a ``phase`` column.
        4. **Multi-tenant key join** — when both DataFrames have
           ``(code, experiment_run, client, type_tenants, num_tenants)`` columns.

        If none of the strategies match, a warning is printed and ``None`` is returned.

        :param df: Monitoring DataFrame to enrich with connection metadata.
        :type df: pandas.DataFrame
        :return: Enriched DataFrame with connection metadata columns added.
        :rtype: pandas.DataFrame
        """
        df_connections = self.get_connections()
        intersection = df.index.intersection(df_connections['phase'])
        if not intersection.empty:
            print("combine on index and column 'phase'")
            if 'phase' in df.columns:
                df.drop('phase', axis=1, inplace=True)
            cols_to_use = [c for c in df_connections.columns if c not in df.columns or c == 'phase']
            result = df.merge(
                df_connections[cols_to_use].drop_duplicates('phase'),
                left_index=True,
                right_on='phase',
                how='inner'
            ).set_index('phase').copy()
            result['phase'] = result.index
            result.drop('connection', axis=1, inplace=True, errors='ignore')
            return result

        cols_phase = ['phase']
        cols_multi_tenant = ['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
        cols_loading = ['code', 'configuration', 'experiment_run']
        check_phase = all(set(cols_phase).issubset(d.columns) for d in [df, df_connections])
        check_multi_tenant = all(set(cols_multi_tenant).issubset(d.columns) for d in [df, df_connections])
        check_loading = all(set(cols_loading).issubset(d.columns) for d in [df, df_connections])

        intersection = df.index.intersection(df_connections.index)
        if not intersection.empty:
            print("combine on index")
            cols_to_use = [c for c in df_connections.columns if c not in df.columns]
            return df.join(df_connections[cols_to_use], how='inner')

        elif check_phase:
            print("combine on columns " + " ".join(cols_phase))
            indexname = df.index.name
            df_connections = df_connections.drop_duplicates(subset=cols_phase, keep='first')
            df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
            df = df.set_index(cols_phase, drop=False)
            df_connections = df_connections.set_index(cols_phase, drop=False)
            result = df.combine_first(df_connections)
            result.index.name = indexname
            return result

        elif check_multi_tenant:
            print("combine on columns " + " ".join(cols_multi_tenant))
            indexname = df.index.name
            df_connections = df_connections.drop_duplicates(subset=cols_multi_tenant, keep='first')
            df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
            df = df.set_index(cols_multi_tenant, drop=False)
            df_connections = df_connections.set_index(cols_multi_tenant, drop=False)
            # normalise index tuples to strings for consistent matching
            df.index = pd.MultiIndex.from_tuples(
                [tuple(map(str, t)) for t in df.index],
                names=df.index.names
            )
            df_connections.index = pd.MultiIndex.from_tuples(
                [tuple(map(str, t)) for t in df_connections.index],
                names=df_connections.index.names
            )
            result = df.combine_first(df_connections)
            result.index = ['-'.join(map(str, i)) for i in result.index]
            return result

        elif check_loading:
            print("combine on columns " + " ".join(cols_loading))
            indexname = df.index.name
            df_connections = df_connections.drop_duplicates(subset=cols_loading, keep='first')
            df_connections.drop('connection', axis=1, inplace=True, errors='ignore')
            df = df.set_index(cols_loading, drop=False)
            df_connections = df_connections.set_index(cols_loading, drop=False)
            # normalise index tuples to strings for consistent matching
            df.index = pd.MultiIndex.from_tuples(
                [tuple(map(str, t)) for t in df.index],
                names=df.index.names
            )
            df_connections.index = pd.MultiIndex.from_tuples(
                [tuple(map(str, t)) for t in df_connections.index],
                names=df_connections.index.names
            )
            result = df.combine_first(df_connections)
            result.index = ['-'.join(map(str, i)) for i in result.index]
            # no pod_count means there has not been a logged loading phase
            if 'pod_count' in result.columns:
                result = result.dropna(subset=['pod_count'])
            return result

        else:
            print("combine failed!")

    def get_monitoring_timeseries_all(self, metric='pg_locks_count', component="stream"):
        """
        Collects long-format time-series data for a given metric across all experiment codes.

        For each code, fetches the wide-format time series, melts it to long format,
        merges connection metadata, and concatenates the results.  The final DataFrame
        is grouped by ``(timestamp, code, phase, experiment_run, client, type_tenants,
        vol_tenants, num_tenants, metric, component)`` and summed.

        :param metric: Monitoring metric name (default ``'pg_locks_count'``).
        :type metric: str
        :param component: Component name used as a label column (default ``'stream'``).
        :type component: str
        :return: Grouped long-format time-series DataFrame, or empty if monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_timeseries = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df_connections = self.get_connections(evaluation)
            df_monitoring = self.get_monitoring_timeseries_single(code, metric=metric)
            df_monitoring.index.name = "timestamp"
            df_long = df_monitoring.reset_index().melt(
                id_vars="timestamp",
                var_name="series",
                value_name="value"
            )
            df_long['metric'] = metric
            df_long['component'] = component
            df_long = pd.merge(df_long, df_connections, left_on='series', right_on='phase', how='left')
            df_timeseries = pd.concat([df_timeseries, df_long])
        df_sum = (
            df_timeseries
            .groupby(
                ["timestamp", "code", "phase", "experiment_run", "client",
                 "type_tenants", 'vol_tenants', "num_tenants", "metric", "component"],
                as_index=False
            )["value"]
            .sum()
        )
        return df_sum

    def get_monitoring_timeseries_all_multitenant(self, metric='pg_locks_count', component="stream"):
        """
        Collects long-format multi-tenant time-series data for a given metric across all experiment codes.

        Behaves like :meth:`get_monitoring_timeseries_all` but additionally annotates each
        row with tenant metadata (``type_tenants``, ``num_tenants``, ``vol_tenants``) from
        the workload configuration.  For non-container tenancy, the ``tenant`` column is
        set to ``"0"`` to indicate a single shared DBMS.

        The final DataFrame is grouped by ``(timestamp, code, experiment_run, client,
        type_tenants, vol_tenants, num_tenants, metric, component)`` and summed.

        :param metric: Monitoring metric name (default ``'pg_locks_count'``).
        :type metric: str
        :param component: Component name used as a label column (default ``'stream'``).
        :type component: str
        :return: Grouped long-format time-series DataFrame, or empty if monitoring is disabled.
        :rtype: pandas.DataFrame
        """
        if not self.with_monitoring:
            return pd.DataFrame()
        df_timeseries = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            workload = self.get_workload(code)
            df_connections = self.get_connections(evaluation)
            df_monitoring = self.get_monitoring_timeseries_single(code, metric=metric)
            df_monitoring.index.name = "timestamp"
            df_long = df_monitoring.reset_index().melt(
                id_vars="timestamp",
                var_name="series",
                value_name="value"
            )
            df_long['metric'] = metric
            df_long['component'] = component
            df_long = pd.merge(df_long, df_connections, left_on='series', right_on='phase', how='left')
            if workload['tenant_per'] == 'container':
                # one time series per container tenant
                pass
            else:
                # one shared DBMS — collapse tenant dimension
                df_long['tenant'] = "0"
            df_long['type_tenants'] = workload['tenant_per']
            df_long['num_tenants'] = workload['num_tenants']
            df_long['vol_tenants'] = workload['multi_tenant_volume']
            df_timeseries = pd.concat([df_timeseries, df_long])
        df_sum = (
            df_timeseries
            .groupby(
                ["timestamp", "code", "experiment_run", "client",
                 "type_tenants", 'vol_tenants', "num_tenants", "metric", "component"],
                as_index=False
            )
            .agg(value=("value", "sum"), configuration=("configuration", "max"))
        )
        return df_sum

    def get_evaluator(self, code=''):
        """
        Returns a benchmarking evaluator for the given experiment code.

        Subclasses override this method to return the appropriate evaluator type.
        The base implementation returns a :class:`evaluators.dbmsbenchmarker` instance.

        :param code: Experiment identifier. Defaults to the first code in ``self.codes``.
        :type code: str
        :return: Evaluator instance for the specified experiment.
        :rtype: evaluators.dbmsbenchmarker
        """
        if code == '':
            code = self.codes[0]
        return evaluators.dbmsbenchmarker(code=code, path=self.path)

    def get_loading_per_pod(self):
        """
        Combines loading metrics per pod from all experiment codes into one DataFrame.

        Concatenates the per-pod loading DataFrames returned by each evaluator.
        The ``connection``, ``phase``, and ``client`` columns are dropped from the result
        because they are not meaningful across experiments.

        :return: Combined DataFrame of per-pod loading metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_all = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_loading_per_pod()
            if len(df) > 0:
                df_all = pd.concat([df_all, df.copy()])
        df_all.drop('connection', axis=1, inplace=True, errors='ignore')
        df_all.drop('phase', axis=1, inplace=True, errors='ignore')
        df_all.drop('client', axis=1, inplace=True, errors='ignore')
        return df_all

    def get_loading_per_connection(self):
        """
        Combines loading metrics per connection from all experiment codes into one DataFrame.

        Concatenates the per-connection loading DataFrames returned by each evaluator.

        :return: Combined DataFrame of per-connection loading metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_all = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_loading_per_connection()
            if len(df) > 0:
                df_all = pd.concat([df_all, df.copy()])
        return df_all

    def get_loading_per_run(self):
        """
        Combines loading metrics per run from all experiment codes into one DataFrame.

        Concatenates the per-run loading DataFrames returned by each evaluator.

        :return: Combined DataFrame of per-run loading metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_all = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_loading_per_run()
            if len(df) > 0:
                df_all = pd.concat([df_all, df.copy()])
        return df_all

    def get_loading_per_run_multitenant(self):
        """
        Combines multi-tenant loading metrics per run from all experiment codes into one DataFrame.

        Concatenates the per-run multi-tenant loading DataFrames returned by each evaluator.

        :return: Combined DataFrame of per-run multi-tenant loading metrics for all experiments.
        :rtype: pandas.DataFrame
        """
        df_all = pd.DataFrame()
        for code in self.codes:
            evaluation = self.get_evaluator(code)
            df = evaluation.get_loading_per_run_multitenant()
            if len(df) > 0:
                df_all = pd.concat([df_all, df.copy()])
        return df_all

    def TEST_get_loading_per_run(self):
        """
        Experimental: computes per-run loading throughput in SF/h from per-connection data.

        Groups the per-connection loading result by ``(code, configuration, experiment_run)``,
        takes the column-wise maximum, then derives ``Throughput [SF/h]`` as
        ``SF * 3600 / time_load``.  The ``connection``, ``phase``, and ``client`` columns
        are dropped from the result.

        :return: DataFrame indexed by ``code-configuration-experiment_run`` with a
                 ``Throughput [SF/h]`` column added.
        :rtype: pandas.DataFrame
        """
        df_all = self.get_loading_per_connection()
        df = df_all.groupby(['code', 'configuration', 'experiment_run']).max()
        df = df.reset_index()
        df.index = (
            df['code'].astype(str) + "-"
            + df['configuration'].astype(str) + "-"
            + df['experiment_run'].astype(str)
        )
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0) / df_load.sort_index()
        df['Throughput [SF/h]'] = df_tpx
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('client', axis=1, inplace=True, errors='ignore')
        return df
