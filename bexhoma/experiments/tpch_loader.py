"""
Load and validate a self-specified ``experiment.yaml``.

This is the loader half of the YAML-driven experiment entry script (see
``docs/Design-Yaml-Experiment-Entry-Script.md``). It is deliberately
separate from :mod:`bexhoma.spec`, which translates a *catalog-driven*
``experiment.yml`` into a ``tpch.py`` CLI argument vector: this module's
``experiment.yaml`` is fully self-specified and is fed straight into
:mod:`bexhoma.experiments.tpch_builder`, never through argv.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import yaml

from bexhoma.experiments.tpch import DBMS_DEFAULTS

__all__ = ["ExperimentYamlError", "load_experiment_yaml", "validate_experiment_yaml"]

#: Top-level keys every ``experiment.yaml`` must carry, independent of workload.
_REQUIRED_TOP_LEVEL_FIELDS = ("workload", "mode", "systems")

#: Workloads the YAML-driven builder can translate today (see plan's scope decisions).
_SUPPORTED_WORKLOADS = ("tpch",)


class ExperimentYamlError(Exception):
    """Raised when an ``experiment.yaml`` is malformed or fails validation."""


def load_experiment_yaml(path: str) -> dict:
    """
    Load an ``experiment.yaml`` file.

    :param path: Path to the experiment YAML file.
    :return: Parsed experiment spec.
    :rtype: dict
    """
    with open(path, "r", encoding="utf-8") as experiment_file:
        return yaml.safe_load(experiment_file)


def validate_experiment_yaml(spec: dict) -> None:
    """
    Validate a parsed ``experiment.yaml`` before it is handed to :mod:`bexhoma.experiments.tpch_builder`.

    Checks, in order: every field in :data:`_REQUIRED_TOP_LEVEL_FIELDS` is present;
    ``workload`` is one of :data:`_SUPPORTED_WORKLOADS` (only ``tpch`` today, per
    the plan's scope decisions); ``systems`` is a non-empty list; and every
    ``systems[].dbms`` names a key in :data:`bexhoma.experiments.tpch.DBMS_DEFAULTS`.

    :param spec: Parsed experiment spec, as returned by :func:`load_experiment_yaml`.
    :raises ExperimentYamlError: On any validation failure.
    """
    for field_name in _REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in spec:
            raise ExperimentYamlError(f"experiment.yaml is missing required field '{field_name}'")

    workload = spec["workload"]
    if workload not in _SUPPORTED_WORKLOADS:
        raise ExperimentYamlError(
            f"unsupported workload '{workload}'; only {_SUPPORTED_WORKLOADS} are translatable today"
        )

    systems = spec["systems"]
    if not isinstance(systems, list) or not systems:
        raise ExperimentYamlError("'systems' must be a non-empty list")

    for system in systems:
        dbms = system.get("dbms")
        if dbms is None:
            raise ExperimentYamlError(f"systems entry is missing required field 'dbms': {system!r}")
        if dbms not in DBMS_DEFAULTS:
            raise ExperimentYamlError(
                f"unknown dbms '{dbms}'; known values are {sorted(DBMS_DEFAULTS)}"
            )
