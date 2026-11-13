"""
The workloads of Benchbase (TPC-C, YCSB, Twitter, ...), loaded and run with Benchbase.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from .benchmark import Benchbase
from .collector import BenchbaseCollector
from .evaluator import BenchbaseEvaluator
from .experiment import BenchbaseExperiment

__all__ = ['Benchbase', 'BenchbaseExperiment', 'BenchbaseEvaluator', 'BenchbaseCollector', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='benchbase', types=('benchbase',), experiment=BenchbaseExperiment, collector=BenchbaseCollector,
    entry_script='benchbase.py')
