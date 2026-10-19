# Concept: Monitoring

Bexhoma automatically observes resource consumption of every cluster component during each benchmark phase and stores the metrics alongside the experiment results.
Metrics are fetched from Prometheus after each phase completes and are included in the experiment summary and in the result files consumed by evaluators and collectors.

---

## Monitoring Modes

Three CLI flags control how deeply bexhoma monitors an experiment:

| Flag | Scope | What is deployed |
|---|---|---|
| (none) | No monitoring | No metrics are collected |
| `-m` | SUT only | cAdvisor sidecar in the SUT pod + per-experiment Prometheus |
| `-mc` | All components | cAdvisor DaemonSet on every node + per-experiment Prometheus |
| `-ma` | Application metrics | DBMS-specific exporter sidecar (e.g., pgexporter) + same Prometheus |

`-m` and `-mc` cover hardware metrics (CPU, memory, network, disk). Network and disk metrics need a preinstalled Prometheus whose exporters report them: the cAdvisor bexhoma installs itself runs with `--disable_metrics disk,network,...` (see below).
`-ma` adds DBMS-internal statistics (buffer pool hits, query rates, replication lag, etc.) scraped from an exporter sidecar.
`-ma` is currently in alpha status.

Which hardware metrics are collected is decided by each metric's `active` flag in `cluster.config` (see [Config](Config.md)).
`-mm` overrides that flag for a single experiment, e.g. `-mm total_gpu_util=on,total_network_rx=off`, and needs `-m` or `-mc`.
Unknown keys stop the experiment before anything is deployed, and the four CPU/RAM metrics the summary reads (`total_cpu_util_s`, `total_cpu_util`, `total_cpu_memory`, `total_cpu_memory_cached`) cannot be switched off.
`bexhoma environment create` lists the available keys under `monitoring.hardware` in `environment.yml` (see [Environment](Environment.md)); in an agent's `experiment.yml`, `observe.metrics` is a list of the keys the hypothesis relies on, which are switched on (it cannot switch metrics off) and must be given whenever hardware monitoring is on.

---

## Prometheus and cAdvisor Provisioning

Bexhoma uses Prometheus as the metrics store and cAdvisor as the container metrics exporter.
At the start of each experiment, bexhoma tests whether the configured Prometheus URL is reachable by sending a `query_range` request from inside the dashboard pod.
Based on the result, it takes one of two paths:

### Preinstalled Prometheus

If your cluster already has a Prometheus server (common in production and managed clusters), set `service_monitoring` in `cluster.config` to its URL and bexhoma will use it directly.
No additional components are installed.

### Auto-Installed Prometheus

If no preinstalled Prometheus is reachable, bexhoma installs the required components automatically:

| Monitoring mode | cAdvisor | Prometheus |
|---|---|---|
| `-m` | Sidecar container in the SUT pod | One per experiment |
| `-mc` | DaemonSet on every cluster node | One per experiment |

All installed components are labelled with the experiment code and removed during the cleanup phase.
The per-experiment Prometheus is configured at startup to scrape the cAdvisor instances bexhoma just deployed.

#### Kubernetes manifest templates

| Component | Template file |
|---|---|
| cAdvisor sidecar (per SUT) | `k8s/deploymenttemplate-PostgreSQL.yml` (and equivalents for other DBMS) |
| cAdvisor DaemonSet (cluster-wide) | `k8s/daemonsettemplate-monitoring.yml` |
| Prometheus server | `k8s/deploymenttemplate-bexhoma-prometheus.yml` |

cAdvisor runs in a container named `cadvisor` with a service port named `port-monitoring` on port 9300.
Prometheus runs with a service port named `port-prometheus` on port 9090.

---

## Hardware Metrics

Hardware metrics come from cAdvisor (per container), node-exporter (per node) and DCGM (per GPU) via Prometheus. The default definitions in `cluster.config` (key, kind and unit) are:

