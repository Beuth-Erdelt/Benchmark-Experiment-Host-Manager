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
    def wait(self, sec):
        """
        Function for waiting some time and inform via output about this

        :param sec: Number of seconds to wait
        """
        print("Waiting "+str(sec)+"s...", end="", flush=True)
        intervals = int(sec)
        time.sleep(intervals)
        print("done")
    def delay(self, sec):
        """
        Function for waiting some time and inform via output about this.
        Synonymous for wait()

        :param sec: Number of seconds to wait
        """
        self.wait(sec)
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
    def test_results(self):
        """
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
        ############ HammerDB
        #self.path = "/home/perdelt/benchmarks/1668286639/"
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".pickle"): 
                df = pd.read_pickle(self.path+"/"+filename)
                print(df)
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
                            print("{} is not running yet - ".format(config.configuration))#, end="", flush=True)
                            if self.cluster.max_sut is not None or self.max_sut is not None:
                                we_can_start_new_sut = True
                                if self.max_sut is not None:
                                    print("In experiment: {} running and {} pending pods: max is {} pods)".format(num_pods_running_experiment, num_pods_pending_experiment, self.max_sut))#, end="", flush=True)
                                    if num_pods_running_experiment+num_pods_pending_experiment >= self.max_sut:
                                        print("{} has to wait".format(config.configuration))
                                        we_can_start_new_sut = False
                                if self.cluster.max_sut is not None:
                                    print("In cluster: {} running and {} pending pods: max is {} pods".format(num_pods_running_cluster, num_pods_pending_cluster, self.cluster.max_sut))#, end="", flush=True)
                                    if num_pods_running_cluster+num_pods_pending_cluster >= self.cluster.max_sut:
                                        print("{} has to wait".format(config.configuration))
                                        we_can_start_new_sut = False
                                if we_can_start_new_sut:
                                    print("{} will start now".format(config.configuration))
                                    config.start_sut()
                                    num_pods_pending_experiment = num_pods_pending_experiment + 1
                                    num_pods_pending_cluster = num_pods_pending_cluster + 1
                            else:
                                print("{} will start now".format(config.configuration))
                                config.start_sut()
                                num_pods_pending_experiment = num_pods_pending_experiment + 1
                                num_pods_pending_cluster = num_pods_pending_cluster + 1
                                #self.wait(10)
                        else:
                            print("{} is pending".format(config.configuration))
                    continue
                # check if loading is done
                config.check_load_data()
                # start loading
                if not config.loading_started:
                    if config.sut_is_running():
                        print("{} is not loaded yet".format(config.configuration))
                    if len(config.benchmark_list) > 0:
                        if config.monitoring_active and not config.monitoring_is_running():
                            print("{} waits for monitoring".format(config.configuration))
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
                            print("{} will start loading but not before {}".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S')))
                            continue
                    else:
                        delay = 60
                        if 'delay_prepare' in config.dockertemplate:
                            # config demands other delay
                            delay = config.dockertemplate['delay_prepare']
                        config.loading_after_time = now + timedelta(seconds=delay)
                        print("{} will start loading but not before {} (that is in {} secs)".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S'), delay))
                        continue
                # check if maintaining
                if config.loading_finished and len(config.benchmark_list) > 0:
                    if config.monitoring_active and not config.monitoring_is_running():
                        print("{} waits for monitoring".format(config.configuration))
                        if not config.monitoring_is_pending():
                            config.start_monitoring()
                        continue
                    if config.maintaining_active:
                        if not config.maintaining_is_running():
                            print("{} is not maintained yet".format(config.configuration))
                            if not config.maintaining_is_pending():
                                config.start_maintaining(parallelism=config.num_maintaining, num_pods=config.num_maintaining_pods)
                            else:
                                print("{} has pending maintaining".format(config.configuration))
                # start benchmarking, if loading is done and monitoring is ready
                if config.loading_finished:
                    # still benchmarks: check loading and maintaining
                    if len(config.benchmark_list) > 0:
                        if config.monitoring_active and not config.monitoring_is_running():
                            print("{} waits for monitoring".format(config.configuration))
                            if not config.monitoring_is_pending():
                                config.start_monitoring()
                            continue
                        if config.maintaining_active and not config.maintaining_is_running():
                            print("{} waits for maintaining".format(config.configuration))
                            continue
                    app = self.cluster.appname
                    component = 'benchmarker'
                    configuration = ''
                    pods = self.cluster.get_job_pods(app, component, self.code, configuration=config.configuration)
                    if len(pods) > 0:
                        # still pods there
                        print("{} has running benchmarks".format(config.configuration))
                        continue
                    else:
                        if len(config.benchmark_list) > 0:
                            # next element in list
                            parallelism = config.benchmark_list.pop(0)
                            client = str(config.client)
                            config.client = config.client+1
                            print("Done {} of {} benchmarks. This will be client {}".format(config.num_experiment_to_apply_done, config.num_experiment_to_apply, client))
                            if len(config.benchmarking_parameters_list) > 0:
                                benchmarking_parameters = config.benchmarking_parameters_list.pop(0)
                                print("We will change parameters of benchmark", benchmarking_parameters)
                                config.set_benchmarking_parameters(**benchmarking_parameters)
                            if config.num_experiment_to_apply > 1:
                                connection=config.configuration+'-'+str(config.num_experiment_to_apply_done+1)+'-'+client
                            else:
                                connection=config.configuration+'-'+client
                            print("Running benchmark {}".format(connection))
                            config.run_benchmarker_pod(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism)
                            #config.run_benchmarker_pod_hammerdb(connection=connection, configuration=config.configuration, client=client, parallelism=parallelism)
                        else:
                            # no list element left
                            if stop:
                                print("{} can be stopped".format(config.configuration))
                                app = self.cluster.appname
                                component = 'sut'
                                pods = self.cluster.get_pods(app, component, self.code, config.configuration)
                                if len(pods) > 0:
                                    pod_sut = pods[0]
                                    self.cluster.store_pod_log(pod_sut, 'dbms')
                                config.stop_sut()
                                config.num_experiment_to_apply_done = config.num_experiment_to_apply_done + 1
                                if config.num_experiment_to_apply_done < config.num_experiment_to_apply:
                                    print("{} starts again".format(config.configuration))
                                    config.benchmark_list = config.benchmark_list_template.copy()
                                    # wait for PV to be gone completely
                                    self.wait(60)
                                    config.reset_sut()
                                    config.start_sut()
                                    self.wait(10)
                                else:
                                    config.experiment_done = True
                            else:
                                print("{} can be stopped, be we leave it running".format(config.configuration))
                else:
                    print("{} is loading".format(config.configuration))
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
                        if status == 'Succeeded':
                            print("Store logs of job {} pod {}".format(job, p))
                            #if status != 'Running':
                            self.cluster.store_pod_log(p)
                            #self.cluster.delete_pod(p)
                        if status == 'Failed':
                            print("Store logs of job {} pod {}".format(job, p))
                            #if status != 'Running':
                            self.cluster.store_pod_log(p)
                            #self.cluster.delete_pod(p)
                success = self.cluster.get_job_status(job)
                self.cluster.logger.debug('job {} has success status {}'.format(job, success))
                #print(job, success)
                if success:
                    # status per pod
                    for p in pods:
                        status = self.cluster.get_pod_status(p)
                        self.cluster.logger.debug('job-pod {} has status {}'.format(p, status))
                        #print(p,status)
                        if status == 'Succeeded':
                            #if status != 'Running':
                            if not self.cluster.pod_log_exists(p):
                                print("Store logs of job {} pod {}".format(job, p))
                                self.cluster.store_pod_log(p)
                            self.cluster.delete_pod(p)
                        if status == 'Failed':
                            #if status != 'Running':
                            if not self.cluster.pod_log_exists(p):
                                print("Store logs of job {} pod {}".format(job, p))
                                self.cluster.store_pod_log(p)
                            self.cluster.delete_pod(p)
                    self.end_benchmarking(job, config)
                    self.cluster.delete_job(job)
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
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            #if filename.startswith("bexhoma-loading-"+jobname) and filename.endswith(".{container}.log".format(container=container)):
            if filename.startswith(jobname) and filename.endswith(".{container}.log".format(container=container)):
                #print(filename)
                (timing_start, timing_end) = get_job_timing(self.path+"/"+filename)
                #print(df)
                if (timing_start, timing_end) == (0,0):
                    print("Error in "+filename)
                else:
                    timing.append((timing_start, timing_end))
        print(timing)
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
                # get monitoring for loading
                if self.monitoring_active:
                    cmd = {}
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
                    if len(endpoints_cluster)>0:
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
        self.storage_label = 'tpch-'+str(SF)
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
        self.storage_label = 'tpch-'+str(SF)
        self.jobtemplate_loading = "jobtemplate-loading-ycsb.yml"
        self.evaluator = evaluators.ycsb(code=self.code, path=self.cluster.resultfolder, include_loading=False, include_benchmarking=True)
    def OLD_log_to_df(self, filename):
        try:
            with open(filename) as f:
                lines = f.readlines()
            stdout = "".join(lines)
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)
            result = []
            #for line in s.split("\n"):
            for line in lines:
                line = line.strip('\n')
                cells = line.split(", ")
                #print(cells)
                if len(cells[0]) and cells[0][0] == "[":
                    result.append(line.split(", "))
            #print(result)
            df = pd.DataFrame(result)
            df.columns = ['category', 'type', 'value']
            df.index.name = connection_name[0]
            return df
        except Exception as e:
            print(e)
            return pd.DataFrame()
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
    def OLD_get_result_sum(self, df, category='[OVERALL]', type='Throughput(ops/sec)'):
        try:
            df2=df[df['type'] == type]
            s=df2[df2['category'] == category]
            total = s.drop(columns=['category','type']).apply(pd.to_numeric).sum(axis=1)
            return total.iloc[0]
        except Exception as e:
            print(e)
            print(df)
            return 0.0
    def OLD_get_result_max(self, df, category='[OVERALL]', type='Throughput(ops/sec)'):
        try:
            df2=df[df['type'] == type]
            s=df2[df2['category'] == category]
            total = s.drop(columns=['category','type']).apply(pd.to_numeric).max(axis=1)
            return total.iloc[0]
        except Exception as e:
            print(e)
            print(df)
            return 0.0
    def OLD_get_result_avg(self, df, category='[OVERALL]', type='Throughput(ops/sec)'):
        try:
            df2=df[df['type'] == type]
            s=df2[df2['category'] == category]
            total = s.drop(columns=['category','type']).apply(pd.to_numeric).mean(axis=1)
            return total.iloc[0]
        except Exception as e:
            print(e)
            print(df)
            return 0.0
    def OLD_get_parts_of_name(self, name):
        parts_name = re.findall('{(.+?)}', self.name_format)
        parts_values = re.findall('-(.+?)-', "-"+name.replace("-","--")+"--")
        return dict(zip(parts_name, parts_values))
    def OLD_get_overview_loading(self, dfs={}):
        tps = []
        if len(dfs) == 0:
            dfs = self.get_result(component="loading")
        for connection, df in dfs.items():
            #print(connection)
            if df.empty:
                print(connection, "is empty")
                continue
            #parts = re.findall('-(.+?)-', connection.replace("-","--")+"--")
            parts = self.get_parts_of_name(connection)
            #print(parts)
            #threads = int(parts[0])
            #pods = int(parts[1])
            #worker = int(parts[2])
            #target = int(parts[2])
            insert_Operations = float(self.get_result_sum(df, category='[INSERT]', type='Operations'))
            insert_OK = float(self.get_result_sum(df, category='[INSERT]', type='Return=OK'))
            overall_Throughput = float(self.get_result_sum(df, category='[OVERALL]', type='Throughput(ops/sec)'))
            overall_RunTime = float(self.get_result_max(df, category='[OVERALL]', type='RunTime(ms)'))
            insert_AverageLatency = float(self.get_result_avg(df, category='[INSERT]', type='AverageLatency(us)'))
            insert_95thPercentileLatency = float(self.get_result_avg(df, category='[INSERT]', type='95thPercentileLatency(us)'))
            insert_99thPercentileLatency = float(self.get_result_avg(df, category='[INSERT]', type='99thPercentileLatency(us)'))
            list_values_name = list(parts.values())
            num_pods = len(df.columns)-2
            #print(list_values_name)
            list_values_df = [
                connection, 
                num_pods, 
                overall_Throughput/int(parts['pods']),
                overall_Throughput, 
                overall_RunTime, 
                insert_Operations, 
                insert_OK, 
                insert_AverageLatency, 
                insert_95thPercentileLatency, 
                insert_99thPercentileLatency, 
                ]
            #print(list_values_df)
            list_values_name.extend(list_values_df)
            #print('combined', list_values_name)
            tps.append(list_values_name)
            #print(target, worker, pods, overall_Throughput, overall_RunTime, overall_Throughput, total_tps/pods)
        #print(tps)
        df_totals = pd.DataFrame(tps)
        #print(list(parts.keys()))
        columns = list(parts.keys())
        columns.extend([
            'connection', 
            'num_pods', 
            'total_tps_per_pod', 
            'overall_Throughput', 
            'overall_RunTime', 
            'insert_Operations', 
            'insert_OK', 
            'insert_AverageLatency', 
            'insert_95thPercentileLatency', 
            'insert_99thPercentileLatency',
            ])
        #print(columns)
        df_totals.columns = columns
        #list(parts.keys()).extend(['overall_Throughput', 'insert_Operations', 'insert_OK', 'overall_RunTime', 'insert_AverageLatency', 'insert_95thPercentileLatency', 'insert_99thPercentileLatency', 'total_tps_per_pod'])
        df_totals = df_totals.astype({'target':'float','pods':'int'})
        df_totals = df_totals.sort_values(['target','pods'])
        return df_totals
    def OLD_get_overview_benchmarking(self, dfs={}):
        tps = []
        if len(dfs) == 0:
            dfs = self.get_result(component="benchmarking")
        for connection, df in dfs.items():
            #print(connection)
            if df.empty:
                print(connection, "is empty")
                continue
            parts = self.get_parts_of_name(connection)
            #parts = re.findall('-(.+?)-', connection.replace("-","--")+"--")
            #print(parts)
            #threads = int(parts[1])
            #pods = int(parts[1])
            #worker = int(parts[2])
            #target = int(parts[3])
            #print(df)
            # read
            read_Operations = float(self.get_result_sum(df, category='[READ]', type='Operations'))
            read_OK = float(self.get_result_sum(df, category='[READ]', type='Return=OK'))
            read_AverageLatency = float(self.get_result_avg(df, category='[READ]', type='AverageLatency(us)'))
            read_95thPercentileLatency = float(self.get_result_avg(df, category='[READ]', type='95thPercentileLatency(us)'))
            read_99thPercentileLatency = float(self.get_result_avg(df, category='[READ]', type='99thPercentileLatency(us)'))
            # update
            update_Operations = float(self.get_result_sum(df, category='[UPDATE]', type='Operations'))
            update_OK = float(self.get_result_sum(df, category='[UPDATE]', type='Return=OK'))
            update_AverageLatency = float(self.get_result_avg(df, category='[UPDATE]', type='AverageLatency(us)'))
            update_95thPercentileLatency = float(self.get_result_avg(df, category='[UPDATE]', type='95thPercentileLatency(us)'))
            update_99thPercentileLatency = float(self.get_result_avg(df, category='[UPDATE]', type='99thPercentileLatency(us)'))
            # overall
            overall_Throughput = float(self.get_result_sum(df, category='[OVERALL]', type='Throughput(ops/sec)'))
            overall_RunTime = float(self.get_result_max(df, category='[OVERALL]', type='RunTime(ms)'))
            # inserts
            insert_Operations = float(self.get_result_sum(df, category='[INSERT]', type='Operations'))
            insert_OK = float(self.get_result_sum(df, category='[INSERT]', type='Return=OK'))
            insert_AverageLatency = float(self.get_result_avg(df, category='[INSERT]', type='AverageLatency(us)'))
            insert_95thPercentileLatency = float(self.get_result_avg(df, category='[INSERT]', type='95thPercentileLatency(us)'))
            insert_99thPercentileLatency = float(self.get_result_avg(df, category='[INSERT]', type='99thPercentileLatency(us)'))
            # scan
            scan_Operations = float(self.get_result_sum(df, category='[SCAN]', type='Operations'))
            scan_OK = float(self.get_result_sum(df, category='[SCAN]', type='Return=OK'))
            scan_AverageLatency = float(self.get_result_avg(df, category='[SCAN]', type='AverageLatency(us)'))
            scan_95thPercentileLatency = float(self.get_result_avg(df, category='[SCAN]', type='95thPercentileLatency(us)'))
            scan_99thPercentileLatency = float(self.get_result_avg(df, category='[SCAN]', type='99thPercentileLatency(us)'))
            # extract from naming (DEPRCATED?)
            list_values_name = list(parts.values())
            num_pods = len(df.columns)-2
            #print(list_values_name)
            list_values_df = [
                connection, 
                num_pods, 
                overall_Throughput, 
                overall_RunTime, 
                overall_Throughput/int(parts['pods']),
                read_Operations, 
                read_OK, 
                read_AverageLatency, 
                read_95thPercentileLatency, 
                read_99thPercentileLatency, 
                update_Operations, 
                update_OK, 
                update_AverageLatency, 
                update_95thPercentileLatency, 
                update_99thPercentileLatency, 
                insert_Operations, 
                insert_OK, 
                insert_AverageLatency, 
                insert_95thPercentileLatency, 
                insert_99thPercentileLatency, 
                scan_Operations, 
                scan_OK, 
                scan_AverageLatency, 
                scan_95thPercentileLatency, 
                scan_99thPercentileLatency, 
                ]
            #print(list_values_df)
            list_values_name.extend(list_values_df)
            #print('combined', list_values_name)
            tps.append(list_values_name)
            #tps.append(list(parts.values()).extend([target, worker, pods, overall_Throughput, overall_RunTime, read_Operations, read_OK, read_AverageLatency, read_95thPercentileLatency, read_99thPercentileLatency,
            #            update_Operations, update_OK, update_AverageLatency, update_95thPercentileLatency, update_99thPercentileLatency, overall_Throughput/pods]))
            #print(target, worker, pods, overall_Throughput, overall_RunTime, overall_Throughput, total_tps/pods)
        #print(tps)
        df_totals = pd.DataFrame(tps)
        columns = list(parts.keys())
        columns.extend([
            'connection', 
            'num_pods', 
            'overall_Throughput', 
            'overall_RunTime', 
            'total_tps_per_pod',
            'read_Operations', 
            'read_OK', 
            'read_AverageLatency', 
            'read_95thPercentileLatency', 
            'read_99thPercentileLatency', 
            'update_Operations', 
            'update_OK', 
            'update_AverageLatency', 
            'update_95thPercentileLatency', 
            'update_99thPercentileLatency', 
            'insert_Operations', 
            'insert_OK', 
            'insert_AverageLatency', 
            'insert_95thPercentileLatency', 
            'insert_99thPercentileLatency'
            'scan_Operations', 
            'scan_OK', 
            'scan_AverageLatency', 
            'scan_95thPercentileLatency', 
            'scan_99thPercentileLatency',
            ])
        #print(columns)
        df_totals.columns = columns
        df_totals = df_totals.astype({'target':'float','pods':'int'})
        df_totals = df_totals.sort_values(['target','pods'])
        return df_totals
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
        cmd = {}
        #stdout = self.experiment.cluster.kubectl('cp --container dashboard '+self.path+'/connections.config '+pod_dashboard+':/results/'+str(self.code)+'/connections.config')
        #self.logger.debug('copy config connections.config: {}'.format(stdout))
        #cmd['upload_config'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/connections.config', from_file=self.path+"/connections.config")
        #self.cluster.kubectl(cmd['upload_config'])
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/', to=self.path+"/")
        self.cluster.kubectl(cmd['download_results'])
        cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/', from_file=self.path+"/")
        #cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/'+str(self.code)+'/', from_file=self.path+"/")
        self.cluster.kubectl(cmd['upload_results'])
    def OLD_get_result(self, component='loading'):
        #path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
        path = self.path
        df_prev = pd.DataFrame()
        #pod_numbers = {}
        if component == "loading":
            ending = "sensor.log"
        else:
            component = "benchmarker"
            ending = ".log"
        connections = dict()
        #path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-"+component) and filename.endswith(".df.pickle"):
                #print(filename)
                #experiment_number = re.findall('{}(.+?).{}'.format(name, ending), filename)
                #print(experiment_number)
                c = re.findall('bexhoma-{}-(.+?)-{}'.format(component, self.code), filename)
                if len(c) == 0:
                    #print("empty")
                    continue
                connection = c[0]
                if connection in connections:
                    connections[connection].append(filename)
                else:
                    connections[connection] = [filename]
        #print(connections)
        dfs = dict()
        for connection, files in connections.items():
            #print(connection)
            #dfs[connection] = pd.DataFrame()
            for filename in files:
                #print(filename)
                #experiment_number = re.findall('bexhoma-{}-{}-{}-(.+?).{}'.format(component, connection, self.code, ending), filename)
                experiment_components = re.findall('bexhoma-{}-{}-{}-(.+?)-(.+?)-(.+?).{}'.format(component, connection, self.code, ending), filename)
                if len(experiment_components) == 0:
                    #print("empty")
                    continue
                #print("experiment_components", experiment_components)
                #experiment_number = experiment_number[0]
                # turns bexhoma-loading-postgresql-8-1-1024-1672704339-1-1-22gkq.sensor.log.df.pickle
                # into 1-1 
                connection_number = experiment_components[0][0]+"-"+experiment_components[0][1]#experiment_number#+"-"+client_number
                #print("connection_number", connection_number)
                #if connection_name in pod_numbers:
                #    pod_numbers[connection_name] = pod_numbers[connection_name] + 1
                #else:
                #    pod_numbers[connection_name] = 1
                try:
                    df = pd.read_pickle(path+"/"+filename)
                    if not df.empty:
                        connection_name = df.index.name+"-"+connection_number
                        #print("found", connection_name, df)
                        df.columns = ['category', 'type', connection_name]#+"-"+str(pod_numbers[connection_name])]
                        if not connection_name in dfs or dfs[connection_name].empty:
                            dfs[connection_name] = df
                        else:
                            dfs[connection_name] = pd.merge(dfs[connection_name], df,  how='left', left_on=['category','type'], right_on = ['category','type'])
                except Exception as e:
                    print(e)
        #print("### All DataFrames ###")
        #print(dfs)
        return dfs



"""
############################################################################
Benchbase
############################################################################
"""

class benchbase(default):
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
        self.set_experiment(volume='benchbase')
        self.set_experiment(script='Schema')
        self.cluster.set_experiments_configfolder('experiments/benchbase')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile('queries.config')
        self.set_workload(
            name = 'Benchbase Queries SF='+str(SF),
            info = 'This experiment performs some Benchbase workloads.'
            )
        self.storage_label = 'tpch-'+str(SF)
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
        cmd = {}
        cmd['download_results'] = 'cp {from_file} {to} -c dashboard'.format(from_file=pod_dashboard+':/results/'+str(self.code)+'/', to=self.path+"/")
        self.cluster.kubectl(cmd['download_results'])
        cmd['upload_results'] = 'cp {from_file} {to} -c dashboard'.format(to=pod_dashboard+':/results/', from_file=self.path+"/")
        self.cluster.kubectl(cmd['upload_results'])



"""
############################################################################
Example
############################################################################
"""

class example(default):
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
            queryfile = 'queries.config',
            SF = '100',
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
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_additional_labels(SF=SF)
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'Custom Example Queries',
            info = 'This experiment performs some custom queries.'
            )
        self.storage_label = 'example'

