# bexhoma/experiments — development notes

---

## How benchmarker results are collected

This document traces the full path from a submitted Kubernetes Job to a metric
stored in the connection file, for every benchmarker type.  It also covers the
TPC-H refresh stream case where two benchmarker jobs run in parallel within the
same client round.

---

## 1. Data structures before a job starts

### 1a. `experiment_dict` and the benchmark round list

`add_benchmark_list()` (in `configurations.py`) builds
`config.experiment_dict["benchmarker"]` from `experiment_dict_template`:

```python
experiment_dict["benchmarker"] = [
    # round 1 — one entry per job to submit in parallel
    [
        {"name": "tpch",         "benchmarker": "dbmsbenchmarker", "parallelism": 1, ...},
        {"name": "tpch-refresh", "benchmarker": "tpch_refresh",    "parallelism": 1,
         "fixed_parallelism": True, ...},
    ],
    # round 2, round 3, …
]
```

Entries with `fixed_parallelism: True` are not scaled when the `-ne` count
grows; all other entries' `parallelism` / `num_pods` are overwritten with the
client count for that round.

### 1b. The connection file (`connections.config`)

The result folder for an experiment is `{resultfolder}/{code}/`.  Two persistent
files track results:

| File | Contents |
|---|---|
| `{code}/connections.config` | Python `repr()` of a list of connection dicts — one per submitted benchmarker job |
| `{code}/{connection}.config` | Single-element version of the above for one connection; durable backup that survives dbmsbenchmarker's rewrite of `connections.config` |
| `{code}/queries.config` | Workload metadata: `SF`, `type`, `duration`, `defaultParameters`, `benchmark_sequence` |

Each connection dict has the shape:

```python
{
    'name': 'PostgreSQL-1-1-1',      # <configuration>-<experimentRun>-<client>-<benchmarkRun>
    'parameter': {
        'code': 1234567890,
        'numExperiment': '1',
        'numBenchmark': '1',         # benchmark_run (1-based position in the round)
        'client': '1',
        'parallelism': 1,
        'num_worker': 0,
        'dockerimage': 'PostgreSQL',
        'connection_parameter': {
            'loading_parameters':      {...},  # ENV vars used during loading phase
            'benchmarking_parameters': {...},  # ENV vars injected into benchmarker pods
            'sut_parameters':          {...},
        },
    },
    'hostsystem': {
        'loading_timespans': {
            'sensor':        [(start_epoch, end_epoch), ...],  # one pair per pod
            'datagenerator': [(start_epoch, end_epoch), ...],
        },
        'benchmarking_timespans': {
            'benchmarker': [(start_epoch, end_epoch), ...],   # filled by end_benchmarking()
        },
    },
    'timeLoad': ...,
    'timeSchema': ...,
    # …JDBC, monitoring, storage sections
}
```

---

## 2. Job submission: `run_benchmarker_pod()`

Source: `configurations.py`, called from `experiments/base.py::work_benchmark_list()`.

For each entry in the current client round, `run_benchmarker_pod()`:

1. Builds the **connection name**: `"{configuration}-{experimentRun}-{client}-{benchmark_run}"`.
2. Constructs the connection dict `c` (described above) and appends it to
   `connections.config`; also writes `{connection}.config` immediately.
3. Writes benchmarking parameters to a Redis queue:
   `bexhoma-{app}-benchmarker-{connection}-{code}` — one item per pod.
4. Sets the Redis **job counter**:
   `bexhoma-benchmarker-podcount-job-{connection}-{experiment}` = `parallelism`.
5. Calls `create_manifest_job()` to submit the Kubernetes Job.

`create_manifest_job()` injects `BEXHOMA_*` environment variables into every
pod container: `BEXHOMA_HOST`, `BEXHOMA_USER`, `BEXHOMA_PASSWORD`,
`BEXHOMA_DATABASE`, `BEXHOMA_SCHEMA`, `BEXHOMA_CLIENT`, `BEXHOMA_BENCHMARK_RUN`,
`BEXHOMA_EXPERIMENT`, `BEXHOMA_CONNECTION`, `BEXHOMA_CONFIGURATION`,
`BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_NUM_PODS`, plus all entries from
`config.benchmarking_parameters` (benchmark-tool-specific ENV like
`YCSB_OPERATIONS`, `BENCHBASE_TERMINALS`, `TPCH_REFRESH_STREAMS`, etc.).

