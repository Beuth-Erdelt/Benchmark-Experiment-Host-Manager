"""
CLI entry point for running a bexhoma experiment from a YAML definition.

Dispatches on the YAML's own shape, since two deliberately separate schemas
exist (see ``docs/Design-Yaml-Experiment-Entry-Script.md``'s "Relation to
``bexhoma/spec.py``" section):

* **Self-specified** (``workload: tpch``, a bare string): built directly in
  Python via :mod:`bexhoma.experiments.tpch_builder` — no argv is generated, no
  subprocess is spawned, nothing is re-parsed through ``tpch.py``'s own CLI.
* **Catalog-driven** (``workload: {name: ..., params: ...}``, a dict —
  :mod:`bexhoma.spec`'s schema): resolved against ``catalog.yaml`` into the
  argument vector of that workload's own entry script (``tpch.py`` for
  ``workload.name == tpch``, ``ycsb.py`` for ``ycsb``), in-process, then run
  via that script's ``run()`` — the exact same build/dispatch logic
  ``python <script>.py <argv>`` uses. Neither path spawns a subprocess or shell.

Usage: ``bexhoma experiment experiment.yaml`` or ``python experiment.py experiment.yaml``.
For a catalog-driven file whose ``catalog.yaml`` doesn't sit alongside it, pass
``--catalog``.

Both paths always write the tiered Markdown report (``-rp``/``write_report``)
to the result folder — a YAML-driven run has no interactive human typing the
flag by hand, so it defaults on rather than silently omitting the report.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse
import os
import shutil

import yaml

from bexhoma.experiments import tpch_builder, tpch_catalog, tpch_loader
from bexhoma import spec as catalog_spec

__all__ = ["is_catalog_driven", "default_catalog_path", "entry_module_for_workload", "run_experiment_yaml"]

#: Catalog-driven workload name -> its entry-script module name. Each module
#: must expose ``build_parser()`` and ``run(args, on_experiment_built=...)``
#: (see :func:`tpch.run` / :func:`ycsb.run`).
_ENTRY_MODULE_BY_WORKLOAD = {
    "tpch": "tpch",
    "ycsb": "ycsb",
}

#: Sibling output contract to contract_catalog.yml -- not itself consulted to
#: build/validate this run, but copied alongside it so an agent reading the
#: result folder later never needs the original repo checkout to interpret it.
_CONTRACT_RESULT_FILENAME = "contract_result.yml"


def _contracts_dir() -> str:
    """
    Directory holding the repo's input/output contracts.

    :return: Absolute path to ``contracts/``, alongside this file.
    :rtype: str
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "contracts")


def _copy_catalog_provenance(result_path: str, experiment_yaml_path: str, catalog_path: str) -> None:
    """
    Copy the ``experiment.yml`` that was actually run, plus the two contracts
    that governed it, into the result folder: ``contract_catalog.yml`` (used
    to validate and translate this run) and ``contract_result.yml`` (documents
    the shape of the result folder this run produces).

    Plain byte copies, best-effort -- a missing file (e.g. a ``--catalog``
    override that doesn't exist, or an old checkout without
    ``contract_result.yml``) is silently skipped rather than aborting an
    otherwise-valid run.

    :param result_path: Experiment's result folder (the built experiment's ``.path``).
    :param experiment_yaml_path: Path to the ``experiment.yml`` file that was run.
    :param catalog_path: Path to the ``contract_catalog.yml`` actually used to
        validate/translate this run (may differ from the repo default via ``--catalog``).
    """
    if os.path.isfile(experiment_yaml_path):
        shutil.copyfile(experiment_yaml_path, os.path.join(result_path, "experiment.yml"))
    if os.path.isfile(catalog_path):
        shutil.copyfile(catalog_path, os.path.join(result_path, "contract_catalog.yml"))
    result_contract_path = os.path.join(_contracts_dir(), _CONTRACT_RESULT_FILENAME)
    if os.path.isfile(result_contract_path):
        shutil.copyfile(result_contract_path, os.path.join(result_path, _CONTRACT_RESULT_FILENAME))


