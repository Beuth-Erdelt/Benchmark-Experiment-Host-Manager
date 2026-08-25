## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1013s 
* Code: 1785563194
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'F'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.9.
  * System metrics are monitored by a cluster-wide installation.
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
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:789433
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785563194
* postgresql-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:792795
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785563194

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785563194-5868c484f4-pqnth: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7346.07 |               170159.00 |           1250000.00 |                              3463.00 | 10.00 |              211.57 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7367.68 |               169660.00 |           1250000.00 |                              3497.00 | 10.00 |              212.19 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7200.63 |               173596.00 |           1250000.00 |                              3371.00 | 10.00 |              207.38 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7524.73 |               166119.00 |           1250000.00 |                              3419.00 | 10.00 |              216.71 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7505.12 |               166553.00 |           1250000.00 |                              3409.00 | 10.00 |              216.15 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7186.68 |               173933.00 |           1250000.00 |                              3509.00 | 10.00 |              206.98 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7339.17 |               170319.00 |           1250000.00 |                              3451.00 | 10.00 |              211.37 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7203.53 |               173526.00 |           1250000.00 |                              3463.00 | 10.00 |              207.46 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |              206.98 |                        58673.59 |               173933.00 |          10000000.00 |                              3447.75 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-MODIFY-WRITE].Operations |   [READ-MODIFY-WRITE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------------:|------------------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        65409.07 |               152884.00 |           10000000 |                             639.00 |              4998460 |                              2555.00 |                          4998460 |                                         2991.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     8192 |           8 |            0 |                         8178.86 |               152833.00 |            1250000 |                             639.00 |               624590 |                              1785.00 |                           624590 |                                         2193.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     8192 |           8 |            0 |                         8179.77 |               152816.00 |            1250000 |                             640.00 |               624284 |                              1771.00 |                           624284 |                                         2163.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     8192 |           8 |            0 |                         8180.04 |               152811.00 |            1250000 |                             629.00 |               625354 |                              1754.00 |                           625354 |                                         2143.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     8192 |           8 |            0 |                         8179.02 |               152830.00 |            1250000 |                             625.00 |               625309 |                              1752.00 |                           625309 |                                         2147.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     8192 |           8 |            0 |                         8179.72 |               152817.00 |            1250000 |                             644.00 |               624328 |                              1806.00 |                           624328 |                                         2215.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     8192 |           8 |            0 |                         8178.75 |               152835.00 |            1250000 |                             636.00 |               625321 |                              1782.00 |                           625321 |                                         2177.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     8192 |           8 |            0 |                         8178.54 |               152839.00 |            1250000 |                             621.00 |               624710 |                              1725.00 |                           624710 |                                         2115.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     8192 |           8 |            0 |                         8179.24 |               152826.00 |            1249999 |                             632.00 |               624474 |                              1775.00 |                           624475 |                                         2171.00 |                          1 |                                    652.00 |                            1 |                                      362.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-MODIFY-WRITE].Operations |   [READ-MODIFY-WRITE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------------:|------------------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        65409.07 |               152884.00 |           10000000 |                             639.00 |              4998460 |                              2555.00 |                          4998460 |                                         2991.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    65536 |               1 |           8 |            0 |                        65433.95 |               152839.00 |            9999999 |                             644.00 |              4998370 |                              1806.00 |                          4998371 |                                         2215.00 |                          1 |                                    652.00 |                            1 |                                      362.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1018.20 |      6.10 |          12.59 |                 23.68 |
| postgresql-1-1-2-1 |      1018.20 |      6.10 |          12.59 |                 23.68 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       925.57 |      5.81 |           0.11 |                  0.11 |
| postgresql-1-1-2-1 |       925.57 |      5.81 |           0.11 |                  0.11 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       923.71 |      7.73 |          15.54 |                 28.46 |
| postgresql-1-1-2-1 |       887.14 |      6.93 |          16.03 |                 29.39 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       883.63 |      6.94 |           0.14 |                  0.14 |
| postgresql-1-1-2-1 |      1253.97 |     15.94 |           0.14 |                  0.14 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