**Important**: `BEXHOMA_PORT` is **not** injected dynamically — it must be
hardcoded in the k8s job template YAML.

---

## 3. Pod synchronization (Redis counters)

Before doing any work, every benchmarker pod decrements and polls two Redis
counters (three in container-tenancy mode):

| Counter | Key | Initialized to |
|---|---|---|
| Job | `bexhoma-benchmarker-podcount-job-{CONNECTION}-{EXPERIMENT}` | `parallelism` of this job |
| Round | `bexhoma-benchmarker-podcount-round-{EXPERIMENT_RUN}-{CLIENT}-{CONFIGURATION}-{EXPERIMENT}` | sum of `parallelism` across all jobs in this configuration's round |

A pod polls until the counter is `<= 0` (not `== 0`), so that a restarted pod
that decrements again still exits the poll immediately.

The round counter ensures that all jobs in a client round (e.g., the query
stream and the refresh stream) start their actual workload at the same wall-clock
moment.

---

## 4. Log retrieval: `clusters.py::store_pod_log()`

In `work_benchmark_list()`, whenever a pod transitions to `Succeeded` or
`Failed`, `cluster.store_pod_log(pod, container)` is called for every
container in the pod (via `kubectl logs`).

The log is saved to:

```
{resultfolder}/{code}/{pod_name}.{container_name}.log
```

Typical container names per job type:

| Job type | Container name | Log suffix |
|---|---|---|
| DBMSBenchmarker query stream | `dbmsbenchmarker` | `.dbmsbenchmarker.log` |
| YCSB / Benchbase / HammerDB | `dbmsbenchmarker` | `.dbmsbenchmarker.log` |
| TPC-H refresh loader | `dbmsbenchmarker` | `.dbmsbenchmarker.log` |
| TPC-H refresh generator (initContainer) | `datagenerator` | `.datagenerator.log` |
| TPC-H / TPC-DS data loader | `sensor` | `.sensor.log` |

---

## 5. Timing extraction: `end_benchmarking()`

Source: `experiments/base.py`, called immediately after a job completes,
before the job is deleted.

### 5a. `get_job_timing_benchmarking(jobname)`

Calls `extract_job_timing(jobname, container="dbmsbenchmarker")` unconditionally.
All benchmarker jobs — including the TPC-H refresh stream — must name their main
container `dbmsbenchmarker` so the log file ends with `.dbmsbenchmarker.log`.

Delegates to `extract_job_timing(jobname, container)`:

```python
def extract_job_timing(self, jobname, container):
    # Scans {path}/*.{container}.log for files whose name starts with jobname
    # From each file, regex-extracts:
    #   BEXHOMA_START:(\d+)   (Unix epoch, measured after sync barriers)
    #   BEXHOMA_END:(\d+)
    # Returns list of (int_start, int_end) tuples — one per pod
```

Every benchmarker pod script must emit these two lines at the end of its
workload section (not at script start) so that the timestamps reflect actual
work time, not container startup.

### 5b. What `end_benchmarking()` does with the timing

```python
firsts, seconds = zip(*timing_benchmarker)
start_time = min(firsts)   # earliest pod start
end_time   = max(seconds)  # latest pod end
config.benchmarking_timespans = {'benchmarker': list(zip(firsts, seconds))}
```

It then writes these timespans to:
- The `benchmarking_timespans` field of the matching entry in `connections.config`.
- The individual `{connection}.config` file (durable backup), then **immediately
  uploads that file back to the pod** via `self.experimentupload_file(connection + '.config')`.
  This upload is required because `evaluate_results()` later calls
  `experimentdownload_file('')` which downloads all pod files and would otherwise
  overwrite the locally-updated individual config with the stale pod copy (written
  at job-submission time with `benchmarking_timespans: {}`).
- The dashboard pod copy (if a dashboard is active).

If `timing_benchmarker` is empty (log not found, pod crashed before emitting
timestamps), `end_benchmarking()` prints a warning and returns without updating
either file.

