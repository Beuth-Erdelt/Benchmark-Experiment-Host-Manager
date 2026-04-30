# Collectors

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Overview

The `collectors` module aggregates results from one or more bexhoma experiments into a single, analysis-ready view.
Each collector wraps a benchmark-specific **evaluator** — the lower-level class that parses raw log files and result folders for a single experiment code.

```
collectors.benchbase(path, codes)        ← collector: spans N experiments
    └── get_evaluator(code)              ← evaluator: single experiment
            └── log parsing, DataFrames
```

Supported benchmark types:

| Collector class | Benchmark tool | Evaluator class |
|---|---|---|
| `collectors.benchbase` | Benchbase | `evaluators.benchbase` |
| `collectors.tpcc` | HammerDB TPC-C | `evaluators.tpcc` |
| `collectors.ycsb` | YCSB | `evaluators.ycsb` |
| `collectors.dbmsbenchmarker` | DBMSBenchmarker | `evaluators.dbmsbenchmarker` |

---

## Concepts

### Naming

* An experiment has a numeric **code**, e.g. `1775855486`.
* The SUT being tested is called a **configuration**, e.g. `PostgreSQL-A`.
* An experiment is run one or more times; the repeat counter is **experiment\_run**.
* Each run has a sequence of phases; the phase number is **client**.
* Each phase can have several parallel drivers called **pods**.
* A **connection** is the state of one configuration as seen by one pod: `<configuration>-<experiment_run>-<client>-<pod>`. Prefixed with the code it becomes globally unique: `<code>-<configuration>-<experiment_run>-<client>-<pod>`.

  Example: `1775855486-PostgreSQL-A-1-2-3` — first run, second client, third pod.

* A **phase** is the monitoring scope for one (configuration, run, client) triple: `<configuration>-<experiment_run>-<client>`.

### Aggregation

Parallel pods are aggregated into their phase. Metric type determines the aggregation function:

| Metric type | Aggregation |
|---|---|
| `counter` | `max − min` (delta over interval) |
| `ratio` | `max` |
| others | `mean` |

Multi-tenancy adds a further dimension: a single service provider may map to several configurations (container instances). Dedicated `_multitenant` methods aggregate across tenants before returning results.

---

## Quick Reference

### Configuration & Metadata

| Method | Returns | Index |
|---|---|---|
| `get_connections()` | Connection metadata for all experiments | connection name |
| `get_metrics_metadata()` | Hardware metric definitions (title, type, active) | metric key |
| `get_monitored_components(code)` | Components monitored in the workload config | component key |
| `get_workload(code)` | Raw workload properties dict | — |
| `get_evaluator(code)` | Benchmark-specific evaluator for one experiment | — |

### Monitoring — Aggregated

| Method | Returns | Index |
|---|---|---|
| `get_monitoring_aggregated_per_phase(component)` | One scalar per metric per phase, all codes combined | phase name |
| `get_monitoring_aggregated_per_phase_multitenant(component)` | Same, additionally aggregated across tenants | `code_run_client_typetenant_numtenant` |

### Monitoring — Time Series

| Method | Format | Index |
|---|---|---|
| `get_monitoring_timeseries_single(code, metric, component)` | Wide — columns are pod instances | timestamp |
| `get_monitoring_timeseries_per_phase(code, metric, component)` | Wide transposed — rows are pod instances | pod/instance |
| `get_monitoring_timeseries_all(metric, component)` | Long — all codes stacked | enumerated |
| `get_monitoring_timeseries_all_multitenant(metric, component)` | Long — all codes, tenant-annotated | enumerated |

### Performance — Benchmarking

| Method | Returns | Index |
|---|---|---|
| `get_performance_per_connection()` | Unaggregated per-pod results, all codes | connection name |
| `get_performance_aggregated_per_phase()` | Aggregated across pods, grouped by phase | phase name |
| `get_performance_aggregated_per_phase_multitenant()` | Same, with tenant metadata columns | phase name |

### Performance — Loading

| Method | Returns | Index |
|---|---|---|
| `get_loading_per_pod()` | Per-pod loading metrics, all codes | connection name |
| `get_loading_per_connection()` | Per-connection loading metrics, all codes | connection name |
| `get_loading_per_run()` | Loading metrics aggregated per experiment run | connection name |

### Utility

| Method | Description |
|---|---|
| `add_metadata(df)` | Joins connection metadata onto any monitoring DataFrame |
| `collectors.get_non_constant(df)` | Drops constant columns — highlights parameters that vary |

---

## Class `collector`

### Constructor

```python
collect = collectors.benchbase(path, codes)
```

* `path` — filesystem path containing the experiment result directories.
* `codes` — list of experiment codes to aggregate, e.g. `["1776751747", "1776754749"]`.

The constructor reads `connections.config` from the first code to build the metrics metadata table.

### Configuration & Metadata

**`get_connections()`**  
Returns a DataFrame of connection metadata for all experiments.  
Columns include: `phase`, `code`, `connection`, `configuration`, `experiment_run`, `client`, `type_tenants`, `num_tenants`, `vol_tenants`.

**`get_metrics_metadata()`**  
Returns a DataFrame listing all hardware metrics defined in the experiment, with columns `title`, `active`, `type`, `metric`.

**`get_monitored_components(code='')`**  
Returns a DataFrame of monitored component roles (e.g. `loading`, `stream`, `database`) with a `description` column.

**`get_evaluator(code='')`**  
Returns the benchmark-specific evaluator for the given experiment code. Used internally but also useful for ad-hoc access to single-experiment data.

---

### Monitoring — Aggregated

