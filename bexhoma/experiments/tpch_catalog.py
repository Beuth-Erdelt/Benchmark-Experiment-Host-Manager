"""
TPC-H-specific half of the catalog-contract translator (see ``bexhoma/spec.py``).

``bexhoma/spec.py`` implements the generic catalog-contract engine (catalog
loading, ``derive:``/knob resolution, validation) and dispatches, by
``experiment['workload']['name']``, to a workload's own argv builder. This
module is that builder for the ``tpch`` workload: it knows ``tpch.py``'s own
CLI flags and the TPC-H post_load (index/constraint/statistics)
indexing-script mapping — none of which belong in the generic engine. The
parts every argv builder shares (resource sweep, DDL parameters, ``--set``
arguments) are in :mod:`bexhoma.spec_argv`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from typing import Any, Optional

from bexhoma import spec
from bexhoma import system_descriptors as descriptors
from bexhoma.benchmarks.tpch import resolve_indexing_key
from bexhoma.cli_args import format_metric_overrides, format_storage_types
from bexhoma.spec import ResolvedSystem, SpecError
from bexhoma.spec_argv import (
    _append_flag, _env_set_arg, append_ddl_flags, append_resource_flags, format_postgres_memory,
    resolve_resource_cells, resource_sweep)

__all__ = [
    "format_postgres_memory",
    "resolve_physical_design_overrides",
    "resource_sweep",
    "resolve_resource_cells",
    "append_resource_flags",
    "append_ddl_flags",
    "build_tpch_argv",
    "option_flags",
]


_DEFAULT_MODE = "run"
_STORAGE_FORMAT_COLUMNAR = "columnar"

def option_flags(system: str) -> dict:
    """The env-var knobs of a system that are boolean options of ``tpch.py``, with their flags.

    The DBMS's ``option_parameters`` in ``dockers.<system>.benchmarks.tpch`` of the cluster
    configuration map an environment variable of the SUT to the option that sets it
    (e.g. PgDuckDB's ``DUCKDB_FORCE_EXECUTION`` to ``duckdb_force_execution``). Such a knob
    is passed as the option, so the run also knows it (workload info, evaluation); every
    other env-var knob becomes ``--set ...container[dbms].env.NAME=VALUE``. The flag is the
    long form of the option, ``--x`` and its name with dashes, as every script option is named.

    :param system: Name of the system, a key of ``dockers``.
    :return: Environment variable -> flag, empty when the system declares none.
    :rtype: dict
    """
    entry = ((descriptors.load_dockers().get(system) or {}).get('benchmarks') or {}).get('tpch') or {}
    return {env_var: '--x' + option.replace('_', '-')
            for env_var, option in (entry.get('option_parameters') or {}).items()}


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

    # one (system_spec, ResolvedSystem, configuration_name) triple per
    # (system, resource cell) pair, see resolve_resource_cells()
    resolved_cells = resolve_resource_cells(catalog, experiment)

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

    # The catalog's loading.pods default (8) differs from tpch.py's -nlp default (1),
    # so it must be emitted explicitly rather than left to argparse.
    pods_default = catalog["workloads"]["tpch"]["loading"]["pods"].get("default")
    _append_flag(argv, "-nlp", loading.get("pods", pods_default))
    _append_flag(argv, "-nlt", loading.get("threads"))
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

    # Concurrent-SUT caps. max_sut_experiment defaults to 1 -- one system at a
    # time, see catalog_concepts.sut_isolation -- so an absent field emits an
    # explicit "-mse 1" (tpch.py's own CLI default is "no limit"). max_sut
    # has no default. A field that is absent or 0 means "no limit": the flag
    # is simply omitted.
    for field_name, flag, default in (("max_sut", "-ms", None), ("max_sut_experiment", "-mse", 1)):
        cap = experiment.get(field_name, default)
        if cap:
            _append_flag(argv, flag, cap)
    # A SUT left running is of no use to an agent, and it holds its node for
    # the next experiment: stop it in every mode but start (catalog_concepts.sut_isolation)
    if argv[0] != "start":
        argv.extend(["-ks", "no"])

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
    append_ddl_flags(argv, experiment)

    for system_spec, resolved, configuration_name in resolved_cells:
        scope = f"@{configuration_name}" if configuration_name else ""
        flags = option_flags(resolved.name)
        for knob in resolved.knobs.values():
            if knob.arg_style in spec.ARG_STYLES_VIA_SET:
                argv.extend([
                    "--set",
                    f"deployment[{resolved.deployment}]{scope}.container[dbms].{knob.name}={knob.value}",
                ])
            elif knob.arg_style == spec.ARG_STYLE_ENV_VAR:
                if knob.env_var in flags:
                    # a boolean option of tpch.py: set when the knob is true
                    if knob.value:
                        argv.append(flags[knob.env_var])
                else:
                    argv.extend(["--set", _env_set_arg(resolved, scope, knob)])
            else:
                raise SpecError(
                    f"system '{resolved.name}' knob '{knob.name}' has arg_style "
                    f"'{knob.arg_style}', not yet translatable to a CLI flag"
                )

    return argv
