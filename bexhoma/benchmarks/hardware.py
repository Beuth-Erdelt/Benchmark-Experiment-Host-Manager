"""
Benchmark class for Hardware (fio/sysbench) experiments.

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
    Benchmark class for raw hardware I/O and CPU benchmarks run via fio/sysbench
    over SSH against a dedicated SUT container (no DBMS, no data loading).
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
                info='This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.',
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
