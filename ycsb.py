"""
:Date: 2022-11-28
:Version: 0.1
:Authors: Patrick Erdelt
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

if __name__ == '__main__':
    description = """Perform YCSB benchmarks in a Kubernetes cluster.
    Number of rows and operations is SF*100,000.
    Optionally monitoring is activated.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='import YCSB data or run YCSB queries', choices=['run', 'start', 'load'], default='run')
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MonetDB', 'SingleStore', 'CockroachDB', 'MySQL', 'MariaDB', 'YugabyteDB', 'Kinetica'], default='PostgreSQL')
    parser.add_argument('-workload', help='YCSB default workload', choices=['a', 'b', 'c', 'd', 'e', 'f'], default='a')
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e', '--experiment', help='sets experiment code for continuing started experiment', default=None)
    parser.add_argument('-d', '--detached', help='puts most of the experiment workflow inside the cluster', action='store_true')
    parser.add_argument('-m', '--monitoring', help='activates monitoring for sut', action='store_true')
    parser.add_argument('-mc', '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms', '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    parser.add_argument('-dt', '--datatransfer', help='activates datatransfer', action='store_true', default=False)
    parser.add_argument('-md', '--monitoring-delay', help='time to wait [s] before execution of the runs of a query', default=10)
    parser.add_argument('-nr', '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nc', '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne', '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    parser.add_argument('-nl', '--num-loading', help='number of parallel loaders per configuration', default=1)
    parser.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default=[1,8])
    parser.add_argument('-sf', '--scaling-factor', help='scaling factor (SF) = number of rows in millions', default=1)
    parser.add_argument('-su', '--scaling-users', help='scaling factor = number of total threads', default=64)
    parser.add_argument('-sbs', '--scaling-batchsize', help='batch size', default="")
    parser.add_argument('-ltf', '--list-target-factors', help='comma separated list of factors of 16384 ops as target - default range(1,9)', default="1,2,3,4,5,6,7,8")
    parser.add_argument('-tb', '--target-base', help='ops as target, base for factors - default 16384 = 2**14', default="16384")
    parser.add_argument('-t', '--timeout', help='timeout for a run of a query', default=180)
    parser.add_argument('-rr', '--request-ram', help='request ram', default='16Gi')
    parser.add_argument('-rc', '--request-cpu', help='request cpus', default='4')
    parser.add_argument('-rct', '--request-cpu-type', help='request node having node label cpu=', default='')
    parser.add_argument('-rg', '--request-gpu', help='request number of gpus', default=1)
    parser.add_argument('-rgt', '--request-gpu-type', help='request node having node label gpu=', default='a100')
    parser.add_argument('-rst', '--request-storage-type', help='request persistent storage of certain type', default=None, choices=[None, '', 'local-hdd', 'shared'])
    parser.add_argument('-rss', '--request-storage-size', help='request persistent storage of certain size', default='10Gi')
    parser.add_argument('-rnn', '--request-node-name', help='request a specific node', default=None)
    parser.add_argument('-rnl', '--request-node-loading', help='request a specific node', default=None)
    parser.add_argument('-rnb', '--request-node-benchmarking', help='request a specific node', default=None)
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
    SU = int(args.scaling_users)
    target_base = int(args.target_base)
    list_target_factors = args.list_target_factors
    if len(list_target_factors) > 0:
        list_target_factors = list_target_factors.split(",")
        list_target_factors = [int(x) for x in list_target_factors]
    batchsize = args.scaling_batchsize
    timeout = int(args.timeout)
    numRun = int(args.num_run)
    num_experiment_to_apply = int(args.num_config)
    num_loading = int(args.num_loading)
    #num_loading_pods = int(args.num_loading_pods)
    num_loading_pods = args.num_loading_pods
    if len(num_loading_pods) > 0:
        num_loading_pods = num_loading_pods.split(",")
        num_loading_pods = [int(x) for x in num_loading_pods]
    #num_virtual_users = args.num_virtual_users
    cpu = str(args.request_cpu)
    memory = str(args.request_ram)
    cpu_type = str(args.request_cpu_type)
    gpu_type = str(args.request_gpu_type)
    gpus = str(args.request_gpu)
    request_storage_type = args.request_storage_type
    request_storage_size = args.request_storage_size
    request_node_name = args.request_node_name
    request_node_loading = args.request_node_loading
    request_node_benchmarking = args.request_node_benchmarking
    datatransfer = args.datatransfer
    test_result = args.test_result
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
    experiment = experiments.ycsb(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    if mode == 'run':
        # we want all YCSB queries
        #experiment.set_queries_full()
        experiment.set_workload(
            name = 'YCSB SF='+str(SF),
            info = 'This experiment compares run time and resource consumption of YCSB queries.',
            defaultParameters = {'SF': SF}
        )
    else:
        # we want to profile the import
        #experiment.set_queries_profiling()
        experiment.set_workload(
            name = 'YCSB Data Loading SF='+str(SF),
            info = 'This imports YCSB data sets.',
            defaultParameters = {'SF': SF}
        )
    if monitoring_cluster:
        # monitor all nodes of cluster (for not missing any component)
        cluster.start_monitoring_cluster()
    #experiment.set_queryfile('queries-tpcds-profiling-tables.config')
    # set resources for dbms
    #experiment.connectionmanagement['timeout'] = 180
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
            #'kubernetes.io/hostname': 'cl-worker13'
        })
    if request_node_name is not None:
        experiment.set_resources(
            nodeSelector = {
                'cpu': cpu_type,
                'gpu': '',
                'kubernetes.io/hostname': request_node_name
            })        
    # persistent storage
    #print(request_storage_type)
    #if not request_storage_type is None:# and (request_storage_type == 'shared' or request_storage_type == 'local-hdd'):
    experiment.set_storage(
        storageClassName = request_storage_type,
        storageSize = request_storage_size,#'100Gi',
        keep = True,
        storageConfiguration = 'mysql-bht'
        )
    # set node labes for components
    """
    experiment.set_nodes(
        #maintaining = 'auxiliary',
        loading = 'loading',
        sut = 'sut',
        #benchmarking = 'benchmarker',
        )
    """
    cluster.start_dashboard()
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'sut',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # note more infos about experiment in workload description
    experiment.workload['info'] = experiment.workload['info']+" YCSB is performed using several threads and processes."
    if len(args.dbms):
        # import is limited to single DBMS
        experiment.workload['info'] = experiment.workload['info']+" Benchmark is limited to DBMS {}.".format(args.dbms)
    #if len(list_loading_split):
    #    # import uses several processes in pods
    #    experiment.workload['info'] = experiment.workload['info']+" Import is handled by {} processes.".format(num_loading_split)
    # add configs
    experiment.loading_active = True
    experiment.jobtemplate_loading = "jobtemplate-loading-ycsb.yml"
    #experiment.name_format = '{dbms}-{threads}-{pods}-{target}'
    experiment.set_experiment(script='Schema')
    ycsb_rows = int(SF)*1000000 # 1kb each, that is SF is size in GB
    ycsb_operations = int(SF)*1000000
    # note more infos about experiment in workload description
    experiment.workload['info'] = experiment.workload['info']+" YCSB data is loaded using several processes."
    if len(args.dbms):
        # import is limited to single DBMS
        experiment.workload['info'] = experiment.workload['info']+" Benchmark is limited to DBMS {}.".format(args.dbms)
    # fix loading
    if not request_node_loading is None:
        experiment.patch_loading(patch="""
        spec:
          template:
            spec:
              nodeSelector:
                kubernetes.io/hostname: {node}
        """.format(node=request_node_loading))
        experiment.workload['info'] = experiment.workload['info']+" Loading is fixed to {}.".format(request_node_loading)
    # fix benchmarking
    if not request_node_benchmarking is None:
        experiment.patch_benchmarking(patch="""
        spec:
          template:
            spec:
              nodeSelector:
                kubernetes.io/hostname: {node}
        """.format(node=request_node_benchmarking))
        experiment.workload['info'] = experiment.workload['info']+" Benchmarking is fixed to {}.".format(request_node_benchmarking)
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="threads-split",
        experiment_design="1-2",
        ROWS=ycsb_rows,
        OPERATIONS=ycsb_operations,
        workload=args.workload,
        )
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients]
    experiment.add_benchmark_list(list_clients)
    for threads in [SU]:#[8]:#[64]:
        for pods in num_loading_pods:#[1,2]:#[1,8]:#range(2,5):
            #pods = 2**p
            #for t in range(1, 15):#range(1, 2):#range(1, 15):
            for t in list_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                target = target_base*t#4*4096*t
                threads_per_pod = int(threads/pods)
                ycsb_operations_per_pod = int(ycsb_operations/pods)
                target_per_pod = int(target/pods)
                if args.dbms == "PostgreSQL":
                    # PostgreSQL
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'PostgreSQL-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='PostgreSQL', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                elif args.dbms == "MySQL":
                    # MySQL
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'MySQL-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='MySQL', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                elif args.dbms == "MariaDB":
                    # MariaDB
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'MariaDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='MariaDB', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                elif args.dbms == "MonetDB":
                    # MonetDB
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'MonetDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='MonetDB', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                elif args.dbms == "SingleStore":
                    # SingleStore
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'SingleStore-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='SingleStore', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                elif args.dbms == "Kinetica":
                    # Kinetica
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'Kinetica-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='Kinetica', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        #BEXHOMA_HOST = 'bexhoma-worker-0.kinetica-workers', # fixed for worker nodes
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        #BEXHOMA_HOST = 'bexhoma-worker-0.kinetica-workers', # fixed for worker nodes
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                elif args.dbms == "YugabyteDB":
                    # YugabyteDB
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'YugabyteDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='YugabyteDB', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D')
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                elif args.dbms == "CockroachDB":
                    # CockroachDB
                    num_worker = 3
                    num_worker_replicas = 1
                    #name_format = 'PostgreSQL-{}-{}-{}-{}'.format(cluster_name, pods, worker, target)
                    name_format = 'CockroachDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='CockroachDB', configuration=name_format.format(threads=threads, pods=pods, target=target), alias='DBMS D', worker=num_worker)
                    config.set_loading_parameters(
                        PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_loading(parallel=pods, num_pods=pods)
                    #config.set_loading(parallel=num_loading, num_pods=num_loading_pods)
                    config.set_benchmarking_parameters(
                        #PARALLEL = str(pods),
                        SF = SF,
                        YCSB_THREADCOUNT = threads_per_pod,
                        YCSB_TARGET = target_per_pod,
                        YCSB_STATUS = 1,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_WORKLOAD = args.workload,
                        ROWS = ycsb_rows,
                        OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        )
                    config.set_ddl_parameters(num_replicas=str(num_worker_replicas))
                config.add_benchmark_list([pods])
    # wait for necessary nodegroups to have planned size
    if aws:
        #cluster.wait_for_nodegroups(node_sizes)
        pass
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
        #cluster.stop_dashboard()
        #cluster.start_dashboard()
exit()
