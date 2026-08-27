"""Launch one validated catalog experiment with an agent-assigned result code.

This small adapter deliberately lives in the agent package. It uses Bexhoma's
existing catalog resolver and per-workload entry script without requiring a
change to ``experiment.py`` merely so the agent can know which result folder to
await.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from bexhoma import spec as catalog_spec
from bexhoma.experiments import tpch_catalog
import experiment as experiment_cli


def run(path: str, catalog_path: str, experiment_code: str) -> None:
    """Resolve and execute a catalog experiment through Bexhoma's normal path."""
    specification = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    catalog = catalog_spec.load_catalog(catalog_path)
    argv = catalog_spec.build_argv(catalog, specification)
    # Serial execution of the systems under test is the catalog contract's own
    # default (catalog_concepts.sut_isolation): build_argv already emits the
    # -ms/-mse caps, so this adapter must not restate them.
    argv.extend(["-e", experiment_code, "-rp"])
    workload_name = specification["workload"]["name"]
    entry_module = experiment_cli.entry_module_for_workload(workload_name)
    parsed_args = entry_module.build_parser().parse_args(argv)
    if workload_name == "tpch":
        # Per-system post_load selection has no CLI representation -- -xii/-xic/
        # -xis are global switches -- so it is attached in-process, exactly as
        # experiment.py does for the same argv. Without it an experiment that
        # asks for indexes on one system but not another silently gets the
        # shared default on both.
        parsed_args.physical_design_overrides = (
            tpch_catalog.resolve_physical_design_overrides(catalog, specification)
        )
    elif workload_name == "ycsb":
        # ycsb.py ignores the SUT's resources: block unless a catalog-driven
        # run opts in, exactly as experiment.py does for the same argv.
        parsed_args.apply_sut_resources = "resources" in specification
    entry_module.run(parsed_args)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("specification")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--experiment-code", required=True)
    args = parser.parse_args()
    run(args.specification, args.catalog, args.experiment_code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
