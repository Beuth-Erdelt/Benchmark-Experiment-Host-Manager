"""
:Date: 2023-01-25
:Version: 1.0
:Authors: Patrick K. Erdelt

Performs a TPC-H loading experiment.
Data is generated and stored in a distributed filesystem (Ceph).
Last character in each line of generated data is removed.
Data is then loaded from filesystem.
Loading pods are synched.
Different numbers of parallel loaders can be compared.
It can verified that all databases contain the same data, using short profiling (only keys).
Monitoring is activated.
Optionally we set some indexes and constraints after import.
Nodes can be fixed.

nohup python experiment-2-3-tpch-loading-filesystem.py profiling \
    -dbms PostgreSQL \
    -t 600 \
    -sf 100 \
    -dt \
    -nlp 4,8,16,32 \
    -ms 1 \
    -m \
    -nr 1 \
    -nc 1 \
    -ne 1 \
    -db \
    -cx perdelt \
    -rnn cl-worker21 \
    -tr \
    &>logs/experiment.2.2.SF100.PostgreSQL.1.log &
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
    description = """Performs a TPC-H loading experiment. Data is generated and imported into a DBMS from a distributed filesystem."""
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['profiling', 'run', 'start', 'load', 'empty'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MonetDB', 'SingleStore', 'CockroachDB', 'MySQL', 'MariaDB', 'YugabyteDB', 'Kinetica'])
    parser.add_argument('-lit', '--limit-import-table', help='limit import to one table, name of this table', default='')
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
    parser.add_argument('-nls', '--num-loading-split', help='portion of loaders that should run in parallel', default="1")
    parser.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default="1")
    parser.add_argument('-nlt', '--num-loading-threads', help='total number of threads per loading process', default="1")
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
    parser.add_argument('-tr', '--test-result', help='test if result fulfills some basic requirements', action='store_true', default=False)
    parser.add_argument('-ii', '--init-indexes', help='adds indexes to tables after ingestion', action='store_true', default=False)
    parser.add_argument('-ic', '--init-constraints', help='adds constraints to tables after ingestion', action='store_true', default=False)
    parser.add_argument('-is', '--init-statistics', help='recomputes statistics of tables after ingestion', action='store_true', default=False)
    parser.add_argument('-rcp', '--recreate-parameter', help='recreate parameter for randomized queries', default=None)
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
    #num_loading = int(args.num_loading)
    num_loading_split = args.num_loading_split
    if len(num_loading_split) > 0:
        num_loading = num_loading_split.split(",")
        list_loading_split = [int(x) for x in num_loading]
    #num_loading_pods = int(args.num_loading_pods)
    num_loading_pods = args.num_loading_pods
    if len(num_loading_pods) > 0:
        num_loading_pods = num_loading_pods.split(",")
        list_loading_pods = [int(x) for x in num_loading_pods]
    #num_loading_threads = int(args.num_loading_threads)
    num_loading_threads = args.num_loading_threads
    if len(num_loading_threads) > 0:
        num_loading_threads = num_loading_threads.split(",")
        list_loading_threads = [int(x) for x in num_loading_threads]
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
    recreate_parameter = args.recreate_parameter
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
            sut = 'sut',
            loading = 'auxiliary',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # new loading in cluster
    experiment.loading_active = True
    experiment.use_distributed_datasource = True
    experiment.set_experiment(script='Schema')
    # optionally set some indexes and constraints after import
    if init_indexes or init_constraints or init_statistics:
        experiment.set_experiment(indexing='Index')
        if init_constraints:
            experiment.set_experiment(indexing='Index_and_Constraints')
        if init_statistics:
            experiment.set_experiment(indexing='Index_and_Constraints_and_Statistics')
    #experiment.set_experiment(script='Schema', indexing='Index')
    # note more infos about experiment in workload description
    experiment.workload['info'] = experiment.workload['info']+" TPC-H data is loaded from a filesystem using several processes."
    if len(limit_import_table):
        # import is limited to single table
        experiment.workload['info'] = experiment.workload['info']+" Import is limited to table {}.".format(limit_import_table)
    if len(args.dbms):
        # import is limited to single DBMS
        experiment.workload['info'] = experiment.workload['info']+" Import is limited to DBMS {}.".format(args.dbms)
    if len(list_loading_split):
        # import uses several processes in pods
        experiment.workload['info'] = experiment.workload['info']+" Import is handled by {} processes.".format(num_loading_split)
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="benchmarking-tpx",
        experiment_design="2-4"
        )
    # add configs
    for loading_pods_split in list_loading_split: # should be a number of splits, e.g. 4 for 1/4th of all pods
        for loading_pods_total in list_loading_pods: # number of loading pods in total
            # split number of loading pods into parallel potions
            if loading_pods_total < loading_pods_split:
                # thats not possible
                continue
            # how many in parallel?
            split_portion = int(loading_pods_total/loading_pods_split)
            if args.dbms == "PostgreSQL":
                # PostgreSQL
                name_format = 'PostgreSQL-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='PostgreSQL', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='PostgreSQL', alias='DBMS A2')
                config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            elif args.dbms == "MonetDB":
                # MonetDB
                name_format = 'MonetDB-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='MonetDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='MonetDB', alias='DBMS A1')
                config.jobtemplate_loading = "jobtemplate-loading-tpch-MonetDB.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            elif args.dbms == "CockroachDB":
                # CockroachDB
                num_worker = 3
                num_worker_replicas = 1
                name_format = 'CockroachDB-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='CockroachDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), alias='DBMS CN', worker=num_worker)
                config.jobtemplate_loading = "jobtemplate-loading-tpch-CockroachDB.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
                config.set_ddl_parameters(num_replicas=str(num_worker_replicas))
            elif args.dbms == "SingleStore":
                # SingleStore
                name_format = 'SingleStore-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='SingleStore', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='MySQL', alias='DBMS A3')
                config.jobtemplate_loading = "jobtemplate-loading-tpch-SingleStore.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            elif args.dbms == "MariaDB":
                # MariaDB
                name_format = 'MariaDB-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='MariaDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='MySQL', alias='DBMS A1')
                config.jobtemplate_loading = "jobtemplate-loading-tpch-MariaDB.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    TRANSFORM_RAW_DATA = 1,
                    MYSQL_LOADING_FROM = "LOCAL",
                    TPCH_TABLE = limit_import_table,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            elif args.dbms == "Kinetica":
                # Kinetica
                name_format = 'Kinetica-{cluster}-{pods}'
                config = configurations.kinetica(experiment=experiment, docker='Kinetica', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='PostgreSQL', alias='DBMS A2')
                config.jobtemplate_loading = "jobtemplate-loading-tpch-Kinetica.yml"
                config.set_loading_parameters(
                    SF = SF,
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    STORE_RAW_DATA = 1,
                    STORE_RAW_DATA_RECREATE = 0,
                    BEXHOMA_SYNCH_LOAD = 1,
                    TRANSFORM_RAW_DATA = 1,
                    TPCH_TABLE = limit_import_table,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    BEXHOMA_HOST = 'bexhoma-kinetica-worker-0.kinetica-workers', # fixed for worker nodes
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            elif args.dbms == "MySQL":
                # MySQL
                for threads in list_loading_threads:
                    name_format = 'MySQL-{cluster}-{pods}-{threads}'
                    config = configurations.default(experiment=experiment, docker='MySQL', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion, threads=threads), dialect='MySQL', alias='DBMS A1')
                    config.jobtemplate_loading = "jobtemplate-loading-tpch-MySQL.yml"
                    config.set_loading_parameters(
                        SF = SF,
                        PODS_TOTAL = str(loading_pods_total),
                        PODS_PARALLEL = str(split_portion),
                        STORE_RAW_DATA = 1,
                        STORE_RAW_DATA_RECREATE = 0,
                        BEXHOMA_SYNCH_LOAD = 1,
                        TRANSFORM_RAW_DATA = 1,
                        MYSQL_LOADING_THREADS = int(threads),#int(num_loading_threads),#int(loading_pods_total),
                        MYSQL_LOADING_PARALLEL = 1, # not possible from RAM disk, only filesystem
                        TPCH_TABLE = limit_import_table,
                        DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                        )
                    config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            elif args.dbms == "YugabyteDB":
                # YugabyteDB
                for threads in list_loading_threads:
                    name_format = 'YugabyteDB-{cluster}-{pods}-{threads}'
                    config = configurations.default(experiment=experiment, docker='YugabyteDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion, threads=threads), dialect='PostgreSQL', alias='DBMS A1')
                    config.jobtemplate_loading = "jobtemplate-loading-tpch-YugabyteDB.yml"
                    config.servicename_sut = "yb-tserver-service"
                    config.set_loading_parameters(
                        SF = SF,
                        PODS_TOTAL = str(loading_pods_total),
                        PODS_PARALLEL = str(split_portion),
                        STORE_RAW_DATA = 1,
                        STORE_RAW_DATA_RECREATE = 0,
                        BEXHOMA_SYNCH_LOAD = 1,
                        TRANSFORM_RAW_DATA = 1,
                        YUGABYTE_LOADING_THREADS = int(threads),#16,#int(num_loading_threads),#int(loading_pods_total),
                        YUGABYTE_LOADING_PARALLEL = 0, # per table (=1) or per file (=0)
                        TPCH_TABLE = limit_import_table,
                        DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                        )
                    config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
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