**`get_monitoring_aggregated_per_phase(component='stream')`**  
Returns one row per phase across all codes. Each metric column is reduced to a scalar using the metric-type aggregation rule (counter → delta, ratio → max, other → mean).

**`get_monitoring_aggregated_per_phase_multitenant(component='stream')`**  
Extends the above by grouping across tenants. Ratio metrics are reduced with `max`; counter metrics with `sum` (except *Total I/O Wait Time*, which uses `max`). Index is the underscore-joined group key.

---

### Monitoring — Time Series

**`get_monitoring_timeseries_single(code, metric='pg_locks_count', component='stream')`**  
Returns a wide-format DataFrame for one metric in one experiment. Rows are timestamps; columns are monitored pod instances.

**`get_monitoring_timeseries_per_phase(code, metric='pg_locks_count', component='stream')`**  
Same data as above, transposed: rows are pod instances, columns are timestamps.

**`get_monitoring_timeseries_all(metric='pg_locks_count', component='stream')`**  
Collects long-format time-series across all codes. Columns include `timestamp`, `value`, `code`, `phase`, `experiment_run`, `client`, `type_tenants`, `num_tenants`, `vol_tenants`, `metric`, `component`. Values are summed across parallel pods.

**`get_monitoring_timeseries_all_multitenant(metric='pg_locks_count', component='stream')`**  
Like `get_monitoring_timeseries_all` but annotates each row with tenant metadata from the workload config. For non-container tenancy the `tenant` column is set to `"0"`.

---

### Performance — Benchmarking

**`get_performance_per_connection()`**  
Unaggregated per-pod results concatenated across all codes. Phase, connection, and configuration columns are prefixed with the experiment code.

**`get_performance_aggregated_per_phase()`**  
Aggregates parallel pods into phases for each code, then concatenates all codes. Produces one row per phase.

**`get_performance_aggregated_per_phase_multitenant()`**  
Same as above but adds `type_tenants`, `num_tenants`, and `vol_tenants` columns from the workload configuration.

---

### Performance — Loading

**`get_loading_per_pod()`**  
Raw loading metrics for each individual pod across all codes.

**`get_loading_per_connection()`**  
Loading metrics aggregated at connection level across all codes.

**`get_loading_per_run()`**  
Loading metrics further aggregated per experiment run (one row per `code-configuration-experiment_run`).

---

### Utility

**`add_metadata(df)`**  
Enriches a monitoring DataFrame with connection metadata by attempting four join strategies in order:

1. Index vs. `phase` column
2. Shared index values
3. `phase` column join
4. Multi-tenant key join on `(code, experiment_run, client, type_tenants, num_tenants)`

**`collectors.get_non_constant(df)`**  
Standalone function. Drops all columns whose values are identical across every row — useful after `get_connections()` to surface the parameters that actually vary across experiment runs.

---

## Benchmark-Specific Subclasses

Each subclass extends `base` by providing the correct evaluator. Most data retrieval is inherited; subclasses add benchmark-specific parsing.

### `collectors.benchbase`

For [Benchbase](https://github.com/cmu-db/benchbase) experiments.

Evaluator provides access to throughput and latency time-series parsed directly from Benchbase log files:

```python
evaluate = collect.get_evaluator(code)
evaluate.get_benchmark_logs_timeseries_df_aggregated(metric, configuration, client, experiment_run)
evaluate.get_benchmark_logs_timeseries_df_single(metric, configuration, client, experiment_run)
```

`metric` is typically `"throughput"` or `"latency"`.

### `collectors.tpcc`

For [HammerDB](https://hammerdb.com/) TPC-C experiments.

Evaluator parses TPM (Transactions Per Minute) and NOPM (New Orders Per Minute) from HammerDB log output.

### `collectors.ycsb`

For [YCSB](https://github.com/brianfrankcooper/YCSB) experiments.

Loading and benchmarking are both instrumented. The evaluator additionally exposes:

```python
evaluate = collect.get_evaluator(code)
evaluate.get_loading_per_connection()
evaluate.get_loading_per_pod()
evaluate.get_benchmark_logs_timeseries_df_aggregated(metric, configuration, client, experiment_run)
evaluate.get_benchmark_logs_timeseries_df_single(metric, configuration, client, experiment_run)
```

### `collectors.dbmsbenchmarker`

For [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) experiments. Adds query-level analytics:

**`get_query_latencies(query_titles=False)`**  
Per-query latency statistics (aggregated with geometric mean across parallel pods) for all codes.

**`get_total_errors(query_titles=False)`**  
Per-query failed-execution counts for all codes.

**`get_total_warnings(query_titles=False)`**  
Per-query result-mismatch counts for all codes.

Pass `query_titles=True` to replace the numeric query index with the human-readable title from the query configuration.

---

## Minimal Example

```python
from bexhoma import collectors

path  = "/results"
codes = ["1776751747", "1776754749"]

collect = collectors.benchbase(path, codes)

# What varied across these two experiments?
df_conn = collect.get_connections()
collectors.get_non_constant(df_conn)

# Benchmarking throughput, one row per phase
collect.get_performance_aggregated_per_phase()

# Hardware monitoring summary
collect.get_monitoring_aggregated_per_phase("stream")

# CPU time-series across all codes (long format)
collect.get_monitoring_timeseries_all(metric="total_cpu_memory")

# Enrich a custom DataFrame with experiment metadata
df = collect.get_monitoring_aggregated_per_phase("stream")
collect.add_metadata(df)
```

---

## References

[1] [Benchmarking Multi-Tenant Architectures in PostgreSQL](https://doi.org/10.48786/edbt.2026.46)  
Erdelt, P.K., and Rabl T. (2026). In: *Proceedings 29th International Conference on Extending Database Technology, EDBT 2026*. OpenProceedings.org.
