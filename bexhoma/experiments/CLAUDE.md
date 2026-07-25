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

`add_benchmark_list()` (`configurations/base.py::SutConfiguration`) builds
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
        'dockerimage': 'postgres:18.3',   # resolved SUT image tag (cfg.dockerimage, set in start_sut()),
                                           # not the catalog docker key
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

## 2. Job submission: `BenchmarkRunner.run_pod()`

Source: `configurations/benchmarking.py::BenchmarkRunner.run_pod()`, invoked as
`config.runner.run_pod(...)` from `experiments/base.py::work_benchmark_list()`.

For each entry in the current client round, `run_pod()`:

1. Builds the **connection name**: `"{configuration}-{experimentRun}-{client}-{benchmark_run}"`.
2. Constructs the connection dict `c` (described above) and appends it to
   `connections.config`; also writes `{connection}.config` immediately.
3. Writes benchmarking parameters to a Redis queue:
   `bexhoma-{app}-benchmarker-{connection}-{code}` — one item per pod.
4. Sets the Redis **job counter**:
   `bexhoma-benchmarker-podcount-job-{connection}-{experiment}` = `parallelism`.
5. Calls `configurations/manifest.py::ManifestBuilder.create_manifest_job()` to submit
   the Kubernetes Job.

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
two entries and calls `run_pod()` twice:

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

Per-experiment-type dispatch:

| Experiment | `show_summary()` override | Behavior |
|---|---|---|
| `mixed` (generic) | `experiments/mixed.py` | loops `benchmark.show_summary(self)` for **every** registered benchmark — only exercised when the experiment class is exactly `mixed` (no subclass overrides it) |
| `tpch`/`tpcds` (→ `dbmsbenchmarker`) | `experiments/dbmsbenchmarker.py` | finds the benchmark with `benchmark_index == 1` and calls **only its** `show_summary(self)` |
| `tpch` specifically | `experiments/tpch.py` | if no `RefreshStreamBenchmark` is in `self.benchmarks` (post-hoc `bexhoma summary` — `enable_refresh_stream()` was not called during the live run), creates one on the fly with a fresh evaluator and **temporarily appends it**, calls `super().show_summary()`, then removes the temporary entry so `self.benchmarks` is restored |
| `ycsb`/`tpcc`/`benchbase` | none — inherit `mixed.show_summary()` | since each of these registers exactly one benchmark, the `mixed` loop calls the template method once |

For all named experiment types, the actual summary content is produced by a single
shared **template method**, `Benchmark.show_summary(experiment)` in
`benchmarks/base.py`, not by per-experiment-type code. `dbmsbenchmarker.show_summary()`
and `tpch.show_summary()` exist only to pick which benchmark's `show_summary()` is the
"primary" call (so the shared header/workflow/monitoring/tests are printed exactly
once per experiment, not once per benchmark).

### 9b. The template method — `Benchmark.show_summary()` (`benchmarks/base.py`)

Since 2026-07-23, the three hooks below **return** a `Section` tree (see §9c1)
instead of printing directly, so the exact same tree can be rendered twice —
once to stdout (`render_stdout()`, byte-identical to the pre-refactor output)
and, when `write_report=True`, once into the tiered Markdown report (see §9h
and `docs/AgentReport.md`):

