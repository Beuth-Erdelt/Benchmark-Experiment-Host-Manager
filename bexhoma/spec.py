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

This module itself carries no workload- or DBMS-specific knowledge: catalog
loading, ``derive:``/knob resolution, and validation are all generic.
:func:`build_argv` dispatches by ``experiment['workload']['name']`` to that
workload's own argv builder — today ``tpch``
(:func:`bexhoma.experiments.tpch_catalog.build_tpch_argv`) and ``ycsb``
(:func:`bexhoma.experiments.ycsb_catalog.build_ycsb_argv`), matching the
prototype catalog in ``catalog.yaml`` (``tpch`` against the
``PostgreSQL``/``PgDuckDB`` pair, ``ycsb`` against ``PostgreSQL`` only).
Extending to another workload means adding its own argv-builder module and a
dispatch branch in :func:`build_argv`, not changing the resolution logic here.

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
    "CATALOG_CONTRACT_VERSION",
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
    "resolve_system_definition",
    "resolve_system",
    "DEFAULT_ARG_STYLE",
    "effective_post_load",
    "validate_experiment",
    "validate_environment",
    "build_argv",
    "entry_script_for_workload",
    "build_command",
    "translate",
]

#: Bump whenever experiment_schema/catalog_concepts/workloads/systems shape
#: changes -- must equal contracts/contract_catalog.yml's catalog_contract_version
#: (see tests/test_naming_conformance.py).
CATALOG_CONTRACT_VERSION = "1.4.0"

#: Names a ``derive:`` expression is allowed to reference.
DERIVE_INPUTS = ("memory_limit", "cpu_limit", "storage_class", "scaling_factor")

#: Kubernetes-style memory quantity unit suffixes, longest first so "Ki" is
#: tried before the decimal "K" would otherwise wrongly match its prefix.
_MEMORY_UNITS: tuple[tuple[str, int], ...] = (
    ("Ki", 1024), ("Mi", 1024 ** 2), ("Gi", 1024 ** 3), ("Ti", 1024 ** 4),
    ("K", 1000), ("M", 1000 ** 2), ("G", 1000 ** 3), ("T", 1000 ** 4),
)

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

#: Fallback ``arg_style`` for a knob/system that doesn't declare one.
DEFAULT_ARG_STYLE = "pg-guc"
_KNOB_TYPE_MEMORY = "memory"


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
    memory_formatter: Callable[[int], Any] = str,
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
    :param memory_formatter: Formats a derived byte count for a
        ``type: memory`` knob into the value the target system actually
        expects (e.g. a PostgreSQL-style ``"20480MB"`` GUC string). Callers
        translating for a specific system pass its own formatter; defaults
        to a plain byte-count string when none is given.
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
                values[knob_name] = memory_formatter(int(raw_value))
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
            arg_style=knob_meta.get("arg_style", definition.get("arg_style", DEFAULT_ARG_STYLE)),
            env_var=knob_meta.get("env_var"),
        )
    return resolved


def effective_post_load(system_spec: dict[str, Any], shared_post_load: dict[str, Any]) -> dict[str, Any]:
    """Resolve the post_load dict that actually applies to one ``systems:`` entry.

    A system's own ``post_load:`` is a *selection* override — legal even when
    the system fully supports the shared default — that lets one experiment
    apply post-load steps to some named systems and not others. Omitting it
    falls back to the shared ``loading.post_load`` default, so today's
    single-block experiment.yml files keep resolving exactly as before. See
    "Validation ordering" in ``docs/Design-Catalog-Contract.md``.

    :param system_spec: One entry of experiment.yml's ``systems:`` list.
    :param shared_post_load: The top-level ``loading.post_load`` default.
    :return: The post_load dict this system actually resolves to.
    :rtype: dict[str, Any]
    """
    return system_spec.get("post_load", shared_post_load)


