# Evaluators

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Overview

The `evaluators` module parses a **single bexhoma experiment** result folder and
exposes its data as structured pandas DataFrames.
It sits one level below the [Collectors](Collectors.md), which aggregate results
across multiple experiment codes.

```
evaluators.benchbase(code, path)
    ├── log_to_df()           ← parse pod log files into DataFrames
    ├── get_df_benchmarking() ← read combined benchmarking pickle
    ├── get_df_loading()      ← read combined loading pickle
    └── get_connections_of_experiment()  ← connection/pod metadata
```

Supported benchmark types:

| Evaluator class | Benchmark tool |
|---|---|
| `evaluators.benchbase` | Benchbase |
| `evaluators.tpcc` | HammerDB TPC-C |
| `evaluators.ycsb` | YCSB |
| `evaluators.dbmsbenchmarker` | DBMSBenchmarker |

---

## Class hierarchy

```
base
└── logger
    ├── benchbase
    ├── tpcc
    ├── ycsb
    └── dbmsbenchmarker
```

`base` provides connection metadata and loading throughput helpers.
`logger` adds the log-file → DataFrame → pickle pipeline used by all
benchmark-specific subclasses.

---

## Constructor

All evaluators share the same constructor signature:

```python
from bexhoma import evaluators

ev = evaluators.ycsb(code="1777285093", path="/data/benchmarks")
```

| Parameter | Description |
|---|---|
| `code` | Experiment identifier — also the name of the result sub-folder |
| `path` | Root directory that contains the per-experiment sub-folders |
| `include_loading` | Whether loading-phase results are expected (evaluators enable this automatically) |
| `include_benchmarking` | Whether benchmarking-phase results are expected (default `True`) |

---

## Quick Reference

### DataFrame Access

| Method | Defined in | Returns |
|---|---|---|
| `get_df_benchmarking()` | `logger` | All benchmarking results for this experiment |
| `get_df_loading()` | `logger` / `ycsb` / `dbmsbenchmarker` | All loading results |
| `get_connections_of_experiment()` | `base` | Connection/pod metadata, one row per pod |
| `get_workload()` | `base` | Raw workload properties dict |
| `get_connection_config()` | `logger` | `connections.config` as a Python list |

### Type Conversion & Aggregation

| Method | Defined in | Description |
|---|---|---|
| `benchmarking_set_datatypes(df)` | all subclasses | Cast benchmarking DataFrame to correct dtypes |
| `benchmarking_aggregate_by_parallel_pods(df)` | all subclasses | Reduce parallel pods → one row per phase |
| `loading_set_datatypes(df)` | `ycsb` | Cast loading DataFrame to correct dtypes |
| `loading_aggregate_by_parallel_pods(df)` | `ycsb` | Reduce parallel loading pods → one row per phase |

### Loading Throughput

| Method | Defined in | Returns |
|---|---|---|
| `get_loading_per_connection()` | `base` / `ycsb` | Loading metrics per connection |
| `get_loading_per_run()` | `base` | Loading metrics aggregated per experiment run |
| `get_loading_per_run_multitenant()` | `base` | Loading metrics per run with tenant grouping |
| `get_loading_per_pod()` | `ycsb` | Raw loading DataFrame, one row per pod |

### Monitoring

| Method | Defined in | Returns |
|---|---|---|
| `get_monitoring_metrics()` | `logger` | List of metric keys from `connections.config` |
| `get_monitoring_metric(metric, component)` | `logger` | Time-series CSV for one metric, all connections |
| `transform_monitoring_results(component)` | `logger` | Combines per-connection CSVs into one file |

### Workflow & Testing

| Method | Defined in | Returns |
|---|---|---|
| `reconstruct_workflow(df)` | `base` / `logger` | Dict mapping configuration → `[[pods], …]` |
| `test_results()` | all | Exit code `0` if results are intact |
| `test_results_column(df, col)` | `base` | `True` if column contains no zero or NaN |

