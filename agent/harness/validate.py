"""Dry-run validate an experiment specification and print the verdict as JSON.

This small adapter exposes :func:`agent.harness.validation.validate_spec` -- the
same structured check the design agent's ``validate`` tool runs -- to a
command-line caller. It touches no cluster and spawns no subprocess, so it can
run offline as a pre-flight gate before a specification is submitted.

Usage: ``python -m agent.harness.validate EXPERIMENT --environment PATH
[--catalog PATH] [--indent N]``. Pass ``--environment ""`` to skip the
placement and resource-ceiling checks; the verdict's ``environment_checked``
field records that they did not run.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from agent.harness import validation

__all__ = ["main"]

#: Default catalog location, matching the repository's ``validate_experiment.py``.
_DEFAULT_CATALOG = os.path.join("contracts", "contract_catalog.yml")


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    :return: Configured parser.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="python -m agent.harness.validate",
        description=(
            "Dry-run validate an experiment specification against "
            "contract_catalog.yml and environment.yml, printing a structured "
            "JSON verdict. Touches no cluster."
        ),
    )
    parser.add_argument("experiment", help="path to the experiment YAML file")
    parser.add_argument(
        "--catalog", default=_DEFAULT_CATALOG,
        help=f"path to contract_catalog.yml (default: {_DEFAULT_CATALOG})",
    )
    parser.add_argument(
        "--environment", required=True,
        help=(
            "path to environment.yml; pass an empty string to skip the "
            "placement and resource-ceiling checks"
        ),
    )
    parser.add_argument(
        "--indent", type=int, default=None,
        help="pretty-print the JSON verdict with this indent (default: compact)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate one specification and write its verdict to standard output.

    :param argv: Command-line arguments, or ``None`` to read ``sys.argv``.
    :return: ``0`` when the verdict is valid, ``1`` when it is not.
    :rtype: int
    """
    args = _build_parser().parse_args(argv)
    verdict = validation.validate_spec(
        args.experiment, args.catalog, args.environment or None,
    )
    json.dump(verdict, sys.stdout, indent=args.indent)
    sys.stdout.write("\n")
    return 0 if verdict.get("valid") else 1


if __name__ == "__main__":
    sys.exit(main())