---

## 6. Post-run evaluation: the evaluator pipeline

After `work_benchmark_list()` returns, `process()` calls `evaluate_results()`,
which invokes `self.evaluator.evaluate_results()`.

### 6a. Log-to-pickle pipeline (all evaluators except `dbmsbenchmarker`)

`transform_all_logs_benchmarking()`:

1. Scans the result folder for `bexhoma-benchmarker*.{container}.log` files.
2. Strips the `bexhoma-benchmarker-` prefix and pod suffix from the filename to
   get the **jobname**.
3. When `self.benchmark_run > 0`, filters to only files whose jobname ends with
   `-{benchmark_run}` (so each evaluator only processes its own logs, not a
   co-running refresh stream).
4. For each matching file, calls `self.end_benchmarking(jobname)` which calls
   `log_to_df(path)` per file, writes non-empty results to a `.df.pickle`
   sidecar, and counts empty files as `missing_dfs`.
5. `_collect_dfs()` concatenates all pickle files into a single aggregated
   DataFrame, written to `bexhoma-benchmarker.{N}.all.df.pickle`
   (`N` = `benchmark_run`, or 1 if unset).

`get_df_benchmarking()` reads from this pickle; it is created on first access
if absent.

### 6b. `dbmsbenchmarker` evaluator

Does **not** use the log-to-pickle pipeline. Instead it wraps a
`dbmsbenchmarker.inspector.inspector` instance that reads the DBMSBenchmarker
library's own result files (pickle/JSON cubes built inside the dashboard pod by
`benchmark.py read`).

---

## 7. Per-benchmarker details

### 7a. DBMSBenchmarker (`evaluators/dbmsbenchmarker.py`)

**Used by**: `tpch.py`, `tpcds.py`, and all workloads that use
`configurations.default` + `jobtemplate-benchmarking-dbmsbenchmarker.yml`.

**Log source**: DBMSBenchmarker library's own result files (read by
`dbmsbenchmarker.inspector`), not the pod stdout log.

**Columns produced by `get_df_benchmarking()`**:

| Column | Description |
|---|---|
| `code`, `configuration`, `connection` | Experiment identity |
| `experiment_run`, `client`, `benchmark_run` | Position in the -ne / -nc sweep |
| `pod_count`, `SF` | Parallelism and scale factor |
| `num_of_queries` | Number of distinct queries executed |
| `time [s]` | Total wall-clock benchmark duration (max pod end − min pod start) |
| `Geo Times [s]` | Geometric mean execution time across all queries |
| `Power@Size [~Q/h]` | `SF × 3600 / geo_mean_execution_s` |
| `Throughput@Size` | `num_queries × 3600 × pod_count / time_s × SF` |

**Aggregation**: geo-mean for `Power@Size` and `Geo Times`; max for `time [s]`;
`Throughput@Size` recomputed from aggregated values.

**Dashboard cube expansion note**: `benchmark.py read` inside the dashboard pod
rewrites `connections.config` by expanding single-connection entries into
per-pod sub-entries.  `get_connections_of_experiment()` supplements missing
connections from individual `{connection}.config` files.

`end_benchmarking()` therefore writes timing to BOTH files and immediately
uploads the individual file back to the pod so that `experimentdownload_file('')`
— called later by `evaluate_results()` — cannot overwrite the locally-updated
copy with the stale pod version (written at job-submission time with
`benchmarking_timespans: {}`).

---

### 7b. YCSB (`evaluators/ycsb.py`)

**Used by**: `ycsb.py`.

**Container**: `dbmsbenchmarker`.

**`log_to_df(filename)` parses**:

Header (one `KEY:value` line per parameter):
`BEXHOMA_CONNECTION`, `BEXHOMA_CONFIGURATION`, `SF`, `BEXHOMA_EXPERIMENT`,
`BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_CLIENT`, `BEXHOMA_BENCHMARK_RUN`,
`YCSB_TARGET`, `YCSB_THREADCOUNT`, `YCSB_WORKLOAD`, `YCSB_OPERATIONS`,
`BEXHOMA_CHILD`, `YCSB_BATCHSIZE`, `BEXHOMA_NUM_PODS`.

