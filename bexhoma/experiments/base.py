"""
Base experiment class and general-purpose experiment types.

Provides :class:`DictToObject`, :class:`base` (the core experiment class
plugged into a cluster object to manage the full lifecycle of a bexhoma
experiment), and derived types :class:`iot`, :class:`tsbs`,
:class:`example`, and :class:`tpcxai`. Each experiment folder must contain
a query file and per-DBMS schema subfolders.

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
from types import SimpleNamespace
from importlib.metadata import version
from pathlib import Path
import math
from typing import List, Tuple, Optional

from bexhoma import evaluators

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = [
    "DictToObject",
    "parse_set_arg",
    "base",
    "iot",
    "tsbs",
    "example",
    "tpcxai",
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
    r'^(?P<kind>deployment|statefulset)\[(?P<workload>[^\]]+)\]\.container\[(?P<container>[^\]]+)\]\.(?P<param>[A-Za-z0-9_]+)$',
    re.IGNORECASE
)

def parse_set_arg(s: str) -> Tuple[dict, str]:
    """
    Parse a single ``--set`` argument of the form ``<selector>=<value>``.

    The selector must match one of:

    * ``deployment[NAME].container[CONTAINER].PARAM``
    * ``statefulset[NAME].container[CONTAINER].PARAM``

    :param s: Raw ``--set`` string from the CLI.
    :return: A tuple of (selector_dict, value_str) where selector_dict
             contains keys ``kind``, ``workload``, ``container``, and ``param``.
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
            "deployment[sut].container[dbms].max_worker_processes"
        )
    d = m.groupdict()
    d["kind"] = d["kind"].lower()
    return d, value.strip()


