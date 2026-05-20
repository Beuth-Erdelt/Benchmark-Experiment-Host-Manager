## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2812s 
* Code: 1778695900
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.7.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:201922
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778695900
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:211701
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778695900
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:201924
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778695900
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:212832
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778695900
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      349.00 |           3.00 |            0.00 |        137.00 |          209.00 |              1 |          |                |             0 | False         |              165.04 |
| PostgreSQL-1-2 |                2 |   16 |      347.00 |           2.00 |            0.00 |        138.00 |          207.00 |              1 |          |                |             0 | False         |              165.99 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |        20.00 |                        2395.94 |                     2364.42 |         0.00 |                                                      35453.00 |                                              16686.00 |
| PostgreSQL-1-1-1-2 |             1.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |        10.00 |                        2402.54 |                     2371.14 |         0.00 |                                                      35611.00 |                                              16641.00 |
| PostgreSQL-1-1-1-3 |             1.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         9.00 |                        2405.45 |                     2373.98 |         0.00 |                                                      35619.00 |                                              16620.00 |
| PostgreSQL-1-1-1-4 |             1.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         8.00 |                        2191.93 |                     2163.18 |         0.00 |                                                      38103.00 |                                              18238.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                         582.69 |                      577.10 |         0.00 |                                                      62346.00 |                                              34314.00 |
| PostgreSQL-1-1-2-2 |             1.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         0.00 |                         580.02 |                      574.20 |         0.00 |                                                      62567.00 |                                              34469.00 |
| PostgreSQL-1-1-2-3 |             1.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                         585.24 |                      579.62 |         0.00 |                                                      62127.00 |                                              34165.00 |
| PostgreSQL-1-1-2-4 |             1.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         2.00 |                         580.25 |                      574.70 |         0.00 |                                                      62399.00 |                                              34458.00 |
| PostgreSQL-1-1-2-5 |             1.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         2.00 |                         583.07 |                      577.33 |         0.00 |                                                      62211.00 |                                              34291.00 |
| PostgreSQL-1-1-2-6 |             1.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                         582.17 |                      576.46 |         0.00 |                                                      62408.00 |                                              34345.00 |
| PostgreSQL-1-1-2-7 |             1.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         2.00 |                         581.39 |                      575.70 |         0.00 |                                                      62298.00 |                                              34390.00 |
| PostgreSQL-1-1-2-8 |             1.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         1.00 |                         582.25 |                      576.49 |         0.00 |                                                      62392.00 |                                              34339.00 |
| PostgreSQL-1-2-1-1 |             2.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |        21.00 |                        2511.64 |                     2477.00 |         0.00 |                                                      34709.00 |                                              15918.00 |
| PostgreSQL-1-2-1-2 |             2.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |        15.00 |                        2535.04 |                     2500.08 |         0.00 |                                                      34330.00 |                                              15771.00 |
| PostgreSQL-1-2-1-3 |             2.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         5.00 |                        2563.74 |                     2528.07 |         0.00 |                                                      34643.00 |                                              15594.00 |
| PostgreSQL-1-2-1-4 |             2.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         5.00 |                        2521.28 |                     2486.01 |         0.00 |                                                      34997.00 |                                              15855.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         2.00 |                         815.39 |                      806.06 |         0.00 |                                                      48370.00 |                                              24519.00 |
| PostgreSQL-1-2-2-2 |             2.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         5.00 |                         812.99 |                      803.30 |         0.00 |                                                      48708.00 |                                              24590.00 |
| PostgreSQL-1-2-2-3 |             2.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                         821.62 |                      812.21 |         0.00 |                                                      48428.00 |                                              24333.00 |
| PostgreSQL-1-2-2-4 |             2.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         2.00 |                         817.36 |                      807.98 |         0.00 |                                                      48260.00 |                                              24459.00 |
| PostgreSQL-1-2-2-5 |             2.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         3.00 |                         815.30 |                      805.56 |         0.00 |                                                      48579.00 |                                              24521.00 |
| PostgreSQL-1-2-2-6 |             2.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                         816.55 |                      806.74 |         0.00 |                                                      48674.00 |                                              24484.00 |
| PostgreSQL-1-2-2-7 |             2.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         2.00 |                         817.16 |                      807.69 |         0.00 |                                                      48376.00 |                                              24465.00 |
| PostgreSQL-1-2-2-8 |             2.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         1.00 |                         816.90 |                      807.09 |         0.00 |                                                      48664.00 |                                              24472.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |      160.00 | 20480.00 |        4.00 | 300.00 |        47.00 |                        9395.87 |                     9272.72 |         0.00 |                                                      38103.00 |                                              17046.25 |
| PostgreSQL-1-1-2 |             1.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         7.00 |                        4657.09 |                     4611.60 |         0.00 |                                                      62567.00 |                                              34346.38 |
| PostgreSQL-1-2-1 |             2.00 |      160.00 | 20480.00 |        4.00 | 300.00 |        46.00 |                       10131.70 |                     9991.15 |         0.00 |                                                      34997.00 |                                              15784.50 |
| PostgreSQL-1-2-2 |             2.00 |      160.00 | 20480.00 |        8.00 | 300.00 |        15.00 |                        6533.26 |                     6456.62 |         0.00 |                                                      48708.00 |                                              24480.38 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       411.56 |      4.24 |           7.41 |                  9.05 |
| PostgreSQL-1-1-2 |       411.56 |      4.24 |           7.41 |                  9.05 |
| PostgreSQL-1-2-1 |     13226.69 |      4.17 |          11.85 |                 17.81 |
| PostgreSQL-1-2-2 |     13226.69 |      4.17 |          11.85 |                 17.81 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1585.39 |     14.77 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2 |      1585.39 |     14.77 |           0.25 |                  0.25 |
| PostgreSQL-1-2-1 |      1611.03 |     14.57 |           0.25 |                  0.25 |
| PostgreSQL-1-2-2 |      1611.03 |     14.57 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      6011.80 |     23.29 |          12.99 |                 17.64 |
| PostgreSQL-1-1-2 |      6254.08 |     21.05 |          14.64 |                 20.58 |
| PostgreSQL-1-2-1 |      5710.99 |     23.77 |          13.37 |                 18.31 |
| PostgreSQL-1-2-2 |      6210.80 |     25.62 |          15.89 |                 22.75 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      4572.77 |     18.91 |           0.42 |                  0.42 |
| PostgreSQL-1-1-2 |      4381.00 |     20.69 |           0.42 |                  0.42 |
| PostgreSQL-1-2-1 |      4922.21 |     19.57 |           0.42 |                  0.42 |
| PostgreSQL-1-2-2 |      4593.63 |     30.20 |           0.42 |                  0.42 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   11.00 |
| PostgreSQL-1-1-2 |                     16.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   11.00 |
| PostgreSQL-1-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   10.00 |
| PostgreSQL-1-2-2 |                     17.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   10.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      7.00 |                                    51.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-1-2 |                      2.00 |                                    22.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-2-1 |                      5.00 |                                    56.00 |                                             0.00 |                      143.00 |                                  143.00 |
| PostgreSQL-1-2-2 |                     21.00 |                                    35.00 |                                             0.00 |                      157.00 |                                  157.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
