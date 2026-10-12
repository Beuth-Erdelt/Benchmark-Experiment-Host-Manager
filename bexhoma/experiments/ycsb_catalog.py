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
its own schema. Resource sweeps (``resources.cpu``/``memory``/``storage_class``
lists) are translated exactly as for ``tpch``, through the shared helpers in
:mod:`bexhoma.experiments.tpch_catalog`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from typing import Any

from bexhoma import spec
from bexhoma.cli_args import format_metric_overrides
from bexhoma.experiments.tpch_catalog import append_resource_flags, resolve_resource_cells, resource_sweep
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
    benchmarking = experiment.get("benchmarking", {})
    resources = experiment.get("resources", {})
    observe = experiment.get("observe", {})
    placement = experiment.get("placement", {})
    system_specs = experiment.get("systems", [])

    num_cells = resource_sweep(resources)[3]
    # ycsb.py builds one configuration per loading target factor; a resource
    # sweep then clones each of them, named {configuration}-{cell} after a
    # process-wide counter, so the per-cell --set scopes below could not name them
    loading_target_factors = params.get("loading_target_factors")
    if num_cells > 1 and isinstance(loading_target_factors, list) and len(loading_target_factors) > 1:
        raise SpecError(
            "a resources sweep cannot be combined with several "
            "workload.params.loading_target_factors -- sweep one of them per experiment"
        )
    # one (system_spec, ResolvedSystem, configuration_name) triple per
    # (system, resource cell) pair, named as ycsb.py's cells will be
    resolved_cells = resolve_resource_cells(catalog, experiment)

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
    if params.get("verify_result"):
        argv.append("-tr")

    _append_flag(argv, "-nlp", loading.get("pods"))
    _append_flag(argv, "-nlt", loading.get("threads"))
    _append_flag(argv, "--loading-timeout", loading.get("timeout_minutes"))
    _append_flag(argv, "-nbp", benchmarking.get("pods"))
    _append_flag(argv, "-nbt", benchmarking.get("threads"))

    # The PostgreSQL configuration below always attaches a CHECKPOINT +
    # VACUUM ANALYZE resetscript so every benchmarking round starts from the
    # same state, but ycsb.py only actually runs it when -ar is passed --
    # there is no experiment.yml knob for this because skipping the reset
    # would only ever introduce a round-to-round confound, never a valid
    # treatment choice.
    argv.append("-ar")

    rounds = workload_spec.get("rounds")
    if rounds:
        argv.extend(["-ne", ",".join(str(clients) for clients in rounds)])
    _append_flag(argv, "-nc", workload_spec.get("repetitions"))

    # Concurrent-SUT caps. max_sut_experiment defaults to 1 -- one system at a
    # time, see catalog_concepts.sut_isolation -- so an absent field emits an
    # explicit "-mse 1" (ycsb.py's own CLI default is "no limit"). max_sut
    # has no default. A field that is absent or 0 means "no limit": the flag
    # is simply omitted.
    for field_name, flag, default in (("max_sut", "-ms", None), ("max_sut_experiment", "-mse", 1)):
        cap = experiment.get(field_name, default)
        if cap:
            _append_flag(argv, flag, cap)

    if observe.get("monitoring_sut"):
        argv.append("-m")
    if observe.get("monitoring_cluster"):
        argv.append("-mc")
    if observe.get("monitoring_app"):
        argv.append("-ma")
    _append_flag(argv, "-mm", format_metric_overrides(dict.fromkeys(observe.get("metrics") or [], True)))

    _append_flag(argv, "-rnn", placement.get("sut"))
    _append_flag(argv, "-rnl", placement.get("loading"))
    _append_flag(argv, "-rnb", placement.get("benchmarking"))

    append_resource_flags(argv, resources)

    for system_spec, resolved, configuration_name in resolved_cells:
        scope = f"@{configuration_name}" if configuration_name else ""
        for knob in resolved.knobs.values():
            if knob.arg_style == spec.DEFAULT_ARG_STYLE:
                argv.extend([
                    "--set",
                    f"deployment[{resolved.deployment}]{scope}.container[dbms].{knob.name}={knob.value}",
                ])
            else:
                raise SpecError(
                    f"system '{resolved.name}' knob '{knob.name}' has arg_style "
                    f"'{knob.arg_style}', not yet translatable to a ycsb.py CLI flag"
                )

    return argv
