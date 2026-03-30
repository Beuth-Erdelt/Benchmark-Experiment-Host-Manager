## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1654s 
* Code: 1773426376
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147853
  * volume_size:20G
  * volume_used:648M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773426376
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147853
  * volume_size:20G
  * volume_used:648M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773426376
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-2 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.449999 |                    0.453332 |      95.1785 |                                                        319897 |                                                132717 |
| PostgreSQL-1-1-1024-1-1 |                1 |          10 |     1024 |        1 |       2 |    300 |            0 |                       0.493333 |                    0.493333 |     103.577  |                                                        359779 |                                                156795 |
| PostgreSQL-1-1-1024-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.513333 |                    0.513333 |     107.776  |                                                         43950 |                                                 17722 |
| PostgreSQL-1-1-1024-2-2 |                1 |          10 |     1024 |        2 |       2 |    300 |            0 |                       0.46     |                    0.463333 |      97.2784 |                                                         75963 |                                                 21255 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.94 |                        0.95 |            0 |                                                        359779 |                                              144756   |
| PostgreSQL-1-1-1024-2 |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.97 |                        0.98 |            0 |                                                         75963 |                                               19488.5 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |         407 |           1 |      2 |             8.84521 |
| PostgreSQL-1-1-1024-2 |         407 |           1 |      2 |             8.84521 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |       142.14 |      0.63 |           5.98 |                  6.23 |
| PostgreSQL-1-1-1024-2 |       142.14 |      0.63 |           5.98 |                  6.23 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |         17.9 |      0.08 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2 |         17.9 |      0.08 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |         9.75 |      0.29 |           6.07 |                  6.33 |
| PostgreSQL-1-1-1024-2 |         9.31 |      0.04 |           6.07 |                  6.33 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |        23.16 |      0.15 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-2 |        22.22 |      0.3  |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1 |                         2 |                                        0 |                                                0 |                           8 |                                       6 |
| PostgreSQL-1-1-1024-2 |                         2 |                                        0 |                                                0 |                           8 |                                       6 |

#### Execution phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1 |                        21 |                                        1 |                                                0 |                           2 |                                       1 |
| PostgreSQL-1-1-1024-2 |                        23 |                                        0 |                                                0 |                           3 |                                       0 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
