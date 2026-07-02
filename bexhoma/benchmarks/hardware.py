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
