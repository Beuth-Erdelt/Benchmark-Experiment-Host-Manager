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
import glob
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
    """
    def __init__(self, code, path, include_loading=False, include_benchmarking=True):
        """
        :param code: Experiment identifier — also the name of the result sub-folder.
        :param path: Root path that contains the result folders.
        :param include_loading: Whether loading-phase results are expected.
        :param include_benchmarking: Whether benchmarking-phase results are expected.
        """
        self.path = path + "/" + code
        self.code = code
        self.include_loading = include_loading
        self.include_benchmarking = include_benchmarking
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
    def transform_all_logs_benchmarking(self):
        """
        Iterates over all benchmarker log files and calls :meth:`end_benchmarking` for each.
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker") and filename.endswith(".dbmsbenchmarker.log"):
                pod_name = filename[filename.rindex("-")+1:-len(".log")]
                jobname = filename[len("bexhoma-benchmarker-"):-len("-"+pod_name+".dbmsbenchmarker.log")]
                self.end_benchmarking(jobname)
    def transform_all_logs_loading(self):
        """
        Iterates over all loader sensor log files and calls :meth:`end_loading` for each.
        """
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-loading") and filename.endswith(".sensor.log"):
                pod_name = filename[filename.rindex("-")+1:-len(".log")]
                jobname = filename[len("bexhoma-loading-"):-len("-"+pod_name+".sensor.log")]
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
    def reconstruct_workflow(self, df):
        """
        Reconstructs the experiment workflow structure from a benchmarking results DataFrame.

        Returns a nested dict mapping each configuration name to a list of runs, where each
        run is a list of result counts per client — for example::

            {'MySQL-24-4-1024': [[1, 2], [1, 2]]}

        means 2 experiment runs, each consisting of client 1 (1 result) then client 2
        (2 results, i.e. 2 pods in parallel).

        :param df: Benchmarking DataFrame with columns ``configuration``, ``experiment_run``,
                   and ``client`` (pods already aggregated).
        :type df: pandas.DataFrame
        :return: Workflow dict mapping configuration name to per-run client result counts.
        :rtype: dict
        """
        configs = dict()
        for _, row in df.iterrows():
            config_name = row['configuration']
            if config_name not in configs:
                configs[config_name] = dict()
            if row['experiment_run'] not in configs[config_name]:
                configs[config_name][row['experiment_run']] = dict()
            if row['client'] not in configs[config_name][row['experiment_run']]:
                configs[config_name][row['experiment_run']][row['client']] = {'result_count': 0}
            configs[config_name][row['experiment_run']][row['client']]['result_count'] += 1
        workflow = dict()
        for config_name, run_dict in configs.items():
            workflow[config_name] = []
            for _run_num, client_dict in run_dict.items():
                client_counts = [client_data['result_count'] for client_data in client_dict.values()]
                workflow[config_name].append(client_counts)
        return workflow
    def test_results(self):
        """
        Validates results locally and returns an exit code.

        :return: ``0`` on success; subclasses return ``1`` on failure.
        :rtype: int
        """
        return 0
    def test_results_column(self, df, test_column, silent=False, title=''):
        """
        Checks whether a column in a DataFrame contains any zero or NaN values.

        :param df: DataFrame to check.
        :type df: pandas.DataFrame
        :param test_column: Column name to inspect.
        :type test_column: str
        :param silent: When ``True``, suppresses printed output.
        :type silent: bool
        :param title: Optional label prefix for the printed message.
        :type title: str
        :return: ``True`` if the column is fully populated with non-zero values,
                 ``False`` otherwise.
        :rtype: bool
        """
        if len(title) > 0:
            title = f"{title} {test_column}"
        else:
            title = test_column
        if not df is None and not df.empty:
            contains_zero_or_nan = df[test_column].isin([0]) | df[test_column].isna()
            if contains_zero_or_nan.any():
                if not silent:
                    print("* TEST failed: {} contains 0 or NaN".format(title))
                return False
            else:
                if not silent:
                    print("* TEST passed: {} contains no 0 or NaN".format(title))
                return True
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
            'experiment_run': c['parameter']['numExperiment'],
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
            'tenant': c['parameter']['TENANT'] if 'TENANT' in c['parameter'] else '',
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
    def get_connections_of_experiment(self):
        """
        Returns connection metadata for a single experiment.

        Reads ``connections.config`` and builds a row per pod/client with the
        following key columns: ``phase``, ``code``, ``connection``, ``configuration``,
        ``experiment_run``, ``client``, ``type_tenants``, ``num_tenants``,
        ``vol_tenants``, plus flattened host-system, loading-parameter,
        benchmarking-parameter, and SUT-parameter fields.

        When a connection entry carries ``orig_name``, the entry represents an
        individual pod; otherwise a synthetic row is generated for each parallel
        client.

        :return: DataFrame of connection metadata, one row per pod/client.
        :rtype: pandas.DataFrame
        """
        with open(self.path + "/connections.config", 'r') as f:
            connections = ast.literal_eval(f.read())
        connections_sorted = sorted(connections, key=lambda conn: conn['name'])
        result = dict()
        for conn in connections_sorted:
            if 'orig_name' in conn:
                # entry represents an individual pod — use the pod name as connection id
                name = conn['name']
                conn['phase'] = "{code}-{connection}".format(code=conn['parameter']['code'], connection=conn['orig_name'])
                connection_id = "{code}-{connection}".format(code=conn['parameter']['code'], connection=name)
                self.add_connection_to_result(conn, connection_id, result)
            else:
                # no per-pod entries — synthesise one row per parallel client
                num_clients = int(conn['parameter']['parallelism'])
                name = conn['name']
                for client_idx in range(1, num_clients + 1):
                    conn['name'] = "{code}-{phase}-{client}".format(code=conn['parameter']['code'], phase=name, client=client_idx)
                    conn['phase'] = "{code}-{phase}".format(code=conn['parameter']['code'], phase=name)
                    connection_id = "{code}-{phase}-{client}".format(code=conn['parameter']['code'], phase=name, client=client_idx)
                    self.add_connection_to_result(conn, connection_id, result)
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
            'tenant', 'type_tenants', 'num_tenants', 'vol_tenants', 'Throughput [SF/h]',
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
    def get_loading_per_run_multitenant(self):
        """
        Returns loading metrics aggregated per ``(code, experiment_run, type_tenants,
        vol_tenants, num_tenants)`` for multi-tenant experiments.

        Takes the per-connection DataFrame from :meth:`get_loading_per_connection` and
        reduces it by taking the max within each tenancy group, then recomputes
        ``'Throughput [SF/h]'`` from the aggregated load time.

        :return: DataFrame with one row per tenant group per experiment run.
        :rtype: pandas.DataFrame
        """
        df = self.get_loading_per_connection()
        df = df.groupby(["code", "experiment_run", "type_tenants", 'vol_tenants', "num_tenants"]).max()
        df = df.reset_index()
        df.index = df['code'].astype(str) + "-" + \
                   df['configuration'].astype(str) + "-" + \
                   df['experiment_run'].astype(str)
        df_load = df['time_load'].copy()
        df_tpx = (df['SF'] * 3600.0)/df_load.sort_index()
        df['Throughput [SF/h]'] = df_tpx
        df.drop('connection', axis=1, inplace=True, errors='ignore')
        df.drop('phase', axis=1, inplace=True, errors='ignore')
        df.drop('client', axis=1, inplace=True, errors='ignore')
        df.drop('pods', axis=1, inplace=True, errors='ignore')
        return df
