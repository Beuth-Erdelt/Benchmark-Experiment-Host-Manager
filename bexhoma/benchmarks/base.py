"""
Abstract Benchmark base classes for bexhoma.

Provides :class:`Benchmark` (abstract) and :class:`DBMSBenchmarkerBenchmark`,
which is the shared base for TPC-H and TPC-DS.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dataclasses import dataclass, field

import pandas as pd
from bexhoma import evaluators

__all__ = ["Benchmark", "DBMSBenchmarkerBenchmark", "Section", "render_stdout"]


@dataclass
class Section:
    """
    A titled block of summary content, shared by the stdout renderer
    (:func:`render_stdout`) and the Markdown report writer
    (:mod:`bexhoma.report_writer`).

    Hooks that used to ``print()`` their content directly now build and
    return a tree of :class:`Section` objects instead, so the two renderers
    can format the same underlying data independently (see
    ``bexhoma/experiments/README.md`` §9 for the full rationale).

    :param heading: Section title, without the leading ``#`` characters.
    :param level: Markdown heading depth (``3`` = ``###``, ``4`` = ``####``).
    :param blank_after_heading: Whether an extra blank line follows the
        heading before its content, matching the exact spacing of the
        ``print()`` call this section replaces.
    :param dataframe: Tabular content, rendered via ``.to_markdown()`` when set.
    :param index: Forwarded to ``.to_markdown(index=...)``.
    :param floatfmt: Forwarded to ``.to_markdown(floatfmt=...)``; ``None``
        omits the argument entirely (matches call sites that never set it).
    :param skip_if_empty: When ``True``, an empty ``dataframe`` is not
        rendered at all (the heading still is) — matches call sites that
        guard their ``print(df.to_markdown(...))`` with ``if not df.empty``.
    :param lines: Freeform bullet/text lines, rendered when there is no
        tabular content (or in addition to it, after the table).
    :param children: Nested subsections, rendered after this section's own
        content.
    :param link_connections: Hint to the Markdown report writer that
        ``dataframe``'s index holds connection names, which should be
        rewritten into links to ``connections.md`` before rendering. Ignored
        by :func:`render_stdout`.
    """
    heading: str
    level: int = 3
    blank_after_heading: bool = True
    dataframe: pd.DataFrame | None = None
    index: bool = True
    floatfmt: str | None = ".2f"
    skip_if_empty: bool = False
    lines: list[str] | None = None
    children: list["Section"] = field(default_factory=list)
    link_connections: bool = False


def _render_section_stdout(section: Section) -> None:
    """
    Print one :class:`Section` and its children, reproducing the exact
    ``print()`` sequence the pre-refactor hooks used to emit inline.

    :param section: Section to print.
    """
    heading_line = "\n" + "#" * section.level + " " + section.heading
    if section.blank_after_heading:
        heading_line += "\n"
    print(heading_line)
    if section.dataframe is not None and not (section.skip_if_empty and section.dataframe.empty):
        kwargs = {"index": section.index}
        if section.floatfmt is not None:
            kwargs["floatfmt"] = section.floatfmt
        print(section.dataframe.to_markdown(**kwargs))
    if section.lines:
        for line in section.lines:
            print(line)
    for child in section.children:
        _render_section_stdout(child)


def render_stdout(document: list[Section]) -> None:
    """
    Print a list of top-level :class:`Section` objects to stdout.

    :param document: Top-level sections in display order.
    """
    for section in document:
        _render_section_stdout(section)


def _format_workflow_lines(workflow: dict) -> list[str]:
    """
    Format a workflow dict (actual or planned) into the bullet lines
    ``show_summary()`` used to print inline.

    :param workflow: Workflow dict as produced by
        :meth:`~bexhoma.evaluators.base.EvaluatorBase.reconstruct_workflow`
        or read from ``workload['workflow_planned']``.
    :return: One bullet line per ``(configuration, experiment_run, client)`` triple.
    :rtype: list[str]
    """
    lines = []
    for config, runs in workflow.items():
        for exp_i, run in enumerate(runs, 1):
            for client_j, client_round in enumerate(run, 1):
                jobs_str = ', '.join(
                    f"{job['type']} ({job['pods']} pods)"
                    for job in client_round
                )
                lines.append(f"* DBMS {config} - Experiment {exp_i} Client {client_j}: {jobs_str}")
    return lines


def build_workflow_section(workflow_actual: dict, workflow_planned: dict) -> Section:
    """
    Build the ``### Workflow`` section (Actual vs. Planned) shown for every
    benchmark type. Not a hook — this block was never overridable, so it is
    built directly by :meth:`Benchmark.show_summary` rather than dispatched
    through a subclassable method.

    :param workflow_actual: Reconstructed actual workflow dict.
    :param workflow_planned: Planned workflow dict from workload config.
    :return: The ``Workflow`` section, with an ``Actual``/``Planned`` child
        for each dict that is non-empty.
    :rtype: Section
    """
    children = []
    if workflow_actual:
        children.append(Section(heading="Actual", level=4, lines=_format_workflow_lines(workflow_actual)))
    if workflow_planned:
        children.append(Section(heading="Planned", level=4, lines=_format_workflow_lines(workflow_planned)))
    return Section(heading="Workflow", level=3, blank_after_heading=False, children=children)


def _key_metrics_section_from_columns(df_aggregated_reduced: pd.DataFrame, columns: list[str]) -> "Section | None":
    """
    Build a ``Key Metrics`` section from whichever of ``columns`` are present
    in ``df_aggregated_reduced``.

    Shared helper for :meth:`Benchmark._build_key_metrics_section` overrides,
    so each benchmark-type subclass only needs to name its own tested
    column(s), not duplicate the section-building logic. Report-only: not
    added to the stdout ``document`` in :meth:`Benchmark.show_summary`, since
    ``index.md`` has no stdout equivalent.

    :param df_aggregated_reduced: The per-phase execution DataFrame.
    :param columns: Column names to surface, in the order they were tested by
        this benchmark's evaluator (``evaluator.record_tests()``).
    :return: The ``Key Metrics`` section, or ``None`` when none of
             ``columns`` are present (e.g. benchmarking was not active).
    :rtype: Section | None
    """
    present = [c for c in columns if c in df_aggregated_reduced.columns]
    if not present:
        return None
    return Section(heading="Key Metrics", level=3, dataframe=df_aggregated_reduced[present], link_connections=True)


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

    def _show_loading_sections(self, experiment, is_multitenant: bool) -> tuple[Section | None, pd.DataFrame]:
        """
        Build the loading section and return the per-run loading DataFrame.

        Default builds ``### Loading / #### Per Run`` when loading is active.
        Override to add extra subsections (e.g. ``#### Per Connection`` for YCSB).

        :param experiment: The owning experiment object.
        :param is_multitenant: Whether the experiment runs in multitenant mode.
        :return: Tuple of the ``Loading`` section (``None`` when loading is not
                 active) and the per-run loading DataFrame (empty when not active).
        :rtype: tuple[Section | None, pandas.DataFrame]
        """
        if experiment.loading_is_active():
            if is_multitenant:
                df = self.evaluator.get_summary_loading_per_run_multitenant()
            else:
                df = self.evaluator.get_summary_loading_per_run()
            section = Section(
                heading="Loading", level=3, blank_after_heading=False,
                children=[Section(heading="Per Run", level=4, dataframe=df)],
            )
            return section, df
        return None, pd.DataFrame()

    def _build_reset_section(self, df_connections: pd.DataFrame) -> Section | None:
        """
        Build the ``#### Reset`` subsection: reset-script duration per connection.

        Reads the ``time_reset`` column from ``df_connections`` (populated by
        :meth:`evaluators.base.LogEvaluator.add_connection_to_result` whenever a
        ``resetscript`` ran before that connection's round was submitted). This
        column carries no benchmark-tool-specific data, so the section applies to
        any benchmark type that sets a ``resetscript`` on a benchmarker entry, not
        just Benchbase TPC-C. Returns ``None`` when no connection triggered a reset.

        :param df_connections: Output of ``evaluator.get_connections_of_experiment()``.
        :return: The ``Reset`` section, or ``None`` when nothing to show.
        :rtype: Section | None
        """
        if df_connections.empty or 'time_reset' not in df_connections.columns:
            return None
        df_reset = df_connections[df_connections['time_reset'] > 0][
            ['phase', 'job', 'experiment_run', 'client', 'benchmark_run', 'time_reset']
        ]
        if df_reset.empty:
            return None
        return Section(heading="Reset", level=4, dataframe=df_reset, index=False)

    def _show_extra_sections(self, experiment, df_aggregated_reduced: pd.DataFrame) -> tuple[list[Section], dict, Section | None]:
        """
        Build benchmark-specific sections shown after ``### Benchmarking → Per Phase``.

        Default is a no-op returning no sections, an empty context dict, and no
        report-only section. Override to insert additional output (e.g. query
        latency, SQL errors/warnings for DBMSBenchmarker), to return any extra
        context needed by :meth:`evaluator.record_tests`, and/or a section that
        should only appear in the Markdown report, never in the stdout summary
        (e.g. the full per-query EXPLAIN dump).

        :param experiment: The owning experiment object.
        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: Tuple of extra sections to append to the summary; an extra
                 context dict forwarded as keyword arguments to
                 ``evaluator.record_tests()``; and a report-only section (or
                 ``None``).
        :rtype: tuple[list[Section], dict, Section | None]
        """
        return [], {}, None

    def _build_benchmarking_section(self, df_connections: pd.DataFrame, is_multitenant: bool) -> tuple[Section, pd.DataFrame]:
        """
        Build the ``### Benchmarking`` section (Per Connection, Per Phase, Reset).

        Not a hook — this block was never overridable, so it is built directly
        by :meth:`show_summary` rather than dispatched through a subclassable
        method.

        :param df_connections: Output of ``evaluator.get_connections_of_experiment()``.
        :param is_multitenant: Whether the experiment runs in multitenant mode.
        :return: Tuple of the ``Benchmarking`` section and the per-phase DataFrame
                 (needed downstream by ``evaluator.record_tests()``).
        :rtype: tuple[Section, pandas.DataFrame]
        """
        df_conn = self.evaluator.get_summary_benchmark_per_connection()
        if is_multitenant:
            df_phase = self.evaluator.get_summary_benchmark_per_phase_multitenant()
        else:
            df_phase = self.evaluator.get_summary_benchmark_per_phase()
        df_aggregated_reduced = df_phase.copy()
        children = [
            Section(heading="Per Connection", level=4, dataframe=df_conn, skip_if_empty=True, link_connections=True),
            Section(heading="Per Phase", level=4, dataframe=df_phase),
        ]
        reset_section = self._build_reset_section(df_connections)
        if reset_section is not None:
            children.append(reset_section)
        return Section(heading="Benchmarking", level=3, blank_after_heading=False, children=children), df_aggregated_reduced

    def _build_key_metrics_section(self, df_aggregated_reduced: pd.DataFrame) -> Section | None:
        """
        Build the headline performance metric(s) for this benchmark type, to
        surface in ``index.md``'s Key Metrics block.

        Report-only — never added to the stdout ``document`` in
        :meth:`show_summary`, since ``index.md`` has no stdout equivalent.
        Default: no key metrics. Override with the exact column name(s) this
        benchmark's evaluator already tests via ``evaluator.record_tests()``'s
        ``experiment._test_column()`` calls, so ``index.md``'s headline number
        always matches what backs the Tests table's pass/fail row for it —
        this is deliberately benchmark-specific knowledge, so it lives here,
        not in the generic :mod:`bexhoma.report_writer`.

        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: A ``Key Metrics`` section, or ``None`` when this benchmark
                 type defines no headline metric (or benchmarking was not
                 active, so the DataFrame is empty).
        :rtype: Section | None
        """
        return None

    def show_summary(self, experiment, write_report: bool = False) -> None:
        """
        Print a Markdown-formatted summary of the experiment, and optionally
        write it to a tiered Markdown report in the result folder.

        Template method: the shared header and monitoring sections are printed
        directly by ``experiment.show_summary_header()``/
        ``experiment.show_summary_monitoring()``; workflow, loading, benchmarking,
        and extra sections are built as a :class:`Section` tree (loading via
        :meth:`_show_loading_sections`, extra sections via
        :meth:`_show_extra_sections`) and printed via :func:`render_stdout` so
        that the same tree can also be handed to
        :func:`bexhoma.report_writer.write_markdown_report` unchanged. Test
        assertions are delegated to :meth:`evaluator.record_tests`.

        :param experiment: The owning experiment object.
        :param write_report: When ``True``, also write a tiered Markdown report
            (``report/index.md`` + detail files) to the result folder.
        """
        experiment._test_results = list(experiment._runtime_test_results)
        self._prepare_evaluator(experiment)
        connections_sorted, monitoring_applications = experiment.show_summary_header()
        workflow_section: Section | None = None
        workflow_actual: dict = {}
        workflow_planned: dict = {}
        df_connections = pd.DataFrame()
        if experiment.benchmarking_is_active():
            df_connections = self.evaluator.get_connections_of_experiment()
            workflow_actual = self.evaluator.reconstruct_workflow(df_connections)
            workflow_planned = experiment.workload.get('workflow_planned', {})
            workflow_section = build_workflow_section(workflow_actual, workflow_planned)
        is_multitenant = experiment.num_tenants > 0
        loading_section, df_loading = self._show_loading_sections(experiment, is_multitenant)
        df_aggregated_reduced = pd.DataFrame()
        benchmarking_section: Section | None = None
        key_metrics_section: Section | None = None
        if experiment.benchmarking_is_active():
            benchmarking_section, df_aggregated_reduced = self._build_benchmarking_section(df_connections, is_multitenant)
            key_metrics_section = self._build_key_metrics_section(df_aggregated_reduced)
        extra_sections, extra_context, explain_section = self._show_extra_sections(experiment, df_aggregated_reduced)
        document: list[Section] = [
            section for section in (workflow_section, loading_section, benchmarking_section)
            if section is not None
        ] + extra_sections
        render_stdout(document)
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
        if write_report:
            print("{:30s}: cleaning up per-connection artefacts".format("Experiment"))
            component_types = ['loading', 'benchmarking', 'loader', 'benchmarker'] + list(experiment.workload['monitoring_components'])
            for component_type in component_types:
                self.evaluator.transform_monitoring_results(component=component_type)
            self.evaluator.cleanup_connection_subfolders()
            print("{:30s}: cleaning up per-connection artefacts completed".format("Experiment"))
            from bexhoma.report_writer import write_markdown_report
            write_markdown_report(
                experiment=experiment,
                benchmark=self,
                workflow_section=workflow_section,
                loading_section=loading_section,
                benchmarking_section=benchmarking_section,
                extra_sections=extra_sections,
                explain_section=explain_section,
                key_metrics_section=key_metrics_section,
                connections_sorted=connections_sorted,
                monitoring_applications=monitoring_applications,
                extra_context=extra_context,
                df_connections=df_connections,
            )
        experiment._print_test_summary()

    def show_summary_section(self, experiment) -> Section | None:
        """
        Build this benchmark's own benchmarking results as a section inside a
        multi-benchmark summary.

        Called for every registered benchmark after the primary benchmark's
        :meth:`show_summary` has already printed the shared experiment header,
        workflow, loading section, monitoring, and test summary — none of that
        is repeated here. Mirrors the ``### Benchmarking`` part of
        :meth:`show_summary` (Per Connection, Per Phase, Reset), scoped to this
        benchmark's own results via ``self.evaluator`` (constructed with this
        benchmark's own ``benchmark_run`` in :meth:`create_evaluator`, so the
        underlying log-to-df pipeline already filters to only this benchmark's
        own connections).

        Override when a benchmark needs different or no section here — e.g.
        :class:`~bexhoma.benchmarks.refresh.RefreshStreamBenchmark` overrides
        this because it has no per-query metrics of its own, only timing.

        :param experiment: The owning experiment object.
        :return: The benchmark's own section, or ``None`` when benchmarking is
                 not active.
        :rtype: Section | None
        """
        if not experiment.benchmarking_is_active():
            return None
        df_conn = self.evaluator.get_summary_benchmark_per_connection()
        if experiment.num_tenants > 0:
            df_phase = self.evaluator.get_summary_benchmark_per_phase_multitenant()
        else:
            df_phase = self.evaluator.get_summary_benchmark_per_phase()
        children = [
            Section(heading="Per Connection", level=4, dataframe=df_conn, skip_if_empty=True, link_connections=True),
            Section(heading="Per Phase", level=4, dataframe=df_phase),
        ]
        df_connections = self.evaluator.get_connections_of_experiment()
        reset_section = self._build_reset_section(df_connections)
        if reset_section is not None:
            children.append(reset_section)
        return Section(heading=self.name, level=3, blank_after_heading=False, children=children)

    def test_results(self, experiment) -> None:
        """
        Validate results and print workflow completion status.

        Compares the experiment's full planned workflow
        (:meth:`~bexhoma.experiments.base.ExperimentBase.get_workflow_list`)
        against this benchmark's evaluator's reconstructed actual workflow.
        Both cover the whole client round, not just this benchmark's own
        entries (see :meth:`~bexhoma.evaluators.logger.LogEvaluator.test_results`),
        so the comparison is correct whether this benchmark is the primary or a
        co-running secondary benchmark. Override for a benchmark with no
        per-query results of its own to validate, e.g.
        :class:`~bexhoma.benchmarks.refresh.RefreshStreamBenchmark`.

        :param experiment: The owning experiment object.
        """
        experiment.cluster.logger.debug(f'{type(self).__name__}.test_results()')
        self.evaluator.test_results()
        workflow = experiment.get_workflow_list()
        if workflow == self.evaluator.workflow:
            print("Result workflow complete")
        else:
            print("Result workflow not complete")


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
            name=self.name,
        )

    def _prepare_evaluator(self, experiment) -> None:
        """
        Load the DBMSBenchmarker inspector before the summary is printed.

        :param experiment: The owning experiment object.
        """
        self.evaluator.load_inspector()

    def _build_key_metrics_section(self, df_aggregated_reduced: pd.DataFrame) -> Section | None:
        """
        Surface Geo Times, Power@Size, and Throughput@Size — the same columns
        :meth:`~bexhoma.evaluators.dbmsbenchmarker.dbmsbenchmarker.record_tests`
        tests via ``experiment._test_column()``.

        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: A ``Key Metrics`` section, or ``None`` when none of the
                 tested columns are present.
        :rtype: Section | None
        """
        return _key_metrics_section_from_columns(
            df_aggregated_reduced, ["Geo Times [s]", "Power@Size [~Q/h]", "Throughput@Size"]
        )

    def _show_extra_sections(self, experiment, df_aggregated_reduced: pd.DataFrame) -> tuple[list[Section], dict, Section | None]:
        """
        Build secondary-benchmark sections, query latency, SQL errors, and warnings.

        :param experiment: The owning experiment object.
        :param df_aggregated_reduced: The per-phase execution DataFrame.
        :return: Tuple of the extra sections to append to the summary; a dict
                 with ``num_errors``, ``num_warnings``, ``num_active_queries``,
                 and ``num_queries_with_explain`` for test recording; and a
                 report-only ``EXPLAIN`` detail section (or ``None``), shown
                 in ``benchmarking.md`` but never in the stdout summary.
        :rtype: tuple[list[Section], dict, Section | None]
        """
        if not experiment.benchmarking_is_active():
            return [], {"num_errors": 0, "num_warnings": 0, "num_active_queries": 0, "num_queries_with_explain": 0}, None
        sections: list[Section] = []
        for bm in experiment.benchmarks:
            if bm.benchmark_index == self.benchmark_index:
                continue
            section = bm.show_summary_section(experiment)
            if section is not None:
                sections.append(section)

        latency_section = Section(heading="Latency of Timer Execution [ms]", level=3, blank_after_heading=False)
        df_latencies = self.evaluator.get_query_latencies(query_titles=True)
        if df_latencies is not None:
            df_latencies = df_latencies.sort_index().T.round(2)
            df_latencies.index.names = ["Queries"]
            latency_section.dataframe = df_latencies
        sections.append(latency_section)

        errors_section = Section(heading="Errors (failed queries)", level=3)
        df_errors = self.evaluator.get_total_errors(query_titles=True)
        num_errors = df_errors.sum().sum()
        if num_errors > 0:
            errors_section.dataframe = df_errors[~(df_errors == 0).all(axis=1)]
            failing_cols_mask = (df_errors != 0).any(axis=0)
            list_error_query_titles = list(df_errors.columns[failing_cols_mask])
            df_errors_by_num = self.evaluator.get_total_errors(query_titles=False)
            list_error_query_nums = list(df_errors_by_num.columns[failing_cols_mask])
            error_lines: list[str] = []
            for query_title, query_num in zip(list_error_query_titles, list_error_query_nums):
                query_num_stripped = str(query_num).lstrip('Q')
                list_errors = self.evaluator.evaluation.get_error(query_num_stripped)
                list_errors = {k: v for k, v in list_errors.items() if len(v) > 0}
                error_lines.append("* " + query_title)
                for k, v in list_errors.items():
                    error_lines.append(f"  * {k}: {v}")
            errors_section.lines = error_lines
        else:
            errors_section.lines = ["No errors"]
        sections.append(errors_section)

        warnings_section = Section(heading="Warnings (result mismatch)", level=3)
        df_warnings = self.evaluator.get_total_warnings(query_titles=True)
        num_warnings = df_warnings.sum().sum()
        if num_warnings > 0:
            warnings_section.dataframe = df_warnings[~(df_warnings == 0).all(axis=1)]
        else:
            warnings_section.lines = ["No warnings"]
        sections.append(warnings_section)

        # EXPLAIN is opt-in evidence (dbmsbenchmarker's -se/--store-explain). The full
        # per-connection dump is report-only (see explain_section below, rendered into
        # benchmarking.md but never printed to stdout) — show_summary() only sees a
        # pass/fail/skipped Tests-table row (record_tests() in evaluators/dbmsbenchmarker.py).
        df_errors_by_num = self.evaluator.get_total_errors(query_titles=False)
        explain_lines: list[str] = []
        num_active_queries = len(df_errors.columns)
        num_queries_with_explain = 0
        for query_title, query_num in zip(list(df_errors.columns), list(df_errors_by_num.columns)):
            query_num_stripped = str(query_num).lstrip('Q')
            list_explains = self.evaluator.evaluation.get_explain(query_num_stripped)
            list_explains = {k: v for k, v in list_explains.items() if len(v) > 0}
            if not list_explains:
                continue
            num_queries_with_explain += 1
            explain_lines.append("* " + query_title)
            for connection_name, explain_text in list_explains.items():
                explain_lines.append(f"  * {connection_name}")
                explain_lines.append("    ```text")
                explain_lines.extend("    " + line for line in explain_text.splitlines())
                explain_lines.append("    ```")
        explain_section = Section(heading="EXPLAIN", level=3, lines=explain_lines) if explain_lines else None

        extra_context = {
            "num_errors": num_errors,
            "num_warnings": num_warnings,
            "num_active_queries": num_active_queries,
            "num_queries_with_explain": num_queries_with_explain,
        }
        return sections, extra_context, explain_section
