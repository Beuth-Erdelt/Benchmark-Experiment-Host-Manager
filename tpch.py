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
import math


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Performs a TPC-H experiment. Data is generated and imported into a DBMS from a distributed filesystem (shared disk)."""
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['profiling', 'run', 'start', 'load', 'empty', 'summary'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms','--dbms',  help='DBMS', choices=['PostgreSQL', 'MonetDB', 'MySQL', 'MariaDB', 'DatabaseService'], default=[], action='append')
    parser.add_argument('-lit', '--limit-import-table', help='limit import to one table, name of this table', default='')
    parser.add_argument('-db',  '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-sl',  '--skip-loading', help='do not ingest, start benchmarking immediately', action='store_true', default=False)
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
    ##############
    ### set parameters
    ##############
    command_args = vars(args)
    ##############
    ### workflow parameters
    ##############
    # start with old experiment?
    code = args.experiment
    # only create testbed or also run a benchmark?
    mode = str(args.mode)
    # scaling of data
    SF = str(args.scaling_factor)
    # timeout of a benchmark
    timeout = int(args.timeout)
    # how often to repeat experiment?
    num_experiment_to_apply = int(args.num_config)
    # should results be tested for validity?
    test_result = args.test_result
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
    # do not ingest, start benchmarking immediately
    skip_loading = args.skip_loading
    ##############
    ### specific to: dbmsbenchmarker TPC-H
    ##############
    # shuffle ordering and random parameters
    recreate_parameter = args.recreate_parameter
    shuffle_queries = args.shuffle_queries
    # limit to one table
    limit_import_table = args.limit_import_table
    ##############
    ### set cluster
    ##############
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
    # limit number of sut
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.tpch(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
    num_loading_split = experiment.get_parameter_as_list('num_loading_split')
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    # set node groups for components
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'auxiliary',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="tpc-h",
        experiment_design="parallel-loading"
    )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_pods_split in num_loading_split: # should be a number of splits, e.g. 4 for 1/4th of all pods
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
                if skip_loading:
                    config.loading_deactivated = True
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
                if skip_loading:
                    config.loading_deactivated = True
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
                # MariaDB
                name_format = 'MariaDB-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='MariaDB', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='MySQL', alias='DBMS A1')
                config.set_storage(
                    storageConfiguration = 'mariadb'
                    )
                if skip_loading:
                    config.loading_deactivated = True
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
                for threads in num_loading_threads:
                    pods_times_threads=int(loading_pods_total)*int(threads)
                    name_format = 'MySQL-{cluster}-{pods_times_threads}'
                    config = configurations.default(experiment=experiment, docker='MySQL', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion, threads=threads, pods_times_threads=pods_times_threads), dialect='MySQL', alias='DBMS A1')
                    config.set_storage(
                        storageConfiguration = 'mysql'
                        )
                    if skip_loading:
                        config.loading_deactivated = True
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
            if ("DatabaseService" in args.dbms):# or len(args.dbms) == 0): # not included per default
                # DatabaseService
                name_format = 'DatabaseService-{cluster}-{pods}'
                config = configurations.default(experiment=experiment, docker='DatabaseService', configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion), dialect='PostgreSQL', alias='DBMS A1')
                config.monitoring_sut = False # cannot be monitored since outside of K8s
                if skip_loading:
                    config.loading_deactivated = True
                config.set_storage(
                    storageConfiguration = 'databaseservice'
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
                    BEXHOMA_HOST = 'bexhoma-service',
                    )
                config.set_benchmarking_parameters(
                    SF = SF,
                    DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
                    DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
                    DBMSBENCHMARKER_DEV = debugging,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
    ##############
    ### wait for necessary nodegroups to have planned size
    ##############
    if aws:
        #cluster.wait_for_nodegroups(node_sizes)
        pass
    ##############
    ### branch for workflows
    ##############
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
        experiment.workload['duration'] = math.ceil(duration_experiment)
        ##################
        experiment.evaluate_results()
        experiment.store_workflow_results()
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
