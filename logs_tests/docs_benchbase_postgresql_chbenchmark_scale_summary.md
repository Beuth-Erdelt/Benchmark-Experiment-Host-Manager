## Show Summary

### Workload
Benchbase Workload chbenchmark SF=100
* Type: benchbase
* Duration: 6973s 
* Code: 1783974695
* Benchbase runs the CH-Benchmark benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'chbenchmark'. Scaling factor is 100. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Experiment uses bexhoma version 0.10.5.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [100] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1224877
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783974695
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1242932
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783974695
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1244195
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783974695
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1245018
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1783974695
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783974695-859fdbbb5f-p7l7q: 0 0

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
| PostgreSQL-1-1 |                1 | 100.00 |      867.00 |           0.00 |            0.00 |        414.00 |          453.00 |              1 |           1 |             |                |             0 | False         |              415.22 |

### Execution

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         100 |    16384 |        1 |               1 |       1 |           0 | 1200.00 |         2298 |                        1074.08 |                     1067.64 |         0.00 |                                                     146824.00 |                                             158529.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          50 |     8192 |        2 |               1 |       1 |           0 | 1200.00 |         1864 |                          86.89 |                       84.63 |         0.00 |                                                     144452.00 |                                             969309.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          50 |     8192 |        2 |               1 |       2 |           0 | 1200.00 |         1784 |                          80.71 |                       78.53 |         0.00 |                                                     147895.00 |                                            1038188.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       1 |           0 | 1200.00 |          634 |                          25.99 |                       25.10 |         0.00 |                                                     107852.00 |                                            1355590.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       2 |           0 | 1200.00 |          621 |                          27.35 |                       26.44 |         0.00 |                                                      75947.00 |                                            1252902.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       3 |           0 | 1200.00 |          625 |                          28.12 |                       27.19 |         0.00 |                                                      95471.00 |                                            1268214.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       4 |           0 | 1200.00 |          619 |                          26.13 |                       25.24 |         0.00 |                                                     110908.00 |                                            1326913.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       5 |           0 | 1200.00 |          630 |                          27.39 |                       26.43 |         0.00 |                                                      85949.00 |                                            1321078.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       1 |           0 | 1200.00 |          294 |                          12.08 |                       11.66 |         0.00 |                                                     433879.00 |                                            1512053.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       2 |           0 | 1200.00 |          280 |                          12.66 |                       12.26 |         0.00 |                                                     304519.00 |                                            1436473.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       3 |           0 | 1200.00 |          303 |                          11.90 |                       11.48 |         0.00 |                                                     319883.00 |                                            1372088.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       4 |           0 | 1200.00 |          294 |                          12.37 |                       11.96 |         0.00 |                                                     400742.00 |                                            1444689.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       5 |           0 | 1200.00 |          307 |                          11.79 |                       11.35 |         0.00 |                                                     496111.00 |                                            1392216.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       6 |           0 | 1200.00 |          264 |                          12.15 |                       11.76 |         0.00 |                                                     270543.00 |                                            1306122.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       7 |           0 | 1200.00 |          311 |                          12.22 |                       11.78 |         0.00 |                                                     506996.00 |                                            1392251.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       8 |           0 | 1200.00 |          275 |                          11.79 |                       11.40 |         0.00 |                                                     397529.00 |                                            1453359.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       9 |           0 | 1200.00 |          312 |                          12.13 |                       11.68 |         0.00 |                                                     422416.00 |                                            1482770.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |      10 |           0 | 1200.00 |          313 |                          12.49 |                       12.04 |         0.00 |                                                     323974.00 |                                            1348181.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         100 |    16384 |               1 |           1 |           0 | 1200.00 |         2298 |                        1074.08 |                     1067.64 |         0.00 |                                                     146824.00 |                                             158529.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         100 |    16384 |               1 |           2 |           0 | 1200.00 |         3648 |                         167.60 |                      163.15 |         0.00 |                                                     147895.00 |                                            1003748.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |         100 |    16380 |               1 |           5 |           0 | 1200.00 |         3129 |                         134.98 |                      130.39 |         0.00 |                                                     110908.00 |                                            1304939.40 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |         100 |    16380 |               1 |          10 |           0 | 1200.00 |         2953 |                         121.58 |                      117.37 |         0.00 |                                                     506996.00 |                                            1414020.20 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