| Category | Metrics (key: kind) | Source |
|---|---|---|
| CPU | `total_cpu_util` CPUs in use (`gauge`), `total_cpu_util_s` CPU seconds (`counter`), `total_cpu_util_user_s` / `total_cpu_util_sys_s` user and system seconds (`counter`) | container |
| CPU throttling | `total_cpu_throttled` throttled seconds per second (`gauge`), `total_cpu_throttled_s` throttled seconds (`counter`); both `sparse` | container |
| CPU of other containers in the pod | `total_cpu_util_others` (`gauge`), `total_cpu_util_others_s` (`counter`) — disabled by default | container |
| Memory | `total_cpu_memory` working set in MiB (`gauge`), `total_cpu_memory_cached` usage including page cache in MiB (`gauge`) | container |
| Network | `total_network_rx` / `total_network_tx` MiB received / sent (`counter`) | pod |
| Filesystem | `total_fs_read` / `total_fs_write` MiB read / written (`counter`), largest device per pod | container |
| Per-core utilisation | `max_core_util` busiest core in % (`ratio`), `core_variance` variance of the per-core busy share in %² (`ratio`) | node |
| I/O wait | `io_wait_pct` share of busy CPU time spent in I/O wait in % (`ratio`), `io_wait_total` I/O wait CPU seconds (`counter`) | node |
| GPU (DCGM) | `total_gpu_util` %, `total_gpu_power` W, `total_gpu_memory` MiB, each summed over the pod's GPUs (`gauge`) — disabled by default | GPU |
| Ceph pool | `ceph_pool_write` / `ceph_pool_read` MiB, `ceph_pool_write_ops` / `ceph_pool_read_ops` operations (`counter`), all clients of the pool | Ceph pool |
| Ceph volume | `ceph_volume_write` / `ceph_volume_read` MiB, `ceph_volume_write_ops` / `ceph_volume_read_ops` operations (`counter`), `ceph_volume_write_latency` / `ceph_volume_read_latency` ms as Ceph sees it (`gauge`) | the SUT's own RBD volume(s) |
| Ceph other volumes | `ceph_others_write_rate` MiB/s, `ceph_others_write_ops_rate` / `ceph_others_read_ops_rate` operations/s (`gauge`), every other volume in the same pool | Ceph pool |

