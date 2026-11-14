"""
TPC-H, run through DBMSBenchmarker, with an optional refresh stream.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from bexhoma.benchmarks.dbmsbenchmarker.collector import DbmsBenchmarkerCollector
from .benchmark import TPCH
from .catalog import build_tpch_argv
from .experiment import TpchExperiment

__all__ = ['TPCH', 'TpchExperiment', 'build_tpch_argv', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='tpch', types=('tpch',), experiment=TpchExperiment, collector=DbmsBenchmarkerCollector,
    entry_script='tpch.py', argv_builder=build_tpch_argv)
