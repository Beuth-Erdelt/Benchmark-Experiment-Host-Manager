"""
:Date: 2023-02-12
:Version: 0.1
:Authors: Patrick K. Erdelt

Perform TPC-C inspired benchmarks based on Benchbase in a Kubernetes cluster.
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
import math
import types


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Perform TPC-C inspired benchmarks based on Benchbase in a Kubernetes cluster.
    Optionally monitoring is actived.
    User can also choose some parameters like number of warehouses and request some resources.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='start sut, also load data or also run the TPC-C queries', choices=['run', 'start', 'load'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms','--dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MySQL', 'MariaDB', 'YugabyteDB', 'CockroachDB', 'DatabaseService', 'Citus'], default=[], nargs='*')
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-sl',  '--skip-loading', help='do not ingest, start benchmarking immediately', action='store_true', default=False)
    parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e', '--experiment', help='sets experiment code for continuing started experiment', default=None)
    #parser.add_argument('-d', '--detached', help='puts most of the experiment workflow inside the cluster', action='store_true')
    parser.add_argument('-m', '--monitoring', help='activates monitoring for sut', action='store_true')
    parser.add_argument('-mc', '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms', '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    #parser.add_argument('-dt', '--datatransfer', help='activates datatransfer', action='store_true', default=False)
    #parser.add_argument('-md', '--monitoring-delay', help='time to wait [s] before execution of the runs of a query', default=10)
    #parser.add_argument('-nr', '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nc', '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne', '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    parser.add_argument('-nw',  '--num-worker', help='number of workers (for distributed dbms)', default=1)
    parser.add_argument('-nwr',  '--num-worker-replicas', help='number of workers replications (for distributed dbms)', default=0)
    parser.add_argument('-nws',  '--num-worker-shards', help='number of worker shards (for distributed dbms)', default=0)
    parser.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default="1")
    parser.add_argument('-nlt', '--num-loading-threads', help='total number of threads per loading process', default="1")
    #parser.add_argument('-nlf', '--num-loading-target-factors', help='comma separated list of factors of 16384 ops as target - default range(1,9)', default="1")
    parser.add_argument('-nbp', '--num-benchmarking-pods', help='comma separated list of  number of benchmarkers per configuration', default="1")
    parser.add_argument('-nbt', '--num-benchmarking-threads', help='total number of threads per benchmarking process', default="1")
    parser.add_argument('-nbf', '--num-benchmarking-target-factors', help='comma separated list of factors of 16384 ops as target - default range(1,9)', default="1")
    #parser.add_argument('-nvu', '--num-virtual-users', help='comma separated list of number of virtual users for Benchbase benchmarking', default="1")
    parser.add_argument('-sf', '--scaling-factor', help='scaling factor (SF) = number of warehouses', default=1)
    #parser.add_argument('-su', '--scaling-users', help='comma separated list of number of users for loading', default="1")
    parser.add_argument('-sd', '--scaling-duration', help='scaling factor = duration in minutes', default=5)
    parser.add_argument('-slg', '--scaling-logging', help='logging status every x seconds', default=0)
    parser.add_argument('-xkey', '--extra-keying', help='activate keying and waiting time', action='store_true', default=False)
    parser.add_argument('-t', '--timeout', help='timeout for a run of a query', default=600)
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
    #parser.add_argument('-nti', '--num-time', help='time per benchmark in seconds', default="60")
    parser.add_argument('-b', '--benchmark', help='type of benchmark', default='tpcc', choices=['tpcc', 'twitter'])
    #parser.add_argument('-nt', '--num-target', help='total number of loaders per configuration', default="1024")
    #parser.add_argument('-ltf', '--list-target-factors', help='comma separated list of factors of 1024 ops as target - default range(1,9)', default="1,2,3,4,5,6,7,8")
    parser.add_argument('-tb', '--target-base', help='ops as target, base for factors - default 1024 = 2**10', default="1024")
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
    ### specific to: Benchbase
    ##############
    SD = int(args.scaling_duration)*60
    target_base = int(args.target_base)
    type_of_benchmark = args.benchmark
    scaling_logging = int(args.scaling_logging)*1000 # adjust unit to miliseconds
    extra_keying = int(args.extra_keying)
    if extra_keying:
        BENCHBASE_KEY_AND_THINK = "true"
    else:
        BENCHBASE_KEY_AND_THINK = "false"
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
    experiment = experiments.benchbase(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
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
        usecase="benchbase_tpcc",
        warehouses=SF,
        #users_loading=scaling_users,
        #users_benchmarking=str(num_virtual_users),
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
                    name_format = 'PostgreSQL-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='PostgreSQL', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS A')
                    config.set_storage(
                        storageConfiguration = 'postgresql'
                        )
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_DATABASE = 'postgres',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_DATABASE = 'postgres',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("MySQL" in args.dbms or len(args.dbms) == 0):
                    # MySQL
                    name_format = 'MySQL-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='MySQL', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS A')
                    config.set_storage(
                        storageConfiguration = 'mysql'
                        )
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'mysql',
                        BEXHOMA_DATABASE = 'benchbase',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        BEXHOMA_USER = "root",
                        BEXHOMA_PASSWORD = "root",
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'mysql',
                                        BEXHOMA_DATABASE = 'benchbase',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("MariaDB" in args.dbms or len(args.dbms) == 0):
                    # MariaDB
                    name_format = 'MariaDB-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='MariaDB', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS A')
                    config.set_storage(
                        storageConfiguration = 'mariadb'
                        )
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'mariadb',
                        BEXHOMA_DATABASE = 'benchbase',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        BEXHOMA_USER = "root",
                        BEXHOMA_PASSWORD = "root",
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'mariadb',
                                        BEXHOMA_DATABASE = 'benchbase',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                if ("YugabyteDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # YugabyteDB
                    name_format = 'YugabyteDB-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='YugabyteDB', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS D')
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
                        #print("****************", pods_worker)
                        return pods_worker
                    config.get_worker_pods = types.MethodType(get_worker_pods, config)
                    def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
                        """
                        Generate a name for the monitoring component.
                        This is used in a pattern for promql.
                        Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`.
                        For YugabyteDB, the service of the SUT to be monitored is named like 'yb-tserver-'.

                        :param app: app the component belongs to
                        :param component: Component, for example sut or monitoring
                        :param experiment: Unique identifier of the experiment
                        :param configuration: Name of the dbms configuration
                        """
                        if component == 'sut':
                            name = 'yb-tserver-'
                        else:
                            name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
                        self.logger.debug("yugabytedb.create_monitoring({})".format(name))
                        return name
                    config.create_monitoring = types.MethodType(create_monitoring, config)
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
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_DATABASE = 'yugabyte',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        BEXHOMA_USER = "yugabyte",
                        BEXHOMA_PASSWORD = "",
                        BEXHOMA_PORT = 5433,
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                        BENCHBASE_CREATE_SCHEMA = "false",
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_DATABASE = 'yugabyte',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        BEXHOMA_USER = "yugabyte",
                                        BEXHOMA_PASSWORD = "",
                                        BEXHOMA_PORT = 5433,
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("CockroachDB" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # CockroachDB
                    name_format = 'CockroachDB-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='CockroachDB', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS D', worker=num_worker)
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
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'cockroachdb',
                        BEXHOMA_DATABASE = 'defaultdb',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        BEXHOMA_USER = "root",
                        BEXHOMA_PASSWORD = "",
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'cockroachdb',
                                        BEXHOMA_DATABASE = 'defaultdb',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        BEXHOMA_USER = "root",
                                        BEXHOMA_PASSWORD = "",
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    #cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("DatabaseService" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # DatabaseService
                    name_format = 'DatabaseService-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='DatabaseService', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DatabaseService')
                    config.monitoring_sut = False # cannot be monitored since outside of K8s
                    if skip_loading:
                        config.loading_deactivated = True
                    config.set_loading_parameters(
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_DATABASE = 'postgres',
                        BEXHOMA_HOST = 'bexhoma-service.perdelt.svc.cluster.local',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_DATABASE = 'postgres',
                                        BEXHOMA_HOST = 'bexhoma-service.perdelt.svc.cluster.local',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    #cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
                if ("Citus" in args.dbms):# or len(args.dbms) == 0): # not included per default
                    # CockroachDB
                    name_format = 'Citus-{threads}-{pods}-{target}'
                    config = configurations.benchbase(experiment=experiment, docker='Citus', configuration=name_format.format(threads=loading_threads, pods=loading_pods, target=loading_target), alias='DBMS F', worker=num_worker)
                    config.set_storage(
                        storageConfiguration = 'citus'
                        )
                    if skip_loading:
                        config.loading_deactivated = True
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
                        PARALLEL = str(loading_pods), # =1
                        SF = SF,
                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                        BENCHBASE_PROFILE = 'postgres',
                        BEXHOMA_DATABASE = 'postgres',
                        #BENCHBASE_TARGET = int(target),
                        BENCHBASE_TERMINALS = loading_threads_per_pod,
                        BENCHBASE_TIME = SD,
                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                        #BEXHOMA_USER = "root",
                        #BEXHOMA_PASSWORD = "",
                        BEXHOMA_REPLICAS = num_worker_replicas,
                        BENCHBASE_CREATE_SCHEMA = "false",
                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
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
                                        PARALLEL = str(benchmarking_pods_scaled),
                                        SF = SF,
                                        BENCHBASE_BENCH = type_of_benchmark,#'tpcc',
                                        BENCHBASE_PROFILE = 'postgres',
                                        BEXHOMA_DATABASE = 'postgres',
                                        BENCHBASE_TARGET = benchmarking_target_per_pod,
                                        BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                        BENCHBASE_TIME = SD,
                                        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
                                        #BEXHOMA_USER = "root",
                                        #BEXHOMA_PASSWORD = "",
                                        BEXHOMA_REPLICAS = num_worker_replicas,
                                        BENCHBASE_STATUS_INTERVAL = scaling_logging, #10*1000,
                                        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
                                        )
                    #print(executor_list)
                    config.add_benchmark_list(executor_list)
                    #cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
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
        #experiment.add_benchmark_list(list_clients)
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
        #experiment.add_benchmark_list(list_clients)
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
        print("Experiment ends at {} ({}): {}s total".format(end_datetime, end, duration_experiment))
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
        #cluster.stop_dashboard()
        #cluster.start_dashboard()
        experiment.show_summary()
exit()