```python
def show_summary(self, experiment, write_report: bool = False):
    experiment._test_results = []
    self._prepare_evaluator(experiment)                                  # hook
    connections_sorted, monitoring_applications = experiment.show_summary_header()
    workflow_section = None
    if experiment.benchmarking_is_active():
        # ### Workflow
        df_connections = self.evaluator.get_connections_of_experiment()
        workflow_actual = self.evaluator.reconstruct_workflow(df_connections)
        workflow_planned = experiment.workload['workflow_planned']
        workflow_section = build_workflow_section(workflow_actual, workflow_planned)
    loading_section, df_loading = self._show_loading_sections(experiment, is_multitenant)  # hook
    execution_section = None
    if experiment.benchmarking_is_active():
        # ### Execution → Per Connection, Per Phase, Reset
        execution_section, df_aggregated_reduced = self._build_execution_section(df_connections, is_multitenant)
    extra_sections, extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)  # hook
    document = [s for s in (workflow_section, loading_section, execution_section) if s is not None] + extra_sections
    render_stdout(document)
    experiment.show_summary_monitoring()
    # ### Application Metrics
    self.evaluator.record_tests(
        experiment, df_loading, df_aggregated_reduced,
        workflow_actual, workflow_planned, **extra_context
    )
    if write_report:
        report_writer.write_markdown_report(experiment, self, workflow_section, loading_section,
                                             execution_section, extra_sections, connections_sorted,
                                             monitoring_applications, extra_context, df_connections)
    experiment._print_test_summary()
```

| Step | Output |
|---|---|
| `experiment._test_results = []` | resets test assertions |
| `self._prepare_evaluator(experiment)` | hook |
| `experiment.show_summary_header()` | `## Show Summary`, workload metadata, connection list, SUT restart counts — still prints directly, not converted to a `Section` |
| `build_workflow_section(...)` | not a hook (never overridable) — builds the `Workflow` section (Actual vs. Planned) |
| `self._show_loading_sections(...)` | hook — returns the `Loading` section (or `None`) |
| `self._build_execution_section(...)` | not a hook — builds the `Execution` section (Per Connection, Per Phase, Reset) |
| `self._show_extra_sections(...)` | hook — returns extra sections (secondary-benchmark sections, latency, errors, warnings, ...) |
| `render_stdout(document)` | prints the whole `Workflow`/`Loading`/`Execution`/extra-sections tree, reproducing the pre-refactor `print()` sequence exactly |
| `experiment.show_summary_monitoring()` | SUT CPU/RAM monitoring tables, records skip/pass/fail tests — still prints directly |
| `### Application Metrics` | from `show_summary_header()`'s `monitoring_applications` — still prints directly |
| `self.evaluator.record_tests(...)` | records metric-column/workflow pass/fail tests (see §9c2) |
| `report_writer.write_markdown_report(...)` | only when `write_report=True` — writes `report/*.md` (§9h) |
| `experiment._print_test_summary()` | `### Tests` pass/fail table |

### 9c. The hooks

#### 9c1. The `Section` data model

`bexhoma.benchmarks.base.Section` is a small dataclass (`heading`, `level`,
`blank_after_heading`, `dataframe`, `index`, `floatfmt`, `skip_if_empty`,
`lines`, `children`, `link_connections`) representing one titled block of
summary content — tabular (`dataframe`), freeform (`lines`), or both, with
nested `children`. `render_stdout()` and
`bexhoma.report_writer._render_sections()` both walk the same tree, formatting
it independently; `link_connections=True` tells only the report renderer that
this DataFrame's index holds connection names, to be rewritten into
`connections.md` links (see §9h).

#### 9c2. Hooks and evaluator method

`Benchmark.show_summary()` is a template method with three overridable hooks
plus one evaluator-side method, so each benchmark tool only needs to supply
the pieces that differ:

