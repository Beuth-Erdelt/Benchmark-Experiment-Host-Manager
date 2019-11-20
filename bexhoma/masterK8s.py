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

from dbmsbenchmarker import *

class testdesign():
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', yamlfolder='k8s/', code=None, instance=None, volume=None, docker=None, script=None):
        kubernetes.config.load_kube_config()
        with open(clusterconfig) as f:
            configfile=f.read()
            self.config = eval(configfile)
        #self.config = config
        self.configfolder = configfolder
        self.code = code
        self.timeLoading = 0
        self.connectionmanagement = {}
        self.connectionmanagement['numProcesses'] = None
        self.connectionmanagement['runsPerConnection'] = None
        self.connectionmanagement['timeout'] = None
        self.host = 'localhost'
        self.port = self.config['credentials']['k8s']['port']
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
    def setExperiments(self, instances=None, volumes=None, dockers=None):
        self.instance = None
        self.instances = instances
        self.volumes = volumes
        self.dockers = dockers
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
    def prepareExperiment(self, instance=None, volume=None, docker=None, script=None):
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
    def startExperiment(self, instance=None, volume=None, docker=None, script=None):
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
    def stopExperiment(self):
        self.getInfo()
        self.stopPortforwarding()
        for p in self.pods:
            self.deletePod(p)
    def cleanExperiment(self):
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
    def runExperiment(self, instance=None, volume=None, docker=None, script=None):
        self.prepareExperiment(instance, volume, docker, script)
        self.startExperiment()
        self.runBenchmarks()
        self.stopExperiment()
        self.cleanExperiment()
    def wait(self, sec):
        print("Waiting "+str(sec)+"s")
        intervals = int(sec)
        intervalLength = 1
        for i in tqdm(range(intervals)):
            time.sleep(intervalLength)
    def generateDeployment(self):
        print("generateDeployment")
        instance = self.i
        template = "deploymenttemplate-"+self.d+".yml"
        specs = instance.split("-")
        print(specs)
        cpu = specs[0]
        mem = specs[1]
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
                dep['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu
                dep['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu
                dep['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem
                dep['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem
                if len(specs) > 2:
                    dep['spec']['template']['spec']['nodeSelector']['gpu'] = node
                    dep['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = int(gpu)
                    #print(dep['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'])
                    #print(dep['spec']['template']['spec']['nodeSelector']['gpu'])
                #print(dep['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'])
                #print(dep['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'])
                #print(dep['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'])
                #print(dep['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'])
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
        if not os.path.isfile(self.yamlfolder+self.deployment):
            self.generateDeployment()
        print("Deploy "+self.deployment)
        self.kubectl('kubectl create -f '+self.yamlfolder+self.deployment)
    def deleteDeployment(self, deployment):
        self.kubectl('kubectl delete deployment '+deployment)
    def getDeployments(self):
        try: 
            api_response = self.v1beta.list_namespaced_deployment(self.namespace, label_selector='app='+self.appname)
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
        if len(self.deployments) > 0:
            forward = ['kubectl', 'port-forward', 'deployment/'+self.deployments[0], str(self.port)+':'+str(self.docker['port'])]
            your_command = " ".join(forward)
            #your_command = " ".join(self.docker['portforward'])
            print(your_command) 
            subprocess.Popen(your_command, stdout=subprocess.PIPE)
    def getChildProcesses(self):
        print("getChildProcesses")
        current_process = psutil.Process()
        children = current_process.children(recursive=False)
        for child in children:
            print('Child pid is {} {}'.format(child.pid, child.name))
            print(child.cmdline())
    def stopPortforwarding(self):
        print("stopPortforwarding")
        #current_process = psutil.Process()
        #children = current_process.children(recursive=False)
        children = [p for p in psutil.process_iter(attrs=['pid', 'name']) if 'kubectl' in p.info['name']]
        for child in children:
            print('Child pid is {} {}'.format(child.pid, child.name))
            #p = psutil.Process(child.pid)
            print(child.cmdline())
            command = child.cmdline()
            #command[0] = 'kubectl'
            if command[1] == 'port-forward':#self.docker['portforward']:
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
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        print(fullcommand)
        proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            #print("OK")
            # originally, it was 
            # except Exception, e: 
            # but this syntax is not supported anymore. 
        except Exception as e:
            print("Nobody is answering yet at %s:%d" % (ip, port))
            #print("something's wrong with %s:%d. Exception is %s" % (ip, port, e))
        finally:
            s.close()
        return found
    def prepareInit(self):
        print("prepareInit")
        cmd = {}
        cmd['prepare_init'] = 'mkdir -p /data/'+self.configfolder+'/'+self.d
        stdin, stdout, stderr = self.executeCTL(cmd['prepare_init'])
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        for script in self.initscript:
            self.kubectl('kubectl cp {from_name} {to_name}'.format(from_name=self.configfolder+'/'+self.d+'/'+script, to_name=self.activepod+':'+scriptfolder+script))
            #':/data/'+str(self.code)+' '+self.config['benchmarker']['resultfolder'].replace("\\", "/")+"/"+str(self.code))
            #scp.put(, scriptfolder+script)
    def loadData(self):
        self.prepareInit()
        print("loadData")
        self.timeLoadingStart = default_timer()
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        commands = self.initscript
        for c in commands:
            self.executeCTL(self.docker['loadData'].format(scriptname=scriptfolder+c))
        self.timeLoadingEnd = default_timer()
        self.timeLoading = self.timeLoadingEnd - self.timeLoadingStart
    def getMemory(self):
        print("getMemory")
        command = "grep MemTotal /proc/meminfo | awk '{print $2}'"
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        result = os.popen(fullcommand).read()
        mem = int(result)*1024#/1024/1024/1024
        return mem
    def getCPU(self):
        print("getCPU")
        command = 'more /proc/cpuinfo | grep \'model name\' | head -n 1'
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        cpu = os.popen(fullcommand).read()
        cpu = cpu.replace('model name\t', 'CPU')
        return cpu.replace('\n','')
    def getCores(self):
        print("getCores")
        cmd = {}
        command = 'grep -c ^processor /proc/cpuinfo'
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        cores = os.popen(fullcommand).read()
        return int(cores)
    def getHostsystem(self):
        print("getHostsystem")
        cmd = {}
        command = 'uname -r'
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        host = os.popen(fullcommand).read()
        return host.replace('\n','')
    def getGPUs(self):
        print("getGPUs")
        cmd = {}
        command = 'nvidia-smi -L'
        #cmd['gpu_types'] = 'docker exec -i benchmark bash -c "'+command+'"'
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        gpus = os.popen(fullcommand).read()
        #stdin, stdout, stderr = self.executeSSH(cmd['gpu_types'])
        l = gpus.split("\n")
        c = Counter([x[x.find(":")+2:x.find("(")-1] for x in l if len(x)>0])
        result = ""
        for i,j in c.items():
            result += str(j)+" x "+i
        return result
    def getCUDA(self):
        print("getCUDA")
        cmd = {}
        command = 'nvidia-smi | grep \'CUDA\''
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        cuda = os.popen(fullcommand).read()
        return cuda.replace('|', '').replace('\n','').strip()
    def getDiskSpaceUsedData(self):
        print("getDiskSpaceUsedData")
        cmd = {}
        if 'datadir' in self.docker:
            datadir = self.docker['datadir']
            #datadir = '/var/lib/mysql'
        else:
            return ""
        command = "du "+datadir+" | awk 'END{print $1}'"
        cmd['disk_space_used'] = command
        stdin, stdout, stderr = self.executeCTL(cmd['disk_space_used'])
        return int(stdout.replace('\n',''))
    def getDiskSpaceUsed(self):
        print("getDiskSpaceUsed")
        cmd = {}
        command = "df / | awk 'NR == 2{print $3}'"
        fullcommand = 'kubectl exec '+self.activepod+' -- bash -c "'+command+'"'
        disk = os.popen(fullcommand).read()
        return int(disk.replace('\n',''))
    def getConnectionName(self):
        return self.d+"-"+self.s+"-"+self.i+'-'+self.config['credentials']['k8s']['clustername']
    def runBenchmarks(self, connection=None, code=None, info=[], resultfolder='', configfolder=''):
        if len(resultfolder) == 0:
            resultfolder = self.config['benchmarker']['resultfolder']
        if len(configfolder) == 0:
            configfolder = self.configfolder
        if connection is None:
            connection = self.getConnectionName()
        if code is None:
            code = self.code
        self.configfolder = configfolder
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
        c['active'] = True
        c['name'] = connection
        c['info'] = info
        c['timeLoad'] = self.timeLoading
        c['priceperhourdollar'] = 0.0  + self.docker['priceperhourdollar']
        c['hostsystem'] = {}
        c['hostsystem']['RAM'] = mem
        c['hostsystem']['CPU'] = cpu
        c['hostsystem']['GPU'] = gpu
        c['hostsystem']['Cores'] = cores
        c['hostsystem']['host'] = host
        c['hostsystem']['disk'] = self.getDiskSpaceUsed()
        c['hostsystem']['datadisk'] = self.getDiskSpaceUsedData()
        #c['hostsystem']['instance'] = self.instance['type']
        if len(cuda) > 0:
            c['hostsystem']['CUDA'] = cuda
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = self.connectionmanagement['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = self.connectionmanagement['runsPerConnection']
        c['connectionmanagement']['timeout'] = self.connectionmanagement['timeout']
        c['monitoring'] = {}
        if 'monitor' in self.config['credentials']['k8s']:
            c['monitoring']['grafanatoken'] = self.config['credentials']['k8s']['monitor']['grafanatoken']
            c['monitoring']['grafanaurl'] = self.config['credentials']['k8s']['monitor']['grafanaurl']
            c['monitoring']['grafanaextend'] = 1
        c['JDBC']['url'] = c['JDBC']['url'].format(serverip='localhost', dbname=self.v)
        if code is not None:
            resultfolder += '/'+str(code)
        self.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            result_path=resultfolder,
            batch=True,
            working='connection'
            )
        self.benchmark.getConfig(configfolder=configfolder)
        if c['name'] in self.benchmark.dbms:
            print("Rerun connection "+connection)
        else:
            self.benchmark.connections.append(c)
        self.benchmark.dbms[c['name']] = tools.dbms(c, False)
        # we must know all jars upfront
        tools.dbms.jars = [d['template']['JDBC']['jar'] for c,d in self.config['dockers'].items()]
        #print(tools.dbms.jars)
        filename = self.benchmark.path+'/connections.config'
        with open(filename, 'w') as f:
            f.write(str(self.benchmark.connections))
        self.benchmark.reporter.append(benchmarker.reporter.dataframer(self.benchmark))
        self.benchmark.reporter.append(benchmarker.reporter.pickler(self.benchmark))
        if code is not None:
            self.benchmark.continueBenchmarks(overwrite = True)
        else:
            self.benchmark.runBenchmarks()
        self.code = self.benchmark.code
        self.copyInits()
        self.copyLog()
        self.downloadLog()
        self.benchmark.reporter.append(benchmarker.reporter.barer(self.benchmark))
        self.benchmark.reporter.append(benchmarker.reporter.ploter(self.benchmark))
        self.benchmark.reporter.append(benchmarker.reporter.boxploter(self.benchmark))
        self.benchmark.reporter.append(benchmarker.reporter.metricer(self.benchmark))
        self.benchmark.reporter.append(benchmarker.reporter.latexer(self.benchmark, 'pagePerQuery'))
        self.benchmark.reporter.append(benchmarker.reporter.tps(self.benchmark))
        self.benchmark.generateReportsAll()
        self.downloadLog()
        return self.code
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
            #cmd['copy_init_scripts'] = 'cp {scriptname} /data/{code}/{connection}_init_{nr}.log'.format(scriptname=scriptfolder+script, code=self.code, connection=self.connection, nr=i)
            cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
            stdin, stdout, stderr = self.executeCTL(cmd['copy_init_scripts'])
            i = i + 1
    def downloadLog(self):
        print("downloadLog")
        self.kubectl('kubectl cp '+self.activepod+':/data/'+str(self.code)+' '+self.config['benchmarker']['resultfolder'].replace("\\", "/")+"/"+str(self.code))

