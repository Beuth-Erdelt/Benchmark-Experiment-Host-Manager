"""Turn the dry-run validator's prose output into a structured verdict.

Wraps :mod:`bexhoma.spec` -- the same resolution path ``validate_experiment.py``
uses -- in the JSON envelope the agent reads back after every ``validate`` call.
Touches no cluster and spawns no subprocess, so the design loop can run offline.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
from typing import Any, Optional

import yaml

from bexhoma import spec

__all__ = [
    "PARSE_STAGE",
    "CATALOG_STAGE",
    "ENVIRONMENT_STAGE",
    "count_runs",
    "validate_spec",
]

#: The specification or a contract file could not be read or parsed as YAML.
PARSE_STAGE = "parse"
#: The specification does not resolve against ``contract_catalog.yml``.
CATALOG_STAGE = "catalog"
#: The specification resolves, but does not fit the cluster in ``environment.yml``.
ENVIRONMENT_STAGE = "environment"
#: The specification is legal and would run, but could not support its own claim.
METHODOLOGY_STAGE = "methodology"

#: Every ``type:`` the catalog is allowed to declare. The first group is
#: enforced by :func:`_check_value`; the second is recognised but left to
#: Patrick's resolver. A type outside this set is a typo in the contract, which
#: would otherwise switch that field's check off silently.
_KNOWN_TYPES = frozenset({
    "int", "str", "bool", "object", "list", "enum",
    "list[int]", "list[str]", "object or list[object]",
    "float", "memory", "quantity", "duration",
})

#: Rounds an experiment runs when it declares no concurrency sweep -- one round
#: of one client, which is what tpch.py falls back to.
_DEFAULT_ROUNDS = [1]
_DEFAULT_REPETITIONS = 1


def _error(message: str, stage: str = CATALOG_STAGE) -> dict[str, str]:
    """Build one verdict error entry."""
    return {"stage": stage, "message": message}


def _check_int(value: Any, definition: dict[str, Any], path: str) -> Optional[dict[str, str]]:
    """Check one value is an integer within the ``min``/``max`` its definition declares."""
    # bool is a subclass of int in Python, so it has to be excluded explicitly.
    if isinstance(value, bool) or not isinstance(value, int):
        return _error(f"{path} must be an integer, not {type(value).__name__}")
    minimum, maximum = definition.get("min"), definition.get("max")
    if minimum is not None and value < minimum:
        return _error(f"{path}={value} is below the declared minimum of {minimum}")
    if maximum is not None and value > maximum:
        return _error(f"{path}={value} is above the declared maximum of {maximum}")
    return None


def _check_value(value: Any, definition: Any, path: str) -> Optional[dict[str, str]]:
    """Check one field's value against the type and bounds the catalog declares.

    Enforces the primitive types used by ``experiment_schema``. Domain-specific
    values such as Kubernetes quantities remain Patrick's resolver's job.

    :param value: The value the experiment supplied.
    :param definition: The catalog's definition of this field, which is a plain
        string for fields the catalog documents without a full definition.
    :param path: Dotted path of the field, for the error message.
    :return: An error entry, or ``None`` when the value fits.
    :rtype: Optional[dict[str, str]]
    """
    if not isinstance(definition, dict):
        return None
    declared = definition.get("type")
    if declared is not None and declared not in _KNOWN_TYPES:
        return _error(f"{path}: the catalog declares unrecognised type {declared!r}")
    if declared == "int":
        return _check_int(value, definition, path)
    if declared == "str" and not isinstance(value, str):
        return _error(f"{path} must be a string, not {type(value).__name__}")
    if declared == "bool" and not isinstance(value, bool):
        return _error(f"{path} must be a boolean, not {type(value).__name__}")
    if declared == "object" and not isinstance(value, dict):
        return _error(f"{path} must be an object, not {type(value).__name__}")
    if declared == "list" and not isinstance(value, list):
        return _error(f"{path} must be a list, not {type(value).__name__}")
    if declared == "enum" and value not in definition.get("values", []):
        return _error(f"{path}={value!r} is not one of {definition.get('values', [])}")
    if declared in ("list[int]", "list[str]"):
        if not isinstance(value, list):
            item_name = "integers" if declared == "list[int]" else "strings"
            return _error(f"{path} must be a list of {item_name}, not {type(value).__name__}")
        if not value:
            return _error(f"{path} must not be empty")
        for index, item in enumerate(value):
            item_path = f"{path}[{index}]"
            if declared == "list[int]":
                if error := _check_int(item, definition, item_path):
                    return error
            elif not isinstance(item, str):
                return _error(f"{item_path} must be a string, not {type(item).__name__}")
    if declared == "object or list[object]":
        cells = value if isinstance(value, list) else [value]
        if not cells or any(not isinstance(cell, dict) for cell in cells):
            return _error(f"{path} must be an object or a non-empty list of objects")
    return None


def _check_fields(value: Any, allowed: Any, path: str) -> Optional[dict[str, str]]:
    """Reject unknown keys, then check each known key's value against its definition."""
    if not isinstance(value, dict):
        return _error(f"{path} must be an object")
    unknown = set(value) - set(allowed)
    if unknown:
        return _error(f"{path} contains unknown field '{sorted(unknown)[0]}'")
    for name, definition in allowed.items():
        if isinstance(definition, dict) and definition.get("required") and not value.get(name):
            return _error(f"{path} is missing required field '{name}'")
    for name, item in value.items():
        error = _check_value(item, allowed[name], f"{path}.{name}")
        if error:
            return error
    return None