Result lines (YCSB format): `[SECTION], MetricName, count, value`

**Columns produced** — identity:

| Column | Source |
|---|---|
| `connection`, `configuration`, `experiment_run`, `client`, `benchmark_run` | Header |
| `threads`, `target`, `SF`, `workload`, `operations`, `batchsize`, `exceptions` | Header |
| `pod`, `pod_count`, `child` | Header |

Per-operation metrics (for each of READ, UPDATE, INSERT, SCAN, CLEANUP, READ-MODIFY-WRITE and their `-FAILED` variants):
`Operations`, `AverageLatency(us)`, `MinLatency(us)`, `MaxLatency(us)`,
`95thPercentileLatency(us)`, `99thPercentileLatency(us)`, `Return=OK`.

Plus: `[OVERALL].RunTime(ms)`, `[OVERALL].Throughput(ops/sec)`.

**Aggregation across parallel pods**: sums `Throughput`, `Operations`,
`Return=OK`; averages `AverageLatency`; takes max for `RunTime`, `MaxLatency`,
percentiles; min for `MinLatency`.

**Time series**: `parse_ycsb_log_file()` parses per-second status lines
(`N sec; M current ops/sec [SECTION: ...]`).  Metrics whose name contains `"9"`
or `"Max"` are aggregated by max; `"Min"` → min; all others → sum.

---

### 7c. Benchbase (`evaluators/benchbase.py`)

**Used by**: `benchbase.py`.

**Container**: `dbmsbenchmarker`.

**`log_to_df(filename)` parses**:

Header: `BEXHOMA_CONNECTION`, `BEXHOMA_DURATION`, `BEXHOMA_CONFIGURATION`,
`BEXHOMA_EXPERIMENT_RUN`, `BEXHOMA_CLIENT`, `BEXHOMA_BENCHMARK_RUN`,
`BEXHOMA_EXPERIMENT`, `BEXHOMA_NUM_PODS`, `BENCHBASE_BENCH`, `BENCHBASE_PROFILE`,
`BENCHBASE_TARGET`, `BENCHBASE_TIME`, `BENCHBASE_BATCHSIZE`, `BENCHBASE_KEY_AND_THINK`,
`BEXHOMA_CHILD`, `SF`, `BEXHOMA_TENANT_ID`.

JSON block between `####BEXHOMA####` markers (normalized via `pd.json_normalize()`):
`scalefactor`, `Benchmark Type`, `DBMS Version`, `DBMS Type`, `isolation`,
`terminals`, `Goodput (requests/second)`, `Throughput (requests/second)`,
`Latency Distribution.{Avg/Min/Max/25th/50th/75th/90th/95th/99th} Latency (microseconds)`.

Early exit (row with `num_errors > 0`) when `"start time has already passed"` appears
in the log (time-sync failure).

**Aggregation across parallel pods**: sums `Goodput`, `Throughput`, `terminals`,
`target`; max for latency percentiles; mean for `AverageLatency`, `batchsize`;
max for `time`, `sf`.

**TPC-C efficiency**: recomputed only when `bench == 'tpcc'` and `terminals == sf × 10`:
`0.45 × 60 × 100 × Goodput / 12.86 / sf`.

**Time series**: `parse_benchbase_log_file()` parses
`[INFO] YYYY-MM-DD HH:MM:SS,mmm ... Throughput: X txn/sec` lines; elapsed second
is computed relative to the first matching line.

---

### 7d. HammerDB TPC-C (`evaluators/tpcc.py`)

**Used by**: `hammerdb.py`.

**Container**: `dbmsbenchmarker`.

**`log_to_df(filename)` parses**:

Header: `BEXHOMA_CONNECTION`, `BEXHOMA_CONFIGURATION`, `BEXHOMA_EXPERIMENT`,
`BEXHOMA_EXPERIMENT_RUN`, `HAMMERDB_ITERATIONS`, `HAMMERDB_DURATION`,
`HAMMERDB_RAMPUP`, `SF`, `HAMMERDB_NUM_VU`, `BEXHOMA_CLIENT`,
`BEXHOMA_BENCHMARK_RUN`, `HAMMERDB_TIMEPROFILE`, `HAMMERDB_ALLWAREHOUSES`,
`HAMMERDB_KEYANDTHINK`, `BEXHOMA_CHILD`, `BEXHOMA_NUM_PODS`.

