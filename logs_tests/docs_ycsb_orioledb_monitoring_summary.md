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
