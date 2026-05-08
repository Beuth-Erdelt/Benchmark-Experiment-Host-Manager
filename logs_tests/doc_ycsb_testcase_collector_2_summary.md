## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 41029s 
* Code: 1776792746
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
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
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
* PostgreSQL-64-8-65536-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247667
  * datadisk:7091
  * volume_size:15G
  * volume_used:7.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1776792746
* PostgreSQL-64-8-65536-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247734
  * datadisk:8555
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1776792746
* PostgreSQL-64-8-65536-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247768
  * datadisk:12548
  * volume_size:15G
  * volume_used:13G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1776792746
* PostgreSQL-64-8-65536-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247775
  * datadisk:12877
  * volume_size:15G
  * volume_used:13G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1776792746

### Loading

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-65536-1 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.82 |              3478130.00 |            375000.00 |                            664575.00 |
| PostgreSQL-64-8-65536-2 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.80 |              3478569.00 |            375000.00 |                            664575.00 |
| PostgreSQL-64-8-65536-3 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.82 |              3477939.00 |            375000.00 |                            666111.00 |
| PostgreSQL-64-8-65536-4 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.81 |              3478325.00 |            375000.00 |                            666111.00 |
| PostgreSQL-64-8-65536-5 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.80 |              3478744.00 |            375000.00 |                            665087.00 |
| PostgreSQL-64-8-65536-6 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.82 |              3478035.00 |            375000.00 |                            662015.00 |
| PostgreSQL-64-8-65536-7 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.81 |              3478499.00 |            375000.00 |                            666623.00 |
| PostgreSQL-64-8-65536-8 |             1.00 |      8.00 |  8192.00 |        1.00 |         0.00 |                          107.79 |              3478826.00 |            375000.00 |                            663551.00 |

### Execution

| DBMS                        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-65536-1-2-1 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.78 |              5532959.00 |          186463.00 |                            1273.00 |            188537.00 |                           3903487.00 |
| PostgreSQL-64-8-65536-1-2-2 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.74 |              5535621.00 |          187574.00 |                            1296.00 |            187426.00 |                           3803135.00 |
| PostgreSQL-64-8-65536-1-2-3 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.60 |              5547238.00 |          187686.00 |                            1284.00 |            187314.00 |                           3883007.00 |
| PostgreSQL-64-8-65536-1-2-4 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.68 |              5540853.00 |          188224.00 |                            1264.00 |            186776.00 |                           3987455.00 |
| PostgreSQL-64-8-65536-1-2-5 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.79 |              5531917.00 |          187636.00 |                            1274.00 |            187364.00 |                           3958783.00 |
| PostgreSQL-64-8-65536-1-2-6 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.60 |              5547406.00 |          187378.00 |                            1265.00 |            187622.00 |                           3919871.00 |
| PostgreSQL-64-8-65536-1-2-7 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.75 |              5534797.00 |          187469.00 |                            1268.00 |            187531.00 |                           3895295.00 |
| PostgreSQL-64-8-65536-1-2-8 |             1.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                           67.80 |              5531010.00 |          187602.00 |                            1283.00 |            187398.00 |                           3829759.00 |
| PostgreSQL-64-8-65536-1-1-1 |             1.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                          926.20 |              3239055.00 |         1501240.00 |                            1152.00 |           1498760.00 |                           1966079.00 |
| PostgreSQL-64-8-65536-2-2-1 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.45 |              3624819.00 |          187872.00 |                            1112.00 |            187128.00 |                           2523135.00 |
| PostgreSQL-64-8-65536-2-2-2 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.32 |              3629464.00 |          187465.00 |                            1107.00 |            187535.00 |                           2516991.00 |
| PostgreSQL-64-8-65536-2-2-3 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.50 |              3623046.00 |          187717.00 |                            1144.00 |            187283.00 |                           2402303.00 |
| PostgreSQL-64-8-65536-2-2-4 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.48 |              3623904.00 |          187602.00 |                            1105.00 |            187398.00 |                           2564095.00 |
| PostgreSQL-64-8-65536-2-2-5 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.58 |              3620500.00 |          187312.00 |                            1125.00 |            187688.00 |                           2523135.00 |
| PostgreSQL-64-8-65536-2-2-6 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.28 |              3630791.00 |          187308.00 |                            1117.00 |            187692.00 |                           2476031.00 |
| PostgreSQL-64-8-65536-2-2-7 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.27 |              3631117.00 |          187420.00 |                            1108.00 |            187580.00 |                           2416639.00 |
| PostgreSQL-64-8-65536-2-2-8 |             2.00 |      8.00 |  6144.00 |        1.00 |         0.00 |                          103.26 |              3631476.00 |          186852.00 |                            1112.00 |            188148.00 |                           2533375.00 |
| PostgreSQL-64-8-65536-2-1-1 |             2.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                          680.78 |              4406684.00 |         1500721.00 |                            1423.00 |           1499279.00 |                           3358719.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-64-8-65536 - Pods [[8, 1], [8, 1]]

#### Planned

* DBMS PostgreSQL-64-8-65536 - Pods [[1, 8], [1, 8]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776792746-PostgreSQL-64-8-65536-1-1 |      1755.22 |      1.03 |           9.87 |                 13.29 |
| 1776792746-PostgreSQL-64-8-65536-1-2 |      1755.22 |      1.03 |           9.87 |                 13.29 |

### Loading phase: component loader

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776792746-PostgreSQL-64-8-65536-1-1 |       484.61 |      0.41 |           0.11 |                  0.11 |
| 1776792746-PostgreSQL-64-8-65536-1-2 |       484.61 |      0.41 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776792746-PostgreSQL-64-8-65536-1-1 |      1554.71 |      1.71 |          10.83 |                 15.05 |
| 1776792746-PostgreSQL-64-8-65536-1-2 |      1752.01 |      1.13 |          11.31 |                 15.95 |
| 1776792746-PostgreSQL-64-8-65536-2-1 |      1756.52 |      1.05 |          11.66 |                 16.00 |
| 1776792746-PostgreSQL-64-8-65536-2-2 |      1445.81 |      1.36 |          11.99 |                 16.00 |

### Execution phase: component benchmarker

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776792746-PostgreSQL-64-8-65536-1-1 |       265.16 |      0.39 |           0.13 |                  0.13 |
| 1776792746-PostgreSQL-64-8-65536-1-2 |       371.97 |      0.29 |           0.11 |                  0.11 |
| 1776792746-PostgreSQL-64-8-65536-2-1 |       270.76 |      0.18 |           0.13 |                  0.14 |
| 1776792746-PostgreSQL-64-8-65536-2-2 |       279.26 |      0.59 |           0.12 |                  0.12 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