def _check_requests_fit_limits(resources: dict[str, Any]) -> Optional[dict[str, str]]:
    """Reject a resource cell that requests more than its own limit allows."""
    for resource, parse in (("cpu", spec.parse_cpu_quantity), ("memory", spec.parse_memory_quantity)):
        cells = resources.get(resource, {})
        for index, cell in enumerate(cells if isinstance(cells, list) else [cells]):
            request, limit = cell.get("request"), cell.get("limit")
            if request is None or limit is None:
                continue
            try:
                if parse(request) > parse(limit):
                    return _error(f"resources.{resource}[{index}].request={request!r} "
                                  f"exceeds its own limit={limit!r}")
            except (spec.SpecError, TypeError, ValueError) as error:
                return _error(str(error))
    return None


def _check_contract_shape(
    catalog: dict[str, Any], experiment: Any,
) -> Optional[dict[str, str]]:
    """Reject fields outside the schema embedded in the agent's catalog."""
    if not isinstance(catalog, dict):
        return {"stage": CATALOG_STAGE, "message": "catalog must be an object"}
    schema = catalog.get("experiment_schema", {}).get("fields", {})
    error = _check_fields(experiment, schema, "experiment.yml")
    if error:
        return error

    workload = experiment.get("workload", {})
    error = _check_fields(workload, schema["workload"]["fields"], "workload")
    if error:
        return error
    workload_contract = catalog.get("workloads", {}).get(workload.get("name"), {})
    error = _check_fields(workload.get("params", {}), workload_contract.get("params", {}), "workload.params")
    if error:
        return error

    loading = experiment.get("loading", {})
    # The workload's own loading block carries the bounds (pods/threads min: 1);
    # the schema block carries the shape. Merge so both are enforced from where
    # each is declared, rather than duplicating the bounds into the schema.
    loading_fields = {**schema["loading"]["fields"], **workload_contract.get("loading", {})}
    error = _check_fields(loading, loading_fields, "loading")
    if error:
        return error
    error = _check_fields(loading.get("post_load", {}),
                          workload_contract.get("loading", {}).get("post_load", {}),
                          "loading.post_load")
    if error:
        return error

    item_fields = schema["systems"]["item_fields"]
    systems = experiment.get("systems", [])
    if not isinstance(systems, list):
        return {"stage": CATALOG_STAGE, "message": "systems must be a list"}
    for index, system in enumerate(systems):
        error = _check_fields(system, item_fields, f"systems[{index}]")
        if error:
            return error
    system_names = [system["name"] for system in systems]
    repeated_names = sorted({name for name in system_names if system_names.count(name) > 1})
    if repeated_names:
        return _error(
            "systems repeats system name(s) "
            f"{repeated_names}, but the Bexhoma TPC-H runtime collapses same-named "
            "entries into one configuration; run one treatment in this experiment "
            "and use a follow-up experiment for the other treatment",
            METHODOLOGY_STAGE,
        )

    for section in ("observe", "placement"):
        error = _check_fields(experiment.get(section, {}), schema[section]["fields"], section)
        if error:
            return error

    resources = experiment.get("resources", {})
    error = _check_fields(resources, schema["resources"]["fields"], "resources")
    if error:
        return error
    for resource in ("cpu", "memory"):
        cells = resources.get(resource, {})
        cells = cells if isinstance(cells, list) else [cells]
        for index, cell in enumerate(cells):
            error = _check_fields(cell, schema["resources"]["fields"][resource]["item_fields"],
                                  f"resources.{resource}[{index}]")
            if error:
                return error
    error = _check_fields(resources.get("storage", {}),
                          schema["resources"]["fields"]["storage"]["fields"],
                          "resources.storage")
    if error:
        return error

    error = _check_requests_fit_limits(resources)
    if error:
        return error

    declared = experiment.get("discriminates", [])
    if not isinstance(declared, list):
        return {"stage": CATALOG_STAGE, "message": "discriminates must be a list"}
    allowed = set(schema["discriminates"].get("values", []))
    if allowed and (unknown := set(declared) - allowed):
        return {"stage": CATALOG_STAGE,
                "message": f"discriminates contains unknown factor '{sorted(unknown)[0]}'"}
    varied = set()
    if len(systems) > 1:
        varied.add("system")
    if len(workload.get("rounds") or _DEFAULT_ROUNDS) > 1:
        varied.add("concurrency")
    for resource in ("cpu", "memory"):
        if isinstance(resources.get(resource), list) and len(resources[resource]) > 1:
            varied.add(resource)
    if mismatch := varied.symmetric_difference(declared):
        return {"stage": METHODOLOGY_STAGE,
                "message": "discriminates must name exactly the varied factors; "
                           f"declared {sorted(declared)}, varied {sorted(varied)}"}
    return None


