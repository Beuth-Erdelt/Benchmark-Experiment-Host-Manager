## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 18992s 
* Code: 1778448224
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2].
  * Experiment uses bexhoma version 0.9.7.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197194
  * volume_size:15G
  * volume_used:7.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778448224
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197200
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778448224
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197206
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778448224
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197214
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778448224

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.50 |              3086374.00 |            375000.00 |                            627199.00 |
| PostgreSQL-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.49 |              3086747.00 |            375000.00 |                            628223.00 |
| PostgreSQL-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.49 |              3086576.00 |            375000.00 |                            627711.00 |
| PostgreSQL-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.50 |              3086432.00 |            375000.00 |                            627199.00 |
| PostgreSQL-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.52 |              3085851.00 |            375000.00 |                            626175.00 |
| PostgreSQL-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.49 |              3086629.00 |            375000.00 |                            626687.00 |
| PostgreSQL-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.52 |              3085920.00 |            375000.00 |                            627711.00 |
| PostgreSQL-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          121.47 |              3087140.00 |            375000.00 |                            627199.00 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                          971.99 |              3087140.00 |           3000000.00 |                            627263.00 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1 |                1 |        1 |       1 |        64 |    32768 |           1 |            0 |                          899.78 |              3334132.00 |            1501375 |                            1126.00 |              1498625 |                           1505279.00 |
| PostgreSQL-1-1-2-1 |                1 |        2 |       1 |         8 |     4096 |           8 |            0 |                          128.76 |              2912503.00 |             187069 |                            1091.00 |               187931 |                           1296383.00 |
| PostgreSQL-1-1-2-2 |                1 |        2 |       2 |         8 |     4096 |           8 |            0 |                          128.56 |              2916937.00 |             187650 |                            1092.00 |               187350 |                           1358847.00 |
| PostgreSQL-1-1-2-3 |                1 |        2 |       3 |         8 |     4096 |           8 |            0 |                          128.96 |              2907856.00 |             187559 |                            1094.00 |               187441 |                           1323007.00 |
| PostgreSQL-1-1-2-4 |                1 |        2 |       4 |         8 |     4096 |           8 |            0 |                          129.13 |              2904065.00 |             187255 |                            1093.00 |               187745 |                           1346559.00 |
| PostgreSQL-1-1-2-5 |                1 |        2 |       5 |         8 |     4096 |           8 |            0 |                          128.67 |              2914478.00 |             187906 |                            1102.00 |               187094 |                           1372159.00 |
| PostgreSQL-1-1-2-6 |                1 |        2 |       6 |         8 |     4096 |           8 |            0 |                          128.45 |              2919367.00 |             187258 |                            1092.00 |               187742 |                           1336319.00 |
| PostgreSQL-1-1-2-7 |                1 |        2 |       7 |         8 |     4096 |           8 |            0 |                          128.43 |              2919856.00 |             187549 |                            1094.00 |               187451 |                           1326079.00 |
| PostgreSQL-1-1-2-8 |                1 |        2 |       8 |         8 |     4096 |           8 |            0 |                          128.84 |              2910559.00 |             187307 |                            1093.00 |               187693 |                           1348607.00 |
| PostgreSQL-1-2-1-1 |                2 |        1 |       1 |        64 |    32768 |           1 |            0 |                          630.06 |              4761419.00 |            1500671 |                            1480.00 |              1499329 |                           2775039.00 |
| PostgreSQL-1-2-2-1 |                2 |        2 |       1 |         8 |     4096 |           8 |            0 |                          112.15 |              3343743.00 |             187447 |                            1118.00 |               187553 |                           1538047.00 |
| PostgreSQL-1-2-2-2 |                2 |        2 |       2 |         8 |     4096 |           8 |            0 |                          111.30 |              3369317.00 |             187477 |                            1120.00 |               187523 |                           1585151.00 |
| PostgreSQL-1-2-2-3 |                2 |        2 |       3 |         8 |     4096 |           8 |            0 |                          112.39 |              3336605.00 |             187928 |                            1131.00 |               187072 |                           1498111.00 |
| PostgreSQL-1-2-2-4 |                2 |        2 |       4 |         8 |     4096 |           8 |            0 |                          112.17 |              3343240.00 |             187744 |                            1120.00 |               187256 |                           1533951.00 |
| PostgreSQL-1-2-2-5 |                2 |        2 |       5 |         8 |     4096 |           8 |            0 |                          111.61 |              3359827.00 |             187554 |                            1125.00 |               187446 |                           1552383.00 |
| PostgreSQL-1-2-2-6 |                2 |        2 |       6 |         8 |     4096 |           8 |            0 |                          112.26 |              3340539.00 |             187112 |                            1122.00 |               187888 |                           1569791.00 |
| PostgreSQL-1-2-2-7 |                2 |        2 |       7 |         8 |     4096 |           8 |            0 |                          111.82 |              3353728.00 |             187479 |                            1125.00 |               187521 |                           1559551.00 |
| PostgreSQL-1-2-2-8 |                2 |        2 |       8 |         8 |     4096 |           8 |            0 |                          112.42 |              3335567.00 |             187225 |                            1126.00 |               187775 |                           1517567.00 |

#### Per Phase

| DBMS             |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                          899.78 |              3334132.00 |         1501375.00 |                            1126.00 |           1498625.00 |                           1505279.00 |
| PostgreSQL-1-1-2 |             1.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                         1029.80 |              2919856.00 |         1499553.00 |                            1102.00 |           1500447.00 |                           1372159.00 |
| PostgreSQL-1-2-1 |             2.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                          630.06 |              4761419.00 |         1500671.00 |                            1480.00 |           1499329.00 |                           2775039.00 |
| PostgreSQL-1-2-2 |             2.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                          896.12 |              3369317.00 |         1499966.00 |                            1131.00 |           1500034.00 |                           1585151.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1710.21 |      1.33 |           9.85 |                 13.26 |
| PostgreSQL-1-1-2 |      1710.21 |      1.33 |           9.85 |                 13.26 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       452.97 |      0.91 |           0.12 |                  0.12 |
| PostgreSQL-1-1-2 |       452.97 |      0.91 |           0.12 |                  0.12 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1563.88 |      2.22 |          10.84 |                 15.07 |
| PostgreSQL-1-1-2 |      1442.61 |      1.83 |          11.25 |                 15.90 |
| PostgreSQL-1-2-1 |      1882.64 |      1.45 |          11.05 |                 16.00 |
| PostgreSQL-1-2-2 |      1556.08 |      1.96 |          11.74 |                 16.00 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       276.40 |      0.34 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2 |       285.18 |      0.42 |           0.13 |                  0.13 |
| PostgreSQL-1-2-1 |       301.12 |      0.30 |           0.13 |                  0.13 |
| PostgreSQL-1-2-2 |       301.12 |      0.62 |           0.12 |                  0.12 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     30.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     30.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     13.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-2-2 |                      9.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
