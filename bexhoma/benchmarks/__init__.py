"""
Benchmark class hierarchy for bexhoma experiments.

Each Benchmark subclass holds result-interpretation logic for one benchmark
tool: which evaluator to instantiate, how to display the summary, and how
to validate results.  Job submission is governed by the experiment dict on
each configuration object, not by these classes.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import Benchmark, DBMSBenchmarkerBenchmark
from .ycsb import YCSB
from .tpcc import TPCC
from .tpch import TPCH
from .tpcds import TPCDS
from .benchbase import Benchbase
from .refresh import RefreshStreamBenchmark

__all__ = [
    "Benchmark",
    "DBMSBenchmarkerBenchmark",
    "YCSB",
    "TPCC",
    "TPCH",
    "TPCDS",
    "Benchbase",
    "RefreshStreamBenchmark",
]
