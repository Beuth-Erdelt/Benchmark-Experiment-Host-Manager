"""
YCSB: the Yahoo Cloud Serving Benchmark, loaded and run with the YCSB tool.

Everything bexhoma knows about this benchmark is in this folder; generic code
reaches it through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).
Its scripts, images and job templates are in ``experiments/ycsb/``,
``images/`` and ``k8s/``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from .benchmark import YCSB
from .catalog import build_ycsb_argv
from .collector import YcsbCollector
from .evaluator import YcsbEvaluator
from .experiment import YcsbExperiment

__all__ = ['YCSB', 'YcsbExperiment', 'build_ycsb_argv', 'YcsbEvaluator', 'YcsbCollector', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='ycsb', types=('ycsb',), experiment=YcsbExperiment, collector=YcsbCollector,
    entry_script='ycsb.py', argv_builder=build_ycsb_argv)
