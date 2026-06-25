## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2471s 
* Code: 1782364325
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222623
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223817
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: benchbase (4 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: benchbase (4 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              0 |           1 |             |                |             0 | False         |               76.90 |
| PostgreSQL-1-2 |                2 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              0 |           1 |             |                |             0 | False         |               76.90 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |           0 | 120.00 |            0 |                         636.60 |                      630.76 |         0.00 |                                                    1090371.00 |                                             249829.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       1 |           0 | 120.00 |            1 |                         477.71 |                      473.88 |         0.00 |                                                    1685708.00 |                                             332123.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       2 |           0 | 120.00 |            0 |                         485.80 |                      481.89 |         0.00 |                                                    1652145.00 |                                             326588.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       1 |           0 | 120.00 |            0 |                         505.12 |                      500.57 |         0.00 |                                                     641983.00 |                                             157003.00 |
| PostgreSQL-1-1-3-1-2 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       2 |           0 | 120.00 |            0 |                         494.12 |                      489.75 |         0.00 |                                                     658908.00 |                                             161178.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       1 |           0 | 120.00 |            1 |                         204.44 |                      203.08 |         0.00 |                                                    1848759.00 |                                             386955.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       2 |           0 | 120.00 |            0 |                         210.92 |                      209.42 |         0.00 |                                                    1797703.00 |                                             374969.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       3 |           0 | 120.00 |            0 |                         208.47 |                      207.16 |         0.00 |                                                    1882198.00 |                                             380525.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       4 |           0 | 120.00 |            1 |                         205.55 |                      204.31 |         0.00 |                                                    1848898.00 |                                             384630.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |           0 | 120.00 |            0 |                         489.02 |                      485.34 |         0.00 |                                                    1401511.00 |                                             326610.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       1 |           0 | 120.00 |            0 |                         588.40 |                      583.32 |         0.00 |                                                    1262257.00 |                                             269739.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       2 |           0 | 120.00 |            0 |                         580.57 |                      575.71 |         0.00 |                                                    1278093.00 |                                             272905.00 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       1 |           0 | 120.00 |            0 |                         616.69 |                      611.22 |         0.00 |                                                     461185.00 |                                             129369.00 |
| PostgreSQL-1-2-3-1-2 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       2 |           0 | 120.00 |            0 |                         616.21 |                      610.55 |         0.00 |                                                     457243.00 |                                             129474.00 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       1 |           0 | 120.00 |            0 |                         204.86 |                      203.47 |         0.00 |                                                    1865151.00 |                                             387985.00 |
| PostgreSQL-1-2-4-1-2 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       2 |           0 | 120.00 |            0 |                         209.17 |                      207.83 |         0.00 |                                                    1812033.00 |                                             381303.00 |
| PostgreSQL-1-2-4-1-3 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       3 |           0 | 120.00 |            0 |                         205.87 |                      204.22 |         0.00 |                                                    1825412.00 |                                             385903.00 |
| PostgreSQL-1-2-4-1-4 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       4 |           0 | 120.00 |            0 |                         212.42 |                      211.01 |         0.00 |                                                    1775657.00 |                                             374683.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |           0 | 120.00 |            0 |                         636.60 |                      630.76 |         0.00 |                                                    1090371.00 |                                             249829.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         320 |    16384 |               1 |           2 |           0 | 120.00 |            1 |                         963.51 |                      955.77 |         0.00 |                                                    1685708.00 |                                             329355.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |         160 |     8192 |               1 |           2 |           0 | 120.00 |            0 |                         999.23 |                      990.32 |         0.00 |                                                     658908.00 |                                             159090.50 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |         320 |    16384 |               1 |           4 |           0 | 120.00 |            2 |                         829.38 |                      823.97 |         0.00 |                                                    1882198.00 |                                             381769.75 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |     8192 |               1 |           1 |           0 | 120.00 |            0 |                         489.02 |                      485.34 |         0.00 |                                                    1401511.00 |                                             326610.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         320 |    16384 |               1 |           2 |           0 | 120.00 |            0 |                        1168.97 |                     1159.03 |         0.00 |                                                    1278093.00 |                                             271322.00 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |         160 |     8192 |               1 |           2 |           0 | 120.00 |            0 |                        1232.90 |                     1221.77 |         0.00 |                                                     461185.00 |                                             129421.50 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |         320 |    16384 |               1 |           4 |           0 | 120.00 |            0 |                         832.32 |                      826.52 |         0.00 |                                                    1865151.00 |                                             382468.50 |

### Monitoring

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       236.54 |      2.99 |           2.46 |                  3.76 |
| PostgreSQL-1-1-2-1 |       564.62 |      5.99 |           3.89 |                  5.51 |
| PostgreSQL-1-1-3-1 |       516.64 |      5.85 |           3.32 |                  5.23 |
| PostgreSQL-1-1-4-1 |       551.32 |      6.39 |           4.54 |                  6.64 |
| PostgreSQL-1-2-1-1 |      2029.18 |      3.83 |           2.47 |                  4.59 |
| PostgreSQL-1-2-2-1 |       928.13 |      8.71 |           3.88 |                  5.48 |
| PostgreSQL-1-2-3-1 |       782.87 |      7.32 |           3.40 |                  5.33 |
| PostgreSQL-1-2-4-1 |       579.57 |      6.13 |           4.51 |                  6.64 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       107.31 |      1.48 |           0.65 |                  0.65 |
| PostgreSQL-1-1-2-1 |       164.51 |      2.76 |           0.70 |                  0.70 |
| PostgreSQL-1-1-3-1 |       150.72 |      2.63 |           0.70 |                  0.70 |
| PostgreSQL-1-1-4-1 |       175.11 |      2.44 |           0.41 |                  0.41 |
| PostgreSQL-1-2-1-1 |        80.68 |      1.15 |           0.65 |                  0.65 |
| PostgreSQL-1-2-2-1 |       159.50 |      3.15 |           0.68 |                  0.68 |
| PostgreSQL-1-2-3-1 |       177.14 |      3.20 |           0.68 |                  0.68 |
| PostgreSQL-1-2-4-1 |       156.33 |      3.24 |           0.41 |                  0.41 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
