"""
CLI entry point for Benchbase TPC-C benchmarks in a Kubernetes cluster.

Runs TPC-C workloads via Benchbase. Supports optional monitoring and
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


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Run Benchbase benchmarks (TPC-C, YCSB, Twitter, CH-Benchmark) against a DBMS in Kubernetes.
    Controls loading concurrency, benchmarking throughput targets, optional connection pooling, and resource allocation.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase: start SUT only, load data, or run the full benchmark', choices=['run', 'start', 'load'])
    parser.add_argument('-dbms', '--dbms', help='one or more DBMS engines to test', choices=['PostgreSQL', 'MySQL', 'MariaDB', 'YugabyteDB', 'CockroachDB', 'TiDB', 'DatabaseService', 'Citus', 'PGBouncer', 'CedarDB'], default=[], nargs='*')
    parser.add_argument('-xnsr',  '--xnum-sut-replicas', help='number of SUT replicas per configuration', default=1, dest='num_sut_replicas')
    parser.add_argument('-xnbf',  '--xnum-benchmarking-target-factors', help='comma-separated multipliers for the benchmarking ops target (target = -xtb × factor)', default="1", dest='num_benchmarking_target_factors')
    parser.add_argument('-xnpp',  '--xnum-pooling-pods', help='comma-separated list of connection-pooler pod counts', default="1", dest='num_pooling_pods')
    parser.add_argument('-xnpi',  '--xnum-pooling-in', help='comma-separated list of max inbound connections per pooler pod', default="", dest='num_pooling_in')
    parser.add_argument('-xnpo',  '--xnum-pooling-out', help='comma-separated list of max outbound connections per pooler pod (to the DBMS)', default="", dest='num_pooling_out')
    parser.add_argument('-xwl',   '--xworkload', help='YCSB workload letter, only used when -xbt ycsb', choices=['a', 'b', 'c', 'd', 'e', 'f', 'c2'], default='a', dest='workload')
    parser.add_argument('-xsd',   '--xscaling-duration', help='benchmark duration in minutes', default=5, dest='scaling_duration')
    parser.add_argument('-xli',   '--xlogging-interval', help='status logging interval in milliseconds (0 = disabled)', default=0, dest='scaling_logging')
    parser.add_argument('-xkey',  '--extra-keying', help='simulate TPC-C keying and think times between transactions', action='store_true', default=False)
    parser.add_argument('-xconn', '--extra-new-connection', help='open a new database connection for every transaction', action='store_true', default=False)
    parser.add_argument('-xbatch','--extra-batchsize', help='number of rows per INSERT batch during loading', default=128)
    parser.add_argument('-xbt',   '--xbenchmark-type', help='Benchbase benchmark suite to run', default='tpcc', choices=['tpcc', 'twitter', 'chbenchmark', 'ycsb'], dest='benchmark')
    parser.add_argument('-xtb',   '--xtarget-base', help='base ops-per-second target; multiply by -xnbf factors to get per-pod target', default="1024", dest='target_base')
    parser.set_defaults(num_worker=1)
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
    num_sut_replicas = int(args.num_sut_replicas)
    ##############
    ### specific to: Benchbase
    ##############
    SD = int(args.scaling_duration)*60
    target_base = int(args.target_base)
    type_of_benchmark = args.benchmark                    # twitter, tpccc, ycsb etc
    scaling_logging = int(args.scaling_logging)*1000      # adjust unit to miliseconds
    extra_keying = int(args.extra_keying)                 # activate key and think time (tpc-c)
    extra_batchsize = int(args.extra_batchsize)           # size of batch for inserts
    if extra_keying:
        BENCHBASE_KEY_AND_THINK = "true"
    else:
        BENCHBASE_KEY_AND_THINK = "false"
    extra_new_connection = int(args.extra_new_connection) # reconnect for every transaction
    if extra_new_connection:
        BENCHBASE_NEWCONNPERTXN = "true"
    else:
        BENCHBASE_NEWCONNPERTXN = "false"
    workload = args.workload                              # workload for ycsb (a, ..., f)
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
    experiment = experiments.benchbase(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.set_benchmark_type(type_of_benchmark)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    num_benchmarking_target_factors = experiment.get_parameter_as_list('num_benchmarking_target_factors')
    num_pooling_pods = experiment.get_parameter_as_list('num_pooling_pods')
    num_pooling_in = experiment.get_parameter_as_list('num_pooling_in')
    num_pooling_out = experiment.get_parameter_as_list('num_pooling_out')
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
        usecase=f"benchbase_{type_of_benchmark}",
        warehouses=SF,
        #users_loading=scaling_users,
        #users_benchmarking=str(num_virtual_users),
        )
    experiment.set_default_loading_parameters(
        SF = SF,
        BENCHBASE_BENCH = type_of_benchmark,
        BENCHBASE_TIME = SD,
        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
        BENCHBASE_BATCHSIZE = extra_batchsize,
        BENCHBASE_STATUS_INTERVAL = scaling_logging,
        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
    )
    experiment.set_default_benchmarking_parameters(
        SF = SF,
        BENCHBASE_BENCH = type_of_benchmark,
        BENCHBASE_TIME = SD,
        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
        BENCHBASE_BATCHSIZE = extra_batchsize,
        BENCHBASE_STATUS_INTERVAL = scaling_logging,
        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
    )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_threads in [1]:                 # always maximum
        for loading_pods in [1]:                # always only 1 pod
            for factor_loading in [1]:          # always maximum
                loading_target = target_base*factor_loading#4*4096*t
                loading_threads_per_pod = int(loading_threads/loading_pods)
                loading_target_per_pod = int(loading_target/loading_pods)
                if ("PostgreSQL" in args.dbms or len(args.dbms) == 0):
                    # PostgreSQL
                    if experiment.tenant_per == 'container':
                        for tenant in range(experiment.num_tenants):
                            name_format = 'PostgreSQL-{threads}-{pods}-{target}-{tenant}'
                            #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target, tenant=tenant)
                            config = configurations.default(experiment=experiment, docker='PostgreSQL', alias='DBMS A')
                            config.set_storage(
                                storageConfiguration = f'postgresql-{tenant}'+"-"+str(config.num_tenants)
                                )
                            config.set_loading_parameters(
                                BENCHBASE_PROFILE = 'postgres',
                                BENCHBASE_TERMINALS = loading_threads_per_pod,
                                BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                                BENCHBASE_YCSB_WORKLOAD = workload,
                                BEXHOMA_TENANT_BY = config.tenant_per,
                                BEXHOMA_TENANT_NUM = config.num_tenants,
                                BEXHOMA_TENANT_ID = tenant,
                                )
                            config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                            config.set_eval_parameters(
                                TENANT_BY = config.tenant_per,
                                TENANT_NUM = config.num_tenants,
                                TENANT_VOL = config.experiment.multi_tenant_volume,
                                TENANT = tenant,
                                )
                            executor_list = []
                            for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                                benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                                BENCHBASE_PROFILE = 'postgres',
                                                BENCHBASE_TARGET = benchmarking_target_per_pod,
                                                BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                                BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                                                BENCHBASE_YCSB_WORKLOAD = workload,
                                                BEXHOMA_TENANT_BY = config.tenant_per,
                                                BEXHOMA_TENANT_NUM = config.num_tenants,
                                                BEXHOMA_TENANT_ID = tenant,
                                                )
                            #print(executor_list)
                            config.add_benchmark_list(executor_list)
                    else:
                        name_format = 'PostgreSQL-{threads}-{pods}-{target}'
                        #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                        config = configurations.default(experiment=experiment, docker='PostgreSQL', alias='DBMS A')
                        if config.tenant_per:
                            config.set_storage(
                                storageConfiguration = 'postgresql-'+config.tenant_per+"-"+str(config.num_tenants)
                                )
                        else:
                            config.set_storage(
                                storageConfiguration = 'postgresql'
                                )
                        config.set_loading_parameters(
                            BENCHBASE_PROFILE = 'postgres',
                            BENCHBASE_TERMINALS = loading_threads_per_pod,
                            BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                            BENCHBASE_YCSB_WORKLOAD = workload,
                            BEXHOMA_TENANT_BY = config.tenant_per,
                            BEXHOMA_TENANT_NUM = config.num_tenants,
                            BEXHOMA_TENANT_ID = 0,
                            )
                        if config.num_tenants > 0:
                            config.set_loading(parallel=loading_pods*config.num_tenants, num_pods=loading_pods*config.num_tenants)
                        else:
                            config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                        if config.tenant_per == 'schema':
                            config.set_experiment(script='Schema_tenant')
                            config.set_experiment(indexing='Checks_tenant')
                        config.set_eval_parameters(
                            TENANT_BY = config.tenant_per,
                            TENANT_NUM = config.num_tenants,
                            TENANT_VOL = config.experiment.multi_tenant_volume,
                            #TENANT = tenant, # not defined here
                            )
                        executor_list = []
                        for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                            benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                            BENCHBASE_PROFILE = 'postgres',
                                            BENCHBASE_TARGET = benchmarking_target_per_pod,
                                            BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                            BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                                            BENCHBASE_YCSB_WORKLOAD = workload,
                                            BEXHOMA_TENANT_BY = config.tenant_per,
                                            BEXHOMA_TENANT_NUM = config.num_tenants,
                                            BEXHOMA_TENANT_ID = 0,
                                            )
                        #print(executor_list)
                        config.add_benchmark_list(executor_list)
                if ("CedarDB" in args.dbms):
                    # PostgreSQL
                    name_format = 'CedarDB-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='CedarDB', alias='DBMS A')
                    config.set_storage(
                        storageConfiguration = 'cedardb'
                        )
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_DATABASE = 'postgres',
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                        BENCHBASE_YCSB_WORKLOAD = workload,
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_DATABASE = 'postgres',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                                        BENCHBASE_YCSB_WORKLOAD = workload,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("PGBouncer" in args.dbms or len(args.dbms) == 0):
                    # PGBouncer
                    if len(num_pooling_in) == 0:
                        num_pooling_in = [int(loading_threads)]
                    if len(num_pooling_out) == 0:
                        num_pooling_out = [int(loading_threads)]
                    for num_c_pods in num_pooling_pods:
                        for num_c_in in num_pooling_in:
                            for num_c_out in num_pooling_out:
                                if len(num_pooling_pods) > 0:
                                    name_format = 'pgb-{threads}-{pooling_pods}-{c_in}-{c_out}'
                                else:
                                    name_format = 'pgb-{threads}-{loading_pods}-{c_in}-{c_out}'
                                # this is too long
                                #name_format = 'PGBouncer-{threads}-{pods}-{target}-{c_in}-{c_out}'
                                #, configuration=name_format.format(threads=loading_threads, loading_pods=loading_pods, pooling_pods=num_c_pods, target=loading_target, c_in=num_c_in, c_out=num_c_out)
                                config = configurations.default(experiment=experiment, docker='PGBouncer', alias='DBMS A')
                                config.path_experiment_docker = 'PostgreSQL'                              # take init scripts of PostgreSQL
                                config.sut_has_pool = True                                                # in particular monitor pool component
                                config.sut_parameters = {
                                    # do not split connections between pool pods:
                                    'DEFAULT_POOL_SIZE': int(num_c_out),                       # max connections to PostgreSQL
                                    'MIN_POOL_SIZE': int(num_c_out),                           # min connections to PostgreSQL
                                    'MAX_CLIENT_CONN': int(num_c_in),                          # max connections to PGBouncer
                                    # split connections between pool pods:
                                    #'DEFAULT_POOL_SIZE': int(num_c_out/num_c_pods),           # max connections to PostgreSQL
                                    #'MIN_POOL_SIZE': int(num_c_out/num_c_pods),               # min connections to PostgreSQL
                                    #'MAX_CLIENT_CONN': int(num_c_in/num_c_pods),              # max connections to PGBouncer
                                }
                                config.set_resources(
                                    replicas_pooling = num_c_pods,
                                )
                                config.set_storage(
                                    storageConfiguration = 'postgresql'
                                    )
                                config.set_loading_parameters(
                                    BENCHBASE_PROFILE = 'postgres',
                                    BEXHOMA_DATABASE = 'postgres',
                                    BENCHBASE_TERMINALS = loading_threads_per_pod,
                                    BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                                    )
                                config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                                executor_list = []
                                for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                                    benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                                    BENCHBASE_PROFILE = 'postgres',
                                                    BEXHOMA_DATABASE = 'postgres',
                                                    BENCHBASE_TARGET = benchmarking_target_per_pod,
                                                    BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                                    BENCHBASE_NEWCONNPERTXN = BENCHBASE_NEWCONNPERTXN,
                                                    )
                                #print(executor_list)
                                config.add_benchmark_list(executor_list)
                if ("MySQL" in args.dbms or len(args.dbms) == 0):
                    # MySQL
                    if experiment.tenant_per == 'container':
                        for tenant in range(experiment.num_tenants):
                            name_format = 'MySQL-{threads}-{pods}-{target}-{tenant}'
                            #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target, tenant=tenant)
                            config = configurations.default(experiment=experiment, docker='MySQL', alias='DBMS A')
                            config.set_storage(
                                storageConfiguration = f'mysql-{tenant}'+"-"+str(config.num_tenants)
                                )
                            config.set_sut_parameters(
                                MYSQL_DATABASE = 'benchbase',
                                )
                            config.set_loading_parameters(
                                BENCHBASE_PROFILE = 'mysql',
                                BEXHOMA_DATABASE = 'benchbase',
                                BENCHBASE_TERMINALS = loading_threads_per_pod,
                                BEXHOMA_TENANT_BY = config.tenant_per,
                                BEXHOMA_TENANT_NUM = config.num_tenants,
                                )
                            config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                            config.set_eval_parameters(
                                TENANT_BY = config.tenant_per,
                                TENANT_NUM = config.num_tenants,
                                TENANT = tenant,
                                TENANT_VOL = config.experiment.multi_tenant_volume,
                                )
                            executor_list = []
                            for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                                benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                                BENCHBASE_PROFILE = 'mysql',
                                                BEXHOMA_DATABASE = 'benchbase',
                                                BENCHBASE_TARGET = benchmarking_target_per_pod,
                                                BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                                BEXHOMA_TENANT_BY = config.tenant_per,
                                                BEXHOMA_TENANT_NUM = config.num_tenants,
                                                )
                            #print(executor_list)
                            config.add_benchmark_list(executor_list)
                    else:
                        name_format = 'MySQL-{threads}-{pods}-{target}'
                        #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                        config = configurations.default(experiment=experiment, docker='MySQL', alias='DBMS A')
                        if config.tenant_per:
                            config.set_storage(
                                storageConfiguration = 'mysql-'+config.tenant_per+"-"+str(config.num_tenants)
                                )
                        else:
                            config.set_storage(
                                storageConfiguration = 'mysql'
                                )
                        config.set_sut_parameters(
                            MYSQL_DATABASE = 'benchbase',
                            )
                        config.set_loading_parameters(
                            BENCHBASE_PROFILE = 'mysql',
                            BEXHOMA_DATABASE = 'benchbase',
                            BENCHBASE_TERMINALS = loading_threads_per_pod,
                            BEXHOMA_TENANT_BY = config.tenant_per,
                            BEXHOMA_TENANT_NUM = config.num_tenants,
                            )
                        if config.num_tenants > 0:
                            config.set_loading(parallel=loading_pods*config.num_tenants, num_pods=loading_pods*config.num_tenants)
                        else:
                            config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                        if config.tenant_per == 'schema':
                            config.set_experiment(script='Schema_tenant')
                            config.set_experiment(indexing='Checks_tenant')
                        config.set_eval_parameters(
                            TENANT_BY = config.tenant_per,
                            TENANT_NUM = config.num_tenants,
                            TENANT_VOL = config.experiment.multi_tenant_volume,
                            #TENANT = tenant, # not defined here
                            )
                        executor_list = []
                        for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                            benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                            BENCHBASE_PROFILE = 'mysql',
                                            BEXHOMA_DATABASE = 'benchbase',
                                            BENCHBASE_TARGET = benchmarking_target_per_pod,
                                            BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                            BEXHOMA_TENANT_BY = config.tenant_per,
                                            BEXHOMA_TENANT_NUM = config.num_tenants,
                                            )
                        #print(executor_list)
                        config.add_benchmark_list(executor_list)
                if ("MariaDB" in args.dbms or len(args.dbms) == 0):
                    # MariaDB
                    name_format = 'MariaDB-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='MariaDB', alias='DBMS A')
                    config.set_storage(
                        storageConfiguration = 'mariadb'
                        )
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'mariadb',
                        BEXHOMA_DATABASE = 'benchbase',
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        )
                    config.set_sut_parameters(
                        MARIADB_DATABASE = "benchbase",
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'mariadb',
                                        BEXHOMA_DATABASE = 'benchbase',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("YugabyteDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # YugabyteDB
                    name_format = 'YugabyteDB-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='YugabyteDB', alias='DBMS D')
                    create_schema = "true"
                    if type_of_benchmark == "tpcc":
                        create_schema = "false"
                    config.monitoring_sut = False # should not be monitored since only dummy
                    config.set_storage(
                        storageConfiguration = 'yugabytedb'
                        )
                    if skip_loading:
                        config.loading_deactivated = True
                    config.sut_service_name = "yb-tserver-service"      # fix service name of SUT, because it is not managed by bexhoma
                    config.sut_pod_name = "yb-tserver-"                 # fix pod name of SUT, because it is not managed by bexhoma
                    config.statefulset_name = 'yb-tserver'              # name of the stateful set of DBMS pods
                    config.sut_container_name = ''                      # fix container name of SUT
                    stateful_set = "yb-tserver"
                    config.deployment_infos['statefulset'] = {}
                    config.deployment_infos['statefulset'][stateful_set] = {}
                    config.deployment_infos['statefulset'][stateful_set]['name'] = stateful_set
                    #config.deployment_infos['statefulset'][stateful_set]['name_service'] = config.get_worker_name(component=stateful_set)
                    config.deployment_infos['statefulset'][stateful_set]['pods'] = [f"{stateful_set}-{i}" for i in range(3)] # self.num_worker
                    config.deployment_infos['statefulset'][stateful_set]['containers'] = []
                    stateful_set = "yb-master"
                    config.deployment_infos['statefulset'][stateful_set] = {}
                    config.deployment_infos['statefulset'][stateful_set]['name'] = stateful_set
                    #config.deployment_infos['statefulset'][stateful_set]['name_service'] = config.get_worker_name(component=stateful_set)
                    config.deployment_infos['statefulset'][stateful_set]['pods'] = [f"{stateful_set}-{i}" for i in range(3)] # self.num_worker
                    config.deployment_infos['statefulset'][stateful_set]['containers'] = []
                    # YugabyteDB: get_worker_pods/endpoints/set_metric_of_config use statefulset_name
                    # and strip the container filter — handled by SutConfiguration branching.
                    config.worker_metric_strip_container = True
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_PORT = 5433,
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_CREATE_SCHEMA = create_schema,
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_PORT = 5433,
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("CockroachDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # CockroachDB
                    name_format = 'CockroachDB-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='CockroachDB', alias='DBMS D', worker=num_worker)
                    config.monitoring_sut = False # should not be monitored since only dummy
                    if skip_loading:
                        config.loading_deactivated = True
                    config.set_storage(
                        storageConfiguration = 'cockroachdb'
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
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'cockroachdb',
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'cockroachdb',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("TiDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # TiDB
                    name_format = 'TiDB-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='TiDB', alias='DBMS D', worker=num_worker)
                    if skip_loading:
                        config.loading_deactivated = True
                    config.set_storage(
                        storageConfiguration = 'tidb'
                        )
                    config.set_resources(
                        replicas_sut = num_sut_replicas
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
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'mysql',
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'mysql',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    #cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("DatabaseService" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # DatabaseService
                    name_format = 'DBS-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='DatabaseService', alias='DatabaseService')
                    config.monitoring_sut = False # cannot be monitored since outside of K8s
                    if skip_loading:
                        config.loading_deactivated = True
                    config.set_storage(
                        storageConfiguration = 'dbs'
                        )
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_DATABASE = 'postgres',
                        BEXHOMA_HOST = 'bexhoma-service.perdelt.svc.cluster.local',
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_DATABASE = 'postgres',
                                        BEXHOMA_HOST = 'bexhoma-service.perdelt.svc.cluster.local',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    #cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("Citus" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # Citus
                    name_format = 'Citus-{threads}-{pods}-{target}'
                    #, configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target)
                    config = configurations.default(experiment=experiment, docker='Citus', alias='DBMS F', worker=num_worker)
                    create_schema = "true"
                    if type_of_benchmark == "tpcc":
                        create_schema = "false"
                    if skip_loading:
                        config.loading_deactivated = True
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
                    config.set_loading_parameters(
                        BENCHBASE_PROFILE = 'postgres',
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        BENCHBASE_CREATE_SCHEMA = create_schema,
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
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
                                        BENCHBASE_PROFILE = 'postgres',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
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