class base():
    """
    Class for defining an experiment.
    Settings are set generally.
    This class should be overloaded to define specific experiments.
    """
    def __init__(self,
                 cluster,
                 code=None,
                 num_experiment_to_apply = 1,
                 timeout = 7200,
                 detached=True):
        """
        Construct a new 'experiment' object.

        :param cluster: Cluster object, typically refering to a K8s cluster
        :param code: Unique identifier for the experiment. If none is given, it is created out of current time
        :param num_experiment_to_apply: How many times should the experiment be repeated at every configuration?
        :param timeout: Maximum timeout per query
        :param detached: DEPRECATED - use only True
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
        self.detached = detached                                        # if orchestrator is living in the cloud (only True is supported)
        self.cluster.set_code(code=self.code)
        self.set_connectionmanagement(
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
        self.client = 0                                                 # number of client in benchmarking list - for synching between different configs (multi-tenant container-wise)
        self.num_maintaining_pods = 0                                   # number of maintaining pods in total (pre-initialized; redeclared below)
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
        self.maintaining_parameters = {}                                # dict of parameters for maintaining component
        self.loading_parameters = {}                                    # dict of parameters for loading component
        self.sut_parameters = {}                                        # dict of parameters for sut and worker component
        self.loading_patch = ""                                         # YAML to patch manifest for loading component
        self.benchmarking_active = True                                 # Bool, tells if benchmarking is active (False for mode=start and mode=load)
        self.benchmarking_patch = ""                                    # YAML to patch manifest for benchmarking component
        self.benchmarking_parameters = {}                               # dict of parameters for benchmarking component
        self.jobtemplate_maintaining = ""                               # name of YAML manifest for maintaining component
        self.jobtemplate_loading = ""                                   # name of YAML manifest for loading component
        self.querymanagement = {}                                       # parameters for query.config
        self.additional_labels = dict()                                 # dict of additional labels for components
        self.workload = {}                                              # dict containing workload infos - will be written to query.config
        self.workload['monitoring_components'] = {}                     # dict for infos about which components are monitored
        self.monitoring_active = True                                   # Bool, tells if monitoring is active
        self.monitor_app_active = True                                  # Bool, tells if application-level metrics are monitored
        self.prometheus_interval = "10s"                                # interval for Prometheus to fetch metrics
        self.prometheus_timeout = "10s"                                 # timeout for Prometheus to fetch metrics
        self.loading_active = False                                     # Bool, tells if distributed loading is active (i.e., push instead of pull)
        self.loading_deactivated = False                                # Bool, tells if loading phase should be skipped
        self.num_loading = 0                                            # number of loading pods in parallel
        self.num_loading_pods = 0                                       # number of loading pods in total
        self.maintaining_active = False                                 # Bool, tells if maintaining is active
        self.num_maintaining = 0                                        # number of maintaining pods in parallel
        self.num_maintaining_pods = 0                                   # number of maintaining pods in total
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
        self.storage_label = ''                                         # label to mark persistent storage with (so that they can be matched to experiment)
        self.experiments_configfolder = ''                              # relative path to config folder of experiment (e.g., 'experiments/tpch')
        self.evaluator = evaluators.logger(                               # set evaluator for experiment - default uses base
            code=self.code, path=self.cluster.resultfolder, include_loading=True, include_benchmarking=True)
        self._test_results: list[tuple[bool, str]] = []                  # collected (passed, label) pairs for show_summary
        self.set_eval_parameters(code = self.code)
    def process(self) -> None:
        """
        Run the experiment according to self.args.mode.

        Dispatches to the appropriate workflow branch (start, load, summary,
        or the default full benchmark run) and prints timing information.
        """
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
            self.show_summary()
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
            start = default_timer()
            start_datetime = str(datetime.now())
            # run workflow
            self.work_benchmark_list(stop_after_benchmarking=True, stop_after_loading=True)
            # total time of experiment
            end = default_timer()
            end_datetime = str(datetime.now())
            duration_experiment = end - start
            print("{:30s}: ends at {} ({}) - {:.2f}s total".format("Experiment", end_datetime, end, duration_experiment))
            self.workload['duration'] = math.ceil(duration_experiment)
            self.evaluate_results()
            self.store_workflow_results()
            self.show_summary()
        elif self.args.mode == 'summary':
            self.show_summary()
        else:
            # total time of experiment
            start = default_timer()
            start_datetime = str(datetime.now())
            print("{:30s}: has code {}".format("Experiment", self.code))
            print("{:30s}: starts at {} ({})".format("Experiment", start_datetime, start))
            print("{:30s}: {}".format("Experiment", self.workload['info']))
            # run workflow
            self.work_benchmark_list(stop_after_benchmarking=self.args.skip_shutdown)
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
            self.show_summary()
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
    def experimentupload_file(self, filename: str) -> str:
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
        filename_local = self.path+'/'+filename
        filename_remote = '/results/'+str(self.code)+'/'+filename
        return self.cluster.upload_file(filename_local=filename_local, filename_remote=filename_remote, pod=self.pod_dashboard)
    def experimentdownload_file(self, filename: str) -> str:
        """
        Download a result file from the dashboard pod.

        :param filename: Name of the file relative to the experiment result folder.
        :return: Output of the download command, or empty string when no dashboard pod is available.
        """
        if not len(self.pod_dashboard):
            pods = self.cluster.get_pods(component='dashboard')
            if len(pods) > 0:
                self.pod_dashboard = pods[0]
            else:
                return ""
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
        cpu = str(args.request_cpu)
        memory = str(args.request_ram)
        cpu_limit = str(args.limit_cpu)
        memory_limit = str(args.limit_ram)
        cpu_type = str(args.request_cpu_type)
        gpu_type = str(args.request_gpu_type)
        gpus = str(args.request_gpu)
        request_storage_type = args.request_storage_type
        request_storage_size = args.request_storage_size
        request_storage_remove = args.request_storage_remove
        request_node_name = args.request_node_name
        request_node_loading = args.request_node_loading
        request_node_benchmarking = args.request_node_benchmarking
        skip_loading = args.skip_loading
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
            if not request_node_loading is None:
                self.patch_loading(patch="""
                spec:
                  template:
                    spec:
                      nodeSelector:
                        kubernetes.io/hostname: {node}
                """.format(node=request_node_loading))
                self.workload['info'] = self.workload['info']+"\nLoading is fixed to {}.".format(request_node_loading)
        # fix benchmarking
        if not request_node_benchmarking is None:
            self.patch_benchmarking(patch="""
            spec:
              template:
                spec:
                  nodeSelector:
                    kubernetes.io/hostname: {node}
            """.format(node=request_node_benchmarking))
            self.workload['info'] = self.workload['info']+"\nBenchmarking is fixed to {}.".format(request_node_benchmarking)
        # fix SUT
        if not request_node_name is None:
            self.set_resources(
                nodeSelector = {
                    'cpu': cpu_type,
                    'gpu': '',
                    'kubernetes.io/hostname': request_node_name
                })        
            self.workload['info'] = self.workload['info']+"\nSUT is fixed to {}.".format(request_node_name)
        if numRun > 1:
            self.workload['info'] = self.workload['info']+"\nEach query is repeated {} times.".format(numRun)
        if skip_loading:
            self.workload['info'] = self.workload['info']+"\nLoading is skipped."
        if request_storage_type and request_storage_size:
            self.workload['info'] = self.workload['info']+"\nDatabase is persisted to disk of type {} and size {}.".format(request_storage_type, request_storage_size)
            if request_storage_remove:
                self.workload['info'] = self.workload['info']+" Persistent storage is removed at experiment start."
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
            self.workload['info'] = self.workload['info']+"\nMaximum DBMS per cluster is {}.".format(self.max_sut)
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
    def test_results_in_dashboard(self) -> int:
        """
        DEPRECATED? Not used currently - depends on good test script for dbmsbenchmarker
        Run test script in dashboard pod.
        Extract exit code.

        :return: exit code of test script
        """
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
            cmd['test_results'] = 'python test-result.py -e {code} -r /results/;echo $?'.format(code=self.code)
            # include sub directories
            #cmd['zip_results'] = 'cd /results;zip -r {code}.zip {code}'.format(code=self.code)
            #fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['zip_results'].replace('"','\\"')+'"'
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['test_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
            try:
                if len(stdout) > 0:
                    print(stdout)
                    return int(stdout.splitlines()[-1:][0])
                else:
                    return 1
            except Exception as e:
                return 1
            finally:
                pass
        return 1
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
    def delay(self,
              sec: int,
              silent: bool = False) -> None:
        """
        Wait for a given number of seconds. Alias for :meth:`wait`.

        :param sec: Number of seconds to wait.
        :param silent: If True, suppress output during the wait.
        """
        self.wait(sec, silent)
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
    def set_querymanagement(self,
                            **kwargs) -> None:
        """
        Sets query management data for the experiment.
        This is for the benchmarker component (dbmsbenchmarker).

        :param kwargs: Dict of meta data, example 'numRun' => 3
        """
        self.querymanagement = kwargs
    # the following can be overwritten by configuration
    def set_connectionmanagement(self,
                                 **kwargs) -> None:
        """
        Sets connection management data for the experiment.
        This is for the benchmarker component (dbmsbenchmarker).
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'timout' => 60
        """
        self.connectionmanagement = kwargs
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
    def set_maintaining_parameters(self,
                                   **kwargs) -> None:
        """
        Sets ENV for maintaining components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.maintaining_parameters = kwargs
    def set_maintaining(self,
                        parallel: int,
                        num_pods: Optional[int] = None) -> None:
        """
        Sets job parameters for maintaining components: Number of parallel pods and optionally (if different) total number of pods.
        By default total number of pods is set to number of parallel pods.
        Can be overwritten by configuration.

        :param parallel: Number of parallel pods
        :param num_pods: Optionally (if different) total number of pods
        """
        self.num_maintaining = int(parallel)
        if num_pods is not None:
            self.num_maintaining_pods = int(num_pods)
        else:
            self.num_maintaining_pods = int(parallel)
        # total number at least number of parallel
        if self.num_maintaining_pods < self.num_maintaining:
            self.num_maintaining_pods = self.num_maintaining
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
    def add_configuration(self,
                          configuration: object) -> None:
        """
        Adds a configuration object to the list of configurations of this experiment.
        When a new configuration object is instanciated, an experiment object has to be provided.
        This method is then called automatically.

        :param configuration: Configuration object
        """
        self.configurations.append(configuration)
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
        self.set_querymanagement(
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
        self.set_querymanagement(
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
            cmd = {}
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loading -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct stream -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loader -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct benchmarker -e {}'.format(self.code)
            _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            for component_type in self.workload['monitoring_components']:
                cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct {} -e {}'.format(component_type, self.code)
                _, stdout, _ = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
                self.cluster.logger.debug(stdout)
        # download evaluation cubes
        print("{:30s}: downloading partial results".format("Experiment"))
        self.experimentdownload_file(filename='')
        print("{:30s}: uploading full results".format("Experiment"))
        self.experimentupload_file(filename='')
    def stop_maintaining(self):
        """
        Stop all maintaining jobs of this experiment.
        If a list of dbms configurations is set, use it.
        Otherwise tell the cluster to stop all maintaining jobs belonging to this experiment code.
        """
        if len(self.configurations) > 0:
            for config in self.configurations:
                config.stop_maintaining()
        else:
            app = self.cluster.appname
            component = 'maintaining'
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
    def stop_loading(self):
        """
        Stop all loading jobs of this experiment.
        If a list of dbms configurations is set, use it.
        Otherwise tell the cluster to stop all loading jobs belonging to this experiment code.
        """
        if len(self.configurations) > 0:
            for config in self.configurations:
                config.stop_loading()
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
                config.stop_monitoring()
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
    def start_monitoring(self):
        """
        Start monitoring for all dbms configurations of this experiment.
        """
        for config in self.configurations:
            config.start_monitoring()
    def start_sut(self):
        """
        Start all dbms configurations of this experiment.
        """
        for config in self.configurations:
            config.start_sut()
    def stop_sut(self):
        """
        Stop all SUT deployments of this experiment.
        If a list of dbms configurations is set, use it.
        Otherwise tell the cluster to stop all monitoring deployments belonging to this experiment code.
        """
        if len(self.configurations) > 0:
            for config in self.configurations:
                config.stop_sut()
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
            config.start_loading()
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
        Returns benchmarking workflow as dict of lists of lists.
        Keys are connection names.
        Values are lists of lists.
        Each inner list is for example added by add_benchmark_list(), c.f.
        Inner lists are repeated according to self.num_experiment_to_apply.
        Example: {'PostgreSQL-24-1-16384': [[1, 2]], 'MySQL-24-1-16384': [[1, 2]], 'PostgreSQL-24-1-32768': [[1, 2]], 'MySQL-24-1-32768': [[1, 2]]}

        :return: Dict of benchmarking workflow
        """
        # planned workflow is part of the workload
        if 'workflow_planned' in self.workload:
            return self.workload['workflow_planned']
        # planned workflow is given by cli arguments and must be constructed
        workflow = {}
        for configuration in self.configurations:
            workflow[configuration.configuration] = [configuration.benchmark_list_template for i in range(configuration.num_experiment_to_apply)]
        self.cluster.logger.debug('base.get_workflow_list({})'.format(workflow))
        #print(workflow)
        return workflow
    def store_workflow_results(self):
        """
        Constructs a list of runs for the planned workflow.
        Stores this information in self.workload['workflow_planned'].
        Updates query.config locally and remotely via update_workload().
        """
        workflow = self.get_workflow_list()
        self.workload['workflow_planned'] = workflow
        self.update_workload()
    def test_workflow(self,
                      workflow_1: dict,
                      workflow_2: dict) -> bool:
        """
        Compares two workflow dicts.
        A workflow is a dict (connection is key, lists of lists are values).
        Ignores the ordering inside the lists of lists.
        """
        def compare_lists(list1, list2):
            if len(list1) != len(list2):
                return False
            # sort inner lists to ignore ordering
            sorted_list1 = sorted([sorted(sublist) for sublist in list1])
            sorted_list2 = sorted([sorted(sublist) for sublist in list2])
            return sorted_list1 == sorted_list2
        if workflow_1.keys() != workflow_2.keys():
            return False
        for key in workflow_1:
            # compare lists, ignoring the ordering
            if not compare_lists(workflow_1[key], workflow_2[key]):
                return False
        return True
    def _record_test(self, passed: bool, label: str) -> bool:
        """
        Append a test result to the internal collector and return the passed flag.

        :param passed: Whether the test passed.
        :type passed: bool
        :param label: Human-readable description of what was tested.
        :type label: str
        :return: The value of passed, allowing inline chaining.
        :rtype: bool
        """
        self._test_results.append((passed, label))
        return passed
    def _test_column(self, df, column: str, title: str = '') -> bool:
        """
        Call evaluator.test_results_column silently and record the result.

        Mirrors the label format used by test_results_column so the summary
        line matches what would have been printed inline.

        :param df: DataFrame to check.
        :param column: Column name to inspect for zero or NaN values.
        :type column: str
        :param title: Optional prefix prepended to the column name in the label.
        :type title: str
        :return: True if the column contains no zero or NaN values.
        :rtype: bool
        """
        passed = self.evaluator.test_results_column(df, column, silent=True, title=title)
        full_title = f"{title} {column}" if len(title) > 0 else column
        suffix = "contains no 0 or NaN" if passed else "contains 0 or NaN"
        return self._record_test(passed, f"{full_title} {suffix}")
    def _print_test_summary(self) -> None:
        """Print all results collected in _test_results as a single summary block."""
        print("\n### Tests")
        for passed, label in self._test_results:
            status = "passed" if passed else "failed"
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
                with open(filename,'r') as inp:
                    queryconfig = ast.literal_eval(inp.read())
                    for k,v in self.workload.items():
                        queryconfig[k] = v
                #filename = self.benchmark.path+'/queries.config'
                with open(filename, 'w') as outp:
                    outp.write(str(queryconfig))
        print("{:30s}: uploading workload file".format("Experiment"))
        pod_dashboard = self.get_dashboard_pod()
        cmd = {}
        # single file
        filename = 'queries.config'
        filename_local = self.result_filename_local(filename)
        filename_remote = self.result_filename_remote(filename)
        self.experimentupload_file(filename=filename)
        #cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
        #cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':'+filename_remote, from_file=filename_local)
        #self.cluster.kubectl(cmd['upload_results'])
    def work_benchmark_list(self, intervals: int = 30, stop_after_starting: bool = False, stop_after_loading: bool = False, stop_after_benchmarking: bool = False) -> None:
        """
        Run typical workflow:

        1) start SUT
        2) start monitoring
        3) start loading (at first scripts (schema or loading via pull), then optionally parallel loading pods)
        4) optionally start maintaining pods
        5) at the same time as 4. run benchmarker jobs corresponding to list given via add_benchmark_list()
        6) remove everything when done

        :param intervals: Seconds to wait before checking change of status
        :param stop_after_starting: stops after phase 2)
        :param stop_after_loading: stops after phase 3)
        :param stop_after_benchmarking: stops after phase 5) This tells if SUT should not be removed when all benchmarking has finished. Set to True if we want to have loaded SUTs for inspection.
        """
        # test if there is a Pometheus server running in the cluster
        if self.cluster.is_monitoring_healthy():
            self.cluster.monitor_cluster_exists = True
            print("{:30s}: is running".format("Cluster monitoring"))
        else:
            self.cluster.monitor_cluster_exists = False
        intervals_wait = 0
        do = True
        while do:
            #time.sleep(intervals)
            self.wait(intervals_wait)
            intervals_wait = intervals
            # count number of running and pending pods
            num_pods_running_experiment = len(self.cluster.get_pods(app = self.appname, component = 'sut', experiment=self.code, status = 'Running'))
            num_pods_pending_experiment = len(self.cluster.get_pods(app = self.appname, component = 'sut', experiment=self.code, status = 'Pending'))
            num_pods_running_cluster = len(self.cluster.get_pods(app = self.appname, component = 'sut', status = 'Running'))
            num_pods_pending_cluster = len(self.cluster.get_pods(app = self.appname, component = 'sut', status = 'Pending'))
            for config in self.configurations:
                # check if sut is running
                if not config.sut_is_running():
                    #print("{} is not running".format(config.configuration))
                    if not config.experiment_done:
                        if not config.sut_is_pending():
                            #print("{:30s}: is not running yet".format(config.configuration))#, end="", flush=True)
                            if self.cluster.max_sut is not None or self.max_sut is not None:
                                we_can_start_new_sut = True
                                if self.max_sut is not None:
                                    #print("In experiment: {} running and {} pending pods: max is {} pods)".format(num_pods_running_experiment, num_pods_pending_experiment, self.max_sut))#, end="", flush=True)
                                    #print("{:30s}: {} running and {} pending pods: max is {} pods per experiment".format(config.configuration, num_pods_running_experiment, num_pods_pending_experiment, self.max_sut))#, end="", flush=True)
                                    if num_pods_running_experiment+num_pods_pending_experiment >= self.max_sut:
                                        print("{:30s}: has to wait - {} running and {} pending pods: max is {} pods per experiment".format(config.configuration, num_pods_running_experiment, num_pods_pending_experiment, self.max_sut))#, end="", flush=True)
                                        #print("{:30s}: has to wait".format(config.configuration))
                                        we_can_start_new_sut = False
                                if self.cluster.max_sut is not None:
                                    #print("{:30s}: {} running and {} pending pods: max is {} pods per cluster".format(config.configuration, num_pods_running_cluster, num_pods_pending_cluster, self.cluster.max_sut))#, end="", flush=True)
                                    if num_pods_running_cluster+num_pods_pending_cluster >= self.cluster.max_sut:
                                        print("{:30s}: has to wait - {} running and {} pending pods: max is {} pods per cluster".format(config.configuration, num_pods_running_cluster, num_pods_pending_cluster, self.cluster.max_sut))#, end="", flush=True)
                                        #print("{:30s}: has to wait".format(config.configuration))
                                        we_can_start_new_sut = False
                                if we_can_start_new_sut:
                                    print("{:30s}: will start now".format(config.configuration))
                                    config.start_sut()
                                    num_pods_pending_experiment = num_pods_pending_experiment + 1
                                    num_pods_pending_cluster = num_pods_pending_cluster + 1
                            else:
                                print("{:30s}: will start now".format(config.configuration))
                                config.start_sut()
                                num_pods_pending_experiment = num_pods_pending_experiment + 1
                                num_pods_pending_cluster = num_pods_pending_cluster + 1
                                #self.wait(10)
                        else:
                            print("{:30s}: is pending".format(config.configuration))
                    continue
                # check if loading is done
                config.check_load_data()
                # start loading
                if not config.loading_started:
                    # check if monitoring has started
                    if len(config.benchmark_list) > 0:
                        if config.monitoring_active and not config.monitoring_is_running():
                            print("{:30s}: waits for monitoring".format(config.configuration))
                            if not config.monitoring_is_pending():
                                config.start_monitoring()
                            continue
                    # check if SUT is healthy
                    if config.sut_is_running():
                        if not config.sut_is_healthy():
                            # we wait for health check
                            print("{:30s}: waits for health check to succeed".format(config.configuration))
                            continue
                        if not config.workers_are_healthy():
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
                                    config.start_loading()
                                    config.start_loading_pod(parallelism=config.num_loading, num_pods=config.num_loading_pods)
                                else:
                                    config.start_loading()
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
                                    config.start_loading()
                                    config.start_loading_pod(parallelism=config.num_loading, num_pods=config.num_loading_pods)
                                else:
                                    config.start_loading()
                # check if maintaining
                if config.loading_finished and len(config.benchmark_list) > 0:
                    if config.monitoring_active and not config.monitoring_is_running():
                        print("{:30s}: waits for monitoring".format(config.configuration))
                        if not config.monitoring_is_pending():
                            config.start_monitoring()
                        continue
                    if config.maintaining_active:
                        if not config.maintaining_is_running():
                            print("{:30s}: is not maintained yet".format(config.configuration))
                            if not config.maintaining_is_pending():
                                config.start_maintaining(parallelism=config.num_maintaining, num_pods=config.num_maintaining_pods)
                            else:
                                print("{:30s}: has pending maintaining".format(config.configuration))
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
                            for config_tmp in self.configurations:
                                config_tmp.tenant_started_to_load = True
                                if config_tmp.loading_active:
                                    config_tmp.start_loading()
                                    config_tmp.start_loading_pod(parallelism=config_tmp.num_loading, num_pods=config_tmp.num_loading_pods)
                                else:
                                    config_tmp.start_loading()
                    elif not config.tenant_started_to_index:
                        ready = True
                        for config_tmp in self.configurations:
                            ready = ready and config_tmp.tenant_ready_to_index
                        if ready:
                            print("#### Starting to index")
                            for config_tmp in self.configurations:
                                config_tmp.tenant_started_to_index = True
                                config_tmp.load_data(scripts=config_tmp.indexscript, time_offset=config_tmp.timeLoading, time_start_int=config_tmp.timeLoadingStart, script_type='indexed')
                # start benchmarking, if loading is done and monitoring is ready
                if config.loading_finished:
                    now = datetime.utcnow()
                    # check if SUT is healthy
                    if config.sut_is_running():
                        if not config.sut_is_healthy():
                            # we wait for health check
                            print("{:30s}: waits for health check to succeed".format(config.configuration))
                            continue
                        if not config.workers_are_healthy():
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
                    # still benchmarks: check loading and maintaining
                    if len(config.benchmark_list) > 0:
                        if config.monitoring_active and not config.monitoring_is_running():
                            print("{:30s}: waits for monitoring".format(config.configuration))
                            if not config.monitoring_is_pending():
                                config.start_monitoring()
                            continue
                        if config.maintaining_active and not config.maintaining_is_running():
                            print("{:30s}: waits for maintaining".format(config.configuration))
                            continue
                    app = self.cluster.appname
                    component = 'benchmarker'
                    configuration = ''
                    pods = self.cluster.get_job_pods(app, component, self.code, configuration=config.configuration)
                    if len(pods) > 0:
                        # still pods there
                        print("{:30s}: has running benchmarks".format(config.configuration))
                        continue
                    else:
                        if len(config.benchmark_list) > 0:
                            # next element in list
                            parallelism = config.benchmark_list.pop(0)
                            client = str(config.client)
                            config.client = config.client+1
                            if config.client > self.client:
                                # this is the first instance of the next benchmark run
                                print("{:30s}: Reset experiment counter. This is first run of client number {}.".format("Experiment", config.client-1))
                                self.client = config.client
                                # reset number of clients per experiment
                                redisQueue = '{}-{}-{}'.format(app, 'benchmarker-podcount', self.code)
                                self.cluster.set_pod_counter(queue=redisQueue, value=0)
                            print("{:30s}: benchmarks done {} of {}. This will be client {}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply, client))
                            if len(config.benchmarking_parameters_list) > 0:
                                benchmarking_parameters = config.benchmarking_parameters_list.pop(0)
                                print("{:30s}: we will change parameters of benchmark as {}".format(config.configuration, benchmarking_parameters))
                                config.set_benchmarking_parameters(**benchmarking_parameters)
                            # we now always add the experiment number to the connection name
                            #if config.num_experiment_to_apply > 1:
                            #    connection = config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-'+client
                            #else:
                            #    connection = config.configuration+'-'+client
                            connection = config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-'+client
                            print("{:30s}: start benchmarking".format(connection))
                            config.run_benchmarker_pod(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism)
                            #config.run_benchmarker_pod_hammerdb(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism)
                        else:
                            # no list element left
                            if not stop_after_benchmarking:
                                print("{:30s}: can be stopped".format(config.configuration))
                                app = self.cluster.appname
                                deployments = list(config.deployment_infos['deployment'].keys())
                                for deployment in deployments:
                                    #print("{:30s}: deployment {}".format(config.configuration, deployment))
                                    pods = self.cluster.get_pods(app, deployment, self.code, config.configuration)
                                    for pod in pods:
                                        #print("{:30s}: store log and description of pod {}".format(config.configuration, pod))
                                        for container in config.deployment_infos['deployment'][deployment]['containers']:
                                            #print("{:30s}: store log of container {}".format(config.configuration, container))
                                            self.cluster.store_pod_log(pod, container, number=config.num_experiment_to_apply_done+1)
                                        if not self.cluster.pod_description_exists(pod_name=pod):
                                            self.cluster.logger.debug("Store description of pod {}".format(pod))
                                            self.cluster.store_pod_description(pod_name=pod, number=config.num_experiment_to_apply_done+1)
                                        restarts = config.get_host_restarts(pod)
                                        print("{:30s}: had {} restarts at worker {}".format(config.configuration, str(restarts), pod))
                                statefulsets = list(config.deployment_infos['statefulset'].keys())
                                for statefulset in statefulsets:
                                    #print("{:30s}: stateful set {}".format(config.configuration, statefulset))
                                    pods = config.get_worker_pods(component=statefulset)
                                    for pod in pods: #config.deployment_infos['statefulset'][statefulset]['pods']:
                                        #print("{:30s}: store log and description of pod {}".format(config.configuration, pod))
                                        for container in config.deployment_infos['statefulset'][statefulset]['containers']:
                                            #print("{:30s}: store log of container {}".format(config.configuration, container))
                                            self.cluster.store_pod_log(pod, container, number=config.num_experiment_to_apply_done+1)
                                        if not self.cluster.pod_description_exists(pod_name=pod):
                                            self.cluster.logger.debug("Store description of pod {}".format(pod))
                                            self.cluster.store_pod_description(pod_name=pod, number=config.num_experiment_to_apply_done+1)
                                        restarts = config.get_host_restarts(pod)
                                        print("{:30s}: had {} restarts at worker {}".format(config.configuration, str(restarts), pod))
                                # old, static way of storing logs1
                                """
                                component = 'sut'
                                pods = self.cluster.get_pods(app, component, self.code, config.configuration)
                                for pod_sut in pods:
                                    for container in config.sut_containers_deployed:
                                        self.cluster.store_pod_log(pod_sut, container)
                                    if not self.cluster.pod_description_exists(pod_name=pod_sut):
                                        self.cluster.logger.debug("Store description of pod {}".format(pod_sut))
                                        self.cluster.store_pod_description(pod_name=pod_sut)
                                    restarts = config.get_host_restarts(pod_sut)
                                    print("{:30s}: had {} restarts at sut {}".format(config.configuration, str(restarts), pod_sut))
                                    #self.cluster.store_pod_log(pod_sut, 'dbms')
                                component = 'worker'
                                #pods = self.cluster.get_pods(app, component, self.code, config.configuration)
                                pods = config.get_worker_pods(component=component)
                                for pod_worker in pods:
                                    for container in config.worker_containers_deployed:
                                        self.cluster.store_pod_log(pod_worker, container, number=config.num_experiment_to_apply_done+1)
                                    if not self.cluster.pod_description_exists(pod_name=pod_worker):
                                        self.cluster.logger.debug("Store description of pod {}".format(pod_worker))
                                        self.cluster.store_pod_description(pod_name=pod_worker)
                                    restarts = config.get_host_restarts(pod_worker)
                                    print("{:30s}: had {} restarts at worker {}".format(config.configuration, str(restarts), pod_worker))
                                    #self.cluster.store_pod_log(pod_worker, 'dbms')
                                component = 'store'
                                #pods = self.cluster.get_pods(app, component, self.code, config.configuration)
                                pods = config.get_worker_pods(component=component)
                                for pod_store in pods:
                                    for container in config.store_containers_deployed:
                                        self.cluster.store_pod_log(pod_store, container, number=config.num_experiment_to_apply_done+1)
                                    if not self.cluster.pod_description_exists(pod_name=pod_store):
                                        self.cluster.logger.debug("Store description of pod {}".format(pod_store))
                                        self.cluster.store_pod_description(pod_name=pod_store)
                                    restarts = config.get_host_restarts(pod_store)
                                    print("{:30s}: had {} restarts at store {}".format(config.configuration, str(restarts), pod_store))
                                    #self.cluster.store_pod_log(pod_store, 'dbms')
                                component = 'pool'
                                pods = self.cluster.get_pods(app, component, self.code, config.configuration)
                                for pod_pool in pods:
                                    for container in config.pool_containers_deployed:
                                        self.cluster.store_pod_log(pod_pool, container)
                                    #self.cluster.store_pod_log(pod_worker, 'dbms')
                                """
                                config.stop_sut()
                                config.num_experiment_to_apply_done = config.num_experiment_to_apply_done + 1
                                if config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                                    while config.sut_is_existing():
                                        print("{:30s}: still being removed".format(config.configuration))
                                        self.wait(30)
                                    print("{:30s}: starts again".format(config.configuration))
                                    # reset number of clients per experiment
                                    #print("{:30s}: reset pod counter".format(config.configuration))
                                    #redisQueue = '{}-{}-{}'.format(app, 'benchmarker-podcount', self.code)
                                    #self.cluster.set_pod_counter(queue=redisQueue, value=0)
                                    # find next sequence of benchmarks
                                    config.benchmark_list = config.benchmark_list_template.copy()
                                    config.benchmarking_parameters_list = config.benchmarking_parameters_list_template.copy()
                                    self.client = 0
                                    # wait for PV to be gone completely
                                    #self.wait(60)
                                    config.reset_sut()
                                    config.start_sut()
                                    self.wait(10)
                                else:
                                    config.experiment_done = True
                            else:
                                print("{:30s}: can be stopped, but we leave it running".format(config.configuration))
                                command = config.generate_port_forward()
                                if not 'sut_service' in self.workload:
                                    self.workload['sut_service'] = dict()
                                self.workload['sut_service'][config.configuration] = config.get_service_sut(config.configuration)
                                print("{:30s}: Ready: {}".format(config.configuration, command))
                                #print(config.num_experiment_to_apply_done, config.num_experiment_to_apply)
                                # if we reach this point for the first time: simulate benchmarking
                                # this collects loading metrics and prepares a connection.config and a query.config
                                # this allows summaries like for "real" benchmarking experiments
                                if config.client == 1 and config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                                    client = str(config.client)
                                    config.client = config.client+1
                                    if config.num_experiment_to_apply > 1:
                                        connection=config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-'+client
                                    else:
                                        connection=config.configuration+'-'+client
                                    #print("{:30s}: start benchmarking".format(connection))
                                    config.run_benchmarker_pod(connection=connection, configuration=config.configuration, client=client, parallelism=1, only_prepare=True)
                                    config.num_experiment_to_apply_done = config.num_experiment_to_apply
                                #print("{} can be stopped, but we leave it running".format(config.configuration))
                else:
                    print("{:30s}: is loading".format(config.configuration))
            for config in self.configurations:
                # all jobs of configuration - benchmarker
                #app = self.cluster.appname
                #component = 'benchmarker'
                #configuration = ''
                #jobs = self.cluster.get_jobs(app, component, self.code, configuration)
                # success of job
                app = self.cluster.appname
                component = 'benchmarker'
                configuration = config.configuration#''
                #success = self.cluster.get_job_status(app=app, component=component, experiment=self.code, configuration=configuration)
                jobs = self.cluster.get_jobs(app, component, self.code, configuration)
                # all pods to these jobs
                pods = self.cluster.get_job_pods(app, component, self.code, configuration)
                # status per job
                for job in jobs:
                    # status per pod
                    for p in pods:
                        if not self.cluster.pod_log_exists(p):
                            status = self.cluster.get_pod_status(p)
                            self.cluster.logger.debug('job-pod {} has status {}'.format(p, status))
                            #print(p,status)
                            if status == 'Succeeded' or status == 'Failed':
                                containers = self.cluster.get_pod_containers(p)
                                for container in containers:
                                    if len(container) > 0:
                                        self.cluster.logger.debug("Store logs of job {} pod {} container {}".format(job, p, container))
                                        self.cluster.store_pod_log(p, container)
                                if not self.cluster.pod_description_exists(pod_name=p):
                                    self.cluster.logger.debug("Store description of job {} pod {}".format(job, p))
                                    self.cluster.store_pod_description(pod_name=p)
                            #if status == 'Succeeded':
                            #    self.cluster.logger.debug("Store logs of job {} pod {}".format(job, p))
                            #    #if status != 'Running':
                            #    self.cluster.store_pod_log(p)
                            #    #self.cluster.delete_pod(p)
                            #if status == 'Failed':
                            #    self.cluster.logger.debug("Store logs of job {} pod {}".format(job, p))
                            #    #if status != 'Running':
                            #    self.cluster.store_pod_log(p)
                            #    #self.cluster.delete_pod(p)
                    success = self.cluster.get_job_status(job)
                    self.cluster.logger.debug('job {} has success status {}'.format(job, success))
                    #print(job, success)
                    if success:
                        # status per pod
                        for p in pods:
                            status = self.cluster.get_pod_status(p)
                            self.cluster.logger.debug('job-pod {} has status {}'.format(p, status))
                            if status == 'Succeeded' or status == 'Failed':
                                containers = self.cluster.get_pod_containers(p)
                                for container in containers:
                                    if len(container) > 0:
                                        self.cluster.logger.debug("Store logs of job {} pod {} container {}".format(job, p, container))
                                        self.cluster.store_pod_log(p, container)
                                if not self.cluster.pod_description_exists(pod_name=p):
                                    self.cluster.logger.debug("Store description of job {} pod {}".format(job, p))
                                    self.cluster.store_pod_description(pod_name=p)
                                self.cluster.delete_pod(p)
                            #print(p,status)
                            #if status == 'Succeeded':
                            #    #if status != 'Running':
                            #    if not self.cluster.pod_log_exists(p):
                            #        self.cluster.logger.debug("Store logs of job {} pod {}".format(job, p))
                            #        self.cluster.store_pod_log(p)
                            #    self.cluster.delete_pod(p)
                            #if status == 'Failed':
                            #    #if status != 'Running':
                            #    if not self.cluster.pod_log_exists(p):
                            #        self.cluster.logger.debug("Store logs of job {} pod {}".format(job, p))
                            #        self.cluster.store_pod_log(p)
                            #    self.cluster.delete_pod(p)
                        self.end_benchmarking(job, config)
                        self.cluster.delete_job(job)
                        config.check_volumes()
            if len(pods) == 0 and len(jobs) == 0:
                do = False
                for config in self.configurations:
                    #if config.sut_is_pending() or config.loading_started or len(config.benchmark_list) > 0:
                    if config.sut_is_pending():
                        self.cluster.logger.debug("{} pending".format(config.configuration))
                        do = True
                    if not config.loading_started or not config.loading_finished:
                        self.cluster.logger.debug("{} not loaded".format(config.configuration))
                        do = True
                    if len(config.benchmark_list) > 0:
                        self.cluster.logger.debug("{} still benchmarks to run: {}".format(config.configuration, config.benchmark_list))
                        do = True
                    if stop_after_starting:
                        if config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                            do = True
    def benchmark_list(self, list_clients):
        """
        DEPRECATED? Is not used anymore.
        Runs a given list of benchmarker applied to all running SUTs of experiment.

        :param list_clients: List of (number of) benchmarker instances
        """
        print("benchmark_list() DEPRECATED")
        exit()
        for i, parallelism in enumerate(list_clients):
            client = str(i+1)
            for config in self.configurations:
                if not config.sut_is_running():
                    continue
                if not config.loading_started:
                    config.start_loading()
                else:
                    config.run_benchmarker_pod(connection=config.configuration+'-'+client, configuration=config.configuration, client=client, parallelism=parallelism)
            while True:
                for config in self.configurations:
                    if not config.sut_is_running():
                        continue
                    if not config.loading_started:
                        config.start_loading()
                time.sleep(10)
                # all jobs of configuration - benchmarker
                app = self.cluster.appname
                component = 'benchmarker'
                configuration = ''
                jobs = self.cluster.get_jobs(app, component, self.code, configuration)
                # all pods to these jobs
                pods = self.cluster.get_job_pods(app, component, self.code, configuration)
                # status per pod
                for p in pods:
                    status = self.cluster.get_pod_status(p)
                    print(p,status)
                    if status == 'Succeeded':
                        #if status != 'Running':
                        self.cluster.store_pod_log(p)
                        if not self.cluster.pod_description_exists(pod_name=p):
                            self.cluster.logger.debug("Store description of pod {}".format(p))
                            self.cluster.store_pod_description(pod_name=p)
                        self.cluster.delete_pod(p)
                    if status == 'Failed':
                        #if status != 'Running':
                        self.cluster.store_pod_log(p)
                        if not self.cluster.pod_description_exists(pod_name=p):
                            self.cluster.logger.debug("Store description of pod {}".format(p))
                            self.cluster.store_pod_description(pod_name=p)
                        self.cluster.delete_pod(p)
                # success of job
                app = self.cluster.appname
                component = 'benchmarker'
                configuration = ''
                success = self.cluster.get_job_status(app=app, component=component, experiment=self.code, configuration=configuration)
                jobs = self.cluster.get_jobs(app, component, self.code, configuration)
                # status per job
                for job in jobs:
                    success = self.cluster.get_job_status(job)
                    print(job, success)
                    if success:
                        self.cluster.delete_job(job)
                if len(pods) == 0 and len(jobs) == 0:
                    break
    def get_job_timing_benchmarking(self,
                                    jobname: str) -> list:
        """
        Extracts start and end times from a benchmarking job.
        This uses extract_job_timing() and sets container to 'dbmsbenchmarker'

        :param jobname: Name of the job
        :return: List of pairs (start,end) per pod
        """
        timing_benchmarker = self.extract_job_timing(jobname, container="dbmsbenchmarker")
        return timing_benchmarker
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
                         config: Optional[object] = None) -> None:
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        :param config: Configuration object
        """
        self.cluster.logger.debug('base.end_benchmarking({})'.format(jobname))
        # mark pod with new end time and duration
        job_labels = self.cluster.get_jobs_labels(app=self.cluster.appname, component='benchmarker', experiment=self.code)
        if len(job_labels) > 0 and len(job_labels[jobname]) > 0:
            # get pairs (start,end) of benchmarking pods
            timing_benchmarker = self.get_job_timing_benchmarking(jobname)
            #print("timing_benchmarker", timing_benchmarker)
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
            #self.timeLoadingEnd = default_timer()
            #self.timeLoading = float(self.timeLoadingEnd) - float(self.timeLoadingStart)
            #self.experiment.cluster.logger.debug("LOADING LABELS")
            #self.experiment.cluster.logger.debug(self.timeLoading)
            #self.experiment.cluster.logger.debug(float(self.timeLoadingEnd))
            #self.experiment.cluster.logger.debug(float(self.timeLoadingStart))
            #self.timeLoading = float(self.timeLoading) + float(timeLoading)
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
            #fullcommand = 'label pods '+pod_sut+' --overwrite loaded=True timeLoadingEnd="{}" timeLoading={}'.format(time_now_int, self.timeLoading)
            #print(fullcommand)
            #self.experiment.cluster.kubectl(fullcommand)
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
                        config.benchmark.getConnectionsFromFile(filename=connectionfile)
                        #print("Connection file:")
                        #print(config.benchmark.connections)
                        for k,c in enumerate(config.benchmark.connections):
                            #print(c['name'])
                            if c['name'] == config.connection:
                                config.benchmark.connections[k]['hostsystem']['benchmarking_timespans'] = config.benchmarking_timespans
                                print("{:30s}: found and updated times {}".format(c['name'], config.benchmarking_timespans))
                                break
                        #print(config.benchmark.connections)
                        with open(connectionfile, 'w') as f:
                            f.write(str(config.benchmark.connections))
                        # upload connections infos with benchmarking times
                        stdout = self.experimentupload_file(filename=filename)
                        #cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        #stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                        self.cluster.logger.debug(stdout)
                # get monitoring for benchmarking
                if self.monitoring_active:
                    if 'deployment' in config.deployment_infos:
                        for name, deployment in config.deployment_infos['deployment'].items():
                            print("{:30s}: needs monitoring (common metrics) for deployment {}".format(connection, name))
                            if name=='sut' and config.monitoring_sut:
                                print("{:30s}: collecting execution metrics of SUT at connection {}".format(connection, config.current_benchmark_connection))
                                config.fetch_metrics(
                                    title=f"Execution phase: SUT deployment",
                                    connection=config.current_benchmark_connection,
                                    connection_file=connection+'.config',
                                    container="dbms",
                                    #container="dbms",
                                    component=name,
                                    component_type="stream",
                                    #component_type="stream",
                                    experiment=self.code,
                                    time_start=start_time,
                                    time_end=end_time,
                                    metrics_type="metrics", # "metrics_special",
                                    pod_dashboard=pod_dashboard
                                    )
                            elif name!='sut':
                                print("{:30s}: collecting execution metrics of {} at connection {}".format(connection, name, config.current_benchmark_connection))
                                config.fetch_metrics(
                                    title=f"Execution phase: component {name}",
                                    connection=config.current_benchmark_connection,
                                    connection_file=connection+'.config',
                                    container=deployment['containers'][0], #"dbms",
                                    #container="dbms",
                                    component=name,
                                    component_type=f"{name}streaming",
                                    #component_type="stream",
                                    experiment=self.code,
                                    time_start=start_time,
                                    time_end=end_time,
                                    metrics_type="metrics",
                                    pod_dashboard=pod_dashboard
                                    )
                    if 'statefulset' in config.deployment_infos:
                        for name, statefulset in config.deployment_infos['statefulset'].items():
                            print("{:30s}: needs monitoring (custom metrics) for stateful set {}".format(connection, name))
                            print("{:30s}: collecting execution metrics of {} at connection {}".format(connection, name, config.current_benchmark_connection))
                            config.fetch_metrics(
                                title=f"Execution phase: component {name}",
                                connection=config.current_benchmark_connection,
                                connection_file=connection+'.config',
                                container="dbms",
                                component=name,
                                component_type=f"{name}streaming",
                                #component_type="stream",
                                experiment=self.code,
                                time_start=start_time,
                                time_end=end_time,
                                metrics_type=f"metrics_{name}",
                                pod_dashboard=pod_dashboard
                                )
                    if config.monitoring_sut:
                        #print("{:30s}: collecting execution metrics of SUT at connection {}".format(connection, config.current_benchmark_connection))
                        #config.fetch_metrics(
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
                            #config.fetch_metrics(
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
                        print("{:30s}: collecting metrics of benchmarker at connection {}".format(connection, config.current_benchmark_connection))
                        config.fetch_metrics(
                            title=f"Execution phase: component benchmarker",
                            connection=config.current_benchmark_connection,
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
        self.evaluator.end_benchmarking(jobname)
    def end_loading(self,
                    jobname: str) -> None:
        """
        Ends a loading job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('base.end_loading({})'.format(jobname))
        self.evaluator.end_loading(jobname)
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
        if 'sut_service' in self.workload:
            print("\n### Services")
            for c in sorted(self.workload['sut_service']):
                print(c)
                print("* {}".format(self.generate_port_forward(self.workload['sut_service'][c])))
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
                            df = self.evaluator.get_monitoring_metric(metric=metricname, component=component) # 'stream')#
                            if not df.empty:
                                list_monitoring_app
                                if metric['metric'] == 'counter':
                                    df = df.max().sort_index() - df.min().sort_index() # compute difference of counter
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
                    # currently: only first component, only stream
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
                    if i == "eval_parameters":
                        print("  * "+i)
                        infos = ["    * {}:{}".format(key,info) for key, info in parameters.items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
                        for info in infos:
                            print(info)
        return connections_sorted, monitoring_applications
    def show_summary(self):
        """
        Show a summary of an experiment of type dbmsbenchmarker.
        """
        self._test_results = []
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
                if 'timeGenerate' in connection.connectiondata:
                    times[c]['timeGenerate'] = connection.connectiondata['timeGenerate']
                if 'timeIngesting' in connection.connectiondata:
                    times[c]['timeIngesting'] = connection.connectiondata['timeIngesting']
                if 'timeSchema' in connection.connectiondata:
                    times[c]['timeSchema'] = connection.connectiondata['timeSchema']
                if 'timeIndex' in connection.connectiondata:
                    times[c]['timeIndex'] = connection.connectiondata['timeIndex']
                if 'timeLoad' in connection.connectiondata:
                    times[c]['timeLoad'] = connection.connectiondata['timeLoad']
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
            workflow_actual = evaluators.base.reconstruct_workflow(self.evaluator, df_time)
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
    def show_summary_monitoring_table(self, evaluate: object, component: str) -> list:
        """
        Build a list of DataFrames containing CPU and RAM monitoring metrics for one component.

        :param evaluate: Evaluator object exposing get_monitoring_metric().
        :param component: Component name used as the metric scope (e.g. 'loading', 'stream').
        :return: List of single-column DataFrames, one per collected metric.
        """
        df_monitoring = list()
        ##########
        df = evaluate.get_monitoring_metric(metric='total_cpu_util_s', component=component)
        df = df.max().sort_index() - df.min().sort_index() # compute difference of counter
        #df = df.T.max().sort_index() - df.T.min().sort_index() # compute difference of counter
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
        return df_monitoring
    def show_summary_monitoring(self) -> None:
        """
        Print monitoring tables for all registered monitoring components and record test results.

        Results are appended to ``self._test_results`` via :meth:`_record_test`.
        """
        if (self.monitoring_active or self.cluster.monitor_cluster_active):
            print("\n### Monitoring")
            for component, title in self.workload['monitoring_components'].items():
                df_monitoring = self.show_summary_monitoring_table(self.evaluator, component)
                if len(df_monitoring) > 0:
                    print(f"\n### {title}\n")
                    df = pd.concat(df_monitoring, axis=1).round(2)
                    df = df.reindex(index=evaluators.natural_sort(df.index))
                    df.index.names = ["DBMS"]
                    print(df.to_markdown(index=True, floatfmt=".2f"))
                    passed = self.evaluator.test_results_column(df, "CPU [CPUs]", silent=True)
                    suffix = "no 0 or NaN" if passed else "0 or NaN"
                    self._record_test(passed, f"{title} contains {suffix} in CPU [CPUs]")
    def OLD_show_summary_monitoring(self):
        test_results = ""
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        evaluate = inspector.inspector(resultfolder)
        evaluate.load_experiment(code=code, silent=True)
        if (self.monitoring_active or self.cluster.monitor_cluster_active):
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "loading")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                if not self.evaluator.test_results_column(df, "CPU [CPUs]", silent=True):
                    test_results = test_results + "TEST failed: Ingestion SUT contains 0 or NaN in CPU [CPUs]\n"
                else:
                    test_results = test_results + "TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]\n"
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "loader")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - Loader")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                if not self.evaluator.test_results_column(df, "CPU [CPUs]", silent=True):
                    test_results = test_results + "TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]\n"
                else:
                    test_results = test_results + "TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]\n"
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "stream")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                if not self.evaluator.test_results_column(df, "CPU [CPUs]", silent=True):
                    test_results = test_results + "TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]\n"
                else:
                    test_results = test_results + "TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]\n"
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "benchmarker")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - Benchmarker")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                if not self.evaluator.test_results_column(df, "CPU [CPUs]", silent=True):
                    test_results = test_results + "TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]\n"
                else:
                    test_results = test_results + "TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]\n"
                print(df)
        return test_results.rstrip('\n')












"""
############################################################################
Simple IoT example experiment
############################################################################
"""


class iot(base):
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
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
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
        self.maintaining_active = True                                  # IoT experiments always run a maintaining job alongside benchmarking
    def set_queries_full(self):
        self.set_queryfile('queries-iot.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-iot-profiling.config')
    def set_querymanagement_maintaining(self,
            numRun=128,
            delay=5,
            datatransfer=False):
        self.set_querymanagement(
            numWarmup = 0,
            numCooldown = 0,
            numRun = numRun,
            delay = delay,
            )
        #self.monitoring_active = True
        self.maintaining_active = True



"""
############################################################################
TSBS
############################################################################
"""


class tsbs(base):
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
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
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
        self.maintaining_active = True                                      # TSBS experiments always run a maintaining job alongside benchmarking
        self.jobtemplate_maintaining = "jobtemplate-maintaining-tsbs.yml"   # K8s job template for the TSBS maintaining container
    def set_queries_full(self):
        self.set_queryfile('queries-tsbs.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tsbs-profiling.config')
    def set_querymanagement_maintaining(self,
            numRun=128,
            delay=5,
            datatransfer=False):
        self.set_querymanagement(
            numWarmup = 0,
            numCooldown = 0,
            numRun = numRun,
            delay = delay,
            )
        #self.monitoring_active = True
        self.maintaining_active = True



# Example experiment class

class example(base):
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
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
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

class tpcxai(base):
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
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
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

