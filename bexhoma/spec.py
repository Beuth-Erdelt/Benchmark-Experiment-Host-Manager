"""
Translate a catalog-backed ``experiment.yml`` into a bexhoma CLI invocation.

This module implements Phase 1 of the catalog contract proposed in
``docs/Design-Catalog-Contract.md`` (see also GitHub issue #764): it resolves
an ``experiment.yml`` against ``catalog.yaml`` (workload parameters, system
knobs, profiles, ``derive:`` formulas) and emits the argument vector an
existing bexhoma entry script already understands. No entry script or
execution code path is changed by this module — it only produces the CLI
arguments a human would otherwise have had to type by hand, so the result
can be run as ``python tpch.py <argv...>`` exactly like any other invocation.

Scope is intentionally narrow: only the ``tpch`` workload against the
``PostgreSQL``/``PgDuckDB`` system pair is translatable today, matching the
prototype catalog in ``catalog.yaml``. Extending to other workloads/systems
means extending :func:`build_argv`'s flag mapping and :func:`resolve_system`'s
``arg_style`` handling, not changing the resolution logic itself.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import operator
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

import yaml

__all__ = [
    "DERIVE_INPUTS",
    "SpecError",
    "ResolvedKnob",
    "ResolvedSystem",
    "load_catalog",
    "load_experiment",
    "load_environment",
    "evaluate_derive_expression",
    "parse_memory_quantity",
    "parse_cpu_quantity",
    "format_postgres_memory",
    "resolve_system_definition",
    "resolve_system",
    "validate_experiment",
    "validate_environment",
    "build_argv",
    "build_command",
    "translate",
]

#: Names a ``derive:`` expression is allowed to reference.
DERIVE_INPUTS = ("memory_limit", "cpu_limit", "storage_class", "scaling_factor")

#: Kubernetes-style memory quantity unit suffixes, longest first so "Ki" is
#: tried before the decimal "K" would otherwise wrongly match its prefix.
_MEMORY_UNITS: tuple[tuple[str, int], ...] = (
    ("Ki", 1024), ("Mi", 1024 ** 2), ("Gi", 1024 ** 3), ("Ti", 1024 ** 4),
    ("K", 1000), ("M", 1000 ** 2), ("G", 1000 ** 3), ("T", 1000 ** 4),
)

#: Divisor to format a byte count as whole megabytes for a PostgreSQL memory GUC.
_BYTES_PER_MEGABYTE = 1024 ** 2

#: Kubernetes-style CPU quantity suffix for millicores (e.g. "500m" == 0.5 cores).
_CPU_MILLICORE_SUFFIX = "m"
_MILLICORES_PER_CORE = 1000

#: environment.yml roles a placement: entry can pin to a Kubernetes node.
_PLACEMENT_ROLES = ("sut", "loading", "benchmarking")

_DERIVE_BINARY_OPS: dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_DERIVE_UNARY_OPS: dict[type, Callable[[float], float]] = {
    ast.USub: operator.neg,
}

#: Header fields every experiment.yml must carry, independent of workload/system.
_REQUIRED_HEADER_FIELDS = ("title", "hypothesis", "discriminates")

_DEFAULT_MODE = "run"
_DEFAULT_ARG_STYLE = "pg-guc"
_ARG_STYLE_ENV_VAR = "env-var"
_STORAGE_FORMAT_COLUMNAR = "columnar"
_KNOB_TYPE_MEMORY = "memory"

#: The only env-var knob this prototype can translate — it happens to already
#: be a first-class tpch.py flag, so it needs no generic env-var CLI mapping yet.
_DUCKDB_FORCE_EXECUTION_ENV_VAR = "DUCKDB_FORCE_EXECUTION"
_DUCKDB_FORCE_EXECUTION_FLAG = "-xdfe"


class SpecError(Exception):
    """Raised when catalog.yaml or experiment.yml is malformed, or the
    experiment is invalid against the catalog (unsupported workload/system
    pairing, illegal parameter value, unmet profile precondition, ...)."""


@dataclass
class ResolvedKnob:
    """A single system knob after profile/derive/override resolution.

    :ivar name: Knob name, as declared in the catalog.
    :ivar value: Final resolved value.
    :ivar arg_style: How this knob is applied — e.g. ``"pg-guc"`` or ``"env-var"``.
    :ivar env_var: Environment variable name, only set when ``arg_style == "env-var"``.
    """
    name: str
    value: Any
    arg_style: str
    env_var: Optional[str] = None


@dataclass
class ResolvedSystem:
    """A fully resolved ``systems:`` entry from an experiment.yml.

    :ivar name: System name, as declared in the catalog.
    :ivar deployment: Kubernetes Deployment name, used to build ``--set`` selectors.
    :ivar knobs: Final knob values, keyed by knob name.
    :ivar physical_design: The system's physical-design support, from the catalog.
    :ivar storage_class: Storage class the experiment resolved to, when the profile
        declares a ``requires.storage_class`` precondition (``None`` for ephemeral,
        even though the precondition was satisfied).
    """
    name: str
    deployment: str
    knobs: dict[str, ResolvedKnob] = field(default_factory=dict)
    physical_design: dict[str, Any] = field(default_factory=dict)
    storage_class: Optional[str] = None


def load_catalog(path: str) -> dict[str, Any]:
    """Load ``catalog.yaml``.

    :param path: Path to the catalog file.
    :return: Parsed catalog, with ``workloads``/``systems`` top-level keys.
    :rtype: dict[str, Any]
    """
    with open(path, "r", encoding="utf-8") as catalog_file:
        return yaml.safe_load(catalog_file)


def load_experiment(path: str) -> dict[str, Any]:
    """Load an ``experiment.yml``.

    :param path: Path to the experiment spec file.
    :return: Parsed experiment spec.
    :rtype: dict[str, Any]
    """
    with open(path, "r", encoding="utf-8") as experiment_file:
        return yaml.safe_load(experiment_file)


def load_environment(path: str) -> dict[str, Any]:
    """Load an ``environment.yml``.

    :param path: Path to the environment descriptor file, as produced by
        :func:`bexhoma.environment.write_environment_yml`.
    :return: Parsed environment descriptor, with ``nodes``/``excluded_nodes``/
        ``storage_classes``/``resource_limits`` top-level keys.
    :rtype: dict[str, Any]
    """
    with open(path, "r", encoding="utf-8") as environment_file:
        return yaml.safe_load(environment_file)


def _eval_derive_node(node: ast.AST, inputs: dict[str, float]) -> float:
    """Recursively evaluate one node of a whitelisted derive-expression AST.

    :param node: AST node, restricted to arithmetic BinOp/UnaryOp/Constant/Name.
    :param inputs: Values available for ``ast.Name`` lookups.
    :return: Evaluated numeric result.
    :rtype: float
    :raises SpecError: On any disallowed construct or unknown name.
    """
    if isinstance(node, ast.BinOp) and type(node.op) in _DERIVE_BINARY_OPS:
        left = _eval_derive_node(node.left, inputs)
        right = _eval_derive_node(node.right, inputs)
        return _DERIVE_BINARY_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _DERIVE_UNARY_OPS:
        return _DERIVE_UNARY_OPS[type(node.op)](_eval_derive_node(node.operand, inputs))
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in inputs:
            raise SpecError(f"derive expression references unknown input '{node.id}'")
        return inputs[node.id]
    raise SpecError(f"derive expression contains a disallowed construct: {ast.dump(node)}")


def evaluate_derive_expression(expression: str, inputs: dict[str, float]) -> float:
    """Evaluate a ``derive:`` formula.

    Deliberately minimal: arithmetic over exactly :data:`DERIVE_INPUTS`, no
    functions, no conditionals — see ``docs/Design-Catalog-Contract.md``.

    :param expression: Formula text, e.g. ``"0.75 * memory_limit"``.
    :param inputs: Numeric values for the declared derive inputs.
    :return: Evaluated result.
    :rtype: float
    :raises SpecError: When the expression uses anything outside the whitelist.
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise SpecError(f"invalid derive expression {expression!r}: {error}") from error
    return _eval_derive_node(tree.body, inputs)


