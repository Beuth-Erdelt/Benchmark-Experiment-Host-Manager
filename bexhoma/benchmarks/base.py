"""
Abstract Benchmark base classes for bexhoma.

Provides :class:`Benchmark` (abstract) and :class:`DBMSBenchmarkerBenchmark`,
which is the shared base for TPC-H and TPC-DS.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import pandas as pd
from bexhoma import evaluators

__all__ = ["Benchmark", "DBMSBenchmarkerBenchmark"]


class Benchmark:
    """
    Abstract base for all benchmark types.

    Governs result interpretation (evaluator selection, summary display,
    result validation).  Job submission is controlled by the experiment dict
    on each configuration object, not by this class.

    :param name: Short identifier, e.g. ``'ycsb'``.
    :param SF: Scaling factor (meaning varies per benchmark).
    """

    def __init__(self, name: str, SF: str = '1') -> None:
        """
        :param name: Short identifier matching the ``"benchmarker"`` field in experiment dict entries.
        :param SF: Scaling factor.
        """
        self.name: str = name
        self.SF: str = str(SF)
        self.benchmark_index: int = 0   # assigned by experiment.add_benchmark(); 1-based
        self.evaluator = None           # set by experiment.add_benchmark()

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Instantiate and return the evaluator for this benchmark.

        :param code: Experiment identifier (result sub-folder name).
        :param path: Root path containing experiment result folders.
        :param benchmark_run: 1-based position of this benchmark in the sequence.
        :return: Evaluator instance.
        """
        raise NotImplementedError

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI arguments and update experiment workload metadata.

        Called from ``experiment.prepare_testbed()``.

        :param experiment: The owning experiment object.
        :param parameter: Dict of CLI arguments as produced by argparse.
        """
        raise NotImplementedError

    def show_summary(self, experiment) -> None:
        """
        Print a Markdown-formatted benchmark-specific summary.

        :param experiment: The owning experiment object.
        """
        raise NotImplementedError

    def test_results(self, experiment) -> None:
        """
        Validate benchmark results and print pass/fail assertions.

        :param experiment: The owning experiment object.
        """
        raise NotImplementedError


class DBMSBenchmarkerBenchmark(Benchmark):
    """
    Shared base for benchmarks that use the DBMSBenchmarker tool
    (TPC-H, TPC-DS).

    Provides :meth:`create_evaluator` wired to ``evaluators.dbmsbenchmarker``.
    """

    def __init__(self, name: str, SF: str = '1') -> None:
        """
        :param name: Short identifier, e.g. ``'tpch'``.
        :param SF: Scaling factor.
        """
        super().__init__(name=name, SF=SF)

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Return a ``dbmsbenchmarker`` evaluator scoped to this benchmark's index.

        :param code: Experiment identifier.
        :param path: Root result path.
        :param benchmark_run: 1-based benchmark position.
        :return: :class:`evaluators.dbmsbenchmarker` instance.
        """
        return evaluators.dbmsbenchmarker(
            code=code,
            path=path,
            include_loading=True,
            include_benchmarking=True,
            benchmark_run=benchmark_run,
        )

    def test_results(self, experiment) -> None:
        """
        Validate DBMSBenchmarker results and print workflow completion status.

        :param experiment: The owning experiment object.
        """
        experiment.cluster.logger.debug('DBMSBenchmarkerBenchmark.test_results()')
        self.evaluator.test_results()
        workflow = experiment.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")

    def show_summary(self, experiment) -> None:
        """
        Print a Markdown-formatted summary of a DBMSBenchmarker experiment.

        Covers workflow, loading times, per-connection and per-phase execution stats,
        query latencies, SQL errors, SQL warnings, monitoring metrics, and
        pass/fail test assertions.

        :param experiment: The owning experiment object.
        """
        experiment._test_results = []
        self.evaluator.load_inspector()
        connections_sorted, monitoring_applications = experiment.show_summary_header()
        if experiment.benchmarking_is_active():
            print("\n### Workflow")
            df = self.evaluator.get_summary_benchmark_per_connection()
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
        if experiment.loading_is_active():
            print("\n### Loading")
            print("\n#### Per Run\n")
            if is_multitenant:
                df = self.evaluator.get_summary_loading_per_run_multitenant()
            else:
                df = self.evaluator.get_summary_loading_per_run()
            print(df.to_markdown(index=True, floatfmt=".2f"))
        if experiment.benchmarking_is_active():
            print("\n### Execution")
            print("\n#### Per Connection\n")
            df = self.evaluator.get_summary_benchmark_per_connection()
            df.drop('configuration', axis=1, inplace=True, errors='ignore')
            df.drop('pod', axis=1, inplace=True, errors='ignore')
            print(df.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Phase\n")
            if is_multitenant:
                df = self.evaluator.get_summary_benchmark_per_phase_multitenant()
            else:
                df = self.evaluator.get_summary_benchmark_per_phase()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            df_aggregated_reduced = df.copy()
            print("\n### Latency of Timer Execution [ms]")
            num_of_queries = 0
            df_latencies = self.evaluator.get_query_latencies(query_titles=True)
            if df_latencies is not None:
                df_latencies = df_latencies.sort_index().T.round(2)
                df_latencies.index.names = ["Queries"]
                print(df_latencies.to_markdown(index=True, floatfmt=".2f"))
                num_of_queries = len(df_latencies.index)
            print("\n### Errors (failed queries)\n")
            df_errors = self.evaluator.get_total_errors(query_titles=True)
            num_errors = df_errors.sum().sum()
            if num_errors > 0:
                df_error_rows = df_errors[~(df_errors == False).all(axis=1)]
                list_error_queries = list(df_error_rows.index)
                df_errors = df_errors[~(df_errors == False).all(axis=1)]
                print(df_errors.to_markdown(index=True, floatfmt=".2f"))
                for error in list_error_queries:
                    numQuery = error[1:]
                    list_errors = self.evaluator.evaluation.get_error(numQuery)
                    list_errors = {k: v for k, v in list_errors.items() if len(v) > 0}
                    print("* " + error)
                    for k, v in list_errors.items():
                        print("  * {}: {}".format(k, v))
            else:
                print("No errors")
            print("\n### Warnings (result mismatch)\n")
            df_warnings = self.evaluator.get_total_warnings(query_titles=True)
            num_warnings = df_warnings.sum().sum()
            if num_warnings > 0:
                df_warnings = df_warnings[~(df_warnings == False).all(axis=1)]
                print(df_warnings.to_markdown(index=True, floatfmt=".2f"))
            else:
                print("No warnings")
        else:
            df_aggregated_reduced = pd.DataFrame()
            num_errors = 0
            num_warnings = 0
        experiment.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            for title, metrics in monitoring_applications.items():
                print("\n#### " + title + "\n")
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        if experiment.benchmarking_is_active():
            experiment._test_column(df_aggregated_reduced, "Geo Times [s]")
            experiment._test_column(df_aggregated_reduced, "Power@Size [~Q/h]")
            experiment._test_column(df_aggregated_reduced, "Throughput@Size")
            passed_errors = num_errors == 0
            experiment._record_test(passed_errors, "No SQL errors" if passed_errors else "SQL errors")
            passed_warnings = num_warnings == 0
            experiment._record_test(passed_warnings, "No SQL warnings" if passed_warnings else "SQL warnings (result mismatch)")
            experiment._record_test(experiment.test_workflow(workflow_actual, workflow_planned), "Workflow as planned")
        experiment._print_test_summary()
