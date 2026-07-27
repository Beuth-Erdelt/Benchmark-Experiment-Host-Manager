"""
Demo/verification script for bexhoma/environment.py — the environment.yml
generator (see docs/Design-Catalog-Contract.md).

Exercises the curation logic (label allowlisting, tainted-node exclusion,
storage-class alias cross-referencing, resource-limit derivation) against
hand-built ``kubernetes.client`` model objects, so it can run without a live
cluster — mirroring dev/spec_prototype_demo.py's approach for bexhoma/spec.py.

Run from the repo root: ``python dev/environment_prototype_demo.py``
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import kubernetes.client as kubernetes_client
from kubernetes.client.rest import ApiException

from bexhoma import environment


def _build_fake_node(name: str, labels: dict, cpu: str, memory: str, taints=None) -> kubernetes_client.V1Node:
    """Build a hand-crafted V1Node for offline curation testing.

    :param name: Node name.
    :param labels: Node labels.
    :param cpu: Allocatable/capacity CPU quantity (used for both).
    :param memory: Allocatable/capacity memory quantity (used for both).
    :param taints: Optional list of ``kubernetes.client.V1Taint``.
    :return: The fake node.
    :rtype: kubernetes.client.V1Node
    """
    return kubernetes_client.V1Node(
        metadata=kubernetes_client.V1ObjectMeta(name=name, labels=labels),
        spec=kubernetes_client.V1NodeSpec(taints=taints or []),
        status=kubernetes_client.V1NodeStatus(
            capacity={"cpu": cpu, "memory": memory},
            allocatable={"cpu": cpu, "memory": memory},
            node_info=kubernetes_client.V1NodeSystemInfo(
                architecture="amd64",
                boot_id="",
                container_runtime_version="containerd://1.7.13",
                kernel_version="5.15.0-113-generic",
                kube_proxy_version="",
                kubelet_version="",
                machine_id="",
                operating_system="linux",
                os_image="Ubuntu 22.04.4 LTS",
                system_uuid="",
            ),
        ),
    )


def main() -> None:
    """Curate fake nodes/storage classes and print the resulting descriptor."""
    worker = _build_fake_node(
        "cl-worker19", {"kubernetes.io/hostname": "cl-worker19", "cpu": "amd", "type": "ssd-pool", "irrelevant-label": "x"},
        cpu="32", memory="134217728Ki",
    )
    small_worker = _build_fake_node(
        "cl-worker20", {"kubernetes.io/hostname": "cl-worker20"}, cpu="16", memory="67108864Ki",
    )
    tainted_master = _build_fake_node(
        "cl-master1", {"kubernetes.io/hostname": "cl-master1"}, cpu="8", memory="16777216Ki",
        taints=[kubernetes_client.V1Taint(key="node-role.kubernetes.io/control-plane", value="", effect="NoSchedule")],
    )

    nodes, excluded_nodes = [], []
    for node in (worker, small_worker, tainted_master):
        taints = environment._node_taints(node)
        if taints:
            excluded_nodes.append({"name": node.metadata.name, "taints": taints})
        else:
            nodes.append(environment.NodeInfo.from_v1node(node))

    print("nodes:")
    for node in nodes:
        print(" ", node)
    print("excluded_nodes:")
    for excluded in excluded_nodes:
        print(" ", excluded)
    assert [node.name for node in nodes] == ["cl-worker19", "cl-worker20"]
    assert [excluded["name"] for excluded in excluded_nodes] == ["cl-master1"]
    assert "irrelevant-label" not in nodes[0].labels
    assert nodes[0].labels["type"] == "ssd-pool"

    fake_storage_class = kubernetes_client.V1StorageClass(
        metadata=kubernetes_client.V1ObjectMeta(name="ssd"),
        provisioner="kubernetes.io/no-provisioner",
        parameters={},
        reclaim_policy="Delete",
        volume_binding_mode="WaitForFirstConsumer",
    )
    storage_class_info = environment.StorageClassInfo.from_v1storageclass(fake_storage_class, aliases={"ssd": "ssd"})
    print("storage_class:", storage_class_info)
    assert storage_class_info.alias == "ssd"

    resource_limits = environment._derive_resource_limits_from_nodes(nodes)
    print("resource_limits (before usage accounting):", resource_limits)
    assert resource_limits["max_allocatable_cpu"] == "32"
    assert resource_limits["max_allocatable_memory"] == "134217728Ki"
    assert resource_limits["max_free_cpu"] is None  # no node has 'free' data yet -> unknown, not "0"
    assert resource_limits["max_free_memory"] is None
    assert resource_limits["node_count"] == 2

    # --- free-capacity accounting: fake pods competing for the same nodes ---
    def _fake_pod(node_name, phase, cpu_request, memory_request):
        return kubernetes_client.V1Pod(
            spec=kubernetes_client.V1PodSpec(
                node_name=node_name,
                containers=[
                    kubernetes_client.V1Container(
                        name="c",
                        resources=kubernetes_client.V1ResourceRequirements(
                            requests={"cpu": cpu_request, "memory": memory_request}
                        ),
                    )
                ],
            ),
            status=kubernetes_client.V1PodStatus(phase=phase),
        )

    fake_pods = [
        _fake_pod("cl-worker19", "Running", "4000m", "16Gi"),
        _fake_pod("cl-worker19", "Running", "2", "8Gi"),
        _fake_pod("cl-worker19", "Succeeded", "1000000m", "1000Gi"),  # terminal — must not count
        _fake_pod(None, "Pending", "1000000m", "1000Gi"),  # unscheduled — must not count
    ]
    requests_by_node = environment._accumulate_pod_requests(fake_pods)
    print("requests_by_node:", requests_by_node)
    assert requests_by_node["cl-worker19"]["cpu"] == 6000.0
    assert "cl-worker20" not in requests_by_node

    for node in nodes:
        node.free = environment._compute_free_resources(node.allocatable, requests_by_node.get(node.name, {}))
    print("nodes with free:")
    for node in nodes:
        print(" ", node.name, node.free)
    assert nodes[0].free["cpu"] == "26000m"  # 32 cores - (4000m + 2 cores) used = 26 cores
    assert nodes[1].free["cpu"] == "16000m"  # no pods on cl-worker20 -> free == allocatable (16 cores), reformatted
    assert nodes[1].free["memory"] == str(environment.parse_memory_quantity(nodes[1].allocatable["memory"]))

    resource_limits = environment._derive_resource_limits_from_nodes(nodes)
    print("resource_limits (after usage accounting):", resource_limits)
    assert resource_limits["max_free_cpu"] == "26000m"  # cl-worker19 has 26 free cores vs cl-worker20's 16
    assert resource_limits["max_free_memory"] not in (None, "0")

    # --- graceful degradation: RBAC forbids cluster-wide pod listing ---
    class _ForbiddenV1Core:
        def list_pod_for_all_namespaces(self):
            raise ApiException(status=403, reason="Forbidden")

    class _ForbiddenCluster:
        v1core = _ForbiddenV1Core()

    forbidden_nodes = [environment.NodeInfo(name="n1", allocatable={"cpu": "8", "memory": "1Gi"})]
    environment.collect_node_usage(_ForbiddenCluster(), forbidden_nodes)
    print("node.free after 403:", forbidden_nodes[0].free)
    assert forbidden_nodes[0].free == {}  # degraded gracefully, not raised

    print()
    print("all assertions passed")


if __name__ == "__main__":
    main()
