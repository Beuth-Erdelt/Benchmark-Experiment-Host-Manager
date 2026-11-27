"""
CLI entry point for Benchbase TPC-C benchmarks in a Kubernetes cluster.

Runs TPC-C workloads via Benchbase. Supports optional monitoring and
configurable parameters such as number of warehouses and resource requests.

Authors: Patrick K. Erdelt
Copyright (C) 2023 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import sys
from bexhoma import *  # noqa: F403
from bexhoma.cli_args import make_base_parser, resolve_scaling_factor, threads_per_pod_error
from bexhoma.experiments.system_builder import (build_configuration, entry_parameters, pooling_variants,
                                                selected_dockers, tenancy_error, tenant_ids)
from bexhoma.system_descriptors import benchmark_entry, dbms_choices, expand, storage_prefix
from dbmsbenchmarker import *  # noqa: F403
import logging
import urllib3
import argparse
from bexhoma.benchmarks.benchbase.experiment import BenchbaseExperiment


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)


def tenant_parameters(experiment, entry: dict, tenant, prefix: str) -> dict:
    """
    What the multi-tenant variants add to a DBMS's configuration in Benchbase.

    The parameter names a DBMS passes to the jobs are its ``tenant_parameters`` in ``cluster.config``;
    the rest (storage name, number of loading pods, script collections) is the same for all DBMS.

    :param experiment: The experiment (``tenant_per``, ``num_tenants``, ``multi_tenant_volume``).
    :param entry: The DBMS's entry for the benchmark.
    :param tenant: The tenant id from :func:`~bexhoma.experiments.system_builder.tenant_ids`, ``None`` without container-tenancy.
    :param prefix: The ``storage_prefix`` of the DBMS.
    :return: ``loading`` and ``benchmarking`` parameters, ``eval`` parameters, ``storage`` (name of the storage),
        ``tenants_per_job`` (loading pods per configuration) and ``experiment`` (scripts) as far as they apply;
        empty for a DBMS without ``multi_tenancy``.
    :rtype: dict
    """
    if not entry.get('multi_tenancy'):
        return {}
    by, number = experiment.tenant_per, experiment.num_tenants
    context = {'tenant_by': by, 'num_tenants': number, 'tenant_id': 0 if tenant is None else tenant}
    declared = entry.get('tenant_parameters') or {}
    result = {
        'loading': expand(declared.get('loading') or {}, context),
        'benchmarking': expand(declared.get('benchmarking') or {}, context),
        'eval': {'TENANT_BY': by, 'TENANT_NUM': number, 'TENANT_VOL': experiment.multi_tenant_volume},
    }
    if tenant is not None:
        result['storage'] = f'{prefix}-{tenant}-{number}'
        result['eval']['TENANT'] = tenant
    else:
        if by:
            result['storage'] = f'{prefix}-{by}-{number}'
        if number > 0:
            result['tenants_per_job'] = number   # every tenant is loaded by the loading pods
        if by == 'schema':
            result['experiment'] = {'script': 'Schema_tenant', 'indexing': 'Checks_tenant'}
    return result


def target_per_pod(target, pods):
    """
    Split a throughput target over the benchmarking pods.

    A target of 0 stays 0 and means unlimited (patched in benchmarker.sh).
    A positive target never rounds down to 0, so it never becomes unlimited by accident.

    :param target: Total target in requests per second.
    :param pods: Number of benchmarking pods.
    :return: Target per pod.
    """
    if target <= 0:
        return 0
    return max(1, int(target/pods))

def main() -> None:
    """Run the entry script with the command line in ``sys.argv``."""
    description = """Run Benchbase benchmarks (TPC-C, YCSB, Twitter, CH-Benchmark) against a DBMS in Kubernetes.
    Controls loading concurrency, benchmarking throughput targets, optional connection pooling, and resource allocation.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase: start SUT only, load data, run the full benchmark, or summarize results', choices=['run', 'start', 'load', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='one or more DBMS engines to test', choices=dbms_choices('benchbase'), default=[], nargs='*')
    parser.add_argument('-xnsr',  '--xnum-sut-replicas', help='number of SUT replicas per configuration', default=1, dest='num_sut_replicas')
    parser.add_argument('-xnpd',  '--xnum-pd-nodes', help='number of PD (Placement Driver) nodes, independent of -nw (TiDB only; keep odd)', default=3, dest='num_pd_nodes')
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
    parser.add_argument('-xbt',   '--xbenchmark-type', help='Benchbase benchmark suite to run', default='tpcc', choices=['tpcc', 'twitter', 'chbenchmark', 'ycsb', 'auctionmark', 'epinions', 'hyadapt', 'noop', 'otmetrics', 'resourcestresser', 'seats', 'sibench', 'smallbank', 'tatp', 'voter', 'wikipedia'], dest='benchmark')
    parser.add_argument('-xtb',   '--xtarget-base', help='base ops-per-second target; multiply by -xnbf factors to get per-pod target (0 = unlimited)', default="1024", dest='target_base')
    parser.add_argument('-xwu',   '--xwarmup', help='warmup in seconds before the measured benchmark duration (not part of the results)', default=0, dest='warmup')
    # -nlt is BenchBase's loaderThreads of the one loader pod; 0 = one thread per processor it sees
    parser.set_defaults(num_worker=1, num_loading_threads="0")
    # evaluate args
    args = parser.parse_args()
    reason = tenancy_error('benchbase', args)
    if reason:
        parser.error(reason)
    loading_values = [value for value in str(args.num_loading_threads).split(',') if value]
    if not all(value.isdigit() for value in loading_values):
        parser.error(f"-nlt {args.num_loading_threads} must be comma-separated integers of at least 0 "
                     f"(0 = one loader thread per processor)")
    checks = [(args.num_benchmarking_threads, args.num_benchmarking_pods, '-nbt', '-nbp')]
    if all(int(value) > 0 for value in loading_values):
        checks.append((args.num_loading_threads, args.num_loading_pods, '-nlt', '-nlp'))
    for threads, pods, threads_option, pods_option in checks:
        reason = threads_per_pod_error(threads, pods, threads_option, pods_option)
        if reason:
            parser.error(reason)
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
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
    ##############
    ### specific to: Benchbase
    ##############
    SD = int(args.scaling_duration)*60
    warmup = int(args.warmup)                             # seconds, not measured
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
    # what the descriptors of cluster.config need besides the command line
    context = {'newconn': BENCHBASE_NEWCONNPERTXN}
    ##############
    ### set cluster
    ##############
    aws = args.aws
    if aws:
        cluster = clusters.AWS(context=args.context)  # noqa: F405
        # scale up
        #cluster.scale_nodegroups(node_sizes)
    else:
        cluster = clusters.Kubernetes(context=args.context)  # noqa: F405
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    # summary mode resumes an existing experiment: use its own persisted SF
    # instead of the -sf CLI default (see resolve_scaling_factor docstring)
    SF = resolve_scaling_factor(cluster, code, mode, args.scaling_factor)
    ##############
    ### prepare and configure experiment
    ##############
    experiment = BenchbaseExperiment(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    if args.max_sut_experiment is not None:
        experiment.max_sut = int(args.max_sut_experiment)
    experiment.set_benchmark_type(type_of_benchmark)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
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
        BENCHBASE_WARMUP = warmup,
        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
        BENCHBASE_BATCHSIZE = extra_batchsize,
        BENCHBASE_STATUS_INTERVAL = scaling_logging,
        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
    )
    experiment.set_default_benchmarking_parameters(
        SF = SF,
        BENCHBASE_BENCH = type_of_benchmark,
        BENCHBASE_TIME = SD,
        BENCHBASE_WARMUP = warmup,
        BENCHBASE_ISOLATION = "TRANSACTION_READ_COMMITTED",
        BENCHBASE_BATCHSIZE = extra_batchsize,
        BENCHBASE_STATUS_INTERVAL = scaling_logging,
        BENCHBASE_KEY_AND_THINK = BENCHBASE_KEY_AND_THINK,
    )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_threads in num_loading_threads:     # 0 = one thread per processor
        for loading_pods in [1]:                    # BenchBase loads with a single pod
            loading_threads_per_pod = int(loading_threads/loading_pods)
            # every DBMS that can run Benchbase (or the ones named by -dbms), as declared in cluster.config
            for docker in selected_dockers(cluster.dockers, 'benchbase', args.dbms, args):
                entry = benchmark_entry(cluster.dockers, docker, 'benchbase')
                # a DBMS behind a connection pooler gets a configuration per pooler setting
                for pooling in pooling_variants(entry, num_pooling_pods,
                                                num_pooling_in or [1],
                                                num_pooling_out or [1]):
                    # a DBMS in the multi-tenant variants gets one configuration per tenant (container-tenancy)
                    for tenant in tenant_ids(experiment, entry):
                        tenants = tenant_parameters(experiment, entry, tenant, storage_prefix(cluster.dockers, docker))
                        config = build_configuration(
                            experiment, docker, 'benchbase', args,
                            loading_parameters={'BENCHBASE_LOADER_THREADS': loading_threads_per_pod, **tenants.get('loading', {})},
                            storage_configuration=tenants.get('storage'),
                            context=context, pooling=pooling or None)
                        pods = loading_pods * tenants.get('tenants_per_job', 1)
                        config.set_loading(parallel=pods, num_pods=pods)
                        if tenants.get('eval'):
                            config.set_eval_parameters(**tenants['eval'])
                        if tenants.get('experiment'):
                            config.set_experiment(**tenants['experiment'])
                        benchmarking_parameters = entry_parameters(
                            cluster.dockers, docker, 'benchbase', 'benchmarking_parameters', args, context)
                        executor_list = []
                        for factor_benchmarking in num_benchmarking_target_factors:
                            benchmarking_target = target_base*factor_benchmarking
                            for benchmarking_threads in num_benchmarking_threads:
                                for benchmarking_pods in num_benchmarking_pods:
                                    for num_executor in list_clients:
                                        benchmarking_pods_scaled = num_executor*benchmarking_pods
                                        benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                                        benchmarking_target_per_pod = target_per_pod(benchmarking_target, benchmarking_pods)
                                        executor_list.append(benchmarking_pods_scaled)
                                        config.add_benchmarking_parameters(
                                            **benchmarking_parameters,
                                            BENCHBASE_TARGET = benchmarking_target_per_pod,
                                            BENCHBASE_TERMINALS = benchmarking_threads_per_pod,
                                            **tenants.get('benchmarking', {}),
                                            )
                        config.add_benchmark_list(executor_list)
    ##############
    ### wait for necessary nodegroups to have planned size
    ##############
    if aws:
        #cluster.wait_for_nodegroups(node_sizes)
        pass
    ##############
    ### branch for workflows
    ##############
    sys.exit(experiment.process())


if __name__ == '__main__':
    main()