def parse_memory_quantity(value: str) -> int:
    """Parse a Kubernetes-style memory quantity into bytes.

    :param value: A quantity such as ``"64Gi"``, ``"512Mi"``, or a plain byte count.
    :return: Number of bytes.
    :rtype: int
    :raises SpecError: When the value cannot be parsed.
    """
    text = str(value).strip()
    for suffix, multiplier in _MEMORY_UNITS:
        if text.endswith(suffix):
            number = text[: -len(suffix)]
            try:
                return int(float(number) * multiplier)
            except ValueError as error:
                raise SpecError(f"invalid memory quantity {value!r}") from error
    try:
        return int(text)
    except ValueError as error:
        raise SpecError(f"invalid memory quantity {value!r}") from error


def parse_cpu_quantity(value: Any) -> float:
    """Parse a Kubernetes-style CPU quantity into whole cores.

    :param value: A quantity such as ``8``, ``"8"``, or millicore ``"500m"``.
    :return: Number of cores.
    :rtype: float
    :raises SpecError: When the value cannot be parsed.
    """
    text = str(value).strip()
    if text.endswith(_CPU_MILLICORE_SUFFIX):
        try:
            return float(text[: -len(_CPU_MILLICORE_SUFFIX)]) / _MILLICORES_PER_CORE
        except ValueError as error:
            raise SpecError(f"invalid cpu quantity {value!r}") from error
    try:
        return float(text)
    except ValueError as error:
        raise SpecError(f"invalid cpu quantity {value!r}") from error


