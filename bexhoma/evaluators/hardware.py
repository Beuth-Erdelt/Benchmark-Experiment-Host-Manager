"""
Evaluator for Hardware (fio/sysbench) experiments.

Provides :class:`HardwareEvaluator`, which extends :class:`LogEvaluator` to parse and
aggregate fio disk I/O results (IOPS, bandwidth, completion-latency percentiles)
produced by ``images/hardware/benchmarker``.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
import re
import traceback

from .logger import LogEvaluator

__all__ = ["HardwareEvaluator"]

# KEY:VALUE lines echoed by benchmarker.sh (identity/scaling) and run_fio.sh
# (workload parameters and results); see images/hardware/benchmarker/*.sh.
_KEYS_IDENTITY = [
    'BEXHOMA_CONNECTION', 'BEXHOMA_CONFIGURATION', 'BEXHOMA_EXPERIMENT',
    'BEXHOMA_EXPERIMENT_RUN', 'BEXHOMA_CLIENT', 'BEXHOMA_BENCHMARK_RUN',
    'BEXHOMA_CHILD', 'BEXHOMA_NUM_PODS',
]
_KEYS_PARAMETERS = [
    'HARDWARE_TYPE', 'HARDWARE_SIZE', 'HARDWARE_DURATION',
    'HARDWARE_FIO_RW', 'HARDWARE_FIO_BS', 'HARDWARE_FIO_IODEPTH',
    'HARDWARE_FIO_NUMJOBS', 'HARDWARE_FIO_ENGINE', 'HARDWARE_FIO_FSYNC',
    'HARDWARE_FIO_RWMIXREAD',
]
_PERCENTILE_LABELS = ['P01', 'P10', 'P50', 'P90', 'P95', 'P99', 'P999', 'P9999']
_KEYS_RESULTS = ['HARDWARE_FIO_READ_IOPS', 'HARDWARE_FIO_WRITE_IOPS',
                 'HARDWARE_FIO_READ_BW_KBPS', 'HARDWARE_FIO_WRITE_BW_KBPS']
for _label in _PERCENTILE_LABELS:
    _KEYS_RESULTS.append(f'HARDWARE_FIO_READ_LAT_{_label}_MS')
    _KEYS_RESULTS.append(f'HARDWARE_FIO_WRITE_LAT_{_label}_MS')


class HardwareEvaluator(LogEvaluator):
    """
    Evaluator for a Hardware (fio) experiment.

    Parses per-pod log files for the ``KEY:VALUE`` parameter and result lines
    echoed by ``benchmarker.sh``/``run_fio.sh`` and assembles them into
    DataFrames. Aggregation over parallel pods follows the same pattern as the
    other logger-based evaluators. ``HARDWARE_TYPE=sysbench`` logs are parsed
    for identity columns only — the CPU/memory result columns are not yet
    extracted.

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Whether loading-phase results are expected.
    :param include_benchmarking: Whether benchmarking-phase results are expected.
    """
    def log_to_df(self, filename):
        """
        Parses a Hardware pod log file into a DataFrame.

        Extracts identity fields, fio workload parameters, and — for
        ``HARDWARE_TYPE=fio`` — IOPS, bandwidth, and completion-latency
        percentiles from the ``KEY:VALUE`` lines echoed by
        ``benchmarker.sh``/``run_fio.sh``.

        :param filename: Absolute path to the Hardware benchmarker log file.
        :type filename: str
        :return: Single-row DataFrame, or empty on parse failure.
        :rtype: pandas.DataFrame
        """
        # test for known errors
        LogEvaluator.log_to_df(self, filename)
        try:
            with open(filename) as f:
                stdout = f.read()
            error_timesynch = re.findall('start time has already passed', stdout)
            if len(error_timesynch) > 0:
                # log is incomplete
                print(filename, "log is incomplete")
                return pd.DataFrame()
            pod_name = filename[filename.rindex("-") + 1:-len(".log")]
            values = {}
            for key in _KEYS_IDENTITY + _KEYS_PARAMETERS + _KEYS_RESULTS:
                match = re.findall(re.escape(key) + ':(.*?)\n', stdout)
                values[key] = match[-1] if match else ''
            errors = re.findall('Error ', stdout)
            num_errors = len(errors)
            connection_name = values['BEXHOMA_CONNECTION']
            configuration_name = values['BEXHOMA_CONFIGURATION']
            code = values['BEXHOMA_EXPERIMENT']
            experiment_run = values['BEXHOMA_EXPERIMENT_RUN']
            client = values['BEXHOMA_CLIENT']
            benchmark_run = values['BEXHOMA_BENCHMARK_RUN'] or '1'
            child = values['BEXHOMA_CHILD']
            pod_count = values['BEXHOMA_NUM_PODS']
            phase = configuration_name + '-' + experiment_run + '-' + client
            job = connection_name
            connection = connection_name + '-' + child
            row = {
                'connection': connection, 'phase': phase, 'job': job,
                'configuration': configuration_name, 'experiment_run': experiment_run,
                'client': client, 'benchmark_run': benchmark_run, 'child': child,
                'pod': pod_name, 'pod_count': pod_count, 'code': code, 'errors': num_errors,
            }
            for key in _KEYS_PARAMETERS + _KEYS_RESULTS:
                row[key.lower()] = values[key]
            df = pd.DataFrame([row])
            df.index.name = connection_name
            return df
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return pd.DataFrame()

    def benchmarking_set_datatypes(self, df):
        """
        Casts all Hardware benchmarking result columns to their appropriate data types.

        :param df: DataFrame of raw Hardware benchmarking results.
        :type df: pandas.DataFrame
        :return: DataFrame with columns cast to correct types.
        :rtype: pandas.DataFrame
        """
        dtype_map = {
            'connection': 'str', 'phase': 'str', 'job': 'str', 'configuration': 'str',
            'experiment_run': 'int', 'code': 'int', 'client': 'int', 'benchmark_run': 'int',
            'child': 'int', 'pod': 'str', 'pod_count': 'int', 'errors': 'int',
            'hardware_type': 'str', 'hardware_size': 'str', 'hardware_duration': 'float',
            'hardware_fio_rw': 'str', 'hardware_fio_bs': 'str', 'hardware_fio_engine': 'str',
            'hardware_fio_iodepth': 'int', 'hardware_fio_numjobs': 'int',
            'hardware_fio_fsync': 'int', 'hardware_fio_rwmixread': 'int',
        }
        for key in _KEYS_RESULTS:
            dtype_map[key.lower()] = 'float'
        df_typed = df.astype(dtype_map)
        if 'tenant_id' not in df_typed.columns:
            df_typed = df_typed.assign(tenant_id=-1)
        return df_typed

    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Aggregates parallel-pod Hardware result rows into one row per group.

        Groups by ``columns``; IOPS and bandwidth columns are summed across
        pods (aggregate throughput), latency percentile columns take the max
        across pods (worst observed tail latency).

        :param df: Typed Hardware benchmarking DataFrame.
        :type df: pandas.DataFrame
        :param columns: Grouping columns (default ``['phase']``).
        :type columns: list[str]
        :return: Aggregated DataFrame with one row per group.
        :rtype: pandas.DataFrame
        """
        df_aggregated = pd.DataFrame()
        for key, grp in df.groupby([df[col] for col in columns]):
            aggregate = {
                'code': 'max', 'job': 'max', 'client': 'max', 'benchmark_run': 'max',
                'pod': 'sum', 'pod_count': 'count', 'errors': 'sum',
                'hardware_duration': 'max', 'hardware_fio_numjobs': 'sum',
                'tenant_id': 'min',
            }
            for col in grp.columns:
                if col.endswith('_iops') or col.endswith('_kbps'):
                    aggregate[col] = 'sum'
                elif col.endswith('_ms'):
                    aggregate[col] = 'max'
            dict_grp = dict()
            dict_grp['configuration'] = grp['configuration'].iloc[0]
            dict_grp['experiment_run'] = grp['experiment_run'].iloc[0]
            dict_grp['phase'] = grp['phase'].iloc[0]
            dict_grp['job'] = grp['job'].iloc[0]
            # constant within one round (one phase group), so take the first pod's value
            for fio_param in ['hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
                               'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_rwmixread']:
                if fio_param in grp.columns:
                    dict_grp[fio_param] = grp[fio_param].iloc[0]
            dict_grp = {**dict_grp, **grp.agg(aggregate)}
            df_grp = pd.DataFrame(dict_grp, index=["-".join(map(str, key))])
            df_aggregated = pd.concat([df_aggregated, df_grp])
        return df_aggregated

    def get_summary_benchmark_per_connection(self):
        """
        Returns benchmarking results with one row per pod, filtered to the key
        display columns.

        :return: DataFrame indexed as ``"DBMS"`` with one row per pod, or an
                 empty DataFrame if there are no benchmarking results.
        :rtype: pandas.DataFrame
        """
        df = self.get_df_benchmarking()
        if df.empty:
            return pd.DataFrame()
        columns = [
            'phase', 'job', 'experiment_run', 'client', 'benchmark_run', 'child',
            'hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
            'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_rwmixread',
            'hardware_fio_numjobs',
            'hardware_fio_read_iops', 'hardware_fio_write_iops',
            'hardware_fio_read_lat_p95_ms', 'hardware_fio_write_lat_p95_ms',
            'hardware_fio_read_lat_p99_ms', 'hardware_fio_write_lat_p99_ms', 'errors',
        ]
        df.fillna(0, inplace=True)
        df_plot = self.benchmarking_set_datatypes(df)
        df_plot_filtered = pd.DataFrame()
        for col in columns:
            if col in df_plot.columns:
                df_plot_filtered[col] = df_plot.loc[:, col]
        df_plot_filtered = df_plot_filtered.rename_axis(index="DBMS").sort_values(['experiment_run', 'client'])
        return df_plot_filtered

    def get_summary_benchmark_per_phase(self):
        """
        Returns benchmarking results aggregated over parallel pods, one row per phase.

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
            df_aggregated = df_aggregated.sort_values(['experiment_run', 'pod_count']).round(2)
            aggregated_list = ['phase', 'experiment_run', 'client', 'benchmark_run', 'pod_count']
            columns = [
                'hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
                'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_rwmixread',
                'hardware_fio_read_iops', 'hardware_fio_write_iops',
                'hardware_fio_read_lat_p95_ms', 'hardware_fio_write_lat_p95_ms',
                'hardware_fio_read_lat_p99_ms', 'hardware_fio_write_lat_p99_ms', 'errors',
            ]
            df_aggregated_reduced = df_aggregated[aggregated_list].copy()
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:, col]
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
        return df_aggregated_reduced

    def get_summary_benchmark_per_phase_multitenant(self):
        """
        Hardware has no multi-tenant concept; delegates to :meth:`get_summary_benchmark_per_phase`.

        :return: Same as :meth:`get_summary_benchmark_per_phase`.
        :rtype: pandas.DataFrame
        """
        return self.get_summary_benchmark_per_phase()
