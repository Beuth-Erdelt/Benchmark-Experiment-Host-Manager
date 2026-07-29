"""
Dry-run validator for an experiment.yaml: checks it against ``contracts/
contract_catalog.yml`` (what can be asked for) and, optionally,
``environment.yml`` (what the cluster actually has), without touching a
live cluster or spawning any subprocess.

Wraps :mod:`bexhoma.spec`'s ``build_argv()`` (catalog resolution — the same
path ``experiment.py``/``bexhoma/spec.py::translate()`` use to build a
``tpch.py`` argument vector) and its ``validate_environment()`` (placement
node existence/taints, CPU/memory ceilings, storage-class existence). See
``docs/Design-Catalog-Contract.md`` for the contract both validate against.

Usage: ``python validate_experiment.py [experiment.yaml]
[-c contracts/contract_catalog.yml] [-e environment.yml]``. Pass ``-e ""``
to skip the environment check.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from bexhoma import spec

__all__ = ["validate"]

_DEFAULT_EXPERIMENT = "experiment.yaml"
_DEFAULT_CATALOG = os.path.join("contracts", "contract_catalog.yml")
_DEFAULT_ENVIRONMENT = os.path.join("dev", "catalog", "environment.yml")


def validate(experiment_path: str, catalog_path: str, environment_path: Optional[str]) -> bool:
    """Validate an experiment.yaml against the catalog contract and, optionally, environment.yml.

    :param experiment_path: Path to the experiment YAML file.
    :param catalog_path: Path to ``contract_catalog.yml``.
    :param environment_path: Path to ``environment.yml``, or ``None`` to skip
        the placement/resource-ceiling check.
    :return: ``True`` if every check passed.
    :rtype: bool
    """
    experiment = spec.load_experiment(experiment_path)
    catalog = spec.load_catalog(catalog_path)

    print(f"Validating {experiment_path} against {catalog_path} ...")
    try:
        argv = spec.build_argv(catalog, experiment)
    except spec.SpecError as error:
        print(f"  FAIL  {error}")
        return False
    print("  OK    resolves against catalog")
    print("  command:", spec.build_command(argv))

    if environment_path is None:
        print("  SKIP  no environment.yml given; placement/resource-ceiling checks not run")
        return True
    if not os.path.isfile(environment_path):
        print(f"  SKIP  {environment_path} not found; placement/resource-ceiling checks not run")
        return True

    print(f"Validating {experiment_path} against {environment_path} ...")
    environment = spec.load_environment(environment_path)
    try:
        spec.validate_environment(environment, experiment)
    except spec.SpecError as error:
        print(f"  FAIL  {error}")
        return False
    print("  OK    fits the cluster's placement/resource ceilings")
    return True


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    :return: Configured parser.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Dry-run validate an experiment.yaml against contract_catalog.yml and "
                     "environment.yml, without touching a live cluster."
    )
    parser.add_argument("file", nargs="?", default=_DEFAULT_EXPERIMENT,
                         help=f"path to the experiment YAML file (default: {_DEFAULT_EXPERIMENT})")
    parser.add_argument("-c", "--catalog", default=_DEFAULT_CATALOG,
                         help=f"path to contract_catalog.yml (default: {_DEFAULT_CATALOG})")
    parser.add_argument("-e", "--environment", default=_DEFAULT_ENVIRONMENT,
                         help="path to environment.yml; pass an empty string to skip the "
                              f"placement/resource-ceiling check (default: {_DEFAULT_ENVIRONMENT})")
    return parser


if __name__ == "__main__":
    cli_args = _build_parser().parse_args()
    passed = validate(cli_args.file, cli_args.catalog, cli_args.environment or None)
    print()
    print("RESULT:", "ALL CHECKS PASSED" if passed else "FAIL")
    sys.exit(0 if passed else 1)