def format_postgres_memory(num_bytes: int) -> str:
    """Format a byte count as a PostgreSQL memory GUC value.

    Always formats in whole megabytes to avoid fractional-GB rounding
    ambiguity — PostgreSQL accepts ``MB`` for every memory GUC used in this
    catalog.

    :param num_bytes: Number of bytes.
    :return: A value such as ``"20480MB"``.
    :rtype: str
    """
    return f"{num_bytes // _BYTES_PER_MEGABYTE}MB"


def resolve_system_definition(catalog: dict[str, Any], system_name: str) -> dict[str, Any]:
    """Resolve a system's catalog entry, merging any ``extends:`` base.

    :param catalog: Parsed catalog.
    :param system_name: System name to resolve.
    :return: Merged system definition (``knobs``, ``profiles``, ``physical_design``, ...).
    :rtype: dict[str, Any]
    :raises SpecError: When the system or its ``extends:`` base does not exist.
    """
    systems = catalog.get("systems", {})
    if system_name not in systems:
        raise SpecError(f"unknown system '{system_name}'")
    entry = systems[system_name]
    base_name = entry.get("extends")
    if base_name is None:
        return dict(entry)
    base = resolve_system_definition(catalog, base_name)
    merged = dict(base)
    merged["knobs"] = {**base.get("knobs", {}), **entry.get("knobs", {})}
    merged["profiles"] = {**base.get("profiles", {}), **entry.get("profiles", {})}
    for key, value in entry.items():
        if key not in ("knobs", "profiles", "extends"):
            merged[key] = value
    return merged


def _resolve_profile(catalog: dict[str, Any], definition: dict[str, Any], profile_name: str) -> dict[str, Any]:
    """Resolve a profile, following a ``ref:`` pointer to another system's profile if present.

    :param catalog: Parsed catalog.
    :param definition: Merged system definition the profile was requested on.
    :param profile_name: Profile name.
    :return: Profile dict with ``knobs``/``derive``/``requires`` keys.
    :rtype: dict[str, Any]
    :raises SpecError: When the profile, or a ``ref:`` it points to, does not exist.
    """
    profiles = definition.get("profiles", {})
    if profile_name not in profiles:
        raise SpecError(f"unknown profile '{profile_name}' for system '{definition.get('deployment', '?')}'")
    profile = profiles[profile_name]
    ref = profile.get("ref")
    if ref is None:
        return profile
    ref_system, separator, ref_profile = ref.partition(".profiles.")
    if not separator:
        raise SpecError(f"malformed profile ref {ref!r}, expected 'System.profiles.name'")
    ref_definition = resolve_system_definition(catalog, ref_system)
    return _resolve_profile(catalog, ref_definition, ref_profile)


