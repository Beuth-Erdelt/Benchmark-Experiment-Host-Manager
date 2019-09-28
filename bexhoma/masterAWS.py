import paramiko
import sys
import boto3
from botocore.exceptions import ClientError
import time
from dbmsbenchmarker import *
import json
import logging
from timeit import default_timer #as timer
from tqdm import tqdm
import socket
from scp import SCPClient
from collections import Counter
import pprint

class testdesign():
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', code=None, instance=None, volume=None, docker=None, script=None):
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
        self.host = self.config['credentials']['AWS']['worker']['ip']
        self.port = 9091
        # AWS:
        self.ssh = None
        # experiment:
        self.setExperiments(self.config['instances'], self.config['volumes'], self.config['dockers'])
        self.setExperiment(instance, volume, docker, script)
    def setExperiments(self, instances, volumes, dockers):
        self.instance = None
        self.instances = instances
        self.volumes = volumes
        self.dockers = dockers
    def setExperiment(self, instance=None, volume=None, docker=None, script=None):
        if instance is not None:
            self.i = instance
            self.instance = self.instances[self.i]
        if volume is not None:
            self.v = volume
            self.volume = self.volumes[self.v]['id']
        if docker is not None:
            self.d = docker
            self.docker = self.dockers[self.d]
        if script is not None:
            self.s = script
            self.initscript = self.volumes[self.v]['initscripts'][self.s]
        self.connectEC2()
    def prepareExperiment(self, instance=None, volume=None, docker=None, script=None):
        self.setExperiment(instance, volume, docker, script)
        self.startInstance()
        self.wait(10)
        self.attachIP()
        self.wait(10)
        self.connectSSH()
        self.wait(10)
        self.attachVolume()
        self.wait(10)
        self.initInstance()
        self.wait(10)
        self.startMonitoring()
        self.wait(10)
        self.mountVolume()
    def startExperiment(self, instance=None, volume=None, docker=None, script=None):
        self.setExperiment(instance, volume, docker, script)
        self.connectSSH()
        self.checkGPUs()
        #self.restartDocker()
        #self.stopDocker()
        #self.removeDocker()
        self.startDocker()
        self.wait(30)
        dbmsactive = self.checkDBMS(self.host, 9091)
        while not dbmsactive:
            self.wait(10)
            dbmsactive = self.checkDBMS(self.host, 9091)
        self.loadData()
    def runExperiment(self, instance=None, volume=None, docker=None, script=None):
        self.prepareExperiment(instance, volume, docker, script)
        self.startExperiment()
        self.runBenchmarks()
        self.stopExperiment()
        self.cleanExperiment()
    def stopExperiment(self):
        self.connectSSH()
        self.stopDocker()
        self.removeDocker()
        self.cleanDocker()
    def cleanExperiment(self):
        self.unmountVolume()
        self.wait(10)
        self.detachVolume()
        self.wait(10)
        self.stopInstance()
        self.wait(10)
    def stopAllExperiments(self):
        self.connectEC2()
        for self.i, self.instance in self.instances.items():
            status, state = self.getInstanceStatus()
            if status == "ok" and state == "running":
                self.attachIP()
                self.connectSSH()
                self.stopDocker()
                self.removeDocker()
                for self.v, self.volume in self.volumes.items():
                    self.unmountVolume()
                    self.detachVolume()
                self.stopInstance()
    def wait(self, sec):
        print("Waiting "+str(sec)+"s")
        intervals = int(sec)
        intervalLength = 1
        for i in tqdm(range(intervals)):
            time.sleep(intervalLength)
    def printResponse(self, response):
        logging.debug(json.dumps(response, indent=4, sort_keys=True))
    def connectSSH(self):
        print("connectSSH: "+self.host)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.config['credentials']['AWS']['worker']['username'], key_filename=self.config['credentials']['AWS']['worker']['ppk'])
    def executeDocker(self, command):
        fullcommand = 'docker exec -i benchmark bash -c "{command}"'.format(command=command)
        stdin, stdout, stderr = self.executeSSH(fullcommand)
        return stdin, stdout, stderr
    def executeSSH(self, command):
        print("executeSSH: "+command)
        if self.ssh is None:
            self.connectSSH()
        stdin, stdout, stderr = self.ssh.exec_command(command)
        outlines=stdout.readlines()
        if len(outlines) > 0 and len(''.join(outlines)) > 0:
            print("Out: ")
            print(''.join(outlines))
        errlines=stderr.readlines()
        if len(errlines) > 0 and len(''.join(errlines)) > 0:
            print("Err: ")
            print(''.join(errlines))
        return stdin, ''.join(outlines), ''.join(errlines)
    def closeSSH(self):
        self.ssh.close()
    def connectEC2(self):
        self.ec2client = boto3.client('ec2')
        self.ec2resource = boto3.resource('ec2')
    def getInstanceStatus(self):
        print("getInstanceStatus")
        responseStatus = self.ec2client.describe_instance_status(InstanceIds=[self.instance['id']])
        self.printResponse(responseStatus)
        if len(responseStatus['InstanceStatuses']) > 0:
            status = responseStatus['InstanceStatuses'][0]['InstanceStatus']['Status']
            state = responseStatus['InstanceStatuses'][0]['InstanceState']['Name']
        else:
            status = ""
            state = ""
        if len(state) > 0 or len(status) > 0:
            print(status, state)
        return status, state
    def startInstance(self):
        print("startInstance: "+self.instance['id'])
        status, state = self.getInstanceStatus()
        if status == "ok" and state == "running":
            return
        response = "nothing"
        # Do a dryrun first to verify permissions
        try:
            self.ec2client.start_instances(InstanceIds=[self.instance['id']], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        # Dry run succeeded, run start_instances without dryrun
        try:
            response = self.ec2client.start_instances(InstanceIds=[self.instance['id']], DryRun=False)
            self.printResponse(response)
            status, state = self.getInstanceStatus()
            #print(status)
            while not(status == "ok" and state == "running"):
                status, state = self.getInstanceStatus()
                #print(status)
                time.sleep(5)
        except ClientError as e:
            print(e)
        finally:
            return response
    def stopInstance(self):
        response = "nothing"
        # Do a dryrun first to verify permissions
        try:
            self.ec2client.stop_instances(InstanceIds=[self.instance['id']], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        # Dry run succeeded, run start_instances without dryrun
        try:
            response = self.ec2client.stop_instances(InstanceIds=[self.instance['id']], DryRun=False)
            self.printResponse(response)
            status, state = self.getInstanceStatus()
            while status != "":
                status = self.getInstanceStatus()
                #print(status)
                time.sleep(5)
        except ClientError as e:
            print(e)
        finally:
            return response
    def attachIP(self):
        allocip = self.config['credentials']['AWS']['worker']['allocid']
        print("attachIP: "+self.host)
        response = "nothing"
        # Do a dryrun first to verify permissions
        try:
            self.ec2client.associate_address(AllocationId=allocip,InstanceId=self.instance['id'], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        # Dry run succeeded, run start_instances without dryrun
        try:
            response = self.ec2client.associate_address(AllocationId=allocip,InstanceId=self.instance['id'], DryRun=False)
            self.printResponse(response)
        except ClientError as e:
            print(e)
        finally:
            return response
    def getVolumeStatus(self):
        print("getVolumeStatus")
        self.ec2volume = self.ec2resource.Volume(self.volume)
        self.ec2volume.reload()
        if len(self.ec2volume.attachments) > 0:
            print(self.ec2volume.attachments)
            return self.ec2volume.attachments[0]['State']
        else:
            return ""
    def attachVolume(self):
        print("attachVolume")
        status = self.getVolumeStatus()
        while len(status) > 0:
            print(status)
            if status == "attached" and len(self.ec2volume.attachments) > 0 and self.ec2volume.attachments[0]['InstanceId'] == self.instance['id']:
                return
            status = self.getVolumeStatus()
            if status != "detaching":
                self.detachVolume()
            time.sleep(10)
        response = "nothing"
        # Do a dryrun first to verify permissions
        try:
            self.ec2volume.attach_to_instance(Device='/dev/'+self.instance['device'], InstanceId=self.instance['id'], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        # Dry run succeeded, run start_instances without dryrun
        try:
            response = self.ec2volume.attach_to_instance(Device='/dev/'+self.instance['device'], InstanceId=self.instance['id'], DryRun=False)
            self.printResponse(response)
            status = self.getVolumeStatus()
            while status != 'attached':
                print(status)
                status = self.getVolumeStatus()
                time.sleep(10)
        except ClientError as e:
            print(e)
        finally:
            return response
    def detachVolume(self):
        print("detachVolume")
        status = self.getVolumeStatus()
        if status != 'attached':
            return
        response = "nothing"
        # Do a dryrun first to verify permissions
        try:
            self.ec2volume.detach_from_instance(Device='/dev/'+self.instance['device'], InstanceId=self.ec2volume.attachments[0]['InstanceId'], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        # Dry run succeeded, run start_instances without dryrun
        try:
            response = self.ec2volume.detach_from_instance(Device='/dev/'+self.instance['device'], InstanceId=self.ec2volume.attachments[0]['InstanceId'], DryRun=False)
            self.printResponse(response)
            status = self.getVolumeStatus()
            while len(status) > 0:
                print(status)
                status = self.getVolumeStatus()
                time.sleep(10)
        except ClientError as e:
            print(e)
        finally:
            return response
    def initInstance(self):
        print("initInstance")
        # init instance
        cmd = {}
        cmd['aws_configure'] = "aws configure <<STDIN\n"+self.config['credentials']['AWS']['AWS_Access_Key_ID']+"\n"+self.config['credentials']['AWS']['AWS_Secret_Access_Key']+"\n"+self.config['credentials']['AWS']['Default_region']+"\n\nSTDIN\n"
        cmd['get_login_ecr'] = 'aws ecr get-login --region '+self.config['credentials']['AWS']['Default_region']+' --no-include-email > login.sh'
        # bash
        cmd['make_mountpoint'] = 'sudo mkdir -p /data'
        self.connectSSH()
        self.executeSSH(cmd['aws_configure'])
        self.executeSSH(cmd['get_login_ecr'])
        self.executeSSH(cmd['make_mountpoint'])
    def startMonitoring(self):
        print("startMonitoring")
        cmd = {}
        cmd['start_monitoring_dcgm'] = 'docker run --runtime=nvidia --name gpu_monitor_dcgm --rm -d --publish 8000:8000 673132930689.dkr.ecr.eu-central-1.amazonaws.com/perdelt/dcgm:latest'
        cmd['start_monitoring_nvlink'] = 'docker run --runtime=nvidia --name gpu_monitor_nvlink --rm -d --publish 8001:8001 673132930689.dkr.ecr.eu-central-1.amazonaws.com/perdelt/nvlink:latest'
        cmd['start_monitoring_node'] = 'docker run --name cpu_monitor_prom --rm -d --publish 9100:9100 prom/node-exporter:latest'
        if self.instance['GPU'] is not None and len(self.instance['GPU']) > 0:
            self.executeSSH(cmd['start_monitoring_dcgm'])
            self.executeSSH(cmd['start_monitoring_nvlink'])
        self.executeSSH(cmd['start_monitoring_node'])
    def getMountDevice(self):
        print("getMountDevice")
        cmd = {}
        command = "lsblk | awk 'END{print $1}'"
        cmd['mount_device'] = command
        stdin, stdout, stderr = self.executeSSH(cmd['mount_device'])
        return stdout.replace("\n","")
    def mountVolume(self):
        print("mountVolume")
        #device=self.getMountDevice()
        #print(device)
        if 'deviceMount' in self.instance:
            device = self.instance['deviceMount']
        else:
            device = self.instance['device']
        cmd = {}
        cmd['mount_volume'] = 'sudo mount /dev/'+device+' /data'
        stdin, stdout, stderr = self.executeSSH(cmd['mount_volume'])
    def unmountVolume(self):
        print("unmountVolume")
        #if 'deviceMount' in self.instance:
        #    device = self.instance['deviceMount']
        #else:
        #    device = self.instance['device']
        cmd = {}
        #cmd['unmount_volume'] = 'sudo umount /dev/'+device
        cmd['unmount_volume'] = 'sudo umount /data'
        stdin, stdout, stderr = self.executeSSH(cmd['unmount_volume'])
    def unparkExperiment(self, connection=None):
        print("unparkExperiment")
        self.removeDocker()
        if connection is None:
            connection = 'benchmark-'+self.getConnectionName()
        cmd = {}
        cmd['rename_docker_container'] = "docker rename "+connection+" benchmark"
        stdin, stdout, stderr = self.executeSSH(cmd['rename_docker_container'])
        self.restartDocker()
    def parkExperiment(self):
        print("parkExperiment")
        self.stopDocker()
        cmd = {}
        cmd['remove_docker_container'] = 'docker rm benchmark-'+self.getConnectionName()
        stdin, stdout, stderr = self.executeSSH(cmd['remove_docker_container'])
        cmd['rename_docker_container'] = "docker rename benchmark benchmark-"+self.getConnectionName()
        stdin, stdout, stderr = self.executeSSH(cmd['rename_docker_container'])
    def listDocker(self):
        print("listDocker")
        cmd = {}
        cmd['list_docker_container'] = "docker ps -a --format '{{.Names}}' | awk '{print $1}'"
        stdin, stdout, stderr = self.executeSSH(cmd['list_docker_container'])
        benchmarks = []
        l=stdout.split('\n')
        for i in l:
           if 'benchmark' in i:
             benchmarks.append(i)
        return benchmarks
    def restartDocker(self):
        print("restartDocker")
        cmd = {}
        cmd['start_docker_container'] = 'docker restart benchmark'
        stdin, stdout, stderr = self.executeSSH(cmd['start_docker_container'])
    def cleanDocker(self):
        print("cleanDocker")
        cmd = {}
        # remove docker volumes
        cmd['clean_docker_volumes'] = 'docker volume rm $(docker volume ls -qf dangling=true)'
        stdin, stdout, stderr = self.executeSSH(cmd['clean_docker_volumes'])
        cmd['clean_docker_all'] = 'docker system prune -f'
        stdin, stdout, stderr = self.executeSSH(cmd['clean_docker_all'])
    def startDocker(self):
        print("startDocker")
        cmd = {}
        cmd['do_login_ecr'] = 'bash login.sh'
        cmd['get_docker_image'] = 'docker pull '+self.docker['image']
        cmd['start_docker_container'] = self.docker['start']#+self.docker['image']
        if len(self.instance['RAM']) > 0:
            cmd['start_docker_container'] += '--shm-size=\''+self.instance['RAM']+'\' --memory=\''+self.instance['RAM']+'\' --memory-swap=\''+self.instance['RAM']+'\' '
        cmd['start_docker_container'] += self.docker['image']
        self.connectSSH()
        self.executeSSH(cmd['do_login_ecr'])
        self.executeSSH(cmd['get_docker_image'])
        self.executeSSH(cmd['start_docker_container'])
    def checkDBMS(self, ip=None, port=None):
        if ip is None:
            ip = self.host
        if port is None:
            port = self.port
        found = False
        s = socket.socket()
        s.settimeout(10)
        try:
            s.connect((ip, port))
            found = True
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
        self.connectSSH()
        cmd = {}
        cmd['prepare_init'] = 'mkdir -p /data/'+self.configfolder+'/'+self.d
        stdin, stdout, stderr = self.executeSSH(cmd['prepare_init'])
        scriptfolder = '/data/{experiment}/{docker}'.format(experiment=self.configfolder, docker=self.d)
        scp = SCPClient(self.ssh.get_transport())
        for script in self.initscript:
            scp.put(self.configfolder+'/'+self.d+'/'+script, scriptfolder+'/'+script)
        scp.close()
    def loadData(self):
        self.prepareInit()
        print("loadData")
        self.timeLoadingStart = default_timer()
        cmd = {}
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        for script in self.initscript:
            cmd['load_docker_data'] = self.docker['loadData'].format(scriptname=scriptfolder+script)
            stdin, stdout, stderr = self.executeDocker(cmd['load_docker_data'])
        self.timeLoadingEnd = default_timer()
        self.timeLoading = self.timeLoadingEnd - self.timeLoadingStart
    def stopDocker(self):
        print("stopDocker")
        cmd = {}
        cmd['stop_docker_container'] = 'docker stop benchmark'
        stdin, stdout, stderr = self.executeSSH(cmd['stop_docker_container'])
    def removeDocker(self):
        print("removeDocker")
        cmd = {}
        cmd['stop_docker_container'] = 'docker rm benchmark'
        stdin, stdout, stderr = self.executeSSH(cmd['stop_docker_container'])
    def checkGPUs(self):
        print("checkGPUs")
        cmd = {}
        cmd['check_gpus'] = 'nvidia-smi'
        stdin, stdout, stderr = self.executeSSH(cmd['check_gpus'])
    def getMemory(self):
        print("getMemory")
        cmd = {}
        command = "docker exec -i benchmark bash -c \"grep MemTotal /proc/meminfo\" | awk '{print $2}'"
        cmd['check_mem'] = command
        stdin, stdout, stderr = self.executeSSH(cmd['check_mem'])
        mem = int(stdout)*1024#/1024/1024/1024
        return mem
    def getCPU(self):
        print("getCPU")
        cmd = {}
        command = 'cat /proc/cpuinfo | grep \'model name\' | head -n 1'
        cmd['check_cpu'] = command
        stdin, stdout, stderr = self.executeDocker(cmd['check_cpu'])
        cpu = stdout.replace('model name\t', 'CPU').replace('\n','')
        return cpu
    def getCores(self):
        print("getCores")
        cmd = {}
        command = 'grep -c ^processor /proc/cpuinfo'
        cmd['check_cores'] = command
        stdin, stdout, stderr = self.executeDocker(cmd['check_cores'])
        #cpu = stdout.replace('model name\t', 'CPU')
        return int(stdout)
    def getHostsystem(self):
        print("getHostsystem")
        cmd = {}
        command = 'uname -r'
        cmd['host_system'] = command
        stdin, stdout, stderr = self.executeSSH(cmd['host_system'])
        return stdout.replace('_', '\\_').replace('\n','')
    def getDiskSpaceUsed(self):
        print("getDiskSpaceUsed")
        cmd = {}
        command = "df / | awk 'NR == 2{print $3}'"
        cmd['disk_space_used'] = command
        stdin, stdout, stderr = self.executeSSH(cmd['disk_space_used'])
        return int(stdout.replace('\n',''))
    def getDiskSpaceUsedData(self):
        print("getDiskSpaceUsedData")
        cmd = {}
        if 'datadir' in self.docker:
            datadir = self.docker['datadir']
            #datadir = '/var/lib/mysql'
        else:
            return ""
        command = "docker exec -i benchmark bash -c 'du "+datadir+"' | awk 'END{ FS=OFS=\"\t\" }END{print $1}'"
        #command = "du -h "+datadir+" | awk 'END{print $1}'"
        cmd['disk_space_used'] = command
        stdin, stdout, stderr = self.executeSSH(cmd['disk_space_used'])
        return int(stdout.replace('\n',''))
    def getGPUs(self):
        print("getGPUs")
        cmd = {}
        command = 'nvidia-smi -L'
        cmd['gpu_types'] = command
        stdin, stdout, stderr = self.executeDocker(cmd['gpu_types'])
        l = stdout.split("\n")
        c = Counter([x[x.find(":")+2:x.find("(")-1] for x in l if len(x)>0])
        result = ""
        for i,j in c.items():
            result += str(j)+" x "+i
        return result
    def getCUDA(self):
        print("getCUDA")
        cmd = {}
        command = 'nvidia-smi | grep \'CUDA\''
        cmd['gpu_driver'] = command
        stdin, stdout, stderr = self.executeDocker(cmd['gpu_driver'])
        return stdout.replace('|', '').replace('\n','').strip()
    def getConnectionName(self):
        return self.d+"-"+self.s+"-"+self.i+'-AWS'
    def runBenchmarks(self, connection=None, code=None, info='', resultfolder='', configfolder='', numClients=1, runsPerConnection=1):
        if self.ssh is None:
            self.connectSSH()
        if len(resultfolder) == 0:
            resultfolder = self.config['benchmarker']['resultfolder']
        if len(configfolder) == 0:
            configfolder = self.configfolder
        if connection is None:
            connection = self.getConnectionName() #self.d+"-"+self.s+"-"+self.i+'-AWS'
            #connection = self.s+"-"+self.i+'-AWS'
        if code is None:
            code = self.code
        self.configfolder = configfolder
        print("runBenchmarks")
        if len(info) == 0:
            info = str(self.s)
        mem = self.getMemory()
        cpu = self.getCPU()
        cores = self.getCores()
        host = self.getHostsystem()
        cuda = self.getCUDA()
        gpu = self.getGPUs()
        #c['info'] += " "+str(mem)+"GB RAM "+cpu
        info = []
        #info.append("loaded in {:,.2f}ms ".format(1000.0*self.timeLoading))
        #info.append("RAM: "+str(mem)+" GB")
        #info.append(cpu)
        #info.append('Host System: '+host)
        #if len(cuda):
        #    info.append('CUDA: '+cuda)
        #info.append('Instance type: '+self.instance['type'])
        #info = "loaded in {:,.2f}ms ".format(1000.0*self.timeLoading)+info
        self.connection = connection
        c = self.docker['template'].copy()
        c['active'] = True
        c['name'] = connection
        c['info'] = info
        c['timeLoad'] = self.timeLoading
        c['priceperhourdollar'] = self.instance['priceperhourdollar'] + self.docker['priceperhourdollar']
        c['hostsystem'] = {}
        c['hostsystem']['RAM'] = mem
        c['hostsystem']['CPU'] = cpu
        c['hostsystem']['GPU'] = gpu
        c['hostsystem']['Cores'] = cores
        c['hostsystem']['host'] = host
        c['hostsystem']['disk'] = self.getDiskSpaceUsed()
        c['hostsystem']['datadisk'] = self.getDiskSpaceUsedData()
        c['hostsystem']['instance'] = self.instance['type']
        if len(cuda) > 0:
            c['hostsystem']['CUDA'] = cuda
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = self.connectionmanagement['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = self.connectionmanagement['runsPerConnection']
        c['connectionmanagement']['timeout'] = self.connectionmanagement['timeout']
        c['monitoring'] = {}
        if 'monitor' in self.config['credentials']['AWS']:
            c['monitoring']['grafanatoken'] = self.config['credentials']['AWS']['monitor']['grafanatoken']
            c['monitoring']['grafanaurl'] = self.config['credentials']['AWS']['monitor']['grafanaurl']
            c['monitoring']['grafanaextend'] = 1
        c['JDBC']['url'] = c['JDBC']['url'].format(serverip=self.host, dbname=self.v)
        print(c['JDBC']['url'])
        if code is not None:
            resultfolder += '/'+str(code)
        self.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            result_path=resultfolder,
            batch=True,
            working='connection'
            )
        #if self.configqueries is not None:
        #    self.benchmark.getConfig(connectionfile=configfolder+'/connections.config', queryfile=configfolder+"/"+self.configqueries)
        #else:
        self.benchmark.getConfig(configfolder=configfolder)
        if c['name'] in self.benchmark.dbms:
            print("Rerun connection "+connection)
        else:
            self.benchmark.connections.append(c)
        self.benchmark.dbms[c['name']] = tools.dbms(c, False)
        # we must know all jars upfront
        tools.dbms.jars = [d['template']['JDBC']['jar'] for c,d in self.config['dockers'].items()]
        filename = self.benchmark.path+'/connections.config'
        with open(filename, 'w') as f:
            #f.write(str(self.benchmark.connections))
            pprint.pprint(self.benchmark.connections, f)
        self.benchmark.reporter.append(benchmarker.reporter.pickler(self.benchmark))
        self.benchmark.reporter.append(benchmarker.reporter.dataframer(self.benchmark))
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
        return self.code
    def copyLog(self):
        print("copyLog")
        if len(self.docker['logfile']):
            self.connectSSH()
            cmd = {}
            cmd['prepare_log'] = 'mkdir -p /data/'+str(self.code)
            stdin, stdout, stderr = self.executeDocker(cmd['prepare_log'])
            cmd['save_log'] = 'cp '+self.docker['logfile']+' /data/'+str(self.code)+'/'+self.connection+'.log'
            stdin, stdout, stderr = self.executeDocker(cmd['save_log'])
    def copyInits(self):
        print("copyInits")
        cmd = {}
        cmd['prepare_log'] = 'mkdir -p /data/'+str(self.code)
        stdin, stdout, stderr = self.executeSSH(cmd['prepare_log'])
        i = 0
        scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.configfolder, docker=self.d)
        for script in self.initscript:
            cmd['copy_init_scripts'] = 'cp {scriptname} /data/{code}/{connection}_init_{nr}.log'.format(scriptname=scriptfolder+script, code=self.code, connection=self.connection, nr=i)
            #cmd['copy_init_scripts'] = 'docker exec -i benchmark bash -c "cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log"'
            stdin, stdout, stderr = self.executeSSH(cmd['copy_init_scripts'])
            i = i + 1
    def downloadLog(self):
        print("downloadLog")
        self.connectSSH()
        scp = SCPClient(self.ssh.get_transport())
        scp.get(local_path=self.config['benchmarker']['resultfolder'], recursive=True, remote_path='/data/'+str(self.code))
        scp.close()


