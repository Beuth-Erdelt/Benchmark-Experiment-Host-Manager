## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 3015s 
* Code: 1778692834
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
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
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197611
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778692834
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197612
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778692834
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197613
  * volume_size:100G
  * volume_used:4.9G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778692834
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197614
  * volume_size:100G
  * volume_used:4.9G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778692834
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |     1181.00 |           4.00 |            0.00 |        549.00 |          628.00 |              1 |          |                |             0 | False         |               48.77 |
| PostgreSQL-1-2 |                2 |   16 |     1181.00 |           4.00 |            0.00 |        549.00 |          628.00 |              1 |          |                |             0 | False         |               48.77 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |         0.00 |                         169.80 |                      168.60 |         0.00 |                                                    1034409.00 |                                             235151.00 |
| PostgreSQL-1-1-1-2 |             1.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |         0.00 |                         169.86 |                      168.48 |         0.00 |                                                    1027137.00 |                                             235350.00 |
| PostgreSQL-1-1-1-3 |             1.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         0.00 |                         170.51 |                      169.29 |         0.00 |                                                    1039781.00 |                                             234515.00 |
| PostgreSQL-1-1-1-4 |             1.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         1.00 |                         166.23 |                      165.07 |         0.00 |                                                    1049999.00 |                                             239908.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                          91.77 |                       91.04 |         0.00 |                                                     899220.00 |                                             217400.00 |
| PostgreSQL-1-1-2-2 |             1.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         0.00 |                          91.25 |                       90.62 |         0.00 |                                                     923182.00 |                                             218775.00 |
| PostgreSQL-1-1-2-3 |             1.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                          91.09 |                       90.33 |         0.00 |                                                     912744.00 |                                             219270.00 |
| PostgreSQL-1-1-2-4 |             1.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         0.00 |                          91.48 |                       90.75 |         0.00 |                                                     905270.00 |                                             218171.00 |
| PostgreSQL-1-1-2-5 |             1.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         0.00 |                          91.94 |                       91.21 |         0.00 |                                                     906529.00 |                                             217096.00 |
| PostgreSQL-1-1-2-6 |             1.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         1.00 |                          90.65 |                       90.03 |         0.00 |                                                     919798.00 |                                             219912.00 |
| PostgreSQL-1-1-2-7 |             1.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         0.00 |                          91.74 |                       91.02 |         0.00 |                                                     897218.00 |                                             217520.00 |
| PostgreSQL-1-1-2-8 |             1.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         1.00 |                          92.74 |                       92.02 |         0.00 |                                                     910038.00 |                                             215272.00 |
| PostgreSQL-1-2-1-1 |             2.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |         0.00 |                         134.53 |                      133.61 |         0.00 |                                                    1297980.00 |                                             296858.00 |
| PostgreSQL-1-2-1-2 |             2.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |         0.00 |                         133.21 |                      132.46 |         0.00 |                                                    1315461.00 |                                             299643.00 |
| PostgreSQL-1-2-1-3 |             2.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         0.00 |                         133.63 |                      132.74 |         0.00 |                                                    1292242.00 |                                             298919.00 |
| PostgreSQL-1-2-1-4 |             2.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         1.00 |                         131.88 |                      130.95 |         0.00 |                                                    1356793.00 |                                             302875.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                          78.71 |                       78.04 |         0.00 |                                                    1070846.00 |                                             253864.00 |
| PostgreSQL-1-2-2-2 |             2.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         0.00 |                          76.63 |                       76.07 |         0.00 |                                                    1091042.00 |                                             260453.00 |
| PostgreSQL-1-2-2-3 |             2.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                          77.23 |                       76.78 |         0.00 |                                                    1059774.00 |                                             258870.00 |
| PostgreSQL-1-2-2-4 |             2.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         0.00 |                          76.24 |                       75.73 |         0.00 |                                                    1073323.00 |                                             262039.00 |
| PostgreSQL-1-2-2-5 |             2.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         0.00 |                          79.21 |                       78.66 |         0.00 |                                                    1075567.00 |                                             252045.00 |
| PostgreSQL-1-2-2-6 |             2.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                          77.10 |                       76.56 |         0.00 |                                                    1078768.00 |                                             259076.00 |
| PostgreSQL-1-2-2-7 |             2.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         0.00 |                          77.42 |                       76.87 |         0.00 |                                                    1101101.00 |                                             257790.00 |
| PostgreSQL-1-2-2-8 |             2.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         0.00 |                          78.83 |                       78.27 |         0.00 |                                                    1078692.00 |                                             253373.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |      160.00 | 20480.00 |        4.00 | 300.00 |         1.00 |                         676.41 |                      671.44 |         0.00 |                                                    1049999.00 |                                             236231.00 |
| PostgreSQL-1-1-2 |             1.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         2.00 |                         732.65 |                      727.02 |         0.00 |                                                     923182.00 |                                             217927.00 |
| PostgreSQL-1-2-1 |             2.00 |      160.00 | 20480.00 |        4.00 | 300.00 |         1.00 |                         533.25 |                      529.76 |         0.00 |                                                    1356793.00 |                                             299573.75 |
| PostgreSQL-1-2-2 |             2.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         0.00 |                         621.38 |                      616.97 |         0.00 |                                                    1101101.00 |                                             257188.75 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       547.92 |      1.42 |           7.50 |                  9.13 |
| PostgreSQL-1-1-2 |       547.92 |      1.42 |           7.50 |                  9.13 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1425.30 |      6.60 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2 |      1425.30 |      6.60 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       810.52 |      3.82 |           9.03 |                 10.96 |
| PostgreSQL-1-1-2 |       913.44 |      3.52 |           9.43 |                 11.66 |
| PostgreSQL-1-2-1 |      2395.08 |      3.34 |           8.43 |                 10.75 |
| PostgreSQL-1-2-2 |       810.78 |      3.48 |           8.99 |                 11.51 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       318.15 |      1.29 |           0.34 |                  0.34 |
| PostgreSQL-1-1-2 |       306.11 |      4.68 |           0.34 |                  0.34 |
| PostgreSQL-1-2-1 |       266.81 |      1.71 |           0.34 |                  0.34 |
| PostgreSQL-1-2-2 |       246.08 |      3.77 |           0.34 |                  0.34 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |
| PostgreSQL-1-1-2 |                     16.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     20.00 |                                    18.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-1-2 |                     15.00 |                                     9.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-1 |                     25.00 |                                     7.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                    23.00 |                                             0.00 |                      161.00 |                                  160.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
