## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2772s 
* Code: 1776754749
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
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
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247609
  * datadisk:4307
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776754749
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247610
  * datadisk:4525
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776754749
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247611
  * datadisk:4686
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776754749
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247611
  * datadisk:4794
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776754749
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                      |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1-2 |             1.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |         0.00 |                         108.69 |                      107.97 |         0.00 |                                                    1744733.00 |                                             366002.00 |
| PostgreSQL-1-1-1024-1-1-3 |             1.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |         1.00 |                         108.97 |                      108.13 |         0.00 |                                                    1663818.00 |                                             365574.00 |
| PostgreSQL-1-1-1024-1-1-4 |             1.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         0.00 |                         106.64 |                      105.98 |         0.00 |                                                    1745407.00 |                                             372692.00 |
| PostgreSQL-1-1-1024-1-1-1 |             1.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         0.00 |                         108.91 |                      108.25 |         0.00 |                                                    1687690.00 |                                             365861.00 |
| PostgreSQL-1-1-1024-1-2-2 |             1.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                          48.20 |                       47.92 |         0.00 |                                                    1817576.00 |                                             414014.00 |
| PostgreSQL-1-1-1024-1-2-5 |             1.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         0.00 |                          48.54 |                       48.17 |         0.00 |                                                    1889149.00 |                                             410942.00 |
| PostgreSQL-1-1-1024-1-2-8 |             1.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                          47.61 |                       47.32 |         0.00 |                                                    1916724.00 |                                             419198.00 |
| PostgreSQL-1-1-1024-1-2-6 |             1.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         0.00 |                          48.41 |                       48.11 |         0.00 |                                                    1881100.00 |                                             412434.00 |
| PostgreSQL-1-1-1024-1-2-1 |             1.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         0.00 |                          48.84 |                       48.51 |         0.00 |                                                    1850373.00 |                                             409045.00 |
| PostgreSQL-1-1-1024-1-2-4 |             1.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                          46.74 |                       46.41 |         0.00 |                                                    1938737.00 |                                             426981.00 |
| PostgreSQL-1-1-1024-1-2-7 |             1.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         0.00 |                          47.96 |                       47.67 |         0.00 |                                                    1895723.00 |                                             416147.00 |
| PostgreSQL-1-1-1024-1-2-3 |             1.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         0.00 |                          48.11 |                       47.82 |         0.00 |                                                    1890551.00 |                                             414449.00 |
| PostgreSQL-1-1-1024-2-1-3 |             2.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |         0.00 |                          80.17 |                       79.81 |         0.00 |                                                    2299240.00 |                                             498261.00 |
| PostgreSQL-1-1-1024-2-1-2 |             2.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |         0.00 |                          79.63 |                       79.16 |         0.00 |                                                    2281057.00 |                                             501793.00 |
| PostgreSQL-1-1-1024-2-1-4 |             2.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         0.00 |                          79.76 |                       79.32 |         0.00 |                                                    2301616.00 |                                             500717.00 |
| PostgreSQL-1-1-1024-2-1-1 |             2.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         0.00 |                          79.20 |                       78.76 |         0.00 |                                                    2311261.00 |                                             503800.00 |
| PostgreSQL-1-1-1024-2-2-1 |             2.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                          57.86 |                       57.49 |         0.00 |                                                    1546193.00 |                                             344360.00 |
| PostgreSQL-1-1-1024-2-2-8 |             2.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         0.00 |                          56.59 |                       56.14 |         0.00 |                                                    1538641.00 |                                             351765.00 |
| PostgreSQL-1-1-1024-2-2-3 |             2.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                          56.78 |                       56.48 |         0.00 |                                                    1581547.00 |                                             350617.00 |
| PostgreSQL-1-1-1024-2-2-2 |             2.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         0.00 |                          57.54 |                       57.09 |         0.00 |                                                    1514894.00 |                                             346056.00 |
| PostgreSQL-1-1-1024-2-2-7 |             2.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         0.00 |                          58.05 |                       57.65 |         0.00 |                                                    1532749.00 |                                             343332.00 |
| PostgreSQL-1-1-1024-2-2-4 |             2.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                          56.41 |                       56.00 |         0.00 |                                                    1520573.00 |                                             353591.00 |
| PostgreSQL-1-1-1024-2-2-6 |             2.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         0.00 |                          56.62 |                       56.24 |         0.00 |                                                    1541436.00 |                                             351194.00 |
| PostgreSQL-1-1-1024-2-2-5 |             2.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         0.00 |                          57.32 |                       56.92 |         0.00 |                                                    1547466.00 |                                             347151.00 |

