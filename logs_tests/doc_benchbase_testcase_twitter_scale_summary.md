## Show Summary

### Workload
Benchbase Workload twitter SF=1600
* Type: benchbase
* Duration: 6032s 
* Code: 1773915579
* Benchbase runs the Twitter benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'twitter'. Scaling factor is 1600. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172521
  * datadisk:22632
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172647
  * datadisk:22758
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-3 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172772
  * datadisk:22883
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-4 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:172916
  * datadisk:23026
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773915579
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |                1 |         160 |    16384 |        1 |       1 |   1200 |            0 |                       16384    |                    16384.1  |            0 |                                                         18410 |                                                  3796 |
| PostgreSQL-1-1-1024-2-1 |                1 |          80 |     8192 |        2 |       1 |   1200 |            0 |                        8191.98 |                     8192.02 |            0 |                                                         18409 |                                                  3818 |
| PostgreSQL-1-1-1024-2-2 |                1 |          80 |     8192 |        2 |       2 |   1200 |            0 |                        8192.02 |                     8192.02 |            0 |                                                         18381 |                                                  3805 |
| PostgreSQL-1-1-1024-3-3 |                1 |          40 |     4096 |        3 |       1 |   1200 |            0 |                        4095.99 |                     4095.99 |            0 |                                                         18320 |                                                  3807 |
| PostgreSQL-1-1-1024-3-2 |                1 |          40 |     4096 |        3 |       2 |   1200 |            0 |                        4095.93 |                     4095.96 |            0 |                                                         18328 |                                                  3820 |
| PostgreSQL-1-1-1024-3-1 |                1 |          40 |     4096 |        3 |       3 |   1200 |            0 |                        4095.99 |                     4095.99 |            0 |                                                         18347 |                                                  3813 |
| PostgreSQL-1-1-1024-3-4 |                1 |          40 |     4096 |        3 |       4 |   1200 |            0 |                        4095.98 |                     4095.99 |            0 |                                                         18324 |                                                  3831 |
| PostgreSQL-1-1-1024-4-8 |                1 |          20 |     2048 |        4 |       1 |   1200 |            0 |                        2047.99 |                     2048    |            0 |                                                         18425 |                                                  3829 |
| PostgreSQL-1-1-1024-4-6 |                1 |          20 |     2048 |        4 |       2 |   1200 |            0 |                        2047.95 |                     2047.97 |            0 |                                                         18394 |                                                  3861 |
| PostgreSQL-1-1-1024-4-5 |                1 |          20 |     2048 |        4 |       3 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18408 |                                                  3830 |
| PostgreSQL-1-1-1024-4-4 |                1 |          20 |     2048 |        4 |       4 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18390 |                                                  3825 |
| PostgreSQL-1-1-1024-4-2 |                1 |          20 |     2048 |        4 |       5 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18419 |                                                  3825 |
| PostgreSQL-1-1-1024-4-7 |                1 |          20 |     2048 |        4 |       6 |   1200 |            0 |                        2048    |                     2048    |            0 |                                                         18393 |                                                  3804 |
| PostgreSQL-1-1-1024-4-3 |                1 |          20 |     2048 |        4 |       7 |   1200 |            0 |                        2047.97 |                     2047.98 |            0 |                                                         18402 |                                                  3846 |
| PostgreSQL-1-1-1024-4-1 |                1 |          20 |     2048 |        4 |       8 |   1200 |            0 |                        2047.99 |                     2048    |            0 |                                                         18418 |                                                  3818 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |         160 |    16384 |           1 |   1200 |            0 |                        16384   |                       16384 |            0 |                                                         18410 |                                               3796    |
| PostgreSQL-1-1-1024-2 |                1 |         160 |    16384 |           2 |   1200 |            0 |                        16384   |                       16384 |            0 |                                                         18409 |                                               3811.5  |
| PostgreSQL-1-1-1024-3 |                1 |         160 |    16384 |           4 |   1200 |            0 |                        16383.9 |                       16384 |            0 |                                                         18347 |                                               3817.75 |
| PostgreSQL-1-1-1024-4 |                1 |         160 |    16384 |           8 |   1200 |            0 |                        16383.9 |                       16384 |            0 |                                                         18425 |                                               3829.75 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 8, 1, 4]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |         593 |           1 |      1 |             9713.32 |
| PostgreSQL-1-1-1024-2 |         593 |           1 |      2 |             9713.32 |
| PostgreSQL-1-1-1024-3 |         593 |           1 |      4 |             9713.32 |
| PostgreSQL-1-1-1024-4 |         593 |           1 |      8 |             9713.32 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |      2713.56 |      6.37 |          13.91 |                 18.71 |
| PostgreSQL-1-1-1024-2 |      2713.56 |      6.37 |          13.91 |                 18.71 |
| PostgreSQL-1-1-1024-3 |      2713.56 |      6.37 |          13.91 |                 18.71 |
| PostgreSQL-1-1-1024-4 |      2713.56 |      6.37 |          13.91 |                 18.71 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |        149.5 |      0.25 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2 |        149.5 |      0.25 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-3 |        149.5 |      0.25 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-4 |        149.5 |      0.25 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |      15519.3 |     13.43 |          20.38 |                 25.41 |
| PostgreSQL-1-1-1024-2 |      15508.8 |     13.46 |          20.43 |                 25.51 |
| PostgreSQL-1-1-1024-3 |      15074   |     13.3  |          20.49 |                 25.61 |
| PostgreSQL-1-1-1024-4 |      15472   |     13.48 |          20.57 |                 25.73 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |      3065.81 |      2.53 |           2.38 |                  2.94 |
| PostgreSQL-1-1-1024-2 |      3065.81 |      4.79 |           2.38 |                  2.94 |
| PostgreSQL-1-1-1024-3 |      3183.87 |      3.5  |           1.13 |                  1.13 |
| PostgreSQL-1-1-1024-4 |      3251.86 |      6.13 |           0.78 |                  0.78 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
