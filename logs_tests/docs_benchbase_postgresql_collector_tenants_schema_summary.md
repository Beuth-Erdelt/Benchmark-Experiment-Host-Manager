## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2391s 
* Code: 1781965171
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type cephcsi and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1323186
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781965171
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324396
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781965171
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1323168
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781965171
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1323158
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781965171
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781965171-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    1 |      137.00 |           2.00 |            0.00 |        137.00 |          185.00 |              2 |           1 |               26.28 |
| 1781965171-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    1 |      136.00 |           2.00 |            0.00 |        136.00 |          185.00 |              2 |           1 |               26.47 |
| 1781965171-PostgreSQL-1-2-0 |                2 | schema         | False         |             2 |           0 |    1 |      137.00 |           2.00 |            0.00 |        137.00 |          185.00 |              2 |           1 |               26.28 |
| 1781965171-PostgreSQL-1-2-1 |                2 | schema         | False         |             2 |           1 |    1 |      136.00 |           2.00 |            0.00 |        136.00 |          185.00 |              2 |           1 |               26.47 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                      78542.00 |                                              29969.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.44 |                        0.43 |        90.28 |                                                      79498.00 |                                              32454.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.44 |                        0.44 |        93.08 |                                                      26999.00 |                                              12835.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.98 |                                                      57708.00 |                                              15838.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        99.38 |                                                     475392.00 |                                             146520.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.47 |                        0.47 |        97.98 |                                                     303542.00 |                                             110335.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        97.98 |                                                     160663.00 |                                              61604.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       109.88 |                                                     133744.00 |                                              54965.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-0 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                      78542.00 |                                              29969.00 |
| PostgreSQL-1-1-1-1 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.44 |                        0.43 |        90.28 |                                                      79498.00 |                                              32454.00 |
| PostgreSQL-1-1-2-0 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.44 |                        0.44 |        93.08 |                                                      26999.00 |                                              12835.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.98 |                                                      57708.00 |                                              15838.00 |
| PostgreSQL-1-2-1-0 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        99.38 |                                                     475392.00 |                                             146520.00 |
| PostgreSQL-1-2-1-1 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.47 |                        0.47 |        97.98 |                                                     303542.00 |                                             110335.00 |
| PostgreSQL-1-2-2-0 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        97.98 |                                                     160663.00 |                                              61604.00 |
| PostgreSQL-1-2-2-1 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       109.88 |                                                     133744.00 |                                              54965.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        43.42 |      0.35 |           0.62 |                  0.88 |
| PostgreSQL-1-1-2-1 |        43.42 |      0.35 |           0.62 |                  0.88 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        16.25 |      0.21 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |        16.25 |      0.21 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         2.25 |      0.01 |           0.69 |                  0.95 |
| PostgreSQL-1-1-2-1 |         2.56 |      0.01 |           0.69 |                  0.95 |
| PostgreSQL-1-2-1-1 |        53.13 |      0.02 |           0.62 |                  0.87 |
| PostgreSQL-1-2-2-1 |         2.85 |      0.02 |           0.50 |                  0.57 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        34.57 |      0.68 |           0.23 |                  0.23 |
| PostgreSQL-1-1-2-1 |        84.22 |      1.30 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1-1 |       161.19 |      2.01 |           0.23 |                  0.23 |
| PostgreSQL-1-2-2-1 |       165.82 |      2.06 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-1-1-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-2-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-2-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