Main results — one row per test iteration:
`Vuser 1:TEST RESULT : System achieved (\d+) NOPM from (\d+) (\w+) TPM`

Optional latency block (when `HAMMERDB_TIMEPROFILE=true`):
`SUMMARY OF N ACTIVE VIRTUAL USERS` → `>>>>> PROC: NEWORD` → label-value pairs:
`CALLS`, `MIN [ms]`, `AVG [ms]`, `MAX [ms]`, `TOTAL [ms]`, `P99 [ms]`,
`P95 [ms]`, `P50 [ms]`.

Early exit when `"start time has already passed"` appears.

**Columns produced** (one row per iteration per pod):
`connection`, `configuration`, `experiment_run`, `client`, `benchmark_run`,
`child`, `pod`, `pod_count`, `iterations`, `duration`, `rampup`, `sf`,
`run` (0-based iteration index), `errors`, `vusers_loading`, `vusers`,
`NOPM`, `TPM`, `dbms`, `efficiency` (only when `keyandthink == 'true'`:
`round(100 × NOPM / vusers / 1.286, 2)`).

**Aggregation across parallel pods**: mean for `NOPM`, `TPM`; sum for `vusers`,
`errors`; max for percentiles.  `efficiency` recomputed from aggregated values
only when `vusers == sf × 10`.

---

### 7e. TPC-H / TPC-DS refresh stream (`tpch_refresh` / `tpcds_refresh`)

**Container**: `dbmsbenchmarker` (the loader.sh main container, renamed from
`sensor` so the standard timing infrastructure finds it).

**No evaluator subclass** currently parses refresh stream logs for benchmark
metrics.  The contribution of the refresh stream to the result set is:

1. **Timing only** — `end_benchmarking()` reads `BEXHOMA_START` / `BEXHOMA_END`
   from the `.dbmsbenchmarker.log` file via the standard
   `get_job_timing_benchmarking()` call (no fallback), and writes
   `benchmarking_timespans` to the `{connection}.config` file just like any
   other job.

2. **Summary display** — `experiments/dbmsbenchmarker.py::show_summary()` calls
   `show_summary_section()` on each registered benchmark with
   `benchmark_index != 1`, which prints `connection`, `experiment_run`,
   `client`, `benchmark_begin`, `benchmark_end`, and `benchmark_duration`.

`benchmark_duration` is computed in `evaluators/base.py::add_connection_to_result()`:
```python
pairs  = c['hostsystem']['benchmarking_timespans']['benchmarker']
begin  = min(p[0] for p in pairs)   # Unix epoch
end    = max(p[1] for p in pairs)
duration = end - begin               # seconds
```

---

## 8. TPC-H with refresh stream: `python tpch.py run -dbms PostgreSQL -sf 1 -ne 3 -xrs 3`

This is the canonical two-job-per-round case.

### 8a. `experiment_dict_template` after `enable_refresh_stream()`

```python
experiment_dict_template["benchmarker"][0] = [
    # benchmark_run = 1 — query stream
    {"name": "tpch", "benchmarker": "dbmsbenchmarker",
     "template": "jobtemplate-benchmarking-dbmsbenchmarker.yml",
     "parallelism": 1, ...},
    # benchmark_run = 2 — refresh stream
    {"name": "tpch-refresh", "benchmarker": "tpch_refresh",
     "template": "jobtemplate-benchmarking-tpch-refresh-PostgreSQL.yml",
     "parallelism": 1, "fixed_parallelism": True, ...},
]
```

### 8b. `add_benchmark_list([1, 1, 1])` (for `-ne 3`)

Produces three rounds, each with two entries.  The `tpch` entry receives
`parallelism = 1` (from the `-ne` list); the `tpch-refresh` entry keeps
`parallelism = 1` unchanged because `fixed_parallelism: True`.

### 8c. Per-round job submission