def resolve_system(
    catalog: dict[str, Any],
    system_spec: dict[str, Any],
    resources: dict[str, Any],
) -> ResolvedSystem:
    """Resolve one ``systems:`` entry of an experiment.yml against the catalog.

    Applies, in order: the named profile's literal ``knobs:``, its
    ``derive:`` formulas evaluated against ``resources``, and finally the
    spec's own ``override:``. Knobs the profile/override never mention keep
    whatever default is already baked into the system's shipped k8s
    template — this function only resolves values an experiment.yml
    actually chose to set.

    :param catalog: Parsed catalog.
    :param system_spec: One entry of experiment.yml's ``systems:`` list
        (``name``, optional ``profile``, optional ``override``).
    :param resources: Experiment resource limits — ``memory_limit``,
        ``cpu_limit``, ``storage_class``, ``scaling_factor``.
    :return: The resolved system.
    :rtype: ResolvedSystem
    :raises SpecError: When a profile's ``requires:`` precondition is unmet,
        or the system/profile/a knob name is unknown.
    """
    system_name = system_spec["name"]
    definition = resolve_system_definition(catalog, system_name)
    known_knobs = definition.get("knobs", {})
    resolved = ResolvedSystem(
        name=system_name,
        deployment=definition["deployment"],
        physical_design=definition.get("physical_design", {}),
    )

    profile_name = system_spec.get("profile")
    values: dict[str, Any] = {}
    if profile_name is not None:
        profile = _resolve_profile(catalog, definition, profile_name)
        if "requires" in profile and "storage_class" in profile["requires"]:
            required_storage_class = profile["requires"]["storage_class"]
            allowed_storage_classes = (
                required_storage_class if isinstance(required_storage_class, list) else [required_storage_class]
            )
            resource_storage_class = resources.get("storage_class")
            if resource_storage_class not in allowed_storage_classes:
                raise SpecError(
                    f"system '{system_name}' profile '{profile_name}' requires "
                    f"storage_class in {allowed_storage_classes}, got "
                    f"'{resource_storage_class}'"
                )
            resolved.storage_class = resource_storage_class
        values.update(profile.get("knobs", {}))
        derive_inputs = {
            "memory_limit": parse_memory_quantity(resources["memory_limit"]),
            "cpu_limit": float(resources.get("cpu_limit", 0)),
            "storage_class": resources.get("storage_class"),
            "scaling_factor": float(resources.get("scaling_factor", 0)),
        }
        for knob_name, expression in profile.get("derive", {}).items():
            raw_value = evaluate_derive_expression(expression, derive_inputs)
            if known_knobs.get(knob_name, {}).get("type") == _KNOB_TYPE_MEMORY:
                values[knob_name] = format_postgres_memory(int(raw_value))
            else:
                values[knob_name] = raw_value

    values.update(system_spec.get("override", {}))

    for knob_name, value in values.items():
        if knob_name not in known_knobs:
            raise SpecError(f"system '{system_name}' has no knob '{knob_name}'")
        knob_meta = known_knobs[knob_name]
        resolved.knobs[knob_name] = ResolvedKnob(
            name=knob_name,
            value=value,
            arg_style=knob_meta.get("arg_style", definition.get("arg_style", _DEFAULT_ARG_STYLE)),
            env_var=knob_meta.get("env_var"),
        )
    return resolved