Node-level metrics describe the whole node the SUT runs on, including other workloads on it, not only the SUT container.
The Ceph metrics are explained in [Ceph storage metrics](#ceph-storage-metrics) below.
The filesystem metrics take the largest device per pod because cAdvisor reports a RAID device and each of its member disks; summing over devices would count every read and write several times.
They count block-device I/O: a volume on a network filesystem (e.g. CephFS, NFS) does its I/O over the network, so it shows in the network metrics instead, and filesystem metrics compare storage backends fairly only when all of them are block devices.

Metrics marked as disabled (`active: False` in `cluster.config`) are present in the configuration but skipped during collection.
To enable them, set `active: True` on the relevant entries, or switch them per experiment with `-mm`.
`bexhoma environment create` records under `monitoring.hardware` whether the cluster's Prometheus actually has data for each metric (`available`).

### Metric kinds

A metric's `metric` field says how its time series is reduced to one value per phase:

| Kind | Reduced to | Use for |
|---|---|---|
| `counter` | the increase during the phase: the sum of its rises (a drop, e.g. a pod leaving the sum, is not subtracted); for a job selected by its own pods also its first value, else maximum − minimum (see [Pods of a phase](#pods-of-a-phase)) | queries returning an ever-growing total, e.g. CPU seconds |
| `gauge` | mean | current values, and queries that already apply `rate()` (a value per second) |
| `ratio` | maximum | ratios and per-node peaks |

A title names the unit in brackets, and says "since Start" or "since Stats Reset" when the value is an average over the server's lifetime rather than over the phase.

See [Config.md](Config.md) for the full metric schema and how to add or modify metric definitions.

---

## PromQL Queries and Placeholders

Every metric definition contains a PromQL query string.
Bexhoma substitutes the following placeholders at runtime before sending the query:

| Placeholder | Substituted value |
|---|---|
| `{configuration}` | The name of the current DBMS configuration, lower-case (e.g., `postgresql-1`) |
| `{experiment}` | The numeric experiment code (e.g., `1775855486`) |
| `{pods}` | A regex of the pods the query is about, per query set (see [Pods of a phase](#pods-of-a-phase)) |
| `{namespace}` | The namespace of the cluster context |
| `{host}` | The Kubernetes node hosting the SUT |
| `{gpuid}` | Pipe-separated list of GPU UUIDs present in the SUT pod |
| `{database}` | The database name (the tenant's database in database-per-tenant mode) |
| `{schema}` | The schema name (the tenant's schema in schema-per-tenant mode) |
| `{storage_class}` | The StorageClass of the configuration's PVC (the cluster default resolved when `-rst ''`) |
| `{pool}` | The Ceph pool behind that StorageClass (`parameters.pool` of a Ceph CSI class) |
| `{rbd_images}` | The RBD images behind the configuration's PVCs, as a regex alternation (`csi-vol-a\|csi-vol-b`) |

The three storage placeholders are filled once per configuration after the SUT is deployed, and only when some query uses them.
When one cannot be filled, every metric that uses it is switched off for that configuration (see below), so it is neither fetched with an empty label nor reported as missing.

Because bexhoma uses Python's `str.format()` for substitution, literal PromQL label selector braces `{}` must be written as `{{}}` in the config:

```python
# PromQL:  container_cpu_usage_seconds_total{container="dbms"}
# In config:
'query': 'sum(container_cpu_usage_seconds_total{{container="dbms"}})'
```

### Container label substitution

The container label `"dbms"` in queries targets the SUT container.
Bexhoma automatically produces parallel queries for other container roles by substituting this label:

| Container role | Label value |
|---|---|
| SUT (DBMS) | `dbms` |
| Data generator | `datagenerator` |
| Sensor / sidecar | `sensor` |
| Benchmarker driver | `dbmsbenchmarker` |

This means a single metric definition covers all components without requiring separate query entries for each.

### Pods of a phase

A stopped pod's cAdvisor series does not end when the pod stops: Prometheus keeps returning its last value for about five minutes.
A query by name pattern then still sums the previous repetition's SUT or the previous round's benchmarker into the next phase (its Max RAM, its CPU total).
The cAdvisor queries in `k8s-cluster.config` handle this in two ways:

- **`{pods}`**: each connection file holds one query set per scope, each with its own pod regex:

  | Query set | `{pods}` | Used for |
  |---|---|---|
  | `metrics` | `(.*)<configuration>-<experiment>(.*)` | the SUT and other deployments |
  | `metrics_benchmarker` | `<benchmarker job name>-[a-z0-9]{5}` | the benchmarker job of exactly this connection |
  | `metrics_loading` | `bexhoma-loading-<configuration>-<experiment>-<run>-.+` | all loading jobs of this repetition (loader, data generator) |
  | `metrics_<statefulset>` | `(.*)<worker name>-(.*)` | workers |

  The job names are those of the job manifests, so a job's queries see only its own pods, whatever the gap to the previous round.
  Several benchmarker jobs in one round each get their own row instead of the sum of all of them.
- **Stale series filter**: every instant selector `X` is written `(X and (time() - timestamp(X)) < 90)`, which drops a series whose newest sample is older than 90 s.
  This keeps the previous SUT pod out of the next repetition, which starts minutes later.
  The `irate(...)` queries need no filter: a stale series has rate 0.
  The threshold assumes a scrape interval of about 30 s; with a longer `scrape_interval`, raise the `90` in the queries to about three intervals.

`{namespace}` keeps pods of other namespaces out: worker pod names carry no experiment code.

A scoped job's counter starts at 0 before its first scrape, so its first value counts as growth: a loader with a single scrape gets its CPU total instead of 0.
Whether a connection is scoped is read from its stored queries (its job query set differs from `metrics`); a `cluster.config` copy with the old literal pod pattern gives job query sets equal to `metrics` and keeps the old rule (`max - min`) without any message.
To use the new queries, copy the cAdvisor metric definitions of `k8s-cluster.config` into your `cluster.config`.

---

## Ceph Storage Metrics

When the SUT's volume lives on Ceph, the Ceph manager's Prometheus exporter tells what happened on the storage side during each phase: the SUT's own volume, every other volume in the same pool, and the pool as a whole.
The cluster and its Ceph pools are normally shared and busy, so load from other volumes is the usual operating condition, not a fault.
It matters for an interpretation when it differs between the configurations or phases being compared.
In a sweep that compares a Ceph class with node-local or in-memory storage, exposure to the shared pool is part of what distinguishes the storage backends, not a confounder between them.

### Where they apply

The metrics need Ceph CSI storage. On other storage they are switched off per configuration, and the configuration's `storage_monitoring` record in `connections.config` says why:

| Storage (`-rst`) | Pool metrics | Volume and other-volume metrics |
|---|---|---|
| none (ephemeral), `ramdisk` | off, no Kubernetes call | off |
| Ceph RBD class (e.g. `cephcsi`, `nvme`), also as the cluster default `''` | on | on |
| CephFS class (e.g. `shared`) | on | off: CephFS has no per-volume statistics |
| other provisioner, legacy Rook FlexVolume class | off | off |
| StorageClass unreadable, PVC without a bound RBD image | as far as resolved | off |
| Prometheus has no Ceph series for the pool, or could not be asked | off | off |

Bexhoma checks once per pool, through the dashboard pod, whether Prometheus reports the pool (`ceph_pool_metadata`) and keeps per-image statistics for it (`ceph_rbd_write_bytes`).
A metric that is off for one configuration still appears for the others: in a storage-class sweep over `nvme` and `ramdisk`, `monitoring.md` shows the `nvme` values and `n/a (ramdisk: no Ceph volume)` for the other configuration.

`environment.yml` records per storage class which Ceph metrics it supports (`ceph`), and per metric what it `needs` (`ceph_pool` or `ceph_volume`).
An experiment that lists such a metric in `observe.metrics` is refused when none of its storage classes can serve it.

### Reading them

* **This SUT** (`ceph_volume_*`) counts the SUT's own volume(s). A new image appears in the exporter after a short delay with its counter already including the earlier writes, and the query reports 0 until then, so a phase's increase is complete once the image is listed.
* **Other volumes** (`ceph_others_*`) are rates averaged over the phase, because volumes appear and disappear while a phase runs. Other pools on the same disks are not counted.
* **All clients** (`ceph_pool_*`) is the whole pool. It does not reconcile exactly with the sum of the volumes; compare volumes with volumes.
* The exporter's counters lag the I/O by about 1–2 minutes, which matters most for phases shorter than about 5 minutes.
* Across configurations of one experiment, pool and other-volume values take the maximum instead of the sum, because the configurations share the pool.

---

## Application Metrics

Application metrics are DBMS-internal statistics exposed by an exporter sidecar container running next to the DBMS.
They are enabled with `-ma` and require a compatible exporter image to be configured in the DBMS's `dockers` entry (see [DBMS.md](DBMS.md)).

Application metrics are scraped from the per-experiment Prometheus via the `service_monitoring_application` URL template, which points to the application Prometheus port (9090) of the exporter sidecar inside the cluster.
They are only collected for the SUT's loading and benchmarking phases, not for loader, benchmarker or data generator pods.

Bexhoma supports two collection patterns, chosen per DBMS in its `dockers` entry:

### Blackbox collection

The exporter is probed once per database, with the target passed as a query parameter.
This allows per-database metric breakdowns within a single DBMS instance (e.g. one database per tenant).
The DBMS sets `blackbox: True` and a `blackbox_target` template, in which `{database}` is replaced by each database name:

Used by: **PostgreSQL**, **PgDuckDB**

```python
'monitor': {
    'sut': {
        'metrics': 'postgresql',
        'blackbox': True,
        'blackbox_target': 'postgres@localhost:5432/{database}?sslmode=disable',
    },
},
```

### Standard collection

The exporter automatically exposes metrics for all databases in the instance via its default metrics endpoint.
No per-database probing is needed; `blackbox` is `False` or left out.

Used by: **MySQL**, **PGBouncer**, **TiDB**, **TiKV**, **Placement Driver**, **YugabyteDB**, **CockroachDB**, **Dragonfly**, **Redis**

### Named application metric sets

The `monitor` block in `cluster.config` defines named metric sets, one per DBMS family.
Each DBMS configuration in `dockers` references the relevant set by component (`monitor.sut.metrics`, `monitor.worker.metrics`, and so on):

| Metric set | Used by |
|---|---|
| `postgresql` | PostgreSQL, PgDuckDB, PGBouncer (SUT component) |
| `pgbouncer` | PGBouncer (pool component) |
| `mysql` | MySQL |
| `tidb` | TiDB (SQL layer) |
| `tikv` | TiDB (TiKV storage) |
| `pd` | TiDB (Placement Driver) |
| `yb-master` | YugabyteDB (master nodes) |
| `yb-tserver` | YugabyteDB (tablet servers) |
| `cockroachdb` | CockroachDB (worker nodes) |
| `dragonfly` | Dragonfly, DragonflyCluster (worker nodes) |
| `redis` | Redis (worker nodes) |

Each named set follows the same metric schema as the hardware metrics (`type`, `active`, `metric`, `query`, `title`, optional `sparse`).
The `type` field must be `application` so bexhoma routes queries to `service_monitoring_application` rather than `service_monitoring`.

---

## Missing Metrics

When Prometheus returns no data for a query, dbmsbenchmarker does not fail: it logs `Metrics missing for <title> (<query>)` and stores a series of zeros, which would otherwise read like a measured idle component.
Bexhoma scans the metric-fetch logs (`bexhoma-metrics-*.log`) and the benchmarker pod logs for these lines and reports each gap once, even when both processes logged it.

Some gaps are expected, and their zeros are correct:

| Reason | When |
|---|---|
| `data pre-existing` | An optional component, the data generator, had nothing to do and exited before the first scrape |
| `series exists only while non-zero` | The metric is marked `sparse: True` in `cluster.config`: its series only exists while the value is non-zero (e.g. backends waiting on locks, or CPU throttling of a container without a CPU limit) |
| `phase shorter than scrape interval` | The fetch's window was too short for the scrapes the component needs (see [Short phases](#short-phases)), so no scrape may have landed inside it |

The test `No monitoring metrics missing` fails only on unexpected gaps; when every gap is expected it is recorded as skipped, with the reasons.
The report lists all gaps in `monitoring.md`'s Missing Metrics, with an `expected` column, and counts expected and unexpected gaps separately in `index.md`'s Health Summary (see [AgentReport](AgentReport.md)).

---

## Timing Adjustments

Prometheus scrapes metrics at fixed intervals (typically every 15–60 seconds), so there is always some lag between when an event occurs and when the metric appears.
Two configuration keys in `cluster.config` adjust the interval; both default to 0:

| Key | Effect |
|---|---|
| `extend` | Widens each monitoring interval by this many seconds on both ends: `[t, t']` → `[t − extend, t' + extend]`. Only for clocks that are out of sync by a few seconds. Keep it well below the gap between phases (≤ 5 s): a wider window counts the neighbouring phase, e.g. its Max RAM. It does not make up for the scrape interval (see below). |
| `shift` | Shifts the entire interval forward: `[t, t']` → `[t + shift, t' + shift]`. Useful when container clocks are systematically ahead of the Prometheus clock. |

See [Config.md](Config.md) for how to set these values.

### Short phases

Prometheus scrapes the containers every `scrape_interval` seconds (`monitor.scrape_interval` in `cluster.config`, default 30, the cluster Prometheus' own interval; not `prometheus_interval`, which only sets bexhoma's own Prometheus).
A phase can only show what was scraped inside its window:

| Component | Shortest measurable window | Why |
|---|---|---|
| SUT, workers | 1.2 × scrape interval | their pod runs before the window, so one scrape inside it is enough |
| jobs: loader, data generator, benchmarker, selected by their own pods (`{pods}`) | 1.2 × scrape interval | their first value counts, so one scrape is enough |
| jobs with an old query (no `{pods}`) | 2 × scrape interval | a job pod starts inside the window, so its CPU total (`max - min`) needs two scrapes |

The window is the one each fetch queried, logged as `Interval length <N>s` in `bexhoma-metrics-<connection>-<component>.log`.
A connection whose window is shorter shows `n/a` instead of `CPU [CPUs]` in the summary and in the report, and is left out of the test `... contains no 0 or NaN in CPU [CPUs]`; the test is skipped when no connection of the component is measurable.
Gaps in such a fetch count as expected (`phase shorter than scrape interval`, see [Missing Metrics](#missing-metrics)).
`Max CPU` (a rate) and `Max RAM` (a gauge) keep their values; peaks between two scrapes are missed in any phase.

Even in a long phase a CPU total is only accurate to about one scrape interval: the counted span is shifted by up to one interval, and the CPU after a job pod's last scrape is never recorded.
Widening the window does not help (it counts the neighbouring phase), so `extend` stays a clock-skew knob.
Results from before this rule (fetch logs without `Interval length`) are evaluated as before.

---

## Monitoring Summary Tables

After each experiment, `show_summary()` prints one monitoring table per registered component (e.g. *Loading phase: SUT deployment*, *Execution phase: SUT deployment*).
Each row corresponds to one **benchmark job** and the `DBMS` column holds the job identifier:

```
<configuration>-<experiment_run>-<client>-<benchmark_run>
```

| Segment | Meaning | Example |
|---|---|---|
| `configuration` | Name of the SUT instance (`<docker>-<counter>`) | `PostgreSQL-1` |
| `experiment_run` | 1-based repetition index (set by `-ne`) | `1`, `2` |
| `client` | 1-based sequential client index within a run | `1`, `2` |
| `benchmark_run` | 1-based parallel benchmark job index within a client phase | `1` |

Example with two sequential clients and two experiment runs (`-ne 1,2`):

| DBMS | CPU [CPUs] | … |
|---|---|---|
| `PostgreSQL-1-1-1-1` | … | experiment_run=1, client=1, benchmark_run=1 |
| `PostgreSQL-1-1-2-1` | … | experiment_run=1, client=2, benchmark_run=1 |
| `PostgreSQL-1-2-1-1` | … | experiment_run=2, client=1, benchmark_run=1 |
| `PostgreSQL-1-2-2-1` | … | experiment_run=2, client=2, benchmark_run=1 |

### Loading phase tables

Loading phase metrics are fetched at the start of each benchmark job using the SUT's loading time window (`timeLoadingStart`–`timeLoadingEnd`).
This means:

- Every benchmark job produces one row in the loading phase table, even though the data was loaded only once.
- Rows that share the same loading window (e.g. all clients in the same experiment run) will show **identical values** — the SUT experienced the same load regardless of how many client sequences followed.
- The second experiment run re-deploys and re-loads the SUT, so its rows cover a different time window and may differ.
