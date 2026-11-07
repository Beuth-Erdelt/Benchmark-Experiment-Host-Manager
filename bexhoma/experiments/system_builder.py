"""
Build the configuration of one DBMS for one benchmark from the cluster configuration.

The entry scripts (``tpch.py``, ``hammerdb.py``, ...) used to carry one block per DBMS
that named the DBMS and set its scripts, storage and parameters. Everything
specific to a DBMS now lives in the ``dockers:`` section of ``cluster.config``
(:mod:`bexhoma.system_descriptors`); a script loops over :func:`selected_dockers` and
calls :func:`build_configuration` for each, adding only what depends on the benchmark
(thread counts, rounds).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import configurations
from bexhoma import system_descriptors as descriptors

__all__ = ["context_of", "selected_dockers", "entry_of", "set_loading_template", "entry_parameters", "limit_loading_pods", "loading_variants",
           "pooling_variants", "apply_sut_attributes", "tenant_ids", "tenancy_error", "loading_layouts", "build_configuration"]

#: Command line options that are numbers in the descriptors' placeholders.
_INTEGER_OPTIONS = ("num_worker", "num_worker_replicas", "num_worker_shards", "num_sut_replicas", "num_pd_nodes")


def context_of(args) -> dict:
    """The command line as the context of the descriptors' ``{placeholders}``.

    :param args: Parsed command line (``argparse.Namespace``).
    :return: ``vars(args)``, with the worker counts as integers.
    :rtype: dict
    """
    context = dict(vars(args))
    for name in _INTEGER_OPTIONS:
        if name in context:
            context[name] = int(context[name])
    return context


def _context(args, context: dict = None) -> dict:
    """The command line (:func:`context_of`) with the values a benchmark adds (they win)."""
    return {**context_of(args), **(context or {})}


def _tenancy(args) -> tuple:
    """``(-mtn, -mtb)`` of the command line, ``(0, '')`` when it has no tenancy options."""
    return getattr(args, 'multi_tenant_num', 0) or 0, getattr(args, 'multi_tenant_by', '') or ''


def _selection(dockers: dict, benchmark: str, dbms: list) -> list:
    """The ``-dbms`` list in the order of the cluster configuration, or the default set without one."""
    if dbms:
        return [name for name in descriptors.compatible_dockers(dockers, benchmark) if name in dbms]
    return descriptors.default_dockers(dockers, benchmark)


def tenancy_error(benchmark: str, args, clusterconfig: str = 'cluster.config') -> str:
    """Why the command line asks for a tenancy that its DBMS do not support, or ``''``.

    For the entry scripts to refuse right after parsing, before a cluster object exists: it reads
    the cluster configuration file, as the parsers do for ``-dbms`` (see
    :func:`~bexhoma.system_descriptors.load_dockers`).

    :param benchmark: Benchmark key.
    :param args: The parsed command line.
    :param clusterconfig: Path of the cluster configuration.
    :return: The message for ``parser.error``, ``''`` when the run is fine.
    :rtype: str
    """
    dockers = descriptors.load_dockers(clusterconfig)
    return descriptors.unsupported_tenancy(
        dockers, benchmark, _selection(dockers, benchmark, list(getattr(args, 'dbms', None) or [])), *_tenancy(args))


def selected_dockers(dockers: dict, benchmark: str, dbms: list, args=None) -> list:
    """The DBMS a run of ``benchmark`` builds configurations for.

    The DBMS named by ``-dbms``, or the default set of the benchmark when there is none,
    in the order of the cluster configuration (not the order of the arguments).

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key.
    :param dbms: The ``-dbms`` list.
    :param args: The parsed command line; with it, a multi-tenant run (``-mtn``) is refused for a DBMS that
        does not support the requested ``-mtb`` mode.
    :return: DBMS names.
    :rtype: list
    :raises bexhoma.system_descriptors.IncompatibleBenchmark: When a named DBMS cannot run the benchmark,
        or cannot run it multi-tenant.
    """
    # a named DBMS that cannot run the benchmark is an error, not silently left out
    for name in dbms or []:
        descriptors.benchmark_entry(dockers, name, benchmark)
    selected = _selection(dockers, benchmark, dbms)
    if args is not None:
        reason = descriptors.unsupported_tenancy(dockers, benchmark, selected, *_tenancy(args))
        if reason:
            raise descriptors.IncompatibleBenchmark(reason)
    return selected


def entry_of(dockers: dict, docker: str, benchmark: str, args, context: dict = None) -> dict:
    """The entry of the DBMS for the benchmark with the ``variants`` applied that the command line selects.

    :param context: Values the benchmark adds to the command line.
    :return: The entry (see :func:`~bexhoma.system_descriptors.effective_entry`).
    :rtype: dict
    :raises bexhoma.system_descriptors.IncompatibleBenchmark: When the DBMS cannot run the benchmark.
    """
    return descriptors.effective_entry(descriptors.benchmark_entry(dockers, docker, benchmark), _context(args, context))


def entry_parameters(dockers: dict, docker: str, benchmark: str, key: str, args, context: dict = None) -> dict:
    """A parameter dict of the DBMS's entry for the benchmark, expanded with the command line.

    :param key: ``loading_parameters``, ``benchmarking_parameters``, ``sut_parameters`` or ``eval_parameters``.
    :param context: Values the benchmark adds to the command line for the ``{placeholders}``.
    :return: The parameters, empty when the entry declares none.
    :rtype: dict
    """
    entry = entry_of(dockers, docker, benchmark, args, context)
    return _without_none(descriptors.expand(entry.get(key) or {}, _context(args, context)))


def set_loading_template(config, entry: dict, docker: str, benchmark: str) -> None:
    """Give the configuration the loading job of its DBMS, and refuse a DBMS that has none.

    The job is the ``loading_template`` of the DBMS's entry. There is no default: a benchmark whose
    experiment brings a loading job of its own (HammerDB, Benchbase, YCSB) needs no entry, every
    other needs one for each DBMS that loads. Nothing is needed when loading is off (``-sl``, ``start``).

    :param config: The configuration.
    :param entry: The DBMS's entry for the benchmark.
    :param docker: Name of the DBMS.
    :param benchmark: Benchmark key.
    :raises bexhoma.system_descriptors.IncompatibleBenchmark: When loading is on and no job can be found.
    """
    if entry.get('loading_template'):
        config.jobtemplate_loading = entry['loading_template']
    elif (config.experiment.loading_is_active() and not config.loading_deactivated
            and not config.experiment.jobtemplate_loading):
        raise descriptors.IncompatibleBenchmark(
            f"{docker} declares no loading_template for benchmark {benchmark!r}, and the benchmark has no loading job "
            f"of its own (add loading_template to dockers.{docker}.benchmarks.{benchmark} in cluster.config)")


def _without_none(parameters: dict) -> dict:
    """``parameters`` without the values a selector left out (``None``)."""
    return {key: value for key, value in parameters.items() if value is not None}


def apply_sut_attributes(config, attributes: dict, context: dict) -> None:
    """Set up the SUT of ``config`` as the ``sut_attributes`` of its DBMS say.

    :param config: The configuration.
    :param attributes: ``sut_attributes`` of the DBMS in the cluster configuration.
    :param context: Values for the ``{placeholders}``.
    :raises ValueError: On a key that is neither a setter, ``statefulsets`` nor a known attribute
        (see :data:`~bexhoma.system_descriptors.SUT_ATTRIBUTES`).
    """
    for key, value in descriptors.expand(attributes, context).items():
        if key == descriptors.SUT_STATEFULSETS:
            # stateful sets that something else manages (e.g. Helm): record their pods
            config.deployment_infos['statefulset'] = {
                name: {'name': name, 'pods': [f"{name}-{i}" for i in range(pods)], 'containers': []}
                for name, pods in value.items()}
        elif key in descriptors.SUT_SETTERS:
            setter = getattr(config, descriptors.SUT_SETTERS[key])
            if isinstance(value, dict):
                setter(**value)
            else:
                setter(value)
        elif key in descriptors.SUT_ATTRIBUTES:
            setattr(config, key, value)
        else:
            # a typo would otherwise become a new attribute that nothing reads
            raise ValueError(f"unknown key {key!r} in sut_attributes of {config.docker}")


def tenant_ids(experiment, entry: dict) -> list:
    """The tenants a DBMS gets a configuration for.

    A DBMS that supports multi-tenancy (``multi_tenancy`` in its entry) gets one configuration per
    tenant for container-tenancy; every other DBMS, and every other kind of tenancy, one
    configuration without a tenant id.

    :param experiment: The experiment (``tenant_per``, ``num_tenants``).
    :param entry: The DBMS's entry for the benchmark.
    :return: The tenant ids, or ``[None]``.
    :rtype: list
    """
    if entry.get('multi_tenancy') and experiment.tenant_per == 'container':
        return list(range(experiment.num_tenants))
    return [None]


def pooling_variants(entry: dict, pods: list, connections_in: list, connections_out: list) -> list:
    """The settings of the configurations to build for a DBMS behind a connection pooler.

    A DBMS whose entry declares ``pooling`` gets one configuration per combination of pooler pods,
    inbound and outbound connections; every other DBMS one without extra settings.

    :param entry: The DBMS's entry for the benchmark.
    :param pods: Numbers of pooler pods (``-xnpp``).
    :param connections_in: Max inbound connections per pooler pod (``-xnpi``).
    :param connections_out: Max outbound connections per pooler pod (``-xnpo``).
    :return: A list of dicts with ``sut_parameters`` and ``resources`` (or ``[{}]``).
    :rtype: list
    """
    declared = entry.get('pooling')
    if not declared:
        return [{}]
    return [descriptors.expand(declared, {'pool_pods': count_pods, 'pool_in': int(count_in), 'pool_out': int(count_out)})
            for count_pods in pods for count_in in connections_in for count_out in connections_out]


def limit_loading_pods(entry: dict, docker: str, total: int, parallel: int) -> tuple:
    """The loading pods a DBMS tolerates: ``max_loading_pods`` of its entry caps the requested ones.

    :param entry: The DBMS's entry for the benchmark.
    :param docker: Name of the DBMS (for the message).
    :param total: Requested number of loading pods (``-nlp``).
    :param parallel: Requested number of pods in parallel.
    :return: ``(total, parallel)``.
    :rtype: tuple
    """
    limit = entry.get('max_loading_pods')
    if limit is None or (total <= limit and parallel <= limit):
        return total, parallel
    if total > limit:
        print('%s: loads with %d pod, ignoring -nlp %s' % (docker, limit, total))
    return min(total, limit), min(parallel, limit)


def loading_variants(entry: dict, threads: list) -> list:
    """The loading parameters of the configurations to build for a DBMS: one set, or one per ``-nlt`` value.

    A DBMS whose entry declares ``per_loading_threads`` gets a configuration per thread count
    (``{threads}`` is that count); every other DBMS gets one without extra parameters.

    :param entry: The DBMS's entry for the benchmark.
    :param threads: The values of ``-nlt``.
    :return: A list of parameter dicts.
    :rtype: list
    """
    declared = entry.get('per_loading_threads')
    if not declared:
        return [{}]
    return [descriptors.expand(declared, {'threads': int(count)}) for count in threads]


def loading_layouts(dockers: dict, benchmark: str, args, splits: list, pods: list, threads: list):
    """The ways to load each selected DBMS, for the scripts that load with parallel pods (TPC-H, TPC-DS, SSB).

    One layout per split of ``-nls``, number of pods of ``-nlp`` (a split larger than the number of
    pods is skipped), DBMS of :func:`selected_dockers` and set of :func:`loading_variants`, with the
    pods capped by :func:`limit_loading_pods`.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key.
    :param args: Parsed command line (``-dbms``, tenancy).
    :param splits: Values of ``-nls``: into how many parts the pods are split (pods in parallel = pods // split).
    :param pods: Values of ``-nlp``.
    :param threads: Values of ``-nlt``.
    :return: ``(docker, entry, pods_total, pods_parallel, loading_parameters)`` per layout; ``loading_parameters``
        holds ``PODS_TOTAL``, ``PODS_PARALLEL`` and the thread variant's parameters.
    :rtype: generator
    """
    for split in splits:
        for total in pods:
            if total < split:
                continue
            for docker in selected_dockers(dockers, benchmark, args.dbms, args):
                entry = descriptors.benchmark_entry(dockers, docker, benchmark)
                pods_total, pods_parallel = limit_loading_pods(entry, docker, total, int(total / split))
                for thread_parameters in loading_variants(entry, threads):
                    yield docker, entry, pods_total, pods_parallel, {
                        'PODS_TOTAL': str(pods_total), 'PODS_PARALLEL': str(pods_parallel), **thread_parameters}


def build_configuration(experiment, docker: str, benchmark: str, args,
                        reset_name: str = None, loading_parameters: dict = None,
                        storage_configuration: str = None, context: dict = None, pooling: dict = None):
    """Create and set up the configuration of ``docker`` for ``benchmark``.

    Takes script folder, reset scripts, storage, SUT/loading/evaluation parameters,
    the scripts an option switches to and the limit of parallel SUT from the DBMS's entry
    in the cluster configuration, and skips loading when ``-sl`` is given. The caller adds what
    the benchmark decides (loading and benchmarking sizes, rounds).

    :param experiment: The experiment the configuration belongs to.
    :param docker: Name of the DBMS.
    :param benchmark: Benchmark key.
    :param args: Parsed command line.
    :param reset_name: Name of the benchmarker entry the reset scripts belong to (default: all).
    :param loading_parameters: Loading parameters the benchmark adds to the DBMS's own.
    :param storage_configuration: Name of the storage if it is not the DBMS's ``storage_prefix``.
    :param context: Values the benchmark adds to the command line for the descriptors' ``{placeholders}``
        (e.g. the suffix of the reset script of the schema variant).
    :param pooling: One of :func:`pooling_variants`: SUT parameters and resources of the connection pooler.
    :return: The configuration, already attached to the experiment.
    :raises bexhoma.system_descriptors.IncompatibleBenchmark: When the DBMS cannot run the benchmark.
    """
    dockers = experiment.cluster.dockers
    context = _context(args, context)
    entry = descriptors.effective_entry(descriptors.benchmark_entry(dockers, docker, benchmark), context)
    # a variant may build the configuration from another docker entry (a cluster mode), keeping the DBMS's scripts
    config_docker = entry.get('docker', docker)
    # worker pods: an expression of the entry, else -nw for a DBMS that takes workers
    options = {}
    if entry.get('worker_count'):
        options['worker'] = descriptors.evaluate(entry['worker_count'], context)
    elif dockers[docker].get('workers', False):
        options['worker'] = context['num_worker']
    config = configurations.default(
        experiment=experiment, docker=config_docker, **options)
    if descriptors.base_system(dockers, docker) != config_docker:
        config.path_experiment_docker = descriptors.base_system(dockers, docker)
    if entry.get('sut_template'):
        config.sut_template = entry['sut_template']
    # how the SUT is set up: the DBMS's attributes, a selected variant's on top
    attributes ={**(dockers[docker].get('sut_attributes') or {}), **(entry.get('sut_attributes') or {})}
    if attributes:
        apply_sut_attributes(config, attributes, context)
    if pooling:
        config.set_sut_parameters(**pooling['sut_parameters'])
        config.set_resources(**pooling['resources'])
    reset_scripts = descriptors.expand(entry.get('reset_scripts'), context)
    if reset_scripts:
        config.set_benchmark_resetscript(list(reset_scripts), name=reset_name)
    config.set_storage(storageConfiguration=storage_configuration or entry.get('storage_prefix')
                       or descriptors.storage_prefix(dockers, docker))
    # SUT environment: boolean options as 'true'/'false' first, so that a declared value wins
    sut_parameters = {env_name: str(context.get(option, False)).lower()
                      for env_name, option in (entry.get('option_parameters') or {}).items()}
    sut_parameters.update(_without_none(descriptors.expand(entry.get('sut_parameters') or {}, context)))
    if sut_parameters:
        config.set_sut_parameters(**sut_parameters)
    if entry.get('eval_parameters'):
        config.set_eval_parameters(**_without_none(descriptors.expand(entry['eval_parameters'], context)))
    for option, scripts in (entry.get('option_experiment') or {}).items():
        if context.get(option, False):
            config.set_experiment(**scripts)
    if context.get('skip_loading', False):
        config.loading_deactivated = True
    set_loading_template(config, entry, docker, benchmark)
    # loading environment: the DBMS's, the benchmark's on top
    loading ={**_without_none(descriptors.expand(entry.get('loading_parameters') or {}, context)), **(loading_parameters or {})}
    if loading:
        config.set_loading_parameters(**loading)
    if entry.get('max_sut_dbms') is not None:
        config.max_sut_dbms = entry['max_sut_dbms']
    return config
