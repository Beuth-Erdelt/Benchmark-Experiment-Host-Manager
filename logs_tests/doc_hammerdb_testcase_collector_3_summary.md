## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 7152s 
* Code: 1778760601
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
  * Benchmarking is tested with [32] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:201021
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778760601
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209162
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778760601
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:201024
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778760601
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:210957
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778760601

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      146.00 |           3.00 |            0.00 |         39.00 |          104.00 |              1 |          16 |          | None           |             0 | False         |              394.52 |
| PostgreSQL-1-2 |                2 |   16 |      142.00 |           2.00 |            0.00 |         39.00 |          101.00 |              1 |          16 |          | None           |             0 | False         |              405.63 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   vusers |   client |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-------------------|-----------------:|---------:|---------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1 |                1 |       32 |        1 |       1 | 119809 | 275999 |         0.00 |          5 |        0 |      10.81 |      17.15 |
| PostgreSQL-1-1-2-1 |                1 |       16 |        2 |       1 |  27215 |  62880 |         0.00 |          5 |        0 |       1.23 |       2.01 |
| PostgreSQL-1-1-2-1 |                1 |       16 |        2 |       1 |  27203 |  62842 |         0.00 |          5 |        0 |       1.23 |       2.02 |
| PostgreSQL-1-2-1-1 |                2 |       32 |        1 |       1 | 138074 | 317878 |         0.00 |          5 |        0 |       8.87 |      19.39 |
| PostgreSQL-1-2-2-1 |                2 |       16 |        2 |       1 |  17951 |  41300 |         0.00 |          5 |        0 |       1.38 |       2.53 |
| PostgreSQL-1-2-2-1 |                2 |       16 |        2 |       1 |  17947 |  41357 |         0.00 |          5 |        0 |       1.36 |       2.56 |

#### Per Phase

| DBMS             |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 |             1.00 |    32.00 |     1.00 |        1.00 |      10.81 |      17.15 |         0.00 | 119809.00 | 275999.00 |       5.00 |     0.00 |
| PostgreSQL-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |       1.23 |       2.02 |         0.00 |  27209.00 |  62861.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-1 |             2.00 |    32.00 |     1.00 |        1.00 |       8.86 |      19.39 |         0.00 | 138074.00 | 317878.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |       1.38 |       2.56 |         0.00 |  17949.00 |  41328.50 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        89.59 |      1.90 |           7.00 |                  7.70 |
| PostgreSQL-1-1-2 |        89.59 |      1.90 |           7.00 |                  7.70 |
| PostgreSQL-1-2-1 |     23627.94 |      2.46 |          10.11 |                 13.53 |
| PostgreSQL-1-2-2 |     23627.94 |      2.46 |          10.11 |                 13.53 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       297.03 |      9.09 |           0.15 |                  0.15 |
| PostgreSQL-1-1-2 |       297.03 |      9.09 |           0.15 |                  0.15 |
| PostgreSQL-1-2-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-2 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |     10284.30 |     26.18 |          10.02 |                 12.76 |
| PostgreSQL-1-1-2 |     13285.63 |     31.73 |          11.55 |                 14.94 |
| PostgreSQL-1-2-1 |     11980.57 |     29.95 |          10.54 |                 13.75 |
| PostgreSQL-1-2-2 |     13309.14 |     31.76 |          11.80 |                 15.43 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       347.14 |      1.38 |           0.90 |                  0.90 |
| PostgreSQL-1-1-2 |       347.14 |      0.93 |           0.90 |                  0.90 |
| PostgreSQL-1-2-1 |       408.07 |      1.84 |           1.12 |                  1.12 |
| PostgreSQL-1-2-2 |       408.07 |      1.00 |           1.12 |                  1.12 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       10.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                     17.00 |                                     0.00 |                                             0.00 |                       10.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                     17.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      6.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      4.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                      6.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                      4.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
