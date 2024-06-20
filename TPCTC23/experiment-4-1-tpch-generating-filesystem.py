"""
:Date: 2023-02-12
:Version: 1.0
:Authors: Patrick K. Erdelt

Performs a TPC-H data generating experiment.
Different numbers of parallel loaders (here: generators) are compared.
Monitoring is activated.
This runs on one node fixed in jobtemplate-loading-tpch-NIL.yml.
-> this scales deterministically

nohup python experiment-2-1-tpch-loading.py run \
    -t 600 \
    -sf 100 \
    -dt \
    -nlp 64,32,16,8,4,2,1 \
    -ms 1 \
    -m \
    -nr 1 \
    -nc 1 \
    -ne 1 \
    -db \
    -cx perdelt \
    -rnn cl-worker21 \
    -tr \
    &>logs/experiment.2.1.SF100.1.log &
"""
from bexhoma import *
from dbmsbenchmarker import *
import logging
#import urllib3
import logging
import argparse
import time
from timeit import default_timer
import datetime
# queue
#import redis
import subprocess
import psutil

#urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Performs a TPC-H data generating experiment."""
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['profiling', 'run', 'start', 'load'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e', '--experiment', help='sets experiment code for continuing started experiment', default=None)
    parser.add_argument('-d', '--detached', help='puts most of the experiment workflow inside the cluster', action='store_true')
    parser.add_argument('-m', '--monitoring', help='activates monitoring', action='store_true')
    parser.add_argument('-mc', '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms', '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    parser.add_argument('-dt', '--datatransfer', help='activates datatransfer', action='store_true', default=False)
    parser.add_argument('-md', '--monitoring-delay', help='time to wait [s] before execution of the runs of a query', default=10)
    parser.add_argument('-nr', '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nc', '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne', '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    parser.add_argument('-nl', '--num-loading', help='number of parallel loaders per configuration', default=1)
    parser.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default=1)
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
    parser.add_argument('-syg', '--synch-generation', help='synch all data generating pods of a configuration', default=0)
    parser.add_argument('-syl', '--synch-loading', help='synch all loading pods of a configuration', default=0)
    parser.add_argument('-mls', '--max-loader-size', help='max size of loader RAM in Gb - configurations requiring more RAM will be suspended', default=None)
    parser.add_argument('-tr', '--test-result', help='test if result fulfills some basic requirements', action='store_true', default=False)
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG)
    if args.debug:
        logger_bexhoma = logging.getLogger('bexhoma')
        logger_bexhoma.setLevel(logging.DEBUG)
        logger_loader = logging.getLogger('load_data_asynch')
        logger_loader.setLevel(logging.DEBUG)
    # set parameter
    monitoring = args.monitoring
    monitoring_cluster = args.monitoring_cluster
    mode = str(args.mode)
    SF = str(args.scaling_factor)
    timeout = int(args.timeout)
    numRun = int(args.num_run)
    num_experiment_to_apply = int(args.num_config)
    num_loading = int(args.num_loading)
    num_loading_pods = args.num_loading_pods
    if len(num_loading_pods) > 0:
        num_loading_pods = num_loading_pods.split(",")
        list_loading_pods = [int(x) for x in num_loading_pods]
    cpu = str(args.request_cpu)
    memory = str(args.request_ram)
    cpu_type = str(args.request_cpu_type)
    gpu_type = str(args.request_gpu_type)
    gpus = str(args.request_gpu)
    request_storage_type = args.request_storage_type
    request_storage_size = args.request_storage_size
    request_node_name = args.request_node_name
    synch_generation = args.synch_generation
    synch_loading = args.synch_loading
    datatransfer = args.datatransfer
    test_result = args.test_result
    max_loader_size = args.max_loader_size
    code = args.experiment
    # set cluster
    aws = args.aws
    if aws:
        cluster = clusters.aws(context=args.context)
        # scale up
        node_sizes = {
            'auxiliary': 1,
            'sut-mid': 1,
            'benchmarker': 1
        }
        #cluster.scale_nodegroups(node_sizes)
    else:
        cluster = clusters.kubernetes(context=args.context)
    cluster_name = cluster.contextdata['clustername']
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    experiment = experiments.tpch(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    if mode == 'run':
        # we want all TPC-H queries
        experiment.set_queries_full()
        experiment.set_workload(
            name = 'TPC-H Queries SF='+str(SF),
            info = 'This experiment compares run time and resource consumption of TPC-H queries in different DBMS.',
            defaultParameters = {'SF': SF}
        )
    else:
        # we want to profile the import
        experiment.set_queries_profiling()
        experiment.set_workload(
            name = 'TPC-H Data Profiling SF='+str(SF),
            info = 'This experiment compares imported TPC-H data sets in different DBMS.',
            defaultParameters = {'SF': SF}
        )
    if monitoring:
        # we want to monitor resource consumption
        experiment.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
    else:
        # we want to just run the queries
        experiment.set_querymanagement_quicktest(numRun=numRun, datatransfer=datatransfer)
    if monitoring_cluster:
        # monitor all nodes of cluster (for not missing any component)
        cluster.start_monitoring_cluster()
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
    experiment.set_storage(
        storageClassName = request_storage_type,
        storageSize = request_storage_size,#'100Gi',
        keep = True
        )
    cluster.start_dashboard()
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'auxiliary',
            loading = 'auxiliary',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # new loading in cluster
    experiment.loading_active = True
    experiment.set_experiment(script='Schema')
    experiment.set_queryfile('queries-tpch-empty.config')
    experiment.set_workload(
        name = 'TPC-H Data Generation SF='+str(SF),
        info = 'This experiment compares generation time of TPC-H data. Data is not imported, but stored to disk. Workload just runs a constant query.',
        defaultParameters = {'SF': SF}
    )
    # add configs
    for pods in list_loading_pods:
        # how many in parallel?
        split_portion = pods#int(loading_pods_total/loading_pods_split)
        # max loader size?
        if max_loader_size is not None:
            if int(max_loader_size) < int(SF)/int(split_portion):
                print("{} loader would require too much RAM per loader (more than {})".format(split_portion, max_loader_size))
                continue
        # MonetDB
        name_format = 'MonetDB-NIL-{pods}'
        config = configurations.default(experiment=experiment, docker='MonetDB', configuration=name_format.format(cluster_name=cluster_name, pods=pods), dialect='MonetDB', alias='DBMS A1')
        config.jobtemplate_loading = "jobtemplate-loading-tpch-NIL.yml"
        config.set_loading_parameters(
            PARALLEL = str(pods),
            PODS_PARALLEL = str(pods),
            SF = SF,
            STORE_RAW_DATA = 1,
            STORE_RAW_DATA_RECREATE = 1,
            #BEXHOMA_SYNCH_LOAD = synch_loading,
            TRANSFORM_RAW_DATA = 0,
            BEXHOMA_SYNCH_GENERATE = synch_generation
            )
        config.set_loading(parallel=pods, num_pods=pods)
    # wait for necessary nodegroups to have planned size
    if aws:
        #cluster.wait_for_nodegroups(node_sizes)
        pass
    # branch for workflows
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
        # run workflow
        experiment.work_benchmark_list()
        # total time of experiment
        end = default_timer()
        end_datetime = str(datetime.datetime.now())
        duration_experiment = end - start
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
        experiment.work_benchmark_list()
        # total time of experiment
        end = default_timer()
        end_datetime = str(datetime.datetime.now())
        duration_experiment = end - start
        print("Experiment ends at {} ({}): {}s total".format(end_datetime, end, duration_experiment))
        ##################
        experiment.evaluate_results()
        experiment.stop_benchmarker()
        experiment.stop_sut()
        #experiment.zip() # OOM? exit code 137
        if test_result:
            test_result_code = experiment.test_results()
            if test_result_code == 0:
                print("Test successful!")
        cluster.restart_dashboard()
exit()
