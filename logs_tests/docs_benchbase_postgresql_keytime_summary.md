## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 12976s 
* Code: 1787832981
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Experiment uses bexhoma version 0.10.13.
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
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_connections'}, '2000')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:373255
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:378333
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False
* postgresql-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:383492
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False
* postgresql-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:389435
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1787832981-cb75b5795-rwh9t: 0 0

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
| PostgreSQL-1-1 |                1 |  160 |     8665.00 |           1.00 |            0.00 |       4096.00 |         4568.00 |              1 |           1 |             |                |             0 | False         |               66.47 |

### Benchmarking

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1  | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1600 |     1024 |        1 |               1 |       1 |           0 | 1800.00 |            0 |                          75.90 |                       75.57 |        99.17 |                                                     548400.00 |                                             133666.00 |
| postgresql-1-1-2-1-1  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       1 |           0 | 1800.00 |            0 |                          37.88 |                       37.72 |        49.50 |                                                     638914.00 |                                             163413.00 |
| postgresql-1-1-2-1-2  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       2 |           0 | 1800.00 |            0 |                          37.97 |                       37.79 |        49.59 |                                                     626171.00 |                                             161275.00 |
| postgresql-1-1-3-1-1  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       1 |           0 | 1800.00 |            0 |                          15.23 |                       15.16 |        19.90 |                                                     637663.00 |                                             163128.00 |
| postgresql-1-1-3-1-2  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       2 |           0 | 1800.00 |            0 |                          15.36 |                       15.30 |        20.08 |                                                     608247.00 |                                             160115.00 |
| postgresql-1-1-3-1-3  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       3 |           0 | 1800.00 |            0 |                          15.22 |                       15.15 |        19.88 |                                                     620403.00 |                                             158827.00 |
| postgresql-1-1-3-1-4  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       4 |           0 | 1800.00 |            0 |                          15.02 |                       14.95 |        19.61 |                                                     648646.00 |                                             163488.00 |
| postgresql-1-1-3-1-5  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       5 |           0 | 1800.00 |            0 |                          15.20 |                       15.13 |        19.86 |                                                     627734.00 |                                             161776.00 |
| postgresql-1-1-4-1-1  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       1 |           0 | 1800.00 |            0 |                           7.50 |                        7.46 |         9.79 |                                                     707969.00 |                                             185400.00 |
| postgresql-1-1-4-1-2  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       2 |           0 | 1800.00 |            0 |                           7.60 |                        7.57 |         9.93 |                                                     710168.00 |                                             186289.00 |
| postgresql-1-1-4-1-3  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       3 |           0 | 1800.00 |            0 |                           7.55 |                        7.51 |         9.86 |                                                     725065.00 |                                             187981.00 |
| postgresql-1-1-4-1-4  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       4 |           0 | 1800.00 |            0 |                           7.55 |                        7.51 |         9.86 |                                                     707896.00 |                                             183602.00 |
| postgresql-1-1-4-1-5  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       5 |           0 | 1800.00 |            0 |                           7.53 |                        7.49 |         9.83 |                                                     690508.00 |                                             183456.00 |
| postgresql-1-1-4-1-6  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       6 |           0 | 1800.00 |            0 |                           7.57 |                        7.54 |         9.89 |                                                     713480.00 |                                             185164.00 |
| postgresql-1-1-4-1-7  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       7 |           0 | 1800.00 |            0 |                           7.55 |                        7.50 |         9.85 |                                                     711451.00 |                                             185728.00 |
| postgresql-1-1-4-1-8  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       8 |           0 | 1800.00 |            0 |                           7.57 |                        7.54 |         9.90 |                                                     719171.00 |                                             188075.00 |
| postgresql-1-1-4-1-9  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       9 |           0 | 1800.00 |            0 |                           7.51 |                        7.47 |         9.81 |                                                     707870.00 |                                             184112.00 |
| postgresql-1-1-4-1-10 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |      10 |           0 | 1800.00 |            0 |                           7.51 |                        7.48 |         9.81 |                                                     693735.00 |                                             183244.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1600 |     1024 |               1 |           1 |           0 | 1800.00 |            0 |                          75.90 |                       75.57 |        99.17 |                                                     548400.00 |                                             133666.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        1600 |     1024 |               1 |           2 |           0 | 1800.00 |            0 |                          75.85 |                       75.52 |        99.09 |                                                     638914.00 |                                             162344.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        1600 |     1020 |               1 |           5 |           0 | 1800.00 |            0 |                          76.03 |                       75.70 |        99.33 |                                                     648646.00 |                                             161466.80 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        1600 |     1020 |               1 |          10 |           0 | 1800.00 |            0 |                          75.43 |                       75.09 |        98.53 |                                                     725065.00 |                                             185305.10 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |
| postgresql-1-1-2-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |
| postgresql-1-1-3-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |
| postgresql-1-1-4-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |
| postgresql-1-1-2-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |
| postgresql-1-1-3-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |
| postgresql-1-1-4-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       396.80 |      4.12 |          26.06 |                 42.33 |
| postgresql-1-1-2-1 |       269.93 |      0.31 |          26.11 |                 42.59 |
| postgresql-1-1-3-1 |       278.01 |      0.40 |          26.80 |                 43.47 |
| postgresql-1-1-4-1 |       288.97 |      0.50 |          27.41 |                 44.27 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       387.23 |      2.10 |           4.18 |                  4.18 |
| postgresql-1-1-2-1 |       387.23 |      2.84 |           4.02 |                  4.02 |
| postgresql-1-1-3-1 |       568.38 |      5.33 |           2.48 |                  2.48 |
| postgresql-1-1-4-1 |       775.40 |      9.39 |           1.17 |                  1.17 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