| Hook | Default (`Benchmark`) | Override |
|---|---|---|
| `_prepare_evaluator(experiment)` | no-op | `DBMSBenchmarkerBenchmark` → `self.evaluator.load_inspector()` |
| `_show_loading_sections(experiment, is_multitenant)` → `(Section \| None, df_loading)` | builds `### Loading → Per Run` when `loading_is_active()` | `YCSB` → also builds `#### Per Connection` first; guards on `df_loading.empty` |
| `_show_extra_sections(experiment, df_aggregated_reduced)` → `(list[Section], dict)` | no-op, returns `([], {})` | `DBMSBenchmarkerBenchmark` → runs the secondary-benchmark loop (see §9d), then builds `Latency`/`Errors`/`Warnings` sections; returns `{"num_errors": N, "num_warnings": N}` |
| `_build_key_metrics_section(df_aggregated_reduced)` → `Section \| None` | no-op, returns `None` | `DBMSBenchmarkerBenchmark`/`YCSB`/`TPCC`/`Benchbase` → surface the exact column(s) their own `record_tests()` tests (Geo Times/Power@Size/Throughput@Size, `[OVERALL].Throughput(ops/sec)`, `NOPM`, `Throughput (requests/second)` respectively), via the shared `_key_metrics_section_from_columns()` helper. Report-only (§9h) — never rendered to stdout. |
| `evaluator.record_tests(experiment, df_loading, df_reduced, workflow_actual, workflow_planned, **extra)` | `evaluators/logger.py` default: tests workflow only | `evaluators/dbmsbenchmarker.py` → also tests Geo Times, Power@Size, Throughput@Size, SQL errors/warnings (from `extra`); `evaluators/ycsb.py`, `evaluators/tpcc.py`, `evaluators/benchbase.py` → test their own metric columns plus workflow |

`record_tests()` lives on the **evaluator**, not the `Benchmark`, because the metric
columns it checks (`df_reduced`) are evaluator-specific; the `extra` kwargs bridge
context computed in `_show_extra_sections()` (e.g. SQL error/warning counts) into it.
Unlike the three hooks above, `record_tests()` was never print-based — no change
was needed for the `Section` refactor.

### 9d. Secondary-benchmark sections (`_show_extra_sections` → generic loop)

`DBMSBenchmarkerBenchmark._show_extra_sections()` (`benchmarks/base.py`) iterates over
every registered benchmark and calls `show_summary_section(experiment)` for each one
that is NOT the currently-running (primary) benchmark, collecting the returned
sections (skipping `None`):

```python
for bm in experiment.benchmarks:
    if bm.benchmark_index == self.benchmark_index:
        continue
    section = bm.show_summary_section(experiment)
    if section is not None:
        sections.append(section)
```

`show_summary_section(experiment) -> Section | None` is defined on `Benchmark` (default
in `benchmarks/base.py`: builds this benchmark's own `#### Per Connection`/`#### Per
Phase`/`#### Reset` as a `Section`, scoped to its own evaluator; returns `None` when
benchmarking is not active) and overridden by `RefreshStreamBenchmark`
(`benchmarks/refresh.py`) since it has no per-query metrics of its own, only timing.

### 9e. `RefreshStreamBenchmark.show_summary_section()` — concrete example

When `enable_refresh_stream()` is called, it calls
`self.add_benchmark(RefreshStreamBenchmark(name='tpch_refresh', SF=...))`.
This assigns `benchmark_index=2` to the new benchmark.

In the secondary-benchmark loop (§9d), the primary TPCH benchmark (`benchmark_index=1`)
is skipped and `RefreshStreamBenchmark.show_summary_section(experiment)` runs:

