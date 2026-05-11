## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 3255s 
* Code: 1778424541
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
  * disk:197151
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778424541
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197152
  * volume_size:100G
  * volume_used:4.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778424541
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197153
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778424541
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197154
  * volume_size:100G
  * volume_used:4.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778424541
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |     1559.00 |           8.00 |            0.00 |        732.00 |          819.00 |              1 |                |             0 | False         |               36.95 |
| PostgreSQL-1-2 |                2 |   16 |     1559.00 |           8.00 |            0.00 |        732.00 |          819.00 |              1 |                |             0 | False         |               36.95 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |         0.00 |                          95.83 |                       95.22 |         0.00 |                                                    1970647.00 |                                             417009.00 |
| PostgreSQL-1-1-1-2 |             1.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |         0.00 |                          95.74 |                       95.09 |         0.00 |                                                    1999546.00 |                                             417769.00 |
| PostgreSQL-1-1-1-3 |             1.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         0.00 |                          93.34 |                       92.67 |         0.00 |                                                    2009154.00 |                                             428316.00 |
| PostgreSQL-1-1-1-4 |             1.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         0.00 |                          94.89 |                       94.30 |         0.00 |                                                    1972538.00 |                                             420821.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                          46.09 |                       45.70 |         0.00 |                                                    2057621.00 |                                             433702.00 |
| PostgreSQL-1-1-2-2 |             1.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         0.00 |                          47.57 |                       47.33 |         0.00 |                                                    1927908.00 |                                             418398.00 |
| PostgreSQL-1-1-2-3 |             1.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                          46.17 |                       45.85 |         0.00 |                                                    2015049.00 |                                             430829.00 |
| PostgreSQL-1-1-2-4 |             1.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         0.00 |                          47.55 |                       47.26 |         0.00 |                                                    1981454.00 |                                             419353.00 |
| PostgreSQL-1-1-2-5 |             1.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         0.00 |                          46.80 |                       46.51 |         0.00 |                                                    2034691.00 |                                             425993.00 |
| PostgreSQL-1-1-2-6 |             1.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                          46.84 |                       46.41 |         0.00 |                                                    2016044.00 |                                             425959.00 |
| PostgreSQL-1-1-2-7 |             1.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         0.00 |                          45.21 |                       44.90 |         0.00 |                                                    2137613.00 |                                             440531.00 |
| PostgreSQL-1-1-2-8 |             1.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         0.00 |                          47.24 |                       46.95 |         0.00 |                                                    1957745.00 |                                             421022.00 |
| PostgreSQL-1-2-1-1 |             2.00 |       40.00 |  5120.00 |     1.00 |    1.00 | 300.00 |         0.00 |                          69.83 |                       69.49 |         0.00 |                                                    2693980.00 |                                             568051.00 |
| PostgreSQL-1-2-1-2 |             2.00 |       40.00 |  5120.00 |     1.00 |    2.00 | 300.00 |         0.00 |                          71.03 |                       70.68 |         0.00 |                                                    2620700.00 |                                             555860.00 |
| PostgreSQL-1-2-1-3 |             2.00 |       40.00 |  5120.00 |     1.00 |    3.00 | 300.00 |         0.00 |                          71.15 |                       70.79 |         0.00 |                                                    2555477.00 |                                             557365.00 |
| PostgreSQL-1-2-1-4 |             2.00 |       40.00 |  5120.00 |     1.00 |    4.00 | 300.00 |         0.00 |                          68.99 |                       68.58 |         0.00 |                                                    2760155.00 |                                             573825.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       20.00 |  2560.00 |     2.00 |    1.00 | 300.00 |         0.00 |                          42.34 |                       42.03 |         0.00 |                                                    2262700.00 |                                             469466.00 |
| PostgreSQL-1-2-2-2 |             2.00 |       20.00 |  2560.00 |     2.00 |    2.00 | 300.00 |         1.00 |                          43.85 |                       43.54 |         0.00 |                                                    2192389.00 |                                             452677.00 |
| PostgreSQL-1-2-2-3 |             2.00 |       20.00 |  2560.00 |     2.00 |    3.00 | 300.00 |         0.00 |                          44.01 |                       43.73 |         0.00 |                                                    2241083.00 |                                             451575.00 |
| PostgreSQL-1-2-2-4 |             2.00 |       20.00 |  2560.00 |     2.00 |    4.00 | 300.00 |         0.00 |                          42.42 |                       42.14 |         0.00 |                                                    2345662.00 |                                             468609.00 |
| PostgreSQL-1-2-2-5 |             2.00 |       20.00 |  2560.00 |     2.00 |    5.00 | 300.00 |         0.00 |                          43.64 |                       43.36 |         0.00 |                                                    2292563.00 |                                             455729.00 |
| PostgreSQL-1-2-2-6 |             2.00 |       20.00 |  2560.00 |     2.00 |    6.00 | 300.00 |         0.00 |                          41.49 |                       41.19 |         0.00 |                                                    2325081.00 |                                             477762.00 |
| PostgreSQL-1-2-2-7 |             2.00 |       20.00 |  2560.00 |     2.00 |    7.00 | 300.00 |         0.00 |                          42.30 |                       42.07 |         0.00 |                                                    2264491.00 |                                             470041.00 |
| PostgreSQL-1-2-2-8 |             2.00 |       20.00 |  2560.00 |     2.00 |    8.00 | 300.00 |         0.00 |                          42.39 |                       42.11 |         0.00 |                                                    2310354.00 |                                             469255.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |      160.00 | 20480.00 |        4.00 | 300.00 |         0.00 |                         379.80 |                      377.29 |         0.00 |                                                    2009154.00 |                                             420978.75 |
| PostgreSQL-1-1-2 |             1.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         0.00 |                         373.48 |                      370.92 |         0.00 |                                                    2137613.00 |                                             426973.38 |
| PostgreSQL-1-2-1 |             2.00 |      160.00 | 20480.00 |        4.00 | 300.00 |         0.00 |                         281.00 |                      279.54 |         0.00 |                                                    2760155.00 |                                             563775.25 |
| PostgreSQL-1-2-2 |             2.00 |      160.00 | 20480.00 |        8.00 | 300.00 |         1.00 |                         342.43 |                      340.17 |         0.00 |                                                    2345662.00 |                                             464389.25 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       563.79 |      1.15 |           7.52 |                  9.12 |
| PostgreSQL-1-1-2 |       563.79 |      1.15 |           7.52 |                  9.12 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      1234.08 |      5.72 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2 |      1234.08 |      5.72 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       481.78 |      2.64 |           8.80 |                 10.63 |
| PostgreSQL-1-1-2 |       497.59 |      2.61 |           9.02 |                 11.01 |
| PostgreSQL-1-2-1 |       483.27 |      2.04 |           8.08 |                 10.10 |
| PostgreSQL-1-2-2 |       467.03 |      2.54 |           8.44 |                 10.59 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       205.91 |      0.98 |           0.33 |                  0.33 |
| PostgreSQL-1-1-2 |       201.12 |      1.44 |           0.33 |                  0.33 |
| PostgreSQL-1-2-1 |       190.65 |      0.74 |           0.30 |                  0.30 |
| PostgreSQL-1-2-2 |       184.20 |      2.57 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |
| PostgreSQL-1-1-2 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                    10.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-1-2 |                      7.00 |                                    15.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-2-1 |                     91.00 |                                    15.00 |                                             0.00 |                      160.00 |                                  160.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                    21.00 |                                             0.00 |                      160.00 |                                  160.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
