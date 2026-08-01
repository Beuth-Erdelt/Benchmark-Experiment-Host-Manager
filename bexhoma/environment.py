"""
Generate ``environment.yml`` — a curated, machine-readable descriptor of the
concrete Kubernetes cluster a ``catalog.yaml``/``experiment.yml`` pair would
run against (see ``docs/Design-Catalog-Contract.md``).

This is the read-only half of that contract: nodes (with curated labels,
their static allocatable/capacity resources, and how much of that is
actually free right now, cluster-wide), storage classes, and a
namespace/cluster resource-limit summary relevant to validating a resolved
experiment before it is run. It deliberately does not dump the raw
Kubernetes API response — only the subset of node/storage-class/limit data
that matters for placing and sizing a benchmarking experiment.

Nodes carrying any taint are excluded from ``nodes:`` entirely rather than
listed with a caveat: bexhoma's placement mechanism (``-rnn``/``-rnl``/
``-rnb``/``-rnp`` node pinning, ``-rct``/``-rgt`` label selectors — see
``bexhoma/cli_args.py``) is ``nodeSelector``-only, with no toleration
mechanism anywhere in the codebase, so a tainted node is not schedulable by
any bexhoma-managed pod today regardless of label match. Excluded nodes are
still surfaced, under ``excluded_nodes:``, so their absence from ``nodes:``
is auditable rather than silent.

The hardware-baseline step (running sysbench cpu/memory per node, fio
against each node's own container-local scratch space, and an optional
sockperf network test between nodes) is opt-in via ``-xhw`` on the CLI, or
:func:`bexhoma.hardware_baseline.run_hardware_baseline` directly. Unlike the
collectors above it is cluster-mutating (it deploys and tears down a short
benchmark sweep), so it stays off by default.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

import kubernetes.client as kubernetes_client
import kubernetes.config as kubernetes_config
import yaml
from kubernetes.client.rest import ApiException

from bexhoma.spec import parse_memory_quantity

#: RBAC users on a shared cluster are commonly granted node/storage-class
#: read but not cluster-scoped pod listing (that would reveal every other
#: user's workloads) — a 403 here is an expected permissions gap, not a
#: broken connection, so it degrades free-capacity accounting rather than
#: aborting the whole run.
_HTTP_FORBIDDEN = 403

__all__ = [
    "EnvironmentError",
    "NodeInfo",
    "StorageClassInfo",
    "collect_nodes",
    "collect_node_usage",
    "collect_storage_classes",
    "collect_resource_limits",
    "build_environment",
    "apply_hardware_baseline",
    "write_environment_yml",
    "main",
]

#: Node labels curated as benchmarking-relevant; every other label Kubernetes
#: attaches (bookkeeping, CNI, cloud-provider internals) is dropped. Includes
#: standard topology/arch labels plus the bexhoma-specific labels already
#: load-bearing for placement today: ``cpu``/``gpu`` (matched by
#: ``-rct``/``-rgt``, see ``configurations/lifecycle.py``'s ``nodeSelector``
#: construction) and ``type``/``alpha.eksctl.io/nodegroup-name`` (AWS
#: nodegroup selection, see ``clusters.py``'s ``AWS.get_nodes()``).
_RELEVANT_NODE_LABEL_KEYS = (
    "kubernetes.io/hostname",
    "kubernetes.io/arch",
    "node.kubernetes.io/instance-type",
    "topology.kubernetes.io/zone",
    "topology.kubernetes.io/region",
    "cpu",
    "gpu",
    "type",
    "alpha.eksctl.io/nodegroup-name",
)

#: Resource-quantity keys curated from node capacity/allocatable maps.
_RELEVANT_NODE_RESOURCE_PREFIXES = ("cpu", "memory", "ephemeral-storage", "hugepages-")
_EXTENDED_GPU_RESOURCE_SUFFIX = "gpu"


class EnvironmentError(Exception):
    """Raised when the live cluster cannot be inspected (e.g. unreachable)."""


@dataclass
class NodeInfo:
    """A single benchmarking-relevant node, curated from a ``V1Node``.

    :ivar name: Node name.
    :ivar labels: Curated label subset (see :data:`_RELEVANT_NODE_LABEL_KEYS`).
    :ivar capacity: Raw Kubernetes quantity strings from ``status.capacity``.
    :ivar allocatable: Raw Kubernetes quantity strings from ``status.allocatable``.
    :ivar os_image: ``status.node_info.os_image``.
    :ivar kernel_version: ``status.node_info.kernel_version``.
    :ivar container_runtime_version: ``status.node_info.container_runtime_version``.
    :ivar architecture: ``status.node_info.architecture``.
    :ivar free: ``allocatable`` minus the summed resource *requests* of every
        non-terminal pod currently scheduled on this node, cluster-wide (not
        just bexhoma's own pods) — populated by :func:`collect_node_usage`,
        empty until then. This is "room right now", distinct from
        ``allocatable``, which is a static per-node total that ignores
        whatever is already running.
    :ivar hardware_baseline: This node's own CPU/RAM (sysbench) and
        container-local disk I/O (fio) results, keyed ``"cpu_mem"``/``"fio"``
        — populated by the opt-in ``-xhw`` sweep
        (:func:`bexhoma.hardware_baseline.run_hardware_baseline`), empty
        otherwise. Node-to-node network results are not per-node; see the
        top-level ``network_matrix`` key :func:`build_environment` returns.
    """
    name: str
    labels: dict[str, str] = field(default_factory=dict)
    capacity: dict[str, str] = field(default_factory=dict)
    allocatable: dict[str, str] = field(default_factory=dict)
    os_image: str = ""
    kernel_version: str = ""
    container_runtime_version: str = ""
    architecture: str = ""
    free: dict[str, str] = field(default_factory=dict)
    hardware_baseline: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_v1node(cls, node: Any) -> "NodeInfo":
        """Curate a ``kubernetes.client.V1Node`` into a :class:`NodeInfo`.

        Pure function — no Kubernetes API access — so it can be exercised
        against hand-built ``V1Node`` objects without a live cluster.

        :param node: A ``kubernetes.client.V1Node`` (or equivalent duck type).
        :return: The curated node.
        :rtype: NodeInfo
        """
        all_labels = node.metadata.labels or {}
        node_info = node.status.node_info
        return cls(
            name=node.metadata.name,
            labels={key: all_labels[key] for key in _RELEVANT_NODE_LABEL_KEYS if key in all_labels},
            capacity=_curate_resource_quantities(node.status.capacity or {}),
            allocatable=_curate_resource_quantities(node.status.allocatable or {}),
            os_image=node_info.os_image,
            kernel_version=node_info.kernel_version,
            container_runtime_version=node_info.container_runtime_version,
            architecture=node_info.architecture,
        )


@dataclass
class StorageClassInfo:
    """A Kubernetes ``StorageClass``, cross-referenced against a cluster's
    bexhoma-friendly storage-class aliases (``cluster.storage_classes``).

    :ivar name: Real Kubernetes ``StorageClass`` name.
    :ivar alias: The bexhoma-friendly alias (e.g. ``ssd``) mapping to this
        StorageClass, or ``None`` if it isn't one of the cluster's declared
        aliases.
    :ivar provisioner: Volume provisioner.
    :ivar parameters: Provisioner-specific parameters.
    :ivar reclaim_policy: Reclaim policy (e.g. ``Delete``, ``Retain``).
    :ivar volume_binding_mode: Volume binding mode.
    """
    name: str
    alias: Optional[str] = None
    provisioner: str = ""
    parameters: dict[str, str] = field(default_factory=dict)
    reclaim_policy: str = ""
    volume_binding_mode: str = ""

    @classmethod
    def from_v1storageclass(cls, storage_class: Any, aliases: dict[str, str]) -> "StorageClassInfo":
        """Curate a ``kubernetes.client.V1StorageClass`` into a :class:`StorageClassInfo`.

        Pure function — no Kubernetes API access.

        :param storage_class: A ``kubernetes.client.V1StorageClass`` (or equivalent duck type).
        :param aliases: Mapping of real StorageClass name to bexhoma-friendly alias.
        :return: The curated storage class.
        :rtype: StorageClassInfo
        """
        name = storage_class.metadata.name
        return cls(
            name=name,
            alias=aliases.get(name),
            provisioner=storage_class.provisioner or "",
            parameters=storage_class.parameters or {},
            reclaim_policy=storage_class.reclaim_policy or "",
            volume_binding_mode=storage_class.volume_binding_mode or "",
        )


def _curate_resource_quantities(quantities: dict[str, str]) -> dict[str, str]:
    """Keep only benchmarking-relevant resource-quantity keys, as raw strings.

    :param quantities: A node's ``status.capacity`` or ``status.allocatable`` map.
    :return: The curated subset, values left as the original Kubernetes quantity strings.
    :rtype: dict[str, str]
    """
    return {
        key: value
        for key, value in quantities.items()
        if key.startswith(_RELEVANT_NODE_RESOURCE_PREFIXES) or key.endswith(_EXTENDED_GPU_RESOURCE_SUFFIX)
    }


def _node_taints(node: Any) -> list[dict[str, str]]:
    """Return a node's taints as plain dicts.

    :param node: A ``kubernetes.client.V1Node``.
    :return: List of ``{key, value, effect}`` dicts.
    :rtype: list[dict[str, str]]
    """
    taints = node.spec.taints or []
    return [{"key": taint.key, "value": taint.value or "", "effect": taint.effect} for taint in taints]


def _cpu_quantity_to_millicores(value: str) -> int:
    """Parse a Kubernetes CPU quantity (``"16"``, ``"16000m"``) into millicores.

    :param value: A CPU quantity string.
    :return: Millicores.
    :rtype: int
    """
    text = str(value).strip()
    if text.endswith("m"):
        return int(text[:-1])
    return int(float(text) * 1000)


#: Resource-name suffixes/prefixes whose quantities are memory-shaped
#: (Ki/Mi/Gi/... or a bare byte count), parsed via ``parse_memory_quantity``
#: rather than as a bare float — covers ``memory``, ``ephemeral-storage``,
#: and the oddly-named ``hugepages-1Gi``/``hugepages-2Mi`` resources (whose
#: size is baked into the key name; the quantity itself is still bytes).
_MEMORY_SHAPED_RESOURCE_MARKERS = ("storage", "hugepages")


def _quantity_to_number(resource_name: str, quantity: str) -> float:
    """Parse a Kubernetes resource quantity into a comparable numeric value.

    ``cpu`` is expressed in millicores, memory-shaped resources in bytes
    (both via existing parsers); anything else (e.g. ``nvidia.com/gpu``) is
    a bare count.

    :param resource_name: Resource key, e.g. ``"cpu"``, ``"memory"``, ``"nvidia.com/gpu"``.
    :param quantity: The quantity's raw Kubernetes string value.
    :return: A comparable/summable numeric value.
    :rtype: float
    """
    if resource_name == "cpu":
        return float(_cpu_quantity_to_millicores(quantity))
    if resource_name == "memory" or any(marker in resource_name for marker in _MEMORY_SHAPED_RESOURCE_MARKERS):
        return float(parse_memory_quantity(quantity))
    try:
        return float(quantity)
    except ValueError:
        return float(parse_memory_quantity(quantity))


def _format_quantity(resource_name: str, amount: float) -> str:
    """Format a numeric resource amount back into a Kubernetes quantity string.

    :param resource_name: Resource key, as passed to :func:`_quantity_to_number`.
    :param amount: Numeric amount, in the same unit :func:`_quantity_to_number` returned.
    :return: A valid Kubernetes quantity string (``"27000m"`` for cpu, a bare
        integer otherwise — a bare number is itself a valid quantity, meaning bytes
        for memory-shaped resources or a plain count for extended resources).
    :rtype: str
    """
    if resource_name == "cpu":
        return f"{int(round(amount))}m"
    return str(int(round(amount)))


def collect_nodes(cluster: Any) -> tuple[list[NodeInfo], list[dict[str, Any]]]:
    """Collect and curate every node in the cluster, splitting out tainted nodes.

    Deliberately does **not** call ``cluster.get_nodes()`` — that method
    always applies a ``label_selector='app=<appname>'`` filter, meant for
    picking out an AWS-style dedicated nodegroup that was explicitly labeled
    for this app. On a plain/on-prem cluster (no such nodegroup labeling)
    that filter matches nothing, silently returning zero nodes — the wrong
    result for a descriptor whose whole purpose is "what does the concrete
    cluster look like". This calls ``list_node()`` directly, unfiltered.

    :param cluster: A ``bexhoma.clusters.Kubernetes`` instance (already connected).
    :return: ``(nodes, excluded_nodes)`` — curated schedulable nodes, and
        ``{name, taints}`` dicts for nodes excluded due to taints.
    :rtype: tuple[list[NodeInfo], list[dict[str, Any]]]
    :raises EnvironmentError: When the Node API can't be reached.
    """
    try:
        api_response = cluster.v1core.list_node()
    except Exception as error:
        raise EnvironmentError(f"could not list nodes: {error}") from error
    nodes: list[NodeInfo] = []
    excluded_nodes: list[dict[str, Any]] = []
    for node in api_response.items or []:
        taints = _node_taints(node)
        if taints:
            excluded_nodes.append({"name": node.metadata.name, "taints": taints})
        else:
            nodes.append(NodeInfo.from_v1node(node))
    return nodes, excluded_nodes


#: Pod phases whose containers no longer hold requested resources.
_TERMINAL_POD_PHASES = ("Succeeded", "Failed")


def _accumulate_pod_requests(pod_items: list[Any]) -> dict[str, dict[str, float]]:
    """Sum resource requests of non-terminal, scheduled pods, grouped by node.

    Pure function — no Kubernetes API access — operating on already-fetched
    ``V1Pod`` items, so it can be exercised without a live cluster.

    :param pod_items: ``V1Pod`` objects, e.g. from ``list_pod_for_all_namespaces().items``.
    :return: Mapping of node name to summed requests, keyed by resource name
        (values in the units :func:`_quantity_to_number` returns).
    :rtype: dict[str, dict[str, float]]
    """
    requests_by_node: dict[str, dict[str, float]] = {}
    for pod in pod_items:
        if pod.status.phase in _TERMINAL_POD_PHASES or not pod.spec.node_name:
            continue
        node_requests = requests_by_node.setdefault(pod.spec.node_name, {})
        for pod_container in pod.spec.containers or []:
            requests = (pod_container.resources and pod_container.resources.requests) or {}
            for resource_name, quantity in requests.items():
                node_requests[resource_name] = (
                    node_requests.get(resource_name, 0.0) + _quantity_to_number(resource_name, quantity)
                )
    return requests_by_node


def _compute_free_resources(allocatable: dict[str, str], used: dict[str, float]) -> dict[str, str]:
    """Compute per-resource free amounts: allocatable minus in-use, floored at zero.

    Pure function, only over the already-curated ``allocatable`` keys — a
    node offers "free" only for the resources it reports at all.

    :param allocatable: A node's curated ``allocatable`` map (see :data:`_RELEVANT_NODE_RESOURCE_PREFIXES`).
    :param used: Summed in-use amounts for the same node, as returned by :func:`_accumulate_pod_requests`.
    :return: Free amount per resource, formatted back into Kubernetes quantity strings.
    :rtype: dict[str, str]
    """
    return {
        resource_name: _format_quantity(
            resource_name,
            max(_quantity_to_number(resource_name, allocatable_value) - used.get(resource_name, 0.0), 0.0),
        )
        for resource_name, allocatable_value in allocatable.items()
    }


def collect_node_usage(cluster: Any, nodes: list[NodeInfo]) -> None:
    """Populate each node's :attr:`NodeInfo.free` — allocatable minus in-use, cluster-wide.

    Cluster-wide, not scoped to bexhoma's own pods: "free right now" needs to
    account for every workload competing for the same nodes, not just ones
    this tool launched. This requires listing pods across every namespace,
    which most users on a shared cluster are deliberately *not* granted (it
    would reveal other users' workloads) — a 403 here is treated as "can't
    compute this", not a fatal error: it prints a warning and leaves every
    node's ``free`` at its dataclass default (``{}``), so the rest of
    ``environment.yml`` (nodes, storage classes, static resource ceilings)
    is still produced.

    :param cluster: A ``bexhoma.clusters.Kubernetes`` instance (already connected).
    :param nodes: Curated, schedulable nodes (mutated in place), as returned by :func:`collect_nodes`.
    :raises EnvironmentError: When the Pod API can't be reached for a reason other than permissions.
    """
    try:
        pods = cluster.v1core.list_pod_for_all_namespaces()
    except ApiException as error:
        if error.status == _HTTP_FORBIDDEN:
            print(
                "WARN: no permission to list pods cluster-wide "
                "(need cluster-scoped 'pods' list access) - skipping free-capacity "
                "accounting; every node's 'free' will stay empty"
            )
            return
        raise EnvironmentError(f"could not list pods for resource-usage accounting: {error}") from error
    except Exception as error:
        raise EnvironmentError(f"could not list pods for resource-usage accounting: {error}") from error
    requests_by_node = _accumulate_pod_requests(pods.items or [])
    for node in nodes:
        node.free = _compute_free_resources(node.allocatable, requests_by_node.get(node.name, {}))


def collect_storage_classes(cluster: Any) -> list[StorageClassInfo]:
    """Collect all Kubernetes ``StorageClass`` objects, cross-referenced against
    ``cluster.storage_classes``.

    Constructs its own ``StorageV1Api`` client, following the same
    ``kubernetes_config.new_client_from_config(context=...)`` idiom
    ``Kubernetes.cluster_access()`` uses for its own API clients — there is
    no existing ``StorageV1Api`` client on ``cluster`` to reuse.

    :param cluster: A ``bexhoma.clusters.Kubernetes`` instance (already connected).
    :return: Curated storage classes.
    :rtype: list[StorageClassInfo]
    :raises EnvironmentError: When the StorageClass API can't be reached.
    """
    # cluster.storage_classes (from the cluster config's credentials.k8s.context.
    # <name>.storage_classes, see clusters.py:135) already holds the real,
    # cluster-specific StorageClass names — the same string doubles as the
    # bexhoma-facing "-rst <name>" alias (get_available_storage_types()'s own
    # docstring: "actual Kubernetes StorageClass names differ from cluster to
    # cluster"), so alias and real name are identical here, not a separate mapping.
    aliases = {name: name for name in getattr(cluster, "storage_classes", [])}
    try:
        v1storage = kubernetes_client.StorageV1Api(
            api_client=kubernetes_config.new_client_from_config(context=cluster.context)
        )
        api_response = v1storage.list_storage_class()
    except Exception as error:
        raise EnvironmentError(f"could not list storage classes: {error}") from error
    return [StorageClassInfo.from_v1storageclass(item, aliases) for item in api_response.items]


def _derive_resource_limits_from_nodes(nodes: list[NodeInfo]) -> dict[str, Any]:
    """Derive cluster-wide resource ceilings from already-collected nodes.

    Includes both the static ``allocatable`` ceiling and, when
    :func:`collect_node_usage` has already populated ``node.free``, the
    "room right now" ceiling — the single largest node by each measure may
    differ (the biggest node isn't necessarily the emptiest one).

    :param nodes: Curated, schedulable nodes (see :func:`collect_nodes`).
    :return: ``max_allocatable_cpu``/``max_allocatable_memory``/``max_free_cpu``/
        ``max_free_memory``/``node_count``.
    :rtype: dict[str, Any]
    """
    return {
        "max_allocatable_cpu": _max_resource_across_nodes(nodes, "cpu", "allocatable"),
        "max_allocatable_memory": _max_resource_across_nodes(nodes, "memory", "allocatable"),
        "max_free_cpu": _max_resource_across_nodes(nodes, "cpu", "free"),
        "max_free_memory": _max_resource_across_nodes(nodes, "memory", "free"),
        "node_count": len(nodes),
    }


def _max_resource_across_nodes(nodes: list[NodeInfo], resource_name: str, attribute_name: str) -> Optional[str]:
    """Find the largest raw quantity for one resource across a node attribute.

    :param nodes: Curated nodes to scan.
    :param resource_name: Resource key, e.g. ``"cpu"`` or ``"memory"``.
    :param attribute_name: Which per-node dict to read — ``"allocatable"`` or ``"free"``.
    :return: The winning node's raw quantity string, or ``None`` if no node reports the
        resource — distinct from a genuine ``"0"``, e.g. when :func:`collect_node_usage`
        was skipped for lack of permissions and no node has any ``free`` data at all.
    :rtype: Optional[str]
    """
    best_value, best_amount = None, -1.0
    for node in nodes:
        quantity = getattr(node, attribute_name).get(resource_name)
        if quantity is None:
            continue
        amount = _quantity_to_number(resource_name, quantity)
        if amount > best_amount:
            best_amount, best_value = amount, quantity
    return best_value


def collect_resource_limits(cluster: Any, nodes: list[NodeInfo]) -> dict[str, Any]:
    """Collect resource limits relevant to validating a resolved experiment.

    Combines a per-node capacity ceiling (derived from ``nodes``, no extra API
    call) with any namespace-scoped ``ResourceQuota``/``LimitRange`` objects
    (via the existing ``cluster.v1core`` client) — the two real Kubernetes
    concepts that actually gate whether a resolved ``resources.cpu.limit``/
    ``memory.limit`` could be scheduled and admitted at all.

    :param cluster: A ``bexhoma.clusters.Kubernetes`` instance (already connected).
    :param nodes: Curated, schedulable nodes (see :func:`collect_nodes`).
    :return: Resource-limit summary.
    :rtype: dict[str, Any]
    """
    limits = _derive_resource_limits_from_nodes(nodes)
    try:
        quotas = cluster.v1core.list_namespaced_resource_quota(cluster.namespace)
        limit_ranges = cluster.v1core.list_namespaced_limit_range(cluster.namespace)
    except Exception as error:
        raise EnvironmentError(f"could not list namespace resource quotas/limit ranges: {error}") from error
    limits["namespace_resource_quotas"] = [
        {"name": item.metadata.name, "hard": dict(item.spec.hard or {})} for item in quotas.items
    ]
    limits["namespace_limit_ranges"] = [
        {
            "name": item.metadata.name,
            "limits": [
                {
                    "type": limit_item.type,
                    "default": dict(limit_item.default or {}),
                    "default_request": dict(limit_item.default_request or {}),
                    "max": dict(limit_item.max or {}),
                    "min": dict(limit_item.min or {}),
                }
                for limit_item in (item.spec.limits or [])
            ],
        }
        for item in limit_ranges.items
    ]
    return limits


def build_environment(cluster: Any) -> dict[str, Any]:
    """Build the full ``environment.yml`` content for ``cluster``.

    :param cluster: A ``bexhoma.clusters.Kubernetes`` instance (already connected).
    :return: The environment descriptor, ready for :func:`write_environment_yml`.
    :rtype: dict[str, Any]
    """
    nodes, excluded_nodes = collect_nodes(cluster)
    collect_node_usage(cluster, nodes)
    return {
        "cluster": {
            "context": cluster.context,
            "namespace": cluster.namespace,
            "collected_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
        "nodes": [vars(node) for node in nodes],
        "excluded_nodes": excluded_nodes,
        "storage_classes": [vars(storage_class) for storage_class in collect_storage_classes(cluster)],
        "resource_limits": collect_resource_limits(cluster, nodes),
    }


def apply_hardware_baseline(
    cluster: Any,
    environment: dict[str, Any],
    *,
    hardware_duration: int = 15,
    network_topology: str = "star",
    hub: Optional[str] = None,
    timeout_minutes: int = 10,
) -> None:
    """Run the opt-in hardware baseline sweep and merge its results into ``environment``.

    Mutates ``environment["nodes"]`` in place (setting each node dict's
    ``"hardware_baseline"`` entry) and adds a top-level ``"network_matrix"``
    key. Only nodes already present in ``environment["nodes"]`` are swept —
    tainted nodes were already excluded by :func:`collect_nodes`.

    Deliberately does not raise on sweep failure: a broken hardware baseline
    must not prevent ``environment.yml`` from being written at all, matching
    the degrade-and-continue behaviour :func:`collect_node_usage` already
    follows for its own permissions gap.

    :param cluster: A ``bexhoma.clusters.Kubernetes`` instance (already connected).
    :param environment: Descriptor built by :func:`build_environment`; mutated in place.
    :param hardware_duration: Seconds each sysbench/fio/sockperf round runs for.
    :param network_topology: ``'none'``, ``'star'``, or ``'full'`` — see
        :func:`bexhoma.hardware_baseline.run_hardware_baseline`.
    :param hub: Hub node for ``network_topology='star'``; defaults to the first node.
    :param timeout_minutes: Wall-clock cap for the whole sweep.
    """
    from bexhoma import hardware_baseline

    node_names = [node["name"] for node in environment["nodes"]]
    try:
        result = hardware_baseline.run_hardware_baseline(
            cluster, node_names,
            hardware_duration=hardware_duration, network_topology=network_topology,
            hub=hub, timeout_minutes=timeout_minutes,
        )
    except hardware_baseline.HardwareBaselineError as error:
        print(f"WARN: hardware baseline sweep skipped: {error}")
        return
    for node in environment["nodes"]:
        if node["name"] in result.per_node:
            node["hardware_baseline"] = result.per_node[node["name"]]
    environment["network_matrix"] = result.network_matrix
    if result.failed_nodes:
        environment["hardware_baseline_failed_nodes"] = result.failed_nodes


def write_environment_yml(environment: dict[str, Any], path: str) -> None:
    """Write an environment descriptor to a YAML file.

    :param environment: Descriptor built by :func:`build_environment`.
    :param path: Output file path.
    """
    with open(path, "w", encoding="utf-8") as environment_file:
        yaml.safe_dump(environment, environment_file, sort_keys=False)


def main(argv: Optional[list[str]] = None) -> None:
    """CLI entry point — parses args, builds ``environment.yml``, writes it.

    Invoked both as ``python -m bexhoma.environment [args]`` and, in-process,
    as the ``bexhoma environment create`` subcommand (see
    ``bexhoma/scripts/cli.py``).

    :param argv: Argument list to parse in place of ``sys.argv[1:]`` — used
        by the ``bexhoma environment create`` dispatch; ``None`` parses the
        real process arguments.
    """
    import argparse

    import urllib3

    from bexhoma import clusters

    # Clusters using a self-signed/internal CA (e.g. an on-prem kubeconfig with
    # insecure-skip-tls-verify) make urllib3 print an InsecureRequestWarning on
    # every single API call — matches the existing convention in tpch.py/
    # hardware.py/example.py's own entry points. Scoped to the CLI path only
    # (not module import) since environment.py's collectors are also used as a
    # library, where silently muting warnings would be a surprising side effect.
    urllib3.disable_warnings()

    cli_parser = argparse.ArgumentParser(prog="bexhoma environment create", description=__doc__)
    cli_parser.add_argument("-cx", "--context", help="kubectl context to use (default: current context)", default=None)
    cli_parser.add_argument("-o", "--output", help="output path for environment.yml", default="dev/catalog/environment.yml")
    cli_parser.add_argument(
        "-xhw", "--xhardware-baseline",
        help="also run a short-lived hardware baseline sweep (sysbench CPU/RAM, fio against "
             "container-local disk, optional inter-node network test) and merge it in; "
             "cluster-mutating, off by default",
        action="store_true", default=False, dest="hardware_baseline")
    cli_parser.add_argument(
        "-xhwd", "--xhardware-baseline-duration",
        help="seconds each sysbench/fio/sockperf round of the baseline sweep runs for",
        type=int, default=15, dest="hardware_baseline_duration")
    cli_parser.add_argument(
        "-xhwnet", "--xhardware-baseline-network",
        help="inter-node network test topology: 'none' (skip), 'star' (every node vs. one "
             "hub), or 'full' (round-robin all-pairs matrix)",
        choices=["none", "star", "full"], default="star", dest="hardware_baseline_network")
    cli_parser.add_argument(
        "-xhwt", "--xhardware-baseline-timeout",
        help="wall-clock cap in minutes for the whole baseline sweep",
        type=int, default=10, dest="hardware_baseline_timeout")
    cli_args = cli_parser.parse_args(argv)

    cli_cluster = clusters.Kubernetes(context=cli_args.context)
    cli_environment = build_environment(cli_cluster)
    if cli_args.hardware_baseline:
        apply_hardware_baseline(
            cli_cluster, cli_environment,
            hardware_duration=cli_args.hardware_baseline_duration,
            network_topology=cli_args.hardware_baseline_network,
            timeout_minutes=cli_args.hardware_baseline_timeout,
        )
    write_environment_yml(cli_environment, cli_args.output)
    print(f"wrote {cli_args.output}")


if __name__ == "__main__":
    main()
