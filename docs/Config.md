# Concept: Cluster Configuration

Bexhoma reads all cluster and experiment settings from a file called `cluster.config` in the working directory.
The file is a Python dict literal (parsed with `ast.literal_eval`).
A fully-commented template is provided at [`k8s-cluster.config`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config).

Copy it to `cluster.config` and adjust the sections below before running any experiment.

---

## Top-Level Structure

```python
{
    'benchmarker': { ... },   # local paths used by the orchestrator
    'credentials': { ... },   # Kubernetes cluster access and monitoring config
    'volumes':     { ... },   # benchmark data sources and init-script sets
    'instances':   { ... },   # legacy (unused in Kubernetes mode)
    'dockers':     { ... },   # DBMS configurations — see DBMS.md
}
```

---

## `benchmarker` — Local Orchestrator Paths

```python
'benchmarker': {
    'resultfolder': '/home/myself/benchmarks',
    'jarfolder':    './jars/'
},
```

| Key | Description |
|---|---|
| `resultfolder` | Absolute path on the **local machine** where experiment results are written. Must exist and be writable. This directory is also mounted into the evaluator container so results are accessible from inside the cluster. |
| `jarfolder` | Path to the directory holding JDBC driver jars. The default `./jars/` works if you keep drivers next to `cluster.config`. Only needed for SQL DBMS used with DBMSBenchmarker. |

---

## `credentials` — Kubernetes Access and Monitoring

### Cluster Contexts

```python
'credentials': {
    'k8s': {
        'appname': 'bexhoma',
        'context': {
            'my-context': {
                'namespace':    'my-namespace',
                'clustername':  'My Cluster',
                'service_sut':  '{service}.{namespace}.svc.cluster.local',
                'port':         9091,
            },
        },
        'monitor': { ... },   # see below
    }
}
```

| Key | Description |
|---|---|
| `appname` | Label applied to all Kubernetes objects created by bexhoma. Do not change — it is used for cleanup and status queries. |
| `context` | Dict of named Kubernetes contexts. The key must match a context name in your `kubeconfig`. You can define multiple clusters here and switch between them with the `-cx` CLI flag. |
| `context.<name>.namespace` | Kubernetes namespace in which bexhoma deploys all components. Ensure your kubeconfig user has `get`/`create`/`delete` rights on this namespace. |
| `context.<name>.clustername` | Human-readable label shown in experiment summaries and reports. |
| `context.<name>.service_sut` | DNS name template for reaching the SUT (System Under Test) service from within the cluster. The placeholders `{service}` and `{namespace}` are filled in automatically. The default follows the standard Kubernetes in-cluster DNS pattern. |
| `context.<name>.port` | Port on the local machine used when forwarding traffic to the SUT via `kubectl port-forward`. Defaults to `9091`. This is also the port exposed by all SUT services inside the cluster. |

To use a **second cluster** simply add another entry under `context`:

```python
'context': {
    'cluster-a': { 'namespace': 'benchmarks', ... },
    'cluster-b': { 'namespace': 'experiments', ... },
},
```

Pass `-cx cluster-b` on the command line to run an experiment on the second cluster.

---

### `monitor` — Hardware and Application Metrics

The `monitor` block sits inside `credentials.k8s` and controls how Prometheus metrics are collected during experiments.

```python
'monitor': {
    'service_monitoring':             'https://prometheus.mycluster.com/api/v1/',
    'service_monitoring_application': 'http://{service}.{namespace}.svc.cluster.local:9090/api/v1/',
    'extend': 20,
    'shift':  0,
    'metrics': {
        'total_cpu_memory':     { ... },
        'total_cpu_util':       { ... },
        'total_network_rx':     { ... },
        ...
    },
    'postgresql': { 'metrics': { ... } },
    'mysql':      { 'metrics': { ... } },
    'pgbouncer':  { 'metrics': { ... } },
    'tidb':       { 'metrics': { ... } },
    'tikv':       { 'metrics': { ... } },
    'pd':         { 'metrics': { ... } },
    'yb-master':  { 'metrics': { ... } },
    'yb-tserver': { 'metrics': { ... } },
    ...
}
```

#### Prometheus endpoints

