"""
Public API of the bexhoma.collectors package.

Exports the collector classes (:class:`CollectorBase`, :class:`BenchbaseCollector`,
:class:`DbmsBenchmarkerCollector`, :class:`HardwareCollector`, :class:`MixedCollector`,
:class:`HammerdbCollector`, :class:`YcsbCollector`) and the utility functions
:func:`get_non_constant` and :func:`map_index_to_queryname`.

Backward-compatible aliases (``base``, ``benchbase``, ``dbmsbenchmarker``, ``hardware``,
``mixed``, ``tpcc``, ``ycsb``) are provided so that existing code that imports
the old lowercase class names continues to work without modification.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import CollectorBase, get_non_constant
from .benchbase import BenchbaseCollector
from .hardware import HardwareCollector
from .hammerdb import HammerdbCollector
from .mixed import MixedCollector

__all__ = [
    "CollectorBase", "HardwareCollector", "MixedCollector",
    "HammerdbCollector", "BenchbaseCollector",
    "get_non_constant",
]