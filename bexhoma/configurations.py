"""
:Date: 2022-10-01
:Version: 0.6.0
:Authors: Patrick K. Erdelt

    Class for managing an DBMS configuation.
    This is plugged into an experiment object.

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
#import kubernetes.client
#from kubernetes.client.rest import ApiException
#from kubernetes import client, config
import subprocess
import os
from timeit import default_timer
import logging
import socket
import yaml
from collections import Counter
import json
import copy
from datetime import datetime, timedelta
import threading
from io import StringIO
import hiyapyco
from math import ceil
import time

from dbmsbenchmarker import *

from bexhoma import experiments





class default():
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

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
    def __init__(self, experiment, docker=None, configuration='', script=None, alias=None, num_experiment_to_apply=None, clients=[1], dialect='', worker=0, dockerimage=''):#, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        self.logger = logging.getLogger('bexhoma')
        self.experiment = experiment #: Unique identifier of the experiment
        self.docker = docker #: Name of the Docker image
        if len(configuration) == 0:
            configuration = docker
        self.configuration = configuration #: Name of the configuration, default: Name of the Docker image
        self.volume = self.experiment.volume
        if docker is not None:
            self.dockertemplate = copy.deepcopy(self.experiment.cluster.dockers[self.docker]) #: Template of the Docker information taken from cluster.config
        if script is not None:
            self.script = script
            self.initscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.script]
        else:
            self.script = self.experiment.script
            self.initscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.script]
        self.indexing = self.experiment.indexing
        if self.indexing:
            self.indexscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.indexing]
        else:
            self.indexscript = []
        self.alias = alias
        if num_experiment_to_apply is not None:
            self.num_experiment_to_apply = num_experiment_to_apply
        else:
            self.num_experiment_to_apply = self.experiment.num_experiment_to_apply
        self.num_experiment_to_apply_done = 0
        #self.clients = clients
        self.appname = self.experiment.cluster.appname
        self.code = self.experiment.cluster.code
        self.path = self.experiment.path
        self.resources = {}
        self.ddl_parameters = {}                                                # DDL schema parameter for init scripts (like index type or sharding strategy)
        self.eval_parameters = {}                                               # parameters that will be handed over to dbmsbenchmarker
        self.storage = {}                                                       # parameters for persistent storage (like type and size)
        self.nodes = {}                                                         # dict of node infos to guide components (like nodeSelector for SUT)
        self.maintaining_parameters = {}                                        # dict of parameters for maintaining component
        self.loading_parameters = {}                                            # dict of parameters for loading component
        self.sut_parameters = {}                                                # dict of parameters for sut and worker component
        self.pod_sut = '' #: Name of the sut's master pod
        self.set_resources(**self.experiment.resources)
        self.set_ddl_parameters(**self.experiment.ddl_parameters)
        self.set_eval_parameters(**self.experiment.eval_parameters)
        self.set_connectionmanagement(**self.experiment.connectionmanagement)
        self.set_storage(**self.experiment.storage)
        self.set_nodes(**self.experiment.nodes)
        self.set_maintaining_parameters(**self.experiment.maintaining_parameters)
        self.set_loading_parameters(**self.experiment.loading_parameters)
        self.set_sut_parameters(**self.experiment.sut_parameters)
        self.patch_loading(self.experiment.loading_patch)
        self.patch_benchmarking(self.experiment.benchmarking_patch)
        self.set_benchmarking_parameters(**self.experiment.benchmarking_parameters)
        self.benchmarking_parameters_list = []
        self.additional_labels = dict()
        self.set_additional_labels(**self.experiment.additional_labels)
        self.experiment.add_configuration(self)
        self.experiment_name = self.code                                        #: Identifier of experiment, default is experiment code. May be overwritten, when pvc of stateful set forbids different names per experiment
        self.dialect = dialect
        self.use_distributed_datasource = False                                 #: True, iff the SUT should mount 'benchmark-data-volume' as source of (non-generated) data
        # scaling of other components
        self.num_worker = worker
        self.num_loading = 0
        self.num_maintaining = 0
        self.num_loading_pods = 0
        self.num_maintaining_pods = 0
        self.num_tenants = self.experiment.num_tenants
        self.tenant_per = self.experiment.tenant_per                            #: '', or schema, database or container
        self.tenant_ready_to_load = False
        self.tenant_started_to_load = False
        self.tenant_ready_to_index = False
        self.tenant_started_to_index = False
        # are there other components?
        self.monitor_app_active = experiment.monitor_app_active
        self.monitoring_active = experiment.monitoring_active
        self.prometheus_interval = experiment.prometheus_interval
        self.prometheus_timeout = experiment.prometheus_timeout
        self.maintaining_active = experiment.maintaining_active
        self.loading_active = experiment.loading_active
        self.loading_deactivated = experiment.loading_deactivated               #: Do not load at all and do not test for loading
        self.monitor_loading = True                                             #: Fetch metrics for the loading phase, if monítoring is active - this is set to False when loading is skipped due to PV
        self.monitoring_sut = True                                              #: Fetch metrics of SUT, if monítoring is active - this is set to False when a service outside of K8s is benchmarked
        self.jobtemplate_maintaining = ""
        self.jobtemplate_loading = ""
        self.storage_label = experiment.storage_label
        self.experiment_done = False                                            #: True, iff the SUT has performed the experiment completely
        self.dockerimage = dockerimage                                          #: Name of the Docker image of the SUT
        self.sut_template = template = "deploymenttemplate-"+self.docker+".yml" #: Name of YAML manifest in k8s/ for deployment of SUT (default: "deploymenttemplate-"+self.docker+".yml")
        self.path_experiment_docker = self.docker                               #: Name of the correspond folder in the experiment path. Default = Name of Docker image (e.g., PostgreSQL for experiment/ycsb/PostgreSQL)
        self.connection_parameter = {}                                          #: Collect all parameters that might be interesting in evaluation of results
        self.timeLoading = 0                                                    #: Time in seconds the system has taken for the initial loading of data
        self.timeGenerating = 0                                                 #: Time in seconds the system has taken for generating the data
        self.timeIngesting = 0                                                  #: Time in seconds the system has taken for ingesting existing
        self.timeSchema = 0                                                     #: Time in seconds the system has taken for creating the db schema
        self.timeIndex = 0                                                      #: Time in seconds the system has taken for indexing the database
        self.times_scripts = dict()                                             #: contains times for each single script that is run on db (create schema, index etc)
        self.loading_started = False                                            #: Time as an integer when initial loading has started
        self.loading_after_time = None                                          #: Time as an integer when initial loading should start - to give the system time to start up completely
        self.loading_finished = False                                           #: Time as an integer when initial loading has finished
        self.client = 1                                                         #: If we have a sequence of benchmarkers, this tells at which position we are  
        self.timeLoadingStart = 0
        self.timeLoadingEnd = 0
        self.loading_timespans = {}                                             #: Dict of lists per container of (start,end) pairs containing time markers of loading pods
        self.benchmarking_timespans = {}                                        #: Dict of lists per container of (start,end) pairs containing time markers of benchmarking pods
        self.sut_service_name = ""                                              #: Name of the DBMS service name, if it is fixed and not installed per configuration
        self.sut_pod_name = ""                                                  #: Name of pod of SUT, if it is not managed by bexhoma
        self.sut_container_name = "dbms"                                        #: Name of the container in the SUT pod, that should be monitored, and for reading infos via ssh
        self.statefulset_name = ""                                              #: Name of the stateful set managing the pods of a distributed dbms
        self.sut_containers_deployed = []                                       #: Name of the containers of the SUT deployment
        self.worker_containers_deployed = []                                    #: Name of the containers of the SUT statefulset
        self.pool_containers_deployed = []                                      #: Name of the containers of the Pool deployment
        #self.sut_envs = {}                                                      #: parameters sent to container via ENV
        self.sut_has_pool = False                                               #: if there is a pool component - in particular for monitoring
        self.reset_sut()
        self.benchmark = None                                                   #: Optional subobject for benchmarking (dbmsbenchmarker instance)
        self.current_benchmark_connection = ""                                  #: Name of the current connection - for metrics collection
    def reset_sut(self):
        """
        Forget that the SUT has been loaded and benchmarked.
        """
        self.timeLoading = 0 #: Time the system has taken for the initial loading of data
        self.timeGenerating = 0 #: Time in seconds the system has taken for generating the data
        self.timeIngesting = 0 #: Time in seconds the system has taken for ingesting existing
        self.timeSchema = 0 #: Time in seconds the system has taken for creating the db schema
        self.timeIndex = 0 #: Time in seconds the system has taken for indexing the database
        self.loading_started = False #: Time as an integer when initial loading has started
        self.loading_after_time = None #: Time as an integer when initial loading should start - to give the system time to start up completely
        self.loading_finished = False #: Time as an integer when initial loading has finished
        self.client = 1 #: If we have a sequence of benchmarkers, this tells at which position we are
        self.is_sut_ready = False
        self.are_worker_ready = False
    def add_benchmark_list(self, list_clients):
        """
        Add a list of (number of) benchmarker instances, that are to benchmark the current SUT.
        Example: `[1,2,1]` means sequentially we will have 1, then 2 and then 1 benchmarker instances.

        :param list_clients: List of (number of) benchmarker instances
        """
        # this queue will be reduced when a job has finished
        self.benchmark_list = copy.deepcopy(list_clients)
        # this queue will stay as a template for future copies of the configuration
        self.benchmark_list_template = copy.deepcopy(list_clients)
        self.benchmarking_parameters_list_template = copy.deepcopy(self.benchmarking_parameters_list)
    def wait(self, sec, silent=False):
        """
        Function for waiting some time and inform via output about this

        :param sec: Number of seconds to wait
        :param silent: True means we do not output anything about this waiting
        """
        #if not silent:
        #    print("Waiting "+str(sec)+"s...", end="", flush=True)
        #intervals = int(sec)
        #time.sleep(intervals)
        #if not silent:
        #    print("done")
        return self.experiment.cluster.wait(sec, silent)
    def delay(self, sec, silent=False):
        """
        Function for waiting some time and inform via output about this.
        Synonymous for wait()

        :param sec: Number of seconds to wait
        :param silent: True means we do not output anything about this waiting
        """
        self.wait(sec, silent)
    def OLD_get_items(self, app='', component='', experiment='', configuration=''):
        if len(app) == 0:
            app = self.experiment.cluster.appname
        if len(experiment) == 0:
            experiment = self.experiment.code
        print("get_items", app, component, experiment, configuration)
        self.pods = self.experiment.cluster.get_pods(app, component, experiment, configuration)
        print(self.pods)
        self.deployments = self.experiment.cluster.get_deployments(app, component, experiment, configuration)
        print(self.deployments)
        self.services = self.experiment.cluster.get_services(app, component, experiment, configuration)
        print(self.services)
        self.pvcs = self.experiment.cluster.get_pvc()
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
    def set_storage(self, **kwargs):
        """
        Sets parameters for the storage that might be attached to components.
        This is in particular for the database of dbms under test.
        Example:

        `storageClassName = 'ssd',
        storageSize = '100Gi',
        keep = False`

        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'storageSize' => '100Gi'
        """
        self.storage = {**self.storage, **kwargs}
        #self.storage = kwargs
    def set_additional_labels(self, **kwargs):
        """
        Sets additional labels, that will be put to K8s objects (and ignored otherwise).
        This is for the SUT component.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of labels, example 'SF' => 100
        """
        self.additional_labels = {**self.additional_labels, **kwargs}
    def set_ddl_parameters(self, **kwargs):
        """
        Sets DDL parameters for the experiments.
        This substitutes placeholders in DDL script.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'index' => 'btree'
        """
        self.ddl_parameters = kwargs
    def set_eval_parameters(self, **kwargs):
        """
        Sets some arbitrary parameters that are supposed to be handed over to the benchmarker component.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'type' => 'noindex'
        """
        #self.eval_parameters = kwargs
        self.eval_parameters = {**self.eval_parameters, **kwargs}
    def set_maintaining_parameters(self, **kwargs):
        """
        Sets ENV for maintaining components.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.maintaining_parameters = kwargs
    def set_maintaining(self, parallel, num_pods=None):
        """
        Sets job parameters for maintaining components: Number of parallel pods and optionally (if different) total number of pods.
        By default total number of pods is set to number of parallel pods.
        Can be set by experiment before creation of configuration.

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
    def set_sut_parameters(self, **kwargs):
        """
        Sets ENV for sut and workers components.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.sut_parameters = kwargs
    def set_loading_parameters(self, **kwargs):
        """
        Sets ENV for loading components.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.loading_parameters = kwargs
    def patch_loading(self, patch):
        """
        Patches YAML of loading components.
        Can be set by experiment before creation of configuration.

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
    def set_benchmarking_parameters(self, **kwargs):
        """
        Sets ENV for benchmarking components.
        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.benchmarking_parameters = kwargs
    def add_benchmarking_parameters(self, **kwargs):
        """
        Sets ENV for benchmarking components.
        Can be set by experiment before creation of configuration.
        This generates a list, where each entry corresponds to a set of clients in a sequence of benchmarkers.

        :param kwargs: Dict of meta data, example 'PARALLEL' => '64'
        """
        self.benchmarking_parameters_list.append(kwargs)
    def set_loading(self, parallel, num_pods=None):
        """
        Sets job parameters for loading components: Number of parallel pods and optionally (if different) total number of pods.
        By default total number of pods is set to number of parallel pods.
        Can be set by experiment before creation of configuration.

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
    def set_nodes(self, **kwargs):
        """
        Sets parameters for nodes for the components of an experiment.
        Will be used for nodeSelector.
        Example:

        sut = 'sut',
        loading = 'auxiliary',
        monitoring = 'auxiliary',
        benchmarking = 'auxiliary',

        Can be set by experiment before creation of configuration.

        :param kwargs: Dict of node infos, example 'sut' => 'sut',
        """
        self.nodes = kwargs
    def set_experiment(self, instance=None, volume=None, docker=None, script=None, indexing=None):
        """ Read experiment details from cluster config"""
        #self.bChangeInstance = True
        #if instance is not None:
        #   self.i = instance
        if volume is not None:
            self.volume = volume
            self.volumeid = self.experiment.cluster.volumes[self.experiment.volume]['id']
        #if docker is not None:
        #   self.d = docker
        #   self.docker = self.cluster.dockers[self.d]
        if script is not None:
            self.script = script
            self.initscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.script]
        if indexing is not None:
            self.indexing = indexing
            self.indexscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.indexing]
    def __OLD_prepare(self, instance=None, volume=None, docker=None, script=None, delay=0):
        """ Per config: Startup SUT and Monitoring """
        #self.setExperiment(instance, volume, docker, script)
        # check if is terminated
        #self.createDeployment()
        self.create_sut()
        self.get_items(component='sut')
        pods = self.experiment.cluster.get_pods(component='sut')
        status = self.get_pod_status(pods[0])
        while status != "Running":
            print(status)
            self.wait(10)
            status = self.get_pod_status(pods[0])
        self.experiment.cluster.startPortforwarding()
        self.experiment.cluster.getChildProcesses()
        # store experiment
        """
        experiment = {}
        experiment['delay'] = delay
        experiment['step'] = "prepareExperiment"
        experiment['docker'] = {self.d: self.docker.copy()}
        experiment['volume'] = self.v
        experiment['initscript'] = {self.s: self.initscript.copy()}
        experiment['instance'] = self.i
        self.log_experiment(experiment)
        """
        if delay > 0:
            self.delay(delay)
    def __OLD_start(self, instance=None, volume=None, docker=None, script=None, delay=0):
        """ Per config: Load Data """
        #self.setExperiment(instance, volume, docker, script)
        self.get_items(component='sut')
        self.get_items(component='sut')
        pods = self.experiment.cluster.get_pods(component='sut')
        status = self.get_pod_status(pods[0])
        while status != "Running":
            print(status)
            self.wait(10)
            status = self.get_pod_status(pods[0])
        dbmsactive = self.check_DBMS_connection(self.host, self.port)
        while not dbmsactive:
            self.startPortforwarding()
            self.wait(10)
            dbmsactive = self.check_DBMS_connection(self.host, self.port)
        self.wait(10)
        print("load_data")
        self.load_data()
        # store experiment
        """
        experiment = {}
        experiment['delay'] = delay
        experiment['step'] = "startExperiment"
        experiment['docker'] = {self.d: self.docker.copy()}
        experiment['volume'] = self.v
        experiment['initscript'] = {self.s: self.initscript.copy()}
        experiment['instance'] = self.i
        self.log_experiment(experiment)
        """
        if delay > 0:
            self.delay(delay)
        # end
    def sut_is_pending(self):
        """
        Returns True, iff system-under-test (dbms) is in pending state.

        :return: True, if dbms is in pendig state
        """
        app = self.appname
        component = 'sut'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.get_pod_status(pod_sut)
            if status == "Pending":
                return True
        return False
    def sut_is_running(self):
        """
        Returns True, iff system-under-test (dbms) is running.

        :return: True, if dbms is running
        """
        app = self.appname
        component = 'sut'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.get_pod_status(pod_sut)
            if status == "Running":
                return True
                #ready = self.experiment.cluster.is_pod_ready(pod_sut)
                #if ready:
                #    return True
                #else:
                #     print("{:30s}: is not healthy yet".format(self.configuration))
        return False
    def sut_is_healthy(self):
        """
        Returns True, iff system-under-test (dbms) is running and healthy.

        :return: True, if dbms is running
        """
        if self.is_sut_ready:
            return True
        app = self.appname
        component = 'sut'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.get_pod_status(pod_sut)
            if status == "Running":
                ready = self.experiment.cluster.is_pod_ready(pod_sut)
                if ready:
                    self.is_sut_ready = True
                    return True
                else:
                    #print("{:30s}: is not healthy yet".format(self.configuration))
                    return False
        return False
    def workers_are_healthy(self):
        """
        Returns True, iff all workers of system-under-test (dbms) are running and healthy.

        :return: True, if dbms is running
        """
        if self.num_worker > 0:
            if self.are_worker_ready:
                return True
            app = self.appname
            component = 'worker'
            configuration = self.configuration
            #pods = self.experiment.cluster.get_pods(app, component, self.experiment_name, configuration)
            num_ready = 0
            pods_worker = self.get_worker_pods()#self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
            for pod in pods_worker:
                #stdin, stdout, stderr = self.execute_command_in_pod_sut(self.dockertemplate['attachWorker'].format(worker=pod, service_sut=name_worker), pod_sut)
                status = self.experiment.cluster.get_pod_status(pod)
                if status == "Running":
                    ready = self.experiment.cluster.is_pod_ready(pod)
                    if ready:
                        num_ready = num_ready + 1
            print("{:30s}: found {} / {} running workers".format(self.configuration, num_ready, self.num_worker))
            self.are_worker_ready = (num_ready == self.num_worker)
            if self.are_worker_ready:
                self.attach_worker()
            return self.are_worker_ready
        else:
            return True
    def sut_is_existing(self):
        """
        Returns True, iff system-under-test (dbms) is existing in cluster (no matter what state).

        :return: True, if dbms is existing
        """
        app = self.appname
        component = 'sut'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            return True
        return False
    def maintaining_is_running(self):
        """
        Returns True, iff maintaining is running.

        :return: True, if dbms is running
        """
        app = self.appname
        component = 'maintaining'
        configuration = self.configuration
        pods_running = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration, status="Running")
        pods_succeeded = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration, status="Succeeded")
        self.logger.debug("maintaining_is_running found {} running and {} succeeded pods".format(len(pods_running), len(pods_succeeded)))
        return len(pods_running) + len(pods_succeeded) == self.num_maintaining
        #if len(pods) > 0:
        #    pod_sut = pods[0]
        #    status = self.experiment.cluster.get_pod_status(pod_sut)
        #    if status == "Running":
        #        return True
        #return False
    def maintaining_is_pending(self):
        """
        Returns True, iff maintaining is in pending state.

        :return: True, if maintaining is in pendig state
        """
        app = self.appname
        component = 'maintaining'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration, status="Pending")
        if len(pods) > 0:
            pod_sut = pods[0]
            #status = self.experiment.cluster.get_pod_status(pod_sut)
            #if status == "Pending":
            return True
        return False
    def monitoring_is_running(self):
        """
        Returns True, iff monitoring is running.

        :return: True, if monitoring is running
        """
        if self.experiment.cluster.monitor_cluster_exists and not self.monitor_app_active:
            return True
        app = self.appname
        component = 'monitoring'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.get_pod_status(pod_sut)
            if status == "Running":
                return True
        return False
    def monitoring_is_pending(self):
        """
        Returns True, iff monitoring is in pending state.

        :return: True, if monitoring is in pendig state
        """
        app = self.appname
        component = 'monitoring'
        configuration = self.configuration
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.get_pod_status(pod_sut)
            if status == "Pending":
                return True
        return False
    def start_loading_pod(self, app='', component='loading', experiment='', configuration='', parallelism=1, num_pods=1):
        """
        Starts a job for parallel data ingestion.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param parallelism: Number of parallel pods in job
        """
        if len(app) == 0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        self.logger.debug("start_loading_pod({})".format(configuration))
        # put list of clients to message queue
        redisQueue = '{}-{}-{}-{}'.format(app, component, self.configuration, self.code)
        for i in range(1, self.num_loading+1):
            #redisClient.rpush(redisQueue, i)
            self.experiment.cluster.add_to_messagequeue(queue=redisQueue, data=i)
        # reset number of clients per job
        redisQueue = '{}-{}-{}-{}'.format(app, 'loader-podcount', self.configuration, self.code)
        self.experiment.cluster.set_pod_counter(queue=redisQueue, value=0)
        # reset number of clients per experiment
        #redisQueue = '{}-{}-{}'.format(app, 'loader-podcount', self.code)
        #self.experiment.cluster.set_pod_counter(queue=redisQueue, value=0)
        # start job
        job = self.create_manifest_loading(app=app, component='loading', experiment=experiment, configuration=configuration, parallelism=parallelism, num_pods=num_pods)
        self.logger.debug("Deploy "+job)
        self.experiment.cluster.kubectl('create -f '+job)#self.yamlfolder+deployment)
    def start_loading(self, delay=0):
        """
        Starts data ingestion by calling scripts inside the sut (dbms) container.

        :param delay: Number of seconds to wait after calling scripts
        """
        app = self.appname
        component = 'sut'
        configuration = self.configuration
        self.logger.debug("start_loading({})".format(configuration))
        pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.get_pod_status(pod_sut)
            if status != "Running":
                return False
            #if self.num_worker > 0:
            #    self.attach_worker()
            #while status != "Running":
            #    print(pod_sut, status)
            #    self.wait(10)
            #    status = self.experiment.cluster.get_pod_status(pod_sut)
            self.logger.debug("check if {} is running".format(pod_sut))
            services = self.experiment.cluster.get_services(app, component, self.experiment.code, configuration)
            service = services[0]
            ports = self.experiment.cluster.get_ports_of_service(app, component, self.experiment.code, configuration)
            forward = ['kubectl', '--context {context}'.format(context=self.experiment.cluster.context), 'port-forward', 'service/'+service] #bexhoma-service']#, '9091', '9300']#, '9400']
            forward.extend(ports)
            your_command = " ".join(forward)
            # we do not test at localhost (forwarded), because there might be conflicts
            """
            self.logger.debug('configuration.start_loading({})'.format(your_command))
            subprocess.Popen(your_command, stdout=subprocess.PIPE, shell=True)
            # wait for port to be connected
            self.wait(2)
            dbmsactive = self.check_DBMS_connection(self.experiment.cluster.host, self.experiment.cluster.port)
            if not dbmsactive:
                # not answering
                self.experiment.cluster.stopPortforwarding()
                return False
            """
            #while not dbmsactive:
            #    self.wait(10)
            #    dbmsactive = self.check_DBMS_connection(self.experiment.cluster.host, self.experiment.cluster.port)
            #self.wait(10)
            self.check_load_data()
            if not self.loading_started:
                #print("load_data")
                self.load_data(scripts=self.initscript)
            # we do not test at localhost (forwarded), because there might be conflicts
            #self.experiment.cluster.stopPortforwarding()
            # store experiment needs new format
            """
            experiment = {}
            experiment['delay'] = delay
            experiment['step'] = "startExperiment"
            experiment['docker'] = {self.d: self.docker.copy()}
            experiment['volume'] = self.v
            experiment['initscript'] = {self.s: self.initscript.copy()}
            experiment['instance'] = self.i
            self.log_experiment(experiment)
            """
            if delay > 0:
                self.delay(delay)
            return True
        # end
    def generate_component_name(self, app='', component='', experiment='', configuration='', experimentRun='', client=''):
        """
        Generate a name for the component.
        Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: Number of the client, if it comes from a sequence of same components (in particular benchmarker)
        """
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        if len(experimentRun) != 0:
            experimentRun = '-'+experimentRun
        if len(client) > 0:
            name = "{app}-{component}-{configuration}-{experiment}{experimentRun}-{client}".format(app=app, component=component, configuration=configuration, experiment=experiment, experimentRun=experimentRun, client=client).lower()
        else:
            name = "{app}-{component}-{configuration}-{experiment}{experimentRun}".format(app=app, component=component, configuration=configuration, experiment=experiment, experimentRun=experimentRun).lower()
        return name
    def start_maintaining(self, app='', component='maintaining', experiment='', configuration='', parallelism=1, num_pods=1):
        """
        Starts a maintaining job.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param parallelism: Number of parallel pods in job
        """
        if len(app) == 0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        job = self.create_manifest_maintaining(app=app, component='maintaining', experiment=experiment, configuration=configuration, parallelism=parallelism, num_pods=num_pods)
        self.logger.debug("Deploy "+job)
        self.experiment.cluster.kubectl('create -f '+job)#self.yamlfolder+deployment)
    def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Generate a name for the monitoring component.
        This is used in a pattern for promql.
        Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`.
        If there is a self.sut_pod_name and we want to monitor SUT, that name is taken instead.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if component == 'sut' and len(self.sut_pod_name) > 0:
            name = self.sut_pod_name
        else:
            name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        self.logger.debug("configuration.create_monitoring({})".format(name))
        return name
    def start_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Starts a monitoring deployment.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if not self.experiment.monitoring_active or (self.experiment.cluster.monitor_cluster_active and self.experiment.cluster.monitor_cluster_exists and not self.monitor_app_active):
            return
        if len(app) == 0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        deployment ='deploymenttemplate-bexhoma-prometheus.yml'
        #if not os.path.isfile(self.yamlfolder+self.deployment):
        name = self.create_monitoring(app, component, experiment, configuration)
        name_sut = self.create_monitoring(app, 'sut', experiment, configuration)
        if self.experiment.cluster.monitor_cluster_active:
            print("{:30s}: wants to monitor all components in cluster".format(configuration))
        if not self.experiment.cluster.monitor_cluster_exists:
            print("{:30s}: cannot rely on preinstalled monitoring".format(configuration))
        print("{:30s}: starts monitoring with prometheus pod".format(configuration))
        deployment_experiment = self.experiment.path+'/{name}.yml'.format(name=name)
        with open(self.experiment.cluster.yamlfolder+deployment) as stream:
            try:
                result=yaml.safe_load_all(stream)
                result = [data for data in result]
                #print(result)
                for dep in result:
                    if dep['kind'] == 'Service':
                        service = dep['metadata']['name'] = name
                        dep['metadata']['labels']['app'] = app
                        dep['metadata']['labels']['component'] = component
                        dep['metadata']['labels']['configuration'] = configuration
                        dep['metadata']['labels']['dbms'] = self.docker
                        dep['metadata']['labels']['experiment'] = experiment
                        dep['metadata']['labels']['volume'] = self.volume
                        dep['spec']['selector'] = dep['metadata']['labels'].copy()
                    if dep['kind'] == 'Deployment':
                        deployment = dep['metadata']['name'] = name
                        dep['metadata']['labels']['app'] = app
                        dep['metadata']['labels']['component'] = component
                        dep['metadata']['labels']['configuration'] = configuration
                        dep['metadata']['labels']['dbms'] = self.docker
                        dep['metadata']['labels']['experiment'] = str(experiment)
                        dep['metadata']['labels']['volume'] = self.volume
                        dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                        dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                        envs = dep['spec']['template']['spec']['containers'][0]['env']
                        #prometheus_interval = "15s"
                        #prometheus_timeout = "15s"
                        prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: '{master}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{master}:9300']
  - job_name: 'monitor-gpu'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{master}:9400']""".format(master=name_sut, prometheus_interval=self.prometheus_interval, prometheus_timeout=self.prometheus_timeout)
                        # application monitor
                        # TODO: test for dbms other than PostgreSQL
                        if self.monitor_app_active:
                            if self.dockertemplate['monitor']['blackbox']:
                                app_monitor_targets = "\n          - postgres@localhost:5432/postgres?sslmode=disable\n"
                                if self.tenant_per == 'database' and self.num_tenants > 0:
                                    connections = [
                                        f"          - postgres@localhost:5432/tenant_{i}?sslmode=disable"
                                        for i in range(self.num_tenants)
                                    ]
                                    app_monitor_targets += "\n".join(connections)
                                prometheus_config += """
  - job_name: 'monitor-app'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    metrics_path: /probe
    static_configs:
      - targets: {app_monitor_targets}
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        regex: .*@([^:/]+:\\d+)/.*
        replacement: ${{1}}
        target_label: instance
      - target_label: __address__
        replacement: {master}:9500""".format(master=name_sut, prometheus_interval=self.prometheus_interval, prometheus_timeout=self.prometheus_timeout, app_monitor_targets=app_monitor_targets)
                            else:
                                # no blackbox mode, normal scraping target directly
                                prometheus_config += """
  - job_name: 'monitor-app'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets:
          - {master}:9500
        labels:
          app: mysql-app""".format(master=name_sut, prometheus_interval=self.prometheus_interval, prometheus_timeout=self.prometheus_timeout)
                        # service of cluster
                        endpoints_cluster = self.experiment.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
                        i = 0
                        for endpoint in endpoints_cluster:
                            print("{:30s}: found monitoring endpoint (cAdvisor) for monitoring {} (added to Prometheus) of daemonset".format(configuration, endpoint))
                            #print('Worker: {worker}.{service_sut}'.format(worker=pod, service_sut=name_worker))
                            prometheus_config += """
  - job_name: '{endpoint}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{endpoint}:9300']""".format(endpoint=endpoint, client=i, prometheus_interval=self.prometheus_interval, prometheus_timeout=self.prometheus_timeout)
                            i = i + 1
                        # services of workers
                        if len(endpoints_cluster) == 0:
                            endpoints_worker = self.get_worker_endpoints()
                            #name_worker = self.generate_component_name(component='worker', configuration=self.configuration, experiment=self.code)
                            #pods_worker = self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
                            i = 0
                            #for pod in pods_worker:
                            for endpoint in endpoints_worker:
                                if endpoint in endpoints_cluster:
                                    # we already monitor this endpoint
                                    print("{:30s}: found worker endpoint (cAdvisor) for monitoring {} (already monitored by cluster)".format(configuration, endpoint))
                                    continue
                                print("{:30s}: found worker endpoint (cAdvisor) for monitoring {} (added to Prometheus) of sidecar container".format(configuration, endpoint))
                                #print('Worker: {worker}.{service_sut}'.format(worker=pod, service_sut=name_worker))
                                prometheus_config += """
  - job_name: '{endpoint}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{endpoint}:9300']""".format(endpoint=endpoint, client=i, prometheus_interval=self.prometheus_interval, prometheus_timeout=self.prometheus_timeout)
                                i = i + 1
                        for i,e in enumerate(envs):
                            if e['name'] == 'BEXHOMA_SERVICE':
                                dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = name_sut
                            if e['name'] == 'DBMSBENCHMARKER_CONFIGURATION':
                                dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = configuration
                            if e['name'] == 'BEXHOMA_WORKERS':
                                dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = prometheus_config
                            #print(e)
                            self.logger.debug('configuration.start_monitoring({})'.format(str(e)))
                        # set nodeSelector
                        if 'monitoring' in self.nodes:
                            if not 'nodeSelector' in dep['spec']['template']['spec']:
                                dep['spec']['template']['spec']['nodeSelector'] = dict()
                            if dep['spec']['template']['spec']['nodeSelector'] is None:
                                dep['spec']['template']['spec']['nodeSelector'] = dict()
                            dep['spec']['template']['spec']['nodeSelector']['type'] = self.nodes['monitoring']
            except yaml.YAMLError as exc:
                print(exc)
        with open(deployment_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        self.logger.debug("Deploy "+deployment)
        self.experiment.cluster.kubectl('create -f '+deployment_experiment)#self.yamlfolder+deployment)
    def stop_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Stops a monitoring deployment and removes its service.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        deployments = self.experiment.cluster.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            self.experiment.cluster.delete_deployment(deployment)
        services = self.experiment.cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            self.experiment.cluster.delete_service(service)
    def stop_maintaining(self, app='', component='maintaining', experiment='', configuration=''):
        """
        Stops a monitoring deployment and removes all its pods.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        jobs = self.experiment.cluster.get_jobs(app, component, experiment, configuration)
        # status per job
        for job in jobs:
            success = self.experiment.cluster.get_job_status(job)
            print(job, success)
            self.experiment.cluster.delete_job(job)
        # all pods to these jobs - automatically stopped? only if finished?
        #self.experiment.cluster.get_job_pods(app, component, experiment, configuration)
        pods = self.experiment.cluster.get_job_pods(app, component, experiment, configuration)
        for pod in pods:
            status = self.experiment.cluster.get_pod_status(pod)
            print(pod, status)
            #if status == "Running":
            # TODO: Find names of containers dynamically
            containers = self.experiment.cluster.get_pod_containers(pod)
            for container in containers:
                stdout = self.experiment.cluster.pod_log(pod=pod, container=container)
                #stdin, stdout, stderr = self.pod_log(client_pod_name)
                filename_log = self.path+'/'+pod+'.'+container+'.log'
                f = open(filename_log, "w")
                f.write(stdout)
                f.close()
            #container = 'datagenerator'
            #if container in containers:
            #    stdout = self.experiment.cluster.pod_log(pod=pod, container=container)
            #    #stdin, stdout, stderr = self.pod_log(client_pod_name)
            #    filename_log = self.path+'/'+pod+'.'+container+'.log'
            #    f = open(filename_log, "w")
            #    f.write(stdout)
            #    f.close()
            #
            #container = 'sensor'
            #if container in containers:
            #    stdout = self.experiment.cluster.pod_log(pod=pod, container='sensor')
            #    #stdin, stdout, stderr = self.pod_log(client_pod_name)
            #    filename_log = self.path+'/'+pod+'.'+container+'.log'
            #    f = open(filename_log, "w")
            #    f.write(stdout)
            #    f.close()
            self.experiment.cluster.delete_pod(pod)
    def stop_loading(self, app='', component='loading', experiment='', configuration=''):
        """
        Stops a loading job and removes all its pods.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        jobs = self.experiment.cluster.get_jobs(app, component, experiment, configuration)
        # status per job
        for job in jobs:
            success = self.experiment.cluster.get_job_status(job)
            print(job, success)
            self.experiment.cluster.delete_job(job)
        # all pods to these jobs - automatically stopped? only if finished?
        #self.experiment.cluster.get_job_pods(app, component, experiment, configuration)
        pods = self.experiment.cluster.get_job_pods(app, component, experiment, configuration)
        for p in pods:
            status = self.experiment.cluster.get_pod_status(p)
            print(p, status)
            #if status == "Running":
            self.experiment.cluster.delete_pod(p)
    def generate_port_forward(self):
        """
        Generates command to port-forward to this SUT.
        Returns it as a string

        :return: Command to port-forward to SUT as a string
        """
        context = self.experiment.cluster.context
        app = self.appname
        component = 'sut'
        experiment = self.experiment_name # self.experiment.code
        configuration = self.configuration
        name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        ports = self.experiment.cluster.get_ports_of_service(app=app, component=component, experiment=experiment, configuration=configuration)
        forward = ['kubectl', '--context {context}'.format(context=context), 'port-forward', 'service/'+name]
        forward.extend(ports)
        command = " ".join(forward)
        #print("{:30s}: {}".format(configuration, command))
        return command
    def DEPRECATED_get_instance_from_resources(self):
        """
        Generates an instance name out of the resource parameters that are set using `set_resources()`.
        Should be DEPRECATED and replaced by something better.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        resources = experiments.DictToObject(self.resources)
        cpu = resources.requests.cpu
        memory = resources.requests.memory
        gpu = resources.requests.gpu
        cpu_type = resources.nodeSelector.cpu
        gpu_type = resources.nodeSelector.gpu
        instance = "{}-{}-{}-{}".format(cpu, memory, gpu, gpu_type)
        return instance
    def use_storage(self):
        """
        Return True, iff storage for the database should be used.
        Otherwise database is inside ephemeral-storage.
        """
        if len(self.storage) > 0:
            use_storage = True
            if 'storageClassName' in self.storage:
                storageClassName = self.storage['storageClassName']
                if storageClassName is None:
                    use_storage = False
            else:
                storageClassName = ''
            if 'storageSize' in self.storage:
                storageSize = self.storage['storageSize']
            else:
                storageSize = ''
            if 'storageConfiguration' in self.storage:
                storageConfiguration = self.storage['storageConfiguration']
            else:
                storageConfiguration = ''
                self.storage['storageConfiguration'] = ''
        else:
            use_storage = False
        return use_storage
    def start_sut(self, app='', component='sut', experiment='', configuration=''):
        """
        Start the system-under-test (dbms).
        This also controls optional worker and storage.
        Resources are set according to `set_resources()`.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        use_storage = self.use_storage()
        use_data = self.use_distributed_datasource
        #storage_label = 'tpc-ds-1'
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        #instance = self.get_instance_from_resources()
        # storage configuration
        if self.storage['storageConfiguration']:
            storageConfiguration = self.storage['storageConfiguration']
            #name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=self.storage['storageConfiguration'])
        else:
            storageConfiguration = configuration
            #name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=configuration)
        # configure names
        if self.num_worker > 0:
            # we assume here, a stateful set is used
            # this means we do not want to have the experiment code as part of the names
            # this would imply there cannot be experiment independent pvcs
            self.experiment_name = self.storage_label#storageConfiguration
        else:
            self.experiment_name = experiment
        name = self.generate_component_name(app=app, component=component, experiment=self.experiment_name, configuration=configuration)
        #name_worker = self.generate_component_name(app=app, component='worker', experiment=self.experiment_name, configuration=configuration)
        name_worker = self.get_worker_name()
        name_service_headless = name_worker# must be the same
        name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
        name_pool = self.generate_component_name(app=app, component='pool', experiment=self.experiment_name, configuration=configuration)
        self.logger.debug('configuration.start_sut(name={})'.format(name))
        # test, if SUT is already running
        deployments = self.experiment.cluster.get_deployments(app=app, component=component, experiment=self.experiment_name, configuration=configuration)
        if len(deployments) > 0:
            # sut is already running
            return False
        # Deployment manifest template - a configured copy will be stored in result folder
        template = self.sut_template #template = "deploymenttemplate-"+self.docker+".yml"
        deployment_experiment = self.experiment.path+'/{name}.yml'.format(name=name)
        print("{:30s}: Name of SUT pods = {}".format(configuration, name))
        print("{:30s}: Name of SUT service = {}".format(configuration, name))
        if use_storage:
            print("{:30s}: Name of SUT PVC name = {}".format(configuration, name_pvc))
        if self.num_worker > 0:
            print("{:30s}: Name of Worker pods = {}".format(configuration, name_worker))
            print("{:30s}: Name of Worker service headless = {}".format(configuration, name_worker))
        # ENV
        # default empty: env = {}
        env = self.sut_parameters #self.sut_envs.copy()
        # generate list of worker names
        list_of_workers = []
        for worker in range(self.num_worker):
            #worker_full_name = "{name_worker}-{worker_number}".format(name_worker=name_worker, worker_number=worker, worker_service=name_worker)
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(name_worker=name_worker, worker_number=worker, worker_service=name_service_headless)
            list_of_workers.append(worker_full_name)
        list_of_workers_as_string = ",".join(list_of_workers)
        env['BEXHOMA_WORKER_LIST'] = list_of_workers_as_string
        list_of_workers_as_string_space = " ".join(list_of_workers)
        env['BEXHOMA_WORKER_LIST_SPACE'] = list_of_workers_as_string_space
        env['BEXHOMA_SUT_NAME'] = name
        if self.num_worker > 0:
            #worker_full_name = "{name_worker}-{worker_number}".format(name_worker=name_worker, worker_number=0, worker_service=name_worker)
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(name_worker=name_worker, worker_number=0, worker_service=name_service_headless)
            env['BEXHOMA_WORKER_FIRST'] = worker_full_name
        env['STATEFULSET_NAME'] = name_worker
        # resources
        #specs = instance.split("-")
        #print(specs)
        #cpu = specs[0]
        #mem = specs[1]
        #node = ''
        #gpu = ''
        #if len(specs) > 2:
        #    gpu = specs[2]
        #    node= specs[3]
        sut_manifest_file = self.experiment.cluster.yamlfolder+template
        #print(sut_manifest_file)
        with open(sut_manifest_file) as stream:
            try:
                result=yaml.safe_load_all(stream)
                result = [data for data in result]
                #print(result)
            except yaml.YAMLError as exc:
                print(exc)
        for key in reversed(range(len(result))):#enumerate(result):
            dep = result[key]
            if dep['kind'] == 'PersistentVolumeClaim':
                pvc = dep['metadata']['name']
                #print("PVC", pvc, name_pvc)
                if not use_storage:
                    del result[key]
                else:
                    self.logger.debug('configuration.start_sut(PVC={},{})'.format(pvc, name_pvc))
                    dep['metadata']['name'] = name_pvc
                    #self.service = dep['metadata']['name']
                    dep['metadata']['labels']['app'] = app
                    dep['metadata']['labels']['component'] = 'storage'
                    dep['metadata']['labels']['configuration'] = storageConfiguration
                    dep['metadata']['labels']['experiment'] = self.storage_label
                    dep['metadata']['labels']['dbms'] = self.docker
                    dep['metadata']['labels']['volume'] = self.volume
                    dep['metadata']['labels']['loaded'] = "False"
                    for label_key, label_value in self.additional_labels.items():
                        dep['metadata']['labels'][label_key] = str(label_value)
                    if self.storage['storageClassName'] is not None and len(self.storage['storageClassName']) > 0:
                        dep['spec']['storageClassName'] = self.storage['storageClassName']
                        #print(dep['spec']['storageClassName'])
                    else:
                        del result[key]['spec']['storageClassName']
                    if len(self.storage['storageSize']) > 0:
                        dep['spec']['resources']['requests']['storage'] = self.storage['storageSize']
                    #print(dep['spec']['accessModes']) # list
                    #print(dep['spec']['resources']['requests']['storage'])
                    pvcs = self.experiment.cluster.get_pvc(app=app, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
                    #print(pvcs)
                    if len(pvcs) > 0:
                        print("{:30s}: storage {} exists".format(configuration, name_pvc))
                        if not self.loading_finished and self.experiment.args_dict['request_storage_remove']:
                            # we have not loaded yet, so this is the first run in this experiment
                            print("{:30s}: storage {} should be removed".format(configuration, name_pvc))
                            self.experiment.cluster.delete_pvc(name_pvc)
                            self.wait(10)
                            pvcs = self.experiment.cluster.get_pvc(app=app, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
                            while len(pvcs) > 0:
                                print("{:30s}: storage {} still exists".format(configuration, name_pvc))
                                self.wait(10)
                                pvcs = self.experiment.cluster.get_pvc(app=app, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
                            print("{:30s}: storage {} is gone".format(configuration, name_pvc))
                        else:
                            yaml_deployment['spec']['template']['metadata']['labels']['storage_exists'] = "True"
                            pvcs_labels = self.experiment.cluster.get_pvc_labels(app=app, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
                            self.logger.debug(pvcs_labels)
                            if len(pvcs_labels) > 0:
                                pvc_labels = pvcs_labels[0]
                                copy_labels = ['loaded', 'timeLoading', 'timeLoadingStart', 'timeLoadingEnd', 'indexed', 'time_generated', 'time_indexed', 'time_ingested', 'time_initconstraints', 'time_initindexes', 'time_initschema', 'time_initstatistics', 'time_loaded']
                                for label in copy_labels:
                                    if label in pvc_labels:
                                        print("{:30s}: label {} copied value {}".format(configuration, label, pvc_labels[label]))
                                        yaml_deployment['spec']['template']['metadata']['labels'][label] = pvc_labels[label]
                                #if 'loaded' in pvc_labels:
                                #    yaml_deployment['spec']['template']['metadata']['labels']['loaded'] = pvc_labels['loaded']
                                #if 'timeLoading' in pvc_labels:
                                #    yaml_deployment['spec']['template']['metadata']['labels']['timeLoading'] = pvc_labels['timeLoading']
                                #if 'timeLoadingStart' in pvc_labels:
                                #    yaml_deployment['spec']['template']['metadata']['labels']['timeLoadingStart'] = pvc_labels['timeLoadingStart']
                                #if 'timeLoadingEnd' in pvc_labels:
                                #    yaml_deployment['spec']['template']['metadata']['labels']['timeLoadingEnd'] = pvc_labels['timeLoadingEnd']
                            del result[key]
                            # we do not need loading pods
                            #print("Loading is set to finished")
                            print("{:30s}: loading is set to finished".format(configuration))
                            self.loading_active = False
                            self.monitor_loading = False
            if dep['kind'] == 'StatefulSet':
                if self.num_worker == 0:
                    del result[key]
                    continue
                # set meta data
                dep['metadata']['name'] = name_worker
                #self.service = dep['metadata']['name']
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = 'worker'
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = self.docker
                dep['metadata']['labels']['volume'] = self.volume
                for label_key, label_value in self.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['spec']['replicas'] = self.num_worker
                dep['spec']['serviceName'] = name_worker
                dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                #dep['spec']['selector'] = dep['metadata']['labels'].copy()
                self.worker_containers_deployed = []
                for i_container, container in enumerate(dep['spec']['template']['spec']['containers']):
                    self.worker_containers_deployed.append(container['name'])
                    #container = dep['spec']['template']['spec']['containers'][0]['name']
                    #print("Container", container)
                    # get and set ENV
                    #env_manifest = {}
                    #envs = container['env']
                    #for num_env, e in enumerate(envs):
                    #    env_manifest[e['name']] = e['value']
                    #print(env_manifest)
                    #env_merged = {**env_manifest, **env}
                    #print(env_merged)
                    self.logger.debug('configuration.create_manifest_statefulset({})'.format(env))
                    #if not 'env' in dep['spec']['template']['spec']['containers'][i_container]:
                    #print(dep['spec']['template']['spec']['containers'][i_container])
                    if not 'env' in dep['spec']['template']['spec']['containers'][i_container] or dep['spec']['template']['spec']['containers'][i_container]['env'] is None:
                        dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    #dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    #print(dep['spec']['template']['spec']['containers'][i_container]['env'])
                    for i_env,e in env.items():
                        index_of_env = next((i for i, d in enumerate(dep['spec']['template']['spec']['containers'][i_container]['env']) if d.get('name') == i_env), -1)
                        #print("*************ENV*********", env, i_env, index_of_env)
                        if index_of_env >= 0:
                            # update value of existing env
                            dep['spec']['template']['spec']['containers'][i_container]['env'][index_of_env]['value'] = str(e)
                        else:
                            # append new env
                            dep['spec']['template']['spec']['containers'][i_container]['env'].append({'name':i_env, 'value':str(e)})
                    #for i_env,e in env.items():
                    #    dep['spec']['template']['spec']['containers'][i_container]['env'].append({'name':i_env, 'value':str(e)})
                    if container['name'] == 'dbms':
                        #print(container['volumeMounts'])
                        for j, vol in enumerate(container['volumeMounts']):
                            if vol['name'] == 'bxw':
                                #print(vol['mountPath'])
                                if not use_storage:
                                    del result[key]['spec']['template']['spec']['containers'][i_container]['volumeMounts'][j]
                    elif not self.monitoring_active or self.experiment.cluster.monitor_cluster_active or self.experiment.cluster.monitor_cluster_exists:
                        # remove monitoring containers
                        if container['name'] == 'cadvisor':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            self.worker_containers_deployed.pop()
                        if container['name'] == 'dcgm-exporter':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            self.worker_containers_deployed.pop()
                # remove volumes
                for j, vol in enumerate(dep['spec']['template']['spec']['volumes']):
                    if vol['name'] == 'bxw':
                        #print(vol['mountPath'])
                        if not use_storage:
                            del result[key]['spec']['template']['spec']['volumes'][j]
                # remove storage template if not used
                if 'volumeClaimTemplates' in result[key]['spec']:
                    if not use_storage:
                        del result[key]['spec']['volumeClaimTemplates']
                    else:
                        #result[key]['spec']['volumeClaimTemplates'][0]['metadata']['name'] = name_worker
                        #self.service = dep['metadata']['name']
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['app'] = app
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['component'] = 'worker'
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['configuration'] = storageConfiguration
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['experiment'] = self.storage_label
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['dbms'] = self.docker
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['volume'] = self.volume
                        for label_key, label_value in self.additional_labels.items():
                            result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels'][label_key] = str(label_value)
                        #print(result[key]['spec']['volumeClaimTemplates'])
                        if self.storage['storageClassName'] is not None and len(self.storage['storageClassName']) > 0:
                            dep['spec']['volumeClaimTemplates'][0]['spec']['storageClassName'] = self.storage['storageClassName']
                            #print(dep['spec']['storageClassName'])
                        else:
                            del result[key]['spec']['storageClassName']
                        if len(self.storage['storageSize']) > 0:
                            dep['spec']['volumeClaimTemplates'][0]['spec']['resources']['requests']['storage'] = self.storage['storageSize']
                #print(pvc)
            if dep['kind'] == 'Job':
                # set meta data
                dep['metadata']['name'] = name_worker
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = 'worker'
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = self.docker
                dep['metadata']['labels']['volume'] = self.volume
                for label_key, label_value in self.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                for i_container, container in enumerate(dep['spec']['template']['spec']['containers']):
                    #container = dep['spec']['template']['spec']['containers'][0]['name']
                    self.logger.debug('configuration.add_env({})'.format(env))
                    #dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    if not 'env' in dep['spec']['template']['spec']['containers'][i_container] or dep['spec']['template']['spec']['containers'][i_container]['env'] is None:
                        dep['spec']['template']['spec']['containers'][i_container]['env'] = list()
                    for i_env,e in env.items():
                        index_of_env = next((i for i, d in enumerate(dep['spec']['template']['spec']['containers'][i_container]['env']) if d.get('name') == i_env), -1)
                        if index_of_env >= 0:
                            # update value of existing env
                            dep['spec']['template']['spec']['containers'][i_container]['env'][index_of_env]['value'] = str(e)
                        else:
                            # append new env
                            dep['spec']['template']['spec']['containers'][i_container]['env'].append({'name':i_env, 'value':str(e)})
                    #for i_env,e in env.items():
                    #    dep['spec']['template']['spec']['containers'][i_container]['env'].append({'name':i_env, 'value':str(e)})                #print(pvc)
            if dep['kind'] == 'Service':
                if dep['metadata']['name'] == 'bexhoma-worker': #!= 'bexhoma-service':
                    if self.num_worker == 0:
                        del result[key]
                        continue
                    dep['metadata']['name'] = name_service_headless# name_worker
                    dep['metadata']['labels']['app'] = app
                    dep['metadata']['labels']['component'] = 'worker'
                    dep['metadata']['labels']['configuration'] = configuration
                    dep['metadata']['labels']['experiment'] = experiment
                    dep['metadata']['labels']['dbms'] = self.docker
                    dep['metadata']['labels']['volume'] = self.volume
                    for label_key, label_value in self.additional_labels.items():
                        dep['metadata']['labels'][label_key] = str(label_value)
                    #dep['spec']['selector'] = dep['metadata']['labels'].copy()
                    dep['spec']['selector']['configuration'] = configuration
                    dep['spec']['selector']['experiment'] = experiment
                    dep['spec']['selector']['dbms'] = self.docker
                    dep['spec']['selector']['volume'] = self.volume
                    if not self.monitoring_active or (self.experiment.cluster.monitor_cluster_exists and not self.monitor_app_active):
                        for i, ports in reversed(list(enumerate(dep['spec']['ports']))):
                            # remove monitoring ports
                            if 'name' in ports and ports['name'] != 'port-dbms' and ports['name'] != 'port-bus':
                                del result[key]['spec']['ports'][i]
                    continue
                if dep['metadata']['name'] == 'bexhoma-pool': #!= 'bexhoma-service':
                    dep['metadata']['name'] = name_pool
                    dep['metadata']['labels']['app'] = app
                    dep['metadata']['labels']['component'] = 'pool'
                    dep['metadata']['labels']['configuration'] = configuration
                    dep['metadata']['labels']['experiment'] = experiment
                    dep['metadata']['labels']['dbms'] = self.docker
                    dep['metadata']['labels']['volume'] = self.volume
                    for label_key, label_value in self.additional_labels.items():
                        dep['metadata']['labels'][label_key] = str(label_value)
                    #dep['spec']['selector'] = dep['metadata']['labels'].copy()
                    dep['spec']['selector']['configuration'] = configuration
                    dep['spec']['selector']['experiment'] = experiment
                    dep['spec']['selector']['dbms'] = self.docker
                    dep['spec']['selector']['volume'] = self.volume
                    continue
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = self.docker
                dep['metadata']['labels']['volume'] = self.volume
                for label_key, label_value in self.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                #dep['spec']['selector'] = dep['metadata']['labels'].copy()
                dep['spec']['selector']['configuration'] = configuration
                dep['spec']['selector']['experiment'] = experiment
                dep['spec']['selector']['dbms'] = self.docker
                dep['spec']['selector']['volume'] = self.volume
                dep['metadata']['name'] = name
                self.service = dep['metadata']['name']
                if not self.monitoring_active or (self.experiment.cluster.monitor_cluster_exists and not self.monitor_app_active):
                    for i, ports in reversed(list(enumerate(dep['spec']['ports']))):
                        # remove monitoring ports
                        if 'name' in ports and ports['name'] != 'port-dbms' and ports['name'] != 'port-bus':
                            del result[key]['spec']['ports'][i]
                #print(pvc)
            if dep['kind'] == 'Deployment':
                if dep['metadata']['name'] == 'bexhoma-pool':
                    dep['metadata']['name'] = name_pool
                    dep['metadata']['labels']['component'] = 'pool'
                else:
                    yaml_deployment = result[key]       # this will be marked 'loaded' iff pvc exists
                    dep['metadata']['name'] = name
                    dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = self.docker
                dep['metadata']['labels']['volume'] = self.volume
                dep['metadata']['labels']['sut'] = name
                dep['metadata']['labels']['pool'] = name_pool
                for label_key, label_value in self.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
                dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                #deployment = dep['metadata']['name']
                #appname = dep['spec']['template']['metadata']['labels']['app']
                if dep['metadata']['name'] != name_pool:
                    self.sut_containers_deployed = []
                else:
                    self.pool_containers_deployed = []
                for i_container, container in reversed(list(enumerate(dep['spec']['template']['spec']['containers']))):
                    if dep['metadata']['name'] != name_pool:
                        self.sut_containers_deployed.append(container['name'])
                    else:
                        self.pool_containers_deployed.append(container['name'])
                    self.logger.debug('configuration.create_manifest_deployment({})'.format(env))
                    #if not 'env' in dep['spec']['template']['spec']['containers'][i_container]:
                    if not 'env' in dep['spec']['template']['spec']['containers'][i_container] or dep['spec']['template']['spec']['containers'][i_container]['env'] is None:
                        dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    #dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    for i_env,e in env.items():
                        index_of_env = next((i for i, d in enumerate(dep['spec']['template']['spec']['containers'][i_container]['env']) if d.get('name') == i_env), -1)
                        if index_of_env >= 0:
                            # update value of existing env
                            dep['spec']['template']['spec']['containers'][i_container]['env'][index_of_env]['value'] = str(e)
                        else:
                            # append new env
                            dep['spec']['template']['spec']['containers'][i_container]['env'].append({'name':i_env, 'value':str(e)})
                    #container = dep['spec']['template']['spec']['containers'][0]['name']
                    #print("Container", container)
                    if container['name'] == 'dbms':
                        #print(container['volumeMounts'])
                        if 'volumeMounts' in container and len(container['volumeMounts']) > 0:
                            for j, vol in reversed(list(enumerate(container['volumeMounts']))):
                                if vol['name'] == 'benchmark-storage-volume':
                                    #print(vol['mountPath'])
                                    if not use_storage:
                                        del result[key]['spec']['template']['spec']['containers'][i_container]['volumeMounts'][j]
                                if vol['name'] == 'benchmark-data-volume':
                                    #print(vol['mountPath'])
                                    if not use_data:
                                        del result[key]['spec']['template']['spec']['containers'][i_container]['volumeMounts'][j]
                        if self.dockerimage:
                            result[key]['spec']['template']['spec']['containers'][i_container]['image'] = self.dockerimage
                        else:
                            self.dockerimage = result[key]['spec']['template']['spec']['containers'][i_container]['image']
                    elif not self.monitoring_active or self.experiment.cluster.monitor_cluster_active or self.experiment.cluster.monitor_cluster_exists:
                        # remove monitoring containers
                        if container['name'] == 'cadvisor':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            self.sut_containers_deployed.pop()
                        if container['name'] == 'dcgm-exporter':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            self.sut_containers_deployed.pop()
                if 'volumes' in dep['spec']['template']['spec']:
                    for i, vol in reversed(list(enumerate(dep['spec']['template']['spec']['volumes']))):
                        if vol['name'] == 'benchmark-storage-volume':
                            if not use_storage:
                                del result[key]['spec']['template']['spec']['volumes'][i]
                            else:
                                vol['persistentVolumeClaim']['claimName'] = name_pvc
                        if vol['name'] == 'benchmark-data-volume':
                            if not use_data:
                                del result[key]['spec']['template']['spec']['volumes'][i]
                        if 'hostPath' in vol and not self.monitoring_active:
                            # we only need hostPath for monitoring
                                del result[key]['spec']['template']['spec']['volumes'][i]
                # init containers only for persistent volumes
                if 'initContainers' in result[key]['spec']['template']['spec'] and not use_storage:
                    del result[key]['spec']['template']['spec']['initContainers']
                #print(deployment)
                #print(appname)
                # parameter from instance name
                # request = limit
                # we only want to manipulate nodeSelector for pool container in pooler
                if dep['metadata']['name'] == name_pool:
                    if 'replicas_pooling' in self.resources:
                        num_replicas_pooling = self.resources['replicas_pooling']
                        result[key]['spec']['replicas'] = num_replicas_pooling
                    """if 'nodeSelector' in self.resources:
                        nodeSelectors = self.resources['nodeSelector'].copy()
                    else:
                        nodeSelectors = {}
                    for nodeSelector, value in nodeSelectors.items():
                        if nodeSelector == 'cpu' or nodeSelector == 'gpu':
                            continue
                        else:
                            dep['spec']['template']['spec']['nodeSelector'][nodeSelector] = value
                            #self.resources['nodeSelector'][nodeSelector] = value """
                # we only want to manipulate resources for dbms container in SUT
                if dep['metadata']['name'] == name:
                    for i_container, container in reversed(list(enumerate(dep['spec']['template']['spec']['containers']))):
                        if container['name'] == 'dbms':
                            break
                    """req_cpu = self.resources['requests']['cpu']
                    req_mem = self.resources['requests']['memory']
                    limit_cpu = self.resources['limits']['cpu']
                    limit_mem = self.resources['limits']['memory']
                    node_cpu = ''
                    node = self.resources['nodeSelector']['node']
                    gpu = self.resources['requests']['gpu']
                    req_cpu = cpu
                    limit_cpu = cpu
                    req_mem = mem
                    limit_mem = mem
                    req_gpu = gpu
                    node_cpu = ''
                    node_gpu = node"""
                    req_cpu = 0
                    limit_cpu = 0
                    req_mem = 0
                    limit_mem = 0
                    req_gpu = 0
                    node_cpu = ''
                    node_gpu = ''
                    # should be overwritten by resources dict?
                    if 'requests' in self.resources and 'cpu' in self.resources['requests']:
                        req_cpu = self.resources['requests']['cpu']
                    if 'requests' in self.resources and 'memory' in self.resources['requests']:
                        req_mem = self.resources['requests']['memory']
                    if 'limits' in self.resources and 'cpu' in self.resources['limits']:
                        limit_cpu = self.resources['limits']['cpu']
                    if 'limits' in self.resources and 'memory' in self.resources['limits']:
                        limit_mem = self.resources['limits']['memory']
                    #nodeSelector: {cpu: epyc-7542}
                    if 'nodeSelector' in self.resources and 'cpu' in self.resources['nodeSelector']:
                        node_cpu = self.resources['nodeSelector']['cpu']
                    if 'nodeSelector' in self.resources and 'gpu' in self.resources['nodeSelector']:
                        node_gpu = self.resources['nodeSelector']['gpu']
                    if 'nodeSelector' in self.resources:
                        nodeSelectors = self.resources['nodeSelector'].copy()
                    else:
                        nodeSelectors = {}
                    num_replicas_pooling = 0
                    if 'replicas_pooling' in self.resources:
                        num_replicas_pooling = self.resources['replicas_pooling']
                    #print(nodeSelectors)
                    # we want to have a resource dict anyway!
                    self.resources = {}
                    self.resources['requests'] = {}
                    self.resources['requests']['cpu'] = req_cpu
                    self.resources['requests']['memory'] = req_mem
                    self.resources['requests']['gpu'] = req_gpu
                    self.resources['limits'] = {}
                    self.resources['limits']['cpu'] = limit_cpu
                    self.resources['limits']['memory'] = limit_mem
                    self.resources['nodeSelector'] = {}
                    self.resources['nodeSelector']['cpu'] = node_cpu
                    self.resources['nodeSelector']['gpu'] = node_gpu
                    if num_replicas_pooling > 0:
                        self.resources['replicas_pooling'] = num_replicas_pooling
                    #print(self.resources)
                    # put resources to yaml file
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['cpu'] = req_cpu
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['cpu'] = limit_cpu
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['memory'] = req_mem
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['memory'] = limit_mem
                    #print(dep['spec']['template']['spec']['containers'][i_container]['resources']['limits'])
                    # remove limits if = 0
                    if limit_cpu == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['cpu']
                    if limit_mem == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['memory']
                    # remove requests if = 0
                    if req_cpu == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['cpu']
                    if req_mem == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['memory']
                    #print(dep['spec']['template']['spec']['containers'][i_container]['resources']['limits'])
                    # add resource gpu
                    #if len(specs) > 2:
                    if node_gpu:
                        if not 'nodeSelector' in dep['spec']['template']['spec']:
                            dep['spec']['template']['spec']['nodeSelector'] = {}
                        if dep['spec']['template']['spec']['nodeSelector'] is None:
                            dep['spec']['template']['spec']['nodeSelector'] = {}
                        dep['spec']['template']['spec']['nodeSelector']['gpu'] = node_gpu
                        dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['nvidia.com/gpu'] = int(req_gpu)
                    else:
                        if 'nvidia.com/gpu' in dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']:
                            del dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['nvidia.com/gpu']
                    # add resource cpu
                    #if node_cpu:
                    if not 'nodeSelector' in dep['spec']['template']['spec']:
                        dep['spec']['template']['spec']['nodeSelector'] = {}
                    if dep['spec']['template']['spec']['nodeSelector'] is None:
                        dep['spec']['template']['spec']['nodeSelector'] = {}
                    dep['spec']['template']['spec']['nodeSelector']['cpu'] = node_cpu
                    if node_cpu == '':
                        del dep['spec']['template']['spec']['nodeSelector']['cpu']
                    # nodeSelector that is not cpu or gpu is copied to yaml
                    for nodeSelector, value in nodeSelectors.items():
                        if nodeSelector == 'cpu' or nodeSelector == 'gpu':
                            continue
                        else:
                            dep['spec']['template']['spec']['nodeSelector'][nodeSelector] = value
                            self.resources['nodeSelector'][nodeSelector] = value
                    # set nodeSelector
                    if 'sut' in self.nodes:
                        if not 'nodeSelector' in dep['spec']['template']['spec']:
                            dep['spec']['template']['spec']['nodeSelector'] = dict()
                        if dep['spec']['template']['spec']['nodeSelector'] is None:
                            dep['spec']['template']['spec']['nodeSelector'] = dict()
                        dep['spec']['template']['spec']['nodeSelector']['type'] = self.nodes['sut']
                    #print('nodeSelector', dep['spec']['template']['spec']['nodeSelector'])
            #if dep['kind'] == 'Service':
            #    service = dep['metadata']['name']
            #    #print(service)
        #with open(self.yamlfolder+"deployment-"+self.d+"-"+instance+".yml","w+") as stream:
        with open(deployment_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        self.logger.debug("Deploy "+deployment_experiment)
        self.experiment.cluster.kubectl('create -f '+deployment_experiment)
        #if self.experiment.monitoring_active:
        #    self.start_monitoring()
        return True
    def stop_sut(self, app='', component='sut', experiment='', configuration=''):
        """
        Stops a sut deployment and removes all its services and (optionally) stateful sets.
        It also stops and removes all related components (monitoring, maintaining, loading).

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        if len(self.storage) > 0 and 'keep' in self.storage and self.storage['keep']:
            # keep the storage
            pass
        else:
            use_storage = self.use_storage()
            if use_storage:
                # remove the storage
                if self.storage['storageConfiguration']:
                    storageConfiguration = self.storage['storageConfiguration']
                else:
                    storageConfiguration = configuration
                name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
                self.experiment.cluster.delete_pvc(name_pvc)
                worker_pvcs = self.experiment.cluster.get_pvc(app=app, component='worker', experiment=experiment, configuration=storageConfiguration)
                for name_pvc in worker_pvcs:
                    self.experiment.cluster.delete_pvc(name_pvc)
        deployments = self.experiment.cluster.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            self.experiment.cluster.delete_deployment(deployment)
        stateful_sets = self.experiment.cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
        for stateful_set in stateful_sets:
            self.experiment.cluster.delete_stateful_set(stateful_set)
        jobs = self.experiment.cluster.get_jobs(app=app, component=component, experiment=experiment, configuration=configuration)
        for job in jobs:
            self.experiment.cluster.delete_job(job)
        services = self.experiment.cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            self.experiment.cluster.delete_service(service)
        if self.experiment.monitoring_active:
            self.stop_monitoring()
        if self.experiment.maintaining_active:
            self.stop_maintaining()
        if self.experiment.loading_active:
            self.stop_loading()
        if component == 'sut':
            self.stop_sut(app=app, component='worker', experiment=experiment, configuration=configuration)
            self.stop_sut(app=app, component='worker', experiment=self.experiment_name, configuration=configuration)
            self.stop_sut(app=app, component='pool', experiment=experiment, configuration=configuration)
    def get_host_gpus(self):
        """
        Returns information about the sut's host GPUs.
        Basically this calls `nvidia-smi` on the host.

        :return: GPUs of the host
        """
        self.logger.debug('configuration.get_host_gpus)')
        #print("checkGPUs")
        cmd = {}
        cmd['check_gpus'] = 'nvidia-smi'
        stdin, stdout, stderr = self.execute_command_in_pod_sut(cmd['check_gpus'])
    def check_DBMS_connection(self, ip, port):
        """
        Check if DBMS is open for connections.
        Tries to open a socket to ip:port.
        Returns True if this is possible.

        :param ip: IP of the host to connect to
        :param port: Port of the server on the host to connect to
        :return: True, iff connecting is possible
        """
        self.logger.debug('configuration.check_DBMS_connection()')
        found = False
        s = socket.socket()
        s.settimeout(10)
        try:
            s.connect((ip, port))
            found = True
            print("Somebody is answering at %s:%d" % (ip, port))
        except Exception as e:
            print("Nobody is answering yet at %s:%d" % (ip, port))
        finally:
            s.close()
        return found
    def get_host_volume(self, pod=''):
        """
        Returns information about the sut's mounted volumes.
        Basically this calls something equivalent to
        size: df -h | grep volumes | awk -F ' ' '{print $2}'
        used: df -h | grep volumes | awk -F ' ' '{print $3}'

        :return: (size, used)
        """
        self.logger.debug('configuration.get_host_volume()')
        try:
            #command = "df -h | grep volumes | awk -F ' ' '{print $2}'"
            command = "df -hP | grep volumes"
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command, pod=pod)
            parts = stdout.split(" ")
            parts = [x for x in parts if x != '']
            if len(parts) > 2:
                size = parts[1]
                #command = "df -h | grep volumes | awk -F ' ' '{print $3}'"
                #stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
                used = parts[2]
                return size, used
            else:
                return 0,0
        except Exception as e:
            logging.error(e)
            return "", ""
    def get_host_hugepages_total(self):
        """
        Returns information about the sut's huge pages setting.
        Basically this calls `cat /proc/meminfo | grep HugePages_Total` on the host.

        :return: HugePages_Total setting of the host
        """
        self.logger.debug('configuration.get_host_memory()')
        try:
            command = "cat /proc/meminfo | grep HugePages_Total"
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
            result = stdout
            mem =  int(result.replace(" ","").replace("HugePages_Total:",""))
            return mem
        except Exception as e:
            logging.error(e)
            return 0
    def get_host_hugepages_free(self):
        """
        Returns information about the sut's huge pages setting.
        Basically this calls `cat /proc/meminfo | grep HugePages_Free` on the host.

        :return: HugePages_Free setting of the host
        """
        self.logger.debug('configuration.get_host_memory()')
        try:
            command = "cat /proc/meminfo | grep HugePages_Free"
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
            result = stdout
            mem =  int(result.replace(" ","").replace("HugePages_Free:",""))
            return mem
        except Exception as e:
            logging.error(e)
            return 0
    def get_host_cpulist(self):
        """
        Returns information about the sut's host RAM.
        Basically this calls `grep MemTotal /proc/meminfo` on the host.

        :return: RAM of the host
        """
        self.logger.debug('configuration.get_host_cpulist()')
        try:
            command = "grep ^Cpus_allowed_list /proc/self/status | awk '{print $2}'"
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
            result = stdout.replace('Cpus_allowed_list:\t', '').replace('\n', '')
            return result
        except Exception as e:
            logging.error(e)
            return ""
    def get_host_memory(self):
        """
        Returns information about the sut's host RAM.
        Basically this calls `grep MemTotal /proc/meminfo` on the host.

        :return: RAM of the host
        """
        self.logger.debug('configuration.get_host_memory()')
        try:
            command = "grep MemTotal /proc/meminfo | awk '{print $2}'"
            #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
            result = stdout#os.popen(fullcommand).read()
            mem =  int(result.replace(" ","").replace("MemTotal:","").replace("kB",""))*1024#/1024/1024/1024
            return mem
        except Exception as e:
            logging.error(e)
            return 0
    def get_host_cpu(self):
        """
        Returns information about the sut's host CPU.
        Basically this calls `more /proc/cpuinfo | grep 'model name'` on the host.

        :return: CPU of the host
        """
        self.logger.debug('configuration.get_host_cpu()')
        command = 'more /proc/cpuinfo | grep \'model name\' | head -n 1'
        #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        #cpu = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
        cpu = stdout#os.popen(fullcommand).read()
        cpu = cpu.replace('model name\t: ', '')
        #cpu = cpu.replace('model name\t: ', 'CPU: ')
        return cpu.replace('\n','')
    def get_host_cores(self):
        """
        Returns information about the sut's host CPU's cores.
        Basically this calls `grep -c ^processor /proc/cpuinfo` on the host.

        :return: CPU's cores of the host
        """
        self.logger.debug('configuration.get_host_cores()')
        cmd = {}
        command = 'grep -c ^processor /proc/cpuinfo'
        #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        #cores = os.popen(fullcommand).read()
        try:
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
            cores = stdout#os.popen(fullcommand).read()
            if len(cores)>0:
                return int(cores)
            else:
                return 0
        except Exception as e:
            logging.error(e)
            return 0
    def get_host_system(self):
        """
        Returns information about the sut's host OS.
        Basically this calls `uname -r` on the host.

        :return: OS of the host
        """
        self.logger.debug('configuration.get_host_system()')
        cmd = {}
        command = 'uname -r'
        #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        #host = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
        host = stdout#os.popen(fullcommand).read()
        return host.replace('\n','')
    def get_host_restarts(self, pod_sut=''):
        """
        Returns information about the sut's host name.
        Basically this calls `kubectl get pod` to receive the information.

        :return: Node name of the host
        """
        self.logger.debug('configuration.get_host_restarts()')
        if len(pod_sut) == 0:
            pod_sut = self.pod_sut
        cmd = {}
        #fullcommand = 'kubectl get pods/'+self.pod_sut+' -o=json'
        result = self.experiment.cluster.kubectl('get pods/'+pod_sut+' -o jsonpath="{.status.containerStatuses[*].restartCount}"')#self.yamlfolder+deployment)
        #result = os.popen(fullcommand).read()
        try:
            #print(result)
            return result
        except Exception as e:
            return ""
        return ""
    def get_host_node(self):
        """
        Returns information about the sut's host name.
        Basically this calls `kubectl get pod` to receive the information.

        :return: Node name of the host
        """
        self.logger.debug('configuration.get_host_node()')
        cmd = {}
        #fullcommand = 'kubectl get pods/'+self.pod_sut+' -o=json'
        result = self.experiment.cluster.kubectl('get pods/'+self.pod_sut+' -o=json')#self.yamlfolder+deployment)
        #result = os.popen(fullcommand).read()
        try:
            datastore = json.loads(result)
            #print(datastore)
            # why check app? if not managed by bexhoma, this will be completely different
            #if self.appname == datastore['metadata']['labels']['app']:
            if self.pod_sut == datastore['metadata']['name']:
                node = datastore['spec']['nodeName']
                return node
        except Exception as e:
            return ""
        return ""
    def get_host_gpus(self):
        """
        Returns information about the sut's host GPUs.
        Basically this calls `nvidia-smi -L` on the host and aggregates result.

        :return: GPUs of the host
        """
        self.logger.debug('configuration.get_host_gpus()')
        cmd = {}
        command = 'nvidia-smi -L'
        #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        #gpus = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
        gpus = stdout#os.popen(fullcommand).read()
        l = gpus.split("\n")
        c = Counter([x[x.find(":")+2:x.find("(")-1] for x in l if len(x)>0])
        result = ""
        for i,j in c.items():
            result += str(j)+" x "+i
        return result
    def get_host_gpu_ids(self):
        """
        Returns information about the sut's host GPUs.
        Basically this calls `nvidia-smi -L` on the host and generates a list of UUIDs of the GPUs.

        :return: List of GPU UUIDs of the host
        """
        self.logger.debug('configuration.get_host_gpu_ids()')
        cmd = {}
        command = 'nvidia-smi -L'
        #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        #gpus = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
        gpus = stdout#os.popen(fullcommand).read()
        l = gpus.split("\n")
        result = []
        for i,gpu in enumerate(l):
            id = gpu[gpu.find('UUID: ')+6:gpu.find(')', gpu.find('UUID: '))]
            if len(id) > 0:
                result.append(id)
        return result
    def get_host_cuda(self):
        """
        Returns information about the sut's host CUDA version.
        Basically this calls `nvidia-smi | grep 'CUDA'` on the host.

        :return: CUDA version of the host
        """
        self.logger.debug('configuration.get_host_cuda()')
        cmd = {}
        command = 'nvidia-smi | grep \'CUDA\''
        #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        #cuda = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
        cuda = stdout#os.popen(fullcommand).read()
        return cuda.replace('|', '').replace('\n','').strip()
    def getTimediff(self):
        self.logger.debug('configuration.getTimediff()')
        cmd = {}
        command = 'date +"%s"'
        #fullcommand = 'kubectl exec '+cluster.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
        timestamp_remote = stdout#os.popen(fullcommand).read()
        #timestamp_remote = os.popen(fullcommand).read()
        timestamp_local = os.popen(command).read()
        #print(timestamp_remote)
        #print(timestamp_local)
        return int(timestamp_remote)-int(timestamp_local)
    def get_host_diskspace_used_data(self):
        """
        Returns information about the sut's host disk space used for the data (the database) in kilobyte.
        Basically this calls `du` on the host directory that is mentioned in cluster.config as to store the database.

        :return: Size of disk used for database in Kilobytes
        """
        self.logger.debug('configuration.get_host_diskspace_used_data()')
        cmd = {}
        if 'datadir' in self.dockertemplate:
            datadir = self.dockertemplate['datadir']
        else:
            return 0
        try:
            command = "du --block-size=1M -Ls "+datadir+" | awk 'END{print \\$1}'"
            cmd['disk_space_used'] = command
            stdin, stdout, stderr = self.execute_command_in_pod_sut(cmd['disk_space_used'])
            return int(stdout.replace('\n',''))
        except Exception as e:
            # Windows
            command = "du --block-size=1M -Ls "+datadir+" | awk 'END{print $1}'"
            cmd['disk_space_used'] = command
            try:
                stdin, stdout, stderr = self.execute_command_in_pod_sut(cmd['disk_space_used'])
                if len(stdout) > 0:
                    size_str = stdout.replace('\n','')
                    if len(size_str) > 0:
                        return int(size_str)
            except Exception as e:
                return 0
        return 0
    def get_host_diskspace_used(self):
        """
        Returns information about the sut's host disk space.
        Basically this calls `df /` on the host.

        :return: Size of disk in Kilobytes
        """
        self.logger.debug('configuration.get_host_diskspace_used()')
        disk = ''
        cmd = {}
        try:
            command = "df / | awk 'NR == 2{print \\$3}'"
            #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
            #disk = os.popen(fullcommand).read()
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
            disk = stdout#os.popen(fullcommand).read()
            return int(disk.replace('\n',''))
        except Exception as e:
            # Windows
            command = "df / | awk 'NR == 2{print $3}'"
            #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
            #disk = os.popen(fullcommand).read()
            try:
                stdin, stdout, stderr = self.execute_command_in_pod_sut(command=command)
                disk = stdout#os.popen(fullcommand).read()
                if len(disk) > 0:
                    return int(disk.replace('\n',''))
            except Exception as e:
                return 0
        # pipe to awk sometimes does not work
        #return int(disk.split('\t')[0])
        return 0
    def check_volumes(self):
        """
        Tests for mounted volume in SUT container and writes size and used info as label to pvc.
        """
        # add volume labels to PV
        app = self.appname
        use_storage = self.use_storage()
        if use_storage:
            if self.storage['storageConfiguration']:
                volume = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=self.storage['storageConfiguration'])
                volume_worker = self.generate_component_name(app=app, component='worker', experiment=self.storage_label, configuration=self.storage['storageConfiguration'])
            else:
                volume = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=self.configuration)
                volume_worker = self.generate_component_name(app=app, component='worker', experiment=self.storage_label, configuration=self.configuration)
            pods_worker = self.get_worker_pods()#self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
            # for worker pods: bexhoma-workers-
            #volume = name_pvc
            #volume_worker = "bexhoma-workers-{}".format(self.pod_sut)
            if volume:
                size, used = self.get_host_volume(pod=self.pod_sut)
                # write infos to SUT's PVC (if exists)
                fullcommand = 'label pvc {} --overwrite volume_size="{}" volume_used="{}"'.format(volume, size, used)
                #print(fullcommand)
                self.experiment.cluster.kubectl(fullcommand)
                ## write infos to worker's PVC (if exists)
                ## TODO: check if exists, test if it writes per worker size infos
                #fullcommand = 'label pvc {} --overwrite volume_size="{}" volume_used="{}"'.format(volume_worker, size, used)
                ##print(fullcommand)
                #self.experiment.cluster.kubectl(fullcommand)
            if volume_worker and pods_worker:
                for pod in pods_worker:
                    size, used = self.get_host_volume(pod=pod)
                    # write infos to SUT's PVC (if exists)
                    fullcommand = 'label pvc bxw-{} --overwrite volume_size="{}" volume_used="{}"'.format(pod, size, used)
                    #print(fullcommand)
                    self.experiment.cluster.kubectl(fullcommand)
                    ## write infos to worker's PVC (if exists)
                    ## TODO: check if exists, test if it writes per worker size infos
                    #fullcommand = 'label pvc {} --overwrite volume_size="{}" volume_used="{}"'.format(volume_worker, size, used)
                    ##print(fullcommand)
                    #self.experiment.cluster.kubectl(fullcommand)
    def get_host_all(self):
        """
        Calls all `get_host_x()` methods.
        Returns information about the sut's host as a dict.
        This requires self.pod_sut to carry the name of the SUTs pod.

        :return: Dict of informations about the host
        """
        server = {}
        server['RAM'] = self.get_host_memory()
        server['CPU'] = self.get_host_cpu()
        server['GPU'] = self.get_host_gpus()
        server['GPUIDs'] = self.get_host_gpu_ids()
        server['Cores'] = self.get_host_cores()
        server['host'] = self.get_host_system()
        server['node'] = self.get_host_node()
        server['disk'] = self.get_host_diskspace_used()
        server['datadisk'] = self.get_host_diskspace_used_data()
        size, used = self.get_host_volume()
        server['volume_size'] = size
        server['volume_used'] = used
        server['cuda'] = self.get_host_cuda()
        server['hugepages_total'] = self.get_host_hugepages_total()
        server['hugepages_free'] = self.get_host_hugepages_free()
        server['cpu_list'] = self.get_host_cpulist()
        server['cuda'] = self.get_host_cuda()
        return server
    def set_metric_of_config_default(self, metric, host, gpuid, schema, database, experiment=None):
        """
        Returns a promql query.
        Parameters in this query are substituted, so that prometheus finds the correct metric.
        Example: In 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))'
        configuration and experiment are placeholders and will be replaced by concrete values.
        This method contains the default behaviour for all components managed by bexhoma.
        For specific behaviour of other components not managed by bexhoma (e.g., a cloud dbms), overwrite set_metric_of_config().

        :param metric: Parametrized promql query
        :param host: Name of the host the metrics should be collected from
        :param gpuid: GPU that the metrics should watch
        :return: promql query without parameters
        """
        if experiment is None:
            experiment = self.code
        return metric.format(host=host, gpuid=gpuid, configuration=self.configuration.lower(), experiment=experiment, schema=schema, database=database)
    def set_metric_of_config(self, metric, host, gpuid, schema, database):
        """
        Returns a promql query.
        Parameters in this query are substituted, so that prometheus finds the correct metric.
        Example: In 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))'
        configuration and experiment are placeholders and will be replaced by concrete values.
        For specific behaviour of other components not managed by bexhoma (e.g., a cloud dbms), overwrite this method.
        The method set_metric_of_config_default() contains the default behaviour for all components managed by bexhoma.

        :param metric: Parametrized promql query
        :param host: Name of the host the metrics should be collected from
        :param gpuid: GPU that the metrics should watch
        :return: promql query without parameters
        """
        #use_storage = self.use_storage()
        # configure names
        if self.num_worker > 0: # and use_storage:
            # we assume here, a stateful set is used
            # this means we do not want to have the experiment code as part of the names
            # this would imply there cannot be experiment independent pvcs
            name_worker = self.get_worker_name()
            return metric.format(host=host, gpuid=gpuid, configuration=name_worker.lower(), experiment="", schema=schema, database=database)
        else:
            self.logger.debug(f"set_metric_of_config_default({metric}, {host}, {gpuid}, experiment={self.experiment_name}, schema={schema}, database={database})")
            return self.set_metric_of_config_default(metric, host, gpuid, experiment=self.experiment_name, schema=schema, database=database)
    def get_connection_config(self, connection, alias='', dialect='', serverip='localhost', monitoring_host='localhost'):
        """
        Returns information about the sut's host disk space.
        Basically this calls `df /` on the host.

        :return: Size of disk in Bytes
        """
        info = []
        self.connection = connection
        c = copy.deepcopy(self.dockertemplate['template'])
        if len(alias) > 0:
            c['alias'] = alias
        elif self.alias is not None:
            c['alias'] = self.alias
        else:
            c['alias'] = connection
        if len(dialect) > 0:
            c['dialect'] = dialect
        #c['docker_alias'] = self.docker['docker_alias']
        c['active'] = True
        c['name'] = connection
        c['docker'] = self.docker
        c['script'] = self.script
        c['info'] = info
        c['timeLoad'] = self.timeLoading # max span (generate + ingest) + schema + index
        c['timeGenerate'] = self.timeGenerating
        c['timeIngesting'] = self.timeIngesting
        c['timeSchema'] = self.timeSchema
        c['timeIndex'] = self.timeIndex
        c['script_times'] = self.times_scripts
        c['priceperhourdollar'] = 0.0  + self.dockertemplate['priceperhourdollar']
        # get hosts information
        pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
        self.pod_sut = pods[0]
        pod_sut = self.pod_sut
        c['hostsystem'] = self.get_host_all()
        # get worker information
        c['worker'] = []
        pods = self.get_worker_pods()#self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
        for pod in pods:
            self.pod_sut = pod
            print("{:30s}: distributed system - get host info for worker {}".format(self.configuration, pod))            
            c['worker'].append(self.get_host_all())
        self.pod_sut = pod_sut
        # take latest resources
        # TODO: read from yaml file
        if 'requests' in self.resources:
            c['hostsystem']['requests_cpu'] = self.resources['requests']['cpu']
            c['hostsystem']['requests_memory'] = self.resources['requests']['memory']
        else:
            c['hostsystem']['requests_cpu'] = 0
            c['hostsystem']['requests_memory'] = 0
        if 'limits' in self.resources:
            c['hostsystem']['limits_cpu'] = self.resources['limits']['cpu']
            c['hostsystem']['limits_memory'] = self.resources['limits']['memory']
        else:
            c['hostsystem']['limits_cpu'] = 0
            c['hostsystem']['limits_memory'] = 0
        #if len(cuda) > 0:
        #    c['hostsystem']['CUDA'] = cuda
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = self.connectionmanagement['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = self.connectionmanagement['runsPerConnection']
        c['connectionmanagement']['timeout'] = self.connectionmanagement['timeout']
        c['connectionmanagement']['singleConnection'] = self.connectionmanagement['singleConnection'] if 'singleConnection' in self.connectionmanagement else True
        c['monitoring'] = {}
        config_K8s = self.experiment.cluster.config['credentials']['k8s']
        if self.experiment.monitoring_active and 'monitor' in config_K8s:
            if len(c['hostsystem']['GPUIDs']) > 0:
                gpuid = '|'.join(c['hostsystem']['GPUIDs'])
            else:
                gpuid = ""
            node = c['hostsystem']['node']
            database = ""
            schema = ""
            if 'JDBC' in c:
                database = c['JDBC']['database'] if 'database' in c['JDBC'] else self.experiment.volume
                schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else 'default'
                #print(self.eval_parameters)
                if self.tenant_per == 'schema' and 'TENANT' in self.eval_parameters:
                    schema = 'tenant_'+self.eval_parameters['TENANT']
                elif self.tenant_per == 'database' and 'TENANT' in self.eval_parameters:
                    database = 'tenant_'+self.eval_parameters['TENANT']
            if 'grafanatoken' in config_K8s['monitor']:
                c['monitoring']['grafanatoken'] = config_K8s['monitor']['grafanatoken']
            if 'grafanaurl' in config_K8s['monitor']:
                c['monitoring']['grafanaurl'] = config_K8s['monitor']['grafanaurl']
            if 'grafanashift' in config_K8s['monitor']:
                c['monitoring']['shift'] = config_K8s['monitor']['grafanashift']
            if 'grafanaextend' in config_K8s['monitor']:
                c['monitoring']['extend'] = config_K8s['monitor']['grafanaextend']
            if 'prometheus_url' in config_K8s['monitor']:
                c['monitoring']['prometheus_url'] = config_K8s['monitor']['prometheus_url']
            if 'service_monitoring' in config_K8s['monitor']:
                c['monitoring']['prometheus_url'] = config_K8s['monitor']['service_monitoring'].format(service=monitoring_host, namespace=self.experiment.cluster.contextdata['namespace'])
            if 'service_monitoring_application' in config_K8s['monitor']:
                c['monitoring']['prometheus_url_application'] = config_K8s['monitor']['service_monitoring_application'].format(service=monitoring_host, namespace=self.experiment.cluster.contextdata['namespace'])
            #c['monitoring']['grafanaextend'] = 1
            c['monitoring']['metrics'] = {}             # default components (managed by bexhoma)
            c['monitoring']['metrics_special'] = {}     # other components (not managed by bexhoma)
            # cluster metrics
            if 'metrics' in config_K8s['monitor']:
                # set_metric_of_config_default
                for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                    # default components (managed by bexhoma)
                    c['monitoring']['metrics'][metricname] = metricdata.copy()
                    #c['monitoring']['metrics'][metricname]['query'] = c['monitoring']['metrics'][metricname]['query'].format(host=node, gpuid=gpuid, configuration=self.configuration.lower(), experiment=self.code)
                    c['monitoring']['metrics'][metricname]['query'] = self.set_metric_of_config_default(metric=c['monitoring']['metrics'][metricname]['query'], host=node, gpuid=gpuid, schema=schema, database=database)
                    # other components (not managed by bexhoma)
                    c['monitoring']['metrics_special'][metricname] = metricdata.copy()
                    c['monitoring']['metrics_special'][metricname]['query'] = self.set_metric_of_config(metric=c['monitoring']['metrics_special'][metricname]['query'], host=node, gpuid=gpuid, schema=schema, database=database)
            # application metrics
            if self.monitor_app_active and 'monitor' in self.dockertemplate and 'metrics' in self.dockertemplate['monitor']:
                for metricname, metricdata in self.dockertemplate['monitor']['metrics'].items():
                    # default components (managed by bexhoma)
                    c['monitoring']['metrics'][metricname] = metricdata.copy()
                    #c['monitoring']['metrics'][metricname]['query'] = c['monitoring']['metrics'][metricname]['query'].format(host=node, gpuid=gpuid, configuration=self.configuration.lower(), experiment=self.code)
                    c['monitoring']['metrics'][metricname]['query'] = self.set_metric_of_config_default(metric=c['monitoring']['metrics'][metricname]['query'], host=node, gpuid=gpuid, schema=schema, database=database)
                    # other components (not managed by bexhoma)
                    c['monitoring']['metrics_special'][metricname] = metricdata.copy()
                    c['monitoring']['metrics_special'][metricname]['query'] = self.set_metric_of_config(metric=c['monitoring']['metrics_special'][metricname]['query'], host=node, gpuid=gpuid, schema=schema, database=database)
        if 'JDBC' in c:
            database = c['JDBC']['database'] if 'database' in c['JDBC'] else self.experiment.volume
            schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else ''
            if self.tenant_per == 'schema':
                schema = 'DBMSBENCHMARKER_SCHEMA'
            elif self.tenant_per == 'database':
                database = 'DBMSBENCHMARKER_DATABASE'
            c['JDBC']['url'] = c['JDBC']['url'].format(
                serverip=serverip,
                dbname=self.experiment.volume,
                DBNAME=self.experiment.volume.upper(),
                timout_s=c['connectionmanagement']['timeout'],
                timeout_ms=c['connectionmanagement']['timeout']*1000,
                namespace=self.experiment.cluster.namespace,
                database=database,
                schema=schema,
                )
        #print(c)
        return c#.copy()
    def run_benchmarker_pod(self,
        connection=None,
        alias='',
        dialect='',
        query=None,
        app='',
        component='benchmarker',
        experiment='',
        configuration='',
        client='1',
        parallelism=1,
        only_prepare=False):
        """
        Runs the benchmarker job.
        Sets meta data in the connection.config.
        Copy query.config and connection.config to the first pod of the job (result folder mounted into every pod)

        :param connection: Name of configuration prolonged by number of runs of the sut (installations) and number of client in a sequence of
        :param alias: An alias can be given if we want to anonymize the dbms
        :param dialect: A name of a SQL dialect can be given
        :param query: The benchmark can be fixed to a specific query
        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: Number of benchmarker this is in a sequence of
        :param parallelism: Number of parallel benchmarker pods we want to have
        :param only_prepare: benchmarker pods will not be started. this makes a dry run
        """
        self.logger.debug('configuration.run_benchmarker_pod()')
        resultfolder = self.experiment.cluster.config['benchmarker']['resultfolder']
        experiments_configfolder = self.experiment.cluster.experiments_configfolder
        app = self.appname
        if connection is None:
            connection = self.configuration#self.getConnectionName()
        if len(configuration) == 0:
            configuration = connection
        code = self.code
        if not isinstance(client, str):
            client = str(client)
        if not self.client:
            self.client = client
        if len(dialect) == 0 and len(self.dialect) > 0:
            dialect = self.dialect
        # set more parameters
        experimentRun = str(self.num_experiment_to_apply_done+1)
        #self.experiment.cluster.stopPortforwarding()
        # set query management for new query file
        tools.query.template = self.experiment.querymanagement
        # store information about current benchmark
        self.current_benchmark_connection = connection
        self.logger.debug('configuration.run_benchmarker_pod(current_benchmark_connection = {})'.format(self.current_benchmark_connection))
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        time_now = str(datetime.now())
        time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
        self.current_benchmark_start = int(time_now_int)
        # get connection config (sut)
        monitoring_host = self.generate_component_name(component='monitoring', configuration=configuration, experiment=self.code)
        service_name = self.get_service_sut(configuration=configuration)#self.generate_component_name(component='sut', configuration=configuration, experiment=self.code)
        service_namespace = self.experiment.cluster.contextdata['namespace']
        service_host = self.experiment.cluster.contextdata['service_sut'].format(service=service_name, namespace=service_namespace)
        pods = self.experiment.cluster.get_pods(component='sut', configuration=configuration, experiment=self.code)
        self.pod_sut = pods[0]
        #service_port = config_K8s['port']
        c = self.get_connection_config(connection, alias, dialect, serverip=service_host, monitoring_host=monitoring_host)#config_K8s['ip'])
        #c['parameter'] = {}
        # add parameters to connection
        if len(self.loading_parameters) > 0:
            self.connection_parameter['loading_parameters'] = self.loading_parameters.copy()
        if len(self.benchmarking_parameters) > 0:
            self.connection_parameter['benchmarking_parameters'] = self.benchmarking_parameters.copy()
        if len(self.sut_parameters) > 0:
            self.connection_parameter['sut_parameters'] = self.sut_parameters.copy()
        if len(self.eval_parameters) > 0:
            self.connection_parameter['eval_parameters'] = self.eval_parameters.copy()
        if len(self.ddl_parameters) > 0:
            self.connection_parameter['ddl_parameters'] = self.ddl_parameters.copy()
        c['parameter'] = self.eval_parameters.copy()
        c['parameter']['parallelism'] = parallelism
        c['parameter']['client'] = client
        c['parameter']['numExperiment'] = experimentRun
        c['parameter']['num_worker'] = self.num_worker
        c['parameter']['dockerimage'] = self.dockerimage
        c['parameter']['connection_parameter'] = self.connection_parameter
        c['hostsystem']['loading_timespans'] = self.loading_timespans
        c['hostsystem']['benchmarking_timespans'] = self.benchmarking_timespans
        #print(c)
        self.check_volumes()
        # add config jarfolder
        #print(self.experiment.cluster.config['benchmarker']['jarfolder'])
        if 'JDBC' in c:
            if isinstance(c['JDBC']['jar'], list):
                for i, j in enumerate(c['JDBC']['jar']):
                    c['JDBC']['jar'][i] = self.experiment.cluster.config['benchmarker']['jarfolder']+c['JDBC']['jar'][i]
            elif isinstance(c['JDBC']['jar'], str):
                c['JDBC']['jar'] = self.experiment.cluster.config['benchmarker']['jarfolder']+c['JDBC']['jar']
        #print(c)
        self.logger.debug('configuration.run_benchmarker_pod(): {}'.format(connection))
        self.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            fixedQuery=query,
            result_path=resultfolder,
            batch=True,
            working='connection',
            code=code
            )
        #self.benchmark.code = '1611607321'
        self.code = self.benchmark.code
        #print("Code", self.code)
        print("{:30s}: benchmarking results in folder {}".format(configuration, self.benchmark.path))
        self.logger.debug('configuration.run_benchmarker_pod(Code={})'.format(self.code))
        # read config for benchmarker
        # empty template:
        #connectionfile = experiments_configfolder+'/connections.config'
        # collecting all configs of experiment in result folder
        connectionfile = self.benchmark.path+'/connections.config'
        if not os.path.isfile(connectionfile):
            # empty template:
            connectionfile = experiments_configfolder+'/connections.config'
        if self.experiment.queryfile is not None:
            queryfile = experiments_configfolder+'/'+self.experiment.queryfile
        else:
            queryfile = experiments_configfolder+'/queries.config'
        self.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        if c['name'] in self.benchmark.dbms:
            print("Rerun connection "+connection)
            # TODO: Find and replace connection info
        else:
            self.benchmark.connections.append(c)
        # NEVER rerun, only one connection in config for detached:
        #self.benchmark.connections = [c]
        #print(self.benchmark.connections)
        #self.logger.debug('configuration.run_benchmarker_pod(): {}'.format(self.benchmark.connections))
        self.benchmark.dbms[c['name']] = tools.dbms(c, False)
        # copy or generate config folder (query and connection)
        # add connection to existing list
        # or: generate new connection list
        filename = self.benchmark.path+'/connections.config'
        with open(filename, 'w') as f:
            f.write(str(self.benchmark.connections))
        #print(str(self.benchmark.connections))
        filename = self.benchmark.path+'/'+c['name']+'.config'
        with open(filename, 'w') as f:
            f.write(str([c]))
        # write appended query config
        if len(self.experiment.workload) > 0:
            for k,v in self.experiment.workload.items():
                self.benchmark.queryconfig[k] = v
            filename = self.benchmark.path+'/queries.config'
            with open(filename, 'w') as f:
                f.write(str(self.benchmark.queryconfig))
        # generate all parameters and store in protocol
        self.benchmark.reporterStore.readProtocol()
        self.benchmark.generateAllParameters()
        self.benchmark.reporterStore.writeProtocol()
        # store experiment
        experiment = {}
        experiment['delay'] = 0
        experiment['step'] = "runBenchmarks"
        experiment['connection'] = connection
        experiment['connectionmanagement'] = self.connectionmanagement.copy()
        self.experiment.cluster.log_experiment(experiment)
        # copy config to pod - dashboard
        pods = self.experiment.cluster.get_pods(component='dashboard')
        if len(pods) > 0:
            pod_dashboard = pods[0]
            cmd = {}
            cmd['prepare_log'] = 'mkdir -p /results/'+str(self.code)
            stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['prepare_log'], pod=pod_dashboard, container="dashboard")
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/queries.config '+pod_dashboard+':/results/'+str(self.code)+'/queries.config')
            self.logger.debug('copy config queries.config: {}'.format(stdout))
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/'+c['name']+'.config '+pod_dashboard+':/results/'+str(self.code)+'/'+c['name']+'.config')
            self.logger.debug('copy config {}: {}'.format(c['name']+'.config', stdout))
            # copy twice to be more sure it worked
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/'+c['name']+'.config '+pod_dashboard+':/results/'+str(self.code)+'/'+c['name']+'.config')
            self.logger.debug('copy config {}: {}'.format(c['name']+'.config', stdout))
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/connections.config '+pod_dashboard+':/results/'+str(self.code)+'/connections.config')
            self.logger.debug('copy config connections.config: {}'.format(stdout))
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/protocol.json '+pod_dashboard+':/results/'+str(self.code)+'/protocol.json')
            self.logger.debug('copy config protocol.json: {}'.format(stdout))
        # put list of clients to message queue
        redisQueue = '{}-{}-{}-{}'.format(app, component, connection, self.code)
        for i in range(1, parallelism+1):
            #redisClient.rpush(redisQueue, i)
            self.experiment.cluster.add_to_messagequeue(queue=redisQueue, data=i)
        if not only_prepare:
            # create pods
            yamlfile = self.create_manifest_benchmarking(connection=connection, component=component, configuration=configuration, experiment=self.code, experimentRun=experimentRun, client=client, parallelism=parallelism, alias=c['alias'], num_pods=parallelism)
            # start pod
            self.experiment.cluster.kubectl('create -f '+yamlfile)
            pods = []
            while len(pods) == 0:
                self.wait(10)
                pods = self.experiment.cluster.get_job_pods(component=component, configuration=configuration, experiment=self.code, client=client)
            client_pod_name = pods[0]
            status = self.experiment.cluster.get_pod_status(client_pod_name)
            self.logger.debug('Pod={} has status={}'.format(client_pod_name, status))
            print("{:30s}: benchmarking is waiting for job {}: ".format(configuration, client_pod_name), end="", flush=True)
            while status != "Running" and status != "Succeeded":
                self.logger.debug('Pod={} has status={}'.format(client_pod_name, status))
                print(".", end="", flush=True)
                #self.wait(10)
                # maybe pod had to be restarted
                pods = []
                while len(pods) == 0:
                    self.wait(10, silent=True)
                    pods = self.experiment.cluster.get_job_pods(component=component, configuration=configuration, experiment=self.code, client=client)
                client_pod_name = pods[0]
                status = self.experiment.cluster.get_pod_status(client_pod_name)
            print("found")
        # get monitoring for loading
        """
        if self.monitoring_active:
            print("get monitoring for loading")
            logger = logging.getLogger('dbmsbenchmarker')
            logging.basicConfig(level=logging.DEBUG)
            for connection_number, connection_data in self.benchmark.dbms.items():
                #connection = self.benchmark.dbms[c['name']]
                print(connection_number, connection_data)
                print(connection_data.connectiondata['monitoring']['prometheus_url'])
                query='loading'
                for m, metric in connection_data.connectiondata['monitoring']['metrics'].items():
                    print(m)
                    monitor.metrics.fetchMetric(query, m, connection_number, connection_data.connectiondata, int(self.timeLoadingStart), int(self.timeLoadingEnd), '{result_path}'.format(result_path=self.benchmark.path))
        """
        # copy config to pod - dashboard
        pods = self.experiment.cluster.get_pods(component='dashboard')
        if len(pods) > 0:
            pod_dashboard = pods[0]
            cmd = {}
            """
            cmd['prepare_log'] = 'mkdir -p /results/'+str(self.code)
            stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['prepare_log'], pod=pod_dashboard, container="dashboard")
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/queries.config '+pod_dashboard+':/results/'+str(self.code)+'/queries.config')
            self.logger.debug('copy config queries.config: {}'.format(stdout))
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/'+c['name']+'.config '+pod_dashboard+':/results/'+str(self.code)+'/'+c['name']+'.config')
            self.logger.debug('copy config {}: {}'.format(c['name']+'.config', stdout))
            # copy twice to be more sure it worked
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/'+c['name']+'.config '+pod_dashboard+':/results/'+str(self.code)+'/'+c['name']+'.config')
            self.logger.debug('copy config {}: {}'.format(c['name']+'.config', stdout))
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/connections.config '+pod_dashboard+':/results/'+str(self.code)+'/connections.config')
            self.logger.debug('copy config connections.config: {}'.format(stdout))
            stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/protocol.json '+pod_dashboard+':/results/'+str(self.code)+'/protocol.json')
            self.logger.debug('copy config protocol.json: {}'.format(stdout))
            """
            # get monitoring for loading
            if self.monitoring_active and self.monitor_loading:
                cmd = {}
                #self.monitoring_sut = True
                if self.monitoring_sut:
                    print("{:30s}: collecting loading metrics of SUT at connection {}".format(connection, self.current_benchmark_connection))
                    #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                    # with container name? should better be part of the metric query
                    #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -cn {} -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(
                    #metric_example = self.benchmark.dbms[self.configuration].connectiondata['monitoring']['metrics_special']['total_cpu_memory']
                    #metric_example = c['name']['monitoring']['metrics_special']['total_cpu_memory']
                    #print("{:30s}: example mtric {}".format(connection, metric_example))
                    metric_example = self.benchmark.dbms[self.current_benchmark_connection].connectiondata['monitoring']['metrics_special']['total_cpu_memory']
                    print("{:30s}: example metric {}".format(connection, metric_example))
                    cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -db -ct loading -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(
                        #self.sut_container_name,
                        connection, 
                        c['name']+'.config', 
                        '/results/'+self.code, 
                        self.code, 
                        self.timeLoadingStart, 
                        self.timeLoadingEnd)
                    stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['fetch_loading_metrics'], pod=pod_dashboard, container="dashboard")
                    self.logger.debug(stdout)
                    self.logger.debug(stderr)
                    # upload connections infos again, metrics has overwritten it
                    filename = 'connections.config'
                    cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                    stdout = self.experiment.cluster.kubectl(cmd['upload_connection_file'])
                    self.logger.debug(stdout)
                # get metrics of loader components
                # only if general monitoring is on
                endpoints_cluster = self.experiment.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
                if len(endpoints_cluster)>0 or self.experiment.cluster.monitor_cluster_exists:
                    # data generator container
                    print("{:30s}: collecting metrics of data generator at connection {}".format(connection, self.current_benchmark_connection))
                    metric_example = self.benchmark.dbms[self.current_benchmark_connection].connectiondata['monitoring']['metrics']['total_cpu_memory'].copy()
                    container = "datagenerator"
                    if container is not None:
                        metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name="dbms"', 'container_label_io_kubernetes_container_name="{}"'.format(container))
                        metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name!="dbms"', 'container_label_io_kubernetes_container_name!="{}"'.format(container))
                        metric_example['query'] = metric_example['query'].replace('container="dbms"', 'container="{}"'.format(container))
                        metric_example['query'] = metric_example['query'].replace('container!="dbms"', 'container!="{}"'.format(container))
                    print("{:30s}: example metric {}".format(connection, metric_example))
                    cmd['fetch_loader_metrics'] = 'python metrics.py -r /results/ -db -ct datagenerator -cn datagenerator -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(
                        connection, 
                        c['name']+'.config', 
                        '/results/'+self.code, 
                        self.code, 
                        self.timeLoadingStart, 
                        self.timeLoadingEnd)
                    stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['fetch_loader_metrics'], pod=pod_dashboard, container="dashboard")
                    self.logger.debug(stdout)
                    self.logger.debug(stderr)
                    # upload connections infos again, metrics has overwritten it
                    filename = 'connections.config'
                    cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                    stdout = self.experiment.cluster.kubectl(cmd['upload_connection_file'])
                    self.logger.debug(stdout)
                    # data injector container "sensor"
                    print("{:30s}: collecting metrics of data injector at connection {}".format(connection, self.current_benchmark_connection))
                    metric_example = self.benchmark.dbms[self.current_benchmark_connection].connectiondata['monitoring']['metrics']['total_cpu_memory'].copy()
                    container = "sensor"
                    if container is not None:
                        metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name="dbms"', 'container_label_io_kubernetes_container_name="{}"'.format(container))
                        metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name!="dbms"', 'container_label_io_kubernetes_container_name!="{}"'.format(container))
                        metric_example['query'] = metric_example['query'].replace('container="dbms"', 'container="{}"'.format(container))
                        metric_example['query'] = metric_example['query'].replace('container!="dbms"', 'container!="{}"'.format(container))
                    print("{:30s}: example metric {}".format(connection, metric_example))
                    cmd['fetch_loader_metrics'] = 'python metrics.py -r /results/ -db -ct loader -cn sensor -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(
                        connection, 
                        c['name']+'.config', 
                        '/results/'+self.code, 
                        self.code, 
                        self.timeLoadingStart, 
                        self.timeLoadingEnd)
                    stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['fetch_loader_metrics'], pod=pod_dashboard, container="dashboard")
                    self.logger.debug(stdout)
                    self.logger.debug(stderr)
                    # upload connections infos again, metrics has overwritten it
                    filename = 'connections.config'
                    cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                    stdout = self.experiment.cluster.kubectl(cmd['upload_connection_file'])
                    self.logger.debug(stdout)
                    # pooling container "pool"
                    if self.sut_has_pool:
                        print("{:30s}: collecting loading metrics of pool at connection {}".format(connection, self.current_benchmark_connection))
                        metric_example = self.benchmark.dbms[self.current_benchmark_connection].connectiondata['monitoring']['metrics']['total_cpu_memory'].copy()
                        container = "pool"
                        if container is not None:
                            metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name="dbms"', 'container_label_io_kubernetes_container_name="{}"'.format(container))
                            metric_example['query'] = metric_example['query'].replace('container_label_io_kubernetes_container_name!="dbms"', 'container_label_io_kubernetes_container_name!="{}"'.format(container))
                            metric_example['query'] = metric_example['query'].replace('container="dbms"', 'container="{}"'.format(container))
                            metric_example['query'] = metric_example['query'].replace('container!="dbms"', 'container!="{}"'.format(container))
                        print("{:30s}: example metric {}".format(connection, metric_example))
                        cmd['fetch_loader_metrics'] = 'python metrics.py -r /results/ -db -ct poolloading -cn pool -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(
                            connection, 
                            c['name']+'.config', 
                            '/results/'+self.code, 
                            self.code, 
                            self.timeLoadingStart, 
                            self.timeLoadingEnd)
                        stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['fetch_loader_metrics'], pod=pod_dashboard, container="dashboard")
                        self.logger.debug(stdout)
                        self.logger.debug(stderr)
                        # upload connections infos again, metrics has overwritten it
                        filename = 'connections.config'
                        cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                        stdout = self.experiment.cluster.kubectl(cmd['upload_connection_file'])
                        self.logger.debug(stdout)
    def execute_command_in_pod_sut(self, command, pod='', container='', params=''):
        """
        Runs an shell command remotely inside a container of a pod.
        This defaults to the current sut's pod and the container "dbms"

        :param command: A shell command
        :param pod: The name of the pod - default current sut's pod
        :param container: The name of the container in the pod - default dbms
        :param params: Optional parameters, currently ignored
        :return: stdout of the shell command
        """
        if len(pod) == 0:
            pod=self.pod_sut
            #pod = self.activepod
        if len(container) == 0:
            container = self.sut_container_name
            #if self.sut_container_name is not None:
            #    container = self.sut_container_name
            #else:
            #    container = ''
            #    #container = 'dbms'
        if self.pod_sut == '':
            self.check_sut()
        return self.experiment.cluster.execute_command_in_pod(command=command, pod=pod, container=container, params=params)
    def copyLog(self):
        print("copyLog")
        pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
        self.pod_sut = pods[0]
        if len(self.dockertemplate['logfile']):
            cmd = {}
            cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=cmd['prepare_log'])
            cmd['save_log'] = 'cp '+self.dockertemplate['logfile']+' /data/'+str(self.code)+'/'+self.configuration+'.log'
            stdin, stdout, stderr = self.execute_command_in_pod_sut(command=cmd['save_log'])
    def prepare_init_dbms(self, scripts):
        """
        Prepares to load data into the dbms.
        This copies the DDL scripts to /tmp on the host of the sut.
        Optionally parameters in DDL script are replaced by ddl_parameters.
        The files are renamed `filled_` then.
        """
        self.logger.debug('configuration.prepare_init_dbms()')
        pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
        self.pod_sut = pods[0]
        scriptfolder = '/tmp/'
        if self.num_tenants > 0 and self.tenant_per == 'schema':
            for tenant in range(self.num_tenants):
                print("{:30s}: scripts for tenant #{}".format(self.configuration, tenant))
                #print(f"Tenant #{tenant}")
                for script in scripts:
                    filename_template = self.path_experiment_docker+'/'+script
                    if os.path.isfile(self.experiment.cluster.experiments_configfolder+'/'+filename_template):
                        with open(self.experiment.cluster.experiments_configfolder+'/'+filename_template, "r") as initscript_template:
                            data = initscript_template.read()
                            #data = data.format(**self.ddl_parameters)
                            #print(data)
                            data = data.format(BEXHOMA_SCHEMA=f"tenant_{tenant}")
                            #print(data)
                            filename_filled = self.path_experiment_docker+f'/filled_{tenant}_{script}'
                            filename_target = f'/filled_{tenant}_{script}'
                            with open(self.experiment.cluster.experiments_configfolder+'/'+filename_filled, "w") as initscript_filled:
                                initscript_filled.write(data)
                            self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename_filled, to_name=self.pod_sut+':'+scriptfolder+filename_target))
            return
        if self.num_tenants > 0 and self.tenant_per == 'database':
            script = 'initdatabases.sql'
            filename_template = self.experiment.cluster.experiments_configfolder+'/'+self.path_experiment_docker+'/'+script
            script_create_database = ''
            for tenant in range(self.num_tenants):
                script_create_database += f'CREATE DATABASE tenant_{tenant};\n'
            with open(filename_template, "w") as initscript_filled:
                initscript_filled.write(script_create_database)
            self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=filename_template, to_name=self.pod_sut+':'+scriptfolder+script))
        if len(self.ddl_parameters):
            #for script in self.initscript:
            for script in scripts:
                filename_template = self.path_experiment_docker+'/'+script
                if os.path.isfile(self.experiment.cluster.experiments_configfolder+'/'+filename_template):
                    with open(self.experiment.cluster.experiments_configfolder+'/'+filename_template, "r") as initscript_template:
                        data = initscript_template.read()
                        data = data.format(**self.ddl_parameters)
                        filename_filled = self.path_experiment_docker+'/filled_'+script
                        with open(self.experiment.cluster.experiments_configfolder+'/'+filename_filled, "w") as initscript_filled:
                            initscript_filled.write(data)
                        self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename_filled, to_name=self.pod_sut+':'+scriptfolder+script))
        else:
            #for script in self.initscript:
            for script in scripts:
                filename = self.path_experiment_docker+'/'+script
                if os.path.isfile(self.experiment.cluster.experiments_configfolder+'/'+filename):
                    self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename, to_name=self.pod_sut+':'+scriptfolder+script))
                    stdin, stdout, stderr = self.execute_command_in_pod_sut("sed -i $'s/\\r//' {to_name}".format(to_name=scriptfolder+script))
                    #self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename, to_name=self.pod_sut+':'+scriptfolder+script))
    def attach_worker(self):
        """
        Attaches worker nodes to the master of the sut.
        This runs the dockertemplate['attachWorker'] command.
        """
        self.logger.debug('Try to attach worker to master')
        if self.num_worker > 0 and 'attachWorker' in self.dockertemplate and len(self.dockertemplate['attachWorker']) > 0:
            print("{:30s}: try to attach workers to master".format(self.configuration))
            pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
            name_worker = self.get_worker_name() #self.generate_component_name(component='worker', experiment=self.experiment_name, configuration=self.configuration) #experiment=self.code, configuration=self.configuration)
            if len(pods) > 0:
                print("{:30s}: master found".format(self.configuration))
                pod_sut = pods[0]
                num_worker = 0
                print("{:30s}: looking for worker pods".format(self.configuration))
                while num_worker < self.num_worker:
                    self.wait(5)
                    num_worker = 0
                    pods_worker = self.get_worker_pods()#self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
                    for pod in pods_worker:
                        #stdin, stdout, stderr = self.execute_command_in_pod_sut(self.dockertemplate['attachWorker'].format(worker=pod, service_sut=name_worker), pod_sut)
                        status = self.experiment.cluster.get_pod_status(pod)
                        if status == "Running":
                            num_worker = num_worker+1
                            print("{:30s}: found running worker {}".format(self.configuration, num_worker))
                    print("{:30s}: found {} running workers of {}".format(self.configuration, num_worker, self.num_worker))
                    #print(self.configuration, "Workers", num_worker, "of", self.num_worker)
                print("{:30s}: list of workers".format(self.configuration))
                pods_worker = self.get_worker_pods()#self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
                for pod in pods_worker:
                    print("{:30s}: worker {}.{} attached".format(self.configuration, pod, name_worker))
                    self.logger.debug('Worker attached: {worker}.{service_sut}'.format(worker=pod, service_sut=name_worker))
                    stdin, stdout, stderr = self.execute_command_in_pod_sut(self.dockertemplate['attachWorker'].format(worker=pod, service_sut=name_worker), pod_sut)
                    print(stdin, stdout, stderr)
                    resultfolder = self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
                    #name_worker_attach = self.generate_component_name(app=self.appname, component='worker', experiment='attach', configuration=self.configuration)
                    filename_log = "{path}/{code}/{pod}.attach.{number}.log".format(path=resultfolder, code=self.code, pod=pod, number=self.num_experiment_to_apply_done+1)
                    f = open(filename_log, "w")
                    f.write(stdout)
                    f.close()
    def check_sut(self):
        """
        Check if the pod of the sut is running.
        If yes, store it's name in `self.pod_sut`.
        """
        pods = self.experiment.cluster.get_pods(app=self.appname, component='sut', configuration=self.configuration, experiment=self.code)
        if len(pods) > 0:
            self.pod_sut = pods[0]
            return True
        else:
            return False
    def check_load_data(self):
        """
        Check if loading of the sut has finished.
        If yes, store timeLoadingStart, timeLoadingEnd, timeLoading as labels and in this object as attributes.
        If there is a loading job: check if all pods are completed. Copy the logs of the containers in the pods and remove the pods. 
        If there is no loading job: Read the labels. If loaded is True, store the timings in this object as attributes.
        """
        if self.loading_deactivated:
            self.loading_started = True
            self.loading_finished = True
            self.loading_active = False
            self.monitor_loading = False
            return
        loading_pods_active = True
        # check if asynch loading inside cluster is done
        if self.loading_active:
            # success of job
            app = self.experiment.cluster.appname
            component = 'loading'
            experiment = self.code
            configuration = self.configuration
            success = self.experiment.cluster.get_job_status(app=app, component=component, experiment=experiment, configuration=configuration)
            jobs = self.experiment.cluster.get_jobs(app, component, self.code, configuration)
            # status per job
            for job in jobs:
                self.experiment.cluster.logger.debug("Found running job {}".format(job))
                success = self.experiment.cluster.get_job_status(job)
                self.experiment.cluster.logger.debug('job {} has success status {}'.format(job, success))
                #print(job, success)
                # store logs of successful pods
                pods = self.experiment.cluster.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                for pod in pods:
                    status = self.experiment.cluster.get_pod_status(pod)
                    self.experiment.cluster.logger.debug("Pod {} has status {}".format(pod, status))
                    if status == "Succeeded":
                        containers = self.experiment.cluster.get_pod_containers(pod)
                        for container in containers:
                            if len(container) > 0:
                                if not self.experiment.cluster.pod_log_exists(pod_name=pod, container=container):
                                    self.experiment.cluster.logger.debug("Store logs of job {} pod {} container {}".format(job, pod, container))
                                    self.experiment.cluster.store_pod_log(pod_name=pod, container=container)
                        if not self.experiment.cluster.pod_description_exists(pod_name=pod):
                            self.experiment.cluster.logger.debug("Store description of job {} pod {}".format(job, pod))
                            self.experiment.cluster.store_pod_description(pod_name=pod)
                        #container = 'datagenerator'
                        #if container in containers:
                        #    if not self.experiment.cluster.pod_log_exists(pod_name=pod, container=container):
                        #        self.experiment.cluster.logger.debug("Store logs of job {} pod {}".format(job, pod))
                        #        self.experiment.cluster.store_pod_log(pod_name=pod, container=container)
                        #container = 'sensor'
                        #if container in containers:
                        #    if not self.experiment.cluster.pod_log_exists(pod_name=pod, container=container):
                        #        self.experiment.cluster.store_pod_log(pod_name=pod, container=container)
                if success:
                    self.experiment.cluster.logger.debug('job {} will be suspended and parallel loading will be considered finished'.format(job, success))
                    # get labels (start) of sut
                    pod_labels = self.experiment.cluster.get_pods_labels(app=app, component='sut', experiment=experiment, configuration=configuration)
                    #print(pod_labels)
                    if len(pod_labels) > 0:
                        pod = next(iter(pod_labels.keys()))
                        if 'timeLoadingStart' in pod_labels[pod]:
                            self.timeLoadingStart = int(pod_labels[pod]['timeLoadingStart'])
                        if 'timeLoadingEnd' in pod_labels[pod]:
                            self.timeLoadingEnd = int(pod_labels[pod]['timeLoadingEnd'])
                        if 'timeLoading' in pod_labels[pod]:
                            self.timeLoading = float(pod_labels[pod]['timeLoading'])
                        if 'timeIndex' in pod_labels[pod]:
                            self.timeIndex = float(pod_labels[pod]['timeIndex'])
                        for key, value in pod_labels[pod].items():
                            if key.startswith("time_"):
                                time_type = key[len("time_"):]
                                self.times_scripts[time_type] = float(value)
                    # delete job and all its pods
                    #pods = self.experiment.cluster.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                    for pod in pods:
                        status = self.experiment.cluster.get_pod_status(pod)
                        self.experiment.cluster.logger.debug("Pod {} has status {}".format(pod, status))
                        self.experiment.cluster.logger.debug("Store logs of job {} pod {}".format(job, pod))
                        #if status == "Running":
                        # TODO: Find names of containers dynamically
                        containers = self.experiment.cluster.get_pod_containers(pod)
                        for container in containers:
                            if len(container) > 0:
                                self.experiment.cluster.store_pod_log(pod_name=pod, container=container)
                        if not self.experiment.cluster.pod_description_exists(pod_name=pod):
                            self.experiment.cluster.logger.debug("Store description of job {} pod {}".format(job, pod))
                            self.experiment.cluster.store_pod_description(pod_name=pod)
                        self.experiment.cluster.delete_pod(pod)
                        #container = 'datagenerator'
                        #if container in containers:
                        #    self.experiment.cluster.store_pod_log(pod_name=pod, container=container)
                        #container = 'sensor'
                        #if container in containers:
                        #    self.experiment.cluster.store_pod_log(pod_name=pod, container=container)
                        #    self.experiment.cluster.delete_pod(pod)
                    self.experiment.end_loading(job)
                    self.experiment.cluster.delete_job(job)
                    loading_pods_active = False
                    if self.monitoring_active:
                        #cmd = {}
                        #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -c {} -ts {} -te {}'.format(self.code, self.timeLoadingStart, self.timeLoadingEnd)
                        #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -c {} -e {} -ts {} -te {}'.format(connection, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                        #self.experiment.cluster.logger.debug('load_metrics:{}'.format(cmd['fetch_loading_metrics']))
                        #stdout = os.popen(cmd['fetch_loading_metrics']).read()# os.system(fullcommand)
                        #stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['fetch_loading_metrics'], pod=client_pod_name)
                        #print(stdout)
                        # currently, only benchmarking fetches loading metrics
                        #self.fetch_metrics_loading(connection=self.configuration)
                        pass
                    # mark pod with new end time and duration
                    pods_sut = self.experiment.cluster.get_pods(app=app, component='sut', experiment=experiment, configuration=configuration)
                    if len(pods_sut) > 0:
                        pod_sut = pods_sut[0]
                        #self.timeLoadingEnd = default_timer()
                        #self.timeLoading = float(self.timeLoadingEnd) - float(self.timeLoadingStart)
                        #self.experiment.cluster.logger.debug("LOADING LABELS")
                        #self.experiment.cluster.logger.debug(self.timeLoading)
                        #self.experiment.cluster.logger.debug(float(self.timeLoadingEnd))
                        #self.experiment.cluster.logger.debug(float(self.timeLoadingStart))
                        #self.timeLoading = float(self.timeLoading) + float(timeLoading)
                        print("{:30s}: showing loader times".format(self.configuration))
                        timing_datagenerator, timing_sensor, timing_total = self.experiment.get_job_timing_loading(job)
                        generator_time = 0
                        loader_time = 0
                        total_time = 0
                        self.loading_timespans = {}
                        self.loading_timespans['datagenerator'] = timing_datagenerator
                        self.loading_timespans['sensor'] = timing_sensor
                        self.loading_timespans['total'] = timing_total
                        if len(timing_datagenerator) > 0:
                            self.experiment.cluster.logger.debug("Generator times (duration per pod [s]): {}".format([end-start for (start,end) in timing_datagenerator]))
                            timing_start = min([start for (start,end) in timing_datagenerator])
                            timing_end = max([end for (start,end) in timing_datagenerator])
                            total_time = timing_end - timing_start
                            generator_time = total_time
                            print("{:30s}: generator timespan (first to last [s]) = {}".format(self.configuration, total_time))
                        #timing_sensor = extract_timing(jobname, container="sensor")
                        if len(timing_sensor) > 0:
                            self.experiment.cluster.logger.debug("Loader times (duration per pod [s]): {}".format([end-start for (start,end) in timing_sensor]))
                            timing_start = min([start for (start,end) in timing_sensor])
                            timing_end = max([end for (start,end) in timing_sensor])
                            total_time = timing_end - timing_start
                            loader_time = total_time
                            print("{:30s}: loader timespan (first to last [s]) = {}".format(self.configuration, total_time))
                        if len(timing_datagenerator) > 0 and len(timing_sensor) > 0:
                            timing_total = timing_datagenerator + timing_sensor
                            self.experiment.cluster.logger.debug("Total times (start/end per pod and container): {}".format(timing_total))
                            timing_start = min([start for (start,end) in timing_total])
                            timing_end = max([end for (start,end) in timing_total])
                            total_time = timing_end - timing_start
                            print("{:30s}: total timespan (first to last [s]) = {}".format(self.configuration, total_time))
                        now = datetime.utcnow()
                        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
                        time_now = str(datetime.now())
                        time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
                        self.timeLoadingEnd = int(time_now_int)
                        # store preloading time (should be for schema creation)
                        self.timeSchema = self.timeLoading
                        if total_time > 0:
                            # this sets the loading time to the max span of pods
                            self.timeLoading = ceil(total_time + self.timeLoading)
                        else:
                            # this sets the loading time to the span until "now" (including waiting and starting overhead)
                            self.timeLoading = ceil(int(self.timeLoadingEnd) - int(self.timeLoadingStart) + self.timeLoading)
                        self.timeGenerating = generator_time
                        self.timeIngesting = loader_time
                        self.experiment.cluster.logger.debug("LOADING LABELS")
                        self.experiment.cluster.logger.debug(self.timeLoadingStart)
                        self.experiment.cluster.logger.debug(self.timeLoadingEnd)
                        self.experiment.cluster.logger.debug(self.timeLoading)
                        fullcommand = 'label pods '+pod_sut+' --overwrite loaded=True timeLoadingEnd="{}" timeLoadingStart="{}" time_ingested={} timeLoading={} time_generated={}'.format(self.timeLoadingEnd, self.timeLoadingStart, loader_time, self.timeLoading, generator_time)
                        #print(fullcommand)
                        self.experiment.cluster.kubectl(fullcommand)
                        use_storage = self.use_storage()
                        if use_storage:
                            if self.storage['storageConfiguration']:
                                name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=self.storage['storageConfiguration'])
                            else:
                                name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=self.configuration)
                            volume = name_pvc
                        else:
                            volume = ''
                        if volume:
                            fullcommand = 'label pvc '+volume+' --overwrite loaded=True timeLoadingEnd="{}" timeLoadingStart="{}" time_ingested={} timeLoading={} time_generated={}'.format(self.timeLoadingEnd, self.timeLoadingStart, loader_time, self.timeLoading, generator_time)
                            #fullcommand = 'label pvc '+volume+' --overwrite loaded=True time_ingested={} timeLoadingStart="{}" timeLoadingEnd="{}" timeLoading={}'.format(loader_time, int(self.timeLoadingStart), int(self.timeLoadingEnd), self.timeLoading)
                            #print(fullcommand)
                            self.experiment.cluster.kubectl(fullcommand)
                    # get metrics of loader components
                    #endpoints_cluster = self.experiment.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
                    # get monitoring for loading
                    """
                    if self.monitoring_active and len(endpoints_cluster)>0:
                        # copy config to pod - dashboard
                        pods = self.experiment.cluster.get_pods(component='dashboard')
                        if len(pods) > 0:
                            pod_dashboard = pods[0]
                            cmd = {}
                            connection = self.configuration#self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
                            #cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(connection, c['name']+'.config', '/results/'+self.code, self.code, self.timeLoadingStart, self.timeLoadingEnd)
                            cmd['fetch_loader_metrics'] = 'python metrics.py -r /results/ -db -ct loader -cn sensor -c {} -cf {} -f {} -e {} -ts {} -te {}'.format(
                                connection,
                                'connections.config',
                                '/results/'+self.code,
                                self.code,
                                timing_start,
                                timing_end)
                            stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(
                                command=cmd['fetch_loader_metrics'], 
                                pod=pod_dashboard, 
                                container="dashboard")
                            self.logger.debug(stdout)
                            self.logger.debug(stderr)
                            # upload connections infos again, metrics has overwritten it
                            filename = 'connections.config'
                            cmd['upload_connection_file'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/'+filename, from_file=self.path+"/"+filename)
                            stdout = self.experiment.cluster.kubectl(cmd['upload_connection_file'])
                            self.logger.debug(stdout)
                    """
                    # check if there is a post-loading phase
                    if len(self.indexscript):
                        # loading has not finished (there is indexing)
                        if self.tenant_per == 'container' and not self.loading_finished:
                            self.tenant_ready_to_index = True
                        else:
                            self.load_data(scripts=self.indexscript, time_offset=self.timeLoading, time_start_int=self.timeLoadingStart, script_type='indexed')
        else:
            loading_pods_active = False
        # check if asynch loading outside cluster is done
        # only if inside cluster is done
        pod_labels = self.experiment.cluster.get_pods_labels(app=self.appname, component='sut', experiment=self.experiment.code, configuration=self.configuration)
        #print(pod_labels)
        if len(pod_labels) > 0:
            pod = next(iter(pod_labels.keys()))
            if len(self.indexscript):
                # we have to check indexing, too
                if 'indexed' in pod_labels[pod]:
                    self.loading_started = True
                    if pod_labels[pod]['indexed'] == 'True':
                        self.loading_finished = True
                    else:
                        self.loading_finished = False
                else:
                    self.loading_finished = False
                if 'time_indexed' in pod_labels[pod]:
                    self.timeIndex = float(pod_labels[pod]['time_indexed'])
            else:
                if not loading_pods_active:
                    if 'loaded' in pod_labels[pod]:
                        self.loading_started = True
                        if pod_labels[pod]['loaded'] == 'True':
                            self.loading_finished = True
                        else:
                            self.loading_finished = False
                    else:
                        self.loading_started = False
            if 'timeLoadingStart' in pod_labels[pod]:
                self.timeLoadingStart = int(pod_labels[pod]['timeLoadingStart'])
            if 'timeLoadingEnd' in pod_labels[pod]:
                self.timeLoadingEnd = int(pod_labels[pod]['timeLoadingEnd'])
            if 'timeLoading' in pod_labels[pod]:
                self.timeLoading = float(pod_labels[pod]['timeLoading'])
            if 'time_loaded' in pod_labels[pod]:
                self.timeSchema = float(pod_labels[pod]['time_loaded']) # stays at pre-ingestion total, even after ingestion and post-ingestion?
            if 'time_generated' in pod_labels[pod]:
                self.timeGenerating = float(pod_labels[pod]['time_generated'])
            if 'time_ingested' in pod_labels[pod]:
                self.timeIngesting = float(pod_labels[pod]['time_ingested'])
            for key, value in pod_labels[pod].items():
                if key.startswith("time_"):
                    time_type = key[len("time_"):]
                    self.times_scripts[time_type] = float(value)
            # timeLoadingEnd="{}" timeLoadingStart="{}" time_ingested={} timeLoading={} time_generated={}'.format(self.timeLoadingEnd, self.timeLoadingStart, loader_time, self.timeLoading, generator_time)
            #self.timeLoading = int(self.timeLoadingEnd) - int(self.timeLoadingStart) + self.timeLoading
        else:
            # if there are no labels at this pod, loading has not been started or finished
            # maybe sut has been restarted? then loading may have been stared though
            # TODO: check if sensible 
            #self.loading_started = False
            #self.loading_finished = False
            pass
    def load_data(self, scripts, time_offset=0, time_start_int=0, script_type='loaded'):
        """
        Start loading data into the sut.
        This runs `load_data_asynch()` as an asynchronous thread.
        At first `prepare_init_dbms()` is run.
        """
        self.logger.debug('configuration.load_data()')
        self.loading_started = True
        self.prepare_init_dbms(scripts)
        service_name = self.get_service_sut(configuration=self.configuration)#self.generate_component_name(component='sut', configuration=self.configuration, experiment=self.code)
        pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
        self.pod_sut = pods[0]
        scriptfolder = '/tmp/'
        commands = scripts.copy()
        c = self.dockertemplate['template']
        database = c['JDBC']['database'] if 'database' in c['JDBC'] else self.experiment.volume
        schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else 'default'
        databases = [database]
        use_storage = self.use_storage()
        if use_storage:
            #storage_label = 'tpc-ds-1'
            if self.storage['storageConfiguration']:
                storageConfiguration = self.storage['storageConfiguration']
            else:
                storageConfiguration = self.configuration
            name_pvc = self.generate_component_name(app=self.appname, component='storage', experiment=self.storage_label, configuration=storageConfiguration)
            volume = name_pvc
        else:
            volume = ''
        #commands = self.initscript.copy()
        print("{:30s}: start asynch loading scripts of type {}".format(self.configuration, script_type))
        if not 'loadData' in self.dockertemplate:
            print("{:30s}: no load command found in config".format(self.configuration))
            return
        else:
            #self.logger.debug("load_data_asynch(app="+self.appname+", component='sut', experiment="+self.code+", configuration="+self.configuration+", pod_sut="+self.pod_sut+", scriptfolder="+scriptfolder+", commands="+str(commands)+", loadData="+self.dockertemplate['loadData']+", path="+self.experiment.path+", volume="+volume+", context="+self.experiment.cluster.context+", service_name="+service_name+", time_offset="+str(time_offset)+", time_start_int="+str(time_start_int)+", script_type="+str(script_type)+", namespace="+self.experiment.cluster.namespace+")")
            #result = load_data_asynch(app=self.appname, component='sut', experiment=self.code, configuration=self.configuration, pod_sut=self.pod_sut, scriptfolder=scriptfolder, commands=commands, loadData=self.dockertemplate['loadData'], path=self.experiment.path)
            if self.num_tenants > 0:
                if self.tenant_per == 'schema':
                    #commands_tenants = []
                    #for tenant in range(self.num_tenants):
                    #    for c in commands:
                    #        filename_filled = f'filled_{tenant}_{c}'
                    #        commands_tenants.append(filename_filled)
                    #commands = commands_tenants.copy()
                    for tenant in range(self.num_tenants):
                        commands_tenants = []
                        for c in commands:
                            filename_filled = f'filled_{tenant}_{c}'
                            commands_tenants.append(filename_filled)
                        thread_args = {
                            'app':self.appname,
                            'component':'sut',
                            'experiment':self.code,
                            'configuration':self.configuration,
                            'pod_sut':self.pod_sut,
                            'scriptfolder':scriptfolder,
                            'commands':commands_tenants,
                            'loadData':self.dockertemplate['loadData'],
                            'path':self.experiment.path,
                            'volume':volume,
                            'context':self.experiment.cluster.context,
                            'service_name':service_name,
                            'time_offset':time_offset,
                            'script_type':script_type,
                            'time_start_int':time_start_int,
                            'namespace':self.experiment.cluster.namespace,
                            'num_tenants':self.num_tenants,
                            'id_tenant':tenant,
                            'database':databases,
                        }
                        self.logger.debug("load_data_asynch - run schema-wise scripts {}".format(thread_args))
                        thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                        thread.start()
                        time.sleep(1)
                elif self.tenant_per == 'database':
                    #commands.insert(0, "initdatabases.sql")
                    ##databases = database.copy()
                    #for tenant in range(self.num_tenants):
                    #    databases.append(f'tenant_{tenant}')
                    ##database = databases.copy()
                    if script_type == 'loaded':
                        # create databases before first script (only)
                        commands_create_databases = ["initdatabases.sql"]
                        script_type_create_databases = "tenants"
                        thread_args = {
                            'app':self.appname,
                            'component':'sut',
                            'experiment':self.code,
                            'configuration':self.configuration,
                            'pod_sut':self.pod_sut,
                            'scriptfolder':scriptfolder,
                            'commands':commands_create_databases,
                            'loadData':self.dockertemplate['loadData'],
                            'path':self.experiment.path,
                            'volume':volume,
                            'context':self.experiment.cluster.context,
                            'service_name':service_name,
                            'time_offset':time_offset,
                            'script_type':script_type_create_databases,
                            'time_start_int':time_start_int,
                            'namespace':self.experiment.cluster.namespace,
                            'num_tenants':0,
                            'id_tenant':0,
                            'database':databases,
                        }
                        self.logger.debug("load_data_asynch - run create database scripts {}".format(thread_args))
                        load_data_asynch(**thread_args)
                    for tenant in range(self.num_tenants):
                        databases = [f'tenant_{tenant}']
                        thread_args = {
                            'app':self.appname,
                            'component':'sut',
                            'experiment':self.code,
                            'configuration':self.configuration,
                            'pod_sut':self.pod_sut,
                            'scriptfolder':scriptfolder,
                            'commands':commands,
                            'loadData':self.dockertemplate['loadData'],
                            'path':self.experiment.path,
                            'volume':volume,
                            'context':self.experiment.cluster.context,
                            'service_name':service_name,
                            'time_offset':time_offset,
                            'script_type':script_type,
                            'time_start_int':time_start_int,
                            'namespace':self.experiment.cluster.namespace,
                            'num_tenants':self.num_tenants,
                            'id_tenant':tenant,
                            'database':databases,
                        }
                        self.logger.debug("load_data_asynch - run database-wise scripts {}".format(thread_args))
                        thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                        thread.start()
                        time.sleep(1)
                elif self.tenant_per == 'container':
                    thread_args = {
                        'app':self.appname,
                        'component':'sut',
                        'experiment':self.code,
                        'configuration':self.configuration,
                        'pod_sut':self.pod_sut,
                        'scriptfolder':scriptfolder,
                        'commands':commands,
                        'loadData':self.dockertemplate['loadData'],
                        'path':self.experiment.path,
                        'volume':volume,
                        'context':self.experiment.cluster.context,
                        'service_name':service_name,
                        'time_offset':time_offset,
                        'script_type':script_type,
                        'time_start_int':time_start_int,
                        'namespace':self.experiment.cluster.namespace,
                        'num_tenants':0,
                        'id_tenant':0,
                        'database':databases,
                    }
                    self.logger.debug("load_data_asynch - run container-wise scripts {}".format(thread_args))
                    thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                    thread.start()
                #print("####################", commands)
                print("{:30s}: runs scripts {}".format(self.configuration, commands))
            else:
                thread_args = {
                    'app':self.appname,
                    'component':'sut',
                    'experiment':self.code,
                    'configuration':self.configuration,
                    'pod_sut':self.pod_sut,
                    'scriptfolder':scriptfolder,
                    'commands':commands,
                    'loadData':self.dockertemplate['loadData'],
                    'path':self.experiment.path,
                    'volume':volume,
                    'context':self.experiment.cluster.context,
                    'service_name':service_name,
                    'time_offset':time_offset,
                    'script_type':script_type,
                    'time_start_int':time_start_int,
                    'namespace':self.experiment.cluster.namespace,
                    'num_tenants':0,
                    'id_tenant':0,
                    'database':databases,
                }
                self.logger.debug("load_data_asynch - run scripts {}".format(thread_args))
                thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                thread.start()
                return
    def get_patched_yaml(self, file, patch=""):
        """
        Applies a YAML formatted patch to a YAML file and returns merged result as a YAML object.

        :param file: Name of YAML file to load
        :param patch: Optional patch to be applied
        :return: YAML object of (patched) file content
        """
        if len(patch) > 0:
            merged = hiyapyco.load([file, patch], method=hiyapyco.METHOD_MERGE)
            self.logger.debug(hiyapyco.dump(merged, default_flow_style=False))
            stream = StringIO(hiyapyco.dump(merged)) # convert string to stream
            result = yaml.safe_load_all(stream)
            result = [data for data in result]
            #print(hiyapyco.dump(merged, default_flow_style=False))
            #patched = yaml.safe_load(hiyapyco.dump(merged))
            return result
        else:
            with open(file) as f:
                result = yaml.safe_load_all(f)
                result = [data for data in result]
                return result
                #unpatched = yaml.safe_load(f)
                #return unpatched
    def get_service_sut(self, configuration):
        """
        Returns the same of the service where to connect to the SUT.
        This in general is the name of the service of the deployed component.
        For SUT, that require a component that is not controlled by bexhoma, this may be overwritten.

        :param configuration: name of the configuration
        :return: name of the configuration's sut's service
        """
        app = self.appname
        #experiment = str(int(self.code))
        if len(self.sut_service_name) > 0:
            servicename = self.sut_service_name
        else:
            servicename = self.generate_component_name(app=app, component='sut', experiment=self.experiment_name, configuration=configuration)
        return servicename
    def create_manifest_job(self, app='', component='benchmarker', experiment='', configuration='', experimentRun='', client='1', parallelism=1, env={}, template='', nodegroup='', num_pods=1, connection='', patch_yaml=''):#, jobname=''):
        """
        Creates a job and sets labels (component/ experiment/ configuration).

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param experimentRun: Number of run of the configuration in this experiment
        :param client: Number of client of the job for this experiment run
        :param parallelism: Number of parallel pods in this job
        :param env: Dict of environment variables for the job manifest
        :param template: Template name of the job manifest
        :param nodegroup: Nodegroup of the pods of the job
        :param num_pods: Number of pods that run in total
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        if not experimentRun:
            experimentRun = str(self.num_experiment_to_apply_done+1)
        #connection = configuration
        #if not len(jobname):
        jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=str(client))
        servicename = self.get_service_sut(configuration=configuration)#self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
        #print(jobname)
        # start (create) time of the job
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        time_now = str(datetime.now())
        time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
        #self.current_benchmark_start = int(time_now_int)
        # parameter of the configuration
        c = copy.deepcopy(self.dockertemplate['template'])
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = self.connectionmanagement['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = self.connectionmanagement['runsPerConnection']
        c['connectionmanagement']['timeout'] = self.connectionmanagement['timeout']
        c['connectionmanagement']['singleConnection'] = self.connectionmanagement['singleConnection'] if 'singleConnection' in self.connectionmanagement else True
        env_default = dict()
        env_default['BEXHOMA_HOST'] = servicename
        env_default['BEXHOMA_CLIENT'] = int(self.client)-1
        #env_default['BEXHOMA_CLIENT'] = str(parallelism) # why?
        env_default['BEXHOMA_EXPERIMENT'] = experiment
        #env['BEXHOMA_CONNECTION'] = connection # only exists for benchmarker
        env_default['BEXHOMA_CONNECTION'] = configuration
        env_default['BEXHOMA_CONFIGURATION'] = configuration
        env_default['BEXHOMA_SLEEP'] = '60'
        env_default['BEXHOMA_VOLUME'] = self.volume
        env_default['BEXHOMA_EXPERIMENT_RUN'] = experimentRun
        env_default['BEXHOMA_PARALLEL'] = str(parallelism)
        env_default['BEXHOMA_NUM_PODS'] = str(num_pods)
        if self.num_tenants > 0 and self.tenant_per == 'container':
            env_default['BEXHOMA_NUM_PODS_TOTAL'] = str(int(num_pods)*self.num_tenants)
        else:
            env_default['BEXHOMA_NUM_PODS_TOTAL'] = str(num_pods)
        env_default['PARALLEL'] = str(parallelism)  # deprecated
        env_default['NUM_PODS'] = str(num_pods)     # deprecated
        name = self.generate_component_name(app=app, component='sut', experiment=self.experiment_name, configuration=configuration)
        name_worker = self.get_worker_name()
        name_service_headless = name_worker# must be the same
        # generate list of worker names
        list_of_workers = []
        for worker in range(self.num_worker):
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(name_worker=name_worker, worker_number=worker, worker_service=name_service_headless)
            list_of_workers.append(worker_full_name)
        list_of_workers_as_string = ",".join(list_of_workers)
        env_default['BEXHOMA_WORKER_LIST'] = list_of_workers_as_string
        list_of_workers_as_string_space = " ".join(list_of_workers)
        env_default['BEXHOMA_WORKER_LIST_SPACE'] = list_of_workers_as_string_space
        env_default['BEXHOMA_SUT_NAME'] = name
        if 'JDBC' in c:
            database = c['JDBC']['database'] if 'database' in c['JDBC'] else self.experiment.volume
            schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else ''
            if self.tenant_per == 'schema':
                schema = 'DBMSBENCHMARKER_SCHEMA'
            elif self.tenant_per == 'database':
                database = 'DBMSBENCHMARKER_DATABASE'
            env_default['BEXHOMA_URL'] = c['JDBC']['url'].format(
                serverip=servicename,
                dbname=self.experiment.volume,
                DBNAME=self.experiment.volume.upper(),
                timout_s=c['connectionmanagement']['timeout'],
                timeout_ms=c['connectionmanagement']['timeout']*1000,
                namespace=self.experiment.cluster.namespace,
                database=database,
                schema=schema,
                )
            env_default['BEXHOMA_URL_LIST'] = c['JDBC']['url'].format(
                serverip=list_of_workers_as_string,
                dbname=self.experiment.volume,
                DBNAME=self.experiment.volume.upper(),
                timout_s=c['connectionmanagement']['timeout'],
                timeout_ms=c['connectionmanagement']['timeout']*1000,
                namespace=self.experiment.cluster.namespace,
                database=database,
                schema=schema,
                )
            env_default['BEXHOMA_USER'] = c['JDBC']['auth'][0]
            env_default['BEXHOMA_PASSWORD'] = c['JDBC']['auth'][1]
            env_default['BEXHOMA_DRIVER'] = c['JDBC']['driver']
            env_default['BEXHOMA_DATABASE'] = database#c['JDBC']['database']
            env_default['BEXHOMA_SCHEMA'] = schema#c['JDBC']['schema']
            env_default['BEXHOMA_VOLUME'] = self.experiment.volume
            if isinstance(c['JDBC']['jar'], str):
                env_default['BEXHOMA_JAR'] = c['JDBC']['jar']
            else:
                env_default['BEXHOMA_JAR'] = c['JDBC']['jar'][0]
        else:
            env_default['BEXHOMA_USER'] = c['auth'][0]
            env_default['BEXHOMA_PASSWORD'] = c['auth'][1]
        if self.num_worker > 0:
            #worker_full_name = "{name_worker}-{worker_number}".format(name_worker=name_worker, worker_number=0, worker_service=name_worker)
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(name_worker=name_worker, worker_number=0, worker_service=name_service_headless)
            env_default['BEXHOMA_WORKER_FIRST'] = worker_full_name
        env = {**env_default, **env}
        self.logger.debug('configuration.create_manifest_job({})'.format(jobname))
        self.logger.debug(env)
        #job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        job_experiment = self.experiment.path+'/{app}-{component}-{configuration}-{experimentRun}-{client}.yml'.format(app=app, component=component, configuration=configuration, experimentRun=experimentRun, client=client).lower()
        #with open(self.experiment.cluster.yamlfolder+"jobtemplate-dbmsbenchmarker.yml") as stream:
        # old unpatched loader:
        #with open(self.experiment.cluster.yamlfolder+template) as stream:
        #    try:
        #        result = yaml.safe_load_all(stream)
        #        result = [data for data in result]
        #        #print(result)
        #    except yaml.YAMLError as exc:
        #        print(exc)
        try:
            result = self.get_patched_yaml(self.experiment.cluster.yamlfolder+template, patch_yaml)
            #stream = StringIO(patched) # convert string to stream
            #result = yaml.safe_load_all(stream)
            #result = [data for data in result]
        except yaml.YAMLError as exc:
            print(exc)
        for dep in result:
            if dep['kind'] == 'Job':
                dep['metadata']['name'] = jobname
                job = dep['metadata']['name']
                dep['spec']['completions'] = num_pods
                dep['spec']['parallelism'] = parallelism
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['connection'] = connection
                dep['metadata']['labels']['dbms'] = self.docker
                dep['metadata']['labels']['experiment'] = str(experiment)
                dep['metadata']['labels']['client'] = str(client)
                dep['metadata']['labels']['experimentRun'] = str(experimentRun)
                dep['metadata']['labels']['volume'] = self.volume
                for label_key, label_value in self.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['metadata']['labels']['start_time'] = str(time_now_int)
                dep['spec']['template']['metadata']['labels']['app'] = app
                dep['spec']['template']['metadata']['labels']['component'] = component
                dep['spec']['template']['metadata']['labels']['configuration'] = configuration
                dep['spec']['template']['metadata']['labels']['connection'] = connection
                dep['spec']['template']['metadata']['labels']['dbms'] = self.docker
                dep['spec']['template']['metadata']['labels']['experiment'] = str(experiment)
                dep['spec']['template']['metadata']['labels']['client'] = str(client)
                dep['spec']['template']['metadata']['labels']['experimentRun'] = str(experimentRun)
                dep['spec']['template']['metadata']['labels']['volume'] = self.volume
                for label_key, label_value in self.additional_labels.items():
                    dep['spec']['template']['metadata']['labels'][label_key] = str(label_value)
                dep['spec']['template']['metadata']['labels']['start_time'] = str(time_now_int)
                for i_container, c in enumerate(dep['spec']['template']['spec']['containers']):
                    #print(i_container)
                    env_manifest = {}
                    envs = c['env']
                    for i,e in enumerate(envs):
                        env_manifest[e['name']] = e['value']
                    #print(env_manifest)
                    env_merged = {**env_manifest, **env}
                    #print(env_merged)
                    self.logger.debug('configuration.create_manifest_job({})'.format(str(env_merged)))
                    dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    for i,e in env_merged.items():
                        dep['spec']['template']['spec']['containers'][i_container]['env'].append({'name':i, 'value':str(e)})
                if 'initContainers' in dep['spec']['template']['spec']:
                    for i_container, c in enumerate(dep['spec']['template']['spec']['initContainers']):
                        #print(i_container)
                        env_manifest = {}
                        envs = c['env']
                        for i,e in enumerate(envs):
                            env_manifest[e['name']] = e['value']
                        #print(env_manifest)
                        env_merged = {**env_manifest, **env}
                        #print(env_merged)
                        dep['spec']['template']['spec']['initContainers'][i_container]['env'] = []
                        for i,e in env_merged.items():
                            dep['spec']['template']['spec']['initContainers'][i_container]['env'].append({'name':i, 'value':str(e)})
                # set nodeSelector
                if len(nodegroup) and nodegroup in self.nodes:
                    if not 'nodeSelector' in dep['spec']['template']['spec']:
                        dep['spec']['template']['spec']['nodeSelector'] = dict()
                    if dep['spec']['template']['spec']['nodeSelector'] is None:
                        dep['spec']['template']['spec']['nodeSelector'] = dict()
                    dep['spec']['template']['spec']['nodeSelector']['type'] = self.nodes[nodegroup]
        with open(job_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        return job_experiment
    def create_manifest_benchmarking(self, connection, app='', component='benchmarker', experiment='', configuration='', experimentRun='', client='1', parallelism=1, alias='', env={}, template='', num_pods=1):
        """
        Creates a job template for the benchmarker.
        This sets meta data in the template and ENV.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: Number of benchmarker if there is a sequence of benchmarkers
        :param parallelism: Number of parallel pods in job
        :param alias: Alias name of the dbms
        :param env: Dict of environment variables
        :param template: Template for the job manifest 
        :return: Name of file in YAML format containing the benchmarker job
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        experimentRun = str(self.num_experiment_to_apply_done+1)
        #jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, client=str(client))
        #self.benchmarker_jobname = jobname
        self.logger.debug('configuration.create_manifest_benchmarking()')
        # determine start time
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=240)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        # store parameters in connection for evaluation
        e = {'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,#start_string, # wait until (=0 do not wait)
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias}
        env = {**env, **e}
        env = {**env, **self.benchmarking_parameters}
        #job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{experimentRun}-{client}.yml'.format(configuration=configuration, client=client)
        return self.create_manifest_job(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client, parallelism=parallelism, env=env, template="jobtemplate-benchmarking-dbmsbenchmarker.yml", num_pods=num_pods, nodegroup='benchmarking', connection=connection, patch_yaml=self.benchmarking_patch)
    def create_manifest_maintaining(self, app='', component='maintaining', experiment='', configuration='', parallelism=1, alias='', num_pods=1, connection=''):
        """
        Creates a job template for maintaining.
        This sets meta data in the template and ENV.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param parallelism: Number of parallel pods in job
        :return: Name of file in YAML format containing the maintaining job
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        experimentRun = str(self.num_experiment_to_apply_done+1)
        connection = self.configuration#self.getConnectionName()
        #jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        #self.maintaining_jobname = jobname
        servicename = self.get_service_sut(configuration=configuration)#self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
        #print(jobname)
        self.logger.debug('configuration.create_manifest_maintaining()')
        # determine start time
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=180)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        env = {'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': start_string,
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias,
            'SENSOR_DATABASE': 'postgresql://postgres:@{}:9091/postgres'.format(servicename)}
        env = {**env, **self.maintaining_parameters}
        #job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        template = "jobtemplate-maintaining.yml"
        if len(self.experiment.jobtemplate_maintaining) > 0:
            template = self.experiment.jobtemplate_maintaining
        return self.create_manifest_job(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=1, parallelism=parallelism, env=env, template=template, num_pods=num_pods, nodegroup='maintaining', connection=connection)#, jobname=jobname)
    def create_manifest_loading(self, app='', component='loading', experiment='', configuration='', parallelism=1, alias='', num_pods=1, connection=''):
        """
        Creates a job template for loading.
        This sets meta data in the template and ENV.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param parallelism: Number of parallel pods in job
        :return: Name of file in YAML format containing the loading job
        """
        if len(app) == 0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        experimentRun = str(self.num_experiment_to_apply_done+1)
        connection = self.configuration#self.getConnectionName()
        #jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        #servicename = self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
        #print(jobname)
        self.logger.debug('configuration.create_manifest_loading()')
        # determine start time
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=60)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        env = {'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,#start_string, # wait until (=0 do not wait)
            }
        # store parameters in connection for evaluation
        if len(self.loading_parameters):
            self.connection_parameter['loading_parameters'] = self.loading_parameters
        #print("self.loading_parameters", self.loading_parameters)
        #env = self.loading_parameters
        env = {**env, **self.loading_parameters}
        self.logger.debug("create_manifest_loading:env={}".format(env))
        template = "jobtemplate-loading.yml"
        if len(self.experiment.jobtemplate_loading) > 0:
            template = self.experiment.jobtemplate_loading
        if len(self.jobtemplate_loading) > 0:
            template = self.jobtemplate_loading
        return self.create_manifest_job(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=1, parallelism=parallelism, env=env, template=template, nodegroup='loading', num_pods=num_pods, connection=connection, patch_yaml=self.loading_patch)
    def get_worker_name(self):
        """
        Returns a template for the worker names.
        Default is component name is 'worker' for a bexhoma managed DBMS.
        If PVC are used, this must be changed, since the experiment code as part of the worker names would imply the PVC also are only valid for the concrete experiment.
        This is used for example to find the pods of the workers in order to get the host infos (CPU, RAM, node name, ...).

        :return: name template for worker pods
        """
        if self.storage['storageConfiguration']:
            storageConfiguration = self.storage['storageConfiguration']
        else:
            storageConfiguration = self.configuration
        # configure names
        if self.num_worker > 0:
            # we assume here, a stateful set is used
            # this means we do not want to have the experiment code as part of the names
            # this would imply there cannot be experiment independent pvcs
            self.experiment_name = self.storage_label#storageConfiguration
        else:
            self.experiment_name = self.code
        #name = self.generate_component_name(app=app, component=component, experiment=self.experiment_name, configuration=configuration)
        #name_worker = self.generate_component_name(app=app, component='worker', experiment=self.experiment_name, configuration=configuration)
        # test shorter names
        #name_worker = self.generate_component_name(app="bx", component='w', experiment=self.experiment_name, configuration=storageConfiguration)
        #this works, but is long for Redis:
        name_worker = self.generate_component_name(app=self.appname, component='worker', experiment=self.experiment_name, configuration=storageConfiguration)
        return name_worker
    def get_worker_pods(self):
        """
        Returns a list of all pod names of workers for the current SUT.
        Default is component name is 'worker' for a bexhoma managed DBMS.
        This is used for example to find the pods of the workers in order to get the host infos (CPU, RAM, node name, ...).

        :return: list of endpoints
        """
        if self.storage['storageConfiguration']:
            storageConfiguration = self.storage['storageConfiguration']
        else:
            storageConfiguration = self.configuration
        # configure names
        if self.num_worker > 0:
            # we assume here, a stateful set is used
            # this means we do not want to have the experiment code as part of the names
            # this would imply there cannot be experiment independent pvcs
            self.experiment_name = self.storage_label#storageConfiguration
        else:
            self.experiment_name = self.code
        #pods_worker = self.experiment.cluster.get_pods(app=self.appname, component='worker', experiment=self.experiment_name, configuration=storageConfiguration)
        pods_worker = self.experiment.cluster.get_pods(app=self.appname, component='worker', experiment=self.code, configuration=self.configuration)
        #pods_worker = self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
        if self.num_worker > 0:
            print("{:30s}: Worker pods found: {}".format(self.configuration, pods_worker))
        #print("Worker pods found: ", pods_worker)
        return pods_worker
    def get_worker_endpoints(self):
        """
        Returns all endpoints of a headless service that monitors nodes of a distributed DBMS.
        These are IPs of cAdvisor instances.
        The endpoint list is to be filled in a config of an instance of Prometheus.
        By default, the workers can be found by the name of their component (worker-0 etc).
        This is neccessary, when we have sidecar containers attached to workers of a distributed dbms.

        :return: list of endpoints
        """
        endpoints = []
        name_worker = self.get_worker_name()
        #name_worker = self.generate_component_name(component='worker', configuration=self.configuration, experiment=self.experiment_name)# self.code)
        pods_worker = self.get_worker_pods()
        for pod in pods_worker:
            endpoint = '{worker}.{service_sut}'.format(worker=pod, service_sut=name_worker)
            endpoints.append(endpoint)
            print("{:30s}: Worker endpoint : {}".format(self.configuration, endpoint))
            #print('Worker endpoint: {endpoint}'.format(endpoint = endpoint))
        return endpoints




# kubectl delete pvc,pods,services,deployments,jobs -l app=bexhoma-client
# kubectl delete pvc,pods,services,deployments,jobs -l app=bexhoma -l component=loading


class hammerdb(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

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
    def create_manifest_benchmarking(self, connection, app='', component='benchmarker', experiment='', configuration='', experimentRun='', client='1', parallelism=1, alias='', num_pods=1):
        """
        Creates a job template for the benchmarker.
        This sets meta data in the template and ENV.
        This sets some settings specific to HammerDB.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: Number of benchmarker if there is a sequence of benchmarkers
        :param parallelism: Number of parallel pods in job
        :param alias: Alias name of the dbms
        :return: Name of file in YAML format containing the benchmarker job
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        experimentRun = str(self.num_experiment_to_apply_done+1)
        #connection = configuration
        jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client)
        #self.benchmarker_jobname = jobname
        servicename = self.get_service_sut(configuration=configuration)#self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
        #print(jobname)
        self.logger.debug('hammerdb.create_manifest_benchmarking({})'.format(jobname))
        # determine start time
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=180)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        env = {'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,#start_string, # wait until (=0 do not wait)
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_PODS': str(num_pods),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias}
        env = {**env, **self.loading_parameters}
        env = {**env, **self.benchmarking_parameters}
        #job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        return self.create_manifest_job(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client, parallelism=parallelism, env=env, template="jobtemplate-benchmarking-hammerdb.yml", num_pods=num_pods, nodegroup='benchmarking', connection=connection, patch_yaml=self.benchmarking_patch)#, jobname=jobname)





class ycsb(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

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
    def create_manifest_benchmarking(self, connection, app='', component='benchmarker', experiment='', configuration='', experimentRun='', client='1', parallelism=1, alias='', num_pods=1):
        """
        Creates a job template for the benchmarker.
        This sets meta data in the template and ENV.
        This sets some settings specific to YCSB.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: Number of benchmarker if there is a sequence of benchmarkers
        :param parallelism: Number of parallel pods in job
        :param alias: Alias name of the dbms
        :return: Name of file in YAML format containing the benchmarker job
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        experimentRun = str(self.num_experiment_to_apply_done+1)
        #connection = configuration
        jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client)
        #self.benchmarker_jobname = jobname
        servicename = self.get_service_sut(configuration=configuration)#self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
        #print(jobname)
        self.logger.debug('ycsb.create_manifest_benchmarking({})'.format(jobname))
        # determine start time
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=180)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        env = {'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,#start_string, # wait until (=0 do not wait)
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_PODS': str(num_pods),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias}
        env = {**env, **self.loading_parameters}
        env = {**env, **self.benchmarking_parameters}
        #job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        return self.create_manifest_job(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client, parallelism=parallelism, env=env, template="jobtemplate-benchmarking-ycsb.yml", num_pods=num_pods, nodegroup='benchmarking', connection=connection, patch_yaml=self.benchmarking_patch)#, jobname=jobname)




class benchbase(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

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
    def create_manifest_benchmarking(self, connection, app='', component='benchmarker', experiment='', configuration='', experimentRun='', client='1', parallelism=1, alias='', num_pods=1):
        """
        Creates a job template for the benchmarker.
        This sets meta data in the template and ENV.
        This sets some settings specific to YCSB.

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: Number of benchmarker if there is a sequence of benchmarkers
        :param parallelism: Number of parallel pods in job
        :param alias: Alias name of the dbms
        :return: Name of file in YAML format containing the benchmarker job
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        experimentRun = str(self.num_experiment_to_apply_done+1)
        #connection = configuration
        jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client)
        #self.benchmarker_jobname = jobname
        servicename = self.get_service_sut(configuration=configuration)#self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
        #print(jobname)
        self.logger.debug('benchbase.create_manifest_benchmarking({})'.format(jobname))
        # determine start time
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=180)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        env = {'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,#start_string, # wait until (=0 do not wait)
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_PODS': str(num_pods),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias}
        env = {**env, **self.loading_parameters}
        env = {**env, **self.benchmarking_parameters}
        #job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        return self.create_manifest_job(app=app, component=component, experiment=experiment, configuration=configuration, experimentRun=experimentRun, client=client, parallelism=parallelism, env=env, template="jobtemplate-benchmarking-benchbase.yml", num_pods=num_pods, nodegroup='benchmarking', connection=connection, patch_yaml=self.benchmarking_patch)#, jobname=jobname)




class yugabytedb(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.
        This class contains specific settings for a YugabyteDB installation.
        This is handled outside of bexhoma with the official helm chart.
        The service name is fixed to be "yb-tserver-service"

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

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
    def get_service_sut(self, configuration):
        """
        Returns the same of the service where to connect to the SUT.
        This in general is the name of the service of the deployed component.
        For SUT, that require a component that is not controlled by bexhoma, this may be overwritten.
        Here, always "yb-tserver-service" is returned.

        :param configuration: name of the configuration
        :return: name of the configuration's sut's service
        """
        return "yb-tserver-service"




class kinetica(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.
        This class contains specific settings for a Kinetica installation.
        This is handled outside of bexhoma with the official KAgent.
        The service name is fixed to be "bexhoma-service-kinetica"

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

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
    def get_service_sut(self, configuration):
        """
        Returns the same of the service where to connect to the SUT.
        This in general is the name of the service of the deployed component.
        For SUT, that require a component that is not controlled by bexhoma, this may be overwritten.
        Here, always "bexhoma-service-kinetica" is returned.

        :param configuration: name of the configuration
        :return: name of the configuration's sut's service
        """
        return "bexhoma-service-kinetica"
    def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Generate a name for the monitoring component.
        Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`.
        For Kinetica, the service to be monitored is named 'bexhoma-service-kinetica'.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if component == 'sut':
            name = 'bexhoma-service-kinetica'
        else:
            name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        self.logger.debug("kinetica.create_monitoring({})".format(name))
        return name
    def set_metric_of_config(self, metric, host, gpuid):
        """
        Returns a promql query.
        Parameters in this query are substituted, so that prometheus finds the correct metric.
        Example: In 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))'
        configuration and experiment are placeholders and will be replaced by concrete values.
        Here: We do not have a SUT that is specific to the experiment or configuration.

        :param metric: Parametrized promql query
        :param host: Name of the host the metrics should be collected from
        :param gpuid: GPU that the metrics should watch
        :return: promql query without parameters
        """
        return metric.format(host=host, gpuid=gpuid, configuration='kinetica', experiment='worker')
    def get_worker_endpoints(self):
        """
        Returns all endpoints of a headless service that monitors nodes of a distributed DBMS.
        These are IPs of cAdvisor instances.
        The endpoint list is to be filled in a config of an instance of Prometheus.
        For Kinetica the service is fixed to be 'bexhoma-service-monitoring-default' and does not depend on the experiment.

        :return: list of endpoints
        """
        endpoints = self.experiment.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
        self.logger.debug("kinetica.get_worker_endpoints({})".format(endpoints))
        return endpoints













