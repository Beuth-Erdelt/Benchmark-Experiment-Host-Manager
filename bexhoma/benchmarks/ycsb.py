"""
Benchmark class for YCSB experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
from types import SimpleNamespace

from bexhoma import evaluators
from .base import Benchmark

__all__ = ["YCSB"]


class YCSB(Benchmark):
    """
    Benchmark class for YCSB (Yahoo Cloud Serving Benchmark).

    :param SF: Scaling factor — dataset size in GB (1 SF ≈ 1 000 000 rows of ~1 kB).
    """

    def __init__(self, SF: str = '1') -> None:
        """
        :param SF: Scaling factor.
        """
        super().__init__(name='ycsb', SF=SF)

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Return a YCSB evaluator scoped to this benchmark's index.

        :param code: Experiment identifier.
        :param path: Root result path.
        :param benchmark_run: 1-based benchmark position.
        :return: :class:`evaluators.ycsb` instance.
        """
        return evaluators.ycsb(
            code=code,
            path=path,
            include_loading=False,
            include_benchmarking=True,
            benchmark_run=benchmark_run,
        )

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set YCSB workload metadata on the experiment.

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
        SFO = str(args.scaling_factor_operations)
        if SFO == 'None':
            SFO = SF
        ycsb_rows = int(SF) * 1000000
        ycsb_operations = int(SFO) * 1000000
        target_base = int(args.target_base)
        extra_insert_order = args.extra_insert_order
        batchsize = args.scaling_batchsize
        num_loading_target_factors = experiment.get_parameter_as_list('num_loading_target_factors')
        num_benchmarking_target_factors = experiment.get_parameter_as_list('num_benchmarking_target_factors')
        if mode == 'run':
            experiment.set_workload(
                name='YCSB SF=' + str(SF),
                info='This experiment compares run time and resource consumption of YCSB queries.',
                type='ycsb',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name='YCSB Data Loading SF=' + str(SF),
                info='This imports YCSB data sets.',
                type='ycsb',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_workload(
                name='YCSB Start DBMS',
                info='This just starts a SUT.',
                intro='Start DBMS and do not load data.',
                type='ycsb',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.set_experiment(script='Schema')
        experiment.workload['info'] += "\nWorkload is '{}'.".format(args.workload.upper())
        if experiment.loading_is_active():
            experiment.workload['info'] += "\nNumber of rows to insert is {}.".format(ycsb_rows)
            experiment.workload['info'] += "\nOrdering of inserts is {}.".format(extra_insert_order)
        if experiment.benchmarking_is_active():
            experiment.workload['info'] += "\nNumber of operations is {}.".format(ycsb_operations)
            experiment.workload['info'] += "\nBatch size is '{}'.".format(batchsize)
        if experiment.loading_is_active() or experiment.benchmarking_is_active():
            experiment.workload['info'] += "\nTarget is based on multiples of '{}'.".format(target_base)
        if experiment.loading_is_active():
            experiment.workload['info'] += "\nFactors for loading are {}.".format(num_loading_target_factors)
        if experiment.benchmarking_is_active():
            experiment.workload['info'] += "\nFactors for benchmarking are {}.".format(num_benchmarking_target_factors)

    def test_results(self, experiment) -> None:
        """
        Validate YCSB results and print workflow completion status.

        :param experiment: The owning experiment object.
        """
        experiment.cluster.logger.debug('YCSB.test_results()')
        self.evaluator.test_results()
        workflow = experiment.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")

    def _show_loading_sections(self, experiment, is_multitenant: bool) -> 'pd.DataFrame':
        """
        Print Per Connection and Per Run loading tables for YCSB.

        :param experiment: The owning experiment object.
        :param is_multitenant: Whether the experiment runs in multitenant mode.
        :return: Per-run loading DataFrame, or an empty DataFrame when no loading
                 data is available.
        :rtype: pandas.DataFrame
        """
        df_loading = self.evaluator.get_summary_loading_per_connection()
        if experiment.loading_is_active() and not df_loading.empty:
            print("\n### Loading")
            print("\n#### Per Connection\n")
            print(df_loading.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Run\n")
            if is_multitenant:
                df_aggregated_loaded = self.evaluator.get_summary_loading_per_run_multitenant()
            else:
                df_aggregated_loaded = self.evaluator.get_summary_loading_per_run()
            print(df_aggregated_loaded.to_markdown(index=True, floatfmt=".2f"))
            return df_aggregated_loaded
        return pd.DataFrame()
