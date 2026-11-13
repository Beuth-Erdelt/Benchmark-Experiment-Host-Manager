"""
Building blocks for the argv builders of the catalog workloads.

:mod:`bexhoma.spec` resolves and validates an experiment spec against the
catalog and hands it to the argv builder of the workload's benchmark (see
:mod:`bexhoma.benchmarks.registry`). What a builder emits for its own
benchmark is its own business; what every builder emits the same way is here:

* the resource sweep (:func:`resource_sweep`, :func:`resolve_resource_cells`,
  :func:`append_resource_flags`),
* the DDL parameters (:func:`append_ddl_flags`),
* one ``--set`` argument (:func:`_env_set_arg`) and one flag (:func:`_append_flag`).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from typing import Any, Optional

from bexhoma import spec
from bexhoma.cli_args import format_storage_types
from bexhoma.spec import ResolvedSystem, SpecError

__all__ = [
    "format_postgres_memory",
    "resource_sweep",
    "resolve_resource_cells",
    "append_resource_flags",
    "append_ddl_flags",
]

#: Divisor to format a byte count as whole megabytes for a PostgreSQL memory GUC.
_BYTES_PER_MEGABYTE = 1024 ** 2


def _env_set_arg(resolved: Any, scope: str, knob: Any) -> str:
    """Return the ``--set`` value that writes an env-var knob into the dbms container.

    :param resolved: Resolved system (provides ``name`` and ``deployment``).
    :param scope: ``"@CONFIG"`` or ``""``.
    :param knob: Resolved knob with ``arg_style == "env-var"``.
    :return: ``deployment[NAME]@CONFIG.container[dbms].env.VAR=VALUE``.
    :rtype: str
    :raises SpecError: When the knob declares no ``env_var``.
    """
    if not knob.env_var:
        raise SpecError(
            f"system '{resolved.name}' knob '{knob.name}' has arg_style 'env-var' but no env_var")
    return f"deployment[{resolved.deployment}]{scope}.container[dbms].env.{knob.env_var}={knob.value}"


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

    Mirrors the entry scripts' own ``-rr``/``-lr``/``-rc``/``-lc`` sweep-list handling: a
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


def resource_sweep(resources: dict[str, Any]) -> tuple[list, list, list, int]:
    """Split ``resources`` into its cpu, memory and storage-class cells.

    ``resources.cpu`` / ``resources.memory`` may each be a single
    ``{request, limit}`` dict (shared by every system, no sweep) or a list of
    them, and ``resources.storage_class`` a single class or a list, ``None``
    meaning ephemeral. Lists are paired by position, a single entry is
    broadcast -- mirrors the entry scripts' ``-rr``/``-lr``/``-rc``/``-lc``/``-rst``
    comma lists (:func:`bexhoma.cli_args.resource_cells`) one for one.

    :param resources: The experiment's ``resources:`` block.
    :return: ``(cpu_cells, memory_cells, storage_class_cells, num_cells)``.
    :rtype: tuple[list, list, list, int]
    :raises SpecError: When two lists with several entries differ in length.
    """
    cpu = resources.get("cpu", {})
    memory = resources.get("memory", {})
    cpu_cells = cpu if isinstance(cpu, list) else [cpu]
    memory_cells = memory if isinstance(memory, list) else [memory]
    storage_class_cells = spec.storage_class_cells(resources)
    num_cells = max(len(cpu_cells), len(memory_cells), len(storage_class_cells))
    if any(len(cells) not in (1, num_cells) for cells in (cpu_cells, memory_cells, storage_class_cells)):
        raise SpecError(
            "resources.cpu, resources.memory and resources.storage_class sweep lists must share "
            f"one length: got {len(cpu_cells)} cpu, {len(memory_cells)} memory and "
            f"{len(storage_class_cells)} storage_class entries"
        )
    return cpu_cells, memory_cells, storage_class_cells, num_cells


def resolve_resource_cells(
    catalog: dict[str, Any], experiment: dict[str, Any],
) -> list[tuple[dict[str, Any], ResolvedSystem, str]]:
    """Resolve every system once per resource cell.

    :param catalog: Parsed catalog.
    :param experiment: Parsed experiment spec.
    :return: One ``(system_spec, ResolvedSystem, configuration_name)`` triple
        per (system, cell) pair. ``configuration_name`` is ``""`` (unscoped)
        when there is only one cell, otherwise the name
        :meth:`~bexhoma.experiments.base.ExperimentBase.expand_resource_cells`
        gives that cell: ``"{system}-{1-based cell position}"``. A position,
        not a resource value -- two cells can share a memory request while
        differing in limit or CPU, and a value-based name would collide. The
        entry scripts expand their cells in the same order (the comma-list
        order :func:`append_resource_flags` emits), so cell N here is cell N
        there and scoped ``--set`` operations land on the right configuration
        (see ``parse_set_arg``'s ``@CONFIG`` scope).
    :rtype: list[tuple[dict, ResolvedSystem, str]]
    :raises SpecError: On resolution failure, e.g. a cell a profile's
        ``requires:`` does not allow.
    """
    cpu_cells, memory_cells, storage_class_cells, num_cells = resource_sweep(experiment.get("resources", {}))
    scaling_factor = experiment["workload"].get("params", {}).get("scaling_factor")
    resolved_cells = []
    for system_spec in experiment.get("systems", []):
        for cell_index in range(num_cells):
            resolve_inputs = {
                "memory_limit": _resource_cell(memory_cells, cell_index).get("limit"),
                "cpu_limit": _resource_cell(cpu_cells, cell_index).get("limit"),
                "storage_class": _resource_cell(storage_class_cells, cell_index),
                "scaling_factor": scaling_factor,
            }
            resolved = spec.resolve_system(catalog, system_spec, resolve_inputs, memory_formatter=format_postgres_memory)
            configuration_name = f"{system_spec['name']}-{cell_index + 1}" if num_cells > 1 else ""
            resolved_cells.append((system_spec, resolved, configuration_name))
    return resolved_cells


def append_resource_flags(argv: list[str], resources: dict[str, Any]) -> None:
    """Append ``-rc/-lc/-rr/-lr/-rss/-rst/-rsr/-rsrp`` for ``resources``, as comma lists when swept.

    ``-rst`` is emitted from ``resources`` itself, never from a profile's
    ``requires:`` -- otherwise a class asked for without such a profile would
    silently run on ephemeral storage. A storage-class list becomes ``-rst``'s
    comma list, ephemeral cells as empty entries.

    :param argv: Argument vector being built, mutated in place.
    :param resources: The experiment's ``resources:`` block.
    """
    cpu_cells, memory_cells, storage_class_cells, num_cells = resource_sweep(resources)
    _append_flag(argv, "-rc", _join_cell_values(cpu_cells, num_cells, "request"))
    _append_flag(argv, "-lc", _join_cell_values(cpu_cells, num_cells, "limit"))
    _append_flag(argv, "-rr", _join_cell_values(memory_cells, num_cells, "request"))
    _append_flag(argv, "-lr", _join_cell_values(memory_cells, num_cells, "limit"))
    _append_flag(argv, "-rss", resources.get("storage", {}).get("size"))
    if len(storage_class_cells) > 1:
        _append_flag(argv, "-rst", format_storage_types(storage_class_cells))
    else:
        _append_flag(argv, "-rst", storage_class_cells[0])
    if spec.removes_existing_storage(resources):
        argv.append("-rsr")
    if spec.removes_storage_per_repetition(resources):
        argv.append("-rsrp")


def append_ddl_flags(argv: list[str], experiment: dict[str, Any]) -> None:
    """Append one ``-xddl KEY=V1,V2`` per DDL parameter the systems select.

    Shared by every workload's argv builder: ``-xddl`` is generic in the entry
    scripts (:mod:`bexhoma.ddl_parameters`), a comma list sweeps the key.
    :func:`bexhoma.spec.validate_ddl` has checked the selection already.

    :param argv: Argument vector being built, mutated in place.
    :param experiment: Parsed, already-validated experiment spec.
    """
    for key, values in spec.ddl_selection(experiment).items():
        argv.extend(["-xddl", f"{key}={','.join(str(value) for value in values)}"])
