## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2880s 
* Code: 1776751747
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247605
  * datadisk:4307
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776751747
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247606
  * datadisk:4533
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776751747
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247607
  * datadisk:4705
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776751747
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247607
  * datadisk:4805
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776751747
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                      |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1-1 |             1.00 |      160.00 | 16384.00 |     1.00 |    1.00 | 300.00 |         3.00 |                         487.99 |                      484.77 |         0.00 |                                                    1525016.00 |                                             327420.00 |
| PostgreSQL-1-1-1024-1-2-2 |             1.00 |       80.00 |  8192.00 |     2.00 |    1.00 | 300.00 |         0.00 |                         255.40 |                      253.68 |         0.00 |                                                    1399302.00 |                                             313005.00 |
| PostgreSQL-1-1-1024-1-2-1 |             1.00 |       80.00 |  8192.00 |     2.00 |    2.00 | 300.00 |         0.00 |                         255.81 |                      254.08 |         0.00 |                                                    1410180.00 |                                             312391.00 |
| PostgreSQL-1-1-1024-2-1-1 |             2.00 |      160.00 | 16384.00 |     1.00 |    1.00 | 300.00 |         0.00 |                         329.17 |                      327.30 |         0.00 |                                                    2213256.00 |                                             484163.00 |
| PostgreSQL-1-1-1024-2-2-1 |             2.00 |       80.00 |  8192.00 |     2.00 |    1.00 | 300.00 |         0.00 |                         205.48 |                      204.10 |         0.00 |                                                    1769770.00 |                                             388228.00 |
| PostgreSQL-1-1-1024-2-2-2 |             2.00 |       80.00 |  8192.00 |     2.00 |    2.00 | 300.00 |         0.00 |                         204.59 |                      203.30 |         0.00 |                                                    1767073.00 |                                             390500.00 |

#### Aggregated Parallel

| DBMS                    |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |             1.00 |      160.00 | 16384.00 |        1.00 | 300.00 |         3.00 |                         487.99 |                      484.77 |         0.00 |                                                    1525016.00 |                                             327420.00 |
| PostgreSQL-1-1-1024-1-2 |             1.00 |      160.00 | 16384.00 |        2.00 | 300.00 |         0.00 |                         511.21 |                      507.76 |         0.00 |                                                    1410180.00 |                                             312698.00 |
| PostgreSQL-1-1-1024-2-1 |             2.00 |      160.00 | 16384.00 |        1.00 | 300.00 |         0.00 |                         329.17 |                      327.30 |         0.00 |                                                    2213256.00 |                                             484163.00 |
| PostgreSQL-1-1-1024-2-2 |             2.00 |      160.00 | 16384.00 |        2.00 | 300.00 |         0.00 |                         410.07 |                      407.39 |         0.00 |                                                    1769770.00 |                                             389364.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024-2 - Pods [[1], [1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[1, 2], [1, 2]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1-1 |      663.00 |        1.00 |   1.00 |               86.88 |
| PostgreSQL-1-1-1024-1-2 |      663.00 |        1.00 |   2.00 |               86.88 |
| PostgreSQL-1-1-1024-2-1 |      663.00 |        1.00 |   1.00 |               86.88 |
| PostgreSQL-1-1-1024-2-2 |      663.00 |        1.00 |   2.00 |               86.88 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776751747-PostgreSQL-1-1-1024-1-1 |       563.40 |      1.22 |           7.50 |                  9.13 |
| 1776751747-PostgreSQL-1-1-1024-1-2 |       563.40 |      1.22 |           7.50 |                  9.13 |

### Loading phase: component loader

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776751747-PostgreSQL-1-1-1024-1-1 |      1446.06 |      6.99 |           0.26 |                  0.26 |
| 1776751747-PostgreSQL-1-1-1024-1-2 |      1446.06 |      6.99 |           0.26 |                  0.26 |

### Execution phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776751747-PostgreSQL-1-1-1024-1-1 |       643.95 |      2.82 |           8.88 |                 10.73 |
| 1776751747-PostgreSQL-1-1-1024-1-2 |       618.28 |      3.84 |           9.06 |                 11.07 |
| 1776751747-PostgreSQL-1-1-1024-2-1 |      1915.46 |      2.12 |           8.05 |                 10.10 |
| 1776751747-PostgreSQL-1-1-1024-2-2 |       523.59 |      2.24 |           8.43 |                 10.61 |

### Execution phase: component benchmarker

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776751747-PostgreSQL-1-1-1024-1-1 |       205.26 |      0.87 |           0.70 |                  0.70 |
| 1776751747-PostgreSQL-1-1-1024-1-2 |       205.26 |      3.03 |           0.70 |                  0.70 |
| 1776751747-PostgreSQL-1-1-1024-2-1 |       153.09 |      0.57 |           0.66 |                  0.66 |
| 1776751747-PostgreSQL-1-1-1024-2-2 |       153.09 |      1.94 |           0.66 |                  0.66 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776751747-PostgreSQL-1-1-1024-1-1 |                        17 |                                        0 |                                                0 |                          17 |                                      16 |
| 1776751747-PostgreSQL-1-1-1024-1-2 |                        17 |                                        0 |                                                0 |                          17 |                                      16 |

#### Execution phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776751747-PostgreSQL-1-1-1024-1-1 |                      5.00 |                                    21.00 |                                             0.00 |                      160.00 |                                  160.00 |
| 1776751747-PostgreSQL-1-1-1024-1-2 |                      1.00 |                                     4.00 |                                             0.00 |                      161.00 |                                  160.00 |
| 1776751747-PostgreSQL-1-1-1024-2-1 |                      1.00 |                                     6.00 |                                             0.00 |                      160.00 |                                  160.00 |
| 1776751747-PostgreSQL-1-1-1024-2-2 |                     28.00 |                                    20.00 |                                             0.00 |                      161.00 |                                  160.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Workflow not as planned
