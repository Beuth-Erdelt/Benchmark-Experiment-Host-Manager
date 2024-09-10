"""
:Date: 2023-01-25
:Version: 1.0
:Authors: Patrick K. Erdelt

Performs a TPC-H experiment.
Data is generated and stored in a distributed filesystem (Ceph).
Last character in each line of generated data is removed.
Data is then loaded from filesystem.
Loading pods are synched.
Different numbers of parallel loaders can be compared.
It can verified that all databases contain the same data, using short profiling (only keys).
Monitoring is activated.
Optionally we set some indexes and constraints after import.
Nodes can be fixed.
"""
from bexhoma import *
from dbmsbenchmarker import *
import logging
import urllib3
import logging
import argparse
import time
from timeit import default_timer
import datetime
import subprocess
import psutil

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Performs a TPC-H experiment. Data is generated and imported into a DBMS from a distributed filesystem (shared disk)."""
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['profiling', 'run', 'start', 'load', 'empty', 'summary'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms','--dbms',  help='DBMS', choices=['PostgreSQL', 'MonetDB', 'MySQL', 'MariaDB'], default=[], action='append')
    parser.add_argument('-lit', '--limit-import-table', help='limit import to one table, name of this table', default='')
    parser.add_argument('-db',  '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-cx',  '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e',   '--experiment', help='sets experiment code for continuing started experiment', default=None)
    parser.add_argument('-m',   '--monitoring', help='activates monitoring', action='store_true')
    parser.add_argument('-mc',  '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms',  '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    parser.add_argument('-dt',  '--datatransfer', help='activates transfer of data per query (not only execution)', action='store_true', default=False)
    parser.add_argument('-nr',  '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nc',  '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne',  '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    parser.add_argument('-nls', '--num-loading-split', help='portion of loaders that should run in parallel', default="1")
    parser.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default="1")
    parser.add_argument('-nlt', '--num-loading-threads', help='total number of threads per loading process', default="1")
    parser.add_argument('-nbp', '--num-benchmarking-pods', help='comma separated list of  number of benchmarkers per configuration', default="1")
    parser.add_argument('-nbt', '--num-benchmarking-threads', help='total number of threads per benchmarking process', default="1")
    parser.add_argument('-sf',  '--scaling-factor', help='scaling factor (SF)', default=1)
    parser.add_argument('-t',   '--timeout', help='timeout for a run of a query', default=600)
    parser.add_argument('-rr',  '--request-ram', help='request ram for sut, default 16Gi', default='16Gi')
    parser.add_argument('-rc',  '--request-cpu', help='request cpus for sut, default 4', default='4')
    parser.add_argument('-rct', '--request-cpu-type', help='request node for sut to have node label cpu=', default='')
    parser.add_argument('-rg',  '--request-gpu', help='request number of gpus for sut', default=1)
    parser.add_argument('-rgt', '--request-gpu-type', help='request node for sut to have node label gpu=', default='')
    parser.add_argument('-rst', '--request-storage-type', help='request persistent storage of certain type', default=None, choices=[None, '', 'local-hdd', 'shared'])
    parser.add_argument('-rss', '--request-storage-size', help='request persistent storage of certain size', default='10Gi')
    parser.add_argument('-rnn', '--request-node-name', help='request a specific node for sut', default=None)
    parser.add_argument('-rnl', '--request-node-loading', help='request a specific node for loading pods', default=None)
    parser.add_argument('-rnb', '--request-node-benchmarking', help='request a specific node for benchmarking pods', default=None)
    parser.add_argument('-tr',  '--test-result', help='test if result fulfills some basic requirements', action='store_true', default=False)
    parser.add_argument('-ii',  '--init-indexes', help='adds indexes to tables after ingestion', action='store_true', default=False)
    parser.add_argument('-ic',  '--init-constraints', help='adds constraints to tables after ingestion', action='store_true', default=False)
    parser.add_argument('-is',  '--init-statistics', help='recomputes statistics of tables after ingestion', action='store_true', default=False)
    parser.add_argument('-rcp', '--recreate-parameter', help='recreate parameter for randomized queries', action='store_true', default=False)
    parser.add_argument('-shq', '--shuffle-queries', help='have different orderings per stream', action='store_true', default=False)
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG)
    debugging = int(args.debug)
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
    #num_loading = int(args.num_loading)
    num_loading_split = args.num_loading_split
    if len(num_loading_split) > 0:
        num_loading = num_loading_split.split(",")
        list_loading_split = [int(x) for x in num_loading]
    #num_loading_pods = int(args.num_loading_pods)
    num_loading_pods = args.num_loading_pods
    if len(num_loading_pods) > 0:
        num_loading_pods = num_loading_pods.split(",")
        num_loading_pods = [int(x) for x in num_loading_pods]
    num_loading_threads = args.num_loading_threads
    if len(num_loading_threads) > 0:
        num_loading_threads = num_loading_threads.split(",")
        num_loading_threads = [int(x) for x in num_loading_threads]
    num_benchmarking_pods = args.num_benchmarking_pods
    if len(num_benchmarking_pods) > 0:
        num_benchmarking_pods = num_benchmarking_pods.split(",")
        num_benchmarking_pods = [int(x) for x in num_benchmarking_pods]
    num_benchmarking_threads = args.num_benchmarking_threads
    if len(num_benchmarking_threads) > 0:
        num_benchmarking_threads = num_benchmarking_threads.split(",")
        num_benchmarking_threads = [int(x) for x in num_benchmarking_threads]
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
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
    recreate_parameter = args.recreate_parameter
    shuffle_queries = args.shuffle_queries
    # indexes
    init_indexes = args.init_indexes
    init_constraints = args.init_constraints
    init_statistics = args.init_statistics
    # limit to one table
    limit_import_table = args.limit_import_table
    # start with old experiment?
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
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
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
    elif mode == 'empty':
        # set benchmarking queries to dummy - SELECT 1
        experiment.set_queryfile('queries-tpch-empty.config')
        experiment.set_workload(
            name = 'TPC-H Data Dummy SF='+str(SF),
            info = 'This experiment is for testing loading. It just runs a SELECT 1 query.',
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
        # patch: use short profiling (only keys)
        experiment.set_queryfile('queries-tpch-profiling-keys.config')
    if monitoring_cluster:
        # monitor all nodes of cluster (for not missing any component)
        experiment.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
        cluster.start_monitoring_cluster()
        experiment.workload['info'] = experiment.workload['info']+" System metrics are monitored by a cluster-wide installation."
    elif monitoring:
        # we want to monitor resource consumption
        experiment.set_querymanagement_monitoring(numRun=numRun, delay=10, datatransfer=datatransfer)
        experiment.workload['info'] = experiment.workload['info']+" System metrics are monitored by sidecar containers."
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
    # persistent storage
    experiment.set_storage(
        storageClassName = request_storage_type,
        storageSize = request_storage_size,#'100Gi',
        keep = True
        )
    cluster.start_datadir()
    cluster.start_resultdir()
    cluster.start_dashboard()
    cluster.start_messagequeue()
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'auxiliary',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # new loading in cluster
    experiment.loading_active = True
    experiment.use_distributed_datasource = True
    experiment.set_experiment(script='Schema')
    # note more infos about experiment in workload description
    experiment.workload['info'] = experiment.workload['info']+" TPC-H (SF={}) data is loaded and benchmark is executed.".format(SF)
    if request_storage_type is not None:
        experiment.workload['info'] = experiment.workload['info']+"\nDatabase is persistent on a volume of type {}.".format(request_storage_type)
    if shuffle_queries:
        experiment.workload['info'] = experiment.workload['info']+"\nQuery ordering is as required by the TPC."
    else:
        experiment.workload['info'] = experiment.workload['info']+"\nQuery ordering is Q1 - Q22."
    if recreate_parameter:
        experiment.workload['info'] = experiment.workload['info']+"\nAll instances use different query parameters."
    else:
        experiment.workload['info'] = experiment.workload['info']+"\nAll instances use the same query parameters."
    # optionally set some indexes and constraints after import
    if init_indexes or init_constraints or init_statistics:
        experiment.set_experiment(indexing='Index')
        init_scripts = " Import sets indexes after loading."
        if init_constraints:
            experiment.set_experiment(indexing='Index_and_Constraints')
            init_scripts = "\nImport sets indexes and constraints after loading."
        if init_statistics:
            experiment.set_experiment(indexing='Index_and_Constraints_and_Statistics')
            init_scripts = "\nImport sets indexes and constraints after loading and recomputes statistics."
        experiment.workload['info'] = experiment.workload['info']+init_scripts
    #experiment.set_experiment(script='Schema', indexing='Index')
    if len(limit_import_table):
        # import is limited to single table
        experiment.workload['info'] = experiment.workload['info']+"\nImport is limited to table {}.".format(limit_import_table)
    if len(args.dbms):
        # import is limited to single DBMS
        experiment.workload['info'] = experiment.workload['info']+"\nBenchmark is limited to DBMS {}.".format(", ".join(args.dbms))
    if len(num_loading_pods):
        # import uses several processes in pods
        experiment.workload['info'] = experiment.workload['info']+"\nImport is handled by {} processes (pods).".format(" and ".join(map(str, num_loading_pods)))
    # fix loading
    if not request_node_loading is None:
        experiment.patch_loading(patch="""
        spec:
          template:
            spec:
              nodeSelector:
                kubernetes.io/hostname: {node}
        """.format(node=request_node_loading))
        experiment.workload['info'] = experiment.workload['info']+"\nLoading is fixed to {}.".format(request_node_loading)
    # fix benchmarking
    if not request_node_benchmarking is None:
        experiment.patch_benchmarking(patch="""
        spec:
          template:
            spec:
              nodeSelector:
                kubernetes.io/hostname: {node}
        """.format(node=request_node_benchmarking))
        experiment.workload['info'] = experiment.workload['info']+"\nBenchmarking is fixed to {}.".format(request_node_benchmarking)
    # fix SUT
    if not request_node_name is None:
        experiment.set_resources(
            nodeSelector = {
                'cpu': cpu_type,
                'gpu': '',
                'kubernetes.io/hostname': request_node_name
            })        
        experiment.workload['info'] = experiment.workload['info']+"\nSUT is fixed to {}.".format(request_node_name)
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="tpc-h",
        experiment_design="parallel-loading"
        )
    # add configs
    for loading_pods_split in list_loading_split: # should be a number of splits, e.g. 4 for 1/4th of all pods
        for loading_pods_total in num_loading_pods: # number of loading pods in total
            # split number of loading pods into parallel potions
            if loading_pods_total < loading_pods_split:
                # thats not possible
                continue
            # how many in parallel?
            split_portion = int(loading_pods_total/loading_pods_split)
            if ("PostgreSQL" in args.dbms or len(args.dbms) == 0):
                # PostgreSQL
                name_format = 'PostgreSQL-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='PostgreSQL', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='PostgreSQL', alias='DBMS A2')
                config.set_storage(
                    storageConfiguration = 'postgresql'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    BEXHOMA_SYNCH_GENERATE = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    )
                config.set_benchmarking_parameters(
                    SF = SF,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
                    DBMSBENCHMARKER_DEV = debugging,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MonetDB" in args.dbms or len(args.dbms) == 0):
                # MonetDB
                name_format = 'MonetDB-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='MonetDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='MonetDB', alias='DBMS A1')
                config.set_storage(
                    storageConfiguration = 'monetdb'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-tpch-MonetDB.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    BEXHOMA_SYNCH_GENERATE = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    )
                config.set_benchmarking_parameters(
                    SF = SF,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
                    DBMSBENCHMARKER_DEV = debugging,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MariaDB" in args.dbms or len(args.dbms) == 0):
                # MonetDB
                name_format = 'MariaDB-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='MariaDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='MySQL', alias='DBMS A1')
                config.set_storage(
                    storageConfiguration = 'mariadb'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-tpch-MariaDB.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    BEXHOMA_SYNCH_GENERATE = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    MYSQL_LOADING_FROM = "LOCAL",
                    )
                config.set_benchmarking_parameters(
                    SF = SF,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
                    DBMSBENCHMARKER_DEV = debugging,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MySQL" in args.dbms or len(args.dbms) == 0):
                # MySQL
                for threads in list_loading_threads:
                    name_format = 'MySQL-{cluster}-{pods}-{threads}'
                    config = configurations.default(experiment=experiment, docker='MySQL', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion, threads=threads), dialect='MySQL', alias='DBMS A1')
                    config.set_storage(
                        storageConfiguration = 'mysql'
                        )
                    config.jobtemplate_loading = "jobtemplate-loading-tpch-MySQL.yml"
                    config.set_loading_parameters(
                        SF = SF,
                        PODS_TOTAL = str(loading_pods_total),
                        PODS_PARALLEL = str(split_portion),
                        STORE_RAW_DATA = 1,
                        STORE_RAW_DATA_RECREATE = 0,
                        BEXHOMA_SYNCH_LOAD = 1,
                        BEXHOMA_SYNCH_GENERATE = 1,
                        TRANSFORM_RAW_DATA = 1,
                        MYSQL_LOADING_THREADS = int(threads),#int(num_loading_threads),#int(loading_pods_total),
                        MYSQL_LOADING_PARALLEL = 1, # not possible from RAM disk, only filesystem
                        TPCH_TABLE = limit_import_table,
                        )
                    config.set_benchmarking_parameters(
                        SF = SF,
                        DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                        DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
                        DBMSBENCHMARKER_DEV = debugging,
                        )
                    config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
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
    elif args.mode == 'summary':
        experiment.show_summary()
    else:
        # configure number of clients per config
        #list_clients = args.num_query_executors.split(",")
        #if len(list_clients) > 0:
        #    list_clients = [int(x) for x in list_clients]
        experiment.add_benchmark_list(list_clients)
        # total time of experiment
        start = default_timer()
        start_datetime = str(datetime.datetime.now())
        print("{:30s}: has code {}".format("Experiment",experiment.code))
        print("{:30s}: starts at {} ({})".format("Experiment",start_datetime, start))
        print("{:30s}: {}".format("Experiment",experiment.workload['info']))
        # run workflow
        experiment.work_benchmark_list()
        # total time of experiment
        end = default_timer()
        end_datetime = str(datetime.datetime.now())
        duration_experiment = end - start
        print("{:30s}: ends at {} ({}) - {:.2f}s total".format("Experiment",end_datetime, end, duration_experiment))
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
        experiment.show_summary()
exit()
