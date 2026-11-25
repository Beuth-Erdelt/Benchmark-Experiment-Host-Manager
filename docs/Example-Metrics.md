# Example: Application Metrics

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This page shows how to collect application metrics, that is, metrics of a DBMS.


## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
BEXHOMA_NODES_WORKER="cl-worker36+cl-worker37+cl-worker29"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

The experiment is run with the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

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
* shows a summary

### Evaluate Results


<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 984s 
* Code: 1795121760
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.0.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:816122
  * datadisk:4307
  * volume_size:1.8T
  * volume_used:797G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795121760
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826476
  * datadisk:20429
  * volume_size:1.8T
  * volume_used:808G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795121760
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795121760-bbbc89d6c-fxshv: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |      103.00 |           2.00 |            0.00 |         92.00 |            9.00 |              1 |         1 |             |                |             0 | False         |              559.22 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |    16384 |           0 | 300.00 |       74 |                       16200.99 |                    16003.92 |         0.00 |                                                      19568.00 |                                               6244.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |        80 |     8192 |           0 | 300.00 |       24 |                        5361.47 |                     5305.58 |         0.00 |                                                      34346.00 |                                              14859.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |        80 |     8192 |           0 | 300.00 |       22 |                        5365.60 |                     5309.63 |         0.00 |                                                      34358.00 |                                              14863.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |       160 |    16384 |           0 | 300.00 |       74 |                       16200.99 |                    16003.92 |         0.00 |                                                      19568.00 |                                               6244.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |       160 |    16384 |           0 | 300.00 |       46 |                       10727.07 |                    10615.20 |         0.00 |                                                      34358.00 |                                              14861.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       171.75 |      4.34 |           2.05 |                  3.68 |
| postgresql-1-1-2-1 |       171.75 |      4.34 |           2.05 |                  3.68 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1067.08 |     15.37 |           0.25 |                  0.26 |
| postgresql-1-1-2-1 |      1067.08 |     15.37 |           0.25 |                  0.26 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      5087.73 |     19.71 |           8.52 |                 14.23 |
| postgresql-1-1-2-1 |      4450.49 |     19.08 |          12.06 |                 16.00 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2956.50 |     13.29 |           1.14 |                  1.14 |
| postgresql-1-1-2-1 |      2661.09 |     11.98 |           0.75 |                  0.75 |

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
| postgresql-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                  14.00 |                                              14.00 |
| postgresql-1-1-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                  14.00 |                                              14.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                               122.00 |                                               49.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-1-2-1 |                                 8.00 |                                               51.00 |                                                        0.00 |                                 160.00 |                                             160.00 |

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
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
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
* Type: hammerdb
* Duration: 1247s 
* Code: 1794765028
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1108875
  * datadisk:3280
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794765028
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1123624
  * datadisk:17865
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794765028

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794765028-798775f6f7-nchcs: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       45.00 |           5.00 |            0.00 |         29.00 |           11.00 |              1 |        16 |             | None           |             0 | False         |             1280.00 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        16 | 283188 | 651266 |         0.00 |          5 |        0 |       2.01 |       2.57 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |  57219 | 131739 |         0.00 |          5 |        0 |       1.96 |       3.12 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |  57201 | 131732 |         0.00 |          5 |        0 |       1.96 |       2.94 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        16 |       2.01 |       2.57 |         0.00 | 283188.00 | 651266.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |        16 |       1.96 |       3.12 |         0.00 |  57210.00 | 131735.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        34.76 |      0.63 |           1.66 |                  2.37 |
| postgresql-1-1-2-1 |        34.76 |      0.63 |           1.66 |                  2.37 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1801.93 |      4.64 |           5.68 |                 10.62 |
| postgresql-1-1-2-1 |      5511.35 |     14.22 |           6.69 |                 12.44 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1184.32 |      2.86 |           0.36 |                  0.36 |
| postgresql-1-1-2-1 |       277.20 |      0.73 |           0.12 |                  0.12 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                  11.00 |                                              11.00 |
| postgresql-1-1-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                  11.00 |                                              11.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                13.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                              16.00 |
| postgresql-1-1-2-1 |                                 8.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                              16.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
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
* Duration: 408s 
* Code: 1794763146
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1113421
  * datadisk:8187
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794763146

### Ingestion
* PostgreSQL-1: 14 of 14 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794763146-895647978-v2l8d: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      112.00 |           5.00 |            1.00 |         57.00 |           46.00 |              2 |         0 |             |                |             0 | False         |               96.43 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               22 |                  22 |         29 |            0.64 |            18011.92 |           8193.10 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |         29 |            0.64 |            18011.92 |           8193.10 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1619.81 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 508.59 |
| Shipping Priority (TPC-H Q3)                        |                1184.51 |
| Order Priority Checking Query (TPC-H Q4)            |                 280.51 |
| Local Supplier Volume (TPC-H Q5)                    |                 554.26 |
| Forecasting Revenue Change (TPC-H Q6)               |                 298.28 |
| Volume Shipping Query (TPC-H Q7)                    |                 712.64 |
| National Market Share (TPC-H Q8)                    |                 385.92 |
| Product Type Profit Measure (TPC-H Q9)              |                2031.69 |
| Returned Item Reporting Query (TPC-H Q10)           |                 859.70 |
| Important Stock Identification (TPC-H Q11)          |                 186.23 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 452.78 |
| Customer Distribution (TPC-H Q13)                   |                1837.30 |
| Promotion Effect Query (TPC-H Q14)                  |                 763.14 |
| Top Supplier Query (TPC-H Q15)                      |                 689.36 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 307.68 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1637.30 |
| Large Volume Customer (TPC-H Q18)                   |                8207.95 |
| Discounted Revenue (TPC-H Q19)                      |                  84.75 |
| Potential Part Promotion (TPC-H Q20)                |                 337.51 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 496.25 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 124.74 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        97.10 |      1.59 |           5.18 |                  9.82 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        32.10 |      0.61 |           0.01 |                  1.34 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      1.49 |           4.93 |                  9.73 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.03 |                  0.03 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   2.00 |                                               2.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 2.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
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
* Duration: 1231s 
* Code: 1794763618
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1119786
  * datadisk:14199
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794763618

