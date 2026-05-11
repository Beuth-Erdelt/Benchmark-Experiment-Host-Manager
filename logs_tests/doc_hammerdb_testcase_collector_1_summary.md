## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3028s 
* Code: 1778481602
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.7.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:200541
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778481602
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:218239
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778481602
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:200543
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778481602
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:213915
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778481602

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |       code | configuration   |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------:|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 | 1778481602 | PostgreSQL-1    |                1 |   16 |      142.00 |           2.00 |            0.00 |         39.00 |          101.00 |              1 | None           |             0 | False         |              405.63 |
| PostgreSQL-1-2 | 1778481602 | PostgreSQL-1    |                2 |   16 |      141.00 |           2.00 |            0.00 |         39.00 |          100.00 |              1 | None           |             0 | False         |              408.51 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   vusers |   client |      NOPM |       TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-------------------|-----------------:|---------:|---------:|----------:|----------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1 |             1.00 |    16.00 |     1.00 | 374778.00 | 861703.00 |         0.00 |       5.00 |     1.00 |       1.83 |       2.54 |
| PostgreSQL-1-1-2-1 |             1.00 |     8.00 |     2.00 |  44584.00 | 102745.00 |         0.00 |       5.00 |     0.00 |       1.17 |       1.88 |
| PostgreSQL-1-1-2-1 |             1.00 |     8.00 |     2.00 |  44593.00 | 102638.00 |         0.00 |       5.00 |     0.00 |       1.23 |       2.00 |
| PostgreSQL-1-2-1-1 |             2.00 |    16.00 |     1.00 | 270148.00 | 621321.00 |         0.00 |       5.00 |     0.00 |       2.25 |       3.01 |
| PostgreSQL-1-2-2-1 |             2.00 |     8.00 |     2.00 |  40823.00 |  94327.00 |         0.00 |       5.00 |     0.00 |       1.14 |       1.78 |
| PostgreSQL-1-2-2-1 |             2.00 |     8.00 |     2.00 |  40791.00 |  94236.00 |         0.00 |       5.00 |     0.00 |       1.13 |       1.71 |

#### Per Phase

| DBMS             |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |       1.83 |       2.54 |         0.00 | 374778.00 | 861703.00 |       5.00 |     1.00 |
| PostgreSQL-1-1-2 |             1.00 |    16.00 |     2.00 |        2.00 |       1.23 |       2.00 |         0.00 |  44588.50 | 102691.50 |       5.00 |     0.00 |
| PostgreSQL-1-2-1 |             2.00 |    16.00 |     1.00 |        1.00 |       2.25 |       3.01 |         0.00 | 270148.00 | 621321.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-2 |             2.00 |    16.00 |     2.00 |        2.00 |       1.14 |       1.78 |         0.00 |  40807.00 |  94281.50 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        88.37 |      2.70 |           7.00 |                  7.70 |
| PostgreSQL-1-1-2 |        88.37 |      2.70 |           7.00 |                  7.70 |
| PostgreSQL-1-2-1 |     10735.26 |      2.33 |          12.19 |                 15.52 |
| PostgreSQL-1-2-2 |     10735.26 |      2.33 |          12.19 |                 15.52 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       188.82 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-1-2 |       188.82 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-2-1 |       207.66 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-2-2 |       207.66 |      0.00 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |      4121.14 |     10.67 |          11.82 |                 16.00 |
| PostgreSQL-1-1-2 |      6349.52 |     15.58 |          12.66 |                 16.00 |
| PostgreSQL-1-2-1 |      4051.12 |     10.38 |          10.74 |                 14.52 |
| PostgreSQL-1-2-2 |      6529.46 |     15.58 |          11.55 |                 15.94 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       791.82 |      2.49 |           2.10 |                  2.10 |
| PostgreSQL-1-1-2 |       791.82 |      2.76 |           2.10 |                  2.10 |
| PostgreSQL-1-2-1 |       613.61 |      1.70 |           1.36 |                  1.36 |
| PostgreSQL-1-2-2 |       613.61 |      1.92 |           1.36 |                  1.36 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       12.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                     16.00 |                                     0.00 |                                             0.00 |                       12.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       11.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                     16.00 |                                     0.00 |                                             0.00 |                       11.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     12.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      5.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                      8.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                      5.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