#### Aggregated Parallel

| DBMS                    |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-1 |             1.00 |      160.00 | 20480.00 |        4.00 | 300.00 |         1.00 |                         433.22 |                      430.34 |         0.00 |                                                    1745407.00 |                                             367532.25 |
| PostgreSQL-1-1-1024-1-2 |             1.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         0.00 |                         384.40 |                      381.94 |         0.00 |                                                    1938737.00 |                                             415401.25 |
| PostgreSQL-1-1-1024-2-1 |             2.00 |      160.00 | 20480.00 |        4.00 | 300.00 |         0.00 |                         318.75 |                      317.05 |         0.00 |                                                    2311261.00 |                                             501142.75 |
| PostgreSQL-1-1-1024-2-2 |             2.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         0.00 |                         457.17 |                      454.01 |         0.00 |                                                    1581547.00 |                                             348508.25 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024-5 - Pods [[1], [1]]
* DBMS PostgreSQL-1-1-1024-4 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-8 - Pods [[1], [1]]
* DBMS PostgreSQL-1-1-1024-3 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-6 - Pods [[1], [1]]
* DBMS PostgreSQL-1-1-1024-2 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-1-1-1024-7 - Pods [[1], [1]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[4, 8], [4, 8]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1-1 |      716.00 |        1.00 |   4.00 |               80.45 |
| PostgreSQL-1-1-1024-1-2 |      716.00 |        1.00 |   8.00 |               80.45 |
| PostgreSQL-1-1-1024-2-1 |      716.00 |        1.00 |   4.00 |               80.45 |
| PostgreSQL-1-1-1024-2-2 |      716.00 |        1.00 |   8.00 |               80.45 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776754749-PostgreSQL-1-1-1024-1-1 |       568.11 |      1.27 |           7.53 |                  9.15 |
| 1776754749-PostgreSQL-1-1-1024-1-2 |       568.11 |      1.27 |           7.53 |                  9.15 |

### Loading phase: component loader

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776754749-PostgreSQL-1-1-1024-1-1 |      1340.24 |      5.54 |           0.26 |                  0.26 |
| 1776754749-PostgreSQL-1-1-1024-1-2 |      1340.24 |      5.54 |           0.26 |                  0.26 |

### Execution phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776754749-PostgreSQL-1-1-1024-1-1 |       554.00 |      2.70 |           8.85 |                 10.69 |
| 1776754749-PostgreSQL-1-1-1024-1-2 |       486.08 |      2.54 |           9.02 |                 11.01 |
| 1776754749-PostgreSQL-1-1-1024-2-1 |      1679.78 |      2.01 |           8.09 |                 10.13 |
| 1776754749-PostgreSQL-1-1-1024-2-2 |       631.07 |      2.77 |           8.61 |                 10.83 |

### Execution phase: component benchmarker

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776754749-PostgreSQL-1-1-1024-1-1 |       265.18 |      1.55 |           0.34 |                  0.34 |
| 1776754749-PostgreSQL-1-1-1024-1-2 |       260.56 |      3.31 |           0.34 |                  0.34 |
| 1776754749-PostgreSQL-1-1-1024-2-1 |       181.07 |      1.25 |           0.30 |                  0.30 |
| 1776754749-PostgreSQL-1-1-1024-2-2 |       188.94 |      2.50 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776754749-PostgreSQL-1-1-1024-1-1 |                        16 |                                        0 |                                                0 |                          17 |                                      16 |
| 1776754749-PostgreSQL-1-1-1024-1-2 |                        16 |                                        0 |                                                0 |                          17 |                                      16 |

#### Execution phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776754749-PostgreSQL-1-1-1024-1-1 |                      9.00 |                                    25.00 |                                             0.00 |                      160.00 |                                  160.00 |
| 1776754749-PostgreSQL-1-1-1024-1-2 |                      4.00 |                                    28.00 |                                             0.00 |                      160.00 |                                  160.00 |
| 1776754749-PostgreSQL-1-1-1024-2-1 |                      2.00 |                                    10.00 |                                             0.00 |                      160.00 |                                  160.00 |
| 1776754749-PostgreSQL-1-1-1024-2-2 |                     12.00 |                                    10.00 |                                             0.00 |                      161.00 |                                  160.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Workflow not as planned
