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

from dbmsbenchmarker import *

class testdesign():
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', yamlfolder='k8s/', code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        self.experiments = []
        self.benchmark = None
        kubernetes.config.load_kube_config()
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
        self.host = 'localhost'
        self.port = self.config['credentials']['k8s']['port']
        self.monitoring_active = True
        # k8s:
        self.namespace = self.config['credentials']['k8s']['namespace']
        self.appname = self.config['credentials']['k8s']['appname']
        self.yamlfolder = yamlfolder
        self.v1core = client.CoreV1Api()
        self.v1beta = kubernetes.client.ExtensionsV1beta1Api()
        self.v1apps = kubernetes.client.AppsV1Api()
        # experiment:
        self.setExperiments(self.config['instances'], self.config['volumes'], self.config['dockers'])
        self.setExperiment(instance, volume, docker, script)
        self.setCode(code)
    def set_workload(self, **kwargs):
        self.workload = kwargs
    def set_connectionmanagement(self, **kwargs):
        self.connectionmanagement = kwargs
    def set_querymanagement(self, **kwargs):
        self.querymanagement = kwargs
    def set_resources(self, **kwargs):
        self.resources = kwargs
    def set_ddl_parameters(self, **kwargs):
        self.ddl_parameters = kwargs
    def set_code(self, code):
        return self.setCode(code)
    def setCode(self, code):
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
    def logExperiment(self, experiment):
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
    def setExperiments(self, instances=None, volumes=None, dockers=None):
        self.instance = None
        self.instances = instances
        self.volumes = volumes
        self.dockers = dockers
    def set_experiment(self, instance=None, volume=None, docker=None, script=None):
        return self.setExperiment(instance, volume, docker, script)
    def setExperiment(self, instance=None, volume=None, docker=None, script=None):
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
    def prepareExperiment(self, instance=None, volume=None, docker=None, script=None, delay=0):
        self.setExperiment(instance, volume, docker, script)
        # check if is terminated
        self.createDeployment()
        self.getInfo()
        status = self.getPodStatus(self.activepod)
        while status != "Running":
            print(status)
            self.wait(10)
            status = self.getPodStatus(self.activepod)
        self.startPortforwarding()
        self.getChildProcesses()
        # store experiment
        experiment = {}
        experiment['delay'] = delay
        experiment['step'] = "prepareExperiment"
        experiment['docker'] = {self.d: self.docker.copy()}
        experiment['volume'] = self.v
        experiment['initscript'] = {self.s: self.initscript.copy()}
        experiment['instance'] = self.i
        self.logExperiment(experiment)
        if delay > 0:
            self.delay(delay)
    def startExperiment(self, instance=None, volume=None, docker=None, script=None, delay=0):
        self.setExperiment(instance, volume, docker, script)
        self.getInfo()
        status = self.getPodStatus(self.activepod)
        while status != "Running":
            print(status)
            self.wait(10)
            status = self.getPodStatus(self.activepod)
        dbmsactive = self.checkDBMS(self.host, self.port)
        while not dbmsactive:
            self.startPortforwarding()
            self.wait(10)
            dbmsactive = self.checkDBMS(self.host, self.port)
        self.wait(10)
        self.loadData()
        # store experiment
        experiment = {}
        experiment['delay'] = delay
        experiment['step'] = "startExperiment"
        experiment['docker'] = {self.d: self.docker.copy()}
        experiment['volume'] = self.v
        experiment['initscript'] = {self.s: self.initscript.copy()}
        experiment['instance'] = self.i
        self.logExperiment(experiment)
        if delay > 0:
            self.delay(delay)
    def stopExperiment(self, delay=0):
        self.getInfo()
        self.stopPortforwarding()
        #for p in self.pods:
        #    self.deletePod(p)
        experiment = {}
        experiment['delay'] = delay
        experiment['step'] = "stopExperiment"
        self.logExperiment(experiment)
        if delay > 0:
            self.delay(delay)
    def cleanExperiment(self, delay=0):
        self.getInfo()
        self.stopPortforwarding()
        for p in self.pvcs:
            self.deletePVC(p)
        for s in self.services:
            self.deleteService(s)
        for d in self.deployments:
            self.deleteDeployment(d)
        for p in self.pods:
            status = self.getPodStatus(p)
            while status != "":
                print(status)
                self.wait(5)
                status = self.getPodStatus(p)
        experiment = {}
        experiment['delay'] = delay
        experiment['step'] = "cleanExperiment"
        self.logExperiment(experiment)
        if delay > 0:
            self.delay(delay)
    def runExperiment(self, instance=None, volume=None, docker=None, script=None, delay=0):
        self.prepareExperiment(instance, volume, docker, script, delay)
        self.startExperiment(delay=delay)
        self.runBenchmarks()
        self.stopExperiment()
        self.cleanExperiment()
    def wait(self, sec):
        print("Waiting "+str(sec)+"s")
        intervals = int(sec)
        intervalLength = 1
        for i in tqdm(range(intervals)):
            time.sleep(intervalLength)
    def delay(self, sec):
        self.wait(sec)
    def generateDeployment(self):
        print("generateDeployment")
        instance = self.i
        template = "deploymenttemplate-"+self.d+".yml"
        specs = instance.split("-")
        print(specs)
        cpu = specs[0]
        mem = specs[1]
        node = ''
        gpu = ''
        if len(specs) > 2:
            gpu = specs[2]
            node= specs[3]
        with open(self.yamlfolder+template) as stream:
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
            if dep['kind'] == 'Deployment':
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
                #    req_cpu = self.resources['requests']['cpu']
                #if 'requests' in self.resources and 'memory' in self.resources['requests']:
                #    req_mem = self.resources['requests']['memory']
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
                    dep['spec']['template']['spec']['nodeSelector']['gpu'] = node_gpu
                    dep['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = int(req_gpu)
                # add resource cpu
                #if node_cpu:
                if not 'nodeSelector' in dep['spec']['template']['spec']:
                    dep['spec']['template']['spec']['nodeSelector'] = {}
                dep['spec']['template']['spec']['nodeSelector']['cpu'] = node_cpu
                if node_cpu == '':
                    del dep['spec']['template']['spec']['nodeSelector']['cpu']
            if dep['kind'] == 'Service':
                service = dep['metadata']['name']
                #print(service)
        with open(self.yamlfolder+"deployment-"+self.d+"-"+instance+".yml","w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        return appname
    def createDeployment(self):
        self.deployment ='deployment-'+self.d+'-'+self.i+'.yml'
        #if not os.path.isfile(self.yamlfolder+self.deployment):
        self.generateDeployment()
        print("Deploy "+self.deployment)
        self.kubectl('kubectl create -f '+self.yamlfolder+self.deployment)
    def deleteDeployment(self, deployment):
        self.kubectl('kubectl delete deployment '+deployment)
    def getDeployments(self):
        try: 
            api_response = self.v1apps.list_namespaced_deployment(self.namespace, label_selector='app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling v1beta->list_namespaced_deployment: %s\n" % e)
    def getPods(self):
        try: 
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector='app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_deployment: %s\n" % e)
    def getPodStatus(self, pod):
        try:
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector='app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return api_response.items[0].status.phase
            else:
                return ""
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod_preset: %s\n" % e)
    def getServices(self):
        try: 
            api_response = self.v1core.list_namespaced_service(self.namespace, label_selector='app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)
    def getPorts(self):
        try: 
            api_response = self.v1core.list_namespaced_service(self.namespace, label_selector='app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [str(p.port) for p in api_response.items[0].spec.ports]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)
    def getPVCs(self):
        try: 
            api_response = self.v1core.list_namespaced_persistent_volume_claim(self.namespace, label_selector='app='+self.appname)
            #pprint(api_response)
            if len(api_response.items) > 0:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)
    def deletePod(self, name):
        print("deletePod")
        body = kubernetes.client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_pod(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    def deletePVC(self, name):
        print("deletePVC")
        body = kubernetes.client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_persistent_volume_claim(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: %s\n" % e)
    def deleteService(self, name):
        print("deleteService")
        body = kubernetes.client.V1DeleteOptions()
        try: 
            api_response = self.v1core.delete_namespaced_service(name, self.namespace, body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
    def startPortforwarding(self):
        print("startPortforwarding")
        ports = self.getPorts()
        #ports = {
        #    str(self.port): str(self.docker['port']),
        #    "9300": "9300",
        #    #"9400": "9400"
        #}
        #portstring = " ".join([str(k)+":"+str(v) for k,v in ports.items()])
        if len(self.deployments) > 0:
            forward = ['kubectl', 'port-forward', 'service/bexhoma-service']#, '9091', '9300']#, '9400']
            forward.extend(ports)
            #forward = ['kubectl', 'port-forward', 'service/service-dbmsbenchmarker', '9091', '9300']#, '9400']
            #forward = ['kubectl', 'port-forward', 'service/service-dbmsbenchmarker', portstring]
            #forward = ['kubectl', 'port-forward', 'deployment/'+self.deployments[0], portstring]
            your_command = " ".join(forward)
            print(your_command)
            subprocess.Popen(forward, stdout=subprocess.PIPE)
    def getChildProcesses(self):
        print("getChildProcesses")
        current_process = psutil.Process()
        children = current_process.children(recursive=False)
        for child in children:
            print('Child pid is {} {}'.format(child.pid, child.name))
            print(child.cmdline())
    def stopPortforwarding(self):
        print("stopPortforwarding")
        children = [p for p in psutil.process_iter(attrs=['pid', 'name']) if 'kubectl' in p.info['name']]
        for child in children:
            print('Child pid is {} {}'.format(child.pid, child.name))
            print(child.cmdline())
            command = child.cmdline()
            if len(command) > 0 and command[1] == 'port-forward':
                print("FOUND")
                child.terminate()
    def getInfo(self):
        self.pods = self.getPods()
        if len(self.pods) > 0:
            self.activepod = self.pods[0]
        else:
            self.activepod = None
        self.deployments = self.getDeployments()
        self.services = self.getServices()
        self.pvcs = self.getPVCs()
    def kubectl(self, command):
        print(command)
        os.system(command)
    def executeCTL(self, command):
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command.replace('"','\\"')+'"'
        print(fullcommand)
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        print(stdout.decode('utf-8'), stderr.decode('utf-8'))
        return "", stdout.decode('utf-8'), stderr.decode('utf-8')
    def checkGPUs(self):
        print("checkGPUs")
        cmd = {}
        cmd['check_gpus'] = 'nvidia-smi'
        stdin, stdout, stderr = self.executeCTL(cmd['check_gpus'])
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
    def prepareInit(self):
        print("prepareInit")
        cmd = {}
        cmd['prepare_init'] = 'mkdir -p /data/'+self.configfolder+'/'+self.d
        stdin, stdout, stderr = self.executeCTL(cmd['prepare_init'])
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
                        self.kubectl('kubectl cp --container dbms {from_name} {to_name}'.format(from_name=self.configfolder+'/'+filename_filled, to_name=self.activepod+':'+scriptfolder+script))
        else:
            for script in self.initscript:
                filename = self.d+'/'+script
                if os.path.isfile(self.configfolder+'/'+filename):
                    self.kubectl('kubectl cp --container dbms {from_name} {to_name}'.format(from_name=self.configfolder+'/'+filename, to_name=self.activepod+':'+scriptfolder+script))
    def loadData(self):
        self.prepareInit()
        print("loadData")
        self.timeLoadingStart = default_timer()
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        shellcommand = 'sh {scriptname}'
        commands = self.initscript
        for c in commands:
            filename, file_extension = os.path.splitext(c)
            if file_extension.lower() == '.sql':
                self.executeCTL(self.docker['loadData'].format(scriptname=scriptfolder+c))
            elif file_extension.lower() == '.sh':
                self.executeCTL(shellcommand.format(scriptname=scriptfolder+c))
        self.timeLoadingEnd = default_timer()
        self.timeLoading = self.timeLoadingEnd - self.timeLoadingStart
    def getMemory(self):
        print("getMemory")
        command = "grep MemTotal /proc/meminfo | awk '{print \\$2}'"
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        result = os.popen(fullcommand).read()
        mem =  int(result.replace(" ","").replace("MemTotal:","").replace("kB",""))*1024#/1024/1024/1024
        return mem
    def getCPU(self):
        print("getCPU")
        command = 'more /proc/cpuinfo | grep \'model name\' | head -n 1'
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        cpu = os.popen(fullcommand).read()
        cpu = cpu.replace('model name\t: ', '')
        #cpu = cpu.replace('model name\t: ', 'CPU: ')
        return cpu.replace('\n','')
    def getCores(self):
        print("getCores")
        cmd = {}
        command = 'grep -c ^processor /proc/cpuinfo'
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        cores = os.popen(fullcommand).read()
        return int(cores)
    def getHostsystem(self):
        print("getHostsystem")
        cmd = {}
        command = 'uname -r'
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        host = os.popen(fullcommand).read()
        return host.replace('\n','')
    def getNode(self):
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
    def getGPUs(self):
        print("getGPUs")
        cmd = {}
        command = 'nvidia-smi -L'
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
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
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
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
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        cuda = os.popen(fullcommand).read()
        return cuda.replace('|', '').replace('\n','').strip()
    def getTimediff(self):
        print("getTimediff")
        cmd = {}
        command = 'date +"%s"'
        fullcommand = 'kubectl exec '+cluster.activepod+' --container=dbms -- bash -c "'+command+'"'
        timestamp_remote = os.popen(fullcommand).read()
        timestamp_local = os.popen(command).read()
        #print(timestamp_remote)
        #print(timestamp_local)
        return int(timestamp_remote)-int(timestamp_local)
    def getDiskSpaceUsedData(self):
        print("getDiskSpaceUsedData")
        cmd = {}
        if 'datadir' in self.docker:
            datadir = self.docker['datadir']
        else:
            return 0
        command = "du "+datadir+" | awk 'END{print \\$1}'"
        cmd['disk_space_used'] = command
        stdin, stdout, stderr = self.executeCTL(cmd['disk_space_used'])
        return int(stdout.replace('\n',''))
    def getDiskSpaceUsed(self):
        print("getDiskSpaceUsed")
        cmd = {}
        command = "df / | awk 'NR == 2{print \\$3}'"
        fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command+'"'
        disk = os.popen(fullcommand).read()
        # pipe to awk sometimes does not work
        #return int(disk.split('\t')[0])
        return int(disk.replace('\n',''))
    def getConnectionName(self):
        return self.d+"-"+self.s+"-"+self.i+'-'+self.config['credentials']['k8s']['clustername']
    def runBenchmarks(self, connection=None, code=None, info=[], resultfolder='', configfolder='', alias='', query=None):
        if len(resultfolder) == 0:
            resultfolder = self.config['benchmarker']['resultfolder']
        if len(configfolder) == 0:
            configfolder = self.configfolder
        if connection is None:
            connection = self.getConnectionName()
        if code is None:
            code = self.code
        tools.query.template = self.querymanagement
        print("runBenchmarks")
        self.getInfo()
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
        c['JDBC']['url'] = c['JDBC']['url'].format(serverip='localhost', dbname=self.v, DBNAME=self.v.upper())
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
        self.logExperiment(experiment)
        # copy deployments
        if os.path.isfile(self.yamlfolder+self.deployment):
            shutil.copy(self.yamlfolder+self.deployment, self.benchmark.path+'/'+connection+'.yml')
        # append necessary reporters
        #self.benchmark.reporter.append(benchmarker.reporter.dataframer(self.benchmark))
        #self.benchmark.reporter.append(benchmarker.reporter.pickler(self.benchmark))
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
    def continueBenchmarks(self, connection=None, query=None):
        #configfolder='experiments/gdelt'
        self.getInfo()
        self.deployment = self.getDeployments()[0]
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
        self.stopPortforwarding()
        self.startPortforwarding()
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
    def runReporting(self):
        evaluator.evaluator(self.benchmark, load=False, force=True)
        self.benchmark.generateReportsAll()
    def copyLog(self):
        print("copyLog")
        if len(self.docker['logfile']):
            cmd = {}
            cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
            stdin, stdout, stderr = self.executeCTL(cmd['prepare_log'])
            cmd['save_log'] = 'cp '+self.docker['logfile']+' /data/'+str(self.code)+'/'+self.connection+'.log'
            stdin, stdout, stderr = self.executeCTL(cmd['save_log'])
    def copyInits(self):
        print("copyInits")
        cmd = {}
        cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
        stdin, stdout, stderr = self.executeCTL(cmd['prepare_log'])
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        i = 0
        for script in self.initscript:
            cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
            stdin, stdout, stderr = self.executeCTL(cmd['copy_init_scripts'])
            i = i + 1
    def downloadLog(self):
        print("downloadLog")
        self.kubectl('kubectl cp --container dbms '+self.activepod+':/data/'+str(self.code)+'/ '+self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code))

