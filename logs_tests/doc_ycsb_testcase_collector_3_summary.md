## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1554s 
* Code: 1778751654
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
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
  * disk:200094
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778751654
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:200435
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778751654
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:200096
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778751654
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:200420
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778751654

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-0-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8055.68 |                15517.00 |            125000.00 |                              5979.00 |
| PostgreSQL-1-1-0-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8072.85 |                15484.00 |            125000.00 |                              5919.00 |
| PostgreSQL-1-1-0-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8066.60 |                15496.00 |            125000.00 |                              5663.00 |
| PostgreSQL-1-1-0-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8056.20 |                15516.00 |            125000.00 |                              5995.00 |
| PostgreSQL-1-1-0-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8053.60 |                15521.00 |            125000.00 |                              6039.00 |
| PostgreSQL-1-1-0-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8048.42 |                15531.00 |            125000.00 |                              6043.00 |
| PostgreSQL-1-1-0-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8065.56 |                15498.00 |            125000.00 |                              5915.00 |
| PostgreSQL-1-1-0-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8060.36 |                15508.00 |            125000.00 |                              5899.00 |
| PostgreSQL-1-2-0-1 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8066.60 |                15496.00 |            125000.00 |                              5799.00 |
| PostgreSQL-1-2-0-2 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8069.72 |                15490.00 |            125000.00 |                              5839.00 |
| PostgreSQL-1-2-0-3 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8065.56 |                15498.00 |            125000.00 |                              5507.00 |
| PostgreSQL-1-2-0-4 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8052.57 |                15523.00 |            125000.00 |                              5891.00 |
| PostgreSQL-1-2-0-5 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8067.64 |                15494.00 |            125000.00 |                              6047.00 |
| PostgreSQL-1-2-0-6 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8056.72 |                15515.00 |            125000.00 |                              5975.00 |
| PostgreSQL-1-2-0-7 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8068.16 |                15493.00 |            125000.00 |                              5851.00 |
| PostgreSQL-1-2-0-8 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8058.28 |                15512.00 |            125000.00 |                              5851.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                        64479.27 |                15531.00 |           1000000.00 |                              5931.50 |
| PostgreSQL-1-2 |             2.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                        64505.24 |                15523.00 |           1000000.00 |                              5845.00 |

### Execution

#### Per Connection

