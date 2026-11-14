"""
TPC-C, loaded and run with HammerDB.

Everything bexhoma knows about it is in this folder; generic code reaches it
through :data:`DESCRIPTOR` (see :mod:`bexhoma.benchmarks.registry`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from .benchmark import HammerDB
from .collector import HammerdbCollector
from .evaluator import HammerdbEvaluator
from .experiment import HammerdbExperiment

__all__ = ['HammerDB', 'HammerdbExperiment', 'HammerdbEvaluator', 'HammerdbCollector', 'DESCRIPTOR']

#: What generic code needs to know about this benchmark.
DESCRIPTOR = BenchmarkDescriptor(
    name='hammerdb', types=('hammerdb',), experiment=HammerdbExperiment, collector=HammerdbCollector,
    entry_script='hammerdb.py')
