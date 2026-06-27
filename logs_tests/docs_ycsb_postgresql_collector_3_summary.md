## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1153s 
* Code: 1781944488
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
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1323754
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781944488
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324617
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781944488
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1306773
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781944488
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1307120
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781944488

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
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7994.54 |                46907.00 |            375000.00 |                              2795.00 | 3.00 |              230.24 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7869.06 |                47655.00 |            375000.00 |                              2859.00 | 3.00 |              226.63 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7864.27 |                47684.00 |            375000.00 |                              2963.00 | 3.00 |              226.49 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7923.09 |                47330.00 |            375000.00 |                              2813.00 | 3.00 |              228.19 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8012.82 |                46800.00 |            375000.00 |                              2847.00 | 3.00 |              230.77 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7940.71 |                47225.00 |            375000.00 |                              2897.00 | 3.00 |              228.69 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7893.41 |                47508.00 |            375000.00 |                              2829.00 | 3.00 |              227.33 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7899.56 |                47471.00 |            375000.00 |                              2909.00 | 3.00 |              227.51 |
| PostgreSQL-1-2-0-1-1 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8011.62 |                46807.00 |            375000.00 |                              2687.00 | 3.00 |              230.73 |
| PostgreSQL-1-2-0-1-2 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8106.36 |                46260.00 |            375000.00 |                              2689.00 | 3.00 |              233.46 |
| PostgreSQL-1-2-0-1-3 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7747.61 |                48402.00 |            375000.00 |                              2737.00 | 3.00 |              223.13 |
| PostgreSQL-1-2-0-1-4 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7915.23 |                47377.00 |            375000.00 |                              2749.00 | 3.00 |              227.96 |
| PostgreSQL-1-2-0-1-5 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8133.96 |                46103.00 |            375000.00 |                              2637.00 | 3.00 |              234.26 |
| PostgreSQL-1-2-0-1-6 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7900.23 |                47467.00 |            375000.00 |                              2695.00 | 3.00 |              227.53 |
| PostgreSQL-1-2-0-1-7 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7887.10 |                47546.00 |            375000.00 |                              2683.00 | 3.00 |              227.15 |
| PostgreSQL-1-2-0-1-8 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8066.60 |                46488.00 |            375000.00 |                              2617.00 | 3.00 |              232.32 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              226.49 |                        63397.46 |                47684.00 |           3000000.00 |                              2864.00 |
| PostgreSQL-1-2 |             2.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              223.13 |                        63768.71 |                48402.00 |           3000000.00 |                              2686.75 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48466.05 |                20633.00 |             499248 |                             457.00 |               500752 |                              1683.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6077.40 |                20568.00 |              62496 |                             610.00 |                62504 |                              1738.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6077.40 |                20568.00 |              62888 |                             602.00 |                62112 |                              1703.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6073.27 |                20582.00 |              62616 |                             616.00 |                62384 |                              1743.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6072.97 |                20583.00 |              62414 |                             566.00 |                62586 |                              1651.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6077.70 |                20567.00 |              62667 |                             539.00 |                62333 |                              1641.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6076.52 |                20571.00 |              62490 |                             607.00 |                62510 |                              1685.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6078.88 |                20563.00 |              62518 |                             568.00 |                62482 |                              1656.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6073.86 |                20580.00 |              62375 |                             566.00 |                62625 |                              1711.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48454.31 |                20638.00 |             501199 |                             521.00 |               498801 |                              1647.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6072.97 |                20583.00 |              62588 |                             558.00 |                62412 |                              1603.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6073.27 |                20582.00 |              62275 |                             578.00 |                62725 |                              1641.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6078.88 |                20563.00 |              62327 |                             567.00 |                62673 |                              1583.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6076.52 |                20571.00 |              62358 |                             567.00 |                62642 |                              1608.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6078.58 |                20564.00 |              62381 |                             585.00 |                62619 |                              1607.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6075.33 |                20575.00 |              62664 |                             593.00 |                62336 |                              1633.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6072.38 |                20585.00 |              62548 |                             579.00 |                62452 |                              1620.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6076.22 |                20572.00 |              62437 |                             579.00 |                62563 |                              1596.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48466.05 |                20633.00 |             499248 |                             457.00 |               500752 |                              1683.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48607.99 |                20583.00 |             500464 |                             616.00 |               499536 |                              1743.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |    49152 |               1 |           1 |            0 |                        48454.31 |                20638.00 |             501199 |                             521.00 |               498801 |                              1647.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        64 |    49152 |               1 |           8 |            0 |                        48604.16 |                20585.00 |             499578 |                             593.00 |               500422 |                              1641.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       291.61 |      6.19 |           4.24 |                  5.56 |
| PostgreSQL-1-1-2-1 |       291.61 |      6.19 |           4.24 |                  5.56 |
| PostgreSQL-1-2-1-1 |       479.60 |      5.35 |           4.36 |                  8.22 |
| PostgreSQL-1-2-2-1 |       479.60 |      5.35 |           4.36 |                  8.22 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       225.20 |      5.90 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       225.20 |      5.90 |           0.11 |                  0.11 |
| PostgreSQL-1-2-1-1 |        98.01 |      0.00 |           0.11 |                  0.11 |
| PostgreSQL-1-2-2-1 |        98.01 |      0.00 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.11 |      0.25 |           3.94 |                  7.38 |
| PostgreSQL-1-1-2-1 |        64.20 |      3.36 |           4.97 |                  8.80 |
| PostgreSQL-1-2-1-1 |        16.81 |      0.47 |           4.54 |                  8.06 |
| PostgreSQL-1-2-2-1 |         0.10 |      0.00 |           4.22 |                  7.94 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     48.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   16.00 |
| PostgreSQL-1-1-2-1 |                     48.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   16.00 |
| PostgreSQL-1-2-1-1 |                     19.00 |                                     0.00 |                                             0.00 |                       50.00 |                                   49.00 |
| PostgreSQL-1-2-2-1 |                     19.00 |                                     0.00 |                                             0.00 |                       50.00 |                                   49.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     50.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   15.00 |
| PostgreSQL-1-1-2-1 |                     48.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   16.00 |
| PostgreSQL-1-2-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-1-2-2-1 |                     49.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   15.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