def validate_experiment(catalog: dict[str, Any], experiment: dict[str, Any]) -> None:
    """Validate an experiment spec against the catalog before translation.

    Checks, in order: every field in :data:`_REQUIRED_HEADER_FIELDS` is
    present and non-empty (``title``, ``hypothesis``, ``discriminates`` — an
    experiment.yml must state what it's testing and which factor it isolates
    before anything else is resolved); the workload exists; every named
    system is in the workload's ``supports:`` list; every
    ``loading.post_load`` option is a legal workload parameter (legality);
    and, for each system, that its ``physical_design`` actually supports the
    requested value (support). See "Validation ordering" in
    ``docs/Design-Catalog-Contract.md``.

    :param catalog: Parsed catalog.
    :param experiment: Parsed experiment spec.
    :raises SpecError: On any validation failure.
    """
    for field_name in _REQUIRED_HEADER_FIELDS:
        if not experiment.get(field_name):
            raise SpecError(f"experiment.yml is missing required header field '{field_name}'")
    if not isinstance(experiment["discriminates"], list):
        raise SpecError("'discriminates' must be a list of factor names")

    workload_name = experiment["workload"]["name"]
    workloads = catalog.get("workloads", {})
    if workload_name not in workloads:
        raise SpecError(f"unknown workload '{workload_name}'")
    workload = workloads[workload_name]

    system_names = [system_spec["name"] for system_spec in experiment.get("systems", [])]
    supported = workload.get("supports", [])
    for system_name in system_names:
        if system_name not in supported:
            raise SpecError(f"workload '{workload_name}' does not support system '{system_name}'")

    post_load = experiment.get("loading", {}).get("post_load", {})
    catalog_post_load = workload.get("loading", {}).get("post_load", {})
    for option_name, value in post_load.items():
        if option_name not in catalog_post_load:
            raise SpecError(f"unknown post_load option '{option_name}' for workload '{workload_name}'")
        option = catalog_post_load[option_name]
        if option.get("type") == "enum" and value not in option.get("values", []):
            raise SpecError(f"post_load.{option_name}={value!r} is not one of {option.get('values')}")
        for system_name in system_names:
            definition = resolve_system_definition(catalog, system_name)
            physical_design = definition.get("physical_design")
            if physical_design is None:
                raise SpecError(
                    f"system '{system_name}' has no physical_design concept; "
                    f"cannot honor post_load.{option_name}"
                )
            supported_value = physical_design.get(option_name)
            if isinstance(supported_value, list):
                if value not in supported_value:
                    raise SpecError(
                        f"system '{system_name}' does not support post_load.{option_name}={value!r}"
                    )
            elif value and not supported_value:
                raise SpecError(f"system '{system_name}' does not support post_load.{option_name}")


def _node_allocatable_ceiling(
    environment: dict[str, Any],
    node_name: Optional[str],
    nodes_by_name: dict[str, dict[str, Any]],
) -> tuple[Optional[float], Optional[int], str]:
    """Resolve the CPU/memory ceiling a ``resources:`` block must fit under.

    :param environment: Parsed environment descriptor.
    :param node_name: The ``placement.sut`` node name, or ``None`` when unpinned.
    :param nodes_by_name: ``environment["nodes"]`` indexed by node name.
    :return: ``(max_cpu_cores, max_memory_bytes, ceiling_scope)``; either
        ceiling is ``None`` when the environment descriptor doesn't record it.
    :rtype: tuple[Optional[float], Optional[int], str]
    """
    if node_name is not None and node_name in nodes_by_name:
        allocatable = nodes_by_name[node_name]["allocatable"]
        return (
            parse_cpu_quantity(allocatable["cpu"]),
            parse_memory_quantity(allocatable["memory"]),
            f"node '{node_name}'",
        )
    resource_limits = environment.get("resource_limits", {})
    max_cpu = resource_limits.get("max_allocatable_cpu")
    max_memory = resource_limits.get("max_allocatable_memory")
    return (
        parse_cpu_quantity(max_cpu) if max_cpu is not None else None,
        parse_memory_quantity(max_memory) if max_memory is not None else None,
        "the cluster's max_allocatable_* ceiling",
    )


