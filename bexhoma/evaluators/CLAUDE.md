# bexhoma/evaluators — development notes

## Purpose

The `evaluators` package parses a single bexhoma experiment result folder and
exposes its data as structured pandas DataFrames.

```
evaluators.<benchmark>(code, path)
    ├── log parsing (log_to_df, parse_*_log_file)
    ├── pickle caching (end_benchmarking, end_loading, _collect_dfs)
    ├── DataFrame access (get_df_benchmarking, get_df_loading)
    ├── connection metadata (get_connections_of_experiment)
    └── aggregation helpers (benchmarking_set_datatypes,
                             benchmarking_aggregate_by_parallel_pods, …)
```

---

## Class hierarchy

| Evaluator | Benchmark tool | Extra capabilities |
|---|---|---|
| `base` | — | connection metadata, loading throughput |
| `logger` | — | log file → pickle pipeline, `plot()` |
| `benchbase` | Benchbase | per-second throughput time series |
| `tpcc` | HammerDB TPC-C | NOPM/TPM + optional latency stats |
| `ycsb` | YCSB | per-second throughput time series (bench + loading) |
| `dbmsbenchmarker` | DBMSBenchmarker | query latency, power/throughput metrics |

`benchbase`, `tpcc`, `ycsb`, and `dbmsbenchmarker` all extend `logger`, which
extends `base`.

---

## Constructor signature

All evaluators share the same constructor signature (inherited from `base`):

```python
evaluator = evaluators.ycsb(code="1777285093", path="/data/benchmarks")
```

| Parameter | Description |
|---|---|
| `code` | Experiment identifier — also the name of the result sub-folder |
| `path` | Root directory that contains the per-experiment sub-folders |
| `include_loading` | Whether loading-phase results are expected (default varies) |
| `include_benchmarking` | Whether benchmarking-phase results are expected (default `True`) |

---

## Key methods (common across evaluators)

| Method | Returns |
|---|---|
| `get_df_benchmarking()` | DataFrame of all benchmarking results |
| `get_df_loading()` | DataFrame of all loading results |
| `get_connections_of_experiment()` | DataFrame of connection/pod metadata |
| `get_connection_config()` | `connections.config` as a Python list |
| `get_workload()` | `queries.config` as a Python dict |
| `get_loading_per_connection()` | Loading metrics per connection |
| `get_loading_per_run()` | Loading metrics aggregated per experiment run |
| `get_loading_per_run_multitenant()` | Loading metrics aggregated per tenant group |
| `benchmarking_set_datatypes(df)` | Cast benchmarking DataFrame to correct dtypes |
| `benchmarking_aggregate_by_parallel_pods(df)` | Aggregate parallel pods → one row per phase |
| `reconstruct_workflow(df)` | Infer the workflow structure from results |

---

## Time-series methods (benchbase and ycsb)

### benchbase

```python
ev = evaluators.benchbase(code=code, path=path)

# Aggregated time series (all pods combined)
ev.get_benchmark_logs_timeseries_df_aggregated(
    metric="throughput", configuration="PostgreSQL-64-8-65536",
    client=1, experiment_run=1)

# Per-pod time series (list of DataFrames)
ev.get_benchmark_logs_timeseries_df_single(
    metric="throughput", configuration="PostgreSQL-64-8-65536",
    client=1, experiment_run=1)
```

### ycsb

```python
ev = evaluators.ycsb(code=code, path=path)

# Benchmarking phase
ev.get_benchmark_logs_timeseries_df_aggregated(
    metric="current_ops_per_sec", configuration="PostgreSQL-64-8-196608",
    client=1, experiment_run=1)
ev.get_benchmark_logs_timeseries_df_single(...)

# Loading phase (no client dimension)
ev.get_loading_logs_timeseries_df_aggregated(
    metric="current_ops_per_sec", configuration="PostgreSQL-64-8-196608",
    experiment_run=1)
ev.get_loading_logs_timeseries_df_single(...)
```

Available metrics (YCSB): `current_ops_per_sec`, `READ_Avg`, `UPDATE_Avg`, `READ_99`,
`UPDATE_Max`, etc.  The metric name controls the aggregation strategy:
- Contains `"9"` or `"Max"` → element-wise **max**
- Contains `"Min"` → element-wise **min**
- All others → **sum** across pods (then divided by pod count for latency averages)

---

## dbmsbenchmarker-specific methods

```python
ev = evaluators.dbmsbenchmarker(code=code, path=path)

ev.get_total_warnings(query_titles=True)   # per-query warning counts
ev.get_total_errors(query_titles=True)     # per-query error counts
ev.get_query_latencies(query_titles=True)  # mean latency per query
```

---

## Conventions

### Docstrings
All public methods use Sphinx-style docstrings:
```python
def my_method(self, param='default'):
    """
    One-line summary.

    :param param: What this controls.
    :type param: str
    :return: What is returned.
    :rtype: pandas.DataFrame
    """
```

### Adding a new evaluator
1. Subclass `logger` (or `base` for very simple cases).
2. Override `log_to_df(filename)` to parse a single pod log into a DataFrame.
3. Override `benchmarking_set_datatypes(df)` and
   `benchmarking_aggregate_by_parallel_pods(df)` as needed.
4. Declare all instance attributes in `__init__` before calling `super().__init__`.

### Pickle caching
Results are cached as `bexhoma-benchmarker.all.df.pickle` and
`bexhoma-loading.all.df.pickle` in the experiment folder.  `get_df_benchmarking()`
and `get_df_loading()` read from these files; they are created on first access by
`evaluate_results()` → `transform_all_logs_*()` → `end_benchmarking/loading()`.

### Local variable naming
- `df` — working DataFrame inside a method
- `df_typed` — after `astype()` cast
- `df_aggregated` — accumulator in `benchmarking_aggregate_by_parallel_pods`
- `df_total` — accumulator in `*_logs_to_timeseries_df`
- `dict_grp` — per-group dict assembled before constructing a DataFrame row
- `aggregate` — dict mapping column name → aggregation function/string
