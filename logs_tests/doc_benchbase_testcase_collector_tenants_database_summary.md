## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 3019s 
* Code: 1778430808
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.7.
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
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197161
  * volume_size:20G
  * volume_used:648M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778430808
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197162
  * volume_size:20G
  * volume_used:648M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778430808
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197163
  * volume_size:20G
  * volume_used:652M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778430808
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197164
  * volume_size:20G
  * volume_used:652M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778430808
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |     1149.00 |           7.00 |            0.00 |        526.00 |          616.00 |              2 | database       |             2 | False         |                3.13 |
| PostgreSQL-1-2 |                2 |    1 |     1149.00 |           7.00 |            0.00 |        526.00 |          616.00 |              2 | database       |             2 | False         |                3.13 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.48 |                        0.48 |       101.48 |                                                      69989.00 |                                              27904.00 |
| PostgreSQL-1-1-1-2 |             1.00 |       10.00 |  1024.00 |     1.00 |    2.00 | 300.00 |         0.00 |                           0.45 |                        0.45 |        93.78 |                                                      66701.00 |                                              28740.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.46 |                        0.47 |        98.68 |                                                     775755.00 |                                             279871.00 |
| PostgreSQL-1-1-2-2 |             1.00 |       10.00 |  1024.00 |     2.00 |    2.00 | 300.00 |         0.00 |                           0.44 |                        0.44 |        92.38 |                                                     583866.00 |                                             253185.00 |
| PostgreSQL-1-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        98.68 |                                                    1058716.00 |                                             175041.00 |
| PostgreSQL-1-2-1-2 |             2.00 |       10.00 |  1024.00 |     1.00 |    2.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       104.98 |                                                     727775.00 |                                             159069.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.49 |                        0.49 |       102.88 |                                                     134429.00 |                                              47273.00 |
| PostgreSQL-1-2-2-2 |             2.00 |       10.00 |  1024.00 |     2.00 |    2.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       104.28 |                                                     170817.00 |                                              54230.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.93 |                        0.93 |         0.00 |                                                      69989.00 |                                              28322.00 |
| PostgreSQL-1-1-2 |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.91 |                        0.91 |         0.00 |                                                     775755.00 |                                             266528.00 |
| PostgreSQL-1-2-1 |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.97 |                        0.97 |         0.00 |                                                    1058716.00 |                                             167055.00 |
| PostgreSQL-1-2-2 |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.98 |                        0.99 |         0.00 |                                                     170817.00 |                                              50751.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       103.88 |      0.34 |           5.98 |                  6.24 |
| PostgreSQL-1-1-2 |       103.88 |      0.34 |           5.98 |                  6.24 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        18.05 |      0.15 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2 |        18.05 |      0.15 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        11.05 |      0.04 |           6.06 |                  6.33 |
| PostgreSQL-1-1-2 |        10.88 |      0.05 |           6.06 |                  6.33 |
| PostgreSQL-1-2-1 |        11.74 |      0.07 |           5.84 |                  6.09 |
| PostgreSQL-1-2-2 |        10.42 |      0.06 |           5.86 |                  6.10 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        35.87 |      0.54 |           0.23 |                  0.23 |
| PostgreSQL-1-1-2 |        33.94 |      0.99 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1 |        55.93 |      1.22 |           0.23 |                  0.23 |
| PostgreSQL-1-2-2 |        54.99 |      1.29 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      4.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    5.00 |
| PostgreSQL-1-1-2 |                      4.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    5.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     23.00 |                                     1.00 |                                             0.00 |                        4.00 |                                    1.00 |
| PostgreSQL-1-1-2 |                     22.00 |                                     1.00 |                                             0.00 |                        5.00 |                                    3.00 |
| PostgreSQL-1-2-1 |                     23.00 |                                     1.00 |                                             0.00 |                        8.00 |                                    5.00 |
| PostgreSQL-1-2-2 |                     22.00 |                                     1.00 |                                             0.00 |                        2.00 |                                    0.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
