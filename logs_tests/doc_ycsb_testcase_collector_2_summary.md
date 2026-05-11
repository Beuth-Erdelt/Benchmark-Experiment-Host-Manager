## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 14212s 
* Code: 1778467307
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
  * disk:197225
  * volume_size:15G
  * volume_used:7.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778467307
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197229
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778467307
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197235
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778467307
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197239
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778467307

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.61 |              2666949.00 |            375000.00 |                            585727.00 |
| PostgreSQL-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.59 |              2667352.00 |            375000.00 |                            587263.00 |
| PostgreSQL-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.60 |              2667145.00 |            375000.00 |                            587775.00 |
| PostgreSQL-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.60 |              2667142.00 |            375000.00 |                            586751.00 |
| PostgreSQL-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.58 |              2667532.00 |            375000.00 |                            586751.00 |
| PostgreSQL-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.59 |              2667353.00 |            375000.00 |                            586239.00 |
| PostgreSQL-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.57 |              2667675.00 |            375000.00 |                            586751.00 |
| PostgreSQL-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          140.59 |              2667355.00 |            375000.00 |                            586751.00 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                         1124.73 |              2667675.00 |           3000000.00 |                            586751.00 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1 |                1 |        1 |       1 |        64 |    49152 |           1 |            0 |                         1192.74 |              2515226.00 |            1500388 |                            1170.00 |              1499612 |                           1347583.00 |
| PostgreSQL-1-1-2-1 |                1 |        2 |       1 |         8 |     6144 |           8 |            0 |                          122.36 |              3064631.00 |             187403 |                            1121.00 |               187597 |                           1660927.00 |
| PostgreSQL-1-1-2-2 |                1 |        2 |       2 |         8 |     6144 |           8 |            0 |                          121.87 |              3076982.00 |             187487 |                            1120.00 |               187513 |                           1729535.00 |
| PostgreSQL-1-1-2-3 |                1 |        2 |       3 |         8 |     6144 |           8 |            0 |                          122.51 |              3061098.00 |             187588 |                            1121.00 |               187412 |                           1641471.00 |
| PostgreSQL-1-1-2-4 |                1 |        2 |       4 |         8 |     6144 |           8 |            0 |                          123.39 |              3039073.00 |             187238 |                            1139.00 |               187762 |                           1641471.00 |
| PostgreSQL-1-1-2-5 |                1 |        2 |       5 |         8 |     6144 |           8 |            0 |                          122.30 |              3066147.00 |             187586 |                            1131.00 |               187414 |                           1669119.00 |
| PostgreSQL-1-1-2-6 |                1 |        2 |       6 |         8 |     6144 |           8 |            0 |                          123.05 |              3047602.00 |             187432 |                            1121.00 |               187568 |                           1700863.00 |
| PostgreSQL-1-1-2-7 |                1 |        2 |       7 |         8 |     6144 |           8 |            0 |                          123.80 |              3028996.00 |             187853 |                            1120.00 |               187147 |                           1665023.00 |
| PostgreSQL-1-1-2-8 |                1 |        2 |       8 |         8 |     6144 |           8 |            0 |                          123.31 |              3041239.00 |             187532 |                            1119.00 |               187468 |                           1728511.00 |
| PostgreSQL-1-2-1-1 |                2 |        1 |       1 |        64 |    49152 |           1 |            0 |                         1248.39 |              2403089.00 |            1499463 |                            1468.00 |              1500537 |                           1543167.00 |
| PostgreSQL-1-2-2-1 |                2 |        2 |       1 |         8 |     6144 |           8 |            0 |                          183.72 |              2041108.00 |             187778 |                            1113.00 |               187222 |                           1074175.00 |
| PostgreSQL-1-2-2-2 |                2 |        2 |       2 |         8 |     6144 |           8 |            0 |                          185.06 |              2026391.00 |             187513 |                            1109.00 |               187487 |                           1019391.00 |
| PostgreSQL-1-2-2-3 |                2 |        2 |       3 |         8 |     6144 |           8 |            0 |                          184.01 |              2037951.00 |             187745 |                            1111.00 |               187255 |                           1034239.00 |
| PostgreSQL-1-2-2-4 |                2 |        2 |       4 |         8 |     6144 |           8 |            0 |                          184.24 |              2035423.00 |             187301 |                            1121.00 |               187699 |                           1085439.00 |
| PostgreSQL-1-2-2-5 |                2 |        2 |       5 |         8 |     6144 |           8 |            0 |                          183.61 |              2042342.00 |             187308 |                            1106.00 |               187692 |                           1049599.00 |
| PostgreSQL-1-2-2-6 |                2 |        2 |       6 |         8 |     6144 |           8 |            0 |                          184.07 |              2037280.00 |             187494 |                            1114.00 |               187506 |                           1074175.00 |
| PostgreSQL-1-2-2-7 |                2 |        2 |       7 |         8 |     6144 |           8 |            0 |                          184.55 |              2031922.00 |             187609 |                            1111.00 |               187391 |                           1008639.00 |
| PostgreSQL-1-2-2-8 |                2 |        2 |       8 |         8 |     6144 |           8 |            0 |                          185.07 |              2026262.00 |             187458 |                            1107.00 |               187542 |                           1008639.00 |

#### Per Phase

| DBMS             |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                         1192.74 |              2515226.00 |         1500388.00 |                            1170.00 |           1499612.00 |                           1347583.00 |
| PostgreSQL-1-1-2 |             1.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                          982.59 |              3076982.00 |         1500119.00 |                            1139.00 |           1499881.00 |                           1729535.00 |
| PostgreSQL-1-2-1 |             2.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                         1248.39 |              2403089.00 |         1499463.00 |                            1468.00 |           1500537.00 |                           1543167.00 |
| PostgreSQL-1-2-2 |             2.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                         1474.33 |              2042342.00 |         1500206.00 |                            1121.00 |           1499794.00 |                           1085439.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1663.65 |      1.15 |           9.90 |                 13.35 |
| PostgreSQL-1-1-2 |      1663.65 |      1.15 |           9.90 |                 13.35 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       456.47 |      0.38 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2 |       456.47 |      0.38 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1589.83 |      2.04 |          10.82 |                 15.04 |
| PostgreSQL-1-1-2 |      1562.27 |      1.95 |          11.24 |                 15.88 |
| PostgreSQL-1-2-1 |      4834.08 |      1.79 |          11.06 |                 15.99 |
| PostgreSQL-1-2-2 |      1519.58 |      1.90 |          11.75 |                 16.00 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       282.11 |      0.36 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2 |       316.33 |      0.63 |           0.12 |                  0.12 |
| PostgreSQL-1-2-1 |       290.24 |      0.33 |           0.13 |                  0.13 |
| PostgreSQL-1-2-2 |       290.24 |      0.73 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     14.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-1-2 |                     14.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-2-1 |                     12.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-2-2 |                     11.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