### Ingestion
* PostgreSQL-1: 27 of 27 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794763618-6745985b8d-tbdst: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    3 |      226.00 |           4.00 |            0.00 |        143.00 |           75.00 |              2 |         0 |             | None           |             0 | False         |               47.79 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |        697 |            0.66 |            16602.59 |           1534.00 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        697 |            0.66 |            16602.59 |           1534.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 204.26 |
| TPC-DS Q2     |                 482.82 |
| TPC-DS Q3     |                 418.63 |
| TPC-DS Q4     |               14904.90 |
| TPC-DS Q5     |                 759.39 |
| TPC-DS Q6     |              193240.27 |
| TPC-DS Q7     |                 563.98 |
| TPC-DS Q8     |                  99.61 |
| TPC-DS Q9     |                2407.88 |
| TPC-DS Q10    |                1066.98 |
| TPC-DS Q11    |                8862.11 |
| TPC-DS Q12    |                 130.64 |
| TPC-DS Q13    |                1106.92 |
| TPC-DS Q14a+b |                6270.89 |
| TPC-DS Q15    |                 292.78 |
| TPC-DS Q16    |                 408.83 |
| TPC-DS Q17    |                 615.19 |
| TPC-DS Q18    |                 613.23 |
| TPC-DS Q19    |                 382.00 |
| TPC-DS Q20    |                 390.41 |
| TPC-DS Q21    |                 419.45 |
| TPC-DS Q22    |                6614.91 |
| TPC-DS Q23a+b |               11442.77 |
| TPC-DS Q24a+b |                 889.81 |
| TPC-DS Q25    |                 595.73 |
| TPC-DS Q26    |                 443.71 |
| TPC-DS Q27    |                 599.78 |
| TPC-DS Q28    |                1870.83 |
| TPC-DS Q29    |                1046.44 |
| TPC-DS Q30    |               69919.46 |
| TPC-DS Q31    |                3387.36 |
| TPC-DS Q32    |                 227.52 |
| TPC-DS Q33    |                 704.33 |
| TPC-DS Q34    |                  37.68 |
| TPC-DS Q35    |                1233.78 |
| TPC-DS Q36    |                 737.12 |
| TPC-DS Q37    |                 336.38 |
| TPC-DS Q38    |                2011.96 |
| TPC-DS Q39a+b |                5098.04 |
| TPC-DS Q40    |                 242.08 |
| TPC-DS Q41    |                2429.79 |
| TPC-DS Q42    |                 169.88 |
| TPC-DS Q43    |                 343.03 |
| TPC-DS Q44    |                   1.72 |
| TPC-DS Q45    |                 186.82 |
| TPC-DS Q46    |                  62.97 |
| TPC-DS Q47    |                2550.35 |
| TPC-DS Q48    |                1095.05 |
| TPC-DS Q49    |                 662.70 |
| TPC-DS Q50    |                1497.84 |
| TPC-DS Q51    |                2228.49 |
| TPC-DS Q52    |                 163.85 |
| TPC-DS Q53    |                 207.31 |
| TPC-DS Q54    |                  67.60 |
| TPC-DS Q55    |                 162.63 |
| TPC-DS Q56    |                 746.49 |
| TPC-DS Q57    |                2068.87 |
| TPC-DS Q58    |                 749.53 |
| TPC-DS Q59    |                 744.01 |
| TPC-DS Q60    |                 673.32 |
| TPC-DS Q61    |                 105.44 |
| TPC-DS Q62    |                 161.76 |
| TPC-DS Q63    |                 205.50 |
| TPC-DS Q64    |                 909.37 |
| TPC-DS Q65    |                1225.23 |
| TPC-DS Q66    |                 524.81 |
| TPC-DS Q67    |                9353.46 |
| TPC-DS Q68    |                  66.60 |
| TPC-DS Q69    |                 394.17 |
| TPC-DS Q70    |                 709.96 |
| TPC-DS Q71    |                 749.02 |
| TPC-DS Q72    |                2402.23 |
| TPC-DS Q73    |                  38.48 |
| TPC-DS Q74    |                2261.59 |
| TPC-DS Q75    |                3095.95 |
| TPC-DS Q76    |                 294.66 |
| TPC-DS Q77    |                 432.49 |
| TPC-DS Q78    |                2446.48 |
| TPC-DS Q79    |                 254.08 |
| TPC-DS Q80    |                 763.98 |
| TPC-DS Q81    |              276038.96 |
| TPC-DS Q82    |                 459.99 |
| TPC-DS Q83    |                 124.31 |
| TPC-DS Q84    |                  23.93 |
| TPC-DS Q85    |                 299.02 |
| TPC-DS Q86    |                 495.38 |
| TPC-DS Q87    |                2084.33 |
| TPC-DS Q88    |                2554.67 |
| TPC-DS Q89    |                  56.70 |
| TPC-DS Q90    |                 287.34 |
| TPC-DS Q91    |                 148.92 |
| TPC-DS Q92    |                  90.37 |
| TPC-DS Q93    |                 481.61 |
| TPC-DS Q94    |                 323.68 |
| TPC-DS Q95    |                7360.22 |
| TPC-DS Q96    |                 169.96 |
| TPC-DS Q97    |                 825.14 |
| TPC-DS Q98    |                 403.70 |
| TPC-DS Q99    |                 282.84 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       212.67 |      2.26 |           6.31 |                 13.38 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        46.98 |      0.34 |           0.01 |                  2.74 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       876.47 |      2.45 |           7.90 |                 14.98 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        21.87 |      0.07 |           0.30 |                  0.31 |

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
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               6.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 826s 
* Code: 1794762275
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
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
  * Experiment is run once.
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
  * disk:1112320
  * datadisk:7091
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794762275
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1113333
  * datadisk:8103
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794762275
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1113879
  * datadisk:8649
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794762275
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1114312
  * datadisk:9081
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794762275

### Ingestion
* PostgreSQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794762275-7c57684cff-tjf89: 0

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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8148.45 |                46021.00 |            375000.00 |                               838.00 | 3.00 |              234.68 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8153.24 |                45994.00 |            375000.00 |                               862.00 | 3.00 |              234.81 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8153.59 |                45992.00 |            375000.00 |                               891.00 | 3.00 |              234.82 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8150.05 |                46012.00 |            375000.00 |                               848.00 | 3.00 |              234.72 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8143.85 |                46047.00 |            375000.00 |                               922.00 | 3.00 |              234.54 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8155.72 |                45980.00 |            375000.00 |                               816.00 | 3.00 |              234.88 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8151.82 |                46002.00 |            375000.00 |                               939.00 | 3.00 |              234.77 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8142.62 |                46054.00 |            375000.00 |                               878.00 | 3.00 |              234.51 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 3.00 |              234.51 |                        65199.34 |                46054.00 |           3000000.00 |                               874.25 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32645.60 |                91896.00 |            1499226 |                             601.00 |              1500774 |                              1482.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     4096 |        0 |                         4083.45 |                91834.00 |             186896 |                             592.00 |               188104 |                              1427.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     4096 |        0 |                         4084.83 |                91803.00 |             187750 |                             664.00 |               187250 |                              1473.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       3 |         8 |     4096 |        0 |                         4084.43 |                91812.00 |             187615 |                             607.00 |               187385 |                              1443.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       4 |         8 |     4096 |        0 |                         4083.32 |                91837.00 |             187135 |                             624.00 |               187865 |                              1455.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       5 |         8 |     4096 |        0 |                         4083.45 |                91834.00 |             187657 |                             592.00 |               187343 |                              1401.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       6 |         8 |     4096 |        0 |                         4084.74 |                91805.00 |             187306 |                             553.00 |               187694 |                              1365.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       7 |         8 |     4096 |        0 |                         4084.12 |                91819.00 |             187791 |                             617.00 |               187209 |                              1426.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       8 |         8 |     4096 |        0 |                         4084.39 |                91813.00 |             187405 |                             658.00 |               187595 |                              1487.00 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       1 |        64 |    49152 |        0 |                        48864.71 |                61394.00 |            1499810 |                             605.00 |              1500190 |                              1806.00 |
| postgresql-1-1-4-1-1 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |     6144 |        0 |                         6121.95 |                61255.00 |             187131 |                             524.00 |               187869 |                              1359.00 |
| postgresql-1-1-4-1-2 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |     6144 |        0 |                         6121.75 |                61257.00 |             187362 |                             560.00 |               187638 |                              1408.00 |
| postgresql-1-1-4-1-3 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |     6144 |        0 |                         6121.25 |                61262.00 |             187372 |                             602.00 |               187628 |                              1388.00 |
| postgresql-1-1-4-1-4 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |     6144 |        0 |                         6122.25 |                61252.00 |             188013 |                             511.00 |               186987 |                              1325.00 |
| postgresql-1-1-4-1-5 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |     6144 |        0 |                         6123.55 |                61239.00 |             187936 |                             538.00 |               187064 |                              1355.00 |
| postgresql-1-1-4-1-6 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |     6144 |        0 |                         6121.55 |                61259.00 |             187449 |                             558.00 |               187551 |                              1382.00 |
| postgresql-1-1-4-1-7 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |     6144 |        0 |                         6121.85 |                61256.00 |             187324 |                             580.00 |               187676 |                              1385.00 |
| postgresql-1-1-4-1-8 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |     6144 |        0 |                         6121.85 |                61256.00 |             187729 |                             567.00 |               187271 |                              1387.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32645.60 |                91896.00 |            1499226 |                             601.00 |              1500774 |                              1482.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           8 |        64 |    32768 |        0 |                        32672.75 |                91837.00 |            1499555 |                             664.00 |              1500445 |                              1487.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        3 |               1 |           1 |        64 |    49152 |        0 |                        48864.71 |                61394.00 |            1499810 |                             605.00 |              1500190 |                              1806.00 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        4 |               1 |           8 |        64 |    49152 |        0 |                        48975.99 |                61262.00 |            1500316 |                             602.00 |              1499684 |                              1408.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       160.87 |      3.13 |           3.95 |                  7.40 |
| postgresql-1-1-2-1 |       160.87 |      3.13 |           3.95 |                  7.40 |
| postgresql-1-1-3-1 |       160.87 |      3.13 |           3.95 |                  7.40 |
| postgresql-1-1-4-1 |       160.87 |      3.13 |           3.95 |                  7.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        95.11 |      0.00 |           0.29 |                  0.29 |
| postgresql-1-1-2-1 |        95.11 |      0.00 |           0.29 |                  0.29 |
| postgresql-1-1-3-1 |        95.11 |      0.00 |           0.29 |                  0.29 |
| postgresql-1-1-4-1 |        95.11 |      0.00 |           0.29 |                  0.29 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       215.55 |      2.37 |           5.08 |                  9.01 |
| postgresql-1-1-2-1 |       191.45 |      2.35 |           5.16 |                  9.17 |
| postgresql-1-1-3-1 |       169.20 |      3.61 |           5.20 |                  9.24 |
| postgresql-1-1-4-1 |       125.92 |      3.25 |           5.21 |                  9.25 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       157.02 |      2.65 |           0.57 |                  0.57 |
| postgresql-1-1-2-1 |       217.50 |      3.62 |           0.10 |                  0.11 |
| postgresql-1-1-3-1 |       186.42 |      4.10 |           0.56 |                  0.57 |
| postgresql-1-1-4-1 |       154.44 |      5.04 |           0.10 |                  0.11 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
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
| postgresql-1-1-1-1 |                                61.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |
| postgresql-1-1-2-1 |                                61.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |
| postgresql-1-1-3-1 |                                61.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |
| postgresql-1-1-4-1 |                                61.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                60.00 |                                                0.00 |                                                        0.00 |                                  11.00 |                                              11.00 |
| postgresql-1-1-2-1 |                                58.00 |                                                0.00 |                                                        0.00 |                                  17.00 |                                              17.00 |
| postgresql-1-1-3-1 |                                56.00 |                                                0.00 |                                                        0.00 |                                  23.00 |                                              23.00 |
| postgresql-1-1-4-1 |                                57.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |

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
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
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
* shows a summary


### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_mysql_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_mysql_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1162s 
* Code: 1794766315
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1088756
  * datadisk:34681
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794766315
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1094072
  * datadisk:38156
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794766315
    * TENANT_VOL:False

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794766315-57d9f6c6cd-tw2xx: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       80.00 |           4.00 |            0.00 |         72.00 |            4.00 |              1 |         1 |             |                |             0 | False         |              720.00 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |    16384 |          -1 | 300.00 |        0 |                       16357.60 |                    16137.62 |         0.00 |                                                      12331.00 |                                               5947.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        80 |     8192 |          -1 | 300.00 |        0 |                        8025.09 |                     7901.03 |         0.00 |                                                      16876.00 |                                               7805.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        80 |     8192 |          -1 | 300.00 |        0 |                        8038.46 |                     7913.05 |         0.00 |                                                      16931.00 |                                               7793.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |       160 |    16384 |          -1 | 300.00 |        0 |                       16357.60 |                    16137.62 |         0.00 |                                                      12331.00 |                                               5947.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |       160 |    16384 |          -1 | 300.00 |        0 |                       16063.55 |                    15814.08 |         0.00 |                                                      16931.00 |                                               7799.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        98.70 |      1.92 |           2.89 |                  4.95 |
| mysql-1-1-2-1 |        98.70 |      1.92 |           2.89 |                  4.95 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       829.92 |     15.10 |           0.56 |                  0.56 |
| mysql-1-1-2-1 |       829.92 |     15.10 |           0.56 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      8414.75 |     28.92 |           6.54 |                 16.00 |
| mysql-1-1-2-1 |      8384.49 |     30.15 |           9.52 |                 16.00 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      4754.03 |     16.21 |           2.23 |                  2.23 |
| mysql-1-1-2-1 |      5405.63 |     26.61 |           1.64 |                  1.64 |

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
| mysql-1-1-1-1 |                                  1.00 |                           474.74 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                           474.74 |                            0.01 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                        398923.38 |                            0.11 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                        392014.76 |                            0.11 |                            0.00 |                              0.00 |

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
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
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
* Type: hammerdb
* Duration: 1384s 
* Code: 1794772016
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1087704
  * datadisk:34413
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794772016
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091920
  * datadisk:35259
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794772016

### Ingestion
* MySQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794772016-54c8468d8-gcfkb: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       46.00 |           4.00 |            0.00 |         39.00 |            3.00 |              1 |        16 |             | None           |             0 | False         |             1252.17 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |  95504 | 222054 |         0.00 |          5 |        0 |       6.89 |       8.57 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 | 111783 | 260127 |         0.00 |          5 |        0 |       5.55 |       6.70 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 | 111783 | 260151 |         0.00 |          5 |        0 |       5.70 |       6.88 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        16 |       6.89 |       8.57 |         0.00 |  95504.00 | 222054.00 |          5 |        0 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |        16 |       5.70 |       6.88 |         0.00 | 111783.00 | 260139.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        89.77 |      3.19 |           5.63 |                  7.41 |
| mysql-1-1-2-1 |        89.77 |      3.19 |           5.63 |                  7.41 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       255.93 |      0.00 |           0.17 |                  0.18 |
| mysql-1-1-2-1 |       255.93 |      0.00 |           0.17 |                  0.18 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      2134.82 |      5.71 |           5.54 |                 12.02 |
| mysql-1-1-2-1 |      2200.28 |      5.88 |           6.49 |                 18.22 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       701.37 |      2.72 |           0.24 |                  0.24 |
| mysql-1-1-2-1 |      1045.77 |      2.78 |           0.14 |                  0.14 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
| mysql-1-1-1-1 |                                  1.00 |                           529.70 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                           529.70 |                            0.01 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                        586751.57 |                            0.01 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                        621381.48 |                            0.01 |                            0.00 |                              0.00 |

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
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
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
* Duration: 751s 
* Code: 1794768592
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091598
  * datadisk:38476
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794768592

### Ingestion
* MySQL-1: 14 of 14 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794768592-878fbc786-8kdvz: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      181.00 |           4.00 |            1.00 |         94.00 |           80.00 |              2 |         0 |             | None           |             0 | False         |               59.67 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               22 |                  22 |        142 |            2.53 |             4427.58 |           1673.24 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  22 |        142 |            2.53 |             4427.58 |           1673.24 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          18524.52 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            269.03 |
| Shipping Priority (TPC-H Q3)                        |           4241.21 |
| Order Priority Checking Query (TPC-H Q4)            |           1083.84 |
| Local Supplier Volume (TPC-H Q5)                    |           2557.36 |
| Forecasting Revenue Change (TPC-H Q6)               |           2376.25 |
| Volume Shipping Query (TPC-H Q7)                    |           1723.33 |
| National Market Share (TPC-H Q8)                    |           6532.22 |
| Product Type Profit Measure (TPC-H Q9)              |          11637.90 |
| Returned Item Reporting Query (TPC-H Q10)           |           2927.37 |
| Important Stock Identification (TPC-H Q11)          |            406.91 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           3761.68 |
| Customer Distribution (TPC-H Q13)                   |          13517.78 |
| Promotion Effect Query (TPC-H Q14)                  |           3243.29 |
| Top Supplier Query (TPC-H Q15)                      |          42142.90 |
| Parts/Supplier Relationship (TPC-H Q16)             |            795.15 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            708.66 |
| Large Volume Customer (TPC-H Q18)                   |           3805.32 |
| Discounted Revenue (TPC-H Q19)                      |            353.32 |
| Potential Part Promotion (TPC-H Q20)                |           1012.17 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          10783.66 |
| Global Sales Opportunity Query (TPC-H Q22)          |            265.00 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       221.64 |      1.93 |           7.98 |                 13.45 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         7.77 |      0.07 |           0.01 |                  1.35 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       105.20 |      0.93 |           8.38 |                 13.86 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        19.28 |      0.11 |           0.40 |                  0.41 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             0.94 |                            0.00 |                            0.02 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.65 |                            0.00 |                            0.03 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
  -lr 128Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 128Gi \
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
* Duration: 2439s 
* Code: 1794769408
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1098052
  * datadisk:44923
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794769408

