"""
:Date: 2021-02-12
:Version: 0.1
:Authors: Patrick Erdelt

Perform TPC-H inspired benchmarks in a Kubernetes cluster.
This either profiles the imported data in several DBMS and compares some statistics, or runs the TPC-H queries.
Optionally monitoring is actived.
User can choose to detach the componenten of the benchmarking system, so that as much as possible is run inside a Kubernetes (K8s) cluster.
User can also choose some parameters like number of runs per query and configuration and request some resources.
"""
from bexhoma import *
from dbmsbenchmarker import *
#import experiments
import logging
import urllib3
import logging
import argparse
import time


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

def do_benchmark():
	description = """Perform TPC-H inspired benchmarks in a Kubernetes cluster.
	This either profiles the imported data in several DBMS and compares some statistics, or runs the TPC-H queries.
	Optionally monitoring is actived.
	User can choose to detach the componenten of the benchmarking system, so that as much as possible is run inside a Kubernetes (K8s) cluster.
	User can also choose some parameters like number of runs per query and configuration and request some resources.
	"""
	# argparse
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['profiling', 'run'])
	parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
	parser.add_argument('-e', '--experiment', help='sets experiment code for continuing started experiment', default=None)
	parser.add_argument('-d', '--detached', help='puts most of the experiment workflow inside the cluster', action='store_true')
	parser.add_argument('-m', '--monitoring', help='activates monitoring', action='store_true')
	parser.add_argument('-ms', '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
	parser.add_argument('-dt', '--datatransfer', help='activates datatransfer', action='store_true', default=False)
	parser.add_argument('-md', '--monitoring-delay', help='time to wait [s] before execution of the runs of a query', default=10)
	parser.add_argument('-nr', '--num-run', help='number of runs per query', default=1)
	parser.add_argument('-nc', '--num-config', help='number of runs per configuration', default=1)
	parser.add_argument('-ne', '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
	parser.add_argument('-sf', '--scaling-factor', help='scaling factor (SF)', default=1)
	parser.add_argument('-t', '--timeout', help='timeout for a run of a query', default=180)
	parser.add_argument('-rr', '--request-ram', help='request ram', default='16Gi')
	parser.add_argument('-rc', '--request-cpu', help='request cpus', default='4')
	parser.add_argument('-rct', '--request-cpu-type', help='request node having node label cpu=', default='')
	parser.add_argument('-rg', '--request-gpu', help='request number of gpus', default=1)
	parser.add_argument('-rgt', '--request-gpu-type', help='request node having node label gpu=', default='a100')
	parser.add_argument('-rst', '--request-storage-type', help='request persistent storage of certain type', default=None, choices=[None, '', 'local-hdd', 'shared'])
	parser.add_argument('-rss', '--request-storage-size', help='request persistent storage of certain size', default='10Gi')
	parser.add_argument('-rnn', '--request-node-name', help='request a specific node', default=None)
	args = parser.parse_args()
	# set parameter
	monitoring = args.monitoring
	mode = str(args.mode)
	SF = str(args.scaling_factor)
	timeout = int(args.timeout)
	numRun = int(args.num_run)
	numExperiments = int(args.num_config)
	cpu = str(args.request_cpu)
	memory = str(args.request_ram)
	cpu_type = str(args.request_cpu_type)
	gpu_type = str(args.request_gpu_type)
	gpus = str(args.request_gpu)
	request_storage_type = args.request_storage_type
	request_storage_size = args.request_storage_size
	request_node_name = args.request_node_name
	datatransfer = args.datatransfer
	code = args.experiment
	# set cluster
	cluster = clusters.kubernetes(context=args.context)
	cluster_name = cluster.contextdata['clustername']
	if args.max_sut is not None:
		cluster.max_sut = int(args.max_sut)
	# set experiment
	if code is None:
		code = cluster.code
	experiment = experiments.tpch(cluster=cluster, SF=SF, timeout=timeout, detached=True, code=code, numExperiments=numExperiments)
	if mode == 'run':
		# we want all TPC-H queries
		experiment.set_queries_full()
		experiment.set_workload(
			name = 'TPC-H Queries SF='+str(SF),
			info = 'This experiment compares run time and resource consumption of TPC-H queries in different DBMS.'
		)
	else:
		# we want to profile the import
		experiment.set_queries_profiling()
		experiment.set_workload(
			name = 'TPC-H Data Profiling SF='+str(SF),
			info = 'This experiment compares imported TPC-H data sets in different DBMS.'
		)
	if monitoring:
		# we want to monitor resource consumption
		experiment.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
	else:
		# we want to just run the queries
		experiment.set_querymanagement_quicktest(numRun=numRun, datatransfer=datatransfer)
	# set resources for dbms
	experiment.set_resources(
		requests = {
			'cpu': cpu,
			'memory': memory,
			'gpu': 0
		},
		limits = {
			'cpu': 0,
			'memory': 0
		},
		nodeSelector = {
			'cpu': cpu_type,
			'gpu': '',
		})
	if request_node_name is not None:
		experiment.set_resources(
			nodeSelector = {
				'cpu': cpu_type,
				'gpu': '',
				'kubernetes.io/hostname': request_node_name
			})		
	# persistent storage
	print(request_storage_type)
	experiment.set_storage(
		storageClassName = request_storage_type,
		storageSize = request_storage_size,#'100Gi',
		keep = False
		)
	cluster.start_dashboard()
	# add configs
	config = configurations.default(experiment=experiment, docker='MonetDB', alias='DBMS A', numExperiments=1, clients=[1])
	#config = configurations.default(experiment=experiment, docker='MemSQL', alias='DBMS B', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='MariaDB', alias='DBMS C', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='PostgreSQL', alias='DBMS D', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='Citus', alias='DBMS D2', numExperiments=1, dialect='OmniSci', clients=[1])
	config = configurations.default(experiment=experiment, docker='MySQL', alias='DBMS E', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='MariaDBCS', alias='DBMS F', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='Exasol', alias='DBMS G', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='DB2', alias='DBMS H', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='SAPHANA', alias='DBMS I', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='Clickhouse', alias='DBMS J', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='SQLServer', alias='DBMS K', numExperiments=1, clients=[1])
	config = configurations.default(experiment=experiment, docker='OmniSci', alias='DBMS L', numExperiments=1, clients=[1])
	experiment.start_sut()
	list_clients = [1]
	experiment.add_benchmark_list(list_clients)
	# add list to all config
	# test if dbms is running
	# test if data is loaded
	# yes: work on list
	# no: try to load
	experiment.work_benchmark_list()
	experiment.evaluate_results()
	experiment.stop_benchmarker()
	experiment.stop_sut()
	cluster.stop_dashboard()
	cluster.start_dashboard()
	exit()