| Key | Description |
|---|---|
| `service_monitoring` | URL of the **cluster-level** Prometheus API (`/api/v1/` suffix required). This is used for hardware metrics (CPU, memory, network, disk I/O). If a preinstalled Prometheus is running in your cluster, set its external or in-cluster URL here. Bexhoma tests reachability at the start of each experiment. |
| `service_monitoring_application` | URL template for the **per-experiment** Prometheus that bexhoma installs itself (used for application-level metrics with `-ma`). The placeholders `{service}` and `{namespace}` are substituted automatically. Leave as-is unless you have a custom application exporter setup. |

#### Timing adjustments

| Key | Description |
|---|---|
| `extend` | Number of seconds added to both ends of each monitoring interval. An interval `[t, t']` becomes `[t − extend, t' + extend]`. A value of 20 compensates for minor clock skew and scrape timing. |
| `shift` | Number of seconds to shift the entire interval forward. An interval `[t, t']` becomes `[t + shift, t' + shift]`. Useful if container clocks are systematically ahead of the Prometheus clock. |

#### Hardware metric definitions (`metrics`)

The `metrics` dict defines which cluster-level (cAdvisor / node-exporter) metrics to collect for every experiment phase.
Each entry has:

```python
'total_cpu_util': {
    'type':   'cluster',    # 'cluster' = hardware metric; 'application' = DBMS-specific
    'active': True,         # False = skip this metric
    'metric': 'gauge',      # 'gauge' (mean), 'counter' (max−min delta), or 'ratio' (max)
    'query':  '<promql>',   # PromQL; {configuration}, {experiment}, {host}, {gpuid} are substituted
    'title':  'CPU Utilization',
},
```

| Field | Values | Effect |
|---|---|---|
| `type` | `cluster` | Queried from `service_monitoring` (hardware metrics) |
| `type` | `application` | Queried from `service_monitoring_application` (DBMS-specific metrics) |
| `active` | `True` / `False` | Set to `False` to disable a metric without removing it |
| `metric` | `gauge` | Aggregated as mean over the interval |
| `metric` | `counter` | Aggregated as max − min (delta) over the interval |
| `metric` | `ratio` | Aggregated as max over the interval |
| `query` | PromQL string | Placeholders: `{configuration}`, `{experiment}`, `{host}`, `{gpuid}`, `{namespace}` |

The default set of hardware metrics covers CPU utilization, CPU throttle, memory (working set and cached), network RX/TX, filesystem read/write, I/O wait, and per-core variance.
GPU metrics (DCGM) are present but disabled by default (`active: False`).

#### Named application metric sets

In addition to the `metrics` dict, named sub-dicts define **DBMS-specific** application metrics that are scraped when application monitoring (`-ma`) is enabled for a matching DBMS.
Each DBMS configuration (in `dockers`) references one of these sets by name via its `monitor.sut.metrics` or `monitor.worker.metrics` field.

| Name | Used by |
|---|---|
| `postgresql` | PostgreSQL, PGBouncer (SUT component) |
| `pgbouncer` | PGBouncer (pool component) |
| `mysql` | MySQL |
| `tidb` | TiDB (SQL layer) |
| `tikv` | TiDB (TiKV storage) |
| `pd` | TiDB (Placement Driver) |
| `yb-master` | YugabyteDB (master nodes) |
| `yb-tserver` | YugabyteDB (tablet servers) |
| `cockroachdb` | CockroachDB (worker nodes) |
| `dragonfly` | Dragonfly |
| `redis` | Redis |

Each named set follows the same structure as `metrics` above.
See [Monitoring](Monitoring.md) for details on enabling and interpreting application metrics.

---

## `volumes` — Data Sources and Init Scripts

The `volumes` section maps each benchmark type to a set of named init-script sequences.
Experiment scripts (`tpch.py`, `ycsb.py`, etc.) reference these by the volume key and script-set name.

```python
'volumes': {
    'tpch': {
        'id': '2',
        'initscripts': {
            'Schema': [
                'initschema-tpch.sql',
            ],
            'Index_and_Constraints': [
                'initindexes-tpch.sql',
                'initconstraints-tpch.sql',
            ],
            'Index_and_Constraints_and_Statistics': [
                'initindexes-tpch.sql',
                'initconstraints-tpch.sql',
                'initstatistics-tpch.sql',
            ],
        }
    },
    'tpcds':    { 'id': '1', 'initscripts': { ... } },
    'tpcc':     { 'id': '1', 'initscripts': { ... } },
    'ycsb':     { 'id': '1', 'initscripts': { ... } },
    'benchbase': { 'id': '1', 'initscripts': { ... } },
    ...
}
```