def is_catalog_driven(spec: dict) -> bool:
    """
    Decide whether a parsed experiment YAML is catalog-driven or self-specified.

    The two schemas differ in exactly one telling way: a catalog-driven file's
    ``workload:`` is a mapping (``{name: tpch, params: {...}}``), while a
    self-specified file's ``workload:`` is a bare string (``tpch``).

    :param spec: Parsed YAML content.
    :return: ``True`` for a catalog-driven spec.
    :rtype: bool
    """
    return isinstance(spec.get('workload'), dict)


def default_catalog_path(experiment_yaml_path: str) -> str:
    """
    Default ``catalog.yaml`` location for a catalog-driven experiment file:
    alongside the experiment file itself.

    :param experiment_yaml_path: Path to the experiment YAML file.
    :return: Default catalog.yaml path.
    :rtype: str
    """
    return os.path.join(os.path.dirname(os.path.abspath(experiment_yaml_path)), 'catalog.yaml')


def entry_module_for_workload(workload_name: str):
    """
    Import and return the entry-script module a catalog-driven workload runs through.

    :param workload_name: ``experiment.yml``'s ``workload.name`` (e.g. ``"tpch"``).
    :return: The imported module (``tpch`` or ``ycsb``), exposing ``build_parser()``
        and ``run(args, on_experiment_built=...)``.
    :raises ValueError: When no entry script is wired up for the workload.
    """
    module_name = _ENTRY_MODULE_BY_WORKLOAD.get(workload_name)
    if module_name is None:
        raise ValueError(
            f"catalog-driven workload '{workload_name}' has no entry script wired up "
            f"(known: {sorted(_ENTRY_MODULE_BY_WORKLOAD)})"
        )
    return __import__(module_name)


def run_experiment_yaml(
    path: str,
    catalog_path: str = None,
    experiment_code: str = None,
) -> None:
    """
    Load an experiment YAML file and run it, dispatching on its schema.

    :param path: Path to the experiment YAML file.
    :param catalog_path: Path to ``catalog.yaml``; only used for catalog-driven
        files. Defaults to ``catalog.yaml`` alongside ``path``.
    :param experiment_code: Optional code assigned before a catalog-driven run.
    """
    with open(path, 'r', encoding='utf-8') as experiment_file:
        raw_spec = yaml.safe_load(experiment_file)

    if is_catalog_driven(raw_spec):
        workload_name = raw_spec['workload']['name']
        entry_module = entry_module_for_workload(workload_name)
        resolved_catalog_path = catalog_path or default_catalog_path(path)
        catalog = catalog_spec.load_catalog(resolved_catalog_path)
        argv = catalog_spec.build_argv(catalog, raw_spec)
        if experiment_code:
            argv.extend(['-e', experiment_code])
        argv.append('-rp')  # YAML-driven runs always get the tiered Markdown report
        parsed_args = entry_module.build_parser().parse_args(argv)
        if workload_name == 'tpch':
            # Per-system post_load selection (e.g. indexes on PostgreSQL, not on a
            # co-running PgDuckDB) has no CLI representation -- -xii/-xic/-xis are
            # global switches -- so it is applied in-process instead, via the same
            # per-configuration override tpch.py already uses for Citus/tenant cases.
            parsed_args.physical_design_overrides = tpch_catalog.resolve_physical_design_overrides(catalog, raw_spec)
        elif workload_name == 'ycsb':
            # ycsb.py never constrains the SUT pod's resources on its own; a
            # catalog-driven run opts in so the experiment.yml's resources: block
            # actually reaches the PostgreSQL configuration (see ycsb.run()).
            parsed_args.apply_sut_resources = 'resources' in raw_spec
        entry_module.run(
            parsed_args,
            on_experiment_built=lambda experiment: _copy_catalog_provenance(
                experiment.path, path, resolved_catalog_path
            ),
        )
    else:
        tpch_loader.validate_experiment_yaml(raw_spec)
        tpch_builder.build_experiment(raw_spec, path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a bexhoma experiment from a YAML definition.")
    parser.add_argument('file', nargs='?', default='experiment.yaml',
                         help='path to the experiment YAML file')
    parser.add_argument('-c', '--catalog', default=None,
                         help="path to catalog.yaml, for a catalog-driven experiment file "
                              "(bexhoma.spec's schema); default: catalog.yaml alongside the experiment file")
    parser.add_argument('--experiment-code', default=None,
                        help='assign a new catalog-driven run its result-folder code')
    args = parser.parse_args()
    run_experiment_yaml(args.file, args.catalog, args.experiment_code)
    exit()
