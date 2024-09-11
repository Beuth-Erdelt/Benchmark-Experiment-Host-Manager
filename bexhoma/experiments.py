"""
:Date: 2022-10-01
:Version: 0.6.0
:Authors: Patrick K. Erdelt

    Classes for managing an experiment.
    This is plugged into a cluster object.
    It collects some configuation objects.
    Two examples are included, dealing with TPC-H and TPC-DS tests.
    Another example concerns TSBS experiment.
    Each experiment also should have an own folder having:

    * a query file
    * a subfolder for each dbms, that may run this experiment, including schema files

    Copyright (C) 2020  Patrick K. Erdelt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from dbmsbenchmarker import parameter, tools, inspector
import logging
import urllib3
import gc
import shutil # for zipping
from os import makedirs, path
import time
import os
import subprocess
from datetime import datetime, timedelta
import re
import pandas as pd
import pickle
import json
import ast
from types import SimpleNamespace

from bexhoma import evaluators

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)



class DictToObject(object):
    """
    https://coderwall.com/p/idfiea/python-dict-to-object
    """
    def __init__(self, dictionary):
        def _traverse(key, element):
            if isinstance(element, dict):
                return key, DictToObject(element)
            else:
                return key, element
        objd = dict(_traverse(k, v) for k, v in dictionary.items())
        self.__dict__.update(objd)



class default():
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
        self.cluster = cluster
        self.code = code
        if self.code is None:
            self.code = str(round(time.time()))
        else:
            self.code = str(self.code)
        self.path = self.cluster.resultfolder+"/"+self.code
        if not path.isdir(self.path):
            makedirs(self.path)
        self.detached = detached
        self.cluster.set_code(code=self.code)
        self.set_connectionmanagement(
            numProcesses = 1,
            runsPerConnection = 0,
            timeout = timeout,
            singleConnection = True)
        self.num_experiment_to_apply = num_experiment_to_apply
        self.max_sut = None
        self.cluster.add_experiment(self)
        self.appname = self.cluster.appname
        self.resources = {}
        self.ddl_parameters = {}
        self.eval_parameters = {}
        self.storage = {}
        self.nodes = {}
        self.maintaining_parameters = {}
        self.loading_parameters = {}
        self.loading_patch = ""
        self.benchmarking_patch = ""
        self.benchmarking_parameters = {}
        self.jobtemplate_maintaining = ""
        self.jobtemplate_loading = ""
        self.querymanagement = {}
        self.additional_labels = dict()
        self.workload = {}
        self.monitoring_active = True
        self.prometheus_interval = "10s"
        self.prometheus_timeout = "10s"
        self.loading_active = False
        self.num_loading = 0
        self.num_loading_pods = 0
        self.maintaining_active = False
        self.num_maintaining = 0
        self.num_maintaining_pods = 0
        self.name_format = None
        self.script = ""
        self.initscript = []
        self.indexing = ""
        self.indexscript = []
        # k8s:
        self.namespace = self.cluster.namespace
        self.configurations = []
        self.storage_label = ''
        self.evaluator = evaluators.base(code=self.code, path=self.cluster.resultfolder, include_loading=True, include_benchmarking=True)
    def prepare_testbed(self, parameter):
        args = SimpleNamespace(**parameter)
        numRun = int(args.num_run)
        datatransfer = args.datatransfer
        num_experiment_to_apply = int(args.num_config)
        # configure number of clients per config
        list_clients = args.num_query_executors.split(",")
        if len(list_clients) > 0:
            list_clients = [int(x) for x in list_clients if len(x) > 0]
        else:
            list_clients = []
        monitoring = args.monitoring
        monitoring_cluster = args.monitoring_cluster
        #num_loading = int(args.num_loading)
        num_loading_split = args.num_loading_split
        if len(num_loading_split) > 0:
            num_loading = num_loading_split.split(",")
            list_loading_split = [int(x) for x in num_loading]
        #num_loading_pods = int(args.num_loading_pods)
        num_loading_pods = args.num_loading_pods
        if len(num_loading_pods) > 0:
            num_loading_pods = num_loading_pods.split(",")
            num_loading_pods = [int(x) for x in num_loading_pods]
        num_loading_threads = args.num_loading_threads
        if len(num_loading_threads) > 0:
            num_loading_threads = num_loading_threads.split(",")
            num_loading_threads = [int(x) for x in num_loading_threads]
        num_benchmarking_pods = args.num_benchmarking_pods
        if len(num_benchmarking_pods) > 0:
            num_benchmarking_pods = num_benchmarking_pods.split(",")
            num_benchmarking_pods = [int(x) for x in num_benchmarking_pods]
        num_benchmarking_threads = args.num_benchmarking_threads
        if len(num_benchmarking_threads) > 0:
            num_benchmarking_threads = num_benchmarking_threads.split(",")
            num_benchmarking_threads = [int(x) for x in num_benchmarking_threads]
        cpu = str(args.request_cpu)
        memory = str(args.request_ram)
        cpu_type = str(args.request_cpu_type)
        gpu_type = str(args.request_gpu_type)
        gpus = str(args.request_gpu)
        request_storage_type = args.request_storage_type
        request_storage_size = args.request_storage_size
        request_node_name = args.request_node_name
        request_node_loading = args.request_node_loading
        request_node_benchmarking = args.request_node_benchmarking
        self.cluster.start_datadir()
        self.cluster.start_resultdir()
        self.cluster.start_dashboard()
        self.cluster.start_messagequeue()
        if monitoring_cluster:
            # monitor all nodes of cluster (for not missing any component)
            self.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
            self.cluster.start_monitoring_cluster()
            self.workload['info'] = self.workload['info']+"\nSystem metrics are monitored by a cluster-wide installation."
        elif monitoring:
            # we want to monitor resource consumption
            self.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
            self.workload['info'] = self.workload['info']+"\nSystem metrics are monitored by sidecar containers."
        else:
            # we want to just run the queries
            self.set_querymanagement_quicktest(numRun=numRun, datatransfer=datatransfer)
        # set resources for dbms
        self.set_resources(
            requests = {
                'cpu': cpu,
                'memory': memory,
                'gpu': 0
            },
            limits = {
                'cpu': 0,
                'memory': 0
            },
            nodeSelector = {
                'cpu': cpu_type,
                'gpu': '',
            })
        # persistent storage
        self.set_storage(
            storageClassName = request_storage_type,
            storageSize = request_storage_size,#'100Gi',
            keep = True
            )
        # note more infos about experiment in workload description
        if len(args.dbms):
            # import is limited to single DBMS
            self.workload['info'] = self.workload['info']+"\nBenchmark is limited to DBMS {}.".format(", ".join(args.dbms))
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
        if request_storage_type and request_storage_size:
            self.workload['info'] = self.workload['info']+"\nDatabase is persisted to disk of type {} and size {}.".format(request_storage_type, request_storage_size)
        self.workload['info'] = self.workload['info']+"\nLoading is tested with {} threads, split into {} pods.".format(num_loading_threads, num_loading_pods)
        self.workload['info'] = self.workload['info']+"\nBenchmarking is tested with {} threads, split into {} pods.".format(num_benchmarking_threads, num_benchmarking_pods)
        self.workload['info'] = self.workload['info']+"\nBenchmarking is run as {} times the number of benchmarking pods.".format(list_clients)
        if num_experiment_to_apply > 1: 
            self.workload['info'] = self.workload['info']+"\nExperiment is run {} times.".format(num_experiment_to_apply)
        else:
            self.workload['info'] = self.workload['info']+"\nExperiment is run once."
    def test_results(self):
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
    def test_results_in_dashboard(self):
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
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['test_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
            try:
                if len(stdout) > 0:
                    print(stdout)
                    return int(stdout.splitlines()[-1:][0])
                else:
                    return 1
            except Exception as e:
                return 1
            finally:
                return 1
        return 1
    def wait(self, sec, silent=False):
        """
        Function for waiting some time and inform via output about this

        :param sec: Number of seconds to wait
        :param silent: True means we do not output anything about this waiting
        """
        #+print("Waiting "+str(sec)+"s...", end="", flush=True)
        #intervals = int(sec)
        #time.sleep(intervals)
        #print("done")
        return self.cluster.wait(sec, silent)
    def delay(self, sec, silent=False):
        """
        Function for waiting some time and inform via output about this.
        Synonymous for wait()

        :param sec: Number of seconds to wait
        :param silent: True means we do not output anything about this waiting
        """
        self.wait(sec, silent)
    def set_queryfile(self, queryfile):
        """
        Sets the name of a query file of the experiment.
        This is for the benchmarker component (dbmsbenchmarker).

        :param code: Unique identifier of an experiment
        """
        self.queryfile = queryfile
    def set_experiments_configfolder(self, experiments_configfolder):
        """
        Sets the configuration folder for the experiment.
        Bexhoma expects subfolders for expeiment types, for example tpch.
        In there, bexhoma looks for query.config files (for dbmsbenchmarker) and subfolders containing the schema per dbms.

        :param experiments_configfolder: Relative path to an experiment folder
        """
        self.experiments_configfolder = experiments_configfolder
    def set_additional_labels(self, **kwargs):
        """
        Sets additional labels, that will be put to K8s objects (and ignored otherwise).
        This is for the SUT component.
        Can be overwritten by configuration.

        :param kwargs: Dict of labels, example 'SF' => 100
        """
        self.additional_labels = {**self.additional_labels, **kwargs}
    def set_workload(self, **kwargs):
        """
        Sets mata data about the experiment, for example name and description.

        :param kwargs: Dict of meta data, example 'name' => 'TPC-H'
        """
        self.workload = kwargs
    def set_querymanagement(self, **kwargs):
        """
        Sets query management data for the experiment.
        This is for the benchmarker component (dbmsbenchmarker).

        :param kwargs: Dict of meta data, example 'numRun' => 3
        """
        self.querymanagement = kwargs
    # the following can be overwritten by configuration
    def set_connectionmanagement(self, **kwargs):
        """
        Sets connection management data for the experiment.
        This is for the benchmarker component (dbmsbenchmarker).
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'timout' => 60
        """
        self.connectionmanagement = kwargs
    def set_resources(self, **kwargs):
        """
        Sets resources for the experiment.
        This is for the SUT component.
        Can be overwritten by experiment and configuration.

        :param kwargs: Dict of meta data, example 'requests' => {'cpu' => 4}
        """
        self.resources = {**self.resources, **kwargs}
    def set_ddl_parameters(self, **kwargs):
        """
        Sets DDL parameters for the experiments.
        This substitutes placeholders in DDL script.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'index' => 'btree'
        """
        self.ddl_parameters = kwargs
    def set_eval_parameters(self, **kwargs):
        """
        Sets some arbitrary parameters that are supposed to be handed over to the benchmarker component.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'type' => 'noindex'
        """
        self.eval_parameters = kwargs
    def set_storage(self, **kwargs):
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
    def set_nodes(self, **kwargs):
        self.nodes = kwargs
    def set_maintaining_parameters(self, **kwargs):
        """
        Sets ENV for maintaining components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.maintaining_parameters = kwargs
    def set_maintaining(self, parallel, num_pods=None):
        """
        Sets job parameters for maintaining components: Number of parallel pods and optionally (if different) total number of pods.
        By default total number of pods is set to number of parallel pods.
        Can be overwritten by configuration.

        :param parallel: Number of parallel pods
        :param num_pods: Optionally (if different) total number of pods
        """
        self.num_maintaining = int(parallel)
        if not num_pods is None:
            self.num_maintaining_pods = int(num_pods)
        else:
            self.num_maintaining_pods = int(parallel)
        # total number at least number of parallel
        if self.num_maintaining_pods < self.num_maintaining:
            self.num_maintaining_pods = self.num_maintaining
    def set_loading_parameters(self, **kwargs):
        """
        Sets ENV for loading components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.loading_parameters = kwargs
    def patch_loading(self, patch):
        """
        Patches YAML of loading components.
        Can be overwritten by configuration.

        :param patch: String in YAML format, overwrites basic YAML file content
        """
        self.loading_patch = patch
    def patch_benchmarking(self, patch):
        """
        Patches YAML of loading components.
        Can be set by experiment before creation of configuration.

        :param patch: String in YAML format, overwrites basic YAML file content
        """
        self.benchmarking_patch = patch
    def set_loading(self, parallel, num_pods=None):
        """
        Sets job parameters for loading components: Number of parallel pods and optionally (if different) total number of pods.
        By default total number of pods is set to number of parallel pods.
        Can be overwritten by configuration.

        :param parallel: Number of parallel pods
        :param num_pods: Optionally (if different) total number of pods
        """
        self.num_loading = int(parallel)
        if not num_pods is None:
            self.num_loading_pods = int(num_pods)
        else:
            self.num_loading_pods = int(parallel)
        # total number at least number of parallel
        if self.num_loading_pods < self.num_loading:
            self.num_loading_pods = self.num_loading
    def set_benchmarking_parameters(self, **kwargs):
        """
        Sets ENV for benchmarking components.
        Can be overwritten by configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.benchmarking_parameters = kwargs
    def add_configuration(self, configuration):
        """
        Adds a configuration object to the list of configurations of this experiment.
        When a new configuration object is instanciated, an experiment object has to be provided.
        This method is then called automatically.

        :param configuration: Configuration object
        """
        self.configurations.append(configuration)
    def set_querymanagement_quicktest(self,
            numRun=1,
            datatransfer=False):
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
            numRun=256,
            delay=10,
            datatransfer=False):
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
    def set_experiment(self, instance=None, volume=None, docker=None, script=None, indexing=None):
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
    def evaluate_results(self, pod_dashboard=''):
        """
        Let the dashboard pod build the evaluations.
        This is specific to dbmsbenchmarker.

        1) All local logs are copied to the pod.
        2) Benchmarker in the dashboard pod is updated (dev channel)
        3) All results of all DBMS are joined (merge.py of benchmarker) in dashboard pod
        4) Evaluation cube is built (python benchmark.py read -e yes) in dashboard pod
        """
        if len(pod_dashboard) == 0:
            pod_dashboard = self.cluster.get_dashboard_pod_name(component='dashboard')
            if len(pod_dashboard) > 0:
                #pod_dashboard = pods[0]
                status = self.cluster.get_pod_status(pod_dashboard)
                print(pod_dashboard, status)
                while status != "Running":
                    self.wait(10)
                    status = self.cluster.get_pod_status(pod_dashboard)
                    print(pod_dashboard, status)
        # copy logs and yamls to result folder
        print("Copy configuration and logs", end="", flush=True)
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".log") or filename.endswith(".yml") or filename.endswith(".error") or filename.endswith(".pickle"): 
                self.cluster.kubectl('cp '+self.path+"/"+filename+' '+pod_dashboard+':/results/'+str(self.code)+'/'+filename+' -c dashboard')
                print(".", end="", flush=True)
        print("done!")
        cmd = {}
        cmd['update_dbmsbenchmarker'] = 'git pull'#/'+str(self.code)
        self.cluster.execute_command_in_pod(command=cmd['update_dbmsbenchmarker'], pod=pod_dashboard, container="dashboard")
        print("Join results ", end="", flush=True)
        cmd['merge_results'] = 'python merge.py -r /results/ -c '+str(self.code)
        self.cluster.execute_command_in_pod(command=cmd['merge_results'], pod=pod_dashboard, container="dashboard")
        print("done!")
        print("Build evaluation cube ", end="", flush=True)
        cmd['evaluate_results'] = 'python benchmark.py read -e yes -r /results/'+str(self.code)
        self.cluster.execute_command_in_pod(command=cmd['evaluate_results'], pod=pod_dashboard, container="dashboard")
        print("done!")
        # download evaluation cubes
        #print("{:30s}: downloading partial results".format("Experiment"))
        #print("{:30s}: uploading full results".format("Experiment"))
        filename = 'evaluation.json'
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/'+filename, to=self.path+"/"+filename)
        self.cluster.kubectl(cmd['download_results'])
        filename = 'evaluation.dict'
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/'+filename, to=self.path+"/"+filename)
        self.cluster.kubectl(cmd['download_results'])
        filename = 'connections.config'
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/'+filename, to=self.path+"/"+filename)
        self.cluster.kubectl(cmd['download_results'])
        filename = 'queries.config'
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/'+filename, to=self.path+"/"+filename)
        self.cluster.kubectl(cmd['download_results'])
        filename = 'protocol.json'
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/'+filename, to=self.path+"/"+filename)
        self.cluster.kubectl(cmd['download_results'])
        # download complete result folder of experiment from pod
        # this includes all measures like times and monitoring data
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/', to=self.path+"/")
        self.cluster.kubectl(cmd['download_results'])
        ############ HammerDB
        #self.path = "/home/perdelt/benchmarks/1668286639/"
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".pickle"): 
                df = pd.read_pickle(self.path+"/"+filename)
                print(self.path+"/"+filename, df)
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
    def stop_benchmarker(self, configuration=''):
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
    def start_sut(self):#, configuration=None):
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
    def add_benchmark_list(self, list_clients):
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
        workflow = {}
        for configuration in self.configurations:
            workflow[configuration.configuration] = [configuration.benchmark_list_template for i in range(configuration.num_experiment_to_apply)]
        self.cluster.logger.debug('default.get_workflow_list({})'.format(workflow))
        #print(workflow)
        return workflow
    def work_benchmark_list(self, intervals=30, stop=True):
        """
        Run typical workflow:

        1) start SUT
        2) start monitoring
        3) start loading (at first scripts (schema or loading via pull), then optionally parallel loading pods)
        4) optionally start maintaining pods
        5) at the same time as 4. run benchmarker jobs corresponding to list given via add_benchmark_list()

        :param intervals: Seconds to wait before checking change of status
        :param stop: Tells if SUT should be removed when all benchmarking has finished. Set to False if we want to have loaded SUTs for inspection.
        """
        # test if there is a Pometheus server running in the cluster
        if self.cluster.test_if_monitoring_healthy():
            self.cluster.monitor_cluster_exists = True
            print("{:30s}: is running".format("Cluster monitoring"))
        else:
            self.cluster.monitor_cluster_exists = False
        do = True
        while do:
            #time.sleep(intervals)
            self.wait(intervals)
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
                    if config.sut_is_running():
                        print("{:30s}: is not loaded yet".format(config.configuration))
                    if len(config.benchmark_list) > 0:
                        if config.monitoring_active and not config.monitoring_is_running():
                            print("{:30s}: waits for monitoring".format(config.configuration))
                            if not config.monitoring_is_pending():
                                config.start_monitoring()
                            continue
                    now = datetime.utcnow()
                    if config.loading_after_time is not None:
                        if now >= config.loading_after_time:
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
                        config.loading_after_time = now + timedelta(seconds=delay)
                        print("{:30s}: will start loading but not before {} (that is in {} secs)".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S'), delay))
                        continue
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
                # start benchmarking, if loading is done and monitoring is ready
                if config.loading_finished:
                    now = datetime.utcnow()
                    # when loaded from PVC, system may not be ready yet
                    if config.loading_after_time is None:
                        # we have started from PVC
                        delay = 60
                        if 'delay_prepare' in config.dockertemplate:
                            # config demands other delay
                            delay = config.dockertemplate['delay_prepare']
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
                            print("{:30s}: benchmarks done {} of {}. This will be client {}".format(config.configuration, config.num_experiment_to_apply_done, config.num_experiment_to_apply, client))
                            if len(config.benchmarking_parameters_list) > 0:
                                benchmarking_parameters = config.benchmarking_parameters_list.pop(0)
                                print("{:30s}: we will change parameters of benchmark as {}".format(config.configuration, benchmarking_parameters))
                                config.set_benchmarking_parameters(**benchmarking_parameters)
                            if config.num_experiment_to_apply > 1:
                                connection=config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-'+client
                            else:
                                connection=config.configuration+'-'+client
                            print("{:30s}: start benchmarking".format(connection))
                            config.run_benchmarker_pod(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism)
                            #config.run_benchmarker_pod_hammerdb(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism)
                        else:
                            # no list element left
                            if stop:
                                print("{:30s}: can be stopped".format(config.configuration))
                                app = self.cluster.appname
                                component = 'sut'
                                pods = self.cluster.get_pods(app, component, self.code, config.configuration)
                                if len(pods) > 0:
                                    pod_sut = pods[0]
                                    self.cluster.store_pod_log(pod_sut, 'dbms')
                                config.stop_sut()
                                config.num_experiment_to_apply_done = config.num_experiment_to_apply_done + 1
                                if config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                                    while config.sut_is_existing():
                                        print("{:30s}: still being removed".format(config.configuration))
                                        self.wait(30)
                                    print("{:30s}: starts again".format(config.configuration))
                                    config.benchmark_list = config.benchmark_list_template.copy()
                                    config.benchmarking_parameters_list = config.benchmarking_parameters_list_template.copy()
                                    # wait for PV to be gone completely
                                    #self.wait(60)
                                    config.reset_sut()
                                    config.start_sut()
                                    self.wait(10)
                                else:
                                    config.experiment_done = True
                            else:
                                print("{} can be stopped, but we leave it running".format(config.configuration))
                else:
                    print("{:30s}: is loading".format(config.configuration))
            # all jobs of configuration - benchmarker
            #app = self.cluster.appname
            #component = 'benchmarker'
            #configuration = ''
            #jobs = self.cluster.get_jobs(app, component, self.code, configuration)
            # success of job
            app = self.cluster.appname
            component = 'benchmarker'
            configuration = ''
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
                                self.cluster.logger.debug("Store logs of job {} pod {} container {}".format(job, p, container))
                                self.cluster.store_pod_log(p, container)
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
                                self.cluster.logger.debug("Store logs of job {} pod {} container {}".format(job, p, container))
                                self.cluster.store_pod_log(p, container)
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
                    if not config.loading_started:
                        self.cluster.logger.debug("{} not loaded".format(config.configuration))
                        do = True
                    if len(config.benchmark_list) > 0:
                        self.cluster.logger.debug("{} still benchmarks to run: {}".format(config.configuration, config.benchmark_list))
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
                        self.cluster.delete_pod(p)
                    if status == 'Failed':
                        #if status != 'Running':
                        self.cluster.store_pod_log(p)
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
    def get_job_timing_benchmarking(self, jobname):
        timing_benchmarker = self.extract_job_timing(jobname, container="dbmsbenchmarker")
        return timing_benchmarker
    def get_job_timing_loading(self, jobname):
        timing_datagenerator = self.extract_job_timing(jobname, container="datagenerator")
        timing_sensor = self.extract_job_timing(jobname, container="sensor")
        timing_total = timing_datagenerator + timing_sensor
        return timing_datagenerator, timing_sensor, timing_total
        #return total_time, generator_time, loader_time
    def extract_job_timing(self, jobname, container):
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
                (timing_start, timing_end) = get_job_timing(self.path+"/"+filename)
                self.cluster.logger.debug("Found times {times}".format(times=(timing_start, timing_end)))
                if (timing_start, timing_end) == (0,0):
                    print("Error in "+filename)
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
    def end_benchmarking(self, jobname, config=None):
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        :param config: Configuration object
        """
        self.cluster.logger.debug('default.end_benchmarking({})'.format(jobname))
        # mark pod with new end time and duration
        job_labels = self.cluster.get_jobs_labels(app=self.cluster.appname, component='benchmarker', experiment=self.code)
        if len(job_labels) > 0 and len(job_labels[jobname]) > 0:
            # get pairs (start,end) of benchmarking pods
            timing_benchmarker = self.get_job_timing_benchmarking(jobname)
            if config is not None:
                config.benchmarking_timespans = {}
                config.benchmarking_timespans['benchmarker'] = timing_benchmarker
            start_time = int(job_labels[jobname]['start_time'])
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
            end_time = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
            print("{:30s}: showing benchmarker times".format(connection))
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
                        cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                        self.cluster.logger.debug(stdout)
                # get monitoring for loading
                if self.monitoring_active:
                    print("{:30s}: collecting execution metrics of SUT".format(connection))
                    cmd['fetch_benchmarking_metrics'] = 'python metrics.py -r /results/ -db -ct stream -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, connection+'.config', '/results/'+self.code, self.code, start_time, end_time)
                    #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                    stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['fetch_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
                    self.cluster.logger.debug(stdout)
                    self.cluster.logger.debug(stderr)
                    # upload connections infos again, metrics has overwritten it
                    filename = 'connections.config'
                    cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                    stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                    self.cluster.logger.debug(stdout)
                    # get metrics of benchmarker components
                    # only if general monitoring is on
                    endpoints_cluster = self.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
                    if len(endpoints_cluster)>0 or self.cluster.monitor_cluster_exists:
                        print("{:30s}: collecting metrics of benchmarker".format(connection))
                        cmd['fetch_benchmarker_metrics'] = 'python metrics.py -r /results/ -db -ct benchmarker -cn dbmsbenchmarker -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, connection+'.config', '/results/'+self.code, self.code, start_time, end_time)
                        #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                        stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['fetch_benchmarker_metrics'], pod=pod_dashboard, container="dashboard")
                        self.cluster.logger.debug(stdout)
                        self.cluster.logger.debug(stderr)
                        # upload connections infos again, metrics has overwritten it
                        filename = 'connections.config'
                        cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        stdout = self.cluster.kubectl(cmd['upload_connection_file'])
                        self.cluster.logger.debug(stdout)
        self.evaluator.end_benchmarking(jobname)
    def end_loading(self, jobname):
        """
        Ends a loading job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('default.end_loading({})'.format(jobname))
        self.evaluator.end_loading(jobname)
    def show_summary(self):
        self.cluster.logger.debug('default.show_summary()')
        print("\n## Show Summary")
        pd.set_option("display.max_rows", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        with open(resultfolder+"/"+code+"/queries.config",'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
        print("\n### Workload\n    "+workload_properties['name'])
        print("    "+workload_properties['intro'])
        print("    "+workload_properties['info'])
        print("\n### Connections")
        with open(resultfolder+"/"+code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
        pretty_connections = json.dumps(connections, indent=2)
        #print(pretty_connections)
        connections_sorted = sorted(connections, key=lambda c: c['name'])
        for c in connections_sorted:
            print(c['name'],
                  "uses docker image",
                  c['parameter']['dockerimage'])
            infos = ["    {}:{}".format(key,info) for key, info in c['hostsystem'].items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
            for info in infos:
                print(info)
        evaluation = evaluators.base(code=code, path=resultfolder)
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
        print("\n### Errors (failed queries)")
        df = evaluate.get_total_errors().T
        num_errors = df.sum().sum()
        if num_errors > 0:
            df.index = df.index.map(map_index_to_queryname)
            print(df)
        else:
            print("No errors")
        #####################
        print("\n### Warnings (result mismatch)")
        df = evaluate.get_total_warnings().T
        num_warnings = df.sum().sum()
        if num_warnings > 0:
            df.index = df.index.map(map_index_to_queryname)
            print(df)
        else:
            print("No warnings")
        #####################
        print("\n### Latency of Timer Execution [ms]")
        df = evaluate.get_aggregated_query_statistics(type='latency', name='execution', query_aggregate='Mean')
        if not df is None:
            df = df.sort_index().T.round(2)
            df.index = df.index.map(map_index_to_queryname)
            print(df)
        #####################
        print("\n### Loading [s]")
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
        print(df.round(2).T)
        #####################
        print("\n### Geometric Mean of Medians of Timer Run [s]")
        df = evaluate.get_aggregated_experiment_statistics(type='timer', name='run', query_aggregate='Median', total_aggregate='Geo')
        df = (df/1000.0).sort_index()
        df.columns = ['Geo Times [s]']
        df_geo_mean_runtime = df.copy()
        print(df.round(2))
        #####################
        print("\n### Power@Size")
        df = evaluate.get_aggregated_experiment_statistics(type='timer', name='execution', query_aggregate='Median', total_aggregate='Geo')
        df = (df/1000.0).sort_index().astype('float')
        df = float(parameter.defaultParameters['SF'])*3600./df
        df.columns = ['Power@Size [~Q/h]']
        df_power = df.copy()
        print(df.round(2))
        #####################
        # aggregate time and throughput for parallel pods
        print("\n### Throughput@Size")
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
            df_time['orig_name'] = orig_name
            df_time['SF'] = int(c['parameter']['connection_parameter']['loading_parameters']['SF'])
            df_time['pods'] = int(c['parameter']['connection_parameter']['loading_parameters']['PODS_PARALLEL'])
            #df_time['threads'] = int(c['parameter']['connection_parameter']['loading_parameters']['MYSQL_LOADING_THREADS'])
            df_time['num_experiment'] = int(c['parameter']['numExperiment'])
            df_time['num_client'] = int(c['parameter']['client'])
            df_time['benchmark_start'] = eva['times']['total'][c['name']]['time_start']
            df_time['benchmark_end'] = eva['times']['total'][c['name']]['time_end']
            df_merged_time = pd.concat([df_merged_time, df_time])
        df_time = df_merged_time.sort_index()
        benchmark_start = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client']).min('benchmark_start')
        benchmark_end = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client']).max('benchmark_end')
        df_benchmark = pd.DataFrame(benchmark_end['benchmark_end'] - benchmark_start['benchmark_start'])
        df_benchmark.columns = ['time [s]']
        benchmark_count = df_time.groupby(['orig_name', 'SF', 'num_experiment', 'num_client']).count()
        df_benchmark['count'] = benchmark_count['benchmark_end']
        df_benchmark['SF'] = df_benchmark.index.map(lambda x: x[1])
        df_benchmark['Throughput@Size [~GB/h]'] = (22*3600*df_benchmark['count']/df_benchmark['time [s]']*df_benchmark['SF']).round(2)
        index_names = list(df_benchmark.index.names)
        index_names[0] = "DBMS"
        df_benchmark.rename_axis(index_names, inplace=True)
        print(df_benchmark)
        #####################
        self.show_summary_monitoring()
        evaluation.test_results_column(df_geo_mean_runtime, "Geo Times [s]")
        evaluation.test_results_column(df_power, "Power@Size [~Q/h]")
        evaluation.test_results_column(df_benchmark, "Throughput@Size [~GB/h]")
    def show_summary_monitoring_table(self, evaluate, component):
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
    def show_summary_monitoring(self):
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
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "loader")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - Loader")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "stream")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluate, "benchmarker")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - Benchmarker")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)



"""
############################################################################
Some more concrete implementations
############################################################################
"""



"""
############################################################################
TPC-DS
############################################################################
"""



class tpcds(default):
    """
    Class for defining an TPC-DS experiment.
    This sets
    
    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-tpcds.config',
            SF = '100',
            num_experiment_to_apply = 1,
            timeout = 7200,
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='tpcds')
        self.set_experiment(script='SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/tpcds')
        self.set_queryfile(queryfile)
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_workload(
            name = 'TPC-DS Queries SF='+str(SF),
            info = 'This experiment performs some TPC-DS inspired queries.'
            )
        self.storage_label = 'tpcds-'+str(SF)
    def set_queries_full(self):
        self.set_queryfile('queries-tpcds.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tpcds-profiling.config')


"""
############################################################################
TPC-H
############################################################################
"""

class tpch(default):
    """
    Class for defining an TPC-H experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-tpch.config',
            SF = '100',
            num_experiment_to_apply = 1,
            timeout = 7200,
            script=None
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        if script is None:
            script = 'SF'+str(SF)+'-index'
        self.set_experiment(volume='tpch')
        self.set_experiment(script=script)
        self.cluster.set_experiments_configfolder('experiments/tpch')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_additional_labels(SF=SF)
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'TPC-H Queries SF='+str(SF),
            info = 'This experiment performs some TPC-H inspired queries.'
            )
        self.storage_label = 'tpch-'+str(SF)
    def set_queries_full(self):
        self.set_queryfile('queries-tpch.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tpch-profiling.config')



"""
############################################################################
TPC-C
############################################################################
"""

class tpcc(default):
    """
    Class for defining an TPC-C experiment (in the HammerDB version).
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor), i.e. number of warehouses
    """
    def __init__(self,
            cluster,
            code=None,
            #queryfile = 'queries-tpch.config',
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='tpcc')
        self.set_experiment(script='Schema')#SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/tpcc')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'TPC-C Queries SF='+str(SF),
            info = 'This experiment performs some TPC-C inspired workloads.'
            )
        self.storage_label = 'hammerdb-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-hammerdb.yml"
        self.evaluator = evaluators.tpcc(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('tpcc.test_results()')
        self.evaluator.test_results()
        workflow = self.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
    def evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to HammerDB.
        """
        self.cluster.logger.debug('tpcc.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        if len(pod_dashboard) == 0:
            pod_dashboard = self.cluster.get_dashboard_pod_name(component='dashboard')
            if len(pod_dashboard) > 0:
                #pod_dashboard = pods[0]
                status = self.cluster.get_pod_status(pod_dashboard)
                print(pod_dashboard, status)
                while status != "Running":
                    self.wait(10)
                    status = self.cluster.get_pod_status(pod_dashboard)
                    print(pod_dashboard, status)
        if self.monitoring_active:
            cmd = {}
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loading -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct stream -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loader -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct benchmarker -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
        # copy logs and yamls to result folder
        #print("Copy configuration and logs", end="", flush=True)
        #directory = os.fsencode(self.path)
        #for file in os.listdir(directory):
        #    filename = os.fsdecode(file)
        #    if filename.endswith(".log") or filename.endswith(".yml") or filename.endswith(".error") or filename.endswith(".pickle"): 
        #        self.cluster.kubectl('cp '+self.path+"/"+filename+' '+pod_dashboard+':/results/'+str(self.code)+'/'+filename+' -c dashboard')
        #        print(".", end="", flush=True)
        #print("done!")
        cmd = {}
        #cmd['update_dbmsbenchmarker'] = 'git pull'#/'+str(self.code)
        #self.cluster.execute_command_in_pod(command=cmd['update_dbmsbenchmarker'], pod=pod_dashboard, container="dashboard")
        #print("Join results ", end="", flush=True)
        #cmd['merge_results'] = 'python merge.py -r /results/ -c '+str(self.code)
        #self.cluster.execute_command_in_pod(command=cmd['merge_results'], pod=pod_dashboard, container="dashboard")
        #print("done!")
        #print("Build evaluation cube ", end="", flush=True)
        #cmd['evaluate_results'] = 'python benchmark.py read -e yes -r /results/'+str(self.code)
        #self.cluster.execute_command_in_pod(command=cmd['evaluate_results'], pod=pod_dashboard, container="dashboard")
        #print("done!")
        # download all results from cluster
        #filename = 'evaluation.json'
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/', to=self.path+"/")
        self.cluster.kubectl(cmd['download_results'])
        cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/', from_file=self.path+"/")
        #cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/', from_file=self.path+"/")
        self.cluster.kubectl(cmd['upload_results'])
    def show_summary(self):
        #print('tpcc.show_summary()')
        print("\n## Show Summary")
        pd.set_option("display.max_rows", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        with open(resultfolder+"/"+code+"/queries.config",'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
        print("\n### Workload\n    "+workload_properties['name'])
        print("    "+workload_properties['intro'])
        print("    "+workload_properties['info'])
        print("\n### Connections")
        with open(resultfolder+"/"+code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
        pretty_connections = json.dumps(connections, indent=2)
        #print(pretty_connections)
        connections_sorted = sorted(connections, key=lambda c: c['name'])
        for c in connections_sorted:
            print(c['name'],
                  "uses docker image",
                  c['parameter']['dockerimage'])
            infos = ["    {}:{}".format(key,info) for key, info in c['hostsystem'].items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
            for info in infos:
                print(info)
        #print("found", len(connections), "connections")
        #evaluate = inspector.inspector(resultfolder)       # no evaluation cube
        #evaluate.load_experiment(code=code, silent=False)
        evaluation = evaluators.tpcc(code=code, path=resultfolder)
        #####################
        df = evaluation.get_df_loading()
        if not df.empty:
            print("\n### Loading")
            print(df)
            #df = df.sort_values(['configuration','experiment_run','client'])
            #df = df[df.columns.drop(list(df.filter(regex='FAILED')))]
            #print(df)
            #print(df.columns)
            #df_plot = evaluation.loading_set_datatypes(df)
            #df_aggregated = evaluation.loading_aggregate_by_parallel_pods(df_plot)
            #df_aggregated.sort_values(['experiment_run','target','pod_count'], inplace=True)
            #df_aggregated = df_aggregated[['experiment_run',"threads","target","pod_count","[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)"]]
            #print(df_aggregated)
        #####################
        df = evaluation.get_df_benchmarking()
        warehouses = 0
        df = evaluation.get_df_benchmarking()
        if not df.empty:
            print("\n### Execution")
            #print(df)
            warehouses = int(df['sf'].max())
            df.fillna(0, inplace=True)
            df_plot = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df_plot)
            df_aggregated = df_aggregated.sort_values(['experiment_run','client','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"vusers","client","pod_count"]].copy()
            columns = ["NOPM", "TPM", "duration", "errors"]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            print(df_aggregated_reduced)
        print("\nWarehouses:", warehouses)
        #####################
        workflow = evaluation.reconstruct_workflow(df)
        if len(workflow) > 0:
            print("\n### Workflow")
            for c in workflow:
                print("DBMS", c, "- Pods", workflow[c])
        #####################
        print("\n### Loading")
        #connections_sorted = sorted(connections, key=lambda c: c['name']) 
        result = dict()
        for c in connections_sorted:
            #print(c)
            """
            print(c['name'], 
                  c['timeLoad'], 
                  '[s] for', 
                  c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS'], 
                  'threads on',
                  c['hostsystem']['node'])
            """
            result[c['name']] = {
                'time_load': c['timeIngesting'],
                #'terminals': c['parameter']['connection_parameter']['loading_parameters']['HAMMERDB_VUSERS'], # these are the benchmark clients
                'terminals': c['parameter']['connection_parameter']['loading_parameters']['PARALLEL'],
                #'target': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TARGET'],
                'pods': c['parameter']['parallelism'],
            }
            #result[c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS']] = c['timeIngesting']
        df = pd.DataFrame(result)#, index=['time_load'])#, index=result.keys())
        #print(df)
        #df = df.T.pivot(columns='terminals', index='target', values='time_load')
        df_connections = df.copy().T
        #print(df_connections)
        df_time_load = pd.DataFrame(df_connections['time_load'], columns=['time_load'])
        df_tpx = (warehouses*3600.0)/df_time_load.sort_index()
        #print(df_tpx)
        #df_loading_tpx = df_tpx['time_load']
        df_connections['Imported warehouses [1/h]'] = df_tpx['time_load']
        print(df_connections)
        #####################
        self.show_summary_monitoring()
        evaluation.test_results_column(df_aggregated_reduced, "NOPM")
    def show_summary_monitoring(self):
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        evaluation = evaluators.tpcc(code=code, path=resultfolder)
        if (self.monitoring_active or self.cluster.monitor_cluster_active):
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "loading")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "loader")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - Loader")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "stream")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "benchmarker")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - Benchmarker")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)




"""
############################################################################
Simple IoT example experiment
############################################################################
"""


class iot(default):
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
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='iot')
        self.set_experiment(script='SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/iot')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'IoT Queries SF='+str(SF),
            info = 'This experiment performs some IoT inspired queries.'
            )
        self.storage_label = 'tpch-'+str(SF)
        self.maintaining_active = True
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


class tsbs(default):
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
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='tsbs')
        self.set_experiment(script='SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/tsbs')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'TSBS Queries SF='+str(SF),
            info = 'This experiment performs some TSBS inspired queries.'
            )
        self.storage_label = 'tsbs-'+str(SF)
        self.maintaining_active = True
        self.jobtemplate_maintaining = "jobtemplate-maintaining-tsbs.yml"
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



"""
############################################################################
YCSB
############################################################################
"""

class ycsb(default):
    """
    Class for defining an YCSB experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor), i.e. number of rows divided by 10.000
    """
    def __init__(self,
            cluster,
            code=None,
            #queryfile = 'queries-tpch.config',
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='ycsb')
        self.set_experiment(script='Schema')#SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/ycsb')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'YCSB Queries SF='+str(SF),
            info = 'This experiment performs some YCSB inspired workloads.'
            )
        self.storage_label = 'ycsb-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-ycsb.yml"
        self.evaluator = evaluators.ycsb(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('ycsb.test_results()')
        self.evaluator.test_results()
        workflow = self.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
    def evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to YCSB.
        """
        self.cluster.logger.debug('ycsb.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        # download results
        if len(pod_dashboard) == 0:
            pod_dashboard = self.cluster.get_dashboard_pod_name(component='dashboard')
            if len(pod_dashboard) > 0:
                #pod_dashboard = pods[0]
                status = self.cluster.get_pod_status(pod_dashboard)
                print(pod_dashboard, status)
                while status != "Running":
                    self.wait(10)
                    status = self.cluster.get_pod_status(pod_dashboard)
                    print(pod_dashboard, status)
        if self.monitoring_active:
            cmd = {}
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loading -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct stream -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loader -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct benchmarker -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
        cmd = {}
        #stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/connections.config '+pod_dashboard+':/results/'+str(self.code)+'/connections.config')
        #self.logger.debug('copy config connections.config: {}'.format(stdout))
        #cmd['upload_config'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/connections.config', from_file=self.path+"/connections.config")
        #self.cluster.kubectl(cmd['upload_config'])
        print("{:30s}: downloading partial results".format("Experiment"))
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/', to=self.path+"/")
        self.cluster.kubectl(cmd['download_results'])
        print("{:30s}: uploading full results".format("Experiment"))
        cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/', from_file=self.path+"/")
        #cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/', from_file=self.path+"/")
        self.cluster.kubectl(cmd['upload_results'])
    def show_summary(self):
        #print('ycsb.show_summary()')
        print("\n## Show Summary")
        pd.set_option("display.max_rows", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        with open(resultfolder+"/"+code+"/queries.config",'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
        print("\n### Workload\n    "+workload_properties['name'])
        print("    "+workload_properties['intro'])
        print("    "+workload_properties['info'])
        print("\n### Connections")
        with open(resultfolder+"/"+code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
        pretty_connections = json.dumps(connections, indent=2)
        #print(pretty_connections)
        connections_sorted = sorted(connections, key=lambda c: c['name'])
        for c in connections_sorted:
            print(c['name'],
                  "uses docker image",
                  c['parameter']['dockerimage'])
            infos = ["    {}:{}".format(key,info) for key, info in c['hostsystem'].items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
            for info in infos:
                print(info)
        #print("found", len(connections), "connections")
        #evaluate = inspector.inspector(resultfolder)       # no evaluation cube
        #evaluate.load_experiment(code=code, silent=False)
        evaluation = evaluators.ycsb(code=code, path=resultfolder)
        #####################
        test_loading = False
        df = evaluation.get_df_loading()
        if not df.empty:
            print("\n### Loading")
            df = df.sort_values(['configuration','experiment_run','client'])
            df = df[df.columns.drop(list(df.filter(regex='FAILED')))]
            #print(df)
            #print(df.columns)
            df_plot = evaluation.loading_set_datatypes(df)
            df_aggregated = evaluation.loading_aggregate_by_parallel_pods(df_plot)
            df_aggregated.sort_values(['experiment_run','target','pod_count'], inplace=True)
            df_aggregated_loaded = df_aggregated[['experiment_run',"threads","target","pod_count","[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)"]]
            print(df_aggregated_loaded)
            test_loading = True
        #####################
        df = evaluation.get_df_benchmarking()
        if not df.empty:
            print("\n### Execution")
            df.fillna(0, inplace=True)
            df_plot = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df_plot)
            df_aggregated = df_aggregated.sort_values(['experiment_run','target','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"threads","target","pod_count"]].copy()
            columns = ["[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)","[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)","[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)","[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)"]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            print(df_aggregated_reduced)
        #evaluation = evaluators.ycsb(code=code, path=path)
        #####################
        self.show_summary_monitoring()
        if test_loading:
            evaluation.test_results_column(df_aggregated_loaded, "[OVERALL].Throughput(ops/sec)")
        evaluation.test_results_column(df_aggregated_reduced, "[OVERALL].Throughput(ops/sec)")
    def show_summary_monitoring(self):
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        evaluation = evaluators.ycsb(code=code, path=resultfolder)
        if (self.monitoring_active or self.cluster.monitor_cluster_active):
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "loading")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "loader")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - Loader")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "stream")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "benchmarker")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - Benchmarker")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)



"""
############################################################################
Benchbase
############################################################################
"""

class benchbase(default):
    """
    Class for defining a Benchbase experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor), i.e. number of rows divided by 10.000
    """
    def __init__(self,
            cluster,
            code=None,
            #queryfile = 'queries-tpch.config',
            SF = '1',
            num_experiment_to_apply = 1,
            timeout = 7200,
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='benchbase')
        self.set_experiment(script='Schema')
        self.cluster.set_experiments_configfolder('experiments/benchbase')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'Benchbase Queries SF='+str(SF),
            info = 'This experiment performs some Benchbase workloads.'
            )
        self.storage_label = 'benchbase-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-benchbase.yml"
        self.evaluator = evaluators.benchbase(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
    def log_to_df(self, filename):
        self.cluster.logger.debug('benchbase.log_to_df({})'.format(filename))
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)
            log = re.findall('####BEXHOMA####(.+?)####BEXHOMA####', stdout, re.DOTALL)
            if len(log) > 0:
                result = json.loads(log[0])
                df = pd.json_normalize(result)
                df.index.name = connection_name[0]
                self.cluster.logger.debug(df)
                #print(df)
                return df
            else:
                print("no results found in log file {}".format(filename))
                return pd.DataFrame()
        except Exception as e:
            print(e)
            return pd.DataFrame()
    def get_parts_of_name(self, name):
        parts_name = re.findall('{(.+?)}', self.name_format)
        parts_values = re.findall('-(.+?)-', "-"+name.replace("-","--")+"--")
        return dict(zip(parts_name, parts_values))
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('benchbase.test_results()')
        self.evaluator.test_results()
        workflow = self.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
    def evaluate_results(self, pod_dashboard=''):
        """
        Build a DataFrame locally that contains all benchmarking results.
        This is specific to Benchbase.
        """
        self.cluster.logger.debug('benchbase.evaluate_results()')
        self.evaluator.evaluate_results(pod_dashboard)
        # download results
        if len(pod_dashboard) == 0:
            pod_dashboard = self.cluster.get_dashboard_pod_name(component='dashboard')
            if len(pod_dashboard) > 0:
                #pod_dashboard = pods[0]
                status = self.cluster.get_pod_status(pod_dashboard)
                print(pod_dashboard, status)
                while status != "Running":
                    self.wait(10)
                    status = self.cluster.get_pod_status(pod_dashboard)
                    print(pod_dashboard, status)
        if self.monitoring_active:
            cmd = {}
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loading -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct stream -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct loader -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
            cmd['transform_benchmarking_metrics'] = 'python metrics.evaluation.py -r /results/ -db -ct benchmarker -e {}'.format(self.code)
            stdin, stdout, stderr = self.cluster.execute_command_in_pod(command=cmd['transform_benchmarking_metrics'], pod=pod_dashboard, container="dashboard")
            self.cluster.logger.debug(stdout)
        cmd = {}
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/', to=self.path+"/")
        self.cluster.kubectl(cmd['download_results'])
        cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/', from_file=self.path+"/")
        self.cluster.kubectl(cmd['upload_results'])
    def show_summary(self):
        #print('benchbase.show_summary()')
        print("\n## Show Summary")
        pd.set_option("display.max_rows", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        with open(resultfolder+"/"+code+"/queries.config",'r') as inp:
            workload_properties = ast.literal_eval(inp.read())
        print("\n### Workload\n    "+workload_properties['name'])
        print("    "+workload_properties['intro'])
        print("    "+workload_properties['info'])
        print("\n### Connections")
        with open(resultfolder+"/"+code+"/connections.config",'r') as inf:
            connections = ast.literal_eval(inf.read())
        pretty_connections = json.dumps(connections, indent=2)
        #print(pretty_connections)
        connections_sorted = sorted(connections, key=lambda c: c['name'])
        for c in connections_sorted:
            print(c['name'],
                  "uses docker image",
                  c['parameter']['dockerimage'])
            infos = ["    {}:{}".format(key,info) for key, info in c['hostsystem'].items() if not 'timespan' in key and not info=="" and not str(info)=="0" and not info==[]]
            for info in infos:
                print(info)
        #print("found", len(connections), "connections")
        #evaluate = inspector.inspector(resultfolder)       # no evaluation cube
        #evaluate.load_experiment(code=code, silent=False)
        evaluation = evaluators.benchbase(code=code, path=resultfolder)
        #####################
        """
        df = evaluation.get_df_loading()
        if not df.empty:
            print("\n### Loading")
            df = df.sort_values(['configuration','experiment_run','client'])
            df = df[df.columns.drop(list(df.filter(regex='FAILED')))]
            #print(df)
            #print(df.columns)
            df_plot = evaluation.loading_set_datatypes(df)
            df_aggregated = evaluation.loading_aggregate_by_parallel_pods(df_plot)
            #print(df_aggregated)
            #print(df_aggregated.T)
            df_aggregated.sort_values(['experiment_run','target','pod_count'], inplace=True)
            df_aggregated = df_aggregated[['experiment_run',"terminals","target","pod_count","Throughput (requests/second)","Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]]
            print(df_aggregated)
        """
        #####################
        warehouses = 0
        df = evaluation.get_df_benchmarking()
        if not df.empty:
            print("\n### Execution")
            warehouses = int(df['sf'].max())
            df.fillna(0, inplace=True)
            df_plot = evaluation.benchmarking_set_datatypes(df)
            df_aggregated = evaluation.benchmarking_aggregate_by_parallel_pods(df_plot)
            #print(df_aggregated)
            #print(df_aggregated.T)
            df_aggregated = df_aggregated.sort_values(['experiment_run','target','pod_count']).round(2)
            df_aggregated_reduced = df_aggregated[['experiment_run',"terminals","target","pod_count"]].copy()
            #columns = ["[OVERALL].Throughput(ops/sec)","[OVERALL].RunTime(ms)","[INSERT].Return=OK","[INSERT].99thPercentileLatency(us)","[INSERT].99thPercentileLatency(us)","[READ].Return=OK","[READ].99thPercentileLatency(us)","[READ].99thPercentileLatency(us)","[UPDATE].Return=OK","[UPDATE].99thPercentileLatency(us)","[UPDATE].99thPercentileLatency(us)","[SCAN].Return=OK","[SCAN].99thPercentileLatency(us)","[SCAN].99thPercentileLatency(us)"]
            columns = ["time", "Throughput (requests/second)","Latency Distribution.95th Percentile Latency (microseconds)","Latency Distribution.Average Latency (microseconds)"]
            for col in columns:
                if col in df_aggregated.columns:
                    df_aggregated_reduced[col] = df_aggregated.loc[:,col]
            df_aggregated_reduced = df_aggregated_reduced.reindex(index=evaluators.natural_sort(df_aggregated_reduced.index))
            print(df_aggregated_reduced)
        print("\nWarehouses:", warehouses)
        #####################
        workflow = evaluation.reconstruct_workflow(df)
        if len(workflow) > 0:
            print("\n### Workflow")
            for c in workflow:
                print("DBMS", c, "- Pods", workflow[c])
        #####################
        print("\n### Loading")
        #connections_sorted = sorted(connections, key=lambda c: c['name']) 
        result = dict()
        for c in connections_sorted:
            """
            print(c['name'], 
                  c['timeLoad'], 
                  '[s] for', 
                  c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS'], 
                  'threads on',
                  c['hostsystem']['node'])
            """
            result[c['name']] = {
                'time_load': c['timeIngesting'],
                'terminals': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS'],
                #'target': c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TARGET'],
                'pods': c['parameter']['parallelism'],
            }
            #result[c['parameter']['connection_parameter']['loading_parameters']['BENCHBASE_TERMINALS']] = c['timeIngesting']
        df = pd.DataFrame(result)#, index=['time_load'])#, index=result.keys())
        #print(df)
        #df = df.T.pivot(columns='terminals', index='target', values='time_load')
        df_connections = df.copy().T
        #print(df_connections)
        df_tpx = (warehouses*3600.0)/df_connections.sort_index()
        #print(df_tpx)
        #df_loading_tpx = df_tpx['time_load']
        df_connections['Imported warehouses [1/h]'] = df_tpx['time_load']
        df_connections = df_connections.reindex(index=evaluators.natural_sort(df_connections.index))
        print(df_connections)
        #pd.DataFrame(df_tpx['time_load']).plot.bar(title="Imported warehouses [1/h]")
        #####################
        self.show_summary_monitoring()
        evaluation.test_results_column(df_aggregated_reduced, "Throughput (requests/second)")
    def show_summary_monitoring(self):
        resultfolder = self.cluster.config['benchmarker']['resultfolder']
        code = self.code
        evaluation = evaluators.benchbase(code=code, path=resultfolder)
        if (self.monitoring_active or self.cluster.monitor_cluster_active):
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "loading")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "loader")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Ingestion - Loader")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "stream")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - SUT")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)
            #####################
            df_monitoring = self.show_summary_monitoring_table(evaluation, "benchmarker")
            ##########
            if len(df_monitoring) > 0:
                print("\n### Execution - Benchmarker")
                df = pd.concat(df_monitoring, axis=1).round(2)
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(df)



"""
############################################################################
Example
############################################################################
"""

class example(default):
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
            script=None
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        if script is None:
            script = 'empty'
        self.set_experiment(volume='example')
        self.set_experiment(script=script)
        self.cluster.set_experiments_configfolder('experiments/example')
        #parameter.defaultParameters = {'SF': str(SF)}
        #self.set_additional_labels(SF=SF)
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'Custom Example Queries',
            info = 'This experiment performs some custom queries.'
            )
        self.storage_label = 'example'


"""
############################################################################
TPCx-AI
############################################################################
"""

class tpcxai(default):
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
            script=None
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
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
        self.storage_label = 'tpcxai-'+str(SF)
    def set_queries_full(self):
        self.set_queryfile('queries-tpcxai.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tpcxai-profiling.config')

