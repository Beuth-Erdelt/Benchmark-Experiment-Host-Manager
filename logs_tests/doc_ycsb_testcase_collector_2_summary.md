## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 13062s 
* Code: 1778734918
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [3].
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
  * disk:197681
  * volume_size:15G
  * volume_used:7.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778734918
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197684
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778734918
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197689
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778734918
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197693
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778734918

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-0-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.56 |              2292684.00 |            375000.00 |                            448511.00 |
| PostgreSQL-1-1-0-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.54 |              2293058.00 |            375000.00 |                            447999.00 |
| PostgreSQL-1-1-0-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.54 |              2293075.00 |            375000.00 |                            447743.00 |
| PostgreSQL-1-1-0-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.54 |              2293082.00 |            375000.00 |                            448511.00 |
| PostgreSQL-1-1-0-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.49 |              2293682.00 |            375000.00 |                            449791.00 |
| PostgreSQL-1-1-0-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.54 |              2293060.00 |            375000.00 |                            448255.00 |
| PostgreSQL-1-1-0-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.52 |              2293232.00 |            375000.00 |                            448511.00 |
| PostgreSQL-1-1-0-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          163.51 |              2293461.00 |            375000.00 |                            447999.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                         1308.23 |              2293682.00 |           3000000.00 |                            448415.00 |

### Execution

#### Per Connection

| DBMS               | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |       1 |        64 |    49152 |           1 |            0 |                         1317.39 |              2277223.00 |            1498683 |                            1126.00 |              1501317 |                           1489919.00 |
| PostgreSQL-1-1-2-6 | PostgreSQL-1    |                1 |        2 |       6 |         8 |     6144 |           8 |            0 |                          153.79 |              2438351.00 |             186980 |                            1095.00 |               188020 |                           1599487.00 |
| PostgreSQL-1-1-2-2 | PostgreSQL-1    |                1 |        2 |       2 |         8 |     6144 |           8 |            0 |                          153.60 |              2441355.00 |             187460 |                            1101.00 |               187540 |                           1626111.00 |
| PostgreSQL-1-1-2-8 | PostgreSQL-1    |                1 |        2 |       8 |         8 |     6144 |           8 |            0 |                          153.19 |              2447862.00 |             187743 |                            1097.00 |               187257 |                           1637375.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |       1 |         8 |     6144 |           8 |            0 |                          153.25 |              2446919.00 |             187840 |                            1099.00 |               187160 |                           1586175.00 |
| PostgreSQL-1-1-2-5 | PostgreSQL-1    |                1 |        2 |       5 |         8 |     6144 |           8 |            0 |                          153.52 |              2442751.00 |             187828 |                            1107.00 |               187172 |                           1662975.00 |
| PostgreSQL-1-1-2-4 | PostgreSQL-1    |                1 |        2 |       4 |         8 |     6144 |           8 |            0 |                          153.29 |              2446336.00 |             187293 |                            1100.00 |               187707 |                           1647615.00 |
| PostgreSQL-1-1-2-3 | PostgreSQL-1    |                1 |        2 |       3 |         8 |     6144 |           8 |            0 |                          153.07 |              2449807.00 |             187375 |                            1120.00 |               187625 |                           1637375.00 |
| PostgreSQL-1-1-2-7 | PostgreSQL-1    |                1 |        2 |       7 |         8 |     6144 |           8 |            0 |                          153.97 |              2435535.00 |             187660 |                            1104.00 |               187340 |                           1623039.00 |
| PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |       1 |        64 |    49152 |           1 |            0 |                         1160.99 |              2583998.00 |            1500249 |                            1465.00 |              1499751 |                           1870847.00 |
| PostgreSQL-1-2-2-4 | PostgreSQL-1    |                2 |        2 |       4 |         8 |     6144 |           8 |            0 |                          180.11 |              2082020.00 |             187496 |                            1102.00 |               187504 |                           1218559.00 |
| PostgreSQL-1-2-2-7 | PostgreSQL-1    |                2 |        2 |       7 |         8 |     6144 |           8 |            0 |                          179.82 |              2085444.00 |             187489 |                            1102.00 |               187511 |                           1238015.00 |
| PostgreSQL-1-2-2-6 | PostgreSQL-1    |                2 |        2 |       6 |         8 |     6144 |           8 |            0 |                          180.04 |              2082814.00 |             187285 |                            1102.00 |               187715 |                           1210367.00 |
| PostgreSQL-1-2-2-3 | PostgreSQL-1    |                2 |        2 |       3 |         8 |     6144 |           8 |            0 |                          179.99 |              2083460.00 |             187932 |                            1107.00 |               187068 |                           1201151.00 |
| PostgreSQL-1-2-2-8 | PostgreSQL-1    |                2 |        2 |       8 |         8 |     6144 |           8 |            0 |                          180.28 |              2080064.00 |             187827 |                            1114.00 |               187173 |                           1233919.00 |
| PostgreSQL-1-2-2-5 | PostgreSQL-1    |                2 |        2 |       5 |         8 |     6144 |           8 |            0 |                          179.93 |              2084119.00 |             187136 |                            1103.00 |               187864 |                           1190911.00 |
| PostgreSQL-1-2-2-2 | PostgreSQL-1    |                2 |        2 |       2 |         8 |     6144 |           8 |            0 |                          180.28 |              2080090.00 |             187651 |                            1106.00 |               187349 |                           1231871.00 |
| PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |       1 |         8 |     6144 |           8 |            0 |                          179.78 |              2085863.00 |             187492 |                            1104.00 |               187508 |                           1236991.00 |

#### Per Phase

| DBMS             |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                         1317.39 |              2277223.00 |         1498683.00 |                            1126.00 |           1501317.00 |                           1489919.00 |
| PostgreSQL-1-1-2 |             1.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                         1227.69 |              2449807.00 |         1500179.00 |                            1120.00 |           1499821.00 |                           1662975.00 |
| PostgreSQL-1-2-1 |             2.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                         1160.99 |              2583998.00 |         1500249.00 |                            1465.00 |           1499751.00 |                           1870847.00 |
| PostgreSQL-1-2-2 |             2.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                         1440.24 |              2085863.00 |         1500308.00 |                            1114.00 |           1499692.00 |                           1238015.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1685.19 |      1.25 |           9.89 |                 13.31 |
| PostgreSQL-1-1-2 |      1685.19 |      1.25 |           9.89 |                 13.31 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       427.53 |      0.88 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2 |       427.53 |      0.88 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1536.20 |      1.69 |          10.82 |                 15.05 |
| PostgreSQL-1-1-2 |      1517.46 |      1.65 |          11.26 |                 15.91 |
| PostgreSQL-1-2-1 |      4769.62 |      1.43 |          11.07 |                 16.00 |
| PostgreSQL-1-2-2 |      1479.43 |      1.96 |          11.73 |                 16.00 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       267.50 |      0.29 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2 |       266.57 |      1.36 |           0.12 |                  0.12 |
| PostgreSQL-1-2-1 |       278.90 |      0.28 |           0.13 |                  0.13 |
| PostgreSQL-1-2-2 |       278.02 |      0.89 |           0.12 |                  0.12 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     37.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     37.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     10.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     13.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-2-1 |                      8.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-2-2 |                      5.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
