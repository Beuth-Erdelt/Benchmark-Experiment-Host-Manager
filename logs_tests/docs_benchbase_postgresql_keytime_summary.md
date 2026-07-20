## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 13998s 
* Code: 1784568232
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Experiment uses bexhoma version 0.10.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1600] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:496031
  * volume_size:100G
  * volume_used:44G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1784568232
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:495658
  * volume_size:100G
  * volume_used:44G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1784568232
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:495421
  * volume_size:100G
  * volume_used:44G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1784568232
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:495304
  * volume_size:100G
  * volume_used:44G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1784568232
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1784568232-758b598948-wnzbk: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

### Loading

#### Per Run

|                |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 160.00 |    11993.00 |           1.00 |            0.00 |       5674.00 |         6318.00 |              1 |           1 |             |                |             0 | False         |               48.03 |

### Execution

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1600 |     1024 |        1 |               1 |       1 |           0 | 1800.00 |            0 |                          74.93 |                       74.58 |        97.86 |                                                    1811537.00 |                                             472492.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       1 |           0 | 1800.00 |            0 |                          37.40 |                       37.24 |        48.86 |                                                     829570.00 |                                             339565.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       2 |           0 | 1800.00 |            0 |                          37.66 |                       37.50 |        49.21 |                                                     806496.00 |                                             332234.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       1 |           0 | 1800.00 |            0 |                          15.02 |                       14.96 |        19.63 |                                                     684466.00 |                                             199496.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       2 |           0 | 1800.00 |            0 |                          15.15 |                       15.09 |        19.80 |                                                     658210.00 |                                             191683.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       3 |           0 | 1800.00 |            0 |                          15.10 |                       15.02 |        19.71 |                                                     666816.00 |                                             196814.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       4 |           0 | 1800.00 |            0 |                          15.24 |                       15.17 |        19.91 |                                                     675913.00 |                                             196994.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       5 |           0 | 1800.00 |            0 |                          15.22 |                       15.14 |        19.86 |                                                     685635.00 |                                             200488.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       1 |           0 | 1800.00 |            0 |                           7.27 |                        7.24 |         9.50 |                                                    5183462.00 |                                             837603.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       2 |           0 | 1800.00 |            0 |                           7.32 |                        7.28 |         9.56 |                                                    5408338.00 |                                             881881.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       3 |           0 | 1800.00 |            0 |                           7.30 |                        7.26 |         9.53 |                                                    5534309.00 |                                             873072.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       4 |           0 | 1800.00 |            0 |                           7.29 |                        7.26 |         9.53 |                                                    5693637.00 |                                             893170.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       5 |           0 | 1800.00 |            0 |                           7.35 |                        7.31 |         9.59 |                                                    5388222.00 |                                             852302.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       6 |           0 | 1800.00 |            0 |                           7.34 |                        7.31 |         9.59 |                                                    5374924.00 |                                             867748.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       7 |           0 | 1800.00 |            0 |                           7.34 |                        7.30 |         9.58 |                                                    5612752.00 |                                             896233.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       8 |           0 | 1800.00 |            0 |                           7.35 |                        7.31 |         9.59 |                                                    5452292.00 |                                             878469.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       9 |           0 | 1800.00 |            0 |                           7.30 |                        7.27 |         9.54 |                                                    5602237.00 |                                             874448.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |      10 |           0 | 1800.00 |            0 |                           7.28 |                        7.24 |         9.50 |                                                    5484944.00 |                                             889498.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1600 |     1024 |               1 |           1 |           0 | 1800.00 |            0 |                          74.93 |                       74.58 |        97.86 |                                                    1811537.00 |                                             472492.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        1600 |     1024 |               1 |           2 |           0 | 1800.00 |            0 |                          75.07 |                       74.74 |        98.08 |                                                     829570.00 |                                             335899.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        1600 |     1020 |               1 |           5 |           0 | 1800.00 |            0 |                          75.73 |                       75.37 |        98.91 |                                                     685635.00 |                                             197095.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        1600 |     1020 |               1 |          10 |           0 | 1800.00 |            0 |                          73.13 |                       72.78 |        95.50 |                                                    5693637.00 |                                             874442.40 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1868.28 |      0.77 |          16.67 |                 32.61 |
| PostgreSQL-1-1-2-1 |      2041.73 |      0.77 |          24.50 |                 40.71 |
| PostgreSQL-1-1-3-1 |      2041.73 |      0.77 |          24.50 |                 40.71 |
| PostgreSQL-1-1-4-1 |      2041.73 |      0.77 |          24.50 |                 40.71 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |     14816.68 |      9.76 |           0.30 |                  0.30 |
| PostgreSQL-1-1-2-1 |     14816.68 |      9.76 |           0.30 |                  0.30 |
| PostgreSQL-1-1-3-1 |     14816.68 |      9.76 |           0.30 |                  0.30 |
| PostgreSQL-1-1-4-1 |     14816.68 |      9.76 |           0.30 |                  0.30 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       362.09 |      0.72 |          26.30 |                 42.57 |
| PostgreSQL-1-1-2-1 |       303.82 |      0.37 |          26.13 |                 42.62 |
| PostgreSQL-1-1-3-1 |       325.13 |      0.41 |          26.89 |                 43.59 |
| PostgreSQL-1-1-4-1 |       330.72 |      0.52 |          27.58 |                 44.44 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       399.54 |      1.94 |           4.13 |                  4.13 |
| PostgreSQL-1-1-2-1 |       399.54 |      2.96 |           3.97 |                  3.97 |
| PostgreSQL-1-1-3-1 |       580.45 |      5.31 |           2.32 |                  2.32 |
| PostgreSQL-1-1-4-1 |       821.37 |     11.74 |           1.18 |                  1.18 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
