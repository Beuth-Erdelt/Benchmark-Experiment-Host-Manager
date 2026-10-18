# Example: Application Metrics

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In the following we demonstrate how to collect application metrics, that is, metrics of a DBMS.


## Perform Benchmark

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

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

## PostgreSQL

### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_appmetrics.log
```

This
* activates monitoring (`-m`) cluster-wide (`-mc`)
* starts a clean instance of PostgreSQL (`-dbms`)
  * with a sidecar container for monitoring (`-ma`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results


<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1475s 
* Code: 1792317325
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:824784
  * volume_size:1.8T
  * volume_used:806G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792317325
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:839543
  * volume_size:1.8T
  * volume_used:820G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792317325
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792317325-7869fcf44b-ghw9f: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |      163.00 |           4.00 |            0.00 |        148.00 |           11.00 |              1 |           1 |             |                |             0 | False         |              353.37 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |          114 |                       14285.07 |                    14083.17 |         0.00 |                                                      28400.00 |                                              11193.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 300.00 |           19 |                        4390.55 |                     4345.74 |         0.00 |                                                      35536.00 |                                              18204.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 300.00 |           21 |                        4390.52 |                     4345.35 |         0.00 |                                                      35489.00 |                                              18214.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 300.00 |          114 |                       14285.07 |                    14083.17 |         0.00 |                                                      28400.00 |                                              11193.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 300.00 |           40 |                        8781.07 |                     8691.09 |         0.00 |                                                      35536.00 |                                              18209.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       153.99 |      1.98 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       153.99 |      1.98 |           2.05 |                  3.69 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1662.06 |     15.49 |           0.26 |                  0.26 |
| postgresql-1-1-2-1 |      1662.06 |     15.49 |           0.26 |                  0.26 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      4910.00 |     19.40 |           8.36 |                 13.94 |
| postgresql-1-1-2-1 |      3633.01 |     14.70 |          10.98 |                 16.00 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      5208.47 |     19.29 |           1.36 |                  1.43 |
| postgresql-1-1-2-1 |      5208.47 |     26.74 |           1.36 |                  1.43 |

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
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                   17 |                                                   0 |                                                           0 |                                     11 |                                                 11 |
| postgresql-1-1-2-1 |                                   17 |                                                   0 |                                                           0 |                                     11 |                                                 11 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                12.00 |                                               78.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-1-2-1 |                                 7.00 |                                               41.00 |                                                        0.00 |                                 160.00 |                                             160.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_postgresql_appmetrics_summary.md" target="_blank" rel="noopener">docs_hammerdb_postgresql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1722s 
* Code: 1792323545
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:824366
  * volume_size:1.8T
  * volume_used:806G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792323545
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:839114
  * volume_size:1.8T
  * volume_used:820G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792323545

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792323545-74774b4bf7-bw298: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       63.00 |           4.00 |            0.00 |         49.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |              914.29 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 246600 | 567759 |         0.00 |          5 |        0 |       2.07 |       2.58 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       1 |  61219 | 140745 |         0.00 |          5 |        0 |       1.59 |       1.94 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       2 |  61184 | 140813 |         0.00 |          5 |        0 |       1.60 |       1.96 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       16 |        1 |               1 |           1 |       2.07 |       2.58 |         0.00 | 246600.00 | 567759.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |       16 |        2 |               1 |           2 |       1.60 |       1.96 |         0.00 |  61201.50 | 140779.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        40.23 |      0.97 |           1.73 |                  2.40 |
| postgresql-1-1-2-1 |        40.23 |      0.97 |           1.73 |                  2.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       184.76 |      0.00 |           0.15 |                  0.15 |
| postgresql-1-1-2-1 |       184.76 |      0.00 |           0.15 |                  0.15 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2568.39 |      8.22 |           5.57 |                 10.39 |
| postgresql-1-1-2-1 |      5898.68 |     14.42 |           6.68 |                 12.41 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       598.93 |      1.62 |           0.35 |                  0.35 |
| postgresql-1-1-2-1 |       598.93 |      1.29 |           0.35 |                  0.35 |

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
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
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
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                   18 |                                                   0 |                                                           0 |                                     15 |                                                  1 |
| postgresql-1-1-2-1 |                                   18 |                                                   0 |                                                           0 |                                     15 |                                                  1 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 9.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                 7.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>


### TPC-H

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 2 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_appmetrics_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 727s 
* Code: 1792320882
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:836001
  * volume_size:1.8T
  * volume_used:817G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792320882

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792320882-5958f65bc6-8smms: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      110.00 |           4.00 |            1.00 |         56.00 |           47.00 |              2 |           0 |             |                |             0 | False         |               98.18 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         34 |            0.68 |            16965.60 |           6988.24 |           0 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         34 |            0.68 |            16965.60 |           6988.24 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1738.52 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 643.15 |
| Shipping Priority (TPC-H Q3)                        |                 649.72 |
| Order Priority Checking Query (TPC-H Q4)            |                 293.78 |
| Local Supplier Volume (TPC-H Q5)                    |                 676.55 |
| Forecasting Revenue Change (TPC-H Q6)               |                 352.52 |
| Volume Shipping Query (TPC-H Q7)                    |                 877.84 |
| National Market Share (TPC-H Q8)                    |                 460.22 |
| Product Type Profit Measure (TPC-H Q9)              |                1114.87 |
| Returned Item Reporting Query (TPC-H Q10)           |                 595.89 |
| Important Stock Identification (TPC-H Q11)          |                 266.68 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 499.53 |
| Customer Distribution (TPC-H Q13)                   |                2923.66 |
| Promotion Effect Query (TPC-H Q14)                  |                 625.02 |
| Top Supplier Query (TPC-H Q15)                      |                 473.12 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 493.93 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                2065.92 |
| Large Volume Customer (TPC-H Q18)                   |                9024.69 |
| Discounted Revenue (TPC-H Q19)                      |                 109.59 |
| Potential Part Promotion (TPC-H Q20)                |                 372.74 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 546.15 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 149.71 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        75.26 |      1.22 |           4.40 |                  9.05 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        19.33 |      0.67 |           0.00 |                  1.11 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        14.94 |      0.81 |           4.66 |                  9.46 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        12.29 |      0.00 |           0.27 |                  0.28 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
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

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                    1 |                                                   0 |                                                           0 |                                      2 |                                                  2 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                    2 |                                                   0 |                                                           0 |                                      0 |                                                  0 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
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


### TPC-DS

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 2 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_appmetrics_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1654s 
* Code: 1792321722
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:834808
  * volume_size:1.8T
  * volume_used:816G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792321722

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792321722-78f8448f98-8ndr7: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      254.00 |           4.00 |            0.00 |        165.00 |           81.00 |              2 |           0 |             | None           |             0 | False         |               42.52 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        778 |            0.69 |            15986.46 |           1374.29 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        778 |            0.69 |            15986.46 |           1374.29 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 220.59 |
| TPC-DS Q2     |                 472.10 |
| TPC-DS Q3     |                 440.50 |
| TPC-DS Q4     |               17323.27 |
| TPC-DS Q5     |                 797.98 |
| TPC-DS Q6     |              201729.20 |
| TPC-DS Q7     |                 601.74 |
| TPC-DS Q8     |                 103.88 |
| TPC-DS Q9     |                2515.66 |
| TPC-DS Q10    |                1085.79 |
| TPC-DS Q11    |                9773.93 |
| TPC-DS Q12    |                 140.68 |
| TPC-DS Q13    |                1135.91 |
| TPC-DS Q14a+b |                6512.17 |
| TPC-DS Q15    |                 296.62 |
| TPC-DS Q16    |                 446.24 |
| TPC-DS Q17    |                 697.75 |
| TPC-DS Q18    |                 608.73 |
| TPC-DS Q19    |                 404.24 |
| TPC-DS Q20    |                 259.62 |
| TPC-DS Q21    |                 293.25 |
| TPC-DS Q22    |                6685.43 |
| TPC-DS Q23a+b |               11087.97 |
| TPC-DS Q24a+b |                 920.72 |
| TPC-DS Q25    |                 695.75 |
| TPC-DS Q26    |                 445.03 |
| TPC-DS Q27    |                  42.64 |
| TPC-DS Q28    |                1915.92 |
| TPC-DS Q29    |                 783.63 |
| TPC-DS Q30    |               66383.54 |
| TPC-DS Q31    |                3732.78 |
| TPC-DS Q32    |                 296.18 |
| TPC-DS Q33    |                 820.09 |
| TPC-DS Q34    |                  40.91 |
| TPC-DS Q35    |                1232.95 |
| TPC-DS Q36    |                  44.34 |
| TPC-DS Q37    |                 439.71 |
| TPC-DS Q38    |                2149.55 |
| TPC-DS Q39a+b |                5018.43 |
| TPC-DS Q40    |                 249.15 |
| TPC-DS Q41    |                2615.93 |
| TPC-DS Q42    |                 173.52 |
| TPC-DS Q43    |                  54.47 |
| TPC-DS Q44    |                1145.72 |
| TPC-DS Q45    |                 190.75 |
| TPC-DS Q46    |                  63.47 |
| TPC-DS Q47    |                2215.30 |
| TPC-DS Q48    |                1092.73 |
| TPC-DS Q49    |                 669.57 |
| TPC-DS Q50    |                1568.68 |
| TPC-DS Q51    |                2286.64 |
| TPC-DS Q52    |                 176.85 |
| TPC-DS Q53    |                 208.40 |
| TPC-DS Q54    |                  67.86 |
| TPC-DS Q55    |                 172.75 |
| TPC-DS Q56    |                 702.24 |
| TPC-DS Q57    |                2090.25 |
| TPC-DS Q58    |                 815.09 |
| TPC-DS Q59    |                 746.14 |
| TPC-DS Q60    |                 928.81 |
| TPC-DS Q61    |                  83.45 |
| TPC-DS Q62    |                 177.45 |
| TPC-DS Q63    |                 213.53 |
| TPC-DS Q64    |                 917.67 |
| TPC-DS Q65    |                1267.37 |
| TPC-DS Q66    |                 542.95 |
| TPC-DS Q67    |                5977.61 |
| TPC-DS Q68    |                  67.90 |
| TPC-DS Q69    |                 381.44 |
| TPC-DS Q70    |                 740.77 |
| TPC-DS Q71    |                 804.15 |
| TPC-DS Q72    |                2182.06 |
| TPC-DS Q73    |                  42.54 |
| TPC-DS Q74    |                2096.70 |
| TPC-DS Q75    |                3108.95 |
| TPC-DS Q76    |                 389.41 |
| TPC-DS Q77    |                 457.54 |
| TPC-DS Q78    |                2647.75 |
| TPC-DS Q79    |                 346.30 |
| TPC-DS Q80    |                 739.17 |
| TPC-DS Q81    |              357478.37 |
| TPC-DS Q82    |                 337.50 |
| TPC-DS Q83    |                 143.50 |
| TPC-DS Q84    |                  79.22 |
| TPC-DS Q85    |                 302.28 |
| TPC-DS Q86    |                 419.03 |
| TPC-DS Q87    |                2475.05 |
| TPC-DS Q88    |                2567.54 |
| TPC-DS Q89    |                 233.87 |
| TPC-DS Q90    |                 283.47 |
| TPC-DS Q91    |                 137.93 |
| TPC-DS Q92    |                 101.07 |
| TPC-DS Q93    |                 442.35 |
| TPC-DS Q94    |                 313.32 |
| TPC-DS Q95    |                8088.14 |
| TPC-DS Q96    |                 173.80 |
| TPC-DS Q97    |                 728.03 |
| TPC-DS Q98    |                 417.84 |
| TPC-DS Q99    |                 285.37 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       232.96 |      2.50 |           6.32 |                 13.17 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        31.50 |      0.29 |           0.01 |                  2.43 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       979.66 |      2.75 |           7.86 |                 14.94 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        20.02 |      0.06 |           0.33 |                  0.33 |

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
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                    1 |                                                   0 |                                                           0 |                                      1 |                                                  1 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                    1 |                                                   0 |                                                           0 |                                      6 |                                                  6 |

### Tests
* TEST passed: Loading measured in this experiment
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



### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_postgresql_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_postgresql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1884s 
* Code: 1792318911
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:828113
  * volume_size:1.8T
  * volume_used:809G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:833033
  * volume_size:1.8T
  * volume_used:814G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:847709
  * volume_size:1.8T
  * volume_used:828G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:851079
  * volume_size:1.8T
  * volume_used:832G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792318911-85c767cd4f-m5pkg: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7829.14 |                47898.00 |            375000.00 |                              3205.00 | 3.00 |              225.48 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7854.72 |                47742.00 |            375000.00 |                              3179.00 | 3.00 |              226.22 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7788.32 |                48149.00 |            375000.00 |                              3191.00 | 3.00 |              224.30 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7909.56 |                47411.00 |            375000.00 |                              3091.00 | 3.00 |              227.80 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7715.57 |                48603.00 |            375000.00 |                              3147.00 | 3.00 |              222.21 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7802.91 |                48059.00 |            375000.00 |                              3167.00 | 3.00 |              224.72 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7965.17 |                47080.00 |            375000.00 |                              3123.00 | 3.00 |              229.40 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7671.22 |                48884.00 |            375000.00 |                              3201.00 | 3.00 |              220.93 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              220.93 |                        62536.61 |                48884.00 |           3000000.00 |                              3163.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32673.33 |                91818.00 |            1499484 |                             603.00 |              1500516 |                              3289.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4083.99 |                91822.00 |             187597 |                             530.00 |               187403 |                             16223.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4083.81 |                91826.00 |             187848 |                             537.00 |               187152 |                             15951.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4084.74 |                91805.00 |             187594 |                             505.00 |               187406 |                             16111.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4084.21 |                91817.00 |             187687 |                             486.00 |               187313 |                             15671.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4083.94 |                91823.00 |             187966 |                             527.00 |               187034 |                             15823.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4084.12 |                91819.00 |             187260 |                             508.00 |               187740 |                             15711.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4084.43 |                91812.00 |             187179 |                             544.00 |               187821 |                             15887.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4084.26 |                91816.00 |             188023 |                             489.00 |               186977 |                             16351.00 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48931.66 |                61310.00 |            1501014 |                             537.00 |              1498986 |                              1484.00 |
| postgresql-1-1-4-1-1 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6116.46 |                61310.00 |             187864 |                             595.00 |               187136 |                              1900.00 |
| postgresql-1-1-4-1-2 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6118.05 |                61294.00 |             187299 |                             610.00 |               187701 |                              1900.00 |
| postgresql-1-1-4-1-3 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6121.45 |                61260.00 |             187527 |                             626.00 |               187473 |                              1920.00 |
| postgresql-1-1-4-1-4 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6115.26 |                61322.00 |             187048 |                             608.00 |               187952 |                              1942.00 |
| postgresql-1-1-4-1-5 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6115.46 |                61320.00 |             187530 |                             642.00 |               187470 |                              2022.00 |
| postgresql-1-1-4-1-6 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6116.86 |                61306.00 |             187319 |                             653.00 |               187681 |                              2091.00 |
| postgresql-1-1-4-1-7 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6115.66 |                61318.00 |             186913 |                             693.00 |               188087 |                              2161.00 |
| postgresql-1-1-4-1-8 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6119.85 |                61276.00 |             187015 |                             548.00 |               187985 |                              1862.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32673.33 |                91818.00 |            1499484 |                             603.00 |              1500516 |                              3289.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32673.51 |                91826.00 |            1501154 |                             544.00 |              1498846 |                             16351.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48931.66 |                61310.00 |            1501014 |                             537.00 |              1498986 |                              1484.00 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48939.05 |                61322.00 |            1498515 |                             693.00 |              1501485 |                              2161.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       249.65 |      5.15 |           4.22 |                  7.40 |
| postgresql-1-1-2-1 |       249.65 |      5.15 |           4.22 |                  7.40 |
| postgresql-1-1-3-1 |       249.65 |      5.15 |           4.22 |                  7.40 |
| postgresql-1-1-4-1 |       249.65 |      5.15 |           4.22 |                  7.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       156.44 |      5.32 |           0.11 |                  0.12 |
| postgresql-1-1-2-1 |       156.44 |      5.32 |           0.11 |                  0.12 |
| postgresql-1-1-3-1 |       156.44 |      5.32 |           0.11 |                  0.12 |
| postgresql-1-1-4-1 |       156.44 |      5.32 |           0.11 |                  0.12 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       167.90 |      2.54 |           5.02 |                  8.89 |
| postgresql-1-1-2-1 |       236.70 |      2.78 |           5.18 |                  9.20 |
| postgresql-1-1-3-1 |       194.53 |      3.32 |           5.21 |                  9.26 |
| postgresql-1-1-4-1 |       180.19 |      3.55 |           5.21 |                  9.28 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       181.88 |      2.74 |           0.31 |                  0.32 |
| postgresql-1-1-2-1 |       154.07 |      3.98 |           0.31 |                  0.32 |
| postgresql-1-1-3-1 |       136.79 |      2.95 |           0.55 |                  0.55 |
| postgresql-1-1-4-1 |       248.61 |      5.59 |           0.55 |                  0.55 |

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
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |
| postgresql-1-1-2-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |
| postgresql-1-1-3-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |
| postgresql-1-1-4-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                58.00 |                                                0.00 |                                                        0.00 |                                  15.00 |                                              15.00 |
| postgresql-1-1-2-1 |                                56.00 |                                                0.00 |                                                        0.00 |                                  63.00 |                                              63.00 |
| postgresql-1-1-3-1 |                                52.00 |                                                0.00 |                                                        0.00 |                                  13.00 |                                              13.00 |
| postgresql-1-1-4-1 |                                56.00 |                                                0.00 |                                                        0.00 |                                  11.00 |                                              11.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



















## MySQL

### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_appmetrics.log
```

