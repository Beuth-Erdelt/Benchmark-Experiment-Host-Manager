"""
CLI entry point for Hardware (fio/sysbench) benchmarks in a Kubernetes cluster.

Runs raw disk I/O (fio) or CPU/memory (sysbench) benchmarks against a
dedicated SUT container over SSH. Unlike every other entry script, there is
no data loading phase and no ``-dbms`` engine choice beyond the single
``Hardware`` target.

The fio workload flags (``-xfrw``, ``-xfbs``, ``-xfid``, ``-xfe``, ``-xfsy``,
``-xffd``, ``-xfmx``) each accept a comma-separated list. Every combination across the
lists is run as one more sequential round against the same SUT, so a
parameter sweep (e.g. queue depth) is expressed as a single invocation
instead of one process per value.

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

FIO_RW_CHOICES = {'write', 'read', 'randwrite', 'randread', 'randrw'}
FIO_ENGINE_CHOICES = {'sync', 'libaio', 'io_uring'}

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
    parser.add_argument('-xtd',  '--xtest-duration', help='fio/sysbench run duration in seconds', default=60, type=int, dest='hardware_duration')
    parser.add_argument('-xfrw', '--xfio-rw', help='comma-separated fio I/O patterns to sweep, each in {write, read, randwrite, randread, randrw}', default='randrw', dest='fio_rw')
    parser.add_argument('-xfbs', '--xfio-blocksize', help='comma-separated fio block sizes to sweep (e.g. 4k,64k,1M)', default='8k', dest='fio_bs')
    parser.add_argument('-xfid', '--xfio-iodepth', help='comma-separated fio queue depths to sweep', default='1', dest='fio_iodepth')
    parser.add_argument('-xfe',  '--xfio-engine', help='comma-separated fio ioengines to sweep, each in {sync, libaio, io_uring}', default='sync', dest='fio_engine')
    parser.add_argument('-xfsy', '--xfio-fsync', help='comma-separated fsync intervals to sweep (0 disables fsync); use fsync xor fdatasync, not both', default='0', dest='fio_fsync')
    parser.add_argument('-xffd', '--xfio-fdatasync', help='comma-separated fdatasync intervals to sweep (0 disables fdatasync); use fsync xor fdatasync, not both', default='0', dest='fio_fdatasync')
    parser.add_argument('-xfmx', '--xfio-rwmixread', help='comma-separated read percentages to sweep when -xfrw=randrw', default='50', dest='fio_rwmixread')
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
    # sweep axes: iodepth/fsync/rwmixread are numeric (get_parameter_as_list casts to int),
    # rw/blocksize/engine are strings and are validated by hand since argparse `choices`
    # cannot validate a comma-separated string
    list_fio_iodepth = experiment.get_parameter_as_list('fio_iodepth')
    list_fio_fsync = experiment.get_parameter_as_list('fio_fsync')
    list_fio_fdatasync = experiment.get_parameter_as_list('fio_fdatasync')
    list_fio_rwmixread = experiment.get_parameter_as_list('fio_rwmixread')
    list_fio_rw = args.fio_rw.split(",")
    list_fio_bs = args.fio_bs.split(",")
    list_fio_engine = args.fio_engine.split(",")
    invalid_fio_rw = [value for value in list_fio_rw if value not in FIO_RW_CHOICES]
    if invalid_fio_rw:
        parser.error(f"-xfrw: invalid choice(s) {invalid_fio_rw}, must be one of {sorted(FIO_RW_CHOICES)}")
    invalid_fio_engine = [value for value in list_fio_engine if value not in FIO_ENGINE_CHOICES]
    if invalid_fio_engine:
        parser.error(f"-xfe: invalid choice(s) {invalid_fio_engine}, must be one of {sorted(FIO_ENGINE_CHOICES)}")
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
    )
    ##############
    ### add configs of hardware targets to be tested
    ##############
    if "Hardware" in args.dbms or len(args.dbms) == 0:
        if experiment.tenant_per == 'container':
            # One SutConfiguration (one SUT pod) per tenant, all sharing the
            # same -rc/-lc/-rnn snapshot (set on experiment.resources before
            # this loop runs), so -mtn N pins N independent, identically
            # CPU-limited SUT pods onto the same node for co-located
            # noisy-neighbor testing. BEXHOMA_TENANT_BY=container makes every
            # tenant's benchmarker pod wait on the shared
            # bexhoma-benchmarker-podcount-exp-<code> counter (see
            # experiments/base.py work_benchmark_list()), so all tenants'
            # sysbench/fio runs start at the same synchronized instant instead
            # of drifting apart with each pod's own scheduling/startup jitter.
            for tenant in range(experiment.num_tenants):
                config = configurations.default(experiment=experiment, docker='Hardware', alias='Hardware')
                # PVC name mirrors the tenant naming used by benchbase.py/ycsb.py
                # ('{docker}-{tenant}-{num_tenants}'), so each tenant's SUT gets
                # its own volume instead of colliding on the shared 'hardware' one.
                config.set_storage(
                    storageConfiguration=f'hardware-{tenant}-{config.num_tenants}'
                )
                executor_list = []
                for fio_rw in list_fio_rw:
                    for fio_bs in list_fio_bs:
                        for fio_iodepth in list_fio_iodepth:
                            for fio_engine in list_fio_engine:
                                for fio_fsync in list_fio_fsync:
                                    for fio_fdatasync in list_fio_fdatasync:
                                        for fio_rwmixread in list_fio_rwmixread:
                                            # rwmixread only affects randrw; skip redundant rounds otherwise
                                            if fio_rw != 'randrw' and fio_rwmixread != list_fio_rwmixread[0]:
                                                continue
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
                                                            HARDWARE_FIO_RW=fio_rw,
                                                            HARDWARE_FIO_BS=fio_bs,
                                                            HARDWARE_FIO_IODEPTH=str(fio_iodepth),
                                                            HARDWARE_FIO_ENGINE=fio_engine,
                                                            HARDWARE_FIO_FSYNC=str(fio_fsync),
                                                            HARDWARE_FIO_FDATASYNC=str(fio_fdatasync),
                                                            HARDWARE_FIO_RWMIXREAD=str(fio_rwmixread),
                                                            HARDWARE_FIO_NUMJOBS=str(benchmarking_threads_per_pod),
                                                            BEXHOMA_TENANT_BY=config.tenant_per,
                                                            BEXHOMA_TENANT_NUM=config.num_tenants,
                                                            BEXHOMA_TENANT_ID=tenant,
                                                        )
                config.add_benchmark_list(executor_list)
        else:
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
            for fio_rw in list_fio_rw:
                for fio_bs in list_fio_bs:
                    for fio_iodepth in list_fio_iodepth:
                        for fio_engine in list_fio_engine:
                            for fio_fsync in list_fio_fsync:
                                for fio_fdatasync in list_fio_fdatasync:
                                    for fio_rwmixread in list_fio_rwmixread:
                                        # rwmixread only affects randrw; skip redundant rounds otherwise
                                        if fio_rw != 'randrw' and fio_rwmixread != list_fio_rwmixread[0]:
                                            continue
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
                                                        HARDWARE_FIO_RW=fio_rw,
                                                        HARDWARE_FIO_BS=fio_bs,
                                                        HARDWARE_FIO_IODEPTH=str(fio_iodepth),
                                                        HARDWARE_FIO_ENGINE=fio_engine,
                                                        HARDWARE_FIO_FSYNC=str(fio_fsync),
                                                        HARDWARE_FIO_FDATASYNC=str(fio_fdatasync),
                                                        HARDWARE_FIO_RWMIXREAD=str(fio_rwmixread),
                                                        HARDWARE_FIO_NUMJOBS=str(benchmarking_threads_per_pod),
                                                    )
            config.add_benchmark_list(executor_list)
    ##############
    ### branch for workflows
    ##############
    experiment.process()
exit()
