"""
Evaluator for Hardware (fio/sysbench) experiments.

Provides :class:`HardwareEvaluator`, which extends :class:`LogEvaluator` to parse and
aggregate fio disk I/O results (IOPS, bandwidth, completion-latency percentiles) and
sysbench CPU/memory results (events/sec, throughput, completion latency) produced by
``images/hardware/benchmarker``.

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

# KEY:VALUE lines echoed by benchmarker.sh (identity/scaling), run_fio.sh
# (fio parameters/results) and run_sysbench.sh (sysbench results); see
# images/hardware/benchmarker/*.sh.
_KEYS_IDENTITY = [
    'BEXHOMA_CONNECTION', 'BEXHOMA_CONFIGURATION', 'BEXHOMA_EXPERIMENT',
    'BEXHOMA_EXPERIMENT_RUN', 'BEXHOMA_CLIENT', 'BEXHOMA_BENCHMARK_RUN',
    'BEXHOMA_CHILD', 'BEXHOMA_NUM_PODS',
]
_KEYS_PARAMETERS = [
    'HARDWARE_TYPE', 'HARDWARE_SIZE', 'HARDWARE_DURATION', 'HARDWARE_THREADS',
    'HARDWARE_FIO_RW', 'HARDWARE_FIO_BS', 'HARDWARE_FIO_IODEPTH',
    'HARDWARE_FIO_NUMJOBS', 'HARDWARE_FIO_ENGINE', 'HARDWARE_FIO_FSYNC',
    'HARDWARE_FIO_FDATASYNC', 'HARDWARE_FIO_RWMIXREAD',
]
_PERCENTILE_LABELS = ['P01', 'P10', 'P50', 'P90', 'P95', 'P99', 'P999', 'P9999']
_KEYS_RESULTS = ['HARDWARE_FIO_READ_IOPS', 'HARDWARE_FIO_WRITE_IOPS',
                 'HARDWARE_FIO_READ_BW_KBPS', 'HARDWARE_FIO_WRITE_BW_KBPS']
for _label in _PERCENTILE_LABELS:
    _KEYS_RESULTS.append(f'HARDWARE_FIO_READ_LAT_{_label}_MS')
    _KEYS_RESULTS.append(f'HARDWARE_FIO_WRITE_LAT_{_label}_MS')
_KEYS_RESULTS += [
    'HARDWARE_SYSBENCH_CPU_EVENTS_PER_SEC', 'HARDWARE_SYSBENCH_CPU_TOTAL_TIME_S',
    'HARDWARE_SYSBENCH_CPU_LAT_P95_MS', 'HARDWARE_SYSBENCH_MEMORY_OPS_PER_SEC',
    'HARDWARE_SYSBENCH_MEMORY_THROUGHPUT_MIBPS', 'HARDWARE_SYSBENCH_MEMORY_LAT_P95_MS',
]

_NATURAL_SORT_DIGIT_WIDTH = 10  # zero-pad width; comfortably covers phase strings like "Hardware-1-1-128"


def _natural_sort_key(value: str) -> str:
    """
    Zero-pads digit runs so a lexicographic sort behaves like a numeric sort.

    Turns ``"Hardware-1-1-10"`` into ``"Hardware-0000000001-0000000001-0000000010"``,
    so ``"...-10"`` sorts after ``"...-9"`` instead of after ``"...-1"``.

    :param value: String to build a natural-sort key for.
    :type value: str
    :return: Sortable string with all digit runs zero-padded.
    :rtype: str
    """
    return re.sub(r'\d+', lambda match: match.group().zfill(_NATURAL_SORT_DIGIT_WIDTH), str(value))


class HardwareEvaluator(LogEvaluator):
    """
    Evaluator for a Hardware (fio) experiment.

    Parses per-pod log files for the ``KEY:VALUE`` parameter and result lines
    echoed by ``benchmarker.sh``/``run_fio.sh``/``run_sysbench.sh`` and assembles
    them into DataFrames. Aggregation over parallel pods follows the same pattern
    as the other logger-based evaluators. A given experiment runs either fio or
    sysbench rounds (``-xht`` is not swept), so the columns of the inactive tool
    are always present but filled with ``0``, the same convention already used
    for fio's own read/write split.

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Whether loading-phase results are expected.
    :param include_benchmarking: Whether benchmarking-phase results are expected.
    """
    def log_to_df(self, filename):
        """
        Parses a Hardware pod log file into a DataFrame.

        Extracts identity fields, workload parameters, and — depending on
        ``HARDWARE_TYPE`` — either fio's IOPS/bandwidth/completion-latency
        percentiles or sysbench's CPU events/sec and memory throughput/latency,
        from the ``KEY:VALUE`` lines echoed by
        ``benchmarker.sh``/``run_fio.sh``/``run_sysbench.sh``.

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
            # only present for -mtb container experiments (hardware.py); -1 marks single-tenant runs
            tenant_id_match = re.findall(r'BEXHOMA_TENANT_ID:(\d+)', stdout)
            tenant_id = int(tenant_id_match[0]) if tenant_id_match else -1
            # measured wall-clock duration of this pod's benchmarker.sh run (fio or
            # sysbench CPU+memory combined), same BEXHOMA_DURATION convention other
            # evaluators (e.g. evaluators/benchbase.py) already parse as 'duration'
            duration_match = re.findall(r'BEXHOMA_DURATION:(\d+)', stdout)
            duration = int(duration_match[0]) if duration_match else 0
            phase = configuration_name + '-' + experiment_run + '-' + client
            job = connection_name
            connection = connection_name + '-' + child
            row = {
                'connection': connection, 'phase': phase, 'job': job,
                'configuration': configuration_name, 'experiment_run': experiment_run,
                'client': client, 'benchmark_run': benchmark_run, 'child': child,
                'pod': pod_name, 'pod_count': pod_count, 'code': code, 'errors': num_errors,
                'tenant_id': tenant_id, 'duration': duration,
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

        A read-only (or write-only) fio workload never echoes the opposing
        direction's ``KEY:VALUE`` lines, so :meth:`log_to_df` defaults those
        columns to ``''``; such blanks are treated as ``0`` here before casting.

        Adds a ``tenant_id`` column (value ``-1``) and a ``duration`` column (value
        ``0``) when absent, so DataFrames loaded from older pickles (predating
        ``-mtb container`` support / ``BEXHOMA_DURATION`` parsing) remain compatible.

        :param df: DataFrame of raw Hardware benchmarking results.
        :type df: pandas.DataFrame
        :return: DataFrame with columns cast to correct types.
        :rtype: pandas.DataFrame
        """
        if 'tenant_id' not in df.columns:
            df = df.assign(tenant_id=-1)
        if 'duration' not in df.columns:
            df = df.assign(duration=0)
        dtype_map = {
            'connection': 'str', 'phase': 'str', 'job': 'str', 'configuration': 'str',
            'experiment_run': 'int', 'code': 'int', 'client': 'int', 'benchmark_run': 'int',
            'child': 'int', 'pod': 'str', 'pod_count': 'int', 'errors': 'int',
            'hardware_type': 'str', 'hardware_size': 'str', 'hardware_duration': 'float',
            'hardware_threads': 'int',
            'hardware_fio_rw': 'str', 'hardware_fio_bs': 'str', 'hardware_fio_engine': 'str',
            'hardware_fio_iodepth': 'int', 'hardware_fio_numjobs': 'int',
            'hardware_fio_fsync': 'int', 'hardware_fio_fdatasync': 'int',
            'hardware_fio_rwmixread': 'int', 'tenant_id': 'int', 'duration': 'int',
        }
        for key in _KEYS_RESULTS:
            dtype_map[key.lower()] = 'float'
        numeric_columns = [
            column for column, dtype in dtype_map.items()
            if dtype in ('int', 'float') and column in df.columns
        ]
        df = df.copy()
        # astype() right below sets the real dtypes anyway, so the replace()
        # inferred dtype doesn't matter; infer_objects(copy=False) just opts
        # into pandas' future default to silence the downcasting FutureWarning.
        df[numeric_columns] = df[numeric_columns].replace('', 0).infer_objects(copy=False)
        df_typed = df.astype(dtype_map)
        return df_typed

    def benchmarking_aggregate_by_parallel_pods(self, df, columns=["phase"]):
        """
        Aggregates parallel-pod Hardware result rows into one row per group.

        Groups by ``columns``; IOPS, bandwidth, events/sec and throughput
        columns are summed across pods (aggregate throughput), latency
        percentile columns take the max across pods (worst observed tail
        latency).

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
                'hardware_threads': 'sum', 'hardware_sysbench_cpu_total_time_s': 'max',
                'tenant_id': 'min', 'duration': 'max',
            }
            for col in grp.columns:
                if (col.endswith('_iops') or col.endswith('_kbps')
                        or col.endswith('_per_sec') or col.endswith('_mibps')):
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
                               'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_fdatasync',
                               'hardware_fio_rwmixread']:
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
            'phase', 'job', 'experiment_run', 'client', 'benchmark_run', 'child', 'duration',
            'hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
            'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_fdatasync',
            'hardware_fio_rwmixread', 'hardware_fio_numjobs',
            'hardware_fio_read_iops', 'hardware_fio_write_iops',
            'hardware_fio_read_lat_p95_ms', 'hardware_fio_write_lat_p95_ms',
            'hardware_fio_read_lat_p99_ms', 'hardware_fio_write_lat_p99_ms',
            'hardware_threads', 'hardware_sysbench_cpu_events_per_sec',
            'hardware_sysbench_cpu_total_time_s', 'hardware_sysbench_cpu_lat_p95_ms',
            'hardware_sysbench_memory_ops_per_sec', 'hardware_sysbench_memory_throughput_mibps',
            'hardware_sysbench_memory_lat_p95_ms', 'errors',
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
            df_aggregated = df_aggregated.sort_values(
                by='phase', key=lambda col: col.map(_natural_sort_key)
            ).round(2)
            aggregated_list = ['phase', 'experiment_run', 'client', 'benchmark_run', 'pod_count', 'duration']
            columns = [
                'hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
                'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_fdatasync',
                'hardware_fio_rwmixread',
                'hardware_fio_read_iops', 'hardware_fio_write_iops',
                'hardware_fio_read_lat_p95_ms', 'hardware_fio_write_lat_p95_ms',
                'hardware_fio_read_lat_p99_ms', 'hardware_fio_write_lat_p99_ms',
                'hardware_threads', 'hardware_sysbench_cpu_events_per_sec',
                'hardware_sysbench_cpu_total_time_s', 'hardware_sysbench_cpu_lat_p95_ms',
                'hardware_sysbench_memory_ops_per_sec', 'hardware_sysbench_memory_throughput_mibps',
                'hardware_sysbench_memory_lat_p95_ms', 'errors',
            ]
            df_aggregated_reduced = df_aggregated[aggregated_list].copy()
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:, col]
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
        return df_aggregated_reduced

    def get_summary_benchmark_per_phase_multitenant(self):
        """
        Returns benchmarking results aggregated per phase and tenant, one row per
        ``(phase, tenant_id)``.

        Used for ``-mtb container`` co-located noisy-neighbor experiments (see
        ``hardware.py``), where each tenant is a separate SUT pod pinned to the
        same node. Like :meth:`get_summary_benchmark_per_phase` but groups by
        ``['phase', 'tenant_id']`` so each tenant appears as a separate row
        instead of being aggregated away.

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
            df_aggregated = df_aggregated.sort_values(['experiment_run', 'tenant_id', 'client', 'pod_count']).round(2)
            aggregated_list = ['phase', 'experiment_run', 'client', 'benchmark_run', 'pod_count', 'tenant_id', 'duration']
            columns = [
                'hardware_fio_rw', 'hardware_fio_bs', 'hardware_fio_iodepth',
                'hardware_fio_engine', 'hardware_fio_fsync', 'hardware_fio_fdatasync',
                'hardware_fio_rwmixread',
                'hardware_fio_read_iops', 'hardware_fio_write_iops',
                'hardware_fio_read_lat_p95_ms', 'hardware_fio_write_lat_p95_ms',
                'hardware_fio_read_lat_p99_ms', 'hardware_fio_write_lat_p99_ms',
                'hardware_threads', 'hardware_sysbench_cpu_events_per_sec',
                'hardware_sysbench_cpu_total_time_s', 'hardware_sysbench_cpu_lat_p95_ms',
                'hardware_sysbench_memory_ops_per_sec', 'hardware_sysbench_memory_throughput_mibps',
                'hardware_sysbench_memory_lat_p95_ms', 'errors',
            ]
            df_aggregated_reduced = df_aggregated[aggregated_list].copy()
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:, col]
            df_aggregated_reduced = df_aggregated_reduced.rename_axis(index="DBMS")
        return df_aggregated_reduced

    def record_tests(self, experiment, df_loading: pd.DataFrame, df_reduced: pd.DataFrame,
                     workflow_actual: dict, workflow_planned: dict, **extra) -> None:
        """
        Record Hardware pass/fail tests: workflow completeness and, depending on
        ``HARDWARE_TYPE``, that every round measured something.

        A fio round with both ``hardware_fio_read_iops`` and ``hardware_fio_write_iops``
        at 0 did not produce a usable fio measurement (e.g. a full PVC or a local
        disk-quota error while collecting results, as seen for round 10 of
        experiment 1783115274) rather than a legitimate all-zero result — a
        ``randread`` round always has 0 write IOPS and vice versa, so only the
        combination of both being 0 indicates a failed round. A sysbench round
        with 0 CPU events/sec did not produce a usable CPU measurement (the
        memory sub-test can legitimately run with 0 CPU events only if
        ``HARDWARE_THREADS`` starves the CPU test, which does not happen with the
        image's fixed CPU-then-memory sequence, so 0 always indicates a failure).

        :param experiment: The owning experiment object.
        :param df_loading: Per-run loading DataFrame; always empty for Hardware.
        :param df_reduced: Per-phase execution DataFrame.
        :param workflow_actual: Reconstructed actual workflow dict.
        :param workflow_planned: Planned workflow dict from workload config.
        """
        if experiment.benchmarking_is_active():
            experiment._record_test(
                experiment.test_workflow(workflow_actual, workflow_planned),
                "Workflow as planned"
            )
            hardware_type = getattr(experiment.args, 'hardware_type', 'fio')
            has_iops_columns = ('hardware_fio_read_iops' in df_reduced.columns
                                 and 'hardware_fio_write_iops' in df_reduced.columns)
            if hardware_type == 'fio' and not df_reduced.empty and has_iops_columns:
                both_zero = ((df_reduced['hardware_fio_read_iops'] == 0)
                             & (df_reduced['hardware_fio_write_iops'] == 0))
                passed = not both_zero.any()
                experiment._record_test(
                    passed,
                    "Execution Phase: every round has non-zero read or write IOPS" if passed
                    else "Execution Phase: at least one round has 0 IOPS for both read and write"
                )
            has_sysbench_columns = 'hardware_sysbench_cpu_events_per_sec' in df_reduced.columns
            if hardware_type == 'sysbench' and not df_reduced.empty and has_sysbench_columns:
                passed = not (df_reduced['hardware_sysbench_cpu_events_per_sec'] == 0).any()
                experiment._record_test(
                    passed,
                    "Execution Phase: every round has non-zero CPU events/sec" if passed
                    else "Execution Phase: at least one round has 0 CPU events/sec"
                )