This
* activates monitoring (`-m`) cluster-wide (`-mc`)
* starts a clean instance of MySQL (`-dbms`)
  * with a sidecar container for monitoring (`-ma`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary


### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1488s 
* Code: 1792325353
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:857321
  * volume_size:1.8T
  * volume_used:837G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792325353
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:858000
  * volume_size:1.8T
  * volume_used:838G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792325353
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792325353-d5496887c-dljxc: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |      119.00 |           5.00 |            0.00 |        110.00 |            4.00 |              1 |           1 |             |                |             0 | False         |              484.03 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        4580.06 |                     4506.60 |         0.00 |                                                      77338.00 |                                              34848.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                        4753.16 |                     4683.54 |         0.00 |                                                      33301.00 |                                              16820.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                        5309.21 |                     5229.52 |         0.00 |                                                      32826.00 |                                              15061.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                        4580.06 |                     4506.60 |         0.00 |                                                      77338.00 |                                              34848.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |         160 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                       10062.37 |                     9913.06 |         0.00 |                                                      33301.00 |                                              15940.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       136.97 |      2.53 |           9.66 |                 11.72 |
| mysql-1-1-2-1 |       136.97 |      2.53 |           9.66 |                 11.72 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       854.41 |     10.75 |           1.54 |                  1.54 |
| mysql-1-1-2-1 |       854.41 |     10.75 |           1.54 |                  1.54 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      2324.37 |      9.20 |          10.86 |                 16.00 |
| mysql-1-1-2-1 |      4383.68 |     16.18 |          12.78 |                 16.00 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      4068.61 |     16.94 |           1.19 |                  1.19 |
| mysql-1-1-2-1 |      4860.70 |     41.25 |           1.19 |                  1.19 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                           455.64 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                           455.64 |                            0.01 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                        111254.29 |                            0.11 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                        246204.36 |                            0.11 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_hammerdb_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1855s 
* Code: 1792331738
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:857105
  * volume_size:1.8T
  * volume_used:837G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792331738
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:859090
  * volume_size:1.8T
  * volume_used:839G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792331738

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792331738-68c995fdd8-lr4fj: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       54.00 |           5.00 |            0.00 |         44.00 |            5.00 |              1 |          16 |             | None           |             0 | False         |             1066.67 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 288541 | 669793 |         0.00 |          5 |        0 |       2.17 |       2.60 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        8 |        2 |               1 |       1 | 302184 | 701936 |         0.00 |          5 |        0 |       2.13 |       2.39 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        8 |        2 |               1 |       2 | 302159 | 701865 |         0.00 |          5 |        0 |       2.15 |       2.38 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |       16 |        1 |               1 |           1 |       2.17 |       2.60 |         0.00 | 288541.00 | 669793.00 |          5 |        0 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |       16 |        2 |               1 |           2 |       2.15 |       2.39 |         0.00 | 302171.50 | 701900.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        68.81 |      1.91 |           5.52 |                  7.30 |
| mysql-1-1-2-1 |        68.81 |      1.91 |           5.52 |                  7.30 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       389.95 |     11.12 |           0.17 |                  0.17 |
| mysql-1-1-2-1 |       389.95 |     11.12 |           0.17 |                  0.17 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      4063.05 |      9.92 |           6.98 |                 21.81 |
| mysql-1-1-2-1 |      4057.82 |      9.84 |           9.44 |                 38.11 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1239.67 |      3.15 |           0.36 |                  0.36 |
| mysql-1-1-2-1 |      1302.98 |      3.40 |           0.36 |                  0.36 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                           483.21 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                           483.21 |                            0.01 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                       1638500.11 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                       1675960.63 |                            0.01 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>


### TPC-H

Example:
```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 3 \
  -nlp 2 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_tpch_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 982s 
* Code: 1792329039
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860816
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792329039

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792329039-cc675b756-j27d5: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      157.00 |           5.00 |            1.00 |         85.00 |           51.00 |              2 |           0 |             | None           |             0 | False         |               68.79 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |        130 |            2.42 |             4617.93 |           1827.69 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |        130 |            2.42 |             4617.93 |           1827.69 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          19344.83 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            261.48 |
| Shipping Priority (TPC-H Q3)                        |           4312.15 |
| Order Priority Checking Query (TPC-H Q4)            |           1029.26 |
| Local Supplier Volume (TPC-H Q5)                    |           2498.32 |
| Forecasting Revenue Change (TPC-H Q6)               |           2450.32 |
| Volume Shipping Query (TPC-H Q7)                    |           1889.96 |
| National Market Share (TPC-H Q8)                    |           6322.49 |
| Product Type Profit Measure (TPC-H Q9)              |           5605.84 |
| Returned Item Reporting Query (TPC-H Q10)           |           3392.17 |
| Important Stock Identification (TPC-H Q11)          |            458.71 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           3991.19 |
| Customer Distribution (TPC-H Q13)                   |          14136.89 |
| Promotion Effect Query (TPC-H Q14)                  |           3076.50 |
| Top Supplier Query (TPC-H Q15)                      |          37232.33 |
| Parts/Supplier Relationship (TPC-H Q16)             |            901.65 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            597.21 |
| Large Volume Customer (TPC-H Q18)                   |           3776.26 |
| Discounted Revenue (TPC-H Q19)                      |            311.71 |
| Potential Part Promotion (TPC-H Q20)                |            672.57 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          10645.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |            311.95 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       215.93 |      2.79 |           8.05 |                 13.56 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         6.07 |      0.05 |           0.01 |                  1.36 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        93.29 |      1.01 |           8.42 |                 13.93 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        14.66 |      0.03 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             0.87 |                            0.00 |                            0.02 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.19 |                            0.00 |                            0.02 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
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


### TPC-DS

Example:
```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 3 \
  -nlp 2 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mysql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_tpcds_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1501s 
* Code: 1792330119
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:898804
  * volume_size:1.8T
  * volume_used:878G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1792330119

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792330119-55cdfb74c9-sgm7c: 1 (dbms=1, monitor-application=0)
  * dbms: OOMKilled (exit 137) at Sun, 18 Oct 2026 15:48:32 +0200; data on a mounted volume

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      753.00 |           6.00 |            0.00 |        177.00 |          566.00 |              2 |           0 |             | None           |             0 | False         |               14.34 | False               |

### Benchmarking

#### Per Connection

No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 1 of 1 connections; Q2 failed in 1 of 1 connections; Q3 failed in 1 of 1 connections; Q4 failed in 1 of 1 connections; Q5 failed in 1 of 1 connections; Q6 failed in 1 of 1 connections; Q7 failed in 1 of 1 connections; Q8 failed in 1 of 1 connections; Q9 failed in 1 of 1 connections; Q10 failed in 1 of 1 connections; Q11 failed in 1 of 1 connections; Q12 failed in 1 of 1 connections; Q13 failed in 1 of 1 connections; Q14 failed in 1 of 1 connections; Q15 failed in 1 of 1 connections; Q16 failed in 1 of 1 connections; Q17 failed in 1 of 1 connections; Q18 failed in 1 of 1 connections; Q19 failed in 1 of 1 connections; Q20 failed in 1 of 1 connections; Q21 failed in 1 of 1 connections; Q22 failed in 1 of 1 connections; Q23 failed in 1 of 1 connections; Q24 failed in 1 of 1 connections; Q25 failed in 1 of 1 connections; Q26 failed in 1 of 1 connections; Q27 failed in 1 of 1 connections; Q28 failed in 1 of 1 connections; Q29 failed in 1 of 1 connections; Q30 failed in 1 of 1 connections; Q31 failed in 1 of 1 connections; Q32 failed in 1 of 1 connections; Q33 failed in 1 of 1 connections; Q34 failed in 1 of 1 connections; Q35 failed in 1 of 1 connections; Q36 failed in 1 of 1 connections; Q37 failed in 1 of 1 connections; Q38 failed in 1 of 1 connections; Q39 failed in 1 of 1 connections; Q40 failed in 1 of 1 connections; Q41 failed in 1 of 1 connections; Q42 failed in 1 of 1 connections; Q43 failed in 1 of 1 connections; Q44 failed in 1 of 1 connections; Q45 failed in 1 of 1 connections; Q46 failed in 1 of 1 connections; Q47 failed in 1 of 1 connections; Q48 failed in 1 of 1 connections; Q49 failed in 1 of 1 connections; Q50 failed in 1 of 1 connections; Q51 failed in 1 of 1 connections; Q52 failed in 1 of 1 connections; Q53 failed in 1 of 1 connections; Q54 failed in 1 of 1 connections; Q55 failed in 1 of 1 connections; Q56 failed in 1 of 1 connections; Q57 failed in 1 of 1 connections; Q58 failed in 1 of 1 connections; Q59 failed in 1 of 1 connections; Q60 failed in 1 of 1 connections; Q61 failed in 1 of 1 connections; Q62 failed in 1 of 1 connections; Q63 failed in 1 of 1 connections; Q64 failed in 1 of 1 connections; Q65 failed in 1 of 1 connections; Q66 failed in 1 of 1 connections; Q67 failed in 1 of 1 connections; Q68 failed in 1 of 1 connections; Q69 failed in 1 of 1 connections; Q70 failed in 1 of 1 connections; Q71 failed in 1 of 1 connections; Q72 failed in 1 of 1 connections; Q73 failed in 1 of 1 connections; Q74 failed in 1 of 1 connections; Q75 failed in 1 of 1 connections; Q76 failed in 1 of 1 connections; Q77 failed in 1 of 1 connections; Q78 failed in 1 of 1 connections; Q79 failed in 1 of 1 connections; Q80 failed in 1 of 1 connections; Q81 failed in 1 of 1 connections; Q82 failed in 1 of 1 connections; Q83 failed in 1 of 1 connections; Q84 failed in 1 of 1 connections; Q85 failed in 1 of 1 connections; Q86 failed in 1 of 1 connections; Q87 failed in 1 of 1 connections; Q88 failed in 1 of 1 connections; Q89 failed in 1 of 1 connections; Q90 failed in 1 of 1 connections; Q91 failed in 1 of 1 connections; Q92 failed in 1 of 1 connections; Q93 failed in 1 of 1 connections; Q94 failed in 1 of 1 connections; Q95 failed in 1 of 1 connections; Q96 failed in 1 of 1 connections; Q97 failed in 1 of 1 connections; Q98 failed in 1 of 1 connections; Q99 failed in 1 of 1 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Per Phase

No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 1 of 1 connections; Q2 failed in 1 of 1 connections; Q3 failed in 1 of 1 connections; Q4 failed in 1 of 1 connections; Q5 failed in 1 of 1 connections; Q6 failed in 1 of 1 connections; Q7 failed in 1 of 1 connections; Q8 failed in 1 of 1 connections; Q9 failed in 1 of 1 connections; Q10 failed in 1 of 1 connections; Q11 failed in 1 of 1 connections; Q12 failed in 1 of 1 connections; Q13 failed in 1 of 1 connections; Q14 failed in 1 of 1 connections; Q15 failed in 1 of 1 connections; Q16 failed in 1 of 1 connections; Q17 failed in 1 of 1 connections; Q18 failed in 1 of 1 connections; Q19 failed in 1 of 1 connections; Q20 failed in 1 of 1 connections; Q21 failed in 1 of 1 connections; Q22 failed in 1 of 1 connections; Q23 failed in 1 of 1 connections; Q24 failed in 1 of 1 connections; Q25 failed in 1 of 1 connections; Q26 failed in 1 of 1 connections; Q27 failed in 1 of 1 connections; Q28 failed in 1 of 1 connections; Q29 failed in 1 of 1 connections; Q30 failed in 1 of 1 connections; Q31 failed in 1 of 1 connections; Q32 failed in 1 of 1 connections; Q33 failed in 1 of 1 connections; Q34 failed in 1 of 1 connections; Q35 failed in 1 of 1 connections; Q36 failed in 1 of 1 connections; Q37 failed in 1 of 1 connections; Q38 failed in 1 of 1 connections; Q39 failed in 1 of 1 connections; Q40 failed in 1 of 1 connections; Q41 failed in 1 of 1 connections; Q42 failed in 1 of 1 connections; Q43 failed in 1 of 1 connections; Q44 failed in 1 of 1 connections; Q45 failed in 1 of 1 connections; Q46 failed in 1 of 1 connections; Q47 failed in 1 of 1 connections; Q48 failed in 1 of 1 connections; Q49 failed in 1 of 1 connections; Q50 failed in 1 of 1 connections; Q51 failed in 1 of 1 connections; Q52 failed in 1 of 1 connections; Q53 failed in 1 of 1 connections; Q54 failed in 1 of 1 connections; Q55 failed in 1 of 1 connections; Q56 failed in 1 of 1 connections; Q57 failed in 1 of 1 connections; Q58 failed in 1 of 1 connections; Q59 failed in 1 of 1 connections; Q60 failed in 1 of 1 connections; Q61 failed in 1 of 1 connections; Q62 failed in 1 of 1 connections; Q63 failed in 1 of 1 connections; Q64 failed in 1 of 1 connections; Q65 failed in 1 of 1 connections; Q66 failed in 1 of 1 connections; Q67 failed in 1 of 1 connections; Q68 failed in 1 of 1 connections; Q69 failed in 1 of 1 connections; Q70 failed in 1 of 1 connections; Q71 failed in 1 of 1 connections; Q72 failed in 1 of 1 connections; Q73 failed in 1 of 1 connections; Q74 failed in 1 of 1 connections; Q75 failed in 1 of 1 connections; Q76 failed in 1 of 1 connections; Q77 failed in 1 of 1 connections; Q78 failed in 1 of 1 connections; Q79 failed in 1 of 1 connections; Q80 failed in 1 of 1 connections; Q81 failed in 1 of 1 connections; Q82 failed in 1 of 1 connections; Q83 failed in 1 of 1 connections; Q84 failed in 1 of 1 connections; Q85 failed in 1 of 1 connections; Q86 failed in 1 of 1 connections; Q87 failed in 1 of 1 connections; Q88 failed in 1 of 1 connections; Q89 failed in 1 of 1 connections; Q90 failed in 1 of 1 connections; Q91 failed in 1 of 1 connections; Q92 failed in 1 of 1 connections; Q93 failed in 1 of 1 connections; Q94 failed in 1 of 1 connections; Q95 failed in 1 of 1 connections; Q96 failed in 1 of 1 connections; Q97 failed in 1 of 1 connections; Q98 failed in 1 of 1 connections; Q99 failed in 1 of 1 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1         | 0/1          | 0/1          | 0/1          | 0/1          | 0/1             | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1             | 0/1             | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1             | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | 0/1          | no         |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Per Phase (Complete Phases Only)

Only the 0 of 1 phases in which every pod completed every active query; each row covers all 99 active queries, so the rows are comparable with each other. Left out: mysql-1-1-1 — see Query Completion per Phase.

### Latency of Timer Execution [ms]
No rows: these totals count only queries that succeeded in every connection of this experiment, and no query did (Q1 failed in 1 of 1 connections; Q2 failed in 1 of 1 connections; Q3 failed in 1 of 1 connections; Q4 failed in 1 of 1 connections; Q5 failed in 1 of 1 connections; Q6 failed in 1 of 1 connections; Q7 failed in 1 of 1 connections; Q8 failed in 1 of 1 connections; Q9 failed in 1 of 1 connections; Q10 failed in 1 of 1 connections; Q11 failed in 1 of 1 connections; Q12 failed in 1 of 1 connections; Q13 failed in 1 of 1 connections; Q14 failed in 1 of 1 connections; Q15 failed in 1 of 1 connections; Q16 failed in 1 of 1 connections; Q17 failed in 1 of 1 connections; Q18 failed in 1 of 1 connections; Q19 failed in 1 of 1 connections; Q20 failed in 1 of 1 connections; Q21 failed in 1 of 1 connections; Q22 failed in 1 of 1 connections; Q23 failed in 1 of 1 connections; Q24 failed in 1 of 1 connections; Q25 failed in 1 of 1 connections; Q26 failed in 1 of 1 connections; Q27 failed in 1 of 1 connections; Q28 failed in 1 of 1 connections; Q29 failed in 1 of 1 connections; Q30 failed in 1 of 1 connections; Q31 failed in 1 of 1 connections; Q32 failed in 1 of 1 connections; Q33 failed in 1 of 1 connections; Q34 failed in 1 of 1 connections; Q35 failed in 1 of 1 connections; Q36 failed in 1 of 1 connections; Q37 failed in 1 of 1 connections; Q38 failed in 1 of 1 connections; Q39 failed in 1 of 1 connections; Q40 failed in 1 of 1 connections; Q41 failed in 1 of 1 connections; Q42 failed in 1 of 1 connections; Q43 failed in 1 of 1 connections; Q44 failed in 1 of 1 connections; Q45 failed in 1 of 1 connections; Q46 failed in 1 of 1 connections; Q47 failed in 1 of 1 connections; Q48 failed in 1 of 1 connections; Q49 failed in 1 of 1 connections; Q50 failed in 1 of 1 connections; Q51 failed in 1 of 1 connections; Q52 failed in 1 of 1 connections; Q53 failed in 1 of 1 connections; Q54 failed in 1 of 1 connections; Q55 failed in 1 of 1 connections; Q56 failed in 1 of 1 connections; Q57 failed in 1 of 1 connections; Q58 failed in 1 of 1 connections; Q59 failed in 1 of 1 connections; Q60 failed in 1 of 1 connections; Q61 failed in 1 of 1 connections; Q62 failed in 1 of 1 connections; Q63 failed in 1 of 1 connections; Q64 failed in 1 of 1 connections; Q65 failed in 1 of 1 connections; Q66 failed in 1 of 1 connections; Q67 failed in 1 of 1 connections; Q68 failed in 1 of 1 connections; Q69 failed in 1 of 1 connections; Q70 failed in 1 of 1 connections; Q71 failed in 1 of 1 connections; Q72 failed in 1 of 1 connections; Q73 failed in 1 of 1 connections; Q74 failed in 1 of 1 connections; Q75 failed in 1 of 1 connections; Q76 failed in 1 of 1 connections; Q77 failed in 1 of 1 connections; Q78 failed in 1 of 1 connections; Q79 failed in 1 of 1 connections; Q80 failed in 1 of 1 connections; Q81 failed in 1 of 1 connections; Q82 failed in 1 of 1 connections; Q83 failed in 1 of 1 connections; Q84 failed in 1 of 1 connections; Q85 failed in 1 of 1 connections; Q86 failed in 1 of 1 connections; Q87 failed in 1 of 1 connections; Q88 failed in 1 of 1 connections; Q89 failed in 1 of 1 connections; Q90 failed in 1 of 1 connections; Q91 failed in 1 of 1 connections; Q92 failed in 1 of 1 connections; Q93 failed in 1 of 1 connections; Q94 failed in 1 of 1 connections; Q95 failed in 1 of 1 connections; Q96 failed in 1 of 1 connections; Q97 failed in 1 of 1 connections; Q98 failed in 1 of 1 connections; Q99 failed in 1 of 1 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       970.77 |      2.95 |          63.98 |                 64.00 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         6.79 |      0.13 |           0.01 |                  2.43 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      1.03 |          63.98 |                 64.00 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Connection Usage Ratio [0..1] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Average Redo Log Bytes per fsync [B] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Buffer Pool Wait Free [count] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Max Dirty Pages [%] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Max Dirty Pages Low Watermark [%] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Buffer Pool Bytes Data [B] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* InnoDB Redo Log Flushed to Disk [B] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Ratio of Dirty Pages in Buffer Pool [%] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Threads Running for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Open Files Usage Ratio [0..1] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.18 |                            0.00 |                            0.02 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             0.40 |                            0.00 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST failed: No SUT container restarts
* TEST passed: SUT data survived container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST failed: Monitoring metrics missing
* TEST failed: Geo Times [s] contains 0 or NaN
* TEST failed: Power@Size [~Q/h] contains 0 or NaN
* TEST failed: Throughput@Size contains 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>



### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms MySQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 2044s 
* Code: 1792326913
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860668
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860671
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:801738
  * volume_size:1.8T
  * volume_used:783G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860678
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792326913-6f7877696f-9qkjh: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8002.39 |                46861.00 |            375000.00 |                              8155.00 | 3.00 |              230.47 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8020.88 |                46753.00 |            375000.00 |                              8039.00 | 3.00 |              231.00 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8008.71 |                46824.00 |            375000.00 |                              7967.00 | 3.00 |              230.65 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7997.61 |                46889.00 |            375000.00 |                              8055.00 | 3.00 |              230.33 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8031.01 |                46694.00 |            375000.00 |                              8079.00 | 3.00 |              231.29 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7994.88 |                46905.00 |            375000.00 |                              7967.00 | 3.00 |              230.25 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7988.07 |                46945.00 |            375000.00 |                              7987.00 | 3.00 |              230.06 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8018.82 |                46765.00 |            375000.00 |                              8063.00 | 3.00 |              230.94 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              230.06 |                        64062.37 |                46945.00 |           3000000.00 |                              8039.00 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32140.56 |                93340.00 |            1500802 |                             661.00 |              1499198 |                               631.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4048.15 |                92635.00 |             187475 |                             707.00 |               187525 |                               653.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4055.63 |                92464.00 |             187746 |                             746.00 |               187254 |                               692.00 |
| mysql-1-1-2-1-3 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4060.77 |                92347.00 |             187439 |                             737.00 |               187561 |                               677.00 |
| mysql-1-1-2-1-4 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4051.38 |                92561.00 |             187657 |                             644.00 |               187343 |                               592.00 |
| mysql-1-1-2-1-5 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4051.86 |                92550.00 |             187108 |                             646.00 |               187892 |                               583.00 |
| mysql-1-1-2-1-6 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4048.15 |                92635.00 |             187507 |                             701.00 |               187493 |                               654.00 |
| mysql-1-1-2-1-7 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4048.93 |                92617.00 |             187395 |                             661.00 |               187605 |                               606.00 |
| mysql-1-1-2-1-8 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4052.65 |                92532.00 |             187489 |                             643.00 |               187511 |                               587.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        47409.84 |                63278.00 |            1499277 |                             859.00 |              1500723 |                               954.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6039.33 |                62093.00 |             187778 |                             667.00 |               187222 |                               594.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6054.64 |                61936.00 |             187583 |                             736.00 |               187417 |                               657.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6063.84 |                61842.00 |             187048 |                             754.00 |               187952 |                               667.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6033.30 |                62155.00 |             187471 |                             760.00 |               187529 |                               690.00 |
| mysql-1-1-4-1-5 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6055.03 |                61932.00 |             187619 |                             736.00 |               187381 |                               655.00 |
| mysql-1-1-4-1-6 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6033.40 |                62154.00 |             187654 |                             670.00 |               187346 |                               595.00 |
| mysql-1-1-4-1-7 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6048.78 |                61996.00 |             187414 |                             711.00 |               187586 |                               633.00 |
| mysql-1-1-4-1-8 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6056.01 |                61922.00 |             187413 |                             771.00 |               187587 |                               677.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32140.56 |                93340.00 |            1500802 |                             661.00 |              1499198 |                               631.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32417.53 |                92635.00 |            1499816 |                             746.00 |              1500184 |                               692.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        47409.84 |                63278.00 |            1499277 |                             859.00 |              1500723 |                               954.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48384.32 |                62155.00 |            1499980 |                             771.00 |              1500020 |                               690.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       379.19 |      8.50 |           8.82 |                 14.52 |
| mysql-1-1-2-1 |       379.19 |      8.50 |           8.82 |                 14.52 |
| mysql-1-1-3-1 |       379.19 |      8.50 |           8.82 |                 14.52 |
| mysql-1-1-4-1 |       379.19 |      8.50 |           8.82 |                 14.52 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       370.08 |     11.52 |           1.05 |                  1.05 |
| mysql-1-1-2-1 |       370.08 |     11.52 |           1.05 |                  1.05 |
| mysql-1-1-3-1 |       370.08 |     11.52 |           1.05 |                  1.05 |
| mysql-1-1-4-1 |       370.08 |     11.52 |           1.05 |                  1.05 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       270.75 |      3.89 |           7.95 |                 14.22 |
| mysql-1-1-2-1 |       298.68 |      3.84 |           8.00 |                 15.10 |
| mysql-1-1-3-1 |       261.91 |      5.18 |           8.04 |                 15.87 |
| mysql-1-1-4-1 |       239.05 |      4.88 |           8.08 |                 16.64 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       303.82 |      3.12 |           1.39 |                  1.40 |
| mysql-1-1-2-1 |       282.42 |      6.28 |           1.39 |                  1.40 |
| mysql-1-1-3-1 |       229.11 |      8.40 |           1.37 |                  1.38 |
| mysql-1-1-4-1 |       331.08 |      8.14 |           1.37 |                  1.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                          9908.63 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                          8558.24 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                          7206.84 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                          9368.60 |                            0.04 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>








## CockroachDB

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms CockroachDB \
  -sf 10 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 3 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 10989s 
* Code: 1792333677
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:854127
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:151647
    * datadisk:700899
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:681817
    * datadisk:700833
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:252912
    * datadisk:700827
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792333677
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792333677-f67bb46db-7vp4q: 0
* bexhoma-worker-cockroachdb-ycsb-10-0: 0
* bexhoma-worker-cockroachdb-ycsb-10-1: 0
* bexhoma-worker-cockroachdb-ycsb-10-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          376.60 |              3319210.00 |           1250000.00 |                            155007.00 | 10.00 |               10.85 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          364.86 |              3425973.00 |           1250000.00 |                            155903.00 | 10.00 |               10.51 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          366.02 |              3415155.00 |           1250000.00 |                            155775.00 | 10.00 |               10.54 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          376.27 |              3322086.00 |           1250000.00 |                            154751.00 | 10.00 |               10.84 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          364.05 |              3433639.00 |           1250000.00 |                            155903.00 | 10.00 |               10.48 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          364.71 |              3427389.00 |           1250000.00 |                            155263.00 | 10.00 |               10.50 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          363.76 |              3436320.00 |           1250000.00 |                            156543.00 | 10.00 |               10.48 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          366.15 |              3413939.00 |           1250000.00 |                            155647.00 | 10.00 |               10.55 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               10.48 |                         2942.40 |              3436320.00 |          10000000.00 |                            155599.00 |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         1635.69 |              6113623.00 |            5002464 |                           36703.00 |              4997536 |                           1948671.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         1635.69 |              6113623.00 |            5002464 |                           36703.00 |              4997536 |                           1948671.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     29067.12 |     22.25 |          19.25 |                 47.99 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       901.87 |      1.45 |           0.12 |                  0.13 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     35013.89 |      8.06 |          22.06 |                 47.99 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       782.26 |      0.56 |           0.24 |                  0.24 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    12891.76 |             17774623.27 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     4374.27 |              3165371.58 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms CockroachDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nw 3 \
  -nwr 3 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1317s 
* Code: 1792344739
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:853969
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:143579
    * datadisk:691715
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:879746
    * datadisk:691506
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:154257
    * datadisk:691678
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792344739
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:853973
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:143760
    * datadisk:691888
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:879853
    * datadisk:691676
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:154330
    * datadisk:691746
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792344739
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792344739-7f9dd56c5f-vrdf2: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-0: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-1: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      299.00 |           4.00 |            0.00 |        290.00 |            5.00 |              1 |           1 |             | None           |             0 | False         |              192.64 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         267.31 |                      266.09 |         0.00 |                                                     187956.00 |                                              59837.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         122.59 |                      122.07 |         0.00 |                                                     191186.00 |                                              65239.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         119.22 |                      118.78 |         0.00 |                                                     190421.00 |                                              67092.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         267.31 |                      266.09 |         0.00 |                                                     187956.00 |                                              59837.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         241.81 |                      240.85 |         0.00 |                                                     191186.00 |                                              66165.50 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2625.98 |     19.22 |           7.54 |                 11.44 |
| cockroachdb-1-1-2-1 |      2625.98 |     19.22 |           7.54 |                 11.44 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       964.88 |      9.36 |           0.27 |                  0.27 |
| cockroachdb-1-1-2-1 |       964.88 |      9.36 |           0.27 |                  0.27 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      4113.62 |     15.73 |           7.92 |                 11.92 |
| cockroachdb-1-1-2-1 |      3767.58 |     13.56 |           7.80 |                 12.17 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       145.74 |      0.55 |           0.30 |                  0.30 |
| cockroachdb-1-1-2-1 |       145.74 |      1.34 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     1354.31 |             13646676.41 |                              0.00 |                                      0.38 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     1354.31 |             13646676.41 |                              0.00 |                                      0.38 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    14453.18 |             10715075.91 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                    13422.10 |              5603661.82 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>





## Redis

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms Redis \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 1 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 585s 
* Code: 1792346117
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Redis'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:854802
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:143873
    * datadisk:717
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:151397
    * datadisk:803
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:617872
    * datadisk:721
    * cpu_list:0-127
  * worker 3
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:878208
    * datadisk:714
    * cpu_list:0-255
  * worker 4
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:870689
    * datadisk:714
    * cpu_list:0-255
  * worker 5
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:854803
    * datadisk:806
    * cpu_list:0-223
  * resources_total: 24.25 CPU, 96.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 96.0 GiB RAM
  * eval_parameters
    * code:1792346117
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-redis-1-1792346117-958975b77-gh27h: 0
* bx-w-redis-ycsb-1-0: 0
* bx-w-redis-ycsb-1-1: 0
* bx-w-redis-ycsb-1-2: 0
* bx-w-redis-ycsb-1-3: 0
* bx-w-redis-ycsb-1-4: 0
* bx-w-redis-ycsb-1-5: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3859.93 |                32384.00 |            125000.00 |                              4683.00 | 1.00 |              111.17 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3840.36 |                32549.00 |            125000.00 |                              4675.00 | 1.00 |              110.60 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3973.05 |                31462.00 |            125000.00 |                              4687.00 | 1.00 |              114.42 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3861.60 |                32370.00 |            125000.00 |                              4683.00 | 1.00 |              111.21 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3841.31 |                32541.00 |            125000.00 |                              4683.00 | 1.00 |              110.63 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3896.75 |                32078.00 |            125000.00 |                              4699.00 | 1.00 |              112.23 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3858.98 |                32392.00 |            125000.00 |                              4703.00 | 1.00 |              111.14 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3882.71 |                32194.00 |            125000.00 |                              4683.00 | 1.00 |              111.82 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              110.60 |                        31014.69 |                32549.00 |           1000000.00 |                              4687.00 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        60853.53 |               164329.00 |            4999181 |                            1623.00 |              5000819 |                              1615.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        60853.53 |               164329.00 |            4999181 |                            1623.00 |              5000819 |                              1615.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       158.90 |      2.83 |           3.07 |                  3.07 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |        59.52 |      0.00 |           0.30 |                  0.31 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       420.73 |      3.42 |           3.27 |                  3.28 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       593.24 |      3.94 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      201.00 |                      2.90 |                       3.00 |                                           5913.96 |

#### Benchmarking phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      403.00 |                      2.91 |                       3.00 |                                          12275.30 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>









## TiDB

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  run &>$LOG_DIR/docs_ycsb_tidb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_tidb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_tidb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 585s 
* Code: 1792346768
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:631401
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:631401
    * cpu_list:0-127
  * sut 1
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:144405
    * cpu_list:0-95
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:169495
    * cpu_list:0-127
  * pd 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:144406
    * datadisk:123
    * cpu_list:0-95
  * pd 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:631401
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:170897
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:144405
    * datadisk:5373
    * cpu_list:0-95
  * tikv 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:631401
    * datadisk:11994
    * cpu_list:0-127
  * tikv 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:169494
    * datadisk:7370
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * eval_parameters
    * code:1792346768
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792346768-6c6588cf4-42vnj: 0
* bexhoma-sut-tidb-1-1792346768-6c6588cf4-6xbtd: 0
* bexhoma-sut-tidb-1-1792346768-6c6588cf4-g7br9: 0
* bexhoma-pd-tidb-ycsb-1-0: 0
* bexhoma-pd-tidb-ycsb-1-1: 0
* bexhoma-pd-tidb-ycsb-1-2: 0
* bexhoma-tikv-tidb-ycsb-1-0: 0
* bexhoma-tikv-tidb-ycsb-1-1: 0
* bexhoma-tikv-tidb-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| tidb-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1574.86 |                79372.00 |            125000.00 |                             21951.00 | 1.00 |               45.36 |
| tidb-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1615.13 |                77393.00 |            125000.00 |                             18831.00 | 1.00 |               46.52 |
| tidb-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1608.23 |                77725.00 |            125000.00 |                             20255.00 | 1.00 |               46.32 |
| tidb-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1583.56 |                78936.00 |            125000.00 |                             19279.00 | 1.00 |               45.61 |
| tidb-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1771.44 |                70564.00 |            125000.00 |                             18191.00 | 1.00 |               51.02 |
| tidb-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1589.64 |                78634.00 |            125000.00 |                             20815.00 | 1.00 |               45.78 |
| tidb-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1594.23 |                78408.00 |            125000.00 |                             22015.00 | 1.00 |               45.91 |
| tidb-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1583.16 |                78956.00 |            125000.00 |                             22031.00 | 1.00 |               45.60 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               45.36 |                        12920.26 |                79372.00 |           1000000.00 |                             20421.00 |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                        13726.84 |                72850.00 |             500121 |                            2547.00 |               499879 |                            103359.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                        13726.84 |                72850.00 |             500121 |                            2547.00 |               499879 |                            103359.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       966.23 |     13.20 |           1.71 |                  2.25 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        71.05 |      0.87 |           0.22 |                  0.22 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       637.61 |      8.26 |           7.82 |                 15.54 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       111.70 |      2.07 |           0.32 |                  0.33 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       808.11 |     13.87 |           1.89 |                  2.42 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        59.82 |      0.96 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       568.99 |     12.38 |           9.52 |                 20.17 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        59.31 |      1.08 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* PD Leader Balance Actions [count] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdbenchmarking.log)
* PD Leader Balance Actions [count] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdloading.log)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration since Start [ms] |
|:-------------|----------------------------------------:|-------------------------------------------:|
| tidb-1-1-1-1 |                                 4202.97 |                                       4.30 |

