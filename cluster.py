"""
    This script contains some code snippets for testing the detached mode in Kubernetes

    Copyright (C) 2021  Patrick Erdelt

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
from bexhoma import *
from dbmsbenchmarker import *
import logging
import urllib3
import logging
import argparse
import time
import pandas as pd
from tabulate import tabulate

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
	description = """Helps managing running Bexhoma experiments in a Kubernetes cluster.
	"""
	# argparse
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['stop','status'])
	parser.add_argument('-e', '--experiment', help='time to wait [s] before execution of the runs of a query', default=None)
	parser.add_argument('-v', '--verbose', help='givres more details about Kubernetes objects', action='store_true')
	args = parser.parse_args()
	if args.mode == 'stop':
		cluster = clusters.kubernetes()
		if args.experiment is None:
			experiment = experiments.default(cluster=cluster, code=cluster.code)
			cluster.stop_sut()
			cluster.stop_monitoring()
			cluster.stop_benchmarker()
		else:
			experiment = experiments.default(cluster=cluster, code=args.experiment)
			experiment.stop_sut()
	elif args.mode == 'status':
		cluster = clusters.kubernetes()
		app = cluster.appname
		pod_labels = cluster.getPodsLabels(app=app)
		#print("Pod Labels", pod_labels)
		experiments = set()
		for pod, labels in pod_labels.items():
			if 'experiment' in labels:
				experiments.add(labels['experiment'])
		#print(experiments)
		for experiment in experiments:
			if args.verbose:
				print(experiment)
			apps = {}
			pod_labels = cluster.getPodsLabels(app=app, experiment=experiment)
			configurations = set()
			for pod, labels in pod_labels.items():
				if 'configuration' in labels:
					configurations.add(labels['configuration'])
			for configuration in configurations:
				logging.debug(configuration)
				apps[configuration] = {}
				component = 'sut'
				apps[configuration][component] = ''
				apps[configuration]['loaded'] = ''
				if args.verbose:
					deployments = cluster.getDeployments(app=app, component=component, experiment=experiment, configuration=configuration)
					print("Deployments", deployments)
					services = cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
					print("SUT Services", services)
				pods = cluster.getPods(app=app, component=component, experiment=experiment, configuration=configuration)
				if args.verbose:
					print("SUT Pods", pods)
				for pod in pods:
					status = cluster.getPodStatus(pod)
					#print(status)
					apps[configuration][component] = "{pod} ({status})".format(pod='', status=status)
					if pod in pod_labels and 'loaded' in pod_labels[pod]:
						if pod_labels[pod]['loaded'] == 'True':
							#apps[configuration]['loaded'] += "True"
							apps[configuration]['loaded'] = pod_labels[pod]['timeLoading']+' [s]'
						elif 'timeLoadingStart' in pod_labels[pod]:
							apps[configuration]['loaded'] = 'Started at '+pod_labels[pod]['timeLoadingStart']
						#if 'timeLoadingStart' in pod_labels[pod]:
						#	apps[configuration]['loaded'] += ' '+pod_labels[pod]['timeLoadingStart']
						#if 'timeLoadingEnd' in pod_labels[pod]:
						#	apps[configuration]['loaded'] += '-'+pod_labels[pod]['timeLoadingEnd']
						#if 'timeLoading' in pod_labels[pod]:
						#	apps[configuration]['loaded'] += '='+pod_labels[pod]['timeLoading']+'s'
				############
				component = 'worker'
				apps[configuration][component] = ''
				if args.verbose:
					stateful_sets = cluster.getStatefulSets(app=app, component=component, experiment=experiment, configuration=configuration)
					print("Stateful Sets", stateful_sets)
					services = cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
					print("Worker Services", services)
				pods = cluster.getPods(app=app, component=component, experiment=experiment, configuration=configuration)
				if args.verbose:
					print("Worker Pods", pods)
				for pod in pods:
					status = cluster.getPodStatus(pod)
					#print(status)
					apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
				############
				component = 'monitoring'
				apps[configuration][component] = ''
				if args.verbose:
					stateful_sets = cluster.getStatefulSets(app=app, component=component, experiment=experiment, configuration=configuration)
					print("Stateful Sets", stateful_sets)
					services = cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
					print("Monitoring Services", services)
				pods = cluster.getPods(app=app, component=component, experiment=experiment, configuration=configuration)
				if args.verbose:
					print("Monitoring Pods", pods)
				for pod in pods:
					status = cluster.getPodStatus(pod)
					#print(status)
					apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
				############
				component = 'benchmarker'
				apps[configuration][component] = ''
				if args.verbose:
					jobs = cluster.getJobs(app=app, component=component, experiment=experiment, configuration=configuration)
					# status per job
					for job in jobs:
						success = cluster.getJobStatus(job)
						print(job, success)
				# all pods to these jobs
				pods = cluster.getJobPods(app=app, component=component, experiment=experiment, configuration=configuration)
				if args.verbose:
					print("Benchmarker Pods", pods)
				for pod in pods:
					status = cluster.getPodStatus(pod)
					#print(status)
					apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
			#print(apps)
			df = pd.DataFrame(apps)
			df = df.T
			df.sort_index(inplace=True)
			df.index.name = experiment
			#print(df)
			h = [df.index.names[0]] + list(df.columns)
			print(tabulate(df,headers=h, tablefmt="grid", floatfmt=".2f", showindex="always"))
