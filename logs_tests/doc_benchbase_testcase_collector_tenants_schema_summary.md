## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2842s 
* Code: 1778698769
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
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197621
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778698769
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197621
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778698769
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197622
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778698769
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197623
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778698769
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      748.00 |           8.00 |            0.00 |        324.00 |          416.00 |              2 |           1 |          | schema         |             2 | False         |                4.81 |
| PostgreSQL-1-2 |                2 |    1 |      748.00 |           8.00 |            0.00 |        324.00 |          416.00 |              2 |           1 |          | schema         |             2 | False         |                4.81 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.49 |                        0.49 |       103.58 |                                                     371687.00 |                                             124356.00 |
| PostgreSQL-1-1-1-2 |             1.00 |       10.00 |  1024.00 |     1.00 |    2.00 | 300.00 |         0.00 |                           0.50 |                        0.51 |       106.38 |                                                     310255.00 |                                              98528.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.46 |                        0.46 |        95.88 |                                                     255985.00 |                                              96852.00 |
| PostgreSQL-1-1-2-2 |             1.00 |       10.00 |  1024.00 |     2.00 |    2.00 | 300.00 |         0.00 |                           0.49 |                        0.50 |       104.28 |                                                     197863.00 |                                              93264.00 |
| PostgreSQL-1-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.48 |                        0.48 |       100.78 |                                                     700704.00 |                                             142658.00 |
| PostgreSQL-1-2-1-2 |             2.00 |       10.00 |  1024.00 |     1.00 |    2.00 | 300.00 |         0.00 |                           0.50 |                        0.51 |       106.38 |                                                     404228.00 |                                             118943.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.45 |                        0.45 |        95.18 |                                                     250564.00 |                                              57257.00 |
| PostgreSQL-1-2-2-2 |             2.00 |       10.00 |  1024.00 |     2.00 |    2.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       104.98 |                                                     665080.00 |                                             115675.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           1.00 |                        1.00 |         0.00 |                                                     371687.00 |                                             111442.00 |
| PostgreSQL-1-1-2 |             1.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.95 |                        0.95 |         0.00 |                                                     255985.00 |                                              95058.00 |
| PostgreSQL-1-2-1 |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.98 |                        0.99 |         0.00 |                                                     700704.00 |                                             130800.50 |
| PostgreSQL-1-2-2 |             2.00 |       20.00 |  2048.00 |        2.00 | 300.00 |         0.00 |                           0.95 |                        0.95 |         0.00 |                                                     665080.00 |                                              86466.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        92.07 |      0.55 |           5.96 |                  6.21 |
| PostgreSQL-1-1-2 |        92.07 |      0.55 |           5.96 |                  6.21 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        17.03 |      0.07 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2 |        17.03 |      0.07 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         6.47 |      0.04 |           6.04 |                  6.29 |
| PostgreSQL-1-1-2 |         6.15 |      0.04 |           6.04 |                  6.29 |
| PostgreSQL-1-2-1 |       131.42 |      0.07 |           5.95 |                  6.21 |
| PostgreSQL-1-2-2 |         6.25 |      0.03 |           5.85 |                  6.09 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        69.34 |      1.29 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2 |        74.76 |      1.96 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1 |        59.20 |      1.07 |           0.23 |                  0.23 |
| PostgreSQL-1-2-2 |        57.46 |      1.35 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| PostgreSQL-1-1-2 |                      2.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-1-2 |                     21.00 |                                     1.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-2-1 |                     21.00 |                                     1.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
