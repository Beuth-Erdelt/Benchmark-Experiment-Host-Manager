"""
Per-DBMS, per-benchmark descriptors of the ``dockers:`` section of ``cluster.config``.

Everything that is specific to a DBMS lives in the cluster configuration, not in
Python. A DBMS (``dockers.<name>``) declares the benchmarks it can run in a
``benchmarks`` dict, one key per benchmark (the keys of ``volumes``). **A missing
key means the DBMS is not compatible with that benchmark.** Each entry holds what
the entry script of that benchmark needs to configure the DBMS:

``default``
    ``True`` when the DBMS runs if ``-dbms`` is not given (absent: ``False``).
``loading_template``
    Name of the loading job template in ``k8s/``. There is no default: without it, a DBMS is refused
    when loading is on, unless the benchmark brings a loading job of its own (HammerDB, Benchbase, YCSB).
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
``tenant_parameters``
    ``{'loading': {...}, 'benchmarking': {...}}``: parameters a multi-tenant run adds to the jobs;
    ``{tenant_by}``, ``{num_tenants}`` and ``{tenant_id}`` are filled in.
``pooling``
    For a DBMS behind a connection pooler: ``{'sut_parameters': ..., 'resources': ...}`` applied to one configuration
    per combination of ``-xnpp``, ``-xnpi`` and ``-xnpo``; ``{pool_pods}``, ``{pool_in}`` and ``{pool_out}`` are filled in.
``multi_tenancy``
    The tenancy modes (``-mtb``: ``container``, ``schema``, ``database``) the DBMS supports in the benchmark.
    A run with ``-mtn`` is refused for a DBMS that does not list the requested mode (:func:`unsupported_tenancy`).
``per_loading_threads``
    Loading parameters of a DBMS that gets one configuration per ``-nlt`` value; ``{threads}`` is that value.
``option_experiment``
    ``{option: {script: ..., indexing: ...}}``: init and indexing scripts the DBMS switches to when the
    boolean command line option is set (e.g. columnar storage).
``experiment_yaml``
    ``True`` when a declarative ``experiment.yaml`` may name this DBMS for the benchmark:
    the builder makes one configuration of it, without workers or tenants.
``variants``
    ``[{'when': <expression>, <entry keys>}]``: changes that depend on the command line, applied
    by :func:`effective_entry`. Besides the keys above, a variant (or the entry itself) may set
    ``docker`` (build the configuration from another ``dockers`` entry, e.g. a cluster mode),
    ``sut_template``, ``storage_prefix``, ``worker_count`` (an expression for the number of worker
    pods, e.g. ``'num_worker * (1 + num_worker_replicas)'``) and ``sut_attributes``.

A DBMS may also declare ``base_system``: the DBMS whose script folder
(``experiments/<benchmark>/<base_system>``) it reuses when that is not its own, and
``storage_prefix``: the name of its storage (volume), the same for every benchmark, and
``workers``: ``True`` when the SUT takes ``-nw`` workers (shards) next to its coordinator,
``sut_attributes``: how the SUT of the DBMS is set up, a dict of ``key: value`` applied to the configuration:
the keys of :data:`SUT_SETTERS` call the setter of that name, ``statefulsets`` (``{name: pods}``) records stateful
sets that something else manages (Helm), and the keys of :data:`SUT_ATTRIBUTES` are attributes of the
configuration; any other key is refused. Values are expanded with the command line (:func:`expand`).
Its alias in the reports (:func:`alias`) and its SQL dialect, the key of the query variants
in the query files (:func:`dialect`), are one per DBMS, ``template.alias`` and ``template.dialect``
of its entry, whatever the benchmark.

The functions take the ``dockers`` dict (``cluster.dockers``), so they work
without a live cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import operator
import os

__all__ = ["IncompatibleBenchmark", "ENTRY_KEYS", "SUT_SETTERS", "SUT_ATTRIBUTES", "SUT_STATEFULSETS","evaluate", "effective_entry", "TENANCY_MODES", "unsupported_tenancy", "load_dockers", "dbms_choices", "benchmark_entry", "compatible_dockers",
           "default_dockers", "dimension_dockers", "unsupported_dimension", "notes", "base_system",
           "storage_prefix", "alias", "dialect", "experiment_yaml_dockers", "refresh_template", "expand",
           "validate_descriptors"]

#: Keys a benchmark entry may carry, with the type of their value.
ENTRY_KEYS = {
    'default': bool,
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
    'multi_tenancy': list,
    'per_loading_threads': dict,
    'option_experiment': dict,
    'tenant_parameters': dict,
    'pooling': dict,
    'variants': list,
    'docker': str,
    'sut_template': str,
    'storage_prefix': str,
    'worker_count': str,
    'sut_attributes': dict,
}

#: Keys of ``sut_attributes`` that call a setter of the configuration (a dict is passed as keyword arguments).
SUT_SETTERS = {
    'sut_role': 'set_sut_role',
    'pvc_selector': 'set_pvc_selector',
    'script_target': 'set_script_target',
    'data_components': 'set_data_components',
    'resources': 'set_resources',
}

#: Keys of ``sut_attributes`` that are set as attributes of the configuration.
SUT_ATTRIBUTES = ('monitoring_sut', 'resource_sweep', 'statefulset_name', 'sut_container_name', 'sut_has_pool',
                  'sut_pod_name', 'sut_service_name', 'worker_metric_strip_container')

#: Key of ``sut_attributes`` that records stateful sets something else manages (``{name: pods}``).
SUT_STATEFULSETS = 'statefulsets'

#: Dict-valued entry keys whose values a variant merges into the entry's (any other key is replaced).
MERGED_KEYS = ('loading_parameters', 'benchmarking_parameters', 'sut_parameters', 'eval_parameters',
               'sut_attributes', 'tenant_parameters', 'pooling')

_ARITHMETIC = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.FloorDiv: operator.floordiv}
_COMPARISON = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt, ast.LtE: operator.le,
               ast.Gt: operator.gt, ast.GtE: operator.ge}


#: Values of ``-mtb``.
TENANCY_MODES = ('container', 'schema', 'database')


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


def unsupported_tenancy(dockers: dict, benchmark: str, dbms: list, number: int, mode: str) -> str:
    """Why a multi-tenant run cannot use these DBMS, or ``''`` when it can.

    A run with ``-mtn`` above 0 needs every selected DBMS to list the requested ``-mtb`` mode in
    ``multi_tenancy``; otherwise it would take part in the tenant machinery without tenant
    storage, parameters or scripts.

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmark: Benchmark key.
    :param dbms: The selected DBMS.
    :param number: ``-mtn``, the number of tenants (0: no tenancy).
    :param mode: ``-mtb``.
    :return: The message, ``''`` when the run is fine.
    :rtype: str
    """
    if int(number) <= 0:
        return ''
    declared = {name: list(dockers[name]['benchmarks'][benchmark].get('multi_tenancy') or [])
                for name in compatible_dockers(dockers, benchmark)}
    refused = [name for name in dbms if mode not in declared.get(name, [])]
    if not refused:
        return ''
    supporting = {name: modes for name, modes in declared.items() if modes}
    where = ('; '.join(f"{name}: {', '.join(modes)}" for name, modes in supporting.items())
             or f"no DBMS supports multi-tenancy in {benchmark}")
    return (f"-mtn {number} -mtb {mode or '(missing)'}: {', '.join(refused)} "
            f"{'does' if len(refused) == 1 else 'do'} not support this tenancy in {benchmark} (supported: {where})")


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


def evaluate(expression: str, context: dict):
    """Evaluate a small expression of the cluster configuration with the command line.

    Only numbers, strings, names of the context, ``+ - * //``, comparisons, ``and``, ``or`` and
    ``not`` are allowed (``'num_worker > 0 and num_worker_replicas > 0'``,
    ``'num_worker * (1 + num_worker_replicas)'``); anything else is refused.

    :param expression: The expression.
    :param context: Name -> value, usually :func:`~bexhoma.experiments.system_builder.context_of`.
    :raises ValueError: On a construct that is not allowed.
    :raises KeyError: When a name is not in the context.
    """
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str, bool)):
            return node.value
        if isinstance(node, ast.Name):
            return context[node.id]
        if isinstance(node, ast.BoolOp):
            values = (visit(value) for value in node.values)
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.Not, ast.USub)):
            operand = visit(node.operand)
            return (not operand) if isinstance(node.op, ast.Not) else -operand
        if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC:
            return _ARITHMETIC[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.Compare) and all(type(op) in _COMPARISON for op in node.ops):
            left = visit(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = visit(comparator)
                if not _COMPARISON[type(op)](left, right):
                    return False
                left = right
            return True
        raise ValueError(f"not allowed in an expression: {ast.dump(node)[:60]}")
    return visit(ast.parse(expression, mode='eval'))


def effective_entry(entry: dict, context: dict) -> dict:
    """The entry of a DBMS for the benchmark with the variants applied that the command line selects.

    ``variants`` is a list of ``{'when': <expression>, <entry keys>}``. Every variant whose
    ``when`` holds (see :func:`evaluate`) is applied in order: dict-valued keys
    (:data:`MERGED_KEYS`) are merged into the entry's, any other key replaces it. The key
    ``variants`` itself is not in the result.

    :param entry: The entry (see :func:`benchmark_entry`).
    :param context: Name -> value, usually :func:`~bexhoma.experiments.system_builder.context_of`.
    :return: A new dict.
    :rtype: dict
    """
    result = {key: value for key, value in entry.items() if key != 'variants'}
    for variant in entry.get('variants') or []:
        if not evaluate(variant['when'], context):
            continue
        for key, value in variant.items():
            if key == 'when':
                continue
            if key in MERGED_KEYS and isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = {**result[key], **value}
            else:
                result[key] = value
    return result


def expand(value, context: dict):
    """Expand ``{name}`` placeholders of a descriptor value with the command line.

    A string that is exactly one placeholder (``'{num_worker}'``) becomes the value itself,
    so numbers stay numbers; other strings are formatted; dicts and lists are expanded
    recursively; everything else is returned unchanged.

    A dict with the key ``'$by'`` is a selector: ``{'$by': 'benchmark', 'tpcc': A, '*': B}`` becomes
    ``A`` if ``context['benchmark']`` is ``'tpcc'``, else ``B``; without a matching key and without
    ``'*'`` it becomes ``None`` (the caller leaves the value out).

    :param value: A value of a descriptor.
    :param context: Name -> value, usually ``vars(args)``.
    :raises KeyError: When a placeholder names nothing in the context.
    """
    if isinstance(value, str):
        if value.startswith('{') and value.endswith('}') and value[1:-1].isidentifier():
            return context[value[1:-1]]
        return value.format(**context) if '{' in value else value
    if isinstance(value, dict):
        if '$by' in value:
            chosen = value.get(str(context[value['$by']]), value.get('*'))
            return None if chosen is None else expand(chosen, context)
        return {key: expand(item, context) for key, item in value.items()}
    if isinstance(value, list):
        return [expand(item, context) for item in value]
    return value


def _names_of(expression: str) -> dict:
    """Every name of the expression, as 1 (to check the expression without a command line)."""
    return {node.id: 1 for node in ast.walk(ast.parse(expression, mode='eval')) if isinstance(node, ast.Name)}


def base_system(dockers: dict, docker: str) -> str:
    """The DBMS whose script folder ``docker`` uses: its ``base_system``, else itself."""
    return dockers[docker].get('base_system', docker)


def alias(dockers: dict, docker: str) -> str:
    """The alias of ``docker`` in the reports: ``template.alias`` of its entry, ``''`` when it has none."""
    return ((dockers.get(docker) or {}).get('template') or {}).get('alias', '')


def dialect(dockers: dict, docker: str) -> str:
    """The SQL dialect of ``docker``: ``template.dialect`` of its entry, ``''`` when it has none."""
    return ((dockers.get(docker) or {}).get('template') or {}).get('dialect', '')


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
    """Check the descriptors of all DBMS: what the module docstring describes.

    Per DBMS: ``base_system`` names a DBMS of ``dockers``, ``storage_prefix`` is a non-empty string,
    ``workers`` is a bool, the keys of ``sut_attributes`` are known, and a DBMS with ``benchmarks``
    has a ``storage_prefix`` and a ``template.alias``. Per benchmark entry and per variant: the
    benchmark exists, every key is known and has its type (:data:`ENTRY_KEYS`), notes have a text,
    ``when`` expressions are allowed (:func:`evaluate`), tenancy modes are known, and the job
    templates exist in ``template_folder``. Across all DBMS: ``template.alias`` and
    ``template.docker_alias`` are unique (equal ones merge in reports, and the
    anonymized connection names of DBMSBenchmarker become equal).

    :param dockers: The ``dockers`` section of the cluster configuration.
    :param benchmarks: The benchmark keys that exist (the keys of ``volumes``).
    :param template_folder: Folder of the job templates (``k8s``); template names are
        only checked for existence when given.
    :return: One message per problem, empty when the descriptors are valid.
    :rtype: list
    """
    problems = []
    for name, docker in dockers.items():
        problems += _docker_problems(dockers, name)
        for benchmark, entry in (docker.get('benchmarks') or {}).items():
            where = f"{name}.benchmarks.{benchmark}"
            if benchmark not in benchmarks:
                problems.append(f"{where}: unknown benchmark (known: {', '.join(sorted(benchmarks))})")
            if not isinstance(entry, dict):
                problems.append(f"{where}: must be a dict")
                continue
            problems += _entry_problems(where, entry, template_folder)
    for field in ('alias', 'docker_alias'):
        owners = {}
        for name, docker in dockers.items():
            value = (docker.get('template') or {}).get(field)
            if value:
                owners.setdefault(value, []).append(name)
        for value, names in sorted(owners.items()):
            if len(names) > 1:
                problems.append(f"template.{field} {value!r} is used by several DBMS: {', '.join(names)}")
    return problems


def _docker_problems(dockers: dict, name: str) -> list:
    """The problems of the DBMS-level keys of ``dockers[name]`` (see :func:`validate_descriptors`)."""
    docker, problems = dockers[name], []
    base = docker.get('base_system')
    if base is not None and base not in dockers:
        problems.append(f"{name}: base_system {base!r} is not a DBMS of dockers")
    prefix = docker.get('storage_prefix')
    if prefix is not None and (not isinstance(prefix, str) or not prefix):
        problems.append(f"{name}: storage_prefix must be a non-empty string, got {prefix!r}")
    if not isinstance(docker.get('workers', False), bool):
        problems.append(f"{name}: workers must be bool, got {docker['workers']!r}")
    if not isinstance(docker.get('sut_attributes', {}), dict):
        problems.append(f"{name}: sut_attributes must be a dict, got {docker['sut_attributes']!r}")
    else:
        problems += _sut_attribute_problems(f"{name}.sut_attributes", docker.get('sut_attributes') or {})
    if docker.get('benchmarks') and prefix is None:
        problems.append(f"{name}: has benchmarks but no storage_prefix")
    if docker.get('benchmarks') and not alias(dockers, name):
        problems.append(f"{name}: has benchmarks but no template.alias")
    return problems


def _entry_problems(where: str, entry: dict, template_folder: str) -> list:
    """The problems of one benchmark entry, ``where`` names it in the messages (see :func:`validate_descriptors`)."""
    problems = _key_problems(where, entry)
    for note in entry.get('notes') or []:
        if not isinstance(note, dict) or not isinstance(note.get('text'), str) or not note['text']:
            problems.append(f"{where}.notes: every note needs a non-empty 'text'")
        elif not isinstance(note.get('when', ''), str):
            problems.append(f"{where}.notes: 'when' must be a string")
    for number, variant in enumerate(entry.get('variants') or [], start=1):
        label = f"{where}.variants[{number}]"
        if not isinstance(variant, dict) or not isinstance(variant.get('when'), str):
            problems.append(f"{label}: needs a 'when' expression")
            continue
        # the expression is checked with every name it uses set to 1, there is no command line here
        try:
            evaluate(variant['when'], _names_of(variant['when']))
        except (ValueError, SyntaxError) as error:
            problems.append(f"{label}.when: {error}")
        # a variant takes the keys of an entry, with their types, but no variants of its own
        if 'variants' in variant:
            problems.append(f"{label}: unknown key 'variants' (a variant has no variants)")
        problems += _key_problems(label, {key: value for key, value in variant.items() if key not in ('when', 'variants')})
    modes = entry.get('multi_tenancy')
    if isinstance(modes, list):
        unknown = [mode for mode in modes if mode not in TENANCY_MODES]
        if unknown:
            problems.append(f"{where}.multi_tenancy: unknown mode {', '.join(map(repr, unknown))} "
                            f"(allowed: {', '.join(TENANCY_MODES)})")
    for key in ('loading_template', 'refresh_template'):
        template = entry.get(key)
        if template_folder and isinstance(template, str) and template \
                and not os.path.isfile(os.path.join(template_folder, template)):
            problems.append(f"{where}.{key}: {template} not found in {template_folder}")
    return problems


def _key_problems(where: str, entry: dict) -> list:
    """Unknown keys and wrong types of an entry or variant (:data:`ENTRY_KEYS`; a ``$by`` selector stands for any type)."""
    problems = []
    for key, value in entry.items():
        if key not in ENTRY_KEYS:
            problems.append(f"{where}: unknown key {key!r} (allowed: {', '.join(ENTRY_KEYS)})")
        elif not (isinstance(value, ENTRY_KEYS[key]) or (isinstance(value, dict) and '$by' in value)):
            problems.append(f"{where}.{key}: must be {ENTRY_KEYS[key].__name__}, got {value!r}")
        elif ENTRY_KEYS[key] is str and not value:
            problems.append(f"{where}.{key}: must not be empty (leave the key out)")
        elif key == 'sut_attributes':
            problems += _sut_attribute_problems(f"{where}.sut_attributes", value)
    return problems


def _sut_attribute_problems(where: str, attributes: dict) -> list:
    """Keys of ``sut_attributes`` that are neither a setter, ``statefulsets`` nor a known attribute."""
    known = (*SUT_SETTERS, SUT_STATEFULSETS, *SUT_ATTRIBUTES)
    return [f"{where}: unknown key {key!r} (allowed: {', '.join(known)})" for key in attributes if key not in known]
