## Show Summary

### Workload
Benchbase Workload twitter SF=1600
* Type: benchbase
* Duration: 5910s 
* Code: 1781995437
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
  * disk:246786
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1781995437
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:246912
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1781995437
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:247054
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1781995437
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:247328
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1781995437
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
| PostgreSQL-1-1 |                1 | 1600 |      509.00 |           0.00 |            0.00 |        244.00 |          265.00 |              1 |           1 |             |                |             0 | False         |            11316.31 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 1200.00 |            0 |                       16384.04 |                    16384.05 |         0.00 |                                                       2336.00 |                                                995.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 1200.00 |            0 |                        8192.03 |                     8192.03 |         0.00 |                                                       2400.00 |                                               1016.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 1200.00 |            0 |                        8192.02 |                     8192.03 |         0.00 |                                                       2406.00 |                                               1019.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       1 |           0 | 1200.00 |            0 |                        4095.99 |                     4096.00 |         0.00 |                                                       2391.00 |                                               1024.00 |
| PostgreSQL-1-1-3-1-2 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       2 |           0 | 1200.00 |            0 |                        4095.99 |                     4095.99 |         0.00 |                                                       2397.00 |                                               1031.00 |
| PostgreSQL-1-1-3-1-3 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       3 |           0 | 1200.00 |            0 |                        4095.99 |                     4095.99 |         0.00 |                                                       2393.00 |                                               1025.00 |
| PostgreSQL-1-1-3-1-4 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       4 |           0 | 1200.00 |            0 |                        4095.99 |                     4096.00 |         0.00 |                                                       2394.00 |                                               1027.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       1 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2393.00 |                                               1027.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       2 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2390.00 |                                               1026.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       3 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2387.00 |                                               1021.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       4 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2397.00 |                                               1027.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       5 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2398.00 |                                               1030.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       6 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2393.00 |                                               1024.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       7 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2399.00 |                                               1032.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       8 |           0 | 1200.00 |            0 |                        2048.00 |                     2048.00 |         0.00 |                                                       2394.00 |                                               1028.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 1200.00 |            0 |                       16384.04 |                    16384.05 |         0.00 |                                                       2336.00 |                                                995.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 1200.00 |            0 |                       16384.05 |                    16384.06 |         0.00 |                                                       2406.00 |                                               1017.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |         160 |    16384 |               1 |           4 |           0 | 1200.00 |            0 |                       16383.97 |                    16383.98 |         0.00 |                                                       2397.00 |                                               1026.75 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |         160 |    16384 |               1 |           8 |           0 | 1200.00 |            0 |                       16384.01 |                    16384.02 |         0.00 |                                                       2399.00 |                                               1026.88 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2026.32 |     14.66 |           8.07 |                 12.50 |
| PostgreSQL-1-1-2-1 |      2026.32 |     14.66 |           8.07 |                 12.50 |
| PostgreSQL-1-1-3-1 |      2026.32 |     14.66 |           8.07 |                 12.50 |
| PostgreSQL-1-1-4-1 |      2026.32 |     14.66 |           8.07 |                 12.50 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        93.31 |      0.87 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2-1 |        93.31 |      0.87 |           0.27 |                  0.27 |
| PostgreSQL-1-1-3-1 |        93.31 |      0.87 |           0.27 |                  0.27 |
| PostgreSQL-1-1-4-1 |        93.31 |      0.87 |           0.27 |                  0.27 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |     10112.78 |      9.37 |          14.81 |                 19.28 |
| PostgreSQL-1-1-2-1 |     10189.62 |      9.36 |          14.87 |                 19.39 |
| PostgreSQL-1-1-3-1 |     10158.97 |      9.93 |          14.98 |                 20.30 |
| PostgreSQL-1-1-4-1 |     10055.34 |      9.88 |          15.10 |                 22.17 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2858.47 |      2.60 |           2.43 |                  3.22 |
| PostgreSQL-1-1-2-1 |      2816.93 |      4.28 |           2.43 |                  3.22 |
| PostgreSQL-1-1-3-1 |      3000.67 |      5.87 |           1.34 |                  1.44 |
| PostgreSQL-1-1-4-1 |      3107.84 |      6.69 |           0.81 |                  0.90 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
