"""
CLI entry point for HammerDB TPC-C benchmarks in a Kubernetes cluster.

Runs TPC-C workloads via HammerDB. Supports optional monitoring and
configurable parameters such as number of warehouses and resource requests.

Authors: Patrick K. Erdelt
Copyright (C) 2023 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import *
from bexhoma.cli_args import make_base_parser
from dbmsbenchmarker import *
import logging
import urllib3
import argparse
import time
from timeit import default_timer
import datetime
import math


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Perform TPC-C inspired benchmarks in a Kubernetes cluster.
    Optionally monitoring is actived.
    User can also choose some parameters like number of warehouses and request some resources.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='start sut, also load data or also run the TPC-C queries', choices=['run', 'start', 'load', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MySQL', 'MariaDB', 'Citus'], default=[], nargs='*')
    parser.add_argument('-dt',   '--datatransfer', help='activates datatransfer', action='store_true', default=False)
    parser.add_argument('-nr',   '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nrt',  '--num-rampup-time', help='Rampup time in minutes', default=2)
    parser.add_argument('-sd',   '--scaling-duration', help='scaling factor = duration in minutes', default=5)
    parser.add_argument('-xlat', '--extra-latency', help='also log latencies', action='store_true', default=False)
    parser.add_argument('-xkey', '--extra-keying', help='activate keying and waiting time', action='store_true', default=False)
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
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
    # how many workers (for distributed dbms)
    num_worker = int(args.num_worker)
    num_worker_replicas = int(args.num_worker_replicas)
    num_worker_shards = int(args.num_worker_shards)
    ##############
    ### specific to: Benchbase
    ##############
    SD = str(args.scaling_duration)
    num_rampup = args.num_rampup_time
    extra_latency = int(args.extra_latency)
    if extra_latency:
        HAMMERDB_TIMEPROFILE = "true"
    else:
        HAMMERDB_TIMEPROFILE = "false"
    extra_keying = int(args.extra_keying)
    if extra_keying:
        HAMMERDB_KEYANDTHINK = "true"
    else:
        HAMMERDB_KEYANDTHINK = "false"
    ##############
    ### set cluster
    ##############
    aws = args.aws
    if aws:
        cluster = clusters.AWS(context=args.context)
        # scale up
        node_sizes = {
            'auxiliary': 1,
            'sut-mid': 1,
            'benchmarker': 1
        }
        #cluster.scale_nodegroups(node_sizes)
    else:
        cluster = clusters.Kubernetes(context=args.context)
    cluster_name = cluster.contextdata['clustername']
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.tpcc(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    # set node groups for components
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'sut',
            monitoring = 'auxiliary',
            benchmarking = 'sut',
            )
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="hammerdb_tpcc",
        experiment_design="4",
        warehouses=SF,
        #users_loading=scaling_users,
        #users_benchmarking=str(num_virtual_users),
        )
    experiment.set_default_loading_parameters(
        SF = SF,
        HAMMERDB_DURATION = str(SD),
        HAMMERDB_RAMPUP = str(num_rampup),
        HAMMERDB_KEYANDTHINK = HAMMERDB_KEYANDTHINK,
        HAMMERDB_TIMEPROFILE = HAMMERDB_TIMEPROFILE,
        HAMMERDB_NUM_VU = 1,
    )
    experiment.set_default_benchmarking_parameters(
        SF = SF,
        BEXHOMA_SYNCH_LOAD = 1,
        HAMMERDB_DURATION = str(SD),
        HAMMERDB_RAMPUP = str(num_rampup),
        HAMMERDB_KEYANDTHINK = HAMMERDB_KEYANDTHINK,
        HAMMERDB_TIMEPROFILE = HAMMERDB_TIMEPROFILE,
    )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_threads in num_loading_threads:#[8]:#[64]:
        for loading_pods in [1]:#num_loading_pods:#[1,2]:#[1,8]:#range(2,5):
            loading_threads_per_pod = int(loading_threads/loading_pods)
            if ("PostgreSQL" in args.dbms or len(args.dbms) == 0):
                # PostgreSQL
                name_format = 'PostgreSQL-{cluster}-{users}-{pods}'
                config_name = name_format.format(cluster=cluster_name, users=loading_threads_per_pod, pods=loading_pods)
                #, configuration=config_name
                config = configurations.default(experiment=experiment, docker='PostgreSQL', dialect='PostgreSQL', alias='DBMS D')
                config.set_storage(
                    storageConfiguration = 'postgresql'
                )
                config.set_loading_parameters(
                    HAMMERDB_TYPE = "postgresql",
                    HAMMERDB_VUSERS = loading_threads_per_pod,
                )
                config.set_loading(parallel=1, num_pods=1)
                executor_list = []
                for factor_benchmarking in [1]:#num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                    benchmarking_target = 1#target_base*factor_benchmarking#4*4096*t
                    for benchmarking_threads in num_benchmarking_threads:
                        for benchmarking_pods in num_benchmarking_pods:#[1,2]:#[1,8]:#range(2,5):
                            for num_executor in list_clients:
                                benchmarking_pods_scaled = num_executor*benchmarking_pods
                                benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                """
                                print("benchmarking_target", benchmarking_target)
                                print("benchmarking_pods", benchmarking_pods)
                                print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                print("benchmarking_threads", benchmarking_threads)
                                print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                """
                                executor_list.append(benchmarking_pods_scaled)
                                config.add_benchmarking_parameters(
                                    HAMMERDB_NUM_VU = str(benchmarking_pods_scaled),
                                    HAMMERDB_TYPE = "postgresql",
                                    HAMMERDB_VUSERS = benchmarking_threads_per_pod,
                                    )
                #print(executor_list)
                config.add_benchmark_list(executor_list)
            if ("MySQL" in args.dbms or len(args.dbms) == 0):
                # MySQL
                name_format = 'MySQL-{cluster}-{users}-{pods}'
                config_name = name_format.format(cluster=cluster_name, users=loading_threads_per_pod, pods=loading_pods)
                #, configuration=config_name
                config = configurations.default(experiment=experiment, docker='MySQL', dialect='MySQL', alias='DBMS D')
                config.set_storage(
                    storageConfiguration = 'mysql'
                )
                #config.num_loading = 1
                config.set_loading_parameters(
                    HAMMERDB_TYPE = "mysql",
                    HAMMERDB_VUSERS = loading_threads_per_pod,
                    HAMMERDB_MYSQL_ENGINE = 'innodb',#'BLACKHOLE',#'memory',
                )
                config.set_loading(parallel=1, num_pods=1)
                executor_list = []
                for factor_benchmarking in [1]:#num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                    benchmarking_target = 1#target_base*factor_benchmarking#4*4096*t
                    for benchmarking_threads in num_benchmarking_threads:
                        for benchmarking_pods in num_benchmarking_pods:#[1,2]:#[1,8]:#range(2,5):
                            for num_executor in list_clients:
                                benchmarking_pods_scaled = num_executor*benchmarking_pods
                                benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                """
                                print("benchmarking_target", benchmarking_target)
                                print("benchmarking_pods", benchmarking_pods)
                                print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                print("benchmarking_threads", benchmarking_threads)
                                print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                """
                                executor_list.append(benchmarking_pods_scaled)
                                config.add_benchmarking_parameters(
                                    HAMMERDB_NUM_VU = str(benchmarking_pods_scaled),
                                    HAMMERDB_TYPE = "mysql",
                                    HAMMERDB_MYSQL_ENGINE = 'innodb',#'BLACKHOLE',#'memory',
                                    HAMMERDB_VUSERS = benchmarking_threads_per_pod,
                                    )
                #print(executor_list)
                config.add_benchmark_list(executor_list)
            if ("MariaDB" in args.dbms or len(args.dbms) == 0):
                # MariaDB
                name_format = 'MariaDB-{cluster}-{users}-{pods}'
                config_name = name_format.format(cluster=cluster_name, users=loading_threads_per_pod, pods=loading_pods)
                #, configuration=config_name
                config = configurations.default(experiment=experiment, docker='MariaDB', dialect='MariaDB', alias='DBMS D')
                config.set_storage(
                    storageConfiguration = 'mariadb'
                )
                #config.num_loading = 1
                config.set_loading_parameters(
                    HAMMERDB_TYPE = "mariadb",
                    HAMMERDB_VUSERS = loading_threads_per_pod,
                    HAMMERDB_MYSQL_ENGINE = 'innodb',#'BLACKHOLE',#'memory',
                )
                config.set_sut_parameters(
                    MARIADB_DATABASE = "tpcc",
                    )
                config.set_loading(parallel=1, num_pods=1)
                executor_list = []
                for factor_benchmarking in [1]:#num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                    benchmarking_target = 1#target_base*factor_benchmarking#4*4096*t
                    for benchmarking_threads in num_benchmarking_threads:
                        for benchmarking_pods in num_benchmarking_pods:#[1,2]:#[1,8]:#range(2,5):
                            for num_executor in list_clients:
                                benchmarking_pods_scaled = num_executor*benchmarking_pods
                                benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                """
                                print("benchmarking_target", benchmarking_target)
                                print("benchmarking_pods", benchmarking_pods)
                                print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                print("benchmarking_threads", benchmarking_threads)
                                print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                """
                                executor_list.append(benchmarking_pods_scaled)
                                config.add_benchmarking_parameters(
                                    HAMMERDB_NUM_VU = str(benchmarking_pods_scaled),
                                    HAMMERDB_TYPE = "mariadb",
                                    HAMMERDB_MYSQL_ENGINE = 'innodb',#'BLACKHOLE',#'memory',
                                    HAMMERDB_VUSERS = benchmarking_threads_per_pod,
                                    )
                #print(executor_list)
                config.add_benchmark_list(executor_list)
            if ("Citus" in args.dbms or len(args.dbms) == 0):
                # PostgreSQL
                name_format = 'Citus-{cluster}-{users}-{pods}'
                config_name = name_format.format(cluster=cluster_name, users=loading_threads_per_pod, pods=loading_pods)
                #, configuration=config_name
                config = configurations.default(experiment=experiment, docker='Citus', dialect='Citus', alias='DBMS D', worker=num_worker)
                config.set_storage(
                    storageConfiguration = 'citus'
                    )
                config.set_ddl_parameters(
                    num_worker_replicas = num_worker_replicas,
                    num_worker_shards = num_worker_shards,
                    )
                config.set_sut_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    BEXHOMA_SHARDS = num_worker_shards,
                    )
                config.set_eval_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    BEXHOMA_SHARDS = num_worker_shards,
                    BEXHOMA_WORKERS = num_worker
                    )
                if skip_loading:
                    config.loading_deactivated = True
                config.set_loading_parameters(
                    HAMMERDB_TYPE = "citus",
                    HAMMERDB_VUSERS = loading_threads_per_pod,
                    BEXHOMA_USER = "postgres",
                    BEXHOMA_PASSWORD = "password1234",
                    BEXHOMA_DATABASE = "postgres",
                )
                config.set_loading(parallel=1, num_pods=1)
                executor_list = []
                for factor_benchmarking in [1]:#num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                    benchmarking_target = 1#target_base*factor_benchmarking#4*4096*t
                    for benchmarking_threads in num_benchmarking_threads:
                        for benchmarking_pods in num_benchmarking_pods:#[1,2]:#[1,8]:#range(2,5):
                            for num_executor in list_clients:
                                benchmarking_pods_scaled = num_executor*benchmarking_pods
                                benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                """
                                print("benchmarking_target", benchmarking_target)
                                print("benchmarking_pods", benchmarking_pods)
                                print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                print("benchmarking_threads", benchmarking_threads)
                                print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                """
                                executor_list.append(benchmarking_pods_scaled)
                                config.add_benchmarking_parameters(
                                    HAMMERDB_NUM_VU = str(benchmarking_pods_scaled),
                                    HAMMERDB_TYPE = "citus",
                                    HAMMERDB_VUSERS = benchmarking_threads_per_pod,
                                    BEXHOMA_USER = "postgres",
                                    BEXHOMA_PASSWORD = "password1234",
                                    BEXHOMA_DATABASE = "postgres",
                                    )
                #print(executor_list)
                config.add_benchmark_list(executor_list)
                cluster.max_sut = 1 # can only run 1 in same cluster because of fixed stateful set
    ##############
    ### wait for necessary nodegroups to have planned size
    ##############
    if aws:
        #cluster.wait_for_nodegroups(node_sizes)
        pass
    ##############
    ### branch for workflows
    ##############
    experiment.process()
exit()
