## Show Summary

### Workload
Benchbase Workload twitter SF=1600
* Type: benchbase
* Duration: 5416s 
* Code: 1792720400
* Benchbase runs the Twitter benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'twitter'. Scaling factor is 1600. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker37.
  * Database is persisted to disk of type nvme and size 1600Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:402952
  * datadisk:39
  * volume_size:1.6T
  * volume_used:39M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720400
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:402985
  * datadisk:39
  * volume_size:1.6T
  * volume_used:39M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720400
    * TENANT_VOL:False
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:402991
  * datadisk:39
  * volume_size:1.6T
  * volume_used:39M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720400
    * TENANT_VOL:False
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:403006
  * datadisk:39
  * volume_size:1.6T
  * volume_used:39M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720400
    * TENANT_VOL:False

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: PostgreSQL-1

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792720400-5dbf9f7cb6-xkwl6: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 | 1600 |       10.00 |          10.00 |            0.00 |          0.00 |            0.00 |              0 |           1 |             |                |             0 | False         |           576000.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 1200.00 |            0 |                        5653.46 |                        0.00 |         0.00 |                                                      98275.00 |                                              28295.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 1200.00 |            0 |                        6727.92 |                        0.00 |         0.00 |                                                      32186.00 |                                              11810.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 1200.00 |            0 |                        6626.80 |                        0.00 |         0.00 |                                                      32399.00 |                                              12001.00 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       1 |           0 | 1200.00 |            0 |                        4096.00 |                        0.00 |         0.00 |                                                        743.00 |                                                546.00 |
| postgresql-1-1-3-1-2 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       2 |           0 | 1200.00 |            0 |                        4096.00 |                        0.00 |         0.00 |                                                        801.00 |                                                562.00 |
| postgresql-1-1-3-1-3 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       3 |           0 | 1200.00 |            0 |                        4096.00 |                        0.00 |         0.00 |                                                       1116.00 |                                                676.00 |
| postgresql-1-1-3-1-4 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          40 |     4096 |        3 |               1 |       4 |           0 | 1200.00 |            0 |                        4096.01 |                        0.00 |         0.00 |                                                       1176.00 |                                                656.00 |
| postgresql-1-1-4-1-1 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       1 |           0 | 1200.00 |            0 |                        2048.01 |                        0.00 |         0.00 |                                                        690.00 |                                                508.00 |
| postgresql-1-1-4-1-2 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       2 |           0 | 1200.00 |            0 |                        2048.01 |                        0.00 |         0.00 |                                                       1028.00 |                                                555.00 |
| postgresql-1-1-4-1-3 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       3 |           0 | 1200.00 |            0 |                        2048.00 |                        0.00 |         0.00 |                                                        704.00 |                                                518.00 |
| postgresql-1-1-4-1-4 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       4 |           0 | 1200.00 |            0 |                        2048.01 |                        0.00 |         0.00 |                                                        726.00 |                                                527.00 |
| postgresql-1-1-4-1-5 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       5 |           0 | 1200.00 |         9101 |                        2048.01 |                        0.00 |         0.00 |                                                        688.00 |                                                503.00 |
| postgresql-1-1-4-1-7 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       7 |           0 | 1200.00 |            0 |                        2048.00 |                        0.00 |         0.00 |                                                        717.00 |                                                523.00 |
| postgresql-1-1-4-1-8 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          20 |     2048 |        4 |               1 |       8 |           0 | 1200.00 |            0 |                        2048.00 |                        0.00 |         0.00 |                                                        980.00 |                                                548.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 1200.00 |            0 |                        5653.46 |                        0.00 |         0.00 |                                                      98275.00 |                                              28295.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 1200.00 |            0 |                       13354.72 |                        0.00 |         0.00 |                                                      32399.00 |                                              11905.50 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |         160 |    16384 |               1 |           4 |           0 | 1200.00 |            0 |                       16384.00 |                        0.00 |         0.00 |                                                       1176.00 |                                                610.00 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |         140 |    14336 |               1 |           7 |           0 | 1200.00 |         9101 |                       14336.04 |                        0.00 |         0.00 |                                                       1028.00 |                                                526.00 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1243.80 |      1.97 |           0.66 |                  0.67 |
| postgresql-1-1-2-1 |      2574.93 |      2.64 |           0.66 |                  0.67 |
| postgresql-1-1-3-1 |      1914.61 |      1.86 |           0.66 |                  0.67 |
| postgresql-1-1-4-1 |      1676.79 |      1.65 |           0.66 |                  0.66 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      3324.87 |      3.44 |           1.52 |                  1.71 |
| postgresql-1-1-2-1 |      7282.68 |      6.87 |           1.25 |                  1.31 |
| postgresql-1-1-3-1 |      8256.27 |      8.86 |           1.44 |                  1.44 |
| postgresql-1-1-4-1 |      8159.76 |      8.04 |           0.85 |                  0.85 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: PostgreSQL-1)
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
