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

    def _prepare_evaluator(self, experiment) -> None:
        """
        Prepare the evaluator before the summary is printed.

        Called at the start of :meth:`show_summary`. Default is a no-op; override
        to perform any evaluator setup that must happen before data is read.

        :param experiment: The owning experiment object.
        """

    def _show_loading_sections(self, experiment, is_multitenant: bool) -> pd.DataFrame:
        """
        Print the loading section and return the per-run loading DataFrame.

        Default prints ``### Loading / #### Per Run`` when loading is active.
        Override to add extra subsections (e.g. ``#### Per Connection`` for YCSB).

        :param experiment: The owning experiment object.
        :param is_multitenant: Whether the experiment runs in multitenant mode.
        :return: Per-run loading DataFrame, or an empty DataFrame when loading is
                 not active.
        :rtype: pandas.DataFrame
        """
        if experiment.loading_is_active():
            print("\n### Loading")
            print("\n#### Per Run\n")
            if is_multitenant:
                df = self.evaluator.get_summary_loading_per_run_multitenant()
            else:
                df = self.evaluator.get_summary_loading_per_run()
            print(df.to_markdown(index=True, floatfmt=".2f"))
            return df
        return pd.DataFrame()

    def _show_extra_sections(self, experiment, df_aggregated_reduced: pd.DataFrame) -> dict:
        """
        Print benchmark-specific sections after ``### Execution → Per Phase``.

        Default is a no-op returning an empty dict. Override to insert additional
        output (e.g. query latency, SQL errors/warnings for DBMSBenchmarker) and
        to return any extra context needed by :meth:`evaluator.record_tests`.

        :param experiment: The owning experiment object.
        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: Extra context dict forwarded as keyword arguments to
                 ``evaluator.record_tests()``.
        :rtype: dict
        """
        return {}

    def show_summary(self, experiment) -> None:
        """
        Print a Markdown-formatted summary of the experiment.

        Template method: shared header, workflow, loading, execution, monitoring,
        and application-metrics sections are printed here; benchmark-specific
        loading display is delegated to :meth:`_show_loading_sections`, extra
        post-execution sections to :meth:`_show_extra_sections`, and test
        assertions to :meth:`evaluator.record_tests`.

        :param experiment: The owning experiment object.
        """
        experiment._test_results = []
        self._prepare_evaluator(experiment)
        connections_sorted, monitoring_applications = experiment.show_summary_header()
        workflow_actual: dict = {}
        workflow_planned: dict = {}
        if experiment.benchmarking_is_active():
            print("\n### Workflow")
            df_conn = self.evaluator.get_connections_of_experiment()
            workflow_actual = self.evaluator.reconstruct_workflow(df_conn)
            workflow_planned = experiment.workload['workflow_planned']
            if workflow_actual:
                print("\n#### Actual\n")
                for config, runs in workflow_actual.items():
                    for exp_i, run in enumerate(runs, 1):
                        for client_j, client_round in enumerate(run, 1):
                            jobs_str = ', '.join(
                                f"{job['type']} ({job['pods']} pods)"
                                for job in client_round
                            )
                            print(f"* DBMS {config} - Experiment {exp_i} Client {client_j}: {jobs_str}")
            if workflow_planned:
                print("\n#### Planned\n")
                for config, runs in workflow_planned.items():
                    for exp_i, run in enumerate(runs, 1):
                        for client_j, client_round in enumerate(run, 1):
                            jobs_str = ', '.join(
                                f"{job['type']} ({job['pods']} pods)"
                                for job in client_round
                            )
                            print(f"* DBMS {config} - Experiment {exp_i} Client {client_j}: {jobs_str}")
        is_multitenant = experiment.num_tenants > 0
        df_loading = self._show_loading_sections(experiment, is_multitenant)
        df_aggregated_reduced = pd.DataFrame()
        if experiment.benchmarking_is_active():
            print("\n### Execution")
            print("\n#### Per Connection\n")
            df_conn = self.evaluator.get_summary_benchmark_per_connection()
            if not df_conn.empty:
                print(df_conn.to_markdown(index=True, floatfmt=".2f"))
            print("\n#### Per Phase\n")
            if is_multitenant:
                df_phase = self.evaluator.get_summary_benchmark_per_phase_multitenant()
            else:
                df_phase = self.evaluator.get_summary_benchmark_per_phase()
            print(df_phase.to_markdown(index=True, floatfmt=".2f"))
            df_aggregated_reduced = df_phase.copy()
        extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)
        experiment.show_summary_monitoring()
        if len(monitoring_applications) > 0:
            print("\n### Application Metrics")
            for title, metrics in monitoring_applications.items():
                print("\n#### " + title + "\n")
                metrics.index.names = ["DBMS"]
                print(metrics.to_markdown(index=True, floatfmt=".2f"))
        self.evaluator.record_tests(
            experiment, df_loading, df_aggregated_reduced,
            workflow_actual, workflow_planned, **extra_context
        )
        experiment._print_test_summary()

    def show_summary_section(self, experiment) -> None:
        """
        Print a benchmark-specific section inside a multi-benchmark summary.

        Called for every registered benchmark after the primary benchmark's
        :meth:`show_summary` has already printed the experiment header.
        Override in subclasses that need to display results for a co-running
        secondary benchmarker.  The default implementation is a no-op so that
        benchmarks used only as primaries do not need to override this method.

        :param experiment: The owning experiment object.
        """

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

    def _prepare_evaluator(self, experiment) -> None:
        """
        Load the DBMSBenchmarker inspector before the summary is printed.

        :param experiment: The owning experiment object.
        """
        self.evaluator.load_inspector()

    def _show_extra_sections(self, experiment, df_aggregated_reduced: pd.DataFrame) -> dict:
        """
        Print secondary-benchmark sections, query latency, SQL errors, and warnings.

        :param experiment: The owning experiment object.
        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: Dict with ``num_errors`` and ``num_warnings`` for test recording.
        :rtype: dict
        """
        if not experiment.benchmarking_is_active():
            return {"num_errors": 0, "num_warnings": 0}
        for bm in experiment.benchmarks:
            if bm.benchmark_index == self.benchmark_index:
                continue
            bm.show_summary_section(experiment)
        print("\n### Latency of Timer Execution [ms]")
        df_latencies = self.evaluator.get_query_latencies(query_titles=True)
        if df_latencies is not None:
            df_latencies = df_latencies.sort_index().T.round(2)
            df_latencies.index.names = ["Queries"]
            print(df_latencies.to_markdown(index=True, floatfmt=".2f"))
        print("\n### Errors (failed queries)\n")
        df_errors = self.evaluator.get_total_errors(query_titles=True)
        num_errors = df_errors.sum().sum()
        if num_errors > 0:
            df_errors_display = df_errors[~(df_errors == 0).all(axis=1)]
            print(df_errors_display.to_markdown(index=True, floatfmt=".2f"))
            failing_cols_mask = (df_errors != 0).any(axis=0)
            list_error_query_titles = list(df_errors.columns[failing_cols_mask])
            df_errors_by_num = self.evaluator.get_total_errors(query_titles=False)
            list_error_query_nums = list(df_errors_by_num.columns[failing_cols_mask])
            for query_title, query_num in zip(list_error_query_titles, list_error_query_nums):
                list_errors = self.evaluator.evaluation.get_error(query_num)
                list_errors = {k: v for k, v in list_errors.items() if len(v) > 0}
                print("* " + query_title)
                for k, v in list_errors.items():
                    print(f"  * {k}: {v}")
        else:
            print("No errors")
        print("\n### Warnings (result mismatch)\n")
        df_warnings = self.evaluator.get_total_warnings(query_titles=True)
        num_warnings = df_warnings.sum().sum()
        if num_warnings > 0:
            df_warnings = df_warnings[~(df_warnings == 0).all(axis=1)]
            print(df_warnings.to_markdown(index=True, floatfmt=".2f"))
        else:
            print("No warnings")
        return {"num_errors": num_errors, "num_warnings": num_warnings}
