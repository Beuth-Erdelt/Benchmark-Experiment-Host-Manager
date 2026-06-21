## Show Summary

### Workload
Benchbase Workload chbenchmark SF=100
* Type: benchbase
* Duration: 6060s 
* Code: 1782002241
* Benchbase runs the CH-Benchmark benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'chbenchmark'. Scaling factor is 100. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [100] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251041
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782002241
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251042
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782002241
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251042
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782002241
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251044
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782002241
    * TENANT_VOL:False

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
| PostgreSQL-1-1 |                1 |  100 |      879.00 |           1.00 |            0.00 |        417.00 |          461.00 |              1 |           1 |             |                |             0 | False         |              409.56 |

### Execution

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         100 |    16384 |        1 |               1 |       1 |           0 | 1200.00 |          300 |                           4.83 |                        4.66 |         0.00 |                                                   71192080.00 |                                           20147019.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          50 |     8192 |        2 |               1 |       1 |           0 | 1200.00 |          130 |                           2.26 |                        2.20 |         0.00 |                                                   74231558.00 |                                           21618603.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          50 |     8192 |        2 |               1 |       2 |           0 | 1200.00 |          142 |                           2.43 |                        2.35 |         0.00 |                                                   71561608.00 |                                           20073408.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       1 |           0 | 1200.00 |           53 |                           0.97 |                        0.94 |         0.00 |                                                   72104715.00 |                                           20254359.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       2 |           0 | 1200.00 |           62 |                           1.01 |                        0.98 |         0.00 |                                                   70193058.00 |                                           19455191.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       3 |           0 | 1200.00 |           68 |                           0.95 |                        0.91 |         0.00 |                                                   72873097.00 |                                           20675622.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       4 |           0 | 1200.00 |           70 |                           0.96 |                        0.92 |         0.00 |                                                   69312262.00 |                                           20222176.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       5 |           0 | 1200.00 |           70 |                           0.96 |                        0.92 |         0.00 |                                                   69654133.00 |                                           20218588.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       1 |           0 | 1200.00 |           27 |                           0.45 |                        0.44 |         0.00 |                                                   74522887.00 |                                           21790539.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |      10 |           0 | 1200.00 |           38 |                           0.48 |                        0.46 |         0.00 |                                                   71570770.00 |                                           20142294.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       2 |           0 | 1200.00 |           35 |                           0.48 |                        0.46 |         0.00 |                                                   70170061.00 |                                           20475835.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       3 |           0 | 1200.00 |           26 |                           0.50 |                        0.48 |         0.00 |                                                   71643268.00 |                                           19950352.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       4 |           0 | 1200.00 |           27 |                           0.44 |                        0.42 |         0.00 |                                                   72868026.00 |                                           22435528.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       5 |           0 | 1200.00 |           28 |                           0.49 |                        0.47 |         0.00 |                                                   70717667.00 |                                           20265040.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       6 |           0 | 1200.00 |           31 |                           0.51 |                        0.49 |         0.00 |                                                   71078575.00 |                                           19208389.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       7 |           0 | 1200.00 |           24 |                           0.45 |                        0.44 |         0.00 |                                                   72331301.00 |                                           21718304.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       8 |           0 | 1200.00 |           22 |                           0.48 |                        0.47 |         0.00 |                                                   71766391.00 |                                           20361203.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       9 |           0 | 1200.00 |           24 |                           0.48 |                        0.47 |         0.00 |                                                   74417638.00 |                                           20500085.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         100 |    16384 |               1 |           1 |           0 | 1200.00 |          300 |                           4.83 |                        4.66 |         0.00 |                                                   71192080.00 |                                           20147019.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         100 |    16384 |               1 |           2 |           0 | 1200.00 |          272 |                           4.70 |                        4.55 |         0.00 |                                                   74231558.00 |                                           20846005.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |         100 |    16380 |               1 |           5 |           0 | 1200.00 |          323 |                           4.85 |                        4.66 |         0.00 |                                                   72873097.00 |                                           20165187.20 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |         100 |    16380 |               1 |          10 |           0 | 1200.00 |          282 |                           4.75 |                        4.60 |         0.00 |                                                   74522887.00 |                                           20684756.90 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
