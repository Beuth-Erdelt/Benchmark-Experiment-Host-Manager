"""
SSB: the Star Schema Benchmark, run through DBMSBenchmarker.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from bexhoma.benchmarks.dbmsbenchmarker.collector import DbmsBenchmarkerCollector
from .benchmark import SSB
from .experiment import SsbExperiment

__all__ = ['SSB', 'SsbExperiment', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='ssb', types=('ssb',), experiment=SsbExperiment, collector=DbmsBenchmarkerCollector,
    entry_script='ssb.py')