def count_runs(experiment: dict[str, Any]) -> int:
    """Count the benchmark runs an experiment expands to.

    Every system is crossed against every resource sweep cell to give one
    resolved configuration, and each configuration runs every entry of
    ``workload.rounds`` once per repetition.

    :param experiment: A loaded experiment.yml.
    :return: Total number of benchmark runs.
    :rtype: int
    """
    resources = experiment.get("resources") or {}
    cpu = resources.get("cpu") or {}
    memory = resources.get("memory") or {}
    num_cells = max(
        len(cpu) if isinstance(cpu, list) else 1,
        len(memory) if isinstance(memory, list) else 1,
    )
    workload = experiment.get("workload") or {}
    rounds = workload.get("rounds") or _DEFAULT_ROUNDS
    repetitions = workload.get("repetitions") or _DEFAULT_REPETITIONS
    systems = experiment.get("systems") or []
    return len(systems) * num_cells * len(rounds) * repetitions


def _check_repetitions(
    catalog: dict[str, Any],
    experiment: dict[str, Any],
) -> Optional[dict[str, str]]:
    """Refuse a comparison that repeats too few times to support a conclusion.

    The threshold is read from the workload's own ``minimum_for_conclusions``
    field rather than hardcoded, so the catalog stays the single source of truth
    and a workload that needs a different number can say so. Applied only when
    the experiment actually compares something -- systems, resource cells, or
    concurrency levels -- since a single-cell smoke test claims nothing that
    variance could undermine.

    This check lives here rather than in :mod:`bexhoma.spec` on purpose: it is a
    methodological rule for agent-designed experiments, and adding it to the
    shared validator would change what Patrick's command-line tool accepts.

    :param catalog: Loaded ``contract_catalog.yml``.
    :param experiment: Loaded experiment.yml.
    :return: An error object, or ``None`` when the experiment is acceptable.
    :rtype: Optional[dict[str, str]]
    """
    workload = experiment.get("workload") or {}
    declared = (
        catalog.get("workloads", {})
        .get(workload.get("name"), {})
        .get("repetitions", {})
    )
    minimum = declared.get("minimum_for_conclusions") if isinstance(declared, dict) else None
    if not minimum:
        return None

    resources = experiment.get("resources") or {}
    cells = max(
        len(resources.get("cpu")) if isinstance(resources.get("cpu"), list) else 1,
        len(resources.get("memory")) if isinstance(resources.get("memory"), list) else 1,
    )
    rounds = workload.get("rounds") or _DEFAULT_ROUNDS
    compares = len(experiment.get("systems") or []) > 1 or cells > 1 or len(rounds) > 1
    repetitions = workload.get("repetitions") or _DEFAULT_REPETITIONS
    if not compares or repetitions >= minimum:
        return None

    return {
        "stage": METHODOLOGY_STAGE,
        "message": (
            f"workload.repetitions={repetitions} but this experiment compares "
            f"several configurations, and '{workload.get('name')}' declares "
            f"minimum_for_conclusions={minimum}: with fewer repetitions a "
            "difference between them cannot be told apart from run-to-run "
            f"variance. Raise repetitions to at least {minimum}"
        ),
    }


