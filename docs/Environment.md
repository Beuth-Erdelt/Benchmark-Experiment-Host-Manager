# Concept: Environment

## Overview

Before an experiment runs, it's useful to know what the target Kubernetes cluster actually looks like: which nodes exist, how much CPU/memory/storage each one has, how much of that is free right now, which storage classes are available, and what namespace-level resource quotas apply.

`bexhoma environment create` inspects the live cluster and writes this as `environment.yml` — a curated, read-only snapshot. It deliberately does not dump the raw Kubernetes API response, only the subset that matters for placing and sizing a benchmarking experiment:

* **`nodes`** — name, curated labels, capacity, allocatable resources, and *free* resources (allocatable minus what's currently in use, cluster-wide, not just bexhoma's own pods).
* **`excluded_nodes`** — nodes carrying a taint. Bexhoma's node placement (`-rnn`/`-rnl`/`-rnb`/`-rnp`, `-rct`/`-rgt`) is `nodeSelector`-only with no toleration mechanism, so a tainted node can't be scheduled onto anyway; it's still listed here so its absence from `nodes` is visible rather than silent.
* **`storage_classes`** — real Kubernetes `StorageClass` names, cross-referenced against the cluster's bexhoma-friendly aliases (e.g. `ssd`).
* **`resource_limits`** — the largest node by CPU/memory (both static allocatable and free-right-now), plus any namespace `ResourceQuota`/`LimitRange` objects.

Free-capacity accounting requires cluster-wide pod listing, which many users on a shared cluster don't have permission for. If that call is forbidden, `environment.yml` is still written — every node's `free` just stays empty, with a warning printed.

## Hardware baseline (optional)

Static specs don't tell you how fast a node's disk or network actually is. Passing `-xhw` additionally runs a short, cluster-mutating sweep — sysbench CPU/RAM, fio against each node's own container-local scratch space, and an optional sockperf network test between nodes — and merges the results into `environment.yml` under each node's `hardware_baseline` key (network results go into a top-level `network_matrix`). It's off by default because, unlike the collectors above, it deploys and tears down real pods.

## Usage

```
bexhoma environment create [-h] [-cx CONTEXT] [-o OUTPUT] [-xhw]
                            [-xhwd HARDWARE_BASELINE_DURATION]
                            [-xhwnet {none,star,full}]
                            [-xhwt HARDWARE_BASELINE_TIMEOUT]
```

Write `environment.yml` for the current kubectl context, to the default path (`dev/catalog/environment.yml`):

```powershell
bexhoma environment create
```

Target a specific context and output path:

```powershell
bexhoma environment create -cx my-context -o dev/catalog/my-cluster.yml
```

Include the hardware baseline sweep (30s per round instead of the default 15s):

```powershell
bexhoma environment create -xhw -xhwd 30
```

Skip the inter-node network test (sysbench/fio only, no sockperf):

```powershell
bexhoma environment create -xhw -xhwnet none
```

Recommended hardware baseline settings — skip the network test, 10s per round, capped at 40 minutes wall-clock:

```powershell
bexhoma environment create -xhw -xhwnet none -xhwd 10 -xhwt 40
```

Full option reference:

```powershell
bexhoma environment create --help
```
