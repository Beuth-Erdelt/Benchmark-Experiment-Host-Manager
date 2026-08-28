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
import re
from typing import Any, NamedTuple

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

#: Display path of the specification's top level, where nested blocks are named
#: by their own key rather than by a dotted path from the root.
_ROOT_PATH = "experiment.yml"
#: Suffix marking a block that repeats, so ``systems[0]`` and the schema's
#: ``systems[]`` compare equal when locating a misplaced field.
_INDEX_SUFFIX = "[]"
_INDEXED = re.compile(r"\[\d+\]")

#: Every ``type:`` the catalog is allowed to declare. The first group is
#: enforced by :func:`_check_value`; the second is recognised but left to
#: Patrick's resolver. A type outside this set is a typo in the contract, which
#: would otherwise switch that field's check off silently.
_KNOWN_TYPES = frozenset({
    "int", "str", "bool", "object", "list", "enum",
    "list[int]", "list[str]", "list[float]", "object or list[object]",
    "float", "memory", "quantity", "duration",
})

#: Rounds an experiment runs when it declares no concurrency sweep -- one round
#: of one client, which is what tpch.py falls back to.
#: Fewest repetitions from which a spread can be estimated at all, used when the
#: catalog names no minimum of its own for the workload (handbook M5.1).
_SPREAD_FLOOR = 2

#: Words that state adequacy instead of a testable outcome. A hypothesis built
#: only from these cannot be refuted by any measurement (handbook M1.1).
_ADEQUACY_STEMS = (
    "acceptab", "adequat", "reasonab", "satisfactor", "sufficient", "successful",
    "smooth", "properly", "correctly", "perform well", "performs well",
    "scale well", "scales well", "handle", "handles", "cope", "copes",
    "good performance", "fine",
)

#: Ways a hypothesis can name an outcome some measurement could contradict: a
#: direction, a margin, or a number to fall on one side of.
_COMPARATIVE_MARKERS = (
    "faster", "slower", "higher", "lower", "better", "worse", "more", "less",
    "fewer", "greater", "smaller", "shorter", "longer", "cheaper",
    "outperform", "beat", "exceed", "exceeds", "above", "below", "at least",
    "at most", "no more than", "no less than", "within", "than", "double",
    "doubles", "halve", "halves", "unchanged", "flat", "rises", "rise",
    "falls", "fall", "grows", "grow", "drops", "drop", "degrade", "degrades",
    "improve", "improves", "increase", "increases", "decrease", "decreases",
    "differ", "differs", "same", "equal",
)

_DEFAULT_ROUNDS = [1]
_DEFAULT_REPETITIONS = 1
_GIBIBYTE_BYTES = 1024 ** 3


def _error(message: str, stage: str = CATALOG_STAGE) -> dict[str, str]:
    """Build one verdict error entry."""
    return {"stage": stage, "message": message}


def _check_int(value: Any, definition: dict[str, Any], path: str) -> dict[str, str] | None:
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