### Ingestion
* MySQL-1: 27 of 27 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794769408-9b56b88c-fhjl6: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      520.00 |           4.00 |            0.00 |        185.00 |          328.00 |              2 |         0 |             | None           |             0 | False         |               20.77 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |       1415 |            2.28 |             4784.27 |            755.62 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1415 |            2.28 |             4784.27 |            755.62 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             54.47 |
| TPC-DS Q2     |          11823.50 |
| TPC-DS Q3     |             15.29 |
| TPC-DS Q4     |         156371.19 |
| TPC-DS Q5     |          35440.01 |
| TPC-DS Q6     |           3576.51 |
| TPC-DS Q7     |           4413.54 |
| TPC-DS Q8     |           1007.10 |
| TPC-DS Q9     |          12024.82 |
| TPC-DS Q10    |            961.65 |
| TPC-DS Q11    |          99914.47 |
| TPC-DS Q12    |            702.29 |
| TPC-DS Q13    |           6877.03 |
| TPC-DS Q14a+b |         131248.32 |
| TPC-DS Q15    |            415.81 |
| TPC-DS Q16    |            861.80 |
| TPC-DS Q17    |           1037.96 |
| TPC-DS Q18    |           2995.38 |
| TPC-DS Q19    |            926.74 |
| TPC-DS Q20    |           1177.30 |
| TPC-DS Q21    |          58446.45 |
| TPC-DS Q22    |          16130.05 |
| TPC-DS Q23a+b |         140801.97 |
| TPC-DS Q24a+b |           3980.00 |
| TPC-DS Q25    |            665.65 |
| TPC-DS Q26    |            926.55 |
| TPC-DS Q27    |           1066.65 |
| TPC-DS Q28    |          12507.65 |
| TPC-DS Q29    |            231.26 |
| TPC-DS Q30    |           5752.73 |
| TPC-DS Q31    |          56977.59 |
| TPC-DS Q32    |           1627.36 |
| TPC-DS Q33    |           2388.32 |
| TPC-DS Q34    |           4834.56 |
| TPC-DS Q35    |          80858.72 |
| TPC-DS Q36    |          22921.19 |
| TPC-DS Q37    |             19.16 |
| TPC-DS Q38    |          33890.66 |
| TPC-DS Q39a+b |           8333.52 |
| TPC-DS Q40    |            942.09 |
| TPC-DS Q41    |           5393.96 |
| TPC-DS Q42    |             41.55 |
| TPC-DS Q43    |              2.41 |
| TPC-DS Q44    |              7.04 |
| TPC-DS Q45    |            300.90 |
| TPC-DS Q46    |           3037.51 |
| TPC-DS Q47    |          25958.29 |
| TPC-DS Q48    |           2175.40 |
| TPC-DS Q49    |            345.77 |
| TPC-DS Q50    |             90.56 |
| TPC-DS Q51    |          22274.15 |
| TPC-DS Q52    |             39.99 |
| TPC-DS Q53    |            525.15 |
| TPC-DS Q54    |           7343.36 |
| TPC-DS Q55    |             21.65 |
| TPC-DS Q56    |            595.27 |
| TPC-DS Q57    |          13516.48 |
| TPC-DS Q58    |          14747.98 |
| TPC-DS Q59    |          14724.97 |
| TPC-DS Q60    |           1455.58 |
| TPC-DS Q61    |            760.63 |
| TPC-DS Q62    |           7477.20 |
| TPC-DS Q63    |            543.87 |
| TPC-DS Q64    |           1162.78 |
| TPC-DS Q65    |          19761.05 |
| TPC-DS Q66    |           6027.70 |
| TPC-DS Q67    |          22315.01 |
| TPC-DS Q68    |            683.12 |
| TPC-DS Q69    |           1189.15 |
| TPC-DS Q70    |          32427.88 |
| TPC-DS Q71    |           1106.52 |
| TPC-DS Q72    |          34091.77 |
| TPC-DS Q73    |           3110.61 |
| TPC-DS Q74    |          25198.20 |
| TPC-DS Q75    |           5463.74 |
| TPC-DS Q76    |           1287.07 |
| TPC-DS Q77    |          23147.49 |
| TPC-DS Q78    |          44131.20 |
| TPC-DS Q79    |           2436.45 |
| TPC-DS Q80    |          13690.75 |
| TPC-DS Q81    |          20595.92 |
| TPC-DS Q82    |             31.49 |
| TPC-DS Q83    |           1680.07 |
| TPC-DS Q84    |            130.18 |
| TPC-DS Q85    |            288.25 |
| TPC-DS Q86    |           2836.99 |
| TPC-DS Q87    |          21827.66 |
| TPC-DS Q88    |           7991.45 |
| TPC-DS Q89    |            681.67 |
| TPC-DS Q90    |            973.24 |
| TPC-DS Q91    |             43.31 |
| TPC-DS Q92    |             45.49 |
| TPC-DS Q93    |             99.74 |
| TPC-DS Q94    |           1091.75 |
| TPC-DS Q95    |           9251.35 |
| TPC-DS Q96    |            438.92 |
| TPC-DS Q97    |          21013.07 |
| TPC-DS Q98    |           2624.17 |
| TPC-DS Q99    |          16792.24 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       628.71 |      3.06 |           9.92 |                 16.95 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |         9.22 |      0.15 |           0.01 |                  2.43 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1346.40 |      1.02 |          13.84 |                 20.87 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        26.70 |      0.50 |           0.36 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.20 |                            0.00 |                            0.02 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                             1.59 |                            0.00 |                            0.04 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* Duration: 1031s 
* Code: 1794767516
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091500
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091501
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091502
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091504
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516

