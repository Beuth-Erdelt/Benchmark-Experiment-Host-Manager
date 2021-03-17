"""
:Date: 2018-08-22
:Version: 0.1
:Authors: Patrick Erdelt

Demo of TPC-DS in a K8s Cluster.

# Compare 4 DBMS on different HW
# 256 runs
# no delay
# Compare result sets
# 2x each DBMS
# MemSQL, OmniSci, MonetDB, PostgreSQL, maybe add MySQL, MariaDB, Kinetica?
# Limit 4 CPUs

This deals with the TPC-DS tests.
"""
#from bexhoma import *
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
	def __init__(self,
			cluster,
			code=None,
			numExperiments = 3,
			timeout = 7200,
			detached=False):
		self.cluster = cluster
		#self.code = self.cluster.code
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
			singleConnection = False)
		self.numExperiments = numExperiments
		self.cluster.add_experiment(self)
		self.appname = self.cluster.appname
		self.resources = {}
		self.ddl_parameters = {}
		#self.connectionmanagement = {}
		#self.connectionmanagement['numProcesses'] = None
		#self.connectionmanagement['runsPerConnection'] = None
		#self.connectionmanagement['timeout'] = None
		#self.connectionmanagement['singleConnection'] = False
		self.querymanagement = {}
		self.workload = {}
		self.monitoring_active = True
		# k8s:
		self.namespace = self.cluster.config['credentials']['k8s']['namespace']
		self.configurations = []
	def wait(self, sec):
		print("Waiting "+str(sec)+"s...", end="", flush=True)
		intervals = int(sec)
		time.sleep(intervals)
		print("done")
		#print("Waiting "+str(sec)+"s")
		#intervals = int(sec)
		#intervalLength = 1
		#for i in tqdm(range(intervals)):
		#	time.sleep(intervalLength)
	def delay(self, sec):
		self.wait(sec)
	def get_items(self, app='', component='', experiment='', configuration=''):
		if len(app) == 0:
			app = self.experiment.cluster.appname
		if len(experiment) == 0:
			experiment = self.code
		print("get_items", app, component, experiment, configuration)
		self.pods = self.cluster.getPods(app, component, experiment, configuration)
		print(self.pods)
		self.deployments = self.cluster.getDeployments(app, component, experiment, configuration)
		print(self.deployments)
		self.services = self.cluster.getServices(app, component, experiment, configuration)
		print(self.services)
		self.jobs = self.cluster.getJobs(app, component, experiment, configuration, '')
		print(self.jobs)
		self.pvcs = self.cluster.getPVCs()
	def set_queryfile(self, queryfile):
		self.queryfile = queryfile
	def set_configfolder(self, configfolder):
		self.configfolder = configfolder
	def set_workload(self, **kwargs):
		self.workload = kwargs
	def set_querymanagement(self, **kwargs):
		self.querymanagement = kwargs
	# can be overwritten by configuration
	def set_connectionmanagement(self, **kwargs):
		self.connectionmanagement = kwargs
	def set_resources(self, **kwargs):
		self.resources = kwargs
	def set_ddl_parameters(self, **kwargs):
		self.ddl_parameters = kwargs
	def add_configuration(self, configuration):
		self.configurations.append(configuration)
	def __set_queryfile(self, queryfile):
		self.cluster.set_queryfile(queryfile)
	def __set_configfolder(self, configfolder):
		self.cluster.set_configfolder(configfolder)
	def set_querymanagement_quicktest(self,
			numRun=1):
		self.set_querymanagement(
			numWarmup = 0,
			numCooldown = 0,
			numRun = numRun,
			delay = 0)
		self.monitoring_active = False
	def set_querymanagement_monitoring(self,
			numRun=256,
			delay=10):
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
					'active': False,
				}
			})
		self.monitoring_active = True
	def __set_resources(self, **kwargs):
		__self.cluster.set_resources(**kwargs)
	def __set_ddl_parameters(self, **kwargs):
		self.cluster.set_ddl_parameters(**kwargs)
	def __set_workload(self, **kwargs):
		self.cluster.set_workload(**kwargs)
	def get_instance_from_resources(self):
		resources = DictToObject(self.cluster.resources)
		cpu = resources.requests.cpu
		memory = resources.requests.memory
		gpu = resources.requests.gpu
		cpu_type = resources.nodeSelector.cpu
		gpu_type = resources.nodeSelector.gpu
		instance = "{}-{}-{}-{}".format(cpu, memory, gpu, gpu_type)
		return instance
	def run(self,
			docker,
			alias='',
			dialect='',
			instance=''):
		if self.detached:
			return self.run_benchmarker_pod(docker, alias, dialect, instance)
		self.cluster.set_experiment(docker=docker)
		if len(instance) == 0:
			instance = self.get_instance_from_resources()
		if len(alias) == 0:
			alias = self.cluster.docker['template']['alias']
		self.cluster.set_experiment(instance=instance) 
		# default: wait 60s
		delay = 60
		if 'delay_prepare' in self.cluster.docker:
			# config demands other delay
			delay = self.cluster.docker['delay_prepare']
		self.cluster.prepareExperiment(delay=delay)
		self.cluster.startExperiment(delay=60)
		for i in range(1, self.numExperiments+1):
			self.cluster.stopPortforwarding()
			self.cluster.startPortforwarding()
			connection = self.cluster.getConnectionName()
			#self.cluster.runBenchmarks(connection=connection+"-"+str(i), alias=alias+'-'+str(i))
			self.cluster.runBenchmarks(connection=self.cluster.d+"-"+str(i), alias=alias+'-'+str(i), dialect=dialect)
		self.cluster.stopExperiment()
		self.cluster.cleanExperiment()
		del gc.garbage[:]
	def run_benchmarker_pod(self,
			docker,
			alias='',
			dialect='',
			instance=''):
		if not self.detached:
			return self.run(docker, alias, dialect, instance)
		self.cluster.set_experiment(docker=docker)
		if len(instance) == 0:
			instance = self.get_instance_from_resources()
		self.cluster.set_experiment(instance=instance) 
		# default: wait 60s
		delay = 60
		if 'delay_prepare' in self.cluster.docker:
			# config demands other delay
			delay = self.cluster.docker['delay_prepare']
		self.cluster.prepareExperiment(delay=delay)
		self.cluster.startExperiment(delay=60)
		for i in range(1, self.numExperiments+1):
			connection = self.cluster.getConnectionName()
			#self.cluster.runBenchmarks(connection=connection+"-"+str(i), alias=alias+'-'+str(i))
			self.cluster.run_benchmarker_pod(connection=self.cluster.d+"-"+str(i), alias=alias+'-'+str(i), dialect=dialect)
		self.cluster.stopExperiment()
		self.cluster.cleanExperiment()
		del gc.garbage[:]
	def prepare(self,
			docker,
			alias,
			instance=''):
		self.cluster.set_experiment(docker=docker)
		if len(instance) == 0:
			instance = self.get_instance_from_resources()
		self.cluster.set_experiment(instance=instance)
		# default: wait 60s
		delay = 60
		if 'delay_prepare' in self.cluster.docker:
			# config demands other delay
			delay = self.cluster.docker['delay_prepare']
		self.cluster.prepareExperiment(delay=delay)
	def prepare_and_start(self,
			docker,
			alias,
			instance=''):
		self.cluster.set_experiment(docker=docker)
		if len(instance) == 0:
			instance = self.get_instance_from_resources()
		self.cluster.set_experiment(instance=instance)
		# default: wait 60s
		delay = 60
		if 'delay_prepare' in self.cluster.docker:
			# config demands other delay
			delay = self.cluster.docker['delay_prepare']
		self.cluster.prepareExperiment(delay=delay)
		self.cluster.startExperiment(delay=60)
	def reporting(self):
		self.cluster.runReporting()
	def clean(self):
		self.cluster.stopExperiment()
		self.cluster.cleanExperiment()
		del gc.garbage[:]
	def zip(self):
		shutil.make_archive(self.cluster.resultfolder+"/"+str(self.cluster.code), 'zip', self.cluster.resultfolder, str(self.cluster.code))
	def set_experiment(self, instance=None, volume=None, docker=None, script=None):
		""" Read experiment details from cluster config"""
		#self.bChangeInstance = True
		#if instance is not None:
		#	self.i = instance
		if volume is not None:
			self.volume = volume
			self.volumeid = self.cluster.volumes[self.volume]['id']
		#if docker is not None:
		#	self.d = docker
		#	self.docker = self.cluster.dockers[self.d]
		if script is not None:
			self.script = script
			self.initscript = self.cluster.volumes[self.volume]['initscripts'][self.script]
	def evaluate_results(self, pod_dashboard=''):
		if len(pod_dashboard) == 0:
			pods = self.cluster.getPods(component='dashboard')
			pod_dashboard = pods[0]
		# copy logs and yamls to result folder
		directory = os.fsencode(self.path)
		for file in os.listdir(directory):
			 filename = os.fsdecode(file)
			 if filename.endswith(".log") or filename.endswith(".yml"): 
				 self.cluster.kubectl('kubectl cp '+self.path+"/"+filename+' '+pod_dashboard+':/results/'+str(self.code)+'/'+filename)
		cmd = {}
		cmd['update_dbmsbenchmarker'] = 'git pull'#/'+str(self.code)
		fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['update_dbmsbenchmarker'].replace('"','\\"')+'"'
		print(fullcommand)
		proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()
		cmd['merge_results'] = 'python merge.py -r /results/ -c '+str(self.code)
		fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['merge_results'].replace('"','\\"')+'"'
		print(fullcommand)
		proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()
		cmd['evaluate_results'] = 'python benchmark.py read -e yes -r /results/'+str(self.code)
		fullcommand = 'kubectl exec '+pod_dashboard+' -- bash -c "'+cmd['evaluate_results'].replace('"','\\"')+'"'
		print(fullcommand)
		proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()
	def stop_monitoring(self):
		for config in self.configurations:
			config.stop_monitoring()
	def start_monitoring(self):
		for config in self.configurations:
			config.start_monitoring()
	def start_sut(self):
		for config in self.configurations:
			config.start_sut()
	def stop_sut(self):
		for config in self.configurations:
			config.stop_sut()
	def start_loading(self):
		for config in self.configurations:
			config.start_loading()
	def load_data(self):
		for config in self.configurations:
			config.load_data()
	def add_benchmark_list(self, list_clients):
		for config in self.configurations:
			config.add_benchmark_list(list_clients)
	def work_benchmark_list(self, intervals=30):
		do = True
		while do:
			time.sleep(intervals)
			for config in self.configurations:
				# check if sut is running
				if not config.sut_is_running():
					print("{} is not running".format(config.configuration))
					continue
				# check if loading is done
				pod_labels = self.cluster.getPodsLabels(app=app, component='sut', experiment=self.code, configuration=config.configuration)
				#print(pod_labels)
				if len(pod_labels) > 0:
					pod = next(iter(pod_labels.keys()))
					if 'loaded' in pod_labels[pod]:
						if pod_labels[pod]['loaded'] == 'True':
							config.loading_finished = True
						else:
							config.loading_finished = False
					else:
						config.loading_started = False
					if 'timeLoadingStart' in pod_labels[pod]:
						config.timeLoadingStart = pod_labels[pod]['timeLoadingStart']
					if 'timeLoadingEnd' in pod_labels[pod]:
						config.timeLoadingEnd = pod_labels[pod]['timeLoadingEnd']
					if 'timeLoading' in pod_labels[pod]:
						config.timeLoading = float(pod_labels[pod]['timeLoading'])
				else:
					config.loading_started = False
				# start loading
				if not config.loading_started:
					print("{} is not loaded".format(config.configuration))
					now = datetime.utcnow()
					if config.loading_after_time is not None:
						if now >= config.loading_after_time:
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
						print("{} will start loading but not before {}".format(config.configuration, config.loading_after_time.strftime('%Y-%m-%d %H:%M:%S')))
						continue
				# benchmark if loading is done and monitoring is ready
				if config.loading_finished:
					if config.monitoring_active and not config.monitoring_is_running():
						print("{} waits for monitoring".format(config.configuration))
						continue
					app = self.cluster.appname
					component = 'benchmarker'
					configuration = ''
					pods = self.cluster.getJobPods(app, component, self.code, configuration=config.configuration)
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
							config.run_benchmarker_pod(connection=config.configuration+'-'+client, configuration=config.configuration, client=client, parallelism=parallelism)
						else:
							# no list element left
							print("{} can be stopped".format(config.configuration))
							config.stop_sut()
				else:
					print("{} is loading".format(config.configuration))
			# all jobs of configuration - benchmarker
			app = self.cluster.appname
			component = 'benchmarker'
			configuration = ''
			jobs = self.cluster.getJobs(app, component, self.code, configuration)
			# all pods to these jobs
			pods = self.cluster.getJobPods(app, component, self.code, configuration)
			# status per pod
			for p in pods:
				status = self.cluster.getPodStatus(p)
				print(p,status)
				if status == 'Succeeded':
					#if status != 'Running':
					self.cluster.store_pod_log(p)
					self.cluster.deletePod(p)
				if status == 'Failed':
					#if status != 'Running':
					self.cluster.store_pod_log(p)
					self.cluster.deletePod(p)
			# success of job
			app = self.cluster.appname
			component = 'benchmarker'
			configuration = ''
			success = self.cluster.getJobStatus(app=app, component=component, experiment=self.code, configuration=configuration)
			jobs = self.cluster.getJobs(app, component, self.code, configuration)
			# status per job
			for job in jobs:
				success = self.cluster.getJobStatus(job)
				print(job, success)
				if success:
					self.cluster.deleteJob(job)
			if len(pods) == 0 and len(jobs) == 0:
				do = False
				for config in self.configurations:
					#if config.sut_is_pending() or config.loading_started or len(config.benchmark_list) > 0:
					if config.sut_is_pending():
						print("{} pending".format(config.configuration))
						do = True
					if not config.loading_started:
						print("{} not loaded".format(config.configuration))
						do = True
					if len(config.benchmark_list) > 0:
						print("{} still benchmarks to run".format(config.configuration))
						do = True
	def benchmark_list(self, list_clients):
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
				jobs = self.cluster.getJobs(app, component, self.code, configuration)
				# all pods to these jobs
				pods = self.cluster.getJobPods(app, component, self.code, configuration)
				# status per pod
				for p in pods:
					status = self.cluster.getPodStatus(p)
					print(p,status)
					if status == 'Succeeded':
						#if status != 'Running':
						self.cluster.store_pod_log(p)
						self.cluster.deletePod(p)
					if status == 'Failed':
						#if status != 'Running':
						self.cluster.store_pod_log(p)
						self.cluster.deletePod(p)
				# success of job
				app = self.cluster.appname
				component = 'benchmarker'
				configuration = ''
				success = self.cluster.getJobStatus(app=app, component=component, experiment=self.code, configuration=configuration)
				jobs = self.cluster.getJobs(app, component, self.code, configuration)
				# status per job
				for job in jobs:
					success = self.cluster.getJobStatus(job)
					print(job, success)
					if success:
						self.cluster.deleteJob(job)
				if len(pods) == 0 and len(jobs) == 0:
					break
	def stop_benchmarker(self):
		# all jobs of configuration - benchmarker
		app = self.appname
		component = 'benchmarker'
		configuration = ''
		jobs = self.cluster.getJobs(app, component, self.code, configuration)
		# status per job
		for job in jobs:
			success = self.cluster.getJobStatus(job)
			print(job, success)
			self.cluster.deleteJob(job)
		# all pods to these jobs
		#self.cluster.getJobPods(app, component, self.code, configuration)
		pods = self.cluster.getJobPods(app, component, self.code, configuration)
		for p in pods:
			status = self.cluster.getPodStatus(p)
			print(p, status)
			self.cluster.deletePod(p)