def _check_value(value: Any, definition: Any, path: str) -> dict[str, str] | None:
    """Check one field's value against the type and bounds the catalog declares.

    Enforces the primitive types used by ``experiment_schema``. Domain-specific
    values such as Kubernetes quantities remain Patrick's resolver's job.

    :param value: The value the experiment supplied.
    :param definition: The catalog's definition of this field, which is a plain
        string for fields the catalog documents without a full definition.
    :param path: Dotted path of the field, for the error message.
    :return: An error entry, or ``None`` when the value fits.
    :rtype: dict[str, str] | None
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
    if declared == "list[float]":
        if not isinstance(value, list):
            return _error(f"{path} must be a list of numbers, not {type(value).__name__}")
        if not value:
            return _error(f"{path} must not be empty")
        for index, item in enumerate(value):
            # bool is a subclass of int, so an accidental true/false must not pass.
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                return _error(
                    f"{path}[{index}] must be a number, not {type(item).__name__}")
    if declared == "object or list[object]":
        cells = value if isinstance(value, list) else [value]
        if not cells or any(not isinstance(cell, dict) for cell in cells):
            return _error(f"{path} must be an object or a non-empty list of objects")
    return None


def _schema_locations(
    catalog: dict[str, Any], experiment: Any,
) -> dict[str, list[str]]:
    """Index every field name the contract defines against the blocks it is legal in.

    Walks the experiment schema and the contract of the workload this
    specification names, so a field rejected in one block can be pointed at the
    block that accepts it.

    :param catalog: Loaded ``contract_catalog.yml``.
    :param experiment: Loaded experiment.yml, read only for its workload name.
    :return: Field name to the sorted display paths defining it.
    :rtype: dict[str, list[str]]
    """
    found: dict[str, set[str]] = {}

    def walk(fields: Any, path: str) -> None:
        if not isinstance(fields, dict):
            return
        for name, definition in fields.items():
            found.setdefault(name, set()).add(path)
            if not isinstance(definition, dict):
                continue
            child = name if path == _ROOT_PATH else f"{path}.{name}"
            walk(definition.get("fields"), child)
            walk(definition.get("item_fields"), f"{child}{_INDEX_SUFFIX}")

    schema = catalog.get("experiment_schema", {}).get("fields", {})
    walk(schema, _ROOT_PATH)

    workload = experiment.get("workload") if isinstance(experiment, dict) else None
    name = workload.get("name") if isinstance(workload, dict) else None
    contract = catalog.get("workloads", {}).get(name, {})
    if isinstance(contract, dict):
        walk(contract.get("params"), "workload.params")
        loading = contract.get("loading")
        walk(loading, "loading")
        if isinstance(loading, dict):
            walk(loading.get("post_load"), "loading.post_load")

    return {field: sorted(paths) for field, paths in found.items()}


def _defined_elsewhere(
    name: str, path: str, locations: dict[str, list[str]] | None,
) -> str:
    """Name the blocks defining ``name``, other than the one it was written in."""
    if not locations:
        return ""
    here = _INDEXED.sub(_INDEX_SUFFIX, path)
    others = [where for where in locations.get(name, []) if where != here]
    return " or ".join(others)


def _check_fields(
    value: Any, allowed: Any, path: str,
    locations: dict[str, list[str]] | None = None,
) -> dict[str, str] | None:
    """Reject unknown keys, then check each known key's value against its definition.

    :param value: The block being checked.
    :param allowed: The field definitions legal in this block.
    :param path: Display path of the block, used in messages.
    :param locations: Field name to the paths the contract defines it at, used
        to point a misplaced field at the block it belongs in.
    """
    if not isinstance(value, dict):
        return _error(f"{path} must be an object")
    unknown = set(value) - set(allowed)
    if unknown:
        name = sorted(unknown)[0]
        message = f"{path} contains unknown field '{name}'"
        # A field that is legal elsewhere is misplaced rather than invented, and
        # the schema already knows where it belongs. Saying so turns a rejection
        # the author has to search the contract to resolve into one they can act
        # on, the way an unavailable storage class names the classes that exist.
        if elsewhere := _defined_elsewhere(name, path, locations):
            message += f"; the contract defines '{name}' under {elsewhere}"
        return _error(message)
    for name, definition in allowed.items():
        if isinstance(definition, dict) and definition.get("required") and not value.get(name):
            return _error(f"{path} is missing required field '{name}'")
    for name, item in value.items():
        # YAML's null says "no value" just as plainly as leaving the key out,
        # and the catalog documents null as meaning unset for the fields whose
        # profiles accept it. Only a required field may not be null, which the
        # missing-field check above already rejects.
        if item is None:
            continue
        error = _check_value(item, allowed[name], f"{path}.{name}")
        if error:
            return error
    return None


def _check_requests_fit_limits(resources: dict[str, Any]) -> dict[str, str] | None:
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


class _Expansion(NamedTuple):
    """How many of each factor an experiment expands to.

    :ivar systems: Systems under test crossed by the experiment.
    :ivar resource_cells: Cells of the CPU/memory sweep, one when there is none.
    :ivar rounds: Entries of the parallel-client sweep.
    :ivar repetitions: Times the whole round list repeats.
    """

    systems: int
    resource_cells: int
    rounds: int
    repetitions: int


def _expansion(experiment: dict[str, Any]) -> _Expansion:
    """Measure the factors an experiment varies.

    Both the run count and the repetitions rule need these four numbers, and
    they have to agree about them, so they are counted once here.

    :param experiment: A loaded experiment.yml.
    :return: The four factor sizes.
    :rtype: _Expansion
    """
    resources = experiment.get("resources") or {}
    # A sweep is a list of cells; anything else is a single fixed cell.
    cells = [resources.get(resource) for resource in ("cpu", "memory")]
    workload = experiment.get("workload") or {}
    return _Expansion(
        systems=len(experiment.get("systems") or []),
        resource_cells=max(
            (len(cell) for cell in cells if isinstance(cell, list) and cell),
            default=1,
        ),
        rounds=len(workload.get("rounds") or _DEFAULT_ROUNDS),
        repetitions=workload.get("repetitions") or _DEFAULT_REPETITIONS,
    )


def _check_workload_shape(
    catalog: dict[str, Any], experiment: Any, schema: dict[str, Any],
    locations: dict[str, list[str]] | None = None,
) -> dict[str, str] | None:
    """Check the workload block and the loading block its contract governs."""
    workload = experiment.get("workload", {})
    if error := _check_fields(workload, schema["workload"]["fields"], "workload",
                              locations):
        return error
    contract = catalog.get("workloads", {}).get(workload.get("name"), {})
    if error := _check_fields(
        workload.get("params", {}), contract.get("params", {}), "workload.params",
        locations,
    ):
        return error

    loading = experiment.get("loading", {})
    # The workload's own loading block carries the bounds (pods/threads min: 1);
    # the schema block carries the shape. Merge so both are enforced from where
    # each is declared, rather than duplicating the bounds into the schema.
    loading_fields = {**schema["loading"]["fields"], **contract.get("loading", {})}
    if error := _check_fields(loading, loading_fields, "loading", locations):
        return error
    return _check_fields(loading.get("post_load", {}),
                         contract.get("loading", {}).get("post_load", {}),
                         "loading.post_load", locations)


def _check_systems_shape(
    experiment: Any, schema: dict[str, Any],
    locations: dict[str, list[str]] | None = None,
) -> dict[str, str] | None:
    """Check each system entry, and refuse treatments Bexhoma would merge."""
    systems = experiment.get("systems", [])
    if not isinstance(systems, list):
        return {"stage": CATALOG_STAGE, "message": "systems must be a list"}
    item_fields = schema["systems"]["item_fields"]
    for index, system in enumerate(systems):
        if error := _check_fields(system, item_fields, f"systems[{index}]",
                                  locations):
            return error
    names = [system["name"] for system in systems]
    if repeated := sorted({name for name in names if names.count(name) > 1}):
        return _error(
            "systems repeats system name(s) "
            f"{repeated}, but the Bexhoma TPC-H runtime collapses same-named "
            "entries into one configuration; run one treatment in this experiment "
            "and use a follow-up experiment for the other treatment",
            METHODOLOGY_STAGE,
        )
    return None


def _check_resources_shape(
    experiment: Any, schema: dict[str, Any],
    locations: dict[str, list[str]] | None = None,
) -> dict[str, str] | None:
    """Check the resource block, each sweep cell, storage, and request/limit sanity."""
    fields = schema["resources"]["fields"]
    resources = experiment.get("resources", {})
    if error := _check_fields(resources, fields, "resources", locations):
        return error
    for resource in ("cpu", "memory"):
        cells = resources.get(resource, {})
        for index, cell in enumerate(cells if isinstance(cells, list) else [cells]):
            if error := _check_fields(cell, fields[resource]["item_fields"],
                                      f"resources.{resource}[{index}]", locations):
                return error
    if error := _check_fields(resources.get("storage", {}),
                              fields["storage"]["fields"], "resources.storage",
                              locations):
        return error
    return _check_requests_fit_limits(resources)


def _check_declared_factors(
    experiment: Any, schema: dict[str, Any],
) -> dict[str, str] | None:
    """Require ``discriminates`` to name exactly the factors the experiment varies."""
    declared = experiment.get("discriminates", [])
    if not isinstance(declared, list):
        return {"stage": CATALOG_STAGE, "message": "discriminates must be a list"}
    allowed = set(schema["discriminates"].get("values", []))
    if allowed and (unknown := set(declared) - allowed):
        return {"stage": CATALOG_STAGE,
                "message": f"discriminates contains unknown factor '{sorted(unknown)[0]}'"}

    resources = experiment.get("resources", {})
    expansion = _expansion(experiment)
    varied = set()
    if expansion.systems > 1:
        varied.add("system")
    if expansion.rounds > 1:
        varied.add("concurrency")
    for resource in ("cpu", "memory"):
        if isinstance(resources.get(resource), list) and len(resources[resource]) > 1:
            varied.add(resource)
    if mismatch := varied.symmetric_difference(declared):
        message = ("M2.6: discriminates must name exactly the varied factors; "
                   f"declared {sorted(declared)}, varied {sorted(varied)}; "
                   f"they differ on {sorted(mismatch)}")
        # An experiment that varies nothing cannot satisfy the rule by editing
        # discriminates, which the catalog requires to be a non-empty list, so
        # the only way out is a second treatment.
        if not varied:
            message += (". This experiment runs a single treatment, so there is "
                        "nothing to isolate: add a second system the workload "
                        "supports, a second entry in rounds to vary concurrency, "
                        "or a list of cpu or memory cells")
        return {"stage": METHODOLOGY_STAGE, "message": message}
    return None


def _check_contract_shape(
    catalog: dict[str, Any], experiment: Any,
) -> list[dict[str, str]]:
    """Reject fields outside the schema embedded in the agent's catalog.

    Independent sections are checked in full rather than stopping at the first
    fault, so an author sees every structural problem in one verdict instead of
    discovering them one validation at a time.

    :param catalog: Loaded ``contract_catalog.yml``.
    :param experiment: Loaded experiment.yml.
    :return: Every problem found, empty when the shape is legal.
    :rtype: list[dict[str, str]]
    """
    if not isinstance(catalog, dict):
        return [{"stage": CATALOG_STAGE, "message": "catalog must be an object"}]
    schema = catalog.get("experiment_schema", {}).get("fields", {})
    locations = _schema_locations(catalog, experiment)
    # Every section check below indexes into the document, so a top level that
    # is not a well-formed object is reported alone rather than used.
    if top_level_error := _check_fields(experiment, schema, _ROOT_PATH, locations):
        return [top_level_error]

    errors = []
    for error in (
        _check_workload_shape(catalog, experiment, schema, locations),
        _check_systems_shape(experiment, schema, locations),
        *(_check_fields(experiment.get(section, {}),
                        schema[section]["fields"], section, locations)
          for section in ("observe", "placement")),
        _check_resources_shape(experiment, schema, locations),
    ):
        if error:
            errors.append(error)

    # The declared-factors rule counts systems, rounds and resource cells, so a
    # section that failed its shape check would make it count nonsense. Only ask
    # once the structure it reads is known to be sound.
    if not errors and (error := _check_declared_factors(experiment, schema)):
        errors.append(error)
    return errors




def count_runs(experiment: dict[str, Any]) -> int:
    """Count the benchmark runs an experiment expands to.

    Every system is crossed against every resource sweep cell to give one
    resolved configuration, and each configuration runs every entry of
    ``workload.rounds`` once per repetition.

    :param experiment: A loaded experiment.yml.
    :return: Total number of benchmark runs.
    :rtype: int
    """
    expansion = _expansion(experiment)
    return (expansion.systems * expansion.resource_cells
            * expansion.rounds * expansion.repetitions)


def _timeout_budget(
    catalog: dict[str, Any], experiment: dict[str, Any],
) -> dict[str, Any]:
    """Estimate the maximum time consumed by declared workload deadlines."""
    workload = experiment.get("workload") or {}
    params = workload.get("params") or {}
    workload_contract = (
        catalog.get("workloads", {}).get(workload.get("name"), {})
    )
    parameter_contract = workload_contract.get("params", {})

    timeout_contract = parameter_contract.get("timeout", {})
    query_timeout = params.get("timeout")
    if query_timeout is None and isinstance(timeout_contract, dict):
        query_timeout = timeout_contract.get("default")

    active_queries = params.get("active_queries")
    if isinstance(active_queries, list):
        query_count = len(active_queries)
    else:
        active_contract = parameter_contract.get("active_queries", {})
        query_count = active_contract.get("max") if isinstance(active_contract, dict) else None

    repeat_contract = parameter_contract.get("query_repeats", {})
    query_repeats = params.get("query_repeats")
    if query_repeats is None and isinstance(repeat_contract, dict):
        query_repeats = repeat_contract.get("default", 1)

    benchmark_minutes = None
    if all(isinstance(value, int) and not isinstance(value, bool) for value in (
        query_timeout, query_count, query_repeats,
    )):
        benchmark_minutes = round(
            count_runs(experiment) * query_count * query_repeats * query_timeout / 60,
            1,
        )

    loading_timeout = (experiment.get("loading") or {}).get("timeout_minutes")
    loading_minutes = None
    if isinstance(loading_timeout, int) and not isinstance(loading_timeout, bool):
        expansion = _expansion(experiment)
        loading_minutes = (
            expansion.systems * expansion.resource_cells
            * expansion.repetitions * loading_timeout
        )

    total_minutes = None
    if benchmark_minutes is not None:
        total_minutes = benchmark_minutes + (loading_minutes or 0)
    return {
        "query_timeout_budget_min": benchmark_minutes,
        "loading_timeout_budget_min": loading_minutes,
        "declared_timeout_budget_min": total_minutes,
        "basis": (
            "Conservative deadline budget, not a runtime prediction: benchmark "
            "phases are sequential, parallel streams within one phase overlap, "
            "and most queries should finish before their timeout."
        ),
    }


def _check_falsifiable_claim(experiment: dict[str, Any]) -> dict[str, str] | None:
    """Refuse a hypothesis no measurement could contradict (handbook M1.1).

    Decidable only in the crude sense the handbook describes: whether the claim
    names any outcome at all. A hypothesis built purely from adequacy language
    is confirmed by every possible run, which makes the experiment unable to
    fail rather than merely likely to succeed.

    :param experiment: Loaded experiment.yml.
    :return: An error object, or ``None`` when the claim names an outcome.
    :rtype: dict[str, str] | None
    """
    hypothesis = experiment.get("hypothesis")
    if not isinstance(hypothesis, str) or not hypothesis.strip():
        return None
    text = hypothesis.lower()
    if any(character.isdigit() for character in text):
        return None
    if any(marker in text for marker in _COMPARATIVE_MARKERS):
        return None
    if not any(stem in text for stem in _ADEQUACY_STEMS):
        return None
    return {
        "stage": METHODOLOGY_STAGE,
        "message": (
            "M1.1: the hypothesis states adequacy rather than an outcome a "
            "measurement could contradict, so every possible run confirms it. "
            "Say which quantity moves in which direction, or against which "
            "threshold it is judged, so that some result would refute it"
        ),
    }


def _check_fixed_envelope(experiment: dict[str, Any]) -> dict[str, str] | None:
    """Refuse an elastic resource envelope in a comparison (handbook M2.3).

    When the guaranteed allocation is below the permitted maximum, the share an
    arm actually receives depends on what else runs on the machine, so the
    envelope becomes an uncontrolled factor varying exactly where the comparison
    is made.

    :param experiment: Loaded experiment.yml.
    :return: An error object, or ``None`` when every cell is fixed.
    :rtype: dict[str, str] | None
    """
    resources = experiment.get("resources")
    if not isinstance(resources, dict):
        return None
    for name in ("cpu", "memory"):
        cells = resources.get(name)
        for cell in (cells if isinstance(cells, list) else [cells]):
            if not isinstance(cell, dict):
                continue
            request, limit = cell.get("request"), cell.get("limit")
            if request is None or limit is None or str(request) == str(limit):
                continue
            return {
                "stage": METHODOLOGY_STAGE,
                "message": (
                    f"M2.3: resources.{name} guarantees {request} but permits "
                    f"{limit}, so each arm receives whatever the node happens to "
                    "have free and the envelope varies where the comparison is "
                    "made. Set request and limit to the same value"
                ),
            }
    return None


def _check_repetitions(
    catalog: dict[str, Any],
    experiment: dict[str, Any],
) -> dict[str, str] | None:
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
    :rtype: dict[str, str] | None
    """
    workload = experiment.get("workload") or {}
    declared = (
        catalog.get("workloads", {})
        .get(workload.get("name"), {})
        .get("repetitions", {})
    )
    minimum = declared.get("minimum_for_conclusions") if isinstance(declared, dict) else None
    # A workload that names no minimum is still bound by M5.1: two runs are the
    # fewest from which any spread can be estimated at all.
    source = (
        f"'{workload.get('name')}' declares minimum_for_conclusions={minimum}"
        if minimum else
        f"the handbook admits no comparison below {_SPREAD_FLOOR} repetitions"
    )
    minimum = minimum or _SPREAD_FLOOR

    expansion = _expansion(experiment)
    compares = (expansion.systems > 1 or expansion.resource_cells > 1
                or expansion.rounds > 1)
    repetitions = expansion.repetitions
    if not compares or repetitions >= minimum:
        return None

    return {
        "stage": METHODOLOGY_STAGE,
        "message": (
            f"M5.1: workload.repetitions={repetitions} but this experiment "
            f"compares several configurations, and {source}: with fewer "
            "repetitions a difference between them cannot be told apart from "
            f"run-to-run variance. Raise repetitions to at least {minimum}"
        ),
    }


