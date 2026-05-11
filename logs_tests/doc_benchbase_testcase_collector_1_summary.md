## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 3094s 
* Code: 1778421401
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.7.
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
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197146
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778421401
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197147
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778421401
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197148
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778421401
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197149
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778421401
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |     1555.00 |           3.00 |            0.00 |        731.00 |          821.00 |              1 |                |             0 | False         |               37.04 |
| PostgreSQL-1-2 |                2 |   16 |     1555.00 |           3.00 |            0.00 |        731.00 |          821.00 |              1 |                |             0 | False         |               37.04 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |      160.00 | 16384.00 |     1.00 |    1.00 | 300.00 |         0.00 |                         414.78 |                      412.21 |         0.00 |                                                    1846538.00 |                                             384684.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       80.00 |  8192.00 |     2.00 |    1.00 | 300.00 |         2.00 |                         221.29 |                      219.86 |         0.00 |                                                    1752750.00 |                                             360538.00 |
| PostgreSQL-1-1-2-2 |             1.00 |       80.00 |  8192.00 |     2.00 |    2.00 | 300.00 |         0.00 |                         217.11 |                      215.80 |         0.00 |                                                    1800939.00 |                                             367448.00 |
| PostgreSQL-1-2-1-1 |             2.00 |      160.00 | 16384.00 |     1.00 |    1.00 | 300.00 |         1.00 |                         328.47 |                      326.80 |         0.00 |                                                    2411053.00 |                                             484669.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       80.00 |  8192.00 |     2.00 |    1.00 | 300.00 |         0.00 |                         200.16 |                      198.81 |         0.00 |                                                    1939081.00 |                                             398311.00 |
| PostgreSQL-1-2-2-2 |             2.00 |       80.00 |  8192.00 |     2.00 |    2.00 | 300.00 |         0.00 |                         200.41 |                      199.13 |         0.00 |                                                    1950275.00 |                                             398489.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |      160.00 | 16384.00 |        1.00 | 300.00 |         0.00 |                         414.78 |                      412.21 |         0.00 |                                                    1846538.00 |                                             384684.00 |
| PostgreSQL-1-1-2 |             1.00 |      160.00 | 16384.00 |        2.00 | 300.00 |         2.00 |                         438.40 |                      435.66 |         0.00 |                                                    1800939.00 |                                             363993.00 |
| PostgreSQL-1-2-1 |             2.00 |      160.00 | 16384.00 |        1.00 | 300.00 |         1.00 |                         328.47 |                      326.80 |         0.00 |                                                    2411053.00 |                                             484669.00 |
| PostgreSQL-1-2-2 |             2.00 |      160.00 | 16384.00 |        2.00 | 300.00 |         0.00 |                         400.57 |                      397.94 |         0.00 |                                                    1950275.00 |                                             398400.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       543.15 |      1.22 |           7.50 |                  9.12 |
| PostgreSQL-1-1-2 |       543.15 |      1.22 |           7.50 |                  9.12 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1190.37 |      5.68 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2 |      1190.37 |      5.68 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       531.93 |      2.93 |           8.79 |                 10.62 |
| PostgreSQL-1-1-2 |       533.59 |      2.54 |           8.98 |                 10.95 |
| PostgreSQL-1-2-1 |       525.00 |      2.74 |           8.10 |                 10.12 |
| PostgreSQL-1-2-2 |       497.26 |      2.39 |           8.41 |                 10.54 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       180.78 |      0.99 |           0.69 |                  0.69 |
| PostgreSQL-1-1-2 |       180.78 |      1.80 |           0.69 |                  0.69 |
| PostgreSQL-1-2-1 |       154.28 |      0.72 |           0.67 |                  0.67 |
| PostgreSQL-1-2-2 |       142.31 |      1.67 |           0.67 |                  0.67 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |
| PostgreSQL-1-1-2 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      5.00 |                                    26.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-1-2 |                     16.00 |                                    21.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-1 |                     14.00 |                                    20.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                    19.00 |                                             0.00 |                      160.00 |                                  160.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
