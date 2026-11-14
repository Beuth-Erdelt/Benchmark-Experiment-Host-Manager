"""
Hardware benchmarks (fio, sysbench, sockperf, netperf) against a container in place of a DBMS,
and the baseline of a cluster's hardware that bexhoma.environment builds from them.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from .benchmark import Hardware
from .collector import HardwareCollector
from .evaluator import HardwareEvaluator
from .experiment import HardwareExperiment

__all__ = ['Hardware', 'HardwareExperiment', 'HardwareEvaluator', 'HardwareCollector', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='hardware', types=('hardware',), experiment=HardwareExperiment, collector=HardwareCollector,
    entry_script='hardware.py')