def validate_environment(environment: dict[str, Any], experiment: dict[str, Any]) -> None:
    """Validate an experiment spec against the cluster's ``environment.yml``.

    Checks, in order: every node named under ``placement:`` exists in
    ``environment.yml`` and is not excluded (tainted); every
    ``resources.cpu``/``resources.memory`` sweep cell's ``request``/``limit``
    fits under the allocatable capacity of the ``placement.sut`` node (or the
    cluster-wide ``resource_limits`` ceiling, when no SUT node is pinned);
    and, when set, ``resources.storage_class`` names a storage class the
    cluster actually has.

    This is independent of :func:`validate_experiment`: that function checks
    an experiment against what the catalog *permits*; this one checks it
    against what the cluster actually *has*. Neither function depends on the
    other, so callers that only have one of the two files can still validate
    what they have.

    :param environment: Parsed environment descriptor, as returned by
        :func:`load_environment`.
    :param experiment: Parsed experiment spec.
    :raises SpecError: On any validation failure.
    """
    nodes_by_name = {node["name"]: node for node in environment.get("nodes", [])}
    excluded_node_names = {node["name"] for node in environment.get("excluded_nodes", [])}

    placement = experiment.get("placement", {})
    for role in _PLACEMENT_ROLES:
        node_name = placement.get(role)
        if node_name is None:
            continue
        if node_name in excluded_node_names:
            raise SpecError(f"placement.{role} node '{node_name}' is excluded from scheduling (tainted)")
        if node_name not in nodes_by_name:
            raise SpecError(f"placement.{role} node '{node_name}' is not in environment.yml's nodes")

    resources = experiment.get("resources", {})
    cpu_cells = resources.get("cpu", {})
    cpu_cells = cpu_cells if isinstance(cpu_cells, list) else [cpu_cells]
    memory_cells = resources.get("memory", {})
    memory_cells = memory_cells if isinstance(memory_cells, list) else [memory_cells]

    max_cpu, max_memory, ceiling_scope = _node_allocatable_ceiling(
        environment, placement.get("sut"), nodes_by_name
    )

    for cell in cpu_cells:
        for key in ("request", "limit"):
            value = cell.get(key)
            if value is None or max_cpu is None:
                continue
            if parse_cpu_quantity(value) > max_cpu:
                raise SpecError(
                    f"resources.cpu.{key}={value!r} exceeds {ceiling_scope}'s allocatable cpu ({max_cpu} cores)"
                )
    for cell in memory_cells:
        for key in ("request", "limit"):
            value = cell.get(key)
            if value is None or max_memory is None:
                continue
            if parse_memory_quantity(value) > max_memory:
                raise SpecError(
                    f"resources.memory.{key}={value!r} exceeds {ceiling_scope}'s "
                    f"allocatable memory ({max_memory} bytes)"
                )

    storage_class = resources.get("storage_class")
    if storage_class is not None:
        known_storage_classes = {entry["name"] for entry in environment.get("storage_classes", [])}
        if storage_class not in known_storage_classes:
            raise SpecError(
                f"resources.storage_class '{storage_class}' is not in environment.yml's storage_classes"
            )


def _append_flag(argv: list[str], flag: str, value: Any) -> None:
    """Append ``flag value`` to ``argv``, unless ``value`` is ``None`` or empty.

    :param argv: Argument vector being built, mutated in place.
    :param flag: CLI flag, e.g. ``"-sf"``.
    :param value: Value to stringify and append; skipped when falsy-empty (but not ``0``).
    """
    if value is None or value == "":
        return
    argv.extend([flag, str(value)])


def _resource_cell(cells: list[dict[str, Any]], index: int) -> dict[str, Any]:
    """Return the resource dict for one sweep cell, broadcasting a single-entry list.

    :param cells: Either a single ``{request, limit}`` dict wrapped in a list, or one
        entry per swept cell.
    :param index: 0-based cell index.
    :return: The ``{request, limit}`` dict for this cell.
    :rtype: dict[str, Any]
    """
    return cells[index] if len(cells) > 1 else cells[0]


def _join_cell_values(cells: list[dict[str, Any]], num_cells: int, key: str) -> Optional[str]:
    """Join a possibly-broadcast list of resource cells into a comma-separated CLI value.

    Mirrors ``tpch.py``'s own ``-rr``/``-lr``/``-rc``/``-lc`` sweep-list handling: a
    single value stays a bare value (``num_cells == 1``), several become a
    comma-separated list, one per resolved configuration.

    :param cells: Either a single-entry or ``num_cells``-entry list of ``{request, limit}`` dicts.
    :param num_cells: Number of resolved cells in this experiment.
    :param key: ``"request"`` or ``"limit"``.
    :return: Comma-separated values, or ``None`` when any cell omits ``key``.
    :rtype: Optional[str]
    """
    values = [_resource_cell(cells, index).get(key) for index in range(num_cells)]
    if any(value is None or value == "" for value in values):
        return None
    return ",".join(str(value) for value in values)


