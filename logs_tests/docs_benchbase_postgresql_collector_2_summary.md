## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1880s 
* Code: 1793569963
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
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
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
  * disk:684465
  * datadisk:4307
  * volume_size:98G
  * volume_used:4.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684465
  * datadisk:17996
  * volume_size:98G
  * volume_used:18G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:684446
  * datadisk:27454
  * volume_size:98G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:683652
  * datadisk:28882
  * volume_size:98G
  * volume_used:29G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793569963
    * TENANT_VOL:False

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793569963-7d87688db6-p7hrj: 0
* bexhoma-sut-postgresql-1-1793569963-64fcdc66-b4rcl: 0

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
| PostgreSQL-1-1 |                1 |   16 |       85.00 |           4.00 |            0.00 |         71.00 |           10.00 |              1 |           1 |             |                |             0 | False         |              677.65 | False               |
| PostgreSQL-1-2 |                2 |   16 |       85.00 |           4.00 |            0.00 |         71.00 |           10.00 |              1 |           1 |             |                |             0 | False         |              677.65 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            6 |                        2869.34 |                     2836.70 |         0.00 |                                                      46570.00 |                                              13932.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |           10 |                        2890.55 |                     2857.99 |         0.00 |                                                      46508.00 |                                              13829.00 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            9 |                        2869.04 |                     2836.76 |         0.00 |                                                      46711.00 |                                              13933.00 |
| postgresql-1-1-1-1-4 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            6 |                        2866.33 |                     2833.85 |         0.00 |                                                      46815.00 |                                              13946.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            2 |                         887.66 |                      878.35 |         0.00 |                                                      48879.00 |                                              22516.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            1 |                         892.16 |                      882.94 |         0.00 |                                                      48586.00 |                                              22403.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            2 |                         889.74 |                      880.83 |         0.00 |                                                      48806.00 |                                              22464.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            0 |                         887.54 |                      878.35 |         0.00 |                                                      49027.00 |                                              22519.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            5 |                         889.51 |                      880.27 |         0.00 |                                                      48845.00 |                                              22468.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            2 |                         887.85 |                      878.91 |         0.00 |                                                      49103.00 |                                              22511.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            4 |                         885.49 |                      876.65 |         0.00 |                                                      48762.00 |                                              22571.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            0 |                         887.81 |                      878.61 |         0.00 |                                                      48735.00 |                                              22512.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 |           0 | 300.00 |            0 |                        1418.63 |                     1406.41 |         0.00 |                                                      51902.00 |                                              28182.00 |
| postgresql-1-2-1-1-2 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 |           0 | 300.00 |            0 |                        1431.51 |                     1418.49 |         0.00 |                                                      51742.00 |                                              27929.00 |
| postgresql-1-2-1-1-3 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 |           0 | 300.00 |            2 |                        1422.33 |                     1409.73 |         0.00 |                                                      51870.00 |                                              28110.00 |
| postgresql-1-2-1-1-4 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 |           0 | 300.00 |            3 |                        1419.57 |                     1406.85 |         0.00 |                                                      51864.00 |                                              28164.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 |           0 | 300.00 |            0 |                         615.19 |                      609.68 |         0.00 |                                                      59721.00 |                                              32491.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 |           0 | 300.00 |            2 |                         618.65 |                      613.19 |         0.00 |                                                      59591.00 |                                              32308.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 |           0 | 300.00 |            1 |                         615.64 |                      610.16 |         0.00 |                                                      59781.00 |                                              32467.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 |           0 | 300.00 |            2 |                         614.65 |                      609.12 |         0.00 |                                                      59591.00 |                                              32518.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 |           0 | 300.00 |            0 |                         617.72 |                      612.10 |         0.00 |                                                      59637.00 |                                              32357.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 |           0 | 300.00 |            0 |                         616.46 |                      610.74 |         0.00 |                                                      59580.00 |                                              32425.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 |           0 | 300.00 |            0 |                         617.77 |                      612.05 |         0.00 |                                                      59535.00 |                                              32356.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 |           0 | 300.00 |            3 |                         615.26 |                      609.67 |         0.00 |                                                      59758.00 |                                              32486.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    20480 |               1 |           4 |           0 | 300.00 |           31 |                       11495.26 |                    11365.30 |         0.00 |                                                      46815.00 |                                              13910.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    20480 |               1 |           8 |           0 | 300.00 |           16 |                        7107.76 |                     7034.90 |         0.00 |                                                      49103.00 |                                              22495.50 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |         160 |    20480 |               1 |           4 |           0 | 300.00 |            5 |                        5692.04 |                     5641.48 |         0.00 |                                                      51902.00 |                                              28096.25 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |         160 |    20480 |               1 |           8 |           0 | 300.00 |            8 |                        4931.34 |                     4886.71 |         0.00 |                                                      59781.00 |                                              32426.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       134.87 |      3.32 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       134.87 |      3.32 |           2.05 |                  3.69 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       837.51 |     14.57 |           0.26 |                  0.26 |
| postgresql-1-1-2-1 |       837.51 |     14.57 |           0.26 |                  0.26 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      4513.45 |     18.42 |           8.81 |                 14.70 |
| postgresql-1-1-2-1 |      3817.53 |     16.79 |          11.58 |                 19.57 |
| postgresql-1-2-1-1 |      3019.71 |     12.39 |           6.96 |                 11.68 |
| postgresql-1-2-2-1 |      2551.53 |     10.94 |           9.29 |                 16.01 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2449.81 |     10.44 |           0.58 |                  0.58 |
| postgresql-1-1-2-1 |      2158.64 |      9.66 |           0.37 |                  0.37 |
| postgresql-1-2-1-1 |      1841.50 |      8.26 |           0.46 |                  0.46 |
| postgresql-1-2-2-1 |      1715.07 |      6.40 |           0.37 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
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

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                39.00 |                                               31.00 |                                                        0.00 |                                 159.00 |                                             159.00 |
| postgresql-1-1-2-1 |                                 8.00 |                                               26.00 |                                                        0.00 |                                 160.00 |                                             160.00 |
| postgresql-1-2-1-1 |                                 9.00 |                                               22.00 |                                                        0.00 |                                 156.00 |                                             156.00 |
| postgresql-1-2-2-1 |                                 6.00 |                                               23.00 |                                                        0.00 |                                 155.00 |                                             155.00 |

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
