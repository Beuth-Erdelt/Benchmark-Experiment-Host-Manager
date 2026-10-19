"""
Base experiment class and general-purpose experiment types.

Provides :class:`DictToObject`, :class:`ExperimentBase` (the core experiment
class plugged into a cluster object to manage the full lifecycle of a bexhoma
experiment), and derived types :class:`IotExperiment`, :class:`TsbsExperiment`,
:class:`ExampleExperiment`, and :class:`TpcxaiExperiment`. Each experiment
folder must contain a query file and per-DBMS schema subfolders.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter, inspector
import logging
import urllib3
from os import makedirs, path
import time
from timeit import default_timer
import os
from datetime import datetime, timedelta
import re
import pandas as pd
import json
import ast
import copy
import functools
import threading
from collections import Counter
from types import SimpleNamespace
from importlib.metadata import version
from pathlib import Path
import math
from typing import TYPE_CHECKING, List, Tuple, Optional

from bexhoma import evaluators
from bexhoma import missing_metrics
from bexhoma.monitoring_math import (counter_total, min_measurable_window, read_connections,
                                     scoped_job_connections, DEFAULT_SCRAPE_INTERVAL_SECONDS)
from bexhoma.cli_args import split_storage_types, resource_cells, set_cell_storage, resolve_keep_sut, split_worker_nodes
from bexhoma import sut_restarts
from bexhoma.tls import TLS_COMPONENT
from bexhoma.metric_fetching import DEFAULT_MAX_PARALLEL_FETCHES, MetricFetchBatch
from bexhoma.parallel_steps import DEFAULT_MAX_PARALLEL_STEPS, OrderedUpload, run_steps
from bexhoma.cluster_calls import CALL_STATS, stored_pods

if TYPE_CHECKING:
    from bexhoma.configurations.base import SutConfiguration

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = [
    "DictToObject",
    "parse_set_arg",
    "ExperimentBase",
    "IotExperiment",
    "TsbsExperiment",
    "ExampleExperiment",
    "TpcxaiExperiment",
]


class DictToObject(object):
    """
    Recursively convert a nested dict into an object with attribute access.

    Nested dicts become nested :class:`DictToObject` instances; all other
    values are stored as-is.
    """
    def __init__(self, dictionary):
        def _traverse(key, element):
            if isinstance(element, dict):
                return key, DictToObject(element)
            else:
                return key, element
        objd = dict(_traverse(k, v) for k, v in dictionary.items())
        self.__dict__.update(objd)


SELECTOR_RE = re.compile(
    r'^(?P<kind>deployment|statefulset)\[(?P<workload>[^\]]+)\]'
    r'(@(?P<config>[^.\[\]]+))?'
    r'\.container\[(?P<container>[^\]]+)\]\.(?P<param>[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)?)$',
    re.IGNORECASE
)


#: Divisor to convert the ``--experiment-timeout`` CLI value (minutes) to seconds.
SECONDS_PER_MINUTE = 60

#: Minutes a benchmark round may take from submission until all of its pods
#: have passed the synchronised start (the round pod counter reaching 0).
#: Rounds normally start within seconds; a pod that cannot be scheduled
#: would otherwise leave the others waiting for it forever. The benchmark
#: itself, once started, has no limit.
BENCHMARK_START_TIMEOUT_MINUTES = 15

#: Container waiting reasons that mean a loading pod cannot pull its image.
IMAGE_PULL_WAITING_REASONS = frozenset({'ErrImagePull', 'ImagePullBackOff'})

#: Wait before the next loop pass after a step of bexhoma itself whose next
#: step needs no change in the cluster (a job ended and deleted, a stuck round
#: skipped, a stopped SUT gone). Every other pass waits the full interval.
FOLLOW_UP_WAIT_SECONDS = 0

#: Follow-up waits in a row before the loop waits the full interval again, so
#: a state that does not resolve never turns into a tight loop.
MAX_FOLLOW_UP_WAITS_IN_A_ROW = 3

def parse_set_arg(s: str) -> Tuple[dict, str]:
    """
    Parse a single ``--set`` argument of the form ``<selector>=<value>``.

    The selector must match one of:

    * ``deployment[NAME].container[CONTAINER].PARAM``
    * ``statefulset[NAME].container[CONTAINER].PARAM``
    * ``deployment[NAME]@CONFIG.container[CONTAINER].PARAM``
    * ``statefulset[NAME]@CONFIG.container[CONTAINER].PARAM``

    ``PARAM`` may carry one extension prefix, e.g. ``duckdb.max_memory``.

    The optional ``@CONFIG`` scope restricts the operation to the one
    configuration whose :attr:`~bexhoma.configurations.base.SutConfiguration.configuration`
    equals ``CONFIG`` (see :meth:`~bexhoma.configurations.manifest.ManifestBuilder.patch_dbms_args`).
    Without it, an operation applies to every configuration matching
    ``NAME`` — this is what makes a resource sweep (several configurations
    built from the same docker image, each with its own derived knob
    values) expressible without changing the meaning of any existing,
    unscoped ``--set``.

    :param s: Raw ``--set`` string from the CLI.
    :return: A tuple of (selector_dict, value_str) where selector_dict
             contains keys ``kind``, ``workload``, ``config``, ``container``, and ``param``.
             ``config`` is ``""`` when the selector carries no ``@CONFIG`` scope.
    :rtype: tuple[dict, str]
    :raises ValueError: When the string has no ``=`` or the selector does not match.
    """
    if "=" not in s:
        raise ValueError(f"--set expects selector=value (got: {s})")
    selector, value = s.split("=", 1)
    m = SELECTOR_RE.match(selector.strip())
    if not m:
        raise ValueError(
            "Invalid selector. Expected e.g. "
            "deployment[sut].container[dbms].max_worker_processes "
            "or deployment[sut]@PostgreSQL-2.container[dbms].shared_buffers"
        )
    d = m.groupdict()
    d["kind"] = d["kind"].lower()
    d["config"] = d["config"] or ""
    return d, value.strip()


class ExperimentBase():
    """
    Class for defining an experiment.
    Settings are set generally.
    This class should be overloaded to define specific experiments.
    """
    #: Whether ``-rc/-lc/-rr/-lr/-rst`` may carry a comma list for this
    #: experiment, so :meth:`expand_resource_cells` sweeps every DBMS
    #: configuration across them (see :func:`bexhoma.cli_args.resource_cells`).
    supports_storage_sweep = False

    def __init__(self,
                 cluster,
                 code=None,
                 num_experiment_to_apply = 1,
                 timeout = 7200):
        """
        Construct a new 'experiment' object.

        :param cluster: Cluster object, typically refering to a K8s cluster
        :param code: Unique identifier for the experiment. If none is given, it is created out of current time
        :param num_experiment_to_apply: How many times should the experiment be repeated at every configuration?
        :param timeout: Maximum timeout per query
        """
        self.cluster = cluster                                          # cluster object
        self.code = code                                                # code of experiment
        if self.code is None:
            self.code = str(round(time.time()))
        else:
            self.code = str(self.code)
        self.path = self.cluster.resultfolder+"/"+self.code             # path to result folder (read from cluster.config)
        if not path.isdir(self.path):
            makedirs(self.path)
        self.cluster.set_code(code=self.code)
        self.set_connection_management(
            numProcesses = 1,
            runsPerConnection = 0,
            timeout = timeout,
            singleConnection = True)
        self.components = {                                             # maps component types to required sub-components
            "loader": {
                "datagenerator": True,
                "sensor": True
             },
            "benchmarker": {
                "dbmsbenchmarker": True
            }
        }
        self.pod_dashboard = ""                                         # name of the dashboard pod
        self.num_experiment_to_apply = num_experiment_to_apply          # how many times should the experiment run in a row?
        self.max_sut = None                                             # max number of SUT in the cluster at the same time
        self.max_parallel_fetches = DEFAULT_MAX_PARALLEL_FETCHES        # metrics.py runs at the same time after a loop pass (1 = one by one)
        self.max_parallel_steps = DEFAULT_MAX_PARALLEL_STEPS            # configurations whose job submissions / job ends of a loop pass run at the same time (1 = one by one)
        self._copy_metrics_script = ""                                  # name of the uploaded copy script, see ensure_copy_metrics_script()
        self.keep_sut = False                                          # keep each configuration's last SUT running at the end (-ks/-ss, resolved in prepare_testbed)
        self.max_experiment_minutes: Optional[int] = None                # abort and remove experiment from cluster after this many minutes; None = no limit
        self.max_loading_minutes: Optional[int] = None                   # abort a configuration that remains in loading after this many minutes; None = no limit
        self.client = 0                                                 # number of client in benchmarking list - for synching between different configs (multi-tenant container-wise)
        self.num_tenants = 0                                            # number of tenants for multi-tenant experiments
        self.tenant_per = ""                                            # granularity of tenancy: 'container', 'schema', etc.
        self.multi_tenant_volume = False                                # True if each tenant gets a dedicated persistent volume
        self.cluster.add_experiment(self)
        self.appname = self.cluster.appname                             # app name for namespacing cluster - default is bexhoma
        self.resources = {}                                             # dict of resources infos that will be attached to SUT (like requested CPUs)
        self.ddl_parameters = {}                                        # DDL schema parameter for init scripts (like index type or sharding strategy)
        self.eval_parameters = {}                                       # parameters that will be handed over to dbmsbenchmarker
        self.storage = {}                                               # parameters for persistent storage (like type and size)
        self.nodes = {}                                                 # dict of node infos to guide components (like nodeSelector for SUT)
        self.loading_parameters = {}                                    # dict of parameters for loading component
        self.default_loading_parameters = {}                            # default ENV for all loading components, merged before per-config overrides
        self.sut_parameters = {}                                        # dict of parameters for sut and worker component
        self.loading_patch = ""                                         # YAML to patch manifest for loading component
        self.benchmarking_active = True                                 # Bool, tells if benchmarking is active (False for mode=start and mode=load)
        self.benchmarking_patch = ""                                    # YAML to patch manifest for benchmarking component
        self.benchmarking_parameters = {}                               # dict of parameters for benchmarking component
        self.default_benchmarking_parameters = {}                       # default ENV for all benchmarking components, merged before per-config overrides
        self.jobtemplate_loading = ""                                   # name of YAML manifest for loading component
        self.jobtemplate_benchmarking = ""                              # name of YAML manifest for benchmarking component
        self.query_management = {}                                      # parameters for query.config
        self.additional_labels = dict()                                 # dict of additional labels for components
        self.workload = {}                                              # dict containing workload infos - will be written to query.config
        self.workload['monitoring_components'] = {}                     # dict for infos about which components are monitored
        self.workload['optional_monitoring_components'] = []            # component types whose empty/zero CPU metrics are not a test failure
        self.monitoring_active = True                                   # Bool, tells if monitoring is active
        self.monitor_app_active = True                                  # Bool, tells if application-level metrics are monitored
        self.monitoring_metric_overrides = {}                           # dict of hardware metric key -> active, overriding cluster.config (-mm)
        self.prometheus_interval = "10s"                               # interval for Prometheus to fetch metrics
        self.prometheus_timeout = "10s"                                 # timeout for Prometheus to fetch metrics
        self.loading_active = False                                     # Bool, tells if distributed loading is active (i.e., push instead of pull)
        self.loading_deactivated = False                                # Bool, tells if loading phase should be skipped
        self.num_loading = 0                                            # number of loading pods in parallel
        self.num_loading_pods = 0                                       # number of loading pods in total
        self.resetscript_active = False                                 # Bool, tells if configured reset scripts should run
        self.script = ""                                                # name of the script collection for creating schema
        self.initscript = []                                            # list of scripts for creating schema
        self.indexing = ""                                              # name of the script collection for creating indexes
        self.indexscript = []                                           # list of scripts for creating indexes
        self.volume = ""                                                # volume key used to look up init scripts in cluster config
        self.volumeid = ""                                              # cluster-internal ID of the persistent volume
        self.queryfile = ""                                             # name of the query config file for dbmsbenchmarker
        # command line parameters
        self.args = None                                                # command line parameters as an object
        self.args_dict = dict()                                         # command line parameters as a dict
        self.dbms_args = []                                             # parsed --set selector/value pairs from CLI
        # k8s:
        self.namespace = self.cluster.namespace                         # name of the K8s namespace to use
        self.configurations = []                                        # list of configurations (i.e., dbms to test)
        self.storage_types = [None]                                     # storage class per resource cell, None = ephemeral (set from -rst)
        self.resource_cells = []                                        # one dict per swept resource cell (set from -rc/-lc/-rr/-lr/-rst)
        self.storage_label = ''                                         # label to mark persistent storage with (so that they can be matched to experiment)
        self.experiments_configfolder = ''                              # relative path to config folder of experiment (e.g., 'experiments/tpch')
        self.evaluator = evaluators.LogEvaluator(                               # set evaluator for experiment - default uses base
            code=self.code, path=self.cluster.resultfolder, include_loading=True, include_benchmarking=True)
        self.benchmarks: list = []                                        # ordered Benchmark objects; index+1 = benchmark_index
        self.evaluators: dict = {}                                        # benchmark.name → evaluator instance
        self._test_results: list[tuple[bool, str]] = []                  # collected (passed, label) pairs for show_summary
        self._runtime_test_results: list[tuple[bool, str]] = []          # failures detected before show_summary rebuilds its test list
        self._benchmark_rounds_starting: dict[str, tuple[str, datetime]] = {}  # configuration → (round counter key, submission time) until all round pods started
        self._image_pull_waits_seen: set[str] = set()                    # loading pods already reported as waiting for their image
        self.set_eval_parameters(code = self.code)
    def process(self) -> None:
        """
        Run the experiment according to self.args.mode.

        Dispatches to the appropriate workflow branch (start, load, summary,
        or the default full benchmark run) and prints timing information.
        """
        self.expand_resource_cells()
        # should results be tested for validity?
        test_result = self.args.test_result
        if self.args.mode == 'start':
            start = default_timer()
            start_datetime = str(datetime.now())
            print("{:30s}: has code {}".format("Experiment", self.code))
            print("{:30s}: starts at {} ({})".format("Experiment", start_datetime, start))
            print("{:30s}: {}".format("Experiment", self.workload['info']))
            # configure number of clients per config = 0
            list_clients = []
            self.add_benchmark_list(list_clients)
            self.benchmarking_active = False
            # persist workflow_planned before work_benchmark_list() so a crash mid-run
            # (e.g. during cube building on resume) still leaves it in queries.config
            self.store_workflow_results()
            start = default_timer()
            start_datetime = str(datetime.now())
            # run workflow
            self.work_benchmark_list(stop_after_benchmarking=True, stop_after_loading=True, stop_after_starting=True)
            # total time of experiment
            end = default_timer()
            end_datetime = str(datetime.now())
            duration_experiment = end - start
            print("{:30s}: ends at {} ({}) - {:.2f}s total".format("Experiment", end_datetime, end, duration_experiment))
            self.workload['duration'] = math.ceil(duration_experiment)
            self.evaluate_results()
            self.store_workflow_results()
            self.show_summary(write_report=getattr(self.args, 'write_report', False))
        elif self.args.mode == 'load':
            start = default_timer()
            start_datetime = str(datetime.now())
            print("{:30s}: has code {}".format("Experiment", self.code))
            print("{:30s}: starts at {} ({})".format("Experiment", start_datetime, start))
            print("{:30s}: {}".format("Experiment", self.workload['info']))
            # configure number of clients per config = 0
            list_clients = []
            self.add_benchmark_list(list_clients)
            self.benchmarking_active = False
            # persist workflow_planned before work_benchmark_list() so a crash mid-run
            # (e.g. during cube building on resume) still leaves it in queries.config
            self.store_workflow_results()
            start = default_timer()
            start_datetime = str(datetime.now())
            # run workflow
            self.work_benchmark_list(stop_after_benchmarking=self.keep_sut, stop_after_loading=True)
            # total time of experiment
            end = default_timer()
            end_datetime = str(datetime.now())
            duration_experiment = end - start
            print("{:30s}: ends at {} ({}) - {:.2f}s total".format("Experiment", end_datetime, end, duration_experiment))
            self.workload['duration'] = math.ceil(duration_experiment)
            self.evaluate_results()
            self.store_workflow_results()
            self.show_summary(write_report=getattr(self.args, 'write_report', False))
        elif self.args.mode == 'summary':
            self.show_summary(write_report=getattr(self.args, 'write_report', False))
        else:
            # total time of experiment
            start = default_timer()
            start_datetime = str(datetime.now())
            print("{:30s}: has code {}".format("Experiment", self.code))
            print("{:30s}: starts at {} ({})".format("Experiment", start_datetime, start))
            print("{:30s}: {}".format("Experiment", self.workload['info']))
            # persist workflow_planned before work_benchmark_list() so a crash mid-run
            # (e.g. during cube building on resume) still leaves it in queries.config
            self.store_workflow_results()
            # run workflow
            self.work_benchmark_list(stop_after_benchmarking=self.keep_sut)
            # total time of experiment
            end = default_timer()
            end_datetime = str(datetime.now())
            duration_experiment = end - start
            print("{:30s}: ends at {} ({}) - {:.2f}s total".format("Experiment", end_datetime, end, duration_experiment))
            self.workload['duration'] = math.ceil(duration_experiment)
            ##################
            self.evaluate_results()
            self.store_workflow_results()
            # zip() skipped: causes OOM (exit code 137) in large experiments
            if test_result:
                test_result_code = self.test_results()
                if test_result_code == 0:
                    print("Test successful!")
            self.show_summary(write_report=getattr(self.args, 'write_report', False))
    def benchmarking_is_active(self) -> bool:
        """
        Returns True, when this is a benchmarking experiment.
        Returns False in case of mode=start or mode=load.
        In that case, benchmarking phase is skipped and no results are expected.

        :return: Iff there is a benchmarking phase
        """
        if 'benchmarking_active' in self.workload:
            self.benchmarking_active = self.workload['benchmarking_active']
        return self.benchmarking_active
    def loading_is_active(self) -> bool:
        """
        Returns True, when this is an experiment including loading.
        Returns False in case of mode=start.
        In that case, loading and benchmarking phases are skipped and no results are expected.

        :return: Iff there is a benchmarking phase
        """
        if 'loading_active' in self.workload:
            self.loading_deactivated = not self.workload['loading_active']
        return not self.loading_deactivated
    def result_filename_local(self, filename: str) -> str:
        """
        Returns filename including path in result folder.

        :param filename: name of a file in a result folder
        :param posix: iff posix format should be used
        :return: self.path / filename
        """
        return self.result_filename(filename, False)
    def result_filename_remote(self, filename: str, posix: bool = True) -> str:
        """
        Returns filename including path in result folder.

        :param filename: name of a file in a result folder
        :param posix: iff posix format should be used
        :return: self.path / filename
        """
        path = Path(r"/results") / filename
        if posix:
            return path.as_posix()
        else:
            return str(path)
    def result_filename(self, filename: str, posix: bool = True) -> str:
        """
        Returns filename including path in a local result folder.

        :param filename: name of a file in a result folder
        :param posix: iff posix format should be used
        :return: self.path / filename
        """
        path = Path(self.path) / filename
        if posix:
            return path.as_posix()
        else:
            return str(path)
    def upload_experiment_file(self, filename: str) -> str:
        """
        Upload a result file to the dashboard pod.

        :param filename: Name of the file relative to the experiment result folder.
        :return: Output of the upload command, or empty string when no dashboard pod is available.
        """
        if not len(self.pod_dashboard):
            pods = self.cluster.get_pods(component='dashboard')
            if len(pods) > 0:
                self.pod_dashboard = pods[0]
            else:
                return ""
        filename_local = self.path+'/.' if not filename else self.path+'/'+filename
        filename_remote = '/results/'+str(self.code)+'/'+filename
        return self.cluster.upload_file(filename_local=filename_local, filename_remote=filename_remote, pod=self.pod_dashboard)
    def upload_experiment_files(self, filenames: list) -> str:
        """
        Upload several result files to the dashboard pod in one go (see ``Kubernetes.upload_files()``).

        :param filenames: Names of files relative to the experiment result folder.
        :return: Output of the upload command, or empty string when no dashboard pod is available.
        """
        filenames = list(dict.fromkeys(filenames))
        if not filenames:
            return ""
        if len(filenames) == 1:
            return self.upload_experiment_file(filenames[0])
        if not len(self.pod_dashboard):
            pods = self.cluster.get_pods(component='dashboard')
            if len(pods) > 0:
                self.pod_dashboard = pods[0]
            else:
                return ""
        return self.cluster.upload_files(
            filenames_local=[self.path+'/'+filename for filename in filenames],
            dir_remote='/results/'+str(self.code), pod=self.pod_dashboard)
    def result_files_lock(self) -> threading.RLock:
        """Lock for the result files every connection reads and rewrites.

        ``connections.config``, ``protocol.json`` and ``experiments.config``
        are read, changed and written again by each job submission and job
        end; with several configurations at once (see
        :func:`~bexhoma.parallel_steps.run_steps`) only one may do so at a time.

        :return: The lock of this experiment.
        """
        return self.__dict__.setdefault('_result_files_lock', threading.RLock())
    def upload_result_files(self, filenames: list) -> None:
        """Upload result files that other configurations may rewrite meanwhile.

        Like :meth:`upload_experiment_files`, but uploads requested by several
        threads at the same time are merged and never overtake each other (see
        :class:`~bexhoma.parallel_steps.OrderedUpload`): the pod always ends
        with the newest local version.

        :param filenames: Names of files relative to the experiment result folder.
        """
        with self.result_files_lock():
            uploader = self.__dict__.get('_ordered_upload')
            if uploader is None:
                uploader = self._ordered_upload = OrderedUpload(
                    lambda names: self.upload_experiment_files(names))
        uploader.upload(filenames)
    #: Copies metric CSVs of one connection to another (``MetricsCollector.copy_fetched``).
    #: Shipped as a file, because ``$`` in an inline ``sh -c`` would be expanded by
    #: the local shell on Linux and not on Windows.
    COPY_METRICS_SCRIPT = (
        '#!/bin/sh\n'
        '# usage: bexhoma-copy-metrics.sh FOLDER SOURCE TARGET COMPONENT_TYPE...\n'
        'folder=$1; src=$2; tgt=$3; shift 3\n'
        'cd "$folder" || exit 1\n'
        'for t in "$@"; do\n'
        '  for f in query_${t}_metric_*_${src}.csv; do\n'
        '    [ -f "$f" ] || continue\n'
        '    g="${f%_${src}.csv}_${tgt}.csv"\n'
        '    { echo "$tgt"; tail -n +2 "$f"; } > "$g.tmp" && mv "$g.tmp" "$g"\n'
        '  done\n'
        'done\n'
    )
    def ensure_copy_metrics_script(self) -> str:
        """Write and upload the metrics copy script once per experiment.

        :return: Its filename in the result folder.
        """
        filename = 'bexhoma-copy-metrics.sh'
        if self._copy_metrics_script != filename:
            with open(self.result_filename_local(filename), 'w', newline='\n') as f:
                f.write(self.COPY_METRICS_SCRIPT)
            self.upload_experiment_file(filename)
            self._copy_metrics_script = filename
        return filename
    def download_experiment_file(self, filename: str) -> str:
        """
        Download a result file from the dashboard pod.

        An empty ``filename`` downloads the whole experiment result folder,
        packed into a single archive in the pod (see
        :meth:`bexhoma.clusters.Kubernetes.download_folder`).

        :param filename: Name of the file relative to the experiment result folder.
        :return: Output of the download command, or empty string when no dashboard pod is available.
        """
        if not len(self.pod_dashboard):
            pods = self.cluster.get_pods(component='dashboard')
            if len(pods) > 0:
                self.pod_dashboard = pods[0]
            else:
                return ""
        if not filename:
            return self.cluster.download_folder(folder_remote='/results/'+str(self.code), folder_local=self.path, pod=self.pod_dashboard)
        filename_local = self.path+'/'+filename
        filename_remote = '/results/'+str(self.code)+'/'+filename
        return self.cluster.download_file(filename_local=filename_local, filename_remote=filename_remote, pod=self.pod_dashboard)
    def get_parameter_as_list(self,
                              parameter: str) -> list:
        """
        Transform comma separated CLI parameters to list.
        This is for example used to transform num_loading_pods.

        :param parameter: Comma separated list of values
        :return: Python list of values
        """
        if parameter in self.args_dict:
            value = self.args_dict[parameter]
        else:
            return []
        if len(value) > 0:
            values = value.split(",")
            value = [int(entry) for entry in values]
        elif value.isdigit():
            value = list(int(value))
        return value
    def get_parameter_as_list_str(self,
                                  parameter: str) -> list:
        """
        Transform a comma separated CLI parameter into a list of strings,
        without casting entries to int. This is for parameters whose values
        are not numbers, e.g. RAM quantities such as ``32Gi,64Gi``.

        :param parameter: Comma separated list of values
        :return: Python list of string values
        :rtype: list[str]
        """
        if parameter not in self.args_dict:
            return []
        value = self.args_dict[parameter]
        if len(value) == 0:
            return []
        return [entry for entry in value.split(",") if len(entry) > 0]
    def prepare_testbed(self,
                        parameter: dict) -> None:
        """
        Prepares a testbed.
        It takes the CLI arguments as a dict.
        This method for example sets workload['info'].
        It also sets monitoring, storage, components settings, SUT resources and nodes for components.
        It makes sure, dashboard, messagequeue, data dir and result dir are ready.

        :param parameter: Comma separated list of values
        """
        if (not 'type' in self.workload) or (len(self.workload['type']) == 0):
            # set default workload type
            self.workload['type'] = 'dbmsbenchmarker'
        args = SimpleNamespace(**parameter)
        self.args = args
        self.args_dict = parameter
        self.dbms_args = []
        if 'sets' in parameter:
            for s in args.sets:
                sel, value = parse_set_arg(s)
                self.dbms_args.append((sel, value))
        #print(self.dbms_args)
        mode = str(parameter['mode'])
        if mode=='load' or mode=='start':
            self.benchmarking_active = False
        if mode=='start':
            self.loading_deactivated = True
        num_experiment_to_apply = int(args.num_config)
        # configure number of clients per config
        list_clients = args.num_query_executors.split(",")
        if len(list_clients) > 0:
            list_clients = [int(x) for x in list_clients if len(x) > 0]
        else:
            list_clients = []
        monitoring = args.monitoring
        monitoring_cluster = args.monitoring_cluster
        monitoring_app = args.monitoring_app
        self.set_monitoring_metric_overrides(
            getattr(args, 'monitoring_metrics', None) or {},
            monitoring_enabled=bool(monitoring or monitoring_cluster),
        )
        # only for dbmsbenchmarker
        if 'num_run' in parameter:
            numRun = int(args.num_run)
        else:
            numRun = 0
        self.workload['num_run'] = numRun
        if 'datatransfer' in parameter:
            datatransfer = args.datatransfer
        else:
            datatransfer = False
        num_loading_pods = self.get_parameter_as_list('num_loading_pods')
        num_loading_threads = self.get_parameter_as_list('num_loading_threads')
        num_benchmarking_pods = self.get_parameter_as_list('num_benchmarking_pods')
        num_benchmarking_threads = self.get_parameter_as_list('num_benchmarking_threads')
        num_pooling_pods = self.get_parameter_as_list('num_pooling_pods')
        num_pooling_in = self.get_parameter_as_list('num_pooling_in')
        num_pooling_out = self.get_parameter_as_list('num_pooling_out')
        cpu_type = str(args.request_cpu_type)
        gpu_type = str(args.request_gpu_type)
        gpus = str(args.request_gpu)
        self.storage_types = split_storage_types(args.request_storage_type)
        # entry scripts with their own parser may not know -rnw
        worker_nodes = split_worker_nodes(
            getattr(args, 'request_node_worker', None), args.request_node_name)
        # -rc/-lc/-rr/-lr/-rst/-rnw may each carry a comma list; one cell per swept
        # setting, expanded per configuration by expand_resource_cells()
        self.resource_cells = resource_cells(
            request_cpu_list=self.get_parameter_as_list_str('request_cpu') or [str(args.request_cpu)],
            limit_cpu_list=self.get_parameter_as_list_str('limit_cpu') or [str(args.limit_cpu)],
            request_ram_list=self.get_parameter_as_list_str('request_ram') or [str(args.request_ram)],
            limit_ram_list=self.get_parameter_as_list_str('limit_ram') or [str(args.limit_ram)],
            storage_type_list=self.storage_types,
            worker_nodes_list=worker_nodes,
        )
        if len(self.resource_cells) > 1 and not self.supports_storage_sweep:
            raise ValueError(
                f"-rc/-lc/-rr/-lr/-rst/-rnw carry a list, but {type(self).__name__} "
                f"cannot sweep resources across configurations."
            )
        valid_storage_types = self.cluster.get_available_storage_types()
        for storage_type in self.storage_types:
            if storage_type not in valid_storage_types:
                raise ValueError(
                    f"Invalid --request-storage-type {storage_type!r} for cluster context "
                    f"{self.cluster.context!r}. Valid values: {valid_storage_types}."
                )
        # a sweep sets each configuration's resources and class itself; the
        # experiment-wide default is the first cell, so it is always valid
        cpu = self.resource_cells[0]['cpu']
        memory = self.resource_cells[0]['memory']
        cpu_limit = self.resource_cells[0]['cpu_limit']
        memory_limit = self.resource_cells[0]['memory_limit']
        request_storage_type = self.storage_types[0]
        request_storage_size = args.request_storage_size
        request_storage_remove = args.request_storage_remove
        # entry scripts with their own parser may not know -rsrp
        request_storage_remove_per_repetition = getattr(args, 'request_storage_remove_per_repetition', False)
        request_node_name = args.request_node_name
        request_node_loading = args.request_node_loading
        request_node_benchmarking = args.request_node_benchmarking
        request_node_pooling = args.request_node_pooling
        skip_loading = args.skip_loading
        # entry scripts with their own parser may not know -ks
        self.keep_sut = resolve_keep_sut(
            mode, getattr(args, 'keep_sut', 'auto'), getattr(args, 'skip_shutdown', False))
        test_result = args.test_result
        num_worker = int(args.num_worker)
        num_worker_replicas = int(args.num_worker_replicas)
        num_worker_shards = int(args.num_worker_shards)
        self.resetscript_active = args.activate_reset
        if args.experiment_timeout is not None:
            self.max_experiment_minutes = int(args.experiment_timeout)
        if args.loading_timeout is not None:
            self.max_loading_minutes = int(args.loading_timeout)
        multi_tenant_num = int(args.multi_tenant_num)
        multi_tenant_by = args.multi_tenant_by
        multi_tenant_volume = args.multi_tenant_volume
        self.num_tenants = multi_tenant_num
        self.tenant_per = multi_tenant_by
        self.multi_tenant_volume = multi_tenant_volume
        self.workload['num_tenants'] = self.num_tenants
        self.workload['tenant_per'] = self.tenant_per
        self.workload['multi_tenant_volume'] = self.multi_tenant_volume
        self.cluster.start_datadir()
        self.cluster.start_resultdir()
        self.cluster.start_dashboard()
        self.cluster.start_messagequeue()
        bexhoma_version = version('bexhoma')
        self.workload['info'] = self.workload['info']+"\nExperiment uses bexhoma version {}.".format(bexhoma_version)
        if monitoring_cluster:
            # monitor all nodes of cluster (for not missing any component)
            self.monitoring_active = True
            if numRun > 0:
                self.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
            self.cluster.start_monitoring_cluster()
            self.workload['info'] = self.workload['info']+"\nSystem metrics are monitored by a cluster-wide installation."
        elif monitoring:
            # we want to monitor resource consumption
            self.monitoring_active = True
            if numRun > 0:
                self.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
            self.workload['info'] = self.workload['info']+"\nSystem metrics are monitored by sidecar containers."
        else:
            # we want to just run the queries
            self.set_querymanagement_quicktest(numRun=numRun, datatransfer=datatransfer)
        self.monitor_app_active = monitoring_app
        if monitoring_app:
            self.workload['info'] = self.workload['info']+"\nApplication metrics are monitored by sidecar containers."
        if self.monitoring_metric_overrides:
            switched = ", ".join(
                f"{key} {'on' if active else 'off'}" for key, active in self.monitoring_metric_overrides.items())
            self.workload['info'] = self.workload['info']+f"\nHardware metrics switched for this experiment: {switched}."
        # set resources for dbms
        self.set_resources(
            requests = {
                'cpu': cpu,
                'memory': memory,
                'gpu': 0
            },
            limits = {
                'cpu': cpu_limit,
                'memory': memory_limit
            },
            nodeSelector = {
                'cpu': cpu_type,
                'gpu': '',
            },
            #replicas_pooling = num_pooling_pods,
        )
        # persistent storage
        self.set_storage(
            storageClassName = request_storage_type,
            storageSize = request_storage_size,#'100Gi',
            keep = True
            )
        # note more infos about experiment in workload description
        if len(args.dbms):
            # import is limited to some DBMS
            #if "," in args.dbms:
            #    # list of DBMS
            #    dbms = ", ".join(args.dbms)
            #else:
            #    # single DBMS
            #    dbms = args.dbms
            dbms = args.dbms
            self.workload['info'] = self.workload['info']+"\nExperiment is limited to DBMS {}.".format(dbms)
        if self.loading_is_active():
            if len(num_loading_pods):
                # import uses several processes in pods
                self.workload['info'] = self.workload['info']+"\nImport is handled by {} processes (pods).".format(" and ".join(map(str, num_loading_pods)))
            # fix loading
            if request_node_loading:
                self.patch_loading(patch="""
                spec:
                  template:
                    spec:
                      nodeSelector:
                        kubernetes.io/hostname: {node}
                """.format(node=request_node_loading))
                self.workload['info'] = self.workload['info']+"\nLoading is fixed to {}.".format(request_node_loading)
        # fix benchmarking
        if request_node_benchmarking:
            self.patch_benchmarking(patch="""
            spec:
              template:
                spec:
                  nodeSelector:
                    kubernetes.io/hostname: {node}
            """.format(node=request_node_benchmarking))
            self.workload['info'] = self.workload['info']+"\nBenchmarking is fixed to {}.".format(request_node_benchmarking)
        # fix SUT
        if request_node_name:
            self.set_resources(
                nodeSelector = {
                    'cpu': cpu_type,
                    'gpu': '',
                    'kubernetes.io/hostname': request_node_name
                })
            self.workload['info'] = self.workload['info']+"\nSUT is fixed to {}.".format(request_node_name)
        # fix workers (all StatefulSets of the SUT), spread evenly over the nodes
        if self.resource_cells[0]['worker_nodes']:
            self.set_resources(nodes_worker=self.resource_cells[0]['worker_nodes'])
        worker_node_cells = [cell['worker_nodes'] for cell in self.resource_cells if cell['worker_nodes']]
        if len({tuple(nodes) for nodes in worker_node_cells}) == 1:
            self.workload['info'] = self.workload['info']+"\nWorkers are fixed to {}.".format(
                ", ".join(worker_node_cells[0]))
        elif worker_node_cells:
            self.workload['info'] = self.workload['info']+"\nWorkers are fixed per configuration: {}.".format(
                "; ".join("{}: {}".format(number, ", ".join(cell['worker_nodes'] or ['not fixed']))
                          for number, cell in enumerate(self.resource_cells, start=1)))
        # fix pooling
        if request_node_pooling:
            self.set_resources(
                nodeSelector_pool = {
                    'kubernetes.io/hostname': request_node_pooling
                })
            self.workload['info'] = self.workload['info']+"\nPooling is fixed to {}.".format(request_node_pooling)
        if numRun > 1:
            self.workload['info'] = self.workload['info']+"\nEach query is repeated {} times.".format(numRun)
        if skip_loading:
            self.workload['info'] = self.workload['info']+"\nLoading is skipped."
        if len({(cell['cpu'], cell['cpu_limit'], cell['memory'], cell['memory_limit']) for cell in self.resource_cells}) > 1:
            self.workload['info'] = self.workload['info']+"\nResources are swept across {} configurations per DBMS: {}.".format(
                len(self.resource_cells), "; ".join(
                    "{}: CPU {}/{}, RAM {}/{}".format(
                        number, cell['cpu'], cell['cpu_limit'], cell['memory'], cell['memory_limit'])
                    for number, cell in enumerate(self.resource_cells, start=1)))
        if len(self.storage_types) > 1:
            self.workload['info'] = self.workload['info']+"\nStorage is swept across configurations: {}, size {}.".format(
                ", ".join(storage_type or "ephemeral" for storage_type in self.storage_types), request_storage_size or "unset")
            if request_storage_remove_per_repetition:
                self.workload['info'] = self.workload['info']+" Persistent storage is removed before every repetition."
            elif request_storage_remove:
                self.workload['info'] = self.workload['info']+" Persistent storage is removed at experiment start."
        elif request_storage_type and request_storage_size:
            self.workload['info'] = self.workload['info']+"\nDatabase is persisted to disk of type {} and size {}.".format(request_storage_type, request_storage_size)
            if request_storage_remove_per_repetition:
                self.workload['info'] = self.workload['info']+" Persistent storage is removed before every repetition."
            elif request_storage_remove:
                self.workload['info'] = self.workload['info']+" Persistent storage is removed at experiment start."
        elif request_storage_size and request_storage_type is None:
            self.workload['info'] = self.workload['info']+"\nDatabase uses ephemeral storage of size {}.".format(request_storage_size)
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nLoading is tested with {} threads, split into {} pods.".format(num_loading_threads, num_loading_pods)
        if self.benchmarking_is_active():
            self.workload['info'] = self.workload['info']+"\nBenchmarking is tested with {} threads, split into {} pods.".format(num_benchmarking_threads, num_benchmarking_pods)
        if len(num_pooling_pods) > 0 and  len(num_pooling_in) > 0 and len(num_pooling_out) > 0:
            self.workload['info'] = self.workload['info']+"\nPooling is done with {} pods having {} inbound and {} outbound connections in total.".format(num_pooling_pods, num_pooling_in, num_pooling_out)
        if self.benchmarking_is_active():
            self.workload['info'] = self.workload['info']+"\nBenchmarking is run as {} times the number of benchmarking pods.".format(list_clients)
        if multi_tenant_num > 0:
            self.workload['info'] = self.workload['info']+"\nNumber of tenants is {}, one {} per tenant.".format(multi_tenant_num, multi_tenant_by)
            if self.multi_tenant_volume:
                self.workload['info'] = self.workload['info']+" Each tenant has a dedicated volume."
        if num_experiment_to_apply > 1: 
            self.workload['info'] = self.workload['info']+"\nExperiment is run {} times.".format(num_experiment_to_apply)
        else:
            self.workload['info'] = self.workload['info']+"\nExperiment is run once."
        if self.max_sut is not None:
            self.workload['info'] = self.workload['info']+"\nMaximum DBMS per experiment is {}.".format(self.max_sut)
        if self.cluster.max_sut is not None:
            self.workload['info'] = self.workload['info']+"\nMaximum DBMS across the whole cluster is {}.".format(self.cluster.max_sut)
        if self.max_experiment_minutes is not None:
            self.workload['info'] = self.workload['info']+"\nExperiment is aborted and removed from the cluster after {} minutes.".format(self.max_experiment_minutes)
        if self.max_loading_minutes is not None:
            self.workload['info'] = self.workload['info']+"\nEach configuration has a loading timeout of {} minutes; diagnostics are captured before teardown.".format(self.max_loading_minutes)
        if self.keep_sut:
            self.workload['info'] = self.workload['info']+"\nThe SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot."
        elif mode == 'load':
            self.workload['info'] = self.workload['info']+"\nSUT pods are stopped after loading."
        if test_result:
            self.workload['info'] = self.workload['info']+"\nResults are validated against basic correctness requirements."
        if len(self.dbms_args) > 0:
            self.workload['info'] = self.workload['info']+"\nDeployment parameter overrides: {}.".format(self.dbms_args)
        if num_worker > 0:
            self.workload['info'] = self.workload['info']+"\nDistributed DBMS uses {} worker nodes, {} replicas and {} shards per node.".format(num_worker, num_worker_replicas, num_worker_shards)
        self.workload['info'] = self.workload['info']+"\nSUT requests {} CPU and {} RAM.".format(cpu, memory)
        if cpu_limit != '0':
            self.workload['info'] = self.workload['info']+" CPU limit is {}.".format(cpu_limit)
        if memory_limit != '0':
            self.workload['info'] = self.workload['info']+" RAM limit is {}.".format(memory_limit)
        if cpu_type:
            self.workload['info'] = self.workload['info']+"\nSUT node must carry label cpu={}.".format(cpu_type)
        if gpu_type:
            self.workload['info'] = self.workload['info']+"\nSUT requests {} GPU(s) on a node labeled gpu={}.".format(gpus, gpu_type)
        self.workload['benchmarking_active'] = self.benchmarking_is_active()
        self.workload['loading_active'] = self.loading_is_active()
    def generate_port_forward(self, service: str) -> str:
        """
        Generate a ``kubectl port-forward`` command string for a given service.

        :param service: Name of the Kubernetes service to forward.
        :return: Shell command string that forwards the cluster port to localhost.
        """
        context = self.cluster.context
        port = self.cluster.port
        app = self.appname
        forward = ['kubectl', '--context {context}'.format(context=context), 'port-forward', 'service/'+service, f"{port}:{port}"]
        command = " ".join(forward)
        #print("{:30s}: {}".format(configuration, command))
        return command
    def get_dashboard_pod(self,
                          pod_dashboard: str = '') -> str:
        """
        Get name of dashboard pod.
        This also checks the status. Waits until available.
        If name of dashboard pod is known: do nothing

        :param pod_dashboard: Optional name of dashboard pod
        """
        self.cluster.logger.debug('testbed.get_dashboard_pod()')
        # download results
        if len(pod_dashboard) == 0:
            pod_dashboard = self.cluster.get_dashboard_pod_name(component='dashboard')
            if len(pod_dashboard) > 0:
                #pod_dashboard = pods[0]
                status = self.cluster.get_pod_status(pod_dashboard)
                self.cluster.logger.debug(pod_dashboard+status)
                while status != "Running":
                    self.wait(10)
                    status = self.cluster.get_pod_status(pod_dashboard)
                    self.cluster.logger.debug(pod_dashboard+status)
        return pod_dashboard
    def test_results(self) -> None:
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('base.test_results()')
        self.evaluator.test_results()
        # not yet implemented in detail for dbmsbenchmarker:
        #workflow = self.get_workflow_list()
        #if workflow == self.evaluator.workflow:
        #    print("Result workflow complete")
        #else:
        #    print("Result workflow not complete")
    def wait(self,
             sec: int,
             silent: bool = False) -> None:
        """
        Wait for a given number of seconds, optionally without printing.

        :param sec: Number of seconds to wait.
        :param silent: If True, suppress output during the wait.
        """
        #+print("Waiting "+str(sec)+"s...", end="", flush=True)
        #intervals = int(sec)
        #time.sleep(intervals)
        #print("done")
        if sec > 0:
            return self.cluster.wait(sec, silent)
    def set_queryfile(self,
                      queryfile: str) -> None:
        """
        Set the name of the query config file used by the benchmarker component.

        :param queryfile: Filename of the dbmsbenchmarker query config (e.g. ``queries.config``).
        """
        self.queryfile = queryfile
    def set_experiments_configfolder(self,
                                     experiments_configfolder: str) -> None:
        """
        Set the relative config folder for the experiment type.

        Bexhoma expects subfolders per experiment type (e.g. ``experiments/tpch``).
        Each subfolder must contain a ``queries.config`` and per-DBMS schema subdirectories.

        :param experiments_configfolder: Relative path to the experiment config folder.
        """
        self.experiments_configfolder = experiments_configfolder
    def set_additional_labels(self,
                              **kwargs) -> None:
        """
        Sets additional labels, that will be put to K8s objects (and ignored otherwise).
        This is for the SUT component.
        Can be overwritten by configuration.

        :param kwargs: Dict of labels, example 'SF' => 100
        """
        self.additional_labels = {**self.additional_labels, **kwargs}
    def set_workload(self,
                     **kwargs) -> None:
        """
        Sets mata data about the experiment, for example name and description.

        :param kwargs: Dict of meta data, example 'name' => 'TPC-H'
        """
        self.workload = {**self.workload, **kwargs}
    def set_query_management(self,
                             **kwargs) -> None:
        """
        Sets query management data for the experiment.
        This is for the benchmarker component (dbmsbenchmarker).

        :param kwargs: Dict of meta data, example 'numRun' => 3
        """
        self.query_management = kwargs
    # the following can be overwritten by configuration
    def set_connection_management(self,
                                  **kwargs) -> None:
        """
        Sets connection management data for the experiment.
        This is for the benchmarker component (dbmsbenchmarker).
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'timout' => 60
        """
        self.connection_management = kwargs
    def set_resources(self,
                      **kwargs) -> None:
        """
        Sets resources for the experiment.
        This is for the SUT component.
        Can be overwritten by experiment and configuration.

        :param kwargs: Dict of meta data, example 'requests' => {'cpu' => 4}
        """
        self.resources = {**self.resources, **kwargs}
    def set_ddl_parameters(self,
                           **kwargs) -> None:
        """
        Sets DDL parameters for the experiments.
        This substitutes placeholders in DDL script.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'index' => 'btree'
        """
        self.ddl_parameters = kwargs
    def set_eval_parameters(self,
                            **kwargs) -> None:
        """
        Sets some arbitrary parameters that are supposed to be handed over to the benchmarker component.
        These are for evaluation purposes only.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'type' => 'noindex'
        """
        self.eval_parameters = kwargs
    def set_storage(self,
                    **kwargs) -> None:
        """
        Sets parameters for the storage that might be attached to components.
        This is in particular for the database of dbms under test.
        Example:

        `storageClassName = 'ssd',
        storageSize = '100Gi',
        keep = False`

        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'storageSize' => '100Gi'
        """
        self.storage = kwargs
    def set_nodes(self,
                  **kwargs) -> None:
        """
        Sets parameters for nodes for the components of an experiment.
        Will be used for nodeSelector.
        Example:

        sut = 'sut',
        loading = 'auxiliary',
        monitoring = 'auxiliary',
        benchmarking = 'auxiliary',

        Can be overwritten by configuration.

        :param kwargs: Dict of node infos, example 'sut' => 'sut',
        """
        self.nodes = kwargs
    def set_sut_parameters(self,
                               **kwargs) -> None:
        """
        Sets ENV for sut and worker components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.sut_parameters = kwargs
    def set_loading_parameters(self,
                               **kwargs) -> None:
        """
        Sets ENV for loading components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.loading_parameters = kwargs
    def patch_loading(self,
                        patch: str) -> None:
        """
        Patches YAML of loading components.
        Can be overwritten by configuration.

        :param patch: String in YAML format, overwrites basic YAML file content
        """
        self.loading_patch = patch
    def patch_benchmarking(self,
                           patch: str) -> None:
        """
        Patches YAML of loading components.
        Can be set by experiment before creation of configuration.

        :param patch: String in YAML format, overwrites basic YAML file content
        """
        self.benchmarking_patch = patch
    def set_loading(self,
                    parallel: int,
                    num_pods: Optional[int] = None) -> None:
        """
        Sets job parameters for loading components: Number of parallel pods and optionally (if different) total number of pods.
        By default total number of pods is set to number of parallel pods.
        Can be overwritten by configuration.

        :param parallel: Number of parallel pods
        :param num_pods: Optionally (if different) total number of pods
        """
        self.num_loading = int(parallel)
        if num_pods is not None:
            self.num_loading_pods = int(num_pods)
        else:
            self.num_loading_pods = int(parallel)
        # total number at least number of parallel
        if self.num_loading_pods < self.num_loading:
            self.num_loading_pods = self.num_loading
    def set_benchmarking_parameters(self,
                                    **kwargs) -> None:
        """
        Sets ENV for benchmarking components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.benchmarking_parameters = kwargs
    def set_default_loading_parameters(self, **kwargs) -> None:
        """
        Sets experiment-wide default ENV for loading components.

        These defaults are merged into every per-configuration loading parameter
        dict before per-configuration kwargs are applied (per-configuration values win).

        :param kwargs: Default ENV vars shared across all configurations of this experiment.
        """
        self.default_loading_parameters = kwargs
    def set_default_benchmarking_parameters(self, **kwargs) -> None:
        """
        Sets experiment-wide default ENV for benchmarking components.

        These defaults are merged into every per-configuration benchmarking parameter
        dict before per-configuration kwargs are applied (per-configuration values win).

        :param kwargs: Default ENV vars shared across all configurations of this experiment.
        """
        self.default_benchmarking_parameters = kwargs
    def add_configuration(self,
                          configuration: object) -> None:
        """
        Adds a configuration object to the list of configurations of this experiment.
        When a new configuration object is instanciated, an experiment object has to be provided.
        This method is then called automatically.

        :param configuration: Configuration object
        """
        self.configurations.append(configuration)

    def expand_resource_cells(self) -> None:
        """
        Turn every configuration into one configuration per resource cell.

        Entry scripts build each DBMS once; when ``-rc/-lc/-rr/-lr/-rst``
        carry comma lists (see :func:`bexhoma.cli_args.resource_cells`), this
        clones each configuration per cell, so every DBMS of every workload is
        swept the same way. Each cell gets its own identity, so cells never
        share pods or a PVC:

        * name ``{docker}-{cell}`` (``PostgreSQL-1``, ``PostgreSQL-2``, ...)
          when the DBMS has one configuration, ``{configuration}-{cell}`` when
          it has several (e.g. a loading-pods sweep or one per tenant);
        * alias ``{docker}@{cell}`` or ``{configuration}@{cell}`` likewise;
        * storage ``{storageConfiguration}-{cell}`` on the cell's class; the
          volume name gets the class appended when the volume is named
          (``SutConfiguration.get_storage_configuration()``).

        A configuration whose SUT bexhoma does not manage (``resource_sweep``
        false, or a fixed ``sut_service_name``) is kept once with the
        experiment-wide default, the first cell. Called by :meth:`process`;
        a second call does nothing.
        """
        cells = self.resource_cells
        if len(cells) <= 1 or getattr(self, '_resource_cells_expanded', False):
            return
        self._resource_cells_expanded = True

        def sweeps(config):
            return config.resource_sweep and not config.sut_service_name

        originals = list(self.configurations)
        per_docker = Counter(config.docker for config in originals if sweeps(config))
        self.configurations = []
        for config in originals:
            if not sweeps(config):
                print("{:30s}: SUT is not managed by bexhoma, not swept across resources".format(config.configuration))
                self.configurations.append(config)
                continue
            base_name = config.docker if per_docker[config.docker] == 1 else config.configuration
            base_storage = config.storage.get('storageConfiguration') or config.configuration
            # clone the untouched original before the first cell changes it;
            # the experiment (and the cluster behind it) stays shared
            clones = [config] + [copy.deepcopy(config, memo={id(self): self}) for _ in cells[1:]]
            for cell_number, (cell, clone) in enumerate(zip(cells, clones), start=1):
                clone.configuration = f'{base_name}-{cell_number}'
                clone.alias = f'{base_name}@{cell_number}'
                clone.set_resources(
                    requests = {'cpu': cell['cpu'], 'memory': cell['memory'], 'gpu': 0},
                    limits = {'cpu': cell['cpu_limit'], 'memory': cell['memory_limit']},
                    nodes_worker = cell.get('worker_nodes'),
                    )
                set_cell_storage(clone, f'{base_storage}-{cell_number}', cell)
                self.configurations.append(clone)

    def add_benchmark(self, benchmark) -> None:
        """
        Register a benchmark and create its evaluator.

        Assigns a 1-based ``benchmark_index``, instantiates the evaluator, wires
        ``evaluator.experiment`` back to this experiment, and sets ``self.evaluator``
        to the first registered benchmark's evaluator for backward-compat.

        :param benchmark: :class:`~bexhoma.benchmarks.base.Benchmark` instance.
        """
        benchmark.benchmark_index = len(self.benchmarks) + 1
        self.benchmarks.append(benchmark)
        benchmark.evaluator = benchmark.create_evaluator(
            self.code, self.cluster.resultfolder, benchmark.benchmark_index)
        benchmark.evaluator.experiment = self
        self.evaluators[benchmark.name] = benchmark.evaluator
        if len(self.benchmarks) == 1:
            self.evaluator = benchmark.evaluator
    def set_querymanagement_quicktest(self,
                                      numRun: int = 1,
                                      datatransfer: bool = False) -> None:
        """
        Sets some parameters that are supposed to be suitable for a quick functional test:

        * small number of runs
        * no delay
        * optional data transfer
        * no monitoring

        :param numRun: Number of runs per query (this is for the benchmarker component)
        :param datatransfer: If data should we retrieved and compared
        """
        self.set_query_management(
            numWarmup = 0,
            numCooldown = 0,
            numRun = numRun,
            delay = 0,
            timer = {
                'connection':
                {
                    'active': True,
                    'delay': 0
                },
                'datatransfer':
                {
                    'active': datatransfer,
                    'sorted': True,
                    'compare': 'result',
                    'store': 'dataframe',
                    'precision': 0,
                }
            })
        self.monitoring_active = False
    def set_monitoring_metric_overrides(self, overrides: dict, monitoring_enabled: bool = True) -> None:
        """
        Switch single cluster-wide hardware metrics on or off for this experiment (``-mm``).

        Checked against ``cluster.config``'s ``monitor.metrics`` before anything
        is deployed, so a typo or a renamed metric stops the run instead of
        being silently ignored. :class:`~bexhoma.configurations.metrics.MetricsCollector`
        applies the overrides when it copies the metric definitions into each
        connection.

        :param overrides: Requested ``active`` flag per metric key.
        :param monitoring_enabled: Whether ``-m`` or ``-mc`` is set; overrides
            without monitoring would have no effect.
        :raises ValueError: On an unknown key, a required metric switched off,
            or overrides without monitoring.
        """
        from bexhoma.environment import REQUIRED_HARDWARE_METRICS
        if not overrides:
            self.monitoring_metric_overrides = {}
            return
        if not monitoring_enabled:
            raise ValueError("--monitoring-metrics needs --monitoring (-m) or --monitoring-cluster (-mc)")
        known = self.cluster.config['credentials']['k8s'].get('monitor', {}).get('metrics', {})
        unknown = sorted(set(overrides) - set(known))
        if unknown:
            raise ValueError(
                f"--monitoring-metrics names metrics that cluster.config does not define: {unknown}. "
                f"Defined: {sorted(known)}")
        switched_off = sorted(key for key, active in overrides.items()
                              if not active and key in REQUIRED_HARDWARE_METRICS)
        if switched_off:
            raise ValueError(
                f"--monitoring-metrics cannot switch off required metrics: {switched_off}")
        self.monitoring_metric_overrides = dict(overrides)
    def set_querymanagement_monitoring(self,
            numRun: int = 256,
            delay: int = 10,
            datatransfer: bool = False) -> None:
        """
        Sets some parameters that are supposed to be suitable for a monitoring test:

        * high number of runs
        * optional delay
        * optional data transfer
        * monitoring active

        :param numRun: Number of runs per query (this is for the benchmarker component)
        :param delay: Number of seconds to wait between queries (this is for the benchmarker component)
        :param datatransfer: If data should we retrieved and compared
        """
        self.set_query_management(
            numWarmup = 0,
            numCooldown = 0,
            numRun = numRun,
            delay = 0,
            timer = {
                'connection':
                {
                    'active': True,
                    'delay': delay
                },
                'datatransfer':
                {
                    'active': datatransfer,
                    'sorted': True,
                    'compare': 'result',
                    'store': [],
                    'precision': 0,
                }
            })
        self.monitoring_active = True
    def zip(self):
        """
        Zip the result folder in the dashboard pod.
        """
        # remote:
        pod_dashboard = self.cluster.get_dashboard_pod_name(component='dashboard')
        if len(pod_dashboard) > 0:
            #pod_dashboard = pods[0]
            status = self.cluster.get_pod_status(pod_dashboard)
            print(pod_dashboard, status)
            while status != "Running":
                self.wait(10)
                status = self.cluster.get_pod_status(pod_dashboard)
                print(pod_dashboard, status)
            cmd = {}
            # only zip first level
            #cmd['zip_results'] = 'cd /results;zip {code}.zip {code}/*'.format(code=self.code)
            # zip complete folder
            cmd['zip_results'] = 'cd /results;zip -r {code}.zip {code}'.format(code=self.code)
            # include sub directories
            #cmd['zip_results'] = 'cd /results;zip -r {code}.zip {code}'.format(code=self.code)
            #fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['zip_results'].replace('"','\\"')+'"'
            self.cluster.execute_command_in_pod(command=cmd['zip_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
            #print(fullcommand)
            #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            #stdout, stderr = proc.communicate()
        # local:
        #shutil.make_archive(self.cluster.resultfolder+"/"+str(self.cluster.code), 'zip', self.cluster.resultfolder, str(self.cluster.code))
    def set_experiment(self,
                       instance=None,
                       volume=None,
                       docker=None,
                       script=None,
                       indexing=None):
        """
        Read experiment details from cluster config

        :param instance: 
        :param volume: 
        :param docker: 
        :param script: 
        """
        #self.bChangeInstance = True
        #if instance is not None:
        #    self.i = instance
        if volume is not None:
            self.volume = volume
            self.volumeid = self.cluster.volumes[self.volume]['id']
        #if docker is not None:
        #    self.d = docker
        #    self.docker = self.cluster.dockers[self.d]
        if script is not None:
            self.script = script
            self.initscript = self.cluster.volumes[self.volume]['initscripts'][self.script]
        if indexing is not None:
            self.indexing = indexing
            self.indexscript = self.cluster.volumes[self.volume]['initscripts'][self.indexing]
    def evaluate_results(self,
                         pod_dashboard: str = '') -> None:
        """
        Let the dashboard pod build the evaluations.
        """
        self.cluster.logger.debug('base.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        self.workload['workflow_errors'] = self.evaluator.workflow_errors
        if len(pod_dashboard) == 0:
            pod_dashboard = self.get_dashboard_pod()
        if self.monitoring_active:
            # fixed phases plus every SUT/cluster/app component registered during the run
            component_types = ['loading', 'benchmarking', 'loader', 'benchmarker'] + list(self.workload['monitoring_components'])
            for component_type in component_types:
                print("{:30s}: transforming metrics for {}".format("Experiment", component_type))
                cmd = 'python metrics.evaluation.py -r /results/ -db -ct {} -e {}'.format(component_type, self.code)
                _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd, pod=pod_dashboard, container="dashboard")
                self.cluster.logger.debug(stdout)
                print("{:30s}: transforming metrics for {} completed".format("Experiment", component_type))
        # download evaluation cubes
        print("{:30s}: downloading partial results".format("Experiment"))
        self.download_experiment_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.upload_experiment_file(filename='')
    def stop_loading(self):
        """
        Stop all loading jobs of this experiment.
        If a list of dbms configurations is set, use it.
        Otherwise tell the cluster to stop all loading jobs belonging to this experiment code.
        """
        if len(self.configurations) > 0:
            for config in self.configurations:
                config.lifecycle.stop_loading()
        else:
            app = self.cluster.appname
            component = 'loading'
            configuration = ''
            jobs = self.cluster.get_jobs(app=app, component=component, experiment=self.code, configuration=configuration)
            for job in jobs:
                self.cluster.delete_job(job)
            # all pods to these jobs
            #self.cluster.get_job_pods(app, component, self.code, configuration)
            pods = self.cluster.get_job_pods(app, component, self.code, configuration)
            for p in pods:
                status = self.cluster.get_pod_status(p)
                print(p, status)
                self.cluster.delete_pod(p)
    def stop_monitoring(self):
        """
        Stop all monitoring deployments of this experiment.
        If a list of dbms configurations is set, use it.
        Otherwise tell the cluster to stop all monitoring deployments belonging to this experiment code.
        """
        if len(self.configurations) > 0:
            for config in self.configurations:
                config.lifecycle.stop_monitoring()
        else:
            app = self.cluster.appname
            component = 'monitoring'
            configuration = ''
            deployments = self.cluster.get_deployments(app=app, component=component, experiment=self.code, configuration=configuration)
            for deployment in deployments:
                self.cluster.delete_deployment(deployment)
    def stop_benchmarker(self,
                         configuration: str = '') -> None:
        """
        Stop all benchmarker jobs of this experiment.
        If a dbms configurations is given, use it.
        Otherwise tell the cluster to stop all benchmarker jobs belonging to this experiment code.
        """
        # all jobs of configuration - benchmarker
        self.cluster.logger.debug("experiment.stop_benchmarker({})".format(configuration))
        app = self.appname
        component = 'benchmarker'
        jobs = self.cluster.get_jobs(app, component, self.code, configuration)
        # status per job
        for job in jobs:
            success = self.cluster.get_job_status(job)
            print(job, success)
            self.cluster.delete_job(job)
        # all pods to these jobs
        #self.cluster.get_job_pods(app, component, self.code, configuration)
        pods = self.cluster.get_job_pods(app, component, self.code, configuration)
        for p in pods:
            status = self.cluster.get_pod_status(p)
            print(p, status)
            self.cluster.delete_pod(p)
    def remove_experiment(self) -> None:
        """
        Stop every component of this experiment and remove it from the cluster.

        Calls all per-component ``stop_*`` methods and then deletes any
        remaining Kubernetes objects labeled with this experiment's code,
        mirroring the teardown of ``bexhoma-experiments stop -e <code>``.
        """
        self.stop_benchmarker()
        self.stop_loading()
        self.stop_monitoring()
        self.stop_sut()
        self.cluster.kubectl('delete all -l experiment='+self.code)
        # "all" does not include Secrets (TLS material of the SUTs, see bexhoma.tls)
        self.cluster.kubectl('delete secret -l experiment='+self.code+',component='+TLS_COMPONENT)
    def start_monitoring(self):
        """
        Start monitoring for all dbms configurations of this experiment.
        """
        for config in self.configurations:
            config.lifecycle.start_monitoring()
    def start_sut(self):
        """
        Start all dbms configurations of this experiment.
        """
        for config in self.configurations:
            config.lifecycle.start_sut()
    def stop_sut(self):
        """
        Stop all SUT deployments of this experiment.
        If a list of dbms configurations is set, use it.
        Otherwise tell the cluster to stop all monitoring deployments belonging to this experiment code.
        """
        if len(self.configurations) > 0:
            for config in self.configurations:
                config.lifecycle.stop_sut()
        else:
            app = self.cluster.appname
            component = 'sut'
            configuration = ''
            deployments = self.cluster.get_deployments(app=app, component=component, experiment=self.code, configuration=configuration)
            for deployment in deployments:
                self.cluster.delete_deployment(deployment)
    def start_loading(self):
        """
        Tells all dbms configurations of this experiment to start loading data.
        """
        for config in self.configurations:
            config.loader.start_exec()
    def add_benchmark_list(self,
                           list_clients: list) -> None:
        """
        Add a list of (number of) benchmarker instances, that are to benchmark the current SUT.
        Example `[1,2,1]` means sequentially we will have 1, then 2 and then 1 benchmarker instances.
        This is applied to all dbms configurations of the experiment.

        :param list_clients: List of (number of) benchmarker instances
        """
        for config in self.configurations:
            config.add_benchmark_list(list_clients)
    def get_workflow_list(self):
        """
        Returns the planned benchmarking workflow extracted from ``experiment_dict``.

        The workflow is a dict keyed by configuration name.  Each value is a list of
        experiment runs (length ``num_experiment_to_apply``), where each run is a list
        of client rounds, and each client round is a list of job descriptors::

            {
                'PostgreSQL-1-1-1': [
                    [  # experiment run 1
                        [  # client round 1
                            {'type': 'tpch',         'pods': 3},
                            {'type': 'tpch_refresh', 'pods': 1},
                        ],
                    ],
                ],
            }

        When ``workflow_planned`` is already present in ``self.workload`` (e.g. because
        ``store_workflow_results()`` was already called), that stored value is returned
        unchanged to preserve idempotency.

        :return: Dict mapping configuration name to the nested workflow structure.
        :rtype: dict
        """
        if 'workflow_planned' in self.workload:
            return self.workload['workflow_planned']
        workflow = {}
        for configuration in self.configurations:
            rounds = [
                [
                    {
                        'type': entry['name'],
                        'pods': entry['parallelism'],
                    }
                    for entry in round_entries
                ]
                for round_entries in configuration.experiment_dict['benchmarker']
            ]
            workflow[configuration.configuration] = [
                rounds for _ in range(configuration.num_experiment_to_apply)
            ]
        self.cluster.logger.debug('base.get_workflow_list({})'.format(workflow))
        return workflow
    def store_workflow_results(self):
        """
        Constructs a list of runs for the planned workflow.
        Stores this information in self.workload['workflow_planned'].
        Updates query.config locally and remotely via update_workload().

        When the experiment has registered :class:`~bexhoma.benchmarks.base.Benchmark`
        objects (via :meth:`~bexhoma.experiments.mixed.mixed.add_benchmark`), the
        ordered benchmark type sequence is written to ``self.workload['benchmark_sequence']``
        so that collectors can later reconstruct the benchmark-run → tool-type mapping
        from ``queries.config``.
        """
        if hasattr(self, 'benchmarks') and self.benchmarks:
            self.workload['benchmark_sequence'] = [
                {'index': bm.benchmark_index, 'type': bm.name}
                for bm in self.benchmarks
            ]
        workflow = self.get_workflow_list()
        self.workload['workflow_planned'] = workflow
        self.update_workload()
    def test_workflow(self,
                      workflow_1: dict,
                      workflow_2: dict) -> bool:
        """
        Compares two workflow dicts for equality.

        Each workflow maps a configuration name to a list of experiment runs,
        where each run is a list of client rounds, and each round is a list of
        job descriptors ``{'type': str, 'pods': int}``.

        The comparison is order-sensitive across experiment runs and client rounds
        (their sequence matters) but order-insensitive within a single client round
        (parallel jobs may be scheduled in any order).

        :param workflow_1: First workflow dict.
        :type workflow_1: dict
        :param workflow_2: Second workflow dict.
        :type workflow_2: dict
        :return: ``True`` if the two workflows are equivalent.
        :rtype: bool
        """
        if workflow_1.keys() != workflow_2.keys():
            return False
        sort_key = lambda job: (job['type'], job['pods'])
        for key in workflow_1:
            runs_1, runs_2 = workflow_1[key], workflow_2[key]
            if len(runs_1) != len(runs_2):
                return False
            for round_list_1, round_list_2 in zip(runs_1, runs_2):
                if len(round_list_1) != len(round_list_2):
                    return False
                for jobs_1, jobs_2 in zip(round_list_1, round_list_2):
                    if sorted(jobs_1, key=sort_key) != sorted(jobs_2, key=sort_key):
                        return False
        return True
    def _record_test(self, passed: bool, label: str) -> bool:
        """
        Append a test result to the internal collector and return the passed flag.

        Coerces ``passed`` to a native ``bool`` before storing: callers sometimes
        pass a ``numpy.bool_`` (e.g. from a pandas ``==`` comparison), and
        ``report_writer.py``'s frontmatter counters use ``is True``/``is False``
        identity checks that silently ignore anything that is not a native bool.

        :param passed: Whether the test passed.
        :type passed: bool
        :param label: Human-readable description of what was tested.
        :type label: str
        :return: The value of passed, allowing inline chaining.
        :rtype: bool
        """
        passed = bool(passed)
        self._test_results.append((passed, label))
        return passed
    def _record_skipped_test(self, label: str) -> None:
        """
        Append a skipped-test entry to the internal collector.

        Use when a test is intentionally not run (e.g. data pre-existing).

        :param label: Human-readable description of what was skipped.
        :type label: str
        """
        self._test_results.append((None, label))
    def _show_loading_provenance(self, connections_sorted: list) -> None:
        """
        Print which configurations did not load in this experiment, and record the loading test.

        A volume found already loaded at experiment start skips loading and
        inherits its loading times from whichever experiment filled it. That
        reuse is deliberate (the volume was not removed), so the test
        ``Loading measured in this experiment`` is skipped, not failed; its
        reason names the configurations whose loading times are inherited.
        Results written before ``storage_reused`` was recorded record nothing.
        A repetition that found the volume of an earlier repetition loaded
        (without ``-rsrp``) is listed too, informational only.

        :param connections_sorted: Connection dicts of ``connections.config``.
        """
        recorded = [c for c in connections_sorted if 'storage_reused' in c]
        if recorded:
            reused = sorted({c.get('configuration', c['name']) for c in recorded if c['storage_reused']})
            if reused:
                print("\n### Reused Storage")
                print("* loading skipped, loading times inherited from an earlier experiment: {}".format(", ".join(reused)))
                self._record_skipped_test("Loading measured in this experiment (storage reused, loading times inherited: {})".format(", ".join(reused)))
            else:
                self._record_test(True, "Loading measured in this experiment")
        # its loading times are copies, so they are no further sample of loading
        inherited = sorted({
            "{}-{}".format(c.get('configuration', c['name']), c.get('parameter', {}).get('numExperiment', '?'))
            for c in connections_sorted
            if c.get('loading_inherited') and not c.get('storage_reused')})
        if inherited:
            print("\n### Inherited Loading")
            print("* loading skipped, loading times copied from an earlier repetition: {}".format(", ".join(inherited)))
    def _test_column(self, df, column: str, title: str = '') -> bool:
        """
        Call evaluator.test_results_column and record the result.

        :param df: DataFrame to check.
        :param column: Column name to inspect for zero or NaN values.
        :type column: str
        :param title: Optional prefix prepended to the column name in the label.
        :type title: str
        :return: True if the column contains no zero or NaN values.
        :rtype: bool
        """
        passed = self.evaluator.test_results_column(df, column)
        full_title = f"{title} {column}" if len(title) > 0 else column
        suffix = "contains no 0 or NaN" if passed else "contains 0 or NaN"
        return self._record_test(passed, f"{full_title} {suffix}")
    def _print_test_summary(self) -> None:
        """Print all results collected in _test_results as a single summary block."""
        print("\n### Tests")
        for passed, label in self._test_results:
            if passed is None:
                status = "skipped"
            elif passed:
                status = "passed"
            else:
                status = "failed"
            print(f"* TEST {status}: {label}")
    def update_workload(self):
        """
        Updates query.config locally and remotely via dashboard pod.
        """
        if len(self.configurations) > 0:
            # there is a configuration, i.e., also a query.config file
            if len(self.workload) > 0:
                #configuration = self.configurations[0]
                # write appended query config
                filename = self.result_filename_local("queries.config")#self.path+"/queries.config"
                # queries.config is only written once run_pod() submits the first
                # benchmarker job; it may not exist yet if the experiment was aborted
                # (e.g. --experiment-timeout) during loading or before the first round.
                if os.path.isfile(filename):
                    with open(filename,'r') as inp:
                        queryconfig = ast.literal_eval(inp.read())
                        for k,v in self.workload.items():
                            queryconfig[k] = v
                    #filename = self.benchmark.path+'/queries.config'
                    # atomic write: see matching comment in
                    # configurations/benchmarking.py::BenchmarkRunner.run_pod()
                    tmp_filename = filename + '.tmp'
                    with open(tmp_filename, 'w') as outp:
                        outp.write(str(queryconfig))
                    os.replace(tmp_filename, filename)
        filename = 'queries.config'
        filename_local = self.result_filename_local(filename)
        if os.path.isfile(filename_local):
            print("{:30s}: uploading workload file".format("Experiment"))
            self.upload_experiment_file(filename=filename)

    def _loading_abort_reason(
        self,
        config: "SutConfiguration",
        now: datetime,
    ) -> Optional[str]:
        """Return why an active load must abort, or ``None`` while it may continue."""
        if not config.loading_started or config.loading_finished:
            config.loading_started_at = None
            return None

        jobs = self.cluster.get_jobs(
            app=config.appname, component='loading', experiment=config.code,
            configuration=config.configuration,
        ) or []
        for job in jobs:
            if self.cluster.get_job_failed(job):
                return (
                    f"Loading job {job} for {config.configuration} reached "
                    "Kubernetes' terminal Failed condition"
                )

        if config.loading_started_at is None:
            config.loading_started_at = now
        if self.max_loading_minutes is None:
            return None
        elapsed_seconds = (now - config.loading_started_at).total_seconds()
        if elapsed_seconds >= self.max_loading_minutes * SECONDS_PER_MINUTE:
            return (
                f"Loading for {config.configuration} exceeded its "
                f"{self.max_loading_minutes} minute timeout"
            )
        return None

    def _abort_loading_if_needed(
        self,
        config: "SutConfiguration",
        now: datetime,
    ) -> bool:
        """Capture diagnostics and remove the experiment when loading must abort."""
        reason = self._loading_abort_reason(config, now)
        if reason is None:
            return False
        print(
            f"{'Experiment':30s}: {reason}; capturing diagnostics and "
            "removing all components"
        )
        self._runtime_test_results.append((False, reason))
        self.remove_experiment()
        return True

    def _note_image_pull_waits(self, config: "SutConfiguration") -> None:
        """Record a failed test when a loading pod of an active load waits for its image.

        The load is not aborted (the pull may still succeed), but the wait
        counts into this repetition's loading times, so they are flagged.
        Each pod is reported once.

        :param config: Configuration whose loading pods are checked.
        """
        if not config.loading_started or config.loading_finished:
            return
        pods = self.cluster.get_job_pods(
            app=config.appname, component='loading', experiment=config.code,
            configuration=config.configuration) or []
        for pod in pods:
            if pod in self._image_pull_waits_seen:
                continue
            reasons = [reason for reason in self.cluster.get_pod_waiting_reasons(pod)
                       if reason in IMAGE_PULL_WAITING_REASONS]
            if not reasons:
                continue
            self._image_pull_waits_seen.add(pod)
            reason = (f"Loading pod {pod} of {config.configuration} waits for its image "
                      f"({', '.join(sorted(set(reasons)))}); loading times of repetition "
                      f"{config.num_experiment_to_apply_done + 1} include that wait")
            print(f"{config.configuration:30s}: {reason}")
            self._runtime_test_results.append((False, reason))

    def _benchmark_start_abort_reason(
        self,
        config: "SutConfiguration",
        now: datetime,
    ) -> Optional[str]:
        """Return why a starting benchmark round must be skipped, or ``None`` while it may continue."""
        starting = self._benchmark_rounds_starting.get(config.configuration)
        if starting is None:
            return None
        round_counter_key, submitted_at = starting
        pods_missing = self.cluster.get_pod_counter(round_counter_key)
        # An unreadable counter is no evidence of a stuck round, so it never
        # triggers the skip; the round is then simply waited for as before.
        if pods_missing is None:
            return None
        if pods_missing <= 0:
            del self._benchmark_rounds_starting[config.configuration]
            return None
        elapsed_seconds = (now - submitted_at).total_seconds()
        if elapsed_seconds < BENCHMARK_START_TIMEOUT_MINUTES * SECONDS_PER_MINUTE:
            return None
        return (
            f"Benchmark round of {config.configuration} did not start within "
            f"{BENCHMARK_START_TIMEOUT_MINUTES} minutes ({pods_missing} pods still missing)"
        )

    def _skip_benchmark_round_if_not_started(
        self,
        config: "SutConfiguration",
        jobs: list[str],
        now: datetime,
    ) -> bool:
        """Capture diagnostics and delete a benchmark round whose pods did not all start in time.

        The configuration then proceeds with its next round, so the other
        rounds and systems are still measured.

        :param config: Configuration whose round is checked.
        :param jobs: Benchmarker jobs of that configuration still present.
        :param now: Current time (UTC).
        :return: ``True`` if the round was skipped.
        :rtype: bool
        """
        reason = self._benchmark_start_abort_reason(config, now)
        if reason is None:
            return False
        print(f"{config.configuration:30s}: {reason}; capturing diagnostics and skipping the round")
        self._runtime_test_results.append((False, reason))
        pods = self.cluster.get_job_pods(
            app=self.cluster.appname, component='benchmarker',
            experiment=self.code, configuration=config.configuration)
        # Descriptions of pending pods name the scheduler's reason, and the
        # job's own description lists pods it could not create.
        for job in jobs:
            self.cluster.store_job_description(job)
        for pod in pods:
            self.cluster.store_pod_description(pod_name=pod)
            if self.cluster.get_pod_status(pod) in ('Running', 'Succeeded', 'Failed'):
                for container in self.cluster.get_pod_containers(pod):
                    if container:
                        self.cluster.store_pod_log(pod, container)
        # The job goes first so that it cannot replace the pods deleted next.
        for job in jobs:
            self.cluster.delete_job(job)
            self._ended_jobs().add(job)
        for pod in pods:
            self.cluster.delete_job_pods(jobname=pod)
        del self._benchmark_rounds_starting[config.configuration]
        return True

    def _waits_for_slot(self, config) -> Optional[str]:
        """Name a configuration of this experiment that waits for the SUT slot ``config`` holds.

        It has not started its SUT yet, is not done, and a cap counts both
        SUTs: ``-mse`` (this experiment), ``-ms`` (cluster-wide), or the
        ``max_sut_dbms`` of its own DBMS when both run the same one. Keeping
        ``config``'s SUT would then make it wait forever.

        :param config: The configuration about to keep its SUT.
        :return: The waiting configuration's name, or None.
        :rtype: str or None
        """
        experiment_cap = self.max_sut is not None or self.cluster.max_sut is not None
        for other in self.configurations:
            if other is config or other.experiment_done:
                continue
            dbms_cap = other.max_sut_dbms is not None and other.docker == config.docker
            if not (experiment_cap or dbms_cap):
                continue
            # a SUT still being removed between repetitions waits for a slot too
            if getattr(other, 'sut_removing', False) or not other.status.sut_exists():
                return other.configuration
        return None

    def _prepare_next_repetition(self, config) -> None:
        """Get a configuration ready for its next repetition, without starting its SUT.

        Resets the configuration and marks its stopped SUT as being removed
        (``config.sut_removing``). The main loop does not touch the
        configuration until the SUT is gone (see :meth:`_sut_still_removing`),
        and serves the other configurations meanwhile. The SUT is then started
        by the main loop like the first one, so ``-mse``, ``-ms`` and
        ``max_sut_dbms`` are checked again: while the old SUT is removed its
        slot is free, and another experiment may take it. Starting here
        without that check would run both SUTs side by side.

        :param config: The configuration whose repetition has ended and whose SUT was stopped.
        """
        # find next sequence of benchmarks
        if not config.experiment_dict["benchmarker"]:
            config.benchmark_list = config.benchmark_list_template.copy()
            config.benchmarking_parameters_list = config.benchmarking_parameters_list_template.copy()
        self.client = 0
        config.reset_sut()
        config.sut_removing = True

    def _sut_still_removing(self, config) -> bool:
        """Whether the stopped SUT of a configuration is still being removed.

        Checked first in every pass for a configuration whose repetition ended
        (:meth:`_prepare_next_repetition`): a terminating SUT pod still has
        phase ``Running``, so the configuration must not be looked at before
        it is gone.

        :param config: Configuration to check.
        :return: True while the SUT exists; False once it is gone (the mark is
            then cleared) or if the configuration was not being removed.
        """
        if not getattr(config, 'sut_removing', False):
            return False
        if config.status.sut_exists():
            print("{:30s}: still being removed".format(config.configuration))
            return True
        print("{:30s}: starts again".format(config.configuration))
        config.sut_removing = False
        return False

    def _ended_jobs(self) -> set:
        """Names of benchmarker jobs this process has ended and deleted.

        A deleted job vanishes from the job list asynchronously. Both loops of
        :meth:`work_benchmark_list` ignore these jobs, so a job still listed
        right after its deletion is neither ended twice nor blocks the next
        round. Job names contain run, client and benchmark index, so they
        never repeat within an experiment.

        :return: The (mutable) set.
        """
        return self.__dict__.setdefault('_jobs_ended', set())

    def _store_finished_job_pod(self, job: str, pod: str) -> None:
        """Store logs of all containers and the description of a finished benchmarker pod.

        Once every file exists, the pod is remembered (see
        :func:`~bexhoma.cluster_calls.stored_pods`) and not inspected again
        in later passes. If a file is missing, the next pass tries again.

        :param job: Name of the job the pod belongs to (for the log).
        :param pod: Name of the pod (phase Succeeded or Failed).
        """
        if pod in stored_pods(self.cluster):
            return
        containers = [container for container in self.cluster.get_pod_containers(pod) if len(container) > 0]
        for container in containers:
            self.cluster.logger.debug("Store logs of job {} pod {} container {}".format(job, pod, container))
            self.cluster.store_pod_log(pod, container)
        if not self.cluster.pod_description_exists(pod_name=pod):
            self.cluster.logger.debug("Store description of job {} pod {}".format(job, pod))
            self.cluster.store_pod_description(pod_name=pod)
        if (containers
                and all(self.cluster.pod_log_exists(pod, container) is True for container in containers)
                and self.cluster.pod_description_exists(pod_name=pod) is True):
            stored_pods(self.cluster).add(pod)

    def _upload_ended_job_files(self, filenames: list) -> None:
        """Upload the files written by :meth:`end_benchmarking` for the jobs of one pass.

        One upload for all; if that fails, file by file as before: a
        connection's own config only warns, ``connections.config`` raises.

        :param filenames: Names collected in ``pending_uploads``.
        """
        filenames = list(dict.fromkeys(filenames))
        if not filenames:
            return
        try:
            self.upload_experiment_files(filenames)
            return
        except RuntimeError as exc:
            print("{:30s}: WARNING - joint upload failed, uploading one by one: {}".format("Experiment", exc))
        for filename in filenames:
            if filename == 'connections.config':
                self.upload_experiment_file(filename=filename)
                continue
            try:
                self.upload_experiment_file(filename=filename)
            except Exception as exc:
                print("{:30s}: WARNING - could not upload {}: {}".format("Experiment", filename, exc))

    def _run_parallel_steps(self, steps: list, summary: str, count=len) -> list:
        """Run the steps of one loop pass side by side, one per configuration.

        Up to :attr:`max_parallel_steps` at once (1 = one by one, in order, as
        before); see :func:`~bexhoma.parallel_steps.run_steps`.

        :param steps: Callables without arguments.
        :param summary: Line printed when more than one unit was done, with ``{}`` for the number.
        :param count: Number of units done, from the list of results.
        :return: The results, in the order of ``steps``.
        """
        started = time.monotonic()
        calls_started = CALL_STATS.snapshot()
        results = run_steps(steps, self.max_parallel_steps)
        done = count(results)
        if done > 1:
            print("{:30s}: {} in {:.1f}s ({} at once; {})".format(
                "Experiment", summary.format(done), time.monotonic() - started,
                max(1, min(self.max_parallel_steps, len(steps))), CALL_STATS.since(calls_started)))
        return results

    def _submit_round(self, config, client_round: list, experiment_run: str, client: str,
                      round_counter_key: str, fetch_batch: MetricFetchBatch) -> None:
        """Submit the benchmarker jobs of one client round of a configuration (experiment dict path).

        Runs side by side with the rounds of other configurations; the round
        and experiment pod counters are set before (in the loop).

        :param config: The configuration.
        :param client_round: Its entries of ``experiment_dict['benchmarker']`` for this round.
        :param experiment_run: Repetition, 1-based, as string.
        :param client: Client round, 1-based, as string.
        :param round_counter_key: Redis key of the round pod counter.
        :param fetch_batch: Batch for the loading-metric fetches.
        """
        for bm_idx, bench_entry in enumerate(client_round):
            benchmark_index = bm_idx + 1
            connection = f"{config.configuration}-{experiment_run}-{client}-{benchmark_index}".lower()
            print("{:30s}: start benchmarking (benchmark_run={})".format(connection, benchmark_index))
            reset_seconds = 0
            if self.resetscript_active and bench_entry.get("resetscript"):
                reset_seconds = config.loader.exec_reset_script(
                    'reset_{}_{}_{}'.format(experiment_run, client, benchmark_index),
                    bench_entry["resetscript"])
            if bench_entry.get("parameters"):
                # Assign directly to avoid the side effect in
                # set_benchmarking_parameters() that overwrites
                # experiment_dict["benchmarker"][0], which would
                # corrupt subsequent -nc repetitions.
                config.benchmarking_parameters = bench_entry["parameters"].copy()
            config.runner.run_pod(
                connection=connection,
                configuration=config.configuration,
                client=client,
                parallelism=bench_entry["parallelism"],
                benchmark_run=str(benchmark_index),
                template_override=bench_entry.get("template", ""),
                reset_seconds=reset_seconds,
                fetch_batch=fetch_batch,
            )
        # Timed from here, not from the counter, so that reset
        # scripts run before submission do not count.
        self._benchmark_rounds_starting[config.configuration] = (round_counter_key, datetime.utcnow())

    def _submit_legacy_round(self, config, parallelism: int, benchmarking_parameters: Optional[dict],
                             experiment_run: str, client: str, round_counter_key: str,
                             fetch_batch: MetricFetchBatch) -> None:
        """Submit the benchmarker job of one round of a configuration (legacy ``benchmark_list`` path).

        :param config: The configuration.
        :param parallelism: Number of benchmarker pods.
        :param benchmarking_parameters: Parameters of this round, or None to keep the current ones.
        :param experiment_run: Repetition, 1-based, as string.
        :param client: Client round, 1-based, as string.
        :param round_counter_key: Redis key of the round pod counter.
        :param fetch_batch: Batch for the loading-metric fetches.
        """
        reset_seconds = 0
        if self.resetscript_active and config.resetscript:
            reset_seconds = config.loader.exec_reset_script(
                'reset_{}_{}'.format(experiment_run, client), config.resetscript)
        if benchmarking_parameters is not None:
            print("{:30s}: we will change parameters of benchmark as {}".format(config.configuration, benchmarking_parameters))
            config.set_benchmarking_parameters(**benchmarking_parameters)
        connection = (config.configuration+'-'+experiment_run+'-'+client).lower()
        print("{:30s}: start benchmarking".format(connection))
        config.runner.run_pod(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism, reset_seconds=reset_seconds, fetch_batch=fetch_batch)
        self._benchmark_rounds_starting[config.configuration] = (round_counter_key, datetime.utcnow())

    def _end_finished_jobs(self, config, end_batch: MetricFetchBatch, end_uploads: list) -> tuple:
        """Store the pods of a configuration's benchmarker jobs and end the jobs that succeeded.

        Runs side by side with the other configurations of the pass.

        :param config: The configuration.
        :param end_batch: Batch for the benchmarking-metric fetches.
        :param end_uploads: Collects the files to upload before ``end_batch`` runs.
        :return: ``(running, incomplete, ended)``: a job is listed, a job has
            not succeeded yet, names of the jobs ended and deleted now.
        """
        running = False
        incomplete = False
        ended = []
        app = self.cluster.appname
        component = 'benchmarker'
        configuration = config.configuration
        # jobs already ended and deleted by this process may still be listed
        jobs = [job for job in (self.cluster.get_jobs(app, component, self.code, configuration) or [])
                if job not in self._ended_jobs()]
        # all pods to these jobs
        pods = self.cluster.get_job_pods(app, component, self.code, configuration) or []
        # status per job
        for job in jobs:
            running = True
            # status per pod
            for p in pods:
                if p not in stored_pods(self.cluster) and not self.cluster.pod_log_exists(p):
                    status = self.cluster.get_pod_status(p)
                    self.cluster.logger.debug('job-pod {} has status {}'.format(p, status))
                    if status == 'Succeeded' or status == 'Failed':
                        self._store_finished_job_pod(job, p)
            success = self.cluster.get_job_status(job)
            self.cluster.logger.debug('job {} has success status {}'.format(job, success))
            if not success:
                incomplete = True
                continue
            # status per pod
            for p in pods:
                status = self.cluster.get_pod_status(p)
                self.cluster.logger.debug('job-pod {} has status {}'.format(p, status))
                if status == 'Succeeded' or status == 'Failed':
                    self._store_finished_job_pod(job, p)
                    self.cluster.delete_pod(p)
            self.end_benchmarking(job, config, fetch_batch=end_batch, pending_uploads=end_uploads)
            self.cluster.delete_job(job)
            self._ended_jobs().add(job)
            config.host.check_volumes()
            ended.append(job)
        return running, incomplete, ended

    def _follow_up_wait(self, current: int, reason: str) -> int:
        """Shorten the next wait of the main loop after a step that needs no cluster change.

        :param current: The next wait as planned so far.
        :param reason: Why, for the debug log.
        :return: The next wait: :data:`FOLLOW_UP_WAIT_SECONDS`, unless
            :data:`MAX_FOLLOW_UP_WAITS_IN_A_ROW` short waits came before.
        """
        if self.__dict__.get('_follow_up_waits_in_a_row', 0) >= MAX_FOLLOW_UP_WAITS_IN_A_ROW:
            return current
        self.cluster.logger.debug("next loop pass without waiting: {}".format(reason))
        return min(current, FOLLOW_UP_WAIT_SECONDS)

    def _leaves_sut_running(self, config, stop_after_starting: bool, stop_after_benchmarking: bool) -> bool:
        """Whether this repetition of a configuration ends with its SUT left running.

        Only the last repetition may (``-ks yes``, the default in modes load
        and start); earlier ones stop and restart the SUT like any run, so
        ``-nc`` is honoured. ``-m start`` stops before loading and never
        repeats. A SUT another configuration waits for is stopped instead of
        kept (see :meth:`_waits_for_slot`), so under a cap only the last
        configurations to finish keep theirs.

        :param config: The configuration whose repetition has run all its benchmarks.
        :param stop_after_starting: As in :meth:`work_benchmark_list`.
        :param stop_after_benchmarking: As in :meth:`work_benchmark_list`.
        :return: True to keep the SUT, False to stop it (and start the next repetition, if any).
        :rtype: bool
        """
        if not stop_after_benchmarking:
            return False
        if not stop_after_starting and config.num_experiment_to_apply_done + 1 < config.num_experiment_to_apply:
            return False
        waiting = self._waits_for_slot(config)
        if waiting is not None:
            print("{:30s}: stopped instead of kept, {} waits for its slot".format(config.configuration, waiting))
            self.workload.setdefault('sut_stopped', {})[config.configuration] = (
                f"stopped instead of kept: {waiting} waited for its slot")
            if stop_after_starting:
                # -m start never repeats: the stop below must not start it again
                config.num_experiment_to_apply_done = config.num_experiment_to_apply - 1
            return False
        return True

    def work_benchmark_list(self, intervals: int = 30, stop_after_starting: bool = False, stop_after_loading: bool = False, stop_after_benchmarking: bool = False) -> None:
        """
        Run typical workflow:

        1) start SUT
        2) start monitoring
        3) start loading (at first scripts (schema or loading via pull), then optionally parallel loading pods)
        4) run benchmarker jobs corresponding to list given via add_benchmark_list()
        5) remove everything when done

        If ``self.max_experiment_minutes`` is set (via ``--experiment-timeout``),
        the elapsed wall-clock time is checked at every iteration; once it is
        reached, the experiment is aborted via :meth:`remove_experiment` and this
        method returns early, regardless of which phase is currently running.

        :param intervals: Seconds to wait before checking change of status
        :param stop_after_starting: stops after phase 2)
        :param stop_after_loading: stops after phase 3)
        :param stop_after_benchmarking: stops after phase 4) This tells if SUT should not be removed when all benchmarking has finished. Set to True if we want to have loaded SUTs for inspection.
        """
        # test if there is a Pometheus server running in the cluster
        if self.cluster.is_monitoring_healthy():
            self.cluster.monitor_cluster_exists = True
            print("{:30s}: is running".format("Cluster monitoring"))
        else:
            self.cluster.monitor_cluster_exists = False
        for config in self.configurations:
            if config.experiment_dict["loader"] or config.experiment_dict["benchmarker"]:
                filename = f"bexhoma-experiment-dict-{config.configuration}-{self.code}.json".lower()
                filepath = self.result_filename_local(filename)
                with open(filepath, 'w') as _f:
                    json.dump(config.experiment_dict, _f, indent=2)
        intervals_wait = 0
        do = True
        experiment_start_time = datetime.utcnow()
        self._follow_up_waits_in_a_row = 0
        while do:
            #time.sleep(intervals)
            self.wait(intervals_wait)
            if 0 < intervals and intervals_wait < intervals:
                self._follow_up_waits_in_a_row += 1
            else:
                self._follow_up_waits_in_a_row = 0
            # a step of this pass may shorten the next wait (see _follow_up_wait())
            intervals_wait = intervals
            pass_started = time.monotonic()
            pass_calls_started = CALL_STATS.snapshot()
            if self.max_experiment_minutes is not None:
                elapsed_minutes = (datetime.utcnow() - experiment_start_time).total_seconds() / SECONDS_PER_MINUTE
                if elapsed_minutes >= self.max_experiment_minutes:
                    print("{:30s}: exceeded maximum timeout of {} minutes ({:.1f} elapsed) - stopping and removing all components".format("Experiment", self.max_experiment_minutes, elapsed_minutes))
                    self.remove_experiment()
                    return
            _benchmark_just_submitted = False
            # count number of running and pending pods
            num_pods_running_experiment = len(self.cluster.get_pods(app=self.appname, component='sut', experiment=self.code, status='Running'))
            num_pods_pending_experiment = len(self.cluster.get_pods(app=self.appname, component='sut', experiment=self.code, status='Pending'))
            num_pods_running_cluster = len(self.cluster.get_pods(app=self.appname, component='sut', status='Running'))
            num_pods_pending_cluster = len(self.cluster.get_pods(app=self.appname, component='sut', status='Pending'))
            # track optimistic in-pass pending counts per DBMS type (reset each loop iteration)
            num_pods_pending_dbms: dict[str, int] = {}
            # metric fetches of all configurations of this pass run together, in parallel
            submit_batch = MetricFetchBatch()
            # job submissions of this pass, run side by side after the loop (_submit_round())
            submissions: list = []
            for config in self.configurations:
                # a SUT stopped between repetitions: wait until it is gone
                if getattr(config, 'sut_removing', False):
                    if not self._sut_still_removing(config):
                        # gone: start it in the next pass, with fresh pod counts for the caps
                        intervals_wait = self._follow_up_wait(intervals_wait, "{} SUT removed".format(config.configuration))
                    continue
                # check if sut is running
                if not config.status.sut_running():
                    if self._abort_loading_if_needed(config, datetime.utcnow()):
                        return
                    if not config.experiment_done:
                        if not config.status.sut_pending():
                            we_can_start_new_sut = True
                            if self.max_sut is not None:
                                if num_pods_running_experiment + num_pods_pending_experiment >= self.max_sut:
                                    print("{:30s}: has to wait - {} running and {} pending pods: max is {} pods per experiment".format(config.configuration, num_pods_running_experiment, num_pods_pending_experiment, self.max_sut))
                                    we_can_start_new_sut = False
                            if self.cluster.max_sut is not None:
                                if num_pods_running_cluster + num_pods_pending_cluster >= self.cluster.max_sut:
                                    print("{:30s}: has to wait - {} running and {} pending pods: max is {} pods per cluster".format(config.configuration, num_pods_running_cluster, num_pods_pending_cluster, self.cluster.max_sut))
                                    we_can_start_new_sut = False
                            if config.max_sut_dbms is not None:
                                dbms_type = config.docker
                                num_running_dbms = len(self.cluster.get_pods(app=self.appname, component='sut', dbms=dbms_type, status='Running'))
                                num_pending_dbms = len(self.cluster.get_pods(app=self.appname, component='sut', dbms=dbms_type, status='Pending'))
                                num_pending_dbms_this_pass = num_pods_pending_dbms.get(dbms_type, 0)
                                if num_running_dbms + num_pending_dbms + num_pending_dbms_this_pass >= config.max_sut_dbms:
                                    print("{:30s}: has to wait - {} running and {} pending pods of dbms {}: max is {} pods per dbms".format(config.configuration, num_running_dbms, num_pending_dbms, dbms_type, config.max_sut_dbms))
                                    we_can_start_new_sut = False
                            if we_can_start_new_sut:
                                print("{:30s}: will start now".format(config.configuration))
                                config.lifecycle.start_sut()
                                num_pods_pending_experiment += 1
                                num_pods_pending_cluster += 1
                                if config.max_sut_dbms is not None:
                                    dbms_type = config.docker
                                    num_pods_pending_dbms[dbms_type] = num_pods_pending_dbms.get(dbms_type, 0) + 1
                        else:
                            print("{:30s}: is pending".format(config.configuration))
                    continue
                # check if loading is done
                config.loader.check()
                if self._abort_loading_if_needed(config, datetime.utcnow()):
                    return
                self._note_image_pull_waits(config)
                # start loading
                if not config.loading_started:
                    # check if monitoring has started
                    _has_benchmarks = (
                        (config.experiment_dict["benchmarker"] and config.client <= len(config.experiment_dict["benchmarker"]))
                        or len(config.benchmark_list) > 0
                    )
                    if _has_benchmarks:
                        if config.monitoring_active and not config.status.monitoring_running():
                            print("{:30s}: waits for monitoring".format(config.configuration))
                            if not config.status.monitoring_pending():
                                config.lifecycle.start_monitoring()
                            continue
                    # check if SUT is healthy
                    if config.status.sut_running():
                        if not config.status.sut_healthy():
                            # we wait for health check
                            print("{:30s}: waits for health check to succeed".format(config.configuration))
                            continue
                        if not config.status.workers_healthy():
                            # we wait for health check
                            print("{:30s}: waits for health check of workers to succeed".format(config.configuration))
                            continue
                        print("{:30s}: is not loaded yet".format(config.configuration))
                    now = datetime.utcnow()
                    if config.loading_after_time is not None:
                        if now >= config.loading_after_time:
                            if self.tenant_per == 'container':
                                # this container has to wait for others
                                config.tenant_ready_to_load = True
                            else:
                                if config.loading_active:
                                    config.loader.start_exec()
                                    config.loader.start_pod(parallelism=config.num_loading, num_pods=config.num_loading_pods)
                                else:
                                    config.loader.start_exec()
                        else:
                            print("{:30s}: will start loading but not before {}".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S')))
                            continue
                    else:
                        delay = 60
                        if 'delay_prepare' in config.dockertemplate:
                            # config demands other delay
                            delay = config.dockertemplate['delay_prepare']
                        if delay > 0:
                            config.loading_after_time = now + timedelta(seconds=delay)
                            print("{:30s}: will start loading but not before {} (that is in {} secs)".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S'), delay))
                            continue
                        else:
                            # start loading now
                            if self.tenant_per == 'container':
                                # this container has to wait for others
                                config.tenant_ready_to_load = True
                            else:
                                if config.loading_active:
                                    config.loader.start_exec()
                                    config.loader.start_pod(parallelism=config.num_loading, num_pods=config.num_loading_pods)
                                else:
                                    config.loader.start_exec()
                _has_benchmarks = (
                    (config.experiment_dict["benchmarker"] and config.client <= len(config.experiment_dict["benchmarker"]))
                    or len(config.benchmark_list) > 0
                )
                if config.loading_finished and _has_benchmarks:
                    if config.monitoring_active and not config.status.monitoring_running():
                        print("{:30s}: waits for monitoring".format(config.configuration))
                        if not config.status.monitoring_pending():
                            config.lifecycle.start_monitoring()
                        continue
                # store logs of successful init job pods
                #print("{:30s}: looking for completed startup pods".format(config.configuration))
                app = self.cluster.appname
                component = 'init'
                pods = self.cluster.get_job_pods(app=app, component=component, experiment=self.code, configuration=configuration)
                for pod in pods:
                    status = self.cluster.get_pod_status(pod)
                    self.cluster.logger.debug("Pod {} has status {}".format(pod, status))
                    if status == "Succeeded":
                        self.cluster.logger.debug("Store logs of starter job pod {}".format(pod))
                        self.cluster.store_pod_log(pod_name=pod)
                        if not self.cluster.pod_description_exists(pod_name=pod):
                            self.cluster.logger.debug("Store description of pod {}".format(pod))
                            self.cluster.store_pod_description(pod_name=pod)
                if self.tenant_per == 'container' and not config.loading_finished:
                    # can we start loading (all tenants/containers are ready)?
                    if not config.tenant_started_to_load:
                        ready = True
                        for config_tmp in self.configurations:
                            ready = ready and config_tmp.tenant_ready_to_load
                        if ready:
                            print("#### Starting to load")
                            # Initialize experiment-level loader counter to total loading pods
                            # across all configurations (count-down to zero). A configuration
                            # with several parallel loader entries (experiment_dict['loader'])
                            # contributes the sum of all its entries' pod counts, not just the
                            # primary entry's num_loading_pods.
                            total_loading_pods = sum(
                                (sum(
                                    entry.get('num_pods', entry.get('parallelism', 1))
                                    for entry in config_tmp.experiment_dict['loader']
                                ) if config_tmp.experiment_dict['loader'] else config_tmp.num_loading_pods)
                                for config_tmp in self.configurations
                                if config_tmp.loading_active
                            )
                            app_name = self.cluster.appname
                            exp_loader_key = '{}-loader-podcount-exp-{}'.format(app_name, self.code)
                            self.cluster.set_pod_counter(queue=exp_loader_key, value=total_loading_pods)
                            exp_gen_key = '{}-generator-podcount-exp-{}'.format(app_name, self.code)
                            self.cluster.set_pod_counter(queue=exp_gen_key, value=total_loading_pods)
                            for config_tmp in self.configurations:
                                config_tmp.tenant_started_to_load = True
                                if config_tmp.loading_active:
                                    config_tmp.loader.start_exec()
                                    config_tmp.loader.start_pod(parallelism=config_tmp.num_loading, num_pods=config_tmp.num_loading_pods)
                                else:
                                    config_tmp.loader.start_exec()
                    elif not config.tenant_started_to_index:
                        ready = True
                        for config_tmp in self.configurations:
                            ready = ready and config_tmp.tenant_ready_to_index
                        if ready:
                            print("#### Starting to index")
                            for config_tmp in self.configurations:
                                config_tmp.tenant_started_to_index = True
                                try:
                                    config_tmp.loader.load_data(scripts=config_tmp.indexscript, time_offset=config_tmp.time_loading, time_start_int=config_tmp.time_loading_start, script_type='index')
                                except RuntimeError as exc:
                                    print("{:30s}: index script upload failed: {}".format(config_tmp.configuration, exc))
                                    config_tmp.loading_finished = True
                                    config_tmp.loading_active = False
                # start benchmarking, if loading is done and monitoring is ready
                if config.loading_finished:
                    now = datetime.utcnow()
                    # check if SUT is healthy
                    if config.status.sut_running():
                        if not config.status.sut_healthy():
                            # we wait for health check
                            print("{:30s}: waits for health check to succeed".format(config.configuration))
                            continue
                        if not config.status.workers_healthy():
                            # we wait for health check
                            print("{:30s}: waits for health check of workers to succeed".format(config.configuration))
                            continue
                    # when loaded from PVC, system may not be ready yet
                    if config.loading_after_time is None:
                        # we have started from PVC
                        delay = 60
                        if 'delay_prepare' in config.dockertemplate:
                            # config demands other delay
                            delay = config.dockertemplate['delay_prepare']
                        if delay > 0:
                            config.loading_after_time = now + timedelta(seconds=delay)
                            print("{:30s}: will start benchmarking but not before {} (that is in {} secs)".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S'), delay))
                            continue
                    elif not now >= config.loading_after_time:
                        # system might not be ready yet
                        print("{:30s}: will start benchmarking but not before {}".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S')))
                        continue
                    # still benchmarks: check loading
                    _use_experiment_dict = bool(config.experiment_dict["benchmarker"])
                    _has_more_rounds = (
                        (config.experiment_dict["benchmarker"] and config.client <= len(config.experiment_dict["benchmarker"]))
                        or len(config.benchmark_list) > 0
                    )
                    if _has_more_rounds:
                        if config.monitoring_active and not config.status.monitoring_running():
                            print("{:30s}: waits for monitoring".format(config.configuration))
                            if not config.status.monitoring_pending():
                                config.lifecycle.start_monitoring()
                            continue
                    app = self.cluster.appname
                    component = 'benchmarker'
                    # Defer benchmark submission and stop_sut() while any jobs exist,
                    # whether still running or succeeded-but-not-yet-cleaned-up.
                    # end_benchmarking() runs in the second loop below; stop_sut() must
                    # not fire until that loop has processed all completed jobs and
                    # deleted them, so we continue here for any non-empty job list.
                    # jobs already ended and deleted by this process may still be listed
                    _active_jobs = [
                        job for job in (self.cluster.get_jobs(app, component, self.code, configuration=config.configuration) or [])
                        if job not in self._ended_jobs()]
                    if _active_jobs:
                        if any(not self.cluster.get_job_status(j) for j in _active_jobs):
                            if self._skip_benchmark_round_if_not_started(config, _active_jobs, datetime.utcnow()):
                                intervals_wait = self._follow_up_wait(intervals_wait, "{} round skipped".format(config.configuration))
                                continue
                            print("{:30s}: has running benchmarks".format(config.configuration))
                        continue
                    if _use_experiment_dict and config.client <= len(config.experiment_dict["benchmarker"]):
                        # experiment dict path: submit all parallel entries in this client round
                        client = str(config.client)
                        experiment_run = str(config.num_experiment_to_apply_done + 1)
                        client_round = config.experiment_dict["benchmarker"][config.client - 1]
                        config.client += 1
                        is_first_in_round = config.client > self.client
                        if is_first_in_round:
                            print("{:30s}: Reset experiment counter. This is first run of client number {}.".format("Experiment", config.client - 1))
                            self.client = config.client
                        # Round counter is per-configuration: initialize for every config so
                        # each SUT's pods find their own key already set in Redis.
                        round_idx = config.client - 2  # 0-based index of the round just started
                        benchmarker_rounds = config.experiment_dict.get("benchmarker") or []
                        if round_idx < len(benchmarker_rounds):
                            total_round_pods = sum(entry["parallelism"] for entry in benchmarker_rounds[round_idx])
                        else:
                            total_round_pods = 0
                        round_counter_key = '{}-benchmarker-podcount-round-{}-{}-{}-{}'.format(app, experiment_run, client, config.configuration, self.code)
                        self.cluster.set_pod_counter(queue=round_counter_key, value=total_round_pods)
                        print("{:30s}: Round pod counter {} initialized to {}.".format("Experiment", round_counter_key, total_round_pods))
                        if is_first_in_round and self.tenant_per == 'container':
                            # Experiment counter spans all configurations so every
                            # container-tenancy pod waits for the full cross-SUT cohort.
                            total_exp_pods = sum(
                                sum(entry["parallelism"] for entry in c_rounds[round_idx])
                                for c in self.configurations
                                for c_rounds in [c.experiment_dict.get("benchmarker") or []]
                                if round_idx < len(c_rounds)
                            )
                            exp_bm_key = '{}-benchmarker-podcount-exp-{}'.format(app, self.code)
                            self.cluster.set_pod_counter(queue=exp_bm_key, value=total_exp_pods)
                            print("{:30s}: Benchmarker experiment counter {} initialized to {}.".format("Experiment", exp_bm_key, total_exp_pods))
                        print("{:30s}: benchmarks done {} of {}. This will be client {}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply, client))
                        # counters are set; the jobs of all configurations are submitted together after this loop
                        submissions.append(functools.partial(
                            self._submit_round, config, client_round, experiment_run, client,
                            round_counter_key, submit_batch))
                        _benchmark_just_submitted = True
                    elif not _use_experiment_dict and len(config.benchmark_list) > 0:
                        # legacy benchmark_list path
                        parallelism = config.benchmark_list.pop(0)
                        client = str(config.client)
                        experiment_run = str(config.num_experiment_to_apply_done + 1)
                        config.client = config.client+1
                        is_first_in_round = config.client > self.client
                        if is_first_in_round:
                            # this is the first instance of the next benchmark run
                            print("{:30s}: Reset experiment counter. This is first run of client number {}.".format("Experiment", config.client-1))
                            self.client = config.client
                        # Initialize round counter for this config (always, per-config key).
                        round_counter_key = '{}-benchmarker-podcount-round-{}-{}-{}-{}'.format(app, experiment_run, client, config.configuration, self.code)
                        self.cluster.set_pod_counter(queue=round_counter_key, value=parallelism)
                        if is_first_in_round and self.tenant_per == 'container':
                            # Container tenancy uses experiment_dict; this legacy path
                            # falls back to the current config's parallelism only.
                            exp_bm_key = '{}-benchmarker-podcount-exp-{}'.format(app, self.code)
                            self.cluster.set_pod_counter(queue=exp_bm_key, value=parallelism)
                            print("{:30s}: Benchmarker experiment counter {} initialized to {}.".format("Experiment", exp_bm_key, parallelism))
                        print("{:30s}: benchmarks done {} of {}. This will be client {}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply, client))
                        benchmarking_parameters = None
                        if len(config.benchmarking_parameters_list) > 0:
                            benchmarking_parameters = config.benchmarking_parameters_list.pop(0)
                        submissions.append(functools.partial(
                            self._submit_legacy_round, config, parallelism, benchmarking_parameters,
                            experiment_run, client, round_counter_key, submit_batch))
                        _benchmark_just_submitted = True
                    else:
                        # no list element left
                        if not self._leaves_sut_running(config, stop_after_starting, stop_after_benchmarking):
                            if getattr(getattr(self, 'args', None), 'mode', None) == 'load':
                                # load-only: no benchmarker job ever runs, so register the connection,
                                # create /results/{code}, upload configs and fetch loading metrics here
                                connection = (config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-1').lower()
                                config.runner.run_pod(connection=connection, configuration=config.configuration, client='1', parallelism=1, only_prepare=True)
                            print("{:30s}: can be stopped".format(config.configuration))
                            app = self.cluster.appname
                            pod_restarts: dict[str, dict] = {}
                            deployments = list(config.deployment_infos['deployment'].keys())
                            for deployment in deployments:
                                pods = self.cluster.get_pods(app, deployment, self.code, config.configuration)
                                for pod in pods:
                                    for container in config.deployment_infos['deployment'][deployment]['containers']:
                                        self.cluster.store_pod_log(pod, container, number=config.num_experiment_to_apply_done+1)
                                    # one read of the restart counts for the previous logs, the summary and the snapshot
                                    per_container = self.cluster.get_pod_restart_counts(pod)
                                    self.cluster.store_previous_pod_logs(pod, number=config.num_experiment_to_apply_done+1, counts=per_container)
                                    if not self.cluster.pod_description_exists(pod_name=pod):
                                        self.cluster.logger.debug("Store description of pod {}".format(pod))
                                        self.cluster.store_pod_description(pod_name=pod, number=config.num_experiment_to_apply_done+1)
                                    restarts = config.host.get_host_restarts(pod, counts=per_container)
                                    pod_restarts[pod] = sut_restarts.restart_snapshot_entry(restarts, per_container)
                                    summary = sut_restarts.format_restart_summary(restarts, per_container)
                                    print("{:30s}: had {} restarts at worker {}".format(config.configuration, summary, pod))
                            statefulsets = list(config.deployment_infos['statefulset'].keys())
                            for statefulset in statefulsets:
                                pods = config.get_worker_pods(component=statefulset)
                                for pod in pods:
                                    for container in config.deployment_infos['statefulset'][statefulset]['containers']:
                                        self.cluster.store_pod_log(pod, container, number=config.num_experiment_to_apply_done+1)
                                    # one read of the restart counts for the previous logs, the summary and the snapshot
                                    per_container = self.cluster.get_pod_restart_counts(pod)
                                    self.cluster.store_previous_pod_logs(pod, number=config.num_experiment_to_apply_done+1, counts=per_container)
                                    if not self.cluster.pod_description_exists(pod_name=pod):
                                        self.cluster.logger.debug("Store description of pod {}".format(pod))
                                        self.cluster.store_pod_description(pod_name=pod, number=config.num_experiment_to_apply_done+1)
                                    restarts = config.host.get_host_restarts(pod, counts=per_container)
                                    pod_restarts[pod] = sut_restarts.restart_snapshot_entry(restarts, per_container)
                                    summary = sut_restarts.format_restart_summary(restarts, per_container)
                                    print("{:30s}: had {} restarts at worker {}".format(config.configuration, summary, pod))
                            experiment_run = str(config.num_experiment_to_apply_done + 1)
                            restarts_filename = self.result_filename_local(
                                f"bexhoma-sut-{config.configuration}-{self.code}-{experiment_run}-restarts.json".lower())
                            with open(restarts_filename, 'w') as _f:
                                json.dump(pod_restarts, _f, indent=2)
                            config.lifecycle.stop_sut()
                            config.num_experiment_to_apply_done = config.num_experiment_to_apply_done + 1
                            if config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                                # the loop waits for the removal and serves the others meanwhile
                                self._prepare_next_repetition(config)
                            else:
                                config.experiment_done = True
                        else:
                            print("{:30s}: can be stopped, but we leave it running".format(config.configuration))
                            command = config.lifecycle.generate_port_forward()
                            if 'sut_service' not in self.workload:
                                self.workload['sut_service'] = dict()
                            self.workload['sut_service'][config.configuration] = config.get_service_sut(config.configuration)
                            print("{:30s}: Ready: {}".format(config.configuration, command))
                            if config.client == 1 and config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                                client = str(config.client)
                                config.client = config.client+1
                                if config.num_experiment_to_apply > 1:
                                    connection = (config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-'+client).lower()
                                else:
                                    connection = (config.configuration+'-'+client).lower()
                                config.runner.run_pod(connection=connection, configuration=config.configuration, client=client, parallelism=1, only_prepare=True)
                                config.num_experiment_to_apply_done = config.num_experiment_to_apply
                            config.experiment_done = True
                else:
                    progress = ""
                    if len(config.experiment_dict['loader']) > 1:
                        sut_labels = self.cluster.get_pods_labels(
                            app=self.cluster.appname, component='sut',
                            experiment=self.code, configuration=config.configuration)
                        if len(sut_labels) > 0:
                            labels = next(iter(sut_labels.values()))
                            num_data_jobs = labels.get('num_data_jobs')
                            num_data_jobs_ready = labels.get('num_data_jobs_ready', '0')
                            if num_data_jobs:
                                progress = " ({}/{} parallel loading jobs done)".format(
                                    num_data_jobs_ready, num_data_jobs)
                    print("{:30s}: is loading{}".format(config.configuration, progress))
            self._run_parallel_steps(submissions, "submitted {} benchmark rounds")
            submit_batch.run(self.max_parallel_fetches)
            _we_have_running_benchmarks = False
            _we_have_incomplete_jobs = False
            end_batch = MetricFetchBatch()
            # files of the jobs ended in this pass, uploaded together before end_batch runs
            end_uploads: list = []
            # the job ends of all configurations run side by side (_end_finished_jobs())
            for running, incomplete, ended in self._run_parallel_steps(
                    [functools.partial(self._end_finished_jobs, config, end_batch, end_uploads)
                     for config in self.configurations],
                    "ended {} benchmarker jobs", count=lambda results: sum(len(ended) for _, _, ended in results)):
                _we_have_running_benchmarks = _we_have_running_benchmarks or running
                _we_have_incomplete_jobs = _we_have_incomplete_jobs or incomplete
                for job in ended:
                    # the next round needs nothing from the cluster
                    intervals_wait = self._follow_up_wait(intervals_wait, "{} job ended".format(job))
            self._upload_ended_job_files(end_uploads)
            end_batch.run(self.max_parallel_fetches)
            print("{:30s}: took {:.1f}s ({})".format(
                "Loop pass", time.monotonic() - pass_started, CALL_STATS.since(pass_calls_started)))
            if _we_have_running_benchmarks: #len(pods) == 0 and len(jobs) == 0:
                do = False
                # A job was submitted this iteration: the Kubernetes API may not yet
                # return it from get_jobs(), so _we_have_incomplete_jobs would be
                # False even though the job is actually running.  Force another pass
                # so the new job can be observed before the termination check fires.
                if _benchmark_just_submitted:
                    do = True
                for config in self.configurations:
                    #if config.status.sut_pending() or config.loading_started or len(config.benchmark_list) > 0:
                    if config.status.sut_pending():
                        #print("{} pending".format(config.configuration))
                        self.cluster.logger.debug("{} pending".format(config.configuration))
                        do = True
                    if not config.loading_started or not config.loading_finished:
                        #print("{} not loaded".format(config.configuration))
                        self.cluster.logger.debug("{} not loaded".format(config.configuration))
                        do = True
                    #print(config.client, len(config.experiment_dict["benchmarker"]))
                    _still_has_benchmarks = (
                        (config.experiment_dict["benchmarker"] and config.client <= len(config.experiment_dict["benchmarker"]))
                        or (not bool(config.experiment_dict["benchmarker"]) and len(config.benchmark_list) > 0)
                    )
                    if _still_has_benchmarks:
                        #print("{} still benchmarks to run".format(config.configuration))
                        self.cluster.logger.debug("{} still benchmarks to run".format(config.configuration))
                        do = True
                    # The else block (stop_sut + reset_sut + start_sut) is deferred to
                    # the next iteration while active jobs exist.  When the last job of a
                    # repetition was just processed, _still_has_benchmarks is False
                    # (client counter not yet reset) but another repetition is pending.
                    # Keep the loop running so the else block can fire next iteration.
                    if not stop_after_starting and config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                        self.cluster.logger.debug("{} more repetitions pending: {}/{}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply))
                        do = True
                    if stop_after_starting:
                        if config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                            #print("{} still not done: {}/{}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply))
                            self.cluster.logger.debug("{} still not done: {}/{}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply))
                            do = True
                if _we_have_incomplete_jobs:
                    self.cluster.logger.debug("there are still running benchmark jobs")
                    do = True
            else:
                # No benchmarker jobs exist: stop the loop once every configuration
                # has finished all its experiment repetitions.
                if all(config.experiment_done for config in self.configurations):
                    do = False
    def get_job_timing_benchmarking(self,
                                    jobname: str) -> list:
        """
        Extracts start and end times from a benchmarking job.
        All benchmarker containers (including refresh-stream loaders) must be named
        ``dbmsbenchmarker`` so the log file ends with ``.dbmsbenchmarker.log``.

        :param jobname: Name of the job
        :return: List of pairs (start,end) per pod
        """
        return self.extract_job_timing(jobname, container="dbmsbenchmarker")
    def get_job_timing_loading(self,
                               jobname: str) -> tuple:
        """
        Extracts start and end times from a loading job.
        This uses extract_job_timing() and sets container to 'datagenerator' and 'sensor'.

        :param jobname: Name of the job
        :return: List of pairs (start,end) per pod, triple of datagenerator, sensor and total (i.e., sum)
        """
        timing_datagenerator = self.extract_job_timing(jobname, container="datagenerator")
        timing_sensor = self.extract_job_timing(jobname, container="sensor")
        timing_total = timing_datagenerator + timing_sensor
        return timing_datagenerator, timing_sensor, timing_total
        #return total_time, generator_time, loader_time
    def extract_job_timing(self,
                           jobname: str,
                           container: str) -> list:
        """
        Extracts start and end times from a job.
        Looks for all container logs of the job.
        Start and end are expected to be noted as BEXHOMA_START and BEXHOMA_END in the logs.

        :param jobname: Name of the job
        :param container: Name of the container in the pods of the job
        :return: List of pairs (start,end) per pod
        """
        def get_job_timing(filename):
            """
            Transforms a log file in text format into list of pairs of timing information.
            This reads BEXHOMA_START and BEXHOMA_END

            :param filename: Name of the log file 
            :return: List of pairs (start,end) per pod
            """
            try:
                with open(filename) as f:
                    lines = f.readlines()
                stdout = "".join(lines)
                pod_name = filename[filename.rindex("-")+1:-len(".log")]
                timing_start = re.findall('BEXHOMA_START:(.+?)\n', stdout)[0]
                timing_end = re.findall('BEXHOMA_END:(.+?)\n', stdout)[0]
                return (int(timing_start), int(timing_end))
            except Exception as e:
                print(e)
                return (0,0)
        directory = os.fsencode(self.path)
        #print(jobname)
        timing = []
        self.cluster.logger.debug("Looking for files {jobname}*.{container}.log".format(jobname=jobname, container=container))
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            #if filename.startswith("bexhoma-loading-"+jobname) and filename.endswith(".{container}.log".format(container=container)):
            if filename.startswith(jobname) and filename.endswith(".{container}.log".format(container=container)):
                self.cluster.logger.debug("Found jobcontainer file {filename}".format(filename=filename))
                filename_local = self.result_filename_local(filename)
                (timing_start, timing_end) = get_job_timing(filename_local)
                #(timing_start, timing_end) = get_job_timing(self.path+"/"+filename)
                self.cluster.logger.debug("Found times {times}".format(times=(timing_start, timing_end)))
                if (timing_start, timing_end) == (0,0):
                    print(f"Error in {filename}: no start and end times")
                else:
                    timing.append((timing_start, timing_end))
            # when log does not contain container name (when is it true?)
            """
            elif filename.startswith(jobname) and filename.endswith(".log"):
                self.cluster.logger.debug("Found job file {filename}".format(filename=filename))
                (timing_start, timing_end) = get_job_timing(self.path+"/"+filename)
                self.cluster.logger.debug("Found times {times}".format(times=(timing_start, timing_end)))
                if (timing_start, timing_end) == (0,0):
                    print("Error in "+filename)
                else:
                    timing.append((timing_start, timing_end))
            """
        #print(timing)
        return timing
    def end_benchmarking(self,
                         jobname: str,
                         config: Optional[object] = None,
                         fetch_batch: Optional[MetricFetchBatch] = None,
                         pending_uploads: Optional[list] = None) -> None:
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        :param config: Configuration object
        :param fetch_batch: Queue the metric fetches here instead of fetching
            right away, so the jobs that ended in one loop pass are processed in parallel.
        :param pending_uploads: Collect the names of the files to upload to the
            dashboard pod here instead of uploading them one by one; the
            caller uploads them (:meth:`upload_experiment_files`) before
            ``fetch_batch`` runs, whose fetches read them in the pod.
        """
        def upload(filename: str) -> str:
            if pending_uploads is None:
                return self.upload_experiment_file(filename=filename)
            pending_uploads.append(filename)
            return ""
        def fetch(**kwargs) -> None:
            if fetch_batch is None:
                config.metrics.fetch(**kwargs)
            else:
                fetch_batch.add_fetch(config, **kwargs)
        self.cluster.logger.debug('base.end_benchmarking({})'.format(jobname))
        # mark pod with new end time and duration
        job_labels = self.cluster.get_jobs_labels(app=self.cluster.appname, component='benchmarker', experiment=self.code)
        if len(job_labels) > 0 and len(job_labels[jobname]) > 0:
            # get pairs (start,end) of benchmarking pods
            timing_benchmarker = self.get_job_timing_benchmarking(jobname)
            #print("timing_benchmarker", timing_benchmarker)
            if not timing_benchmarker:
                print("{:30s}: no timing data found for job {}".format(jobname, jobname))
                return
            # Unzip the pairs into two separate lists: firsts and seconds
            firsts, seconds = zip(*timing_benchmarker)
            # Find the minimum of the first entries and the maximum of the second entries
            start_time = min(firsts)
            end_time = max(seconds)
            #print(f"Min of first entries: {start_time}")
            #print(f"Max of second entries: {end_time}")
            if config is not None:
                config.benchmarking_timespans = {}
                config.benchmarking_timespans['benchmarker'] = timing_benchmarker
            start_time_job = int(job_labels[jobname]['start_time'])
            connection = job_labels[jobname]['connection']
            # Persist timing in the per-connection config file immediately, unconditionally
            # of the dashboard pod, so it survives even if the combined connections.config
            # is later overwritten (e.g. by dbmsbenchmarker's benchmark.py expansion).
            if config is not None:
                individual_config_path = self.path + "/" + connection + ".config"
                if os.path.exists(individual_config_path):
                    try:
                        with open(individual_config_path, 'r') as f:
                            individual_conns = ast.literal_eval(f.read())
                        for ki, ci in enumerate(individual_conns):
                            if ci['name'] == connection:
                                individual_conns[ki]['hostsystem']['benchmarking_timespans'] = config.benchmarking_timespans
                                break
                        with open(individual_config_path, 'w') as f:
                            f.write(str(individual_conns))
                        print("{:30s}: wrote benchmarking_timespans to {}".format(connection, individual_config_path))
                        # Upload the individual config to the pod so that evaluate_results()'s
                        # download_experiment_file('') does not later overwrite it with the
                        # stale pod copy (which was written at job-submission time with {}).
                        upload(connection + '.config')
                    except Exception as exc:
                        print("{:30s}: WARNING - could not update {}: {}".format(connection, individual_config_path, exc))
                else:
                    print("{:30s}: WARNING - individual config not found: {}".format(connection, individual_config_path))
            now = datetime.utcnow()
            now_string = now.strftime('%Y-%m-%d %H:%M:%S')
            time_now = str(datetime.now())
            end_time_job = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
            print("{:30s}: showing benchmarker times".format(connection))
            print("{:30s}: benchmarker timespan job from {} to {}".format(connection, start_time_job, end_time_job))
            print("{:30s}: benchmarker timespan pods from {} to {}".format(connection, start_time, end_time))
            print("{:30s}: benchmarker timespan (start to end single container [s]) = {}".format(connection, end_time-start_time))
            print("{:30s}: benchmarker times (start/end per pod and container) = {}".format(connection, timing_benchmarker))
            self.cluster.logger.debug("BENCHMARKING LABELS")
            self.cluster.logger.debug("connection: "+str(connection))
            self.cluster.logger.debug("start_time: "+str(start_time))
            self.cluster.logger.debug("end_time: "+str(end_time))
            self.cluster.logger.debug("duration: "+str(end_time-start_time))
            # copy config to pod - dashboard
            pods = self.cluster.get_pods(component='dashboard')
            if len(pods) > 0:
                pod_dashboard = pods[0]
                cmd = {}
                # store benchmarker times in config and upload it to cluster again
                if config is not None:
                    #connectionfile = config.benchmark.path+'/connections.config'
                    filename = 'connections.config'
                    connectionfile = self.path+"/"+filename
                    #print("Add benchmarker times to", connectionfile)
                    #print("Times", config.benchmarking_timespans)
                    #print("Find connection =", config.connection)
                    if config.benchmark is not None:
                        # jobs of other configurations may end at the same time (see parallel_steps)
                        with self.result_files_lock():
                            config.benchmark.getConnectionsFromFile(filename=connectionfile)
                            #print("Connection file:")
                            #print(config.benchmark.connections)
                            for k,c in enumerate(config.benchmark.connections):
                                #print(c['name'])
                                if c['name'] == connection:
                                    config.benchmark.connections[k]['hostsystem']['benchmarking_timespans'] = config.benchmarking_timespans
                                    print("{:30s}: found and updated times {}".format(c['name'], config.benchmarking_timespans))
                                    break
                            #print(config.benchmark.connections)
                            with open(connectionfile, 'w') as f:
                                f.write(str(config.benchmark.connections))
                        # upload connections infos with benchmarking times
                        stdout = upload(filename)
                        #cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        #stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                        self.cluster.logger.debug(stdout)
                # get monitoring for benchmarking
                if self.monitoring_active:
                    if 'deployment' in config.deployment_infos:
                        for name, deployment in config.deployment_infos['deployment'].items():
                            print("{:30s}: needs monitoring (common metrics) for deployment {}".format(connection, name))
                            if name=='sut' and config.monitoring_sut:
                                print("{:30s}: collecting execution metrics of SUT at connection {}".format(connection, connection))
                                fetch(
                                    title=f"Benchmarking phase: SUT deployment",
                                    connection=connection,
                                    connection_file=connection+'.config',
                                    container="dbms",
                                    #container="dbms",
                                    component=name,
                                    component_type="benchmarking",
                                    #component_type="benchmarking",
                                    experiment=self.code,
                                    time_start=start_time,
                                    time_end=end_time,
                                    metrics_type="metrics", # "metrics_special",
                                    pod_dashboard=pod_dashboard
                                    )
                            elif name!='sut':
                                print("{:30s}: collecting execution metrics of {} at connection {}".format(connection, name, connection))
                                fetch(
                                    title=f"Benchmarking phase: component {name}",
                                    connection=connection,
                                    connection_file=connection+'.config',
                                    container=deployment['containers'][0], #"dbms",
                                    #container="dbms",
                                    component=name,
                                    component_type=f"{name}benchmarking",
                                    #component_type="benchmarking",
                                    experiment=self.code,
                                    time_start=start_time,
                                    time_end=end_time,
                                    metrics_type="metrics",
                                    pod_dashboard=pod_dashboard
                                    )
                    if 'statefulset' in config.deployment_infos:
                        for name, statefulset in config.deployment_infos['statefulset'].items():
                            print("{:30s}: needs monitoring (custom metrics) for stateful set {}".format(connection, name))
                            print("{:30s}: collecting execution metrics of {} at connection {}".format(connection, name, connection))
                            fetch(
                                title=f"Benchmarking phase: component {name}",
                                connection=connection,
                                connection_file=connection+'.config',
                                container="dbms",
                                component=name,
                                component_type=f"{name}benchmarking",
                                #component_type="benchmarking",
                                experiment=self.code,
                                time_start=start_time,
                                time_end=end_time,
                                metrics_type=f"metrics_{name}",
                                pod_dashboard=pod_dashboard
                                )
                    if config.monitoring_sut:
                        #print("{:30s}: collecting execution metrics of SUT at connection {}".format(connection, config.current_benchmark_connection))
                        #config.metrics.fetch(
                        #    connection=config.current_benchmark_connection,
                        #    connection_file=connection+'.config',
                        #    container="dbms",
                        #    component_type="stream",
                        #    experiment=self.code,
                        #    time_start=start_time,
                        #    time_end=end_time,
                        #    metrics_type="metrics_special",
                        #    pod_dashboard=pod_dashboard
                        #    )
                        """
                        #print(config.current_benchmark_connection)
                        #print(config.benchmark.dbms.keys())
                        metric_example = config.benchmark.dbms[config.current_benchmark_connection].connectiondata['monitoring']['metrics_special']['total_cpu_memory'].copy()
                        print("{:30s}: example metric {}".format(connection, metric_example))
                        cmd['fetch_benchmarking_metrics'] = 'python metrics.py -r /results/ -db -ct stream -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, connection+'.config', '/results/'+self.code, self.code, start_time, end_time)
                        #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                        _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['fetch_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
                        self.cluster.logger.debug(stdout)
                        self.cluster.logger.debug(stderr)
                        # upload connections infos again, metrics has overwritten it
                        filename = 'connections.config'
                        cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                        self.cluster.logger.debug(stdout)
                        """
                        # Pooler
                        if config.sut_has_pool:
                            pass
                            #print("{:30s}: collecting execution metrics of pooler at connection {}".format(connection, config.current_benchmark_connection))
                            #config.metrics.fetch(
                            #    connection=config.current_benchmark_connection,
                            #    connection_file=connection+'.config',
                            #    container="pool",
                            #    component_type="pool",
                            #    experiment=self.code,
                            #    time_start=start_time,
                            #    time_end=end_time,
                            #    metrics_type="metrics",
                            #    pod_dashboard=pod_dashboard
                            #    )
                            """
                            #print(config.current_benchmark_connection)
                            #print(config.benchmark.dbms.keys())
                            metric_example = config.benchmark.dbms[config.current_benchmark_connection].connectiondata['monitoring']['metrics']['total_cpu_memory'].copy()
                            container = "pool"
                            if container is not None:
                                metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name="dbms"', 'container_label_io_kubernetes_container_name="{}"'.format(container))
                                metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name!="dbms"', 'container_label_io_kubernetes_container_name!="{}"'.format(container))
                                metric_example['query'] = metric_example['query'].replace('container="dbms"', 'container="{}"'.format(container))
                                metric_example['query'] = metric_example['query'].replace('container!="dbms"', 'container!="{}"'.format(container))
                            print("{:30s}: example metric {}".format(connection, metric_example))
                            cmd['fetch_benchmarking_metrics'] = 'python metrics.py -r /results/ -db -ct pool -cn pool -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, connection+'.config', '/results/'+self.code, self.code, start_time, end_time)
                            #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['fetch_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
                            self.cluster.logger.debug(stdout)
                            self.cluster.logger.debug(stderr)
                            # upload connections infos again, metrics has overwritten it
                            filename = 'connections.config'
                            cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                            stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                            self.cluster.logger.debug(stdout)
                            """
                    # get metrics of benchmarker components
                    # only if general monitoring is on
                    endpoints_cluster = self.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
                    if len(endpoints_cluster)>0 or self.cluster.monitor_cluster_exists:
                        print("{:30s}: collecting metrics of benchmarker at connection {}".format(connection, connection))
                        fetch(
                            title=f"Benchmarking phase: component benchmarker",
                            connection=connection,
                            connection_file=connection+'.config',
                            container="dbmsbenchmarker",
                            component="benchmarker",
                            component_type="benchmarker",
                            experiment=self.code,
                            time_start=start_time,
                            time_end=end_time,
                            metrics_type="metrics",
                            pod_dashboard=pod_dashboard
                            )
                        """
                        metric_example = config.benchmark.dbms[config.current_benchmark_connection].connectiondata['monitoring']['metrics']['total_cpu_memory'].copy()
                        container = "dbmsbenchmarker"
                        if container is not None:
                            metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name="dbms"', 'container_label_io_kubernetes_container_name="{}"'.format(container))
                            metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name!="dbms"', 'container_label_io_kubernetes_container_name!="{}"'.format(container))
                            metric_example['query'] = metric_example['query'].replace('container="dbms"', 'container="{}"'.format(container))
                            metric_example['query'] = metric_example['query'].replace('container!="dbms"', 'container!="{}"'.format(container))
                        print("{:30s}: example metric {}".format(connection, metric_example))
                        cmd['fetch_benchmarker_metrics'] = 'python metrics.py -r /results/ -db -ct benchmarker -cn dbmsbenchmarker -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, connection+'.config', '/results/'+self.code, self.code, start_time, end_time)
                        #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                        _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['fetch_benchmarker_metrics'], pod=pod_dashboard, container="dashboard")
                        self.cluster.logger.debug(stdout)
                        self.cluster.logger.debug(stderr)
                        # upload connections infos again, metrics has overwritten it
                        filename = 'connections.config'
                        cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                        self.cluster.logger.debug(stdout)
                        """
        if self.benchmarks:
            try:
                benchmark_run = int(jobname.split("-")[-1])
                evaluator = self.benchmarks[benchmark_run - 1].evaluator
            except (IndexError, ValueError):
                evaluator = self.evaluator
        else:
            evaluator = self.evaluator
        # the evaluator keeps counters; parsing is CPU-bound and gains nothing from threads
        with self.result_files_lock():
            evaluator.end_benchmarking(jobname)

    def end_loading(self,
                    jobname: str) -> None:
        """
        Ends a loading job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('base.end_loading({})'.format(jobname))
        if self.benchmarks:
            try:
                benchmark_run = int(jobname.split("-")[-1])
                evaluator = self.benchmarks[benchmark_run - 1].evaluator
            except (IndexError, ValueError):
                evaluator = self.evaluator
        else:
            evaluator = self.evaluator
        evaluator.end_loading(jobname)
    def show_summary_header(self) -> tuple:
        """
        Print workload metadata and per-connection details, then return sorted connection list and monitoring data.

        :return: Tuple of (connections_sorted, monitoring_applications) where connections_sorted
                 is a list of connection dicts ordered by name and monitoring_applications maps
                 component title to a DataFrame of application metrics.
        """
        print("\n## Show Summary")
        pd.set_option("display.max_rows", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        with open(resultfolder+"/"+code+"/queries.config",'r') as inp:
            self.workload = ast.literal_eval(inp.read())
        print("\n### Workload\n"+self.workload['name'])
        print("* Type: "+self.workload['type'])
        if 'duration' in self.workload:
            print("* Duration: {}s ".format(self.workload['duration']))
        else:
            print("* Duration: {}s ".format('missing'))
        print("* Code: "+code)
        print("* "+self.workload['intro'])
        print("* "+self.workload['info'].replace('\n', '\n  * '))
        if 'workflow_errors' in self.workload and len(self.workload['workflow_errors']) > 0:
            for error, messages in self.workload['workflow_errors'].items():
                print("* Error: "+error)
                for message in messages:
                    print("  * "+message)
        if 'sut_service' in self.workload or 'sut_stopped' in self.workload:
            print("\n### Services")
            for c in sorted(self.workload.get('sut_service', {})):
                print(c)
                print("* {}".format(self.generate_port_forward(self.workload['sut_service'][c])))
            for c in sorted(self.workload.get('sut_stopped', {})):
                print(c)
                print("* {}".format(self.workload['sut_stopped'][c]))
        print("\n### Connections")
        with open(resultfolder+"/"+code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
        num_run = self.workload['num_run'] if 'num_run' in self.workload else 1
        #print("num_run", num_run)
        pretty_connections = json.dumps(connections, indent=2)
        #print(pretty_connections)
        connections_sorted = sorted(connections, key=lambda c: c['name'])
        list_monitoring_app = list()
        #df_monitoring_app = pd.DataFrame()
        monitoring_applications = dict()
        for c in connections_sorted:
            print("* {} uses docker image {}".format(c['name'], c['parameter']['dockerimage']))
            if 'monitoring' in c and 'metrics' in c['monitoring']: # and len(list_monitoring_app) == 0:
                for component, title in self.workload['monitoring_components'].items():
                    #print(component, title)
                    list_monitoring_app = list()
                    df_monitoring_app = pd.DataFrame()
                    num_metrics_included = 0
                    for metricname, metric in c['monitoring']['metrics'].items():
                        #print(metric['type'])
                        if num_metrics_included >= 5:
                            continue
                        if metric['type'] == 'application' and metric['active'] == True:
                            df = self.evaluator.get_monitoring_metric(metric=metricname, component=component) # 'benchmarking')#
                            if not df.empty:
                                list_monitoring_app
                                if metric['metric'] == 'counter':
                                    df = counter_total(df, component)
                                else:
                                    df = df.max().sort_index()
                                df_cleaned = pd.DataFrame(df)
                                df_cleaned.columns = [metric['title']]
                                if not df_cleaned.empty:
                                    list_monitoring_app.append(df_cleaned.copy())
                                    num_metrics_included = num_metrics_included + 1
                    if len(list_monitoring_app) > 0:
                        df_monitoring_app = pd.concat(list_monitoring_app, axis=1).round(2)
                        df_monitoring_app = df_monitoring_app.reindex(index=evaluators.natural_sort(df_monitoring_app.index))
                        df_monitoring_app = df_monitoring_app.rename_axis(index="DBMS")
                        monitoring_applications[title] = df_monitoring_app
                    #print(df_monitoring_app)
                    #print(monitoring_applications)
                    # currently: only first component, only benchmarking
                    # TODO: make dynamical
                    #break
            infos = ["  * {}:{}".format(key,info) for key, info in c['hostsystem'].items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
            for info in infos:
                print(info)
            if 'sut' in c and len(c['sut']) > 0:
                for i, sut in enumerate(c['sut']):
                    print("  * sut {}".format(i))
                    infos = ["    * {}:{}".format(key,info) for key, info in sut.items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
                    for info in infos:
                        print(info)
            if 'worker' in c and len(c['worker']) > 0:
                for worker_type in c['worker'].keys():
                    for i, worker in enumerate(c['worker'][worker_type]):
                        print("  * {} {}".format(worker_type, i))
                        infos = ["    * {}:{}".format(key,info) for key, info in worker.items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
                        for info in infos:
                            print(info)
            if 'connection_parameter' in c['parameter'] and len(c['parameter']['connection_parameter']) > 0:
                for i, parameters in c['parameter']['connection_parameter'].items():
                    if i == "resources_total" and isinstance(parameters, dict):
                        # requested by the SUT pod plus all StatefulSets (dbms containers)
                        print("  * resources_total: {} CPU, {} GiB RAM requested in {} pods".format(
                            parameters.get('cpu'), parameters.get('memory_gib'), parameters.get('pods')))
                        for component, entry in parameters.get('components', {}).items():
                            print("    * {}: {} x, {} CPU, {} GiB RAM".format(
                                component, entry.get('replicas'), entry.get('cpu'), entry.get('memory_gib')))
                    if i == "eval_parameters":
                        print("  * "+i)
                        infos = ["    * {}:{}".format(key,info) for key, info in parameters.items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
                        for info in infos:
                            print(info)
        self._show_loading_provenance(connections_sorted)
        result_dir = Path(resultfolder) / code
        restarts_files = sorted(result_dir.glob("bexhoma-sut-*-restarts.json"))
        if restarts_files:
            print("\n### SUT Container Restarts")
            # Aggregated by max per pod, not summed across files -- see
            # sut_restarts.read_restart_counts().
            per_pod_total, _ = sut_restarts.read_restart_counts(result_dir)
            per_pod_summary = sut_restarts.read_restart_summaries(result_dir)
            restart_details = sut_restarts.collect_restart_details(result_dir)
            for pod, summary in per_pod_summary.items():
                print(f"* {pod}: {summary}")
                for detail in restart_details:
                    if detail.pod == pod:
                        print(f"  * {sut_restarts.format_detail(detail)}")
            total_restarts = sum(per_pod_total.values())
            self._record_test(total_restarts == 0, "No SUT container restarts")
            # A restarted container without a data volume re-initializes an
            # empty database, so every later query fails because of the
            # restart, not on its own merits.
            known = [d.data_volume for d in restart_details if d.data_volume is not None]
            if known:
                self._record_test(all(known), "SUT data survived container restarts")
            elif restart_details:
                self._record_skipped_test("SUT data survived container restarts (no describe log)")
            else:
                self._record_skipped_test("SUT data survived container restarts (no restarts)")
        return connections_sorted, monitoring_applications
    def show_summary(self, write_report: bool = False):
        """
        Print a basic experiment summary using the DBMSBenchmarker inspector directly.

        .. deprecated::
            Probably unused in practice.  All named experiment types (``tpch``,
            ``tpcds``, ``benchbase``, ``ycsb``, ``tpcc``) override this via
            :meth:`~bexhoma.experiments.dbmsbenchmarker.dbmsbenchmarker.show_summary`,
            which delegates to the :mod:`bexhoma.benchmarks` pipeline.
            This implementation is only reachable for legacy result folders whose
            ``queries.config`` still contains ``type='dbmsbenchmarker'`` — a value
            written by ``experiments.base`` before the named experiment subclasses
            existed.

        :param write_report: Accepted for signature parity with the
            ``bexhoma.benchmarks`` pipeline's ``show_summary(write_report=...)``;
            this legacy path has no tiered-report counterpart, so it is ignored.
        """
        self._test_results = list(self._runtime_test_results)
        self.cluster.logger.debug('base.show_summary()')
        connections_sorted, monitoring_applications = self.show_summary_header()
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        num_run = self.workload['num_run'] if 'num_run' in self.workload else 1
        #####################
        evaluate = inspector.inspector(resultfolder)
        evaluate.load_experiment(code=code, silent=True)
        query_properties = evaluate.get_experiment_query_properties()
        #print(query_properties)
        def map_index_to_queryname(numQuery):
            if numQuery[1:] in query_properties and 'config' in query_properties[numQuery[1:]] and 'title' in query_properties[numQuery[1:]]['config']:
                return query_properties[numQuery[1:]]['config']['title']
            else:
                return numQuery
        #####################
        if self.benchmarking_is_active():
            print("\n### Errors (failed queries)\n")
            df = evaluate.get_total_errors().T
            num_errors = df.sum().sum()
            if num_errors > 0:
                df_errors = df.copy()
                df_errors = df_errors[~(df_errors == False).all(axis=1)]
                list_error_queries = list(df_errors.index)
                # set readable names
                df.index = df.index.map(map_index_to_queryname)
                # remove only False rows
                df = df[~(df == False).all(axis=1)]
                #print(df)
                print(df.to_markdown(index=True, floatfmt=".2f"))
                for error in list_error_queries:
                    numQuery = error[1:]        # remove the leading "Q""
                    list_errors = evaluate.get_error(numQuery)
                    list_errors = {k:v for k,v in list_errors.items() if len(v) > 0}
                    #print(list_errors)
                    print("* "+map_index_to_queryname(error))
                    #df_error = pd.DataFrame.from_dict(list_errors, orient='index').sort_index()
                    #print(df_error)
                    for k,v in list_errors.items():
                        print("  * {}: {}".format(k,v))
            else:
                print("No errors")
        #####################
        if self.benchmarking_is_active():
            print("\n### Warnings (result mismatch)\n")
            df = evaluate.get_total_warnings().T
            num_warnings = df.sum().sum()
            if num_warnings > 0:
                # set readable names
                df.index = df.index.map(map_index_to_queryname)
                # remove only False rows
                df = df[~(df == False).all(axis=1)]
                #print(df)
                print(df.to_markdown(index=True, floatfmt=".2f"))
            else:
                print("No warnings")
        #####################
        if self.benchmarking_is_active():
            print("\n### Latency of Timer Execution [ms]")
            num_of_queries = 0
            df = evaluate.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
            if not df is None:
                df = df.sort_index().T.round(2)
                df.index = df.index.map(map_index_to_queryname)
                #print(df)
                df.index.names = ["DBMS"]
                print(df.to_markdown(index=True, floatfmt=".2f"))
                num_of_queries = len(df.index)
        #####################
        if self.loading_is_active():
            print("\n### Loading [s]\n")
            times = {}
            for c, connection in evaluate.benchmarks.dbms.items():
                times[c]={}
                if 'time_generated' in connection.connectiondata:
                    times[c]['time_generated'] = connection.connectiondata['time_generated']
                if 'time_ingested' in connection.connectiondata:
                    times[c]['time_ingested'] = connection.connectiondata['time_ingested']
                if 'time_schema' in connection.connectiondata:
                    times[c]['time_schema'] = connection.connectiondata['time_schema']
                if 'time_index' in connection.connectiondata:
                    times[c]['time_index'] = connection.connectiondata['time_index']
                if 'time_loading' in connection.connectiondata:
                    times[c]['time_loading'] = connection.connectiondata['time_loading']
            df = pd.DataFrame(times)
            df = df.reindex(sorted(df.columns), axis=1)
            df = df.round(2).T
            #df.index.names = ["DBMS"]
            df = df.rename_axis(index="DBMS")
            #print(df)
            print(df.to_markdown(index=True, floatfmt=".2f"))
        #####################
        if self.benchmarking_is_active():
            print("\n### Geometric Mean of Medians of Timer Run [s]\n")
            df = evaluate.get_aggregated_experiment_statistics(type='timer', name='run', query_aggregate='Median', total_aggregate='Geo')
            df = (df/1000.0).sort_index()
            df.columns = ['Geo Times [s]']
            df_geo_mean_runtime = df.copy()
            #print(df.round(2))
            df.index.names = ["DBMS"]
            print(df.round(2).to_markdown(index=True, floatfmt=".2f"))
        #####################
        if self.benchmarking_is_active():
            print("\n### Power@Size ((3600*SF)/(geo times))\n")
            df = evaluate.get_aggregated_experiment_statistics(type='timer', name='execution', query_aggregate='Median', total_aggregate='Geo')
            df = (df/1000.0).sort_index().astype('float')
            #print(self.workload['defaultParameters'])
            #print(self.workload['defaultParameters']['SF'])
            df = float(self.workload['defaultParameters']['SF'])*3600./df
            df.columns = ['Power@Size [~Q/h]']
            df_power = df.copy()
            #print(df.round(2))
            df.index.names = ["DBMS"]
            print(df.round(2).to_markdown(index=True, floatfmt=".2f"))
        #####################
        if self.benchmarking_is_active():
            # aggregate time and throughput for parallel pods
            print("\n### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))\n")
            df_merged_time = pd.DataFrame()
            for connection_nr, connection in evaluate.benchmarks.dbms.items():
                df_time = pd.DataFrame()
                c = connection.connectiondata
                connection_name = c['name']
                orig_name = c['orig_name']
                eva = evaluate.get_experiment_connection_properties(c['name'])
                df_time.index = [connection_name]
                #df_time['SF'] = int(SF)
                #print(c)
                #print(connection.name)
                #print(connection.connection)
                df_time['orig_name'] = orig_name
                df_time['SF'] = float(c['parameter']['connection_parameter']['loading_parameters']['SF'])
                df_time['pods'] = int(c['parameter']['connection_parameter']['loading_parameters']['PODS_PARALLEL'])
                #df_time['threads'] = int(c['parameter']['connection_parameter']['loading_parameters']['MYSQL_LOADING_THREADS'])
                df_time['num_experiment'] = int(c['parameter']['numExperiment'])
                df_time['num_client'] = int(c['parameter']['client'])
                df_time['benchmark_start'] = int(eva['times']['total'][c['name']]['time_start'])
                df_time['benchmark_end'] = int(eva['times']['total'][c['name']]['time_end'])
                df_merged_time = pd.concat([df_merged_time, df_time])
            df_time = df_merged_time.sort_index()
            benchmark_start = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client'])[['benchmark_start']].min(numeric_only=True)
            benchmark_end = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client'])[['benchmark_end']].max(numeric_only=True)
            df_benchmark = pd.DataFrame(benchmark_end['benchmark_end'] - benchmark_start['benchmark_start'])
            df_benchmark.columns = ['time [s]']
            benchmark_count = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client']).count()
            df_benchmark['count'] = benchmark_count['benchmark_end']
            df_benchmark['SF'] = df_benchmark.index.map(lambda x: x[1])
            df_benchmark['Throughput@Size'] = (num_run*num_of_queries*3600.*df_benchmark['count']/df_benchmark['time [s]']*df_benchmark['SF']).round(2)
            #df_benchmark['Throughput@Size [~GB/h]'] = (22*3600.*df_benchmark['count']/df_benchmark['time [s]']*df_benchmark['SF']).round(2)
            index_names = list(df_benchmark.index.names)
            index_names[0] = "DBMS"
            df_benchmark.rename_axis(index_names, inplace=True)
            df_benchmark.index = df_benchmark.index.get_level_values(0)
            #print(df_benchmark)
            print(df_benchmark.to_markdown(index=True, floatfmt=".2f"))
        #####################
        if self.benchmarking_is_active():
            print("\n### Workflow\n")
            #print(df_time)
            df_time.index.names = ["DBMS"]
            print(df_time.to_markdown(index=True, floatfmt=".2f"))
            workflow_actual = evaluators.EvaluatorBase.reconstruct_workflow(self.evaluator, df_time)
            #workflow_actual = self.evaluator.reconstruct_workflow(df_time)
            workflow_planned = self.workload['workflow_planned']
            if len(workflow_actual) > 0:
                print("\n#### Actual\n")
                for c in workflow_actual:
                    print("* DBMS", c, "- Pods", workflow_actual[c])
            if len(workflow_planned) > 0:
                print("\n#### Planned\n")
                for c in workflow_planned:
                    print("* DBMS", c, "- Pods", workflow_planned[c])
        #####################
        self.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            for title, metrics in monitoring_applications.items():
                print("\n#### "+title+"\n")
                metrics.index.names = ["DBMS"]
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        if self.benchmarking_is_active():
            self._test_column(df_geo_mean_runtime, "Geo Times [s]")
            self._test_column(df_power, "Power@Size [~Q/h]")
            self._test_column(df_benchmark, "Throughput@Size")
            passed_errors = num_errors == 0
            self._record_test(passed_errors, "No SQL errors" if passed_errors else "SQL errors")
            passed_warnings = num_warnings == 0
            self._record_test(passed_warnings, "No SQL warnings" if passed_warnings else "SQL warnings (result mismatch)")
            self._record_test(self.test_workflow(workflow_actual, workflow_planned), "Workflow as planned")
        self._print_test_summary()
    def scrape_interval(self) -> float:
        """
        Scrape interval of the cluster Prometheus in seconds, from ``cluster.config``.

        :return: ``monitor.scrape_interval``, or :data:`DEFAULT_SCRAPE_INTERVAL_SECONDS`.
        :rtype: float
        """
        try:
            monitor = self.cluster.config['credentials']['k8s']['monitor']
            return float(monitor.get('scrape_interval', DEFAULT_SCRAPE_INTERVAL_SECONDS))
        except (AttributeError, KeyError, TypeError, ValueError):
            return float(DEFAULT_SCRAPE_INTERVAL_SECONDS)
    def short_phase_connections(self, evaluate: object, component: str, connections) -> set:
        """
        Connections whose phase window was too short to measure the component's CPU.

        The window is the one the fetch queried (``Interval length`` in its
        ``bexhoma-metrics-{connection}-{component}.log``); the threshold is
        :func:`~bexhoma.monitoring_math.min_measurable_window`, lower for a job
        whose queries select only its own pods. A connection without such a
        log line (older results) is never short.

        :param evaluate: Evaluator with the result folder as ``path``.
        :param component: Monitoring component, e.g. ``loading``, ``benchmarker``.
        :param connections: Connection names to check.
        :return: The short ones.
        :rtype: set
        """
        scoped = scoped_job_connections(read_connections(evaluate.path), component)
        short = set()
        for connection in connections:
            threshold = min_measurable_window(component, self.scrape_interval(), connection in scoped)
            window = missing_metrics.fetch_window(
                Path(evaluate.path) / missing_metrics.fetch_log_name(connection, component))
            if window is not None and window < threshold:
                short.add(connection)
        return short
    @staticmethod
    def mark_not_measurable(df: pd.DataFrame, short: set, column: str = "CPU [CPUs]") -> pd.DataFrame:
        """
        Show ``n/a`` instead of a value for connections whose phase was too short.

        Apply after testing the column and after rounding: the column becomes text.

        :param df: Monitoring table, one row per connection.
        :param short: Connections from :meth:`short_phase_connections`.
        :param column: The column to mark.
        :return: ``df``, unchanged without short connections.
        :rtype: pandas.DataFrame
        """
        rows = [connection for connection in df.index if connection in short]
        if not rows or column not in df.columns:
            return df
        df = df.copy()
        df[column] = ["n/a" if connection in short else f"{value:.2f}"
                      for connection, value in df[column].items()]
        return df
    def show_summary_monitoring_table(self, evaluate: object, component: str) -> Tuple[list, set]:
        """
        Build a list of DataFrames containing CPU and RAM monitoring metrics for one component.

        :param evaluate: Evaluator object exposing get_monitoring_metric().
        :param component: Component name used as the metric scope (e.g. 'loading', 'benchmarking').
        :return: List of single-column DataFrames (one per collected metric), and the
                 connections whose phase window was too short to measure ``CPU [CPUs]``
                 (:meth:`short_phase_connections`): their 0 or NaN is no gap.
        :rtype: tuple[list, set]
        """
        df_monitoring = list()
        ##########
        df = evaluate.get_monitoring_metric(metric='total_cpu_util_s', component=component)
        short = self.short_phase_connections(evaluate, component, df.columns) if not df.empty else set()
        # a dead pod of the previous phase may still be in the sum, see counter_total()
        df = counter_total(df, component, scoped_job_connections(
            read_connections(evaluate.path), component, 'total_cpu_util_s'))
        df_cleaned = pd.DataFrame(df)
        df_cleaned.columns = ["CPU [CPUs]"]
        if not df_cleaned.empty:
            df_monitoring.append(df_cleaned.copy())
        ##########
        df = evaluate.get_monitoring_metric(metric='total_cpu_util', component=component)
        #df = evaluate.get_loading_metrics('total_cpu_util')
        df = df.max().sort_index()
        df_cleaned = pd.DataFrame(df)
        df_cleaned.columns = ["Max CPU"]
        if not df_cleaned.empty:
            df_monitoring.append(df_cleaned.copy())
        ##########
        df = evaluate.get_monitoring_metric(metric='total_cpu_memory', component=component)/1024
        #df = evaluate.get_loading_metrics('total_cpu_memory')/1024
        df = df.max().sort_index()
        df_cleaned = pd.DataFrame(df).round(2)
        df_cleaned.columns = ["Max RAM [Gb]"]
        if not df_cleaned.empty:
            df_monitoring.append(df_cleaned.copy())
        ##########
        df = evaluate.get_monitoring_metric(metric='total_cpu_memory_cached', component=component)/1024
        #df = evaluate.get_loading_metrics('total_cpu_memory_cached')/1024
        df = df.max().sort_index()
        df_cleaned = pd.DataFrame(df)
        df_cleaned.columns = ["Max RAM Cached [Gb]"]
        if not df_cleaned.empty:
            df_monitoring.append(df_cleaned.copy())
        return df_monitoring, short
    def show_summary_monitoring(self) -> None:
        """
        Print monitoring tables for all registered monitoring components and record test results.

        The ``### Monitoring`` header is only printed when at least one component
        has collected data.  Results are appended to ``self._test_results`` via
        :meth:`_record_test`.
        """
        if not (self.monitoring_active or self.cluster.monitor_cluster_active):
            return
        optional_components = self.workload.get('optional_monitoring_components', [])
        header_printed = False
        for component, title in self.workload['monitoring_components'].items():
            df_monitoring, short = self.show_summary_monitoring_table(self.evaluator, component)
            if len(df_monitoring) > 0:
                if not header_printed:
                    print("\n### Monitoring")
                    header_printed = True
                print(f"\n### {title}\n")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                df.index.names = ["DBMS"]
                # a phase too short to hold the scrapes it needs is not measurable:
                # its row shows n/a and is left out of the test
                measurable = df.drop(index=[connection for connection in df.index if connection in short])
                print(self.mark_not_measurable(df, short).to_markdown(index=True, floatfmt=".2f"))
                passed = self.evaluator.test_results_column(measurable, "CPU [CPUs]")
                if not passed and component in optional_components:
                    # Data generator produces no CPU load when data is pre-existing; skip test.
                    self._record_skipped_test(f"{title} contains 0 or NaN in CPU [CPUs] (data pre-existing)")
                elif measurable.empty:
                    # every phase of the component ran shorter than it can be measured
                    self._record_skipped_test(f"{title} contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)")
                else:
                    suffix = "no 0 or NaN" if passed else "0 or NaN"
                    self._record_test(passed, f"{title} contains {suffix} in CPU [CPUs]")
        # dbmsbenchmarker zero-fills a metric Prometheus did not return, so a
        # missing metric is only visible in the logs of the processes fetching it
        missing = missing_metrics.collect_missing_metrics(
            Path(self.evaluator.path), optional_components, scrape_interval=self.scrape_interval())
        if missing:
            print("\n### Missing Monitoring Metrics")
            for entry in missing:
                connection = f" for connection {entry.connection}" if entry.connection else ""
                expected = f", expected: {entry.expected}" if entry.expected else ""
                print(f"* {entry.title}{connection} ({entry.source}{expected})")
        unexpected = [entry for entry in missing if not entry.expected]
        if unexpected:
            self._record_test(False, "Monitoring metrics missing")
        elif missing:
            # Every gap has a harmless reason, e.g. a data generator that exited
            # before the first scrape, or a series that only exists while non-zero.
            reasons = "; ".join(sorted({entry.expected for entry in missing}))
            self._record_skipped_test(f"Monitoring metrics missing ({reasons})")
        else:
            self._record_test(True, "No monitoring metrics missing")









# Simple IoT example experiment


class IotExperiment(ExperimentBase):
    """
    Class for defining an TSBS experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-iot.config',
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            ):
        ExperimentBase.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.set_experiment(volume='iot')
        self.set_experiment(script='SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/iot')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'IoT Queries SF='+str(SF),
            info = 'This experiment performs some IoT inspired queries.',
            type = 'iot',
            )
        self.storage_label = 'tpch-'+str(SF)                           # label used to match persistent storage to this experiment
    def set_queries_full(self):
        self.set_queryfile('queries-iot.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-iot-profiling.config')



# TSBS experiment


class TsbsExperiment(ExperimentBase):
    """
    Class for defining an TSBS experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-tsbs.config',
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            ):
        ExperimentBase.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.set_experiment(volume='tsbs')
        self.set_experiment(script='SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/tsbs')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'TSBS Queries SF='+str(SF),
            info = 'This experiment performs some TSBS inspired queries.',
            type = 'tsdb',
            )
        self.storage_label = 'tsbs-'+str(SF)                               # label used to match persistent storage to this experiment
    def set_queries_full(self):
        self.set_queryfile('queries-tsbs.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tsbs-profiling.config')



# Example experiment class

class ExampleExperiment(ExperimentBase):
    """
    Class for defining a custom example experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries.config',
            num_experiment_to_apply = 1,
            timeout = 7200,
            script=None,
            ):
        ExperimentBase.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        if script is None:
            script = 'empty'
        self.set_experiment(volume='example')
        self.set_experiment(script=script)
        self.cluster.set_experiments_configfolder('experiments/example')
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'Custom Example Queries',
            info = 'This experiment performs some custom queries.'
            )
        self.storage_label = 'example'                                      # label used to match persistent storage to this experiment


# TPCx-AI experiment class

class TpcxaiExperiment(ExperimentBase):
    """
    Class for defining an TPCx-AI experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-tpcxai.config',
            SF = '100',
            num_experiment_to_apply = 1,
            timeout = 7200,
            script=None,
            ):
        ExperimentBase.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        if script is None:
            script = 'SF'+str(SF)+'-index'
        self.set_experiment(volume='tpcxai')
        self.set_experiment(script=script)
        self.cluster.set_experiments_configfolder('experiments/tpcxai')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_additional_labels(SF=SF)
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'TPCx-AI Queries SF='+str(SF),
            info = 'This experiment performs some TPCx-AI inspired queries.'
            )
        self.storage_label = 'tpcxai-'+str(SF)                             # label used to match persistent storage to this experiment
    def set_queries_full(self):
        self.set_queryfile('queries-tpcxai.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tpcxai-profiling.config')
