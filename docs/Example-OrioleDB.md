# Example: Benchmark OrioleDB

This example shows how to benchmark OrioleDB, PostgreSQL with the storage engine OrioleDB, with YCSB, Benchbase and HammerDB on a single node.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[OrioleDB](https://www.orioledb.com) is a table access method for PostgreSQL: rows are stored in the B-tree of the primary key (index-organized tables), old row versions are kept in an undo log instead of the table, so its tables need no `VACUUM`, and it has a buffer cache of its own.
Bexhoma runs the image `orioledb/orioledb:v1.10.3-pg18` (OrioleDB 1.10.3 on PostgreSQL 18.6), with OrioleDB as the default table access method, and uses the scripts, loaders and clients of PostgreSQL.
OrioleDB is meant for transactional workloads, so bexhoma offers it for YCSB, Benchbase and HammerDB only.

OrioleDB is dual-licensed under Apache-2.0 and the PostgreSQL License; it calls itself public beta, "recommended for experiments, testing, benchmarking", not for production.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [OrioleDB](https://www.orioledb.com)
1. [OrioleDB on GitHub](https://github.com/orioledb/orioledb)
1. [OrioleDB in Docker](https://hub.docker.com/r/orioledb/orioledb)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. Test script of this page: [test-docs-orioledb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-orioledb.sh), [test-docs-orioledb.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-orioledb.ps1)


## Perform YCSB Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example:
```bash
bexhoma ycsb \
  -dbms OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb.log
```

This loads 1 million rows of YCSB with 4 loader pods of 16 threads each and runs workload A (50% reads, 50% updates) with 32 threads against a target of 32768 operations per second, see [Example: YCSB](Example-YCSB.md).

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running

```

The code of the experiment is its unique identifier.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e <code>` (removes everything that is related to experiment `<code>`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_orioledb_summary.md" target="_blank" rel="noopener">docs_ycsb_orioledb.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 438s 
* Code: 1795419821
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 4 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [4] pods.
  * Benchmarking is tested with [32] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1036265
  * volume_size:1.7T
  * volume_used:1012.0G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795419821

### Ingestion
* OrioleDB-1: 4 of 4 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795419821-6ccf65cfdd-m7mr7: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:-------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| orioledb-1-1-0-1-1 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4081.10 |                61258.00 |            250000.00 |                               763.00 | 1.00 |               58.77 |
| orioledb-1-1-0-1-2 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.50 |                61267.00 |            250000.00 |                               814.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-3 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4079.43 |                61283.00 |            250000.00 |                               777.00 | 1.00 |               58.74 |
| orioledb-1-1-0-1-4 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.10 |                61273.00 |            250000.00 |                               792.00 | 1.00 |               58.75 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| OrioleDB-1-1 |             1.00 |     16.00 | 16384.00 |        4.00 |     0.00 | 1.00 |               58.74 |                        16321.14 |                61283.00 |           1000000.00 |                               786.50 |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        32 |    32768 |        0 |                        32459.10 |                30808.00 |             499205 |                             525.00 |               500795 |                              1022.00 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        32 |    32768 |        0 |                        32459.10 |                30808.00 |             499205 |                             525.00 |               500795 |                              1022.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run has 10 million operations (`-xop 10`), about 5 minutes at the target.
The template has a `postgres_exporter` sidecar, as PostgreSQL; `-ma` collects the metric set `postgresql`, see [Example: Benchmark PostgreSQL](Example-PostgreSQL.md#application-metrics).

```bash
bexhoma ycsb \
  -dbms OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_orioledb_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_orioledb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 704s 
* Code: 1795420281
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 4 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [4] pods.
  * Benchmarking is tested with [32] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1037192
  * volume_size:1.7T
  * volume_used:1012.9G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795420281

### Ingestion
* OrioleDB-1: 4 of 4 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795420281-774c46bbf6-rd74q: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:-------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| orioledb-1-1-0-1-1 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.63 |                61235.00 |            250000.00 |                               822.00 | 1.00 |               58.79 |
| orioledb-1-1-0-1-2 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.43 |                61238.00 |            250000.00 |                               831.00 | 1.00 |               58.79 |
| orioledb-1-1-0-1-3 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.97 |                61230.00 |            250000.00 |                               835.00 | 1.00 |               58.79 |
| orioledb-1-1-0-1-4 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.97 |                61230.00 |            250000.00 |                               848.00 | 1.00 |               58.79 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| OrioleDB-1-1 |             1.00 |     16.00 | 16384.00 |        4.00 |     0.00 | 1.00 |               58.79 |                        16331.00 |                61238.00 |           1000000.00 |                               834.00 |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        32 |    32768 |        0 |                        32738.05 |               305455.00 |            5000374 |                             520.00 |              4999626 |                              1094.00 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        32 |    32768 |        0 |                        32738.05 |               305455.00 |            5000374 |                             520.00 |              4999626 |                              1094.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1 |        81.92 |      1.36 |           9.20 |                  9.24 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1 |        82.52 |      2.36 |           0.10 |                  0.10 |

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1 |       486.20 |      1.83 |           9.45 |                 11.03 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1 |       888.15 |      3.27 |           0.29 |                  0.29 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-----------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| orioledb-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS             |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-----------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| orioledb-1-1-1-1 |                                30.00 |                                                0.00 |                                                        0.00 |                                  13.00 |                                              13.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
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

### Application Metrics

The metrics of the `postgres_exporter` are those of PostgreSQL.
Counters of dead rows (`n_dead_tup`) and HOT updates stay 0 for OrioleDB tables, as old row versions are in the undo log.


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

```bash
bexhoma ycsb \
  -dbms OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_storage.log
```

The second run (`-nc 2`) restarts the SUT on the loaded volume; OrioleDB recovers its tables from its own checkpoint at the start.

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_orioledb_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_orioledb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 754s 
* Code: 1795421060
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 4 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [16] threads, split into [4] pods.
  * Benchmarking is tested with [32] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1035873
  * volume_size:48.9G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795421060
* orioledb-1-2-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1028349
  * volume_size:48.9G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795421060

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: OrioleDB-1-2

### Data Parameters of Reused Volumes
* OrioleDB-1: DDL values of the volume: fillfactor=100, autovacuum_scale=0.2
* OrioleDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* OrioleDB-1: 4 of 4 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795421060-bcd57c65f-xqsgk: 0
* bexhoma-sut-orioledb-1-1795421060-55bb55ff56-xlgd7: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS OrioleDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS OrioleDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:-------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| orioledb-1-1-0-1-1 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.50 |                61267.00 |            250000.00 |                               751.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-2 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.57 |                61266.00 |            250000.00 |                               710.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-3 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.23 |                61271.00 |            250000.00 |                               814.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-4 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.10 |                61273.00 |            250000.00 |                               772.00 | 1.00 |               58.75 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| OrioleDB-1-1 |             1.00 |     16.00 | 16384.00 |        4.00 |     0.00 | 1.00 |               58.75 |                        16321.40 |                61273.00 |           1000000.00 |                               761.75 |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        32 |    32768 |        0 |                        32470.70 |                30797.00 |             500524 |                             503.00 |               499476 |                              5239.00 |
| orioledb-1-2-1-1-1 | orioledb-1-2-1 | orioledb-1-2-1-1 |                2 |        1 |               1 |       1 |        32 |    32768 |        0 |                        32467.53 |                30800.00 |             499593 |                            1006.00 |               500407 |                              4551.00 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        32 |    32768 |        0 |                        32470.70 |                30797.00 |             500524 |                             503.00 |               499476 |                              5239.00 |
| orioledb-1-2-1 | orioledb-1-2-1 |                2 |        1 |               1 |           1 |        32 |    32768 |        0 |                        32467.53 |                30800.00 |             499593 |                            1006.00 |               500407 |                              4551.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Comparison with PostgreSQL

OrioleDB and [PostgreSQL](Example-PostgreSQL.md) run the same PostgreSQL 18.6 with the same settings, except for the storage engine and its cache (`orioledb.main_buffers=16GB` instead of `shared_buffers=16GB`).
This run benchmarks both with YCSB workload A, one after the other on the same node (`-ms 1`), with a target that neither reaches (`-xnbf 8`, 131072 operations per second).

```bash
bexhoma ycsb \
  -dbms PostgreSQL OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 8 \
  -xnlf 1 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -xop 10 \
  -m \
  -ms 1 \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_postgresql.log
```

Both templates switch autovacuum off (`autovacuum=off`), so PostgreSQL does not pay for vacuuming during the run; the dead rows of its updates stay in the table.

In the example result, OrioleDB has a higher throughput (about 71,000 against 61,500 operations per second) and a lower 99th percentile read latency (461 µs against 617 µs), with about the same update latency and slightly less CPU.
Its memory is higher from the start, as the cache of OrioleDB tables (`orioledb.main_buffers`) is allocated when the server starts.
This is a single run of a single workload; the difference varies between runs.

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_orioledb_postgresql_summary.md" target="_blank" rel="noopener">docs_ycsb_orioledb_postgresql.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1152s 
* Code: 1795421833
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [8].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL', 'OrioleDB'].
  * Import is handled by 4 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [4] pods.
  * Benchmarking is tested with [32] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 1.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1031099
  * volume_size:1.7T
  * volume_used:1006.9G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795421833
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1030741
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:1007G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795421833

### Ingestion
* OrioleDB-1: 4 of 4 units ok
* PostgreSQL-1: 4 of 4 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795421833-66b797f58-l5zhz: 0
* bexhoma-sut-postgresql-1-1795421833-fcccc968c-qc4b7: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| orioledb-1-1-0-1-1   |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4083.77 |                61218.00 |            250000.00 |                               754.00 | 1.00 |               58.81 |
| orioledb-1-1-0-1-2   |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.90 |                61231.00 |            250000.00 |                               781.00 | 1.00 |               58.79 |
| orioledb-1-1-0-1-3   |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.17 |                61242.00 |            250000.00 |                               740.00 | 1.00 |               58.78 |
| orioledb-1-1-0-1-4   |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.43 |                61238.00 |            250000.00 |                               768.00 | 1.00 |               58.79 |
| postgresql-1-1-0-1-1 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4083.23 |                61226.00 |            250000.00 |                               790.00 | 1.00 |               58.80 |
| postgresql-1-1-0-1-2 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4083.17 |                61227.00 |            250000.00 |                               793.00 | 1.00 |               58.80 |
| postgresql-1-1-0-1-3 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4082.10 |                61243.00 |            250000.00 |                               829.00 | 1.00 |               58.78 |
| postgresql-1-1-0-1-4 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4084.17 |                61212.00 |            250000.00 |                               779.00 | 1.00 |               58.81 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| OrioleDB-1-1   |             1.00 |     16.00 | 16384.00 |        4.00 |     0.00 | 1.00 |               58.78 |                        16331.26 |                61242.00 |           1000000.00 |                               760.75 |
| PostgreSQL-1-1 |             1.00 |     16.00 | 16384.00 |        4.00 |     0.00 | 1.00 |               58.78 |                        16332.66 |                61243.00 |           1000000.00 |                               797.75 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1-1-1   | orioledb-1-1-1   | orioledb-1-1-1-1   |                1 |        1 |               1 |       1 |        32 |   131072 |        0 |                        71451.54 |               139955.00 |            4999909 |                             461.00 |              5000091 |                              1732.00 |
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        32 |   131072 |        0 |                        61507.05 |               162583.00 |            5000584 |                             617.00 |              4999416 |                              1759.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1   | orioledb-1-1-1   |                1 |        1 |               1 |           1 |        32 |   131072 |        0 |                        71451.54 |               139955.00 |            4999909 |                             461.00 |              5000091 |                              1732.00 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        32 |   131072 |        0 |                        61507.05 |               162583.00 |            5000584 |                             617.00 |              4999416 |                              1759.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1   |        77.96 |      1.28 |           9.20 |                  9.24 |
| postgresql-1-1-1-1 |        67.44 |      1.11 |           1.57 |                  2.74 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1   |        63.05 |      2.21 |           0.10 |                  0.10 |
| postgresql-1-1-1-1 |        72.00 |      2.18 |           0.10 |                  0.10 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1   |       537.62 |      4.98 |           9.45 |                 11.04 |
| postgresql-1-1-1-1 |       596.50 |      4.65 |           1.97 |                  3.36 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| orioledb-1-1-1-1   |       613.67 |      5.44 |           0.55 |                  0.55 |
| postgresql-1-1-1-1 |       634.55 |      4.63 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection orioledb-1-1-1-1 (bexhoma-metrics-orioledb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
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
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
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


## Technical Details

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'OrioleDB': {
    'base_system': 'PostgreSQL',
    'storage_prefix': 'orioledb',
    'benchmarks': {
        'ycsb': {...},        # as PostgreSQL
        'benchbase': {...},   # as PostgreSQL
        'hammerdb': {...},    # as PostgreSQL
    },
    'abbreviation': 'ori',
    'loadData': 'psql -U postgres -d {database} < {scriptname}',
    'delay_prepare': 0,
    'template': {
        'version': 'v1.10.3',
        'alias': 'General-J',
        'docker_alias': 'GP-J',
        'dialect': 'PostgreSQL',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/{database}?reWriteBatchedInserts=true&currentSchema={schema}',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'postgres',
            'schema': 'public',
            'explain': ['EXPLAIN (VERBOSE, FORMAT JSON) {query}'],
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # as PostgreSQL
},
```

It is the configuration of [PostgreSQL](Example-PostgreSQL.md#configuration-of-bexhoma) for the OLTP benchmarks, with its own storage name and abbreviation (`ori`), so its volumes are not shared with PostgreSQL.
TPC-H, TPC-DS and SSB have no entry, so `-dbms` does not offer OrioleDB for them.

### Deployment

[deploymenttemplate-OrioleDB.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-OrioleDB.yml): one SUT pod, deployment `bexhoma-deployment-orioledb`, image `orioledb/orioledb:v1.10.3-pg18` (Alpine).
It is the template of PostgreSQL with these differences:

| Point | Handling | Without it |
|---|---|---|
| Engine | `-c shared_preload_libraries=orioledb` and `-c default_table_access_method=orioledb`: every table that a script or a benchmark client creates is an OrioleDB table, without `USING orioledb` in the DDL | the tables are heap tables of PostgreSQL |
| Extension | the `initdb` of the image creates the extension `orioledb` in `template1` and `postgres`, so every database has it, also those created by a benchmark | `CREATE TABLE` of an OrioleDB table fails |
| Configuration | the arguments start with `-c`, so the entrypoint runs `postgres -c ...` on `$PGDATA` (`/var/lib/postgresql/data/pgdata`, as PostgreSQL) | the default command of the image, `postgres -D /etc/postgresql`, fixes `data_directory` to the mount point of the volume |
| Listen address | `-c listen_addresses=*` | the `postgresql.conf` written by `initdb` keeps `localhost`: the loaders and benchmarkers get `Connection refused` |
| Memory | `orioledb.main_buffers=16GB` (the cache of OrioleDB tables) and `shared_buffers=1GB` (only system catalogs and sequences are heap tables), instead of `shared_buffers=16GB`; `orioledb.undo_buffers=256MB` as in the image; `orioledb.checkpoint_completion_ratio=1.0`, as OrioleDB recommends when only OrioleDB tables are used | the cache of OrioleDB tables is 64 MB |
| User | the image runs as `postgres` with UID 70 (not 999): `fix-permissions` changes the owner of tenant folders to `70:70`; `preStop` uses `su-exec` and `/usr/local/bin/pg_ctl` | - |

All other settings (connections, WAL, checkpoints, `autovacuum=off`, locks) are those of PostgreSQL.
Server options are set as for PostgreSQL, e.g. `--set deployment[bexhoma-deployment-orioledb].container[dbms].work_mem=1GB`.

### Schema and Scripts

OrioleDB uses the scripts of PostgreSQL (`base_system: PostgreSQL`), for YCSB ([`experiments/ycsb/PostgreSQL`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/PostgreSQL)), Benchbase and HammerDB, and their clients: the JDBC binding of YCSB with `postgresql-42.5.0.jar`, the profile `postgres` of Benchbase and `HAMMERDB_TYPE=postgresql` of HammerDB.
What differs for OrioleDB tables:

| Script step | Effect on OrioleDB tables |
|---|---|
| `VACUUM` (reset, `checkschema`) | nothing to remove (old row versions are in the undo log); `ANALYZE` collects statistics as for heap tables |
| `CHECKPOINT` | also writes the OrioleDB checkpoint |
| `-xddl fillfactor` (YCSB) | OrioleDB supports `fillfactor` on tables and indexes: it reserves space in the B-tree leaf pages against page splits (inserts and updates), not for HOT updates |
| `-xddl autovacuum_scale` (YCSB) | stored, without effect (no autovacuum of OrioleDB tables) |

Isolation: OrioleDB has no serializable snapshot isolation.
With `orioledb.serializable=table_lock` (the default, kept by the template) a `SERIALIZABLE` transaction locks every table it touches, so concurrent serializable transactions on a table run one after the other.
Bexhoma runs Benchbase with `TRANSACTION_READ_COMMITTED`, but Benchbase `twitter` fixes `SERIALIZABLE` in the PostgreSQL profile.

### Load Durability

With `-xld`, the durability scripts of PostgreSQL run, see [PostgreSQL](Example-PostgreSQL.md#load-durability): `synchronous_commit`, `fsync` and `full_page_writes` are settings of PostgreSQL; OrioleDB writes no full page images, so `full_page_writes` only concerns heap tables.
Results for [YCSB durable](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_orioledb_durable_summary.md) and [YCSB unsafe](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_orioledb_unsafe_summary.md), see [Test: Load Durability](Test-Durability.md).

### Reset Scripts

With `-ar`, the reset of PostgreSQL runs before each benchmarking round, see [PostgreSQL](Example-PostgreSQL.md#reset-scripts): `VACUUM VERBOSE ANALYZE` only analyzes the OrioleDB tables, `CHECKPOINT` and `pg_stat_reset*` work as for PostgreSQL.
Result for [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_orioledb_summary.md), see [Test: Reset Scripts](Test-Reset.md).


## Benchbase

Benchbase TPC-C with 16 warehouses and 16 threads for 5 minutes, see [Example: Benchbase](Example-Benchbase.md):

```bash
bexhoma benchbase \
  -dbms OrioleDB \
  -sf 16 \
  -xbt tpcc \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_tpcc_orioledb.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_tpcc_orioledb_summary.md" target="_blank" rel="noopener">docs_benchbase_tpcc_orioledb.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 710s 
* Code: 1795423039
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1031224
  * volume_size:1.7T
  * volume_used:1007.1G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795423039

### Ingestion
* OrioleDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795423039-687447c595-2wlf7: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

| DBMS         |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:-------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| OrioleDB-1-1 |                1 |   16 |      106.00 |           6.00 |            0.00 |         92.00 |            8.00 |              1 |         1 |             | None           |             0 | False         |              543.40 | False               |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                        4143.92 |                     4125.58 |         0.00 |                                                       9839.00 |                                               3857.00 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                        4143.92 |                     4125.58 |         0.00 |                                                       9839.00 |                                               3857.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>


## HammerDB

HammerDB TPC-C with 16 warehouses and 16 virtual users for 5 minutes, see [Example: HammerDB](Example-HammerDB.md):

```bash
bexhoma hammerdb \
  -dbms OrioleDB \
  -sf 16 \
  -xsd 5 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_orioledb.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_orioledb_summary.md" target="_blank" rel="noopener">docs_hammerdb_orioledb.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: hammerdb
* Duration: 765s 
* Code: 1795423770
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1031474
  * volume_size:1.7T
  * volume_used:1007.3G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795423770

### Ingestion
* OrioleDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795423770-ccdf9dcf-sppfr: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

| DBMS         |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:-------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| OrioleDB-1-1 |                1 |   16 |       57.00 |           6.00 |            0.00 |         40.00 |           11.00 |              1 |         8 |             | None           |             0 | False         |             1010.53 | False               |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 | 322843 | 742895 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 | 322843.00 | 742895.00 |          5 |        0 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>
