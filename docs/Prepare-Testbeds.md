# Example: Prepare Testbeds

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Overview

A **testbed** is a running, data-loaded DBMS deployment inside the Kubernetes cluster, ready for benchmarking.
Preparing a testbed involves the following steps:

1. Start the SUT (System Under Test — the DBMS container).
2. Start monitoring.
3. Run the loading phase (generate and import data).
4. Run the benchmarking phase.
5. Collect and evaluate measurements.
6. Remove all ephemeral components from the cluster.

Normally you want all phases to run in one go.
Bexhoma exposes three operating modes that let you stop the process at different points, which is useful for debugging, extending the implementation, or inspecting the DBMS state after loading.

> **Note:** All examples below keep the DBMS running after the experiment finishes.
> The summary output includes a "Services" section with the `kubectl port-forward` command to connect to the running instance.

---

## Operating Modes

Every benchmark script (`ycsb.py`, `benchbase.py`, `hammerdb.py`, `tpch.py`, `tpcds.py`) accepts the same three positional mode arguments:

| Mode | What happens |
|---|---|
| `start` | Start the SUT only. No data is loaded. Useful to inspect the fresh DBMS or run custom SQL by hand. |
| `load` | Start the SUT and run the data loading phase. Stops before benchmarking. Useful to pre-populate a volume and check import metrics. |
| `run` | Full experiment: start SUT, load data (or reuse an existing volume), run the benchmark, collect results. |

Data volumes are identified by DBMS, benchmark, and scale factor.
If a volume already exists and is marked as loaded, the `load` step is skipped automatically in `run` mode — the data is reused.

### Keeping or stopping the SUT

`-ks/--keep-sut {auto,yes,no}` decides whether the SUT of each configuration's last repetition is left running at the end:

| Value | `run` | `load` | `start` |
|---|---|---|---|
| `auto` (default) | stopped | kept | kept |
| `yes` (or `-ss/--skip-shutdown`) | kept | kept | kept |
| `no` | stopped | stopped | refused (start only starts SUTs) |

Earlier repetitions (`-nc`) always stop and restart their SUT.
Use `load -ks no` to measure loading only, e.g. bulk-write throughput per storage class (`-rst nvme,cephcsi -rsrp -nc 3`); the data stays on the volume, where a later `run` without `-rsr` finds it.

A kept SUT never blocks the experiment: when a cap (`-ms`, `-mse`, or a per-DBMS limit) leaves no room for a configuration that still has to start, the finished SUT is stopped instead, and the summary's "Services" section says so. With `-ms 1` and several configurations, only the last one to finish stays running.
Experiments run by the agent harness always stop their SUTs (except in `start`).

### Durability during the load

`-xld/--load-durability {durable,relaxed,unsafe}` sets how much durability the DBMS gives up while data is loaded:

| Level | During the load | Example |
|---|---|---|
| `durable` | crash-safe, whatever the server was started with | PostgreSQL `synchronous_commit`, `fsync`, `full_page_writes` on; MySQL/MariaDB `innodb_flush_log_at_trx_commit=1` (MariaDB also doublewrite on; MySQL cannot switch it on at runtime) |
| `relaxed` (default) | commits do not wait for the log flush; key checks are skipped | PostgreSQL `synchronous_commit=off`; MySQL `innodb_flush_log_at_trx_commit`, `foreign_key_checks=0` |
| `unsafe` | the strongest lever of the DBMS; a crash during the load can corrupt the data | MySQL redo log off and doublewrite `DETECT_ONLY` (MySQL cannot switch it off at runtime); MariaDB doublewrite off; PostgreSQL `fsync=off`, `full_page_writes=off` |

`-xld` affects the load only, like `-xii`/`-xic`/`-xis`. Before the check script, the server returns to its configured state (template and `--set`), so the benchmark always runs as configured, whatever the level. `unsafe` ends with a checkpoint (PostgreSQL also flushes the OS cache).
`relaxed` is the default; for TPC-H, TPC-DS and the MySQL loads of TPC-C and YCSB it is what the load always did.

