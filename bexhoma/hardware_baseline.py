"""
Run a short-lived, cluster-wide hardware baseline sweep and merge its results
into an ``environment.yml``-style descriptor (see ``bexhoma/environment.py``).

Deploys one ``Hardware`` SUT per cluster node (all as ``SutConfiguration``
objects under a single, shared experiment), measures CPU/RAM (sysbench) and
container-local disk I/O (fio) on each node's own SUT, optionally measures
inter-node network latency (sockperf) as a star (every node vs. one hub) or
full round-robin matrix, then removes every component the sweep created --
regardless of whether it succeeded.

The fio round always runs once against each node's own container-local
(ephemeral) storage, exactly as before. ``run_hardware_baseline()``'s
``storage_classes`` parameter can additionally request the same fio round
against one or more named StorageClasses -- each gets its own short-lived
``Hardware`` SUT per node, backed by a throwaway PersistentVolumeClaim from
that class instead of the node's local disk, so e.g. a Ceph-backed class can
be compared against local/ephemeral storage on the same node.

This reuses the existing ``Hardware`` benchmark machinery
(``bexhoma/experiments/hardware.py``, ``bexhoma/configurations``,
``bexhoma/evaluators/hardware.py``) unmodified: no new Kubernetes manifests
and no changes to ``images/hardware/*`` are needed. A node is pinned to its
own SUT (and its own benchmarker pods) via the same ``kubernetes.io/hostname``
nodeSelector patch ``prepare_testbed()`` already builds for ``-rnn``/``-rnb``,
and the network test simply overrides one node's benchmarker round's own
``BEXHOMA_HOST`` to point at another node's SUT service -- a per-round
override the manifest pipeline already supports generically.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Any, Optional

from bexhoma import configurations, experiments
from bexhoma.cli_args import make_base_parser

__all__ = [
    "HardwareBaselineError",
    "HardwareBaselineResult",
    "compute_star_schedule",
    "compute_round_robin_schedule",
    "run_hardware_baseline",
]

#: Placeholder used only inside the round-robin circle-method computation to
#: pad an odd node count to even; never leaks into a returned schedule.
_BYE = "__bye__"

#: Round-index convention within a per-node ``add_benchmark_list()`` sequence,
#: as it appears in parsed results' ``client`` column. ``BEXHOMA_CLIENT`` is
#: written by ``ManifestBuilder.create_manifest_job()`` as ``cfg.client - 1``
#: (``bexhoma/configurations/manifest.py``) -- but ``work_benchmark_list()``
#: (``experiments/base.py``, the experiment-dict submission branch) already
#: increments ``config.client`` *before* calling ``run_pod()``/
#: ``create_manifest_job()`` for that same round, so by the time the env var
#: is computed, ``cfg.client`` already reflects "next round", not "this one".
#: Net effect, confirmed against a real run's logs: the first round a config
#: runs (the sysbench CPU/RAM self-test) is logged as ``client == 1``, the
#: second (fio) as ``client == 2``, and network rounds (if any) start at
#: ``client == 3`` -- i.e. this *is* 1-indexed, matching
#: ``add_benchmark_list()``'s own round numbering. Used by
#: :func:`_collect_results` to tell a real network round apart from a
#: same-``hardware_type`` self-test/bye filler round at a later index.
_CPU_BASELINE_ROUND = 1
_FIO_BASELINE_ROUND = 2
_FIRST_NETWORK_ROUND = 3

_DEFAULT_HARDWARE_SIZE = "256M"
_DEFAULT_THREADS = "1"
_FIO_DEFAULTS = {
    "HARDWARE_FIO_RW": "randrw", "HARDWARE_FIO_BS": "8k", "HARDWARE_FIO_IODEPTH": "1",
    "HARDWARE_FIO_NUMJOBS": "1", "HARDWARE_FIO_ENGINE": "sync", "HARDWARE_FIO_FSYNC": "0",
    "HARDWARE_FIO_FDATASYNC": "0", "HARDWARE_FIO_RWMIXREAD": "50",
}
#: TCP, not sockperf's own UDP default: this network round exists to assess
#: data systems (DBMS traffic is TCP), not raw UDP datagram latency.
_SOCKPERF_DEFAULTS = {
    "HARDWARE_SOCKPERF_MODE": "ul", "HARDWARE_SOCKPERF_PROTOCOL": "tcp",
    "HARDWARE_SOCKPERF_MSGSIZE": "64", "HARDWARE_SOCKPERF_MPS": "max",
}

#: Kubernetes DNS-label limits leave little room once app/component/experiment
#: prefixes are added by ``generate_component_name()``; node hostnames are
#: truncated defensively rather than risking a manifest-name collision.
_MAX_NODE_ID_LENGTH = 20

#: Same rationale as _MAX_NODE_ID_LENGTH, kept shorter since it is appended
#: to (not instead of) the node id in an extra storage-class sweep's
#: configuration name -- see run_hardware_baseline()'s storage_classes param.
_MAX_STORAGE_CLASS_ID_LENGTH = 10

#: PVC size requested for each extra, named-storage-class fio sweep; only
#: needs to comfortably fit the fio test file (_DEFAULT_HARDWARE_SIZE).
#: Irrelevant to the always-on ephemeral fio round, which never allocates a
#: PVC at all -- see the module docstring.
_DEFAULT_HARDWARE_STORAGE_SIZE = "1Gi"


class HardwareBaselineError(Exception):
    """Raised when a hardware baseline sweep cannot be constructed or run."""


@dataclass
class HardwareBaselineResult:
    """Outcome of a :func:`run_hardware_baseline` sweep.

    :ivar code: Experiment code the sweep ran under (locates its result folder).
    :ivar per_node: Node name to its own CPU/RAM/fio result rows. Always has
        ``"cpu_mem"`` (sysbench) and ``"fio"`` (the always-on fio round
        against the node's own container-local/ephemeral storage) once the
        sweep succeeds for that node, plus one ``"fio:<storage_class>"``
        entry per extra entry of ``storage_classes`` passed to
        :func:`run_hardware_baseline` (e.g. ``"fio:cephcsi"``), each
        measuring fio against a throwaway PersistentVolumeClaim provisioned
        from that StorageClass instead.
    :ivar network_matrix: ``"{origin}->{target}"`` to that round's sockperf result dict.
    :ivar failed_nodes: Node names that produced no usable result at all.
    """
    code: str
    per_node: dict[str, dict[str, Any]] = field(default_factory=dict)
    network_matrix: dict[str, dict[str, Any]] = field(default_factory=dict)
    failed_nodes: list[str] = field(default_factory=list)


def _sanitize_dns_label(value: str, max_length: int) -> str:
    """Turn arbitrary text into a short, DNS-label-safe configuration-name fragment.

    :param value: Raw text (a node hostname, a StorageClass name, ...).
    :param max_length: Length cap applied after sanitizing.
    :return: Lowercase, ``-``-delimited, length-capped identifier.
    :rtype: str
    """
    sanitized = "".join(character if character.isalnum() else "-" for character in value.lower())
    sanitized = sanitized.strip("-") or "id"
    return sanitized[:max_length]


def _sanitize_node_id(node: str) -> str:
    """Turn a Kubernetes node name into a short, DNS-label-safe configuration suffix.

    :param node: Raw ``kubernetes.io/hostname`` value.
    :return: Lowercase, ``-``-delimited, length-capped identifier.
    :rtype: str
    """
    return _sanitize_dns_label(node, _MAX_NODE_ID_LENGTH)


def _sanitize_storage_class_id(storage_class: str) -> str:
    """Turn a StorageClass name into a short, DNS-label-safe configuration suffix.

    :param storage_class: Real Kubernetes ``StorageClass`` name.
    :return: Lowercase, ``-``-delimited, length-capped identifier.
    :rtype: str
    """
    return _sanitize_dns_label(storage_class, _MAX_STORAGE_CLASS_ID_LENGTH)


def _fio_result_key(storage_class: Optional[str]) -> str:
    """Result-dict key a fio round's row is stored under, in ``per_node[node]``.

    :param storage_class: ``None`` for the always-on ephemeral round (kept as
        the pre-existing ``"fio"`` key for backward compatibility), or a
        StorageClass name for an extra sweep.
    :return: ``"fio"`` or ``"fio:<storage_class>"``.
    :rtype: str
    """
    return "fio" if storage_class is None else f"fio:{storage_class}"


def _validate_storage_classes(storage_classes: Optional[list[Optional[str]]]) -> list[str]:
    """Validate and normalize the ``storage_classes`` sweep parameter.

    ``None`` entries mark the always-on ephemeral fio round every node's
    primary sweep already runs unconditionally -- accepted (e.g.
    ``[None, 'cephcsi']``, matching how a caller would naturally write "the
    usual ephemeral run, plus cephcsi") but otherwise a no-op here, since
    that round does not depend on this parameter at all.

    :param storage_classes: Extra StorageClasses to additionally run a fio
        round against (each via its own throwaway PVC), or ``None``/empty
        for the previous, ephemeral-only behaviour.
    :return: The distinct, order-preserving non-``None`` entries.
    :rtype: list[str]
    :raises HardwareBaselineError: On a duplicate StorageClass name.
    """
    named = [entry for entry in (storage_classes or []) if entry is not None]
    seen: set[str] = set()
    for name in named:
        if name in seen:
            raise HardwareBaselineError(f"storage_classes contains a duplicate: {name!r}")
        seen.add(name)
    return named


def compute_star_schedule(nodes: list[str], hub: str) -> dict[str, list[Optional[str]]]:
    """Build a one-round star network-test schedule: every node targets ``hub``.

    ``hub`` itself gets a single self-test round (target ``None``) instead of
    zero rounds, so every node's benchmark round count stays equal -- required
    for the round-indexed bookkeeping :func:`run_hardware_baseline` and
    :func:`_collect_results` rely on.

    :param nodes: Node names to schedule.
    :param hub: The node every other node's round targets; must be in ``nodes``.
    :return: Node name to a length-1 list: the round's target node name, or
        ``None`` for a self-test round.
    :rtype: dict[str, list[Optional[str]]]
    :raises HardwareBaselineError: When ``hub`` is not one of ``nodes``.
    """
    if hub not in nodes:
        raise HardwareBaselineError(f"hub {hub!r} is not one of the given nodes")
    return {node: [hub if node != hub else None] for node in nodes}


def compute_round_robin_schedule(nodes: list[str]) -> dict[str, list[Optional[str]]]:
    """Build a full round-robin network-test schedule via the circle method.

    Every node is paired with every other node exactly once, spread across
    ``len(nodes) - 1`` rounds (``len(nodes)`` after padding, if the count is
    odd); a round never pairs a node with itself or reuses a node twice, so
    all pairs within one round run concurrently without contending for the
    same node. A node's bye round is a self-test (target ``None``) instead of
    being omitted, so every node's list has the same length.

    :param nodes: Node names to schedule; order only affects which nodes are
        paired within the same first round, not overall coverage.
    :return: Node name to a per-round list of target node names (``None``
        entries mark a self-test/bye round).
    :rtype: dict[str, list[Optional[str]]]
    """
    if len(nodes) < 2:
        return {node: [] for node in nodes}
    working = list(nodes)
    if len(working) % 2 == 1:
        working.append(_BYE)
    total = len(working)
    num_rounds = total - 1
    targets: dict[str, list[Optional[str]]] = {node: [None] * num_rounds for node in nodes}
    fixed = working[0]
    rotating = working[1:]
    for round_index in range(num_rounds):
        arrangement = [fixed] + rotating
        for i in range(total // 2):
            first, second = arrangement[i], arrangement[total - 1 - i]
            if first != _BYE and second != _BYE:
                targets[first][round_index] = second
                targets[second][round_index] = first
        rotating = rotating[-1:] + rotating[:-1]
    return targets


def _build_parsed_args(*, timeout_minutes: Optional[int], hardware_duration: int) -> argparse.Namespace:
    """Build the base-parser argument namespace ``prepare_testbed()`` expects.

    Reuses :func:`bexhoma.cli_args.make_base_parser`'s own defaults instead of
    hand-duplicating them, then overrides only what this feature needs.

    :param timeout_minutes: Wall-clock cap forwarded as ``--experiment-timeout``.
    :param hardware_duration: Seconds each round runs for; only used here to
        build the human-readable workload description (see ``hardware_type``
        below), not to configure any actual round.
    :return: Parsed namespace, as if built from an empty CLI invocation.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(parents=[make_base_parser()])
    args = parser.parse_args([])
    args.mode = "run"
    args.dbms = ["Hardware"]
    args.request_storage_type = None
    args.multi_tenant_num = 0
    args.multi_tenant_by = "container"
    args.experiment_timeout = timeout_minutes
    args.monitoring = False
    args.monitoring_app = False
    args.monitoring_cluster = False
    # bexhoma.benchmarks.hardware.Hardware.configure_workload() (called from
    # prepare_testbed(), before any of this sweep's own per-round HARDWARE_TYPE
    # overrides exist) reads these two hardware.py-specific flags straight off
    # args -- they are not part of make_base_parser(). Only used to build the
    # human-readable workload['info'] text; every round's real HARDWARE_TYPE
    # env var always comes from add_benchmarking_parameters() in
    # run_hardware_baseline(), never from this value. 'sysbench' is picked
    # because its configure_workload() branch needs no further sweep-specific
    # attributes, unlike 'fio'/'sockperf'/'netperf', whose branches read
    # additional args.* attributes make_base_parser() doesn't define either.
    args.hardware_type = "sysbench"
    args.hardware_duration = hardware_duration
    return args


def _node_nodeselector_patch(node: str) -> str:
    """Build the YAML nodeSelector patch pinning benchmarker pods to ``node``.

    Same shape ``prepare_testbed()`` builds for ``-rnb`` at
    ``bexhoma/experiments/base.py:620-627``, just applied per node/config
    instead of once for the whole experiment.

    :param node: Node name to pin to.
    :return: YAML patch string for :meth:`SutConfiguration.patch_benchmarking`.
    :rtype: str
    """
    return """
    spec:
      template:
        spec:
          nodeSelector:
            kubernetes.io/hostname: {node}
    """.format(node=node)


def run_hardware_baseline(
    cluster: Any,
    node_names: list[str],
    *,
    hardware_duration: int = 15,
    network_topology: str = "star",
    hub: Optional[str] = None,
    storage_classes: Optional[list[Optional[str]]] = None,
    timeout_minutes: int = 10,
) -> HardwareBaselineResult:
    """Run a short-lived hardware baseline sweep and tear it down afterward.

    :param cluster: Already-connected ``bexhoma.clusters.Kubernetes`` instance.
    :param node_names: Node names to include (already filtered to schedulable,
        untainted nodes by the caller).
    :param hardware_duration: Seconds each sysbench/fio/sockperf round runs for.
    :param network_topology: ``'none'`` (skip network test), ``'star'``
        (every node vs. one hub), or ``'full'`` (round-robin all-pairs matrix).
    :param hub: Hub node for ``network_topology='star'``; defaults to the
        first entry of ``node_names``.
    :param storage_classes: Extra StorageClasses to additionally run the fio
        round against, e.g. ``[None, 'cephcsi']``. Each named entry gets its
        own short-lived ``Hardware`` SUT per node, backed by a throwaway PVC
        from that class; results land in the returned
        :class:`HardwareBaselineResult` under ``per_node[node]["fio:<name>"]``.
        A ``None`` entry is accepted for readability but otherwise ignored --
        the plain, ephemeral-storage fio round (``per_node[node]["fio"]``)
        always runs regardless of this parameter, exactly as before.
        Defaults to ``None`` (no extra classes), reproducing the previous,
        ephemeral-only behaviour exactly.
    :param timeout_minutes: Wall-clock cap for the whole sweep; the experiment
        is aborted and removed if exceeded (see ``-et``/``max_experiment_minutes``).
    :return: Collected per-node and network-matrix results.
    :rtype: HardwareBaselineResult
    :raises HardwareBaselineError: For an invalid ``network_topology``, an
        empty ``node_names``, or a duplicate entry in ``storage_classes``.
    """
    if not node_names:
        raise HardwareBaselineError("no schedulable nodes given")
    if network_topology not in ("none", "star", "full"):
        raise HardwareBaselineError(f"invalid network_topology {network_topology!r}")
    extra_storage_classes = _validate_storage_classes(storage_classes)

    if network_topology == "star":
        network_targets = compute_star_schedule(node_names, hub if hub is not None else node_names[0])
    elif network_topology == "full":
        network_targets = compute_round_robin_schedule(node_names)
    else:
        network_targets = {node: [] for node in node_names}

    args = _build_parsed_args(timeout_minutes=timeout_minutes, hardware_duration=hardware_duration)
    experiment = experiments.hardware(
        cluster=cluster, timeout=int(args.timeout), code=None, num_experiment_to_apply=1)
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    experiment.set_additional_labels(usecase="hardware-baseline")
    experiment.set_default_benchmarking_parameters(
        HARDWARE_TEST_DIR="/database/fio-test",
        HARDWARE_SIZE=_DEFAULT_HARDWARE_SIZE,
        HARDWARE_DURATION=str(hardware_duration),
        HARDWARE_THREADS=_DEFAULT_THREADS,
    )
    experiment.prepare_testbed(vars(args))

    result = HardwareBaselineResult(code=experiment.code)
    configs_by_node: dict[str, Any] = {}
    storage_class_configs: dict[str, dict[str, Any]] = {}
    try:
        for node in node_names:
            config = configurations.default(
                experiment=experiment, docker="Hardware",
                configuration=f"hw-{_sanitize_node_id(node)}", alias=node,
            )
            config.set_storage(storageConfiguration="hardware")
            config.set_resources(nodeSelector={"cpu": "", "gpu": "", "kubernetes.io/hostname": node})
            config.patch_benchmarking(patch=_node_nodeselector_patch(node))
            configs_by_node[node] = config

        for storage_class in extra_storage_classes:
            for node in node_names:
                extra_configuration = (
                    f"hw-{_sanitize_node_id(node)}-{_sanitize_storage_class_id(storage_class)}"
                )
                extra_config = configurations.default(
                    experiment=experiment, docker="Hardware",
                    configuration=extra_configuration, alias=node,
                )
                extra_config.set_storage(
                    storageConfiguration=extra_configuration,
                    storageClassName=storage_class,
                    storageSize=_DEFAULT_HARDWARE_STORAGE_SIZE,
                    # A throwaway PVC for a one-shot fio measurement must not
                    # survive this sweep's teardown -- unlike a normal DBMS
                    # run, where 'keep' (inherited as True from the
                    # experiment-level default set in prepare_testbed())
                    # deliberately preserves data between repeated runs.
                    keep=False,
                )
                extra_config.set_resources(
                    nodeSelector={"cpu": "", "gpu": "", "kubernetes.io/hostname": node})
                extra_config.patch_benchmarking(patch=_node_nodeselector_patch(node))
                extra_config.add_benchmarking_parameters(HARDWARE_TYPE="fio", **_FIO_DEFAULTS)
                extra_config.add_benchmark_list([1])
                storage_class_configs.setdefault(node, {})[storage_class] = extra_config

        for node in node_names:
            config = configs_by_node[node]
            config.add_benchmarking_parameters(HARDWARE_TYPE="sysbench")
            config.add_benchmarking_parameters(HARDWARE_TYPE="fio", **_FIO_DEFAULTS)
            for target in network_targets.get(node, []):
                if target is None:
                    config.add_benchmarking_parameters(HARDWARE_TYPE="sysbench")
                else:
                    target_config = configs_by_node[target]
                    config.add_benchmarking_parameters(
                        HARDWARE_TYPE="sockperf",
                        BEXHOMA_HOST=target_config.get_service_sut(target_config.configuration),
                        **_SOCKPERF_DEFAULTS,
                    )
            total_rounds = 2 + len(network_targets.get(node, []))
            config.add_benchmark_list([1] * total_rounds)

        experiment.process()
    except Exception as error:
        print(f"WARN: hardware baseline sweep failed: {error}")
    finally:
        experiment.remove_experiment()

    _collect_results(
        cluster, experiment, configs_by_node, network_targets, result,
        storage_class_configs=storage_class_configs)
    result.failed_nodes = [node for node in node_names if node not in result.per_node]
    return result


#: A parsed benchmarking row carries every tool's columns at once (fio,
#: sysbench, sockperf, netperf), zero/blank-filled for whichever tool did not
#: actually run that round (see HardwareEvaluator.log_to_df()'s docstring) --
#: left as-is, a sysbench round's ``hardware_fio_read_iops: 0.0`` reads as a
#: real (if confusing) measurement rather than "not applicable". Dropping the
#: other tools' columns per stored entry avoids that ambiguity.
_OTHER_TOOL_COLUMN_PREFIXES = {
    "sysbench": ("hardware_fio_", "hardware_sockperf_", "hardware_netperf_"),
    "fio": ("hardware_sysbench_", "hardware_sockperf_", "hardware_netperf_"),
    "sockperf": ("hardware_fio_", "hardware_sysbench_", "hardware_netperf_"),
}


def _drop_other_tool_columns(row_dict: dict[str, Any], hardware_type: str) -> dict[str, Any]:
    """Drop zero/blank-filled columns belonging to a different ``HARDWARE_TYPE``.

    :param row_dict: A parsed, aggregated result row, as ``dict``.
    :param hardware_type: Which tool this row actually measured.
    :return: ``row_dict`` with other tools' columns removed.
    :rtype: dict[str, Any]
    """
    prefixes = _OTHER_TOOL_COLUMN_PREFIXES.get(hardware_type, ())
    return {key: value for key, value in row_dict.items() if not key.startswith(prefixes)}


def _collect_results(
    cluster: Any,
    experiment: Any,
    configs_by_node: dict[str, Any],
    network_targets: dict[str, list[Optional[str]]],
    result: HardwareBaselineResult,
    storage_class_configs: Optional[dict[str, dict[str, Any]]] = None,
) -> None:
    """Parse the sweep's already-collected pod logs into ``result`` in place.

    Reuses the ``Hardware`` benchmark's own evaluator
    (:class:`bexhoma.evaluators.hardware.HardwareEvaluator`, already
    instantiated by ``experiment.process()`` for its own summary/tests) --
    it already parses every ``HARDWARE_*`` ``KEY:VALUE`` line the benchmarker
    scripts emit; nothing new is needed here beyond mapping its rows back to
    node/pair identity via the ``hw-<node_id>`` configuration names assigned
    in :func:`run_hardware_baseline`, and the round-index convention
    documented at :data:`_FIRST_NETWORK_ROUND`.

    :param cluster: Cluster the sweep ran against (unused directly; kept for
        symmetry with other collector-style functions and possible future use).
    :param experiment: The completed (and already torn down) experiment.
    :param configs_by_node: Node name to its primary ``SutConfiguration``
        (the one running sysbench, the ephemeral fio round, and any network
        rounds).
    :param network_targets: The same per-node round-target schedule
        :func:`run_hardware_baseline` built, needed to recover which node a
        network round's ``client`` index targeted.
    :param result: Result object to populate in place.
    :param storage_class_configs: Node name to ``{storage_class: SutConfiguration}``
        for the extra, named-storage-class fio-only sweeps (see
        :func:`run_hardware_baseline`'s ``storage_classes`` parameter); each
        such configuration only ever runs a single fio round, so its rows are
        matched by configuration identity alone, not the round-index
        convention the primary configurations rely on. ``None``/empty when
        no extra storage classes were requested.
    """
    del cluster
    try:
        evaluator = experiment.benchmarks[0].evaluator
        df_raw = evaluator.get_df_benchmarking()
        if df_raw.empty:
            return
        df_typed = evaluator.benchmarking_set_datatypes(df_raw)
        df_aggregated = evaluator.benchmarking_aggregate_by_parallel_pods(
            df_typed, columns=["configuration", "client"])
    except Exception as error:
        print(f"WARN: could not parse hardware baseline results: {error}")
        return
    configuration_to_node = {config.configuration: node for node, config in configs_by_node.items()}
    configuration_to_storage_class = {
        config.configuration: (node, storage_class)
        for node, by_class in (storage_class_configs or {}).items()
        for storage_class, config in by_class.items()
    }
    for _, row in df_aggregated.iterrows():
        configuration = row["configuration"]
        storage_class_match = configuration_to_storage_class.get(configuration)
        if storage_class_match is not None:
            node, storage_class = storage_class_match
            row_dict = row.to_dict()
            row_dict["hardware_type"] = "fio"
            result.per_node.setdefault(node, {})[_fio_result_key(storage_class)] = (
                _drop_other_tool_columns(row_dict, "fio"))
            continue
        node = configuration_to_node.get(configuration)
        if node is None:
            continue
        client = int(row["client"])
        # benchmarking_aggregate_by_parallel_pods() does not carry the
        # hardware_type column through (it's not in its hardcoded per-column
        # aggregation/copy rules) -- round order is fixed by
        # run_hardware_baseline() itself, so client alone already identifies
        # the round; hardware_type is reconstructed here purely for the
        # human-readable value stored in the result, not used to decide
        # anything.
        row_dict = row.to_dict()
        if client == _CPU_BASELINE_ROUND:
            row_dict["hardware_type"] = "sysbench"
            result.per_node.setdefault(node, {})["cpu_mem"] = _drop_other_tool_columns(row_dict, "sysbench")
        elif client == _FIO_BASELINE_ROUND:
            row_dict["hardware_type"] = "fio"
            result.per_node.setdefault(node, {})[_fio_result_key(None)] = _drop_other_tool_columns(row_dict, "fio")
        elif client >= _FIRST_NETWORK_ROUND:
            targets = network_targets.get(node, [])
            target_index = client - _FIRST_NETWORK_ROUND
            if 0 <= target_index < len(targets) and targets[target_index] is not None:
                row_dict["hardware_type"] = "sockperf"
                result.network_matrix[f"{node}->{targets[target_index]}"] = _drop_other_tool_columns(row_dict, "sockperf")
