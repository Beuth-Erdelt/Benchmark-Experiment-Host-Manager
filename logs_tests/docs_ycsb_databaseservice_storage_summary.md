## Show Summary

### Workload
YCSB SF=5
* Type: ycsb
* Duration: 774s 
* Code: 1795467781
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 5000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:900164
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795467781

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-ycsb.sql

### Ingestion
* DatabaseService-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1795467781-65847f977d-d7sm9: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:--------------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| databaseservice-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5352.77 |               116762.00 |            625000.00 |                             14063.00 | 5.00 |              154.16 |
| databaseservice-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5378.94 |               116194.00 |            625000.00 |                             14063.00 | 5.00 |              154.91 |
| databaseservice-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5351.81 |               116783.00 |            625000.00 |                             14079.00 | 5.00 |              154.13 |
| databaseservice-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5340.92 |               117021.00 |            625000.00 |                             14079.00 | 5.00 |              153.82 |
| databaseservice-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5435.16 |               114992.00 |            625000.00 |                             14039.00 | 5.00 |              156.53 |
| databaseservice-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5387.84 |               116002.00 |            625000.00 |                             14071.00 | 5.00 |              155.17 |
| databaseservice-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5361.77 |               116566.00 |            625000.00 |                             14167.00 | 5.00 |              154.42 |
| databaseservice-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         5288.99 |               118170.00 |            625000.00 |                             14111.00 | 5.00 |              152.32 |

#### Per Run

| DBMS                |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DatabaseService-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 5.00 |              152.32 |                        42898.19 |               118170.00 |           5000000.00 |                             14084.00 |

### Benchmarking

#### Per Connection

| connection                | phase                 | job                     |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1-1-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        65293.76 |               153154.00 |            4999611 |                             612.00 |              5000389 |                             27679.00 |

#### Per Phase

| DBMS                  | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        65293.76 |               153154.00 |            4999611 |                             612.00 |              5000389 |                             27679.00 |

### Monitoring

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |       497.41 |      5.15 |           0.28 |                  0.28 |

### Benchmarking phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| databaseservice-1-1-1-1 |       548.89 |      4.63 |           1.04 |                  1.04 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection databaseservice-1-1-1-1 (bexhoma-metrics-databaseservice-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
