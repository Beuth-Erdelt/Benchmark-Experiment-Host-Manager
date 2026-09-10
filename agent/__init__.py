"""Agent side of the AI-conducted benchmarking prototype.

Design documents live beside this package; the model-facing harness is in
:mod:`agent.harness`. :mod:`agent.lifecycle` (local) and
:mod:`agent.lifecycle_controller` (in-cluster) are operator wrappers that chain
the harness phases; nothing in :mod:`agent.harness` imports them.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""

__all__: list[str] = []