---

## Class `base`

`base` is the root evaluator. It owns the experiment folder path, error tracking,
and the connection-metadata helpers that underpin all downstream aggregation.

### Key attributes

| Attribute | Set by | Description |
|---|---|---|
| `self.path` | `__init__` | Absolute path to the experiment result folder (`{path}/{code}`) |
| `self.code` | `__init__` | Experiment identifier string |
| `self.include_loading` | `__init__` | Flag: loading-phase results expected |
| `self.include_benchmarking` | `__init__` | Flag: benchmarking-phase results expected |
| `self.workflow` | `test_results` | Reconstructed workflow dict |
| `self.workflow_errors` | `log_to_df` | Dict of parse errors keyed by filename |

### `get_connections_of_experiment()`

Returns a DataFrame of connection/pod metadata read from `connections.config`.
One row per pod (when `orig_name` is present) or per client (otherwise).

Key columns: `phase`, `code`, `connection`, `configuration`, `experiment_run`,
`client`, `pods`, `time_load`, `time_preload`, `time_generate`, `time_ingest`,
`time_postload`, `type_tenants`, `num_tenants`, `vol_tenants`, plus flattened
`host_*`, `loading_parameters_*`, `benchmarking_parameters_*`, `sut_parameters_*`,
and `arg_*` fields.

### `get_workload()`

Reads `queries.config` from the experiment folder and returns its content as
a Python dictionary.  Useful for accessing the scale factor:

```python
sf = int(ev.get_workload()['defaultParameters']['SF'])
```

### `get_loading_per_connection()`

Returns loading metrics enriched with the scale factor and a
`'Throughput [SF/h]'` column, one row per connection/pod.

### `get_loading_per_run()`

Aggregates to one row per `(code, configuration, experiment_run)` by taking the
max across connections and recomputing the throughput from the aggregated load time.

### `get_loading_per_run_multitenant()`

Like `get_loading_per_run()` but groups by
`(code, experiment_run, type_tenants, vol_tenants, num_tenants)`.

---

## Class `logger`

`logger` extends `base` with the log-file parsing and pickle-caching pipeline.
All benchmark-specific evaluators inherit from `logger`.

### Log-file pipeline

When results have not yet been cached:

```
evaluate_results()
  ├── transform_all_logs_benchmarking()
  │     └── end_benchmarking(jobname)   ← log_to_df → .df.pickle
  ├── transform_all_logs_loading()
  │     └── end_loading(jobname)        ← log_to_df → .df.pickle
  └── _collect_dfs()                    ← merges .df.pickle → .all.df.pickle
```

`get_df_benchmarking()` and `get_df_loading()` trigger this pipeline on first
call if the combined pickle does not yet exist.

### `get_df_benchmarking()`

Returns the combined benchmarking DataFrame from `bexhoma-benchmarker.all.df.pickle`,
running the log pipeline first if the file is absent.

### `get_df_loading()`

Returns the combined loading DataFrame from `bexhoma-loading.all.df.pickle`.

### `get_monitoring_metrics()`

Returns the list of metric keys defined in `connections.config`.

### `get_monitoring_metric(metric, component='loading')`

Returns a time-series DataFrame for one metric and one component role.
Rows are timestamps; columns are connection names, prefixed with `{code}-`.

### `plot(df, column, x, y, ...)`

Convenience matplotlib wrapper.  With `plot_by=None` produces a single chart
with one line per value of `column`.  With `plot_by` set, produces a grid of
sub-plots — one per group — with lines split by `column` within each sub-plot.

---

## Class `benchbase`

