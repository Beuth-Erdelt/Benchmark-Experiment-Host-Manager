## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 15414s 
* Code: 1778719395
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
  * disk:197657
  * volume_size:15G
  * volume_used:7.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778719395
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197662
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778719395
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197667
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778719395
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197672
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778719395

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-0-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.91 |              2699646.00 |            375000.00 |                            603135.00 |
| PostgreSQL-1-1-0-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.86 |              2700537.00 |            375000.00 |                            604159.00 |
| PostgreSQL-1-1-0-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.94 |              2699009.00 |            375000.00 |                            604159.00 |
| PostgreSQL-1-1-0-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.92 |              2699327.00 |            375000.00 |                            607743.00 |
| PostgreSQL-1-1-0-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.95 |              2698741.00 |            375000.00 |                            602623.00 |
| PostgreSQL-1-1-0-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.92 |              2699307.00 |            375000.00 |                            604159.00 |
| PostgreSQL-1-1-0-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.88 |              2700083.00 |            375000.00 |                            604671.00 |
| PostgreSQL-1-1-0-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          138.94 |              2698985.00 |            375000.00 |                            604159.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                         1111.34 |              2700537.00 |           3000000.00 |                            604351.00 |

### Execution

#### Per Connection

| DBMS               | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |       1 |        64 |    32768 |           1 |            0 |                          895.97 |              3348308.00 |            1499348 |                            1125.00 |              1500652 |                           1818623.00 |
| PostgreSQL-1-1-2-5 | PostgreSQL-1    |                1 |        2 |       5 |         8 |     4096 |           8 |            0 |                          171.37 |              2188196.00 |             187796 |                            1088.00 |               187204 |                           1157119.00 |
| PostgreSQL-1-1-2-8 | PostgreSQL-1    |                1 |        2 |       8 |         8 |     4096 |           8 |            0 |                          172.26 |              2176948.00 |             187514 |                            1088.00 |               187486 |                           1113087.00 |
| PostgreSQL-1-1-2-2 | PostgreSQL-1    |                1 |        2 |       2 |         8 |     4096 |           8 |            0 |                          173.45 |              2162048.00 |             187351 |                            1086.00 |               187649 |                           1166335.00 |
| PostgreSQL-1-1-2-4 | PostgreSQL-1    |                1 |        2 |       4 |         8 |     4096 |           8 |            0 |                          171.83 |              2182447.00 |             186990 |                            1092.00 |               188010 |                           1157119.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |       1 |         8 |     4096 |           8 |            0 |                          172.37 |              2175502.00 |             187600 |                            1091.00 |               187400 |                           1128447.00 |
| PostgreSQL-1-1-2-3 | PostgreSQL-1    |                1 |        2 |       3 |         8 |     4096 |           8 |            0 |                          172.01 |              2180100.00 |             187703 |                            1082.00 |               187297 |                           1148927.00 |
| PostgreSQL-1-1-2-7 | PostgreSQL-1    |                1 |        2 |       7 |         8 |     4096 |           8 |            0 |                          171.63 |              2184913.00 |             187665 |                            1096.00 |               187335 |                           1187839.00 |
| PostgreSQL-1-1-2-6 | PostgreSQL-1    |                1 |        2 |       6 |         8 |     4096 |           8 |            0 |                          172.87 |              2169235.00 |             187900 |                            1093.00 |               187100 |                           1167359.00 |
| PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |       1 |        64 |    32768 |           1 |            0 |                          903.51 |              3320401.00 |            1499926 |                            1476.00 |              1500074 |                           2398207.00 |
| PostgreSQL-1-2-2-6 | PostgreSQL-1    |                2 |        2 |       6 |         8 |     4096 |           8 |            0 |                          154.34 |              2429632.00 |             187746 |                            1100.00 |               187254 |                           1385471.00 |
| PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |       1 |         8 |     4096 |           8 |            0 |                          154.03 |              2434660.00 |             188003 |                            1111.00 |               186997 |                           1337343.00 |
| PostgreSQL-1-2-2-3 | PostgreSQL-1    |                2 |        2 |       3 |         8 |     4096 |           8 |            0 |                          154.43 |              2428337.00 |             187836 |                            1116.00 |               187164 |                           1358847.00 |
| PostgreSQL-1-2-2-4 | PostgreSQL-1    |                2 |        2 |       4 |         8 |     4096 |           8 |            0 |                          154.09 |              2433699.00 |             187619 |                            1099.00 |               187381 |                           1323007.00 |
| PostgreSQL-1-2-2-8 | PostgreSQL-1    |                2 |        2 |       8 |         8 |     4096 |           8 |            0 |                          154.58 |              2426004.00 |             187344 |                            1099.00 |               187656 |                           1350655.00 |
| PostgreSQL-1-2-2-7 | PostgreSQL-1    |                2 |        2 |       7 |         8 |     4096 |           8 |            0 |                          153.92 |              2436259.00 |             187597 |                            1110.00 |               187403 |                           1398783.00 |
| PostgreSQL-1-2-2-2 | PostgreSQL-1    |                2 |        2 |       2 |         8 |     4096 |           8 |            0 |                          154.10 |              2433447.00 |             187703 |                            1106.00 |               187297 |                           1374207.00 |
| PostgreSQL-1-2-2-5 | PostgreSQL-1    |                2 |        2 |       5 |         8 |     4096 |           8 |            0 |                          154.00 |              2435087.00 |             187678 |                            1102.00 |               187322 |                           1377279.00 |

#### Per Phase

| DBMS             |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                          895.97 |              3348308.00 |         1499348.00 |                            1125.00 |           1500652.00 |                           1818623.00 |
| PostgreSQL-1-1-2 |             1.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                         1377.79 |              2188196.00 |         1500519.00 |                            1096.00 |           1499481.00 |                           1187839.00 |
| PostgreSQL-1-2-1 |             2.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                          903.51 |              3320401.00 |         1499926.00 |                            1476.00 |           1500074.00 |                           2398207.00 |
| PostgreSQL-1-2-2 |             2.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                         1233.48 |              2436259.00 |         1501526.00 |                            1116.00 |           1498474.00 |                           1398783.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1653.64 |      1.21 |           9.89 |                 13.33 |
| PostgreSQL-1-1-2 |      1653.64 |      1.21 |           9.89 |                 13.33 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       431.99 |      0.41 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2 |       431.99 |      0.41 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1552.17 |      1.38 |          10.83 |                 15.05 |
| PostgreSQL-1-1-2 |      1453.23 |      2.04 |          11.24 |                 15.89 |
| PostgreSQL-1-2-1 |      4713.33 |      1.10 |          11.07 |                 16.00 |
| PostgreSQL-1-2-2 |      1480.77 |      1.98 |          11.74 |                 16.00 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       265.57 |      0.24 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2 |       265.57 |      0.46 |           0.13 |                  0.13 |
| PostgreSQL-1-2-1 |       280.87 |      0.22 |           0.13 |                  0.13 |
| PostgreSQL-1-2-2 |       279.47 |      1.05 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     40.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     40.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     14.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     10.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-2-1 |                     13.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-2-2 |                     13.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
