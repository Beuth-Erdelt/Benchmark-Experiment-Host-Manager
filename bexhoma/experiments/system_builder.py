"""
Build the configuration of one DBMS for one benchmark from the cluster configuration.

The entry scripts (``tpch.py``, ``hammerdb.py``, ...) used to carry one block per DBMS
that named the DBMS and set its dialect, scripts, storage and parameters. Everything
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

__all__ = ["context_of", "selected_dockers", "entry_parameters", "build_configuration"]

#: Command line options that are numbers in the descriptors' placeholders.
_INTEGER_OPTIONS = ("num_worker", "num_worker_replicas", "num_worker_shards")


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


def selected_dockers(dockers: dict, benchmark: str, dbms: list) -> list:
    """The DBMS a run of ``benchmark`` builds configurations for.

    The DBMS named by ``-dbms``, or the default set of the benchmark when there is none,
    in the order of the cluster configuration (not the order of the arguments).

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key.
    :param dbms: The ``-dbms`` list.
    :return: DBMS names.
    :rtype: list
    :raises bexhoma.system_descriptors.IncompatibleBenchmark: When a named DBMS cannot run the benchmark.
    """
    for name in dbms or []:
        descriptors.benchmark_entry(dockers, name, benchmark)
    if dbms:
        return [name for name in descriptors.compatible_dockers(dockers, benchmark) if name in dbms]
    return descriptors.default_dockers(dockers, benchmark)


def entry_parameters(dockers: dict, docker: str, benchmark: str, key: str, args) -> dict:
    """A parameter dict of the DBMS's entry for the benchmark, expanded with the command line.

    :param key: ``loading_parameters``, ``benchmarking_parameters``, ``sut_parameters`` or ``eval_parameters``.
    :return: The parameters, empty when the entry declares none.
    :rtype: dict
    """
    entry = descriptors.benchmark_entry(dockers, docker, benchmark)
    return descriptors.expand(entry.get(key) or {}, context_of(args))


def build_configuration(experiment, docker: str, benchmark: str, args,
                        reset_name: str = None, loading_parameters: dict = None):
    """Create and set up the configuration of ``docker`` for ``benchmark``.

    Takes dialect, script folder, reset scripts, storage, SUT/loading/evaluation parameters
    and the limit of parallel SUT from the DBMS's entry in the cluster configuration, and
    skips loading when ``-sl`` is given. The caller adds what the benchmark decides
    (loading and benchmarking sizes, rounds).

    :param experiment: The experiment the configuration belongs to.
    :param docker: Name of the DBMS.
    :param benchmark: Benchmark key.
    :param args: Parsed command line.
    :param reset_name: Name of the benchmarker entry the reset scripts belong to (default: all).
    :param loading_parameters: Loading parameters the benchmark adds to the DBMS's own.
    :return: The configuration, already attached to the experiment.
    :raises bexhoma.system_descriptors.IncompatibleBenchmark: When the DBMS cannot run the benchmark.
    """
    dockers = experiment.cluster.dockers
    entry = descriptors.benchmark_entry(dockers, docker, benchmark)
    context = context_of(args)
    options = {}
    if dockers[docker].get('workers', False):
        options['worker'] = context['num_worker']
    config = configurations.default(
        experiment=experiment, docker=docker, dialect=entry.get('dialect', ''), **options)
    if descriptors.base_system(dockers, docker) != docker:
        config.path_experiment_docker = descriptors.base_system(dockers, docker)
    if entry.get('reset_scripts'):
        config.set_benchmark_resetscript(list(entry['reset_scripts']), name=reset_name)
    config.set_storage(storageConfiguration=descriptors.storage_prefix(dockers, docker))
    if entry.get('sut_parameters'):
        config.set_sut_parameters(**descriptors.expand(entry['sut_parameters'], context))
    if entry.get('eval_parameters'):
        config.set_eval_parameters(**descriptors.expand(entry['eval_parameters'], context))
    if context.get('skip_loading', False):
        config.loading_deactivated = True
    loading = {**descriptors.expand(entry.get('loading_parameters') or {}, context), **(loading_parameters or {})}
    if loading:
        config.set_loading_parameters(**loading)
    if entry.get('max_sut_dbms') is not None:
        config.max_sut_dbms = entry['max_sut_dbms']
    return config
