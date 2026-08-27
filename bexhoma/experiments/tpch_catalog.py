"""
TPC-H-specific half of the catalog-contract translator (see ``bexhoma/spec.py``).

``bexhoma/spec.py`` implements the generic catalog-contract engine (catalog
loading, ``derive:``/knob resolution, validation) and dispatches, by
``experiment['workload']['name']``, to a workload's own argv builder. This
module is that builder for the ``tpch`` workload: it knows ``tpch.py``'s own
CLI flags, PostgreSQL's memory-GUC formatting, and the TPC-H post_load
(index/constraint/statistics) indexing-script mapping — none of which belong
in the generic engine.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from typing import Any, Optional

from bexhoma import spec
from bexhoma.benchmarks.tpch import resolve_indexing_key
from bexhoma.spec import ResolvedSystem, SpecError

__all__ = [
    "format_postgres_memory",
    "resolve_physical_design_overrides",
    "build_tpch_argv",
]

#: Divisor to format a byte count as whole megabytes for a PostgreSQL memory GUC.
_BYTES_PER_MEGABYTE = 1024 ** 2

_DEFAULT_MODE = "run"
_ARG_STYLE_ENV_VAR = "env-var"
_STORAGE_FORMAT_COLUMNAR = "columnar"

#: The only env-var knob this prototype can translate — it happens to already
#: be a first-class tpch.py flag, so it needs no generic env-var CLI mapping yet.
_DUCKDB_FORCE_EXECUTION_ENV_VAR = "DUCKDB_FORCE_EXECUTION"
_DUCKDB_FORCE_EXECUTION_FLAG = "-xdfe"


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


def resolve_physical_design_overrides(catalog: dict[str, Any], experiment: dict[str, Any]) -> dict[str, str]:
    """Resolve each named system's effective post_load into an indexing-script override.

    Bridges the ``systems[].post_load`` *selection* (see
    :func:`bexhoma.spec.validate_experiment`) to bexhoma's existing
    per-configuration indexing-script override
    (:meth:`~bexhoma.configurations.base.SutConfiguration.set_experiment`), the
    mechanism ``tpch.py``'s ``-xii``/``-xic``/``-xis`` CLI flags cannot express
    per system — those stay global switches, untouched by this function.
    Intended for :mod:`experiment` (the catalog-driven dispatcher) to attach to
    the parsed ``argparse.Namespace`` as ``physical_design_overrides`` before
    calling ``tpch.run()``; never surfaced as a CLI flag itself.

    :param catalog: Parsed catalog.
    :param experiment: Parsed experiment spec.
    :return: ``{system_name: indexing_key}``, one entry per ``systems:`` entry.
    :rtype: dict[str, str]
    """
    shared_post_load = experiment.get("loading", {}).get("post_load", {})
    overrides = {}
    for system_spec in experiment.get("systems", []):
        post_load = spec.effective_post_load(system_spec, shared_post_load)
        overrides[system_spec["name"]] = resolve_indexing_key(
            indexes=bool(post_load.get("indexes")),
            constraints=bool(post_load.get("constraints")),
            statistics=bool(post_load.get("statistics")),
        )
    return overrides


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


def build_tpch_argv(catalog: dict[str, Any], experiment: dict[str, Any]) -> list[str]:
    """Translate a resolved experiment.yml into a ``tpch.py`` argument vector.

    Called by :func:`bexhoma.spec.build_argv` once it has already validated
    ``experiment`` and confirmed its workload is ``tpch`` — this function
    assumes both and does not re-validate.

    Only emits flags the spec actually sets — every flag left out falls
    back to ``tpch.py``'s own argparse default, so this never needs to
    duplicate defaults the CLI already owns.

    A ``systems[].post_load`` override (see :func:`bexhoma.spec.effective_post_load`)
    is a *selection* the catalog schema supports, but ``-xii``/``-xic``/``-xis``/
    ``-xcol`` are global CLI switches — ``tpch.py`` has no per-system scoping
    for them yet. When every named system resolves to the same effective
    post_load, that shared value is emitted exactly as before, since a global
    flag can represent it faithfully. When systems diverge, these flags are
    left unset here rather than applying one system's choice to all of
    them — :func:`resolve_physical_design_overrides` resolves the actual
    per-system selection through a different mechanism entirely
    (:meth:`~bexhoma.configurations.base.SutConfiguration.set_experiment`,
    applied by ``tpch.py``'s in-process caller, not by argv), so silently
    emitting nothing here is safe rather than lossy.

    :param catalog: Parsed catalog.
    :param experiment: Parsed, already-validated experiment spec (``workload.name == 'tpch'``).
    :return: Argument vector, usable as ``python tpch.py`` followed by these tokens.
    :rtype: list[str]
    :raises SpecError: On resolution failure.
    """
    workload_spec = experiment["workload"]
    params = workload_spec.get("params", {})
    loading = experiment.get("loading", {})
    shared_post_load = loading.get("post_load", {})
    resources = experiment.get("resources", {})
    observe = experiment.get("observe", {})
    placement = experiment.get("placement", {})
    system_specs = experiment.get("systems", [])

    effective_post_loads = [spec.effective_post_load(system_spec, shared_post_load) for system_spec in system_specs]
    post_load_diverges = any(post_load != effective_post_loads[0] for post_load in effective_post_loads[1:])
    if post_load_diverges:
        post_load = {}
    else:
        post_load = effective_post_loads[0] if effective_post_loads else shared_post_load

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
    # that cell: "{system}-{1-based cell position}". A position, not a resource
    # value -- two cells can share a memory request while differing in limit or
    # CPU, and a value-based name would collide. tpch.py iterates its cells in the
    # same order (the -rr/-lr/-rc/-lc list order this builder emits below), so
    # cell N here is cell N there and the --set operations land on the right
    # configuration (see parse_set_arg's @CONFIG scope).
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
            resolved = spec.resolve_system(catalog, system_spec, resolve_inputs, memory_formatter=format_postgres_memory)
            configuration_name = (
                f"{system_spec['name']}-{cell_index + 1}" if num_cells > 1 else ""
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
    if params.get("verbose_explain"):
        argv.append("-xve")
    if params.get("store_explain"):
        argv.append("-xse")

    _append_flag(argv, "-nlp", loading.get("pods"))
    _append_flag(argv, "-nlt", loading.get("threads"))
    _append_flag(argv, "-xnls", loading.get("split"))
    _append_flag(argv, "--loading-timeout", loading.get("timeout_minutes"))
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

    # Concurrent-SUT caps. The contract default is 1 -- one system at a time,
    # see catalog_concepts.sut_isolation -- so an absent field emits an
    # explicit "-ms 1"/"-mse 1" (tpch.py's own CLI default is "no limit").
    # A field set to 0 means "no limit": the flag is simply omitted.
    for field_name, flag in (("max_sut", "-ms"), ("max_sut_experiment", "-mse")):
        cap = experiment.get(field_name, 1)
        if cap:
            _append_flag(argv, flag, cap)

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
            if knob.arg_style == spec.DEFAULT_ARG_STYLE:
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
