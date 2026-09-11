"""Harness that drives a language model through the benchmarking loop.

A question goes in, a validated experiment specification goes to the cluster,
and a later invocation reads the results back and says what they mean. A shared
tool-calling loop drives bounded contexts for design, evidence interpretation,
follow-up selection, and optional authoring (see ``agent/README.md`` for how to
run it and ``agent/ARCHITECTURE.md`` for its boundaries and decisions).

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""

__all__: list[str] = []