# https://stackoverflow.com/questions/37278647/fire-and-forget-python-async-await/53255955#53255955

#import asyncio

#def fire_and_forget(f):
#    def wrapped(*args, **kwargs):
#        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)
#    return wrapped



#@fire_and_forget
def load_data_asynch(app, component, experiment, configuration, pod_sut, scriptfolder, commands, loadData, path, volume, context, service_name, time_offset=0, time_start_int=0, script_type='loaded', namespace='', num_tenants=0, id_tenant=0, database=[]):
    logger = logging.getLogger('load_data_asynch')
    #with open('asynch.test.log','w') as file:
    #    file.write('started')
    #path = self.experiment.path
    #loadData = self.dockertemplate['loadData']
    def execute_command_in_pod_sut(command, pod, context):
        fullcommand = 'kubectl --context {context} exec {pod} --container=dbms -- bash -c "{command}"'.format(context=context, pod=pod, command=command.replace('"','\\"'))
        logger.debug('execute_command_in_pod_sut({})'.format(fullcommand))
        #print(fullcommand)
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        #print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        logger.debug(stdout.decode('utf-8'))
        logger.debug(stderr.decode('utf-8'))
        return "", stdout.decode('utf-8'), stderr.decode('utf-8')
    def kubectl(command, context):
        fullcommand = 'kubectl --context {context} {command}'.format(context=context, command=command)
        logger.debug('execute_command_in_pod_sut({})'.format(fullcommand))
        #print(fullcommand)
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        #print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        logger.debug(stdout.decode('utf-8'))
        logger.debug(stderr.decode('utf-8'))
        return stdout.decode('utf-8')
        #return os.system(fullcommand)
    #pods = self.experiment.cluster.get_pods(component='sut', configuration=configuration, experiment=experiment)
    #pod_sut = pods[0]
    #print("load_data")
    time_scriptgroup_start = default_timer() # for more precise float time spans
    # do we have started previously?
    if time_start_int == 0:
        now = datetime.utcnow() # for UTC time as int
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        time_now = str(datetime.now())
        timeLoadingStart = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
    else:
        # loading has been started previously
        timeLoadingStart = int(time_start_int)
        #time_now_int = int(time_start_int)
    logger.debug("#### time_scriptgroup_start: "+str(time_scriptgroup_start))
    logger.debug("#### timeLoadingStart: "+str(timeLoadingStart))
    logger.debug("#### timeLoading before scrips: "+str(time_offset))
    # mark pod
    labels = dict()
    labels[script_type] = 'False'
    labels["num_tenants"] = num_tenants
    if (num_tenants > 0 and id_tenant == 0) or num_tenants == 0:
        # only the first tenant writes timeStart
        logger.debug(f"#### First tenant {id_tenant} logs starting time")
        labels['timeLoadingStart'] = timeLoadingStart
        labels['num_tenants_ready'] = 0
        #if num_tenants > 0:
        #    labels['id_tenant'] = id_tenant
    fullcommand = 'label pods '+pod_sut+' --overwrite '
    for key, value in labels.items():
        fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
    #fullcommand = 'label pods '+pod_sut+' --overwrite {script_type}=False timeLoadingStart="{timeLoadingStart}" num_tenants="{num_tenants}"'.format(script_type=script_type, timeLoadingStart=timeLoadingStart, num_tenants=num_tenants)
    #print(fullcommand)
    kubectl(fullcommand, context)
    #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #stdout, stderr = proc.communicate()
    if len(volume) > 0:
        # mark pvc
        #fullcommand = 'label pvc '+volume+' --overwrite {script_type}=False timeLoadingStart="{timeLoadingStart}" num_tenants="{num_tenants}"'.format(script_type=script_type, timeLoadingStart=timeLoadingStart, num_tenants=num_tenants)
        fullcommand = 'label pvc '+volume+' --overwrite '
        for key, value in labels.items():
            fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
        #print(fullcommand)
        kubectl(fullcommand, context)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
    # scripts
    #scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiment.cluster.experiments_configfolder, docker=self.docker)
    #shellcommand = '[ -f {scriptname} ] && sh {scriptname}'
    times_script = dict()
    shellcommand = 'if [ -f {scriptname} ]; then sh {scriptname}; else exit 0; fi'
    #commands = self.initscript
    for db in database:
        for c in commands:
            time_scrip_start = default_timer() # for more precise float time spans
            #time_now = str(datetime.now())
            #time_scrip_start = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
            filename, file_extension = os.path.splitext(c)
            if file_extension.lower() == '.sql':
                stdin, stdout, stderr = execute_command_in_pod_sut(loadData.format(scriptname=scriptfolder+c, service_name=service_name, namespace=namespace, database=db), pod_sut, context)
                filename_log = path+'/{app}-loading-{configuration}-{filename}-{database}{extension}.log'.format(app=app, configuration=configuration, filename=filename, database=db, extension=file_extension.lower()).lower()
                #print(filename_log)
                if len(stdout) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stdout)
                filename_log = path+'/{app}-loading-{configuration}-{filename}-{database}{extension}.error'.format(app=app, configuration=configuration, filename=filename, database=db, extension=file_extension.lower()).lower()
                #print(filename_log)
                if len(stderr) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stderr)
            elif file_extension.lower() == '.sh':
                stdin, stdout, stderr = execute_command_in_pod_sut(shellcommand.format(scriptname=scriptfolder+c, service_name=service_name, namespace=namespace, database=db), pod_sut, context)
                filename_log = path+'/{app}-loading-{configuration}-{filename}{database}{extension}.log'.format(app=app, configuration=configuration, filename=filename, database=db, extension=file_extension.lower()).lower()
                #print(filename_log)
                if len(stdout) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stdout)
                filename_log = path+'/{app}-loading-{configuration}-{filename}{database}{extension}.error'.format(app=app, configuration=configuration, filename=filename, database=db, extension=file_extension.lower()).lower()
                #print(filename_log)
                if len(stderr) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stderr)
            #time_now = str(datetime.now())
            #time_scrip_end = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
            time_scrip_end = default_timer()
            sep = filename.find("-")
            if sep > 0:
                subscript_type = filename[:sep].lower()
                times_script[subscript_type] = time_scrip_end - time_scrip_start
                logger.debug("#### script="+str(subscript_type)+" time="+str(times_script[subscript_type]))
    # mark pod
    # get labels
    num_tenants_ready = 0
    if num_tenants > 0:
        while True:
            # kubectl get pod bexhoma-sut-postgresql-bht-2-1750309362-8657bf4ff5-njg5d -o jsonpath="{.metadata.labels}"
            fullcommand = 'get pod {pod_sut} -o jsonpath="{{.metadata.labels}}"'.format(pod_sut=pod_sut)
            labels = kubectl(fullcommand, context)
            #print(labels)
            labels = json.loads(labels)
            logger.debug(f"#### Found labels {id_tenant}: {labels}")
            if 'timeLoadingStart' in labels:
                timeLoadingStart = int(labels['timeLoadingStart'])
            if 'timeLoadingEnd' in labels:
                timeLoadingEnd = int(labels['timeLoadingEnd'])
            if 'timeLoading' in labels:
                timeLoading = int(labels['timeLoading'])
            if 'num_tenants_ready' in labels:
                num_tenants_ready = int(labels['num_tenants_ready'])
            logger.debug(f"num_tenants_ready, id_tenant: {num_tenants_ready}, {id_tenant}")
            if num_tenants_ready == id_tenant:
                break
            time.sleep(1)
        #num_tenants_ready = num_tenants_ready + 1
    # set time end and number of tenants ready
    time_scriptgroup_end = default_timer()
    time_now = str(datetime.now())
    timeLoadingEnd = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
    timeLoading = timeLoadingEnd - timeLoadingStart + time_offset # ceil(time_scriptgroup_end - time_scriptgroup_start + time_offset)
    logger.debug("#### time_scriptgroup_end: "+str(time_scriptgroup_end))
    logger.debug("#### timeLoadingEnd: "+str(timeLoadingEnd))
    logger.debug("#### timeLoading after scrips: "+str(timeLoading))
    #now = datetime.utcnow()
    #now_string = now.strftime('%Y-%m-%d %H:%M:%S')
    #time_now = str(datetime.now())
    #time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
    # store infos in labels of sut pod and it's pvc
    labels = dict()
    labels['num_tenants_ready'] = id_tenant + 1
    labels['time_{script_type}'.format(script_type=script_type)] = timeLoadingEnd - timeLoadingStart # ceil(time_scriptgroup_end - time_scriptgroup_start)
    #labels['timeLoadingEnd'] = time_now_int # is float, so needs ""
    labels['timeLoadingEnd'] = timeLoadingEnd
    if (num_tenants > 0 and id_tenant == num_tenants-1) or num_tenants == 0:
        # only the last tenant writes "finished"
        logger.debug(f"#### Last tenant {id_tenant} marks loading as finished")
        labels[script_type] = 'True'
        labels['timeLoading'] = timeLoading
    #labels['timeLoading'] = timeLoading
    for subscript_type, time_subscript_type in times_script.items():
        labels['time_{script_type}'.format(script_type=subscript_type)] = ceil(time_subscript_type)
    #fullcommand = 'label pods {pod_sut} --overwrite timeLoadingEnd="{timeLoadingEnd}" '.format(pod_sut=pod_sut, timeLoadingEnd=timeLoadingEnd)
    fullcommand = 'label pods {pod_sut} --overwrite '.format(pod_sut=pod_sut)
    for key, value in labels.items():
        fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
    #fullcommand = 'label pods '+pod_sut+' --overwrite {script_type}=True time_{script_type}={timing_current} timeLoadingEnd="{timing}" timeLoading={timespan}'.format(script_type=script_type, timing=time_now_int, timespan=timeLoading, timing_current=(timeLoadingEnd - timeLoadingStart))
    #print(fullcommand)
    kubectl(fullcommand, context)
    #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #stdout, stderr = proc.communicate()
    if len(volume) > 0:
        # mark volume
        #fullcommand = 'label pvc {volume} --overwrite timeLoadingEnd="{timeLoadingEnd}" '.format(volume=volume, timeLoadingEnd=timeLoadingEnd)
        fullcommand = 'label pvc {volume} --overwrite '.format(volume=volume)
        for key, value in labels.items():
            fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
        #fullcommand = 'label pvc '+volume+' --overwrite {script_type}=True time_{script_type}={timing_current} timeLoadingEnd="{timing}" timeLoading={timespan}'.format(script_type=script_type, timing=time_now_int, timespan=timeLoading, timing_current=(timeLoadingEnd - timeLoadingStart))
        #print(fullcommand)
        kubectl(fullcommand, context)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
