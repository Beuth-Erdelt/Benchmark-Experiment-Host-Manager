"""
General-purpose mixed-workload experiment class.

Provides :class:`mixed`, which extends :class:`base` to support multiple
registered :class:`~bexhoma.benchmarks.base.Benchmark` objects, a central
``experiment_dict_template`` copied to each new configuration, and delegation
of workload configuration, summary display, and result validation to the
individual benchmark objects.

All named single-benchmark experiment classes (``ycsb``, ``tpcc``, ``tpch``,
``tpcds``, ``benchbase``) are subclasses of :class:`mixed`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import logging
import urllib3

from .base import base

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["mixed"]


class mixed(base):
    """
    General experiment class supporting multiple parallel or sequential benchmarks.

    Holds an ``experiment_dict_template`` that is deep-copied to every new
    configuration on :meth:`add_configuration`, and a list of registered
    :class:`~bexhoma.benchmarks.base.Benchmark` objects that govern result
    interpretation.

    Named single-benchmark experiments (YCSB, TPC-C, TPC-H, TPC-DS, Benchbase)
    subclass :class:`mixed` and pre-populate the template in ``__init__``.
    Direct use of :class:`mixed` is intended for fully custom experiment dicts.

    :param cluster: Cluster object, typically referring to a Kubernetes cluster.
    :param code: Unique experiment identifier; generated from current time if ``None``.
    :param num_experiment_to_apply: How many times to repeat the full experiment.
    :param timeout: Maximum timeout per query in seconds.
    """

    def __init__(self,
                 cluster,
                 code=None,
                 num_experiment_to_apply: int = 1,
                 timeout: int = 7200) -> None:
        """
        :param cluster: Cluster object.
        :param code: Experiment identifier; auto-generated if ``None``.
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        """
        base.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        self.benchmarks: list = []
        self.evaluators: dict = {}
        self.experiment_dict_template: dict = {"loader": [], "benchmarker": []}

    def add_benchmark(self, benchmark) -> None:
        """
        Register a benchmark and create its evaluator.

        Assigns a 1-based ``benchmark_index`` to the benchmark, instantiates
        its evaluator, wires ``evaluator.experiment`` back to this experiment,
        and sets ``self.evaluator`` to the first registered benchmark's evaluator
        for backward-compatibility with single-benchmark call sites.

        :param benchmark: :class:`~bexhoma.benchmarks.base.Benchmark` instance to register.
        """
        benchmark.benchmark_index = len(self.benchmarks) + 1
        self.benchmarks.append(benchmark)
        benchmark.evaluator = benchmark.create_evaluator(
            self.code, self.cluster.resultfolder, benchmark.benchmark_index)
        benchmark.evaluator.experiment = self
        self.evaluators[benchmark.name] = benchmark.evaluator
        if len(self.benchmarks) == 1:
            self.evaluator = benchmark.evaluator

    def add_configuration(self, configuration) -> None:
        """
        Add a configuration and copy the experiment dict template to it.

        If the configuration already has an ``experiment_dict`` attribute with
        empty ``"loader"`` and ``"benchmarker"`` lists, the template is deep-copied
        into it.  Configurations that do not carry ``experiment_dict`` (pre-migration
        configurations) are left unchanged.

        :param configuration: Configuration object to register.
        """
        super().add_configuration(configuration)
        if (
            hasattr(configuration, 'experiment_dict')
            and not configuration.experiment_dict["loader"]
            and not configuration.experiment_dict["benchmarker"]
        ):
            configuration.experiment_dict = copy.deepcopy(self.experiment_dict_template)

    def prepare_testbed(self, parameter: dict) -> None:
        """
        Configure all registered benchmarks and then delegate to :meth:`base.prepare_testbed`.

        Calls :meth:`~bexhoma.benchmarks.base.Benchmark.configure_workload` on every
        registered benchmark in registration order before forwarding to the parent.

        :param parameter: Dict of CLI arguments as produced by argparse.
        """
        for benchmark in self.benchmarks:
            benchmark.configure_workload(self, parameter)
        base.prepare_testbed(self, parameter)

    def show_summary(self) -> None:
        """
        Print a Markdown-formatted summary for every registered benchmark.

        Delegates to :meth:`~bexhoma.benchmarks.base.Benchmark.show_summary` on
        each benchmark in registration order.
        """
        for benchmark in self.benchmarks:
            benchmark.show_summary(self)

    def test_results(self) -> None:
        """
        Validate results for every registered benchmark.

        Delegates to :meth:`~bexhoma.benchmarks.base.Benchmark.test_results` on
        each benchmark in registration order.
        """
        for benchmark in self.benchmarks:
            benchmark.test_results(self)
