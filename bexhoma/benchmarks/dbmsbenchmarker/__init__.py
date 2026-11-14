"""
The DBMSBenchmarker tool family: what the benchmarks that run their queries through
DBMSBenchmarker share (TPC-H, TPC-DS, SSB). Not a benchmark of its own: it has no
entry script and no experiment class that a summary is rebuilt from.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from .benchmark import DBMSBenchmarkerBenchmark
from .collector import DbmsBenchmarkerCollector
from .evaluator import DbmsBenchmarkerEvaluator
from .experiment import DbmsBenchmarkerExperiment

__all__ = ['DBMSBenchmarkerBenchmark', 'DbmsBenchmarkerExperiment', 'DbmsBenchmarkerEvaluator', 'DbmsBenchmarkerCollector', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='dbmsbenchmarker', types=('dbmsbenchmarker',), collector=DbmsBenchmarkerCollector)
