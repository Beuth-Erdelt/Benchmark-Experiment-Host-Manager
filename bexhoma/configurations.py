"""
    Class to managing experiments in a Kubernetes cluster
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
import time
from timeit import default_timer #as timer
import psutil
import logging
import socket
import yaml
from tqdm import tqdm
from collections import Counter
import shutil
import json
import ast
import copy
from datetime import datetime, timedelta

from dbmsbenchmarker import *
from bexhoma import masterK8s, experiments





class default():
    def __init__(self, experiment, docker=None, script=None, alias=None, numExperiments=1, clients=[1]):#, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        self.experiment = experiment
        #self.code = code
        self.docker = docker
        self.volume = self.experiment.volume
        if docker is not None:
            self.dockertemplate = copy.deepcopy(self.experiment.cluster.dockers[self.docker])
        if script is not None:
            self.script = script
            self.initscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.script]
        else:
            self.script = self.experiment.script
            self.initscript = self.experiment.cluster.volumes[self.experiment.volume]['initscripts'][self.script]
        self.alias = alias
        self.numExperiments = numExperiments
        self.clients = clients
        #if self.code is None:
        #    self.code = str(round(time.time()))
        self.appname = self.experiment.cluster.appname
        self.code = self.experiment.cluster.code
        self.set_resources(**self.experiment.resources)
        self.set_ddl_parameters(**self.experiment.ddl_parameters)
        self.set_connectionmanagement(**self.experiment.connectionmanagement)
        self.experiment.add_configuration(self)
        self.timeLoading = 0
        self.loading_started = False
        self.loading_after_time = None
        self.client = 1
        # per configuration: sut+service
        # per configuration: monitoring+service
        # per configuration: list of benchmarker
    def add_benchmark_list(self, list_clients):
        self.benchmark_list = copy.deepcopy(list_clients)
    def wait(self, sec):
        print("Waiting "+str(sec)+"s...", end="", flush=True)
        intervals = int(sec)
        time.sleep(intervals)
        print("done")
        #print("Waiting "+str(sec)+"s")
        #intervals = int(sec)
        #intervalLength = 1
        #for i in tqdm(range(intervals)):
        #    time.sleep(intervalLength)
    def delay(self, sec):
        self.wait(sec)
    def get_items(self, app='', component='', experiment='', configuration=''):
        if len(app) == 0:
            app = self.experiment.cluster.appname
        if len(experiment) == 0:
            experiment = self.experiment.code
        print("get_items", app, component, experiment, configuration)
        self.pods = self.experiment.cluster.getPods(app, component, experiment, configuration)
        print(self.pods)
        self.deployments = self.experiment.cluster.getDeployments(app, component, experiment, configuration)
        print(self.deployments)
        self.services = self.experiment.cluster.getServices(app, component, experiment, configuration)
        print(self.services)
        self.pvcs = self.experiment.cluster.getPVCs()
    def set_connectionmanagement(self, **kwargs):
        self.connectionmanagement = kwargs
    def set_resources(self, **kwargs):
        self.resources = kwargs
    def set_ddl_parameters(self, **kwargs):
        self.ddl_parameters = kwargs
    def set_experiment(self, instance=None, volume=None, docker=None, script=None):
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
    def prepare(self, instance=None, volume=None, docker=None, script=None, delay=0):
        """ Per config: Startup SUT and Monitoring """
        #self.setExperiment(instance, volume, docker, script)
        # check if is terminated
        #self.createDeployment()
        self.create_sut()
        self.get_items(component='sut')
        pods = self.experiment.cluster.getPods(component='sut')
        status = self.getPodStatus(pods[0])
        while status != "Running":
            print(status)
            self.wait(10)
            status = self.getPodStatus(pods[0])
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
        self.logExperiment(experiment)
        """
        if delay > 0:
            self.delay(delay)
    def start(self, instance=None, volume=None, docker=None, script=None, delay=0):
        """ Per config: Load Data """
        #self.setExperiment(instance, volume, docker, script)
        self.get_items(component='sut')
        self.get_items(component='sut')
        pods = self.experiment.cluster.getPods(component='sut')
        status = self.getPodStatus(pods[0])
        while status != "Running":
            print(status)
            self.wait(10)
            status = self.getPodStatus(pods[0])
        dbmsactive = self.checkDBMS(self.host, self.port)
        while not dbmsactive:
            self.startPortforwarding()
            self.wait(10)
            dbmsactive = self.checkDBMS(self.host, self.port)
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
        self.logExperiment(experiment)
        """
        if delay > 0:
            self.delay(delay)
        # end
    def sut_is_running(self):
        app = self.appname
        component = 'sut'
        configuration = self.docker
        pods = self.experiment.cluster.getPods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.getPodStatus(pod_sut)
            if status == "Running":
                return True
        return False
    def sut_is_pending(self):
        app = self.appname
        component = 'sut'
        configuration = self.docker
        pods = self.experiment.cluster.getPods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.getPodStatus(pod_sut)
            if status == "Pending":
                return True
        return False
    def start_loading(self, delay=0):
        """ Per config: Load Data """
        app = self.appname
        component = 'sut'
        configuration = self.docker
        pods = self.experiment.cluster.getPods(app, component, self.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self.experiment.cluster.getPodStatus(pod_sut)
            if status != "Running":
                return False
            #while status != "Running":
            #    print(pod_sut, status)
            #    self.wait(10)
            #    status = self.experiment.cluster.getPodStatus(pod_sut)
            services = self.experiment.cluster.getServices(app, component, self.experiment.code, configuration)
            service = services[0]
            ports = self.experiment.cluster.getPorts(app, component, self.experiment.code, configuration)
            forward = ['kubectl', 'port-forward', 'service/'+service] #bexhoma-service']#, '9091', '9300']#, '9400']
            forward.extend(ports)
            your_command = " ".join(forward)
            print(your_command)
            subprocess.Popen(forward, stdout=subprocess.PIPE)
            dbmsactive = self.checkDBMS(self.experiment.cluster.host, self.experiment.cluster.port)
            while not dbmsactive:
                self.wait(10)
                dbmsactive = self.checkDBMS(self.experiment.cluster.host, self.experiment.cluster.port)
            self.wait(10)
            print("load_data")
            self.load_data()
            self.experiment.cluster.stopPortforwarding()
            # store experiment
            """
            experiment = {}
            experiment['delay'] = delay
            experiment['step'] = "startExperiment"
            experiment['docker'] = {self.d: self.docker.copy()}
            experiment['volume'] = self.v
            experiment['initscript'] = {self.s: self.initscript.copy()}
            experiment['instance'] = self.i
            self.logExperiment(experiment)
            """
            if delay > 0:
                self.delay(delay)
            return True
        # end
    def generate_component_name(self, app='', component='', experiment='', configuration='', client=''):
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.docker
        if len(experiment) == 0:
            experiment = self.code
        if len(client) > 0:
            name = "{app}-{component}-{configuration}-{experiment}-{client}".format(app=app, component=component, configuration=configuration, experiment=experiment, client=client).lower()
        else:
            name = "{app}-{component}-{configuration}-{experiment}".format(app=app, component=component, configuration=configuration, experiment=experiment).lower()
        return name
    def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        print("create_monitoring")
        name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        #if len(app) == 0:
        #    app = self.appname
        #if len(experiment) == 0:
        #    experiment = self.code
        #name = "{app}_{component}_{configuration}_{experiment}".format(app=app, component=component, configuration=configuration, experiment=experiment)
        print(name)
        return name
    def start_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        print("start_monitoring")
        if len(app) == 0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.docker
        if len(experiment) == 0:
            experiment = self.code
        deployment ='deploymenttemplate-bexhoma-prometheus.yml'
        #if not os.path.isfile(self.yamlfolder+self.deployment):
        name = self.create_monitoring(app, component, experiment, configuration)
        name_sut = self.create_monitoring(app, 'sut', experiment, configuration)
        deployment_experiment = self.experiment.path+'/deployment-{name}.yml'.format(name=name)
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
        self.experiment.cluster.kubectl('kubectl create -f '+deployment_experiment)#self.yamlfolder+deployment)
    def stop_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.docker
        if len(experiment) == 0:
            experiment = self.code
        deployments = self.experiment.cluster.getDeployments(app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            self.experiment.cluster.deleteDeployment(deployment)
        services = self.experiment.cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            self.experiment.cluster.deleteService(service)
    def get_instance_from_resources(self):
        resources = experiments.DictToObject(self.resources)
        cpu = resources.requests.cpu
        memory = resources.requests.memory
        gpu = resources.requests.gpu
        cpu_type = resources.nodeSelector.cpu
        gpu_type = resources.nodeSelector.gpu
        instance = "{}-{}-{}-{}".format(cpu, memory, gpu, gpu_type)
        return instance
    def start_sut(self, app='', component='sut', experiment='', configuration=''):
        print("generateDeployment")
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.docker
        if len(experiment) == 0:
            experiment = self.code
        instance = self.get_instance_from_resources()#self.i
        template = "deploymenttemplate-"+self.docker+".yml"
        name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        deployments = self.experiment.cluster.getDeployments(app=app, component=component, experiment=experiment, configuration=configuration)
        if len(deployments) > 0:
            # sut is already running
            return False
        deployment_experiment = self.experiment.path+'/deployment-{name}.yml'.format(name=name)
        # resources
        specs = instance.split("-")
        #print(specs)
        cpu = specs[0]
        mem = specs[1]
        node = ''
        gpu = ''
        if len(specs) > 2:
            gpu = specs[2]
            node= specs[3]
        with open(self.experiment.cluster.yamlfolder+template) as stream:
            try:
                result=yaml.safe_load_all(stream)
                result = [data for data in result]
                #print(result)
            except yaml.YAMLError as exc:
                print(exc)
        for dep in result:
            if dep['kind'] == 'PersistentVolumeClaim':
                pvc = dep['metadata']['name']
                #print(pvc)
            if dep['kind'] == 'Service':
                dep['metadata']['name'] = name
                self.service = dep['metadata']['name']
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['spec']['selector'] = dep['metadata']['labels'].copy()
                #print(pvc)
            if dep['kind'] == 'Deployment':
                dep['metadata']['name'] = name
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                deployment = dep['metadata']['name']
                appname = dep['spec']['template']['metadata']['labels']['app']
                #print(deployment)
                #print(appname)
                # parameter from instance name
                # request = limit
                req_cpu = cpu
                limit_cpu = cpu
                req_mem = mem
                limit_mem = mem
                req_gpu = gpu
                node_cpu = ''
                node_gpu = node
                # should be overwritten by resources dict?
                #if 'requests' in self.resources and 'cpu' in self.resources['requests']:
                #   req_cpu = self.resources['requests']['cpu']
                #if 'requests' in self.resources and 'memory' in self.resources['requests']:
                #   req_mem = self.resources['requests']['memory']
                if 'limits' in self.resources and 'cpu' in self.resources['limits']:
                    limit_cpu = self.resources['limits']['cpu']
                if 'limits' in self.resources and 'memory' in self.resources['limits']:
                    limit_mem = self.resources['limits']['memory']
                #nodeSelector: {cpu: epyc-7542}
                if 'nodeSelector' in self.resources and 'cpu' in self.resources['nodeSelector']:
                    node_cpu = self.resources['nodeSelector']['cpu']
                if 'nodeSelector' in self.resources and 'gpu' in self.resources['nodeSelector']:
                    node_gpu = self.resources['nodeSelector']['gpu']
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
                #print(self.resources)
                # put resources to yaml file
                dep['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = req_cpu
                dep['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = limit_cpu
                dep['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = req_mem
                dep['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = limit_mem
                # remove limits if = 0
                if limit_cpu == 0:
                    del dep['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu']
                if limit_mem == 0:
                    del dep['spec']['template']['spec']['containers'][0]['resources']['limits']['memory']
                # add resource gpu
                #if len(specs) > 2:
                if node_gpu:
                    if not 'nodeSelector' in dep['spec']['template']['spec']:
                        dep['spec']['template']['spec']['nodeSelector'] = {}
                    if dep['spec']['template']['spec']['nodeSelector'] is None:
                        dep['spec']['template']['spec']['nodeSelector'] = {}
                    dep['spec']['template']['spec']['nodeSelector']['gpu'] = node_gpu
                    dep['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = int(req_gpu)
                # add resource cpu
                #if node_cpu:
                if not 'nodeSelector' in dep['spec']['template']['spec']:
                    dep['spec']['template']['spec']['nodeSelector'] = {}
                if dep['spec']['template']['spec']['nodeSelector'] is None:
                    dep['spec']['template']['spec']['nodeSelector'] = {}
                dep['spec']['template']['spec']['nodeSelector']['cpu'] = node_cpu
                if node_cpu == '':
                    del dep['spec']['template']['spec']['nodeSelector']['cpu']
            if dep['kind'] == 'Service':
                service = dep['metadata']['name']
                #print(service)
        #with open(self.yamlfolder+"deployment-"+self.d+"-"+instance+".yml","w+") as stream:
        with open(deployment_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        print("Deploy "+deployment_experiment)
        self.experiment.cluster.kubectl('kubectl create -f '+deployment_experiment)
        if self.experiment.monitoring_active:
            self.start_monitoring()
        return True
    def stop_sut(self, app='', component='sut', experiment='', configuration=''):
        if len(app)==0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.docker
        if len(experiment) == 0:
            experiment = self.code
        deployments = self.experiment.cluster.getDeployments(app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            self.experiment.cluster.deleteDeployment(deployment)
        services = self.experiment.cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            self.experiment.cluster.deleteService(service)
        if self.experiment.monitoring_active:
            self.stop_monitoring()
    def checkGPUs(self):
        print("checkGPUs")
        cmd = {}
        cmd['check_gpus'] = 'nvidia-smi'
        stdin, stdout, stderr = self.executeCTL(cmd['check_gpus'], self.pod_sut)
    def checkDBMS(self, ip, port):
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
    def getMemory(self):
        print("getMemory")
        command = "grep MemTotal /proc/meminfo | awk '{print $2}'"
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        result = os.popen(fullcommand).read()
        mem =  int(result.replace(" ","").replace("MemTotal:","").replace("kB",""))*1024#/1024/1024/1024
        return mem
    def getCPU(self):
        print("getCPU")
        command = 'more /proc/cpuinfo | grep \'model name\' | head -n 1'
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        cpu = os.popen(fullcommand).read()
        cpu = cpu.replace('model name\t: ', '')
        #cpu = cpu.replace('model name\t: ', 'CPU: ')
        return cpu.replace('\n','')
    def getCores(self):
        print("getCores")
        cmd = {}
        command = 'grep -c ^processor /proc/cpuinfo'
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        cores = os.popen(fullcommand).read()
        return int(cores)
    def getHostsystem(self):
        print("getHostsystem")
        cmd = {}
        command = 'uname -r'
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        host = os.popen(fullcommand).read()
        return host.replace('\n','')
    def getNode(self):
        print("getNode")
        cmd = {}
        fullcommand = 'kubectl get pods/'+self.pod_sut+' -o=json'
        result = os.popen(fullcommand).read()
        datastore = json.loads(result)
        #print(datastore)
        if self.appname == datastore['metadata']['labels']['app']:
            if self.pod_sut == datastore['metadata']['name']:
                node = datastore['spec']['nodeName']
                return node
        return ""
    def getGPUs(self):
        print("getGPUs")
        cmd = {}
        command = 'nvidia-smi -L'
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        gpus = os.popen(fullcommand).read()
        l = gpus.split("\n")
        c = Counter([x[x.find(":")+2:x.find("(")-1] for x in l if len(x)>0])
        result = ""
        for i,j in c.items():
            result += str(j)+" x "+i
        return result
    def getGPUIDs(self):
        print("getGPUIDs")
        cmd = {}
        command = 'nvidia-smi -L'
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        gpus = os.popen(fullcommand).read()
        l = gpus.split("\n")
        result = []
        for i,gpu in enumerate(l):
            id = gpu[gpu.find('UUID: ')+6:gpu.find(')', gpu.find('UUID: '))]
            if len(id) > 0:
                result.append(id)
        return result
    def getCUDA(self):
        print("getCUDA")
        cmd = {}
        command = 'nvidia-smi | grep \'CUDA\''
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        cuda = os.popen(fullcommand).read()
        return cuda.replace('|', '').replace('\n','').strip()
    def getTimediff(self):
        print("getTimediff")
        cmd = {}
        command = 'date +"%s"'
        fullcommand = 'kubectl exec '+cluster.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        timestamp_remote = os.popen(fullcommand).read()
        timestamp_local = os.popen(command).read()
        #print(timestamp_remote)
        #print(timestamp_local)
        return int(timestamp_remote)-int(timestamp_local)
    def getDiskSpaceUsedData(self):
        print("getDiskSpaceUsedData")
        cmd = {}
        if 'datadir' in self.dockertemplate:
            datadir = self.dockertemplate['datadir']
        else:
            return 0
        command = "du "+datadir+" | awk 'END{print $1}'"
        cmd['disk_space_used'] = command
        stdin, stdout, stderr = self.executeCTL(cmd['disk_space_used'], self.pod_sut)
        return int(stdout.replace('\n',''))
    def getDiskSpaceUsed(self):
        print("getDiskSpaceUsed")
        cmd = {}
        command = "df / | awk 'NR == 2{print $3}'"
        fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
        disk = os.popen(fullcommand).read()
        # pipe to awk sometimes does not work
        #return int(disk.split('\t')[0])
        return int(disk.replace('\n',''))
    #def getConnectionName(self):
    #    return self.d+"-"+self.s+"-"+self.i+'-'+config_K8s['clustername']
    def get_connection_config(self, connection, alias='', dialect='', serverip='localhost', monitoring_host='localhost'):
        #if connection is None:
        #    connection = self.getConnectionName()
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
        c = copy.deepcopy(self.dockertemplate['template'])
        if len(alias) > 0:
            c['alias'] = alias
        if len(dialect) > 0:
            c['dialect'] = dialect
        #c['docker_alias'] = self.docker['docker_alias']
        c['active'] = True
        c['name'] = connection
        c['docker'] = self.docker
        c['script'] = self.script
        c['info'] = info
        c['timeLoad'] = self.timeLoading
        c['priceperhourdollar'] = 0.0  + self.dockertemplate['priceperhourdollar']
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
        config_K8s = self.experiment.cluster.config['credentials']['k8s']
        if self.experiment.monitoring_active and 'monitor' in config_K8s:
            if 'grafanatoken' in config_K8s['monitor']:
                c['monitoring']['grafanatoken'] = config_K8s['monitor']['grafanatoken']
            if 'grafanaurl' in config_K8s['monitor']:
                c['monitoring']['grafanaurl'] = config_K8s['monitor']['grafanaurl']
            if 'grafanashift' in config_K8s['monitor']:
                c['monitoring']['grafanashift'] = config_K8s['monitor']['grafanashift']
            if 'grafanaextend' in config_K8s['monitor']:
                c['monitoring']['grafanaextend'] = config_K8s['monitor']['grafanaextend']
            if 'prometheus_url' in config_K8s['monitor']:
                c['monitoring']['prometheus_url'] = config_K8s['monitor']['prometheus_url']
            if 'service_monitoring' in config_K8s['monitor']:
                c['monitoring']['prometheus_url'] = config_K8s['monitor']['service_monitoring'].format(service=monitoring_host, namespace=config_K8s['namespace'])
            #c['monitoring']['grafanaextend'] = 1
            c['monitoring']['metrics'] = {}
            if 'metrics' in config_K8s['monitor']:
                if len(c['hostsystem']['GPUIDs']) > 0:
                    gpuid = '|'.join(c['hostsystem']['GPUIDs'])
                else:
                    gpuid = ""
                node = c['hostsystem']['node']
                for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                    c['monitoring']['metrics'][metricname] = metricdata.copy()
                    c['monitoring']['metrics'][metricname]['query'] = c['monitoring']['metrics'][metricname]['query'].format(host=node, gpuid=gpuid)
        c['JDBC']['url'] = c['JDBC']['url'].format(serverip=serverip, dbname=self.experiment.volume, DBNAME=self.experiment.volume.upper())
        #print(c)
        return c#.copy()
    def run_benchmarker_pod(self, connection=None, code=None, info=[], resultfolder='', configfolder='', alias='', dialect='', query=None, app='', component='benchmarker', experiment='', configuration='', client='1', parallelism=1):
        print("run_benchmarker_pod")
        if len(resultfolder) == 0:
            resultfolder = self.experiment.cluster.config['benchmarker']['resultfolder']
        if len(configfolder) == 0:
            configfolder = self.experiment.cluster.configfolder
        if connection is None:
            connection = self.docker#self.getConnectionName()
        if len(configuration) == 0:
            configuration = connection
        if code is None:
            code = self.code
        if not isinstance(client, str):
            client = str(client)
        self.experiment.cluster.stopPortforwarding()
        # set query management for new query file
        tools.query.template = self.experiment.querymanagement
        # get connection config (sut)
        monitoring_host = self.generate_component_name(component='monitoring', configuration=configuration, experiment=self.code)
        service_name = self.generate_component_name(component='sut', configuration=configuration, experiment=self.code)
        service_namespace = self.experiment.cluster.config['credentials']['k8s']['namespace']
        service_host = self.experiment.cluster.config['credentials']['k8s']['service_sut'].format(service=service_name, namespace=service_namespace)
        pods = self.experiment.cluster.getPods(component='sut', configuration=configuration, experiment=self.code)
        self.pod_sut = pods[0]
        #service_port = config_K8s['port']
        c = self.get_connection_config(connection, alias, dialect, serverip=service_host, monitoring_host=monitoring_host)#config_K8s['ip'])
        c['parameter'] = {}
        c['parameter']['parallelism'] = parallelism
        c['parameter']['client'] = client
        print(c)
        print(self.experiment.cluster.config['benchmarker']['jarfolder'])
        if isinstance(c['JDBC']['jar'], list):
            for i, j in enumerate(c['JDBC']['jar']):
                c['JDBC']['jar'][i] = self.experiment.cluster.config['benchmarker']['jarfolder']+c['JDBC']['jar'][i]
        elif isinstance(c['JDBC']['jar'], str):
            c['JDBC']['jar'] = self.experiment.cluster.config['benchmarker']['jarfolder']+c['JDBC']['jar']
        print(c)
        print(self.dockertemplate)
        print(self.experiment.cluster.dockers[self.docker])
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
        if self.experiment.queryfile is not None:
            queryfile = configfolder+'/'+self.experiment.queryfile
        else:
            queryfile = configfolder+'/queries.config'
        self.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        if c['name'] in self.benchmark.dbms:
            print("Rerun connection "+connection)
            # TODO: Find and replace connection info
        else:
            self.benchmark.connections.append(c)
        # NEVER rerun, only one connection in config for detached:
        self.benchmark.connections = [c]
        print(self.benchmark.connections)
        self.benchmark.dbms[c['name']] = tools.dbms(c, False)
        # copy or generate config folder (query and connection)
        # add connection to existing list
        # or: generate new connection list
        filename = self.benchmark.path+'/connections.config'
        with open(filename, 'w') as f:
            f.write(str(self.benchmark.connections))
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
        self.experiment.cluster.logExperiment(experiment)
        # copy deployments
        #if os.path.isfile(self.yamlfolder+self.deployment):
        #    shutil.copy(self.yamlfolder+self.deployment, self.benchmark.path+'/'+connection+'.yml')
        # create pod
        yamlfile = self.create_job(connection=connection, component=component, configuration=configuration, experiment=self.code, client=client, parallelism=parallelism)
        # start pod
        self.experiment.cluster.kubectl('kubectl create -f '+yamlfile)
        self.wait(10)
        pods = self.experiment.cluster.getJobPods(component=component, configuration=configuration, experiment=self.code, client=client)
        client_pod_name = pods[0]
        status = self.experiment.cluster.getPodStatus(client_pod_name)
        print(client_pod_name, status)
        while status != "Running":
            print(client_pod_name, status)
            self.wait(10)
            status = self.experiment.cluster.getPodStatus(client_pod_name)
        # copy config to pod
        cmd = {}
        cmd['prepare_log'] = 'mkdir -p /results/'+str(self.code)
        fullcommand = 'kubectl exec '+client_pod_name+' -- bash -c "'+cmd['prepare_log'].replace('"','\\"')+'"'
        print(fullcommand)
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        #stdin, stdout, stderr = self.executeCTL_client(cmd['prepare_log'])
        #cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=self.benchmark.path+'/queries.config')+' /results/'+str(self.code)+'/queries.config'
        #stdin, stdout, stderr = self.executeCTL_client(cmd['copy_init_scripts'])
        self.experiment.cluster.kubectl('kubectl cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/queries.config '+client_pod_name+':/results/'+str(self.code)+'/queries.config')
        #cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=self.benchmark.path+'/connections.config')+' /results/'+str(self.code)+'/connections.config'
        #stdin, stdout, stderr = self.executeCTL_client(cmd['copy_init_scripts'])
        self.experiment.cluster.kubectl('kubectl cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/connections.config '+client_pod_name+':/results/'+str(self.code)+'/'+c['name']+'.config')
        self.experiment.cluster.kubectl('kubectl cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/connections.config '+client_pod_name+':/results/'+str(self.code)+'/connections.config')
        self.experiment.cluster.kubectl('kubectl cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/protocol.json '+client_pod_name+':/results/'+str(self.code)+'/protocol.json')
        """
        self.wait(10)
        jobs = self.getJobs(component=component, configuration=configuration, experiment=self.code, client=client)
        jobname = jobs[0]
        while not self.getJobStatus(jobname=jobname, component=component, configuration=configuration, experiment=self.code, client=client):
            print("job running")
            self.wait(60)
        # write pod log
        stdin, stdout, stderr = self.pod_log(client_pod_name)
        filename_log = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+client_pod_name+'.log'
        f = open(filename_log, "w")
        f.write(stdout)
        f.close()
        # delete job and pods
        self.deleteJob(jobname=jobname)
        self.deleteJobPod(component=component, configuration=configuration, experiment=self.code, client=client)
        self.wait(60)
        # prepare reporting
        #self.copy_results()
        self.copyInits()
        self.copyLog()
        self.downloadLog()
        #self.benchmark.reporter.append(benchmarker.reporter.metricer(self.benchmark))
        #evaluator.evaluator(self.benchmark, load=False, force=True)
        """
    def kubectl(self, command):
        print(command)
        os.system(command)
    def executeCTL(self, command, pod):
        fullcommand = 'kubectl exec '+pod+' --container=dbms -- bash -c "'+command.replace('"','\\"')+'"'
        print(fullcommand)
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        return "", stdout.decode('utf-8'), stderr.decode('utf-8')
    def copyLog(self):
        print("copyLog")
        pods = self.experiment.cluster.getPods(component='sut', configuration=self.docker, experiment=self.code)
        self.pod_sut = pods[0]
        if len(self.dockertemplate['logfile']):
            cmd = {}
            cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
            stdin, stdout, stderr = self.executeCTL(cmd['prepare_log'], self.pod_sut)
            cmd['save_log'] = 'cp '+self.dockertemplate['logfile']+' /data/'+str(self.code)+'/'+self.docker+'.log'
            stdin, stdout, stderr = self.executeCTL(cmd['save_log'], self.pod_sut)
    def prepareInit(self):
        print("prepareInit")
        pods = self.experiment.cluster.getPods(component='sut', configuration=self.docker, experiment=self.code)
        self.pod_sut = pods[0]
        cmd = {}
        cmd['prepare_init'] = 'mkdir -p /data/'+self.experiment.cluster.configfolder+'/'+self.docker
        stdin, stdout, stderr = self.executeCTL(cmd['prepare_init'], self.pod_sut)
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiment.cluster.configfolder, docker=self.docker)
        # the inits are in the result folder?
        #i = 0
        #for script in self.initscript:
        #    #cmd['copy_init_scripts'] = 'cp {scriptname} /data/{code}/{connection}_init_{nr}.log'.format(scriptname=scriptfolder+script, code=self.code, connection=self.connection, nr=i)
        #    cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
        #    stdin, stdout, stderr = self.executeCTL(cmd['copy_init_scripts'])
        #    i = i + 1
        if len(self.ddl_parameters):
            for script in self.initscript:
                filename_template = self.docker+'/'+script
                if os.path.isfile(self.experiment.cluster.configfolder+'/'+filename_template):
                    with open(self.experiment.cluster.configfolder+'/'+filename_template, "r") as initscript_template:
                        data = initscript_template.read()
                        data = data.format(**self.ddl_parameters)
                        filename_filled = self.docker+'/filled_'+script
                        with open(self.experiment.cluster.configfolder+'/'+filename_filled, "w") as initscript_filled:
                            initscript_filled.write(data)
                        self.experiment.cluster.kubectl('kubectl cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.configfolder+'/'+filename_filled, to_name=self.pod_sut+':'+scriptfolder+script))
        else:
            for script in self.initscript:
                filename = self.docker+'/'+script
                if os.path.isfile(self.experiment.cluster.configfolder+'/'+filename):
                    self.experiment.cluster.kubectl('kubectl cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.configfolder+'/'+filename, to_name=self.pod_sut+':'+scriptfolder+script))
    def load_data(self):
        if self.loading_started:
            return
        self.loading_started = True
        self.prepareInit()
        pods = self.experiment.cluster.getPods(component='sut', configuration=self.docker, experiment=self.code)
        self.pod_sut = pods[0]
        print("load_data")
        self.timeLoadingStart = default_timer()
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiment.cluster.configfolder, docker=self.docker)
        shellcommand = 'sh {scriptname}'
        commands = self.initscript
        for c in commands:
            filename, file_extension = os.path.splitext(c)
            if file_extension.lower() == '.sql':
                stdin, stdout, stderr = self.executeCTL(self.dockertemplate['loadData'].format(scriptname=scriptfolder+c), self.pod_sut)
                filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.log'.format(configuration=self.docker, filename=filename, extension=file_extension.lower())
                print(filename_log)
                if len(stdout) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stdout)
                filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.error'.format(configuration=self.docker, filename=filename, extension=file_extension.lower())
                print(filename_log)
                if len(stderr) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stderr)
            elif file_extension.lower() == '.sh':
                stdin, stdout, stderr = self.executeCTL(shellcommand.format(scriptname=scriptfolder+c), self.pod_sut)
                filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.log'.format(configuration=self.docker, filename=filename, extension=file_extension.lower())
                print(filename_log)
                if len(stdout) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stdout)
                filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.error'.format(configuration=self.docker, filename=filename, extension=file_extension.lower())
                print(filename_log)
                if len(stderr) > 0:
                    with open(filename_log,'w') as file:
                        file.write(stderr)
        self.timeLoadingEnd = default_timer()
        self.timeLoading = self.timeLoadingEnd - self.timeLoadingStart
    def create_job(self, connection, app='', component='benchmarker', experiment='', configuration='', client='1', parallelism=1):
        print("create_job")
        if len(app) == 0:
            app = self.appname
        code = str(int(experiment))
        #connection = configuration
        jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, client=str(client))
        print(jobname)
        # determine start time
        now = datetime.utcnow()
        start = now + timedelta(seconds=180)
        #start = datetime.strptime('2021-03-04 23:15:25', '%Y-%m-%d %H:%M:%S')
        #wait = (start-now).seconds
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        #yamlfile = self.experiment.cluster.yamlfolder+"job-dbmsbenchmarker-"+code+".yml"
        job_experiment = self.experiment.path+'/job-dbmsbenchmarker-{configuration}-{client}.yml'.format(configuration=configuration, client=client)
        with open(self.experiment.cluster.yamlfolder+"jobtemplate-dbmsbenchmarker.yml") as stream:
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
                dep['spec']['completions'] = parallelism
                dep['spec']['parallelism'] = parallelism
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
                    if e['name'] == 'DBMSBENCHMARKER_CLIENT':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = str(parallelism)
                    if e['name'] == 'DBMSBENCHMARKER_CODE':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = code
                    if e['name'] == 'DBMSBENCHMARKER_CONNECTION':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = connection
                    if e['name'] == 'DBMSBENCHMARKER_SLEEP':
                        dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = '60'
                    print(e)
                e = {'name': 'DBMSBENCHMARKER_NOW', 'value': now_string}
                dep['spec']['template']['spec']['containers'][0]['env'].append(e)
                e = {'name': 'DBMSBENCHMARKER_START', 'value': start_string}
                dep['spec']['template']['spec']['containers'][0]['env'].append(e)
        #if not path.isdir(self.path):
        #    makedirs(self.path)
        with open(job_experiment,"w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        return job_experiment

# kubectl delete pvc,pods,services,deployments,jobs -l app=bexhoma-client