def build_argv(catalog: dict[str, Any], experiment: dict[str, Any]) -> list[str]:
    """Translate a resolved experiment.yml into a ``tpch.py`` argument vector.

    Only emits flags the spec actually sets — every flag left out falls
    back to ``tpch.py``'s own argparse default, so this never needs to
    duplicate defaults the CLI already owns.

    :param catalog: Parsed catalog.
    :param experiment: Parsed experiment spec.
    :return: Argument vector, usable as ``python tpch.py`` followed by these tokens.
    :rtype: list[str]
    :raises SpecError: When ``experiment`` fails validation or resolution.
    """
    validate_experiment(catalog, experiment)

    workload_spec = experiment["workload"]
    params = workload_spec.get("params", {})
    loading = experiment.get("loading", {})
    post_load = loading.get("post_load", {})
    resources = experiment.get("resources", {})
    observe = experiment.get("observe", {})
    placement = experiment.get("placement", {})
    system_specs = experiment.get("systems", [])

    cpu = resources.get("cpu", {})
    memory = resources.get("memory", {})
    storage = resources.get("storage", {})
    # resources.cpu / resources.memory may each be a single {request, limit} dict
    # (today's shape: shared by every system, no sweep) or a list of them (a
    # resource sweep: every system in `systems:` is crossed against every list
    # entry, one resolved configuration per (system, cell) pair) -- mirrors
    # tpch.py's own -rr/-lr/-rc/-lc comma-list handling one for one.
    cpu_cells = cpu if isinstance(cpu, list) else [cpu]
    memory_cells = memory if isinstance(memory, list) else [memory]
    num_cells = max(len(cpu_cells), len(memory_cells))
    if len(cpu_cells) not in (1, num_cells) or len(memory_cells) not in (1, num_cells):
        raise SpecError(
            "resources.cpu and resources.memory sweep lists must share one length: "
            f"got {len(cpu_cells)} cpu entries and {len(memory_cells)} memory entries"
        )

    # one (system_spec, ResolvedSystem, configuration_name) triple per resolved cell;
    # configuration_name is "" (unscoped) when there is only one cell, otherwise it
    # must match the configuration name tpch.py's own resource-sweep loop will give
    # that cell (docker + "-" + memory request), so the --set operations emitted
    # below land on the right configuration (see parse_set_arg's @CONFIG scope)
    resolved_cells: list[tuple[dict[str, Any], ResolvedSystem, str]] = []
    for system_spec in system_specs:
        for cell_index in range(num_cells):
            cell_cpu = _resource_cell(cpu_cells, cell_index)
            cell_memory = _resource_cell(memory_cells, cell_index)
            resolve_inputs = {
                "memory_limit": cell_memory.get("limit"),
                "cpu_limit": cell_cpu.get("limit"),
                "storage_class": resources.get("storage_class"),
                "scaling_factor": params.get("scaling_factor"),
            }
            resolved = resolve_system(catalog, system_spec, resolve_inputs)
            configuration_name = (
                f"{system_spec['name']}-{cell_memory.get('request')}" if num_cells > 1 else ""
            )
            resolved_cells.append((system_spec, resolved, configuration_name))

    argv: list[str] = [experiment.get("mode", _DEFAULT_MODE)]

    if system_specs:
        argv.append("-dbms")
        argv.extend(system_spec["name"] for system_spec in system_specs)

    _append_flag(argv, "-sf", params.get("scaling_factor"))
    _append_flag(argv, "-t", params.get("timeout"))
    _append_flag(argv, "-xqr", params.get("query_repeats"))
    if params.get("verify_result"):
        argv.append("-tr")
    if params.get("measure_datatransfer"):
        argv.append("-xdt")
    if params.get("active_queries"):
        argv.extend(["-xaq", ",".join(str(query) for query in params["active_queries"])])
    if params.get("recreate_parameter"):
        argv.append("-xrcp")
    if params.get("shuffle_queries"):
        argv.append("-xshq")
    _append_flag(argv, "-xlit", params.get("limit_import_table"))
    _append_flag(argv, "-xrs", params.get("refresh_streams"))
    _append_flag(argv, "-xrso", params.get("refresh_stream_offset"))

    _append_flag(argv, "-nlp", loading.get("pods"))
    _append_flag(argv, "-nlt", loading.get("threads"))
    _append_flag(argv, "-xnls", loading.get("split"))
    if post_load.get("indexes"):
        argv.append("-xii")
    if post_load.get("constraints"):
        argv.append("-xic")
    if post_load.get("statistics"):
        argv.append("-xis")
    if post_load.get("storage_format") == _STORAGE_FORMAT_COLUMNAR:
        argv.append("-xcol")

    rounds = workload_spec.get("rounds")
    if rounds:
        argv.extend(["-ne", ",".join(str(round_clients) for round_clients in rounds)])
    _append_flag(argv, "-nc", workload_spec.get("repetitions"))

    if observe.get("monitoring_sut"):
        argv.append("-m")
    if observe.get("monitoring_cluster"):
        argv.append("-mc")
    if observe.get("monitoring_app"):
        argv.append("-ma")

    _append_flag(argv, "-rnn", placement.get("sut"))
    _append_flag(argv, "-rnl", placement.get("loading"))
    _append_flag(argv, "-rnb", placement.get("benchmarking"))

    _append_flag(argv, "-rc", _join_cell_values(cpu_cells, num_cells, "request"))
    _append_flag(argv, "-lc", _join_cell_values(cpu_cells, num_cells, "limit"))
    _append_flag(argv, "-rr", _join_cell_values(memory_cells, num_cells, "request"))
    _append_flag(argv, "-lr", _join_cell_values(memory_cells, num_cells, "limit"))
    _append_flag(argv, "-rss", storage.get("size"))

    storage_classes = {resolved.storage_class for _, resolved, _ in resolved_cells if resolved.storage_class}
    if len(storage_classes) > 1:
        raise SpecError(f"resolved systems require conflicting storage classes: {sorted(storage_classes)}")
    if storage_classes:
        _append_flag(argv, "-rst", next(iter(storage_classes)))

    for system_spec, resolved, configuration_name in resolved_cells:
        scope = f"@{configuration_name}" if configuration_name else ""
        for knob in resolved.knobs.values():
            if knob.arg_style == _DEFAULT_ARG_STYLE:
                argv.extend([
                    "--set",
                    f"deployment[{resolved.deployment}]{scope}.container[dbms].{knob.name}={knob.value}",
                ])
            elif knob.arg_style == _ARG_STYLE_ENV_VAR:
                if knob.env_var == _DUCKDB_FORCE_EXECUTION_ENV_VAR:
                    if knob.value:
                        argv.append(_DUCKDB_FORCE_EXECUTION_FLAG)
                else:
                    raise SpecError(
                        f"system '{resolved.name}' knob '{knob.name}' has arg_style "
                        f"'env-var' but no known CLI mapping yet"
                    )
            else:
                raise SpecError(
                    f"system '{resolved.name}' knob '{knob.name}' has arg_style "
                    f"'{knob.arg_style}', not yet translatable to a CLI flag"
                )

    return argv


def build_command(argv: list[str], entry_script: str = "tpch.py") -> str:
    """Render an argument vector as a copy-pasteable shell command.

    :param argv: Argument vector, as returned by :func:`build_argv`.
    :param entry_script: Entry script to invoke.
    :return: A single command string.
    :rtype: str
    """
    quoted = [f'"{token}"' if " " in token else token for token in argv]
    return " ".join(["python", entry_script, *quoted])


def translate(experiment_path: str, catalog_path: str) -> list[str]:
    """Load, validate, and translate an experiment.yml into a ``tpch.py`` argument vector.

    :param experiment_path: Path to the experiment spec.
    :param catalog_path: Path to ``catalog.yaml``.
    :return: Argument vector, usable as ``python tpch.py`` followed by these tokens.
    :rtype: list[str]
    """
    catalog = load_catalog(catalog_path)
    experiment = load_experiment(experiment_path)
    return build_argv(catalog, experiment)