def _format_cpu(cores: float) -> str:
    """Format a CPU requirement in whole or fractional cores."""
    return f"{cores:g} cores"


def _format_memory(num_bytes: int) -> str:
    """Format a byte requirement as GiB when it divides evenly."""
    if num_bytes % _GIBIBYTE_BYTES == 0:
        return f"{num_bytes // _GIBIBYTE_BYTES}Gi"
    return f"{num_bytes} bytes"


def _maximum_sut_limit(
    experiment: dict[str, Any],
    resource: str,
) -> float | int:
    """Return the largest SUT limit declared for one resource."""
    resources = experiment.get("resources") or {}
    declared = resources.get(resource, {})
    cells = declared if isinstance(declared, list) else [declared]
    parser = (
        spec.parse_cpu_quantity
        if resource == "cpu"
        else spec.parse_memory_quantity
    )
    limits = [
        parser(cell["limit"])
        for cell in cells
        if isinstance(cell, dict) and cell.get("limit") is not None
    ]
    if not limits:
        return 0
    return max(limits)


def _check_component_placement(
    catalog: dict[str, Any],
    environment: dict[str, Any],
    experiment: dict[str, Any],
) -> dict[str, str] | None:
    """Check peak co-located SUT and benchmarker limits against pinned nodes.

    Kubernetes schedules Pods from their requests, but that alone permits a
    node whose declared limits add up beyond its allocatable capacity. This
    agent-only preflight check deliberately uses limits so a valid design has a
    safe peak envelope rather than merely being schedulable.

    :param catalog: Loaded ``contract_catalog.yml``.
    :param environment: Loaded ``environment.yml``.
    :param experiment: Loaded experiment specification.
    :return: An environment-stage error, or ``None`` when pinned components fit.
    :rtype: dict[str, str] | None
    """
    workload = experiment.get("workload") or {}
    components = (
        catalog.get("workloads", {})
        .get(workload.get("name"), {})
        .get("component_resources", {})
    )
    benchmarker = (
        components.get("benchmarker")
        if isinstance(components, dict)
        else None
    )
    if not isinstance(benchmarker, dict):
        return None

    placement = experiment.get("placement") or {}
    benchmarker_node = placement.get("benchmarking")
    if benchmarker_node is None:
        # Without pinning, Kubernetes may distribute these Pods across nodes;
        # summing them against one arbitrary node would reject legal designs.
        return None

    nodes = {node["name"]: node for node in environment.get("nodes", [])}
    node = nodes.get(benchmarker_node)
    if node is None:
        # The shared environment validator reports absent placement nodes.
        return None

    per_pod = benchmarker.get("per_pod_limit") or {}
    replicas = benchmarker.get("replicas") or {}
    try:
        per_stream = int(replicas["per_concurrent_stream"])
        per_pod_cpu = spec.parse_cpu_quantity(per_pod["cpu"])
        per_pod_memory = spec.parse_memory_quantity(per_pod["memory"])
        if per_stream < 1:
            raise ValueError("per_concurrent_stream must be at least 1")
    except (KeyError, spec.SpecError, TypeError, ValueError) as error:
        return _error(
            "workloads."
            f"{workload.get('name')}.component_resources.benchmarker is "
            f"invalid: {error}"
        )
    peak_clients = max(workload.get("rounds") or _DEFAULT_ROUNDS)
    benchmarker_pods = per_stream * peak_clients
    requirements: dict[str, float | int] = {
        "cpu": per_pod_cpu * benchmarker_pods,
        "memory": per_pod_memory * benchmarker_pods,
    }
    descriptions = f"{benchmarker_pods} benchmarker pod(s) (round {peak_clients})"
    if placement.get("sut") == benchmarker_node:
        requirements["cpu"] += float(_maximum_sut_limit(experiment, "cpu"))
        requirements["memory"] += int(_maximum_sut_limit(experiment, "memory"))
        descriptions = f"one active SUT pod and {descriptions}"

    allocatable = node.get("allocatable") or {}
    for resource, parser, formatter in (
        ("cpu", spec.parse_cpu_quantity, _format_cpu),
        ("memory", spec.parse_memory_quantity, _format_memory),
    ):
        available = allocatable.get(resource)
        if available is None:
            continue
        available_parsed = parser(available)
        required = requirements[resource]
        if required > available_parsed:
            return _error(
                f"placement pins {descriptions} to node '{benchmarker_node}'; "
                f"their declared peak {resource} limits require "
                f"{formatter(required)}, exceeding allocatable "
                f"{formatter(available_parsed)}. Lower workload.rounds or use "
                "a separate/larger benchmarking node",
                ENVIRONMENT_STAGE,
            )
    return None


