"""
:Date: 2022-05-01
:Version: 0.5
:Authors: Patrick Erdelt

    Class to manage experiments in a Kubernetes cluster
    Copyright (C) 2020  Patrick Erdelt

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
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import client, config
import subprocess
import os
from os import makedirs, path
import time
from timeit import default_timer
import psutil
import logging
import socket
import yaml
from tqdm import tqdm
from collections import Counter
import shutil
import json
import ast

from dbmsbenchmarker import *

class testdesign():
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', yamlfolder='k8s/', context=None, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        self.logger = logging.getLogger('bexhoma')
        if context is None:
            # use current context
            context = config.list_kube_config_contexts()[1]['name']
        self.context = context
        self.experiments = []
        self.benchmark = None
        with open(clusterconfig) as f:
            configfile=f.read()
            self.config = eval(configfile)
        self.configfolder = configfolder
        self.resultfolder = self.config['benchmarker']['resultfolder']
        self.queryfile = queryfile
        self.clusterconfig = clusterconfig
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
        self.contextdata = self.config['credentials']['k8s']['context'][self.context]
        self.host = 'localhost'
        self.port = self.contextdata['port']
        self.monitoring_active = True
        # k8s:
        self.namespace = self.contextdata['namespace']
        self.appname = self.config['credentials']['k8s']['appname']
        self.yamlfolder = yamlfolder
        # experiment:
        self.set_experiments(self.config['instances'], self.config['volumes'], self.config['dockers'])
        self.set_experiment(instance, volume, docker, script)
        self.set_code(code)
        self.cluster_access()
    def cluster_access(self):
        """
        provide access to an K8s cluster by initializing connection handlers.
        """
        self.logger.debug('testdesign.cluster_access({})'.format(self.context))
        kubernetes.config.load_kube_config(context=self.context)
        self.v1core = client.CoreV1Api(api_client=config.new_client_from_config(context=self.context))
        #self.v1beta = kubernetes.client.ExtensionsV1beta1Api(api_client=config.new_client_from_config(context=self.context))
        self.v1apps = kubernetes.client.AppsV1Api(api_client=config.new_client_from_config(context=self.context))
        self.v1batches = kubernetes.client.BatchV1Api(api_client=config.new_client_from_config(context=self.context))
    def set_code(self, code):
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
        self.queryfile = queryfile
    def set_configfolder(self, configfolder):
        self.configfolder = configfolder
    def set_workload(self, **kwargs):
        self.workload = kwargs
    def set_querymanagement(self, **kwargs):
        self.querymanagement = kwargs
    # the following can be overwritten by experiment and configuration
    def set_connectionmanagement(self, **kwargs):
        self.connectionmanagement = kwargs
    def set_resources(self, **kwargs):
        self.resources = kwargs
    def set_ddl_parameters(self, **kwargs):
        self.ddl_parameters = kwargs
    def DEPRECATED_setCode(self, code):
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
    def log_experiment(self, experiment):
        """
        Function to log current step of experiment.
        This is supposed to be written on disk for comprehension and repetition.
        This should be reworked and yield a YAML format for example.
        Moreover this should respect "new" workflows with detached parallel loaders for example.

        :param experiment: Dict that stores parameters of current experiment stept
        """
        self.logger.debug('testdesign.log_experiment()')
        # TODO: update to new structure
        experiment['clusterconfig'] = self.clusterconfig
        experiment['configfolder'] = self.configfolder
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
        self.logger.debug('testdesign.set_experiments()')
        """ Read experiment details from cluster config"""
        self.instance = None
        self.instances = instances
        self.volumes = volumes
        self.dockers = dockers
    def set_experiment(self, instance=None, volume=None, docker=None, script=None):
        self.logger.debug('testdesign.set_experiment()')
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
    def wait(self, sec):
        """
        Function for waiting some time and inform via output about this

        :param sec: Number of seconds to wait
        """
        print("Waiting {} s...".format(sec), end="", flush=True)
        intervals = int(sec)
        time.sleep(intervals)
        print("Done waiting {} s".format(sec))
        #print("Waiting "+str(sec)+"s")
        #intervals = int(sec)
        #intervalLength = 1
        #for i in tqdm(range(intervals)):
        #    time.sleep(intervalLength)
    def delay(self, sec):
        """
        Function for waiting some time and inform via output about this.
        Synonymous for wait()

        :param sec: Number of seconds to wait
        """
        self.wait(sec)
    def delete_deployment(self, deployment):
        """
        Delete a deployment given by name.

        :param deployment: Name of the deployment to be deleted.
        """
        self.logger.debug('testdesign.delete_deployment()')
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
        self.logger.debug('testdesign.get_deployments({})'.format(label))
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
        self.logger.debug('testdesign.get_pods()')
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
        self.logger.debug('get_pods label='+label)
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
        self.logger.debug('testdesign.get_stateful_sets()')
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
        self.logger.debug('testdesign.get_nodes()')
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
        self.logger.debug('testdesign.get_pod_status()')
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
    def get_pods_labels(self, app='', component='', experiment='', configuration=''):
        """
        Return all labels of pods matching a set of labels (component/ experiment/ configuration)

        :param app: app the set belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        self.logger.debug('testdesign.get_pods_labels()')
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
        self.logger.debug('testdesign.get_services()')
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
        self.logger.debug('get_services'+label)
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
        self.logger.debug('testdesign.get_ports_of_service()')
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
        self.logger.debug('testdesign.get_pvc()')
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
        self.logger.debug('testdesign.get_pvc_labels()')
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
        self.logger.debug('testdesign.get_pvc_specs()')
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
        self.logger.debug('testdesign.get_pvc_status()')
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
    def delete_stateful_set(self, name):
        """
        Delete a stateful set given by name

        :param name: name of the stateful set to be deleted
        """
        self.logger.debug('testdesign.delete_stateful_set({})'.format(name))
        body = kubernetes.client.V1DeleteOptions()
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
        self.logger.debug('testdesign.delete_pod({})'.format(name))
        body = kubernetes.client.V1DeleteOptions()
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

        :param name: name of the stateful set to be deleted
        """
        self.logger.debug('testdesign.delete_pvc({})'.format(name))
        body = kubernetes.client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_persistent_volume_claim(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.delete_pvc(name=name)
    def delete_service(self, name):
        """
        Delete a service given by name

        :param name: name of the stateful set to be deleted
        """
        self.logger.debug('testdesign.delete_service({})'.format(name))
        body = kubernetes.client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_service(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
            self.cluster_access()
            self.wait(2)
            return self.delete_service(name=name)
    def OLD_startPortforwarding(self, service='', app='', component='sut'):
        self.logger.debug('testdesign.startPortforwarding()')
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
        self.logger.debug('testdesign.getChildProcesses()')
        current_process = psutil.Process()
        children = current_process.children(recursive=False)
        #for child in children:
        #    print('Child pid is {} {}'.format(child.pid, child.name))
        #    print(child.cmdline())
    def OLD_stopPortforwarding(self):
        self.logger.debug('testdesign.stopPortforwarding()')
        children = [p for p in psutil.process_iter(attrs=['pid', 'name']) if 'kubectl' in p.info['name']]
        for child in children:
            try:
                #print('Child pid is {} {}'.format(child.pid, child.name))
                self.logger.debug('testdesign.stopPortforwarding() - Child {} {}'.format(child.pid, child.name))
                command = child.cmdline()
                #print(command)
                if len(command) > 0 and command[3] == 'port-forward':
                    self.logger.debug('testdesign.stopPortforwarding() - Found child {}'.format(child.name))
                    child.terminate()
            except Exception as e:
                print(e)
    def DEPRECATED_getInfo(self, app='', component='', experiment='', configuration=''):
        print("get_pods", app, component, experiment, configuration)
        self.pods = self.get_pods(app, component, experiment, configuration)
        print(self.pods)
        if len(self.pods) > 0:
            self.activepod = self.pods[0]
        else:
            self.activepod = None
        self.deployments = self.get_deployments(app, component, experiment, configuration)
        print(self.deployments)
        self.services = self.get_services(app, component, experiment, configuration)
        print(self.services)
        self.pvcs = self.get_pvc()
    def kubectl(self, command):
        """
        Runs an kubectl command in the current context.

        :param command: An eksctl command
        :return: stdout of the kubectl command
        """
        fullcommand = 'kubectl --context {context} {command}'.format(context=self.context, command=command)
        self.logger.debug('testdesign.kubectl({})'.format(fullcommand))
        #print(fullcommand)
        return os.popen(fullcommand).read()# os.system(fullcommand)
    def executeCTL(self, command, pod='', container='', params=''):
        """
        Runs an shell command remotely inside a container of a pod.

        :param command: A shell command
        :param pod: The name of the pod
        :param container: The name of the container in the pod
        :param params: Optional parameters, currently ignored
        :return: stdout of the shell command
        """
        if len(pod) == 0:
            pod = self.activepod
        command_clean = command.replace('"','\\"')
        if len(container) > 0:
            fullcommand = 'kubectl --context {context} exec {pod} --container={container} -- bash -c "{command}"'.format(context=self.context, pod=pod, container=container, command=command_clean)
        else:
            fullcommand = 'kubectl --context {context} exec {pod} -- bash -c "{command}"'.format(context=self.context, pod=pod, command=command_clean)
            #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command_clean+'"'
        #print(fullcommand)
        self.logger.debug('testdesign.executeCTL({})'.format(fullcommand))
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        try:
            #print(stdout.decode('utf-8'), stderr.decode('utf-8'))
            str_stdout = stdout.decode('utf-8')
            str_stderr = stderr.decode('utf-8')
            return "", str_stdout, str_stderr
        except Exception as e:
            print(e)
            print(stdout, stderr)
            return "", stdout, stderr
        return "", "", ""
    def DEPRECATED_prepareInit(self):
        print("prepareInit")
        cmd = {}
        cmd['prepare_init'] = 'mkdir -p /data/'+self.configfolder+'/'+self.d
        stdin, stdout, stderr = self.executeCTL(command=cmd['prepare_init'], container='dbms')
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        # the inits are in the result folder?
        #i = 0
        #for script in self.initscript:
        #    #cmd['copy_init_scripts'] = 'cp {scriptname} /data/{code}/{connection}_init_{nr}.log'.format(scriptname=scriptfolder+script, code=self.code, connection=self.connection, nr=i)
        #    cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
        #    stdin, stdout, stderr = self.executeCTL(cmd['copy_init_scripts'])
        #    i = i + 1
        if len(self.ddl_parameters):
            for script in self.initscript:
                filename_template = self.d+'/'+script
                if os.path.isfile(self.configfolder+'/'+filename_template):
                    with open(self.configfolder+'/'+filename_template, "r") as initscript_template:
                        data = initscript_template.read()
                        data = data.format(**self.ddl_parameters)
                        filename_filled = self.d+'/filled_'+script
                        with open(self.configfolder+'/'+filename_filled, "w") as initscript_filled:
                            initscript_filled.write(data)
                        self.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.configfolder+'/'+filename_filled, to_name=self.activepod+':'+scriptfolder+script))
        else:
            for script in self.initscript:
                filename = self.d+'/'+script
                if os.path.isfile(self.configfolder+'/'+filename):
                    self.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.configfolder+'/'+filename, to_name=self.activepod+':'+scriptfolder+script))
    def DEPRECATED_loadData(self):
        self.prepareInit()
        print("loadData")
        self.timeLoadingStart = default_timer()
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        shellcommand = 'sh {scriptname}'
        commands = self.initscript
        for c in commands:
            filename, file_extension = os.path.splitext(c)
            if file_extension.lower() == '.sql':
                self.executeCTL(self.docker['loadData'].format(scriptname=scriptfolder+c), container='dbms')
            elif file_extension.lower() == '.sh':
                self.executeCTL(shellcommand.format(scriptname=scriptfolder+c), container='dbms')
        self.timeLoadingEnd = default_timer()
        self.timeLoading = self.timeLoadingEnd - self.timeLoadingStart
    def DEPRECATED_get_host_gpus(self):
        print("checkGPUs")
        cmd = {}
        cmd['check_gpus'] = 'nvidia-smi'
        stdin, stdout, stderr = self.executeCTL(cmd['check_gpus'], container='dbms')
    def check_DBMS_connection(self, ip, port):
        """
        CHeck if DBMS is open for connections.
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
    def DEPRECATED_getMemory(self):
        print("getMemory")
        command = "grep MemTotal /proc/meminfo | awk '{print \\$2}'"
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        mem = stdout#os.popen(fullcommand).read()
        mem =  int(mem.replace(" ","").replace("MemTotal:","").replace("kB",""))*1024#/1024/1024/1024
        return mem
    def DEPRECATED_getCPU(self):
        print("getCPU")
        command = 'more /proc/cpuinfo | grep \'model name\' | head -n 1'
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        cpu = stdout#os.popen(fullcommand).read()
        #cpu = os.popen(fullcommand).read()
        cpu = cpu.replace('model name\t: ', '')
        #cpu = cpu.replace('model name\t: ', 'CPU: ')
        return cpu.replace('\n','')
    def DEPRECATED_getCores(self):
        print("getCores")
        cmd = {}
        command = 'grep -c ^processor /proc/cpuinfo'
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        cores = stdout#os.popen(fullcommand).read()
        #cores = os.popen(fullcommand).read()
        return int(cores)
    def DEPRECATED_getHostsystem(self):
        print("getHostsystem")
        cmd = {}
        command = 'uname -r'
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        host = stdout#os.popen(fullcommand).read()
        #host = os.popen(fullcommand).read()
        return host.replace('\n','')
    def DEPRECATED_getNode(self):
        print("getNode")
        cmd = {}
        fullcommand = 'kubectl get pods/'+self.activepod+' -o=json'
        result = os.popen(fullcommand).read()
        datastore = json.loads(result)
        if self.appname == datastore['metadata']['labels']['app']:
            if self.deployments[0] in datastore['metadata']['name']:
                node = datastore['spec']['nodeName']
                return node
        return ""
    def DEPRECATED_getGPUs(self):
        print("getGPUs")
        cmd = {}
        command = 'nvidia-smi -L'
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        #gpus = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        gpus = stdout#os.popen(fullcommand).read()
        l = gpus.split("\n")
        c = Counter([x[x.find(":")+2:x.find("(")-1] for x in l if len(x)>0])
        result = ""
        for i,j in c.items():
            result += str(j)+" x "+i
        return result
    def DEPRECATED_getGPUIDs(self):
        print("getGPUIDs")
        cmd = {}
        command = 'nvidia-smi -L'
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        #gpus = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        gpus = stdout#os.popen(fullcommand).read()
        l = gpus.split("\n")
        result = []
        for i,gpu in enumerate(l):
            id = gpu[gpu.find('UUID: ')+6:gpu.find(')', gpu.find('UUID: '))]
            if len(id) > 0:
                result.append(id)
        return result
    def DEPRECATED_getCUDA(self):
        print("getCUDA")
        cmd = {}
        command = 'nvidia-smi | grep \'CUDA\''
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        #cuda = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        cuda = stdout#os.popen(fullcommand).read()
        return cuda.replace('|', '').replace('\n','').strip()
    def OLD__getTimediff(self):
        print("getTimediff")
        cmd = {}
        command = 'date +"%s"'
        fullcommand = 'kubectl exec '+cluster.activepod+' --container=dbms -- bash -c "'+command+'"'
        #stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        #gpus = stdout#os.popen(fullcommand).read()
        timestamp_remote = os.popen(fullcommand).read()
        timestamp_local = os.popen(command).read()
        #print(timestamp_remote)
        #print(timestamp_local)
        return int(timestamp_remote)-int(timestamp_local)
    def DEPRECATED_getDiskSpaceUsedData(self):
        print("getDiskSpaceUsedData")
        cmd = {}
        if 'datadir' in self.docker:
            datadir = self.docker['datadir']
        else:
            return 0
        command = "du "+datadir+" | awk 'END{print \\$1}'"
        cmd['disk_space_used'] = command
        stdin, stdout, stderr = self.executeCTL(cmd['disk_space_used'], container='dbms')
        return int(stdout.replace('\n',''))
    def DEPRECATED_getDiskSpaceUsed(self):
        print("getDiskSpaceUsed")
        cmd = {}
        command = "df / | awk 'NR == 2{print \\$3}'"
        #fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        #disk = os.popen(fullcommand).read()
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        disk = stdout#os.popen(fullcommand).read()
        # pipe to awk sometimes does not work
        #return int(disk.split('\t')[0])
        return int(disk.replace('\n',''))
    def DEPRECATED_getConnectionName(self):
        return self.d+"-"+self.s+"-"+self.i+'-'+self.contextdata['clustername']
    def DEPRECATED_get_connection_config(self, connection=None, alias='', dialect='', serverip='localhost', monitoring_host='localhost'):
        if connection is None:
            connection = self.getConnectionName()
        print("get_connection_config")
        #self.getInfo(component='sut')
        mem = self.getMemory()
        cpu = self.getCPU()
        cores = self.getCores()
        host = self.getHostsystem()
        cuda = self.getCUDA()
        gpu = self.getGPUs()
        info = []
        self.connection = connection
        c = self.docker['template'].copy()
        if len(alias) > 0:
            c['alias'] = alias
        if len(dialect) > 0:
            c['dialect'] = dialect
        #c['docker_alias'] = self.docker['docker_alias']
        c['active'] = True
        c['name'] = connection
        c['docker'] = self.d
        c['script'] = self.s
        c['info'] = info
        c['timeLoad'] = self.timeLoading
        c['priceperhourdollar'] = 0.0  + self.docker['priceperhourdollar']
        c['hostsystem'] = {}
        c['hostsystem']['RAM'] = mem
        c['hostsystem']['CPU'] = cpu
        c['hostsystem']['GPU'] = gpu
        c['hostsystem']['GPUIDs'] = self.getGPUIDs()
        c['hostsystem']['Cores'] = cores
        c['hostsystem']['host'] = host
        c['hostsystem']['node'] = self.getNode()
        c['hostsystem']['disk'] = self.getDiskSpaceUsed()
        c['hostsystem']['datadisk'] = self.getDiskSpaceUsedData()
        #c['hostsystem']['instance'] = self.instance['type']
        #c['hostsystem']['resources'] = self.resources
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
        if len(cuda) > 0:
            c['hostsystem']['CUDA'] = cuda
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = self.connectionmanagement['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = self.connectionmanagement['runsPerConnection']
        c['connectionmanagement']['timeout'] = self.connectionmanagement['timeout']
        c['connectionmanagement']['singleConnection'] = self.connectionmanagement['singleConnection'] if 'singleConnection' in self.connectionmanagement else False
        c['monitoring'] = {}
        if self.monitoring_active and 'monitor' in self.config['credentials']['k8s']:
            if 'grafanatoken' in self.config['credentials']['k8s']['monitor']:
                c['monitoring']['grafanatoken'] = self.config['credentials']['k8s']['monitor']['grafanatoken']
            if 'grafanaurl' in self.config['credentials']['k8s']['monitor']:
                c['monitoring']['grafanaurl'] = self.config['credentials']['k8s']['monitor']['grafanaurl']
            if 'grafanashift' in self.config['credentials']['k8s']['monitor']:
                c['monitoring']['grafanashift'] = self.config['credentials']['k8s']['monitor']['grafanashift']
            if 'grafanaextend' in self.config['credentials']['k8s']['monitor']:
                c['monitoring']['grafanaextend'] = self.config['credentials']['k8s']['monitor']['grafanaextend']
            if 'prometheus_url' in self.config['credentials']['k8s']['monitor']:
                c['monitoring']['prometheus_url'] = self.config['credentials']['k8s']['monitor']['prometheus_url']
            if 'service_monitoring' in self.config['credentials']['k8s']['monitor']:
                c['monitoring']['prometheus_url'] = self.config['credentials']['k8s']['monitor']['service_monitoring'].format(service=monitoring_host, namespace=self.contextdata['namespace'])
            #c['monitoring']['grafanaextend'] = 1
            c['monitoring']['metrics'] = {}
            if 'metrics' in self.config['credentials']['k8s']['monitor']:
                if len(c['hostsystem']['GPUIDs']) > 0:
                    gpuid = '|'.join(c['hostsystem']['GPUIDs'])
                else:
                    gpuid = ""
                node = c['hostsystem']['node']
                for metricname, metricdata in self.config['credentials']['k8s']['monitor']['metrics'].items():
                    c['monitoring']['metrics'][metricname] = metricdata.copy()
                    c['monitoring']['metrics'][metricname]['query'] = c['monitoring']['metrics'][metricname]['query'].format(host=node, gpuid=gpuid)
        c['JDBC']['url'] = c['JDBC']['url'].format(serverip=serverip, dbname=self.v, DBNAME=self.v.upper())
        return c
    def DEPRECATED_runBenchmarks(self, connection=None, code=None, info=[], resultfolder='', configfolder='', alias='', dialect='', query=None):
        if len(resultfolder) == 0:
            resultfolder = self.config['benchmarker']['resultfolder']
        if len(configfolder) == 0:
            configfolder = self.configfolder
        if connection is None:
            connection = self.getConnectionName()
        if code is None:
            code = int(self.code)
        tools.query.template = self.querymanagement
        c = self.get_connection_config(connection, alias, dialect)
        print("runBenchmarks")
        if code is not None:
            resultfolder += '/'+str(code)
        self.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            fixedQuery=query,
            result_path=resultfolder,
            batch=True,
            working='connection'
            )
        # read config for benchmarker
        connectionfile = configfolder+'/connections.config'
        if self.queryfile is not None:
            queryfile = configfolder+'/'+self.queryfile
        else:
            queryfile = configfolder+'/queries.config'
        self.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        if c['name'] in self.benchmark.dbms:
            print("Rerun connection "+connection)
        else:
            self.benchmark.connections.append(c)
        self.benchmark.dbms[c['name']] = tools.dbms(c, False)
        # DEPRECATED: we must know all jars upfront
        """
        tools.dbms.jars = []
        for c,d in self.config['dockers'].items():
            if isinstance(d['template']['JDBC']['jar'], list):
                tools.dbms.jars.extend(d['template']['JDBC']['jar'])
            else:
                tools.dbms.jars.append(d['template']['JDBC']['jar'])
        """
        # write appended connection config
        filename = self.benchmark.path+'/connections.config'
        with open(filename, 'w') as f:
            f.write(str(self.benchmark.connections))
        # write appended query config
        if len(self.workload) > 0:
            for k,v in self.workload.items():
                self.benchmark.queryconfig[k] = v
            filename = self.benchmark.path+'/queries.config'
            with open(filename, 'w') as f:
                f.write(str(self.benchmark.queryconfig))
        # store experiment
        experiment = {}
        experiment['delay'] = 0
        experiment['step'] = "runBenchmarks"
        experiment['connection'] = connection
        experiment['connectionmanagement'] = self.connectionmanagement.copy()
        self.log_experiment(experiment)
        # copy deployments
        #if os.path.isfile(self.yamlfolder+self.deployment):
        #    shutil.copy(self.yamlfolder+self.deployment, self.benchmark.path+'/'+connection+'.yml')
        # append necessary reporters
        #self.benchmark.reporter.append(benchmarker.reporter.dataframer(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.pickler(self.benchmark))
        # restart network
        #self.stopPortforwarding()
        #self.startPortforwarding()
        # run or continue benchmarking
        if code is not None:
            self.benchmark.continueBenchmarks(overwrite = True)
        else:
            self.benchmark.runBenchmarks()
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
    def OLD_continueBenchmarks(self, connection=None, query=None):
        #configfolder='experiments/gdelt'
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
    def copyLog(self):
        print("copyLog")
        if len(self.docker['logfile']):
            cmd = {}
            cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
            stdin, stdout, stderr = self.executeCTL(cmd['prepare_log'], container='dbms')
            cmd['save_log'] = 'cp '+self.docker['logfile']+' /data/'+str(self.code)+'/'+self.connection+'.log'
            stdin, stdout, stderr = self.executeCTL(cmd['save_log'], container='dbms')
    def copyInits(self):
        print("copyInits")
        cmd = {}
        cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
        stdin, stdout, stderr = self.executeCTL(cmd['prepare_log'], container='dbms')
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        i = 0
        for script in self.initscript:
            cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
            stdin, stdout, stderr = self.executeCTL(cmd['copy_init_scripts'], container='dbms')
            i = i + 1
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
    def downloadLog(self):
        print("downloadLog")
        self.kubectl('cp --container dbms '+self.activepod+':/data/'+str(self.code)+'/ '+self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code))
    def DEPRECATED_run_benchmarker_pod(self, connection=None, code=None, info=[], resultfolder='', configfolder='', alias='', dialect='', query=None, app='', component='benchmarker', experiment='', configuration='', client='1'):
        if len(resultfolder) == 0:
            resultfolder = self.config['benchmarker']['resultfolder']
        if len(configfolder) == 0:
            configfolder = self.configfolder
        if connection is None:
            connection = self.getConnectionName()
        if len(configuration) == 0:
            configuration = connection
        if code is None:
            code = self.code
        if not isinstance(client, str):
            client = str(client)
        #self.stopPortforwarding()
        # set query management for new query file
        tools.query.template = self.querymanagement
        # get connection config (sut)
        monitoring_host = self.generate_component_name(component='monitoring', configuration=configuration, experiment=self.code)
        service_name = self.generate_component_name(component='sut', configuration=configuration, experiment=self.code)
        service_namespace = self.contextdata['namespace']
        service_host = self.contextdata['service_sut'].format(service=service_name, namespace=service_namespace)
        #service_port = self.config['credentials']['k8s']['port']
        c = self.get_connection_config(connection, alias, dialect, serverip=service_host, monitoring_host=monitoring_host)#self.config['credentials']['k8s']['ip'])
        if isinstance(c['JDBC']['jar'], list):
            for i, j in enumerate(c['JDBC']['jar']):
                c['JDBC']['jar'][i] = j.replace("/home/perdelt/", "./")
        elif isinstance(c['JDBC']['jar'], str):
            c['JDBC']['jar'] = c['JDBC']['jar'].replace("/home/perdelt/", "./")
        print("run_benchmarker_pod")
        #if code is not None:
        #    resultfolder += '/'+str(int(code))
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
        print("Code", self.code)
        # read config for benchmarker
        connectionfile = configfolder+'/connections.config'
        if self.queryfile is not None:
            queryfile = configfolder+'/'+self.queryfile
        else:
            queryfile = configfolder+'/queries.config'
        self.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        if c['name'] in self.benchmark.dbms:
            print("Rerun connection "+connection)
        else:
            self.benchmark.connections.append(c)
        self.benchmark.dbms[c['name']] = tools.dbms(c, False)
        # copy or generate config folder (query and connection)
        # add connection to existing list
        # or: generate new connection list
        filename = self.benchmark.path+'/connections.config'
        with open(filename, 'w') as f:
            f.write(str(self.benchmark.connections))
        # write appended query config
        if len(self.workload) > 0:
            for k,v in self.workload.items():
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
        self.log_experiment(experiment)
        # copy deployments
        #if os.path.isfile(self.yamlfolder+self.deployment):
        #    shutil.copy(self.yamlfolder+self.deployment, self.benchmark.path+'/'+connection+'.yml')
        # create pod
        yamlfile = self.create_job(connection=connection, component=component, configuration=configuration, experiment=self.code, client=client)
        # start pod
        self.kubectl('create -f '+yamlfile)
        self.wait(10)
        pods = self.get_job_pods(component=component, configuration=configuration, experiment=self.code, client=client)
        client_pod_name = pods[0]
        status = self.get_pod_status(client_pod_name)
        print(client_pod_name, status)
        while status != "Running":
            print(client_pod_name, status)
            self.wait(10)
            status = self.get_pod_status(client_pod_name)
        # copy config to pod
        cmd = {}
        cmd['prepare_log'] = ('mkdir /results/{code}'.format(self.code)).replace('"','\\"')
        #fullcommand = 'kubectl exec '+client_pod_name+' -- bash -c "'+cmd['prepare_log'].replace('"','\\"')+'"'
        #print(fullcommand)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
        stdin, stdout, stderr = self.executeCTL(command=command, pod=self.activepod, container='dbms')
        print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        #stdin, stdout, stderr = self.executeCTL_client(cmd['prepare_log'])
        #cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=self.benchmark.path+'/queries.config')+' /results/'+str(self.code)+'/queries.config'
        #stdin, stdout, stderr = self.executeCTL_client(cmd['copy_init_scripts'])
        self.kubectl('cp '+self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/queries.config '+client_pod_name+':/results/'+str(self.code)+'/queries.config')
        #cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=self.benchmark.path+'/connections.config')+' /results/'+str(self.code)+'/connections.config'
        #stdin, stdout, stderr = self.executeCTL_client(cmd['copy_init_scripts'])
        self.kubectl('cp '+self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/connections.config '+client_pod_name+':/results/'+str(self.code)+'/connections.config')
        self.kubectl('cp '+self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/protocol.json '+client_pod_name+':/results/'+str(self.code)+'/protocol.json')
        self.wait(10)
        jobs = self.get_jobs(component=component, configuration=configuration, experiment=self.code, client=client)
        jobname = jobs[0]
        while not self.get_job_status(jobname=jobname, component=component, configuration=configuration, experiment=self.code, client=client):
            print("job running")
            self.wait(60)
        # write pod log
        stdout = self.pod_log(client_pod_name)
        #stdin, stdout, stderr = self.pod_log(client_pod_name)
        filename_log = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+client_pod_name+'.log'
        f = open(filename_log, "w")
        f.write(stdout)
        f.close()
        # delete job and pods
        self.delete_job(jobname=jobname)
        self.delete_job_pods(component=component, configuration=configuration, experiment=self.code, client=client)
        self.wait(60)
        # prepare reporting
        #self.copy_results()
        self.copyInits()
        self.copyLog()
        self.downloadLog()
        #self.benchmark.reporter.append(benchmarker.reporter.metricer(self.benchmark))
        #evaluator.evaluator(self.benchmark, load=False, force=True)
        return self.code
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
        self.logger.debug('getJobs '+label)
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
            # returns number of completed pods (!)
            #return api_response.status.succeeded
            # we want status of job (!)
            #self.logger.debug("api_response.status.succeeded = {}".format(api_response.status.succeeded))
            #self.logger.debug("api_response.status.conditions = {}".format(api_response.status.conditions))
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
        self.logger.debug('testdesign.delete_job()')
        try: 
            if len(jobname) == 0:
                jobs = self.get_jobs(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                jobname = jobs[0]
            self.logger.debug('testdesign.delete_job({})'.format(jobname))
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
        self.logger.debug('testdesign.delete_job_pods()')
        body = kubernetes.client.V1DeleteOptions()
        try: 
            if len(jobname) == 0:
                pods = self.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                if len(pods) > 0:
                    for pod in pods:
                        self.delete_job_pods(jobname=pod, app=app, component=component, experiment=experiment, configuration=configuration, client=client)
                    return
                #jobname = pods[0]
            self.logger.debug('testdesign.delete_job_pods({})'.format(jobname))
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
    def create_job(self, connection, app='', component='benchmarker', experiment='', configuration='', client='1'):
        """
        Creates a job and sets labels (component/ experiment/ configuration).
        TODO: Set ENV

        :param connection: ONLY FOR DBMSBENCHMARKER, should be ENV
        :param app: app the job belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        :param client: DEPRECATED? Is part of the template name
        """
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        #connection = configuration
        jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, client=str(client))
        self.logger.debug('testdesign.create_job({})'.format(jobname))
        #print(jobname)
        yamlfile = self.yamlfolder+"job-dbmsbenchmarker-"+code+".yml"
        job_experiment = self.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        with open(self.yamlfolder+"jobtemplate-dbmsbenchmarker.yml") as stream:
            try:
                result=yaml.safe_load_all(stream)
                result = [data for data in result]
                #print(result)
            except yaml.YAMLError as exc:
                print(exc)
        for dep in result:
            if dep['kind'] == 'Job':
                dep['metadata']['name'] = jobname
                job = dep['metadata']['name']
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = str(experiment)
                dep['metadata']['labels']['client'] = str(client)
                dep['spec']['template']['metadata']['labels']['app'] = app
                dep['spec']['template']['metadata']['labels']['component'] = component
                dep['spec']['template']['metadata']['labels']['configuration'] = configuration
                dep['spec']['template']['metadata']['labels']['experiment'] = str(experiment)
                dep['spec']['template']['metadata']['labels']['client'] = str(client)
                envs = dep['spec']['template']['spec']['containers'][0]['env']
                for i,e in enumerate(envs):
                    if e['name'] == 'DBMSBENCHMARKER_CODE':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = code
                    if e['name'] == 'DBMSBENCHMARKER_CONNECTION':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = connection
                    if e['name'] == 'DBMSBENCHMARKER_SLEEP':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = '60'
                    print(e)
        #if not path.isdir(self.path):
        #    makedirs(self.path)
        with open(job_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        return job_experiment
    def DEPRECATED_create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        #self.logger.debug('testdesign.create_monitoring()')
        name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        self.logger.debug('testdesign.create_monitoring({})'.format(name))
        return name
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
        self.logger.debug('testdesign.create_dashboard_name({})'.format(name))
        return name
    def DEPRECATED_start_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        self.logger.debug('testdesign.start_monitoring()')
        if len(app) == 0:
            app = self.appname
        if len(experiment) == 0:
            experiment = self.code
        deployment ='deploymenttemplate-bexhoma-prometheus.yml'
        #if not os.path.isfile(self.yamlfolder+self.deployment):
        name = self.create_monitoring(app, component, experiment, configuration)
        name_sut = self.create_monitoring(app, 'sut', experiment, configuration)
        deployment_experiment = self.path+'/deployment-{name}.yml'.format(name=name)
        with open(self.yamlfolder+deployment) as stream:
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
                        dep['metadata']['labels']['experiment'] = experiment
                        dep['spec']['selector'] = dep['metadata']['labels'].copy()
                    if dep['kind'] == 'Deployment':
                        deployment = dep['metadata']['name'] = name
                        dep['metadata']['labels']['app'] = app
                        dep['metadata']['labels']['component'] = component
                        dep['metadata']['labels']['configuration'] = configuration
                        dep['metadata']['labels']['experiment'] = str(experiment)
                        dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                        dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                        envs = dep['spec']['template']['spec']['containers'][0]['env']
                        for i,e in enumerate(envs):
                            if e['name'] == 'BEXHOMA_SERVICE':
                                dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = name_sut
                            if e['name'] == 'DBMSBENCHMARKER_CONFIGURATION':
                                dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = configuration
                            print(e)
            except yaml.YAMLError as exc:
                print(exc)
        with open(deployment_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        print("Deploy "+deployment)
        self.kubectl('create -f '+deployment_experiment)#self.yamlfolder+deployment)
    def start_dashboard(self, app='', component='dashboard'):
        """
        Starts the dashboard component and its service.
        Manifest is expected in 'deploymenttemplate-bexhoma-dashboard.yml'

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        """
        deployment = 'deploymenttemplate-bexhoma-dashboard.yml'
        name = self.create_dashboard_name(app, component)
        self.logger.debug('testdesign.start_dashboard({})'.format(deployment))
        self.kubectl('create -f '+self.yamlfolder+deployment)
    def stop_dashboard(self, app='', component='dashboard'):
        """
        Stops the dashboard component and its service.

        :param app: app the dashboard belongs to
        :param component: Component name, should be 'dashboard' typically
        """
        self.logger.debug('testdesign.stop_dashboard()')
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
    def DEPRECATED_evaluate_results(self, pod_dashboard=''):
        if len(pod_dashboard) == 0:
            pods = self.get_pods(component='dashboard')
            pod_dashboard = pods[0]
        # copy logs and yamls to result folder
        directory = os.fsencode(self.path)
        for file in os.listdir(directory):
             filename = os.fsdecode(file)
             if filename.endswith(".log") or filename.endswith(".yml"): 
                 self.kubectl('cp '+self.path+"/"+filename+' '+pod_dashboard+':/results/'+str(self.code)+'/'+filename)
        cmd = {}
        cmd['update_dbmsbenchmarker'] = 'git pull'.replace('"','\\"')#/'+str(self.code)
        self.executeCTL(command=cmd['update_dbmsbenchmarker'], pod=pod_dashboard)
        #fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['update_dbmsbenchmarker'].replace('"','\\"')+'"'
        #print(fullcommand)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
        cmd['merge_results'] = 'python merge.py -r /results/ -c {code}'.format(self.code)
        self.executeCTL(command=cmd['merge_results'], pod=pod_dashboard)
        #fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['merge_results'].replace('"','\\"')+'"'
        #print(fullcommand)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
        cmd['evaluate_results'] = 'python benchmark.py read -e yes -r /results/{code}'.format(self.code)
        self.executeCTL(command=cmd['evaluate_results'], pod=pod_dashboard)
        #fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['evaluate_results'].replace('"','\\"')+'"'
        #print(fullcommand)
        #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = proc.communicate()
    def connect_dashboard(self):
        """
        Connects to the dashboard component.
        This means the output ports of the dashboard component are forwarded to localhost.
        Expect results be available under port 8050 (dashboard) and 8888 (Jupyter).
        """
        print("connect_dashboard")
        pods_dashboard = self.get_pods(component='dashboard')
        if len(pods_dashboard) > 0:
            pod_dashboard = pods_dashboard[0]
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
            #print(fullcommand)
            #proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            #stdout, stderr = proc.communicate()




# kubectl delete pvc,pods,services,deployments,jobs -l app=bexhoma-client