For each round (client = 1, 2, 3), `work_benchmark_list()` iterates over the
two entries and calls `run_benchmarker_pod()` twice:

| `benchmark_run` | Connection name | K8s Job name | Image |
|---|---|---|---|
| `1` | `PostgreSQL-1-1-1` | `bexhoma-benchmarker-PostgreSQL-…-1-1-1` | `dbmsbenchmarker` (queries) |
| `2` | `PostgreSQL-1-1-2` | `bexhoma-benchmarker-PostgreSQL-…-1-1-2` | `loader_tpch_refresh_postgresql` (RF1+RF2) |

The round counter is initialized to `1 + 1 = 2` (sum of `parallelism` values).
Both pods decrement it independently; both start their workload the moment the
counter reaches ≤ 0.

### 8d. Log files per round (client=1, experiment_run=1)

```
{code}/bexhoma-benchmarker-PostgreSQL-…-1-1-1-{pod}.dbmsbenchmarker.log  ← query stream
{code}/bexhoma-benchmarker-PostgreSQL-…-1-1-2-{pod}.datagenerator.log    ← dbgen initContainer
{code}/bexhoma-benchmarker-PostgreSQL-…-1-1-2-{pod}.dbmsbenchmarker.log  ← RF1+RF2 loader
```

### 8e. `end_benchmarking()` called twice per round

| Job | `get_job_timing_benchmarking()` tries | Result |
|---|---|---|
| query stream (`-1-1-1`) | container `"dbmsbenchmarker"` → found | timestamps from query stream log |
| refresh stream (`-1-1-2`) | container `"dbmsbenchmarker"` → found | timestamps from RF1+RF2 loader log |

Both results are written to their respective `{connection}.config` files
immediately.

### 8f. Two rows in `connections.config`

After the round, `connections.config` contains (among entries from other rounds):

```python
{'name': 'PostgreSQL-1-1-1', 'parameter': {'numBenchmark': '1', ...},
 'hostsystem': {'benchmarking_timespans': {'benchmarker': [(t0, t1)]}, ...}},
{'name': 'PostgreSQL-1-1-2', 'parameter': {'numBenchmark': '2', ...},
 'hostsystem': {'benchmarking_timespans': {'benchmarker': [(t0, t1)]}, ...}},
```

### 8g. Evaluation split

| Entry | Evaluator sees it? | What is stored |
|---|---|---|
| `PostgreSQL-1-1-1` (query stream) | Yes — `evaluators.dbmsbenchmarker` reads DBMSBenchmarker cube | per-query latencies, `Power@Size`, `Throughput@Size` |
| `PostgreSQL-1-1-2` (refresh stream) | Not in the cube — detected as "sidecar" entry by `show_summary()` | `benchmark_begin`, `benchmark_end`, `benchmark_duration` (seconds) |

---

## 9. How `show_summary()` presents results

### 9a. Which `show_summary()` runs and why

The MRO for `tpch` is: `tpch → dbmsbenchmarker → mixed → base`.

`tpch` overrides `show_summary()` (at `experiments/tpch.py`):
1. If no `RefreshStreamBenchmark` is in `self.benchmarks` (post-hoc
   `bexperiments summary` — `enable_refresh_stream()` was not called), creates
   one on the fly with a fresh evaluator and **temporarily appends it** to
   `self.benchmarks`.
2. Calls `super().show_summary()` — which is `dbmsbenchmarker.show_summary()`.
3. Removes the temporary benchmark (if it was added) so `self.benchmarks`
   is restored to its original state.

Appending before `super()` rather than calling `show_summary_section()` after
ensures that the generic benchmark loop inside `dbmsbenchmarker.show_summary()`
places the section right after `### Execution → Per Phase` and before
`### Latency`, consistent with the live-run position.

`dbmsbenchmarker.show_summary()` (at `experiments/dbmsbenchmarker.py:108`) does
NOT delegate to `mixed.show_summary()` (which loops over `self.benchmarks`).
The generic benchmark loop inside `dbmsbenchmarker.show_summary()` (lines 153–156)
calls `bm.show_summary_section(self)` for every benchmark with
`benchmark_index != 1` — this covers the live-run case where
`enable_refresh_stream()` registered a `RefreshStreamBenchmark`.

