## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2383s 
* Code: 1781948898
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
  * disk:1328470
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781948898
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1338106
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781948898
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1327509
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781948898
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1335263
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781948898
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
| PostgreSQL-1-1 |                1 |   16 |      204.00 |           1.00 |            0.00 |         84.00 |          119.00 |              1 |           1 |             |                |             0 | False         |              282.35 |
| PostgreSQL-1-2 |                2 |   16 |      331.00 |           1.00 |            0.00 |        154.00 |          176.00 |              1 |           1 |             |                |             0 | False         |              174.02 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |           10 |                        2394.66 |                     2360.52 |         0.00 |                                                      50271.00 |                                              16694.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            8 |                        2383.67 |                     2349.86 |         0.00 |                                                      50805.00 |                                              16770.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            9 |                        2423.09 |                     2388.39 |         0.00 |                                                      49498.00 |                                              16498.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |           12 |                        2396.24 |                     2361.57 |         0.00 |                                                      49901.00 |                                              16683.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |           12 |                        1058.63 |                     1042.72 |         0.00 |                                                      50045.00 |                                              18882.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            1 |                        1063.77 |                     1047.46 |         0.00 |                                                      50120.00 |                                              18790.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            3 |                        1066.78 |                     1050.53 |         0.00 |                                                      49986.00 |                                              18738.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            7 |                        1056.03 |                     1040.10 |         0.00 |                                                      50438.00 |                                              18928.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            3 |                        1060.69 |                     1044.95 |         0.00 |                                                      50036.00 |                                              18842.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            9 |                        1077.56 |                     1061.02 |         0.00 |                                                      49590.00 |                                              18551.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            6 |                        1067.93 |                     1051.63 |         0.00 |                                                      49355.00 |                                              18717.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            7 |                        1070.23 |                     1053.41 |         0.00 |                                                      49850.00 |                                              18676.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            9 |                        2122.67 |                     2097.23 |         0.00 |                                                      69069.00 |                                              18835.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            4 |                        1299.00 |                     1284.53 |         0.00 |                                                      92628.00 |                                              30778.00 |
| PostgreSQL-1-2-1-1-3 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            6 |                        2153.06 |                     2127.30 |         0.00 |                                                      68735.00 |                                              18570.00 |
| PostgreSQL-1-2-1-1-4 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            7 |                        2111.41 |                     2086.29 |         0.00 |                                                      69009.00 |                                              18937.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            4 |                        1134.60 |                     1116.74 |         0.00 |                                                      48578.00 |                                              17617.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            6 |                        1159.87 |                     1141.48 |         0.00 |                                                      47888.00 |                                              17234.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            3 |                        1139.74 |                     1121.85 |         0.00 |                                                      48580.00 |                                              17537.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            5 |                        1150.27 |                     1132.23 |         0.00 |                                                      47742.00 |                                              17378.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |           10 |                        1157.31 |                     1139.23 |         0.00 |                                                      47671.00 |                                              17271.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            7 |                        1139.57 |                     1121.72 |         0.00 |                                                      49603.00 |                                              17540.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            3 |                        1154.21 |                     1136.75 |         0.00 |                                                      48064.00 |                                              17318.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            6 |                        1127.96 |                     1109.93 |         0.00 |                                                      49300.00 |                                              17721.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           39 |                        9597.66 |                     9460.33 |         0.00 |                                                      50805.00 |                                              16661.25 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           48 |                        8521.60 |                     8391.82 |         0.00 |                                                      50438.00 |                                              18765.50 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           26 |                        7686.14 |                     7595.34 |         0.00 |                                                      92628.00 |                                              21780.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           44 |                        9163.53 |                     9019.92 |         0.00 |                                                      49603.00 |                                              17452.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       145.35 |      2.35 |           2.05 |                  3.69 |
| PostgreSQL-1-1-2-1 |       145.35 |      2.35 |           2.05 |                  3.69 |
| PostgreSQL-1-2-1-1 |      7980.67 |      3.57 |           7.52 |                 14.44 |
| PostgreSQL-1-2-2-1 |      7980.67 |      3.57 |           7.52 |                 14.44 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       564.02 |     12.96 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2-1 |       564.02 |     12.96 |           0.26 |                  0.26 |
| PostgreSQL-1-2-1-1 |      1919.37 |     15.53 |           0.27 |                  0.27 |
| PostgreSQL-1-2-2-1 |      1919.37 |     15.53 |           0.27 |                  0.27 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3256.32 |     12.68 |           6.65 |                 10.92 |
| PostgreSQL-1-1-2-1 |      4144.77 |     14.95 |          10.17 |                 17.06 |
| PostgreSQL-1-2-1-1 |      4667.84 |     17.80 |           6.16 |                 10.08 |
| PostgreSQL-1-2-2-1 |      4050.91 |     14.89 |           9.69 |                 16.26 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      5026.62 |     18.83 |           0.43 |                  0.43 |
| PostgreSQL-1-1-2-1 |      4945.37 |     35.49 |           0.43 |                  0.43 |
| PostgreSQL-1-2-1-1 |      3473.40 |     16.70 |           0.42 |                  0.42 |
| PostgreSQL-1-2-2-1 |      2972.21 |     27.16 |           0.42 |                  0.42 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |
| PostgreSQL-1-2-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   13.00 |
| PostgreSQL-1-2-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   13.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      9.00 |                                    54.00 |                                             0.00 |                      157.00 |                                  157.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                    55.00 |                                             0.00 |                      157.00 |                                  158.00 |
| PostgreSQL-1-2-1-1 |                      7.00 |                                    47.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-2-1 |                      7.00 |                                    54.00 |                                             0.00 |                      160.00 |                                  160.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
