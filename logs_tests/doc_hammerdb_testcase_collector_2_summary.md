## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3970s 
* Code: 1778756497
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
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
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
  * disk:197712
  * volume_size:15G
  * volume_used:3.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778756497
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197713
  * volume_size:15G
  * volume_used:3.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778756497
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197715
  * volume_size:15G
  * volume_used:4.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778756497
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197716
  * volume_size:15G
  * volume_used:4.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778756497

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      386.00 |           3.00 |            0.00 |        159.00 |          224.00 |              1 |          16 |          | None           |             0 | False         |              149.22 |
| PostgreSQL-1-2 |                2 |   16 |      386.00 |           3.00 |            0.00 |        159.00 |          224.00 |              1 |          16 |          | None           |             0 | False         |              149.22 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   vusers |   client |   child |   NOPM |   TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-------------------|-----------------:|---------:|---------:|--------:|-------:|------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1 |                1 |       32 |        1 |       1 |   7416 | 17249 |         0.00 |          5 |        0 |       0.00 |       0.00 |
| PostgreSQL-1-1-2-1 |                1 |       16 |        2 |       1 |   9138 | 21018 |         0.00 |          5 |        0 |     283.75 |     491.58 |
| PostgreSQL-1-1-2-1 |                1 |       16 |        2 |       1 |   9170 | 21094 |         0.00 |          5 |        0 |     275.02 |     472.51 |
| PostgreSQL-1-2-1-1 |                2 |       32 |        1 |       1 |   6855 | 15842 |         0.00 |          5 |        0 |     341.81 |     570.89 |
| PostgreSQL-1-2-2-1 |                2 |       16 |        2 |       1 |  10070 | 23399 |         0.00 |          5 |        0 |       0.00 |       0.00 |
| PostgreSQL-1-2-2-1 |                2 |       16 |        2 |       1 |  10067 | 23397 |         0.00 |          5 |        0 |       0.00 |       0.00 |

#### Per Phase

| DBMS             |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |     NOPM |      TPM |   duration |   errors |
|:-----------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 |             1.00 |    32.00 |     1.00 |        1.00 |       0.00 |       0.00 |         0.00 |  7416.00 | 17249.00 |       5.00 |     0.00 |
| PostgreSQL-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |     283.75 |     491.58 |         0.00 |  9154.00 | 21056.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-1 |             2.00 |    32.00 |     1.00 |        1.00 |     341.81 |     570.89 |         0.00 |  6855.00 | 15842.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |       0.00 |       0.00 |         0.00 | 10068.50 | 23398.00 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       109.72 |      0.81 |           7.13 |                  8.75 |
| PostgreSQL-1-1-2 |       109.72 |      0.81 |           7.13 |                  8.75 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       277.71 |      4.85 |           0.15 |                  0.16 |
| PostgreSQL-1-1-2 |       277.71 |      4.85 |           0.15 |                  0.16 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       272.65 |      1.38 |           7.60 |                  9.33 |
| PostgreSQL-1-1-2 |       302.96 |      1.05 |           7.91 |                  9.81 |
| PostgreSQL-1-2-1 |       700.10 |      0.84 |           7.57 |                  9.48 |
| PostgreSQL-1-2-2 |       308.38 |      1.24 |           7.49 |                  9.54 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        28.26 |      0.11 |           0.17 |                  0.17 |
| PostgreSQL-1-1-2 |        28.26 |      0.14 |           0.17 |                  0.17 |
| PostgreSQL-1-2-1 |        24.36 |      0.09 |           0.16 |                  0.16 |
| PostgreSQL-1-2-2 |        27.59 |      0.14 |           0.16 |                  0.16 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     18.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                     18.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      3.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                      4.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                     12.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