#### Loading phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [count] |
|:-------------|--------------------------:|------------------------------------:|
| tidb-1-1-1-1 |                     37.00 |                                0.00 |

#### Loading phase: component tikv

| DBMS         |   TiKV Store Size Used [GiB] |   TiKV Store Used [%] |   TiKV Compaction Time Median, Max over Instances [s] |   TiKV Compaction Flow [GiB] |   TiKV Compaction Pending [GiB] |
|:-------------|-----------------------------:|----------------------:|------------------------------------------------------:|-----------------------------:|--------------------------------:|
| tidb-1-1-1-1 |                        22.78 |                  1.38 |                                                  5.68 |                         5.94 |                            0.48 |

#### Benchmarking phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration since Start [ms] |
|:-------------|----------------------------------------:|-------------------------------------------:|
| tidb-1-1-1-1 |                                 5588.12 |                                       4.33 |

#### Benchmarking phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [count] |
|:-------------|--------------------------:|------------------------------------:|
| tidb-1-1-1-1 |                     39.00 |                                0.00 |

#### Benchmarking phase: component tikv

| DBMS         |   TiKV Store Size Used [GiB] |   TiKV Store Used [%] |   TiKV Compaction Time Median, Max over Instances [s] |   TiKV Compaction Flow [GiB] |   TiKV Compaction Pending [GiB] |
|:-------------|-----------------------------:|----------------------:|------------------------------------------------------:|-----------------------------:|--------------------------------:|
| tidb-1-1-1-1 |                        23.49 |                  1.43 |                                                  2.57 |                         0.41 |                            0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