```python
def show_summary_section(self, experiment) -> Section | None:
    df_conn = self.evaluator.get_connections_of_experiment()
    # Filter to this benchmark's connections (benchmark_run == self.benchmark_index == 2)
    df_section = df_conn[
        (df_conn['benchmark_run'].astype(int) == self.benchmark_index)
        & df_conn['benchmark_duration'].notna()
    ][timing_cols]
    if df_section.empty:
        return None
    return Section(heading=self.name, level=3, blank_after_heading=True,
                    dataframe=df_section, floatfmt=None, link_connections=True)
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

### 9f. Adding a new co-running benchmarker type

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

4. The generic loop inside `DBMSBenchmarkerBenchmark._show_extra_sections()` (§9d)
   will call `show_summary_section()` automatically — no further changes needed.

### 9g. stdout is still the default; nothing changes unless `-rp` is passed

`show_summary(experiment, write_report=False)` — the default — behaves exactly as
before the 2026-07-23 refactor: `render_stdout(document)` reproduces the historical
`print()` sequence byte-for-byte, and `experiment._test_results` (populated by
`_record_test()`/`_record_skipped_test()`/`_test_column()`, printed by
`_print_test_summary()`) still lives only for the duration of the call. Pass
`write_report=True` (wired to the `-rp`/`--report` CLI flag on every entry script and
on `bexhoma summary`) to additionally persist a tiered Markdown report — see §9h.

### 9h. The agent-consumable Markdown report (`-rp` / `write_report=True`)

`bexhoma/report_writer.py::write_markdown_report()` consumes the exact same
`Section` trees, `connections_sorted`, `monitoring_applications`, and
`extra_context` that `show_summary()` just built and rendered to stdout, and
writes `{resultfolder}/{code}/report/{index,workflow,loading,execution,monitoring,connections}.md`
— one file per active phase/topic, plus `index.md` as the always-written entry
point. It needs no live cluster connection (it reads the same local files every
evaluator method already reads), so `bexhoma summary -e <code> -rp` works from the
result folder alone, exactly like a plain `bexhoma summary -e <code>`.

Full design (the three-tier structure, the output contract, the Full Metric
Catalog, cross-referencing/linkification, and the provenance-globbing
consistency guarantee) is documented in `docs/AgentReport.md` and in
`report_writer.py`'s own module docstring — not duplicated here. The one thing
worth calling out at this level: `write_markdown_report()` does *no* duplicate
data-fetching for anything `show_summary()` already computed (same `Section`
trees, same DataFrames) — the one deliberate exception is `monitoring.md`'s Full
Metric Catalog appendix, which enumerates every configured Prometheus metric,
not just the four hardcoded hardware metrics and first five active application
metrics `show_summary()` itself is capped at; that is genuinely new
data-gathering, not a re-fetch.

`index.md`'s Key Metrics block (the benchmark type's headline performance
number(s) — see §9c2's `_build_key_metrics_section` row) is deliberately built
on the **benchmark** class, not in `report_writer.py`: which column counts as
"the" tested metric is benchmark-specific knowledge (Geo Times/Power@Size for
DBMSBenchmarker, NOPM for HammerDB, ...), so it lives alongside every other
benchmark-specific override, keeping `report_writer.py` itself generic across
benchmark types.

---

## 10. Key source locations

| Topic | File | Method / lines |
|---|---|---|
| Orchestration loop | `experiments/base.py` | `work_benchmark_list()` |
| Job submission | `configurations/benchmarking.py` | `BenchmarkRunner.run_pod()` |
| K8s Job creation | `configurations/manifest.py` | `ManifestBuilder.create_manifest_job()` |
| Log retrieval | `clusters.py` | `store_pod_log()` |
| Timing extraction | `experiments/base.py` | `end_benchmarking()`, `get_job_timing_benchmarking()`, `extract_job_timing()` |
| Connection file write | `experiments/base.py` | `end_benchmarking()` (timespans) + `configurations/benchmarking.py::BenchmarkRunner.run_pod()` (initial create) |
| Log-to-pickle pipeline | `evaluators/logger.py` | `end_benchmarking()`, `_collect_dfs()`, `transform_all_logs_benchmarking()` |
| YCSB metrics | `evaluators/ycsb.py` | `log_to_df()`, `benchmarking_aggregate_by_parallel_pods()` |
| Benchbase metrics | `evaluators/benchbase.py` | `log_to_df()`, `benchmarking_aggregate_by_parallel_pods()` |
| HammerDB metrics | `evaluators/tpcc.py` | `log_to_df()`, `benchmarking_aggregate_by_parallel_pods()` |
| DBMSBenchmarker metrics | `evaluators/dbmsbenchmarker.py` | `get_df_benchmarking()` |
| Refresh stream timing in summary | `benchmarks/refresh.py` | `RefreshStreamBenchmark.show_summary_section()` |
| Connection metadata (incl. duration) | `evaluators/base.py` | `add_connection_to_result()`, `get_connections_of_experiment()` |
| Refresh stream setup | `experiments/tpch.py` | `enable_refresh_stream()` |
| `fixed_parallelism` guard | `configurations/base.py` | `SutConfiguration.add_benchmark_list()` |
