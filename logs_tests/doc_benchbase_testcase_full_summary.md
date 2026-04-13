## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2660s 
* Code: 1775827791
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
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:155277
  * datadisk:4307
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775827791
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:156201
  * datadisk:5231
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775827791
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:155277
  * datadisk:4307
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775827791
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:156180
  * datadisk:5210
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775827791
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                      |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1-1 |             1.00 |      160.00 | 16384.00 |     1.00 |    1.00 | 300.00 |         2.00 |                        1982.75 |                     1966.45 |         0.00 |                                                     280744.00 |                                              80656.00 |
| PostgreSQL-1-1-1024-1-2-2 |             1.00 |       80.00 |  8192.00 |     2.00 |    1.00 | 300.00 |         1.00 |                         920.26 |                      912.49 |         0.00 |                                                     313801.00 |                                              86917.00 |
| PostgreSQL-1-1-1024-1-2-1 |             1.00 |       80.00 |  8192.00 |     2.00 |    2.00 | 300.00 |         1.00 |                         918.01 |                      910.36 |         0.00 |                                                     318089.00 |                                              87112.00 |
| PostgreSQL-1-1-1024-2-1-1 |             2.00 |      160.00 | 16384.00 |     1.00 |    1.00 | 300.00 |         3.00 |                        1958.05 |                     1941.80 |         0.00 |                                                     284622.00 |                                              81682.00 |
| PostgreSQL-1-1-1024-2-2-1 |             2.00 |       80.00 |  8192.00 |     2.00 |    1.00 | 300.00 |         2.00 |                         918.34 |                      910.71 |         0.00 |                                                     319410.00 |                                              87099.00 |
| PostgreSQL-1-1-1024-2-2-2 |             2.00 |       80.00 |  8192.00 |     2.00 |    2.00 | 300.00 |         2.00 |                         913.52 |                      906.03 |         0.00 |                                                     319653.00 |                                              87503.00 |

#### Aggregated Parallel

| DBMS                    |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |             1.00 |      160.00 | 16384.00 |        1.00 | 300.00 |         2.00 |                        1982.75 |                     1966.45 |         0.00 |                                                     280744.00 |                                              80656.00 |
| PostgreSQL-1-1-1024-1-2 |             1.00 |      160.00 | 16384.00 |        2.00 | 300.00 |         2.00 |                        1838.27 |                     1822.86 |         0.00 |                                                     318089.00 |                                              87014.50 |
| PostgreSQL-1-1-1024-2-1 |             2.00 |      160.00 | 16384.00 |        1.00 | 300.00 |         3.00 |                        1958.05 |                     1941.80 |         0.00 |                                                     284622.00 |                                              81682.00 |
| PostgreSQL-1-1-1024-2-2 |             2.00 |      160.00 | 16384.00 |        2.00 | 300.00 |         4.00 |                        1831.86 |                     1816.74 |         0.00 |                                                     319653.00 |                                              87301.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 1], [2, 1]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[1, 2], [1, 2]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1-1 |      252.00 |        1.00 |   1.00 |              228.57 |
| PostgreSQL-1-1-1024-1-2 |      252.00 |        1.00 |   2.00 |              228.57 |
| PostgreSQL-1-1-1024-2-1 |      261.00 |        1.00 |   1.00 |              220.69 |
| PostgreSQL-1-1-1024-2-2 |      261.00 |        1.00 |   2.00 |              220.69 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1-1 |       624.69 |      3.66 |           7.42 |                  9.06 |
| PostgreSQL-1-1-1024-1-2 |       624.69 |      3.66 |           7.42 |                  9.06 |
| PostgreSQL-1-1-1024-2-1 |      5982.68 |      4.08 |           8.58 |                 11.35 |
| PostgreSQL-1-1-1024-2-2 |      5982.68 |      4.08 |           8.58 |                 11.35 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1-1 |      1490.78 |     10.28 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-1-2 |      1490.78 |     10.28 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2-1 |      1342.16 |      9.81 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2-2 |      1342.16 |      9.81 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1-1 |      2280.76 |      9.42 |           9.53 |                 11.70 |
| PostgreSQL-1-1-1024-1-2 |      2437.13 |      8.56 |          10.30 |                 13.05 |
| PostgreSQL-1-1-1024-2-1 |      2240.26 |      8.95 |           9.55 |                 11.72 |
| PostgreSQL-1-1-1024-2-2 |      2075.44 |      8.44 |          10.21 |                 12.88 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1-1 |       549.32 |      2.17 |           1.64 |                  1.64 |
| PostgreSQL-1-1-1024-1-2 |       549.32 |      4.70 |           1.64 |                  1.64 |
| PostgreSQL-1-1-1024-2-1 |       574.79 |      2.12 |           0.77 |                  0.77 |
| PostgreSQL-1-1-1024-2-2 |       574.79 |      4.22 |           0.77 |                  0.77 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                    |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   16.00 |
| PostgreSQL-1-1-1024-1-2 |                     16.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   16.00 |
| PostgreSQL-1-1-1024-2-1 |                     15.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |
| PostgreSQL-1-1-1024-2-2 |                     15.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS                    |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |                      7.00 |                                    22.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-1-1024-1-2 |                     13.00 |                                    17.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-1-1024-2-1 |                      6.00 |                                    20.00 |                                             0.00 |                      156.00 |                                  156.00 |
| PostgreSQL-1-1-1024-2-2 |                      5.00 |                                    19.00 |                                             0.00 |                      160.00 |                                  160.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
