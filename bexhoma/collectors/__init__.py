"""
Public API of the bexhoma.collectors package.

Exports the collector classes (:class:`CollectorBase`, :class:`BenchbaseCollector`,
:class:`DbmsBenchmarkerCollector`, :class:`MixedCollector`, :class:`TpccCollector`,
:class:`YcsbCollector`) and the utility functions :func:`get_non_constant` and
:func:`map_index_to_queryname`.

Backward-compatible aliases (``base``, ``benchbase``, ``dbmsbenchmarker``,
``mixed``, ``tpcc``, ``ycsb``) are provided so that existing code that imports
the old lowercase class names continues to work without modification.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import CollectorBase, get_non_constant
from .dbmsbenchmarker import DbmsBenchmarkerCollector, map_index_to_queryname
from .benchbase import BenchbaseCollector
from .tpcc import TpccCollector
from .ycsb import YcsbCollector
from .mixed import MixedCollector

# backward-compat aliases
base = CollectorBase
dbmsbenchmarker = DbmsBenchmarkerCollector
benchbase = BenchbaseCollector
tpcc = TpccCollector
ycsb = YcsbCollector
mixed = MixedCollector

__all__ = [
    "CollectorBase", "DbmsBenchmarkerCollector", "MixedCollector",
    "TpccCollector", "BenchbaseCollector", "YcsbCollector",
    "get_non_constant", "map_index_to_queryname",
    "base", "dbmsbenchmarker", "mixed", "tpcc", "benchbase", "ycsb",
]