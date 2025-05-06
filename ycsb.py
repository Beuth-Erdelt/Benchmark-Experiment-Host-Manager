"""
    This script contains code that manages YCSB experiments in a K8s cluster.

    Copyright (C) 2021  Patrick Erdelt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
import pandas as pd
import types
import math


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Perform YCSB benchmarks in a Kubernetes cluster.
    Number of rows and operations is SF*1,000,000.
    This installs a clean copy for each target and split of the driver.
    Optionally monitoring is activated.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='import YCSB data or run YCSB queries', choices=['run', 'start', 'load', 'summary'], default='run')
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms','--dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MySQL', 'MariaDB', 'YugabyteDB', 'CockroachDB', 'DatabaseService', 'PGBouncer', 'Redis', 'Citus'], default=[], nargs='*')
    parser.add_argument('-db',  '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-sl',  '--skip-loading', help='do not ingest, start benchmarking immediately', action='store_true', default=False)
    parser.add_argument('-cx',  '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e',   '--experiment', help='sets experiment code for continuing started experiment', default=None)
    parser.add_argument('-m',   '--monitoring', help='activates monitoring for sut', action='store_true')
    parser.add_argument('-mc',  '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms',  '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    parser.add_argument('-nc',  '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne',  '--num-query-executors', help='comma separated list of number of parallel clients', default="")
    parser.add_argument('-nw',  '--num-worker', help='number of workers (for distributed dbms)', default=0)
    parser.add_argument('-nwr',  '--num-worker-replicas', help='number of workers replications (for distributed dbms)', default=0)
    parser.add_argument('-nws',  '--num-worker-shards', help='number of worker shards (for distributed dbms)', default=0)
    #parser.add_argument('-nl',  '--num-loading', help='number of parallel loaders per configuration', default=1)
    parser.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default="1")
    parser.add_argument('-nlt', '--num-loading-threads', help='total number of threads per loading process', default="1")
    parser.add_argument('-nlf', '--num-loading-target-factors', help='comma separated list of factors of 16384 ops as target - default range(1,9)', default="1")
    parser.add_argument('-nbp', '--num-benchmarking-pods', help='comma separated list of  number of benchmarkers per configuration', default="1")
    parser.add_argument('-nbt', '--num-benchmarking-threads', help='total number of threads per benchmarking process', default="1")
    parser.add_argument('-nbf', '--num-benchmarking-target-factors', help='comma separated list of factors of 16384 ops as target - default range(1,9)', default="1")
    parser.add_argument('-npp', '--num-pooling-pods', help='comma separated list of  number of pooling pods per configuration', default="1")
    parser.add_argument('-npi', '--num-pooling-in', help='comma separated list of max connections into a connection pooler', default="")
    parser.add_argument('-npo', '--num-pooling-out', help='comma separated list of max connections out of a connection pooler', default="")
    parser.add_argument('-wl',  '--workload', help='YCSB default workload', choices=['a', 'b', 'c', 'e', 'f'], default='')
    parser.add_argument('-sf',  '--scaling-factor', help='scaling factor (SF) = number of rows in millions', default=1)
    parser.add_argument('-sfo', '--scaling-factor-operations', help='scaling factor = number of operations in millions (=SF if not set)', default=None)
    #parser.add_argument('-su',  '--scaling-users', help='scaling factor = number of total threads', default=64)
    parser.add_argument('-sbs', '--scaling-batchsize', help='batch size', default="")
    parser.add_argument('-slg', '--scaling-logging', help='logging status every x seconds', default=10)
    #parser.add_argument('-ltf', '--list-target-factors', help='comma separated list of factors of 16384 ops as target - default range(1,9)', default="1,2,3,4,5,6,7,8")
    parser.add_argument('-tb',  '--target-base', help='ops as target, base for factors - default 16384 = 2**14', default="16384")
    parser.add_argument('-t',   '--timeout', help='timeout for a run of a query', default=180)
    parser.add_argument('-lr',  '--limit-ram', help='limit ram for sut, default 0 (none)', default='0')
    parser.add_argument('-lc',  '--limit-cpu', help='limit cpus for sut, default 0 (none)', default='0')
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
    ### specific to: YCSB
    ##############
    SFO = str(args.scaling_factor_operations)
    if SFO == 'None':
        SFO = SF
    ycsb_rows = int(SF)*1000000 # 1kb each, that is SF is size in GB
    ycsb_operations = int(SFO)*1000000
    target_base = int(args.target_base)
    batchsize = args.scaling_batchsize
    scaling_logging = int(args.scaling_logging) # ycsb expects seconds? *1000 # adjust unit to miliseconds
    workload = args.workload
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
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.ycsb(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
    num_loading_target_factors = experiment.get_parameter_as_list('num_loading_target_factors')
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    num_benchmarking_target_factors = experiment.get_parameter_as_list('num_benchmarking_target_factors')
    num_pooling_pods = experiment.get_parameter_as_list('num_pooling_pods')
    num_pooling_in = experiment.get_parameter_as_list('num_pooling_in')
    num_pooling_out = experiment.get_parameter_as_list('num_pooling_out')
    # if we want to loop over pooling pods, we only allow 1 configuration of loading pods (number and target)
    # this is because naming length is limited in k8s
    if len(num_pooling_pods) > 0:
        num_loading_pods = [num_loading_pods[0]]
        num_loading_threads = [num_loading_threads[0]]
    # set node labes for components
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'sut',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="ycsb",
        experiment_design="compare-scaleout",
        rows=ycsb_rows,
        operations=ycsb_operations,
        workload=workload,
        )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_threads in num_loading_threads:#[8]:#[64]:
        for loading_pods in num_loading_pods:#[1,2]:#[1,8]:#range(2,5):
            for factor_loading in num_loading_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                loading_target = target_base*factor_loading#4*4096*t
                loading_threads_per_pod = int(loading_threads/loading_pods)
                ycsb_operations_per_pod = int(ycsb_operations/loading_pods)
                loading_target_per_pod = int(loading_target/loading_pods)
                if ("PostgreSQL" in args.dbms or len(args.dbms) == 0):
                    # PostgreSQL
                    name_format = 'PostgreSQL-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='PostgreSQL', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS A')
                    config.set_storage(
                        storageConfiguration = 'postgresql'
                        )
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = "jdbc",
                        YCSB_MEASUREMENT_TYPE = "hdrhistogram",
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
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        YCSB_MEASUREMENT_TYPE = "hdrhistogram",
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
                                config = configurations.ycsb(experiment=experiment, docker='PGBouncer', configuration=name_format.format(threads=loading_threads, loading_pods=loading_pods, pooling_pods=num_c_pods, target=loading_target, c_in=num_c_in, c_out=num_c_out), alias='DBMS A')
                                config.path_experiment_docker = 'PostgreSQL'                              # take init scripts of PostgreSQL
                                config.sut_has_pool = True                                                # in particular monitor pool component
                                config.sut_envs = {
                                    'DEFAULT_POOL_SIZE': int(num_c_out/num_c_pods),                       # max connections to PostgreSQL
                                    'MIN_POOL_SIZE': int(num_c_out/num_c_pods),                           # min connections to PostgreSQL
                                    'MAX_CLIENT_CONN': int(num_c_in/num_c_pods),                          # max connections to PGBouncer
                                }
                                config.set_resources(
                                    replicas_pooling = num_c_pods,
                                )
                                config.set_storage(
                                    storageConfiguration = 'postgresql'
                                    )
                                config.set_loading_parameters(
                                    PARALLEL = str(loading_pods),
                                    SF = SF,
                                    BEXHOMA_SYNCH_LOAD = 1,
                                    YCSB_THREADCOUNT = loading_threads_per_pod,
                                    YCSB_TARGET = loading_target_per_pod,
                                    YCSB_STATUS = 1,
                                    YCSB_WORKLOAD = workload,
                                    YCSB_ROWS = ycsb_rows,
                                    YCSB_OPERATIONS = ycsb_operations_per_pod,
                                    YCSB_BATCHSIZE = batchsize,
                                    YCSB_STATUS_INTERVAL = scaling_logging,
                                    BEXHOMA_DBMS = "jdbc",
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
                                                ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                                benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                                executor_list.append(benchmarking_pods_scaled)
                                                config.add_benchmarking_parameters(
                                                    PARALLEL = str(benchmarking_pods_scaled),
                                                    SF = SF,
                                                    BEXHOMA_SYNCH_LOAD = 1,
                                                    YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                                    YCSB_TARGET = benchmarking_target_per_pod,
                                                    YCSB_STATUS = 1,
                                                    YCSB_WORKLOAD = workload,
                                                    YCSB_ROWS = ycsb_rows,
                                                    YCSB_OPERATIONS = ycsb_operations_per_pod,
                                                    YCSB_BATCHSIZE = batchsize,
                                                    YCSB_STATUS_INTERVAL = scaling_logging,
                                                    BEXHOMA_DBMS = "jdbc",
                                                    )
                                #print(executor_list)
                                config.add_benchmark_list(executor_list)
                if ("MySQL" in args.dbms or len(args.dbms) == 0):
                    # MySQL
                    name_format = 'MySQL-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='MySQL', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS B')
                    config.set_storage(
                        storageConfiguration = 'mysql'
                        )
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = "jdbc",
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
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("MariaDB" in args.dbms or len(args.dbms) == 0):
                    # MariaDB
                    name_format = 'MariaDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='MariaDB', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS C')
                    config.set_storage(
                        storageConfiguration = 'mariadb'
                        )
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = "jdbc",
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
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("YugabyteDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # YugabyteDB
                    name_format = 'YugabyteDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='YugabyteDB', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS D')
                    config.set_storage(
                        storageConfiguration = 'yugabytedb'
                        )
                    if skip_loading:
                        config.loading_deactivated = True
                    config.sut_service_name = "yb-tserver-service"      # fix service name of SUT, because it is not managed by bexhoma
                    config.sut_pod_name = "yb-tserver-"                 # fix pod name of SUT, because it is not managed by bexhoma
                    config.statefulset_name = 'yb-tserver'              # name of the stateful set of DBMS pods
                    config.sut_container_name = ''                      # fix container name of SUT
                    def get_worker_pods(self):
                        """
                        Returns a list of all pod names of workers for the current SUT.
                        Default is component name is 'worker' for a bexhoma managed DBMS.
                        This is used for example to find the pods of the workers in order to get the host infos (CPU, RAM, node name, ...).
                        YugabyteDB: This is yb-tserver-0, -1 etc.

                        :return: list of endpoints
                        """
                        #pods_worker = ['yb-tserver-0', 'yb-tserver-1', 'yb-tserver-2']
                        pods_worker = cluster.get_statefulset_pods(self.statefulset_name)
                        #pods_worker = self.experiment.cluster.get_pods(app='', component='', configuration='yb-tserver', experiment='')
                        print("****************", pods_worker)
                        return pods_worker
                    config.get_worker_pods = types.MethodType(get_worker_pods, config)
                    #def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
                    #    """
                    #    Generate a name for the monitoring component.
                    #    This is used in a pattern for promql.
                    #    Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`.
                    #    For YugabyteDB, the service of the SUT to be monitored is named like 'yb-tserver-'.
                    #    :param app: app the component belongs to
                    #    :param component: Component, for example sut or monitoring
                    #    :param experiment: Unique identifier of the experiment
                    #    :param configuration: Name of the dbms configuration
                    #    """
                    #    if component == 'sut':
                    #        name = 'yb-tserver-'
                    #    else:
                    #        name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
                    #    self.logger.debug("yugabytedb.create_monitoring({})".format(name))
                    #    return name
                    #config.create_monitoring = types.MethodType(create_monitoring, config)
                    def get_worker_endpoints(self):
                        """
                        Returns all endpoints of a headless service that monitors nodes of a distributed DBMS.
                        These are IPs of cAdvisor instances.
                        The endpoint list is to be filled in a config of an instance of Prometheus.
                        By default, the workers can be found by the name of their component (worker-0 etc).
                        This is neccessary, when we have sidecar containers attached to workers of a distributed dbms.

                        :return: list of endpoints
                        """
                        endpoints = []
                        #name_worker = self.generate_component_name(component='worker', configuration=self.configuration, experiment=self.code)
                        pods_worker = self.get_worker_pods()
                        for pod in pods_worker:
                            #endpoint = '{worker}.{service_sut}'.format(worker=pod, service_sut=name_worker)
                            endpoint = '{worker}'.format(worker=pod)
                            endpoints.append(endpoint)
                            print('Worker Endpoint: {endpoint}'.format(endpoint = endpoint))
                        self.logger.debug("yugabytedb.get_worker_endpoints({})".format(endpoints))
                        return endpoints
                    config.get_worker_endpoints = types.MethodType(get_worker_endpoints, config)
                    def set_metric_of_config(self, metric, host, gpuid):
                        """
                        Returns a promql query.
                        Parameters in this query are substituted, so that prometheus finds the correct metric.
                        Example: In 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))'
                        configuration and experiment are placeholders and will be replaced by concrete values.
                        YugabyteDB: We do not have a SUT that is specific to the experiment or configuration. The pod names follow a pattern like yb-tserver and there is no container name.

                        :param metric: Parametrized promql query
                        :param host: Name of the host the metrics should be collected from
                        :param gpuid: GPU that the metrics should watch
                        :return: promql query without parameters
                        """
                        metric = metric.replace(', container="dbms"', '')
                        metric = metric.replace(', container_label_io_kubernetes_container_name="dbms"', '')
                        return metric.format(host=host, gpuid=gpuid, configuration='yb-tserver', experiment='')
                    config.set_metric_of_config = types.MethodType(set_metric_of_config, config)
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = "jdbc",
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
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(num_executor*benchmarking_pods),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("CockroachDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # CockroachDB
                    name_format = 'CockroachDB-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='CockroachDB', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS D', worker=num_worker)
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
                    if skip_loading:
                        config.loading_deactivated = True
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = "jdbc",
                        BEXHOMA_REPLICAS = num_worker_replicas,
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
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(num_executor*benchmarking_pods),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("DatabaseService" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # DatabaseService
                    name_format = 'DatabaseService-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='DatabaseService', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DatabaseService')
                    config.monitoring_sut = False # cannot be monitored since outside of K8s
                    config.set_storage(
                        storageConfiguration = 'databaseservice'
                        )
                    if skip_loading:
                        config.loading_deactivated = True
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = "jdbc",
                        )
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:
                        benchmarking_target = target_base*factor_benchmarking
                        for benchmarking_threads in num_benchmarking_threads:
                            for benchmarking_pods in num_benchmarking_pods:
                                for num_executor in list_clients:
                                    benchmarking_pods_scaled = num_executor*benchmarking_pods
                                    benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(num_executor*benchmarking_pods),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    #cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("Redis" in args.dbms or len(args.dbms) == 0):
                    # PostgreSQL
                    name_format = 'Redis-{threads}-{pods}-{target}'
                    num_worker_inc_replicas = num_worker * (1+num_worker_replicas)
                    config = configurations.ycsb(experiment=experiment, docker='Redis', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS KV', worker=num_worker_inc_replicas)
                    if num_worker > 0:
                        config.sut_template = "deploymenttemplate-RedisCluster.yml"
                        bexhoma_dbms = "redis-cluster"
                    else:
                        bexhoma_dbms = "redis"
                    config.set_storage(
                        storageConfiguration = 'redis'
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
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = scaling_logging,
                        BEXHOMA_DBMS = bexhoma_dbms,
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        )
                    def get_worker_name(self):
                        """
                        Returns a template for the worker names.
                        Default is component name is 'worker' for a bexhoma managed DBMS.
                        If PVC are used, this must be changed, since the experiment code as part of the worker names would imply the PVC also are only valid for the concrete experiment.
                        This is used for example to find the pods of the workers in order to get the host infos (CPU, RAM, node name, ...).
                        For Redis, this is shortend to bx-w- in the beginning, since Redis has a limitation for hostnames.

                        :return: name template for worker pods
                        """
                        if self.storage['storageConfiguration']:
                            storageConfiguration = self.storage['storageConfiguration']
                        else:
                            storageConfiguration = self.configuration
                        # configure names
                        if self.num_worker > 0:
                            # we assume here, a stateful set is used
                            # this means we do not want to have the experiment code as part of the names
                            # this would imply there cannot be experiment independent pvcs
                            self.experiment_name = self.storage_label#storageConfiguration
                        else:
                            self.experiment_name = self.code
                        #name = self.generate_component_name(app=app, component=component, experiment=self.experiment_name, configuration=configuration)
                        #name_worker = self.generate_component_name(app=app, component='worker', experiment=self.experiment_name, configuration=configuration)
                        # test shorter names
                        name_worker = self.generate_component_name(app="bx", component='w', experiment=self.experiment_name, configuration=storageConfiguration)
                        #this works, but is long:
                        #name_worker = self.generate_component_name(app=self.appname, component='worker', experiment=self.experiment_name, configuration=storageConfiguration)
                        return name_worker
                    config.get_worker_name = types.MethodType(get_worker_name, config)
                    config.set_loading(parallel=loading_pods, num_pods=loading_pods)
                    executor_list = []
                    for factor_benchmarking in num_benchmarking_target_factors:#range(1, 9):#range(1, 2):#range(1, 15):
                        benchmarking_target = target_base*factor_benchmarking#4*4096*t
                        for benchmarking_threads in num_benchmarking_threads:
                            for benchmarking_pods in num_benchmarking_pods:#[1,2]:#[1,8]:#range(2,5):
                                for num_executor in list_clients:
                                    benchmarking_pods_scaled = num_executor*benchmarking_pods
                                    benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = bexhoma_dbms,
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("Citus" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # Citus
                    name_format = 'Citus-{threads}-{pods}-{target}'
                    config = configurations.ycsb(experiment=experiment, docker='Citus', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS F', worker=num_worker)
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
                        PARALLEL = str(loading_pods),
                        SF = SF,
                        BEXHOMA_SYNCH_LOAD = 1,
                        YCSB_THREADCOUNT = loading_threads_per_pod,
                        YCSB_TARGET = loading_target_per_pod,
                        YCSB_STATUS = 1,
                        YCSB_WORKLOAD = workload,
                        YCSB_ROWS = ycsb_rows,
                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                        YCSB_BATCHSIZE = batchsize,
                        YCSB_STATUS_INTERVAL = 10,
                        BEXHOMA_DBMS = "jdbc",
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        YCSB_USE_HOSTLIST = "true",
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
                                    ycsb_operations_per_pod = int(ycsb_operations/benchmarking_pods_scaled)
                                    benchmarking_target_per_pod = int(benchmarking_target/benchmarking_pods)
                                    """
                                    print("benchmarking_target", benchmarking_target)
                                    print("benchmarking_pods", benchmarking_pods)
                                    print("benchmarking_pods_scaled", benchmarking_pods_scaled)
                                    print("benchmarking_threads", benchmarking_threads)
                                    print("ycsb_operations_per_pod", ycsb_operations_per_pod)
                                    print("benchmarking_threads_per_pod", benchmarking_threads_per_pod)
                                    print("benchmarking_target_per_pod", benchmarking_target_per_pod)
                                    """
                                    executor_list.append(benchmarking_pods_scaled)
                                    config.add_benchmarking_parameters(
                                        PARALLEL = str(num_executor*benchmarking_pods),
                                        SF = SF,
                                        BEXHOMA_SYNCH_LOAD = 1,
                                        YCSB_THREADCOUNT = benchmarking_threads_per_pod,
                                        YCSB_TARGET = benchmarking_target_per_pod,
                                        YCSB_STATUS = 1,
                                        YCSB_WORKLOAD = workload,
                                        YCSB_ROWS = ycsb_rows,
                                        YCSB_OPERATIONS = ycsb_operations_per_pod,
                                        YCSB_BATCHSIZE = batchsize,
                                        YCSB_STATUS_INTERVAL = scaling_logging,
                                        BEXHOMA_DBMS = "jdbc",
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        YCSB_USE_HOSTLIST = "true",
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
        #experiment.evaluate_results()
        #experiment.store_workflow_results()
        experiment.show_summary()
    else:
        # total time of experiment
        start = default_timer()
        start_datetime = str(datetime.datetime.now())
        #print("Experiment starts at {} ({})".format(start_datetime, start))
        print("{:30s}: has code {}".format("Experiment",experiment.code))
        print("{:30s}: starts at {} ({})".format("Experiment",start_datetime, start))
        print("{:30s}: {}".format("Experiment",experiment.workload['info']))
        # run workflow
        experiment.work_benchmark_list()
        # total time of experiment
        end = default_timer()
        end_datetime = str(datetime.datetime.now())
        duration_experiment = end - start
        #print("Experiment ends at {} ({}): {}s total".format(end_datetime, end, duration_experiment))
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
        #cluster.restart_dashboard()        # only for dbmsbenchmarker because of dashboard. Jupyter server does not need to restart
        experiment.show_summary()
exit()
