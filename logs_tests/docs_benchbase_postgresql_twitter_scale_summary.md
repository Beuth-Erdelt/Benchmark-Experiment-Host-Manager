## Show Summary

### Workload
Benchbase Workload twitter SF=1600
* Type: benchbase
* Duration: 5822s 
* Code: 1782067250
* Benchbase runs the Twitter benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'twitter'. Scaling factor is 1600. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:239751
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782067250
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:238583
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782067250
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:239803
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782067250
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:239000
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782067250
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 1600 |      503.00 |           0.00 |            0.00 |        235.00 |          268.00 |              1 |           1 |             |                |             0 | False         |            11451.29 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 1200.00 |            0 |                        8192.05 |                     8192.05 |         0.00 |                                                       2468.00 |                                               1039.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 1200.00 |            0 |                        8192.04 |                     8192.05 |         0.00 |                                                       2471.00 |                                               1040.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       1 |           0 | 1200.00 |          712 |                        4095.99 |                     4095.40 |         0.00 |                                                       2471.00 |                                               1068.00 |
| PostgreSQL-1-1-3-1-2 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       2 |           0 | 1200.00 |          777 |                        4095.99 |                     4095.35 |         0.00 |                                                       2472.00 |                                               1068.00 |
| PostgreSQL-1-1-3-1-3 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       3 |           0 | 1200.00 |          787 |                        4095.99 |                     4095.34 |         0.00 |                                                       2481.00 |                                               1072.00 |
| PostgreSQL-1-1-3-1-4 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       4 |           0 | 1200.00 |          775 |                        4095.99 |                     4095.35 |         0.00 |                                                       2481.00 |                                               1065.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       1 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2135.00 |                                                996.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       2 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2137.00 |                                                992.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       3 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2136.00 |                                                996.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       4 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2135.00 |                                                992.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       5 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2135.00 |                                                994.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       6 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2138.00 |                                                993.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       7 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2135.00 |                                                996.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       8 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2132.00 |                                                995.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 1200.00 |            0 |                       16384.09 |                    16384.10 |         0.00 |                                                       2471.00 |                                               1039.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |         160 |    16384 |               1 |           4 |           0 | 1200.00 |         3051 |                       16383.98 |                    16381.44 |         0.00 |                                                       2481.00 |                                               1068.25 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |         160 |    16384 |               1 |           8 |           0 | 1200.00 |            0 |                       16384.01 |                    16384.02 |         0.00 |                                                       2138.00 |                                                994.25 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2239.59 |     14.29 |           8.07 |                 12.66 |
| PostgreSQL-1-1-2-1 |      2239.59 |     14.29 |           8.07 |                 12.66 |
| PostgreSQL-1-1-3-1 |      2239.59 |     14.29 |           8.07 |                 12.66 |
| PostgreSQL-1-1-4-1 |      2239.59 |     14.29 |           8.07 |                 12.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        80.77 |      0.71 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2-1 |        80.77 |      0.71 |           0.26 |                  0.26 |
| PostgreSQL-1-1-3-1 |        80.77 |      0.71 |           0.26 |                  0.26 |
| PostgreSQL-1-1-4-1 |        80.77 |      0.71 |           0.26 |                  0.26 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |     10404.89 |     10.26 |          14.84 |                 19.47 |
| PostgreSQL-1-1-2-1 |     10182.45 |      9.29 |          14.86 |                 19.53 |
| PostgreSQL-1-1-3-1 |     10261.14 |      9.01 |          14.99 |                 20.38 |
| PostgreSQL-1-1-4-1 |      9710.63 |      9.71 |          15.09 |                 22.15 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2860.60 |      2.72 |           2.42 |                  2.80 |
| PostgreSQL-1-1-2-1 |      2860.60 |      4.79 |           2.42 |                  2.80 |
| PostgreSQL-1-1-3-1 |      3162.83 |      6.73 |           1.44 |                  1.63 |
| PostgreSQL-1-1-4-1 |      3425.68 |      8.83 |           0.79 |                  0.79 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