class tpcds(default):
	def __init__(self,
			cluster,
			code=None,
			queryfile = 'queries-tpcds.config',
			SF = '100',
			numExperiments = 3,
			timeout = 7200,
			detached=False):
		default.__init__(self, cluster, code, numExperiments, timeout, detached)
		self.set_experiment(volume='tpcds')
		self.set_experiment(script='SF'+str(SF)+'-index')
		self.cluster.set_configfolder('experiments/tpcds')
		self.set_queryfile(queryfile)
		parameter.defaultParameters = {'SF': str(SF)}
		self.set_workload(
			name = 'TPC-DS Queries SF='+str(SF),
			info = 'This experiment performs some TPC-DS inspired queries.'
			)
	def set_queries_full(self):
		self.set_queryfile('queries-tpcds.config')
	def set_queries_profiling(self):
		self.set_queryfile('queries-tpcds-profiling.config')


class tpch(default):
	def __init__(self,
			cluster,
			code=None,
			queryfile = 'queries-tpch.config',
			SF = '100',
			numExperiments = 3,
			timeout = 7200,
			detached=False):
		default.__init__(self, cluster, code, numExperiments, timeout, detached)
		self.set_experiment(volume='tpch')
		self.set_experiment(script='SF'+str(SF)+'-index')
		self.cluster.set_configfolder('experiments/tpch')
		parameter.defaultParameters = {'SF': str(SF)}
		self.set_queryfile(queryfile)
		self.set_workload(
			name = 'TPC-H Queries SF='+str(SF),
			info = 'This experiment performs some TPC-H inspired queries.'
			)
	def set_queries_full(self):
		self.set_queryfile('queries-tpch.config')
	def set_queries_profiling(self):
		self.set_queryfile('queries-tpch-profiling.config')