The `mixed.show_summary()` loop is only used when the experiment class is exactly
`mixed` (no subclass that overrides it).  For all named experiment types
(`tpch`, `tpcds`, `ycsb`, `tpcc`, `benchbase`) it is overridden and never called.

### 9b. Exact steps of `dbmsbenchmarker.show_summary()`

| Step | Code | Output |
|---|---|---|
| 1 | `self._test_results = []` | resets test assertions |
| 2 | `self.evaluator.load_inspector()` | loads the DBMSBenchmarker cube from disk |
| 3 | `show_summary_header()` | prints `## Show Summary`, workload metadata, connection list |
| 4 | `evaluator.get_df_benchmarking()` | fetches the aggregated per-phase DataFrame (used for tests at the end) |
| 5 | `evaluator.get_summary_benchmark_per_connection()` + `reconstruct_workflow()` | prints `### Workflow` with actual vs. planned |
| 6 | `evaluator.get_summary_loading_per_run[_multitenant]()` | prints `### Loading → Per Run` (when loading is active) |
| 7 | `evaluator.get_summary_benchmark_per_connection()` | prints `### Execution → Per Connection` |
| 8 | `evaluator.get_summary_benchmark_per_phase[_multitenant]()` | prints `### Execution → Per Phase` |
| 9 | **Generic benchmark loop** (see §9c) | prints one section per secondary registered benchmark |
| 10 | `evaluator.get_query_latencies()` | prints `### Latency of Timer Execution [ms]` |
| 11 | `evaluator.get_total_errors()` | prints `### Errors (failed queries)` |
| 12 | `evaluator.get_total_warnings()` | prints `### Warnings (result mismatch)` |
| 13 | `show_summary_monitoring()` | prints SUT CPU/RAM monitoring tables |
| 14 | Application metrics loop | prints `### Application Metrics` for active `monitoring_components` |
| 15 | `_test_column(df, ...)` + `_record_test(...)` | records pass/fail for Geo Times, Power@Size, Throughput@Size, SQL errors, warnings, workflow |
| 16 | `_print_test_summary()` | prints `### Tests` pass/fail table |

`self.evaluator` at step 4–12 is the `evaluators.dbmsbenchmarker` instance wired
to `benchmark_run=1` (overwritten by the first `add_benchmark()` call in
`mixed.add_benchmark()`).  It reads from the DBMSBenchmarker inspector cube and
therefore only sees connections produced by the primary query stream job.

### 9c. Generic benchmark loop (step 9)

After step 8, `dbmsbenchmarker.show_summary()` iterates over all registered
benchmarks and calls `show_summary_section(experiment)` for each one that is NOT
the primary benchmark (benchmark_index == 1):

```python
for bm in self.benchmarks:
    if bm.benchmark_index == 1:
        continue
    bm.show_summary_section(self)
```

`show_summary_section(experiment)` is defined on `Benchmark` (default: no-op) and
overridden in each secondary benchmark class to print that benchmark's specific
section without re-printing the experiment header.

The same loop exists in `DBMSBenchmarkerBenchmark.show_summary()` (in
`benchmarks/base.py`), where it is expressed as:

```python
for bm in experiment.benchmarks:
    if bm.benchmark_index == self.benchmark_index:
        continue
    bm.show_summary_section(experiment)
```

### 9d. `RefreshStreamBenchmark.show_summary_section()` — concrete example

When `enable_refresh_stream()` is called, it calls
`self.add_benchmark(RefreshStreamBenchmark(name='tpch_refresh', SF=...))`.
This assigns `benchmark_index=2` to the new benchmark.

At step 9, `dbmsbenchmarker.show_summary()` sees `self.benchmarks = [TPCH(idx=1), RefreshStreamBenchmark(idx=2)]`,
skips TPCH (idx=1), and calls `RefreshStreamBenchmark.show_summary_section(experiment)`:

