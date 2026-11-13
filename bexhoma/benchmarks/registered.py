"""
The descriptors of all benchmarks, in one place.

Transitional: while the classes of a benchmark still live in the layer packages
(``experiments/``, ``evaluators/``, ``collectors/``), this module is the only
one that lists the benchmarks for :mod:`bexhoma.benchmarks.registry`. When a
benchmark moves to its own folder ``bexhoma/benchmarks/<name>/``, its entry
moves there as that folder's ``DESCRIPTOR``, and this module shrinks until it
is gone.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma.benchmarks.registry import BenchmarkDescriptor, register
from bexhoma.collectors.benchbase import BenchbaseCollector
from bexhoma.benchmarks.dbmsbenchmarker.collector import DbmsBenchmarkerCollector
from bexhoma.collectors.hardware import HardwareCollector
from bexhoma.collectors.hammerdb import HammerdbCollector
from bexhoma.experiments.benchbase import BenchbaseExperiment
from bexhoma.experiments.hardware import HardwareExperiment
from bexhoma.experiments.hammerdb import HammerdbExperiment

register(BenchmarkDescriptor(
    name='benchbase', types=('benchbase',), experiment=BenchbaseExperiment, collector=BenchbaseCollector,
    entry_script='benchbase.py'))
register(BenchmarkDescriptor(
    name='hammerdb', types=('hammerdb',), experiment=HammerdbExperiment, collector=HammerdbCollector,
    entry_script='hammerdb.py'))
register(BenchmarkDescriptor(
    name='hardware', types=('hardware',), experiment=HardwareExperiment, collector=HardwareCollector,
    entry_script='hardware.py'))
