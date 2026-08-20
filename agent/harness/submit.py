"""Launch one validated catalog experiment with an agent-assigned result code.

This small adapter deliberately lives in the agent package. It uses Bexhoma's
existing catalog resolver and TPC-H parser without requiring a change to
``experiment.py`` merely so the agent can know which result folder to await.

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
import tpch


def run(path: str, catalog_path: str, experiment_code: str) -> None:
    """Resolve and execute a catalog experiment through Bexhoma's normal path."""
    specification = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    catalog = catalog_spec.load_catalog(catalog_path)
    argv = catalog_spec.build_argv(catalog, specification)
    argv.extend(["-e", experiment_code, "-rp"])
    tpch.run(tpch.build_parser().parse_args(argv))


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
