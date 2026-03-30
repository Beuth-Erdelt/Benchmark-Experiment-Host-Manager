## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1694s 
* Code: 1773428073
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
  * Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-0-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-0-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Execution

#### Per Pod

| DBMS                      |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-0-1-1 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.5      |                    0.496666 |     104.277  |                                                        121050 |                                                 40628 |
| PostgreSQL-1-1-1024-1-1-1 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.503332 |                    0.503332 |     105.676  |                                                         57129 |                                                 21444 |
| PostgreSQL-1-1-1024-0-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.526667 |                    0.53     |     111.275  |                                                        177050 |                                                 50583 |
| PostgreSQL-1-1-1024-1-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.446667 |                    0.446667 |      93.7791 |                                                         37374 |                                                 15766 |

#### Aggregated Parallel

| DBMS   |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| 1-1    |                1 |          20 |     2048 |           2 |    300 |            0 |                           1    |                        1    |            0 |                                                        121050 |                                               31036   |
| 1-2    |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.97 |                        0.98 |            0 |                                                        177050 |                                               33174.5 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned

* DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-0-1 |         271 |           1 |      1 |             13.2841 |
| PostgreSQL-1-1-1024-0-2 |         271 |           1 |      1 |             13.2841 |
| PostgreSQL-1-1-1024-1-1 |         224 |           1 |      1 |             16.0714 |
| PostgreSQL-1-1-1024-1-2 |         224 |           1 |      1 |             16.0714 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |        70.34 |      0.42 |           5.84 |                  5.98 |
| PostgreSQL-1-1-1024-0-2 |        70.34 |      0.42 |           5.84 |                  5.98 |
| PostgreSQL-1-1-1024-1-1 |        70.83 |      0.41 |           5.85 |                  5.99 |
| PostgreSQL-1-1-1024-1-2 |        70.83 |      0.41 |           5.85 |                  5.99 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |         9.01 |      0.06 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-0-2 |         9.01 |      0.06 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-1-1 |         8.28 |      0.05 |           0.24 |                  0.24 |
| PostgreSQL-1-1-1024-1-2 |         8.28 |      0.05 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |         4.47 |      0.02 |           5.89 |                  6.03 |
| PostgreSQL-1-1-1024-0-2 |         3.81 |      0.02 |           5.89 |                  6.03 |
| PostgreSQL-1-1-1024-1-1 |         4.84 |      0.02 |           5.89 |                  6.03 |
| PostgreSQL-1-1-1024-1-2 |         3.88 |      0.02 |           5.89 |                  6.03 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |        22.69 |      0.23 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-0-2 |        22.99 |      0.07 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-1-1 |        28.53 |      0.33 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-1-2 |        28.53 |      0.07 |           0.11 |                  0.11 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                    |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-0-1 |                         1 |                                        0 |                                                0 |                           1 |                                       1 |
| PostgreSQL-1-1-1024-0-2 |                         1 |                                        0 |                                                0 |                           1 |                                       1 |
| PostgreSQL-1-1-1024-1-1 |                         2 |                                        0 |                                                0 |                           2 |                                       1 |
| PostgreSQL-1-1-1024-1-2 |                         2 |                                        0 |                                                0 |                           2 |                                       1 |

#### Execution phase: SUT deployment

| DBMS                    |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-0-1 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |
| PostgreSQL-1-1-1024-0-2 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |
| PostgreSQL-1-1-1024-1-1 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |
| PostgreSQL-1-1-1024-1-2 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
