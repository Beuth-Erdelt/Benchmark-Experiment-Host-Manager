"""
YCSB-specific half of the catalog-contract translator (see ``bexhoma/spec.py``).

``bexhoma/spec.py`` implements the generic catalog-contract engine (catalog
loading, ``derive:``/knob resolution, validation) and dispatches, by
``experiment['workload']['name']``, to a workload's own argv builder. This
module is that builder for the ``ycsb`` workload: it knows ``ycsb.py``'s own
CLI flags and PostgreSQL's memory-GUC formatting -- neither of which belongs
in the generic engine. Mirrors :mod:`bexhoma.experiments.tpch_catalog`.

Scope: the catalog trims ``workloads.ycsb`` to ``supports: [PostgreSQL]`` (see
``contracts/contract_catalog.yml``), so this builder only has to translate the
PostgreSQL case. It has no post_load / physical-design step -- YCSB manages
its own schema -- and no resource sweep: ``resources.cpu``/``resources.memory``
must each be a single ``{request, limit}`` dict.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from typing import Any

from bexhoma import spec
from bexhoma.experiments.tpch_catalog import format_postgres_memory
from bexhoma.spec import SpecError

__all__ = ["build_ycsb_argv"]

_DEFAULT_MODE = "run"
_ARG_STYLE_ENV_VAR = "env-var"


def _append_flag(argv: list[str], flag: str, value: Any) -> None:
    """Append ``flag value`` to ``argv``, unless ``value`` is ``None`` or empty.

    :param argv: Argument vector being built, mutated in place.
    :param flag: CLI flag, e.g. ``"-sf"``.
    :param value: Value to stringify and append; skipped when ``None`` or ``""``
        (but not when ``0``).
    """
    if value is None or value == "":
        return
    argv.extend([flag, str(value)])


def _comma(values: Any) -> str | None:
    """Render a scalar or list as a comma-separated CLI value.

    :param values: A scalar, or a list of scalars (e.g. ``[1, 2]`` ->  ``"1,2"``).
    :return: The comma-joined string, or ``None`` when ``values`` is falsy-empty.
    :rtype: str | None
    """
    if values is None or values == "" or values == []:
        return None
    if isinstance(values, (list, tuple)):
        return ",".join(str(entry) for entry in values)
    return str(values)


def _single_resource_cell(resources: dict[str, Any], key: str) -> dict[str, Any]:
    """Return the single ``{request, limit}`` dict for ``resources[key]``.

    :param resources: The experiment's ``resources:`` block.
    :param key: ``"cpu"`` or ``"memory"``.
    :return: The ``{request, limit}`` dict (``{}`` when the key is absent).
    :rtype: dict[str, Any]
    :raises SpecError: When the value is a list -- a resource sweep, which the
        ``ycsb`` argv builder does not translate yet.
    """
    cell = resources.get(key, {})
    if isinstance(cell, list):
        raise SpecError(
            f"resources.{key} is a sweep list; the ycsb workload does not support "
            f"resource sweeps yet -- use a single {{request, limit}} dict"
        )
    return cell or {}


def build_ycsb_argv(catalog: dict[str, Any], experiment: dict[str, Any]) -> list[str]:
    """Translate a resolved experiment.yml into a ``ycsb.py`` argument vector.

    Called by :func:`bexhoma.spec.build_argv` once it has already validated
    ``experiment`` and confirmed its workload is ``ycsb`` -- this function
    assumes both and does not re-validate.

    Only emits flags the spec actually sets -- every flag left out falls back
    to ``ycsb.py``'s own argparse default, so this never needs to duplicate
    defaults the CLI already owns.

    :param catalog: Parsed catalog.
    :param experiment: Parsed, already-validated experiment spec
        (``workload.name == 'ycsb'``).
    :return: Argument vector, usable as ``python ycsb.py`` followed by these tokens.
    :rtype: list[str]
    :raises SpecError: On resolution failure.
    """
    workload_spec = experiment["workload"]
    params = workload_spec.get("params", {})
    loading = experiment.get("loading", {})
    resources = experiment.get("resources", {})
    observe = experiment.get("observe", {})
    placement = experiment.get("placement", {})
    system_specs = experiment.get("systems", [])

    cpu_cell = _single_resource_cell(resources, "cpu")
    memory_cell = _single_resource_cell(resources, "memory")
    storage = resources.get("storage", {})

    argv: list[str] = [experiment.get("mode", _DEFAULT_MODE)]

    if system_specs:
        argv.append("-dbms")
        argv.extend(system_spec["name"] for system_spec in system_specs)

    _append_flag(argv, "-sf", params.get("scaling_factor"))
    _append_flag(argv, "-xop", params.get("operations_scale"))
    _append_flag(argv, "-t", params.get("timeout"))
    _append_flag(argv, "-xtb", params.get("target_base"))
    _append_flag(argv, "-xnlf", _comma(params.get("loading_target_factors")))
    _append_flag(argv, "-xnbf", _comma(params.get("benchmarking_target_factors")))
    _append_flag(argv, "-xwl", params.get("workload"))
    _append_flag(argv, "-xsbs", params.get("batchsize"))
    _append_flag(argv, "-xli", params.get("logging_interval"))
    _append_flag(argv, "-xio", params.get("insert_order"))
    _append_flag(argv, "-xmet", params.get("max_execution_time"))

    _append_flag(argv, "-nlp", loading.get("pods"))
    _append_flag(argv, "-nlt", loading.get("threads"))

    rounds = workload_spec.get("rounds")
    if rounds:
        argv.extend(["-ne", ",".join(str(clients) for clients in rounds)])
    _append_flag(argv, "-nc", workload_spec.get("repetitions"))

    # Concurrent-SUT caps. The contract default is 1 -- one system at a time,
    # see catalog_concepts.sut_isolation -- so an absent field emits an
    # explicit "-ms 1"/"-mse 1" (ycsb.py's own CLI default is "no limit").
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

    _append_flag(argv, "-rc", cpu_cell.get("request"))
    _append_flag(argv, "-lc", cpu_cell.get("limit"))
    _append_flag(argv, "-rr", memory_cell.get("request"))
    _append_flag(argv, "-lr", memory_cell.get("limit"))
    _append_flag(argv, "-rss", storage.get("size"))
    _append_flag(argv, "-rst", resources.get("storage_class"))

    resolve_inputs = {
        "memory_limit": memory_cell.get("limit"),
        "cpu_limit": cpu_cell.get("limit"),
        "storage_class": resources.get("storage_class"),
        "scaling_factor": params.get("scaling_factor"),
    }
    for system_spec in system_specs:
        resolved = spec.resolve_system(
            catalog, system_spec, resolve_inputs, memory_formatter=format_postgres_memory
        )
        for knob in resolved.knobs.values():
            if knob.arg_style == spec.DEFAULT_ARG_STYLE:
                argv.extend([
                    "--set",
                    f"deployment[{resolved.deployment}].container[dbms].{knob.name}={knob.value}",
                ])
            else:
                raise SpecError(
                    f"system '{resolved.name}' knob '{knob.name}' has arg_style "
                    f"'{knob.arg_style}', not yet translatable to a ycsb.py CLI flag"
                )

    return argv
