## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1992s 
* Code: 1793571888
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
  * Status is logged every 10ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:688672
  * datadisk:4307
  * volume_size:1.8T
  * volume_used:673G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:698324
  * datadisk:13950
  * volume_size:1.8T
  * volume_used:682G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:688684
  * datadisk:4307
  * volume_size:1.8T
  * volume_used:673G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:706207
  * datadisk:20874
  * volume_size:1.8T
  * volume_used:690G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793571888
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793571888-58864fcd4f-d62gq: 0
* bexhoma-sut-postgresql-1-1793571888-68b5b4f494-c4n7k: 0

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

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       81.00 |           2.00 |            0.00 |         71.00 |            8.00 |              1 |           1 |             |                |             0 | False         |              711.11 | False               |
| PostgreSQL-1-2 |                2 |   16 |       81.00 |           3.00 |            0.00 |         69.00 |            9.00 |              1 |           1 |             |                |             0 | False         |              711.11 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            7 |                        2515.59 |                     2488.51 |         0.00 |                                                      64766.00 |                                              15893.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            6 |                        1349.42 |                     1336.62 |         0.00 |                                                      96944.00 |                                              29618.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |           12 |                        2528.65 |                     2501.41 |         0.00 |                                                      64251.00 |                                              15811.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            6 |                        2515.39 |                     2488.45 |         0.00 |                                                      64840.00 |                                              15894.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            3 |                        1385.60 |                     1368.30 |         0.00 |                                                      36437.00 |                                              14423.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            3 |                        1383.52 |                     1366.43 |         0.00 |                                                      36424.00 |                                              14444.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            7 |                        1387.62 |                     1370.57 |         0.00 |                                                      36398.00 |                                              14401.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            2 |                        1379.10 |                     1361.50 |         0.00 |                                                      36632.00 |                                              14490.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            3 |                        1393.69 |                     1376.28 |         0.00 |                                                      36312.00 |                                              14339.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            7 |                        1392.73 |                     1375.19 |         0.00 |                                                      36334.00 |                                              14349.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            0 |                        1388.05 |                     1370.91 |         0.00 |                                                      36454.00 |                                              14396.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            2 |                        1391.59 |                     1373.58 |         0.00 |                                                      36184.00 |                                              14361.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |           15 |                        3930.25 |                     3882.03 |         0.00 |                                                      30327.00 |                                              10170.00 |
| postgresql-1-2-1-1-2 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |           21 |                        3902.64 |                     3854.40 |         0.00 |                                                      30707.00 |                                              10244.00 |
| postgresql-1-2-1-1-3 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |           28 |                        3902.49 |                     3854.92 |         0.00 |                                                      30629.00 |                                              10245.00 |
| postgresql-1-2-1-1-4 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |           12 |                        3922.52 |                     3873.36 |         0.00 |                                                      30472.00 |                                              10191.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            2 |                        1035.77 |                     1024.55 |         0.00 |                                                      39784.00 |                                              19296.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |           11 |                        1043.82 |                     1032.72 |         0.00 |                                                      39713.00 |                                              19147.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            4 |                        1041.54 |                     1030.10 |         0.00 |                                                      39773.00 |                                              19188.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            5 |                        1043.23 |                     1031.74 |         0.00 |                                                      39758.00 |                                              19158.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            4 |                        1039.68 |                     1028.63 |         0.00 |                                                      39801.00 |                                              19218.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            3 |                        1042.23 |                     1030.95 |         0.00 |                                                      39723.00 |                                              19176.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            6 |                        1042.16 |                     1030.90 |         0.00 |                                                      39633.00 |                                              19177.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            4 |                        1036.67 |                     1025.27 |         0.00 |                                                      40050.00 |                                              19273.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           31 |                        8909.05 |                     8815.00 |         0.00 |                                                      96944.00 |                                              19304.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           27 |                       11101.89 |                    10962.77 |         0.00 |                                                      36632.00 |                                              14400.38 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           76 |                       15657.90 |                    15464.72 |         0.00 |                                                      30707.00 |                                              10212.50 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           39 |                        8325.09 |                     8234.85 |         0.00 |                                                      40050.00 |                                              19204.12 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       129.99 |      2.73 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       129.99 |      2.73 |           2.05 |                  3.69 |
| postgresql-1-2-1-1 |       138.84 |      5.27 |           2.06 |                  3.70 |
| postgresql-1-2-2-1 |       138.84 |      5.27 |           2.06 |                  3.70 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       781.39 |     15.20 |           0.26 |                  0.26 |
| postgresql-1-1-2-1 |       781.39 |     15.20 |           0.26 |                  0.26 |
| postgresql-1-2-1-1 |       477.63 |     14.69 |           0.24 |                  0.24 |
| postgresql-1-2-2-1 |       477.63 |     14.69 |           0.24 |                  0.24 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      5238.72 |     22.33 |           6.98 |                 11.51 |
| postgresql-1-1-2-1 |      5170.85 |     23.42 |          11.65 |                 19.66 |
| postgresql-1-2-1-1 |      5919.25 |     23.78 |           9.21 |                 15.40 |
| postgresql-1-2-2-1 |      3899.39 |     15.96 |          12.14 |                 20.61 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2167.08 |      9.73 |           0.54 |                  0.54 |
| postgresql-1-1-2-1 |      2719.85 |     14.72 |           0.39 |                  0.39 |
| postgresql-1-2-1-1 |      2656.65 |     10.89 |           0.59 |                  0.59 |
| postgresql-1-2-2-1 |      2411.96 |      9.42 |           0.40 |                  0.40 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |
| postgresql-1-1-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   3.00 |                                               3.00 |
| postgresql-1-2-1-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |
| postgresql-1-2-2-1 |                                17.00 |                                                0.00 |                                                        0.00 |                                   9.00 |                                               9.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 4.00 |                                               39.00 |                                                        0.00 |                                 150.00 |                                             150.00 |
| postgresql-1-1-2-1 |                                 7.00 |                                               40.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-1-1 |                                 6.00 |                                               43.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-2-1 |                                10.00 |                                               27.00 |                                                        0.00 |                                 160.00 |                                             160.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