def _verdict(
    errors: list[dict[str, str]],
    environment_checked: bool,
    experiment: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Assemble the verdict object the agent receives.

    :param errors: Problems found, empty when the specification is valid.
    :param environment_checked: Whether the cluster-fit checks actually ran.
    :param experiment: Loaded experiment.yml, or ``None`` when it did not parse.
    :return: The verdict.
    :rtype: dict[str, Any]
    """
    return {
        "valid": not errors,
        "errors": errors,
        # An unchecked environment means placement and resource ceilings were
        # never verified, so "valid" is weaker than it looks -- say so rather
        # than let the agent read it as a full pass.
        "environment_checked": environment_checked,
        "estimate": {
            "runs": count_runs(experiment) if isinstance(experiment, dict) else None,
            "duration_min": None,
        },
    }


def validate_spec(
    experiment_path: str,
    catalog_path: str,
    environment_path: Optional[str] = None,
) -> dict[str, Any]:
    """Dry-run validate an experiment.yml and report the result as a verdict.

    :param experiment_path: Path to the experiment YAML file to check.
    :param catalog_path: Path to ``contract_catalog.yml``.
    :param environment_path: Path to ``environment.yml``; when ``None`` or
        missing, the placement and resource-ceiling checks are skipped and the
        verdict says so.
    :return: ``{"valid", "errors", "environment_checked", "estimate"}``.
    :rtype: dict[str, Any]
    """
    try:
        experiment = spec.load_experiment(experiment_path)
        catalog = spec.load_catalog(catalog_path)
    except (OSError, yaml.YAMLError) as error:
        return _verdict([{"stage": PARSE_STAGE, "message": str(error)}], False)

    # The shape walk indexes into the catalog's own structure, so a catalog that
    # has been restructured raises rather than returning a verdict. Report that
    # as a broken contract instead of letting it escape as a tool-call crash.
    try:
        shape_error = _check_contract_shape(catalog, experiment)
    except (KeyError, TypeError) as error:
        return _verdict([{"stage": CATALOG_STAGE,
                          "message": f"the catalog is missing the structure validation needs: {error}"}],
                        False)
    if shape_error:
        return _verdict([shape_error], False)

    try:
        spec.build_argv(catalog, experiment)
    except (spec.SpecError, IndexError, KeyError, TypeError, ValueError) as error:
        return _verdict([{"stage": CATALOG_STAGE, "message": str(error)}], False, experiment)

    methodology_error = _check_repetitions(catalog, experiment)
    if methodology_error is not None:
        return _verdict([methodology_error], False, experiment)

    if not environment_path or not os.path.isfile(environment_path):
        return _verdict([], False, experiment)

    try:
        environment = spec.load_environment(environment_path)
        spec.validate_environment(environment, experiment)
    except (OSError, yaml.YAMLError) as error:
        return _verdict([{"stage": PARSE_STAGE, "message": str(error)}], False, experiment)
    except spec.SpecError as error:
        return _verdict([{"stage": ENVIRONMENT_STAGE, "message": str(error)}], True, experiment)

    return _verdict([], True, experiment)
