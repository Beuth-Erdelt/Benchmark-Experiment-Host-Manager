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
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import client, config
import subprocess
import os
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
import copy
from datetime import datetime, timedelta

import threading

from dbmsbenchmarker import *
from bexhoma import masterK8s, experiments





class default():
	"""
	:Date: 2022-10-01
	:Version: 0.6.0
	:Authors: Patrick K. Erdelt

		Class for managing an DBMS configuation.
		This is plugged into an experiment object.

        :param experiment: Unique identifier of the experiment
        :param docker: Unique identifier of the experiment
        :param configuration: Unique identifier of the experiment
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

        :attribute experiment: Unique identifier of the experiment
        :attribute docker: Name of the docker image of the dbms

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
		self.experiment = experiment
		#self.code = code
		self.docker = docker
		if len(configuration) == 0:
			configuration = docker
		self.configuration = configuration
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
		if num_experiment_to_apply is not None:
			self.num_experiment_to_apply = num_experiment_to_apply
		else:
			self.num_experiment_to_apply = self.experiment.num_experiment_to_apply
		self.num_experiment_to_apply_done = 0
		self.clients = clients
		#if self.code is None:
		#	self.code = str(round(time.time()))
		self.appname = self.experiment.cluster.appname
		self.code = self.experiment.cluster.code
		self.resources = {}
		self.set_resources(**self.experiment.resources)
		self.set_ddl_parameters(**self.experiment.ddl_parameters)
		self.set_eval_parameters(**self.experiment.eval_parameters)
		self.set_connectionmanagement(**self.experiment.connectionmanagement)
		self.set_storage(**self.experiment.storage)
		self.set_nodes(**self.experiment.nodes)
		self.set_maintaining_parameters(**self.experiment.maintaining_parameters)
		self.experiment.add_configuration(self)
		self.dialect = dialect
		self.num_worker = worker
		self.num_loading = 0
		self.num_maintaining = 0
		self.monitoring_active = experiment.monitoring_active
		self.maintaining_active = experiment.maintaining_active
		self.loading_active = experiment.loading_active
		self.parallelism = 1
		self.storage_label = experiment.storage_label
		self.experiment_done = False
		self.dockerimage = dockerimage
		self.connection_parameter = {}
		# per configuration: sut+service
		# per configuration: monitoring+service
		# per configuration: list of benchmarker
		self.reset_sut()
	def reset_sut(self):
		"""
		Forget that the SUT has been loaded and benchmarked.
		"""
		self.timeLoading = 0
		self.loading_started = False
		self.loading_after_time = None
		self.loading_finished = False
		self.client = 1		
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
	def wait(self, sec, silent=False):
		"""
		Function for waiting some time and inform via output about this

		:param sec: Number of seconds to wait
		:param silent: True means we do not output anything about this waiting
		"""
		if not silent:
			print("Waiting "+str(sec)+"s...", end="", flush=True)
		intervals = int(sec)
		time.sleep(intervals)
		if not silent:
			print("done")
	def delay(self, sec):
		"""
		Function for waiting some time and inform via output about this.
		Synonymous for wait()

		:param sec: Number of seconds to wait
		"""
		self.wait(sec)
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
		self.storage = kwargs
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
		Can be set by experiment before creation of configuration.

		:param kwargs: Dict of meta data, example 'type' => 'noindex'
		"""
		self.eval_parameters = kwargs
	def set_maintaining_parameters(self, **kwargs):
		"""
		Sets ENV for maintaining components.
		Can be set by experiment before creation of configuration.

		:param kwargs: Dict of meta data, example 'PARALLEL' => '64'
		"""
		self.maintaining_parameters = kwargs
	def set_nodes(self, **kwargs):
		self.nodes = kwargs
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
		#	pod_sut = pods[0]
		#	status = self.experiment.cluster.get_pod_status(pod_sut)
		#	if status == "Running":
		#		return True
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
	def start_loading_pod(self, app='', component='loading', experiment='', configuration='', parallelism=1):
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
		# put list of clients to message queue
		pods_messagequeue = self.experiment.cluster.get_pods(component='messagequeue')
		if len(pods_messagequeue) > 0:
			pod_messagequeue = pods_messagequeue[0]
		else:
			pod_messagequeue = 'bexhoma-messagequeue-5ff94984ff-mv9zn'
		print("I am using messagequeue {}".format(pod_messagequeue))
		redisQueue = 'bexhoma-maintain-{}-{}'.format(self.configuration, self.code)
		#l = redisClient.lrange(redisQueue, 0, -1)
		#print(l)
		for i in range(1, self.num_loading+1):
			#redisClient.rpush(redisQueue, i)
			redisCommand = 'redis-cli rpush {redisQueue} {child} '.format(redisQueue=redisQueue, child=i)
			self.experiment.cluster.executeCTL(command=redisCommand, pod=pod_messagequeue)
		# start job
		job = self.create_job_loading(app=app, component='loading', experiment=experiment, configuration=configuration, parallelism=parallelism)
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
		pods = self.experiment.cluster.get_pods(app, component, self.experiment.code, configuration)
		if len(pods) > 0:
			pod_sut = pods[0]
			status = self.experiment.cluster.get_pod_status(pod_sut)
			if status != "Running":
				return False
			if self.num_worker > 0:
				self.attach_worker()
			#while status != "Running":
			#	print(pod_sut, status)
			#	self.wait(10)
			#	status = self.experiment.cluster.get_pod_status(pod_sut)
			print("ckeck if {} is running".format(pod_sut))
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
			#	self.wait(10)
			#	dbmsactive = self.check_DBMS_connection(self.experiment.cluster.host, self.experiment.cluster.port)
			#self.wait(10)
			self.check_load_data()
			if not self.loading_started:
				#print("load_data")
				self.load_data()
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
	def generate_component_name(self, app='', component='', experiment='', configuration='', client=''):
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
		if len(client) > 0:
			name = "{app}-{component}-{configuration}-{experiment}-{client}".format(app=app, component=component, configuration=configuration, experiment=experiment, client=client).lower()
		else:
			name = "{app}-{component}-{configuration}-{experiment}".format(app=app, component=component, configuration=configuration, experiment=experiment).lower()
		return name
	def start_maintaining(self, app='', component='maintaining', experiment='', configuration='', parallelism=1):
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
		job = self.create_job_maintaining(app=app, component='maintaining', experiment=experiment, configuration=configuration, parallelism=parallelism)
		self.logger.debug("Deploy "+job)
		self.experiment.cluster.kubectl('create -f '+job)#self.yamlfolder+deployment)
	def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
		"""
		Generate a name for the monitoring component.
		Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`

		:param app: app the component belongs to
		:param component: Component, for example sut or monitoring
		:param experiment: Unique identifier of the experiment
		:param configuration: Name of the dbms configuration
		"""
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
		if not self.experiment.monitoring_active:
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
		print("start_monitoring of {}".format(name_sut))
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
						prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: '{master}'
	scrape_interval: 3s
	scrape_timeout: 3s
	static_configs:
	  - targets: ['{master}:9300']
  - job_name: 'monitor-gpu'
	scrape_interval: 3s
	scrape_timeout: 3s
	static_configs:
	  - targets: ['{master}:9400']""".format(master=name_sut)
						# services of workers
						name_worker = self.generate_component_name(component='worker', configuration=self.configuration, experiment=self.code)
						pods_worker = self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
						i = 0
						for pod in pods_worker:
							print('Worker: {worker}.{service_sut}'.format(worker=pod, service_sut=name_worker))
							prometheus_config += """
  - job_name: '{worker}'
	scrape_interval: 3s
	scrape_timeout: 3s
	static_configs:
	  - targets: ['{worker}.{service_sut}:9300']""".format(worker=pod, service_sut=name_worker, client=i)
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
		for p in pods:
			status = self.experiment.cluster.get_pod_status(p)
			print(p, status)
			#if status == "Running":
			self.experiment.cluster.delete_pod(p)
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
	def get_instance_from_resources(self):
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
		#storage_label = 'tpc-ds-1'
		if len(app)==0:
			app = self.appname
		if len(configuration) == 0:
			configuration = self.configuration
		if len(experiment) == 0:
			experiment = self.code
		instance = self.get_instance_from_resources()#self.i
		template = "deploymenttemplate-"+self.docker+".yml"
		name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
		name_worker = self.generate_component_name(app=app, component='worker', experiment=experiment, configuration=configuration)
		if self.storage['storageConfiguration']:
			name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=self.storage['storageConfiguration'])
		else:
			name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=configuration)
		self.logger.debug('configuration.start_sut(name={})'.format(name))
		deployments = self.experiment.cluster.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
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
					dep['metadata']['labels']['configuration'] = configuration
					dep['metadata']['labels']['experiment'] = self.storage_label
					dep['metadata']['labels']['dbms'] = self.docker
					dep['metadata']['labels']['loaded'] = "False"
					if self.storage['storageClassName'] is not None and len(self.storage['storageClassName']) > 0:
						dep['spec']['storageClassName'] = self.storage['storageClassName']
						#print(dep['spec']['storageClassName'])
					else:
						del result[key]['spec']['storageClassName']
					if len(self.storage['storageSize']) > 0:
						dep['spec']['resources']['requests']['storage'] = self.storage['storageSize']
					#print(dep['spec']['accessModes']) # list
					#print(dep['spec']['resources']['requests']['storage'])
					pvcs = self.experiment.cluster.get_pvc(app=app, component='storage', experiment=self.storage_label, configuration=configuration)
					#print(pvcs)
					if len(pvcs) > 0:
						print("Storage {} exists".format(name_pvc))
						yaml_deployment['spec']['template']['metadata']['labels']['storage_exists'] = "True"
						pvcs_labels = self.experiment.cluster.get_pvc_labels(app=app, component='storage', experiment=self.storage_label, configuration=configuration)
						self.logger.debug(pvcs_labels)
						if len(pvcs_labels) > 0:
							pvc_labels = pvcs_labels[0]
							if 'loaded' in pvc_labels:
								yaml_deployment['spec']['template']['metadata']['labels']['loaded'] = pvc_labels['loaded']
							if 'timeLoading' in pvc_labels:
								yaml_deployment['spec']['template']['metadata']['labels']['timeLoading'] = pvc_labels['timeLoading']
							if 'timeLoadingStart' in pvc_labels:
								yaml_deployment['spec']['template']['metadata']['labels']['timeLoadingStart'] = pvc_labels['timeLoadingStart']
							if 'timeLoadingEnd' in pvc_labels:
								yaml_deployment['spec']['template']['metadata']['labels']['timeLoadingEnd'] = pvc_labels['timeLoadingEnd']
						del result[key]
			if dep['kind'] == 'StatefulSet':
				if self.num_worker == 0:
					del result[key]
					continue
				dep['metadata']['name'] = name_worker
				#self.service = dep['metadata']['name']
				dep['metadata']['labels']['app'] = app
				dep['metadata']['labels']['component'] = 'worker'
				dep['metadata']['labels']['configuration'] = configuration
				dep['metadata']['labels']['experiment'] = experiment
				dep['metadata']['labels']['dbms'] = self.docker
				dep['spec']['replicas'] = self.num_worker
				dep['spec']['serviceName'] = name_worker
				dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
				dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
				#dep['spec']['selector'] = dep['metadata']['labels'].copy()
				for i, container in enumerate(dep['spec']['template']['spec']['containers']):
					#container = dep['spec']['template']['spec']['containers'][0]['name']
					#print("Container", container)
					if container['name'] == 'dbms':
						#print(container['volumeMounts'])
						for j, vol in enumerate(container['volumeMounts']):
							if vol['name'] == 'bexhoma-workers':
								#print(vol['mountPath'])
								if not use_storage:
									del result[key]['spec']['template']['spec']['containers'][i]['volumeMounts'][j]
				if not use_storage and 'volumeClaimTemplates' in result[key]['spec']:
					del result[key]['spec']['volumeClaimTemplates']
				#print(pvc)
			if dep['kind'] == 'Service':
				if dep['metadata']['name'] != 'bexhoma-service':
					if self.num_worker == 0:
						del result[key]
						continue
					dep['metadata']['name'] = name_worker
					dep['metadata']['labels']['app'] = app
					dep['metadata']['labels']['component'] = 'worker'
					dep['metadata']['labels']['configuration'] = configuration
					dep['metadata']['labels']['experiment'] = experiment
					dep['metadata']['labels']['dbms'] = self.docker
					dep['spec']['selector'] = dep['metadata']['labels'].copy()
					if not self.monitoring_active:
						for i, ports in reversed(list(enumerate(dep['spec']['ports']))):
							# remove monitoring ports
							if 'name' in ports and ports['name'] != 'port-dbms':
								del result[key]['spec']['ports'][i]
					continue
				dep['metadata']['labels']['app'] = app
				dep['metadata']['labels']['component'] = component
				dep['metadata']['labels']['configuration'] = configuration
				dep['metadata']['labels']['experiment'] = experiment
				dep['metadata']['labels']['dbms'] = self.docker
				dep['spec']['selector'] = dep['metadata']['labels'].copy()
				dep['metadata']['name'] = name
				self.service = dep['metadata']['name']
				if not self.monitoring_active:
					for i, ports in reversed(list(enumerate(dep['spec']['ports']))):
						# remove monitoring ports
						if 'name' in ports and ports['name'] != 'port-dbms':
							del result[key]['spec']['ports'][i]
				#print(pvc)
			if dep['kind'] == 'Deployment':
				yaml_deployment = result[key]
				dep['metadata']['name'] = name
				dep['metadata']['labels']['app'] = app
				dep['metadata']['labels']['component'] = component
				dep['metadata']['labels']['configuration'] = configuration
				dep['metadata']['labels']['experiment'] = experiment
				dep['metadata']['labels']['dbms'] = self.docker
				dep['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
				dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
				dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
				deployment = dep['metadata']['name']
				appname = dep['spec']['template']['metadata']['labels']['app']
				for i, container in reversed(list(enumerate(dep['spec']['template']['spec']['containers']))):
					#container = dep['spec']['template']['spec']['containers'][0]['name']
					#print("Container", container)
					if container['name'] == 'dbms':
						#print(container['volumeMounts'])
						for j, vol in enumerate(container['volumeMounts']):
							if vol['name'] == 'benchmark-storage-volume':
								#print(vol['mountPath'])
								if not use_storage:
									del result[key]['spec']['template']['spec']['containers'][i]['volumeMounts'][j]
						if self.dockerimage:
							result[key]['spec']['template']['spec']['containers'][i]['image'] = self.dockerimage
						else:
							self.dockerimage = result[key]['spec']['template']['spec']['containers'][i]['image']
					elif not self.monitoring_active:
						# remove monitoring containers
						if container['name'] == 'cadvisor':
							del result[key]['spec']['template']['spec']['containers'][i]
						if container['name'] == 'dcgm-exporter':
							del result[key]['spec']['template']['spec']['containers'][i]
				for i, vol in reversed(list(enumerate(dep['spec']['template']['spec']['volumes']))):
					if vol['name'] == 'benchmark-storage-volume':
						if not use_storage:
							del result[key]['spec']['template']['spec']['volumes'][i]
						else:
							vol['persistentVolumeClaim']['claimName'] = name_pvc
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
				req_cpu = cpu
				limit_cpu = cpu
				req_mem = mem
				limit_mem = mem
				req_gpu = gpu
				node_cpu = ''
				node_gpu = node
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
				else:
					if 'nvidia.com/gpu' in dep['spec']['template']['spec']['containers'][0]['resources']['limits']:
						del dep['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu']
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
		self.experiment.cluster.kubectl('create -f '+deployment_experiment)
		#if self.experiment.monitoring_active:
		#	self.start_monitoring()
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
				name_pvc = self.generate_component_name(app=app, component='storage', experiment=self.storage_label, configuration=configuration)
				self.experiment.cluster.delete_pvc(name_pvc)
		deployments = self.experiment.cluster.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
		for deployment in deployments:
			self.experiment.cluster.delete_deployment(deployment)
		stateful_sets = self.experiment.cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
		for stateful_set in stateful_sets:
			self.experiment.cluster.delete_stateful_set(stateful_set)
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(cmd['check_gpus'], self.pod_sut, container='dbms')
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
			stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
		cores = stdout#os.popen(fullcommand).read()
		if len(cores)>0:
			return int(cores)
		else:
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
		host = stdout#os.popen(fullcommand).read()
		return host.replace('\n','')
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
			if self.appname == datastore['metadata']['labels']['app']:
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
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
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
		cuda = stdout#os.popen(fullcommand).read()
		return cuda.replace('|', '').replace('\n','').strip()
	def getTimediff(self):
		self.logger.debug('configuration.getTimediff()')
		cmd = {}
		command = 'date +"%s"'
		#fullcommand = 'kubectl exec '+cluster.pod_sut+' --container=dbms -- bash -c "'+command+'"'
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
		timestamp_remote = stdout#os.popen(fullcommand).read()
		#timestamp_remote = os.popen(fullcommand).read()
		timestamp_local = os.popen(command).read()
		#print(timestamp_remote)
		#print(timestamp_local)
		return int(timestamp_remote)-int(timestamp_local)
	def getDiskSpaceUsedData(self):
		self.logger.debug('configuration.getDiskSpaceUsedData()')
		cmd = {}
		if 'datadir' in self.dockertemplate:
			datadir = self.dockertemplate['datadir']
		else:
			return 0
		try:
			command = "du "+datadir+" | awk 'END{print \\$1}'"
			cmd['disk_space_used'] = command
			stdin, stdout, stderr = self.experiment.cluster.executeCTL(cmd['disk_space_used'], self.pod_sut, container='dbms')
			return int(stdout.replace('\n',''))
		except Exception as e:
			# Windows
			command = "du "+datadir+" | awk 'END{print $1}'"
			cmd['disk_space_used'] = command
			stdin, stdout, stderr = self.experiment.cluster.executeCTL(cmd['disk_space_used'], self.pod_sut, container='dbms')
			if len(stdout) > 0:
				return int(stdout.replace('\n',''))
		return 0
	def getDiskSpaceUsed(self):
		self.logger.debug('configuration.getDiskSpaceUsed()')
		disk = ''
		cmd = {}
		try:
			command = "df / | awk 'NR == 2{print \\$3}'"
			#fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
			#disk = os.popen(fullcommand).read()
			stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
			disk = stdout#os.popen(fullcommand).read()
			return int(disk.replace('\n',''))
		except Exception as e:
			# Windows
			command = "df / | awk 'NR == 2{print $3}'"
			#fullcommand = 'kubectl exec '+self.pod_sut+' --container=dbms -- bash -c "'+command+'"'
			#disk = os.popen(fullcommand).read()
			stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=command, pod=self.pod_sut, container='dbms')
			disk = stdout#os.popen(fullcommand).read()
			if len(disk) > 0:
				return int(disk.replace('\n',''))
		# pipe to awk sometimes does not work
		#return int(disk.split('\t')[0])
		return 0
	def get_host_all(self):
		"""
		Calls all `get_host_x()` methods.
		Returns information about the sut's host as a dict.

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
		server['disk'] = self.getDiskSpaceUsed()
		server['datadisk'] = self.getDiskSpaceUsedData()
		server['cuda'] = self.get_host_cuda()
		return server
	def get_connection_config(self, connection, alias='', dialect='', serverip='localhost', monitoring_host='localhost'):
		#if connection is None:
		#	connection = self.getConnectionName()
		"""
		print("get_connection_config")
		#self.getInfo(component='sut')
		mem = self.get_host_memory()
		cpu = self.get_host_cpu()
		cores = self.get_host_cores()
		host = self.get_host_system()
		cuda = self.get_host_cuda()
		gpu = self.get_host_gpus()
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
		c['timeLoad'] = self.timeLoading
		c['priceperhourdollar'] = 0.0  + self.dockertemplate['priceperhourdollar']
		# get hosts information
		pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
		self.pod_sut = pods[0]
		pod_sut = self.pod_sut
		c['hostsystem'] = self.get_host_all()
		# get worker information
		c['worker'] = []
		pods = self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
		for pod in pods:
			self.pod_sut = pod
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
		#	c['hostsystem']['CUDA'] = cuda
		c['connectionmanagement'] = {}
		c['connectionmanagement']['numProcesses'] = self.connectionmanagement['numProcesses']
		c['connectionmanagement']['runsPerConnection'] = self.connectionmanagement['runsPerConnection']
		c['connectionmanagement']['timeout'] = self.connectionmanagement['timeout']
		c['connectionmanagement']['singleConnection'] = self.connectionmanagement['singleConnection'] if 'singleConnection' in self.connectionmanagement else True
		c['monitoring'] = {}
		config_K8s = self.experiment.cluster.config['credentials']['k8s']
		if self.experiment.monitoring_active and 'monitor' in config_K8s:
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
			#c['monitoring']['grafanaextend'] = 1
			c['monitoring']['metrics'] = {}
			if 'metrics' in config_K8s['monitor']:
				# instance="bexhoma-sut-mysql-1615839517:9300"
				# instance=~"bexhoma-sut-mysql-1615839517.*"
				if len(c['hostsystem']['GPUIDs']) > 0:
					gpuid = '|'.join(c['hostsystem']['GPUIDs'])
				else:
					gpuid = ""
				node = c['hostsystem']['node']
				for metricname, metricdata in config_K8s['monitor']['metrics'].items():
					c['monitoring']['metrics'][metricname] = metricdata.copy()
					c['monitoring']['metrics'][metricname]['query'] = c['monitoring']['metrics'][metricname]['query'].format(host=node, gpuid=gpuid, configuration=self.configuration.lower(), experiment=self.code)
		c['JDBC']['url'] = c['JDBC']['url'].format(serverip=serverip, dbname=self.experiment.volume, DBNAME=self.experiment.volume.upper(), timout_s=c['connectionmanagement']['timeout'], timeout_ms=c['connectionmanagement']['timeout']*1000)
		#print(c)
		return c#.copy()
	def run_benchmarker_pod(self, connection=None, code=None, info=[], resultfolder='', experiments_configfolder='', alias='', dialect='', query=None, app='', component='benchmarker', experiment='', configuration='', client='1', parallelism=1):
		self.logger.debug('configuration.run_benchmarker_pod()')
		if len(resultfolder) == 0:
			resultfolder = self.experiment.cluster.config['benchmarker']['resultfolder']
		if len(experiments_configfolder) == 0:
			experiments_configfolder = self.experiment.cluster.experiments_configfolder
		if connection is None:
			connection = self.configuration#self.getConnectionName()
		if len(configuration) == 0:
			configuration = connection
		if code is None:
			code = self.code
		if not isinstance(client, str):
			client = str(client)
		if len(dialect) == 0 and len(self.dialect) > 0:
			dialect = self.dialect
		#self.experiment.cluster.stopPortforwarding()
		# set query management for new query file
		tools.query.template = self.experiment.querymanagement
		# get connection config (sut)
		monitoring_host = self.generate_component_name(component='monitoring', configuration=configuration, experiment=self.code)
		service_name = self.generate_component_name(component='sut', configuration=configuration, experiment=self.code)
		service_namespace = self.experiment.cluster.contextdata['namespace']
		service_host = self.experiment.cluster.contextdata['service_sut'].format(service=service_name, namespace=service_namespace)
		pods = self.experiment.cluster.get_pods(component='sut', configuration=configuration, experiment=self.code)
		self.pod_sut = pods[0]
		#service_port = config_K8s['port']
		c = self.get_connection_config(connection, alias, dialect, serverip=service_host, monitoring_host=monitoring_host)#config_K8s['ip'])
		#c['parameter'] = {}
		c['parameter'] = self.eval_parameters
		c['parameter']['parallelism'] = parallelism
		c['parameter']['client'] = client
		c['parameter']['numExperiment'] = str(self.num_experiment_to_apply_done+1)
		c['parameter']['dockerimage'] = self.dockerimage
		c['parameter']['connection_parameter'] = self.connection_parameter
		#print(c)
		#print(self.experiment.cluster.config['benchmarker']['jarfolder'])
		if isinstance(c['JDBC']['jar'], list):
			for i, j in enumerate(c['JDBC']['jar']):
				c['JDBC']['jar'][i] = self.experiment.cluster.config['benchmarker']['jarfolder']+c['JDBC']['jar'][i]
		elif isinstance(c['JDBC']['jar'], str):
			c['JDBC']['jar'] = self.experiment.cluster.config['benchmarker']['jarfolder']+c['JDBC']['jar']
		#print(c)
		#print(self.dockertemplate)
		#print(self.experiment.cluster.dockers[self.docker])
		#if code is not None:
		#	resultfolder += '/'+str(int(code))
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
		self.logger.debug('configuration.run_benchmarker_pod(Code={})'.format(self.code))
		# read config for benchmarker
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
		self.benchmark.connections = [c]
		#print(self.benchmark.connections)
		self.logger.debug('configuration.run_benchmarker_pod(): {}'.format(self.benchmark.connections))
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
		self.experiment.cluster.log_experiment(experiment)
		# copy deployments
		#if os.path.isfile(self.yamlfolder+self.deployment):
		#	shutil.copy(self.yamlfolder+self.deployment, self.benchmark.path+'/'+connection+'.yml')
		# create pod
		yamlfile = self.create_job(connection=connection, component=component, configuration=configuration, experiment=self.code, client=client, parallelism=parallelism, alias=c['alias'])
		# start pod
		self.experiment.cluster.kubectl('create -f '+yamlfile)
		pods = []
		while len(pods) == 0:
			self.wait(10)
			pods = self.experiment.cluster.get_job_pods(component=component, configuration=configuration, experiment=self.code, client=client)
		client_pod_name = pods[0]
		status = self.experiment.cluster.get_pod_status(client_pod_name)
		self.logger.debug('Pod={} has status={}'.format(client_pod_name, status))
		print("Waiting for job {}: ".format(client_pod_name), end="", flush=True)
		while status != "Running":
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
		# copy config to pod
		cmd = {}
		cmd['prepare_log'] = 'mkdir -p /results/'+str(self.code)
		stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=cmd['prepare_log'], pod=client_pod_name)
		#disk = stdout#os.popen(fullcommand).read()
		#fullcommand = 'kubectl exec '+client_pod_name+' -- bash -c "'+cmd['prepare_log'].replace('"','\\"')+'"'
		#print(fullcommand)
		#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#stdout, stderr = proc.communicate()
		#print(stdout.decode('utf-8'), stderr.decode('utf-8'))
		#stdin, stdout, stderr = self.executeCTL_client(cmd['prepare_log'])
		#cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=self.benchmark.path+'/queries.config')+' /results/'+str(self.code)+'/queries.config'
		#stdin, stdout, stderr = self.executeCTL_client(cmd['copy_init_scripts'])
		stdout = self.experiment.cluster.kubectl('cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/queries.config '+client_pod_name+':/results/'+str(self.code)+'/queries.config')
		self.logger.debug('copy config queries.config: {}'.format(stdout))
		#cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=self.benchmark.path+'/connections.config')+' /results/'+str(self.code)+'/connections.config'
		#stdin, stdout, stderr = self.executeCTL_client(cmd['copy_init_scripts'])
		stdout = self.experiment.cluster.kubectl('cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/connections.config '+client_pod_name+':/results/'+str(self.code)+'/'+c['name']+'.config')
		self.logger.debug('copy config {}: {}'.format(c['name']+'.config', stdout))
		# copy twice to be more sure it worked
		stdout = self.experiment.cluster.kubectl('cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/connections.config '+client_pod_name+':/results/'+str(self.code)+'/'+c['name']+'.config')
		self.logger.debug('copy config {}: {}'.format(c['name']+'.config', stdout))
		stdout = self.experiment.cluster.kubectl('cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/connections.config '+client_pod_name+':/results/'+str(self.code)+'/connections.config')
		self.logger.debug('copy config connections.config: {}'.format(stdout))
		stdout = self.experiment.cluster.kubectl('cp '+self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/protocol.json '+client_pod_name+':/results/'+str(self.code)+'/protocol.json')
		self.logger.debug('copy config protocol.json: {}'.format(stdout))
		# get monitoring for loading
		if self.monitoring_active:
			cmd = {}
			#cmd['update_dbmsbenchmarker'] = 'git pull'#/'+str(self.code)
			#fullcommand = 'kubectl exec '+client_pod_name+' -- bash -c "'+cmd['update_dbmsbenchmarker'].replace('"','\\"')+'"'
			#print(fullcommand)
			#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			#stdout, stderr = proc.communicate()
			cmd['fetch_loading_metrics'] = 'python metrics.py -r /results/ -c {} -ts {} -te {}'.format(self.code, self.timeLoadingStart, self.timeLoadingEnd)
			stdin, stdout, stderr = self.experiment.cluster.executeCTL(command=cmd['fetch_loading_metrics'], pod=client_pod_name)
			#fullcommand = 'kubectl exec '+client_pod_name+' -- bash -c "'+cmd['fetch_loading_metrics'].replace('"','\\"')+'"'
			#print(fullcommand)
			#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			#stdout, stderr = proc.communicate()
			#print(stdout.decode('utf-8'), stderr.decode('utf-8'))
		"""
		self.wait(10)
		jobs = self.get_jobs(component=component, configuration=configuration, experiment=self.code, client=client)
		jobname = jobs[0]
		while not self.get_job_status(jobname=jobname, component=component, configuration=configuration, experiment=self.code, client=client):
			print("job running")
			self.wait(60)
		# write pod log
		stdin, stdout, stderr = self.pod_log(client_pod_name)
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
		"""
	def kubectl(self, command):
		fullcommand = 'kubectl --context {context} {command}'.format(context=self.experiment.cluster.context, command=command)
		#print(fullcommand)
		self.logger.debug('configuration.kubectl({})'.format(fullcommand))
		return os.system(fullcommand)
	def executeCTL(self, command, pod='', container='', params=''):
		if len(pod) == 0:
			pod = self.activepod
		command_clean = command.replace('"','\\"')
		if len(container) > 0:
			fullcommand = 'kubectl --context {context} exec {pod} --container={container} -- bash -c "{command}"'.format(context=self.experiment.cluster.context, pod=pod, container=container, command=command_clean)
		else:
			fullcommand = 'kubectl --context {context} exec {pod} -- bash -c "{command}"'.format(context=self.experiment.cluster.context, pod=pod, command=command_clean)
			#fullcommand = 'kubectl exec '+self.activepod+' --container=dbms -- bash -c "'+command_clean+'"'
		#print(fullcommand)
		self.logger.debug('configuration.executeCTL({})'.format(fullcommand))
		proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()
		#print(stdout.decode('utf-8'), stderr.decode('utf-8'))
		str_stdout = stdout.decode('utf-8')
		str_stderr = stderr.decode('utf-8')
		return "", str_stdout, str_stderr
		#return "", stdout.decode('utf-8'), stderr.decode('utf-8')
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
	"""
	def copyLog(self):
		print("copyLog")
		pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
		self.pod_sut = pods[0]
		if len(self.dockertemplate['logfile']):
			cmd = {}
			cmd['prepare_log'] = 'mkdir /data/'+str(self.code)
			stdin, stdout, stderr = self.executeCTL(command=cmd['prepare_log'], pod=self.pod_sut)
			cmd['save_log'] = 'cp '+self.dockertemplate['logfile']+' /data/'+str(self.code)+'/'+self.configuration+'.log'
			stdin, stdout, stderr = self.executeCTL(command=cmd['save_log'], pod=self.pod_sut)
	def prepareInit(self):
		self.logger.debug('configuration.prepareInit()')
		pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
		self.pod_sut = pods[0]
		#cmd = {}
		#cmd['prepare_init'] = 'mkdir -p /data/'+self.experiment.cluster.experiments_configfolder+'/'+self.configuration
		#stdin, stdout, stderr = self.executeCTL(cmd['prepare_init'], self.pod_sut)
		#scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiment.cluster.experiments_configfolder, docker=self.docker)
		scriptfolder = '/tmp/'
		# the inits are in the result folder?
		#i = 0
		#for script in self.initscript:
		#	#cmd['copy_init_scripts'] = 'cp {scriptname} /data/{code}/{connection}_init_{nr}.log'.format(scriptname=scriptfolder+script, code=self.code, connection=self.connection, nr=i)
		#	cmd['copy_init_scripts'] = 'cp {scriptname}'.format(scriptname=scriptfolder+script)+' /data/'+str(self.code)+'/'+self.connection+'_init_'+str(i)+'.log'
		#	stdin, stdout, stderr = self.executeCTL(cmd['copy_init_scripts'])
		#	i = i + 1
		if len(self.ddl_parameters):
			for script in self.initscript:
				filename_template = self.docker+'/'+script
				if os.path.isfile(self.experiment.cluster.experiments_configfolder+'/'+filename_template):
					with open(self.experiment.cluster.experiments_configfolder+'/'+filename_template, "r") as initscript_template:
						data = initscript_template.read()
						data = data.format(**self.ddl_parameters)
						filename_filled = self.docker+'/filled_'+script
						with open(self.experiment.cluster.experiments_configfolder+'/'+filename_filled, "w") as initscript_filled:
							initscript_filled.write(data)
						self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename_filled, to_name=self.pod_sut+':'+scriptfolder+script))
		else:
			for script in self.initscript:
				filename = self.docker+'/'+script
				if os.path.isfile(self.experiment.cluster.experiments_configfolder+'/'+filename):
					self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename, to_name=self.pod_sut+':'+scriptfolder+script))
					stdin, stdout, stderr = self.executeCTL("sed -i $'s/\\r//' {to_name}".format(to_name=scriptfolder+script), self.pod_sut)
					#self.experiment.cluster.kubectl('cp --container dbms {from_name} {to_name}'.format(from_name=self.experiment.cluster.experiments_configfolder+'/'+filename, to_name=self.pod_sut+':'+scriptfolder+script))
	def attach_worker(self):
		if self.num_worker > 0:
			pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
			name_worker = self.generate_component_name(component='worker', experiment=self.code, configuration=self.configuration)
			if len(pods) > 0:
				pod_sut = pods[0]
				num_worker = 0
				while num_worker < self.num_worker:
					num_worker = 0
					pods_worker = self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
					for pod in pods_worker:
						#stdin, stdout, stderr = self.executeCTL(self.dockertemplate['attachWorker'].format(worker=pod, service_sut=name_worker), pod_sut)
						status = self.experiment.cluster.get_pod_status(pod)
						if status == "Running":
							num_worker = num_worker+1
					print(self.configuration, "Workers", num_worker, "of", self.num_worker)
				pods_worker = self.experiment.cluster.get_pods(component='worker', configuration=self.configuration, experiment=self.code)
				for pod in pods_worker:
					self.logger.debug('Worker attached: {worker}.{service_sut}'.format(worker=pod, service_sut=name_worker))
					stdin, stdout, stderr = self.executeCTL(self.dockertemplate['attachWorker'].format(worker=pod, service_sut=name_worker), pod_sut)
	def check_sut(self):
		pods = self.experiment.cluster.get_pods(app=self.appname, component='sut', configuration=self.configuration, experiment=self.code)
		if len(pods) > 0:
			self.pod_sut = pods[0]
			return True
		else:
			return False
	def check_load_data(self):
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
				success = self.experiment.cluster.get_job_status(job)
				self.experiment.cluster.logger.debug('job {} has success status {}'.format(job, success))
				#print(job, success)
				if success:
					self.experiment.cluster.logger.debug('job {} will be suspended and parallel loading will be considered finished'.format(job, success))
					# get labels (start) of sut
					pod_labels = self.experiment.cluster.get_pods_labels(app=app, component='sut', experiment=experiment, configuration=configuration)
					#print(pod_labels)
					if len(pod_labels) > 0:
						pod = next(iter(pod_labels.keys()))
						if 'timeLoadingStart' in pod_labels[pod]:
							self.timeLoadingStart = float(pod_labels[pod]['timeLoadingStart'])
						if 'timeLoadingEnd' in pod_labels[pod]:
							self.timeLoadingEnd = float(pod_labels[pod]['timeLoadingEnd'])
						if 'timeLoading' in pod_labels[pod]:
							self.timeLoading = float(pod_labels[pod]['timeLoading'])
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
						now = datetime.utcnow()
						now_string = now.strftime('%Y-%m-%d %H:%M:%S')
						time_now = str(datetime.now())
						time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
						self.timeLoadingEnd = int(time_now_int)
						self.timeLoading = int(self.timeLoadingEnd) - int(self.timeLoadingStart) + self.timeLoading
						self.experiment.cluster.logger.debug("LOADING LABELS")
						self.experiment.cluster.logger.debug(self.timeLoadingStart)
						self.experiment.cluster.logger.debug(self.timeLoadingEnd)
						self.experiment.cluster.logger.debug(self.timeLoading)
						fullcommand = 'label pods '+pod_sut+' --overwrite loaded=True timeLoadingEnd="{}" timeLoading={}'.format(time_now_int, self.timeLoading)
						#print(fullcommand)
						self.experiment.cluster.kubectl(fullcommand)
						# TODO: Also mark volume
					# delete job and all its pods
					self.experiment.cluster.delete_job(job)
					pods = self.experiment.cluster.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration)
					for pod in pods:
						status = self.experiment.cluster.get_pod_status(pod)
						print(pod, status)
						#if status == "Running":
						# TODO: Find names of containers dynamically
						container = 'datagenerator'
						stdout = self.experiment.cluster.pod_log(pod=pod, container=container)
						#stdin, stdout, stderr = self.pod_log(client_pod_name)
						filename_log = self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+pod+'.'+container+'.log'
						f = open(filename_log, "w")
						f.write(stdout)
						f.close()
						#
						container = 'sensor'
						stdout = self.experiment.cluster.pod_log(pod=pod, container='sensor')
						#stdin, stdout, stderr = self.pod_log(client_pod_name)
						filename_log = self.experiment.cluster.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+pod+'.'+container+'.log'
						f = open(filename_log, "w")
						f.write(stdout)
						f.close()
						self.experiment.cluster.delete_pod(pod)
					loading_pods_active = False
		else:
			loading_pods_active = False
		# check if asynch loading outside cluster is done
		# only if inside cluster if done
		if not loading_pods_active:
			pod_labels = self.experiment.cluster.get_pods_labels(app=self.appname, component='sut', experiment=self.experiment.code, configuration=self.configuration)
			#print(pod_labels)
			if len(pod_labels) > 0:
				pod = next(iter(pod_labels.keys()))
				if 'loaded' in pod_labels[pod]:
					self.loading_started = True
					if pod_labels[pod]['loaded'] == 'True':
						self.loading_finished = True
					else:
						self.loading_finished = False
				else:
					self.loading_started = False
				if 'timeLoadingStart' in pod_labels[pod]:
					self.timeLoadingStart = pod_labels[pod]['timeLoadingStart']
				if 'timeLoadingEnd' in pod_labels[pod]:
					self.timeLoadingEnd = pod_labels[pod]['timeLoadingEnd']
				if 'timeLoading' in pod_labels[pod]:
					self.timeLoading = float(pod_labels[pod]['timeLoading'])
			else:
				self.loading_started = False
				self.loading_finished = False
	def load_data(self):
		self.logger.debug('configuration.load_data()')
		self.loading_started = True
		self.prepareInit()
		pods = self.experiment.cluster.get_pods(component='sut', configuration=self.configuration, experiment=self.code)
		self.pod_sut = pods[0]
		#scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiment.cluster.experiments_configfolder, docker=self.docker)
		scriptfolder = '/tmp/'
		commands = self.initscript.copy()
		#print("load_data asynch")
		#if len(self.ddl_parameters):
		#	for i,c in enumerate(commands):
		#		commands[i] = '/filled_'+c
		use_storage = self.use_storage()
		if use_storage:
			#storage_label = 'tpc-ds-1'
			name_pvc = self.generate_component_name(app=self.appname, component='storage', experiment=self.storage_label, configuration=self.configuration)
			volume = name_pvc
		else:
			volume = ''
		print("start loading asynch {}".format(self.pod_sut))
		self.logger.debug("load_data_asynch(app="+self.appname+", component='sut', experiment="+self.code+", configuration="+self.configuration+", pod_sut="+self.pod_sut+", scriptfolder="+scriptfolder+", commands="+str(commands)+", loadData="+self.dockertemplate['loadData']+", path="+self.experiment.path+", volume="+volume+", context="+self.experiment.cluster.context+")")
		#result = load_data_asynch(app=self.appname, component='sut', experiment=self.code, configuration=self.configuration, pod_sut=self.pod_sut, scriptfolder=scriptfolder, commands=commands, loadData=self.dockertemplate['loadData'], path=self.experiment.path)
		thread_args = {'app':self.appname, 'component':'sut', 'experiment':self.code, 'configuration':self.configuration, 'pod_sut':self.pod_sut, 'scriptfolder':scriptfolder, 'commands':commands, 'loadData':self.dockertemplate['loadData'], 'path':self.experiment.path, 'volume':volume, 'context':self.experiment.cluster.context}
		thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
		thread.start()
		#pending = asyncio.all_tasks()
		#loop.run_until_complete(asyncio.gather(*pending))
		#print(result)
		return
		"""
		self.timeLoadingStart = default_timer()
		# mark pod
		fullcommand = 'label pods '+self.pod_sut+' --overwrite loaded=False timeLoadingStart="{}"'.format(self.timeLoadingStart)
		print(fullcommand)
		self.experiment.cluster.kubectl(fullcommand)
		#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#stdout, stderr = proc.communicate()
		# scripts
		shellcommand = 'sh {scriptname}'
		for c in commands:
			filename, file_extension = os.path.splitext(c)
			if file_extension.lower() == '.sql':
				#if len(self.ddl_parameters):
				#	filename_script = scriptfolder+'/filled_'+c
				#else:
				#	filename_script = scriptfolder+c
				filename_script = scriptfolder+c
				stdin, stdout, stderr = self.executeCTL(self.dockertemplate['loadData'].format(scriptname=filename_script), self.pod_sut)
				filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.log'.format(configuration=self.configuration, filename=filename, extension=file_extension.lower())
				print(filename_log)
				if len(stdout) > 0:
					with open(filename_log,'w') as file:
						file.write(stdout)
				filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.error'.format(configuration=self.configuration, filename=filename, extension=file_extension.lower())
				print(filename_log)
				if len(stderr) > 0:
					with open(filename_log,'w') as file:
						file.write(stderr)
			elif file_extension.lower() == '.sh':
				stdin, stdout, stderr = self.executeCTL(shellcommand.format(scriptname=filename_script), self.pod_sut)
				filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.log'.format(configuration=self.configuration, filename=filename, extension=file_extension.lower())
				print(filename_log)
				if len(stdout) > 0:
					with open(filename_log,'w') as file:
						file.write(stdout)
				filename_log = self.experiment.path+'/load-sut-{configuration}-{filename}{extension}.error'.format(configuration=self.configuration, filename=filename, extension=file_extension.lower())
				print(filename_log)
				if len(stderr) > 0:
					with open(filename_log,'w') as file:
						file.write(stderr)
		self.timeLoadingEnd = default_timer()
		self.timeLoading = self.timeLoadingEnd - self.timeLoadingStart
		fullcommand = 'label pods '+self.pod_sut+' --overwrite loaded=True timeLoadingStart="{}" timeLoadingEnd="{}" timeLoading={}'.format(self.timeLoadingStart, self.timeLoadingEnd, self.timeLoading)
		print(fullcommand)
		self.experiment.cluster.kubectl(fullcommand)
		#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#stdout, stderr = proc.communicate()
		"""
	def create_job(self, connection, app='', component='benchmarker', experiment='', configuration='', client='1', parallelism=1, alias=''):
		if len(app) == 0:
			app = self.appname
		code = str(int(experiment))
		#connection = configuration
		jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration, client=str(client))
		#print(jobname)
		self.logger.debug('configuration.create_job({})'.format(jobname))
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
				dep['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
				dep['spec']['template']['metadata']['labels']['app'] = app
				dep['spec']['template']['metadata']['labels']['component'] = component
				dep['spec']['template']['metadata']['labels']['configuration'] = configuration
				dep['spec']['template']['metadata']['labels']['experiment'] = str(experiment)
				dep['spec']['template']['metadata']['labels']['client'] = str(client)
				dep['spec']['template']['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
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
					if e['name'] == 'DBMSBENCHMARKER_ALIAS':
						dep['spec']['template']['spec']['containers'][0]['env'][i]['value'] = alias
					self.logger.debug('configuration.create_job({})'.format(str(e)))
					#print(e)
				e = {'name': 'DBMSBENCHMARKER_NOW', 'value': now_string}
				dep['spec']['template']['spec']['containers'][0]['env'].append(e)
				e = {'name': 'DBMSBENCHMARKER_START', 'value': start_string}
				dep['spec']['template']['spec']['containers'][0]['env'].append(e)
				# set nodeSelector
				if 'benchmarking' in self.nodes:
					if not 'nodeSelector' in dep['spec']['template']['spec']:
						dep['spec']['template']['spec']['nodeSelector'] = dict()
					if dep['spec']['template']['spec']['nodeSelector'] is None:
						dep['spec']['template']['spec']['nodeSelector'] = dict()
					dep['spec']['template']['spec']['nodeSelector']['type'] = self.nodes['benchmarking']
		#if not path.isdir(self.path):
		#	makedirs(self.path)
		with open(job_experiment,"w+") as stream:
			try:
				stream.write(yaml.dump_all(result))
			except yaml.YAMLError as exc:
				print(exc)
		return job_experiment
	#def create_job_maintaining(self, app='', component='maintaining', experiment='', configuration='', client='1', parallelism=1, alias=''):
	def create_job_maintaining(self, app='', component='maintaining', experiment='', configuration='', parallelism=1, alias=''):
		if len(app) == 0:
			app = self.appname
		jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
		servicename = self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
		#print(jobname)
		self.logger.debug('configuration.create_job_maintainer({})'.format(jobname))
		# determine start time
		now = datetime.utcnow()
		start = now + timedelta(seconds=180)
		#start = datetime.strptime('2021-03-04 23:15:25', '%Y-%m-%d %H:%M:%S')
		#wait = (start-now).seconds
		now_string = now.strftime('%Y-%m-%d %H:%M:%S')
		start_string = start.strftime('%Y-%m-%d %H:%M:%S')
		#yamlfile = self.experiment.cluster.yamlfolder+"job-dbmsbenchmarker-"+code+".yml"
		job_experiment = self.experiment.path+'/job-maintaining-{configuration}.yml'.format(configuration=configuration)
		jobtemplate = self.experiment.cluster.yamlfolder+"jobtemplate-maintaining.yml"
		if len(self.experiment.jobtemplate_maintaining) > 0:
			jobtemplate = self.experiment.cluster.yamlfolder+self.experiment.jobtemplate_maintaining
		with open(jobtemplate) as stream:
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
				#dep['metadata']['labels']['client'] = str(client)
				dep['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
				dep['spec']['template']['metadata']['labels']['app'] = app
				dep['spec']['template']['metadata']['labels']['component'] = component
				dep['spec']['template']['metadata']['labels']['configuration'] = configuration
				dep['spec']['template']['metadata']['labels']['experiment'] = str(experiment)
				#dep['spec']['template']['metadata']['labels']['client'] = str(client)
				dep['spec']['template']['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
				# set nodeSelector
				if 'maintaining' in self.nodes:
					if not 'nodeSelector' in dep['spec']['template']['spec']:
						dep['spec']['template']['spec']['nodeSelector'] = dict()
					if dep['spec']['template']['spec']['nodeSelector'] is None:
						dep['spec']['template']['spec']['nodeSelector'] = dict()
					dep['spec']['template']['spec']['nodeSelector']['type'] = self.nodes['maintaining']
				# store parameters in connection for evaluation
				if len(self.maintaining_parameters):
					self.connection_parameter['maintaining_parameters'] = self.maintaining_parameters
				# set ENV variables - defaults
				env_default = {}
				if 'SENSOR_RATE' in self.maintaining_parameters:
					env_default['SENSOR_RATE'] = self.maintaining_parameters['SENSOR_RATE']
				else:
					env_default['SENSOR_RATE'] = '0.1'
				if 'SENSOR_NUMBER' in self.maintaining_parameters:
					env_default['SENSOR_NUMBER'] = self.maintaining_parameters['SENSOR_NUMBER']
				else:
					env_default['SENSOR_NUMBER'] = '144000'
				# set ENV variables - in YAML
				# all init containers
				if 'initContainers' in dep['spec']['template']['spec']:
					for num_container, container in enumerate(dep['spec']['template']['spec']['initContainers']):
						envs = dep['spec']['template']['spec']['initContainers'][num_container]['env']
						for i,e in enumerate(envs):
							if e['name'] == 'BEXHOMA_HOST':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = servicename
							if e['name'] == 'SENSOR_DATABASE':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = 'postgresql://postgres:@{}:9091/postgres'.format(servicename)
							if e['name'] == 'SENSOR_RATE':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(env_default['SENSOR_RATE'])
							if e['name'] == 'SENSOR_NUMBER':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(env_default['SENSOR_NUMBER'])
							self.logger.debug('configuration.create_job_maintaining({})'.format(str(e)))
							#print(e)
				# all containers
				for num_container, container in enumerate(dep['spec']['template']['spec']['containers']):
					envs = dep['spec']['template']['spec']['containers'][num_container]['env']
					for i,e in enumerate(envs):
						if e['name'] == 'BEXHOMA_HOST':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = servicename
						if e['name'] == 'SENSOR_DATABASE':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = 'postgresql://postgres:@{}:9091/postgres'.format(servicename)
						if e['name'] == 'SENSOR_RATE':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(env_default['SENSOR_RATE'])
						if e['name'] == 'SENSOR_NUMBER':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(env_default['SENSOR_NUMBER'])
						self.logger.debug('configuration.create_job_maintaining({})'.format(str(e)))
						#print(e)
		with open(job_experiment,"w+") as stream:
			try:
				stream.write(yaml.dump_all(result))
			except yaml.YAMLError as exc:
				print(exc)
		return job_experiment
	def create_job_loading(self, app='', component='loading', experiment='', configuration='', parallelism=1, alias=''):
		if len(app) == 0:
			app = self.appname
		if len(configuration) == 0:
			configuration = self.configuration
		if len(experiment) == 0:
			experiment = self.code
		jobname = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
		servicename = self.generate_component_name(app=app, component='sut', experiment=experiment, configuration=configuration)
		#print(jobname)
		self.logger.debug('configuration.create_job_loading({})'.format(jobname))
		# determine start time
		now = datetime.utcnow()
		start = now + timedelta(seconds=180)
		#start = datetime.strptime('2021-03-04 23:15:25', '%Y-%m-%d %H:%M:%S')
		#wait = (start-now).seconds
		now_string = now.strftime('%Y-%m-%d %H:%M:%S')
		start_string = start.strftime('%Y-%m-%d %H:%M:%S')
		#yamlfile = self.experiment.cluster.yamlfolder+"job-dbmsbenchmarker-"+code+".yml"
		job_experiment = self.experiment.path+'/job-loading-{configuration}.yml'.format(configuration=configuration)
		jobtemplate = self.experiment.cluster.yamlfolder+"jobtemplate-loading.yml"
		if len(self.experiment.jobtemplate_loading) > 0:
			jobtemplate = self.experiment.cluster.yamlfolder+self.experiment.jobtemplate_loading
		with open(jobtemplate) as stream:
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
				#dep['metadata']['labels']['client'] = str(client)
				dep['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
				dep['spec']['template']['metadata']['labels']['app'] = app
				dep['spec']['template']['metadata']['labels']['component'] = component
				dep['spec']['template']['metadata']['labels']['configuration'] = configuration
				dep['spec']['template']['metadata']['labels']['experiment'] = str(experiment)
				#dep['spec']['template']['metadata']['labels']['client'] = str(client)
				dep['spec']['template']['metadata']['labels']['experimentRun'] = str(self.num_experiment_to_apply_done+1)
				# set nodeSelector
				if 'loading' in self.nodes:
					if not 'nodeSelector' in dep['spec']['template']['spec']:
						dep['spec']['template']['spec']['nodeSelector'] = dict()
					if dep['spec']['template']['spec']['nodeSelector'] is None:
						dep['spec']['template']['spec']['nodeSelector'] = dict()
					dep['spec']['template']['spec']['nodeSelector']['type'] = self.nodes['loading']
				# store parameters in connection for evaluation
				if len(self.maintaining_parameters):
					self.connection_parameter['loading_parameters'] = self.maintaining_parameters
				# set ENV variables - defaults
				env_default = {}
				if 'PARALLEL' in self.maintaining_parameters:
					env_default['PARALLEL'] = self.maintaining_parameters['PARALLEL']
				else:
					env_default['PARALLEL'] = '24'
				if 'CHILD' in self.maintaining_parameters:
					env_default['CHILD'] = self.maintaining_parameters['1']
				else:
					env_default['CHILD'] = '1'
				if 'RNGSEED' in self.maintaining_parameters:
					env_default['RNGSEED'] = self.maintaining_parameters['RNGSEED']
				else:
					env_default['RNGSEED'] = '123'
				if 'SF' in self.maintaining_parameters:
					env_default['SF'] = self.maintaining_parameters['SF']
				else:
					env_default['SF'] = '10'
				# set ENV variables - in YAML
				# all init containers
				if 'initContainers' in dep['spec']['template']['spec']:
					for num_container, container in enumerate(dep['spec']['template']['spec']['initContainers']):
						envs = dep['spec']['template']['spec']['initContainers'][num_container]['env']
						for i,e in enumerate(envs):
							if e['name'] == 'BEXHOMA_HOST':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = servicename
							if e['name'] == 'BEXHOMA_CLIENT':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(parallelism)
							if e['name'] == 'BEXHOMA_EXPERIMENT':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = experiment
							if e['name'] == 'BEXHOMA_CONNECTION':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = configuration
							if e['name'] == 'BEXHOMA_SLEEP':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = '60'
							if e['name'] == 'PARALLEL':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(env_default['PARALLEL'])
							if e['name'] == 'CHILD':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(env_default['CHILD'])
							if e['name'] == 'RNGSEED':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(env_default['RNGSEED'])
							if e['name'] == 'SF':
								dep['spec']['template']['spec']['initContainers'][num_container]['env'][i]['value'] = str(env_default['SF'])
							self.logger.debug('configuration.create_job_loading({})'.format(str(e)))
							#print(e)
				# all containers
				for num_container, container in enumerate(dep['spec']['template']['spec']['containers']):
					envs = dep['spec']['template']['spec']['containers'][num_container]['env']
					for i,e in enumerate(envs):
						if e['name'] == 'BEXHOMA_HOST':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = servicename
						if e['name'] == 'BEXHOMA_CLIENT':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(parallelism)
						if e['name'] == 'BEXHOMA_EXPERIMENT':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = experiment
						if e['name'] == 'BEXHOMA_CONNECTION':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = configuration
						if e['name'] == 'BEXHOMA_SLEEP':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = '60'
						if e['name'] == 'PARALLEL':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(env_default['PARALLEL'])
						if e['name'] == 'CHILD':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(env_default['CHILD'])
						if e['name'] == 'RNGSEED':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(env_default['RNGSEED'])
						if e['name'] == 'SF':
							dep['spec']['template']['spec']['containers'][num_container]['env'][i]['value'] = str(env_default['SF'])
						self.logger.debug('configuration.create_job_loading({})'.format(str(e)))
						#print(e)
		with open(job_experiment,"w+") as stream:
			try:
				stream.write(yaml.dump_all(result))
			except yaml.YAMLError as exc:
				print(exc)
		return job_experiment







# kubectl delete pvc,pods,services,deployments,jobs -l app=bexhoma-client





# https://stackoverflow.com/questions/37278647/fire-and-forget-python-async-await/53255955#53255955

#import asyncio

#def fire_and_forget(f):
#	def wrapped(*args, **kwargs):
#		return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)
#	return wrapped



#@fire_and_forget
def load_data_asynch(app, component, experiment, configuration, pod_sut, scriptfolder, commands, loadData, path, volume, context):
	logger = logging.getLogger('load_data_asynch')
	#with open('asynch.test.log','w') as file:
	#	file.write('started')
	#path = self.experiment.path
	#loadData = self.dockertemplate['loadData']
	def executeCTL(command, pod, context):
		fullcommand = 'kubectl --context {context} exec {pod} --container=dbms -- bash -c "{command}"'.format(context=context, pod=pod, command=command.replace('"','\\"'))
		logger.debug('executeCTL({})'.format(fullcommand))
		#print(fullcommand)
		proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()
		#print(stdout.decode('utf-8'), stderr.decode('utf-8'))
		logger.debug(stdout.decode('utf-8'))
		logger.debug(stderr.decode('utf-8'))
		return "", stdout.decode('utf-8'), stderr.decode('utf-8')
	def kubectl(command, context):
		fullcommand = 'kubectl --context {context} {command}'.format(context=context, command=command)
		logger.debug('executeCTL({})'.format(fullcommand))
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
	timeLoadingStart = default_timer()
	now = datetime.utcnow()
	now_string = now.strftime('%Y-%m-%d %H:%M:%S')
	time_now = str(datetime.now())
	time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
	# mark pod
	fullcommand = 'label pods '+pod_sut+' --overwrite loaded=False timeLoadingStart="{}"'.format(time_now_int)
	#print(fullcommand)
	kubectl(fullcommand, context)
	#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#stdout, stderr = proc.communicate()
	if len(volume) > 0:
		# mark pvc
		fullcommand = 'label pvc '+volume+' --overwrite loaded=False timeLoadingStart="{}"'.format(time_now_int)
		#print(fullcommand)
		kubectl(fullcommand, context)
		#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#stdout, stderr = proc.communicate()
	# scripts
	#scriptfolder = '/data/{experiment}/{docker}/'.format(experiment=self.experiment.cluster.experiments_configfolder, docker=self.docker)
	#shellcommand = '[ -f {scriptname} ] && sh {scriptname}'
	shellcommand = 'if [ -f {scriptname} ]; then sh {scriptname}; else exit 0; fi'
	#commands = self.initscript
	for c in commands:
		filename, file_extension = os.path.splitext(c)
		if file_extension.lower() == '.sql':
			stdin, stdout, stderr = executeCTL(loadData.format(scriptname=scriptfolder+c), pod_sut, context)
			filename_log = path+'/load-sut-{configuration}-{filename}{extension}.log'.format(configuration=configuration, filename=filename, extension=file_extension.lower())
			#print(filename_log)
			if len(stdout) > 0:
				with open(filename_log,'w') as file:
					file.write(stdout)
			filename_log = path+'/load-sut-{configuration}-{filename}{extension}.error'.format(configuration=configuration, filename=filename, extension=file_extension.lower())
			#print(filename_log)
			if len(stderr) > 0:
				with open(filename_log,'w') as file:
					file.write(stderr)
		elif file_extension.lower() == '.sh':
			stdin, stdout, stderr = executeCTL(shellcommand.format(scriptname=scriptfolder+c), pod_sut, context)
			filename_log = path+'/load-sut-{configuration}-{filename}{extension}.log'.format(configuration=configuration, filename=filename, extension=file_extension.lower())
			#print(filename_log)
			if len(stdout) > 0:
				with open(filename_log,'w') as file:
					file.write(stdout)
			filename_log = path+'/load-sut-{configuration}-{filename}{extension}.error'.format(configuration=configuration, filename=filename, extension=file_extension.lower())
			#print(filename_log)
			if len(stderr) > 0:
				with open(filename_log,'w') as file:
					file.write(stderr)
	# mark pod
	timeLoadingEnd = default_timer()
	timeLoading = timeLoadingEnd - timeLoadingStart
	now = datetime.utcnow()
	now_string = now.strftime('%Y-%m-%d %H:%M:%S')
	time_now = str(datetime.now())
	time_now_int = int(datetime.timestamp(datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S.%f')))
	fullcommand = 'label pods '+pod_sut+' --overwrite loaded=True timeLoadingEnd="{}" timeLoading={}'.format(time_now_int, timeLoading)
	#print(fullcommand)
	kubectl(fullcommand, context)
	#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#stdout, stderr = proc.communicate()
	if len(volume) > 0:
		# mark volume
		fullcommand = 'label pvc '+volume+' --overwrite loaded=True timeLoadingEnd="{}" timeLoading={}'.format(time_now_int, timeLoading)
		#print(fullcommand)
		kubectl(fullcommand, context)
		#proc = subprocess.Popen(fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#stdout, stderr = proc.communicate()
