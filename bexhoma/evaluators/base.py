"""
Base evaluator class for bexhoma experiments.

Provides :func:`natural_sort` and :class:`base`, which loads an experiment
result folder, parses workflow state and connection configuration, and
exposes monitoring data. All other evaluators inherit from :class:`base`
via :class:`logger`.

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
from pathlib import Path

def natural_sort(l):
    """
    Sorts a list in natural (human) order so that embedded digit runs are
    compared numerically rather than lexicographically.  Works for lists of
    strings, integers, or any mix whose elements have a meaningful ``str()``
    representation.

    :param l: List to sort.
    :type l: list
    :return: Sorted list.
    :rtype: list
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', str(key))]
    return sorted(l, key=alphanum_key)

class base:
    """
    Base evaluator for a single bexhoma experiment.

    Loads the experiment result folder identified by ``code`` inside ``path``,
    provides helpers for scanning log files and reconstructing the workflow,
    and exposes connection/loading metadata.  All benchmark-specific evaluators
    inherit from this class (via :class:`logger`).

    :param code: Experiment identifier — also the name of the result sub-folder.
    :param path: Root path that contains the result folders.
    :param include_loading: Whether loading-phase results are expected.
    :param include_benchmarking: Whether benchmarking-phase results are expected.
    :param benchmark_run: 1-based position in the benchmark sequence; 0 means unset.
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True, benchmark_run: int = 0):
        """
        :param code: Experiment identifier — also the name of the result sub-folder.
        :param path: Root path that contains the result folders.
        :param include_loading: Whether loading-phase results are expected.
        :param include_benchmarking: Whether benchmarking-phase results are expected.
        :param benchmark_run: 1-based position of this evaluator in the benchmark sequence; 0 means unset.
        :type benchmark_run: int
        """
        self.path = path + "/" + code
        self.code = code
        self.include_loading = include_loading
        self.include_benchmarking = include_benchmarking
        self.benchmark_run: int = benchmark_run
        self.experiment = None
        self.workflow = dict()
        self.workflow_errors = dict()
        self.num_missing_benchmarking_dfs = 0
        self.num_missing_loading_dfs = 0
    def log_to_df(self, filename):
        """
        Scans a pod log file for known errors and records them in ``self.workflow_errors``.

        Returns an empty DataFrame; subclasses override this method to also parse
        benchmark results out of the log.

        :param filename: Absolute path to the log file.
        :type filename: str
        :return: Empty DataFrame (subclasses return populated DataFrames).
        :rtype: pandas.DataFrame
        """
        self.workflow_errors[filename] = dict()
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            def test_for_known_errors(text, error_message):
                matches = re.findall('(.+?)' + error_message, text)
                if matches:
                    self.workflow_errors[filename][error_message] = matches
            test_for_known_errors(stdout, 'Temporary failure in name resolution')
        except Exception:
            pass
        if not self.workflow_errors[filename]:
            del self.workflow_errors[filename]
        return pd.DataFrame()

    def log_to_df_loading(self, filename: str) -> pd.DataFrame:
        """
        Parse a loading pod log file and return the result as a DataFrame.

        Default implementation delegates to :meth:`log_to_df`, which is
        correct for benchmarks whose loading and benchmarking log formats are
        identical (e.g. YCSB).  Subclasses where the formats differ must
        override this method.

        :param filename: Absolute path to the loading log file.
        :type filename: str
        :return: DataFrame of loading results, or empty DataFrame on failure.
        :rtype: pandas.DataFrame
        """
        return self.log_to_df(filename)

    def transform_all_logs_benchmarking(self):
        """
        Iterates over all benchmarker log files and calls :meth:`end_benchmarking` for each.

        When ``self.benchmark_run > 0``, only processes log files whose jobname ends
        with the matching benchmark index (last ``-``-separated component), so that
        each evaluator in a multi-benchmark experiment only ingests its own logs.
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker") and filename.endswith(".dbmsbenchmarker.log"):
                inner = filename[len("bexhoma-benchmarker-"):-len(".dbmsbenchmarker.log")]
                jobname = inner[:inner.rindex("-")]
                if self.benchmark_run > 0:
                    try:
                        file_benchmark_run = int(jobname.split("-")[-1])
                    except (ValueError, IndexError):
                        file_benchmark_run = 1
                    if file_benchmark_run != self.benchmark_run:
                        continue
                self.end_benchmarking(jobname)

    def transform_all_logs_loading(self):
        """
        Iterates over all loader sensor log files and calls :meth:`end_loading` for each.

        When ``self.benchmark_run > 0``, only processes log files whose jobname ends
        with the matching benchmark index, so that each evaluator only ingests its own
        loading logs.
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-loading") and filename.endswith(".sensor.log"):
                inner = filename[len("bexhoma-loading-"):-len(".sensor.log")]
                jobname = inner[:inner.rindex("-")]
                if self.benchmark_run > 0:
                    try:
                        file_benchmark_run = int(jobname.split("-")[-1])
                    except (ValueError, IndexError):
                        file_benchmark_run = 1
                    if file_benchmark_run != self.benchmark_run:
                        continue
                self.end_loading(jobname)
    def end_benchmarking(self, jobname):
        """
        Processes all benchmarker log files for a given job name.

        Scans the result folder for files matching
        ``bexhoma-benchmarker-<jobname>*.dbmsbenchmarker.log`` and calls
        :meth:`log_to_df` on each one.

        :param jobname: Job name used to filter matching log files.
        :type jobname: str
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker-" + jobname) and filename.endswith(".dbmsbenchmarker.log"):
                self.log_to_df(self.path + "/" + filename)

    def end_loading(self, jobname):
        """
        Processes all loader sensor log files for a given job name.

        Scans the result folder for files matching
        ``bexhoma-loading-<jobname>*.sensor.log`` and calls
        :meth:`log_to_df` on each one.

        :param jobname: Job name used to filter matching log files.
        :type jobname: str
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-loading-" + jobname) and filename.endswith(".sensor.log"):
                self.log_to_df(self.path + "/" + filename)
    def _collect_dfs(self, filename_result='', filename_source_start='', filename_source_end='', num_missing=0):
        """
        No-op base implementation; overridden by :class:`logger` to collect pickled DataFrames.

        :param filename_result: Name of the combined pickle file to write.
        :type filename_result: str
        :param filename_source_start: Filename prefix used to match source pickle files.
        :type filename_source_start: str
        :param filename_source_end: Filename suffix used to match source pickle files.
        :type filename_source_end: str
        :param num_missing: Number of per-pod DataFrames that failed to parse and are absent from the union.
        :type num_missing: int
        """
        pass
    def evaluate_results(self, pod_dashboard=''):
        """
        Scans all log files and grabs some information.
        In this class basically it scans for errors.
        """
        if self.include_benchmarking:
            self.transform_all_logs_benchmarking()
            # only sensible for logger classes:
            self._collect_dfs(filename_result="bexhoma-benchmarker.all.df.pickle" , filename_source_start="bexhoma-benchmarker", filename_source_end=".log.df.pickle")
        if self.include_loading:
            self.transform_all_logs_loading()
            # only sensible for logger classes:
            self._collect_dfs(filename_result="bexhoma-loading.all.df.pickle" , filename_source_start="bexhoma-loading", filename_source_end=".log.df.pickle")
    def get_df_benchmarking(self):
        """
        Returns the DataFrame containing all benchmarking-phase results.

        :return: Empty DataFrame; overridden by subclasses.
        :rtype: pandas.DataFrame
        """
        return pd.DataFrame()

    def get_df_loading(self):
        """
        Returns the DataFrame containing all loading-phase results.

        :return: Empty DataFrame; overridden by subclasses.
        :rtype: pandas.DataFrame
        """
        return pd.DataFrame()
    def reconstruct_workflow(self, df: 'pd.DataFrame') -> dict:
        """
        Reconstructs the actual experiment workflow from connection metadata.

        Reads ``benchmark_sequence`` from ``queries.config`` to map each
        ``benchmark_run`` index to its benchmarker type, then groups the
        DataFrame by ``(configuration, experiment_run, client, benchmark_run)``
        to produce a structure that mirrors the planned workflow format::

            {
                'MySQL-24-4-1024': [
                    [  # experiment run 1
                        [  # client round 1
                            {'type': 'dbmsbenchmarker', 'pods': 4},
                            {'type': 'tpch_refresh',    'pods': 1},
                        ],
                        [  # client round 2
                            {'type': 'dbmsbenchmarker', 'pods': 8},
                            {'type': 'tpch_refresh',    'pods': 1},
                        ],
                    ],
                ],
            }

        :param df: Connection metadata DataFrame returned by
                   :meth:`get_connections_of_experiment`, with at least the
                   columns ``configuration``, ``experiment_run``, ``client``,
                   ``benchmark_run``, and ``pods``.
        :type df: pandas.DataFrame
        :return: Workflow dict mapping configuration name to the nested structure.
        :rtype: dict
        """
        workload = self.get_workload()
        bm_sequence = {
            entry['index']: entry['type']
            for entry in workload.get('benchmark_sequence', [])
        }
        configs: dict = {}
        for _, row in df.iterrows():
            config_name = row['configuration']
            experiment_run = row['experiment_run']
            client = int(row['client'])
            benchmark_run = int(row['benchmark_run'])
            pods = int(row['pods'])
            if config_name not in configs:
                configs[config_name] = {}
            if experiment_run not in configs[config_name]:
                configs[config_name][experiment_run] = {}
            if client not in configs[config_name][experiment_run]:
                configs[config_name][experiment_run][client] = {}
            if benchmark_run not in configs[config_name][experiment_run][client]:
                configs[config_name][experiment_run][client][benchmark_run] = {
                    'type': bm_sequence.get(benchmark_run, str(benchmark_run)),
                    'pods': pods,
                }
        workflow: dict = {}
        for config_name, run_dict in configs.items():
            workflow[config_name] = [
                [
                    [
                        run_dict[exp_run][client][bm_run]
                        for bm_run in sorted(run_dict[exp_run][client])
                    ]
                    for client in sorted(run_dict[exp_run])
                ]
                for exp_run in sorted(run_dict)
            ]
        return workflow
    def test_results(self):
        """
        Validates results locally and returns an exit code.

        :return: ``0`` on success; subclasses return ``1`` on failure.
        :rtype: int
        """
        return 0
    def test_results_column(self, df, test_column: str) -> bool:
        """
        Check whether a column in a DataFrame contains any zero or NaN values.

        :param df: DataFrame to check.
        :type df: pandas.DataFrame
        :param test_column: Column name to inspect.
        :type test_column: str
        :return: ``True`` if the column is fully populated with non-zero values,
                 ``False`` otherwise.
        :rtype: bool
        """
        if df is not None and not df.empty:
            contains_zero_or_nan = df[test_column].isin([0]) | df[test_column].isna()
            return not contains_zero_or_nan.any()
        return False
    def get_workload(self):
        """
        Returns the workload configuration of an experiment.

        Reads the ``queries.config`` file from the experiment result folder and
        returns its contents as a Python dictionary.

        :return: Workload properties dictionary.
        :rtype: dict
        """
        with open(self.path + "/queries.config", 'r') as f:
            return ast.literal_eval(f.read())
    def add_connection_to_result(self, c, connection_id, result):
        """
        Appends a flattened connection entry to ``result`` keyed by ``connection_id``.

        Extracts scalar fields from the connection config dict ``c`` — including
        host-system, loading-parameter, benchmarking-parameter, SUT-parameter, and
        ``args`` sections — and stores them with prefixed keys
        (``host_*``, ``loading_parameters_*``, ``benchmarking_parameters_*``,
        ``sut_parameters_*``, ``arg_*``).  Non-scalar values (lists and dicts) are
        skipped.

        :param c: Single connection entry from ``connections.config``.
        :type c: dict
        :param connection_id: Key to use when inserting into ``result``.
        :type connection_id: str
        :param result: Accumulator dict that maps connection IDs to metadata rows.
        :type result: dict
        """
        num_loading_pods = len(c['hostsystem']['loading_timespans']['sensor']) if 'loading_timespans' in c['hostsystem'] and 'sensor' in c['hostsystem']['loading_timespans'] else 0
        result[connection_id] = {
            'code': c['parameter']['code'],
            'connection': c['name'],
            'configuration': c['configuration'] if 'configuration' in c else '',
            'phase': c['phase'],
            'job': c['job'],
            'experiment_run': c['parameter']['numExperiment'],
            'benchmark_run': int(c['parameter'].get('numBenchmark', 0)),
            'client': int(c['parameter']['client']),
            'dockerimage': c['parameter']['dockerimage'],
            'time_load': float(c['timeLoad']),
            'time_preload': float(c['timeSchema']),
            'time_generate': float(c['timeGenerate']),
            'time_ingest': float(c['timeIngesting']),
            'time_postload': float(c['timeIndex']),
            'terminals': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS']
                if 'BENCHBASE_TERMINALS' in c['parameter']['connection_parameter']['loading_parameters'] else c['parameter']['connection_parameter']['loading_parameters']['HAMMERDB_VUSERS'] if 'HAMMERDB_VUSERS' in c['parameter']['connection_parameter']['loading_parameters'] else 0,
            'pods': c['parameter']['parallelism'],
            'loading_pods': num_loading_pods,
            'tenant_id': c['parameter']['TENANT'] if 'TENANT' in c['parameter'] else '',
            'num_worker': int(c['parameter']['num_worker']),
            'type_tenants': c['parameter']['TENANT_BY'] if 'TENANT_BY' in c['parameter'] else 'None',
            'num_tenants': int(c['parameter']['TENANT_NUM']) if 'TENANT_NUM' in c['parameter'] else 0,
            'vol_tenants': c['parameter']['TENANT_VOL'] if 'TENANT_VOL' in c['parameter'] else 'False',
            'datadisk': c['hostsystem']['datadisk'],
        }
        for key, hostdata in c['hostsystem'].items():
            if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                result[connection_id][f'host_{key}'] = hostdata
        if 'loading_parameters' in c['parameter']['connection_parameter']:
            for key, hostdata in c['parameter']['connection_parameter']['loading_parameters'].items():
                if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                    result[connection_id][f'loading_parameters_{key}'] = hostdata
        if 'benchmarking_parameters' in c['parameter']['connection_parameter']:
            for key, hostdata in c['parameter']['connection_parameter']['benchmarking_parameters'].items():
                if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                    result[connection_id][f'benchmarking_parameters_{key}'] = hostdata
        if 'sut_parameters' in c['parameter']['connection_parameter']:
            for key, hostdata in c['parameter']['connection_parameter']['sut_parameters'].items():
                if not isinstance(hostdata, list) and not isinstance(hostdata, dict):
                    result[connection_id][f'sut_parameters_{key}'] = hostdata
        if 'storage' in c:
            for key, storagedata in c['storage'].items():
                if not isinstance(storagedata, list) and not isinstance(storagedata, dict):
                    result[connection_id][f'sut_storage_{key}'] = storagedata
        if 'args' in c['hostsystem']:
            for arg in c['hostsystem']['args']:
                if "=" in arg:
                    arg_key, arg_value = arg.split("=", 1)
                    result[connection_id][f'arg_{arg_key}'] = arg_value
        pairs = c['hostsystem'].get('benchmarking_timespans', {}).get('benchmarker', [])
        if pairs:
            begin_ts = min(p[0] for p in pairs)
            end_ts = max(p[1] for p in pairs)
            result[connection_id]['benchmark_begin'] = datetime.fromtimestamp(begin_ts).strftime('%Y-%m-%d %H:%M:%S')
            result[connection_id]['benchmark_end'] = datetime.fromtimestamp(end_ts).strftime('%Y-%m-%d %H:%M:%S')
            result[connection_id]['benchmark_duration'] = end_ts - begin_ts
    def get_connections_of_experiment(self):
        """
        Returns connection metadata for a single experiment.

        Reads ``connections.config`` and builds a row per pod/client with the
        following key columns: ``phase`` (code-prefixed phase identifier,
        ``<code>-<configuration>-<experiment_run>-<client>``), ``job``
        (code-prefixed job identifier,
        ``<code>-<configuration>-<experiment_run>-<client>-<benchmark_run>``),
        ``code``, ``connection``, ``configuration``, ``experiment_run``, ``client``,
        ``type_tenants``, ``num_tenants``, ``vol_tenants``, plus flattened
        host-system, loading-parameter, benchmarking-parameter, and SUT-parameter
        fields.

        When a connection entry carries ``orig_name``, the entry represents an
        individual pod; otherwise a synthetic row is generated for each parallel
        client.

        :return: DataFrame of connection metadata, one row per pod/client.
        :rtype: pandas.DataFrame
        """
        with open(self.path + "/connections.config", 'r') as f:
            connections = ast.literal_eval(f.read())
        # Collect names already covered (both current name and orig_name for per-pod entries)
        covered_names = set()
        for conn in connections:
            covered_names.add(conn['name'])
            if 'orig_name' in conn:
                covered_names.add(conn['orig_name'])
        # Supplement with individual {connection}.config files for connections absent from the
        # combined file (e.g. the refresh stream after dbmsbenchmarker expands connections.config).
        for entry in sorted(os.listdir(self.path)):
            if not entry.endswith('.config') or entry in ('connections.config', 'queries.config'):
                continue
            conn_name = entry[:-len('.config')]
            if conn_name in covered_names:
                continue
            try:
                with open(self.path + "/" + entry, 'r') as f:
                    indiv_conns = ast.literal_eval(f.read())
                for indiv_conn in indiv_conns:
                    if indiv_conn.get('name') == conn_name:
                        connections.append(indiv_conn)
                        covered_names.add(conn_name)
                        break
            except Exception:
                pass
        connections_sorted = sorted(connections, key=lambda conn: conn['name'])
        result = dict()
        for conn in connections_sorted:
            code = conn['parameter']['code']
            benchmark_run_num = str(int(conn['parameter'].get('numBenchmark', 0)))
            if 'orig_name' in conn:
                # entry represents an individual pod — use the pod name as connection id
                name = conn['name']
                job_id = conn['orig_name']
                if benchmark_run_num and job_id.endswith('-' + benchmark_run_num):
                    phase_id = job_id[:-len('-' + benchmark_run_num)]
                else:
                    phase_id = job_id
                conn['phase'] = phase_id
                conn['job'] = job_id
                connection_id = f"{code}-{name}"
                self.add_connection_to_result(conn, connection_id, result)
            else:
                # no per-pod entries — synthesise one row per parallel client
                num_clients = int(conn['parameter']['parallelism'])
                job_id = conn['name']
                if benchmark_run_num and job_id.endswith('-' + benchmark_run_num):
                    phase_id = job_id[:-len('-' + benchmark_run_num)]
                else:
                    phase_id = job_id
                for client_idx in range(1, num_clients + 1):
                    conn['name'] = f"{code}-{job_id}-{client_idx}"
                    conn['phase'] = phase_id
                    conn['job'] = job_id
                    connection_id = f"{code}-{job_id}-{client_idx}"
                    self.add_connection_to_result(conn, connection_id, result)
                    # add_connection_to_result copies the mutated conn['name'] which
                    # carries the code prefix.  Use the pod-level name without the
                    # code prefix so callers see "PostgreSQL-1-1-1-2-1" not
                    # "1781731967-PostgreSQL-1-1-1-2-1".
                    result[connection_id]['connection'] = f"{job_id}-{client_idx}"
        return pd.DataFrame(result).T
    def get_loading_per_connection(self):
        """
        Returns loading metrics for each individual connection (pod/client), enriched
        with the scale factor and a ``'Throughput [SF/h]'`` derived column.

        :return: DataFrame with one row per connection.
        :rtype: pandas.DataFrame
        """
        workload_properties = self.get_workload()
        df = self.get_connections_of_experiment()
        df['SF'] = int(workload_properties['defaultParameters']['SF'])
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        df['Throughput [SF/h]'] = df_tpx
        selected_cols = [
            'code', 'SF', 'configuration', 'connection', 'phase',
            'experiment_run', 'client', 'time_load', 'time_preload',
            'time_generate', 'time_ingest', 'time_postload', 'pods', 'loading_pods', 'terminals',
            'tenant_id', 'type_tenants', 'num_tenants', 'vol_tenants', 'Throughput [SF/h]',
        ]
        return df[selected_cols].copy()
    def get_loading_per_run(self):
        """
        Returns loading metrics aggregated per ``(code, configuration, experiment_run)``.

        Takes the per-connection DataFrame from :meth:`get_loading_per_connection` and
        reduces it to one row per experiment run by taking the max across connections,
        then recomputes ``'Throughput [SF/h]'`` from the aggregated load time.

        :return: DataFrame with one row per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_loading_per_connection()
        df = df.groupby(['code', 'configuration', 'experiment_run']).max()
        df = df.reset_index()
        df.index = df['configuration'].astype(str) + "-" + df['experiment_run'].astype(str)
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0) / df_load.sort_index()
        df['Throughput [SF/h]'] = df_tpx
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('client', axis=1, inplace=True, errors='ignore')
        df.drop('pods', axis=1, inplace=True, errors='ignore')
        return df
    def _get_tenant_loading_from_logs(self) -> dict:
        """
        Reads per-pod sensor log files and extracts per-tenant loading durations.

        Parses ``BEXHOMA_TENANT_ID <N>`` (space-separated, echoed by the loader
        script) and ``BEXHOMA_DURATION:N`` from every loader sensor log file
        (``bexhoma-loading-*.sensor.log``) in the experiment result folder.
        When multiple pods serve the same tenant (parallel loading), the maximum
        duration across those pods is kept so that the returned value reflects
        the full tenant loading span.

        :return: Dict mapping tenant_id (int) to loading duration in seconds (int).
        :rtype: dict
        """
        tenant_durations: dict = {}
        try:
            directory = os.fsencode(self.path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if not (filename.startswith("bexhoma-loading") and filename.endswith(".sensor.log")):
                    continue
                log_path = os.path.join(self.path, filename)
                try:
                    with open(log_path, encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    tenant_match = re.search(r'BEXHOMA_TENANT_ID\s+(\d+)', content)
                    duration_match = re.search(r'BEXHOMA_DURATION:(\d+)', content)
                    if tenant_match and duration_match:
                        tenant_id = int(tenant_match.group(1))
                        duration = int(duration_match.group(1))
                        tenant_durations[tenant_id] = max(tenant_durations.get(tenant_id, 0), duration)
                except Exception:
                    pass
        except Exception:
            pass
        return tenant_durations

    def get_loading_per_run_multitenant(self):
        """
        Returns loading metrics aggregated per
        ``(code, experiment_run, type_tenants, vol_tenants, num_tenants, tenant_id)``
        for multi-tenant experiments.

        For container tenancy the ``tenant_id`` key distinguishes individual tenant
        loading times.

        For schema/database tenancy, reads per-pod sensor log files via
        :meth:`_get_tenant_loading_from_logs` to expand the single shared
        connection row into one row per tenant.  Each row carries the tenant's
        own loading duration (``time_ingest`` / ``time_load``) and a matching
        ``tenant_id``.  If the sensor logs are absent the result collapses to
        one row with ``tenant_id = ''`` (same as before).

        :return: DataFrame with one row per tenant per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_loading_per_connection()
        if (df['type_tenants'].isin(['schema', 'database'])).any():
            tenant_durations = self._get_tenant_loading_from_logs()
            if tenant_durations:
                expanded = []
                for _, row in df.iterrows():
                    if row['type_tenants'] in ('schema', 'database'):
                        for tid, duration in tenant_durations.items():
                            new_row = row.copy()
                            new_row['tenant_id'] = str(tid)
                            new_row['time_ingest'] = float(duration)
                            new_row['time_load'] = float(duration)
                            sf = float(row['SF'])
                            new_row['Throughput [SF/h]'] = sf * 3600.0 / duration if duration > 0 else 0.0
                            expanded.append(new_row)
                    else:
                        expanded.append(row)
                df = pd.DataFrame(expanded)
        df = df.groupby(["code", "experiment_run", "type_tenants", 'vol_tenants', "num_tenants", "tenant_id"]).max()
        df = df.reset_index()
        df.index = (df['code'].astype(str) + "-" +
                    df['configuration'].astype(str) + "-" +
                    df['experiment_run'].astype(str) + "-" +
                    df['tenant_id'].astype(str))
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        df['Throughput [SF/h]'] = df_tpx
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('client', axis=1, inplace=True, errors='ignore')
        df.drop('pods', axis=1, inplace=True, errors='ignore')
        return df
    def get_summary_loading_per_run_multitenant(self):
        """
        Returns loading metrics per tenant per experiment run, with housekeeping columns removed.

        Wraps :meth:`get_loading_per_run_multitenant` and drops ``code`` and
        ``configuration`` so the result is ready to display in :meth:`show_summary`.

        :return: DataFrame with one row per ``(tenant_id, experiment_run)`` combination.
        :rtype: pandas.DataFrame
        """
        df = self.get_loading_per_run_multitenant()
        df.drop('code', axis=1, inplace=True, errors='ignore')
        df.drop('configuration', axis=1, inplace=True, errors='ignore')
        return df
