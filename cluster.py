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


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
	description = """Perform TPC-H inspired benchmarks in a Kubernetes cluster.
	This either profiles the imported data in several DBMS and compares some statistics, or runs the TPC-H queries.
	Optionally monitoring is actived.
	User can choose to detach the componenten of the benchmarking system, so that as much as possible is run inside a Kubernetes (K8s) cluster.
	User can also choose some parameters like number of runs per query and configuration and request some resources.
	"""
	# argparse
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['stop','status'])
	parser.add_argument('-e', '--experiment', help='time to wait [s] before execution of the runs of a query', default=None)
	args = parser.parse_args()
	if args.mode == 'stop':
		cluster = clusters.kubernetes()
		if args.experiment is None:
			experiment = experiments.tpch(cluster=cluster, code=cluster.code)
			cluster.stop_sut()
			cluster.stop_benchmarker()
		else:
			experiment = experiments.tpch(cluster=cluster, code=args.experiment)
			experiment.stop_sut()
	elif args.mode == 'status':
		cluster = clusters.kubernetes()
		app = cluster.appname
		experiment = ''
		configuration = ''
		component = 'sut'
		deployments = cluster.getDeployments(app=app, component=component, experiment=experiment, configuration=configuration)
		print("Deployments", deployments)
		services = cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
		print("Services", services)
		pods = cluster.getPods(app=app, component=component, experiment=experiment, configuration=configuration)
		print("Pods", pods)
		############
		component = 'worker'
		stateful_sets = cluster.getStatefulSets(app=app, component=component, experiment=experiment, configuration=configuration)
		print("Stateful Sets", stateful_sets)
		services = cluster.getServices(app=app, component=component, experiment=experiment, configuration=configuration)
		print("Services", services)
		pods = cluster.getPods(app=app, component=component, experiment=experiment, configuration=configuration)
		print("Pods", pods)
		############
		component = 'benchmarker'
		jobs = cluster.getJobs(app=app, component=component, experiment=experiment, configuration=configuration)
		# status per job
		for job in jobs:
			success = self.cluster.getJobStatus(job)
			print(job, success)
		# all pods to these jobs
		pods = cluster.getJobPods(app=app, component=component, experiment=experiment, configuration=configuration)
