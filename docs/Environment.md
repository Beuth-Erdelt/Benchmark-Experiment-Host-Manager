# Concept: Environment

## Overview

Before an experiment runs, it's useful to know what the target Kubernetes cluster actually looks like: which nodes exist, how much CPU/memory/storage each one has, how much of that other workloads have already reserved, which storage classes are available, what namespace-level resource quotas apply, and which hardware metrics can be monitored.

`bexhoma environment create` inspects the live cluster and writes this as `environment.yml` — a curated, read-only snapshot. It deliberately does not dump the raw Kubernetes API response, only the subset that matters for placing and sizing a benchmarking experiment:

* **`nodes`** — name, curated labels, capacity and allocatable resources, plus the current occupancy, cluster-wide (not just bexhoma's own pods):
  * `free` — allocatable minus the requests of all Pending and Running pods on the node.
  * `requested` — those requests summed.
  * `limits_pct` — their limits as a percentage of allocatable. Above 100 the node is overcommitted: a pod can be squeezed even when `free` leaves room.
* **`occupancy_source`** — where the occupancy came from: `prometheus`, `kubernetes_api` or `unavailable` (see below).
* **`excluded_nodes`** — nodes carrying a taint. Bexhoma's node placement (`-rnn`/`-rnl`/`-rnb`/`-rnp`, `-rct`/`-rgt`) is `nodeSelector`-only with no toleration mechanism, so a tainted node can't be scheduled onto anyway; it's still listed here so its absence from `nodes` is visible rather than silent.
* **`storage_classes`** — real Kubernetes `StorageClass` names, cross-referenced against the cluster's bexhoma-friendly aliases (e.g. `ssd`).
* **`resource_limits`** — the largest node by CPU/memory (both static allocatable and free-right-now), plus any namespace `ResourceQuota`/`LimitRange` objects.
* **`monitoring`** — the cluster-wide hardware metrics from `cluster.config`'s `monitor.metrics` (see [Monitoring](Monitoring.md)), one entry per metric with its `title`, `kind` (`gauge`, `counter` or `ratio`), default `active` flag, and `required` (true for the four CPU/RAM metrics bexhoma's own summary and result checks read). `available` says whether the cluster's Prometheus holds every series the metric's query reads; it is left out, and `availability_checked` is `false`, when Prometheus could not be reached. `source_sha256` fingerprints the metric definitions, so a file older than `cluster.config` can be detected. Application metrics are not listed: they depend on a system's exporter, not on the cluster.

The values are a snapshot: `cluster.collected_at` records when they were taken.

## Occupancy: Prometheus first, then the pod listing

Occupancy is read in this order:

1. **Prometheus** (kube-state-metrics), at `cluster.config`'s `service_monitoring` URL. Prometheus usually lives inside the cluster, so the queries run through `curl` in the bexhoma dashboard pod; the URL must be reachable from there (e.g. `http://prometheus.monitor.svc.cluster.local:9090/api/v1/`, not an external hostname). This needs no permission to list pods cluster-wide, and each pod is counted once even with redundant Prometheus or kube-state-metrics instances.
2. **Kubernetes API** — listing every pod cluster-wide. Used when no Prometheus is configured, no dashboard pod is running, Prometheus has no kube-state-metrics, or a query fails.
3. **Unavailable** — when the pod listing is forbidden too, which is common on a shared cluster. `environment.yml` is still written; every node's `free`, `requested` and `limits_pct` stay empty, with a warning printed.

The same Prometheus route checks metric availability for the `monitoring` section.

## Progress output

`bexhoma environment create` prints one line per step: the context and namespace, how many nodes are schedulable or excluded, which occupancy source was used (and the Prometheus URL and pod), the storage classes found, how many monitoring metrics have data, the hardware baseline sweep when requested, and the path written.

## Hardware baseline (optional)

Static specs don't tell you how fast a node's disk or network actually is. Passing `-xhw` additionally runs a short, cluster-mutating sweep — sysbench CPU/RAM, fio against each node's own container-local scratch space, and an optional sockperf (TCP) network test between nodes — and merges the results into `environment.yml` under each node's `hardware_baseline` key (network results go into a top-level `network_matrix`). It's off by default because, unlike the collectors above, it deploys and tears down real pods.

`-xhwsc` additionally sweeps fio against one or more extra StorageClasses, alongside the always-present ephemeral-storage fio round — useful for comparing e.g. `cephcsi` or `local-hdd` against a node's local scratch disk. Each named class gets a single throwaway PVC on one node, not one per node — a network-backed class isn't assumed to be node-local, so one measurement per class is enough. Results land as an extra `"fio:<name>"` entry under that one node's `hardware_baseline`; every other node keeps only its own ephemeral `"fio"` entry.

## Usage

```
bexhoma environment create [-h] [-cx CONTEXT] [-o OUTPUT] [-xhw]
                            [-xhwd HARDWARE_BASELINE_DURATION]
                            [-xhwnet {none,star,full}]
                            [-xhwt HARDWARE_BASELINE_TIMEOUT]
                            [-xhwsc HARDWARE_BASELINE_STORAGE_CLASSES]
```

Write `environment.yml` for the current kubectl context, to the default path (`environment.yml` in the current directory):

```powershell
bexhoma environment create
```

Target a specific context and output path:

```powershell
bexhoma environment create -cx my-context -o config/my-cluster.yml
```

Include the hardware baseline sweep (30s per round instead of the default 15s):

```powershell
bexhoma environment create -xhw -xhwd 30
```

Skip the inter-node network test (sysbench/fio only, no sockperf):

```powershell
bexhoma environment create -xhw -xhwnet none
```

Also sweep fio against extra StorageClasses (each via its own throwaway PVC), alongside the always-present ephemeral-storage round:

```powershell
bexhoma environment create -xhw -xhwsc cephcsi,local-hdd
```

Recommended hardware baseline settings — skip the network test, 10s per round, capped at 40 minutes wall-clock:

```powershell
bexhoma environment create -xhw -xhwnet none -xhwd 10 -xhwt 40
```

Full option reference:

```powershell
bexhoma environment create --help
```