### Ingestion
* MySQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794767516-676b47d8b7-tx4nd: 0

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

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7919.91 |                47349.00 |            375000.00 |                              7763.00 | 3.00 |              228.09 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7949.46 |                47173.00 |            375000.00 |                              7631.00 | 3.00 |              228.94 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7998.29 |                46885.00 |            375000.00 |                              8147.00 | 3.00 |              230.35 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7961.45 |                47102.00 |            375000.00 |                              7739.00 | 3.00 |              229.29 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7965.50 |                47078.00 |            375000.00 |                              7803.00 | 3.00 |              229.41 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7960.43 |                47108.00 |            375000.00 |                              7751.00 | 3.00 |              229.26 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7977.70 |                47006.00 |            375000.00 |                              7671.00 | 3.00 |              229.76 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7979.91 |                46993.00 |            375000.00 |                              7747.00 | 3.00 |              229.82 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 3.00 |              228.09 |                        63712.67 |                47349.00 |           3000000.00 |                              7781.50 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32109.26 |                93431.00 |            1500261 |                             725.00 |              1499739 |                              4223.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     4096 |        0 |                         4038.51 |                92856.00 |             187467 |                             795.00 |               187533 |                              4435.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     4096 |        0 |                         4034.90 |                92939.00 |             187710 |                             884.00 |               187290 |                              4467.00 |
| mysql-1-1-2-1-3 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       3 |         8 |     4096 |        0 |                         4038.51 |                92856.00 |             188040 |                             817.00 |               186960 |                              4435.00 |
| mysql-1-1-2-1-4 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       4 |         8 |     4096 |        0 |                         4039.69 |                92829.00 |             187682 |                             778.00 |               187318 |                              4391.00 |
| mysql-1-1-2-1-5 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       5 |         8 |     4096 |        0 |                         4053.62 |                92510.00 |             187428 |                             774.00 |               187572 |                              4427.00 |
| mysql-1-1-2-1-6 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       6 |         8 |     4096 |        0 |                         4038.69 |                92852.00 |             187551 |                             809.00 |               187449 |                              4455.00 |
| mysql-1-1-2-1-7 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       7 |         8 |     4096 |        0 |                         4046.57 |                92671.00 |             187704 |                             768.00 |               187296 |                              4411.00 |
| mysql-1-1-2-1-8 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       8 |         8 |     4096 |        0 |                         4049.11 |                92613.00 |             187978 |                             794.00 |               187022 |                              4387.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |        64 |    49152 |        0 |                        45293.27 |                66235.00 |            1499362 |                             652.00 |              1500638 |                              4863.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |     6144 |        0 |                         5968.96 |                62825.00 |             187720 |                             738.00 |               187280 |                              4061.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |     6144 |        0 |                         5977.14 |                62739.00 |             187527 |                             804.00 |               187473 |                              4073.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |     6144 |        0 |                         5953.42 |                62989.00 |             187287 |                             803.00 |               187713 |                              4091.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |     6144 |        0 |                         5997.70 |                62524.00 |             187349 |                             838.00 |               187651 |                              4127.00 |
| mysql-1-1-4-1-5 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |     6144 |        0 |                         5995.40 |                62548.00 |             187883 |                             801.00 |               187117 |                              4069.00 |
| mysql-1-1-4-1-6 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |     6144 |        0 |                         5988.02 |                62625.00 |             187154 |                             821.00 |               187846 |                              4119.00 |
| mysql-1-1-4-1-7 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |     6144 |        0 |                         5975.81 |                62753.00 |             187401 |                             771.00 |               187599 |                              4099.00 |
| mysql-1-1-4-1-8 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |     6144 |        0 |                         6004.90 |                62449.00 |             187224 |                             792.00 |               187776 |                              4063.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32109.26 |                93431.00 |            1500261 |                             725.00 |              1499739 |                              4223.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           8 |        64 |    32768 |        0 |                        32339.59 |                92939.00 |            1501560 |                             884.00 |              1498440 |                              4467.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           1 |        64 |    49152 |        0 |                        45293.27 |                66235.00 |            1499362 |                             652.00 |              1500638 |                              4863.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |           8 |        64 |    49152 |        0 |                        47861.35 |                62989.00 |            1499545 |                             838.00 |              1500455 |                              4127.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       483.22 |      9.87 |           8.92 |                 14.62 |
| mysql-1-1-2-1 |       483.22 |      9.87 |           8.92 |                 14.62 |
| mysql-1-1-3-1 |       483.22 |      9.87 |           8.92 |                 14.62 |
| mysql-1-1-4-1 |       483.22 |      9.87 |           8.92 |                 14.62 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       182.14 |      0.00 |           1.04 |                  1.05 |
| mysql-1-1-2-1 |       182.14 |      0.00 |           1.04 |                  1.05 |
| mysql-1-1-3-1 |       182.14 |      0.00 |           1.04 |                  1.05 |
| mysql-1-1-4-1 |       182.14 |      0.00 |           1.04 |                  1.05 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       408.66 |      6.15 |           8.06 |                 14.30 |
| mysql-1-1-2-1 |       421.50 |      6.52 |           8.09 |                 15.09 |
| mysql-1-1-3-1 |       282.09 |      5.22 |           8.12 |                 15.97 |
| mysql-1-1-4-1 |       308.63 |      6.09 |           8.15 |                 16.78 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       297.62 |      6.46 |           0.90 |                  0.90 |
| mysql-1-1-2-1 |       522.89 |      8.82 |           0.32 |                  0.32 |
| mysql-1-1-3-1 |       304.00 |      4.92 |           1.31 |                  1.31 |
| mysql-1-1-4-1 |       346.66 |      6.84 |           0.30 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
| mysql-1-1-1-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                         18544.15 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                         20979.49 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                         22226.56 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                         22519.92 |                            0.04 |                            0.00 |                              0.00 |

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
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1635s 
* Code: 1794773455
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1064695
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1397428
    * datadisk:11687
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1064695
    * datadisk:11538
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:648328
    * datadisk:11467
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794773455
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794773455-6d44767854-kx8rm: 0
* bx-w-cr-1-1794773455-0: 0
* bx-w-cr-1-1794773455-1: 0
* bx-w-cr-1-1794773455-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2217.59 |               563675.00 |           1250000.00 |                             12751.00 | 10.00 |               63.87 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2209.96 |               565620.00 |           1250000.00 |                             12695.00 | 10.00 |               63.65 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2214.21 |               564535.00 |           1250000.00 |                             12663.00 | 10.00 |               63.77 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2210.10 |               565584.00 |           1250000.00 |                             12543.00 | 10.00 |               63.65 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2215.63 |               564173.00 |           1250000.00 |                             12679.00 | 10.00 |               63.81 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2212.89 |               564871.00 |           1250000.00 |                             12759.00 | 10.00 |               63.73 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2215.68 |               564162.00 |           1250000.00 |                             12599.00 | 10.00 |               63.81 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2225.23 |               561740.00 |           1250000.00 |                             12831.00 | 10.00 |               64.09 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |    SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 10.00 |               63.65 |                        17721.30 |               565620.00 |          10000000.00 |                             12690.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        14199.38 |               704256.00 |            4998021 |                            6395.00 |              5001979 |                            122943.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        14199.38 |               704256.00 |            4998021 |                            6395.00 |              5001979 |                            122943.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     23039.75 |     46.78 |          19.66 |                 47.97 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       834.44 |      1.99 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     24347.83 |     37.76 |          23.50 |                 47.95 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       765.50 |      1.33 |           0.34 |                  0.34 |

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
| cockroachdb-1-1-1-1 |                                    66267.31 |             51295992.67 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    38181.27 |             28410188.27 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1230s 
* Code: 1794775134
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1057984
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388334
    * datadisk:2500
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:639026
    * datadisk:2433
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058005
    * datadisk:2296
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794775134
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1055714
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388623
    * datadisk:2786
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:639307
    * datadisk:2712
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1055714
    * datadisk:2573
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794775134
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794775134-7458d645fd-ghjc6: 0
* bx-w-cr-1-1794775134-0: 0
* bx-w-cr-1-1794775134-1: 0
* bx-w-cr-1-1794775134-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      228.00 |           1.00 |            0.00 |        223.00 |            4.00 |              1 |         1 |             | None           |             0 | False         |              252.63 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         435.88 |                      433.91 |         0.00 |                                                      92361.00 |                                              36687.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         193.12 |                      192.29 |         0.00 |                                                     101845.00 |                                              41395.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         188.36 |                      187.49 |         0.00 |                                                     103613.00 |                                              42443.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         435.88 |                      433.91 |         0.00 |                                                      92361.00 |                                              36687.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         381.49 |                      379.78 |         0.00 |                                                     103613.00 |                                              41919.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      3347.01 |     25.29 |           7.98 |                 11.57 |
| cockroachdb-1-1-2-1 |      3347.01 |     25.29 |           7.98 |                 11.57 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       854.40 |     12.16 |           0.27 |                  0.27 |
| cockroachdb-1-1-2-1 |       854.40 |     12.16 |           0.27 |                  0.27 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      7217.51 |     26.23 |           8.61 |                 12.80 |
| cockroachdb-1-1-2-1 |      6606.97 |     23.62 |           8.72 |                 13.67 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       305.37 |      1.31 |           0.32 |                  0.32 |
| cockroachdb-1-1-2-1 |       303.92 |      1.34 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     1235.25 |             12206491.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     1235.25 |             12206491.00 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    24365.21 |             12204661.27 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                    21419.36 |              8707094.30 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>





## Redis

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms Redis \
  -sf 3 \
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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 521s 
* Code: 1794776408
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Redis'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053145
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388002
    * datadisk:2172
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:638916
    * datadisk:2324
    * cpu_list:0-127
  * worker 2
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:300332
    * datadisk:2182
    * cpu_list:0-255
  * worker 3
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:161733
    * datadisk:2156
    * cpu_list:0-95
  * worker 4
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:890622
    * datadisk:2202
    * cpu_list:0-255
  * worker 5
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:223105
    * datadisk:2431
    * cpu_list:0-127
  * resources_total: 24.25 CPU, 96.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 96.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794776408
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794776408-6c4df58d44-6jw5n: 0
* bx-w-rd-1-1794776408-0: 0
* bx-w-rd-1-1794776408-1: 0
* bx-w-rd-1-1794776408-2: 0
* bx-w-rd-1-1794776408-3: 0
* bx-w-rd-1-1794776408-4: 0
* bx-w-rd-1-1794776408-5: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6003.36 |                62465.00 |            375000.00 |                              2739.00 | 3.00 |              172.90 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6025.65 |                62234.00 |            375000.00 |                              2741.00 | 3.00 |              173.54 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6010.58 |                62390.00 |            375000.00 |                              2737.00 | 3.00 |              173.10 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         5998.08 |                62520.00 |            375000.00 |                              2737.00 | 3.00 |              172.74 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6042.44 |                62061.00 |            375000.00 |                              2739.00 | 3.00 |              174.02 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6039.23 |                62094.00 |            375000.00 |                              2745.00 | 3.00 |              173.93 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6010.87 |                62387.00 |            375000.00 |                              2733.00 | 3.00 |              173.11 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6010.67 |                62389.00 |            375000.00 |                              2737.00 | 3.00 |              173.11 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 3.00 |              172.74 |                        48140.88 |                62520.00 |           3000000.00 |                              2738.50 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        52073.03 |               192038.00 |            4999208 |                            1679.00 |              5000792 |                              1666.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        52073.03 |               192038.00 |            4999208 |                            1679.00 |              5000792 |                              1666.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       444.12 |      5.28 |           9.08 |                  9.09 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       219.80 |      7.00 |           0.94 |                  0.94 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       539.91 |      5.03 |          10.30 |                 10.32 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       837.73 |      5.18 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      201.00 |                      8.71 |                       3.00 |                                          17745.79 |

