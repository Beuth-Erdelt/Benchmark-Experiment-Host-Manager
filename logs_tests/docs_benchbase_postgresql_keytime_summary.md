## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 10977s 
* Code: 1783812297
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Experiment uses bexhoma version 0.10.4.
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
  * disk:1062821
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783812297
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062847
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783812297
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062856
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783812297
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062866
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783812297
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783812297-c86d9d9f4-8s4mb: 0 0

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
| PostgreSQL-1-1 |                1 | 160.00 |     4893.00 |           1.00 |            0.00 |       2183.00 |         2709.00 |              1 |           1 |             |                |             0 | False         |              117.72 |

### Execution

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1600 |     1024 |        1 |               1 |       1 |           0 | 1800.00 |            0 |                          75.60 |                       75.25 |        98.75 |                                                     665032.00 |                                             201918.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       1 |           0 | 1800.00 |            0 |                          37.92 |                       37.78 |        49.57 |                                                     729907.00 |                                             241425.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       2 |           0 | 1800.00 |            0 |                          37.86 |                       37.69 |        49.46 |                                                     740845.00 |                                             244621.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       1 |           0 | 1800.00 |            0 |                          15.12 |                       15.06 |        19.76 |                                                     773592.00 |                                             236449.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       2 |           0 | 1800.00 |            0 |                          15.22 |                       15.15 |        19.88 |                                                     723871.00 |                                             232006.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       3 |           0 | 1800.00 |            0 |                          15.12 |                       15.04 |        19.74 |                                                     759177.00 |                                             234602.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       4 |           0 | 1800.00 |            0 |                          15.15 |                       15.08 |        19.79 |                                                     767241.00 |                                             232059.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       5 |           0 | 1800.00 |            0 |                          15.10 |                       15.03 |        19.72 |                                                     769635.00 |                                             236309.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       1 |           0 | 1800.00 |            0 |                           7.43 |                        7.39 |         9.69 |                                                    1491642.00 |                                             417386.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |      10 |           0 | 1800.00 |            0 |                           7.65 |                        7.62 |        10.00 |                                                    1439930.00 |                                             417164.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       2 |           0 | 1800.00 |            0 |                           7.45 |                        7.42 |         9.74 |                                                    1397715.00 |                                             405487.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       3 |           0 | 1800.00 |            0 |                           7.45 |                        7.41 |         9.72 |                                                    1582314.00 |                                             424616.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       4 |           0 | 1800.00 |            0 |                           7.52 |                        7.50 |         9.84 |                                                    1356526.00 |                                             392942.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       5 |           0 | 1800.00 |            0 |                           7.50 |                        7.47 |         9.81 |                                                    1409202.00 |                                             410174.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       6 |           0 | 1800.00 |            0 |                           7.46 |                        7.42 |         9.74 |                                                    1478807.00 |                                             403901.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       7 |           0 | 1800.00 |            0 |                           7.53 |                        7.50 |         9.84 |                                                    1434196.00 |                                             413686.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       8 |           0 | 1800.00 |            0 |                           7.50 |                        7.48 |         9.81 |                                                    1538011.00 |                                             428255.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       9 |           0 | 1800.00 |            0 |                           7.48 |                        7.46 |         9.79 |                                                    1402319.00 |                                             418458.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1600 |     1024 |               1 |           1 |           0 | 1800.00 |            0 |                          75.60 |                       75.25 |        98.75 |                                                     665032.00 |                                             201918.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        1600 |     1024 |               1 |           2 |           0 | 1800.00 |            0 |                          75.78 |                       75.47 |        99.03 |                                                     740845.00 |                                             243023.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        1600 |     1020 |               1 |           5 |           0 | 1800.00 |            0 |                          75.70 |                       75.37 |        98.90 |                                                     773592.00 |                                             234285.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        1600 |     1020 |               1 |          10 |           0 | 1800.00 |            0 |                          74.99 |                       74.67 |        97.98 |                                                    1582314.00 |                                             413206.90 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1647.90 |      1.47 |          16.65 |                 32.60 |
| PostgreSQL-1-1-2-1 |      1647.90 |      1.47 |          16.65 |                 32.60 |
| PostgreSQL-1-1-3-1 |      1647.90 |      1.47 |          16.65 |                 32.60 |
| PostgreSQL-1-1-4-1 |      1647.90 |      1.47 |          16.65 |                 32.60 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |     15221.30 |     16.51 |           0.30 |                  0.30 |
| PostgreSQL-1-1-2-1 |     15221.30 |     16.51 |           0.30 |                  0.30 |
| PostgreSQL-1-1-3-1 |     15221.30 |     16.51 |           0.30 |                  0.30 |
| PostgreSQL-1-1-4-1 |     15221.30 |     16.51 |           0.30 |                  0.30 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       405.90 |      3.71 |          26.08 |                 42.35 |
| PostgreSQL-1-1-2-1 |       299.29 |      0.32 |          26.14 |                 42.63 |
| PostgreSQL-1-1-3-1 |       317.28 |      0.49 |          26.85 |                 43.53 |
| PostgreSQL-1-1-4-1 |       325.55 |      0.52 |          27.46 |                 44.32 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       410.50 |      1.58 |           4.16 |                  4.16 |
| PostgreSQL-1-1-2-1 |       410.50 |      2.34 |           3.98 |                  3.98 |
| PostgreSQL-1-1-3-1 |       504.05 |      4.95 |           2.35 |                  2.35 |
| PostgreSQL-1-1-4-1 |       752.63 |      9.90 |           1.06 |                  1.06 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