Evaluator for [Benchbase](https://github.com/cmu-db/benchbase) experiments.

Parses per-pod log files produced by the Benchbase benchmarking tool and exposes
throughput, goodput, and latency distribution results.

### `log_to_df(filename)`

Parses a single Benchbase pod log file.  Extracts header fields
(`connection`, `configuration`, `experiment_run`, `client`, `pod`, etc.) and
the JSON result block delimited by `####BEXHOMA####`.  Returns a one-row
DataFrame whose columns include:

* `Throughput (requests/second)`, `Goodput (requests/second)`
* `Latency Distribution.*` (25th / 50th / 75th / 90th / 95th / 99th percentile, average, min, max)
* `efficiency` (TPC-C key-and-think mode only)

### `benchmarking_set_datatypes(df)`

Casts a benchmarking DataFrame to the correct column types.

### `benchmarking_aggregate_by_parallel_pods(df, columns=['phase'])`

Reduces parallel pods to one row per group (default: per `phase`).
Throughput and goodput are summed; latency percentiles use `max`; minimum
latency uses `min`; average latency uses `mean`.

### `parse_benchbase_log_file(file_path)`

Low-level parser. Extracts per-second throughput from lines matching the
Benchbase log format and returns a list of `{'second': …, 'throughput': …}` dicts.

### `benchmark_logs_to_timeseries_df(list_logs, metric='throughput', aggregate=True)`

Builds a per-second time-series DataFrame from all pod logs matching each ID
in `list_logs`.

* `"9"` or `"Max"` in the metric name → element-wise **max** across pods
* `"Min"` in the metric name → element-wise **min**
* all others → **sum**

Returns an aggregated DataFrame indexed by `'second'` (with an `'avg'` column)
when `aggregate=True`, or a list of per-pod DataFrames when `aggregate=False`.

### `get_benchmark_logs_timeseries_df_aggregated(metric='throughput', configuration='', client='1', experiment_run='1')`

Convenience wrapper around `benchmark_logs_to_timeseries_df` with `aggregate=True`.
Filters `get_df_benchmarking()` by the given `configuration`, `client`, and
`experiment_run` to obtain the pod list.

```python
df_ts = ev.get_benchmark_logs_timeseries_df_aggregated(
    metric="throughput",
    configuration="PostgreSQL-64-8-65536",
    client=1,
    experiment_run=1)
# df_ts.index  → seconds since benchmark start
# df_ts['throughput']  → txn/sec, summed across pods
```

### `get_benchmark_logs_timeseries_df_single(metric='throughput', configuration='', client='1', experiment_run='1')`

Like the aggregated variant but returns a list of per-pod DataFrames instead.

### `get_summary_benchmark_per_connection()`

Returns benchmarking results with one row per pod, filtered to the key display
columns (experiment run, terminals, target, client, child, time, errors,
throughput, goodput, efficiency, and latency percentiles), sorted by
`(experiment_run, client, child)`.  Used by `show_summary()`.

### `get_summary_benchmark_per_phase()`

Returns benchmarking results aggregated over parallel pods (via
`benchmarking_aggregate_by_parallel_pods`), one row per phase, filtered to the
same display columns as the per-connection view plus `pod_count`.
Used by `show_summary()`.

### `get_summary_loading_per_run()`

Delegates to :class:`base`'s `get_loading_per_run()`.  Returns one row per
`(code, configuration, experiment_run)` with `time_load` and
`Throughput [SF/h]`.  Used by `show_summary()`.

---

## Class `tpcc`

Evaluator for [HammerDB](https://hammerdb.com/) TPC-C experiments.

### `log_to_df(filename)`

Parses a single HammerDB pod log file.  Key extracted columns:

* `NOPM` (New Orders Per Minute), `TPM` (Transactions Per Minute)
* `efficiency` — meaningful only when key-and-think time is enabled
* Optional latency statistics when logged: `CALLS`, `MIN [ms]`, `AVG [ms]`,
  `MAX [ms]`, `TOTAL [ms]`, `P99 [ms]`, `P95 [ms]`, `P50 [ms]`

### `benchmarking_set_datatypes(df)`

Casts all columns to the correct types.  Handles two schemas: with and without
the optional latency columns.

### `benchmarking_aggregate_by_parallel_pods(df, columns=['phase'])`

Reduces parallel pods to one row per group.  NOPM and TPM are averaged
(not summed) across pods; efficiency is recomputed after aggregation using the
tpxNOPM formula.

---

## Class `ycsb`

Evaluator for [YCSB](https://github.com/brianfrankcooper/YCSB) experiments.

Covers both the benchmarking phase and the loading phase, each with their own
aggregation helpers and time-series methods.

### `log_to_df(filename)`

Parses a single YCSB pod log file into a one-row DataFrame.  Columns include
`[OVERALL].Throughput(ops/sec)` and, depending on the workload, per-operation
statistics such as:

* `[READ].Operations`, `[READ].AverageLatency(us)`, `[READ].99thPercentileLatency(us)`, …
* `[UPDATE].*`, `[INSERT].*`, `[SCAN].*`, `[READ-MODIFY-WRITE].*`
* `[*-FAILED].*` variants for error counting

### `benchmarking_set_datatypes(df)` / `loading_set_datatypes(df)`

Cast the benchmarking or loading DataFrame columns to the correct types.
Unknown operation types are handled gracefully by conditional type application.

### `benchmarking_aggregate_by_parallel_pods(df, columns=['phase'])`

Reduces parallel benchmarking pods to one row per group.  Throughput is summed;
average latency uses mean; percentile latency uses max; minimum uses min.

### `loading_aggregate_by_parallel_pods(df, columns=['phase'])`

Same reduction logic for loading pods.

### `get_df_loading()`

Returns the combined loading DataFrame from `bexhoma-loading.all.df.pickle`.

### `get_loading_per_connection()`

Merges the aggregated loading results with connection metadata on
`(code, configuration, experiment_run)`, normalises the index, drops rows
without a recorded loading phase, and attaches the scale factor.

### `get_loading_per_pod()`

Returns the raw loading DataFrame (one row per pod) from `get_df_loading()`.

### `parse_ycsb_log_file(file_path)`

Low-level parser.  Each line produces a dict with `sec`, `total_operations`,
`current_ops_per_sec`, and a nested `metrics` dict for per-operation statistics.

### `logs_to_timeseries_df(list_logs, metric='current_ops_per_sec', aggregate=True, filetype='benchmarker')`

Core time-series builder.  `filetype` controls whether benchmarker or loading
log files are matched.  The last measurement of each pod is removed as unreliable.
Aggregation strategy:

| Metric name contains | Aggregation |
|---|---|
| `"9"` or `"Max"` | element-wise **max** |
| `"Min"` | element-wise **min** |
| `"current_ops_per_sec"` | **sum** |
| others | **sum** then divided by pod count |

### `get_benchmark_logs_timeseries_df_aggregated(metric='current_ops_per_sec', configuration='', client='1', experiment_run='1')`

Aggregated time series for the benchmarking phase, filtered by
`(configuration, client, experiment_run)`.

```python
df_ts = ev.get_benchmark_logs_timeseries_df_aggregated(
    metric="current_ops_per_sec",
    configuration="PostgreSQL-64-8-196608",
    client=2,
    experiment_run=1)
# df_ts.index  → seconds (int)
# df_ts['current_ops_per_sec']  → summed across pods
```

### `get_benchmark_logs_timeseries_df_single(metric='current_ops_per_sec', configuration='', client='1', experiment_run='1')`

Returns a list of per-pod DataFrames for the benchmarking phase.

### `get_loading_logs_timeseries_df_aggregated(metric='current_ops_per_sec', configuration='', experiment_run='1')`

Aggregated time series for the **loading** phase.  No `client` parameter —
loading pods are identified by `(configuration, experiment_run)` only.

```python
df_ts = ev.get_loading_logs_timeseries_df_aggregated(
    configuration="PostgreSQL-64-8-196608",
    experiment_run=1)
```

### `get_loading_logs_timeseries_df_single(metric='current_ops_per_sec', configuration='', experiment_run='1')`

Returns a list of per-pod DataFrames for the loading phase.

---

## Class `dbmsbenchmarker`

Evaluator for [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker)
experiments.  Uses the `dbmsbenchmarker.inspector` API rather than raw log
parsing.

### `get_inspector()`

Loads the DBMSBenchmarker inspector for this experiment.  Called automatically
by `__init__`; may be called again if `self.evaluation` is `None`.

### `get_df_loading()`

Returns loading phase timing (generate, ingest, schema, index, load) extracted
from the inspector's connection data.  Index is the DBMS name.

### `get_df_benchmarking()`

Returns a combined DataFrame of throughput and timing metrics:

* `Power@Size [~Q/h]` — power metric (derived from geometric-mean execution time)
* `Throughput@Size` — throughput metric
* `time [s]` — wall-clock benchmark duration (derived from `benchmark_start`/`benchmark_end` timestamps)
* `pod_count` — number of parallel pods

### `benchmarking_aggregate_by_parallel_pods(df, columns=['phase'])`

Reduces parallel pods to one row per group.  Geometric mean is used for
`total_timer_execution` and `Power@Size`; `Throughput@Size` is recomputed
from the aggregated timing.

### `get_total_warnings(query_titles=False)`

Returns per-query warning counts (result mismatches) as a DataFrame.
Pass `query_titles=True` to replace numeric query indexes with titles from
`queries.config`.

### `get_total_errors(query_titles=False)`

Returns per-query error counts (failed executions).

### `get_query_latencies(query_titles=False)`

Returns mean execution latency per query and DBMS, rounded to 2 decimal places.

---

## Minimal Examples

### Benchbase

```python
from bexhoma import evaluators

ev = evaluators.benchbase(code="1777285093", path="/data/benchmarks")

# All benchmarking results
df_bench = ev.get_df_benchmarking()

# Aggregate parallel pods → one row per phase
df_bench = ev.benchmarking_set_datatypes(df_bench)
df_agg   = ev.benchmarking_aggregate_by_parallel_pods(df_bench)

# Per-second throughput for one phase
df_ts = ev.get_benchmark_logs_timeseries_df_aggregated(
    metric="throughput",
    configuration="PostgreSQL-64-8-65536",
    client=1,
    experiment_run=1)
```

### YCSB

```python
ev = evaluators.ycsb(code="1777285093", path="/data/benchmarks")

# Summary DataFrames
df_bench   = ev.get_df_benchmarking()
df_loading = ev.get_df_loading()

# Connection metadata
df_conn = ev.get_connections_of_experiment()

# Loading throughput
ev.get_loading_per_connection()
ev.get_loading_per_pod()

# Benchmarking time series
ev.get_benchmark_logs_timeseries_df_aggregated(
    configuration="PostgreSQL-64-8-196608", client=2, experiment_run=1)
ev.get_benchmark_logs_timeseries_df_single(
    configuration="PostgreSQL-64-8-196608", client=2, experiment_run=1)

# Loading time series (no client dimension)
ev.get_loading_logs_timeseries_df_aggregated(
    configuration="PostgreSQL-64-8-196608", experiment_run=1)
ev.get_loading_logs_timeseries_df_single(
    configuration="PostgreSQL-64-8-196608", experiment_run=1)
```

### DBMSBenchmarker (TPC-H)

```python
ev = evaluators.dbmsbenchmarker(code="1777285093", path="/data/benchmarks")

# Throughput and power metrics
ev.get_df_benchmarking()

# Loading times
ev.get_df_loading()

# Query-level diagnostics
ev.get_query_latencies(query_titles=True)
ev.get_total_errors(query_titles=True)
ev.get_total_warnings(query_titles=True)
```

