"""
Experiment class for Hardware (fio/sysbench) benchmarks.

Provides :class:`HardwareExperiment`, which extends :class:`MixedExperiment` to
orchestrate raw hardware I/O (fio) and CPU/memory (sysbench) benchmarks against
a dedicated SUT container inside a Kubernetes cluster. Unlike every other
experiment type, Hardware never loads data — there is no schema, no DDL, and
no loader job template; ``experiment_dict_template["loader"]`` stays empty and
``loading_deactivated`` is set ``True`` unconditionally so
``loading_is_active()`` reports no loading phase regardless of ``mode``.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import logging
import urllib3

from bexhoma import benchmarks
from .mixed import MixedExperiment

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["HardwareExperiment"]


class HardwareExperiment(MixedExperiment):
    """
    Hardware experiment: orchestrates fio/sysbench benchmarks against a
    dedicated SUT container inside a Kubernetes cluster.

    Registers a :class:`~bexhoma.benchmarks.hardware.Hardware` benchmark object
    and pre-populates the experiment dict template with the Hardware-specific
    job template. Extends :class:`MixedExperiment`.
    """

    def __init__(self,
                 cluster,
                 code=None,
                 num_experiment_to_apply=1,
                 timeout=7200):
        """
        :param cluster: Cluster object.
        :param code: Experiment identifier; auto-generated if ``None``.
        :param num_experiment_to_apply: Repetition count.
        :param timeout: Per-query timeout in seconds.
        """
        MixedExperiment.__init__(self, cluster, code, num_experiment_to_apply, timeout)
        # loading_is_active() returns `not self.loading_deactivated` (a flag
        # distinct from `loading_active`, which is about push- vs pull-style
        # distributed loading and irrelevant here). Hardware has no loading
        # phase in any mode, so this must be True unconditionally — otherwise
        # show_summary() tries to print a "### Loading" section that
        # HardwareEvaluator has no get_summary_loading_per_run() for.
        self.loading_deactivated = True
        # SutConfiguration.__init__() unconditionally indexes
        # cluster.volumes[self.volume]['initscripts'][self.script], even though
        # Hardware never loads data (loading_active stays False) — 'Schema' is
        # never actually executed, it only needs to resolve to a valid (empty)
        # entry. See cluster.config['volumes']['hardware'].
        self.set_experiment(volume='hardware')
        self.set_experiment(script='Schema')
        # BenchmarkRunner.run_pod() reads seed connections.config/queries.config
        # from cluster.experiments_configfolder before the real job runs (used
        # to bootstrap dbmsbenchmarker's config object even though Hardware
        # never queries through dbmsbenchmarker) — see experiments/hardware/.
        self.cluster.set_experiments_configfolder('experiments/hardware')
        self.set_queryfile('queries.config')
        self.storage_label = 'hardware'
        self.set_workload(
            name='Hardware Benchmark',
            info='This experiment measures raw hardware I/O and CPU/memory performance.',
            type='hardware',
        )
        self.jobtemplate_benchmarking = "jobtemplate-benchmarking-hardware.yml"
        self.components = {
            "benchmarker": {"dbmsbenchmarker": True},
        }
        self.add_benchmark(benchmarks.Hardware())
        self.experiment_dict_template = {
            "loader": [],
            "benchmarker": [[
                {
                    "name":        "hardware",
                    "benchmarker": "hardware",
                    "template":    "jobtemplate-benchmarking-hardware.yml",
                    "parallelism": 1,
                    "num_pods":    1,
                    "target":      "sut",
                    "parameters":  {},
                },
            ]],
        }
