"""
:Date: 2021-02-12
:Version: 0.1
:Authors: Patrick Erdelt

Perform TPC-DS inspired benchmarks in a Kubernetes cluster.
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
from timeit import default_timer
import datetime


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

def do_benchmark():
	description = """Perform TPC-DS inspired benchmarks in a Kubernetes cluster.
	This either profiles the imported data in several DBMS and compares some statistics, or runs the TPC-DS queries.
	Optionally monitoring is actived.
	User can choose to detach the componenten of the benchmarking system, so that as much as possible is run inside a Kubernetes (K8s) cluster.
	User can also choose some parameters like number of runs per query and configuration and request some resources.
	"""
	# argparse
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('mode', help='profile the import of TPC-DS data, or run the TPC-DS queries, or start DBMS and load data, or just start the DBMS', choices=['profiling', 'run', 'start', 'load'])
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
	num_experiment_to_apply = int(args.num_config)
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
	experiment = experiments.tpcds(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
	if mode == 'run':
		# we want all TPC-H queries
		experiment.set_queries_full()
		experiment.set_workload(
			name = 'TPC-DS Queries SF='+str(SF),
			info = 'This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.'
		)
	else:
		# we want to profile the import
		experiment.set_queries_profiling()
		experiment.set_workload(
			name = 'TPC-DS Data Profiling SF='+str(SF),
			info = 'This experiment compares imported TPC-DS data sets in different DBMS.'
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
	config = configurations.default(experiment=experiment, docker='MonetDB', configuration='MonetDB-{}'.format(cluster_name), alias='DBMS A', dialect='MonetDB')
	#config = configurations.default(experiment=experiment, docker='MemSQL', configuration='MemSQL-{}'.format(cluster_name), alias='DBMS B', dialect='MonetDB')
	#config = configurations.default(experiment=experiment, docker='MariaDB', configuration='MariaDB-{}'.format(cluster_name), alias='DBMS C')
	config = configurations.default(experiment=experiment, docker='PostgreSQL', configuration='PostgreSQL-{}'.format(cluster_name), alias='DBMS D', dialect='MonetDB')
	#config = configurations.default(experiment=experiment, docker='Citus', configuration='Citus-{}'.format(cluster_name), alias='DBMS E', dialect='OmniSci')
	#config = configurations.default(experiment=experiment, docker='MySQL', configuration='MySQL-{}'.format(cluster_name), alias='DBMS F')
	#config = configurations.default(experiment=experiment, docker='MariaDBCS', configuration='MariaDBCS-{}'.format(cluster_name), alias='DBMS G')
	#config = configurations.default(experiment=experiment, docker='Exasol', configuration='Exasol-{}'.format(cluster_name), alias='DBMS H')
	#config = configurations.default(experiment=experiment, docker='DB2', configuration='DB2-{}'.format(cluster_name), alias='DBMS I')
	#config = configurations.default(experiment=experiment, docker='SAPHANA', configuration='SAPHANA-{}'.format(cluster_name), alias='DBMS J', dialect='MonetDB')
	#config = configurations.default(experiment=experiment, docker='Clickhouse', configuration='Clickhouse-{}'.format(cluster_name), alias='DBMS K')
	#config = configurations.default(experiment=experiment, docker='SQLServer', configuration='SQLServer-{}'.format(cluster_name), alias='DBMS L')
	#config = configurations.default(experiment=experiment, docker='OmniSci', configuration='OmniSci-{}'.format(cluster_name) alias='DBMS M')
	if args.mode == 'start':
		experiment.start_sut()
	elif args.mode == 'load':
		# start all DBMS
		experiment.start_sut()
		# configure number of clients per config = 0
		list_clients = []
		# total time of experiment
		experiment.add_benchmark_list(list_clients)
		start = default_timer()
		start_datetime = str(datetime.datetime.now())
		print("Experiment starts at {} ({})".format(start_datetime, start))
		# run workflow
		experiment.work_benchmark_list(stop=False)
		# total time of experiment
		end = default_timer()
		end_datetime = str(datetime.datetime.now())
		duration_experiment = end - start
		print("Experiment ends at {} ({}): {}s total".format(end_datetime, end, duration_experiment))
	else:
		# configure number of clients per config
		list_clients = args.num_query_executors.split(",")
		if len(list_clients) > 0:
			list_clients = [int(x) for x in list_clients]
		experiment.add_benchmark_list(list_clients)
		# total time of experiment
		start = default_timer()
		start_datetime = str(datetime.datetime.now())
		print("Experiment starts at {} ({})".format(start_datetime, start))
		# run workflow
		experiment.work_benchmark_list(stop=True)
		# total time of experiment
		end = default_timer()
		end_datetime = str(datetime.datetime.now())
		duration_experiment = end - start
		print("Experiment ends at {} ({}): {}s total".format(end_datetime, end, duration_experiment))
		##################
		experiment.evaluate_results()
		experiment.stop_benchmarker()
		experiment.stop_sut()
		cluster.stop_dashboard()
		cluster.start_dashboard()
		# OOM? exit code 137
		#experiment.zip()
	exit()