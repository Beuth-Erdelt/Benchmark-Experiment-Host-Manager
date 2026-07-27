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
from .base import Benchmark, Section, _key_metrics_section_from_columns

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
            name=self.name,
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
        scaling_logging = int(args.scaling_logging)
        max_execution_time = int(args.max_execution_time)
        num_sut_replicas = int(args.num_sut_replicas)
        num_pd_nodes = int(args.num_pd_nodes)
        num_loading_target_factors = experiment.get_parameter_as_list('num_loading_target_factors')
        num_benchmarking_target_factors = experiment.get_parameter_as_list('num_benchmarking_target_factors')
        if mode == 'run':
            experiment.set_workload(
                name=f'YCSB SF={SF}',
                info='This experiment compares run time and resource consumption of YCSB queries.',
                type='ycsb',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name=f'YCSB Data Loading SF={SF}',
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
        experiment.workload['info'] += f"\nWorkload is '{args.workload.upper()}'."
        if experiment.loading_is_active():
            experiment.workload['info'] += f"\nNumber of rows to insert is {ycsb_rows}."
            experiment.workload['info'] += f"\nOrdering of inserts is {extra_insert_order}."
        if experiment.benchmarking_is_active():
            experiment.workload['info'] += f"\nNumber of operations is {ycsb_operations}."
            experiment.workload['info'] += f"\nBatch size is '{batchsize}'."
        if experiment.loading_is_active() or experiment.benchmarking_is_active():
            experiment.workload['info'] += f"\nTarget is based on multiples of '{target_base}'."
        if experiment.loading_is_active():
            experiment.workload['info'] += f"\nFactors for loading are {num_loading_target_factors}."
        if experiment.benchmarking_is_active():
            experiment.workload['info'] += f"\nFactors for benchmarking are {num_benchmarking_target_factors}."
            if args.activate_reset:
                experiment.workload['info'] += " A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round."
            if max_execution_time > 0:
                experiment.workload['info'] += f"\nBenchmarking is capped at {max_execution_time}s execution time."
        if experiment.loading_is_active() or experiment.benchmarking_is_active():
            experiment.workload['info'] += f"\nStatus is logged every {scaling_logging}s."
        if "TiDB" in args.dbms or len(args.dbms) == 0:
            experiment.workload['info'] += f"\nTiDB uses {num_sut_replicas} SUT replica(s) and {num_pd_nodes} PD node(s)."

    def _show_loading_sections(self, experiment, is_multitenant: bool) -> tuple[Section | None, pd.DataFrame]:
        """
        Build Per Connection and Per Run loading sections for YCSB.

        :param experiment: The owning experiment object.
        :param is_multitenant: Whether the experiment runs in multitenant mode.
        :return: Tuple of the ``Loading`` section (``None`` when no loading data
                 is available) and the per-run loading DataFrame.
        :rtype: tuple[Section | None, pandas.DataFrame]
        """
        df_loading = self.evaluator.get_summary_loading_per_connection()
        if experiment.loading_is_active() and not df_loading.empty:
            if is_multitenant:
                df_aggregated_loaded = self.evaluator.get_summary_loading_per_run_multitenant()
            else:
                df_aggregated_loaded = self.evaluator.get_summary_loading_per_run()
            section = Section(
                heading="Loading", level=3, blank_after_heading=False,
                children=[
                    Section(heading="Per Connection", level=4, dataframe=df_loading, link_connections=True),
                    Section(heading="Per Run", level=4, dataframe=df_aggregated_loaded),
                ],
            )
            return section, df_aggregated_loaded
        return None, pd.DataFrame()

    def _build_key_metrics_section(self, df_aggregated_reduced: pd.DataFrame) -> Section | None:
        """
        Surface ``[OVERALL].Throughput(ops/sec)`` — the same column
        :meth:`~bexhoma.evaluators.ycsb.ycsb.record_tests` tests via
        ``experiment._test_column()``.

        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: A ``Key Metrics`` section, or ``None`` when the tested
                 column is not present.
        :rtype: Section | None
        """
        return _key_metrics_section_from_columns(df_aggregated_reduced, ["[OVERALL].Throughput(ops/sec)"])
