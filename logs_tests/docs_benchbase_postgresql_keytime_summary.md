## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 10548s 
* Code: 1785156246
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Experiment uses bexhoma version 0.10.8.
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
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808270
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1785156246
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811325
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1785156246
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825456
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1785156246
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:816715
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1785156246
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785156246-6f9c7f58df-tt92m: 0 0

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
| PostgreSQL-1-1 |                1 |  160 |     4401.00 |           1.00 |            0.00 |       2101.00 |         2299.00 |              1 |           1 |             |                |             0 | False         |              130.88 |

### Execution

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1600 |     1024 |        1 |               1 |       1 |           0 | 1800.00 |            1 |                          74.15 |                       73.79 |        96.83 |                                                    4215672.00 |                                             670873.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       1 |           0 | 1800.00 |            0 |                          37.66 |                       37.48 |        49.18 |                                                     109148.00 |                                             239824.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       2 |           0 | 1800.00 |            0 |                          37.84 |                       37.67 |        49.44 |                                                     109805.00 |                                             243248.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       1 |           0 | 1800.00 |            0 |                          15.25 |                       15.18 |        19.91 |                                                     118649.00 |                                              38459.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       2 |           0 | 1800.00 |            0 |                          15.22 |                       15.16 |        19.90 |                                                     122191.00 |                                              39408.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       3 |           0 | 1800.00 |            0 |                          15.22 |                       15.15 |        19.88 |                                                     123670.00 |                                              39121.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       4 |           0 | 1800.00 |            0 |                          15.38 |                       15.31 |        20.10 |                                                     121402.00 |                                              39175.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       5 |           0 | 1800.00 |            0 |                          15.18 |                       15.10 |        19.82 |                                                     124310.00 |                                              39896.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       1 |           0 | 1800.00 |            0 |                           7.65 |                        7.63 |        10.01 |                                                     108627.00 |                                              34411.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       2 |           0 | 1800.00 |            0 |                           7.65 |                        7.62 |         9.99 |                                                     109474.00 |                                              34385.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       3 |           0 | 1800.00 |            0 |                           7.57 |                        7.54 |         9.89 |                                                     106777.00 |                                              34275.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       4 |           0 | 1800.00 |            0 |                           7.67 |                        7.63 |        10.02 |                                                     107368.00 |                                              34073.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       5 |           0 | 1800.00 |            0 |                           7.62 |                        7.58 |         9.95 |                                                     107807.00 |                                              34078.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       6 |           0 | 1800.00 |            0 |                           7.58 |                        7.55 |         9.90 |                                                     108086.00 |                                              34521.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       7 |           0 | 1800.00 |            0 |                           7.60 |                        7.56 |         9.93 |                                                     106883.00 |                                              34177.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       8 |           0 | 1800.00 |            0 |                           7.65 |                        7.62 |        10.00 |                                                     109114.00 |                                              34266.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       9 |           0 | 1800.00 |            0 |                           7.60 |                        7.57 |         9.94 |                                                     106716.00 |                                              34447.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |      10 |           0 | 1800.00 |            0 |                           7.62 |                        7.59 |         9.96 |                                                     108223.00 |                                              34485.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1600 |     1024 |               1 |           1 |           0 | 1800.00 |            1 |                          74.15 |                       73.79 |        96.83 |                                                    4215672.00 |                                             670873.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        1600 |     1024 |               1 |           2 |           0 | 1800.00 |            0 |                          75.50 |                       75.15 |        98.62 |                                                     109805.00 |                                             241536.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        1600 |     1020 |               1 |           5 |           0 | 1800.00 |            0 |                          76.25 |                       75.91 |        99.61 |                                                     124310.00 |                                              39211.80 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        1600 |     1020 |               1 |          10 |           0 | 1800.00 |            0 |                          76.22 |                       75.89 |        99.58 |                                                     109474.00 |                                              34311.80 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1521.61 |      1.36 |          16.60 |                 32.55 |
| PostgreSQL-1-1-2-1 |      1521.61 |      1.36 |          16.60 |                 32.55 |
| PostgreSQL-1-1-3-1 |      1521.61 |      1.36 |          16.60 |                 32.55 |
| PostgreSQL-1-1-4-1 |      1521.61 |      1.36 |          16.60 |                 32.55 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |     20190.69 |     24.71 |           0.31 |                  0.31 |
| PostgreSQL-1-1-2-1 |     20190.69 |     24.71 |           0.31 |                  0.31 |
| PostgreSQL-1-1-3-1 |     20190.69 |     24.71 |           0.31 |                  0.31 |
| PostgreSQL-1-1-4-1 |     20190.69 |     24.71 |           0.31 |                  0.31 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       287.08 |      0.37 |          25.88 |                 42.15 |
| PostgreSQL-1-1-2-1 |       280.22 |      0.51 |          26.04 |                 42.52 |
| PostgreSQL-1-1-3-1 |       304.83 |      0.41 |          26.74 |                 43.42 |
| PostgreSQL-1-1-4-1 |       299.30 |      0.34 |          27.33 |                 44.20 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       398.61 |      1.92 |           4.12 |                  4.12 |
| PostgreSQL-1-1-2-1 |       398.61 |      3.17 |           3.97 |                  3.97 |
| PostgreSQL-1-1-3-1 |       592.41 |      5.31 |           2.45 |                  2.45 |
| PostgreSQL-1-1-4-1 |       881.95 |     10.02 |           1.17 |                  1.17 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
