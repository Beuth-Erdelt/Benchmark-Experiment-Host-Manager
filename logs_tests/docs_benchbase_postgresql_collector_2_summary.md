## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2469s 
* Code: 1781946398
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type cephcsi and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1300641
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946398
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324147
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946398
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324154
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946398
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324191
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946398
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              1 |           1 |             |                |             0 | False         |               76.90 |
| PostgreSQL-1-2 |                2 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              1 |           1 |             |                |             0 | False         |               76.90 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            1 |                         258.69 |                      256.71 |         0.00 |                                                     648544.00 |                                             154479.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            1 |                         256.22 |                      254.13 |         0.00 |                                                     654097.00 |                                             155983.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            2 |                         255.59 |                      253.53 |         0.00 |                                                     663236.00 |                                             156487.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            0 |                         257.01 |                      255.07 |         0.00 |                                                     658256.00 |                                             155501.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            0 |                         162.50 |                      160.97 |         0.00 |                                                     486458.00 |                                             122961.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            0 |                         156.52 |                      155.18 |         0.00 |                                                     509817.00 |                                             127737.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            0 |                         159.07 |                      157.77 |         0.00 |                                                     501836.00 |                                             125464.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            0 |                         161.34 |                      159.94 |         0.00 |                                                     492330.00 |                                             123922.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            2 |                         158.77 |                      157.28 |         0.00 |                                                     499356.00 |                                             125821.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            1 |                         155.79 |                      154.43 |         0.00 |                                                     509814.00 |                                             128328.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            2 |                         159.45 |                      157.95 |         0.00 |                                                     500457.00 |                                             125385.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            0 |                         159.28 |                      157.94 |         0.00 |                                                     496603.00 |                                             125477.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            0 |                         250.53 |                      248.29 |         0.00 |                                                     641790.00 |                                             159420.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            0 |                         249.65 |                      247.43 |         0.00 |                                                     645849.00 |                                             159962.00 |
| PostgreSQL-1-2-1-1-3 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            1 |                         251.71 |                      249.51 |         0.00 |                                                     642326.00 |                                             158637.00 |
| PostgreSQL-1-2-1-1-4 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            0 |                         251.63 |                      249.49 |         0.00 |                                                     645227.00 |                                             158674.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            0 |                         152.21 |                      150.71 |         0.00 |                                                     523425.00 |                                             131372.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            0 |                         151.42 |                      149.91 |         0.00 |                                                     525007.00 |                                             132001.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            1 |                         153.37 |                      151.91 |         0.00 |                                                     516741.00 |                                             130355.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            0 |                         150.39 |                      149.02 |         0.00 |                                                     524000.00 |                                             132908.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            0 |                         152.05 |                      150.71 |         0.00 |                                                     527355.00 |                                             131444.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            0 |                         152.11 |                      150.53 |         0.00 |                                                     525382.00 |                                             131413.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            0 |                         150.96 |                      149.56 |         0.00 |                                                     533427.00 |                                             132367.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            0 |                         151.96 |                      150.48 |         0.00 |                                                     535277.00 |                                             131562.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    20480 |               1 |           4 |           0 | 300.00 |            4 |                        1027.51 |                     1019.43 |         0.00 |                                                     663236.00 |                                             155612.50 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    20480 |               1 |           8 |           0 | 300.00 |            5 |                        1272.71 |                     1261.46 |         0.00 |                                                     509817.00 |                                             125636.88 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |    20480 |               1 |           4 |           0 | 300.00 |            1 |                        1003.52 |                      994.71 |         0.00 |                                                     645849.00 |                                             159173.25 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         160 |    20480 |               1 |           8 |           0 | 300.00 |            1 |                        1214.47 |                     1202.83 |         0.00 |                                                     535277.00 |                                             131677.75 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       184.47 |      0.86 |           2.14 |                  3.72 |
| PostgreSQL-1-1-2-1 |       184.47 |      0.86 |           2.14 |                  3.72 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1638.57 |      9.29 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |      1638.57 |      9.29 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       398.94 |      2.08 |           3.50 |                  5.50 |
| PostgreSQL-1-1-2-1 |       502.62 |      2.14 |           4.10 |                  6.56 |
| PostgreSQL-1-2-1-1 |      1196.20 |      1.93 |           3.07 |                  5.44 |
| PostgreSQL-1-2-2-1 |       538.20 |      2.15 |           4.05 |                  6.47 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       490.38 |      2.87 |           0.35 |                  0.35 |
| PostgreSQL-1-1-2-1 |       439.79 |      4.21 |           0.35 |                  0.35 |
| PostgreSQL-1-2-1-1 |       420.17 |      2.08 |           0.33 |                  0.33 |
| PostgreSQL-1-2-2-1 |       416.33 |      5.42 |           0.33 |                  0.33 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |
| PostgreSQL-1-1-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     24.00 |                                    28.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-1-2-1 |                     18.00 |                                    31.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-1-1 |                      3.00 |                                    19.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-2-1 |                     15.00 |                                    20.00 |                                             0.00 |                      160.00 |                                  160.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
