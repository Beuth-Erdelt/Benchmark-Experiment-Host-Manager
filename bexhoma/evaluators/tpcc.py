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
            iterations = re.findall('HAMMERDB_ITERATIONS (.+?)\n', stdout)[0]
            duration = re.findall('HAMMERDB_DURATION (.+?)\n', stdout)[0]
            rampup = re.findall('HAMMERDB_RAMPUP (.+?)\n', stdout)[0]
            sf = re.findall('SF (.+?)\n', stdout)[0]
            vusers_loading = re.findall('HAMMERDB_NUM_VU (.+?)\n', stdout)[0]
            client = re.findall('BEXHOMA_CLIENT:(.+?)\n', stdout)[0]
            benchmark_run = re.findall('BEXHOMA_BENCHMARK_RUN:(.+?)\n', stdout)
            benchmark_run = benchmark_run[0] if benchmark_run else '1'
            timeprofile = re.findall('HAMMERDB_TIMEPROFILE (.+?)\n', stdout)[0]
            allwarehouses = re.findall('HAMMERDB_ALLWAREHOUSES (.+?)\n', stdout)[0]
            keyandthink = re.findall('HAMMERDB_KEYANDTHINK (.+?)\n', stdout)[0]
            child = re.findall('BEXHOMA_CHILD (.+?)\n', stdout)[0]
            error_timesynch = re.findall('start time has already passed', stdout)
            if len(error_timesynch) > 0:
                # log is incomplete
                print(filename, "log is incomplete")
                return pd.DataFrame()
            pod_count = re.findall('BEXHOMA_NUM_PODS (.+?)\n', stdout)[0]
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
            # efficiency is only meaningful when key-and-think time is enabled
            if keyandthink == "true":
                efficiency = round(100. * float(result_tuples[0][0][0]) / float(result_tuples[0][1]) / 1.286, 2)
            else:
                efficiency = 0
            phase = configuration_name + '-' + experiment_run + '-' + client
            job = connection_name
            connection = connection_name + '-' + child
            latency_values = list(extracted_data.values())
            rows = [
                (connection, phase, job, configuration_name, experiment_run, client, benchmark_run, child, pod_name, pod_count,
                 code, iterations, duration, rampup, sf, run_idx, num_errors, vusers_loading,
                 vuser, efficiency, result[0], result[1], result[2]) + tuple(latency_values)
                for run_idx, (result, vuser) in enumerate(result_tuples)
            ]
            df = pd.DataFrame(rows)
            col_names = ['connection', 'phase', 'job', 'configuration', 'experiment_run', 'client', 'benchmark_run', 'child', 'pod',
                         'pod_count', 'code', 'iterations', 'duration', 'rampup', 'sf', 'run',
                         'errors', 'vusers_loading', 'vusers', 'efficiency', 'NOPM', 'TPM', 'dbms']
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
                    'CALLS':'max',
                    'MIN [ms]':'max',
                    'AVG [ms]':'mean',
                    'MAX [ms]':'max',
                    'TOTAL [ms]':'max',
                    'P99 [ms]':'max',
                    'P95 [ms]':'max',
                    'P50 [ms]':'max',
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
            dict_grp = dict()
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['job'] = grp['job'].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            df_grp = pd.DataFrame(dict_grp, index=["-".join(map(str, key))])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        # efficiency is only valid when vusers == 10 × SF (standard TPC-C convention)
        df_aggregated['efficiency'] = 0.
        tpcc_mask = df_aggregated['sf'] * 10 == df_aggregated['vusers']
        df_aggregated.loc[tpcc_mask, 'efficiency'] = (
            100. * df_aggregated['NOPM'] / 12.86 / df_aggregated['sf']
        )
        return df_aggregated
    def get_summary_benchmark_per_connection(self):
        """
        Returns benchmarking results with one row per pod, filtered to the key
        display columns.

        Applies :meth:`benchmarking_set_datatypes` and selects the columns used
        for the per-connection summary table (experiment run, terminals, target,
        client, child, time, errors, throughput, goodput, efficiency, and
        latency percentiles), then sorts by ``(experiment_run, client, child)``.

        :return: DataFrame indexed as ``"DBMS"`` with one row per pod, or ``None``
                 if there are no benchmarking results.
        :rtype: pandas.DataFrame or None
        """
        df = self.get_df_benchmarking()
        if not df.empty:
            if "P95 [ms]" in df:
                # we have latencies
                columns = ['phase', 'job', 'experiment_run',"vusers","client","benchmark_run", "child", "NOPM", "TPM", "efficiency", "duration", "errors","P95 [ms]","P99 [ms]"]
            else:
                columns = ['phase', 'job', 'experiment_run',"vusers","client","benchmark_run", "child", "NOPM", "TPM", "efficiency", "duration", "errors"]
            df.fillna(0, inplace=True)
            df_plot = self.benchmarking_set_datatypes(df)
            df_plot_filtered = pd.DataFrame()
            for col in columns:
                if col in df_plot.columns:
                    df_plot_filtered[col] = df_plot.loc[:,col]
            df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(['experiment_run', 'client'])
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
            df.fillna(0, inplace=True)
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
            df.fillna(0, inplace=True)
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
            experiment._record_test(
                experiment.test_workflow(workflow_actual, workflow_planned),
                "Workflow as planned"
            )


