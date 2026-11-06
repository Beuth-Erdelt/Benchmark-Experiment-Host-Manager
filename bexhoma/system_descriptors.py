"""
Per-DBMS, per-benchmark descriptors of the ``dockers:`` section of ``cluster.config``.

Everything that is specific to a DBMS lives in the cluster configuration, not in
Python. A DBMS (``dockers.<name>``) declares the benchmarks it can run in a
``benchmarks`` dict, one key per benchmark (the keys of ``volumes``). **A missing
key means the DBMS is not compatible with that benchmark.** Each entry holds what
the entry script of that benchmark needs to configure the DBMS:

``default``
    ``True`` when the DBMS runs if ``-dbms`` is not given (absent: ``False``).
``dialect``
    SQL dialect string forwarded to DBMSBenchmarker (absent: none).
``loading_template``
    Name of the loading job template in ``k8s/`` (absent: the benchmark's own default).
``dimensions``
    ``True`` when ``-xdim`` (placement of the dimension tables of a star or snowflake
    schema on a multi-node DBMS) applies to this DBMS: its ``distributed`` variant has
    scripts in the subfolder ``distributed`` of the script folder (absent: ``False``).
``unsupported_dimensions``
    ``{variant: reason}`` of the ``-xdim`` variants the DBMS refuses for this benchmark.
``notes``
    Lines for the workload info of the experiment: ``[{'text': ..., 'when': ...}]``. ``text`` is
    formatted with the command line arguments (``{num_pd_nodes}``). ``when`` is ``selected``
    (the DBMS is in ``-dbms``, or ``-dbms`` is not given) or the name of a boolean argument
    that has to be set; without ``when`` the line is always shown.
``refresh_template``
    Name of the job template in ``k8s/`` that runs the TPC-H refresh stream against this DBMS.
``max_loading_pods``
    Number of loading pods the DBMS tolerates (e.g. ``1`` when parallel loads lose rows).
``sut_parameters``
    Environment of the SUT container that the benchmark needs by default; a value the
    experiment sets itself wins.
``option_parameters``
    ``{ENV_NAME: option}``: environment of the SUT container taken from an option of the
    experiment (a boolean becomes ``true``/``false``); an explicit value wins.
``reset_scripts``
    Scripts run on the SUT before each benchmarking round (with ``-ar``), in this order.
``loading_parameters`` / ``benchmarking_parameters`` / ``eval_parameters``
    Environment of the loading and benchmarking jobs, and evaluation parameters, that the
    benchmark needs for this DBMS (e.g. the driver type). Values are expanded with the
    command line (:func:`expand`).
``max_sut_dbms``
    Number of SUT of this DBMS that may run at the same time.
``experiment_yaml``
    ``True`` when a declarative ``experiment.yaml`` may name this DBMS for the benchmark:
    the builder makes one configuration of it, without workers or tenants.

A DBMS may also declare ``base_system``: the DBMS whose script folder
(``experiments/<benchmark>/<base_system>``) it reuses when that is not its own, and
``storage_prefix``: the name of its storage (volume), the same for every benchmark, and
``workers``: ``True`` when the SUT takes ``-nw`` workers (shards) next to its coordinator.
Its alias in the reports is one per DBMS, ``template.alias`` of its entry, whatever the
benchmark (:func:`alias`).

The functions take the ``dockers`` dict (``cluster.dockers``), so they work
without a live cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import os

__all__ = ["IncompatibleBenchmark", "ENTRY_KEYS", "load_dockers", "dbms_choices", "benchmark_entry", "compatible_dockers",
           "default_dockers", "dimension_dockers", "unsupported_dimension", "notes", "base_system",
           "storage_prefix", "alias", "experiment_yaml_dockers", "refresh_template", "expand",
           "validate_descriptors"]

#: Keys a benchmark entry may carry, with the type of their value.
ENTRY_KEYS = {
    'default': bool,
    'dialect': str,
    'loading_template': str,
    'dimensions': bool,
    'unsupported_dimensions': dict,
    'notes': list,
    'refresh_template': str,
    'max_loading_pods': int,
    'sut_parameters': dict,
    'option_parameters': dict,
    'experiment_yaml': bool,
    'reset_scripts': list,
    'loading_parameters': dict,
    'benchmarking_parameters': dict,
    'eval_parameters': dict,
    'max_sut_dbms': int,
}


class IncompatibleBenchmark(ValueError):
    """A DBMS was asked to run a benchmark it declares no entry for."""


def load_dockers(clusterconfig: str = 'cluster.config') -> dict:
    """The ``dockers`` section of the cluster configuration, for code that runs before a cluster object exists.

    Reads the same file the cluster object reads. Without a local ``cluster.config``
    it falls back to the repository's ``k8s-cluster.config`` (a run needs the local
    file anyway, but the command line can be checked without it).

    :param clusterconfig: Path of the cluster configuration.
    :return: The ``dockers`` dict.
    :rtype: dict
    """
    if not os.path.isfile(clusterconfig):
        clusterconfig = os.path.join(os.path.dirname(clusterconfig), 'k8s-cluster.config')
    with open(clusterconfig, encoding='utf-8') as file:
        return ast.literal_eval(file.read())['dockers']


def dbms_choices(benchmark: str, clusterconfig: str = 'cluster.config') -> list:
    """The values of ``-dbms`` for ``benchmark``: the DBMS that declare an entry for it.

    For the command line parsers of the entry scripts, which are built before a cluster
    object exists (see :func:`load_dockers`).
    """
    return compatible_dockers(load_dockers(clusterconfig), benchmark)


def compatible_dockers(dockers: dict, benchmark: str) -> list:
    """The DBMS that can run ``benchmark``, in the order of the configuration.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key, e.g. a key of ``volumes``.
    :return: Names of the DBMS with a ``benchmarks.<benchmark>`` entry.
    :rtype: list
    """
    return [name for name, docker in dockers.items() if benchmark in (docker.get('benchmarks') or {})]


def default_dockers(dockers: dict, benchmark: str) -> list:
    """The DBMS that run ``benchmark`` when ``-dbms`` is not given.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key.
    :return: Names of the compatible DBMS whose entry has ``default: True``.
    :rtype: list
    """
    return [name for name in compatible_dockers(dockers, benchmark)
            if dockers[name]['benchmarks'][benchmark].get('default', False)]


def dimension_dockers(dockers: dict, benchmark: str) -> list:
    """The DBMS that ``-xdim`` applies to in ``benchmark`` (entries with ``dimensions: True``)."""
    return [name for name in compatible_dockers(dockers, benchmark)
            if dockers[name]['benchmarks'][benchmark].get('dimensions', False)]


def unsupported_dimension(dockers: dict, docker: str, benchmark: str, variant: str) -> str:
    """Why ``docker`` refuses the ``-xdim`` variant in ``benchmark``, or ``''`` when it accepts it."""
    entry = ((dockers.get(docker) or {}).get('benchmarks') or {}).get(benchmark) or {}
    return (entry.get('unsupported_dimensions') or {}).get(variant, '')


def notes(dockers: dict, benchmark: str, args) -> str:
    """The workload info lines the DBMS entries of ``benchmark`` declare, for the given arguments.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key.
    :param args: The parsed command line (``-dbms`` as ``args.dbms``).
    :return: Each line with a leading newline, ``''`` when none applies.
    :rtype: str
    """
    selected = getattr(args, 'dbms', None) or []
    text = ''
    for name in compatible_dockers(dockers, benchmark):
        for note in dockers[name]['benchmarks'][benchmark].get('notes') or []:
            when = note.get('when')
            if when is None:
                applies = True
            elif when == 'selected':
                applies = not selected or name in selected
            else:
                applies = bool(getattr(args, when, False))
            if applies:
                text += '\n' + note['text'].format(**vars(args))
    return text


def benchmark_entry(dockers: dict, docker: str, benchmark: str) -> dict:
    """The entry of a DBMS for a benchmark.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param docker: Name of the DBMS.
    :param benchmark: Benchmark key.
    :return: The entry (see the module docstring).
    :rtype: dict
    :raises IncompatibleBenchmark: When the DBMS is unknown or declares no entry for the benchmark.
    """
    if docker not in dockers:
        raise IncompatibleBenchmark(f"unknown DBMS {docker!r}")
    entry = (dockers[docker].get('benchmarks') or {}).get(benchmark)
    if entry is None:
        raise IncompatibleBenchmark(
            f"{docker} is not compatible with benchmark {benchmark!r} "
            f"(compatible: {', '.join(compatible_dockers(dockers, benchmark)) or 'none'})")
    return entry


def refresh_template(dockers: dict, dbms: list, benchmark: str) -> str:
    """The job template of the refresh stream for the experiment's DBMS.

    An experiment has one refresh job for all its DBMS, so every DBMS must declare a
    ``refresh_template`` and they must agree. There is no fallback to another DBMS's job.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param dbms: The DBMS of the experiment.
    :param benchmark: Benchmark key.
    :return: The common ``refresh_template``.
    :rtype: str
    :raises IncompatibleBenchmark: When a DBMS declares none, or they declare different ones.
    """
    templates = {}
    for name in dbms:
        template = benchmark_entry(dockers, name, benchmark).get('refresh_template')
        if not template:
            have = [d for d in compatible_dockers(dockers, benchmark)
                    if dockers[d]['benchmarks'][benchmark].get('refresh_template')]
            raise IncompatibleBenchmark(
                f"{name} has no refresh job for benchmark {benchmark!r} (DBMS with one: {', '.join(have) or 'none'})")
        templates[name] = template
    if len(set(templates.values())) > 1:
        raise IncompatibleBenchmark(
            f"one refresh job serves all DBMS of an experiment, but they need different ones: "
            + ", ".join(f"{name}: {template}" for name, template in templates.items()))
    return next(iter(templates.values()))


def expand(value, context: dict):
    """Expand ``{name}`` placeholders of a descriptor value with the command line.

    A string that is exactly one placeholder (``'{num_worker}'``) becomes the value itself,
    so numbers stay numbers; other strings are formatted; dicts and lists are expanded
    recursively; everything else is returned unchanged.

    :param value: A value of a descriptor.
    :param context: Name -> value, usually ``vars(args)``.
    :raises KeyError: When a placeholder names nothing in the context.
    """
    if isinstance(value, str):
        if value.startswith('{') and value.endswith('}') and value[1:-1].isidentifier():
            return context[value[1:-1]]
        return value.format(**context) if '{' in value else value
    if isinstance(value, dict):
        return {key: expand(item, context) for key, item in value.items()}
    if isinstance(value, list):
        return [expand(item, context) for item in value]
    return value


def base_system(dockers: dict, docker: str) -> str:
    """The DBMS whose script folder ``docker`` uses: its ``base_system``, else itself."""
    return dockers[docker].get('base_system', docker)


def alias(dockers: dict, docker: str) -> str:
    """The alias of ``docker`` in the reports: ``template.alias`` of its entry, ``''`` when it has none."""
    return ((dockers.get(docker) or {}).get('template') or {}).get('alias', '')


def storage_prefix(dockers: dict, docker: str) -> str:
    """The name of the storage (volume) of ``docker``.

    :raises IncompatibleBenchmark: When the DBMS is unknown or declares no ``storage_prefix``.
    """
    if docker not in dockers:
        raise IncompatibleBenchmark(f"unknown DBMS {docker!r}")
    if not dockers[docker].get('storage_prefix'):
        raise IncompatibleBenchmark(f"{docker} declares no storage_prefix")
    return dockers[docker]['storage_prefix']


def experiment_yaml_dockers(dockers: dict, benchmark: str) -> list:
    """The DBMS a declarative ``experiment.yaml`` may name for ``benchmark`` (``experiment_yaml: True``)."""
    return [name for name in compatible_dockers(dockers, benchmark)
            if dockers[name]['benchmarks'][benchmark].get('experiment_yaml', False)]


def validate_descriptors(dockers: dict, benchmarks: set, template_folder: str = '') -> list:
    """Check the ``benchmarks`` and ``base_system`` declarations of all DBMS.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmarks: The benchmark keys that exist (the keys of ``volumes``).
    :param template_folder: Folder of the job templates (``k8s``); template names are
        only checked for existence when given.
    :return: One message per problem, empty when the descriptors are valid.
    :rtype: list
    """
    problems = []
    for name, docker in dockers.items():
        base = docker.get('base_system')
        if base is not None and base not in dockers:
            problems.append(f"{name}: base_system {base!r} is not a DBMS of dockers")
        prefix = docker.get('storage_prefix')
        if prefix is not None and (not isinstance(prefix, str) or not prefix):
            problems.append(f"{name}: storage_prefix must be a non-empty string, got {prefix!r}")
        if not isinstance(docker.get('workers', False), bool):
            problems.append(f"{name}: workers must be bool, got {docker['workers']!r}")
        if docker.get('benchmarks') and prefix is None:
            problems.append(f"{name}: has benchmarks but no storage_prefix")
        if docker.get('benchmarks') and not alias(dockers, name):
            problems.append(f"{name}: has benchmarks but no template.alias")
        for benchmark, entry in (docker.get('benchmarks') or {}).items():
            where = f"{name}.benchmarks.{benchmark}"
            if benchmark not in benchmarks:
                problems.append(f"{where}: unknown benchmark (known: {', '.join(sorted(benchmarks))})")
            if not isinstance(entry, dict):
                problems.append(f"{where}: must be a dict")
                continue
            for key, value in entry.items():
                if key not in ENTRY_KEYS:
                    problems.append(f"{where}: unknown key {key!r} (allowed: {', '.join(ENTRY_KEYS)})")
                elif not isinstance(value, ENTRY_KEYS[key]):
                    problems.append(f"{where}.{key}: must be {ENTRY_KEYS[key].__name__}, got {value!r}")
                elif ENTRY_KEYS[key] is str and not value:
                    problems.append(f"{where}.{key}: must not be empty (leave the key out)")
            for note in entry.get('notes') or []:
                if not isinstance(note, dict) or not isinstance(note.get('text'), str) or not note['text']:
                    problems.append(f"{where}.notes: every note needs a non-empty 'text'")
                elif not isinstance(note.get('when', ''), str):
                    problems.append(f"{where}.notes: 'when' must be a string")
            for key in ('loading_template', 'refresh_template'):
                template = entry.get(key)
                if template_folder and isinstance(template, str) and template \
                        and not os.path.isfile(os.path.join(template_folder, template)):
                    problems.append(f"{where}.{key}: {template} not found in {template_folder}")
    return problems
