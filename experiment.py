"""
CLI entry point for running a bexhoma experiment from a YAML definition.

Dispatches on the YAML's own shape, since two deliberately separate schemas
exist (see ``docs/Design-Yaml-Experiment-Entry-Script.md``'s "Relation to
``bexhoma/spec.py``" section):

* **Self-specified** (``workload: tpch``, a bare string): built directly in
  Python via :mod:`bexhoma.experiment_builder` — no argv is generated, no
  subprocess is spawned, nothing is re-parsed through ``tpch.py``'s own CLI.
* **Catalog-driven** (``workload: {name: ..., params: ...}``, a dict —
  :mod:`bexhoma.spec`'s schema): resolved against ``catalog.yaml`` into a
  ``tpch.py`` argument vector, in-process, then run via :func:`tpch.run` —
  the exact same build/dispatch logic ``python tpch.py <argv>`` uses.
  Neither path spawns a subprocess or shell.

Usage: ``bexhoma experiment experiment.yaml`` or ``python experiment.py experiment.yaml``.
For a catalog-driven file whose ``catalog.yaml`` doesn't sit alongside it, pass
``--catalog``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse
import os

import yaml

from bexhoma import experiment_builder, experiment_loader
from bexhoma import spec as catalog_spec

__all__ = ["is_catalog_driven", "default_catalog_path", "run_experiment_yaml"]


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


def run_experiment_yaml(path: str, catalog_path: str = None) -> None:
    """
    Load an experiment YAML file and run it, dispatching on its schema.

    :param path: Path to the experiment YAML file.
    :param catalog_path: Path to ``catalog.yaml``; only used for catalog-driven
        files. Defaults to ``catalog.yaml`` alongside ``path``.
    """
    with open(path, 'r', encoding='utf-8') as experiment_file:
        raw_spec = yaml.safe_load(experiment_file)

    if is_catalog_driven(raw_spec):
        import tpch
        catalog = catalog_spec.load_catalog(catalog_path or default_catalog_path(path))
        argv = catalog_spec.build_argv(catalog, raw_spec)
        tpch.run(tpch.build_parser().parse_args(argv))
    else:
        experiment_loader.validate_experiment_yaml(raw_spec)
        experiment_builder.build_experiment(raw_spec, path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a bexhoma experiment from a YAML definition.")
    parser.add_argument('file', nargs='?', default='experiment.yaml',
                         help='path to the experiment YAML file')
    parser.add_argument('-c', '--catalog', default=None,
                         help="path to catalog.yaml, for a catalog-driven experiment file "
                              "(bexhoma.spec's schema); default: catalog.yaml alongside the experiment file")
    args = parser.parse_args()
    run_experiment_yaml(args.file, args.catalog)
    exit()
