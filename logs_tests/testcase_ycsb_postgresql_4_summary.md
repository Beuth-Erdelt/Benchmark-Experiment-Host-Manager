## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2262s 
* Code: 1793686799
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'E'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812866
  * datadisk:2391
  * volume_size:49G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793686799

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793686799-54bf55db55-9m55b: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976881.00 |            125000.00 |                              1231.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976911.00 |            125000.00 |                              1238.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976899.00 |            125000.00 |                              1239.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976881.00 |            125000.00 |                              1301.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976854.00 |            125000.00 |                              1205.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976876.00 |            125000.00 |                              1233.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976890.00 |            125000.00 |                              1214.00 | 1.00 |                3.69 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976889.00 |            125000.00 |                              1246.00 | 1.00 |                3.69 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.69 |                         1023.66 |               976911.00 |           1000000.00 |                              1238.38 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976893.00 |                 6250 |                              4395.00 |             118676 |                            1803.00 |                           74 |                                     1679.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976885.00 |                 6250 |                              4147.00 |             118633 |                            1784.00 |                          117 |                                     1717.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976892.00 |                 6231 |                              4199.00 |             118769 |                            1803.00 |                            0 |                                        0.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976898.00 |                 6250 |                              4219.00 |             118685 |                            1787.00 |                           65 |                                     1668.00 |
| postgresql-1-1-1-1-5 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976865.00 |                 6250 |                              4223.00 |             118702 |                            1828.00 |                           48 |                                    17247.00 |
| postgresql-1-1-1-1-6 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976879.00 |                 6250 |                              4419.00 |             118719 |                            1805.00 |                           31 |                                    13527.00 |
| postgresql-1-1-1-1-7 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976884.00 |                 6250 |                              4407.00 |             118737 |                            1822.00 |                           13 |                                    13823.00 |
| postgresql-1-1-1-1-8 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976865.00 |                 6455 |                              4123.00 |             118545 |                            1797.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.66 |               976898.00 |                50186 |                              4419.00 |             949466 |                            1828.00 |                          348 |                                    17247.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
