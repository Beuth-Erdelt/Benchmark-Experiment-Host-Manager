"""
The benchmarks of bexhoma.

A benchmark is a folder ``bexhoma/benchmarks/<name>/`` with its benchmark,
experiment, evaluator and collector classes and a ``DESCRIPTOR`` in its
``__init__``. Generic code reaches the benchmarks through
:mod:`bexhoma.benchmarks.registry`, which finds the folders by itself; this
package imports none of them.

Exports the generic classes: :class:`Benchmark`, the base class of every
benchmark, and :class:`RefreshStreamBenchmark` for a refresh stream that runs
beside a benchmark.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import Benchmark
from .refresh import RefreshStreamBenchmark

__all__ = [
    "Benchmark",
    "RefreshStreamBenchmark",
]
