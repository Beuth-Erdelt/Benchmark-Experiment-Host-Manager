## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 4817s 
* Code: 1782506247
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Experiment uses bexhoma version 0.10.1.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1600] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220975
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782506247
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220975
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782506247
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220975
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782506247
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220975
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782506247
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782506247-5cc87845d4-nv9bs: 0 0

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

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |  160 |     3897.00 |           7.00 |            0.00 |       1823.00 |         2067.00 |              1 |           1 |             |                |             0 | False         |              147.81 |

### Execution

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1600 |     1024 |        1 |               1 |       1 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |           0 |      512 |        2 |               1 |       1 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |           0 |      512 |        2 |               1 |       2 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |           0 |      204 |        3 |               1 |       1 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |           0 |      204 |        3 |               1 |       2 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |           0 |      204 |        3 |               1 |       3 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |           0 |      204 |        3 |               1 |       4 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |           0 |      204 |        3 |               1 |       5 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       1 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |      10 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       2 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       3 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       4 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       5 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       6 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       7 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       8 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\benchbase.py:469: FutureWarning: 
Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call 
result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', 
True)`
  df.fillna(0, inplace=True)
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |           0 |      102 |        4 |               1 |       9 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1600 |     1024 |               1 |           1 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |           0 |     1024 |               1 |           2 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |           0 |     1020 |               1 |           5 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |           0 |     1020 |               1 |          10 |           0 | 1800.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                          0.00 |                                                  0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      4799.67 |      3.79 |          16.54 |                 32.49 |
| PostgreSQL-1-1-2-1 |      4799.67 |      3.79 |          16.54 |                 32.49 |
| PostgreSQL-1-1-3-1 |      4799.67 |      3.79 |          16.54 |                 32.49 |
| PostgreSQL-1-1-4-1 |      4799.67 |      3.79 |          16.54 |                 32.49 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |     14193.19 |     18.88 |           0.30 |                  0.30 |
| PostgreSQL-1-1-2-1 |     14193.19 |     18.88 |           0.30 |                  0.30 |
| PostgreSQL-1-1-3-1 |     14193.19 |     18.88 |           0.30 |                  0.30 |
| PostgreSQL-1-1-4-1 |     14193.19 |     18.88 |           0.30 |                  0.30 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        10.26 |      0.09 |          17.47 |                 33.44 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.01 |          17.47 |                 33.44 |
| PostgreSQL-1-1-3-1 |         0.00 |      0.00 |          17.47 |                 33.44 |
| PostgreSQL-1-1-4-1 |         0.00 |      0.00 |          17.47 |                 33.44 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        34.90 |      0.17 |           0.16 |                  0.16 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.02 |           0.16 |                  0.16 |
| PostgreSQL-1-1-3-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-4-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST failed: Throughput (requests/second) contains 0 or NaN
* TEST passed: Workflow as planned