def _verdict(
    errors: list[dict[str, str]],
    environment_checked: bool,
    experiment: dict[str, Any] | None = None,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the verdict object the agent receives.

    :param errors: Problems found, empty when the specification is valid.
    :param environment_checked: Whether the cluster-fit checks actually ran.
    :param experiment: Loaded experiment.yml, or ``None`` when it did not parse.
    :return: The verdict.
    :rtype: dict[str, Any]
    """
    estimate = {
        "runs": count_runs(experiment) if isinstance(experiment, dict) else None,
        "duration_min": None,
    }
    if isinstance(experiment, dict) and isinstance(catalog, dict):
        estimate.update(_timeout_budget(catalog, experiment))
    return {
        "valid": not errors,
        "errors": errors,
        # An unchecked environment means placement and resource ceilings were
        # never verified, so "valid" is weaker than it looks -- say so rather
        # than let the agent read it as a full pass.
        "environment_checked": environment_checked,
        "estimate": estimate,
    }


def _check_storage_class(
    environment: dict[str, Any], experiment: dict[str, Any],
) -> dict[str, str] | None:
    """Name the storage classes this cluster offers when the spec asks for another.

    The shared resolver rejects an unavailable class without saying which ones
    exist, which leaves an author guessing at a closed list it cannot see.

    :param environment: The cluster descriptor.
    :param experiment: The specification being validated.
    :return: An error entry, or ``None`` when the requested class exists.
    :rtype: dict[str, str] | None
    """
    requested = (experiment.get("resources") or {}).get("storage_class")
    if requested is None:
        return None
    available = sorted(
        entry["name"] for entry in environment.get("storage_classes", [])
        if isinstance(entry, dict) and "name" in entry
    )
    if requested in available:
        return None
    return {
        "stage": ENVIRONMENT_STAGE,
        "message": (
            f"resources.storage_class {requested!r} is not offered by this cluster; "
            f"it has {', '.join(available) or 'none'}. Omit the field entirely to "
            "take node-local storage instead, which every profile that lists null "
            "among its allowed classes permits."
        ),
    }


def validate_spec(
    experiment_path: str,
    catalog_path: str,
    environment_path: str | None = None,
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
        shape_errors = _check_contract_shape(catalog, experiment)
    except (KeyError, TypeError) as error:
        return _verdict([{"stage": CATALOG_STAGE,
                          "message": f"the catalog is missing the structure validation needs: {error}"}],
                        False)
    if shape_errors:
        return _verdict(shape_errors, False)

    try:
        spec.build_argv(catalog, experiment)
    except (spec.SpecError, IndexError, KeyError, TypeError, ValueError) as error:
        return _verdict(
            [{"stage": CATALOG_STAGE, "message": str(error)}], False,
            experiment, catalog,
        )

    # Principles of the handbook that are decidable from the
    # specification alone; the rest is the agent's to apply. They are
    # independent of each other, so all of them are reported together rather
    # than one per attempt -- a design with three method defects would
    # otherwise cost three attempts to learn about them.
    methodology_errors = [
        error for error in (
            _check_falsifiable_claim(experiment),
            _check_fixed_envelope(experiment),
            _check_repetitions(catalog, experiment),
        ) if error is not None
    ]
    if methodology_errors:
        return _verdict(methodology_errors, False, experiment, catalog)

    if not environment_path or not os.path.isfile(environment_path):
        return _verdict([], False, experiment, catalog)

    try:
        environment = spec.load_environment(environment_path)
    except (OSError, yaml.YAMLError) as error:
        return _verdict(
            [{"stage": PARSE_STAGE, "message": str(error)}], False,
            experiment, catalog,
        )

    # Storage class and pod placement fail independently of each other, so both
    # are reported together. The shared resolver is only asked once the storage
    # class is known to exist, because an unavailable class is the fault it
    # would report anyway, in less helpful words.
    environment_errors = []
    if storage_error := _check_storage_class(environment, experiment):
        environment_errors.append(storage_error)
    else:
        try:
            spec.validate_environment(environment, experiment)
        except spec.SpecError as error:
            environment_errors.append(
                {"stage": ENVIRONMENT_STAGE, "message": str(error)})
    if component_error := _check_component_placement(catalog, environment, experiment):
        environment_errors.append(component_error)

    return _verdict(environment_errors, True, experiment, catalog)
