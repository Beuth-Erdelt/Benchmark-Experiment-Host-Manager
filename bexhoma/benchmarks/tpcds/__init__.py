"""
TPC-DS, run through DBMSBenchmarker.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from bexhoma.benchmarks.dbmsbenchmarker.collector import DbmsBenchmarkerCollector
from .benchmark import TPCDS
from .experiment import TpcdsExperiment

__all__ = ['TPCDS', 'TpcdsExperiment', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='tpcds', types=('tpcds',), experiment=TpcdsExperiment, collector=DbmsBenchmarkerCollector,
    entry_script='tpcds.py')
