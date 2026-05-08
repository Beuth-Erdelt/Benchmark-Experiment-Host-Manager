## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2551s 
* Code: 1776757570
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247613
  * datadisk:637
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776757570
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247613
  * datadisk:638
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776757570
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247614
  * datadisk:639
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776757570
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247615
  * datadisk:640
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776757570
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                      |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1-2 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.46 |                        0.47 |        97.98 |                                                     271814.00 |                                              77688.00 |
| PostgreSQL-1-1-1024-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    2.00 | 300.00 |         0.00 |                           0.48 |                        0.48 |       100.78 |                                                     278876.00 |                                              87129.00 |
| PostgreSQL-1-1-1024-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        99.38 |                                                      71530.00 |                                              26247.00 |
| PostgreSQL-1-1-1024-1-2-2 |             1.00 |       10.00 |  1024.00 |     2.00 |    2.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       105.68 |                                                      54352.00 |                                              24651.00 |
| PostgreSQL-1-1-1024-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.55 |                        0.55 |       114.77 |                                                     895400.00 |                                             106873.00 |
| PostgreSQL-1-1-1024-2-1-2 |             2.00 |       10.00 |  1024.00 |     1.00 |    2.00 | 300.00 |         0.00 |                           0.51 |                        0.51 |       106.38 |                                                    1052755.00 |                                             124738.00 |
| PostgreSQL-1-1-1024-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.46 |                        0.46 |        95.88 |                                                      85224.00 |                                              49256.00 |
| PostgreSQL-1-1-1024-2-2-2 |             2.00 |       10.00 |  1024.00 |     2.00 |    2.00 | 300.00 |         0.00 |                           0.51 |                        0.51 |       106.38 |                                                      87742.00 |                                              32728.00 |

#### Aggregated Parallel

| DBMS                    |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.94 |                        0.95 |         0.00 |                                                     278876.00 |                                              82408.50 |
| PostgreSQL-1-1-1024-1-2 |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.98 |                        0.98 |         0.00 |                                                      71530.00 |                                              25449.00 |
| PostgreSQL-1-1-1024-2-1 |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           1.06 |                        1.05 |         0.00 |                                                    1052755.00 |                                             115805.50 |
| PostgreSQL-1-1-1024-2-2 |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.97 |                        0.96 |         0.00 |                                                      87742.00 |                                              40992.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-2 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2], [2, 2]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1-1 |      427.00 |        1.00 |   2.00 |                8.43 |
| PostgreSQL-1-1-1024-1-2 |      427.00 |        1.00 |   2.00 |                8.43 |
| PostgreSQL-1-1-1024-2-1 |      427.00 |        1.00 |   2.00 |                8.43 |
| PostgreSQL-1-1-1024-2-2 |      427.00 |        1.00 |   2.00 |                8.43 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776757570-PostgreSQL-1-1-1024-1-1 |        95.56 |      0.52 |           5.97 |                  6.24 |
| 1776757570-PostgreSQL-1-1-1024-1-2 |        95.56 |      0.52 |           5.97 |                  6.24 |

### Loading phase: component loader

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776757570-PostgreSQL-1-1-1024-1-1 |        18.20 |      0.09 |           0.25 |                  0.25 |
| 1776757570-PostgreSQL-1-1-1024-1-2 |        18.20 |      0.09 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776757570-PostgreSQL-1-1-1024-1-1 |         5.82 |      0.13 |           6.04 |                  6.29 |
| 1776757570-PostgreSQL-1-1-1024-1-2 |         6.60 |      0.03 |           6.04 |                  6.29 |
| 1776757570-PostgreSQL-1-1-1024-2-1 |       125.18 |      0.06 |           5.95 |                  6.21 |
| 1776757570-PostgreSQL-1-1-1024-2-2 |         6.16 |      0.03 |           5.85 |                  6.10 |

### Execution phase: component benchmarker

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776757570-PostgreSQL-1-1-1024-1-1 |        30.32 |      0.29 |           0.23 |                  0.23 |
| 1776757570-PostgreSQL-1-1-1024-1-2 |        92.83 |      1.41 |           0.23 |                  0.23 |
| 1776757570-PostgreSQL-1-1-1024-2-1 |        85.19 |      0.24 |           0.23 |                  0.23 |
| 1776757570-PostgreSQL-1-1-1024-2-2 |        25.11 |      0.79 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776757570-PostgreSQL-1-1-1024-1-1 |                         1 |                                        0 |                                                0 |                           2 |                                       2 |
| 1776757570-PostgreSQL-1-1-1024-1-2 |                         1 |                                        0 |                                                0 |                           2 |                                       2 |

#### Execution phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776757570-PostgreSQL-1-1-1024-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| 1776757570-PostgreSQL-1-1-1024-1-2 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| 1776757570-PostgreSQL-1-1-1024-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| 1776757570-PostgreSQL-1-1-1024-2-2 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Workflow not as planned
