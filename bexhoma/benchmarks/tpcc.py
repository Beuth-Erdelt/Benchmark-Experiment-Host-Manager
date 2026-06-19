"""
Benchmark class for TPC-C (HammerDB) experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
from types import SimpleNamespace

from bexhoma import evaluators
from .base import Benchmark

__all__ = ["TPCC"]


class TPCC(Benchmark):
    """
    Benchmark class for TPC-C experiments run via HammerDB.

    :param SF: Scaling factor — number of TPC-C warehouses.
    """

    def __init__(self, SF: str = '1') -> None:
        """
        :param SF: Scaling factor (number of warehouses).
        """
        super().__init__(name='hammerdb', SF=SF)

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Return a TPC-C evaluator scoped to this benchmark's index.

        :param code: Experiment identifier.
        :param path: Root result path.
        :param benchmark_run: 1-based benchmark position.
        :return: :class:`evaluators.tpcc` instance.
        """
        return evaluators.tpcc(
            code=code,
            path=path,
            include_loading=False,
            include_benchmarking=True,
            benchmark_run=benchmark_run,
        )

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set TPC-C workload metadata on the experiment.

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
        SD = int(args.scaling_duration)
        extra_latency = int(args.extra_latency)
        extra_keying = int(args.extra_keying)
        if mode == 'run':
            experiment.set_workload(
                name='HammerDB Workload SF={} (warehouses for TPC-C)'.format(SF),
                info='This experiment compares run time and resource consumption of TPC-C queries in different DBMS.',
                type='tpcc',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name='HammerDB Data Loading SF={} (warehouses for TPC-C)'.format(SF),
                info='This imports TPC-C data sets.',
                type='tpcc',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_workload(
                name='HammerDB Start DBMS',
                info='This just starts a SUT.',
                intro='Start DBMS and do not load data.',
                type='tpcc',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.set_experiment(script='Schema')
        if experiment.loading_is_active():
            experiment.workload['info'] += "\nTPC-C data is generated and loaded using several threads."
        if experiment.loading_is_active() or experiment.benchmarking_is_active():
            if SF:
                experiment.workload['info'] += "\nScaling factor (i.e., number of warehouses) is {}.".format(SF)
        if experiment.benchmarking_is_active():
            if SD:
                experiment.workload['info'] += " Benchmarking runs for {} minutes.".format(SD)
            if extra_keying:
                experiment.workload['info'] += " Benchmarking has keying and thinking times activated."
            if extra_latency:
                experiment.workload['info'] += " Benchmarking also logs latencies."

    def test_results(self, experiment) -> None:
        """
        Validate TPC-C results and print workflow completion status.

        :param experiment: The owning experiment object.
        """
        experiment.cluster.logger.debug('TPCC.test_results()')
        self.evaluator.test_results()
        workflow = experiment.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")

