"""
Shared argument parser factory for bexhoma CLI scripts.

Provides :func:`make_base_parser`, which returns an :class:`argparse.ArgumentParser`
pre-loaded with all arguments that are common to ``benchbase.py``, ``hammerdb.py``,
``tpch.py``, ``tpcds.py``, and ``ycsb.py``.

Authors: Patrick K. Erdelt
Copyright (C) 2023 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse
import ast
import os
import re

from bexhoma.load_durability import DEFAULT_LEVEL as LOAD_DURABILITY_DEFAULT, LEVELS as LOAD_DURABILITY_LEVELS

__all__ = [
    "make_base_parser", "resolve_scaling_factor",
    "parse_metric_overrides", "format_metric_overrides",
    "split_storage_types", "format_storage_types",
    "storage_suffix", "set_cell_storage", "resource_cells",
    "KEEP_SUT_CHOICES", "resolve_keep_sut", "split_worker_nodes",
]

#: ``-rnw`` value that stands for the SUT's node (``-rnn``).
WORKER_NODE_SUT = 'sut'

#: Values of ``-ks/--keep-sut``.
KEEP_SUT_CHOICES = ('auto', 'yes', 'no')

#: Modes whose SUTs ``--keep-sut auto`` keeps: they exist to leave a running SUT behind.
_MODES_KEEPING_SUT = ('load', 'start')


def resolve_keep_sut(mode: str, keep_sut: str = 'auto', skip_shutdown: bool = False) -> bool:
    """Decide whether each configuration's last SUT is kept running at the end.

    :param mode: The experiment mode (``run``, ``load``, ``start``, ...).
    :param keep_sut: ``-ks/--keep-sut``: ``auto``, ``yes`` or ``no``.
    :param skip_shutdown: ``-ss/--skip-shutdown``, an alias for ``--keep-sut yes``.
    :return: True to keep the SUTs.
    :rtype: bool
    :raises ValueError: For ``-ss`` with ``--keep-sut no``, an unknown value,
        or ``start`` with ``--keep-sut no`` (it would start SUTs only to stop them).
    """
    if keep_sut not in KEEP_SUT_CHOICES:
        raise ValueError(f"--keep-sut must be one of {', '.join(KEEP_SUT_CHOICES)}, not {keep_sut!r}")
    if skip_shutdown:
        if keep_sut == 'no':
            raise ValueError("-ss/--skip-shutdown keeps the SUTs, --keep-sut no stops them: use one")
        keep_sut = 'yes'
    if keep_sut == 'auto':
        return mode in _MODES_KEEPING_SUT
    if keep_sut == 'no' and mode == 'start':
        raise ValueError("mode start only starts the SUTs; --keep-sut no would stop them right away")
    return keep_sut == 'yes'


def split_worker_nodes(value, sut_node=None) -> list:
    """
    Split ``-rnw``'s value into one list of worker nodes per resource cell.

    Nodes of one cell are joined by ``+`` (``cl-worker37+cl-worker38``);
    commas separate cells, paired by position with the other resource lists
    like ``-rst``. ``sut`` stands for the SUT's node (``-rnn``).

    :param value: ``args.request_node_worker``; ``None`` or empty means no pinning.
    :param sut_node: ``args.request_node_name``, for ``sut``.
    :return: One node list per cell (``[None]`` without ``-rnw``).
    :rtype: list[Optional[list[str]]]
    :raises ValueError: For an empty cell, or ``sut`` without ``-rnn``.
    """
    if not value:
        return [None]
    cells = []
    for cell in str(value).split(','):
        nodes = []
        for node in cell.split('+'):
            node = node.strip()
            if not node:
                raise ValueError(f"-rnw {value!r}: empty node name in cell {cell!r}")
            if node == WORKER_NODE_SUT:
                if not sut_node:
                    raise ValueError(f"-rnw {value!r}: '{WORKER_NODE_SUT}' needs the SUT node (-rnn)")
                node = sut_node
            if node not in nodes:
                nodes.append(node)
        cells.append(nodes)
    return cells


def check_tenant_loading_pods(num_loading_pods, num_tenants: int, tenant_by: str,
                              one_pod_per_tenant: bool = False) -> None:
    """Check that schema/database tenancy gets the same number of loader pods per tenant.

    The loaders split the pods evenly across tenants (``BEXHOMA_NUM_PODS / BEXHOMA_TENANT_NUM``);
    with a remainder, a tenant would load a part twice. Container tenancy runs one loader
    job per tenant and needs no check.

    :param num_loading_pods: Parsed ``-nlp`` values.
    :param num_tenants: ``-mtn``; 0 means no tenancy.
    :param tenant_by: ``-mtb``: ``schema``, ``database`` or ``container``.
    :param one_pod_per_tenant: ``-nlp`` counts pods per tenant (the experiment starts
        ``-nlp`` x ``-mtn`` pods) and the loader maps pod k to tenant k-1 (Benchbase),
        so ``-nlp`` must be 1.
    :raises ValueError: When an ``-nlp`` value is not a multiple of ``-mtn`` (or, with
        ``one_pod_per_tenant``, not 1).
    """
    if num_tenants <= 0 or tenant_by not in ('schema', 'database'):
        return
    if one_pod_per_tenant:
        several = [pods for pods in num_loading_pods if int(pods) != 1]
        if several:
            raise ValueError(
                f"-nlp {','.join(map(str, several))} is not 1: {tenant_by} tenancy of this "
                f"benchmark loads each of the -mtn {num_tenants} tenants with one pod"
            )
        return
    uneven = [pods for pods in num_loading_pods if int(pods) % num_tenants != 0]
    if uneven:
        raise ValueError(
            f"-nlp {','.join(map(str, uneven))} is not a multiple of -mtn {num_tenants}: "
            f"{tenant_by} tenancy needs the same number of loader pods per tenant"
        )


def resource_cells(request_cpu_list, limit_cpu_list, request_ram_list, limit_ram_list, storage_type_list=None,
                   worker_nodes_list=None):
    """Zip per-dimension resource CLI lists into one resource cell per swept value.

    Every list with more than one entry must share the same length; a
    single-entry list is broadcast (repeated) to that length. This lets
    e.g. ``-rr 32Gi,64Gi -lr 32Gi,64Gi`` sweep RAM across two configurations
    per DBMS while ``-rc``/``-lc`` stay one shared CPU value for both.

    :param request_cpu_list: Parsed ``-rc`` values.
    :param limit_cpu_list: Parsed ``-lc`` values.
    :param request_ram_list: Parsed ``-rr`` values.
    :param limit_ram_list: Parsed ``-lr`` values.
    :param storage_type_list: Parsed ``-rst`` values
        (:func:`split_storage_types`), ``None`` for ephemeral;
        omitted means one experiment-wide storage class.
    :param worker_nodes_list: Parsed ``-rnw`` values (:func:`split_worker_nodes`),
        one node list (or ``None``) per cell; omitted means no worker pinning.
    :return: List of ``{'cpu', 'cpu_limit', 'memory', 'memory_limit', 'storage_type',
        'worker_nodes'}`` dicts, one per cell.
    :rtype: list[dict]
    :raises ValueError: When two lists both have more than one entry but different lengths.
    """
    lists = {
        'cpu': request_cpu_list,
        'cpu_limit': limit_cpu_list,
        'memory': request_ram_list,
        'memory_limit': limit_ram_list,
        'storage_type': storage_type_list if storage_type_list is not None else [None],
        'worker_nodes': worker_nodes_list if worker_nodes_list is not None else [None],
    }
    num_cells = max((len(values) for values in lists.values() if len(values) > 1), default=1)
    for name, values in lists.items():
        if len(values) > 1 and len(values) != num_cells:
            raise ValueError(
                f"resource sweep lists must share one length: '{name}' has {len(values)} "
                f"entries, expected 1 or {num_cells}"
            )
    return [
        {name: (values[i] if len(values) > 1 else values[0]) for name, values in lists.items()}
        for i in range(num_cells)
    ]


def split_storage_types(value) -> list:
    """
    Split ``-rst``'s value into one storage class per resource cell.

    A value without a comma is one class for the whole experiment and keeps
    its meaning unchanged (``None`` ephemeral, ``''``, ``'ramdisk'`` or a
    class name). A comma list sweeps the storage class across configurations,
    paired by position with the ``-rr``/``-lr``/``-rc``/``-lc`` lists; an
    empty entry there means ephemeral node-local storage.

    :param value: ``args.request_storage_type``.
    :return: One storage class per cell, ``None`` for ephemeral.
    :rtype: list[Optional[str]]
    """
    if value is None or "," not in value:
        return [value]
    return [entry.strip() or None for entry in value.split(",")]


def format_storage_types(storage_types: list) -> str:
    """
    Format one storage class per cell as ``-rst``'s comma list.

    The inverse of :func:`split_storage_types` for a sweep: ``None``
    (ephemeral) becomes an empty entry.

    :param storage_types: One storage class per cell, ``None`` for ephemeral.
    :return: The flag value.
    :rtype: str
    """
    return ",".join(storage_type or "" for storage_type in storage_types)


def storage_suffix(storage_type) -> str:
    """
    Name a storage class as part of a volume name.

    A PVC is found again by name alone, so the class is part of it (see
    :meth:`bexhoma.configurations.base.SutConfiguration.get_storage_configuration`):
    otherwise a volume loaded on one backend could be reused for another, in
    this run or a later one.

    :param storage_type: The storage class, ``None`` for ephemeral.
    :return: A DNS-label-safe suffix such as ``cephcsi`` or ``ephemeral``.
    :rtype: str
    """
    return re.sub(r'[^a-z0-9-]+', '-', (storage_type or 'ephemeral').lower()).strip('-')


def set_cell_storage(config, storage_configuration, cell) -> None:
    """
    Give one resource cell its own volume name and storage class.

    The class is added to the volume name when the volume is named
    (``get_storage_configuration()``), not here.

    :param config: The cell's SUT configuration.
    :param storage_configuration: ``storageConfiguration`` name for the cell.
    :param cell: The cell, a dict with at least ``storage_type`` (``None`` for ephemeral).
    """
    config.set_storage(
        storageConfiguration=storage_configuration,
        storageClassName=cell['storage_type'],
    )

#: Spellings accepted for one ``-mm key=value`` switch.
_METRIC_SWITCH_VALUES = {"on": True, "true": True, "off": False, "false": False}


def parse_metric_overrides(text: str) -> dict:
    """
    Parse ``-mm``'s ``key=on,key=off`` list into ``{metric_key: active}``.

    Used as the argparse ``type`` of ``--monitoring-metrics``, so a malformed
    entry is a usage error before anything is deployed.

    :param text: Comma-separated ``key=on|off`` (``true``/``false`` also accepted).
    :return: Requested ``active`` flag per metric key.
    :rtype: dict[str, bool]
    :raises argparse.ArgumentTypeError: On an entry that is not ``key=on|off``.
    """
    overrides = {}
    for entry in text.split(","):
        if not entry.strip():
            continue
        key, separator, value = entry.partition("=")
        switch = _METRIC_SWITCH_VALUES.get(value.strip().lower())
        if not separator or not key.strip() or switch is None:
            raise argparse.ArgumentTypeError(
                f"monitoring metric override {entry!r} must be key=on or key=off")
        overrides[key.strip()] = switch
    return overrides


def format_metric_overrides(overrides: dict) -> str:
    """
    Format ``{metric_key: active}`` as ``-mm``'s ``key=on,key=off`` value.

    :param overrides: Requested ``active`` flag per metric key.
    :return: The flag value, empty when there are no overrides.
    :rtype: str
    """
    return ",".join(f"{key}={'on' if active else 'off'}" for key, active in overrides.items())


def resolve_scaling_factor(cluster, code, mode: str, cli_scaling_factor) -> str:
    """
    Returns the scaling factor an entry script should construct its experiment
    object with.

    For ``mode='summary'`` on an existing experiment ``code``, reads the
    already-persisted ``defaultParameters.SF`` from that experiment's
    ``queries.config`` instead of trusting the ``-sf`` CLI default. Constructing
    the experiment with the wrong SF re-arms dbmsbenchmarker's shared, process-global
    ``parameter.defaultParameters`` with a value the experiment never actually used;
    if results are then re-evaluated, that wrong value leaks back into
    ``queries.config`` and corrupts Power@Size/Throughput-style metrics for an
    experiment that ran at a different scale factor. For every other mode (a fresh
    or resumed live run), the CLI value is authoritative and is returned unchanged.

    :param cluster: Already-constructed cluster object (provides ``resultfolder``).
    :param code: Experiment identifier, or ``None`` for a brand-new experiment.
    :param mode: The entry script's ``mode`` positional argument.
    :param cli_scaling_factor: Value of ``args.scaling_factor`` (the ``-sf`` CLI default).
    :return: Scaling factor to use, as a string.
    :rtype: str
    """
    if mode == 'summary' and code is not None:
        filename = os.path.join(cluster.resultfolder, str(code), 'queries.config')
        if os.path.isfile(filename):
            with open(filename, 'r') as inp:
                workload_properties = ast.literal_eval(inp.read())
            sf = workload_properties.get('defaultParameters', {}).get('SF')
            if sf is not None:
                return str(sf)
    return str(cli_scaling_factor)


def make_base_parser():
    """
    Returns an :class:`~argparse.ArgumentParser` (with ``add_help=False``) pre-loaded
    with all arguments common to the bexhoma benchmark entry-point scripts.

    Intended to be passed as a parent::

        parser = argparse.ArgumentParser(parents=[make_base_parser()], ...)

    Standardised defaults that differ from some of the original per-script
    values:

    - ``--timeout`` → ``600``
    - ``--request-gpu-type`` → ``''``
    - ``--num-worker`` → ``0``  (use ``parser.set_defaults(num_worker=1)`` to override)

    :return: Argument parser carrying all shared arguments.
    :rtype: argparse.ArgumentParser
    """
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument('-aws', '--aws', help='pin components to AWS EKS node groups', action='store_true', default=False)
    p.add_argument('-db',  '--debug', help='enable debug logging', action='store_true')
    p.add_argument('-sl',  '--skip-loading', help='skip data loading and start benchmarking immediately', action='store_true', default=False)
    p.add_argument('-ss',  '--skip-shutdown', help='keep SUT pods running after the experiment finishes; same as --keep-sut yes', action='store_true', default=False)
    p.add_argument('-ks',  '--keep-sut', help="keep the SUT of each configuration's last repetition running at the end: auto (default) keeps it in modes load and start and stops it otherwise; yes keeps it, no stops it. A kept SUT that another configuration waits for (-ms/-mse) is stopped", choices=KEEP_SUT_CHOICES, default='auto')
    p.add_argument('-xld', '--load-durability', help="durability of the DBMS during the load only (afterwards the configured state of template and --set is restored): durable makes the load crash-safe (e.g. PostgreSQL synchronous_commit/fsync on, MySQL innodb_flush_log_at_trx_commit=1); relaxed (default) commits without flushing and skips checks (e.g. PostgreSQL synchronous_commit=off, MySQL innodb_flush_log_at_trx_commit); unsafe uses the strongest lever of the DBMS (e.g. MySQL redo log off, PostgreSQL fsync=off), a crash during the load can lose data. Runs the scripts durability-<level>.* and restoredurability-<level>.* the DBMS folder has", choices=LOAD_DURABILITY_LEVELS, default=LOAD_DURABILITY_DEFAULT)
    p.add_argument('-ar',  '--activate-reset', help='activate configured reset scripts (e.g. CHECKPOINT/VACUUM) when set on a benchmarker entry; off by default', action='store_true', default=False)
    p.add_argument('-cx',  '--context', help='kubectl context to use (default: current context)', default=None)
    p.add_argument('-e',   '--experiment', help='resume an existing experiment by its code', default=None)
    p.add_argument('-m',   '--monitoring', help='enable Prometheus monitoring for the SUT', action='store_true')
    p.add_argument('-ma',  '--monitoring-app', help='enable application-level metrics collection', action='store_true', default=False)
    p.add_argument('-mc',  '--monitoring-cluster', help='enable node-level monitoring for the entire cluster', action='store_true', default=False)
    p.add_argument('-mm',  '--monitoring-metrics', help="switch single cluster-wide hardware metrics of cluster.config on or off for this experiment, overriding their 'active' flag, e.g. total_gpu_util=on,total_network_rx=off; needs -m or -mc", type=parse_metric_overrides, default={}, dest='monitoring_metrics')
    p.add_argument('-ms',  '--max-sut', help='maximum number of DBMS configurations to run in parallel cluster-wide (default: no limit)', default=None)
    p.add_argument('-mse', '--max-sut-experiment', help='maximum number of DBMS configurations in this experiment to run in parallel (default: no limit)', default=None)
    p.add_argument('-et',  '--experiment-timeout', help='maximum wall-clock duration of the experiment in minutes; when exceeded, the experiment is stopped and all its components are removed from the cluster (default: no limit)', type=int, default=None)
    p.add_argument('-lt',  '--loading-timeout', help='maximum loading duration per configuration in minutes; captures diagnostics and removes the experiment when exceeded (default: no limit)', type=int, default=None)
    p.add_argument('-nc',  '--num-config', help='number of experiment repetitions per configuration', default=1)
    p.add_argument('-ne',  '--num-query-executors', help='comma-separated list of parallel client counts to sweep', default="1")
    p.add_argument('-nw',  '--num-worker', help='number of worker nodes for distributed DBMS', default=0)
    p.add_argument('-nwr', '--num-worker-replicas', help='number of replicas per worker node', default=0)
    p.add_argument('-nws', '--num-worker-shards', help='number of shards per worker node', default=0)
    p.add_argument('-nlp', '--num-loading-pods', help='comma-separated list of total loader pod counts', default="1")
    p.add_argument('-nlt', '--num-loading-threads', help='comma-separated list of total loader threads (split across pods)', default="1")
    p.add_argument('-nbp', '--num-benchmarking-pods', help='comma-separated list of benchmarker pod counts', default="1")
    p.add_argument('-nbt', '--num-benchmarking-threads', help='total benchmarking threads, split evenly across pods', default="1")
    p.add_argument('-sf',  '--scaling-factor', help='scaling factor controlling dataset size', default=1)
    p.add_argument('-t',   '--timeout', help='per-query timeout in seconds', default=1800)
    p.add_argument('-lr',  '--limit-ram', help='RAM limit for the SUT and worker pods (e.g. 64Gi; 0 = no limit); comma-separated to sweep several settings (e.g. 32Gi,64Gi), one configuration per entry', default='0')
    p.add_argument('-lc',  '--limit-cpu', help='CPU limit for the SUT and worker pods (e.g. 4; 0 = no limit); comma-separated to sweep, must then match the length of any other swept resource list', default='0')
    p.add_argument('-rr',  '--request-ram', help='RAM request for the SUT and worker pods (e.g. 16Gi); comma-separated to sweep several settings (e.g. 32Gi,64Gi), one configuration per entry', default='16Gi')
    p.add_argument('-rc',  '--request-cpu', help='CPU request for the SUT and worker pods (e.g. 4); comma-separated to sweep, must then match the length of any other swept resource list', default='4')
    p.add_argument('-rct', '--request-cpu-type', help='require SUT node to carry label cpu=<value>', default='')
    p.add_argument('-rg',  '--request-gpu', help='number of GPUs to request for the SUT pod', default=1)
    p.add_argument('-rgt', '--request-gpu-type', help='require SUT node to carry label gpu=<value>', default='')
    p.add_argument('-rst', '--request-storage-type', help="storage class for the SUT persistent volume ('' or unset = ephemeral, 'ramdisk' = in-memory; other values must be declared for the active cluster context, see cluster config 'storage_classes'); comma-separated to sweep the class, one configuration per entry and paired by position with -rc/-lc/-rr/-lr, an empty entry meaning ephemeral", default=None)
    p.add_argument('-rss', '--request-storage-size', help='size of the SUT persistent volume (e.g. 10Gi)', default='')
    p.add_argument('-rsr', '--request-storage-remove', help='delete any existing PVC for the SUT before starting', action='store_true', default=False)
    p.add_argument('-rsrp', '--request-storage-remove-per-repetition', help='delete the PVC of the SUT before every repetition (-nc), so each repetition loads into a fresh volume; implies -rsr', action='store_true', default=False)
    p.add_argument('-rnn', '--request-node-name', help='pin the SUT pod to this Kubernetes node', default=None, nargs='?', const=None)
    p.add_argument('-rnl', '--request-node-loading', help='pin loader pods to this Kubernetes node', default=None, nargs='?', const=None)
    p.add_argument('-rnb', '--request-node-benchmarking', help='pin benchmarker pods to this Kubernetes node', default=None, nargs='?', const=None)
    p.add_argument('-rnp', '--request-node-pooling', help='pin pooling pods to this Kubernetes node', default=None, nargs='?', const=None)
    p.add_argument('-rnw', '--request-node-worker', help="pin the worker pods (all StatefulSets of the SUT) to these Kubernetes nodes, joined by '+' and spread evenly (e.g. cl-worker37+cl-worker38+cl-worker39); 'sut' stands for the -rnn node; comma-separated to sweep, one configuration per entry and paired by position with -rc/-lc/-rr/-lr/-rst", default=None, nargs='?', const=None)
    p.add_argument('-mtn', '--multi-tenant-num', help='number of tenants for multi-tenant experiments', default=0)
    p.add_argument('-mtb', '--multi-tenant-by', help='tenancy granularity: schema, database, or container', default='')
    p.add_argument('-mtv', '--multi-tenant-volume', help='allocate a separate persistent volume per tenant', action='store_true', default=False)
    p.add_argument('-tr',  '--test-result', help='validate that results meet basic correctness requirements', action='store_true', default=False)
    p.add_argument('-rp',  '--report', help='also write a tiered Markdown summary report (report/index.md + detail files) to the result folder', action='store_true', default=False, dest='write_report')
    p.add_argument("--set", dest="sets", action="append", default=[], help="override a deployment parameter, e.g. deployment[sut].container[dbms].max_worker_processes=128 (PostgreSQL -c key=value, MySQL/MariaDB --key=value, chosen by the template) or an environment variable via ...container[dbms].env.NAME=VALUE")
    return p
