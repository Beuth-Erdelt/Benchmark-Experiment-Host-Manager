# Example: Testing Collectors

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This page shows examples for running benchmarks with all three collector types active simultaneously:
* `-m`: SUT (system under test) metrics collected by a cluster-wide Prometheus installation
* `-ma`: Application metrics collected by sidecar containers attached to the SUT pod
* `-mc`: Cluster-wide metrics collected by the cluster-wide Prometheus installation

The script `scripts/test-docs-collector.sh` runs 18 experiments covering Benchbase TPC-C, TPC-H, YCSB, and HammerDB — each in single-tenant and multi-tenant configurations. Each benchmark group runs three experiments: two with a fresh persistent volume (`-rsr`) to test data generation and loading, and a third that reuses the existing volume to test repeated benchmarking runs.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

## Perform Tests

You will have to change the node selectors there (to names of nodes that exist in your cluster — or leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"
BEXHOMA_NUM_TENANTS=2

mkdir -p $LOG_DIR
```

## Benchbase TPC-C

### Test 1: Single tenant, fresh PVC, scale nbp=1,2

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nc 2 \
  -nbp 1,2 \
  -nbt 160 \
  -xli 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_collector_1.log
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
* imports TPC-C data for 16 warehouses (`-sf 16`) into a persistent 100Gi volume (`-rsr -rss 100Gi`), which is freshly created
* runs 2 experiment iterations (`-nc 2`) each with 2 benchmarking configurations (`-nbp 1,2`):
  * 1 pod × 160 threads; then 2 pods × 80 threads each
  * target is 16×(`-xnbf`) × 1024 (`-xtb`) ops per pod
  * each stream runs for 5 minutes (`-xsd 5`)
* monitors SUT metrics (`-m`), application metrics via sidecar (`-ma`), and cluster metrics (`-mc`)
* runs at most 1 DBMS at a time (`-ms`)
* verifies workflow matches plan (`-tr`)

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_collector_1_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_collector_1.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1850s 
* Code: 1793568043
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Status is logged every 10ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684832
  * datadisk:4308
  * volume_size:98G
  * volume_used:4.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793568043
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684473
  * datadisk:17606
  * volume_size:98G
  * volume_used:18G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793568043
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684468
  * datadisk:26902
  * volume_size:98G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793568043
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684466
  * datadisk:28370
  * volume_size:98G
  * volume_used:28G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793568043
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793568043-6ffbcc6778-fql99: 0
* bexhoma-sut-postgresql-1-1793568043-7b5ddbf446-pnxr8: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       89.00 |           3.00 |            0.00 |         76.00 |           10.00 |              1 |           1 |             |                |             0 | False         |              647.19 | False               |
| PostgreSQL-1-2 |                2 |   16 |       89.00 |           3.00 |            0.00 |         76.00 |           10.00 |              1 |           1 |             |                |             0 | False         |              647.19 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |           34 |                       12593.71 |                    12460.11 |         0.00 |                                                      35810.00 |                                              12682.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 300.00 |            7 |                        3938.43 |                     3903.55 |         0.00 |                                                      39335.00 |                                              20298.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 300.00 |            7 |                        3950.96 |                     3915.50 |         0.00 |                                                      39167.00 |                                              20237.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |           15 |                        6155.99 |                     6105.52 |         0.00 |                                                      47368.00 |                                              25978.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          80 |     8192 |        2 |               1 |       1 |           0 | 300.00 |            7 |                        2905.06 |                     2881.19 |         0.00 |                                                      50020.00 |                                              27525.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          80 |     8192 |        2 |               1 |       2 |           0 | 300.00 |            6 |                        2909.90 |                     2886.17 |         0.00 |                                                      50063.00 |                                              27482.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 300.00 |           34 |                       12593.71 |                    12460.11 |         0.00 |                                                      35810.00 |                                              12682.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 300.00 |           14 |                        7889.39 |                     7819.05 |         0.00 |                                                      39335.00 |                                              20267.50 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |         160 |    16384 |               1 |           1 |           0 | 300.00 |           15 |                        6155.99 |                     6105.52 |         0.00 |                                                      47368.00 |                                              25978.00 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |         160 |    16384 |               1 |           2 |           0 | 300.00 |           13 |                        5814.96 |                     5767.35 |         0.00 |                                                      50063.00 |                                              27503.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       153.01 |      3.21 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       153.01 |      3.21 |           2.05 |                  3.69 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       897.00 |     14.59 |           0.25 |                  0.25 |
| postgresql-1-1-2-1 |       897.00 |     14.59 |           0.25 |                  0.25 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      5171.82 |     21.08 |           8.19 |                 13.66 |
| postgresql-1-1-2-1 |      3584.33 |     13.21 |          10.63 |                 18.00 |
| postgresql-1-2-1-1 |      2930.95 |     13.10 |           6.24 |                 10.31 |
| postgresql-1-2-2-1 |      2738.41 |     10.40 |           8.62 |                 14.66 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2515.46 |      9.41 |           1.24 |                  1.24 |
| postgresql-1-1-2-1 |      2142.08 |      8.85 |           0.70 |                  0.70 |
| postgresql-1-2-1-1 |      1589.41 |      6.48 |           1.12 |                  1.12 |
| postgresql-1-2-2-1 |      1770.69 |      6.66 |           0.66 |                  0.66 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   7.00 |                                               7.00 |
| postgresql-1-1-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   7.00 |                                               7.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 9.00 |                                               38.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-1-2-1 |                                 9.00 |                                               28.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-1-1 |                                 8.00 |                                               23.00 |                                                        0.00 |                                 154.00 |                                             154.00 |
| postgresql-1-2-2-1 |                                 9.00 |                                               28.00 |                                                        0.00 |                                 157.00 |                                             157.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Test 2: Single tenant, fresh PVC, scale nbp=4,8

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 20 \
  -nc 2 \
  -nbp 4,8 \
  -nbt 160 \
  -xli 10 \
  -m -ma -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 100Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_collector_2.log
```

Same as test 1 but with `nbp=4,8` (4 or 8 benchmarking pods) and `xnbf=20` (target factor 20). This tests scale-out of the benchmarking driver further. The PVC is recreated (`-rsr`).

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_collector_2_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_collector_2.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1880s 
* Code: 1793569963
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
  * Status is logged every 10ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684465
  * datadisk:4307
  * volume_size:98G
  * volume_used:4.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684465
  * datadisk:17996
  * volume_size:98G
  * volume_used:18G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684446
  * datadisk:27454
  * volume_size:98G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:683652
  * datadisk:28882
  * volume_size:98G
  * volume_used:29G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793569963-7d87688db6-p7hrj: 0
* bexhoma-sut-postgresql-1-1793569963-64fcdc66-b4rcl: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       85.00 |           4.00 |            0.00 |         71.00 |           10.00 |              1 |           1 |             |                |             0 | False         |              677.65 | False               |
| PostgreSQL-1-2 |                2 |   16 |       85.00 |           4.00 |            0.00 |         71.00 |           10.00 |              1 |           1 |             |                |             0 | False         |              677.65 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            6 |                        2869.34 |                     2836.70 |         0.00 |                                                      46570.00 |                                              13932.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |           10 |                        2890.55 |                     2857.99 |         0.00 |                                                      46508.00 |                                              13829.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            9 |                        2869.04 |                     2836.76 |         0.00 |                                                      46711.00 |                                              13933.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            6 |                        2866.33 |                     2833.85 |         0.00 |                                                      46815.00 |                                              13946.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            2 |                         887.66 |                      878.35 |         0.00 |                                                      48879.00 |                                              22516.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            1 |                         892.16 |                      882.94 |         0.00 |                                                      48586.00 |                                              22403.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            2 |                         889.74 |                      880.83 |         0.00 |                                                      48806.00 |                                              22464.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            0 |                         887.54 |                      878.35 |         0.00 |                                                      49027.00 |                                              22519.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            5 |                         889.51 |                      880.27 |         0.00 |                                                      48845.00 |                                              22468.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            2 |                         887.85 |                      878.91 |         0.00 |                                                      49103.00 |                                              22511.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            4 |                         885.49 |                      876.65 |         0.00 |                                                      48762.00 |                                              22571.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            0 |                         887.81 |                      878.61 |         0.00 |                                                      48735.00 |                                              22512.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            0 |                        1418.63 |                     1406.41 |         0.00 |                                                      51902.00 |                                              28182.00 |
| postgresql-1-2-1-1-2 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            0 |                        1431.51 |                     1418.49 |         0.00 |                                                      51742.00 |                                              27929.00 |
| postgresql-1-2-1-1-3 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            2 |                        1422.33 |                     1409.73 |         0.00 |                                                      51870.00 |                                              28110.00 |
| postgresql-1-2-1-1-4 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            3 |                        1419.57 |                     1406.85 |         0.00 |                                                      51864.00 |                                              28164.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            0 |                         615.19 |                      609.68 |         0.00 |                                                      59721.00 |                                              32491.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            2 |                         618.65 |                      613.19 |         0.00 |                                                      59591.00 |                                              32308.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            1 |                         615.64 |                      610.16 |         0.00 |                                                      59781.00 |                                              32467.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            2 |                         614.65 |                      609.12 |         0.00 |                                                      59591.00 |                                              32518.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            0 |                         617.72 |                      612.10 |         0.00 |                                                      59637.00 |                                              32357.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            0 |                         616.46 |                      610.74 |         0.00 |                                                      59580.00 |                                              32425.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            0 |                         617.77 |                      612.05 |         0.00 |                                                      59535.00 |                                              32356.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            3 |                         615.26 |                      609.67 |         0.00 |                                                      59758.00 |                                              32486.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           31 |                       11495.26 |                    11365.30 |         0.00 |                                                      46815.00 |                                              13910.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           16 |                        7107.76 |                     7034.90 |         0.00 |                                                      49103.00 |                                              22495.50 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |         160 |    20480 |               1 |           4 |           0 | 300.00 |            5 |                        5692.04 |                     5641.48 |         0.00 |                                                      51902.00 |                                              28096.25 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |         160 |    20480 |               1 |           8 |           0 | 300.00 |            8 |                        4931.34 |                     4886.71 |         0.00 |                                                      59781.00 |                                              32426.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       134.87 |      3.32 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       134.87 |      3.32 |           2.05 |                  3.69 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       837.51 |     14.57 |           0.26 |                  0.26 |
| postgresql-1-1-2-1 |       837.51 |     14.57 |           0.26 |                  0.26 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      4513.45 |     18.42 |           8.81 |                 14.70 |
| postgresql-1-1-2-1 |      3817.53 |     16.79 |          11.58 |                 19.57 |
| postgresql-1-2-1-1 |      3019.71 |     12.39 |           6.96 |                 11.68 |
| postgresql-1-2-2-1 |      2551.53 |     10.94 |           9.29 |                 16.01 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2449.81 |     10.44 |           0.58 |                  0.58 |
| postgresql-1-1-2-1 |      2158.64 |      9.66 |           0.37 |                  0.37 |
| postgresql-1-2-1-1 |      1841.50 |      8.26 |           0.46 |                  0.46 |
| postgresql-1-2-2-1 |      1715.07 |      6.40 |           0.37 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |
| postgresql-1-1-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                39.00 |                                               31.00 |                                                        0.00 |                                 159.00 |                                             159.00 |
| postgresql-1-1-2-1 |                                 8.00 |                                               26.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-1-1 |                                 9.00 |                                               22.00 |                                                        0.00 |                                 156.00 |                                             156.00 |
| postgresql-1-2-2-1 |                                 6.00 |                                               23.00 |                                                        0.00 |                                 155.00 |                                             155.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Test 3: Single tenant, reuse PVC

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 -xsd 5 -xtb 1024 -xnbf 20 -nc 2 -nbp 4,8 -nbt 160 -xli 10 \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -lr 64Gi -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_collector_3.log
```

Same parameters as test 2 but without `-rsr -rst`. The persistent volume from the previous experiment is reused, so no data generation or loading takes place.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_collector_3_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_collector_3.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1992s 
* Code: 1793571888
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
  * Status is logged every 10ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:688672
  * datadisk:4307
  * volume_size:1.8T
  * volume_used:673G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:698324
  * datadisk:13950
  * volume_size:1.8T
  * volume_used:682G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:688684
  * datadisk:4307
  * volume_size:1.8T
  * volume_used:673G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:706207
  * datadisk:20874
  * volume_size:1.8T
  * volume_used:690G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793571888-58864fcd4f-d62gq: 0
* bexhoma-sut-postgresql-1-1793571888-68b5b4f494-c4n7k: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       81.00 |           2.00 |            0.00 |         71.00 |            8.00 |              1 |           1 |             |                |             0 | False         |              711.11 | False               |
| PostgreSQL-1-2 |                2 |   16 |       81.00 |           3.00 |            0.00 |         69.00 |            9.00 |              1 |           1 |             |                |             0 | False         |              711.11 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            7 |                        2515.59 |                     2488.51 |         0.00 |                                                      64766.00 |                                              15893.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            6 |                        1349.42 |                     1336.62 |         0.00 |                                                      96944.00 |                                              29618.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |           12 |                        2528.65 |                     2501.41 |         0.00 |                                                      64251.00 |                                              15811.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            6 |                        2515.39 |                     2488.45 |         0.00 |                                                      64840.00 |                                              15894.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            3 |                        1385.60 |                     1368.30 |         0.00 |                                                      36437.00 |                                              14423.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            3 |                        1383.52 |                     1366.43 |         0.00 |                                                      36424.00 |                                              14444.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            7 |                        1387.62 |                     1370.57 |         0.00 |                                                      36398.00 |                                              14401.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            2 |                        1379.10 |                     1361.50 |         0.00 |                                                      36632.00 |                                              14490.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            3 |                        1393.69 |                     1376.28 |         0.00 |                                                      36312.00 |                                              14339.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            7 |                        1392.73 |                     1375.19 |         0.00 |                                                      36334.00 |                                              14349.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            0 |                        1388.05 |                     1370.91 |         0.00 |                                                      36454.00 |                                              14396.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            2 |                        1391.59 |                     1373.58 |         0.00 |                                                      36184.00 |                                              14361.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |           15 |                        3930.25 |                     3882.03 |         0.00 |                                                      30327.00 |                                              10170.00 |
| postgresql-1-2-1-1-2 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |           21 |                        3902.64 |                     3854.40 |         0.00 |                                                      30707.00 |                                              10244.00 |
| postgresql-1-2-1-1-3 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |           28 |                        3902.49 |                     3854.92 |         0.00 |                                                      30629.00 |                                              10245.00 |
| postgresql-1-2-1-1-4 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |           12 |                        3922.52 |                     3873.36 |         0.00 |                                                      30472.00 |                                              10191.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            2 |                        1035.77 |                     1024.55 |         0.00 |                                                      39784.00 |                                              19296.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |           11 |                        1043.82 |                     1032.72 |         0.00 |                                                      39713.00 |                                              19147.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            4 |                        1041.54 |                     1030.10 |         0.00 |                                                      39773.00 |                                              19188.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            5 |                        1043.23 |                     1031.74 |         0.00 |                                                      39758.00 |                                              19158.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            4 |                        1039.68 |                     1028.63 |         0.00 |                                                      39801.00 |                                              19218.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            3 |                        1042.23 |                     1030.95 |         0.00 |                                                      39723.00 |                                              19176.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            6 |                        1042.16 |                     1030.90 |         0.00 |                                                      39633.00 |                                              19177.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            4 |                        1036.67 |                     1025.27 |         0.00 |                                                      40050.00 |                                              19273.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           31 |                        8909.05 |                     8815.00 |         0.00 |                                                      96944.00 |                                              19304.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           27 |                       11101.89 |                    10962.77 |         0.00 |                                                      36632.00 |                                              14400.38 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           76 |                       15657.90 |                    15464.72 |         0.00 |                                                      30707.00 |                                              10212.50 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           39 |                        8325.09 |                     8234.85 |         0.00 |                                                      40050.00 |                                              19204.12 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       129.99 |      2.73 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       129.99 |      2.73 |           2.05 |                  3.69 |
| postgresql-1-2-1-1 |       138.84 |      5.27 |           2.06 |                  3.70 |
| postgresql-1-2-2-1 |       138.84 |      5.27 |           2.06 |                  3.70 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       781.39 |     15.20 |           0.26 |                  0.26 |
| postgresql-1-1-2-1 |       781.39 |     15.20 |           0.26 |                  0.26 |
| postgresql-1-2-1-1 |       477.63 |     14.69 |           0.24 |                  0.24 |
| postgresql-1-2-2-1 |       477.63 |     14.69 |           0.24 |                  0.24 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      5238.72 |     22.33 |           6.98 |                 11.51 |
| postgresql-1-1-2-1 |      5170.85 |     23.42 |          11.65 |                 19.66 |
| postgresql-1-2-1-1 |      5919.25 |     23.78 |           9.21 |                 15.40 |
| postgresql-1-2-2-1 |      3899.39 |     15.96 |          12.14 |                 20.61 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2167.08 |      9.73 |           0.54 |                  0.54 |
| postgresql-1-1-2-1 |      2719.85 |     14.72 |           0.39 |                  0.39 |
| postgresql-1-2-1-1 |      2656.65 |     10.89 |           0.59 |                  0.59 |
| postgresql-1-2-2-1 |      2411.96 |      9.42 |           0.40 |                  0.40 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |
| postgresql-1-1-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |
| postgresql-1-2-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |
| postgresql-1-2-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 4.00 |                                               39.00 |                                                        0.00 |                                 150.00 |                                             150.00 |
| postgresql-1-1-2-1 |                                 7.00 |                                               40.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-1-1 |                                 6.00 |                                               43.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-2-1 |                                10.00 |                                               27.00 |                                                        0.00 |                                 160.00 |                                             160.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

## Benchbase TPC-C Multi-Tenant

Multi-tenant tests use `BEXHOMA_NUM_TENANTS=2` and the `-mtb` / `-mtn` flags to isolate tenants by schema, database, or container.

### Schema isolation

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 -xsd 5 -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp 1 -nbp 1 -nbt 10 \
  -xkey \
  -m -ma -mc \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -mtb schema -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_collector_tenants_schema.log
```

This
* runs 2 tenants (`-mtn 2`) each isolated by PostgreSQL schema (`-mtb schema`) inside one shared DBMS container
* `-ne "2,2"`: each experiment repetition uses 2 loader pods and 2 benchmarking pods (one per tenant)
* `-xkey`: enables TPC-C keying and thinking times (realistic user simulation at low throughput)
* SF=1 is sufficient because the load is split across tenants

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_collector_tenants_schema_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_collector_tenants_schema.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2030s 
* Code: 1793573943
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685337
  * datadisk:637
  * volume_size:49G
  * volume_used:637M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793573943
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685332
  * datadisk:638
  * volume_size:49G
  * volume_used:638M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793573943
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685334
  * datadisk:639
  * volume_size:49G
  * volume_used:639M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793573943
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685336
  * datadisk:640
  * volume_size:49G
  * volume_used:640M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793573943
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema_tenant, indexing=Checks_tenant

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793573943-7478f976d-8448k: 0
* bexhoma-sut-postgresql-1-1793573943-579b89c555-z7mm8: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793573943-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    1 |       26.00 |           5.00 |            0.00 |         26.00 |            6.00 |              2 |           1 |              138.46 | False               |
| 1793573943-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    1 |       25.00 |           5.00 |            0.00 |         25.00 |            6.00 |              2 |           1 |              144.00 | False               |
| 1793573943-PostgreSQL-1-2-0 |                2 | schema         | False         |             2 |           0 |    1 |       26.00 |           5.00 |            0.00 |         26.00 |            6.00 |              2 |           1 |              138.46 | True                |
| 1793573943-PostgreSQL-1-2-1 |                2 | schema         | False         |             2 |           1 |    1 |       25.00 |           5.00 |            0.00 |         25.00 |            6.00 |              2 |           1 |              144.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.54 |                        0.53 |       110.58 |                                                      29067.00 |                                              12387.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      38835.00 |                                              12996.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       100.08 |                                                      29806.00 |                                              14077.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       107.08 |                                                      28662.00 |                                              13245.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      71175.00 |                                              26536.00 |
| postgresql-1-2-1-1-2 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.49 |                        0.49 |       102.18 |                                                      79121.00 |                                              26210.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.50 |                        0.49 |       103.58 |                                                      41593.00 |                                              19725.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.49 |                        0.49 |       103.58 |                                                      40766.00 |                                              17667.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-0 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.54 |                        0.53 |       110.58 |                                                      29067.00 |                                              12387.00 |
| postgresql-1-1-1-1 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      38835.00 |                                              12996.00 |
| postgresql-1-1-2-0 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       100.08 |                                                      29806.00 |                                              14077.00 |
| postgresql-1-1-2-1 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       107.08 |                                                      28662.00 |                                              13245.00 |
| postgresql-1-2-1-0 | postgresql-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      71175.00 |                                              26536.00 |
| postgresql-1-2-1-1 | postgresql-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.49 |                        0.49 |       102.18 |                                                      79121.00 |                                              26210.00 |
| postgresql-1-2-2-0 | postgresql-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.50 |                        0.49 |       103.58 |                                                      41593.00 |                                              19725.00 |
| postgresql-1-2-2-1 | postgresql-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.49 |                        0.49 |       103.58 |                                                      40766.00 |                                              17667.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        39.31 |      0.99 |           0.62 |                  0.88 |
| postgresql-1-1-2-1 |        39.31 |      0.99 |           0.62 |                  0.88 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         2.45 |      0.06 |           0.69 |                  0.95 |
| postgresql-1-1-2-1 |         2.25 |      0.02 |           0.69 |                  0.95 |
| postgresql-1-2-1-1 |         2.44 |      0.02 |           0.48 |                  0.54 |
| postgresql-1-2-2-1 |         2.50 |      0.01 |           0.50 |                  0.57 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        88.15 |      1.08 |           0.33 |                  0.33 |
| postgresql-1-1-2-1 |        64.68 |      1.63 |           0.11 |                  0.11 |
| postgresql-1-2-1-1 |        40.74 |      1.07 |           0.28 |                  0.28 |
| postgresql-1-2-2-1 |        83.23 |      1.60 |           0.27 |                  0.28 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |
| postgresql-1-1-2-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                21.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                21.00 |                                                1.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                21.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                21.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Database isolation

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 -xsd 5 -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp 1 -nbp 1 -nbt 10 \
  -xkey \
  -m -ma -mc \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -mtb database -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_collector_tenants_database.log
```

Same as schema isolation but each tenant gets its own PostgreSQL database (`-mtb database`) inside one shared DBMS container.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_collector_tenants_database_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_collector_tenants_database.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1991s 
* Code: 1793576016
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685330
  * datadisk:668
  * volume_size:49G
  * volume_used:668M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793576016
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685331
  * datadisk:669
  * volume_size:49G
  * volume_used:669M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793576016
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685333
  * datadisk:670
  * volume_size:49G
  * volume_used:670M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793576016
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685325
  * datadisk:671
  * volume_size:49G
  * volume_used:671M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793576016
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793576016-7f5c8885f8-bjj8n: 0
* bexhoma-sut-postgresql-1-1793576016-85fd65f47c-dnnkl: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793576016-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |       25.00 |           4.00 |            0.00 |         25.00 |            7.00 |              2 |           1 |              144.00 | False               |
| 1793576016-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |       25.00 |           4.00 |            0.00 |         25.00 |            7.00 |              2 |           1 |              144.00 | False               |
| 1793576016-PostgreSQL-1-2-0 |                2 | database       | False         |             2 |           0 |    1 |       25.00 |           4.00 |            0.00 |         25.00 |            7.00 |              2 |           1 |              144.00 | True                |
| 1793576016-PostgreSQL-1-2-1 |                2 | database       | False         |             2 |           1 |    1 |       25.00 |           4.00 |            0.00 |         25.00 |            7.00 |              2 |           1 |              144.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       101.48 |                                                      31357.00 |                                              14926.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.55 |                        0.55 |       114.77 |                                                      34146.00 |                                              14228.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                      33121.00 |                                              14726.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       107.08 |                                                      34377.00 |                                              14398.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        98.68 |                                                      81468.00 |                                              31531.00 |
| postgresql-1-2-1-1-2 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.28 |                                                      67949.00 |                                              26729.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       100.78 |                                                      44351.00 |                                              21653.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.43 |                        0.43 |        90.98 |                                                      41713.00 |                                              20855.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-0 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       101.48 |                                                      31357.00 |                                              14926.00 |
| postgresql-1-1-1-1 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.55 |                        0.55 |       114.77 |                                                      34146.00 |                                              14228.00 |
| postgresql-1-1-2-0 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                      33121.00 |                                              14726.00 |
| postgresql-1-1-2-1 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       107.08 |                                                      34377.00 |                                              14398.00 |
| postgresql-1-2-1-0 | postgresql-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        98.68 |                                                      81468.00 |                                              31531.00 |
| postgresql-1-2-1-1 | postgresql-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.28 |                                                      67949.00 |                                              26729.00 |
| postgresql-1-2-2-0 | postgresql-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       100.78 |                                                      44351.00 |                                              21653.00 |
| postgresql-1-2-2-1 | postgresql-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.43 |                        0.43 |        90.98 |                                                      41713.00 |                                              20855.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        37.51 |      0.85 |           0.64 |                  0.91 |
| postgresql-1-1-2-1 |        37.51 |      0.85 |           0.64 |                  0.91 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         3.94 |      0.06 |           0.71 |                  0.98 |
| postgresql-1-1-2-1 |         3.64 |      0.02 |           0.71 |                  0.98 |
| postgresql-1-2-1-1 |         4.21 |      0.03 |           0.49 |                  0.56 |
| postgresql-1-2-2-1 |         3.74 |      0.02 |           0.50 |                  0.58 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        18.46 |      0.23 |           0.11 |                  0.11 |
| postgresql-1-1-2-1 |        59.37 |      1.66 |           0.34 |                  0.34 |
| postgresql-1-2-1-1 |        48.64 |      1.02 |           0.28 |                  0.28 |
| postgresql-1-2-2-1 |        18.05 |      0.22 |           0.11 |                  0.11 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 5.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |
| postgresql-1-1-2-1 |                                 5.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                23.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                23.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                23.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-2-2-1 |                                23.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

### Container isolation

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 -xsd 5 -nc 2 \
  -ne "1,1" \
  -nlp 1 -nbp 1 -nbt 10 \
  -xkey \
  -m -ma -mc \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -mtb container -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_collector_tenants_container.log
```

Each tenant gets its own separate DBMS container (`-mtb container`). `-ne "1,1"` means 1 loader and 1 benchmarker pod per tenant. Storage is reduced to 10Gi per tenant since each container has its own volume.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_collector_tenants_container_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_collector_tenants_container.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2664s 
* Code: 1793578044
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685318
  * datadisk:330
  * volume_size:49G
  * volume_used:330M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685320
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685322
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685324
  * datadisk:332
  * volume_size:49G
  * volume_used:332M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685323
  * datadisk:330
  * volume_size:49G
  * volume_used:330M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* postgresql-2-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685320
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* postgresql-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685322
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* postgresql-2-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685324
  * datadisk:332
  * volume_size:49G
  * volume_used:332M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793578044
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2, PostgreSQL-2-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks
* PostgreSQL-2: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793578044-77b89f66f8-x22tw: 0
* bexhoma-sut-postgresql-1-1793578044-866b7785f-phl2k: 0
* bexhoma-sut-postgresql-2-1793578044-59d4fd97bd-q46zr: 0
* bexhoma-sut-postgresql-2-1793578044-668bf4f4f4-h8k5w: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: benchbase (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793578044-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |       30.00 |           3.00 |            0.00 |         23.00 |            4.00 |              1 |           1 |              120.00 | False               |
| 1793578044-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |       31.00 |           3.00 |            0.00 |         23.00 |            5.00 |              1 |           1 |              116.13 | False               |
| 1793578044-PostgreSQL-1-2-0 |                2 | container      | False         |             2 |           0 |    1 |       30.00 |           3.00 |            0.00 |         23.00 |            4.00 |              1 |           1 |              120.00 | True                |
| 1793578044-PostgreSQL-2-2-1 |                2 | container      | False         |             2 |           1 |    1 |       31.00 |           3.00 |            0.00 |         23.00 |            5.00 |              1 |           1 |              116.13 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      35507.00 |                                              15676.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                      29284.00 |                                              13355.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       100.78 |                                                      75945.00 |                                              28280.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.53 |                        0.53 |       110.58 |                                                      38261.00 |                                              17962.00 |
| postgresql-2-1-1-1-1 | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           1 | 300.00 |            0 |                           0.56 |                        0.56 |       117.57 |                                                      34815.00 |                                              14499.00 |
| postgresql-2-1-2-1-1 | postgresql-2-1-2 | postgresql-2-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      32721.00 |                                              14931.00 |
| postgresql-2-2-1-1-1 | postgresql-2-2-1 | postgresql-2-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           1 | 300.00 |            0 |                           0.45 |                        0.45 |        95.18 |                                                      81465.00 |                                              29634.00 |
| postgresql-2-2-2-1-1 | postgresql-2-2-2 | postgresql-2-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      40503.00 |                                              19088.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-0 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      35507.00 |                                              15676.00 |
| postgresql-1-1-2-0 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                      29284.00 |                                              13355.00 |
| postgresql-1-2-1-0 | postgresql-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.48 |                        0.48 |       100.78 |                                                      75945.00 |                                              28280.00 |
| postgresql-1-2-2-0 | postgresql-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.53 |                        0.53 |       110.58 |                                                      38261.00 |                                              17962.00 |
| postgresql-2-1-1-1 | postgresql-2-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.56 |                        0.56 |       117.57 |                                                      34815.00 |                                              14499.00 |
| postgresql-2-1-2-1 | postgresql-2-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      32721.00 |                                              14931.00 |
| postgresql-2-2-1-1 | postgresql-2-2-1 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.45 |                        0.45 |        95.18 |                                                      81465.00 |                                              29634.00 |
| postgresql-2-2-2-1 | postgresql-2-2-2 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      40503.00 |                                              19088.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        16.71 |      0.44 |           0.51 |                  0.66 |
| postgresql-1-1-2-1 |        16.71 |      0.44 |           0.51 |                  0.66 |
| postgresql-2-1-1-1 |        16.86 |      0.53 |           0.51 |                  0.66 |
| postgresql-2-1-2-1 |        16.86 |      0.53 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         1.69 |      0.01 |           0.54 |                  0.68 |
| postgresql-1-1-2-1 |         1.56 |      0.01 |           0.54 |                  0.68 |
| postgresql-1-2-1-1 |         1.96 |      0.01 |           0.44 |                  0.47 |
| postgresql-1-2-2-1 |         1.51 |      0.01 |           0.44 |                  0.48 |
| postgresql-2-1-1-1 |         1.75 |      0.01 |           0.54 |                  0.68 |
| postgresql-2-1-2-1 |         1.55 |      0.01 |           0.54 |                  0.68 |
| postgresql-2-2-1-1 |         1.65 |      0.01 |           0.43 |                  0.46 |
| postgresql-2-2-2-1 |         1.66 |      0.02 |           0.44 |                  0.47 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        29.93 |      0.80 |           0.33 |                  0.33 |
| postgresql-1-1-2-1 |        26.01 |      1.00 |           0.11 |                  0.11 |
| postgresql-1-2-1-1 |        64.20 |      1.01 |           0.28 |                  0.28 |
| postgresql-1-2-2-1 |        15.14 |      0.19 |           0.11 |                  0.11 |
| postgresql-2-1-1-1 |        42.77 |      0.65 |           0.27 |                  0.27 |
| postgresql-2-1-2-1 |        11.27 |      0.13 |           0.22 |                  0.22 |
| postgresql-2-2-1-1 |         9.64 |      0.09 |           0.11 |                  0.11 |
| postgresql-2-2-2-1 |        15.50 |      0.21 |           0.11 |                  0.11 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Tx Total [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-1-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-2-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-2-1-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-2-1-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-2-2-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-2-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

## TPC-H

### Test 1: SF=3, fresh PVC

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 -xqr 3 -nc 2 -ne 1,2 \
  -nlp 8 -nbp 1 \
  -xii -xic -xis \
  -m -ma -mc \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_collector_1.log
```

This
* loads TPC-H data at SF=3 using 8 parallel loader pods (`-nlp 8`) into a fresh 30Gi volume
* repeats each query 3 times (`-xqr 3`) so even the single-stream configuration runs long enough for resource monitoring to capture samples
* runs 2 experiment iterations (`-nc 2`) each with two stream configurations (`-ne 1,2`): 1 then 2 concurrent benchmarking pods
* sets indexes, constraints, and statistics after loading (`-xii -xic -xis`)
* verifies workflow matches plan (`-tr`)

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_collector_1_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_collector_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1321s 
* Code: 1793580776
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Each query is repeated 3 times.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685328
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793580776
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685329
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793580776
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685329
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793580776
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685331
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793580776
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685332
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793580776
* postgresql-1-2-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685332
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793580776

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793580776-55789b46df-hbt4q: 0
* bexhoma-sut-postgresql-1-1793580776-7b9d5868-d297j: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      100.00 |           4.00 |           25.00 |         24.00 |           42.00 |              8 |           0 |             |                |             0 | False         |              108.00 | False               |
| PostgreSQL-1-2 |                2 |    3 |      100.00 |           4.00 |           25.00 |         24.00 |           42.00 |              8 |           0 |             |                |             0 | False         |              108.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         67 |            0.51 |            21214.42 |          10638.81 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         67 |            0.51 |            21110.88 |          10638.81 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         68 |            0.51 |            21244.35 |          10482.35 |           0 | postgresql-1-1-2-1-2 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         82 |            0.57 |            19010.37 |           8692.68 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         73 |            0.55 |            19624.69 |           9764.38 |           0 | postgresql-1-2-2-1-1 |
| postgresql-1-2-2-1-2 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         73 |            0.55 |            19479.41 |           9764.38 |           0 | postgresql-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         67 |            0.51 |            21214.42 |          10638.81 |           0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |                 132 |         68 |            0.51 |            21177.51 |          20964.71 |           0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         82 |            0.57 |            19010.37 |           8692.68 |           0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |                 132 |         73 |            0.55 |            19551.92 |          19528.77 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-2-1-1-1 |   postgresql-1-2-2-1-1 |   postgresql-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1542.54 |                1553.43 |                1550.16 |                2389.23 |                1905.32 |                1852.74 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 479.85 |                 518.42 |                 651.21 |                1313.90 |                 451.32 |                 445.70 |
| Shipping Priority (TPC-H Q3)                        |                 484.46 |                 539.83 |                 505.64 |                 898.94 |                 627.84 |                 591.42 |
| Order Priority Checking Query (TPC-H Q4)            |                 241.07 |                 238.46 |                 240.83 |                 248.79 |                 237.65 |                 257.69 |
| Local Supplier Volume (TPC-H Q5)                    |                 517.41 |                 487.99 |                 489.80 |                 731.82 |                 535.00 |                 507.00 |
| Forecasting Revenue Change (TPC-H Q6)               |                 264.35 |                 305.60 |                 305.73 |                 292.68 |                 299.18 |                 299.21 |
| Volume Shipping Query (TPC-H Q7)                    |                 750.24 |                 651.17 |                 651.02 |                 829.91 |                 739.17 |                 739.94 |
| National Market Share (TPC-H Q8)                    |                 317.89 |                 308.26 |                 308.36 |                1278.63 |                 308.19 |                 308.59 |
| Product Type Profit Measure (TPC-H Q9)              |                 908.19 |                 860.45 |                 870.65 |                1288.85 |                1121.12 |                1126.55 |
| Returned Item Reporting Query (TPC-H Q10)           |                1334.54 |                1120.79 |                1111.91 |                1286.24 |                1273.86 |                1295.44 |
| Important Stock Identification (TPC-H Q11)          |                 179.96 |                 141.25 |                 155.68 |                 166.36 |                 159.11 |                 157.58 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 457.08 |                 453.87 |                 454.10 |                 448.98 |                 461.97 |                 460.73 |
| Customer Distribution (TPC-H Q13)                   |                1991.46 |                1912.97 |                1863.25 |                2119.50 |                2257.46 |                2092.33 |
| Promotion Effect Query (TPC-H Q14)                  |                 492.29 |                 683.68 |                 685.98 |                 468.56 |                 693.19 |                 491.16 |
| Top Supplier Query (TPC-H Q15)                      |                 376.16 |                 401.04 |                 400.76 |                 375.75 |                 400.52 |                 562.70 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 334.75 |                 348.37 |                 349.87 |                 562.29 |                 343.70 |                 406.96 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1632.37 |                1639.72 |                1639.62 |                1645.15 |                1804.23 |                1875.21 |
| Large Volume Customer (TPC-H Q18)                   |                7887.26 |                7909.25 |                8002.24 |                8878.35 |                8828.21 |                8922.21 |
| Discounted Revenue (TPC-H Q19)                      |                  75.23 |                  74.12 |                  64.37 |                  78.08 |                  83.23 |                  78.05 |
| Potential Part Promotion (TPC-H Q20)                |                 290.07 |                 270.98 |                 260.87 |                 266.71 |                 285.59 |                 299.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 488.18 |                 503.87 |                 505.44 |                 499.03 |                 579.13 |                 681.97 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 127.87 |                 129.69 |                 123.77 |                 167.98 |                 229.78 |                 125.72 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       100.18 |      1.71 |           4.59 |                  8.84 |
| postgresql-1-1-2-1 |       100.18 |      1.71 |           4.59 |                  8.84 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.55 |           0.00 |                  0.28 |
| postgresql-1-1-2-1 | n/a          |      0.55 |           0.00 |                  0.28 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       107.66 |      3.05 |           4.98 |                  9.79 |
| postgresql-1-1-2-1 |       335.49 |      7.38 |           8.60 |                 15.55 |
| postgresql-1-2-1-1 |       211.16 |      3.30 |           9.92 |                 14.65 |
| postgresql-1-2-2-1 |       267.34 |      6.89 |           5.12 |                  9.45 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        13.70 |      0.46 |           0.28 |                  0.29 |
| postgresql-1-1-2-1 |        25.52 |      0.60 |           0.31 |                  0.31 |
| postgresql-1-2-1-1 |        12.90 |      0.02 |           0.28 |                  0.28 |
| postgresql-1-2-2-1 |        30.07 |      0.88 |           0.33 |                  0.33 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  10.00 |                                              10.00 |
| postgresql-1-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   7.00 |                                               7.00 |
| postgresql-1-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  10.00 |                                              10.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
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

### Test 2: SF=6, fresh PVC

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 6 -nc 2 -ne 1,2 \
  -nlp 8 -nbp 1 \
  -xii -xic -xis \
  -m -ma -mc \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_collector_2.log
```

Same as test 1 but doubles the scaling factor to SF=6. The PVC is recreated (`-rsr`).

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_collector_2_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_collector_2.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=6
* Type: tpch
* Duration: 3032s 
* Code: 1793582179
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=6) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685335
  * datadisk:16351
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793582179
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685335
  * datadisk:16351
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793582179
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685335
  * datadisk:16351
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793582179
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685352
  * datadisk:16351
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793582179
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685352
  * datadisk:16351
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793582179
* postgresql-1-2-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685352
  * datadisk:16351
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793582179

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793582179-644c446c86-94trn: 0
* bexhoma-sut-postgresql-1-1793582179-7c9fdbbb7d-xvl8q: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    6 |      204.00 |           3.00 |           19.00 |         52.00 |          126.00 |              8 |           0 |             |                |             0 | False         |              105.88 | False               |
| PostgreSQL-1-2 |                2 |    6 |      204.00 |           3.00 |           19.00 |         52.00 |          126.00 |              8 |           0 |             |                |             0 | False         |              105.88 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         52 |            1.24 |            17438.08 |           9138.46 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         54 |            1.21 |            17905.61 |           8800.00 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         54 |            1.23 |            17567.18 |           8800.00 |           0 | postgresql-1-1-2-1-2 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         65 |            1.57 |            13790.91 |           7310.77 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         52 |            1.20 |            17982.06 |           9138.46 |           0 | postgresql-1-2-2-1-1 |
| postgresql-1-2-2-1-2 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         53 |            1.24 |            17353.95 |           8966.04 |           0 | postgresql-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         52 |            1.24 |            17438.08 |           9138.46 |           0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 6.00 |               44 |                  44 |         54 |            1.22 |            17735.58 |          17600.00 |           0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         65 |            1.57 |            13790.91 |           7310.77 |           0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        2 |               1 |           2 | 6.00 |               44 |                  44 |         53 |            1.22 |            17665.21 |          17932.08 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-2-1-1-1 |   postgresql-1-2-2-1-1 |   postgresql-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                3203.81 |                3709.64 |                3723.82 |                7379.62 |                3268.79 |                3164.10 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                1314.62 |                1162.70 |                1141.67 |                6306.58 |                1246.95 |                1221.03 |
| Shipping Priority (TPC-H Q3)                        |                1996.34 |                1494.51 |                1437.91 |                3827.64 |                1071.49 |                1115.60 |
| Order Priority Checking Query (TPC-H Q4)            |                 753.78 |                 451.19 |                 456.73 |                 611.65 |                 464.52 |                 476.74 |
| Local Supplier Volume (TPC-H Q5)                    |                1857.57 |                1459.99 |                1459.51 |                1739.08 |                1356.73 |                1379.42 |
| Forecasting Revenue Change (TPC-H Q6)               |                 689.74 |                1091.97 |                1101.01 |                 783.56 |                 709.77 |                 764.96 |
| Volume Shipping Query (TPC-H Q7)                    |                1984.88 |                1780.20 |                1753.23 |                1798.60 |                1711.66 |                1644.16 |
| National Market Share (TPC-H Q8)                    |                 782.81 |                 736.70 |                 736.26 |                5118.11 |                 644.87 |                 675.05 |
| Product Type Profit Measure (TPC-H Q9)              |                1937.91 |                2108.91 |                2115.26 |                2886.72 |                1866.39 |                2326.13 |
| Returned Item Reporting Query (TPC-H Q10)           |                1806.84 |                1388.88 |                1496.32 |                1517.45 |                2126.93 |                1578.69 |
| Important Stock Identification (TPC-H Q11)          |                 407.72 |                 360.44 |                 331.35 |                 360.37 |                 402.76 |                 423.73 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1073.83 |                1256.13 |                1220.65 |                1107.30 |                1085.96 |                1086.88 |
| Customer Distribution (TPC-H Q13)                   |                4568.58 |                4894.13 |                5054.20 |                4214.41 |                4376.88 |                4473.20 |
| Promotion Effect Query (TPC-H Q14)                  |                 986.12 |                1023.42 |                1085.76 |                1143.64 |                1195.04 |                1177.19 |
| Top Supplier Query (TPC-H Q15)                      |                1284.82 |                 927.02 |                 890.82 |                 922.35 |                 943.24 |                 957.25 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 537.69 |                 564.97 |                 980.48 |                 576.38 |                 584.21 |                 852.61 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                3065.78 |                3616.53 |                2980.37 |                3294.69 |                3988.16 |                3407.64 |
| Large Volume Customer (TPC-H Q18)                   |               19288.55 |               20814.80 |               20327.72 |               17447.32 |               20437.48 |               21035.77 |
| Discounted Revenue (TPC-H Q19)                      |                 157.66 |                 143.95 |                 156.16 |                 182.36 |                 179.29 |                 387.12 |
| Potential Part Promotion (TPC-H Q20)                |                 698.77 |                 758.96 |                 778.12 |                 883.88 |                 926.21 |                 751.37 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                1227.11 |                1314.89 |                1305.64 |                1308.72 |                1498.11 |                1280.17 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 230.48 |                 270.92 |                 276.10 |                 260.84 |                 257.89 |                 264.25 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       246.14 |      2.03 |           4.45 |                 12.29 |
| postgresql-1-1-2-1 |       246.14 |      2.03 |           4.45 |                 12.29 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        47.89 |      1.86 |           0.01 |                  0.56 |
| postgresql-1-1-2-1 |        47.89 |      1.86 |           0.01 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       129.46 |      3.39 |          15.75 |                 25.35 |
| postgresql-1-1-2-1 |       364.89 |      8.10 |          18.16 |                 37.86 |
| postgresql-1-2-1-1 |        90.05 |      2.86 |           9.19 |                 17.84 |
| postgresql-1-2-2-1 |       376.75 |     10.07 |          14.33 |                 33.04 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        13.27 |      0.43 |           0.29 |                  0.29 |
| postgresql-1-1-2-1 |        26.85 |      0.88 |           0.27 |                  0.27 |
| postgresql-1-2-1-1 |        14.24 |      0.02 |           0.32 |                  0.32 |
| postgresql-1-2-2-1 |        27.90 |      0.71 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   8.00 |                                               8.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   8.00 |                                               8.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  12.00 |                                              12.00 |
| postgresql-1-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |
| postgresql-1-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  14.00 |                                              14.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
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

### Test 3: SF=6, reuse PVC

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 6 -nc 2 -ne 1,2 \
  -nlp 8 -nbp 1 \
  -xii -xic -xis \
  -m -ma -mc \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rss 60Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_collector_3.log
```

Same parameters as test 2 but without `-rsr -rst`. The persistent volume is reused, so loading is skipped.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_collector_3_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_collector_3.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=6
* Type: tpch
* Duration: 1454s 
* Code: 1793585285
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=6) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 60Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:701695
  * datadisk:16351
  * volume_size:1.8T
  * volume_used:686G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793585285
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:701695
  * datadisk:16351
  * volume_size:1.8T
  * volume_used:686G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793585285
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:701695
  * datadisk:16351
  * volume_size:1.8T
  * volume_used:686G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793585285
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:701697
  * datadisk:16350
  * volume_size:1.8T
  * volume_used:686G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793585285
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:701697
  * datadisk:16350
  * volume_size:1.8T
  * volume_used:686G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793585285
* postgresql-1-2-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:701697
  * datadisk:16350
  * volume_size:1.8T
  * volume_used:686G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793585285

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793585285-5b5ffd7889-bdt6s: 0
* bexhoma-sut-postgresql-1-1793585285-6b865dcd94-dkt2k: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    6 |      193.00 |           3.00 |           23.00 |         36.00 |          126.00 |              8 |           0 |             |                |             0 | False         |              111.92 | False               |
| PostgreSQL-1-2 |                2 |    6 |      180.00 |           3.00 |           22.00 |         35.00 |          115.00 |              8 |           0 |             |                |             0 | False         |              120.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         50 |            1.21 |            17862.05 |           9504.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         52 |            1.17 |            18388.81 |           9138.46 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         50 |            1.21 |            17920.61 |           9504.00 |           0 | postgresql-1-1-2-1-2 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         53 |            1.26 |            17093.18 |           8966.04 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         51 |            1.20 |            17994.81 |           9317.65 |           0 | postgresql-1-2-2-1-1 |
| postgresql-1-2-2-1-2 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 6.00 |               22 |                  22 |         51 |            1.19 |            18136.59 |           9317.65 |           0 | postgresql-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         50 |            1.21 |            17862.05 |           9504.00 |           0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 6.00 |               44 |                  44 |         52 |            1.19 |            18153.20 |          18276.92 |           0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 6.00 |               22 |                  22 |         53 |            1.26 |            17093.18 |           8966.04 |           0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        2 |               1 |           2 | 6.00 |               44 |                  44 |         51 |            1.20 |            18065.56 |          18635.29 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-2-1-1-1 |   postgresql-1-2-2-1-1 |   postgresql-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                2874.32 |                3154.74 |                3113.83 |                2890.92 |                3369.82 |                3358.83 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                1277.68 |                1234.16 |                1189.41 |                1267.95 |                1199.47 |                1138.19 |
| Shipping Priority (TPC-H Q3)                        |                2341.63 |                1236.73 |                1229.17 |                1852.65 |                1180.76 |                1181.23 |
| Order Priority Checking Query (TPC-H Q4)            |                 599.13 |                 563.28 |                 977.35 |                 601.32 |                 483.73 |                 472.57 |
| Local Supplier Volume (TPC-H Q5)                    |                1366.45 |                1886.98 |                1599.86 |                1452.90 |                1320.78 |                1326.67 |
| Forecasting Revenue Change (TPC-H Q6)               |                 848.01 |                 704.18 |                 705.96 |                 821.09 |                 708.15 |                 734.85 |
| Volume Shipping Query (TPC-H Q7)                    |                1729.51 |                1613.82 |                1656.44 |                1728.18 |                1929.07 |                1965.44 |
| National Market Share (TPC-H Q8)                    |                 784.09 |                 652.42 |                 624.62 |                 763.65 |                 645.41 |                 629.46 |
| Product Type Profit Measure (TPC-H Q9)              |                1848.89 |                1775.25 |                1692.87 |                2328.57 |                2270.29 |                2190.06 |
| Returned Item Reporting Query (TPC-H Q10)           |                1624.31 |                1620.67 |                1664.88 |                1602.66 |                1548.46 |                1584.90 |
| Important Stock Identification (TPC-H Q11)          |                 386.82 |                 401.20 |                 359.28 |                 410.81 |                 398.84 |                 366.01 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1079.22 |                1065.61 |                1065.98 |                1108.62 |                1032.07 |                1057.05 |
| Customer Distribution (TPC-H Q13)                   |                3742.45 |                3731.99 |                4001.91 |                4534.24 |                3825.74 |                3817.75 |
| Promotion Effect Query (TPC-H Q14)                  |                1393.63 |                1110.32 |                1140.05 |                1141.03 |                1141.28 |                1122.01 |
| Top Supplier Query (TPC-H Q15)                      |                 894.90 |                 918.78 |                 941.90 |                 912.09 |                 930.08 |                 918.33 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 547.44 |                 544.31 |                 544.63 |                 538.43 |                 544.64 |                 537.55 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                3334.31 |                3192.91 |                3492.86 |                3470.02 |                3301.92 |                3277.02 |
| Large Volume Customer (TPC-H Q18)                   |               19441.43 |               20052.11 |               19494.66 |               18585.08 |               18315.76 |               18304.70 |
| Discounted Revenue (TPC-H Q19)                      |                 164.07 |                 157.81 |                 178.10 |                 166.90 |                 166.62 |                 166.54 |
| Potential Part Promotion (TPC-H Q20)                |                 748.76 |                 691.86 |                 752.92 |                1812.52 |                1836.40 |                1835.42 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                1264.22 |                1980.20 |                2046.01 |                1281.45 |                1333.56 |                1334.64 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 250.42 |                 257.67 |                 247.96 |                 248.01 |                 261.66 |                 261.36 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       268.95 |      2.00 |           3.81 |                 12.35 |
| postgresql-1-1-2-1 |       268.95 |      2.00 |           3.81 |                 12.35 |
| postgresql-1-2-1-1 |       256.34 |      2.21 |           3.34 |                 12.43 |
| postgresql-1-2-2-1 |       256.34 |      2.21 |           3.34 |                 12.43 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-2-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | 23.44        |      0.31 |           0.00 |                  0.56 |
| postgresql-1-1-2-1 | 23.44        |      0.31 |           0.00 |                  0.56 |
| postgresql-1-2-1-1 | n/a          |      0.65 |           0.01 |                  0.56 |
| postgresql-1-2-2-1 | n/a          |      0.65 |           0.01 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       166.06 |      4.15 |          16.24 |                 30.84 |
| postgresql-1-1-2-1 |       402.88 |      9.42 |          16.58 |                 36.35 |
| postgresql-1-2-1-1 |       158.23 |      3.84 |          16.40 |                 29.44 |
| postgresql-1-2-2-1 |       326.14 |      8.17 |          15.82 |                 35.44 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        13.06 |      0.47 |           0.28 |                  0.28 |
| postgresql-1-1-2-1 |        25.95 |      0.83 |           0.29 |                  0.29 |
| postgresql-1-2-1-1 |        12.88 |      0.41 |           0.27 |                  0.28 |
| postgresql-1-2-2-1 |        26.71 |      0.83 |           0.29 |                  0.29 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   8.00 |                                               8.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   8.00 |                                               8.00 |
| postgresql-1-2-1-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |
| postgresql-1-2-2-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  12.00 |                                              12.00 |
| postgresql-1-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |
| postgresql-1-2-2-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
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

## TPC-H Multi-Tenant

### Schema isolation

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 \
  -nbp 1 -nbt 64 \
  -xii -xic -xis \
  -m -ma -mc \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -mtb schema -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_collector_tenants_schema.log
```

Runs TPC-H with 2 tenants isolated by schema, each loaded by 1 of 2 parallel loader pods (`-nlp $BEXHOMA_NUM_TENANTS`), each benchmarked by 64 threads.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_collector_tenants_schema_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_collector_tenants_schema.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1515s 
* Code: 1793586815
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685351
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-1-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685351
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685352
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685352
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685353
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-2-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685353
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685353
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-2-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685353
  * datadisk:16354
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793586815
    * TENANT_BY:schema
    * TENANT_NUM:2

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema_tenant, indexing=Index_and_Constraints_and_Statistics_tenant

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793586815-7fdccd7f44-thxbv: 0
* bexhoma-sut-postgresql-1-1793586815-5cdb4ffd78-n4jql: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793586815-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    3 |      119.00 |           4.00 |            1.00 |        119.00 |           45.00 |              2 |           0 |               90.76 | False               |
| 1793586815-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    3 |      118.00 |           4.00 |            1.00 |        118.00 |           45.00 |              2 |           0 |               91.53 | False               |
| 1793586815-PostgreSQL-1-2-0 |                2 | schema         | False         |             2 |           0 |    3 |      119.00 |           4.00 |            1.00 |        119.00 |           45.00 |              2 |           0 |               90.76 | True                |
| 1793586815-PostgreSQL-1-2-1 |                2 | schema         | False         |             2 |           1 |    3 |      118.00 |           4.00 |            1.00 |        118.00 |           45.00 |              2 |           0 |               91.53 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         26 |            0.55 |            19798.62 |           9138.46 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-1-1-2 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.54 |            20050.00 |           9504.00 |           1 | postgresql-1-1-1-1-2 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.55 |            19530.72 |           9504.00 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         24 |            0.55 |            19673.96 |           9900.00 |           1 | postgresql-1-1-2-1-2 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         35 |            0.82 |            13111.14 |           6788.57 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-1-1-2 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         36 |            0.80 |            13426.70 |           6600.00 |           1 | postgresql-1-2-1-1-2 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         28 |            0.61 |            17827.84 |           8485.71 |           0 | postgresql-1-2-2-1-1 |
| postgresql-1-2-2-1-2 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         27 |            0.58 |            18681.95 |           8800.00 |           1 | postgresql-1-2-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         26 |            0.55 |            19798.62 |           9138.46 |           0 |
| postgresql-1-1-1_1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.54 |            20050.00 |           9504.00 |           1 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.55 |            19530.72 |           9504.00 |           0 |
| postgresql-1-1-2_1 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         24 |            0.55 |            19673.96 |           9900.00 |           1 |
| postgresql-1-2-1_0 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         35 |            0.82 |            13111.14 |           6788.57 |           0 |
| postgresql-1-2-1_1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         36 |            0.80 |            13426.70 |           6600.00 |           1 |
| postgresql-1-2-2_0 | postgresql-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         28 |            0.61 |            17827.84 |           8485.71 |           0 |
| postgresql-1-2-2_1 | postgresql-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         27 |            0.58 |            18681.95 |           8800.00 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-1 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-1-1-2 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-2-1-1-1 |   postgresql-1-2-1-1-2 |   postgresql-1-2-2-1-1 |   postgresql-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1612.40 |                1608.60 |                1812.46 |                1984.89 |                3765.30 |                3631.48 |                1612.79 |                1602.14 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 542.19 |                 564.70 |                 892.64 |                 678.69 |                2162.45 |                2151.94 |                 533.98 |                 545.04 |
| Shipping Priority (TPC-H Q3)                        |                 595.46 |                 573.98 |                 565.85 |                 560.97 |                1784.97 |                1917.18 |                 553.04 |                 540.22 |
| Order Priority Checking Query (TPC-H Q4)            |                 289.70 |                 288.60 |                 288.41 |                 281.54 |                 296.21 |                 281.09 |                 278.25 |                 280.55 |
| Local Supplier Volume (TPC-H Q5)                    |                 609.08 |                 624.51 |                 613.20 |                 606.18 |                 757.73 |                 715.35 |                 786.26 |                1032.23 |
| Forecasting Revenue Change (TPC-H Q6)               |                 296.66 |                 303.95 |                 300.53 |                 312.58 |                 308.90 |                 303.36 |                 654.70 |                 307.41 |
| Volume Shipping Query (TPC-H Q7)                    |                 719.23 |                 769.15 |                 741.94 |                 745.68 |                 776.14 |                 704.43 |                 763.99 |                 788.28 |
| National Market Share (TPC-H Q8)                    |                 429.86 |                 393.99 |                 356.34 |                 348.56 |                2465.89 |                2521.29 |                 375.32 |                 378.66 |
| Product Type Profit Measure (TPC-H Q9)              |                 954.31 |                 947.31 |                 965.17 |                 969.30 |                1715.15 |                1840.05 |                1046.97 |                 988.69 |
| Returned Item Reporting Query (TPC-H Q10)           |                 528.73 |                 513.96 |                 544.48 |                 537.41 |                 501.78 |                 722.10 |                 530.21 |                 532.13 |
| Important Stock Identification (TPC-H Q11)          |                 190.06 |                 185.88 |                 189.91 |                 184.04 |                 388.81 |                 208.44 |                 168.86 |                 198.60 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 458.72 |                 469.48 |                 477.06 |                 483.71 |                 688.67 |                 485.99 |                 475.89 |                 473.02 |
| Customer Distribution (TPC-H Q13)                   |                1887.18 |                1885.70 |                1868.79 |                1908.11 |                1980.34 |                1910.74 |                1929.00 |                2105.15 |
| Promotion Effect Query (TPC-H Q14)                  |                 508.61 |                 519.79 |                 546.90 |                 543.57 |                 538.53 |                 542.58 |                 870.94 |                 863.86 |
| Top Supplier Query (TPC-H Q15)                      |                 405.55 |                 389.94 |                 410.30 |                 427.98 |                 682.55 |                 834.09 |                 771.26 |                 434.56 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 395.11 |                 316.54 |                 321.74 |                 318.98 |                 668.13 |                 423.33 |                 390.14 |                 336.63 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1711.27 |                1687.87 |                1686.85 |                1676.99 |                1712.92 |                1723.52 |                1623.44 |                1606.82 |
| Large Volume Customer (TPC-H Q18)                   |                8107.32 |                7731.16 |                8220.61 |                8136.27 |                9287.37 |                9417.26 |                8651.23 |                8865.99 |
| Discounted Revenue (TPC-H Q19)                      |                  81.95 |                  78.64 |                  81.54 |                  85.39 |                  96.10 |                 100.28 |                 100.56 |                  94.99 |
| Potential Part Promotion (TPC-H Q20)                |                 344.99 |                 368.92 |                 327.06 |                 328.45 |                 347.56 |                 376.83 |                 341.52 |                 342.24 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 499.74 |                 516.20 |                 535.51 |                 535.11 |                 535.71 |                 671.72 |                 533.92 |                 516.00 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 144.94 |                 141.10 |                 133.55 |                 132.09 |                 228.14 |                 252.46 |                 143.14 |                 147.46 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       179.86 |      1.87 |           8.30 |                 17.77 |
| postgresql-1-1-2-1 |       179.86 |      1.87 |           8.30 |                 17.77 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        74.87 |      0.89 |           0.01 |                  1.46 |
| postgresql-1-1-2-1 |        74.87 |      0.89 |           0.01 |                  1.46 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      1.63 |           9.05 |                 18.62 |
| postgresql-1-1-2-1 | n/a          |      0.58 |           9.57 |                 19.14 |
| postgresql-1-2-1-1 | 16.55        |      0.56 |           3.54 |                  6.45 |
| postgresql-1-2-2-1 | n/a          |      2.46 |           9.30 |                 17.96 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-2-1-1 | 26.73        |      0.00 |           0.28 |                  0.28 |
| postgresql-1-2-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  10.00 |                                              10.00 |
| postgresql-1-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                  10.00 |                                              10.00 |
| postgresql-1-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
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

### Database isolation

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 \
  -nbp 1 -nbt 64 \
  -xii -xic -xis \
  -m -ma -mc \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -mtb database -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_collector_tenants_database.log
```

Same as schema isolation but each tenant gets its own PostgreSQL database (`-mtb database`).

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_collector_tenants_database_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_collector_tenants_database.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1146s 
* Code: 1793588409
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685346
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-1-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685346
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685347
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685347
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685348
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-2-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685348
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685348
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-2-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685348
  * datadisk:16384
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793588409
    * TENANT_BY:database
    * TENANT_NUM:2

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793588409-86475d9797-wmlv2: 0
* bexhoma-sut-postgresql-1-1793588409-6b65fc6fb6-6v9c8: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793588409-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    3 |      109.00 |           4.00 |            1.00 |        109.00 |           47.00 |              2 |           0 |               99.08 | False               |
| 1793588409-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    3 |      110.00 |           4.00 |            1.00 |        110.00 |           47.00 |              2 |           0 |               98.18 | False               |
| 1793588409-PostgreSQL-1-2-0 |                2 | database       | False         |             2 |           0 |    3 |      109.00 |           4.00 |            1.00 |        109.00 |           47.00 |              2 |           0 |               99.08 | True                |
| 1793588409-PostgreSQL-1-2-1 |                2 | database       | False         |             2 |           1 |    3 |      110.00 |           4.00 |            1.00 |        110.00 |           47.00 |              2 |           0 |               98.18 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         23 |            0.54 |            19948.05 |          10330.43 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-1-1-2 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.52 |            20621.79 |           9504.00 |           1 | postgresql-1-1-1-1-2 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         23 |            0.54 |            19930.25 |          10330.43 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         23 |            0.53 |            20563.85 |          10330.43 |           1 | postgresql-1-1-2-1-2 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         35 |            0.78 |            13772.80 |           6788.57 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-1-1-2 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         36 |            0.75 |            14396.66 |           6600.00 |           1 | postgresql-1-2-1-1-2 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.54 |            20143.77 |           9504.00 |           0 | postgresql-1-2-2-1-1 |
| postgresql-1-2-2-1-2 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.54 |            20028.83 |           9504.00 |           1 | postgresql-1-2-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         23 |            0.54 |            19948.05 |          10330.43 |           0 |
| postgresql-1-1-1_1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.52 |            20621.79 |           9504.00 |           1 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         23 |            0.54 |            19930.25 |          10330.43 |           0 |
| postgresql-1-1-2_1 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         23 |            0.53 |            20563.85 |          10330.43 |           1 |
| postgresql-1-2-1_0 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         35 |            0.78 |            13772.80 |           6788.57 |           0 |
| postgresql-1-2-1_1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         36 |            0.75 |            14396.66 |           6600.00 |           1 |
| postgresql-1-2-2_0 | postgresql-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.54 |            20143.77 |           9504.00 |           0 |
| postgresql-1-2-2_1 | postgresql-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  22 |         25 |            0.54 |            20028.83 |           9504.00 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-1 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-2-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-1-1-2 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-2-1-1-1 |   postgresql-1-2-1-1-2 |   postgresql-1-2-2-1-1 |   postgresql-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1596.54 |                1597.83 |                1730.69 |                1607.91 |                3967.14 |                3919.74 |                1597.39 |                1602.68 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 543.38 |                 543.35 |                 511.25 |                 532.82 |                2567.40 |                2492.36 |                 487.57 |                 560.36 |
| Shipping Priority (TPC-H Q3)                        |                 557.07 |                 567.86 |                 497.29 |                 538.34 |                1993.21 |                2174.98 |                 531.10 |                 533.38 |
| Order Priority Checking Query (TPC-H Q4)            |                 274.63 |                 259.28 |                 261.27 |                 269.12 |                 272.88 |                 278.17 |                 271.23 |                 267.69 |
| Local Supplier Volume (TPC-H Q5)                    |                 564.67 |                 569.86 |                 604.99 |                 581.69 |                 885.15 |                1270.00 |                 543.89 |                 584.06 |
| Forecasting Revenue Change (TPC-H Q6)               |                 301.51 |                 295.22 |                 296.36 |                 299.86 |                 721.13 |                 304.51 |                 299.93 |                 299.18 |
| Volume Shipping Query (TPC-H Q7)                    |                 677.61 |                 652.76 |                 741.34 |                 729.42 |                 797.25 |                 775.65 |                 697.91 |                 722.79 |
| National Market Share (TPC-H Q8)                    |                 328.41 |                 311.30 |                 352.29 |                 343.57 |                2653.97 |                2661.59 |                 306.69 |                 318.71 |
| Product Type Profit Measure (TPC-H Q9)              |                1020.41 |                 954.98 |                 973.71 |                 938.96 |                1930.95 |                1942.65 |                 864.26 |                 924.78 |
| Returned Item Reporting Query (TPC-H Q10)           |                 530.04 |                 496.05 |                 538.30 |                 529.53 |                 531.40 |                 531.22 |                 502.17 |                 524.99 |
| Important Stock Identification (TPC-H Q11)          |                 184.60 |                 172.15 |                 182.59 |                 196.26 |                 188.66 |                 176.06 |                 164.26 |                 199.75 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 454.09 |                 462.00 |                 466.65 |                 466.53 |                 472.66 |                 464.60 |                 466.52 |                 470.32 |
| Customer Distribution (TPC-H Q13)                   |                1927.71 |                1925.35 |                1989.48 |                1971.39 |                1944.59 |                1993.40 |                1896.03 |                2064.70 |
| Promotion Effect Query (TPC-H Q14)                  |                 531.42 |                 520.20 |                 531.58 |                 528.31 |                 532.52 |                 530.53 |                 518.37 |                 545.01 |
| Top Supplier Query (TPC-H Q15)                      |                 406.36 |                 391.68 |                 412.75 |                 401.51 |                 395.99 |                 396.58 |                 397.22 |                 401.30 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 316.99 |                 458.85 |                 314.52 |                 310.96 |                 325.16 |                 329.79 |                 489.14 |                 374.22 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1708.80 |                1638.18 |                1688.39 |                1653.77 |                1650.80 |                1656.83 |                1871.11 |                1809.16 |
| Large Volume Customer (TPC-H Q18)                   |                7798.65 |                7870.72 |                7729.64 |                7864.90 |                8288.93 |                8137.82 |                7483.19 |                7565.34 |
| Discounted Revenue (TPC-H Q19)                      |                  88.91 |                  92.13 |                  90.33 |                  83.72 |                  95.30 |                  97.80 |                  85.75 |                  91.81 |
| Potential Part Promotion (TPC-H Q20)                |                 529.46 |                 284.21 |                 475.03 |                 284.28 |                 525.75 |                 338.97 |                 496.98 |                 326.85 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 516.09 |                 519.41 |                 521.57 |                 528.14 |                 524.38 |                 506.27 |                 528.14 |                 541.95 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 140.92 |                 127.18 |                 145.20 |                 133.90 |                 144.79 |                 143.81 |                 141.20 |                 141.80 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        88.25 |      1.08 |           2.41 |                  9.97 |
| postgresql-1-1-2-1 |        88.25 |      1.08 |           2.41 |                  9.97 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        61.54 |      0.93 |           0.01 |                  1.29 |
| postgresql-1-1-2-1 |        61.54 |      0.93 |           0.01 |                  1.29 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      3.86 |          17.15 |                 26.74 |
| postgresql-1-1-2-1 | n/a          |      2.81 |          12.39 |                 21.98 |
| postgresql-1-2-1-1 | 43.46        |      1.30 |           8.64 |                 16.57 |
| postgresql-1-2-2-1 | n/a          |      3.50 |          19.43 |                 28.59 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-2-1-1 | 25.96        |      1.51 |           0.30 |                  0.31 |
| postgresql-1-2-2-1 | n/a          |      0.00 |           0.28 |                  0.28 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |
| postgresql-1-1-2-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 4.00 |                                                0.00 |                                                        0.00 |                                  14.00 |                                              14.00 |
| postgresql-1-1-2-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                  14.00 |                                              14.00 |
| postgresql-1-2-1-1 |                                 4.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |
| postgresql-1-2-2-1 |                                 4.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
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

### Container isolation

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 -xqr 3 -nc 2 \
  -ne "1,1" \
  -nlp 1 -nlt 1 \
  -nbp 1 -nbt 64 \
  -xii -xic -xis \
  -m -ma -mc \
  -tr \
  -lr 64Gi -rr 64Gi \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -mtb container -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_collector_tenants_container.log
```

Each tenant gets its own DBMS container (`-mtb container`) with its own 15Gi volume. `-ne "1,1"` means 1 loader and 1 benchmarker pod per tenant. `-xqr 3` repeats each query 3 times so the single-stream-per-tenant configuration still runs long enough for resource monitoring to capture samples.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_collector_tenants_container_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_collector_tenants_container.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1523s 
* Code: 1793589652
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Each query is repeated 3 times.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685317
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685315
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-2-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685317
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685315
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2, PostgreSQL-2-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* PostgreSQL-2: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-2: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793589652-f45bcf47-pp922: 0
* bexhoma-sut-postgresql-1-1793589652-7cccf94664-2z92d: 0
* bexhoma-sut-postgresql-2-1793589652-6dbccd459c-fz7md: 0
* bexhoma-sut-postgresql-2-1793589652-685dff56d6-8qfpd: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793589652-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    3 |      164.00 |           3.00 |            0.00 |        100.00 |           47.00 |              1 |           0 |               65.85 | False               |
| 1793589652-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    3 |      148.00 |           4.00 |            0.00 |        101.00 |           41.00 |              1 |           0 |               72.97 | False               |
| 1793589652-PostgreSQL-1-2-0 |                2 | container      | False         |             2 |           0 |    3 |      164.00 |           3.00 |            0.00 |        100.00 |           47.00 |              1 |           0 |               65.85 | True                |
| 1793589652-PostgreSQL-2-2-1 |                2 | container      | False         |             2 |           1 |    3 |      148.00 |           4.00 |            0.00 |        101.00 |           41.00 |              1 |           0 |               72.97 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.55 |            19770.00 |           9504.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.58 |            18616.59 |           9504.00 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         70 |            0.49 |            21977.43 |          10182.86 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.49 |            21993.84 |          11137.50 |           0 | postgresql-1-2-2-1-1 |
| postgresql-2-1-1-1-1 | PostgreSQL-2    | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         73 |            0.54 |            20155.28 |           9764.38 |           1 | postgresql-2-1-1-1-1 |
| postgresql-2-1-2-1-1 | PostgreSQL-2    | postgresql-2-1-2 | postgresql-2-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.58 |            18677.36 |           9632.43 |           1 | postgresql-2-1-2-1-1 |
| postgresql-2-2-1-1-1 | PostgreSQL-2    | postgresql-2-2-1 | postgresql-2-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.54 |            20151.14 |           9632.43 |           1 | postgresql-2-2-1-1-1 |
| postgresql-2-2-2-1-1 | PostgreSQL-2    | postgresql-2-2-2 | postgresql-2-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.53 |            20428.08 |          11137.50 |           1 | postgresql-2-2-2-1-1 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.55 |            19770.00 |           9504.00 |           0 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.58 |            18616.59 |           9504.00 |           0 |
| postgresql-1-2-1_0 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         70 |            0.49 |            21977.43 |          10182.86 |           0 |
| postgresql-1-2-2_0 | postgresql-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.49 |            21993.84 |          11137.50 |           0 |
| postgresql-2-1-1_1 | postgresql-2-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         73 |            0.54 |            20155.28 |           9764.38 |           1 |
| postgresql-2-1-2_1 | postgresql-2-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.58 |            18677.36 |           9632.43 |           1 |
| postgresql-2-2-1_1 | postgresql-2-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.54 |            20151.14 |           9632.43 |           1 |
| postgresql-2-2-2_1 | postgresql-2-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.53 |            20428.08 |          11137.50 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-2-1-1-1 |   postgresql-1-2-2-1-1 |   postgresql-2-1-1-1-1 |   postgresql-2-1-2-1-1 |   postgresql-2-2-1-1-1 |   postgresql-2-2-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                2007.84 |                1876.49 |                2612.66 |                1586.57 |                1919.04 |                1873.12 |                2650.72 |                1610.05 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 483.79 |                 453.74 |                1002.96 |                 405.08 |                 442.50 |                 459.69 |                1048.96 |                 474.99 |
| Shipping Priority (TPC-H Q3)                        |                 695.75 |                 511.68 |                 871.45 |                 482.71 |                 492.27 |                 508.37 |                 876.17 |                 504.29 |
| Order Priority Checking Query (TPC-H Q4)            |                 272.56 |                 250.14 |                 213.58 |                 231.95 |                 406.63 |                 253.71 |                 232.75 |                 241.55 |
| Local Supplier Volume (TPC-H Q5)                    |                 550.41 |                 541.77 |                 499.78 |                 524.00 |                 500.93 |                 535.52 |                 552.30 |                 536.01 |
| Forecasting Revenue Change (TPC-H Q6)               |                 304.81 |                 619.98 |                 272.64 |                 275.96 |                 287.24 |                 557.57 |                 296.09 |                 296.48 |
| Volume Shipping Query (TPC-H Q7)                    |                 781.06 |                 753.40 |                 561.94 |                 645.02 |                 892.83 |                 792.42 |                 661.39 |                 677.22 |
| National Market Share (TPC-H Q8)                    |                 304.47 |                 381.53 |                1277.79 |                 319.48 |                 340.26 |                 373.40 |                1352.42 |                 315.96 |
| Product Type Profit Measure (TPC-H Q9)              |                1096.93 |                1087.23 |                1100.55 |                 880.17 |                1424.19 |                1320.25 |                1345.38 |                1202.69 |
| Returned Item Reporting Query (TPC-H Q10)           |                 543.07 |                 555.67 |                 480.05 |                 533.36 |                 513.80 |                 523.12 |                 516.60 |                 520.58 |
| Important Stock Identification (TPC-H Q11)          |                 168.03 |                 174.55 |                 175.17 |                 155.80 |                 162.71 |                 169.37 |                 151.30 |                 173.46 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 473.51 |                 711.61 |                 420.52 |                 447.74 |                 522.55 |                 684.42 |                 461.55 |                 706.50 |
| Customer Distribution (TPC-H Q13)                   |                2419.29 |                1974.60 |                1774.16 |                2144.32 |                2020.53 |                1915.64 |                1848.96 |                1900.63 |
| Promotion Effect Query (TPC-H Q14)                  |                 523.54 |                 537.64 |                 443.93 |                 509.81 |                 600.63 |                 535.52 |                 491.75 |                 513.99 |
| Top Supplier Query (TPC-H Q15)                      |                 394.07 |                 407.07 |                 364.90 |                 399.58 |                 392.44 |                 407.06 |                 390.57 |                 396.44 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 435.71 |                 435.68 |                 350.23 |                 375.24 |                 352.72 |                 383.65 |                 381.57 |                 407.89 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                2100.31 |                1929.58 |                1462.54 |                1620.38 |                1922.89 |                1737.33 |                1641.60 |                1584.56 |
| Large Volume Customer (TPC-H Q18)                   |                9275.18 |                9170.14 |                7655.75 |                7964.89 |                8929.59 |                9118.33 |                7697.06 |                7567.51 |
| Discounted Revenue (TPC-H Q19)                      |                  97.59 |                  80.58 |                  69.43 |                  84.85 |                  78.68 |                  78.59 |                  84.34 |                  72.48 |
| Potential Part Promotion (TPC-H Q20)                |                 326.25 |                 279.82 |                 242.89 |                 308.73 |                 337.73 |                 314.68 |                 320.80 |                 341.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 618.77 |                 718.80 |                 458.32 |                 482.16 |                 545.14 |                 586.35 |                 507.18 |                 491.24 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 127.49 |                 213.90 |                 132.59 |                 124.71 |                 126.15 |                 300.56 |                 132.50 |                 130.63 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        56.04 |      0.81 |           4.61 |                  8.84 |
| postgresql-1-1-2-1 |        56.04 |      0.81 |           4.61 |                  8.84 |
| postgresql-2-1-1-1 |        91.35 |      1.69 |           5.18 |                  9.91 |
| postgresql-2-1-2-1 |        91.35 |      1.69 |           5.18 |                  9.91 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        32.24 |      0.46 |           0.01 |                  0.84 |
| postgresql-1-1-2-1 |        32.24 |      0.46 |           0.01 |                  0.84 |
| postgresql-2-1-1-1 |        32.89 |      0.42 |           0.00 |                  1.56 |
| postgresql-2-1-2-1 |        32.89 |      0.42 |           0.00 |                  1.56 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       227.73 |      3.54 |           6.16 |                 11.39 |
| postgresql-1-1-2-1 |       236.09 |      4.26 |           5.84 |                 11.50 |
| postgresql-1-2-1-1 |       179.77 |      3.05 |           8.21 |                 12.54 |
| postgresql-1-2-2-1 |       208.19 |      3.95 |           9.51 |                 13.84 |
| postgresql-2-1-1-1 |       134.96 |      3.65 |           5.00 |                  9.80 |
| postgresql-2-1-2-1 |       245.63 |      3.53 |           8.38 |                 13.19 |
| postgresql-2-2-1-1 |       146.20 |      2.84 |           5.83 |                 10.17 |
| postgresql-2-2-2-1 |       126.33 |      3.54 |           4.86 |                  9.19 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        13.60 |      0.42 |           0.28 |                  0.29 |
| postgresql-1-1-2-1 |        15.04 |      0.03 |           0.33 |                  0.34 |
| postgresql-1-2-1-1 |        13.20 |      0.02 |           0.30 |                  0.30 |
| postgresql-1-2-2-1 |        12.87 |      0.02 |           0.26 |                  0.26 |
| postgresql-2-1-1-1 |        13.52 |      0.82 |           0.30 |                  0.30 |
| postgresql-2-1-2-1 |        13.21 |      0.02 |           0.28 |                  0.28 |
| postgresql-2-2-1-1 |        14.22 |      0.65 |           0.36 |                  0.36 |
| postgresql-2-2-2-1 |        13.70 |      0.03 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-2-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-2-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-2-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
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

## YCSB

### Test 1: Fresh PVC, nbf=2

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 -xwl a \
  -xtb 16384 -xnbf 2 -xnlf 4 \
  -nc 2 -ne 1 \
  -nlp 8 -nlt 64 \
  -nbp 1,8 -nbt 64 \
  -xop 1 \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_collector_1.log
```

This
* loads 3M YCSB rows (`-sf 3`) using 8 loader pods × 64 threads each (`-nlp 8 -nlt 64`) into a fresh 15Gi volume
* runs YCSB workload A (50% reads, 50% updates), 1M operations (`-xop 1`)
* two benchmarking configurations: 1 pod × 64 threads, then 8 pods × 8 threads each (`-nbp 1,8 -nbt 64`)
* target is 2×(`-xnbf`) × 16384 (`-xtb`) ops per pod

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_collector_1_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_collector_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 874s 
* Code: 1793591274
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:686922
  * datadisk:7091
  * volume_size:49G
  * volume_used:7.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793591274
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:687775
  * datadisk:7500
  * volume_size:49G
  * volume_used:7.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793591274
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685319
  * datadisk:7910
  * volume_size:49G
  * volume_used:7.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793591274
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685319
  * datadisk:8112
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793591274

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: fillfactor=100, autovacuum_scale=0.2
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793591274-797b4f57d5-xsqkm: 0
* bexhoma-sut-postgresql-1-1793591274-6c48f98d8b-hxk8t: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8139.26 |                46073.00 |            375000.00 |                               812.00 | 3.00 |              234.41 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8141.91 |                46058.00 |            375000.00 |                               749.00 | 3.00 |              234.49 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8146.68 |                46031.00 |            375000.00 |                               930.00 | 3.00 |              234.62 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8141.38 |                46061.00 |            375000.00 |                               890.00 | 3.00 |              234.47 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8145.98 |                46035.00 |            375000.00 |                               902.00 | 3.00 |              234.60 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8146.33 |                46033.00 |            375000.00 |                               921.00 | 3.00 |              234.61 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8142.79 |                46053.00 |            375000.00 |                               917.00 | 3.00 |              234.51 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8142.79 |                46053.00 |            375000.00 |                               834.00 | 3.00 |              234.51 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              234.41 |                        65147.12 |                46073.00 |           3000000.00 |                               869.38 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32196.79 |                31059.00 |             500447 |                             633.00 |               499553 |                              8055.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4067.16 |                30734.00 |              62441 |                             608.00 |                62559 |                              4987.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4067.42 |                30732.00 |              62621 |                             625.00 |                62379 |                              5503.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4067.95 |                30728.00 |              62649 |                             639.00 |                62351 |                              5155.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4058.31 |                30801.00 |              62449 |                             602.00 |                62551 |                              5327.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4068.22 |                30726.00 |              62525 |                             647.00 |                62475 |                              5311.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4068.22 |                30726.00 |              62231 |                             633.00 |                62769 |                              5655.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4063.19 |                30764.00 |              62408 |                             644.00 |                62592 |                              4827.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4067.82 |                30729.00 |              62250 |                             650.00 |                62750 |                              5643.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        24402.74 |                40979.00 |             499756 |                            1649.00 |               500244 |                             53311.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4066.50 |                30739.00 |              62671 |                             889.00 |                62329 |                             11599.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4068.22 |                30726.00 |              62386 |                             817.00 |                62614 |                              9647.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4066.63 |                30738.00 |              62537 |                             852.00 |                62463 |                             10887.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4065.70 |                30745.00 |              62408 |                             849.00 |                62592 |                              9775.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4066.50 |                30739.00 |              62579 |                             823.00 |                62421 |                             10119.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4068.22 |                30726.00 |              62601 |                             860.00 |                62399 |                             10391.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4067.42 |                30732.00 |              62670 |                             838.00 |                62330 |                              9335.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4058.31 |                30801.00 |              62523 |                             892.00 |                62477 |                             11919.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32196.79 |                31059.00 |             500447 |                             633.00 |               499553 |                              8055.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32528.28 |                30801.00 |             499574 |                             650.00 |               500426 |                              5655.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        64 |    32768 |               1 |           1 |            0 |                        24402.74 |                40979.00 |             499756 |                            1649.00 |               500244 |                             53311.00 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        64 |    32768 |               1 |           8 |            0 |                        32527.48 |                30801.00 |             500375 |                             892.00 |               499625 |                             11919.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       157.51 |      3.50 |           3.86 |                  5.19 |
| postgresql-1-1-2-1 |       157.51 |      3.50 |           3.86 |                  5.19 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       123.22 |      4.62 |           0.53 |                  0.54 |
| postgresql-1-1-2-1 |       123.22 |      4.62 |           0.53 |                  0.54 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      1.11 |           4.67 |                  8.27 |
| postgresql-1-1-2-1 | n/a          |      0.87 |           4.85 |                  8.64 |
| postgresql-1-2-1-1 | 116.30       |      2.99 |           3.50 |                  7.11 |
| postgresql-1-2-2-1 | n/a          |      1.88 |           4.72 |                  8.81 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.10 |                  0.10 |
| postgresql-1-2-1-1 | 66.64        |      2.24 |           0.54 |                  0.54 |
| postgresql-1-2-2-1 | n/a          |      0.00 |           0.09 |                  0.10 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                64.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                64.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                48.00 |                                                0.00 |                                                        0.00 |                                  17.00 |                                              17.00 |
| postgresql-1-1-2-1 |                                49.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                              16.00 |
| postgresql-1-2-1-1 |                                12.00 |                                                0.00 |                                                        0.00 |                                  53.00 |                                              53.00 |
| postgresql-1-2-2-1 |                                31.00 |                                                0.00 |                                                        0.00 |                                  34.00 |                                              34.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Test 2: Fresh PVC, nbf=3

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 -xwl a \
  -xtb 16384 -xnbf 3 -xnlf 4 \
  -nc 2 -ne 1 \
  -nlp 8 -nlt 64 \
  -nbp 1,8 -nbt 64 \
  -xop 1 \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_collector_2.log
```

Same as test 1 but with `xnbf=3` (target factor 3 × 16384). The PVC is recreated (`-rsr`).

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_collector_2_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_collector_2.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 958s 
* Code: 1793592196
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [3].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685320
  * datadisk:7091
  * volume_size:49G
  * volume_used:7.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793592196
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685321
  * datadisk:7626
  * volume_size:49G
  * volume_used:7.5G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793592196
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685312
  * datadisk:8170
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793592196
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685312
  * datadisk:8363
  * volume_size:49G
  * volume_used:8.2G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793592196

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: fillfactor=100, autovacuum_scale=0.2
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793592196-74d9c97d5f-q5hp4: 0
* bexhoma-sut-postgresql-1-1793592196-75c9bfcfc5-pqd9b: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8142.79 |                46053.00 |            375000.00 |                              1027.00 | 3.00 |              234.51 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8148.45 |                46021.00 |            375000.00 |                              1059.00 | 3.00 |              234.68 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8143.32 |                46050.00 |            375000.00 |                               996.00 | 3.00 |              234.53 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8141.38 |                46061.00 |            375000.00 |                              1001.00 | 3.00 |              234.47 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8146.33 |                46033.00 |            375000.00 |                              1080.00 | 3.00 |              234.61 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8147.21 |                46028.00 |            375000.00 |                              1025.00 | 3.00 |              234.64 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8144.03 |                46046.00 |            375000.00 |                              1051.00 | 3.00 |              234.55 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8142.97 |                46052.00 |            375000.00 |                              1035.00 | 3.00 |              234.52 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              234.47 |                        65156.49 |                46061.00 |           3000000.00 |                              1034.25 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        39045.72 |                25611.00 |             500837 |                             686.00 |               499163 |                             45503.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         5110.59 |                24459.00 |              62560 |                             663.00 |                62440 |                             38111.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         4778.10 |                26161.00 |              62223 |                             710.00 |                62777 |                             39135.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         4876.91 |                25631.00 |              62371 |                             715.00 |                62629 |                             39775.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         5060.73 |                24700.00 |              62320 |                             683.00 |                62680 |                             40095.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         5094.97 |                24534.00 |              62601 |                             684.00 |                62399 |                             40127.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         4738.80 |                26378.00 |              62487 |                             685.00 |                62513 |                             40159.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         5046.83 |                24768.00 |              62700 |                             674.00 |                62300 |                             37439.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         4968.40 |                25159.00 |              62166 |                             687.00 |                62834 |                             39583.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        27126.00 |                36865.00 |             500092 |                            1544.00 |               499908 |                             49599.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         4317.19 |                28954.00 |              62669 |                             910.00 |                62331 |                             42527.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         4653.59 |                26861.00 |              62785 |                             876.00 |                62215 |                             40575.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         4616.81 |                27075.00 |              62267 |                             852.00 |                62733 |                             43679.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         4303.96 |                29043.00 |              62721 |                             965.00 |                62279 |                             44095.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         4280.38 |                29203.00 |              62286 |                             975.00 |                62714 |                             42463.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         4507.59 |                27731.00 |              62195 |                             862.00 |                62805 |                             42655.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         4699.07 |                26601.00 |              62518 |                             862.00 |                62482 |                             42143.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         4404.20 |                28382.00 |              62628 |                             900.00 |                62372 |                             46271.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    49152 |               1 |           1 |            0 |                        39045.72 |                25611.00 |             500837 |                             686.00 |               499163 |                             45503.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    49152 |               1 |           8 |            0 |                        39675.34 |                26378.00 |             499428 |                             715.00 |               500572 |                             40159.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        64 |    49152 |               1 |           1 |            0 |                        27126.00 |                36865.00 |             500092 |                            1544.00 |               499908 |                             49599.00 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        64 |    49152 |               1 |           8 |            0 |                        35782.79 |                29203.00 |             500069 |                             975.00 |               499931 |                             46271.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       170.66 |      3.77 |           3.86 |                  4.93 |
| postgresql-1-1-2-1 |       170.66 |      3.77 |           3.86 |                  4.93 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       121.04 |      1.45 |           0.53 |                  0.53 |
| postgresql-1-1-2-1 |       121.04 |      1.45 |           0.53 |                  0.53 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      1.82 |           4.83 |                  8.55 |
| postgresql-1-1-2-1 | n/a          |      2.27 |           5.05 |                  8.97 |
| postgresql-1-2-1-1 | 109.33       |      3.34 |           3.65 |                  7.28 |
| postgresql-1-2-2-1 | n/a          |      0.13 |           3.50 |                  7.18 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.09 |                  0.10 |
| postgresql-1-2-1-1 | 38.01        |      0.00 |           0.31 |                  0.32 |
| postgresql-1-2-2-1 | n/a          |      0.00 |           0.10 |                  0.11 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                63.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |
| postgresql-1-1-2-1 |                                63.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-1-2-1 |                                 3.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-2-1-1 |                                 8.00 |                                                0.00 |                                                        0.00 |                                  57.00 |                                              57.00 |
| postgresql-1-2-2-1 |                                 7.00 |                                                0.00 |                                                        0.00 |                                  58.00 |                                              58.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Test 3: Reuse PVC, nbf=3

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 -xwl a \
  -xtb 16384 -xnbf 3 -xnlf 4 \
  -nc 2 -ne 1 \
  -nlp 8 -nlt 64 \
  -nbp 1,8 -nbt 64 \
  -xop 8 \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_collector_3.log
```

Same parameters as test 2 but the persistent volume is reused (no `-rsr -rst`), and `-xop 8` raises the operation count so execution still runs long enough for resource monitoring to capture samples now that the loading phase is skipped.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_collector_3_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_collector_3.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1519s 
* Code: 1793593225
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 8000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [3].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:694462
  * datadisk:7092
  * volume_size:1.8T
  * volume_used:679G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793593225
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:694260
  * datadisk:8947
  * volume_size:1.8T
  * volume_used:678G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793593225
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:692408
  * datadisk:7093
  * volume_size:1.8T
  * volume_used:677G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793593225
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:694275
  * datadisk:8951
  * volume_size:1.8T
  * volume_used:679G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793593225

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793593225-5785675f75-m9mcm: 0
* bexhoma-sut-postgresql-1-1793593225-5ff76fcccb-2xcvf: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8139.96 |                46069.00 |            375000.00 |                               861.00 | 3.00 |              234.43 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8141.38 |                46061.00 |            375000.00 |                               847.00 | 3.00 |              234.47 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8145.62 |                46037.00 |            375000.00 |                               734.00 | 3.00 |              234.59 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8140.32 |                46067.00 |            375000.00 |                               834.00 | 3.00 |              234.44 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8144.91 |                46041.00 |            375000.00 |                               809.00 | 3.00 |              234.57 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8144.21 |                46045.00 |            375000.00 |                               886.00 | 3.00 |              234.55 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8139.61 |                46071.00 |            375000.00 |                               825.00 | 3.00 |              234.42 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8142.79 |                46053.00 |            375000.00 |                               749.00 | 3.00 |              234.51 |
| postgresql-1-2-0-1-1 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8142.79 |                46053.00 |            375000.00 |                               924.00 | 3.00 |              234.51 |
| postgresql-1-2-0-1-2 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8145.09 |                46040.00 |            375000.00 |                               839.00 | 3.00 |              234.58 |
| postgresql-1-2-0-1-3 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8145.62 |                46037.00 |            375000.00 |                               934.00 | 3.00 |              234.59 |
| postgresql-1-2-0-1-4 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8140.67 |                46065.00 |            375000.00 |                               898.00 | 3.00 |              234.45 |
| postgresql-1-2-0-1-5 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8143.85 |                46047.00 |            375000.00 |                               939.00 | 3.00 |              234.54 |
| postgresql-1-2-0-1-6 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8143.15 |                46051.00 |            375000.00 |                               876.00 | 3.00 |              234.52 |
| postgresql-1-2-0-1-7 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8139.96 |                46069.00 |            375000.00 |                               949.00 | 3.00 |              234.43 |
| postgresql-1-2-0-1-8 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8140.32 |                46067.00 |            375000.00 |                               955.00 | 3.00 |              234.44 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              234.42 |                        65138.80 |                46071.00 |           3000000.00 |                               818.12 |
| PostgreSQL-1-2 |             2.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              234.43 |                        65141.46 |                46069.00 |           3000000.00 |                               914.25 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        49049.96 |               163099.00 |            3997201 |                             547.00 |              4002799 |                              1457.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6133.95 |               163027.00 |             500076 |                             631.00 |               499924 |                              1517.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6133.80 |               163031.00 |             499639 |                             561.00 |               500361 |                              1445.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6134.18 |               163021.00 |             499384 |                             626.00 |               500616 |                              1516.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6134.29 |               163018.00 |             499513 |                             653.00 |               500487 |                              1521.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6133.73 |               163033.00 |             499724 |                             637.00 |               500276 |                              1531.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6134.33 |               163017.00 |             500264 |                             638.00 |               499736 |                              1552.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6132.98 |               163053.00 |             499224 |                             607.00 |               500776 |                              1486.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6133.28 |               163045.00 |             499270 |                             591.00 |               500730 |                              1479.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        49035.83 |               163146.00 |            4001591 |                             554.00 |              3998409 |                              1570.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6133.13 |               163049.00 |             499336 |                             624.00 |               500664 |                              1528.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6133.69 |               163034.00 |             500226 |                             602.00 |               499774 |                              1524.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6133.31 |               163044.00 |             499342 |                             639.00 |               500658 |                              1547.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6133.31 |               163044.00 |             499848 |                             540.00 |               500152 |                              1472.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6133.88 |               163029.00 |             500060 |                             575.00 |               499940 |                              1525.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6134.52 |               163012.00 |             499338 |                             659.00 |               500662 |                              1558.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6133.61 |               163036.00 |             500048 |                             535.00 |               499952 |                              1430.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6133.50 |               163039.00 |             500724 |                             543.00 |               499276 |                              1483.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    49152 |               1 |           1 |            0 |                        49049.96 |               163099.00 |            3997201 |                             547.00 |              4002799 |                              1457.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    49152 |               1 |           8 |            0 |                        49070.54 |               163053.00 |            3997094 |                             653.00 |              4002906 |                              1552.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        64 |    49152 |               1 |           1 |            0 |                        49035.83 |               163146.00 |            4001591 |                             554.00 |              3998409 |                              1570.00 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        64 |    49152 |               1 |           8 |            0 |                        49068.96 |               163049.00 |            3998922 |                             659.00 |              4001078 |                              1558.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       158.40 |      3.39 |           3.87 |                  5.49 |
| postgresql-1-1-2-1 |       158.40 |      3.39 |           3.87 |                  5.49 |
| postgresql-1-2-1-1 |       168.69 |      3.41 |           3.86 |                  5.00 |
| postgresql-1-2-2-1 |       168.69 |      3.41 |           3.86 |                  5.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       134.00 |      3.73 |           0.29 |                  0.29 |
| postgresql-1-1-2-1 |       134.00 |      3.73 |           0.29 |                  0.29 |
| postgresql-1-2-1-1 |       187.12 |      6.13 |           0.29 |                  0.29 |
| postgresql-1-2-2-1 |       187.12 |      6.13 |           0.29 |                  0.29 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       506.33 |      3.24 |           5.20 |                  9.23 |
| postgresql-1-1-2-1 |       490.62 |      3.38 |           5.21 |                  9.27 |
| postgresql-1-2-1-1 |       529.83 |      3.50 |           5.20 |                  9.24 |
| postgresql-1-2-2-1 |       426.51 |      3.42 |           5.22 |                  9.28 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       536.01 |      4.06 |           0.57 |                  0.57 |
| postgresql-1-1-2-1 |       672.30 |      5.58 |           0.10 |                  0.11 |
| postgresql-1-2-1-1 |       543.21 |      3.95 |           0.57 |                  0.57 |
| postgresql-1-2-2-1 |       649.94 |      5.34 |           0.10 |                  0.11 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                64.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                64.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-2-1-1 |                                60.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-2-2-1 |                                60.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                62.00 |                                                0.00 |                                                        0.00 |                                  22.00 |                                              22.00 |
| postgresql-1-1-2-1 |                                57.00 |                                                0.00 |                                                        0.00 |                                  12.00 |                                              12.00 |
| postgresql-1-2-1-1 |                                55.00 |                                                0.00 |                                                        0.00 |                                  18.00 |                                              18.00 |
| postgresql-1-2-2-1 |                                59.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                              16.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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

## HammerDB

### Test 1: Fresh PVC, nbt=16

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 -xsd 5 -nc 2 \
  -nlt 16 -nbp 1,2 -nbt 16 \
  -xlat \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_collector_1.log
```

This
* loads TPC-C data for 16 warehouses (`-sf 16`) using 16 loading threads (`-nlt 16`) into a fresh 15Gi volume
* runs HammerDB for 5 minutes (`-xsd 5`) per stream with two benchmarking configurations: 1 then 2 pods, 16 virtual users each (`-nbp 1,2 -nbt 16`)
* logs latencies (`-xlat`)
* monitors SUT metrics (`-m`), application metrics (`-ma`), and cluster metrics (`-mc`)

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_collector_1_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_collector_1.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2498s 
* Code: 1793594796
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685325
  * datadisk:3304
  * volume_size:49G
  * volume_used:3.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685327
  * datadisk:12018
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685329
  * datadisk:14874
  * volume_size:49G
  * volume_used:15G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685330
  * datadisk:15486
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793594796-6f6688df9f-7s8lj: 0
* bexhoma-sut-postgresql-1-1793594796-547c8964d9-nkjjr: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       44.00 |           4.00 |            0.00 |         30.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |             1309.09 | False               |
| PostgreSQL-1-2 |                2 |   16 |       44.00 |           4.00 |            0.00 |         30.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |             1309.09 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 163778 | 377587 |         0.00 |          5 |        0 |       2.96 |       4.01 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       1 |  49241 | 113739 |         0.00 |          5 |        0 |       2.84 |       3.56 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       2 |  49194 | 113605 |         0.00 |          5 |        0 |       2.88 |       3.56 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |       16 |        1 |               1 |       1 |  46610 | 107507 |         0.00 |          5 |        0 |       3.32 |       4.61 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        8 |        2 |               1 |       1 |  43959 | 101172 |         0.00 |          5 |        0 |       3.00 |       3.98 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        8 |        2 |               1 |       2 |  43931 | 101187 |         0.00 |          5 |        0 |       3.01 |       3.84 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       16 |        1 |               1 |           1 |       2.96 |       4.01 |         0.00 | 163778.00 | 377587.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |       16 |        2 |               1 |           2 |       2.88 |       3.56 |         0.00 |  49217.50 | 113672.00 |          5 |        0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |       16 |        1 |               1 |           1 |       3.32 |       4.61 |         0.00 |  46610.00 | 107507.00 |          5 |        0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |       16 |        2 |               1 |           2 |       3.01 |       3.98 |         0.00 |  43945.00 | 101179.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        30.71 |      0.89 |           1.67 |                  2.39 |
| postgresql-1-1-2-1 |        30.71 |      0.89 |           1.67 |                  2.39 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.14 |                  0.15 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.14 |                  0.15 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1794.64 |      5.37 |           4.26 |                  7.89 |
| postgresql-1-1-2-1 |      5406.01 |     13.15 |           5.29 |                  9.70 |
| postgresql-1-2-1-1 |      5286.18 |     13.12 |           2.57 |                  4.52 |
| postgresql-1-2-2-1 |      5502.89 |     13.83 |           3.37 |                  6.06 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       733.87 |      1.84 |           0.28 |                  0.28 |
| postgresql-1-1-2-1 |       243.39 |      0.67 |           0.11 |                  0.12 |
| postgresql-1-2-1-1 |       248.82 |      0.68 |           0.21 |                  0.21 |
| postgresql-1-2-2-1 |       238.47 |      0.62 |           0.12 |                  0.12 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                12.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                 9.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                10.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>

### Test 2: Fresh PVC, nbt=32

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 -xsd 5 -nc 2 \
  -nlt 16 -nbp 1,2 -nbt 32 \
  -xlat \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -rsr -rss 50Gi -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_collector_2.log
```

Same as test 1 but with `nbt=32` virtual users per benchmarking pod. The PVC is recreated (`-rsr`).

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_collector_2_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_collector_2.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2606s 
* Code: 1793597333
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [32] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685532
  * datadisk:3304
  * volume_size:49G
  * volume_used:3.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793597333
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685336
  * datadisk:12294
  * volume_size:49G
  * volume_used:13G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793597333
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685338
  * datadisk:17437
  * volume_size:49G
  * volume_used:18G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793597333
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685340
  * datadisk:18586
  * volume_size:49G
  * volume_used:19G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793597333

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793597333-685f8df4b5-p5sfm: 0
* bexhoma-sut-postgresql-1-1793597333-7c685844b7-slm6n: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       54.00 |           4.00 |            0.00 |         40.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |             1066.67 | False               |
| PostgreSQL-1-2 |                2 |   16 |       54.00 |           4.00 |            0.00 |         40.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |             1066.67 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       32 |        1 |               1 |       1 | 151852 | 348934 |         0.00 |          5 |        0 |       5.00 |       7.09 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |  91682 | 210893 |         0.00 |          5 |        0 |       2.98 |       3.70 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |       16 |        2 |               1 |       2 |  91650 | 210815 |         0.00 |          5 |        0 |       2.97 |       3.83 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |       32 |        1 |               1 |       1 |  85125 | 196144 |         0.00 |          5 |        0 |       3.29 |       4.50 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |  59404 | 136887 |         0.00 |          5 |        0 |       3.04 |       3.99 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |       16 |        2 |               1 |       2 |  59337 | 136770 |         0.00 |          5 |        0 |       2.97 |       3.81 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       32 |        1 |               1 |           1 |       5.00 |       7.09 |         0.00 | 151852.00 | 348934.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |       32 |        2 |               1 |           2 |       2.98 |       3.83 |         0.00 |  91666.00 | 210854.00 |          5 |        0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |       32 |        1 |               1 |           1 |       3.29 |       4.50 |         0.00 |  85125.00 | 196144.00 |          5 |        0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |       32 |        2 |               1 |           2 |       3.04 |       3.99 |         0.00 |  59370.50 | 136828.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        32.02 |      0.95 |           1.73 |                  2.45 |
| postgresql-1-1-2-1 |        32.02 |      0.95 |           1.73 |                  2.45 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       159.00 |      0.00 |           0.14 |                  0.14 |
| postgresql-1-1-2-1 |       159.00 |      0.00 |           0.14 |                  0.14 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      8197.05 |     21.81 |           4.88 |                  8.72 |
| postgresql-1-1-2-1 |     10721.98 |     26.58 |           7.05 |                 12.22 |
| postgresql-1-2-1-1 |     10528.49 |     26.53 |           4.32 |                  7.04 |
| postgresql-1-2-2-1 |     11474.23 |     28.95 |           7.44 |                 13.10 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       759.99 |      2.19 |           0.43 |                  0.43 |
| postgresql-1-1-2-1 |       450.04 |      1.12 |           0.23 |                  0.23 |
| postgresql-1-2-1-1 |       423.13 |      1.10 |           0.42 |                  0.42 |
| postgresql-1-2-2-1 |       341.26 |      1.02 |           0.20 |                  0.21 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                  10.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                  10.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                12.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                 9.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                15.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>

### Test 3: Reuse PVC, nbt=32

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 -xsd 5 -nc 2 \
  -nlt 16 -nbp 1,2 -nbt 32 \
  -xlat \
  -m -ma -mc \
  -ms $BEXHOMA_MS -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_collector_3.log
```

Same parameters as test 2 but the persistent volume is reused (no `-rsr -rst`). Since the database persists, loading is fast (pre-loaded data is already present) and the experiment focuses on benchmarking with the existing dataset.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_collector_3_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_collector_3.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2680s 
* Code: 1793600001
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [32] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:688704
  * datadisk:3304
  * volume_size:1.8T
  * volume_used:673G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793600001
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699769
  * datadisk:14367
  * volume_size:1.8T
  * volume_used:684G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793600001
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:688708
  * datadisk:3304
  * volume_size:1.8T
  * volume_used:673G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793600001
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:700050
  * datadisk:14656
  * volume_size:1.8T
  * volume_used:684G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793600001

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793600001-7496d5bd94-dmh7l: 0
* bexhoma-sut-postgresql-1-1793600001-8877bd9bf-bgx5p: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       40.00 |           3.00 |            0.00 |         30.00 |            7.00 |              1 |          16 |             | None           |             0 | False         |             1440.00 | False               |
| PostgreSQL-1-2 |                2 |   16 |       39.00 |           3.00 |            0.00 |         29.00 |            7.00 |              1 |          16 |             | None           |             0 | False         |             1476.92 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       32 |        1 |               1 |       1 | 178647 | 411755 |         0.00 |          5 |        0 |       5.02 |       8.36 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |  90237 | 207617 |         0.00 |          5 |        0 |       1.95 |       2.34 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |       16 |        2 |               1 |       2 |  90195 | 207467 |         0.00 |          5 |        0 |       1.93 |       2.30 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |       32 |        1 |               1 |       1 | 189119 | 435667 |         0.00 |          5 |        0 |       9.32 |      15.97 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |  32897 |  75846 |         0.00 |          5 |        0 |       1.82 |       2.22 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |       16 |        2 |               1 |       2 |  32839 |  75840 |         0.00 |          5 |        0 |       1.80 |       2.19 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       32 |        1 |               1 |           1 |       5.02 |       8.36 |         0.00 | 178647.00 | 411755.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |       32 |        2 |               1 |           2 |       1.95 |       2.34 |         0.00 |  90216.00 | 207542.00 |          5 |        0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |       32 |        1 |               1 |           1 |       9.32 |      15.97 |         0.00 | 189119.00 | 435667.00 |          5 |        0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |       32 |        2 |               1 |           2 |       1.82 |       2.22 |         0.00 |  32868.00 |  75843.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        30.46 |      0.56 |           1.70 |                  2.96 |
| postgresql-1-1-2-1 |        30.46 |      0.56 |           1.70 |                  2.96 |
| postgresql-1-2-1-1 |        28.68 |      0.62 |           1.67 |                  2.39 |
| postgresql-1-2-2-1 |        28.68 |      0.62 |           1.67 |                  2.39 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-2-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      8929.39 |     24.54 |           5.48 |                  9.88 |
| postgresql-1-1-2-1 |     12139.85 |     29.23 |           7.69 |                 13.39 |
| postgresql-1-2-1-1 |      8109.45 |     21.47 |           5.60 |                 10.12 |
| postgresql-1-2-2-1 |     13017.44 |     31.32 |           7.30 |                 12.62 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       908.39 |      2.68 |           0.50 |                  0.50 |
| postgresql-1-1-2-1 |       399.86 |      1.05 |           0.21 |                  0.21 |
| postgresql-1-2-1-1 |       856.12 |      2.58 |           0.49 |                  0.49 |
| postgresql-1-2-2-1 |       136.01 |      0.55 |           0.17 |                  0.18 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* CPU Utilization [CPUs] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Index Scan Count [scans] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Autoanalyze Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Autovacuum Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                16.00 |                                                0.00 |                                                        0.00 |                                  13.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                16.00 |                                                0.00 |                                                        0.00 |                                  13.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               1.00 |
| postgresql-1-2-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                10.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                12.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                12.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                 7.00 |                                                0.00 |                                                        0.00 |                                  32.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>