**Durability of the benchmark.** The SUT templates set no durability options, so every DBMS runs with its own defaults, which are crash-safe (MySQL/MariaDB flush the redo log at every commit and use doublewrite, PostgreSQL waits for the WAL flush at commit).
A less durable benchmark is set per run with `--set`, so it is visible in the command and the results, e.g. `--set deployment[bexhoma-deployment-mysql].container[dbms].innodb_flush_log_at_trx_commit=2` or `--set ...container[dbms].innodb_doublewrite=OFF`.
For PostgreSQL, `--set` passes the value as `-c` on the command line, and a command-line value cannot be changed by `ALTER SYSTEM`. The durability scripts therefore also set `synchronous_commit` for the database (`ALTER DATABASE ... SET`, which wins over the command line for new sessions, and is reset after the load): `-xld relaxed --set synchronous_commit=on` loads with `off` and benchmarks with `on`. `fsync` and `full_page_writes` exist server-wide only; with `--set` they keep their value, so bexhoma refuses a `--set` value that conflicts with the level (declared in the scripts' `-- server-wide:` line) before loading.

**Where the scripts run.** Like index or constraint scripts, the durability scripts are part of the init script lists in the cluster config (`volumes.<benchmark>.initscripts`): every pre-load list starts with the placeholder `durability.sql`, every post-load list has `restoredurability.sql` right before `checkschema-*`.
bexhoma replaces the placeholders according to `-xld` by the scripts the DBMS folder has (e.g. `experiments/tpch/MySQL/`):

| `-xld` | `durability.sql` becomes | `restoredurability.sql` becomes |
|---|---|---|
| `durable` | `durability-durable.*` | `restoredurability-durable.*` |
| `relaxed` | `durability-relaxed.*` | `restoredurability-relaxed.*` |
| `unsafe` | `durability-relaxed.*`, `durability-unsafe.*` | `restoredurability-unsafe.*`, `restoredurability-relaxed.*` |

`.*` is `.sql`, then `.sh` (MariaDB uses shell scripts, as `SET GLOBAL` needs root). A script the DBMS folder does not have is not run; a list without a placeholder gets no durability scripts.
They exist for PostgreSQL (also used by PgDuckDB and PGBouncer), MySQL and MariaDB (all levels) and Citus (`durable`, `relaxed`), in every benchmark; other DBMS load as configured.
The copies in different benchmarks are identical; `tests/test_load_durability.py` fails on any difference that is not declared there (TPC-H, TPC-C and YCSB on MySQL keep their own `relaxed` settings).

---

## Environment Variables

The examples below assume three node-selector variables and a log directory.
Adjust the node names to match your cluster, or drop `-rnn`/`-rnl`/`-rnb` entirely to let Kubernetes schedule freely.

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1        # number of parallel experiment management processes

mkdir -p $LOG_DIR
```

---

## Reading the Summary Output

After each mode completes, Bexhoma prints a summary.
The sections have consistent meaning across all benchmark types:

| Section | Present in | Description |
|---|---|---|
| **Workload** | all modes | Experiment metadata: type, code, duration, parameter choices, bexhoma version |
| **Services** | all modes | `kubectl port-forward` command to reach the running SUT from your local machine |
| **Connections** | all modes | Hardware details of the node hosting the SUT (RAM, CPU, disk, resource requests) |
| **Loading** | `load`, `run` | Import throughput metrics (rows/second, time, pod count) |
| **Execution** | `run` | Benchmark results: throughput, latency, error count |
| **Workflow** | `run` | Planned vs. actual pod configuration — useful for verifying scale-out |
| **Ingestion - SUT** | `load`, `run` | CPU and RAM consumed by the DBMS during the loading phase |
| **Ingestion - Loader** | `load`, `run` | CPU and RAM consumed by the loader pods during the loading phase |
| **Execution - SUT** | `run` | CPU and RAM consumed by the DBMS during benchmarking |
| **Execution - Benchmarker** | `run` | CPU and RAM consumed by the driver pods during benchmarking |
| **Tests** | all modes | Automated sanity checks — e.g., no zero throughput, no NaN metrics, workflow matches plan |

A `TEST failed` line does not necessarily abort the experiment; it flags a condition worth investigating (e.g., a query error in TPC-DS Q90, or a monitoring gap). A `TEST skipped` line means the check was inconclusive rather than failing — e.g. a component with pre-existing data produces no CPU load, a phase ran shorter than one Prometheus scrape interval so a CPU counter delta of 0 cannot be distinguished from a real gap, or every missing monitoring metric has an expected reason (see [Monitoring](Monitoring.md#missing-metrics)).

---

## Inspecting Cluster State

You can watch or clean up all pods belonging to a specific benchmark using its use-case label:

```bash
# Watch components
kubectl get all -l app=bexhoma,usecase=<label>

# Remove all components
kubectl delete all -l app=bexhoma,usecase=<label>
```

| Benchmark | Label |
|---|---|
| YCSB | `ycsb` |
| Benchbase TPC-C | `benchbase_tpcc` |
| HammerDB TPC-C | `hammerdb_tpcc` |
| TPC-H | `tpc-h` |
| TPC-DS | `tpc-ds` |

---

## YCSB

YCSB is a key-value workload generator.
Configurations are numbered sequentially per DBMS — the first configuration is `PostgreSQL-1`, the second `PostgreSQL-2`, and so on.

### Start DBMS

Starts PostgreSQL without loading any data.
After this completes you can connect to the instance and run queries manually.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_ycsb_postgresql_start.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_start_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_start.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB Start DBMS
* Type: ycsb
* Duration: 161s 
* Code: 1794483474
* Start DBMS and do not load data.
* This just starts a SUT.
  * Workload is 'C'.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker36.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794483474 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1009496
  * datadisk:39
  * volume_size:1.8T
  * volume_used:986G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794483474

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No monitoring metrics missing
```

</details>

The summary confirms the SUT is running and shows the port-forward command.

### Start DBMS and Load Data

Starts PostgreSQL and imports YCSB data using 8 parallel loader pods with 64 threads each.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -nlp 8 \
  -nlt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_ycsb_postgresql_load.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_load_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_load.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB Data Loading SF=1
* Type: ycsb
* Duration: 319s 
* Code: 1794483659
* Load data and do not run a benchmark.
* This imports YCSB data sets.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794483659 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1011865
  * datadisk:2390
  * volume_size:1.8T
  * volume_used:989G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794483659

### Ingestion
* PostgreSQL-1: 8 of 8 units ok

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.05 |                61303.00 |            125000.00 |                               898.00 | 1.00 |               58.72 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.69 |                61314.00 |            125000.00 |                               854.00 | 1.00 |               58.71 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.45 |                61321.00 |            125000.00 |                               912.00 | 1.00 |               58.71 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.55 |                61318.00 |            125000.00 |                               881.00 | 1.00 |               58.71 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.75 |                61312.00 |            125000.00 |                               811.00 | 1.00 |               58.72 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.52 |                61289.00 |            125000.00 |                               917.00 | 1.00 |               58.74 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.85 |                61309.00 |            125000.00 |                               795.00 | 1.00 |               58.72 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.85 |                61309.00 |            125000.00 |                               916.00 | 1.00 |               58.72 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.71 |                        16310.72 |                61321.00 |           1000000.00 |                               873.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |        72.85 |      1.18 |           1.72 |                  2.75 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |       102.21 |      2.40 |           0.10 |                  0.10 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
```

</details>

Key parameters:
- `-nlp 8`: 8 parallel loader pods
- `-nlt 64`: 64 threads per loader pod

The summary's **Loading** table shows aggregate throughput across all loader pods.
The **Ingestion** tables show how much CPU and RAM the SUT and loader consumed.

### Start DBMS and Load Data and Run Workload

Full experiment: loads data and then runs YCSB workload C with 8 benchmarker pods.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -nlp 8 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_run.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_run_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_run.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 427s 
* Code: 1794484004
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794484004 9091:9091

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1011866
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:989G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794484004

### Ingestion
* PostgreSQL-1: 8 of 8 units ok

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.28 |                61266.00 |            125000.00 |                               742.00 | 1.00 |               58.76 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2041.12 |                61241.00 |            125000.00 |                               765.00 | 1.00 |               58.78 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2041.12 |                61241.00 |            125000.00 |                               801.00 | 1.00 |               58.78 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.98 |                61245.00 |            125000.00 |                               680.00 | 1.00 |               58.78 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.38 |                61263.00 |            125000.00 |                               752.00 | 1.00 |               58.76 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.72 |                61253.00 |            125000.00 |                               786.00 | 1.00 |               58.77 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.75 |                61252.00 |            125000.00 |                               775.00 | 1.00 |               58.77 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.68 |                61254.00 |            125000.00 |                               761.00 | 1.00 |               58.77 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.76 |                        16326.03 |                61266.00 |           1000000.00 |                               757.75 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |     2048 |           8 |            0 |                         2039.15 |                61300.00 |             125000 |                             754.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       2 |         8 |     2048 |           8 |            0 |                         2038.39 |                61323.00 |             125000 |                             751.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       3 |         8 |     2048 |           8 |            0 |                         2038.72 |                61313.00 |             125000 |                             696.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       4 |         8 |     2048 |           8 |            0 |                         2039.38 |                61293.00 |             125000 |                             721.00 |
| postgresql-1-1-1-1-5 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       5 |         8 |     2048 |           8 |            0 |                         2038.32 |                61325.00 |             125000 |                             605.00 |
| postgresql-1-1-1-1-6 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       6 |         8 |     2048 |           8 |            0 |                         2038.49 |                61320.00 |             125000 |                             729.00 |
| postgresql-1-1-1-1-7 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       7 |         8 |     2048 |           8 |            0 |                         2037.82 |                61340.00 |             125000 |                             679.00 |
| postgresql-1-1-1-1-8 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       8 |         8 |     2048 |           8 |            0 |                         2038.89 |                61308.00 |             125000 |                             762.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    16384 |               1 |           8 |            0 |                        16309.16 |                61340.00 |            1000000 |                             762.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        71.13 |      1.15 |           1.58 |                  2.76 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       116.38 |      2.65 |           0.10 |                  0.11 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        35.80 |      0.87 |           1.85 |                  3.02 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       105.72 |      2.26 |           0.10 |                  0.10 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

Key parameters:
- `-nbp 8`: 8 parallel benchmarker pods
- `-nbt 64`: 64 threads per benchmarker pod
- `-ss`: use a single shared storage volume

The **Execution** table aggregates throughput across all benchmarker pods.
The **Workflow** section confirms the actual pod count matched the plan.

---

## Benchbase (TPC-C)

Benchbase runs TPC-C transactions.
Configurations are numbered sequentially per DBMS — `PostgreSQL-1`, `PostgreSQL-2`, etc.

### Start DBMS

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_benchbase_postgresql_start.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_start_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_start.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Start DBMS
* Type: benchbase
* Duration: 161s 
* Code: 1794484464
* Start DBMS and do not load data.
* This just starts a SUT.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker36.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794484464 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1009517
  * datadisk:39
  * volume_size:1.8T
  * volume_used:986G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794484464
    * TENANT_VOL:False

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No monitoring metrics missing
* TEST skipped: Throughput (requests/second) (benchmarking phase not active)
```

</details>

### Start DBMS and Load Data

Imports TPC-C data (scale factor 1) using 8 parallel loader pods.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_benchbase_postgresql_load.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_load_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_load.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Data tpcc Loading SF=1
* Type: benchbase
* Duration: 243s 
* Code: 1794484642
* Load data and do not run a benchmark.
* This imports a Benchbase data set.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT. Scaling factor is 1. Target is based on multiples of '1024'.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794484642 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1009809
  * datadisk:330
  * volume_size:1.8T
  * volume_used:987G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794484642
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       31.00 |           3.00 |            0.00 |         25.00 |            3.00 |              1 |           1 |             |                |             0 | False         |              116.13 | False               |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |        18.27 |      0.46 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST skipped: Throughput (requests/second) (benchmarking phase not active)
```

</details>

The **Loading** table reports `Throughput [SF/h]` — scale factors loaded per hour.

### Start DBMS and Load Data and Run Workload

Loads data with 1 pod (Benchbase loads serially by design) and runs the workload with 8 benchmarker pods for 5 minutes.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_run.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_run_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_run.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 572s 
* Code: 1794484910
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794484910 9091:9091

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1009810
  * datadisk:330
  * volume_size:1.8T
  * volume_used:987G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794484910
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       30.00 |           3.00 |            0.00 |         24.00 |            3.00 |              1 |           1 |             |                |             0 | False         |              120.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       1 |           0 | 300.00 |            1 |                          74.73 |                       74.10 |         0.00 |                                                     528952.00 |                                             106868.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       2 |           0 | 300.00 |            0 |                          76.52 |                       75.81 |         0.00 |                                                     524069.00 |                                             104516.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       3 |           0 | 300.00 |            0 |                          74.39 |                       73.63 |         0.00 |                                                     532803.00 |                                             107403.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       4 |           0 | 300.00 |            0 |                          73.56 |                       72.81 |         0.00 |                                                     553346.00 |                                             108533.00 |
| postgresql-1-1-1-1-5 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       5 |           0 | 300.00 |            0 |                          72.57 |                       71.83 |         0.00 |                                                     548775.00 |                                             109963.00 |
| postgresql-1-1-1-1-6 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       6 |           0 | 300.00 |            0 |                          75.00 |                       74.19 |         0.00 |                                                     535332.00 |                                             106554.00 |
| postgresql-1-1-1-1-7 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       7 |           0 | 300.00 |            0 |                          74.43 |                       73.62 |         0.00 |                                                     541799.00 |                                             107273.00 |
| postgresql-1-1-1-1-8 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       8 |           0 | 300.00 |            0 |                          76.96 |                       76.23 |         0.00 |                                                     519205.00 |                                             103755.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |          64 |     1024 |               1 |           8 |           0 | 300.00 |            1 |                         598.16 |                      592.23 |         0.00 |                                                     553346.00 |                                             106858.12 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         3.16 |      0.18 |           0.47 |                  0.59 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       383.58 |      1.58 |           0.98 |                  1.32 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       317.48 |      1.87 |           0.25 |                  0.25 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

The **Execution** table reports:
- `Throughput (requests/second)` and `Goodput (requests/second)` — total and successful transaction rate
- `Latency Distribution.95th Percentile Latency (microseconds)` — tail latency
- `efficiency` — how close actual throughput came to the target

---

## HammerDB (TPC-C)

HammerDB runs TPC-C using virtual users (vusers).
Configurations are numbered sequentially per DBMS — `PostgreSQL-1`, `PostgreSQL-2`, etc.

### Start DBMS

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_hammerdb_postgresql_start.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_start_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_start.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Start DBMS
* Type: tpcc
* Duration: 163s 
* Code: 1794489144
* Start DBMS and do not load data.
* This just starts a SUT.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker36.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794489144 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1018673
  * datadisk:39
  * volume_size:1.8T
  * volume_used:995G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794489144

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No monitoring metrics missing
```

</details>

### Start DBMS and Load Data

Imports TPC-C data (1 warehouse = scale factor 1) using a single loader pod.
HammerDB's loader is inherently single-threaded, so `-nlp 1 -nlt 1` is typical.

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_hammerdb_postgresql_load.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_load_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_load.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Data Loading SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 246s 
* Code: 1794489326
* Load data and do not run a benchmark.
* This imports TPC-C data sets.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794489326 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1019945
  * datadisk:278
  * volume_size:1.8T
  * volume_used:997G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794489326

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       21.00 |           2.00 |            0.00 |         16.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              171.43 | False               |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |         0.42 |      0.01 |           0.41 |                  0.45 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* Network Tx Total [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
```

</details>

The **Loading** table reports `Imported warehouses [1/h]`.

### Start DBMS and Load Data and Run Workload

Loads data and runs TPC-C for 5 minutes with 64 virtual users.

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_run.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_run_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_run.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
* Type: tpcc
* Duration: 692s 
* Code: 1794489613
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794489613 9091:9091

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1021082
  * datadisk:278
  * volume_size:1.8T
  * volume_used:998G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794489613

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       22.00 |           2.00 |            0.00 |         16.00 |            4.00 |              1 |           1 |             | None           |             0 | False         |              163.64 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       64 |        1 |               1 |       1 |  63169 | 145437 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       64 |        1 |               1 |           1 |         0.00 | 63169.00 | 145437.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         1.59 |      0.05 |           0.48 |                  0.55 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2379.64 |      6.88 |           2.07 |                  3.15 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       204.05 |      0.61 |           0.25 |                  0.25 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>

The **Execution** table reports `NOPM` (New Orders Per Minute) and `TPM` (Transactions Per Minute), which are the standard HammerDB TPC-C metrics.

---

## TPC-H

TPC-H is the standard analytical benchmark with 22 queries.
Data is generated by a loader pod using `dbgen`, then loaded into the SUT.
After loading, the DBMSBenchmarker tool runs the 22 queries and records per-query latency.

### Start DBMS

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_tpch_postgresql_start.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_start_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_start.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Start DBMS
* Type: tpch
* Duration: 164s 
* Code: 1794486117
* Start DBMS and do not load data.
* This just starts a SUT.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker36.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794486117 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1009716
  * datadisk:39
  * volume_size:1.8T
  * volume_used:987G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794486117

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No monitoring metrics missing
```

</details>

### Start DBMS and Load Data

Generates and loads TPC-H data at scale factor 1.
The flags `-xii -xic -xis` trigger index creation, constraint application, and statistics gathering after the raw data is ingested.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_tpch_postgresql_load.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_load_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_load.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Data Loading SF=1
* Type: tpch
* Duration: 290s 
* Code: 1794486307
* Load data and do not run a benchmark.
* This imports TPC-H data sets.
  * TPC-H (SF=1) data is loaded.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794486307 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1012435
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:989G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794486307

### Ingestion
* PostgreSQL-1: 8 of 8 units ok

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       55.00 |           3.00 |            0.00 |         35.00 |           15.00 |              1 |           0 |             |                |             0 | False         |               65.45 | False               |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |        29.26 |      0.55 |           2.01 |                  3.56 |

### Loading phase: component data generator

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1 | n/a          |         0 |           0.00 |                  0.73 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
```

</details>

The **Loading** table breaks down time (in seconds) into phases:

| Column | Meaning |
|---|---|
| `time_preload` | Time to run the scripts before ingestion, e.g. creating the schema (DDL) |
| `time_generate` | Time to generate raw data files with `dbgen` |
| `time_ingest` | Time to import data into the DBMS |
| `time_postload` | Time to run the scripts after ingestion, e.g. creating indexes and constraints and recomputing statistics |
| `time_load` | Total loading time |
| `Throughput [SF/h]` | Scale factor loaded per hour, based on `time_load` |

### Start DBMS and Load Data and Run Workload

Loads TPC-H data and runs all 22 queries once.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_run.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_run_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_run.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 323s 
* Code: 1794486628
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794486628 9091:9091

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1012436
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:989G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794486628

### Ingestion
* PostgreSQL-1: 8 of 8 units ok

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       50.00 |           2.00 |            0.00 |         29.00 |           17.00 |              1 |           0 |             |                |             0 | False         |               72.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.21 |            17186.23 |           6092.31 |           0 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.21 |            17186.23 |           6092.31 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1004.63 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 192.18 |
| Shipping Priority (TPC-H Q3)                        |                 234.66 |
| Order Priority Checking Query (TPC-H Q4)            |                 101.70 |
| Local Supplier Volume (TPC-H Q5)                    |                 210.03 |
| Forecasting Revenue Change (TPC-H Q6)               |                 130.49 |
| Volume Shipping Query (TPC-H Q7)                    |                 235.58 |
| National Market Share (TPC-H Q8)                    |                 142.09 |
| Product Type Profit Measure (TPC-H Q9)              |                 526.98 |
| Returned Item Reporting Query (TPC-H Q10)           |                 192.24 |
| Important Stock Identification (TPC-H Q11)          |                  59.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 194.32 |
| Customer Distribution (TPC-H Q13)                   |                 609.34 |
| Promotion Effect Query (TPC-H Q14)                  |                 145.10 |
| Top Supplier Query (TPC-H Q15)                      |                 151.18 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 142.39 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 560.24 |
| Large Volume Customer (TPC-H Q18)                   |                2190.11 |
| Discounted Revenue (TPC-H Q19)                      |                  42.48 |
| Potential Part Promotion (TPC-H Q20)                |                 103.17 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 262.77 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  86.45 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        14.93 |      0.30 |           0.51 |                  1.72 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.73 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.65 |           1.72 |                  3.35 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

The **Execution** section reports per-query latency in the **Latency of Timer Execution** table and the TPC-H standard metrics:

| Metric | Meaning |
|---|---|
| `Geo Times [s]` | Geometric mean of per-query median runtimes |
| `Power@Size` | TPC-H Power metric: `(3600 × SF) / geo_times` — higher is better |
| `Throughput@Size` | TPC-H Throughput metric across all streams and queries |

---

## TPC-DS

TPC-DS is the decision-support benchmark with 99 queries.
Its structure mirrors TPC-H: `dbgen2` generates data, a loader imports it, DBMSBenchmarker runs the queries.

### Start DBMS

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_tpcds_postgresql_start.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_start_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_start.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Start DBMS
* Type: tpcds
* Duration: 189s 
* Code: 1794487010
* Start DBMS and do not load data.
* This just starts a SUT.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * SUT is fixed to cl-worker36.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794487010 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1009719
  * datadisk:39
  * volume_size:1.8T
  * volume_used:987G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794487010

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No monitoring metrics missing
```

</details>

### Start DBMS and Load Data

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_tpcds_postgresql_load.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_load_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_load.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Data Loading SF=1
* Type: tpcds
* Duration: 377s 
* Code: 1794487259
* Load data and do not run a benchmark.
* This imports TPC-DS data sets.
  * TPC-DS (SF=1) data is loaded.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794487259 9091:9091

### Connections
* postgresql-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1015418
  * datadisk:5747
  * volume_size:1.8T
  * volume_used:992G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794487259

### Ingestion
* PostgreSQL-1: 25 of 25 units ok

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       99.00 |           3.00 |            0.00 |         60.00 |           32.00 |              1 |           0 |             | None           |             0 | False         |               36.36 | False               |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |        67.56 |      1.61 |           2.82 |                  5.50 |

### Loading phase: component data generator

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1 |         9.02 |      0.38 |           0.00 |                  0.61 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1 (bexhoma-metrics-postgresql-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
```

</details>

### Start DBMS and Load Data and Run Workload

Loads TPC-DS data and runs all 99 queries.
Some queries may fail on certain DBMS (e.g., Q90 raises a division-by-zero on PostgreSQL at SF=1); these are flagged in the **Errors** section and in **Tests**.

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_run.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_run_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_run.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 568s 
* Code: 1794487704
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1794487704 9091:9091

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1015420
  * datadisk:5747
  * volume_size:1.8T
  * volume_used:992G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794487704

### Ingestion
* PostgreSQL-1: 25 of 25 units ok

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       90.00 |           2.00 |            0.00 |         56.00 |           31.00 |              1 |           0 |             | None           |             0 | False         |               40.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        176 |            0.30 |            12078.45 |           2025.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        176 |            0.30 |            12078.45 |           2025.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 294.80 |
| TPC-DS Q2     |                 185.09 |
| TPC-DS Q3     |                 131.68 |
| TPC-DS Q4     |                6077.52 |
| TPC-DS Q5     |                 355.94 |
| TPC-DS Q6     |               55192.16 |
| TPC-DS Q7     |                 285.36 |
| TPC-DS Q8     |                  46.49 |
| TPC-DS Q9     |                1677.99 |
| TPC-DS Q10    |                 862.78 |
| TPC-DS Q11    |                3337.02 |
| TPC-DS Q12    |                  54.21 |
| TPC-DS Q13    |                 465.66 |
| TPC-DS Q14a+b |                1490.84 |
| TPC-DS Q15    |                 100.21 |
| TPC-DS Q16    |                 160.63 |
| TPC-DS Q17    |                 248.20 |
| TPC-DS Q18    |                 343.29 |
| TPC-DS Q19    |                 116.76 |
| TPC-DS Q20    |                  74.60 |
| TPC-DS Q21    |                 155.10 |
| TPC-DS Q22    |                3075.32 |
| TPC-DS Q23a+b |                4085.70 |
| TPC-DS Q24a+b |                  46.80 |
| TPC-DS Q25    |                 253.34 |
| TPC-DS Q26    |                 192.48 |
| TPC-DS Q27    |                 275.66 |
| TPC-DS Q28    |                 563.66 |
| TPC-DS Q29    |                 270.06 |
| TPC-DS Q30    |                7870.16 |
| TPC-DS Q31    |                1320.80 |
| TPC-DS Q32    |                  71.76 |
| TPC-DS Q33    |                 327.53 |
| TPC-DS Q34    |                  19.69 |
| TPC-DS Q35    |                 957.08 |
| TPC-DS Q36    |                 780.64 |
| TPC-DS Q37    |                 192.97 |
| TPC-DS Q38    |                 779.12 |
| TPC-DS Q39a+b |                1843.72 |
| TPC-DS Q40    |                 101.31 |
| TPC-DS Q41    |                 729.75 |
| TPC-DS Q42    |                  66.12 |
| TPC-DS Q43    |                  23.21 |
| TPC-DS Q44    |                 326.80 |
| TPC-DS Q45    |                  67.99 |
| TPC-DS Q46    |                  26.77 |
| TPC-DS Q47    |                1472.48 |
| TPC-DS Q48    |                 468.81 |
| TPC-DS Q49    |                 328.29 |
| TPC-DS Q50    |                 380.66 |
| TPC-DS Q51    |                 654.12 |
| TPC-DS Q52    |                  67.32 |
| TPC-DS Q53    |                  83.93 |
| TPC-DS Q54    |                  60.47 |
| TPC-DS Q55    |                 170.69 |
| TPC-DS Q56    |                 509.44 |
| TPC-DS Q57    |                 699.43 |
| TPC-DS Q58    |                 306.56 |
| TPC-DS Q59    |                 291.08 |
| TPC-DS Q60    |                 310.84 |
| TPC-DS Q61    |                 100.43 |
| TPC-DS Q62    |                  74.23 |
| TPC-DS Q63    |                  82.75 |
| TPC-DS Q64    |                 531.94 |
| TPC-DS Q65    |                 411.12 |
| TPC-DS Q66    |                 168.22 |
| TPC-DS Q67    |                2871.95 |
| TPC-DS Q68    |                  31.11 |
| TPC-DS Q69    |                 193.39 |
| TPC-DS Q70    |                 319.09 |
| TPC-DS Q71    |                 259.88 |
| TPC-DS Q72    |                 757.36 |
| TPC-DS Q73    |                  22.11 |
| TPC-DS Q74    |                1127.62 |
| TPC-DS Q75    |                 789.62 |
| TPC-DS Q76    |                 102.86 |
| TPC-DS Q77    |                 239.72 |
| TPC-DS Q78    |                 977.22 |
| TPC-DS Q79    |                  80.31 |
| TPC-DS Q80    |                 353.52 |
| TPC-DS Q81    |               33088.16 |
| TPC-DS Q82    |                 405.48 |
| TPC-DS Q83    |                 151.00 |
| TPC-DS Q84    |                 113.78 |
| TPC-DS Q85    |                 247.47 |
| TPC-DS Q86    |                 171.15 |
| TPC-DS Q87    |                 805.68 |
| TPC-DS Q88    |                2005.23 |
| TPC-DS Q89    |                  72.44 |
| TPC-DS Q90    |                  98.10 |
| TPC-DS Q91    |                 117.42 |
| TPC-DS Q92    |                  56.62 |
| TPC-DS Q93    |                 206.09 |
| TPC-DS Q94    |                 216.18 |
| TPC-DS Q95    |                2842.49 |
| TPC-DS Q96    |                  71.34 |
| TPC-DS Q97    |                 278.37 |
| TPC-DS Q98    |                 134.11 |
| TPC-DS Q99    |                 107.15 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        72.81 |      1.34 |           2.82 |                  5.50 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        14.41 |      0.36 |           0.00 |                  0.83 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       188.16 |      1.48 |           2.97 |                  5.83 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        15.22 |      0.03 |           0.31 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

The **Execution** section reports per-query latency for all 99 TPC-DS queries and the same Power@Size / Throughput@Size metrics as TPC-H.
