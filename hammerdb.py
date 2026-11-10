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
from bexhoma.cli_args import make_base_parser, resolve_scaling_factor
from bexhoma.experiments.system_builder import build_configuration, entry_parameters, selected_dockers, tenancy_error
from bexhoma.system_descriptors import dbms_choices
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
    description = """Run HammerDB TPC-C benchmarks against a DBMS in Kubernetes.
    Controls loading virtual user count, benchmark duration, ramp-up time, and optional latency profiling.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase: start SUT only, load data, run the full benchmark, or summarize results', choices=['run', 'start', 'load', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='one or more DBMS engines to test', choices=dbms_choices('tpcc'), default=[], nargs='*')
    parser.add_argument('-xdt',   '--xdata-transfer', help='also measure data transfer volume per query (not just execution time)', action='store_true', default=False, dest='datatransfer')
    parser.add_argument('-xqr',   '--xnum-query-runs', help='number of times to repeat each query', default=1, dest='num_run')
    parser.add_argument('-xrt',   '--xrampup-time', help='ramp-up period in minutes before measurements begin', default=2, dest='num_rampup_time')
    parser.add_argument('-xsd',   '--xscaling-duration', help='benchmark duration in minutes', default=5, dest='scaling_duration')
    parser.add_argument('-xlat',  '--extra-latency', help='record per-transaction latency profile (HammerDB TIMEPROFILE)', action='store_true', default=False)
    parser.add_argument('-xkey',  '--extra-keying', help='simulate TPC-C keying and think times between transactions', action='store_true', default=False)
    # evaluate args
    args = parser.parse_args()
    reason = tenancy_error('tpcc', args)
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
    test_result = args.test_result
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
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
    experiment = experiments.tpcc(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    if args.max_sut_experiment is not None:
        experiment.max_sut = int(args.max_sut_experiment)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    # -rc/-lc/-rr/-lr/-rst may each carry a comma list: experiment.process()
    # then clones every configuration below once per resource cell
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
    for loading_threads in num_loading_threads:
        for loading_pods in [1]:
            loading_threads_per_pod = int(loading_threads/loading_pods)
            # every DBMS that can run TPC-C (or the ones named by -dbms), as declared in cluster.config
            for docker in selected_dockers(cluster.dockers, 'tpcc', args.dbms, args):
                config = build_configuration(
                    experiment, docker, 'tpcc', args,
                    loading_parameters={'HAMMERDB_VUSERS': loading_threads_per_pod})
                config.set_loading(parallel=1, num_pods=1)
                benchmarking_parameters = entry_parameters(cluster.dockers, docker, 'tpcc', 'benchmarking_parameters', args)
                executor_list = []
                for benchmarking_threads in num_benchmarking_threads:
                    for benchmarking_pods in num_benchmarking_pods:
                        for num_executor in list_clients:
                            benchmarking_pods_scaled = num_executor*benchmarking_pods
                            benchmarking_threads_per_pod = int(benchmarking_threads/benchmarking_pods)
                            executor_list.append(benchmarking_pods_scaled)
                            config.add_benchmarking_parameters(
                                **benchmarking_parameters,
                                HAMMERDB_NUM_VU = str(benchmarking_pods_scaled),
                                HAMMERDB_VUSERS = benchmarking_threads_per_pod,
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
    experiment.process()
exit()
