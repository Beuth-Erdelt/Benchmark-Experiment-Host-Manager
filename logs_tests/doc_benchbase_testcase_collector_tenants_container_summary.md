## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2653s 
* Code: 1776762792
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
  * Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1024-0-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247620
  * datadisk:330
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-0-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247621
  * datadisk:331
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-0-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247622
  * datadisk:331
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-0-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247623
  * datadisk:332
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247620
  * datadisk:330
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-1-1-1024-1-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247621
  * datadisk:331
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-1-1-1024-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247622
  * datadisk:331
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-1-1-1024-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247623
  * datadisk:331
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776762792
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Execution

#### Per Pod

| DBMS                        |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.50 |                        0.51 |       106.38 |                                                      93376.00 |                                              36426.00 |
| PostgreSQL-1-1-1024-0-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.46 |                        0.47 |        97.98 |                                                     289052.00 |                                             101287.00 |
| PostgreSQL-1-1-1024-1-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.43 |                        0.43 |        90.98 |                                                     165079.00 |                                              40087.00 |
| PostgreSQL-1-1-1024-0-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.48 |                        0.49 |       103.58 |                                                      41517.00 |                                              21969.00 |
| PostgreSQL-1-1-1024-1-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        99.38 |                                                     715760.00 |                                             220391.00 |
| PostgreSQL-1-1-1024-0-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.49 |                        0.48 |       100.78 |                                                     916157.00 |                                             203239.00 |
| PostgreSQL-1-1-1024-0-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.51 |                        0.51 |       107.78 |                                                     449486.00 |                                             144368.00 |
| PostgreSQL-1-1-1024-1-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       104.98 |                                                     317351.00 |                                             112904.00 |

#### Aggregated Parallel

| DBMS   |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| 1-1    |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.97 |                        0.97 |         0.00 |                                                     289052.00 |                                              68856.50 |
| 1-2    |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.91 |                        0.93 |         0.00 |                                                     165079.00 |                                              31028.00 |
| 2-1    |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.96 |                        0.95 |         0.00 |                                                     916157.00 |                                             211815.00 |
| 2-2    |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           1.01 |                        1.01 |         0.00 |                                                     449486.00 |                                             128636.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024-1-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-0-1 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1], [1, 1]]

### Loading

| DBMS                      |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:--------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-0-1-1 |      256.00 |        1.00 |   1.00 |               14.06 |
| PostgreSQL-1-1-1024-0-1-2 |      256.00 |        1.00 |   1.00 |               14.06 |
| PostgreSQL-1-1-1024-0-2-1 |      256.00 |        1.00 |   1.00 |               14.06 |
| PostgreSQL-1-1-1024-0-2-2 |      256.00 |        1.00 |   1.00 |               14.06 |
| PostgreSQL-1-1-1024-1-1-1 |      292.00 |        1.00 |   1.00 |               12.33 |
| PostgreSQL-1-1-1024-1-1-2 |      292.00 |        1.00 |   1.00 |               12.33 |
| PostgreSQL-1-1-1024-1-2-1 |      292.00 |        1.00 |   1.00 |               12.33 |
| PostgreSQL-1-1-1024-1-2-2 |      292.00 |        1.00 |   1.00 |               12.33 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776762792-PostgreSQL-1-1-1024-0-1-1 |        43.28 |      0.26 |           5.84 |                  5.98 |
| 1776762792-PostgreSQL-1-1-1024-0-1-2 |        43.28 |      0.26 |           5.84 |                  5.98 |
| 1776762792-PostgreSQL-1-1-1024-1-1-1 |        42.98 |      0.30 |           5.84 |                  5.99 |
| 1776762792-PostgreSQL-1-1-1024-1-1-2 |        42.98 |      0.30 |           5.84 |                  5.99 |

### Loading phase: component loader

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776762792-PostgreSQL-1-1-1024-0-1-1 |         9.71 |      0.07 |           0.27 |                  0.27 |
| 1776762792-PostgreSQL-1-1-1024-0-1-2 |         9.71 |      0.07 |           0.27 |                  0.27 |
| 1776762792-PostgreSQL-1-1-1024-1-1-1 |         8.51 |      0.05 |           0.25 |                  0.25 |
| 1776762792-PostgreSQL-1-1-1024-1-1-2 |         8.51 |      0.05 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776762792-PostgreSQL-1-1-1024-0-1-1 |         4.30 |      0.02 |           5.88 |                  6.03 |
| 1776762792-PostgreSQL-1-1-1024-0-1-2 |         3.72 |      0.02 |           5.88 |                  6.03 |
| 1776762792-PostgreSQL-1-1-1024-0-2-1 |        72.10 |      0.04 |           5.84 |                  5.99 |
| 1776762792-PostgreSQL-1-1-1024-0-2-2 |         4.03 |      0.02 |           5.78 |                  5.91 |
| 1776762792-PostgreSQL-1-1-1024-1-1-1 |         4.61 |      0.02 |           5.88 |                  6.03 |
| 1776762792-PostgreSQL-1-1-1024-1-1-2 |         4.14 |      0.02 |           5.88 |                  6.03 |
| 1776762792-PostgreSQL-1-1-1024-1-2-1 |         5.00 |      0.04 |           5.78 |                  5.90 |
| 1776762792-PostgreSQL-1-1-1024-1-2-2 |         4.61 |      0.02 |           5.79 |                  5.92 |

### Execution phase: component benchmarker

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776762792-PostgreSQL-1-1-1024-0-1-1 |        21.57 |      0.62 |           0.23 |                  0.23 |
| 1776762792-PostgreSQL-1-1-1024-0-1-2 |        21.77 |      0.70 |           0.23 |                  0.23 |
| 1776762792-PostgreSQL-1-1-1024-0-2-1 |        15.85 |      0.18 |           0.23 |                  0.23 |
| 1776762792-PostgreSQL-1-1-1024-0-2-2 |        21.59 |      0.58 |           0.23 |                  0.23 |
| 1776762792-PostgreSQL-1-1-1024-1-1-1 |        50.06 |      1.00 |           0.11 |                  0.11 |
| 1776762792-PostgreSQL-1-1-1024-1-1-2 |        50.06 |      1.03 |           0.23 |                  0.23 |
| 1776762792-PostgreSQL-1-1-1024-1-2-1 |        23.13 |      0.41 |           0.23 |                  0.23 |
| 1776762792-PostgreSQL-1-1-1024-1-2-2 |        26.35 |      0.67 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776762792-PostgreSQL-1-1-1024-0-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| 1776762792-PostgreSQL-1-1-1024-0-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| 1776762792-PostgreSQL-1-1-1024-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| 1776762792-PostgreSQL-1-1-1024-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS                                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776762792-PostgreSQL-1-1-1024-0-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| 1776762792-PostgreSQL-1-1-1024-0-1-2 |                     11.00 |                                     1.00 |                                             0.00 |                        2.00 |                                    2.00 |
| 1776762792-PostgreSQL-1-1-1024-0-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| 1776762792-PostgreSQL-1-1-1024-0-2-2 |                     11.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| 1776762792-PostgreSQL-1-1-1024-1-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| 1776762792-PostgreSQL-1-1-1024-1-1-2 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| 1776762792-PostgreSQL-1-1-1024-1-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    4.00 |
| 1776762792-PostgreSQL-1-1-1024-1-2-2 |                     11.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Workflow not as planned
