"""
Build a running :class:`~bexhoma.experiments.tpch.TpchExperiment` straight
from a parsed ``experiment.yaml`` — no argv is ever generated, nothing is
handed to a shell.

This is the builder half of the YAML-driven experiment entry script (see
``docs/Design-Yaml-Experiment-Entry-Script.md``). It still funnels through
:meth:`~bexhoma.experiments.base.ExperimentBase.prepare_testbed`, the seam
every existing entry script (``tpch.py``, ``tpcds.py``, ...) already uses;
the dict it expects is populated here from the YAML instead of from
``argparse``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from bexhoma import clusters, configurations, experiments
from bexhoma.cli_args import resolve_scaling_factor
from bexhoma.experiments.tpch import DBMS_DEFAULTS, TpchExperiment

__all__ = ["build_experiment"]

#: k8s job-template per DBMS for the TPC-H RF1/RF2 refresh stream, mirrors tpch.py.
_REFRESH_TEMPLATES = {
    'PostgreSQL': 'jobtemplate-benchmarking-tpch-refresh-PostgreSQL.yml',
    'MySQL':      'jobtemplate-benchmarking-tpch-refresh-MySQL.yml',
    'MariaDB':    'jobtemplate-benchmarking-tpch-refresh-MariaDB.yml',
    'MonetDB':    'jobtemplate-benchmarking-tpch-refresh-MonetDB.yml',
}
_DEFAULT_REFRESH_TEMPLATE = 'jobtemplate-benchmarking-tpch-refresh-PostgreSQL.yml'

#: Provenance pointer keys and their copy target filename in the result folder.
_PROVENANCE_FILES = (('catalog', 'catalog.yaml'), ('environment', 'environment.yml'))


def _import_tpch_module():
    """
    Import the repo-root ``tpch.py`` module to reuse its real, single-sourced
    ``build_parser()`` argparse defaults.

    ``tpch.py`` lives at the repo root, not inside the ``bexhoma`` package, so
    it is only importable when the repo root is on ``sys.path`` — true when
    this process was started as ``python experiment.py`` (Python prepends the
    launched script's directory), but not guaranteed for other callers (e.g.
    a test suite run from a different working directory), hence the fallback.

    :return: The imported ``tpch`` module.
    """
    try:
        import tpch as tpch_module
    except ModuleNotFoundError:
        repo_root = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(repo_root))
        import tpch as tpch_module
    return tpch_module


def _build_cluster(cluster_spec: dict):
    """
    Construct the cluster object named by ``experiment.yaml``'s ``cluster:`` block.

    :param cluster_spec: Parsed ``cluster:`` mapping (``aws``, ``context``).
    :return: A :class:`~bexhoma.clusters.Kubernetes` or :class:`~bexhoma.clusters.AWS` instance.
    """
    context = cluster_spec.get('context')
    if cluster_spec.get('aws', False):
        return clusters.AWS(context=context)
    return clusters.Kubernetes(context=context)


def _build_prepare_testbed_parameter(spec: dict, tpch_module) -> dict:
    """
    Build the dict :meth:`~bexhoma.experiments.base.ExperimentBase.prepare_testbed` expects.

    Starts from ``tpch.py``'s own real argparse defaults (obtained by feeding
    its parser a synthetic single-element argv, never a human-typed command
    line), then overlays every YAML-set field onto its argparse **dest** name.
    One default is overridden unconditionally rather than left at ``tpch.py``'s
    own: ``write_report`` (``-rp``) is always ``True``, since a YAML-driven run
    has no interactive human available to type the flag by hand.

    :param spec: Parsed, already-validated experiment spec.
    :param tpch_module: The imported repo-root ``tpch`` module.
    :return: Parameter dict, ready for ``experiment.prepare_testbed()``.
    """
    mode = spec['mode']
    experiment_cfg = spec.get('experiment', {}) or {}
    monitoring_cfg = spec.get('monitoring', {}) or {}
    loading_cfg = spec.get('loading', {}) or {}
    tpch_cfg = spec.get('tpch', {}) or {}
    rounds = spec.get('rounds', [1])

    parameter = vars(tpch_module.build_parser().parse_args([mode]))
    parameter['write_report'] = True  # YAML-driven runs always get the tiered Markdown report
    parameter['experiment'] = experiment_cfg.get('code')
    parameter['num_config'] = experiment_cfg.get('num_config', parameter['num_config'])
    parameter['timeout'] = experiment_cfg.get('timeout', parameter['timeout'])
    parameter['scaling_factor'] = experiment_cfg.get('scaling_factor', parameter['scaling_factor'])
    parameter['num_query_executors'] = ",".join(str(round_clients) for round_clients in rounds)
    parameter['monitoring'] = monitoring_cfg.get('sut', False)
    parameter['monitoring_cluster'] = monitoring_cfg.get('cluster', False)
    parameter['monitoring_app'] = monitoring_cfg.get('app', False)
    parameter['num_loading_pods'] = ",".join(str(pods) for pods in loading_cfg.get('pods', [1]))
    parameter['num_loading_threads'] = ",".join(str(threads) for threads in loading_cfg.get('threads', [1]))
    parameter['num_loading_split'] = str(loading_cfg.get('split', 1))
    parameter['recreate_parameter'] = tpch_cfg.get('recreate_parameter', False)
    parameter['shuffle_queries'] = tpch_cfg.get('shuffle_queries', False)
    parameter['init_indexes'] = tpch_cfg.get('init_indexes', False)
    parameter['init_constraints'] = tpch_cfg.get('init_constraints', False)
    parameter['init_statistics'] = tpch_cfg.get('init_statistics', False)
    parameter['init_columns'] = tpch_cfg.get('init_columns', False)
    parameter['datatransfer'] = tpch_cfg.get('datatransfer', False)
    parameter['verbose_explain'] = tpch_cfg.get('verbose_explain', False)
    parameter['store_explain'] = tpch_cfg.get('store_explain', False)
    active_queries = tpch_cfg.get('active_queries') or []
    parameter['active_queries'] = ",".join(str(query) for query in active_queries)
    parameter['num_refresh_streams'] = tpch_cfg.get('refresh_streams', 0)
    parameter['num_refresh_stream_offset'] = tpch_cfg.get('refresh_stream_offset', 0)
    parameter['duckdb_force_execution'] = tpch_cfg.get('duckdb_force_execution', False)
    parameter['dbms'] = [system['dbms'] for system in spec['systems']]
    return parameter


def _configure_system(experiment: TpchExperiment, system: dict, duckdb_force_execution_default: bool) -> None:
    """
    Build and attach one :class:`~bexhoma.configurations.base.SutConfiguration`
    for one ``systems:`` entry, mirroring the setter sequence ``tpch.py``'s own
    per-DBMS branches call.

    Phase 1 limitation: builds exactly one configuration per system (the
    single-cell path); resource sweeps and multiple parallel loading cells,
    like ``tpch.py``'s own ``-rr``/``-lr``/``-nlp``/``-xnls`` comma-list
    sweeps, are follow-up work, same scoping as ``DBMS_DEFAULTS`` excluding
    ``Citus``/container-tenancy.

    :param experiment: The experiment these DBMS configurations are attached to.
    :param system: One entry of ``spec['systems']``.
    :param duckdb_force_execution_default: Top-level ``tpch.duckdb_force_execution``
        fallback, used for ``PgDuckDB`` systems that don't set their own
        ``sut_parameters.DUCKDB_FORCE_EXECUTION`` override.
    :raises KeyError: When ``system['dbms']`` is not a key of
        :data:`~bexhoma.experiments.tpch.DBMS_DEFAULTS` (caught earlier by
        :func:`bexhoma.experiment_loader.validate_experiment_yaml`).
    """
    dbms = system['dbms']
    defaults = DBMS_DEFAULTS[dbms]
    configuration_name = system.get('configuration', '') or ''
    alias = system.get('alias') or dbms

    config = configurations.default(
        experiment=experiment, docker=defaults['docker'], dialect=defaults['dialect'],
        configuration=configuration_name, alias=alias,
    )
    if 'path_experiment_docker' in defaults:
        config.path_experiment_docker = defaults['path_experiment_docker']

    resources = system.get('resources', {}) or {}
    cpu = resources.get('cpu', {}) or {}
    memory = resources.get('memory', {}) or {}
    config.set_resources(
        requests={'cpu': cpu.get('request', '4'), 'memory': memory.get('request', '16Gi'), 'gpu': 0},
        limits={'cpu': cpu.get('limit', '0'), 'memory': memory.get('limit', '0')},
    )

    storage_cfg = system.get('storage', {}) or {}
    storage_kwargs = {'storageConfiguration': configuration_name or defaults['storage_prefix']}
    if storage_cfg.get('class'):
        storage_kwargs['storageClassName'] = storage_cfg['class']
    if storage_cfg.get('size'):
        storage_kwargs['storageSize'] = storage_cfg['size']
    config.set_storage(**storage_kwargs)

    if system.get('skip_loading', False):
        config.loading_deactivated = True

    loading_cfg = system.get('loading', {}) or {}
    loading_pods_total = int(loading_cfg.get('pods', 1))
    loading_pods_split = int(loading_cfg.get('split', 1))
    split_portion = loading_pods_total // loading_pods_split

    config.jobtemplate_loading = defaults['jobtemplate_loading']
    config.set_loading_parameters(
        PODS_TOTAL=str(loading_pods_total),
        PODS_PARALLEL=str(split_portion),
        **(system.get('loading_parameters') or {}),
    )
    config.set_benchmarking_parameters(**(system.get('benchmarking_parameters') or {}))
    config.set_loading(parallel=split_portion, num_pods=loading_pods_total)

    sut_parameters = dict(system.get('sut_parameters') or {})
    if dbms == 'PgDuckDB' and 'DUCKDB_FORCE_EXECUTION' not in sut_parameters:
        sut_parameters['DUCKDB_FORCE_EXECUTION'] = str(duckdb_force_execution_default).lower()
    if sut_parameters:
        config.set_sut_parameters(**sut_parameters)


def _copy_provenance_files(spec: dict, spec_path: str, result_path: str) -> None:
    """
    Copy the ``experiment.yaml`` that was actually used, plus optional
    ``catalog``/``environment`` provenance pointers, into the result folder.

    Plain byte copies (never a round-tripped ``yaml.safe_dump()``) so comments
    and formatting the author wrote survive. Missing ``catalog``/``environment``
    files are silently skipped — this is best-effort provenance, not a hard
    requirement, so it must never abort an otherwise-valid run.

    :param spec: Parsed experiment spec (only its provenance-pointer keys are read).
    :param spec_path: Path to the ``experiment.yaml`` file that was loaded.
    :param result_path: Experiment's result folder (``experiment.path``).
    """
    spec_dir = os.path.dirname(os.path.abspath(spec_path))
    shutil.copyfile(spec_path, os.path.join(result_path, 'experiment.yaml'))
    for key, target_name in _PROVENANCE_FILES:
        pointer = spec.get(key)
        if not pointer:
            continue
        source = pointer if os.path.isabs(pointer) else os.path.join(spec_dir, pointer)
        if os.path.isfile(source):
            shutil.copyfile(source, os.path.join(result_path, target_name))


def build_experiment(spec: dict, spec_path: str) -> TpchExperiment:
    """
    Build a fully-configured :class:`~bexhoma.experiments.tpch.TpchExperiment`
    from an already-validated ``experiment.yaml``.

    :param spec: Parsed experiment spec, as returned by
        :func:`bexhoma.experiment_loader.load_experiment_yaml` and validated by
        :func:`bexhoma.experiment_loader.validate_experiment_yaml`.
    :param spec_path: Path to the ``experiment.yaml`` file that was loaded —
        used to resolve relative ``catalog``/``environment`` provenance
        pointers and to copy the file itself into the result folder.
    :return: The built experiment, with every ``systems:`` entry already
        attached as a :class:`~bexhoma.configurations.base.SutConfiguration`
        and :meth:`~bexhoma.experiments.base.ExperimentBase.prepare_testbed`
        already called.
    :rtype: TpchExperiment
    """
    tpch_module = _import_tpch_module()

    mode = spec['mode']
    experiment_cfg = spec.get('experiment', {}) or {}
    tpch_cfg = spec.get('tpch', {}) or {}
    cluster = _build_cluster(spec.get('cluster', {}) or {})

    code = experiment_cfg.get('code')
    if code is None:
        code = cluster.code
    SF = resolve_scaling_factor(cluster, code, mode, experiment_cfg.get('scaling_factor', 1))

    experiment = experiments.tpch(
        cluster=cluster, SF=SF, timeout=int(experiment_cfg.get('timeout', 600)),
        code=code, num_experiment_to_apply=int(experiment_cfg.get('num_config', 1)),
    )
    _copy_provenance_files(spec, spec_path, experiment.path)

    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    active_queries = tpch_cfg.get('active_queries') or None
    experiment.set_active_queries(active_queries)
    experiment.set_additional_labels(usecase="tpc-h", experiment_design="parallel-loading")
    experiment.set_default_loading_parameters(
        SF=SF, STORE_RAW_DATA=1, STORE_RAW_DATA_RECREATE=0,
        BEXHOMA_SYNCH_LOAD=1, BEXHOMA_SYNCH_GENERATE=1, TRANSFORM_RAW_DATA=1,
        TPCH_TABLE=tpch_cfg.get('limit_import_table', ''),
    )
    experiment.set_default_benchmarking_parameters(
        SF=SF,
        DBMSBENCHMARKER_RECREATE_PARAMETER=tpch_cfg.get('recreate_parameter', False),
        DBMSBENCHMARKER_SHUFFLE_QUERIES=tpch_cfg.get('shuffle_queries', False),
        DBMSBENCHMARKER_DEV=0,
        DBMSBENCHMARKER_VERBOSE_EXPLAIN=tpch_cfg.get('verbose_explain', False),
        DBMSBENCHMARKER_STORE_EXPLAIN=tpch_cfg.get('store_explain', False),
    )

    num_refresh_streams = tpch_cfg.get('refresh_streams', 0)
    if num_refresh_streams > 0:
        experiment.set_default_benchmarking_parameters(
            TPCH_REFRESH_STREAMS=num_refresh_streams,
            TPCH_REFRESH_STREAM_OFFSET=tpch_cfg.get('refresh_stream_offset', 0),
            TRANSFORM_RAW_DATA=1, STORE_RAW_DATA=1,
        )
        first_dbms = spec['systems'][0]['dbms']
        experiment.enable_refresh_stream(
            template=_REFRESH_TEMPLATES.get(first_dbms, _DEFAULT_REFRESH_TEMPLATE)
        )

    parameter = _build_prepare_testbed_parameter(spec, tpch_module)
    experiment.prepare_testbed(parameter)

    duckdb_force_execution_default = tpch_cfg.get('duckdb_force_execution', False)
    for system in spec['systems']:
        _configure_system(experiment, system, duckdb_force_execution_default)

    rounds = spec.get('rounds', [1])
    experiment.add_benchmark_list(rounds)
    experiment.process()
    return experiment
