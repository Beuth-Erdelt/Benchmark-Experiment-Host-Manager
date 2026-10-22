"""
Evaluator for HammerDB TPC-C experiments.

Provides :class:`TpccEvaluator`, which extends :class:`LogEvaluator` to parse and aggregate
transactions-per-minute (TPM) and throughput results produced by HammerDB.

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


from .base import natural_sort
from .logger import LogEvaluator

__all__ = ["TpccEvaluator"]

#: Columns parsed from HammerDB's time profile (besides every ``* [ms]`` one).
#: A pod without a profile has none of them; they stay NaN instead of being
#: zero-filled, since a latency of 0 ms would read like a real measurement.
_PROFILE_COLUMNS = {'CALLS', 'SD', 'RATIO'}


#: Refresh rate of HammerDB's transaction counter in seconds (``tcset refreshrate``
#: in images/hammerdb/benchmarker/benchmarker.sh).
_TCOUNT_REFRESH = 10


def _is_profile_column(column) -> bool:
    return column in _PROFILE_COLUMNS or str(column).endswith(' [ms]')


def _fill_missing_counts(df):
    """
    Zero-fill missing values in place, except in time-profile columns.

    :param df: Raw TPC-C benchmarking DataFrame.
    :type df: pandas.DataFrame
    """
    columns = [column for column in df.columns if not _is_profile_column(column)]
    df[columns] = df[columns].fillna(0)


def _max_all(series):
    # NaN when any pod has no profile: the phase's worst latency is unknown.
    return series.max(skipna=False)


def _mean_all(series):
    return series.mean(skipna=False)


class TpccEvaluator(LogEvaluator):
    """
    Evaluator for a HammerDB TPC-C experiment.

    Parses per-pod log files to extract NOPM, TPM, and optional latency statistics
    (CALLS, MIN, AVG, MAX, TOTAL, P99, P95, P50, SD, RATIO) and assembles them into
    DataFrames.  Aggregation over parallel pods follows the same pattern as the other
    logger-based evaluators.

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Whether loading-phase results are expected.
    :param include_benchmarking: Whether benchmarking-phase results are expected.
    """
    def get_terminals(self, loading_parameters):
        """
        Returns the number of HammerDB virtual users from ``HAMMERDB_VUSERS``.

        :param loading_parameters: The connection's ``loading_parameters`` dict.
        :type loading_parameters: dict
        :return: Virtual user count, or ``0`` when not set.
        :rtype: int
        """
        return loading_parameters.get('HAMMERDB_VUSERS', 0)

    def log_to_df(self, filename):
        """
        Parses a HammerDB TPC-C pod log file into a DataFrame.

        Extracts NOPM, TPM, vuser counts, and — when HammerDB time-profile output
        is present — latency statistics (CALLS, MIN, AVG, MAX, TOTAL, P99, P95,
        P50, SD, RATIO) for the ``NEWORD`` procedure.

        :param filename: Absolute path to the HammerDB log file.
        :type filename: str
        :return: DataFrame with one row per TPC-C result iteration,
                 or empty on parse failure.
        :rtype: pandas.DataFrame
        """
        # test for known errors
        LogEvaluator.log_to_df(self, filename)
        # extract status and result fields
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            pod_name = filename[filename.rindex("-")+1:-len(".log")]
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)[0]
            configuration_name = re.findall('BEXHOMA_CONFIGURATION:(.+?)\n', stdout)[0]
            code = re.findall('BEXHOMA_EXPERIMENT:(.+?)\n', stdout)[0]
            experiment_run = re.findall('BEXHOMA_EXPERIMENT_RUN:(.+?)\n', stdout)[0]
            iterations = re.findall('HAMMERDB_ITERATIONS:(.+?)\n', stdout)[0]
            duration = re.findall('HAMMERDB_DURATION:(.+?)\n', stdout)[0]
            rampup = re.findall('HAMMERDB_RAMPUP:(.+?)\n', stdout)[0]
            sf = re.findall('SF:(.+?)\n', stdout)[0]
            vusers_loading = re.findall('HAMMERDB_NUM_VU:(.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            benchmark_run = re.findall('BEXHOMA_BENCHMARK_RUN:(.+?)\n', stdout)
            benchmark_run = benchmark_run[0] if benchmark_run else '1'
            timeprofile = re.findall('HAMMERDB_TIMEPROFILE:(.+?)\n', stdout)[0]
            allwarehouses = re.findall('HAMMERDB_ALLWAREHOUSES:(.+?)\n', stdout)[0]
            keyandthink = re.findall('HAMMERDB_KEYANDTHINK:(.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD:(.+?)\n', stdout)[0]
            error_timesynch = re.findall('start time has already passed', stdout)
            if len(error_timesynch) > 0:
                # log is incomplete
                print(filename, "log is incomplete")
                return pd.DataFrame()
            pod_count = re.findall('BEXHOMA_NUM_PODS:(.+?)\n', stdout)[0]
            errors = re.findall('Error ', stdout)
            if len(errors) > 0:
                # something went wrong
                print(filename, "something went wrong")
            num_errors = len(errors)
            results = re.findall("Vuser 1:TEST RESULT : System achieved (.+?) NOPM from (.+?) (.+?) TPM", stdout)
            vusers = re.findall("Vuser 1:(.+?) Active", stdout)
            result_tuples = list(zip(results, vusers))
            extracted_data = {}
            summary_match = re.search(r'SUMMARY OF (\d+) ACTIVE VIRTUAL USERS', stdout)
            if summary_match:
                relevant_text = stdout[summary_match.start():]
                neword_match = re.search('>>>>> PROC: NEWORD', relevant_text)
                if neword_match:
                    relevant_text = relevant_text[neword_match.start():]
                    separator = '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
                    end_index = relevant_text.find(separator)
                    if end_index != -1:
                        relevant_text = relevant_text[:end_index]
                    # match label-number pairs, e.g. "CALLS: 5426322", "MIN: 2.990ms"
                    for label, value in re.findall(r'(\w+):\s*([\d\.]+)', relevant_text):
                        if label in extracted_data or label + " [ms]" in extracted_data:
                            continue
                        if 'ms' in value or label in ['MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50']:
                            extracted_data[label + " [ms]"] = float(value.replace('ms', '').strip())
                        else:
                            extracted_data[label] = float(value.strip())
            sf_int = int(sf)
            vusers_first = int(float(result_tuples[0][1]))
            # efficiency is only meaningful when key-and-think time is enabled and vusers == 10 × SF
            if keyandthink == "true" and vusers_first == 10 * sf_int:
                efficiency = round(100. * float(result_tuples[0][0][0]) / sf_int / 12.86, 2)
            else:
                efficiency = 0
            phase = (configuration_name + '-' + experiment_run + '-' + client).lower()
            job = connection_name
            connection = connection_name + '-' + child
            latency_values = list(extracted_data.values())
            rows = [
                (connection, phase, job, configuration_name, experiment_run, client, benchmark_run, child, pod_name, pod_count,
                 code, iterations, duration, rampup, sf, run_idx, num_errors, vusers_loading,
                 vuser, efficiency, result[0], result[1], result[2], keyandthink) + tuple(latency_values)
                for run_idx, (result, vuser) in enumerate(result_tuples)
            ]
            df = pd.DataFrame(rows)
            col_names = ['connection', 'phase', 'job', 'configuration', 'experiment_run', 'client', 'benchmark_run', 'child', 'pod',
                         'pod_count', 'code', 'iterations', 'duration', 'rampup', 'sf', 'run',
                         'errors', 'vusers_loading', 'vusers', 'efficiency', 'NOPM', 'TPM', 'dbms', 'keyandthink']
            col_names.extend(list(extracted_data.keys()))
            df.columns = col_names
            df.index.name = connection_name
            return df
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return pd.DataFrame()
    def test_results(self):
        """
        Validates results by reading all pickle files and delegating to the parent check.

        :return: ``0`` on success, ``1`` if an exception is raised.
        :rtype: int
        """
        try:
            directory = os.fsencode(self.path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".pickle"):
                    df = pd.read_pickle(self.path+"/"+filename)
                    list(df['vusers'])
            return super().test_results()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return 1
    def benchmarking_set_datatypes(self, df):
        """
        Casts all TPC-C benchmarking result columns to their appropriate data types.

        Handles two variants: with latency statistics (``CALLS`` present) and without.

        :param df: DataFrame of raw TPC-C benchmarking results.
        :type df: pandas.DataFrame
        :return: DataFrame with columns cast to correct types.
        :rtype: pandas.DataFrame
        """
        if 'CALLS' in df:
            df_typed = df.astype({
                'connection':'str',
                'phase':'str',
                'job':'str',
                'configuration':'str',
                'experiment_run':'int',
                'code':'int',
                'client':'int',
                'benchmark_run':'int',
                'pod':'str',
                'pod_count':'int',
                'iterations':'int',
                'duration':'int',
                'rampup':'int',
                'sf':'int',
                'run':'int',
                'errors':'int',
                'vusers_loading':'int',
                'vusers':'int',
                'NOPM':'int',
                'TPM':'int',
                'efficiency':'float',
                'dbms':'str',
                'CALLS':'float',
                'MIN [ms]':'float',
                'AVG [ms]':'float',
                'MAX [ms]':'float',
                'TOTAL [ms]':'float',
                'P99 [ms]':'float',
                'P95 [ms]':'float',
                'P50 [ms]':'float',
            })
        else:
            df_typed = df.astype({
                'connection':'str',
                'phase':'str',
                'job':'str',
                'configuration':'str',
                'experiment_run':'int',
                'code':'int',
                'client':'int',
                'benchmark_run':'int',
                'pod':'str',
                'pod_count':'int',
                'iterations':'int',
                'duration':'int',
                'rampup':'int',
                'sf':'int',
                'run':'int',
                'errors':'int',
                'vusers_loading':'int',
                'vusers':'int',
                'NOPM':'int',
                'TPM':'int',
                'efficiency':'float',
                'dbms':'str',
            })
        if 'tenant_id' not in df_typed.columns:
            df_typed = df_typed.assign(tenant_id=-1)
        return df_typed
    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Aggregates parallel-pod TPC-C result rows into one row per group.

        Groups by ``columns`` and applies per-metric aggregation (NOPM/TPM averaged
        across pods, max for latency percentiles, etc.). Also recomputes efficiency for
        runs where vusers equal 10× the scale factor.

        The ``phase`` column holds the phase identifier
        (``configuration-experiment_run-client``) and the ``job`` column holds the
        job identifier (``configuration-experiment_run-client-benchmark_run``).

        The default ``columns=['phase']`` groups by phase, producing one row per phase.
        To keep one row per job, pass ``columns=['job']``.

        :param df: Typed TPC-C benchmarking DataFrame.
        :type df: pandas.DataFrame
        :param columns: Grouping columns (default ``['phase']``).
        :type columns: list[str]
        :return: Aggregated DataFrame with one row per group.
        :rtype: pandas.DataFrame
        """
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby([df[col] for col in columns]):
            if 'CALLS' in grp:
                aggregate = {
                    'connection':'max',
                    'job':'max',
                    'client':'max',
                    'benchmark_run':'max',
                    'code':'max',
                    'pod':'sum',
                    'pod_count':'count',
                    'iterations':'max',
                    'duration':'max',
                    'sf':'max',
                    'run':'max',
                    'errors':'sum',
                    'vusers_loading':'max',
                    'vusers':'sum',
                    'NOPM':'mean',
                    'TPM':'mean',
                    'efficiency':'min',
                    'dbms':'max',
                    'CALLS':_max_all,
                    'MIN [ms]':_max_all,
                    'AVG [ms]':_mean_all,
                    'MAX [ms]':_max_all,
                    'TOTAL [ms]':_max_all,
                    'P99 [ms]':_max_all,
                    'P95 [ms]':_max_all,
                    'P50 [ms]':_max_all,
                    'tenant_id': 'min',
                }
            else:
                aggregate = {
                    'code':'max',
                    'job':'max',
                    'client':'max',
                    'benchmark_run':'max',
                    'pod':'sum',
                    'pod_count':'count',
                    'iterations':'max',
                    'duration':'max',
                    'sf':'max',
                    'run':'max',
                    'errors':'sum',
                    'vusers_loading':'max',
                    'vusers':'sum',
                    'NOPM':'mean',
                    'TPM':'mean',
                    'efficiency':'min',
                    'dbms':'max',
                    'tenant_id': 'min',
                }
            if 'keyandthink' in grp:
                # missing in results parsed before it was kept
                aggregate['keyandthink'] = 'max'
            dict_grp = dict()
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['job'] = grp['job'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            df_grp = pd.DataFrame(dict_grp, index=["-".join(map(str, key))])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        # efficiency is only valid with key-and-think time and vusers == 10 × SF (standard TPC-C convention)
        df_aggregated['efficiency'] = 0.
        tpcc_mask = df_aggregated['sf'] * 10 == df_aggregated['vusers']
        if 'keyandthink' in df_aggregated:
            tpcc_mask &= df_aggregated['keyandthink'] == "true"
        df_aggregated.loc[tpcc_mask, 'efficiency'] = (
            100. * df_aggregated['NOPM'] / 12.86 / df_aggregated['sf']
        )
        return df_aggregated
    def parse_hammerdb_log_file(self, file_path):
        """
        Parses the HammerDB transaction counter lines of a pod log file.

        The benchmarker prints each transaction counter log (one per VU test) after
        the run.  Every counter line ``<n> <DBMS> tpm @ <date>`` becomes a dict with
        keys ``second`` (elapsed since the first counter line of the pod) and ``tpm``.
        ``second`` is rounded to the refresh rate: the counter sleeps 10 s and then
        queries, so its timestamps drift (180, 191, 201, ...) and pods would not line up.
        The first line after each ``Hammerdb Transaction Counter Log`` header is
        skipped: the counter always starts with 0, as it has no previous sample.

        :param file_path: Absolute path to the HammerDB pod log file.
        :type file_path: str
        :return: List of ``{'second': int, 'tpm': int}`` dicts.
        :rtype: list[dict]
        """
        pattern = re.compile(r'^(\d+) \S+ tpm @ \w+ (\w+)\s+(\d+) (\d{2}:\d{2}:\d{2}) \S+ (\d{4})$')
        datetime_first_measure = None
        skip_next = False
        results = []
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('Hammerdb Transaction Counter Log'):
                    skip_next = True
                    continue
                match = pattern.match(line)
                if not match:
                    continue
                if skip_next:
                    skip_next = False
                    continue
                tpm, month, day, time, year = match.groups()
                dt = datetime.strptime('{} {} {} {}'.format(year, month, day, time), '%Y %b %d %H:%M:%S')
                if datetime_first_measure is None:
                    datetime_first_measure = dt
                elapsed = (dt - datetime_first_measure).total_seconds()
                results.append({
                    "second": int(round(elapsed / _TCOUNT_REFRESH)) * _TCOUNT_REFRESH,
                    "tpm": int(tpm),
                })
        return results
    def benchmark_logs_to_timeseries_df(self, list_logs, metric="tpm", aggregate=True):
        """
        Parses HammerDB log files for the given pod IDs and assembles a time-series DataFrame.

        Each pod ID in ``list_logs`` is resolved to matching log files via a glob pattern.
        The transaction counter measures the whole database, so parallel pods report the
        same quantity: when ``aggregate`` is ``True`` the values are averaged per second
        (like NOPM and TPM in :meth:`benchmarking_aggregate_by_parallel_pods`).
        When ``aggregate`` is ``False`` a list of per-pod DataFrames is returned instead.

        :param list_logs: Pod IDs (short suffixes) used to locate matching log files.
        :type list_logs: list[str]
        :param metric: Metric column to extract (default ``'tpm'``).
        :type metric: str
        :param aggregate: Whether to aggregate all pod DataFrames into one.
        :type aggregate: bool
        :return: Aggregated DataFrame indexed by ``'second'`` (with an ``'avg'`` column
                 appended) when ``aggregate`` is ``True``, or a list of per-pod DataFrames.
        :rtype: pandas.DataFrame or list[pandas.DataFrame]
        """
        def find_matching_files(directory, pattern):
            return glob.glob(os.path.abspath(os.path.normpath(os.path.join(directory, pattern))))
        list_df = []
        for file_logs in list_logs:
            pattern = 'bexhoma-benchmarker-*-{}.log'.format(file_logs)
            for file in find_matching_files(self.path, pattern):
                parsed_results = self.parse_hammerdb_log_file(file)
                if not parsed_results:
                    continue
                df = pd.DataFrame(parsed_results).set_index('second')
                df = df.groupby(df.index).mean()  # collapse samples rounded to the same second
                list_df.append(df[[metric]])
        if not aggregate:
            return list_df
        if not list_df:
            return pd.DataFrame()
        df_total = pd.concat(list_df).groupby(level=0).mean()
        df_total['avg'] = int(df_total[metric].mean())
        return df_total
    def get_benchmark_logs_timeseries_df_aggregated(self, metric="tpm", configuration="", client='1', experiment_run='1'):
        """
        Returns a DataFrame of time series of a metric for the benchmarking phase,
        aggregated over all pods per second.

        Retrieves pod IDs from :meth:`get_df_benchmarking` filtered by the given
        ``configuration``, ``client``, and ``experiment_run``, then delegates to
        :meth:`benchmark_logs_to_timeseries_df` with ``aggregate=True``.

        :param metric: Metric column to extract (default ``'tpm'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-1'``).
        :type configuration: str
        :param client: Client number (default ``'1'``).
        :type client: str or int
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: DataFrame indexed by ``'second'`` with the metric and an ``'avg'`` column.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].unique().tolist()
        return self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=True)
    def get_benchmark_logs_timeseries_df_single(self, metric="tpm", configuration="", client='1', experiment_run='1'):
        """
        Returns a list of DataFrames of time series of a metric for the benchmarking
        phase, one per pod.

        Retrieves pod IDs from :meth:`get_df_benchmarking` filtered by the given
        ``configuration``, ``client``, and ``experiment_run``, then delegates to
        :meth:`benchmark_logs_to_timeseries_df` with ``aggregate=False``.

        :param metric: Metric column to extract (default ``'tpm'``).
        :type metric: str
        :param configuration: Configuration name (e.g. ``'PostgreSQL-1'``).
        :type configuration: str
        :param client: Client number (default ``'1'``).
        :type client: str or int
        :param experiment_run: Experiment run number (default ``'1'``).
        :type experiment_run: str or int
        :return: List of DataFrames, one per pod, each indexed by ``'second'``.
        :rtype: list[pandas.DataFrame]
        """
        df = self.get_df_benchmarking()
        list_logs = df[(df['client'] == str(client)) & (df['configuration'] == configuration) & (df['experiment_run'] == str(experiment_run))]['pod'].unique().tolist()
        return self.benchmark_logs_to_timeseries_df(list_logs, metric=metric, aggregate=False)
    def get_summary_benchmark_per_connection(self):
        """
        Returns benchmarking results with one row per pod, filtered to the key
        display columns.

        Applies :meth:`benchmarking_set_datatypes` and selects the columns used
        for the per-connection summary table (experiment run, terminals, target,
        client, child, time, errors, throughput, goodput, efficiency, and
        latency percentiles), then naturally sorts by the connection name.

        :return: DataFrame indexed as ``"DBMS"`` with one row per pod, or an
                 empty DataFrame if there are no benchmarking results.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_benchmarking()
        if df.empty:
            return pd.DataFrame()
        if "P95 [ms]" in df:
            # we have latencies
            columns = ['phase', 'job', 'experiment_run',"vusers","client","benchmark_run", "child", "NOPM", "TPM", "efficiency", "duration", "errors","P95 [ms]","P99 [ms]"]
        else:
            columns = ['phase', 'job', 'experiment_run',"vusers","client","benchmark_run", "child", "NOPM", "TPM", "efficiency", "duration", "errors"]
        _fill_missing_counts(df)
        df_plot = self.benchmarking_set_datatypes(df)
        df_plot_filtered = pd.DataFrame()
        for col in columns:
            if col in df_plot.columns:
                df_plot_filtered[col] = df_plot.loc[:,col]
        df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS")
        df_plot_filtered = df_plot_filtered.reindex(index=natural_sort(df_plot_filtered.index))
        return df_plot_filtered
    def get_summary_benchmark_per_phase(self):
        """
        Returns benchmarking results aggregated over parallel pods, one row per phase.

        Applies :meth:`benchmarking_set_datatypes`, aggregates via
        :meth:`benchmarking_aggregate_by_parallel_pods`, and selects the columns
        used for the per-phase summary table (experiment run, terminals, target,
        pod count, time, errors, throughput, goodput, efficiency, and latency
        percentiles), sorted by ``(experiment_run, target, pod_count)``.

        :return: DataFrame indexed as ``"DBMS"`` with one row per phase, or an
                 empty DataFrame if there are no benchmarking results.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            _fill_missing_counts(df)
            df_plot = self.benchmarking_set_datatypes(df)
            df_aggregated = self.benchmarking_aggregate_by_parallel_pods(df_plot)
            df_aggregated = df_aggregated.sort_values(['experiment_run','pod_count']).round(2)
            if "P95 [ms]" in df_aggregated:
                # we have latencies
                aggregated_list = ['phase', 'experiment_run',"vusers","client","benchmark_run","pod_count","P95 [ms]","P99 [ms]", "efficiency"]
                columns = ["NOPM", "TPM", "efficiency", "duration", "errors","P95 [ms]","P99 [ms]"]
            else:
                aggregated_list = ['phase', 'experiment_run',"vusers","client","benchmark_run","pod_count", "efficiency"]
                columns = ["NOPM", "TPM", "efficiency", "duration", "errors"]
            df_aggregated_reduced = df_aggregated[aggregated_list].copy()
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
        return df_aggregated_reduced
    def get_summary_benchmark_per_phase_multitenant(self):
        """
        Returns TPC-C benchmarking results aggregated per phase and tenant, one row per ``(phase, tenant_id)``.

        Like :meth:`get_summary_benchmark_per_phase` but groups by
        ``['phase', 'tenant_id']`` so each tenant appears as a separate row.

        :return: DataFrame indexed as ``"DBMS"`` with one row per (phase, tenant), or an
                 empty DataFrame if there are no benchmarking results.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_benchmarking()
        df_aggregated_reduced = pd.DataFrame()
        if not df.empty:
            _fill_missing_counts(df)
            df_plot = self.benchmarking_set_datatypes(df)
            df_aggregated = self.benchmarking_aggregate_by_parallel_pods(df_plot, columns=['phase', 'tenant_id'])
            df_aggregated = df_aggregated.sort_values(['experiment_run', 'tenant_id', 'pod_count']).round(2)
            if "P95 [ms]" in df_aggregated:
                aggregated_list = ['phase', 'experiment_run', "vusers", "client", "benchmark_run", "pod_count", "tenant_id", "P95 [ms]", "P99 [ms]", "efficiency"]
                columns = ["NOPM", "TPM", "efficiency", "duration", "errors", "P95 [ms]", "P99 [ms]"]
            else:
                aggregated_list = ['phase', 'experiment_run', "vusers", "client", "benchmark_run", "pod_count", "tenant_id", "efficiency"]
                columns = ["NOPM", "TPM", "efficiency", "duration", "errors"]
            df_aggregated_reduced = df_aggregated[[c for c in aggregated_list if c in df_aggregated.columns]].copy()
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:, col]
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
        return df_aggregated_reduced
    def get_summary_loading_per_run(self):
        """
        Returns loading metrics aggregated per experiment run.

        Delegates to :meth:`get_loading_per_run` (defined in :class:`base`),
        which reduces the per-connection loading DataFrame to one row per
        ``(code, configuration, experiment_run)`` and adds a
        ``'Throughput [SF/h]'`` column.

        :return: DataFrame with one row per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_loading_per_run()
        df.drop('code', axis=1, inplace=True, errors='ignore')
        df.drop('configuration', axis=1, inplace=True, errors='ignore')
        return df

    def record_tests(self, experiment, df_loading: pd.DataFrame, df_reduced: pd.DataFrame,
                     workflow_actual: dict, workflow_planned: dict, **extra) -> None:
        """
        Record TPC-C pass/fail tests: NOPM throughput and workflow completeness.

        :param experiment: The owning experiment object.
        :param df_loading: Per-run loading DataFrame (unused here).
        :param df_reduced: Per-phase execution DataFrame.
        :param workflow_actual: Reconstructed actual workflow dict.
        :param workflow_planned: Planned workflow dict from workload config.
        """
        if experiment.benchmarking_is_active():
            experiment._test_column(df_reduced, "NOPM")
            # log_to_df computes efficiency only with key-and-think time
            keyandthink = str(experiment.default_benchmarking_parameters.get('HAMMERDB_KEYANDTHINK', 'false')) == "true"
            experiment._test_efficiency(
                df_reduced, "vusers",
                computed=keyandthink,
                reason="needs key-and-think time (-xkey)")
            experiment._record_test(
                experiment.test_workflow(workflow_actual, workflow_planned),
                "Workflow as planned"
            )


