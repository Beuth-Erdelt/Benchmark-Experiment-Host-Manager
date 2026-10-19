## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1884s 
* Code: 1792318911
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:828113
  * volume_size:1.8T
  * volume_used:809G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:833033
  * volume_size:1.8T
  * volume_used:814G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:847709
  * volume_size:1.8T
  * volume_used:828G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:851079
  * volume_size:1.8T
  * volume_used:832G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792318911

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792318911-85c767cd4f-m5pkg: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7829.14 |                47898.00 |            375000.00 |                              3205.00 | 3.00 |              225.48 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7854.72 |                47742.00 |            375000.00 |                              3179.00 | 3.00 |              226.22 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7788.32 |                48149.00 |            375000.00 |                              3191.00 | 3.00 |              224.30 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7909.56 |                47411.00 |            375000.00 |                              3091.00 | 3.00 |              227.80 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7715.57 |                48603.00 |            375000.00 |                              3147.00 | 3.00 |              222.21 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7802.91 |                48059.00 |            375000.00 |                              3167.00 | 3.00 |              224.72 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7965.17 |                47080.00 |            375000.00 |                              3123.00 | 3.00 |              229.40 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7671.22 |                48884.00 |            375000.00 |                              3201.00 | 3.00 |              220.93 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              220.93 |                        62536.61 |                48884.00 |           3000000.00 |                              3163.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32673.33 |                91818.00 |            1499484 |                             603.00 |              1500516 |                              3289.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4083.99 |                91822.00 |             187597 |                             530.00 |               187403 |                             16223.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4083.81 |                91826.00 |             187848 |                             537.00 |               187152 |                             15951.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4084.74 |                91805.00 |             187594 |                             505.00 |               187406 |                             16111.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4084.21 |                91817.00 |             187687 |                             486.00 |               187313 |                             15671.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4083.94 |                91823.00 |             187966 |                             527.00 |               187034 |                             15823.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4084.12 |                91819.00 |             187260 |                             508.00 |               187740 |                             15711.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4084.43 |                91812.00 |             187179 |                             544.00 |               187821 |                             15887.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4084.26 |                91816.00 |             188023 |                             489.00 |               186977 |                             16351.00 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48931.66 |                61310.00 |            1501014 |                             537.00 |              1498986 |                              1484.00 |
| postgresql-1-1-4-1-1 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6116.46 |                61310.00 |             187864 |                             595.00 |               187136 |                              1900.00 |
| postgresql-1-1-4-1-2 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6118.05 |                61294.00 |             187299 |                             610.00 |               187701 |                              1900.00 |
| postgresql-1-1-4-1-3 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6121.45 |                61260.00 |             187527 |                             626.00 |               187473 |                              1920.00 |
| postgresql-1-1-4-1-4 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6115.26 |                61322.00 |             187048 |                             608.00 |               187952 |                              1942.00 |
| postgresql-1-1-4-1-5 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6115.46 |                61320.00 |             187530 |                             642.00 |               187470 |                              2022.00 |
| postgresql-1-1-4-1-6 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6116.86 |                61306.00 |             187319 |                             653.00 |               187681 |                              2091.00 |
| postgresql-1-1-4-1-7 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6115.66 |                61318.00 |             186913 |                             693.00 |               188087 |                              2161.00 |
| postgresql-1-1-4-1-8 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6119.85 |                61276.00 |             187015 |                             548.00 |               187985 |                              1862.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32673.33 |                91818.00 |            1499484 |                             603.00 |              1500516 |                              3289.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32673.51 |                91826.00 |            1501154 |                             544.00 |              1498846 |                             16351.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48931.66 |                61310.00 |            1501014 |                             537.00 |              1498986 |                              1484.00 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48939.05 |                61322.00 |            1498515 |                             693.00 |              1501485 |                              2161.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       249.65 |      5.15 |           4.22 |                  7.40 |
| postgresql-1-1-2-1 |       249.65 |      5.15 |           4.22 |                  7.40 |
| postgresql-1-1-3-1 |       249.65 |      5.15 |           4.22 |                  7.40 |
| postgresql-1-1-4-1 |       249.65 |      5.15 |           4.22 |                  7.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       156.44 |      5.32 |           0.11 |                  0.12 |
| postgresql-1-1-2-1 |       156.44 |      5.32 |           0.11 |                  0.12 |
| postgresql-1-1-3-1 |       156.44 |      5.32 |           0.11 |                  0.12 |
| postgresql-1-1-4-1 |       156.44 |      5.32 |           0.11 |                  0.12 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       167.90 |      2.54 |           5.02 |                  8.89 |
| postgresql-1-1-2-1 |       236.70 |      2.78 |           5.18 |                  9.20 |
| postgresql-1-1-3-1 |       194.53 |      3.32 |           5.21 |                  9.26 |
| postgresql-1-1-4-1 |       180.19 |      3.55 |           5.21 |                  9.28 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       181.88 |      2.74 |           0.31 |                  0.32 |
| postgresql-1-1-2-1 |       154.07 |      3.98 |           0.31 |                  0.32 |
| postgresql-1-1-3-1 |       136.79 |      2.95 |           0.55 |                  0.55 |
| postgresql-1-1-4-1 |       248.61 |      5.59 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-4-1 (bexhoma-metrics-postgresql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |
| postgresql-1-1-2-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |
| postgresql-1-1-3-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |
| postgresql-1-1-4-1 |                                   20 |                                                   0 |                                                           0 |                                     45 |                                                 45 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                58.00 |                                                0.00 |                                                        0.00 |                                  15.00 |                                              15.00 |
| postgresql-1-1-2-1 |                                56.00 |                                                0.00 |                                                        0.00 |                                  63.00 |                                              63.00 |
| postgresql-1-1-3-1 |                                52.00 |                                                0.00 |                                                        0.00 |                                  13.00 |                                              13.00 |
| postgresql-1-1-4-1 |                                56.00 |                                                0.00 |                                                        0.00 |                                  11.00 |                                              11.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
