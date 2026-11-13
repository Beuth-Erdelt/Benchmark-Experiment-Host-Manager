"""
Public API of the bexhoma.collectors package.

Exports the generic collector classes :class:`CollectorBase` and
:class:`MixedCollector` and the utility function :func:`get_non_constant`.
The collector of a benchmark is in that benchmark's folder,
``bexhoma/benchmarks/<name>/collector.py``.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import CollectorBase, get_non_constant
from .mixed import MixedCollector

__all__ = [
    "CollectorBase", "MixedCollector",
    "get_non_constant",
]