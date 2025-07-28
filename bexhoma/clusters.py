"""
:Date: 2022-10-01
:Version: 0.6.0
:Authors: Patrick K. Erdelt

    Module to manage testbeds.
    Historically this supported different implementations based on IaaS.
    All methods will be deprecated except for Kubernetes (K8s), so the structure will change in future.

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
import time
import kubernetes.client as kubernetes_client
import kubernetes.config as kubernetes_config
from kubernetes.client.rest import ApiException
#from kubernetes import client, config
import subprocess
import os
import time
import psutil
import logging
import socket
import ast
import urllib.request
import urllib.parse
from pprint import pprint
from datetime import datetime, timedelta

from dbmsbenchmarker import *

class testbed():
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class to manage experiments in a Kubernetes cluster.

        TODO:

        * Remove instance / volume references from IaaS
        * Documentation for purpose and position
        * Documentation for "copy log and init" mechanisms 
        * Clearify if `OLD_` can be reused

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
    def __init__(self, clusterconfig='cluster.config', experiments_configfolder='experiments/', yamlfolder='k8s/', context=None, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        self.logger = logging.getLogger('bexhoma')
        self.clusterconfig = clusterconfig
        self.appname = 'bexhoma'
        self.namespace = 'bexhoma'
        with open(clusterconfig) as f:
            configfile=f.read()
            self.config = eval(configfile)
        if context is None:
            # use current context
            try:
                context = kubernetes_config.list_kube_config_contexts()[1]['name']
                self.contextdata = self.config['credentials']['k8s']['context'][context]
                self.host = 'localhost'
                self.port = self.contextdata['port']
                # k8s:
                self.namespace = self.contextdata['namespace']
                self.appname = self.config['credentials']['k8s']['appname']
                self.yamlfolder = yamlfolder
            except:
                print("WARN: No Kubernetes context found")
        self.context = context
        self.experiments = []
        self.benchmark = None
        self.experiments_configfolder = experiments_configfolder
        self.resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        self.queryfile = queryfile
        self.timeLoading = 0
        self.resources = {}
        self.ddl_parameters = {}
        self.connectionmanagement = {}
        self.connectionmanagement['numProcesses'] = None
        self.connectionmanagement['runsPerConnection'] = None
        self.connectionmanagement['timeout'] = None
        self.connectionmanagement['singleConnection'] = False
        self.querymanagement = {}
        self.workload = {}
        self.monitoring_active = True
        self.monitor_app_active = True
        self.monitor_cluster_active = False
        self.monitor_cluster_exists = False                                                     # True, if there are cAdvisors and a Prometheus server independent from bexhoma
        # experiment:
        self.set_experiments(self.config['instances'], self.config['volumes'], self.config['dockers'])
        self.set_experiment(instance, volume, docker, script)
        self.set_code(code)
        self.cluster_access()
    def cluster_access(self):
        """
        provide access to an K8s cluster by initializing connection handlers.
        """
        self.logger.debug('testbed.cluster_access({})'.format(self.context))
        try:
            kubernetes_config.load_kube_config(context=self.context)
            self.v1core = kubernetes_client.CoreV1Api(api_client=kubernetes_config.new_client_from_config(context=self.context))
            #self.v1beta = kubernetes_client.ExtensionsV1beta1Api(api_client=config.new_client_from_config(context=self.context))
            self.v1apps = kubernetes_client.AppsV1Api(api_client=kubernetes_config.new_client_from_config(context=self.context))
            self.v1batches = kubernetes_client.BatchV1Api(api_client=kubernetes_config.new_client_from_config(context=self.context))
        except:
            print("WARN: Could not connect to Kubernetes")
    def set_code(self, code):
        """
        Sets the unique identifier of an experiment.
        Use case: We start a cluster (without experiment), then define an experiment, which creates an identifier.
        This identifier will be set in the cluster as the default experiment.

        :param code: Unique identifier of an experiment
        """
        self.code = code
        if self.code is not None:
            resultfolder = self.config['benchmarker']['resultfolder']
            resultfolder += '/'+str(self.code)
            # store experiment list
            filename = resultfolder+'/experiments.config'
            if os.path.isfile(filename):
                print("experiments found")
                with open(filename, 'r') as f:
                    self.experiments = ast.literal_eval(f.read())
    # the following can be overwritten by experiment
    def set_queryfile(self, queryfile):
        """
        Sets the name of a query file of an experiment.
        This is for the benchmarker component (dbmsbenchmarker).

        :param code: Unique identifier of an experiment
        """
        self.queryfile = queryfile
    def set_experiments_configfolder(self, experiments_configfolder):
        """
        Sets the configuration folder for the experiments.
        Bexhoma expects subfolders for experiment types, for example tpch.
        In there, bexhoma looks for query.config files (for dbmsbenchmarker) and subfolders containing the schema per dbms.

        :param experiments_configfolder: Relative path to an experiment folder
        """
        self.experiments_configfolder = experiments_configfolder
    def set_workload(self, **kwargs):
        """
        Sets mata data about the experiments for example name and description.

        :param kwargs: Dict of meta data, example 'name' => 'TPC-H'
        """
        self.workload = kwargs
    def set_querymanagement(self, **kwargs):
        """
        Sets query management data for the experiments.
        This is for the benchmarker component (dbmsbenchmarker).

        :param kwargs: Dict of meta data, example 'numRun' => 3
        """
        self.querymanagement = kwargs
    # the following can be overwritten by experiment and configuration
    def set_connectionmanagement(self, **kwargs):
        """
        Sets connection management data for the experiments.
        This is for the benchmarker component (dbmsbenchmarker).
        Can be overwritten by experiment and configuration.

        :param kwargs: Dict of meta data, example 'timout' => 60
        """
        self.connectionmanagement = kwargs
    def set_resources(self, **kwargs):
        """
        Sets resources for the experiments.
        This is for the SUT component.
        Can be overwritten by experiment and configuration.

        :param kwargs: Dict of meta data, example 'requests' => {'cpu' => 4}
        """
        self.resources = kwargs
    def set_ddl_parameters(self, **kwargs):
        """
        Sets DDL parameters for the experiments.
        This substitutes placeholders in DDL script.
        Can be overwritten by experiment and configuration.

        :param kwargs: Dict of meta data, example 'index' => 'btree'
        """
        self.ddl_parameters = kwargs
    def log_experiment(self, experiment):
        """
        Function to log current step of experiment.
        This is supposed to be written on disk for comprehension and repetition.
        This should be reworked and yield a YAML format for example.
        Moreover this should respect "new" workflows with detached parallel loaders for example.

        :param experiment: Dict that stores parameters of current experiment stept
        """
        self.logger.debug('testbed.log_experiment()')
        # TODO: update to new structure
        experiment['clusterconfig'] = self.clusterconfig
        experiment['experiments_configfolder'] = self.experiments_configfolder
        experiment['yamlfolder'] = self.yamlfolder
        experiment['queryfile'] = self.queryfile
        experiment['clustertype'] = "K8s"
        self.experiments.append(experiment)
        # store experiment list
        if self.benchmark is not None and self.benchmark.path is not None:
            filename = self.benchmark.path+'/experiments.config'
            with open(filename, 'w') as f:
                f.write(str(self.experiments))
    def set_experiments(self, instances=None, volumes=None, dockers=None):
        """
        Assigns dicts containing information about instances, volumes and dbms (docker images).
        This typically comes from a cluster.config.

        :param instances: Dict of instances (DEPRECATED, was for IaaS?)
        :param volumes: Dict of volumes, that carry data
        :param dockers: Dict of docker images and meta data about how to usw
        """
        self.logger.debug('testbed.set_experiments()')
        """ Read experiment details from cluster config"""
        self.instance = None
        self.instances = instances
        self.volumes = volumes
        self.dockers = dockers
    def set_experiment(self, instance=None, volume=None, docker=None, script=None):
        """
        Sets a specific setting for an experiment.
        In particular this sets instance, volume and dbms (docker image) and name of a list of DDL scrips.
        This typically comes from a cluster.config.

        :param instances: Dict of instances (DEPRECATED, was for IaaS?)
        :param volumes: Dict of volumes, that carry data
        :param dockers: Dict of docker images and meta data about how to usw
        :param script: Name of list of DDL scripts, that are run when start_loading() is called
        """
        self.logger.debug('testbed.set_experiment()')
        # Will be deprecated
        #return self.setExperiment(instance, volume, docker, script)
        self.bChangeInstance = True
        if instance is not None:
            self.i = instance
        if volume is not None:
            self.v = volume
            self.volume = self.volumes[self.v]['id']
        if docker is not None:
            self.d = docker
            self.docker = self.dockers[self.d]
        if script is not None:
            self.s = script
            self.initscript = self.volumes[self.v]['initscripts'][self.s]
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
        intervals = int(sec)
        for x in [1]:
            if not silent:
                print("{:30s}: ".format("- waiting {}s -".format(sec)), end="", flush=True)
                #print('wait {}s'.format(intervals), end='\r')
            time.sleep(intervals)
        if not silent:
            print("done")
        #if not silent:
        #    print("")
    def delay(self, sec, silent=False):
        """
        Function for waiting some time and inform via output about this.
        Synonymous for wait()

        :param sec: Number of seconds to wait
        :param silent: True means we do not output anything about this waiting
        """
        self.wait(sec, silent)
    def delete_deployment(self, deployment):
        """
        Delete a deployment given by name.

        :param deployment: Name of the deployment to be deleted.
        """
        self.logger.debug('testbed.delete_deployment()')
        self.kubectl('delete deployment '+deployment)
    def get_deployments(self, app='', component='', experiment='', configuration=''):
        """
        Return all deployments matching a set of labels (component/ experiment/ configuration)

        :param app: app the deployment belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        #print(label)
        self.logger.debug('testbed.get_deployments({})'.format(label))
        try: 
            api_response = self.v1apps.list_namespaced_deployment(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling v1beta->list_namespaced_deployment: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
    def get_pods(self, app='', component='', experiment='', configuration='', status=''):
        """
        Return all pods matching a set of labels (component/ experiment/ configuration)

        :param app: app the pod belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param status: Status of the pod
        """
        self.logger.debug('testbed.get_pods()')
        # kubectl get pods --selector='job-name=bexhoma-client,app=bexhoma-client'
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        if len(status)>0:
            field_selector = 'status.phase='+status
        else:
            field_selector = ''
        self.logger.debug('get_pods label({})'.format(label))
        try: 
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label, field_selector=field_selector)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod for get_pods: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_pods(app=app, component=component, experiment=experiment, configuration=configuration, status=status)
    def get_stateful_sets(self, app='', component='', experiment='', configuration=''):
        """
        Return all stateful sets matching a set of labels (component/ experiment/ configuration)

        :param app: app the set belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        self.logger.debug('testbed.get_stateful_sets()')
        # kubectl get pods --selector='job-name=bexhoma-client,app=bexhoma-client'
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_stateful_sets'+label)
        try: 
            api_response = self.v1apps.list_namespaced_stateful_set(self.namespace, label_selector=label)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling AppsV1Api->list_namespaced_stateful_set: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
    def get_nodes(self, app='', nodegroup_type='', nodegroup_name=''):
        """
        Get all nodes of a cluster.

        :param app: Name of the pod
        :param nodegroup_type: Type of the nodegroup, e.g. sut
        :param nodegroup_name: Name of the nodegroup, e.g. sut_high_memory
        """
        self.logger.debug('testbed.get_nodes()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(nodegroup_type)>0:
            label += ',type='+nodegroup_type
        if len(nodegroup_name)>0:
            label += ',name='+nodegroup_name
        try:
            api_response = self.v1core.list_node(label_selector=label)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return api_response.items
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node for get_nodes: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_nodes(app=app, nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name)
    def get_pod_status(self, pod, app=''):
        """
        Return status of a pod given by name

        :param app: app the set belongs to
        :param pod: Name of the pod the status of which should be returned
        """
        self.logger.debug('testbed.get_pod_status()')
        try:
            if len(app) == 0:
                app = self.appname
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector='app='+app)
            #pprint(api_response)
            if len(api_response.items) > 0:
                for item in api_response.items:
                    if item.metadata.name == pod:
                        return item.status.phase
                return ""
            else:
                return ""
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod for get_pod_status: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_pod_status(pod=pod, app=app)
    def is_pod_ready(self, pod):
        self.logger.debug('testbed.is_pod_ready()')
        try:
            api_response = self.v1core.read_namespaced_pod(name=pod, namespace=self.namespace) # not available, label_selector='app='+app)
            #pprint(api_response)
            # Find the "Ready" condition
            #if len(api_response.status) > 0:
            for condition in api_response.status.conditions:
                if condition.type == "Ready":
                    #print("We found", pod, "is healthy =", condition.status == "True")
                    return condition.status == "True"
            return False  # If there's no "Ready" condition
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_pod for is_pod_ready: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.is_pod_ready(pod=pod, app=app)
            #print(f"Error fetching pod status: {e}")
            #return False
    def get_pods_labels(self, app='', component='', experiment='', configuration=''):
        """
        Return all labels of pods matching a set of labels (component/ experiment/ configuration)

        :param app: app the set belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        self.logger.debug('testbed.get_pods_labels()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        pod_labels = {}
        try:
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label)
            #pprint(api_response)
            if len(api_response.items) > 0:
                for item in api_response.items:
                    pod_labels[item.metadata.name] = item.metadata.labels
            return pod_labels
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod for get_pods_labels: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_pods_labels(app=app, component=component, experiment=experiment, configuration=configuration)
    def get_services(self, app='', component='', experiment='', configuration=''):
        """
        Return all services matching a set of labels (component/ experiment/ configuration)

        :param app: app the service belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        self.logger.debug('testbed.get_services()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_services({})'.format(label))
        try: 
            api_response = self.v1core.list_namespaced_service(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
    def get_ports_of_service(self, app='', component='', experiment='', configuration=''):
        """
        Return all ports of a services matching a set of labels (component/ experiment/ configuration)

        :param app: app the service belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        self.logger.debug('testbed.get_ports_of_service()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_ports_of_service'+label)
        try: 
            api_response = self.v1core.list_namespaced_service(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [str(p.port) for p in api_response.items[0].spec.ports]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_ports_of_service(app=app, component=component, experiment=experiment, configuration=configuration)
    def get_pvc(self, app='', component='', experiment='', configuration=''):
        """
        Return all persistent volume claims matching a set of labels (component/ experiment/ configuration)

        :param app: app the pvc belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        self.logger.debug('testbed.get_pvc()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_pvc({})'.format(label))
        try: 
            api_response = self.v1core.list_namespaced_persistent_volume_claim(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_pvc(app=app, component=component, experiment=experiment, configuration=configuration)
    def get_pvc_labels(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return all labels of persistent volume claims matching a set of labels (component/ experiment/ configuration) or name

        :param app: app the pvc belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param pvc: Name of the PVC
        """
        self.logger.debug('testbed.get_pvc_labels()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_pvc'+label)
        try: 
            api_response = self.v1core.list_namespaced_persistent_volume_claim(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                if len(pvc) > 0:
                    return [p.metadata.labels for p in api_response.items if p.metadata.name == pvc]
                else:
                    return [p.metadata.labels for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_pvc_labels(app=app, component=component, experiment=experiment, configuration=configuration, pvc=pvc)
    def get_pvc_specs(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return all specs of persistent volume claims matching a set of labels (component/ experiment/ configuration) or name

        :param app: app the pvc belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param pvc: Name of the PVC
        """
        self.logger.debug('testbed.get_pvc_specs()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_pvc'+label)
        try: 
            api_response = self.v1core.list_namespaced_persistent_volume_claim(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                if len(pvc) > 0:
                    return [p.spec for p in api_response.items if p.metadata.name == pvc]
                else:
                    return [p.spec for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_pvc_specs(app=app, component=component, experiment=experiment, configuration=configuration, pvc=pvc)
    def get_pvc_status(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return status of persistent volume claims matching a set of labels (component/ experiment/ configuration) or name

        :param app: app the pvc belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param pvc: Name of the PVC
        """
        self.logger.debug('testbed.get_pvc_status()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        self.logger.debug('get_pvc'+label)
        try: 
            api_response = self.v1core.list_namespaced_persistent_volume_claim(self.namespace, label_selector=label)#'app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                if len(pvc) > 0:
                    return [p.status for p in api_response.items if p.metadata.name == pvc]
                else:
                    return [p.spec for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_pvc_status(app=app, component=component, experiment=experiment, configuration=configuration, pvc=pvc)
    def get_statefulset_pods(self, stateful_set=''):
        """
        Return all pods belonging to a given stateful set.

        :param stateful_set: name of the stateful set
        :return: list of pod names
        """
        self.logger.debug('testbed.get_statefulset_pods()')
        label = f"statefulset.kubernetes.io/pod-name={stateful_set}"
        self.logger.debug('get_statefulset_pods'+label)
        try: 
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label)#'app='+appname)
            pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.get_statefulset_pods(stateful_set=stateful_set)
    def delete_stateful_set(self, name):
        """
        Delete a stateful set given by name

        :param name: name of the stateful set to be deleted
        """
        self.logger.debug('testbed.delete_stateful_set({})'.format(name))
        body = kubernetes_client.V1DeleteOptions()
        try: 
            api_response = self.v1apps.delete_namespaced_stateful_set(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling AppsV1Api->delete_namespaced_stateful_set: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.delete_stateful_set(name=name)
    def delete_pod(self, name):
        """
        Delete a pod given by name

        :param name: name of the pod to be deleted
        """
        self.logger.debug('testbed.delete_pod({})'.format(name))
        body = kubernetes_client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_pod(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.delete_pod(name=name)
    def delete_pvc(self, name):
        """
        Delete a persistent volume claim given by name

        :param name: name of the pvc to be deleted
        """
        self.logger.debug('testbed.delete_pvc({})'.format(name))
        body = kubernetes_client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_persistent_volume_claim(name, self.namespace, body=body)
            #pprint(api_response)
            return True
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return False
            #return self.delete_pvc(name=name)
    def delete_service(self, name):
        """
        Delete a service given by name

        :param name: name of the service to be deleted
        """
        self.logger.debug('testbed.delete_service({})'.format(name))
        body = kubernetes_client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_service(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.delete_service(name=name)
    def OLD_startPortforwarding(self, service='', app='', component='sut'):
        self.logger.debug('testbed.startPortforwarding()')
        ports = self.get_ports_of_service(app=app, component=component)
        if len(service) == 0:
            service = self.service
        if len(service) == 0:
            service = 'bexhoma-service'
        self.getInfo(component='sut')
        if len(self.deployments) > 0:
            forward = ['kubectl', '--context {context}'.format(context=self.context), 'port-forward', 'service/'+service] #bexhoma-service']#, '9091', '9300']#, '9400']
            #forward = ['kubectl', 'port-forward', 'pod/'+self.activepod]#, '9091', '9300']#, '9400']
            forward.extend(ports)
            #forward = ['kubectl', 'port-forward', 'service/service-dbmsbenchmarker', '9091', '9300']#, '9400']
            #forward = ['kubectl', 'port-forward', 'service/service-dbmsbenchmarker', portstring]
            #forward = ['kubectl', 'port-forward', 'deployment/'+self.deployments[0], portstring]
            your_command = " ".join(forward)
            #print(your_command)
            subprocess.Popen(your_command, stdout=subprocess.PIPE, shell=True)
    def OLD_getChildProcesses(self):
        self.logger.debug('testbed.getChildProcesses()')
        current_process = psutil.Process()
        children = current_process.children(recursive=False)
        #for child in children:
        #    print('Child pid is {} {}'.format(child.pid, child.name))
        #    print(child.cmdline())
    def OLD_stopPortforwarding(self):
        self.logger.debug('testbed.stopPortforwarding()')
        children = [p for p in psutil.process_iter(attrs=['pid', 'name']) if 'kubectl' in p.info['name']]
        for child in children:
            try:
                #print('Child pid is {} {}'.format(child.pid, child.name))
                self.logger.debug('testbed.stopPortforwarding() - Child {} {}'.format(child.pid, child.name))
                command = child.cmdline()
                #print(command)
                if len(command) > 0 and command[3] == 'port-forward':
                    self.logger.debug('testbed.stopPortforwarding() - Found child {}'.format(child.name))
                    child.terminate()
            except Exception as e:
                print(e)
    def kubectl(self, command):
        """
        Runs an kubectl command in the current context.

        :param command: An eksctl command
        :return: stdout of the kubectl command
        """
        fullcommand = 'kubectl --context {context} {command}'.format(context=self.context, command=command)
        self.logger.debug('testbed.kubectl({})'.format(fullcommand))
        #print(fullcommand)
        # Try reading the output with fallback encodings
        try:
            result = subprocess.check_output(fullcommand, shell=True, encoding='utf-8')
        except UnicodeDecodeError:
            # Fallback to Latin-1 or Windows-1252
            result = subprocess.check_output(fullcommand, shell=True, encoding='latin1')
        #print(result)
        return result
        #return os.popen(fullcommand).read()# os.system(fullcommand)
    def execute_command_in_pod(self, command, pod='', container='', params=''):
        """
        Runs an shell command remotely inside a container of a pod.

        :param command: A shell command
        :param pod: The name of the pod
        :param container: The name of the container in the pod
        :param params: Optional parameters, currently ignored
        :return: stdout of the shell command
        """
        if len(pod) == 0:
            self.logger.debug('testbed.execute_command_in_pod({}): empty pod name given for command'.format(command))
            return "", "", ""
            #pod = self.activepod
        command_clean = command.replace('"','\\"')
        if len(container) > 0:
            fullcommand = 'kubectl --context {context} exec {pod} --container={container} -- sh -c "{command}"'.format(context=self.context, pod=pod, container=container, command=command_clean)
        else:
            fullcommand = 'kubectl --context {context} exec {pod} -- sh -c "{command}"'.format(context=self.context, pod=pod, command=command_clean)
            #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command_clean+'"'
        #print(fullcommand)
        self.logger.debug('testbed.execute_command_in_pod({})'.format(fullcommand))
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        try:
            #print(stdout.decode('utf-8'), stderr.decode('utf-8'))
            str_stdout = stdout.decode('utf-8')
            str_stderr = stderr.decode('utf-8')
            if 'Error from server: error dialing backend' in str_stdout or 'Error from server: error dialing backend' in str_stderr:
                print("Connection error found")
                self.wait(5)
                return self.execute_command_in_pod(command=command, pod=pod, container=container, params=params)
            else:
                return "", str_stdout, str_stderr
        except Exception as e:
            print(e)
            print(stdout, stderr)
            str_stdout = stdout.decode('utf-8')
            str_stderr = stderr.decode('utf-8')
            if 'Error from server: error dialing backend' in str_stdout or 'Error from server: error dialing backend' in str_stderr:
                print("Connection error found")
                self.wait(5)
                return self.execute_command_in_pod(command=command, pod=pod, container=container, params=params)
            else:
                return "", stdout, stderr
        return "", "", ""
    def check_DBMS_connection(self, ip, port):
        """
        Check if DBMS is open for connections.
        Tries to open a socket to ip:port.
        Returns True if this is possible.

        :param ip: IP of the host to connect to
        :param port: Port of the server on the host to connect to
        :return: True, iff connecting is possible
        """
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
    def OLD__getTimediff(self):
        print("getTimediff")
        cmd = {}
        command = 'date +"%s"'
        fullcommand = 'kubectl exec '+cluster.activepod+' --container=dbms -- bash -c "'+command+'"'
        #stdin, stdout, stderr = self.execute_command_in_pod(command=command, pod=self.activepod, container='dbms')
        #gpus = stdout#os.popen(fullcommand).read()
        timestamp_remote = os.popen(fullcommand).read()
        timestamp_local = os.popen(command).read()
        #print(timestamp_remote)
        #print(timestamp_local)
        return int(timestamp_remote)-int(timestamp_local)
    def OLD_continueBenchmarks(self, connection=None, query=None):
        #experiments_configfolder='experiments/gdelt'
        #self.getInfo(component='sut')
        #self.deployment = self.get_deployments()[0]
        self.connection = connection
        self.resultfolder = self.config['benchmarker']['resultfolder']
        resultfolder = self.resultfolder+ '/'+str(self.code)
        connectionfile = resultfolder+'/connections.config'
        queryfile = resultfolder+'/queries.config'
        self.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            fixedQuery=query,
            result_path=resultfolder,
            batch=True,
            working='connection'
            )
        self.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        #self.stopPortforwarding()
        #self.startPortforwarding()
        self.benchmark.continueBenchmarks(overwrite = False)
        self.code = self.benchmark.code
        # prepare reporting
        self.copyInits()
        self.copyLog()
        self.downloadLog()
        self.benchmark.reporter.append(benchmarker.reporter.metricer(self.benchmark))
        evaluator.evaluator(self.benchmark, load=False, force=True)
        #self.benchmark.reporter.append(benchmarker.reporter.barer(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.ploter(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.boxploter(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.tps(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.hister(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.latexer(self.benchmark, 'pagePerQuery'))
        return self.code
    def OLD_runReporting(self):
        evaluator.evaluator(self.benchmark, load=False, force=True)
        self.benchmark.generateReportsAll()
    def OLD_copyLog(self):
        print("copyLog")
        if len(self.docker['logfile']):
            cmd = {}
            cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
            stdin, stdout, stderr = self.execute_command_in_pod(cmd['prepare_log'], container='dbms')
            cmd['save_log'] = 'cp '+self.docker['logfile']+' /data/'+str(self.code)+'/'+self.connection+'.log'
            stdin, stdout, stderr = self.execute_command_in_pod(cmd['save_log'], container='dbms')
    def OLD_copyInits(self):
        print("copyInits")
        cmd = {}
        cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
        stdin, stdout, stderr = self.execute_command_in_pod(cmd['prepare_log'], container='dbms')
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiments_configfolder, docker=self.d)
        i = 0
        for script in self.initscript:
            cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script, namespace=self.namespace)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
            stdin, stdout, stderr = self.execute_command_in_pod(cmd['copy_init_scripts'], container='dbms')
            i = i + 1
    def pod_description(self, pod, container=''):
        container = ''  # never sensitive to container
        if len(container) > 0:
            fullcommand = 'describe pod '+pod+' --container='+container
        else:
            fullcommand = 'describe pod '+pod
        #print(fullcommand)
        output = self.kubectl(fullcommand)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
        #print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        #return "", stdout.decode('utf-8'), stderr.decode('utf-8')
        return output
    def pod_log(self, pod, container=''):
        if len(container) > 0:
            fullcommand = 'logs '+pod+' --container='+container
        else:
            fullcommand = 'logs '+pod
        #print(fullcommand)
        output = self.kubectl(fullcommand)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
        #print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        #return "", stdout.decode('utf-8'), stderr.decode('utf-8')
        return output
    def get_pod_containers(self, pod):
        """
        Return all containers and initcontainers of a pod

        :param pod: name of the pod
        :return: list of names of (init)containers
        """
        fullcommand = 'get pods '+pod+' -o jsonpath="{.spec.containers[*].name}"'
        #print(fullcommand)
        output = self.kubectl(fullcommand)
        #print("get_pod_containers", output)
        containers = output.split(" ")
        #fullcommand = "get pods "+pod+" -o jsonpath='{.spec.initContainers[*].name}'"
        fullcommand = 'get pods '+pod+' -o jsonpath="{.spec.initContainers[*].name}"'
        #print(fullcommand)
        output = self.kubectl(fullcommand)
        #print("get_pod_containers", output)
        initContainers = output.split(" ")
        self.logger.debug("Pod {} has container {}".format(pod, containers + initContainers))
        return containers + initContainers
    def OLD_downloadLog(self):
        print("downloadLog")
        self.kubectl('cp --container dbms '+self.activepod+':/data/'+str(self.code)+'/ '+self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code))
    def get_jobs(self, app='', component='', experiment='', configuration='', client=''):
        """
        Return all jobs matching a set of labels (component/ experiment/ configuration)

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED?
        """
        #print("getJobs")
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        if len(client)>0:
            label += ',client='+client
        self.logger.debug('getJobs({})'.format(label))
        try: 
            api_response = self.v1batches.list_namespaced_job(self.namespace, label_selector=label)#'app='+appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling BatchV1Api->list_namespaced_job: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.get_jobs(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
    def get_jobs_labels(self, app='', component='', experiment='', configuration='', client=''):
        """
        Return all jobs matching a set of labels (component/ experiment/ configuration)

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED?
        """
        #print("getJobs")
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        if len(client)>0:
            label += ',client='+client
        self.logger.debug('get_jobs_labels '+label)
        job_labels = {}
        try:
            api_response = self.v1batches.list_namespaced_job(self.namespace, label_selector=label)#'app='+appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                for item in api_response.items:
                    job_labels[item.metadata.name] = item.metadata.labels
                return job_labels
            else:
                return []
        except ApiException as e:
            print("Exception when calling BatchV1Api->list_namespaced_job: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.get_jobs_labels(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
    def get_job_status(self, jobname='', app='', component='', experiment='', configuration='', client=''):
        """
        Return status of a jobs given by name or matching a set of labels (component/ experiment/ configuration)

        :param jobname: Name of the job we want to know the status of
        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED?
        """
        #print("getJobStatus")
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        if len(client)>0:
            label += ',client='+client
        self.logger.debug('getJobStatus '+label)
        try: 
            if len(jobname) == 0:
                jobs = self.get_jobs(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                if len(jobs) == 0:
                    return "no job"
                jobname = jobs[0]
            api_response = self.v1batches.read_namespaced_job_status(jobname, self.namespace)#, label_selector='app='+cluster.appname)
            #pprint(api_response)
            self.logger.debug("api_response.spec.completions {}".format(api_response.spec.completions))
            self.logger.debug("api_response.status.succeeded {}".format(api_response.status.succeeded))
            # returns number of completed pods (!)
            #return api_response.status.succeeded
            # we want status of job (!)
            #self.logger.debug("api_response.status.succeeded = {}".format(api_response.status.succeeded))
            #self.logger.debug("api_response.status.conditions = {}".format(api_response.status.conditions))
            if api_response.status.succeeded is not None and api_response.spec.completions <= api_response.status.succeeded:
                self.logger.debug("Number of completions reached")
                return True
            if api_response.status.succeeded is not None and api_response.status.succeeded > 0 and api_response.status.conditions is not None and len(api_response.status.conditions) > 0:
                self.logger.debug(api_response.status.conditions[0].type)
                return api_response.status.conditions[0].type == 'Complete'
            else:
                return 0
        except ApiException as e:
            print("Exception when calling BatchV1Api->read_namespaced_job_status: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.get_job_status(jobname=jobname, app=app, component=component, experiment=experiment, configuration=configuration, client=client)
            else:
                return 0
    def delete_job(self, jobname='', app='', component='', experiment='', configuration='', client=''):
        """
        Delete a job given by name or matching a set of labels (component/ experiment/ configuration)

        :param jobname: Name of the job we want to delete
        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED?
        """
        self.logger.debug('testbed.delete_job()')
        try: 
            if len(jobname) == 0:
                jobs = self.get_jobs(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                jobname = jobs[0]
            self.logger.debug('testbed.delete_job({})'.format(jobname))
            api_response = self.v1batches.delete_namespaced_job(jobname, self.namespace)#, label_selector='app='+cluster.appname)
            #pprint(api_response)
            #pprint(api_response.status.succeeded)
            return True
        except ApiException as e:
            print("Exception when calling BatchV1Api->delete_namespaced_job: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.delete_job(jobname=jobname, app=app, component=component, experiment=experiment, configuration=configuration, client=client)
    def delete_job_pods(self, jobname='', app='', component='', experiment='', configuration='', client=''):
        """
        Delete all pods of a job given by name or matching a set of labels (component/ experiment/ configuration)

        :param jobname: Name of the job we want to delete the pods of
        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED?
        """
        self.logger.debug('testbed.delete_job_pods()')
        body = kubernetes_client.V1DeleteOptions()
        try: 
            if len(jobname) == 0:
                pods = self.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                if len(pods) > 0:
                    for pod in pods:
                        self.delete_job_pods(jobname=pod, app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                    return
                #jobname = pods[0]
            self.logger.debug('testbed.delete_job_pods({})'.format(jobname))
            api_response = self.v1core.delete_namespaced_pod(jobname, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.delete_job_pods(jobname=jobname, app=app, component=component, experiment=experiment, configuration=configuration, client=client)
    def get_job_pods(self, app='', component='', experiment='', configuration='', client=''):
        """
        Return all pods of a jobs matching a set of labels (component/ experiment/ configuration)

        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED?
        """
        #print("getJobPods")
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(component)>0:
            label += ',component='+component
        if len(experiment)>0:
            label += ',experiment='+experiment
        if len(configuration)>0:
            label += ',configuration='+configuration
        if len(client)>0:
            label += ',client='+client
        self.logger.debug('getJobPods '+label)
        try: 
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label)#'app='+appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod for getJobPods: %s\n" % e)
            #if int(e) == 401:
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            # try again, if not failed due to "not found"
            if not e.status == 404:
                return self.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
    def create_dashboard_name(self, app='', component='dashboard'):
        """
        Creates a suitable name for the dashboard component.

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        """
        if len(app) == 0:
            app = self.appname
        name = "{app}_{component}".format(app=app, component=component)
        #print(name)
        self.logger.debug('testbed.create_dashboard_name({})'.format(name))
        return name
    def create_messagequeue_name(self, app='', component='messagequeue'):
        """
        Creates a suitable name for the message queue component.

        :param app: app the messagequeue belongs to
        :param component: Component name, should be 'messagequeue' typically
        """
        if len(app) == 0:
            app = self.appname
        name = "{app}_{component}".format(app=app, component=component)
        #print(name)
        self.logger.debug('testbed.create_messagequeue({})'.format(name))
        return name
    def dashboard_is_running(self):
        """
        Returns True, iff dashboard is running.

        :return: True, iff dashboard is running
        """
        app = self.appname
        component = 'dashboard'
        pod_dashboard = self.get_dashboard_pod_name(app=app, component=component)
        if len(pod_dashboard) > 0:
            # dashboard exists
            self.logger.debug('testbed.dashboard_is_running()=exists')
            #pod_dashboard = pods_dashboard[0]
            status = self.get_pod_status(pod_dashboard)
            #print("{:30s}: {} in pod {}".format("Dashboard", status, pod_dashboard))
            if status == "Running":
                self.logger.debug('testbed.dashboard_is_running() is running')
                return True
        return False
    def start_dashboard(self, app='', component='dashboard'):
        """
        Starts the dashboard component and its service, if there is no such pod.
        Manifest is expected in 'deploymenttemplate-bexhoma-dashboard.yml'.

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        """
        if len(self.get_dashboard_pod_name()):
            # there already is a dashboard pod
            print("{:30s}: is running".format("Dashboard"))
            return
        else:
            print("{:30s}: is starting...".format("Dashboard"), end="", flush=True)
            deployment = 'deploymenttemplate-bexhoma-dashboard.yml'
            name = self.create_dashboard_name(app, component)
            self.logger.debug('testbed.start_dashboard({})'.format(deployment))
            self.kubectl('create -f '+self.yamlfolder+deployment)
            while (not self.dashboard_is_running()):
               self.wait(10, silent=True)
            print("done")
            return
    def test_if_monitoring_healthy(self):
        """
        Tests if query_range?query=node_memory_MemTotal_bytes&start=1&end=2&step=1 at service_monitoring returns status code of 200.
        This is for testing if Prometheus is up and running.

        :return: True if Prometheus returns status code 200
        """
        self.logger.debug('testbed.test_if_monitoring_healthy()')
        config_K8s = self.config['credentials']['k8s']
        if 'service_monitoring' in config_K8s['monitor']:
            url = config_K8s['monitor']['service_monitoring'].format(namespace=self.contextdata['namespace'], service="monitoring")
            query = "sum(node_memory_MemTotal_bytes)"
            safe_query = urllib.parse.quote_plus(query)
            try:
                #code= urllib.request.urlopen(url+"query_range?query="+safe_query+"&start=1&end=2&step=1").getcode()
                # curl -ILs www.welt.de | head -n 1|cut -d$' ' -f2
                pod_dashboard = self.get_dashboard_pod_name()
                self.logger.debug('Inside pod {}'.format(pod_dashboard))
                now = datetime.utcnow()
                start = now - timedelta(seconds=300) # 5 minutes ago
                end = now - timedelta(seconds=240) # 4 minutes ago
                cmd = {}
                query_url = "{url}query_range?query={safe_query}&start={start}&end={end}&step=60".format(url=url, safe_query=safe_query, start=int(start.timestamp()), end=int(end.timestamp()))
                self.logger.debug('Test URL {}'.format(query_url))
                command = "curl -L --max-time 10 -is '{}' | head -n 1 | cut -d ' ' -f2".format(query_url)
                #command = "curl -is '{}' | head -n 1|cut -d$' ' -f2".format(url+"query_range?query="+safe_query+"&start=1&end=2&step=1")
                self.logger.debug('Command {}'.format(command))
                #fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
                #cores = os.popen(fullcommand).read()
                stdin, stdout, stderr = self.execute_command_in_pod(pod=pod_dashboard, command=command, container="dashboard")
                #print("Return", stdout, stderr)
                status = stdout#os.popen(fullcommand).read()
                self.logger.debug('Status {}'.format(status))
                if len(status)>0:
                    #return int(status)
                    #print(int(status))
                    if int(status) == 200:
                        return True
                    else:
                        return False
                else:
                    return False
                #except Exception as e:
                #    logging.error(e)
                #    return 0
                # curl -I http://www.example.org
                #if code == 200:
                #    #print("{:30s}: is running".format("Prometheus"))
                #    return True
                #else:
                #    #print("{:30s}: is not running".format("Prometheus"))
                #    return False
            except Exception as e:
                #print("{:30s}: is not running".format("Prometheus"))
                print(e)
                return False
    def start_monitoring_cluster(self, app='', component='monitoring'):
        """
        Starts the monitoring component and its service.
        Manifest for node exporters is expected in 'deamonsettemplate-monitoring.yml'.

        :param app: app monitoring belongs to
        :param component: Component name, should be 'monitoring' typically
        """
        self.monitor_cluster_active = True
        self.monitor_cluster_exists = self.test_if_monitoring_healthy()
        if self.monitor_cluster_exists:
            return
        if not self.monitor_cluster_exists:
            # give it 5 tries, one every 10 seconds
            for tries in range(5):
                self.wait(10, silent=True)
                self.monitor_cluster_exists = self.test_if_monitoring_healthy()
                if self.monitor_cluster_exists:
                    return
        endpoints = self.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
        if len(endpoints) > 0:
            # monitoring exists
            self.logger.debug('testbed.start_monitoring_cluster()=exists')
            print("{:30s}: is running".format("Cluster monitoring"))
            return
        else:
            self.logger.debug('testbed.start_monitoring_cluster()=deploy')
            deployment = 'daemonsettemplate-monitoring.yml'
            self.kubectl('create -f '+self.yamlfolder+deployment)
            print("{:30s}: starting...".format("Cluster monitoring"))
            while (not len(self.get_service_endpoints(service_name="bexhoma-service-monitoring-default"))):
               self.wait(10, silent=True)
            print("done")
            return
    def messagequeue_is_running(self, component='messagequeue'):
        """
        Returns True, iff message queue is running.

        :return: True, iff message queue is running
        """
        pods_messagequeue = self.get_pods(component=component)
        if len(pods_messagequeue) > 0:
            # message queue exists
            pod_messagequeue = pods_messagequeue[0]
            self.logger.debug('testbed.messagequeue_is_running()=exists')
            #pod_dashboard = pods_dashboard[0]
            status = self.get_pod_status(pod_messagequeue)
            #print("{:30s}: {} in pod {}".format("Message Queue", status, pod_messagequeue))
            if status == "Running":
                self.logger.debug('testbed.messagequeue_is_running() is running')
                return True
        return False
    def start_messagequeue(self, app='', component='messagequeue'):
        """
        Starts the message queue.
        Manifest is expected in 'deploymenttemplate-bexhoma-messagequeue.yml'

        :param app: app the messagequeue belongs to
        :param component: Component name, should be 'messagequeue' typically
        """
        pods_messagequeue = self.get_pods(component=component)
        if len(pods_messagequeue) > 0:
            # message queue exists
            self.logger.debug('testbed.start_messagequeue()=exists')
            print("{:30s}: is running".format("Message Queue"))
            return
        else:
            print("{:30s}: is starting...".format("Message Queue"), end="", flush=True)
            deployment = 'deploymenttemplate-bexhoma-messagequeue.yml'
            name = self.create_messagequeue_name(app, component)
            self.logger.debug('testbed.start_messagequeue({})'.format(deployment))
            self.kubectl('create -f '+self.yamlfolder+deployment)
            while (not self.messagequeue_is_running()):
               self.wait(10, silent=True)
            print("done")
            return
    def start_datadir(self):
        """
        Starts the data directory in a shared filesystem.
        This is where data generator pods can store generated data and where loading pods can read the data from. 
        Manifest is expected in 'pvc-bexhoma-data.yml'
        """
        app = self.appname
        # get data directory
        pvcs = self.get_pvc(app=app, component='data-source', experiment='', configuration='')
        if len(pvcs) > 0:
            print("{:30s}: is running".format("Data Directory"))
            return
        else:
            print("{:30s}: is starting...".format("Data Directory"), end="", flush=True)
            deployment = 'pvc-bexhoma-data.yml'
            self.kubectl('create -f '+self.yamlfolder+deployment)
            while (not len(self.get_pvc(app=app, component='data-source', experiment='', configuration=''))):
               self.wait(10, silent=True)
            print("done")
            return
    def start_resultdir(self):
        """
        Starts the result directory in a shared filesystem.
        This is where benchmark execution pods can store result data and where the evaluation pods can read results from.
        Also collected metrics will be stored there.
        Manifest is expected in 'pvc-bexhoma-results.yml'
        """
        app = self.appname
        # get result directory
        pvcs = self.get_pvc(app=app, component='results', experiment='', configuration='')
        if len(pvcs) > 0:
            print("{:30s}: is running".format("Result Directory"))
            return
        else:
            print("{:30s}: is starting...".format("Result Directory"), end="", flush=True)
            deployment = 'pvc-bexhoma-results.yml'
            self.kubectl('create -f '+self.yamlfolder+deployment)
            while (not len(self.get_pvc(app=app, component='results', experiment='', configuration=''))):
               self.wait(10, silent=True)
            print("done")
            return
    def get_dashboard_pod_name(self, app='', component='dashboard'):
        """
        Returns the name of the dashboard pod.

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        :return: name of the dashboard pod
        """
        pods_dashboard = self.get_pods(component=component)
        if len(pods_dashboard) > 0:
            # dashboard exists
            self.logger.debug('testbed.get_dashboard_pod_name()=exists')
            return pods_dashboard[0]
        else:
            self.logger.debug('testbed.get_dashboard_pod_name()=not exists')
            return ""
    def restart_dashboard(self, app='', component='dashboard'):
        """
        Stops the dashboard component and its service.

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        """
        self.logger.debug('testbed.restart_dashboard()')
        pod_dashboard = self.get_dashboard_pod_name(app=app, component=component)
        if len(pod_dashboard) > 0:
            self.delete_pod(pod_dashboard)
    def stop_dashboard(self, app='', component='dashboard'):
        """
        Stops the dashboard component and its service.

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        """
        self.logger.debug('testbed.stop_dashboard()')
        deployments = self.get_deployments(app=app, component=component)
        for deployment in deployments:
            self.delete_deployment(deployment)
        services = self.get_services(app=app, component=component)
        for service in services:
            self.delete_service(service)
    def stop_maintaining(self, experiment='', configuration=''):
        """
        Stops all maintaining components (jobs and their pods) in the cluster.
        Can be limited to a specific experiment or dbms configuration.

        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        # all jobs of configuration - benchmarker
        app = self.appname
        component = 'maintaining'
        jobs = self.get_jobs(app, component, experiment, configuration)
        # status per job
        for job in jobs:
            success = self.get_job_status(job)
            self.logger.debug("Job and status {} {}".format(job, success))
            self.delete_job(job)
        # all pods to these jobs - automatically stopped?
        #self.get_job_pods(app, component, experiment, configuration)
        pods = self.get_job_pods(app, component, experiment, configuration)
        for p in pods:
            status = self.get_pod_status(p)
            print(p, status)
            #if status == "Running":
            self.delete_pod(p)
    def stop_loading(self, experiment='', configuration=''):
        """
        Stops all loading components (jobs and their pods) in the cluster.
        Can be limited to a specific experiment or dbms configuration.

        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        app = self.appname
        component = 'loading'
        jobs = self.get_jobs(app, component, experiment, configuration)
        # status per job
        for job in jobs:
            success = self.get_job_status(job)
            print(job, success)
            self.delete_job(job)
        # all pods to these jobs - automatically stopped?
        #self.get_job_pods(app, component, experiment, configuration)
        pods = self.get_job_pods(app, component, experiment, configuration)
        for p in pods:
            status = self.get_pod_status(p)
            print(p, status)
            #if status == "Running":
            self.delete_pod(p)
    def stop_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Stops all monitoring components (deployments and their pods) in the cluster and their service.
        Can be limited to a specific experiment or dbms configuration.

        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        deployments = self.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            self.delete_deployment(deployment)
        services = self.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            self.delete_service(service)
    def stop_sut(self, app='', component='sut', experiment='', configuration=''):
        """
        Stops all sut components (deployments and their pods, stateful sets and services) in the cluster.
        Can be limited to a specific experiment or dbms configuration.

        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        deployments = self.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            self.delete_deployment(deployment)
        services = self.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            self.delete_service(service)
        stateful_sets = self.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
        for stateful_set in stateful_sets:
            self.delete_stateful_set(stateful_set)
        if component == 'sut':
            self.stop_sut(app=app, component='worker', experiment=experiment, configuration=configuration)
            self.stop_sut(app=app, component='pool', experiment=experiment, configuration=configuration)
    def stop_benchmarker(self, experiment='', configuration=''):
        """
        Stops all benchmarking components (jobs and their pods) in the cluster.
        Can be limited to a specific experiment or dbms configuration.

        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        app = self.appname
        component = 'benchmarker'
        jobs = self.get_jobs(app, component, experiment, configuration)
        # status per job
        for job in jobs:
            success = self.get_job_status(job)
            print(job, success)
            self.delete_job(job)
        # all pods to these jobs
        self.get_job_pods(app, component, experiment, configuration)
        pods = self.get_job_pods(app, component, experiment, configuration)
        for p in pods:
            status = self.get_pod_status(p)
            print(p, status)
            self.delete_pod(p)
    def connect_dashboard(self):
        """
        Connects to the dashboard component.
        This means the output ports of the dashboard component are forwarded to localhost.
        Expect results be available under port 8050 (dashboard) and 8888 (Jupyter).
        """
        print("connect_dashboard")
        pod_dashboard = self.get_dashboard_pod_name(component='dashboard')
        if len(pod_dashboard) > 0:
            #pod_dashboard = pods_dashboard[0]
            cmd = {}
            fullcommand = 'port-forward pod/{pod} 8050:8050 8888:8888 --address 0.0.0.0'.format(pod=pod_dashboard)
            self.kubectl(fullcommand)
            #print(fullcommand)
            #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            #stdout, stderr = proc.communicate()
    def connect_master(self, experiment='', configuration=''):
        """
        Connects to the master node of a sut component.
        This means the output ports of the component are forwarded to localhost.
        Must be limited to a specific experiment or dbms configuration.

        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        print("connect_master")
        if experiment is None:
            experiment = ''
        if configuration is None:
            configuration = ''
        pods_master = self.get_services(component='sut', experiment=experiment, configuration=configuration)
        if len(pods_master) > 0:
            pod_master = pods_master[0]
            print("Connect to {}".format(pod_master))
            cmd = {}
            fullcommand = 'port-forward svc/{pod} {port} --address 0.0.0.0'.format(pod=pod_master, port=self.port)
            self.kubectl(fullcommand)
    def add_to_messagequeue(self, queue, data):
        """
        Add data to (Redis) message queue.

        :param queue: Name of the queue
        :param data: Data to be added to queue
        """
        pods_messagequeue = self.get_pods(component='messagequeue')
        if len(pods_messagequeue) > 0:
            pod_messagequeue = pods_messagequeue[0]
        else:
            pod_messagequeue = 'bexhoma-messagequeue-5ff94984ff-mv9zn'
        self.logger.debug("I am using messagequeue {}".format(pod_messagequeue))
        redisCommand = 'redis-cli rpush {redisQueue} {data} '.format(redisQueue=queue, data=data)
        self.execute_command_in_pod(command=redisCommand, pod=pod_messagequeue)
    def set_pod_counter(self, queue, value=0):
        """
        Add data to (Redis) message queue.

        :param queue: Name of the queue
        :param data: Data to be added to queue
        """
        pods_messagequeue = self.get_pods(component='messagequeue')
        if len(pods_messagequeue) > 0:
            pod_messagequeue = pods_messagequeue[0]
        else:
            pod_messagequeue = 'bexhoma-messagequeue-5ff94984ff-mv9zn'
        self.logger.debug("I am using messagequeue {}".format(pod_messagequeue))
        redisCommand = 'redis-cli set {redisQueue} {value} '.format(redisQueue=queue, value=value)
        self.execute_command_in_pod(command=redisCommand, pod=pod_messagequeue)
    def get_service_endpoints(self, service_name="bexhoma-service-monitoring-default"):
        """
        Returns a list of all endpoints of a service as a list.
        This is in particular interesting for headless services.
        It is used to find all nodes in a cluster, if monitoring of cluster is active.

        :param service_name: Name of the service
        :return: List of IPs of endpoints
        """
        #kubectl get endpoints -o jsonpath="{range .items[*]}{.metadata.name},{.subsets[*].addresses[*].ip}{'\n'}{end}"
        #service_name = "bexhoma-service-monitoring-default"
        self.logger.debug("get_service_endpoints({})".format(service_name))
        endpoints = self.kubectl("get endpoints -o jsonpath=\"{range .items[*]}{.metadata.name},{.subsets[*].addresses[*].ip}{'\\n'}{end}\"")
        try:
            endpoints_of_service = endpoints.split("\n")
            for service in endpoints_of_service:
                if service.startswith(service_name):
                    #print(service)
                    endpoints_string = service[service.find(",")+1:]
                    #print(endpoints_string)
                    endpoints_list = endpoints_string.split(" ")
                    self.logger.debug("endpoints: {}".format(endpoints_list))
                    return endpoints_list
        except Exception as e:
            print("Exception when calling get_service_endpoints: %s\n" % e)
        return []



# kubectl delete pvc,pods,services,deployments,jobs -l app=bexhoma-client



























class kubernetes(testbed):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for containing specific Kubernetes (K8s) methods.
        This class can be overloaded to define specific implementations of Kubernetes, for example AWS.

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
    def __init__(self, clusterconfig='cluster.config', experiments_configfolder='experiments/', yamlfolder='k8s/', context=None, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        """
        Construct a new 'kubernetes' object.

        :param clusterconfig: Filename of the configuration of this cluster
        :param experiments_configfolder: Folder where to find experiment files
        :param context: Name of the context to use - important for kubectl to choose the cluster
        :param code: Unique identifier of the experiments
        """
        # list of configurations (connections, docker)
        # per configuration: sut+service
        # per configuration: monitoring+service
        # per configuration: list of benchmarker
        self.code = code
        testbed.__init__(self, clusterconfig=clusterconfig, experiments_configfolder=experiments_configfolder, context=context, yamlfolder=yamlfolder, code=self.code, instance=instance, volume=volume, docker=docker, script=script, queryfile=queryfile)
        self.max_sut = None
        self.experiments = []
    def add_experiment(self, experiment):
        """
        Add an experiment to this cluster.

        :param experiment: Experiment object
        """
        self.experiments.append(experiment)
    def store_pod_description(self, pod_name, container='', number=None):
        """
        Store the describe result of a pod in a local file in the experiment result folder.
        Optionally the name of a container can be given (mandatory, if pod has multiple containers).
        If file containing pod log is already present, we do nothing (no update).

        :param pod_name: Name of the pod
        :param container: Name of the container
        """
        container = ''  # never sensitive to container
        # write pod log
        resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        if not number is None:
            if len(container) > 0:
                filename_log = "{path}/{code}/{pod}.{container}.{number}.describe".format(path=resultfolder, code=self.code, pod=pod_name, container=container, number=number)
            else:
                filename_log = "{path}/{code}/{pod}.{number}.describe".format(path=resultfolder, code=self.code, pod=pod_name, number=number)
        else:
            if len(container) > 0:
                filename_log = "{path}/{code}/{pod}.{container}.describe".format(path=resultfolder, code=self.code, pod=pod_name, container=container)
            else:
                filename_log = "{path}/{code}/{pod}.describe".format(path=resultfolder, code=self.code, pod=pod_name)
        # do not overwrite
        if not os.path.isfile(filename_log):
            # max 10 tries to receive the describe (timeout might occure)
            tries = 1
            while tries<10:
                stdout = self.pod_description(pod_name, container)
                if len(stdout) > 0:
                    f = open(filename_log, "w")
                    f.write(stdout)
                    f.close()
                    return
                else:
                    tries = tries + 1
    def pod_description_exists(self, pod_name, container=''):
        """
        Returns, if describe result of pod already exists on local disk.

        :param pod_name: Name of the pod
        :param container: Name of the container
        :return: stdout of the eksctl command
        :return: does log of pod exist?
        """
        container = ''  # never sensitive to container
        # look for pod log
        if len(container) > 0:
            filename_log = "{path}/{code}/{pod}.{container}.describe".format(path=self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", ""), code=self.code, pod=pod_name, container=container)
        else:
            filename_log = "{path}/{code}/{pod}.describe".format(path=self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", ""), code=self.code, pod=pod_name)
        return os.path.isfile(filename_log)
    def store_pod_log(self, pod_name, container='', number=None):
        """
        Store the log of a pod in a local file in the experiment result folder.
        Optionally the name of a container can be given (mandatory, if pod has multiple containers).
        If file containing pod log is already present, we do nothing (no update).

        :param pod_name: Name of the pod
        :param container: Name of the container
        """
        # write pod log
        resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        if not number is None:
            if len(container) > 0:
                filename_log = "{path}/{code}/{pod}.{container}.{number}.log".format(path=resultfolder, code=self.code, pod=pod_name, container=container, number=number)
            else:
                filename_log = "{path}/{code}/{pod}.{number}.log".format(path=resultfolder, code=self.code, pod=pod_name, number=number)
        else:
            if len(container) > 0:
                filename_log = "{path}/{code}/{pod}.{container}.log".format(path=resultfolder, code=self.code, pod=pod_name, container=container)
            else:
                filename_log = "{path}/{code}/{pod}.log".format(path=resultfolder, code=self.code, pod=pod_name)
        # do not overwrite
        if not os.path.isfile(filename_log):
            # max 10 tries to receive the log (timeout might occure)
            tries = 1
            while tries<10:
                stdout = self.pod_log(pod_name, container)
                if len(stdout) > 0:
                    f = open(filename_log, "w")
                    f.write(stdout)
                    f.close()
                    return
                else:
                    tries = tries + 1
    def pod_log_exists(self, pod_name, container=''):
        """
        Returns, if log of pod already exists on local disk.

        :param pod_name: Name of the pod
        :param container: Name of the container
        :return: stdout of the eksctl command
        :return: does log of pod exist?
        """
        # look for pod log
        if len(container) > 0:
            filename_log = "{path}/{code}/{pod}.{container}.log".format(path=self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", ""), code=self.code, pod=pod_name, container=container)
        else:
            filename_log = "{path}/{code}/{pod}.log".format(path=self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", ""), code=self.code, pod=pod_name)
        return os.path.isfile(filename_log)






class aws(kubernetes):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for containing Kubernetes methods specific to AWS.
        This adds handling of nodegroups for elasticity.

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
    def __init__(self, clusterconfig='cluster.config', experiments_configfolder='experiments/', yamlfolder='k8s/', context=None, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        """
        Construct a new 'aws' kubernetes object.

        :param clusterconfig: Filename of the configuration of this cluster
        :param experiments_configfolder: Folder where to find experiment files
        :param context: Name of the context to use - important for kubectl to choose the cluster
        :param code: Unique identifier of the experiments
        """
        self.code = code
        kubernetes.__init__(self, clusterconfig=clusterconfig, experiments_configfolder=experiments_configfolder, context=context, yamlfolder=yamlfolder, code=self.code, instance=instance, volume=volume, docker=docker, script=script, queryfile=queryfile)
        self.cluster = self.context#data['cluster']
    def eksctl(self, command):
        """
        Runs an eksctl command.

        :param command: An eksctl command
        :return: stdout of the eksctl command
        """
        #fullcommand = 'eksctl --context {context} {command}'.format(context=self.context, command=command)
        fullcommand = 'eksctl {command}'.format(command=command)
        self.logger.debug('aws.eksctl({})'.format(fullcommand))
        return os.popen(fullcommand).read()# os.system(fullcommand)
    def get_nodes(self, app='', nodegroup_type='', nodegroup_name=''):
        """
        Get all nodes of a cluster.
        This overwrites the cluster method with the AWS specific nodegroup-name label. 

        :param app: Name of the pod
        :param nodegroup_type: Type of the nodegroup, e.g. sut
        :param nodegroup_name: Name of the nodegroup, e.g. sut_high_memory
        """
        self.logger.debug('aws.get_nodes()')
        label = ''
        if len(app)==0:
            app = self.appname
        label += 'app='+app
        if len(nodegroup_type)>0:
            label += ',type='+nodegroup_type
        if len(nodegroup_name)>0:
            label += ',alpha.eksctl.io/nodegroup-name='+nodegroup_name
        try:
            api_response = self.v1core.list_node(label_selector=label)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return api_response.items
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node for get_nodes: %s\n" % e)
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_nodes(app=app, nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name)
    def scale_nodegroups(self, nodegroup_names, size=None):
        print("aws.scale_nodegroups({nodegroup_names}, {size})".format(nodegroup_names=nodegroup_names, size=size))
        for nodegroup_name, size_default in nodegroup_names.items():
            if size is not None:
                size_default = size
            self.scale_nodegroup(nodegroup_name, size_default)
    def scale_nodegroup(self, nodegroup_name, size):
        print("aws.scale_nodegroup({nodegroup_name}, {size})".format(nodegroup_name=nodegroup_name, size=size))
        if not self.check_nodegroup(nodegroup_name=nodegroup_name, num_nodes_aux_planned=size):
            #fullcommand = "eksctl scale nodegroup --cluster=Test-2 --nodes=0 --nodes-min=0 --name=Kleine_Gruppe"
            command = "scale nodegroup --cluster={cluster} --nodes={size} --name={nodegroup_name}".format(cluster=self.cluster, size=size, nodegroup_name=nodegroup_name)
            return self.eksctl(command)
        #if not self.check_nodegroup(nodegroup_type, num_nodes_aux_planned):
        #    command = "scale nodegroup --cluster={cluster} --nodes={size} --name={nodegroup}".format(cluster=self.cluster, size=size, nodegroup=nodegroup)
        #    return self.eksctl(command)
        #else:
        #    return ""
    def get_nodegroup_size(self, nodegroup_type='', nodegroup_name=''):
        resp = self.get_nodes(nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name)
        num_nodes_aux_actual = len(resp)
        self.logger.debug('aws.get_nodegroup_size({},{}) = {}'.format(nodegroup_type, nodegroup_name, num_nodes_aux_actual))
        return num_nodes_aux_actual
    def check_nodegroup(self, nodegroup_type='', nodegroup_name='', num_nodes_aux_planned=0):
        num_nodes_aux_actual = self.get_nodegroup_size(nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name)
        self.logger.debug('aws.check_nodegroup({}, {}, {}) = {}'.format(nodegroup_type, nodegroup_name, num_nodes_aux_planned, num_nodes_aux_actual))
        return num_nodes_aux_planned == num_nodes_aux_actual
    def wait_for_nodegroups(self, nodegroup_names, size=None):
        print("aws.wait_for_nodegroups({nodegroup_names})".format(nodegroup_names=nodegroup_names))
        for nodegroup_name, size_default in nodegroup_names.items():
            if size is not None:
                size_default = size
            self.wait_for_nodegroup(nodegroup_name=nodegroup_name, num_nodes_aux_planned=size_default)
    def wait_for_nodegroup(self, nodegroup_type='', nodegroup_name='', num_nodes_aux_planned=0):
        while (not self.check_nodegroup(nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name, num_nodes_aux_planned=num_nodes_aux_planned)):
           self.wait(30)
        print("Nodegroup {},{} ready".format(nodegroup_type, nodegroup_name))
        return True



