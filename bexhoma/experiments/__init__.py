"""
Public API of the bexhoma.experiments package.

Exports the generic experiment classes :class:`ExperimentBase` and
:class:`MixedExperiment`. The experiment class of a benchmark is in that
benchmark's folder, ``bexhoma/benchmarks/<name>/experiment.py``.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import ExperimentBase
from .mixed import MixedExperiment

__all__ = [
    "ExperimentBase", "MixedExperiment",
]