#### Benchmarking phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      393.00 |                      8.71 |                       3.00 |                                          16579.48 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
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
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_tidb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_tidb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_tidb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 516s 
* Code: 1794776970
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1406394
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406394
    * cpu_list:0-127
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:298344
    * cpu_list:0-255
  * sut 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:893414
    * cpu_list:0-255
  * pd 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406394
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1074259
    * datadisk:123
    * cpu_list:0-223
  * pd 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:648911
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406394
    * datadisk:21038
    * cpu_list:0-127
  * tikv 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:648911
    * datadisk:12195
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1074259
    * datadisk:20997
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794776970
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* TiDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-tidb-1-1794776970-7df56497c5-26gvp: 0
* bexhoma-sut-tidb-1-1794776970-7df56497c5-hbm9s: 0
* bexhoma-sut-tidb-1-1794776970-7df56497c5-x64bq: 0
* bx-pd-ti-1-1794776970-0: 0
* bx-pd-ti-1-1794776970-1: 0
* bx-pd-ti-1-1794776970-2: 0
* bx-tikv-ti-1-1794776970-0: 0
* bx-tikv-ti-1-1794776970-1: 0
* bx-tikv-ti-1-1794776970-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| tidb-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1866.81 |                66959.00 |            125000.00 |                             14439.00 | 1.00 |               53.76 |
| tidb-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1883.64 |                66361.00 |            125000.00 |                             13911.00 | 1.00 |               54.25 |
| tidb-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1911.14 |                65406.00 |            125000.00 |                             13103.00 | 1.00 |               55.04 |
| tidb-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1876.03 |                66630.00 |            125000.00 |                             14367.00 | 1.00 |               54.03 |
| tidb-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1911.55 |                65392.00 |            125000.00 |                             14303.00 | 1.00 |               55.05 |
| tidb-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1910.99 |                65411.00 |            125000.00 |                             15383.00 | 1.00 |               55.04 |
| tidb-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1908.86 |                65484.00 |            125000.00 |                             15287.00 | 1.00 |               54.98 |
| tidb-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1908.40 |                65500.00 |            125000.00 |                             13783.00 | 1.00 |               54.96 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |     0.00 | 1.00 |               53.76 |                        15177.42 |                66959.00 |           1000000.00 |                             14322.00 |

### Benchmarking

#### Per Connection

| connection     | phase      | job          |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    16384 |        0 |                        13714.22 |                72917.00 |             500396 |                            3333.00 |               499604 |                            107199.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    16384 |        0 |                        13714.22 |                72917.00 |             500396 |                            3333.00 |               499604 |                            107199.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1030.85 |     14.99 |           2.38 |                  2.96 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        50.38 |      0.60 |           0.22 |                  0.22 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       871.47 |     13.32 |           8.53 |                 17.27 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        97.54 |      2.04 |           0.42 |                  0.43 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       854.49 |     14.31 |           2.55 |                  3.13 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        41.08 |      0.66 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1100.14 |     21.93 |          10.07 |                 23.02 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       106.88 |      1.91 |           1.05 |                  1.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* PD Leader Balance Actions [count] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdbenchmarking.log, expected: series exists only while non-zero)
* PD Leader Balance Actions [count] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration since Start [ms] |
|:-------------|----------------------------------------:|-------------------------------------------:|
| tidb-1-1-1-1 |                                 4381.22 |                                       3.30 |

#### Loading phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [count] |
|:-------------|--------------------------:|------------------------------------:|
| tidb-1-1-1-1 |                     39.00 |                                0.00 |

#### Loading phase: component tikv

| DBMS         |   TiKV Store Size Used [GiB] |   TiKV Store Used [%] |   TiKV Compaction Time Median, Max over Instances [s] |   TiKV Compaction Flow [GiB] |   TiKV Compaction Pending [GiB] |
|:-------------|-----------------------------:|----------------------:|------------------------------------------------------:|-----------------------------:|--------------------------------:|
| tidb-1-1-1-1 |                        50.44 |                  1.15 |                                                  2.31 |                         6.36 |                            0.48 |

#### Benchmarking phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration since Start [ms] |
|:-------------|----------------------------------------:|-------------------------------------------:|
| tidb-1-1-1-1 |                                 6354.28 |                                       3.59 |

#### Benchmarking phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [count] |
|:-------------|--------------------------:|------------------------------------:|
| tidb-1-1-1-1 |                     41.00 |                                0.00 |

#### Benchmarking phase: component tikv

| DBMS         |   TiKV Store Size Used [GiB] |   TiKV Store Used [%] |   TiKV Compaction Time Median, Max over Instances [s] |   TiKV Compaction Flow [GiB] |   TiKV Compaction Pending [GiB] |
|:-------------|-----------------------------:|----------------------:|------------------------------------------------------:|-----------------------------:|--------------------------------:|
| tidb-1-1-1-1 |                        52.42 |                  1.19 |                                                  1.67 |                         1.16 |                            0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
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
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_tidb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_tidb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_tidb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1104s 
* Code: 1794777562
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:893409
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:893409
    * cpu_list:0-255
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:298350
    * cpu_list:0-255
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1410129
    * cpu_list:0-127
  * pd 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1410129
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:652317
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1077768
    * datadisk:123
    * cpu_list:0-223
  * tikv 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1410129
    * datadisk:24567
    * cpu_list:0-127
  * tikv 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:652317
    * datadisk:15606
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1077768
    * datadisk:24497
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794777562
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:893436
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:893436
    * cpu_list:0-255
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:298353
    * cpu_list:0-255
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1408882
    * cpu_list:0-127
  * pd 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1408882
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:651314
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1077456
    * datadisk:123
    * cpu_list:0-223
  * tikv 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1408882
    * datadisk:23318
    * cpu_list:0-127
  * tikv 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:651314
    * datadisk:14606
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1077456
    * datadisk:23088
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794777562
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* TiDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-tidb-1-1794777562-6bfcc9f459-dsb88: 0
* bexhoma-sut-tidb-1-1794777562-6bfcc9f459-hrh5m: 0
* bexhoma-sut-tidb-1-1794777562-6bfcc9f459-lmxsc: 0
* bx-pd-ti-1-1794777562-0: 0
* bx-pd-ti-1-1794777562-1: 0
* bx-pd-ti-1-1794777562-2: 0
* bx-tikv-ti-1-1794777562-0: 0
* bx-tikv-ti-1-1794777562-1: 0
* bx-tikv-ti-1-1794777562-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      173.00 |           2.00 |            0.00 |        169.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              332.95 | False               |

### Benchmarking

#### Per Connection