### Volume keys and `id`

| Field | Description |
|---|---|
| key (`tpch`, `ycsb`, …) | Identifier referenced by experiment scripts to locate the correct init-script set |
| `id` | A numeric tag appended to the Kubernetes PVC name to allow multiple incompatible data formats for the same benchmark to coexist on the cluster (e.g., switching between columnar and row-store schemas without overwriting data). Changing `id` effectively creates a new storage volume. |

### `initscripts` — named script sequences

Each entry under `initscripts` is a named list of files.
Experiment CLI flags (`-ii`, `-ic`, `-is`) control which sets are executed and when:

| Flag | Typical script set | When it runs |
|---|---|---|
| (none) | `Schema` | Before data ingestion: creates the empty schema |
| `-ii` | `Index` | After data ingestion: creates indexes |
| `-ic` | `Index_and_Constraints` | After data ingestion: creates indexes and foreign key constraints |
| `-is` | `Index_and_Constraints_and_Statistics` | After indexes/constraints: refreshes query planner statistics |

Scripts are executed in list order.
The file suffix determines how they are executed:

| Suffix | Execution |
|---|---|
| `.sql` | Piped to the DBMS command-line client via the `loadData` command from the `dockers` entry |
| `.sh` | Executed as a shell script inside the SUT container |

Script files must be present in the benchmark's experiment config folder, e.g., `experiments/tpch/<DBMS>/` for TPC-H.
See [DBMS](DBMS.md) for per-DBMS DDL script locations.

### Placeholders in init scripts

Init scripts may use these placeholders, which bexhoma substitutes at runtime:

| Placeholder | Value |
|---|---|
| `{BEXHOMA_DATABASE}` | Target database name (used in database-per-tenant mode) |
| `{BEXHOMA_SCHEMA}` | Target schema name (used in schema-per-tenant mode) |

### Volumes defined in the default config

| Key | Benchmark | Typical script sets |
|---|---|---|
| `tpch` | TPC-H | `Schema`, `Schema-Columnar`, `Schema_dummy`, `Index`, `Index_and_Constraints`, `Index_and_Constraints_and_Statistics`, `Schema_tenant`, `Index_and_Constraints_and_Statistics_tenant`, `SF1`, `SF10`, `SF30`, `SF100`, `SF300` (each with optional `-index` and `-index-constraints` variants) |
| `tpcds` | TPC-DS | `Schema`, `Schema_dummy`, `Index`, `Index_and_Constraints`, `Index_and_Constraints_and_Statistics`, `SF1`, `SF10`, `SF30`, `SF100` (each with optional `-index` and `-index-constraints` variants) |
| `tpcc` | HammerDB / Benchbase TPC-C | `Schema`, `Checks` |
| `ycsb` | YCSB | `Schema`, `Checks` |
| `benchbase` | Benchbase | `Empty`, `Schema`, `Checks`, `Schema_tenant`, `Checks_tenant` |

---

## `instances` — Legacy IaaS Settings

```python
'instances': {},
```

This section is a remnant of an earlier IaaS (VM-based) deployment mode.
It is **not used** in Kubernetes mode and should be left empty.

---

## `dockers` — DBMS Configurations

The `dockers` section defines how each DBMS is started, connected to, and monitored.
See [DBMS](DBMS.md) for the full reference and per-DBMS configuration snippets.

---

## Minimal Working Configuration

The minimum set of changes required to run the first experiment on a new cluster:

1. Set `benchmarker.resultfolder` to a local directory that exists and is writable.
2. Under `credentials.k8s.context`, add an entry whose key matches a context in your `kubeconfig`, and set `namespace` to the Kubernetes namespace you have access to.
3. Set `credentials.k8s.monitor.service_monitoring` to the URL of a Prometheus instance in your cluster, or leave it as a placeholder if you have no preinstalled Prometheus (bexhoma will install one per experiment).
4. Ensure the storage classes referenced in `k8s/pvc-bexhoma-results.yml` and `k8s/pvc-bexhoma-data.yml` exist in your cluster and support `ReadWriteMany` access.

Everything else can be left at its default values for a first run.