| DBMS               | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |       1 |        64 |    49152 |           1 |            0 |                        48444.92 |                20642.00 |             498226 |                             563.00 |               501774 |                              1337.00 |
| PostgreSQL-1-1-2-5 | PostgreSQL-1    |                1 |        2 |       5 |         8 |     6144 |           8 |            0 |                         6075.04 |                20576.00 |              62202 |                             612.00 |                62798 |                               984.00 |
| PostgreSQL-1-1-2-2 | PostgreSQL-1    |                1 |        2 |       2 |         8 |     6144 |           8 |            0 |                         6077.70 |                20567.00 |              62482 |                             631.00 |                62518 |                              1008.00 |
| PostgreSQL-1-1-2-3 | PostgreSQL-1    |                1 |        2 |       3 |         8 |     6144 |           8 |            0 |                         6077.99 |                20566.00 |              62507 |                             588.00 |                62493 |                               971.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |       1 |         8 |     6144 |           8 |            0 |                         6070.02 |                20593.00 |              62439 |                             597.00 |                62561 |                               962.00 |
| PostgreSQL-1-1-2-8 | PostgreSQL-1    |                1 |        2 |       8 |         8 |     6144 |           8 |            0 |                         6076.81 |                20570.00 |              62486 |                             626.00 |                62514 |                              1012.00 |
| PostgreSQL-1-1-2-6 | PostgreSQL-1    |                1 |        2 |       6 |         8 |     6144 |           8 |            0 |                         6073.86 |                20580.00 |              62642 |                             613.00 |                62358 |                               992.00 |
| PostgreSQL-1-1-2-4 | PostgreSQL-1    |                1 |        2 |       4 |         8 |     6144 |           8 |            0 |                         6077.70 |                20567.00 |              62814 |                             595.00 |                62186 |                               969.00 |
| PostgreSQL-1-1-2-7 | PostgreSQL-1    |                1 |        2 |       7 |         8 |     6144 |           8 |            0 |                         6073.27 |                20582.00 |              62283 |                             604.00 |                62717 |                               963.00 |
| PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |       1 |        64 |    49152 |           1 |            0 |                        48468.40 |                20632.00 |             500557 |                             574.00 |               499443 |                              1222.00 |
| PostgreSQL-1-2-2-2 | PostgreSQL-1    |                2 |        2 |       2 |         8 |     6144 |           8 |            0 |                         6079.47 |                20561.00 |              62673 |                             578.00 |                62327 |                               936.00 |
| PostgreSQL-1-2-2-5 | PostgreSQL-1    |                2 |        2 |       5 |         8 |     6144 |           8 |            0 |                         6074.74 |                20577.00 |              62356 |                             621.00 |                62644 |                              1042.00 |
| PostgreSQL-1-2-2-7 | PostgreSQL-1    |                2 |        2 |       7 |         8 |     6144 |           8 |            0 |                         6074.74 |                20577.00 |              62618 |                             477.00 |                62382 |                               864.00 |
| PostgreSQL-1-2-2-4 | PostgreSQL-1    |                2 |        2 |       4 |         8 |     6144 |           8 |            0 |                         6072.38 |                20585.00 |              62360 |                             425.00 |                62640 |                               856.00 |
| PostgreSQL-1-2-2-3 | PostgreSQL-1    |                2 |        2 |       3 |         8 |     6144 |           8 |            0 |                         6075.04 |                20576.00 |              62319 |                             538.00 |                62681 |                               877.00 |
| PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |       1 |         8 |     6144 |           8 |            0 |                         6076.22 |                20572.00 |              62673 |                             493.00 |                62327 |                               847.00 |
| PostgreSQL-1-2-2-6 | PostgreSQL-1    |                2 |        2 |       6 |         8 |     6144 |           8 |            0 |                         6075.04 |                20576.00 |              62505 |                             548.00 |                62495 |                               886.00 |
| PostgreSQL-1-2-2-8 | PostgreSQL-1    |                2 |        2 |       8 |         8 |     6144 |           8 |            0 |                         6075.92 |                20573.00 |              62380 |                             623.00 |                62620 |                              1004.00 |

#### Per Phase

| DBMS             |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                        48444.92 |                20642.00 |          498226.00 |                             563.00 |            501774.00 |                              1337.00 |
| PostgreSQL-1-1-2 |             1.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                        48602.39 |                20593.00 |          499855.00 |                             631.00 |            500145.00 |                              1012.00 |
| PostgreSQL-1-2-1 |             2.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                        48468.40 |                20632.00 |          500557.00 |                             574.00 |            499443.00 |                              1222.00 |
| PostgreSQL-1-2-2 |             2.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                        48603.56 |                20585.00 |          499884.00 |                             623.00 |            500116.00 |                              1042.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       187.81 |      6.25 |           6.89 |                  7.39 |
| PostgreSQL-1-1-2 |       187.81 |      6.25 |           6.89 |                  7.39 |
| PostgreSQL-1-2-1 |       587.58 |      4.84 |           7.10 |                  8.47 |
| PostgreSQL-1-2-2 |       587.58 |      4.84 |           7.10 |                  8.47 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        22.99 |      1.26 |           7.32 |                  8.53 |
| PostgreSQL-1-1-2 |       166.34 |      4.33 |           7.50 |                  8.87 |
| PostgreSQL-1-2-1 |       123.30 |      4.18 |           7.46 |                  8.77 |
| PostgreSQL-1-2-2 |       118.07 |      3.95 |           7.50 |                  8.85 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        43.61 |      0.00 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.13 |                  0.13 |
| PostgreSQL-1-2-1 |        58.42 |      0.00 |           0.13 |                  0.14 |
| PostgreSQL-1-2-2 |         0.00 |      0.00 |           0.13 |                  0.14 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    1.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    1.00 |
| PostgreSQL-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                     58.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