### Benchbase's TPC-C

Example:
```bash

bexhoma benchbase \
  -dbms TiDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  run &>$LOG_DIR/docs_benchbase_tidb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_tidb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_tidb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1274s 
* Code: 1792347432
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:619408
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619408
    * cpu_list:0-127
  * sut 1
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:145175
    * cpu_list:0-95
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:168978
    * cpu_list:0-127
  * pd 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:141439
    * datadisk:123
    * cpu_list:0-95
  * pd 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619408
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:167992
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:168348
    * datadisk:9144
    * cpu_list:0-127
  * tikv 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:894446
    * datadisk:24450
    * cpu_list:0-255
  * tikv 2
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:902000
    * datadisk:24562
    * cpu_list:0-255
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * eval_parameters
    * code:1792347432
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:619409
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619409
    * cpu_list:0-127
  * sut 1
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:142124
    * cpu_list:0-95
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:173821
    * cpu_list:0-127
  * pd 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:144056
    * datadisk:123
    * cpu_list:0-95
  * pd 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619409
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:173821
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:173821
    * datadisk:11727
    * cpu_list:0-127
  * tikv 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:893123
    * datadisk:23126
    * cpu_list:0-255
  * tikv 2
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:904359
    * datadisk:23140
    * cpu_list:0-255
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * eval_parameters
    * code:1792347432
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792347432-64dc45fb4-dvvb5: 0
* bexhoma-sut-tidb-1-1792347432-64dc45fb4-gjkbz: 0
* bexhoma-sut-tidb-1-1792347432-64dc45fb4-wvpsm: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-0: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-1: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-2: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-0: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-1: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      232.00 |           5.00 |            0.00 |        223.00 |            4.00 |              1 |           1 |             | None           |             0 | False         |              248.28 | False               |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         422.51 |                      420.65 |         0.00 |                                                      93952.00 |                                              37856.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         187.19 |                      184.98 |         0.00 |                                                     105555.00 |                                              42724.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         203.06 |                      200.67 |         0.00 |                                                     102407.00 |                                              39383.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         422.51 |                      420.65 |         0.00 |                                                      93952.00 |                                              37856.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         390.25 |                      385.65 |         0.00 |                                                     105555.00 |                                              41053.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       928.99 |      4.98 |           1.34 |                  1.88 |
| tidb-1-1-2-1 |       928.99 |      4.98 |           1.34 |                  1.88 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        63.84 |      0.30 |           0.21 |                  0.21 |
| tidb-1-1-2-1 |        63.84 |      0.30 |           0.21 |                  0.21 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2708.40 |     15.77 |          13.60 |                 29.90 |
| tidb-1-1-2-1 |      2708.40 |     15.77 |          13.60 |                 29.90 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       114.09 |      1.05 |           0.49 |                  0.49 |
| tidb-1-1-2-1 |       114.09 |      1.05 |           0.49 |                  0.49 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3102.39 |     11.66 |           2.44 |                  2.98 |
| tidb-1-1-2-1 |      2993.80 |     10.78 |           2.70 |                  3.24 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       306.06 |      1.04 |           0.22 |                  0.22 |
| tidb-1-1-2-1 |       297.88 |      1.05 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3836.32 |     14.60 |          15.44 |                 31.98 |
| tidb-1-1-2-1 |      4229.86 |     15.56 |          17.59 |                 37.38 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       221.98 |      0.80 |           0.34 |                  0.34 |
| tidb-1-1-2-1 |       221.98 |      2.14 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>






## PGBouncer

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms PGBouncer \
  -sf 16 \
  -xwl c \
  -xtb 16384 \
  -xnbf 11 \
  -xnlf 11 \
  -nc 1 \
  -ne 1 \
  -nlp 16 \
  -nlt 64 \
  -nbp 16 \
  -nbt 128 \
  -xnpp 4 \
  -xnpi 128 \
  -xnpo 64 \
  -xop 16 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 80Gi \
  -rnn $BEXHOMA_NODE_SUT \
  run &>$LOG_DIR/docs_ycsb_pgbouncer_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_pgbouncer_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_pgbouncer_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=16
* Type: ycsb
* Duration: 1144s 
* Code: 1783895142
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 16000000.
  * Ordering of inserts is hashed.
  * Number of operations is 16000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [11].
  * Factors for benchmarking are [11].
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 16 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 80Gi.
  * Loading is tested with [64] threads, split into [16] pods.
  * Benchmarking is tested with [128] threads, split into [16] pods.
  * Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PGBouncer-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1125018
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * pool 0
    * node:cl-worker39
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker24
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 2
    * node:cl-worker25
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 3
    * node:cl-worker28
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * eval_parameters
    * code:1783895142

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1783895142-6c7964bfd4-2g2jp: 0 0
* bexhoma-pool-pgbouncer-1-1783895142-6c7964bfd4-gmznv: 0 0
* bexhoma-pool-pgbouncer-1-1783895142-6c7964bfd4-wvvrq: 0 0
* bexhoma-pool-pgbouncer-1-1783895142-6c7964bfd4-z8p9d: 0 0
* bexhoma-sut-pgbouncer-1-1783895142-9b64d588-9bvbk: 0 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PGBouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3136.62 |               318815.00 |           1000000.00 |                              1969.00 | 16.00 |              180.67 |
| PGBouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3127.47 |               319747.00 |           1000000.00 |                              1892.00 | 16.00 |              180.14 |
| PGBouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3140.04 |               318467.00 |           1000000.00 |                              2183.00 | 16.00 |              180.87 |
| PGBouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3234.82 |               309136.00 |           1000000.00 |                              1937.00 | 16.00 |              186.33 |
| PGBouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3144.30 |               318036.00 |           1000000.00 |                              2447.00 | 16.00 |              181.11 |
| PGBouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3203.07 |               312200.00 |           1000000.00 |                              2327.00 | 16.00 |              184.50 |
| PGBouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3108.66 |               321682.00 |           1000000.00 |                              2157.00 | 16.00 |              179.06 |
| PGBouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3650.26 |               273953.00 |           1000000.00 |                              2103.00 | 16.00 |              210.26 |
| PGBouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3584.26 |               278998.00 |           1000000.00 |                              1971.00 | 16.00 |              206.45 |
| PGBouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3330.23 |               300280.00 |           1000000.00 |                              1945.00 | 16.00 |              191.82 |
| PGBouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3145.75 |               317889.00 |           1000000.00 |                              2031.00 | 16.00 |              181.20 |
| PGBouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3534.57 |               282920.00 |           1000000.00 |                              2279.00 | 16.00 |              203.59 |
| PGBouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3323.05 |               300928.00 |           1000000.00 |                              2335.00 | 16.00 |              191.41 |
| PGBouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3174.60 |               315000.00 |           1000000.00 |                              2165.00 | 16.00 |              182.86 |
| PGBouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3138.89 |               318584.00 |           1000000.00 |                              2143.00 | 16.00 |              180.80 |
| PGBouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3603.60 |               277500.00 |           1000000.00 |                              2101.00 | 16.00 |              207.57 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |         0.00 | 16.00 |              179.06 |                        52580.20 |               321682.00 |          16000000.00 |                              2124.06 |

### Execution

#### Per Connection

| DBMS                 | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1-1  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       1 |         8 |    11264 |          16 |            0 |                         3234.30 |               309186.00 |            1000000 |                            2755.00 |
| PGBouncer-1-1-1-1-2  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       2 |         8 |    11264 |          16 |            0 |                         3239.39 |               308700.00 |            1000000 |                            2789.00 |
| PGBouncer-1-1-1-1-3  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       3 |         8 |    11264 |          16 |            0 |                         3238.58 |               308777.00 |            1000000 |                            2829.00 |
| PGBouncer-1-1-1-1-4  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       4 |         8 |    11264 |          16 |            0 |                         3240.76 |               308570.00 |            1000000 |                            2713.00 |
| PGBouncer-1-1-1-1-5  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       5 |         8 |    11264 |          16 |            0 |                         3235.26 |               309094.00 |            1000000 |                            2819.00 |
| PGBouncer-1-1-1-1-6  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       6 |         8 |    11264 |          16 |            0 |                         3276.39 |               305214.00 |            1000000 |                            2647.00 |
| PGBouncer-1-1-1-1-7  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       7 |         8 |    11264 |          16 |            0 |                         3231.05 |               309497.00 |            1000000 |                            2807.00 |
| PGBouncer-1-1-1-1-8  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       8 |         8 |    11264 |          16 |            0 |                         3248.01 |               307881.00 |            1000000 |                            2691.00 |
| PGBouncer-1-1-1-1-9  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       9 |         8 |    11264 |          16 |            0 |                         3255.82 |               307142.00 |            1000000 |                            2739.00 |
| PGBouncer-1-1-1-1-10 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      10 |         8 |    11264 |          16 |            0 |                         4336.85 |               230582.00 |            1000000 |                            2303.00 |
| PGBouncer-1-1-1-1-11 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      11 |         8 |    11264 |          16 |            0 |                         3300.35 |               302998.00 |            1000000 |                            2643.00 |
| PGBouncer-1-1-1-1-12 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      12 |         8 |    11264 |          16 |            0 |                         3236.37 |               308988.00 |            1000000 |                            2751.00 |
| PGBouncer-1-1-1-1-13 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      13 |         8 |    11264 |          16 |            0 |                         3290.21 |               303932.00 |            1000000 |                            2631.00 |
| PGBouncer-1-1-1-1-14 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      14 |         8 |    11264 |          16 |            0 |                         3241.52 |               308497.00 |            1000000 |                            2731.00 |
| PGBouncer-1-1-1-1-15 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      15 |         8 |    11264 |          16 |            0 |                         3250.44 |               307651.00 |            1000000 |                            2725.00 |
| PGBouncer-1-1-1-1-16 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      16 |         8 |    11264 |          16 |            0 |                         3242.00 |               308452.00 |            1000000 |                            2751.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PGBouncer-1-1-1 | PGBouncer-1-1-1 |                1 |       128 |   180224 |               1 |          16 |            0 |                        53097.30 |               309497.00 |           16000000 |                            2829.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         1.42 |      0.01 |           0.08 |                  0.08 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1403.46 |      6.51 |          23.91 |                 42.17 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1352.86 |      7.56 |           0.11 |                  0.11 |

### Execution phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         0.91 |      0.01 |           0.08 |                  0.08 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |       965.82 |      4.77 |          26.76 |                 45.03 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1188.78 |      6.15 |           0.10 |                  0.11 |

### Application Metrics

#### Loading phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Waiting Clients [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Load Pressure [%] |
|:------------------|-----------------------------------------:|--------------------------------:|--------------------------------------:|-------------------------------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1 |                                 53474.10 |                            0.28 |                                  0.00 |                                     157.00 |                             100.00 |

#### Loading phase: SUT deployment

| DBMS              |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PGBouncer-1-1-1-1 |                    257.00 |                                     0.00 |                                             0.00 |                       32.00 |                                   32.00 |

#### Execution phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Waiting Clients [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Load Pressure [%] |
|:------------------|-----------------------------------------:|--------------------------------:|--------------------------------------:|-------------------------------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1 |                                 57082.92 |                            0.11 |                                  0.00 |                                      56.00 |                             100.00 |

#### Execution phase: SUT deployment

| DBMS              |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PGBouncer-1-1-1-1 |                    257.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms PGBouncer \
  -sf 16 \
  -xsd 10 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 32 \
  -xnpp 2 \
  -xnpi 32 \
  -xnpo 32 \
  -xconn \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  run &>$LOG_DIR/docs_benchbase_pgbouncer_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_pgbouncer_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_pgbouncer_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1760s 
* Code: 1783896325
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [32] threads, split into [1, 2] pods.
  * Pooling is done with [2] pods having [32] inbound and [32] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PGBouncer-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1091129
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * pool 0
    * node:cl-worker25
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker28
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * eval_parameters
    * code:1783896325
* PGBouncer-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1091414
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * pool 0
    * node:cl-worker25
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker28
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * eval_parameters
    * code:1783896325

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1783896325-5f88b97b5c-p7mrw: 0 0
* bexhoma-pool-pgbouncer-1-1783896325-5f88b97b5c-xc9cz: 0 0
* bexhoma-sut-pgbouncer-1-1783896325-56bf9dc46f-tsxhm: 0 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PGBouncer-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PGBouncer-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|               |   experiment_run |    SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:--------------|-----------------:|------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PGBouncer-1-1 |                1 | 16.00 |      336.00 |           1.00 |            0.00 |        148.00 |          187.00 |              1 |           1 |             | None           |             0 | False         |              171.43 |

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------|:----------------|:------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PGBouncer-1-1-1-1-1 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 |                1 |          32 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            2 |                        1350.97 |                      463.77 |         0.00 |                                                      48407.00 |                                              23681.00 |
| PGBouncer-1-1-2-1-1 | PGBouncer-1-1-2 | PGBouncer-1-1-2-1 |                1 |          16 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            1 |                         568.26 |                      442.12 |         0.00 |                                                      60777.00 |                                              28149.00 |
| PGBouncer-1-1-2-1-2 | PGBouncer-1-1-2 | PGBouncer-1-1-2-1 |                1 |          16 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            2 |                         573.52 |                      441.96 |         0.00 |                                                      60695.00 |                                              27891.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PGBouncer-1-1-1 | PGBouncer-1-1-1 |                1 |          32 |    16384 |               1 |           1 |          -1 | 600.00 |            2 |                        1350.97 |                      463.77 |         0.00 |                                                      48407.00 |                                              23681.00 |
| PGBouncer-1-1-2 | PGBouncer-1-1-2 |                1 |          32 |    16384 |               1 |           2 |          -1 | 600.00 |            3 |                        1141.78 |                      884.08 |         0.00 |                                                      60777.00 |                                              28020.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         0.52 |      0.00 |           0.04 |                  0.04 |
| PGBouncer-1-1-2-1 |         0.52 |      0.00 |           0.04 |                  0.04 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |       188.91 |      2.62 |           4.71 |                  6.35 |
| PGBouncer-1-1-2-1 |       188.91 |      2.62 |           4.71 |                  6.35 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1907.89 |     15.32 |           0.25 |                  0.25 |
| PGBouncer-1-1-2-1 |      1907.89 |     15.32 |           0.25 |                  0.25 |

### Execution phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         1.61 |      0.00 |           0.05 |                  0.05 |
| PGBouncer-1-1-2-1 |         1.71 |      0.00 |           0.05 |                  0.05 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |       832.83 |      3.13 |           5.08 |                  6.97 |
| PGBouncer-1-1-2-1 |      1529.59 |      3.68 |           5.58 |                  7.91 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |     11840.07 |     30.18 |           0.47 |                  0.47 |
| PGBouncer-1-1-2-1 |     11840.07 |     39.09 |           0.47 |                  0.47 |

### Application Metrics

#### Loading phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Waiting Clients [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Load Pressure [%] |
|:------------------|-----------------------------------------:|--------------------------------:|--------------------------------------:|-------------------------------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1 |                                   223.21 |                            0.16 |                                  0.00 |                                      48.00 |                             100.00 |
| PGBouncer-1-1-2-1 |                                   223.21 |                            0.16 |                                  0.00 |                                      48.00 |                             100.00 |

#### Loading phase: SUT deployment

| DBMS              |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PGBouncer-1-1-1-1 |                     64.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |
| PGBouncer-1-1-2-1 |                     64.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |

#### Execution phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Waiting Clients [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Load Pressure [%] |
|:------------------|-----------------------------------------:|--------------------------------:|--------------------------------------:|-------------------------------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1 |                                  9627.75 |                            0.50 |                                  0.00 |                                      63.00 |                             100.00 |
| PGBouncer-1-1-2-1 |                                 18545.54 |                            0.15 |                                  0.00 |                                      64.00 |                             100.00 |

#### Execution phase: SUT deployment

| DBMS              |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PGBouncer-1-1-1-1 |                     65.00 |                                    27.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PGBouncer-1-1-2-1 |                     65.00 |                                    28.00 |                                             0.00 |                        9.00 |                                    9.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>




## YugabyteDB

Make sure to have YugabyteDB installed [externally](https://bexhoma.readthedocs.io/en/latest/Example-YugaByteDB.html), because bexhoma does not manage it.

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 950s 
* Code: 1773432301
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1294649
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773432301

### Loading

| DBMS                  |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-64-8-65536 |                1 |        64 |    65536 |           8 |            0 |                         19489.3 |                   52544 |                1e+06 |                                 8961 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-64-8-65536-1 |                1 |        64 |    65536 |           1 |            0 |                         34422.5 |                  290508 |        5.00119e+06 |                               7643 |          4.99881e+06 |                                43583 |

### Workflow

#### Actual

* DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned

* DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |      1234.82 |     13.47 |            5.6 |                  13.6 |

### Loading phase: component yb-master

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |         6.87 |      0.04 |           0.24 |                  0.26 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |        38.93 |         0 |           0.11 |                  0.11 |

### Execution phase: component yb-tserver

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |      10378.5 |     39.73 |           9.51 |                 20.76 |

### Execution phase: component yb-master

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |        10.69 |      0.06 |           0.26 |                  0.29 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |       319.68 |      1.25 |           0.14 |                  0.14 |

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS                    |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:------------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-64-8-65536-1 |                         3754.31 |                       0.42 |                        7.06 |                         0 |                         617 |

#### Loading phase: component yb-master

| DBMS                    |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:------------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-64-8-65536-1 |                               0.02 |                             0.54 |                                   0 |               5.017e+08 |                               0.02 |

#### Execution phase: component yb-tserver

| DBMS                    |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:------------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-64-8-65536-1 |                         31676.4 |                       0.67 |                        2.47 |                         0 |                         585 |

#### Execution phase: component yb-master

| DBMS                    |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:------------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-64-8-65536-1 |                               0.01 |                             0.52 |                                   0 |             5.01948e+08 |                               0.01 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/docs_benchbase_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1265s 
* Code: 1773430865
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1262462
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773430865
* YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1263692
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773430865

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| YugabyteDB-1-1-1024-1-1 |                1 |          16 |    16384 |        1 |       1 |    300 |            0 |                        475.947 |                     473.847 |            0 |                                                         81863 |                                                 33609 |
| YugabyteDB-1-1-1024-2-1 |                1 |           8 |     8192 |        2 |       1 |    300 |            0 |                        225.253 |                     224.247 |            0 |                                                         94011 |                                                 35505 |
| YugabyteDB-1-1-1024-2-2 |                1 |           8 |     8192 |        2 |       2 |    300 |            0 |                        214.683 |                     213.59  |            0 |                                                         97092 |                                                 37254 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| YugabyteDB-1-1-1024-1 |                1 |          16 |    16384 |           1 |    300 |            0 |                         475.95 |                      473.85 |            0 |                                                         81863 |                                               33609   |
| YugabyteDB-1-1-1024-2 |                1 |          16 |    16384 |           2 |    300 |            0 |                         439.94 |                      437.84 |            0 |                                                         97092 |                                               36379.5 |

### Workflow

#### Actual

* DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

#### Planned

* DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| YugabyteDB-1-1-1024-1 |         102 |           1 |      1 |             564.706 |
| YugabyteDB-1-1-1024-2 |         102 |           1 |      2 |             564.706 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |      2010.86 |     22.68 |           7.39 |                 16.15 |
| YugabyteDB-1-1-1024-2 |      2508.42 |     22.68 |           7.39 |                 16.15 |

### Loading phase: component yb-master

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        17.84 |      0.21 |           0.34 |                  0.38 |
| YugabyteDB-1-1-1024-2 |        24.18 |      0.21 |           0.36 |                  0.4  |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        75.68 |         0 |           0.25 |                  0.26 |
| YugabyteDB-1-1-1024-2 |        75.68 |         0 |           0.25 |                  0.26 |

### Execution phase: component yb-tserver

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |     10821.6  |     39.06 |          10.15 |                 20.45 |
| YugabyteDB-1-1-1024-2 |      9532.47 |     36.81 |          11.15 |                 22.77 |

### Execution phase: component yb-master

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        13.01 |      0.07 |           0.39 |                  0.43 |
| YugabyteDB-1-1-1024-2 |        17.1  |      0.08 |           0.45 |                  0.49 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |       102.58 |      0.52 |            0.3 |                   0.3 |
| YugabyteDB-1-1-1024-2 |        92.67 |      0.98 |            0.3 |                   0.3 |

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS                  |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:----------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-1-1-1024-1 |                          243.83 |                       0.44 |                       26.87 |                         0 |                         856 |
| YugabyteDB-1-1-1024-2 |                         3048.64 |                       0.44 |                       26.87 |                         0 |                         856 |

#### Loading phase: component yb-master

| DBMS                  |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:----------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-1-1-1024-1 |                               3.05 |                            22.47 |                                0.04 |             5.00068e+08 |                               3.01 |
| YugabyteDB-1-1-1024-2 |                               3.05 |                            22.47 |                                0.04 |             5.00234e+08 |                               3.01 |

#### Execution phase: component yb-tserver

| DBMS                  |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:----------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-1-1-1024-1 |                        16629.5  |                       0.28 |                       11.22 |                         0 |                         599 |
| YugabyteDB-1-1-1024-2 |                         7310.32 |                       0.31 |                        1.19 |                         0 |                         612 |

#### Execution phase: component yb-master

| DBMS                  |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:----------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-1-1-1024-1 |                               3.02 |                             0.44 |                                0.03 |             5.00262e+08 |                               2.99 |
| YugabyteDB-1-1-1024-2 |                               1.11 |                             0.32 |                                0    |             5.01112e+08 |                               1.11 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

</details>