```python
def show_summary_section(self, experiment):
    df_conn = self.evaluator.get_connections_of_experiment()
    # Filter to this benchmark's connections (benchmark_run == self.benchmark_index == 2)
    df_section = df_conn[
        (df_conn['benchmark_run'].astype(int) == self.benchmark_index)
        & df_conn['benchmark_duration'].notna()
    ][timing_cols]
    if not df_section.empty:
        print(f"\n### {self.name}\n")
        print(df_section.to_markdown(index=True))
```

`self.evaluator` is `evaluators.base(benchmark_run=2)`.
`get_connections_of_experiment()` reads from `connections.config` (which has entries
for both benchmark_run=1 and benchmark_run=2).  The filter `benchmark_run == 2` selects
only the refresh-stream entries, so the output is:

```
### tpch_refresh

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| PostgreSQL-1-1-1-2-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-06-16 05:03:06 | 2026-06-16 05:03:12 |                    6 |
| PostgreSQL-1-2-1-2-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-2 |                2 |        1 |               2 |           1 | …                   | …                   |                    … |
| PostgreSQL-1-3-1-2-1 | PostgreSQL-1-3-1 | PostgreSQL-1-3-1-2 |                3 |        1 |               2 |           1 | …                   | …                   |                    … |
```

The trailing `-1` in `connection` is the pod index within the job (synthesised from
`parallelism` when `benchmark.py read` has not produced per-pod sub-entries with
`orig_name`).  The refresh stream always has `parallelism = 1`, so this index is
always `1`.  `phase` and `job` contain no code prefix; the collector's
``get_connections()`` prepends the code when joining with monitoring data.

### 9e. Adding a new co-running benchmarker type

To add any new secondary benchmarker that runs in parallel with the query stream:

1. **Create a `Benchmark` subclass** that implements `show_summary_section(experiment)`.
   Return `evaluators.base(...)` from `create_evaluator()` if only timing is needed,
   or a richer evaluator if the pod logs contain parseable metrics.

2. **Register it** with `experiment.add_benchmark(MyBenchmark())` after the primary
   benchmark is already registered. `add_benchmark()` will assign
   `benchmark_index = len(self.benchmarks) + 1`.

3. **Add an experiment_dict entry** with `"fixed_parallelism": True` so the pod count
   does not scale with `-ne`.  The entry's `"benchmarker"` field should match the
   benchmark's `name` (used for log filtering in the evaluator).

4. The generic loop in `dbmsbenchmarker.show_summary()` will call
   `show_summary_section()` automatically — no further changes needed.

---

## 10. Key source locations

| Topic | File | Method / lines |
|---|---|---|
| Orchestration loop | `experiments/base.py` | `work_benchmark_list()` |
| Job submission | `configurations.py` | `run_benchmarker_pod()` |
| K8s Job creation | `configurations.py` | `create_manifest_job()` |
| Log retrieval | `clusters.py` | `store_pod_log()` |
| Timing extraction | `experiments/base.py` | `end_benchmarking()`, `get_job_timing_benchmarking()`, `extract_job_timing()` |
| Connection file write | `experiments/base.py` | `end_benchmarking()` (timespans) + `run_benchmarker_pod()` (initial create) |
| Log-to-pickle pipeline | `evaluators/logger.py` | `end_benchmarking()`, `_collect_dfs()`, `transform_all_logs_benchmarking()` |
| YCSB metrics | `evaluators/ycsb.py` | `log_to_df()`, `benchmarking_aggregate_by_parallel_pods()` |
| Benchbase metrics | `evaluators/benchbase.py` | `log_to_df()`, `benchmarking_aggregate_by_parallel_pods()` |
| HammerDB metrics | `evaluators/tpcc.py` | `log_to_df()`, `benchmarking_aggregate_by_parallel_pods()` |
| DBMSBenchmarker metrics | `evaluators/dbmsbenchmarker.py` | `get_df_benchmarking()` |
| Refresh stream timing in summary | `experiments/dbmsbenchmarker.py` | `show_summary()` |
| Connection metadata (incl. duration) | `evaluators/base.py` | `add_connection_to_result()`, `get_connections_of_experiment()` |
| Refresh stream setup | `experiments/tpch.py` | `enable_refresh_stream()` |
| `fixed_parallelism` guard | `configurations.py` | `add_benchmark_list()` |