| connection     | phase      | job          |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         414.12 |                      412.36 |         0.00 |                                                     103844.00 |                                              38622.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         187.13 |                      185.13 |         0.00 |                                                     106050.00 |                                              42610.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         207.98 |                      205.76 |         0.00 |                                                     104627.00 |                                              38446.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         414.12 |                      412.36 |         0.00 |                                                     103844.00 |                                              38622.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         395.10 |                      390.89 |         0.00 |                                                     106050.00 |                                              40528.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1064.09 |      7.45 |           3.25 |                  3.83 |
| tidb-1-1-2-1 |      1064.09 |      7.45 |           3.25 |                  3.83 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        49.42 |      0.29 |           0.21 |                  0.21 |
| tidb-1-1-2-1 |        49.42 |      0.29 |           0.21 |                  0.21 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3023.97 |     24.96 |          12.82 |                 31.57 |
| tidb-1-1-2-1 |      3023.97 |     24.96 |          12.82 |                 31.57 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       247.91 |      3.07 |           0.61 |                  0.63 |
| tidb-1-1-2-1 |       247.91 |      3.07 |           0.61 |                  0.63 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3100.23 |     11.54 |           3.85 |                  4.43 |
| tidb-1-1-2-1 |      2740.20 |     10.08 |           2.70 |                  3.28 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       185.71 |      0.75 |           0.21 |                  0.22 |
| tidb-1-1-2-1 |       185.80 |      0.74 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      4712.50 |     17.79 |          14.79 |                 33.49 |
| tidb-1-1-2-1 |      4503.22 |     16.77 |          16.76 |                 34.55 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       218.83 |      1.21 |           0.34 |                  0.34 |
| tidb-1-1-2-1 |       258.97 |      1.40 |           0.58 |                  0.58 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
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
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
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
* Duration: 736s 
* Code: 1794778724
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
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 16 processes (pods).
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 80Gi.
  * Loading is tested with [64] threads, split into [16] pods.
  * Benchmarking is tested with [128] threads, split into [16] pods.
  * Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* pgbouncer-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091350
  * datadisk:38200
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * pool 0
    * node:cl-worker37
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker29
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 2
    * node:cl-worker39
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 3
    * node:cl-worker27
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794778724

### Ingestion
* PGBouncer-1: 16 of 16 units ok

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-4zfp4: 0
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-7vpnw: 0
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-dp6bp: 0
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-g6jxg: 0
* bexhoma-sut-pgbouncer-1-1794778724-6c797f9857-7d6b7: 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| pgbouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6325.95 |               158079.00 |           1000000.00 |                              1864.00 | 16.00 |              364.37 |
| pgbouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6309.27 |               158497.00 |           1000000.00 |                              2107.00 | 16.00 |              363.41 |
| pgbouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6969.81 |               143476.00 |           1000000.00 |                              2153.00 | 16.00 |              401.46 |
| pgbouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6299.61 |               158740.00 |           1000000.00 |                              2273.00 | 16.00 |              362.86 |
| pgbouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6418.36 |               155803.00 |           1000000.00 |                              1884.00 | 16.00 |              369.70 |
| pgbouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6521.41 |               153341.00 |           1000000.00 |                              1992.00 | 16.00 |              375.63 |
| pgbouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         7406.58 |               135015.00 |           1000000.00 |                              1853.00 | 16.00 |              426.62 |
| pgbouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6480.92 |               154299.00 |           1000000.00 |                              2071.00 | 16.00 |              373.30 |
| pgbouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6365.13 |               157106.00 |           1000000.00 |                              1964.00 | 16.00 |              366.63 |
| pgbouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6364.85 |               157113.00 |           1000000.00 |                              2137.00 | 16.00 |              366.62 |
| pgbouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6316.24 |               158322.00 |           1000000.00 |                              2051.00 | 16.00 |              363.82 |
| pgbouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6447.74 |               155093.00 |           1000000.00 |                              2179.00 | 16.00 |              371.39 |
| pgbouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         7575.93 |               131997.00 |           1000000.00 |                              1964.00 | 16.00 |              436.37 |
| pgbouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         8630.96 |               115862.00 |           1000000.00 |                              1884.00 | 16.00 |              497.14 |
| pgbouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6278.45 |               159275.00 |           1000000.00 |                              2343.00 | 16.00 |              361.64 |
| pgbouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         8150.89 |               122686.00 |           1000000.00 |                              1819.00 | 16.00 |              469.49 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |    SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |     0.00 | 16.00 |              361.64 |                       108862.10 |               159275.00 |          16000000.00 |                              2033.62 |

### Benchmarking

#### Per Connection

| connection           | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1-1-1  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       1 |         8 |    11264 |        0 |                         6840.37 |               146191.00 |            1000000 |                            1444.00 |
| pgbouncer-1-1-1-1-2  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       2 |         8 |    11264 |        0 |                         8777.47 |               113928.00 |            1000000 |                            1186.00 |
| pgbouncer-1-1-1-1-3  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       3 |         8 |    11264 |        0 |                         6714.88 |               148923.00 |            1000000 |                            1511.00 |
| pgbouncer-1-1-1-1-4  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       4 |         8 |    11264 |        0 |                         6829.62 |               146421.00 |            1000000 |                            1469.00 |
| pgbouncer-1-1-1-1-5  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       5 |         8 |    11264 |        0 |                         6816.54 |               146702.00 |            1000000 |                            1413.00 |
| pgbouncer-1-1-1-1-6  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       6 |         8 |    11264 |        0 |                         6802.21 |               147011.00 |            1000000 |                            1505.00 |
| pgbouncer-1-1-1-1-7  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       7 |         8 |    11264 |        0 |                         6795.51 |               147156.00 |            1000000 |                            1433.00 |
| pgbouncer-1-1-1-1-8  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       8 |         8 |    11264 |        0 |                         6920.75 |               144493.00 |            1000000 |                            1337.00 |
| pgbouncer-1-1-1-1-9  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       9 |         8 |    11264 |        0 |                         6752.15 |               148101.00 |            1000000 |                            1483.00 |
| pgbouncer-1-1-1-1-10 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      10 |         8 |    11264 |        0 |                         6861.30 |               145745.00 |            1000000 |                            1437.00 |
| pgbouncer-1-1-1-1-11 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      11 |         8 |    11264 |        0 |                         6785.46 |               147374.00 |            1000000 |                            1547.00 |
| pgbouncer-1-1-1-1-12 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      12 |         8 |    11264 |        0 |                         8973.92 |               111434.00 |            1000000 |                            1100.00 |
| pgbouncer-1-1-1-1-13 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      13 |         8 |    11264 |        0 |                         6870.40 |               145552.00 |            1000000 |                            1427.00 |
| pgbouncer-1-1-1-1-14 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      14 |         8 |    11264 |        0 |                         8825.58 |               113307.00 |            1000000 |                            1209.00 |
| pgbouncer-1-1-1-1-15 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      15 |         8 |    11264 |        0 |                         6863.23 |               145704.00 |            1000000 |                            1462.00 |
| pgbouncer-1-1-1-1-16 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      16 |         8 |    11264 |        0 |                         6808.93 |               146866.00 |            1000000 |                            1488.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1 | pgbouncer-1-1-1 |                1 |        1 |               1 |          16 |       128 |   180224 |        0 |                       115238.31 |               148923.00 |           16000000 |                            1547.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         1.18 |      0.01 |           0.08 |                  0.08 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |      1261.40 |     10.11 |          24.65 |                 42.92 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       744.93 |      6.21 |           0.43 |                  0.44 |

### Benchmarking phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.40 |      0.01 |           0.09 |                  0.09 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       789.08 |      7.70 |          26.74 |                 45.01 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       717.88 |      6.68 |           0.20 |                  0.21 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                 56822.81 |                             0.63 |                                  0.00 |                                     181.00 |                                                       26.79 |

#### Loading phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                               257.00 |                                                0.00 |                                                        0.00 |                                  31.00 |                                              31.00 |

#### Benchmarking phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                 57876.32 |                             0.18 |                                  0.00 |                                      78.00 |                                                       50.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                               257.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pool contains no 0 or NaN in CPU [CPUs]
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
* Duration: 1586s 
* Code: 1794779515
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 1 processes (pods).
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [32] threads, split into [1, 2] pods.
  * Pooling is done with [2] pods having [32] inbound and [32] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* pgbouncer-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1057463
  * datadisk:4308
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * pool 0
    * node:cl-worker29
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker27
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794779515
* pgbouncer-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1060949
  * datadisk:4585
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * pool 0
    * node:cl-worker29
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker27
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794779515

