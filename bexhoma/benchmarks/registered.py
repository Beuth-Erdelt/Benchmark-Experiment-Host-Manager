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
from bexhoma.collectors.dbmsbenchmarker import DbmsBenchmarkerCollector
from bexhoma.collectors.hardware import HardwareCollector
from bexhoma.collectors.hammerdb import HammerdbCollector
from bexhoma.collectors.ycsb import YcsbCollector
from bexhoma.experiments.benchbase import BenchbaseExperiment
from bexhoma.experiments.hardware import HardwareExperiment
from bexhoma.experiments.ssb import SsbExperiment
from bexhoma.experiments.hammerdb import HammerdbExperiment
from bexhoma.experiments.tpcds import TpcdsExperiment
from bexhoma.experiments.tpch import TpchExperiment
from bexhoma.experiments.tpch_catalog import build_tpch_argv
from bexhoma.experiments.ycsb import YcsbExperiment
from bexhoma.experiments.ycsb_catalog import build_ycsb_argv

# The first benchmark with an ``argv_builder`` is the one whose entry script
# bexhoma.spec.entry_script_for_workload() falls back to.
register(BenchmarkDescriptor(
    name='tpch', types=('tpch',), experiment=TpchExperiment, collector=DbmsBenchmarkerCollector,
    entry_script='tpch.py', argv_builder=build_tpch_argv))
register(BenchmarkDescriptor(
    name='tpcds', types=('tpcds',), experiment=TpcdsExperiment, collector=DbmsBenchmarkerCollector,
    entry_script='tpcds.py'))
register(BenchmarkDescriptor(
    name='ssb', types=('ssb',), experiment=SsbExperiment, collector=DbmsBenchmarkerCollector,
    entry_script='ssb.py'))
register(BenchmarkDescriptor(
    name='ycsb', types=('ycsb',), experiment=YcsbExperiment, collector=YcsbCollector,
    entry_script='ycsb.py', argv_builder=build_ycsb_argv))
register(BenchmarkDescriptor(
    name='benchbase', types=('benchbase',), experiment=BenchbaseExperiment, collector=BenchbaseCollector,
    entry_script='benchbase.py'))
register(BenchmarkDescriptor(
    name='hammerdb', types=('hammerdb',), experiment=HammerdbExperiment, collector=HammerdbCollector,
    entry_script='hammerdb.py'))
register(BenchmarkDescriptor(
    name='hardware', types=('hardware',), experiment=HardwareExperiment, collector=HardwareCollector,
    entry_script='hardware.py'))
# The tool family behind TPC-H, TPC-DS and SSB: a benchmark run of this type has a
# collector, but no experiment class of its own to rebuild a summary from
register(BenchmarkDescriptor(
    name='dbmsbenchmarker', types=('dbmsbenchmarker',), collector=DbmsBenchmarkerCollector))
