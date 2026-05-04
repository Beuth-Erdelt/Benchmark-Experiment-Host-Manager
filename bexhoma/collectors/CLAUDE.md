# bexhoma/collectors — development notes

## Purpose

The `collectors` package aggregates results from one or more bexhoma experiments into analysis-ready DataFrames.
Each collector wraps a benchmark-specific evaluator from `bexhoma/evaluators/`.

```
collectors.<benchmark>(path, codes)   ← spans N experiment codes
    └── get_evaluator(code)           ← delegates to evaluators.<benchmark>
            └── log parsing, pickle files, DataFrames
```

---

## Class hierarchy

| Collector | Evaluator | Benchmark tool |
|---|---|---|
| `base` | `evaluators.dbmsbenchmarker` (default) | — |
| `benchbase` | `evaluators.benchbase` | Benchbase |
| `tpcc` | `evaluators.tpcc` | HammerDB TPC-C |
| `ycsb` | `evaluators.ycsb` | YCSB |
| `dbmsbenchmarker` | `evaluators.dbmsbenchmarker` | DBMSBenchmarker |

`benchbase`, `tpcc`, `ycsb`, and `dbmsbenchmarker` are thin subclasses that only override
`get_evaluator()`. All data retrieval and aggregation logic lives in `base`.

---

## Generating test data

Experiments must be run against a live Kubernetes cluster to produce result folders.
The driver script that generates the collector test data is:

```bash
bash scripts/test-docs-collector.sh
```

This script runs experiments for Benchbase, TPC-H (DBMSBenchmarker), YCSB, and HammerDB
and writes logs to `logs_tests/`:

```
logs_tests/doc_benchbase_testcase_collector_1.log
logs_tests/doc_benchbase_testcase_collector_2.log
logs_tests/doc_tpch_testcase_collector_1.log
logs_tests/doc_tpch_testcase_collector_2.log
logs_tests/doc_ycsb_testcase_collector_1.log
logs_tests/doc_ycsb_testcase_collector_2.log
logs_tests/doc_hammerdb_testcase_collector_1.log
logs_tests/doc_hammerdb_testcase_collector_2.log
```

Multi-tenant variants (schema / database / container tenancy) are also generated:

```
logs_tests/doc_benchbase_testcase_collector_tenants_schema.log
logs_tests/doc_benchbase_testcase_collector_tenants_database.log
logs_tests/doc_benchbase_testcase_collector_tenants_container.log
logs_tests/doc_tpch_testcase_collector_tenants_schema.log
...
```

---

## Interactive exploration (notebooks)

The `dev/` folder contains Jupyter notebooks for each collector type:

```
dev/Collector-YCSB.ipynb
dev/Collector-Benchbase.ipynb
dev/Collector-TPC-H.ipynb
dev/Collector-HammerDB.ipynb
```

Typical notebook pattern:

```python
from bexhoma import collectors

path  = r"D:\data\benchmarks"
codes = ["1777285093", "1776792746"]

collect = collectors.ycsb(path, codes)

# Inspect what varies across the two experiments
collectors.get_non_constant(collect.get_connections()).T

# Connection and metric metadata
collect.get_metrics_metadata()
collect.get_monitored_components()

# Monitoring aggregates and time series
collect.get_monitoring_aggregated_per_phase("stream")
collect.get_monitoring_timeseries_per_phase(codes[0], metric="cpu_throttled_seconds_total", component="stream")
collect.get_monitoring_timeseries_all(metric="cpu_throttled_seconds_total")

# Benchmarking performance
collect.get_performance_per_connection()
collect.get_performance_aggregated_per_phase()

# Loading performance
collect.get_loading_per_pod()
collect.get_loading_per_run()

# YCSB-specific: benchmark time series (per configuration, client, experiment_run)
collect.get_benchmark_timeseries_per_phase()
collect.get_benchmark_timeseries_all()

# YCSB-specific: loading time series (per configuration, experiment_run; no client dimension)
collect.get_loading_timeseries_per_phase()
collect.get_loading_timeseries_all()

# Direct evaluator access for a single experiment
ev = collect.get_evaluator(code=codes[0])
ev.get_benchmark_logs_timeseries_df_aggregated(configuration="PostgreSQL-64-8-65536", experiment_run=1, client=2)
ev.get_benchmark_logs_timeseries_df_single(configuration="PostgreSQL-64-8-65536", experiment_run=1, client=2)
ev.get_loading_logs_timeseries_df_aggregated(configuration="PostgreSQL-64-8-65536", experiment_run=1)
ev.get_loading_logs_timeseries_df_single(configuration="PostgreSQL-64-8-65536", experiment_run=1)
```

---

## Documentation

The user-facing reference is `docs/Collectors.md`.
Update it whenever methods are added, renamed, or their return shapes change.

---

## Conventions

### Docstrings
All public methods use Sphinx-style docstrings:
```python
def my_method(self, param='default'):
    """
    One-line summary.

    Longer description when behaviour is non-obvious.

    :param param: What this controls.
    :type param: str
    :return: What is returned.
    :rtype: pandas.DataFrame
    """
```

### Adding a new method to base
Follow the existing pattern:
- iterate over `self.codes`
- call `self.get_evaluator(code)` inside the loop
- guard empty DataFrames with `if df.empty: continue` or `if len(df) > 0`
- concatenate with `pd.concat([df_all, df.copy()])`
- return the combined DataFrame

### Adding a benchmark-specific time-series method (benchbase / ycsb)
The benchmarking phase groups by `(configuration, client, experiment_run)`.
The loading phase (ycsb only) groups by `(configuration, experiment_run)` — no `client` dimension.

Wide format (`_per_phase`): index = second, one column per phase labelled `{code}-{configuration}-{client}-{experiment_run}`.

Long format (`_all`): columns `second`, `code`, `configuration`, `client`, `experiment_run`, `metric`, `value` plus connection metadata joined from `get_connections(evaluation)`.

### Local variable naming
- `evaluation` — the evaluator instance for one code inside a loop
- `df_all` / `df_code` / `df_result` / `df_timeseries` — accumulator DataFrames
- `df_long` — the per-phase long-format slice before concatenation
- `join_keys` — the list of columns used as the merge key when attaching metadata
- `extra_cols` — metadata columns to carry over (excludes `connection` and `phase`)
