"""
Benchmark class for Hardware (fio/sysbench/sockperf/netperf) experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from types import SimpleNamespace

from bexhoma import evaluators
from .base import Benchmark

__all__ = ["Hardware"]


class Hardware(Benchmark):
    """
    Benchmark class for raw hardware I/O, CPU, and network benchmarks run via
    fio/sysbench/sockperf/netperf against a dedicated SUT container (no DBMS, no data loading).
    """

    def __init__(self) -> None:
        super().__init__(name='hardware')

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Return a Hardware evaluator scoped to this benchmark's index.

        :param code: Experiment identifier.
        :param path: Root result path.
        :param benchmark_run: 1-based benchmark position.
        :return: :class:`evaluators.hardware` instance.
        """
        return evaluators.hardware(
            code=code,
            path=path,
            include_loading=False,
            include_benchmarking=True,
            benchmark_run=benchmark_run,
        )

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set Hardware workload metadata on the experiment.

        Hardware never loads data — ``experiment.loading_active`` stays at its
        base-class default (``False``).

        :param experiment: The owning experiment object.
        :param parameter: Dict of CLI arguments as produced by argparse.
        """
        args = SimpleNamespace(**parameter)
        experiment.args = args
        experiment.args_dict = parameter
        mode = str(parameter['mode'])
        if mode == 'start':
            experiment.benchmarking_active = False
        hardware_type = args.hardware_type
        if mode == 'run':
            experiment.set_workload(
                name=f'Hardware Benchmark ({hardware_type})',
                info='This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.',
                type='hardware',
                defaultParameters={'HARDWARE_TYPE': hardware_type},
            )
        else:
            experiment.set_workload(
                name='Hardware Start SUT',
                info='This just starts the hardware SUT.',
                intro='Start SUT and do not benchmark.',
                type='hardware',
                defaultParameters={'HARDWARE_TYPE': hardware_type},
            )
        if experiment.benchmarking_is_active():
            experiment.workload['info'] += f"\nBenchmark tool: {hardware_type}."
            if hardware_type == 'fio':
                list_fio_rw = args.fio_rw.split(",")
                list_fio_bs = args.fio_bs.split(",")
                list_fio_engine = args.fio_engine.split(",")
                list_fio_iodepth = experiment.get_parameter_as_list('fio_iodepth')
                list_fio_fsync = experiment.get_parameter_as_list('fio_fsync')
                list_fio_fdatasync = experiment.get_parameter_as_list('fio_fdatasync')
                list_fio_rwmixread = experiment.get_parameter_as_list('fio_rwmixread')
                experiment.workload['info'] += f"\nTest file size is '{args.hardware_size}', duration per round is {args.hardware_duration}s."
                experiment.workload['info'] += f"\nI/O pattern(s) swept: {list_fio_rw}."
                experiment.workload['info'] += f"\nBlock size(s) swept: {list_fio_bs}."
                experiment.workload['info'] += f"\nQueue depth(s) swept: {list_fio_iodepth}."
                experiment.workload['info'] += f"\nI/O engine(s) swept: {list_fio_engine}."
                experiment.workload['info'] += f"\nFsync interval(s) swept: {list_fio_fsync}."
                experiment.workload['info'] += f"\nFdatasync interval(s) swept: {list_fio_fdatasync}."
                if 'randrw' in list_fio_rw:
                    experiment.workload['info'] += f"\nRead mix percentage(s) swept: {list_fio_rwmixread}."
            elif hardware_type == 'sysbench':
                list_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
                list_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
                experiment.workload['info'] += (
                    f"\nDuration per round is {args.hardware_duration}s, capping each of the CPU "
                    "and memory phases (see images/hardware/benchmarker/run_sysbench.sh)."
                )
                experiment.workload['info'] += (
                    f"\nTotal sysbench thread count(s) swept: {list_benchmarking_threads}, "
                    f"split across pod count(s): {list_benchmarking_pods}."
                )
                experiment.workload['info'] += "\nCPU phase: sysbench cpu --cpu-max-prime=20000 (fixed)."
                experiment.workload['info'] += (
                    "\nMemory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G "
                    "(fixed; may finish before the duration cap if this transfers first)."
                )
            elif hardware_type == 'sockperf':
                list_sockperf_mode = args.sockperf_mode.split(",")
                list_sockperf_protocol = args.sockperf_protocol.split(",")
                list_sockperf_msgsize = experiment.get_parameter_as_list('sockperf_msgsize')
                list_sockperf_mps = args.sockperf_mps.split(",")
                experiment.workload['info'] += f"\nDuration per round is {args.hardware_duration}s."
                experiment.workload['info'] += f"\nMode(s) swept: {list_sockperf_mode} (pp = ping-pong, ul = under-load)."
                experiment.workload['info'] += f"\nProtocol(s) swept: {list_sockperf_protocol}."
                experiment.workload['info'] += f"\nMessage size(s) swept: {list_sockperf_msgsize} bytes."
                experiment.workload['info'] += f"\nMessage rate(s) swept: {list_sockperf_mps} (messages/sec, or 'max' for uncapped)."
            elif hardware_type == 'netperf':
                list_netperf_protocol = args.netperf_protocol.split(",")
                experiment.workload['info'] += f"\nDuration per round is {args.hardware_duration}s."
                experiment.workload['info'] += f"\nProtocol(s) swept: {list_netperf_protocol} (selects TCP_RR/UDP_RR)."
                experiment.workload['info'] += "\nConcurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh)."

    def test_results(self, experiment) -> None:
        """
        Validate Hardware results and print workflow completion status.

        :param experiment: The owning experiment object.
        """
        experiment.cluster.logger.debug('Hardware.test_results()')
        self.evaluator.test_results()
        workflow = experiment.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")
