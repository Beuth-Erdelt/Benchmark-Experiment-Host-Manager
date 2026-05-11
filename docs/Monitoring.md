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

`-m` and `-mc` cover hardware metrics (CPU, memory, network, disk).
`-ma` adds DBMS-internal statistics (buffer pool hits, query rates, replication lag, etc.) scraped from an exporter sidecar.
`-ma` is currently in alpha status.

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

Hardware metrics are collected from cAdvisor via Prometheus and cover the following resource categories by default:

| Category | Metrics collected |
|---|---|
| CPU utilisation | Instantaneous utilisation (`gauge`), total CPU seconds (`counter`), user-space seconds, system seconds |
| CPU throttling | Throttled time (`gauge` and `counter`) |
| CPU by other containers | CPU used by non-DBMS containers in the same pod (`gauge` and `counter`) |
| Memory | Working set bytes (`gauge`), cached bytes including inactive file cache (`gauge`) |
| Network | Receive bytes (`counter`), transmit bytes (`counter`) — disabled by default |
| Filesystem | Read bytes (`counter`), write bytes (`counter`) — disabled by default |
| I/O wait | Node-level I/O wait percentage (`gauge`) |
| Per-core variance | Standard deviation of per-core CPU utilisation across the DBMS pod (`gauge`) |
| GPU (DCGM) | GPU utilisation, power, and memory (`gauge`) — disabled by default |

Metrics marked as disabled (`active: False` in `cluster.config`) are present in the configuration but skipped during collection.
To enable them, set `active: True` on the relevant entries.

See [Config.md](Config.md) for the full metric schema and how to add or modify metric definitions.

---

## PromQL Queries and Placeholders

Every metric definition contains a PromQL query string.
Bexhoma substitutes the following placeholders at runtime before sending the query:

| Placeholder | Substituted value |
|---|---|
| `{configuration}` | The name of the current DBMS configuration (e.g., `PostgreSQL`) |
| `{experiment}` | The numeric experiment code (e.g., `1775855486`) |
| `{host}` | The Kubernetes node hosting the SUT |
| `{gpuid}` | Pipe-separated list of GPU UUIDs present in the SUT pod |
| `{namespace}` | The Kubernetes namespace of the current context |

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

---

## Application Metrics

Application metrics are DBMS-internal statistics exposed by an exporter sidecar container running next to the DBMS.
They are enabled with `-ma` and require a compatible exporter image to be configured in the DBMS's `dockers` entry (see [DBMS.md](DBMS.md)).

Application metrics are scraped from the per-experiment Prometheus via the `service_monitoring_application` URL template, which points to the application Prometheus port (9090) of the exporter sidecar inside the cluster.

Bexhoma supports two collection patterns:

### Blackbox collection

The exporter exposes a `/probe` endpoint.
Bexhoma sends one request per database, passing the target as a query parameter.
This allows per-database metric breakdowns within a single DBMS instance.

Used by: **PostgreSQL**, **PGBouncer**

```python
'monitor': {
    'blackbox': True,
    'metrics': { ... }
}
```

### Standard collection

The exporter automatically exposes metrics for all databases in the instance via its default metrics endpoint.
No per-database probing is needed.

Used by: **MySQL**, **TiDB**, **TiKV**, **Placement Driver**, **YugabyteDB**, **CockroachDB**, **Dragonfly**, **Redis**

```python
'monitor': {
    'blackbox': False,
    'metrics': { ... }
}
```

### Named application metric sets

The `monitor` block in `cluster.config` defines named metric sets, one per DBMS family.
Each DBMS configuration in `dockers` references the relevant set via its `monitor.sut.metrics` or `monitor.worker.metrics` field:

| Metric set | Used by |
|---|---|
| `postgresql` | PostgreSQL, PGBouncer (SUT component) |
| `pgbouncer` | PGBouncer (pool component) |
| `mysql` | MySQL, MariaDB |
| `tidb` | TiDB (SQL layer) |
| `tikv` | TiDB (TiKV storage) |
| `pd` | TiDB (Placement Driver) |
| `yb-master` | YugabyteDB (master nodes) |
| `yb-tserver` | YugabyteDB (tablet servers) |
| `cockroachdb` | CockroachDB (worker nodes) |
| `dragonfly` | Dragonfly |
| `redis` | Redis |

Each named set follows the same metric schema as the hardware metrics (`type`, `active`, `metric`, `query`, `title`).
The `type` field must be `application` so bexhoma routes queries to `service_monitoring_application` rather than `service_monitoring`.

---

## Timing Adjustments

Prometheus scrapes metrics at fixed intervals (typically every 15–60 seconds), so there is always some lag between when an event occurs and when the metric appears.
Two configuration keys in `cluster.config` compensate for this:

| Key | Effect |
|---|---|
| `extend` | Widens each monitoring interval by this many seconds on both ends: `[t, t']` → `[t − extend, t' + extend]`. The default of 20 s absorbs minor clock skew and scrape latency. |
| `shift` | Shifts the entire interval forward: `[t, t']` → `[t + shift, t' + shift]`. Useful when container clocks are systematically ahead of the Prometheus clock. |

See [Config.md](Config.md) for how to set these values.
