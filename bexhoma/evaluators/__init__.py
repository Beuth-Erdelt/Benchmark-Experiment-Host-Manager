"""
Public API of the bexhoma.evaluators package.

Exports :class:`EvaluatorBase`, :class:`LogEvaluator`,
:class:`DbmsBenchmarkerEvaluator`, :class:`BenchbaseEvaluator`,
:class:`TpccEvaluator`, and :class:`YcsbEvaluator` evaluator classes,
plus the :func:`natural_sort` utility from :mod:`base`.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import EvaluatorBase, natural_sort
from .logger import LogEvaluator
from .dbmsbenchmarker import DbmsBenchmarkerEvaluator
from .benchbase import BenchbaseEvaluator
from .tpcc import TpccEvaluator
from .ycsb import YcsbEvaluator

# backward-compat aliases
base = EvaluatorBase
logger = LogEvaluator
dbmsbenchmarker = DbmsBenchmarkerEvaluator
benchbase = BenchbaseEvaluator
tpcc = TpccEvaluator
ycsb = YcsbEvaluator

__all__ = [
    "EvaluatorBase", "LogEvaluator", "DbmsBenchmarkerEvaluator",
    "BenchbaseEvaluator", "TpccEvaluator", "YcsbEvaluator", "natural_sort",
    # backward-compat aliases
    "base", "logger", "dbmsbenchmarker", "tpcc", "benchbase", "ycsb",
]