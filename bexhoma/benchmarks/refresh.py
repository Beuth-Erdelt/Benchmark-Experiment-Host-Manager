"""
Benchmark class for co-running stream benchmarkers (e.g. TPC-H refresh stream).

Provides :class:`RefreshStreamBenchmark`, a lightweight :class:`Benchmark`
subclass for secondary benchmarker jobs that run in parallel with a primary
benchmark inside the same client round.  These jobs produce no query metrics;
their contribution is recorded as wall-clock timing only.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import evaluators
from .base import Benchmark

__all__ = ["RefreshStreamBenchmark"]


class RefreshStreamBenchmark(Benchmark):
    """
    Benchmark class for a co-running refresh / maintenance stream.

    Registered alongside the primary benchmark (e.g. ``TPCH``) via
    :meth:`~bexhoma.experiments.mixed.mixed.add_benchmark`.  The job runs
    as ``benchmark_run = self.benchmark_index`` (typically 2) in parallel
    with the query stream.

    No query metrics are collected.  :meth:`show_summary_section` prints
    the wall-clock timing (begin, end, duration) for each client round,
    reading from the timing stored in each connection's ``.config`` file
    by :meth:`~bexhoma.experiments.base.base.end_benchmarking`.

    The k8s job template must name the main container ``dbmsbenchmarker``
    so that the log file ends with ``.dbmsbenchmarker.log`` and the standard
    timing infrastructure picks it up automatically.

    :param name: Short identifier; must match the ``"benchmarker"`` field in
        the experiment dict entry (e.g. ``'tpch_refresh'``).
    :param SF: Scaling factor (forwarded for context; not used by this class).
    """

    def __init__(self, name: str = 'tpch_refresh', SF: str = '1') -> None:
        """
        :param name: Name that matches the ``"benchmarker"`` key in the experiment dict.
        :param SF: Scaling factor.
        """
        super().__init__(name=name, SF=SF)

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        """
        Return a base evaluator for reading connection metadata.

        The base evaluator is sufficient because the refresh stream stores
        only timing data (no separate pickle/cube files).

        :param code: Experiment identifier.
        :param path: Root result path.
        :param benchmark_run: 1-based benchmark position.
        :return: :class:`evaluators.base` instance.
        """
        return evaluators.base(
            code=code,
            path=path,
            include_loading=False,
            include_benchmarking=True,
            benchmark_run=benchmark_run,
        )

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        No-op: the refresh stream has no workload metadata of its own.

        :param experiment: The owning experiment object.
        :param parameter: Dict of CLI arguments as produced by argparse.
        """

    def test_results(self, experiment) -> None:
        """
        No-op: no pass/fail assertions are defined for the refresh stream.

        :param experiment: The owning experiment object.
        """

    def show_summary(self, experiment) -> None:
        """
        Print the refresh-stream section when called from :meth:`mixed.show_summary`.

        Delegates to :meth:`show_summary_section` so the same output is
        produced whether the call comes from ``mixed`` or from
        ``dbmsbenchmarker.show_summary``.

        :param experiment: The owning experiment object.
        """
        self.show_summary_section(experiment)

    def show_summary_section(self, experiment) -> None:
        """
        Print a timing table for this refresh stream's client rounds.

        Reads :meth:`~bexhoma.evaluators.base.base.get_connections_of_experiment`
        from the base evaluator, filters to rows whose ``benchmark_run`` equals
        :attr:`benchmark_index`, and prints ``phase``, ``job``,
        ``experiment_run``, ``client``, ``benchmark_run``, ``pod_count``
        (from the ``pods`` column), ``benchmark_begin``, ``benchmark_end``,
        and ``benchmark_duration``.

        Timing is available only when the k8s job template names the main
        container ``dbmsbenchmarker``, so that
        :meth:`~bexhoma.experiments.base.base.end_benchmarking` writes the
        ``benchmarking_timespans`` field to the connection's ``.config`` file.

        Silently returns when no timing data is available.

        :param experiment: The owning experiment object.
        """
        df_conn = self.evaluator.get_connections_of_experiment()
        if 'benchmark_run' not in df_conn.columns or 'benchmark_duration' not in df_conn.columns:
            return
        display_cols = [
            col for col in (
                'connection', 'phase', 'job',
                'experiment_run', 'client', 'benchmark_run', 'pods',
                'benchmark_begin', 'benchmark_end', 'benchmark_duration',
            )
            if col in df_conn.columns
        ]
        df_section = df_conn[
            (df_conn['benchmark_run'].astype(int) == self.benchmark_index)
            & df_conn['benchmark_duration'].notna()
        ][display_cols]
        if df_section.empty:
            return
        if 'connection' in df_section.columns:
            df_section = df_section.set_index('connection')
        df_section = df_section.rename(columns={'pods': 'pod_count'})
        print(f"\n### {self.name}\n")
        print(df_section.to_markdown(index=True))
