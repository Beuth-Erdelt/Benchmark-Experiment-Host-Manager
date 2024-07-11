"""
:Date: 2023-02-12
:Version: 0.1
:Authors: Patrick K. Erdelt

Perform TPC-C inspired benchmarks based on HammerDB in a Kubernetes cluster.
Optionally monitoring is actived.
User can also choose some parameters like number of warehouses and request some resources.
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
    description = """Perform TPC-C inspired benchmarks in a Kubernetes cluster.
    Optionally monitoring is actived.
    User can also choose some parameters like number of warehouses and request some resources.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='start sut, also load data or also run the TPC-C queries', choices=['run', 'start', 'load'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MonetDB', 'SingleStore', 'CockroachDB', 'MySQL', 'MariaDB', 'YugabyteDB', 'Kinetica'])
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e', '--experiment', help='sets experiment code for continuing started experiment', default=None)
    #parser.add_argument('-d', '--detached', help='puts most of the experiment workflow inside the cluster', action='store_true')
    parser.add_argument('-m', '--monitoring', help='activates monitoring for sut', action='store_true')
    parser.add_argument('-mc', '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms', '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    parser.add_argument('-dt', '--datatransfer', help='activates datatransfer', action='store_true', default=False)
    #parser.add_argument('-md', '--monitoring-delay', help='time to wait [s] before execution of the runs of a query', default=10)
    parser.add_argument('-nr', '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nc', '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne', '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    parser.add_argument('-nvu', '--num-virtual-users', help='space separated list of number of virtual users for HammerDB', default="1")
    parser.add_argument('-nrt', '--num-rampup-time', help='Rampup time in minutes', default=2)
    parser.add_argument('-nbp', '--num-benchmarking-pods', help='comma separated list of  number of benchmarkers per configuration', default="1")
    parser.add_argument('-sf', '--scaling-factor', help='scaling factor (SF) = number of warehouses', default=1)
    parser.add_argument('-su', '--scaling-users', help='comma separated list of number of users for loading', default="1")
    parser.add_argument('-sd', '--scaling-duration', help='scaling factor = duration in minutes', default=5)
    parser.add_argument('-t', '--timeout', help='timeout for a run of a query', default=180)
    parser.add_argument('-rr', '--request-ram', help='request ram', default='16Gi')
    parser.add_argument('-rc', '--request-cpu', help='request cpus', default='4')
    parser.add_argument('-rct', '--request-cpu-type', help='request node having node label cpu=', default='')
    parser.add_argument('-rg', '--request-gpu', help='request number of gpus', default=1)
    parser.add_argument('-rgt', '--request-gpu-type', help='request node having node label gpu=', default='a100')
    parser.add_argument('-rst', '--request-storage-type', help='request persistent storage of certain type', default=None, choices=[None, '', 'local-hdd', 'shared'])
    parser.add_argument('-rss', '--request-storage-size', help='request persistent storage of certain size', default='10Gi')
    parser.add_argument('-rnn', '--request-node-name', help='request a specific node', default=None)
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
    scaling_users = str(args.scaling_users)
    if len(scaling_users) > 0:
        list_scaling_users = scaling_users.split(",")
        list_scaling_users = [int(x) for x in list_scaling_users]
    SD = str(args.scaling_duration)
    timeout = int(args.timeout)
    numRun = int(args.num_run)
    num_experiment_to_apply = int(args.num_config)
    #num_virtual_users = args.num_virtual_users
    num_rampup = args.num_rampup_time
    num_virtual_users = args.num_virtual_users
    if len(num_virtual_users) > 0:
        num_virtual_users = num_virtual_users.split(" ")
        num_virtual_users_list = [int(x) for x in num_virtual_users]
    num_benchmarking_pods = args.num_benchmarking_pods
    if len(num_benchmarking_pods) > 0:
        num_benchmarking_pods = num_benchmarking_pods.split(",")
        list_benchmarking_pods = [int(x) for x in num_benchmarking_pods]
        #print(list_benchmarking_pods)
    cpu = str(args.request_cpu)
    memory = str(args.request_ram)
    cpu_type = str(args.request_cpu_type)
    gpu_type = str(args.request_gpu_type)
    gpus = str(args.request_gpu)
    request_storage_type = args.request_storage_type
    request_storage_size = args.request_storage_size
    request_node_name = args.request_node_name
    datatransfer = args.datatransfer
    test_result = args.test_result
    code = args.experiment
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
    experiment = experiments.tpcc(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    if mode == 'run':
        # we want all TPC-C queries
        #experiment.set_queries_full()
        experiment.set_workload(
            name = 'HammerDB Workload SF={} (warehouses for TPC-C)'.format(SF),
            info = 'This experiment compares run time and resource consumption of TPC-C queries in different DBMS.',
            defaultParameters = {'SF': SF}
        )
    else:
        # we want to profile the import
        #experiment.set_queries_profiling()
        experiment.set_workload(
            name = 'TPC-C Data Profiling PostgreSQL SF='+str(SF),
            info = 'This experiment compares importing TPC-C data sets into different DBMS.',
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
        storageConfiguration = 'postgresql-bht'
        )
    cluster.start_dashboard()
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'sut',
            monitoring = 'auxiliary',
            benchmarking = 'sut',
            )
    # note more infos about experiment in workload description
    experiment.workload['info'] = experiment.workload['info']+" TPC-C data is generated and loaded using several threads."
    if len(args.dbms):
        # import is limited to single DBMS
        experiment.workload['info'] = experiment.workload['info']+" Benchmark is limited to DBMS {}.".format(args.dbms)
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="hammerdb_tpcc",
        experiment_design="4",
        warehouses=SF,
        #users_loading=scaling_users,
        #users_benchmarking=str(num_virtual_users),
        )
    # add configs
    experiment.loading_active = True
    experiment.jobtemplate_loading = "jobtemplate-loading-hammerdb.yml"
    experiment.set_experiment(script='Schema')
    for SU in list_scaling_users:               # reinstall for new number of loading threads
        for pods in list_benchmarking_pods:     # reinstall for new number of benchmarking pods
            if args.dbms == "PostgreSQL":
                # PostgreSQL
                name_format = 'PostgreSQL-{cluster}-{users}-{pods}'
                config_name = name_format.format(cluster=cluster_name, users=SU, pods=pods)
                config = configurations.hammerdb(experiment=experiment, docker='PostgreSQL', configuration=config_name, dialect='PostgreSQL', alias='DBMS D')
                #config.num_loading = 1
                config.set_loading_parameters(
                    PARALLEL = SU,
                    SF = SF,
                    HAMMERDB_DURATION = str(SD),
                    HAMMERDB_RAMPUP = str(num_rampup),
                    HAMMERDB_TYPE = "postgresql",
                    HAMMERDB_VUSERS = num_virtual_users#"1 2 4 8 16 32"
                )
                #config.set_loading(parallel=SU, num_pods=SU)
                config.set_loading(parallel=1, num_pods=1)
                """
                config.set_benchmarking_parameters(
                    PARALLEL = int(pods),
                    SF = SF,
                    HAMMERDB_DURATION = str(SD),
                    HAMMERDB_RAMPUP = str(num_rampup),
                    HAMMERDB_TYPE = "postgresql",
                    HAMMERDB_VUSERS = virtual_users
                    )
                config.add_benchmark_list([int(pods)])
                """
                for virtual_users in num_virtual_users_list:
                    config.add_benchmarking_parameters(
                        PARALLEL = SU,
                        SF = SF,
                        HAMMERDB_DURATION = str(SD),
                        HAMMERDB_RAMPUP = str(num_rampup),
                        HAMMERDB_TYPE = "postgresql",
                        HAMMERDB_VUSERS = int(virtual_users/pods),
                        )
                config.add_benchmark_list([pods]*len(num_virtual_users_list))
            if args.dbms == "MySQL":
                # MySQL
                name_format = 'MySQL-{cluster}-{users}'
                config_name = name_format.format(cluster=cluster_name, users=SU)
                config = configurations.hammerdb(experiment=experiment, docker='MySQL', configuration=config_name, dialect='MySQL', alias='DBMS D')
                #config.num_loading = 1
                config.set_loading_parameters(
                    PARALLEL = SU,
                    SF = SF,
                    HAMMERDB_DURATION = str(SD),
                    HAMMERDB_RAMPUP = str(num_rampup),
                    HAMMERDB_TYPE = "mysql",
                    HAMMERDB_VUSERS = num_virtual_users,#"1 2 4 8 16 32"
                    HAMMERDB_MYSQL_ENGINE = 'innodb',#'BLACKHOLE',#'memory',
                    USER = "root",
                    PASSWORD = "root",
                )
                #config.set_loading(parallel=SU, num_pods=SU)
                config.set_loading(parallel=1, num_pods=1)
                for virtual_users in num_virtual_users_list:
                    config.add_benchmarking_parameters(
                        PARALLEL = SU,
                        SF = SF,
                        HAMMERDB_DURATION = str(SD),
                        HAMMERDB_RAMPUP = str(num_rampup),
                        HAMMERDB_TYPE = "mysql",
                        HAMMERDB_VUSERS = virtual_users,
                        HAMMERDB_MYSQL_ENGINE = 'innodb',#'BLACKHOLE',#'memory',
                        USER = "root",
                        PASSWORD = "root",
                        )
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
        # configure number of clients per config
        #list_clients = args.num_query_executors.split(",")
        #if len(list_clients) > 0:
        #    list_clients = [int(x) for x in list_clients]
        #experiment.add_benchmark_list(list_clients)
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
        experiment.show_summary()
exit()
