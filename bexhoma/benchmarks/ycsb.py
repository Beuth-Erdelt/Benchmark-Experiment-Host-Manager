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

    def show_summary(self, experiment) -> None:
        """
        Print a Markdown-formatted summary of a YCSB experiment.

        :param experiment: The owning experiment object.
        """
        experiment._test_results = []
        connections_sorted, monitoring_applications = experiment.show_summary_header()
        df = self.evaluator.get_df_benchmarking()
        if experiment.benchmarking_is_active():
            print("\n### Workflow")
            workflow_actual = self.evaluator.reconstruct_workflow(df)
            workflow_planned = experiment.workload['workflow_planned']
            if len(workflow_actual) > 0:
                print("\n#### Actual\n")
                for c in workflow_actual:
                    print("* DBMS", c, "- Pods", workflow_actual[c])
            if len(workflow_planned) > 0:
                print("\n#### Planned\n")
                for c in workflow_planned:
                    print("* DBMS", c, "- Pods", workflow_planned[c])
        is_multitenant = experiment.num_tenants > 0
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
            test_loading = True
        else:
            df_aggregated_loaded = pd.DataFrame()
            test_loading = False
        if experiment.benchmarking_is_active():
            print("\n### Execution")
            print("\n#### Per Connection\n")
            df = self.evaluator.get_summary_benchmark_per_connection()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Phase\n")
            if is_multitenant:
                df = self.evaluator.get_summary_benchmark_per_phase_multitenant()
            else:
                df = self.evaluator.get_summary_benchmark_per_phase()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            df_aggregated_reduced = df.copy()
        else:
            df_aggregated_reduced = pd.DataFrame()
        contains_failed = any('FAILED' in col for col in df_aggregated_reduced.columns)
        experiment.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            for title, metrics in monitoring_applications.items():
                print("\n#### " + title + "\n")
                metrics.index.names = ["DBMS"]
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        if test_loading:
            experiment._test_column(df_aggregated_loaded, "[OVERALL].Throughput(ops/sec)", title="Loading Phase:")
        experiment._test_column(df_aggregated_reduced, "[OVERALL].Throughput(ops/sec)", title="Execution Phase:")
        if experiment.benchmarking_is_active():
            experiment._record_test(experiment.test_workflow(workflow_actual, workflow_planned), "Workflow as planned")
        experiment._record_test(
            not contains_failed,
            "Execution Phase: contains no FAILED column" if not contains_failed else "Execution Phase: contains FAILED column",
        )
        experiment._print_test_summary()
        return not contains_failed
