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
        self.benchmarking_parameters = {}
        self.jobtemplate_maintaining = ""
        self.jobtemplate_loading = ""
        self.querymanagement = {}
        self.workload = {}
        self.monitoring_active = True
        self.loading_active = False
        self.num_loading = 0
        self.num_loading_pods = 0
        self.maintaining_active = False
        self.num_maintaining = 0
        self.num_maintaining_pods = 0
        # k8s:
        self.namespace = self.cluster.namespace
        self.configurations = []
        self.storage_label = ''
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
    def set_experiment(self, instance=None, volume=None, docker=None, script=None):
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
                if config.loading_finished:
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
            app = self.cluster.appname
            component = 'benchmarker'
            configuration = ''
            jobs = self.cluster.get_jobs(app, component, self.code, configuration)
            # all pods to these jobs
            pods = self.cluster.get_job_pods(app, component, self.code, configuration)
            # status per pod
            for p in pods:
                status = self.cluster.get_pod_status(p)
                self.cluster.logger.debug('job-pod {} has status {}'.format(p, status))
                #print(p,status)
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
                self.cluster.logger.debug('job {} has success status {}'.format(job, success))
                #print(job, success)
                if success:
                    self.end_benchmarking(job)
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
                        self.cluster.logger.debug("{} still benchmarks to run".format(config.configuration))
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
    def end_benchmarking(self, jobname):
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('default.end_benchmarking({})'.format(jobname))
    def end_loading(self, jobname):
        """
        Ends a loading job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('default.end_loading({})'.format(jobname))




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
            #detached=False
            ):
        default.__init__(self, cluster, code, num_experiment_to_apply, timeout)#, detached)
        self.set_experiment(volume='tpch')
        self.set_experiment(script='SF'+str(SF)+'-index')
        self.cluster.set_experiments_configfolder('experiments/tpch')
        parameter.defaultParameters = {'SF': str(SF)}
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
    def end_benchmarking(self,jobname):
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        #app = self.appname
        #code = self.code
        #experiment = code
        #jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, client=str(client))
        #jobname = self.benchmarker_jobname
        self.cluster.logger.debug('tpcc.end_benchmarking({})'.format(jobname))
        pods = self.cluster.get_pods(component='dashboard')
        if len(pods) > 0:
            pod_dashboard = pods[0]
            status = self.cluster.get_pod_status(pod_dashboard)
            print(pod_dashboard, status)
            while status != "Running":
                self.wait(10)
                status = self.cluster.get_pod_status(pod_dashboard)
                print(pod_dashboard, status)
            filename_logs = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}/{}*'.format(self.code, jobname)
            #filename_logs = '/results/{}/{}*'.format(self.code, jobname)
            filename_df = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+jobname+'.df.pickle'
            cmd = {}
            # get connection name
            cmd['extract_results'] = 'grep -R BEXHOMA_CONNECTION {filename_logs}'.format(filename_logs=filename_logs)
            print(cmd['extract_results'])
            stdout = os.popen(cmd['extract_results']).read()
            #stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['extract_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
            print(stdout)
            connection_name = re.findall('BEXHOMA_CONNECTION:(.+?)\n', stdout)
            # get NOPM and TPM
            cmd['extract_results'] = 'grep -R RESULT {filename_logs}'.format(filename_logs=filename_logs)
            print(cmd['extract_results'])
            stdout = os.popen(cmd['extract_results']).read()
            #stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['extract_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
            print(stdout)
            list_nopm = re.findall('achieved (.+?) NOPM', stdout)
            list_tpm = re.findall('from (.+?) ', stdout)
            # get vuser
            cmd['extract_results'] = 'grep -R \'Active Virtual Users\' {filename_logs}'.format(filename_logs=filename_logs)
            print(cmd['extract_results'])
            stdout = os.popen(cmd['extract_results']).read()
            #stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['extract_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
            print(stdout)
            list_vuser = re.findall('Vuser 1:(.+?) Active', stdout)
            # what we have found
            print(list_nopm)
            print(list_tpm)
            print(list_vuser)
            # build DataFrame
            if len(list_nopm) and len(list_tpm) and len(list_vuser):
                df = pd.DataFrame(list(zip(list_nopm, list_tpm, list_vuser)))
                df.columns = ['NOPM','TPM', 'VUSERS']
                if len(connection_name) > 0:
                    df.index.name = str(connection_name[0])
                print(df)
                f = open(filename_df, "wb")
                pickle.dump(df, f)
                f.close()
                #self.loading_parameters['HAMMERDB_VUSERS']
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        try:
            path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
            #path = '../benchmarks/1669163583'
            directory = os.fsencode(path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".pickle"): 
                    df = pd.read_pickle(path+"/"+filename)
                    print(df)
                    print(df.index.name)
                    print(list(df['VUSERS']))
                    print(" ".join(l))
            return 0
        except Exception as e:
            return 1



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
    def end_loading(self, jobname):
        """
        Ends a loading job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('tsbs.end_loading({})'.format(jobname))
        filename_logs = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}/{}*'.format(self.code, jobname)
        cmd = {}
        # get connection name
        cmd['extract_results'] = 'grep -R loaded {filename_logs}'.format(filename_logs=filename_logs)
        print(cmd['extract_results'])
        stdout = os.popen(cmd['extract_results']).read()
        #stdin, stdout, stderr = self.experiment.cluster.execute_command_in_pod(command=cmd['extract_results'], pod=pod_dashboard, container="dashboard")#self.yamlfolder+deployment)
        print(stdout)
        return super().end_loading(jobname)

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
    def log_to_df(self, filename):
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
    def end_loading(self, jobname):
        """
        Ends a loading job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('ycsb.end_loading({})'.format(jobname))
        path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
        #path = '../benchmarks/1669640632'
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-") and filename.endswith(".sensor.log"):
                print(filename)
                df = self.log_to_df(path+"/"+filename)
                filename_df = path+"/"+filename+".df.pickle"
                f = open(filename_df, "wb")
                pickle.dump(df, f)
                f.close()
        return super().end_loading(jobname)
    def end_benchmarking(self, jobname):
        """
        Ends a benchmarker job.
        This is for storing or cleaning measures.

        :param jobname: Name of the job to clean
        """
        self.cluster.logger.debug('ycsb.end_benchmarking({})'.format(jobname))
        path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
        #path = '../benchmarks/1669640632'
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("bexhoma-benchmarker") and filename.endswith(".log"):
                print(filename)
                df = self.log_to_df(path+"/"+filename)
                filename_df = path+"/"+filename+".df.pickle"
                f = open(filename_df, "wb")
                pickle.dump(df, f)
                f.close()
        return super().end_benchmarking(jobname)
    def test_results(self):
        """
        Run test script locally.
        Extract exit code.

        :return: exit code of test script
        """
        self.cluster.logger.debug('ycsb.test_results()')
        try:
            path = self.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+'/{}'.format(self.code)
            #path = '../benchmarks/1669163583'
            directory = os.fsencode(path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".pickle"): 
                    df = pd.read_pickle(path+"/"+filename)
                    print(filename)
                    print(df)
            return 0
        except Exception as e:
            return 1