### Ingestion
* PGBouncer-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1794779515-66ff998d6c-9dql8: 0
* bexhoma-pool-pgbouncer-1-1794779515-66ff998d6c-gv76s: 0
* bexhoma-sut-pgbouncer-1-1794779515-7d6c84df-lv6cz: 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PGBouncer-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PGBouncer-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PGBouncer-1-1 |                1 |   16 |       97.00 |           4.00 |            0.00 |         70.00 |           23.00 |              1 |         1 |             | None           |             0 | False         |              593.81 | False               |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| pgbouncer-1-1-1-1-1 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       1 |        32 |    16384 |          -1 | 600.00 |        2 |                        1276.21 |                      467.14 |         0.00 |                                                      36326.00 |                                              25067.00 |
| pgbouncer-1-1-2-1-1 | pgbouncer-1-1-2 | pgbouncer-1-1-2-1 |                1 |        2 |               1 |       1 |        16 |     8192 |          -1 | 600.00 |        0 |                         654.98 |                      459.70 |         0.00 |                                                      51562.00 |                                              24420.00 |
| pgbouncer-1-1-2-1-2 | pgbouncer-1-1-2 | pgbouncer-1-1-2-1 |                1 |        2 |               1 |       2 |        16 |     8192 |          -1 | 600.00 |        0 |                         658.55 |                      460.02 |         0.00 |                                                      51350.00 |                                              24287.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| pgbouncer-1-1-1 | pgbouncer-1-1-1 |                1 |        1 |               1 |           1 |        32 |    16384 |          -1 | 600.00 |        2 |                        1276.21 |                      467.14 |         0.00 |                                                      36326.00 |                                              25067.00 |
| pgbouncer-1-1-2 | pgbouncer-1-1-2 |                1 |        2 |               1 |           2 |        32 |    16384 |          -1 | 600.00 |        0 |                        1313.53 |                      919.72 |         0.00 |                                                      51562.00 |                                              24353.50 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.38 |      0.00 |           0.04 |                  0.04 |
| pgbouncer-1-1-2-1 |         0.38 |      0.00 |           0.04 |                  0.04 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       197.20 |      2.73 |           4.41 |                  6.05 |
| pgbouncer-1-1-2-1 |       197.20 |      2.73 |           4.41 |                  6.05 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       748.85 |     13.28 |           0.35 |                  0.35 |
| pgbouncer-1-1-2-1 |       748.85 |     13.28 |           0.35 |                  0.35 |

### Benchmarking phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         1.83 |      0.01 |           0.05 |                  0.05 |
| pgbouncer-1-1-2-1 |         2.17 |      0.01 |           0.06 |                  0.06 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       703.13 |      3.67 |           5.05 |                  6.96 |
| pgbouncer-1-1-2-1 |      1311.67 |      4.90 |           5.59 |                  7.94 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |     15695.20 |     32.13 |           0.54 |                  0.54 |
| pgbouncer-1-1-2-1 |     12841.40 |     30.72 |           0.41 |                  0.41 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-2-1 (bexhoma-metrics-pgbouncer-1-1-2-1-poolbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                   239.83 |                             0.21 |                                  0.00 |                                      48.00 |                                                       50.00 |
| pgbouncer-1-1-2-1 |                                   239.83 |                             0.21 |                                  0.00 |                                      48.00 |                                                       50.00 |

#### Loading phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                65.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |
| pgbouncer-1-1-2-1 |                                65.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |

#### Benchmarking phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                  9655.95 |                             0.47 |                                  0.00 |                                      62.00 |                                                       70.97 |
| pgbouncer-1-1-2-1 |                                 19850.58 |                             0.25 |                                  0.00 |                                      62.00 |                                                       61.29 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                65.00 |                                               23.00 |                                                        0.00 |                                   7.00 |                                               7.00 |
| pgbouncer-1-1-2-1 |                                65.00 |                                               25.00 |                                                        0.00 |                                   8.00 |                                               8.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
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
  run &>$LOG_DIR/docs_ycsb_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1239s 
* Code: 1794910206
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
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:554787
  * datadisk:39
  * volume_size:879G
  * volume_used:542G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:554790
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058112
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1405842
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:555226
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1405842
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058112
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794910206

### Ingestion
* YugabyteDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794910206-bcbfb6f4f-pqw7f: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1975.85 |                63264.00 |            125000.00 |                             15031.00 | 1.00 |               56.90 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1966.92 |                63551.00 |            125000.00 |                             15407.00 | 1.00 |               56.65 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1991.24 |                62775.00 |            125000.00 |                             15039.00 | 1.00 |               57.35 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1978.13 |                63191.00 |            125000.00 |                             15415.00 | 1.00 |               56.97 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1992.95 |                62721.00 |            125000.00 |                             15127.00 | 1.00 |               57.40 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2003.04 |                62405.00 |            125000.00 |                             15439.00 | 1.00 |               57.69 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1962.91 |                63681.00 |            125000.00 |                             15087.00 | 1.00 |               56.53 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1852.37 |                67481.00 |            125000.00 |                             15903.00 | 1.00 |               53.35 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               53.35 |                        15723.42 |                67481.00 |           1000000.00 |                             15306.00 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        12101.37 |               826353.00 |            5001234 |                           52799.00 |              4998766 |                             61887.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        12101.37 |               826353.00 |            5001234 |                           52799.00 |              4998766 |                             61887.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1854.49 |     32.87 |           6.06 |                 13.32 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         7.10 |      0.07 |           0.24 |                  0.26 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        72.33 |      1.28 |           0.20 |                  0.21 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     24091.74 |     34.30 |          10.40 |                 21.51 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        39.57 |      0.16 |           0.31 |                  0.34 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1155.28 |      1.96 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                    3751.65 |                                        0.26 |                                         3.48 |                     59.00 |                      612.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.18 |                                         0.59 |                                0.00 |                       500.93 |                               0.17 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                   13960.01 |                                        0.70 |                                         4.01 |                     63.00 |                      616.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.18 |                                         0.08 |                                0.00 |                       501.00 |                               0.17 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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
  run &>$LOG_DIR/docs_benchbase_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1541s 
* Code: 1794908443
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:553740
  * datadisk:39
  * volume_size:879G
  * volume_used:541G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553740
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058593
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406344
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553740
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058594
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406344
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794908443
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:554332
  * datadisk:39
  * volume_size:879G
  * volume_used:542G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:554319
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1059236
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406976
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:554319
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1059236
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406976
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794908443

### Ingestion
* YugabyteDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794908443-57b6b9fb97-nhjxh: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |   16 |      441.00 |         305.00 |            0.00 |        134.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              130.61 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         223.16 |                      222.25 |         0.00 |                                                     183890.00 |                                              71679.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         143.28 |                      142.56 |         0.00 |                                                     142508.00 |                                              55806.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        1 |                         156.12 |                      155.45 |         0.00 |                                                     128837.00 |                                              51218.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         223.16 |                      222.25 |         0.00 |                                                     183890.00 |                                              71679.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        1 |                         299.40 |                      298.01 |         0.00 |                                                     142508.00 |                                              53512.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      3039.45 |     33.04 |           8.40 |                 17.32 |
| yugabytedb-1-1-2-1 |      3039.45 |     33.04 |           8.40 |                 17.32 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        34.29 |      0.21 |           0.38 |                  0.40 |
| yugabytedb-1-1-2-1 |        34.29 |      0.21 |           0.38 |                  0.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       630.95 |     10.07 |           0.26 |                  0.26 |
| yugabytedb-1-1-2-1 |       630.95 |     10.07 |           0.26 |                  0.26 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      9600.51 |     34.03 |          10.45 |                 19.24 |
| yugabytedb-1-1-2-1 |     10121.34 |     37.61 |          11.51 |                 20.24 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        21.31 |      0.16 |           0.43 |                  0.46 |
| yugabytedb-1-1-2-1 |        22.95 |      0.18 |           0.46 |                  0.49 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        79.77 |      0.30 |           0.29 |                  0.29 |
| yugabytedb-1-1-2-1 |       175.00 |      0.78 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                     239.46 |                                        0.77 |                                        10.48 |                     16.00 |                      614.00 |
| yugabytedb-1-1-2-1 |                                     239.46 |                                        0.77 |                                        10.48 |                     16.00 |                      614.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               1.78 |                                         1.41 |                                0.04 |                       500.80 |                               1.78 |
| yugabytedb-1-1-2-1 |                               1.78 |                                         1.41 |                                0.04 |                       500.80 |                               1.78 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                    7877.99 |                                        0.55 |                                         8.00 |                     16.00 |                      620.00 |
| yugabytedb-1-1-2-1 |                                   10785.08 |                                        0.55 |                                         1.88 |                     16.00 |                      611.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.02 |                                         0.10 |                                0.00 |                       500.84 |                               0.02 |
| yugabytedb-1-1-2-1 |                               0.00 |                                         0.10 |                                0.00 |                       501.01 |                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>
