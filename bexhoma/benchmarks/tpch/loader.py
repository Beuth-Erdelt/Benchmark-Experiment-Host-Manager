"""
Load and validate a self-specified ``experiment.yaml``.

This is the loader half of the YAML-driven experiment entry script (see
``docs/Design-Yaml-Experiment-Entry-Script.md``). It is deliberately
separate from :mod:`bexhoma.spec`, which translates a *catalog-driven*
``experiment.yml`` into a ``tpch.py`` CLI argument vector: this module's
``experiment.yaml`` is fully self-specified and is fed straight into
:mod:`bexhoma.benchmarks.tpch.builder`, never through argv.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import yaml

from bexhoma.system_descriptors import experiment_yaml_dockers, load_dockers

__all__ = ["ExperimentYamlError", "load_experiment_yaml", "validate_experiment_yaml", "loading_count", "merged_loading"]

#: Top-level keys every ``experiment.yaml`` must carry, independent of workload.
_REQUIRED_TOP_LEVEL_FIELDS = ("workload", "mode", "systems")

#: Workloads the YAML-driven builder can translate today (see plan's scope decisions).
_SUPPORTED_WORKLOADS = ("tpch",)


class ExperimentYamlError(Exception):
    """Raised when an ``experiment.yaml`` is malformed or fails validation."""


#: Counts of a ``loading:`` block. Each system gets exactly one configuration, so each is one value.
_LOADING_COUNTS = ("pods", "threads", "split")


def merged_loading(spec: dict, system: dict) -> dict:
    """The ``loading:`` block that applies to one system: the top-level one, the system's own on top.

    :param spec: Parsed experiment spec.
    :param system: One entry of ``spec['systems']``.
    :return: Merged loading block.
    :rtype: dict
    """
    return {**(spec.get("loading") or {}), **(system.get("loading") or {})}


def loading_count(loading: dict, key: str) -> int:
    """One count of a ``loading:`` block: a positive number, or a list holding exactly one.

    A list form (``pods: [4]``) is accepted because the block mirrors the comma lists of ``tpch.py``
    (``-nlp``, ``-nlt``, ``-xnls``), but the YAML path builds one configuration per system and
    cannot sweep: a list with several values is refused, use ``tpch.py`` or a catalog-driven file.

    :param loading: A (merged) ``loading:`` block.
    :param key: ``pods``, ``threads`` or ``split``.
    :return: The count; 1 when the key is absent.
    :rtype: int
    :raises ExperimentYamlError: For several values, or a value that is not a positive integer.
    """
    value = loading.get(key, 1)
    if isinstance(value, list):
        if len(value) != 1:
            raise ExperimentYamlError(
                f"loading.{key} must be one value, got {value!r}: experiment.yaml builds one configuration "
                f"per system and cannot sweep (use tpch.py or a catalog-driven file for that)")
        value = value[0]
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ExperimentYamlError(f"loading.{key} must be a positive integer, got {value!r}")
    return value


def load_experiment_yaml(path: str) -> dict:
    """
    Load an ``experiment.yaml`` file.

    :param path: Path to the experiment YAML file.
    :return: Parsed experiment spec.
    :rtype: dict
    """
    with open(path, "r", encoding="utf-8") as experiment_file:
        return yaml.safe_load(experiment_file)


def validate_experiment_yaml(spec: dict, dockers: dict = None) -> None:
    """
    Validate a parsed ``experiment.yaml`` before it is handed to :mod:`bexhoma.benchmarks.tpch.builder`.

    Checks, in order: every field in :data:`_REQUIRED_TOP_LEVEL_FIELDS` is present;
    ``workload`` is one of :data:`_SUPPORTED_WORKLOADS` (only ``tpch`` today, per
    the plan's scope decisions); ``systems`` is a non-empty list; and every
    ``systems[].dbms`` names a DBMS whose ``tpch`` entry in the cluster configuration is
    marked ``experiment_yaml``.

    :param spec: Parsed experiment spec, as returned by :func:`load_experiment_yaml`.
    :param dockers: The ``dockers`` section of the cluster configuration; read from
        ``cluster.config`` when not given.
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

    known = sorted(experiment_yaml_dockers(dockers if dockers is not None else load_dockers(), "tpch"))
    for system in systems:
        dbms = system.get("dbms")
        if dbms is None:
            raise ExperimentYamlError(f"systems entry is missing required field 'dbms': {system!r}")
        if dbms not in known:
            raise ExperimentYamlError(f"unknown dbms '{dbms}'; known values are {known}")
        for block in (spec.get("loading"), system.get("loading")):
            if block is not None and not isinstance(block, dict):
                raise ExperimentYamlError(f"'loading' must be a mapping, got {block!r}")
        loading = merged_loading(spec, system)
        counts = {key: loading_count(loading, key) for key in _LOADING_COUNTS}
        if counts["split"] > counts["pods"]:
            raise ExperimentYamlError(
                f"loading.split ({counts['split']}) must not exceed loading.pods ({counts['pods']}) for '{dbms}'")