def validate_experiment(catalog: dict[str, Any], experiment: dict[str, Any]) -> None:
    """Validate an experiment spec against the catalog before translation.

    Checks, in order: every field in :data:`_REQUIRED_HEADER_FIELDS` is
    present and non-empty (``title``, ``hypothesis``, ``discriminates`` — an
    experiment.yml must state what it's testing and which factor it isolates
    before anything else is resolved); the optional ``follow_up_of``, if
    present, is a string; the optional ``max_sut``/``max_sut_experiment``
    concurrent-SUT caps, if present, are non-negative integers (0 = no
    limit); the workload exists; every named
    system is in the workload's ``supports:`` list; and, for each system's
    *effective* post_load (its own ``systems[].post_load`` override — a
    selection choice — or else the shared ``loading.post_load`` default),
    that every option is a legal workload parameter (legality) and that the
    system's ``physical_design`` actually supports the requested value
    (support). See "Validation ordering" in ``docs/Design-Catalog-Contract.md``.

    :param catalog: Parsed catalog.
    :param experiment: Parsed experiment spec.
    :raises SpecError: On any validation failure.
    """
    for field_name in _REQUIRED_HEADER_FIELDS:
        if not experiment.get(field_name):
            raise SpecError(f"experiment.yml is missing required header field '{field_name}'")
    if not isinstance(experiment["discriminates"], list):
        raise SpecError("'discriminates' must be a list of factor names")
    follow_up_of = experiment.get("follow_up_of")
    if follow_up_of is not None and not isinstance(follow_up_of, str):
        raise SpecError("'follow_up_of' must be a string (a prior run's experiment_code)")

    for cap_field in ("max_sut", "max_sut_experiment"):
        cap = experiment.get(cap_field)
        if cap is not None and (isinstance(cap, bool) or not isinstance(cap, int) or cap < 0):
            raise SpecError(f"'{cap_field}' must be a non-negative integer (0 = no limit)")

    workload_name = experiment["workload"]["name"]
    workloads = catalog.get("workloads", {})
    if workload_name not in workloads:
        raise SpecError(f"unknown workload '{workload_name}'")
    workload = workloads[workload_name]

    system_specs = experiment.get("systems", [])
    supported = workload.get("supports", [])
    for system_spec in system_specs:
        if system_spec["name"] not in supported:
            raise SpecError(f"workload '{workload_name}' does not support system '{system_spec['name']}'")

    shared_post_load = experiment.get("loading", {}).get("post_load", {})
    catalog_post_load = workload.get("loading", {}).get("post_load", {})
    for system_spec in system_specs:
        system_name = system_spec["name"]
        post_load = effective_post_load(system_spec, shared_post_load)
        for option_name, value in post_load.items():
            if option_name not in catalog_post_load:
                raise SpecError(f"unknown post_load option '{option_name}' for workload '{workload_name}'")
            option = catalog_post_load[option_name]
            if option.get("type") == "enum" and value not in option.get("values", []):
                raise SpecError(f"post_load.{option_name}={value!r} is not one of {option.get('values')}")
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


def build_argv(catalog: dict[str, Any], experiment: dict[str, Any]) -> list[str]:
    """Validate an experiment spec, then translate it into its workload's CLI argument vector.

    Carries no workload-specific knowledge itself: it validates
    ``experiment`` against ``catalog`` and dispatches, by
    ``experiment['workload']['name']``, to that workload's own argv builder.
    Today only ``tpch`` has one
    (:func:`bexhoma.experiments.tpch_catalog.build_tpch_argv`) — extending to
    another workload means adding its own argv-builder module and a branch
    here, not changing any resolution logic in this module.

    :param catalog: Parsed catalog.
    :param experiment: Parsed experiment spec.
    :return: Argument vector, usable as ``python <entry_script>.py`` followed by these tokens.
    :rtype: list[str]
    :raises SpecError: When ``experiment`` fails validation or resolution, or
        no argv builder exists yet for its workload.
    """
    validate_experiment(catalog, experiment)
    workload_name = experiment["workload"]["name"]
    if workload_name == "tpch":
        from bexhoma.experiments.tpch_catalog import build_tpch_argv
        return build_tpch_argv(catalog, experiment)
    if workload_name == "ycsb":
        from bexhoma.experiments.ycsb_catalog import build_ycsb_argv
        return build_ycsb_argv(catalog, experiment)
    raise SpecError(f"no argv builder implemented yet for workload '{workload_name}'")


#: Catalog-driven workload name -> the entry script its argv runs through.
_ENTRY_SCRIPT_BY_WORKLOAD = {
    "tpch": "tpch.py",
    "ycsb": "ycsb.py",
}


def entry_script_for_workload(workload_name: str) -> str:
    """Return the entry script a catalog-driven workload's argv runs through.

    :param workload_name: ``experiment['workload']['name']``.
    :return: Entry script filename (e.g. ``"ycsb.py"``); falls back to
        ``"tpch.py"`` for an unknown name so :func:`build_command` still renders.
    :rtype: str
    """
    return _ENTRY_SCRIPT_BY_WORKLOAD.get(workload_name, "tpch.py")


def build_command(argv: list[str], entry_script: str = "tpch.py") -> str:
    """Render an argument vector as a copy-pasteable shell command.

    :param argv: Argument vector, as returned by :func:`build_argv`.
    :param entry_script: Entry script to invoke — see
        :func:`entry_script_for_workload`.
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
