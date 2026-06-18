"""
Benchmark class for Benchbase experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
from types import SimpleNamespace

from bexhoma import evaluators
from .base import Benchmark

__all__ = ["Benchbase"]


class Benchbase(Benchmark):
    """
    Benchmark class for Benchbase workloads (TPC-C, SEATS, Twitter, etc.).

    :param SF: Scaling factor — meaning depends on the chosen Benchbase workload.
    """

    def __init__(self, SF: str = '1') -> None:
        """
        :param SF: Scaling factor.
        """
        super().__init__(name='benchbase', SF=SF)

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Return a Benchbase evaluator scoped to this benchmark's index.

        :param code: Experiment identifier.
        :param path: Root result path.
        :param benchmark_run: 1-based benchmark position.
        :return: :class:`evaluators.benchbase` instance.
        """
        return evaluators.benchbase(
            code=code,
            path=path,
            include_loading=False,
            include_benchmarking=True,
            benchmark_run=benchmark_run,
        )

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set Benchbase workload metadata on the experiment.

        :param experiment: The owning experiment object.
        :param parameter: Dict of CLI arguments as produced by argparse.
        """
        args = SimpleNamespace(**parameter)
        experiment.args = args
        experiment.args_dict = parameter
        mode = str(parameter['mode'])
        if mode == 'load' or mode == 'start':
            experiment.benchmarking_active = False
        if mode == 'start':
            experiment.loading_deactivated = True
        SF = str(self.SF)
        SD = int(args.scaling_duration) * 60
        target_base = int(args.target_base)
        type_of_benchmark = args.benchmark
        workload = args.workload
        extra_keying = int(args.extra_keying)
        extra_new_connection = int(args.extra_new_connection)
        num_benchmarking_target_factors = experiment.get_parameter_as_list('num_benchmarking_target_factors')
        if mode == 'run':
            experiment.set_workload(
                name='Benchbase Workload {} SF={}'.format(type_of_benchmark, SF),
                info='This experiment compares run time and resource consumption of Benchbase queries in different DBMS.',
                type='benchbase',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name='Benchbase Data {} Loading SF={}'.format(type_of_benchmark, SF),
                info='This imports a Benchbase data set.',
                type='benchbase',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_workload(
                name='Benchbase Start DBMS',
                info='This just starts a SUT.',
                intro='Start DBMS and do not load data.',
                type='benchbase',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.set_experiment(script='Schema')
        if experiment.loading_is_active():
            experiment.workload['info'] += "\nBenchbase data is generated and loaded using several threads."
        if experiment.benchmarking_is_active():
            if len(type_of_benchmark):
                experiment.workload['info'] += "\nBenchmark is '{}'.".format(type_of_benchmark)
                if type_of_benchmark == "ycsb":
                    experiment.workload['info'] += " Workload is '{}'.".format(workload)
        if experiment.loading_is_active() or experiment.benchmarking_is_active():
            if SF:
                experiment.workload['info'] += " Scaling factor is {}.".format(SF)
            experiment.workload['info'] += " Target is based on multiples of '{}'.".format(target_base)
        if experiment.benchmarking_is_active():
            experiment.workload['info'] += " Factors for benchmarking are {}.".format(num_benchmarking_target_factors)
            if extra_keying:
                experiment.workload['info'] += " Benchmarking has keying and thinking times activated."
            if extra_new_connection:
                experiment.workload['info'] += " There is a reconnect for each transaction."
            if SD:
                experiment.workload['info'] += " Benchmarking runs for {} minutes.".format(int(SD / 60))

    def test_results(self, experiment) -> None:
        """
        Validate Benchbase results and print workflow completion status.

        :param experiment: The owning experiment object.
        """
        experiment.cluster.logger.debug('Benchbase.test_results()')
        self.evaluator.test_results()
        workflow = experiment.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")

