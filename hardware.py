"""
CLI entry point for Hardware (fio/sysbench) benchmarks in a Kubernetes cluster.

Runs raw disk I/O (fio) or CPU/memory (sysbench) benchmarks against a
dedicated SUT container over SSH. Unlike every other entry script, there is
no data loading phase and no ``-dbms`` engine choice beyond the single
``Hardware`` target.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import *
from bexhoma.cli_args import make_base_parser
import logging
import urllib3
import argparse


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Run Hardware (fio/sysbench) benchmarks against a SUT in Kubernetes.
    Controls fio workload shape (read/write pattern, block size, queue depth, engine)
    or selects sysbench for CPU/memory benchmarking.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase: start SUT only, run the benchmark, or summarize results', choices=['run', 'start', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='hardware target(s) to test', choices=['Hardware'], default=[], nargs='*')
    parser.add_argument('-xht',  '--xhardware-type', help='benchmark tool: fio (disk I/O) or sysbench (CPU/memory)', choices=['fio', 'sysbench'], default='fio', dest='hardware_type')
    parser.add_argument('-xts',  '--xtest-size', help='fio test file size (e.g. 1G, 64G)', default='1G', dest='hardware_size')
    parser.add_argument('-xtd',  '--xtest-duration', help='fio/sysbench run duration in seconds', default=30, type=int, dest='hardware_duration')
    parser.add_argument('-xfrw', '--xfio-rw', help='fio I/O pattern', choices=['write', 'read', 'randwrite', 'randread', 'randrw'], default='randrw', dest='fio_rw')
    parser.add_argument('-xfbs', '--xfio-blocksize', help='fio block size (e.g. 8k, 1M)', default='8k', dest='fio_bs')
    parser.add_argument('-xfid', '--xfio-iodepth', help='fio queue depth', default=1, type=int, dest='fio_iodepth')
    parser.add_argument('-xfe',  '--xfio-engine', help='fio ioengine', choices=['sync', 'libaio', 'io_uring'], default='sync', dest='fio_engine')
    parser.add_argument('-xfsy', '--xfio-fsync', help='call fsync every N writes (0 disables it)', default=0, type=int, dest='fio_fsync')
    parser.add_argument('-xfmx', '--xfio-rwmixread', help='percentage of reads when -xfrw=randrw', default=50, type=int, dest='fio_rwmixread')
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if args.debug:
        logger_bexhoma = logging.getLogger('bexhoma')
        logger_bexhoma.setLevel(logging.DEBUG)
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
    # timeout of a benchmark
    timeout = int(args.timeout)
    # how often to repeat experiment?
    num_experiment_to_apply = int(args.num_config)
    # configure number of parallel benchmarker pods per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
    ##############
    ### specific to: Hardware
    ##############
    hardware_type = args.hardware_type
    ##############
    ### set cluster
    ##############
    aws = args.aws
    if aws:
        cluster = clusters.AWS(context=args.context)
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
    experiment = experiments.hardware(cluster=cluster, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    if args.max_sut_experiment is not None:
        experiment.max_sut = int(args.max_sut_experiment)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    experiment.prepare_testbed(command_args)
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="hardware",
        hardware_type=hardware_type,
    )
    experiment.set_default_benchmarking_parameters(
        HARDWARE_TYPE=hardware_type,
        HARDWARE_TEST_DIR='/database/fio-test',
        HARDWARE_SIZE=str(args.hardware_size),
        HARDWARE_DURATION=str(args.hardware_duration),
        HARDWARE_FIO_RW=str(args.fio_rw),
        HARDWARE_FIO_BS=str(args.fio_bs),
        HARDWARE_FIO_IODEPTH=str(args.fio_iodepth),
        HARDWARE_FIO_ENGINE=str(args.fio_engine),
        HARDWARE_FIO_FSYNC=str(args.fio_fsync),
        HARDWARE_FIO_RWMIXREAD=str(args.fio_rwmixread),
    )
    ##############
    ### add configs of hardware targets to be tested
    ##############
    if "Hardware" in args.dbms or len(args.dbms) == 0:
        config = configurations.default(experiment=experiment, docker='Hardware', alias='Hardware')
        # storageClassName follows -rst as usual (defaults to None — no PVC,
        # /database lives in the SUT container's own ephemeral storage; see
        # images/hardware/sut/Dockerfile, which bakes the directory in so it
        # exists either way). Pass -rst explicitly to benchmark real PVC-backed
        # storage instead.
        config.set_storage(
            storageConfiguration='hardware'
        )
        executor_list = []
        for benchmarking_threads in num_benchmarking_threads:
            for benchmarking_pods in num_benchmarking_pods:
                for num_executor in list_clients:
                    benchmarking_pods_scaled = num_executor * benchmarking_pods
                    # -nbt (threads per benchmarking pod) maps to fio's own per-pod
                    # numjobs concurrency, same role -nbt plays for YCSB_THREADCOUNT /
                    # BENCHBASE_TERMINALS / HAMMERDB_VUSERS in the other entry scripts.
                    benchmarking_threads_per_pod = int(benchmarking_threads / benchmarking_pods)
                    executor_list.append(benchmarking_pods_scaled)
                    config.add_benchmarking_parameters(
                        HARDWARE_FIO_NUMJOBS=str(benchmarking_threads_per_pod),
                    )
        config.add_benchmark_list(executor_list)
    ##############
    ### branch for workflows
    ##############
    experiment.process()
exit()
