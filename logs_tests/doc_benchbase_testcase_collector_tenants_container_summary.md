## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 3015s 
* Code: 1778704497
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
  * Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197629
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197630
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197632
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197632
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197629
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197630
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197631
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197632
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778704497
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   tenant | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|---------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      421.00 |           4.00 |            0.00 |        172.00 |          245.00 |              1 |           1 |        0 | container      |             2 | False         |                8.55 |
| PostgreSQL-1-2 |                2 |    1 |      421.00 |           4.00 |            0.00 |        172.00 |          245.00 |              1 |           1 |        0 | container      |             2 | False         |                8.55 |
| PostgreSQL-2-1 |                1 |    1 |      415.00 |           3.00 |            0.00 |        176.00 |          236.00 |              1 |           1 |        1 | container      |             2 | False         |                8.67 |
| PostgreSQL-2-2 |                2 |    1 |      415.00 |           3.00 |            0.00 |        176.00 |          236.00 |              1 |           1 |        1 | container      |             2 | False         |                8.67 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       104.98 |                                                      63152.00 |                                              23993.00 |
| PostgreSQL-1-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        98.68 |                                                     100178.00 |                                              30348.00 |
| PostgreSQL-1-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.48 |                        0.48 |       101.48 |                                                    1138926.00 |                                             169215.00 |
| PostgreSQL-1-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.46 |        97.28 |                                                     107728.00 |                                              77528.00 |
| PostgreSQL-2-1-1-1 |             1.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.43 |                        0.43 |        90.98 |                                                      54752.00 |                                              24558.00 |
| PostgreSQL-2-1-2-1 |             1.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.46 |        97.28 |                                                      44304.00 |                                              22159.00 |
| PostgreSQL-2-2-1-1 |             2.00 |       10.00 |  1024.00 |     1.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.46 |        97.28 |                                                    4701521.00 |                                             738201.00 |
| PostgreSQL-2-2-2-1 |             2.00 |       10.00 |  1024.00 |     2.00 |    1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        99.38 |                                                    1393726.00 |                                             364734.00 |

#### Per Phase

| DBMS             |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 |             1.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.50 |                        0.50 |       104.98 |                                                      63152.00 |                                              23993.00 |
| PostgreSQL-1-1-2 |             1.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        98.68 |                                                     100178.00 |                                              30348.00 |
| PostgreSQL-1-2-1 |             2.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.48 |                        0.48 |       101.48 |                                                    1138926.00 |                                             169215.00 |
| PostgreSQL-1-2-2 |             2.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.47 |                        0.46 |        97.28 |                                                     107728.00 |                                              77528.00 |
| PostgreSQL-2-1-1 |             1.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.43 |                        0.43 |        90.98 |                                                      54752.00 |                                              24558.00 |
| PostgreSQL-2-1-2 |             1.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.47 |                        0.46 |        97.28 |                                                      44304.00 |                                              22159.00 |
| PostgreSQL-2-2-1 |             2.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.47 |                        0.46 |        97.28 |                                                    4701521.00 |                                             738201.00 |
| PostgreSQL-2-2-2 |             2.00 |       10.00 |  1024.00 |        1.00 | 300.00 |         0.00 |                           0.47 |                        0.47 |        99.38 |                                                    1393726.00 |                                             364734.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        43.12 |      0.39 |           5.84 |                  5.98 |
| PostgreSQL-1-1-2 |        43.12 |      0.39 |           5.84 |                  5.98 |
| PostgreSQL-2-1-1 |        42.71 |      0.45 |           5.83 |                  5.98 |
| PostgreSQL-2-1-2 |        42.71 |      0.45 |           5.83 |                  5.98 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         8.76 |      0.11 |           0.24 |                  0.24 |
| PostgreSQL-1-1-2 |         8.76 |      0.11 |           0.24 |                  0.24 |
| PostgreSQL-2-1-1 |         8.55 |      0.10 |           0.24 |                  0.24 |
| PostgreSQL-2-1-2 |         8.55 |      0.10 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         4.39 |      0.02 |           5.88 |                  6.03 |
| PostgreSQL-1-1-2 |         4.87 |      0.02 |           5.88 |                  6.03 |
| PostgreSQL-1-2-1 |         5.51 |      0.03 |           5.78 |                  5.90 |
| PostgreSQL-1-2-2 |         4.51 |      0.02 |           5.78 |                  5.91 |
| PostgreSQL-2-1-1 |         4.80 |      0.02 |           5.88 |                  6.03 |
| PostgreSQL-2-1-2 |         4.19 |      0.02 |           5.88 |                  6.03 |
| PostgreSQL-2-2-1 |         5.17 |      0.05 |           5.78 |                  5.90 |
| PostgreSQL-2-2-2 |         4.65 |      0.02 |           5.78 |                  5.91 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        10.30 |      0.09 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2 |        48.12 |      1.00 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1 |         9.05 |      0.11 |           0.10 |                  0.11 |
| PostgreSQL-1-2-2 |        29.08 |      0.83 |           0.11 |                  0.11 |
| PostgreSQL-2-1-1 |        31.86 |      0.70 |           0.11 |                  0.11 |
| PostgreSQL-2-1-2 |        31.87 |      0.73 |           0.23 |                  0.23 |
| PostgreSQL-2-2-1 |        33.08 |      0.72 |           0.11 |                  0.11 |
| PostgreSQL-2-2-2 |        34.29 |      0.87 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-1-2 |                      2.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-1-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                     11.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-2-1-2 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-2-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    4.00 |
| PostgreSQL-2-2-2 |                     11.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
