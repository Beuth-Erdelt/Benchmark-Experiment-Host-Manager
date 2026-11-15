"""
Public API of the bexhoma.evaluators package.

Exports the generic evaluator classes :class:`EvaluatorBase` and
:class:`LogEvaluator`, plus the :func:`natural_sort` utility from :mod:`base`.
The evaluator of a benchmark is in that benchmark's folder,
``bexhoma/benchmarks/<name>/evaluator.py``.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from .base import EvaluatorBase, natural_sort
from .logger import LogEvaluator

__all__ = [
    "EvaluatorBase", "LogEvaluator", "natural_sort",
]