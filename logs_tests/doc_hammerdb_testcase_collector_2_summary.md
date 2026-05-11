## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3080s 
* Code: 1778484673
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
  * disk:200546
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778484673
* PostgreSQL-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:210388
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778484673
* PostgreSQL-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:200548
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778484673
* PostgreSQL-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209502
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778484673

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |       code | configuration   |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------:|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 | 1778484673 | PostgreSQL-1    |                1 |   16 |      138.00 |           2.00 |            0.00 |         39.00 |           97.00 |              1 | None           |             0 | False         |              417.39 |
| PostgreSQL-1-2 | 1778484673 | PostgreSQL-1    |                2 |   16 |      139.00 |           2.00 |            0.00 |         39.00 |           98.00 |              1 | None           |             0 | False         |              414.39 |

### Execution

#### Per Connection

| DBMS               |   experiment_run |   vusers |   client |      NOPM |       TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-------------------|-----------------:|---------:|---------:|----------:|----------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1 |             1.00 |    32.00 |     1.00 | 133186.00 | 307525.00 |         0.00 |       5.00 |     0.00 |      11.79 |      19.21 |
| PostgreSQL-1-1-2-1 |             1.00 |    16.00 |     2.00 |  16883.00 |  38978.00 |         0.00 |       5.00 |     0.00 |       1.43 |       2.67 |
| PostgreSQL-1-1-2-1 |             1.00 |    16.00 |     2.00 |  16880.00 |  38964.00 |         0.00 |       5.00 |     0.00 |       1.36 |       2.52 |
| PostgreSQL-1-2-1-1 |             2.00 |    32.00 |     1.00 | 124506.00 | 286164.00 |         0.00 |       5.00 |     0.00 |       7.44 |      21.39 |
| PostgreSQL-1-2-2-1 |             2.00 |    16.00 |     2.00 |  17467.00 |  40569.00 |         0.00 |       5.00 |     0.00 |       1.42 |       2.64 |
| PostgreSQL-1-2-2-1 |             2.00 |    16.00 |     2.00 |  17449.00 |  40576.00 |         0.00 |       5.00 |     0.00 |       1.40 |       2.58 |

#### Per Phase

| DBMS             |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 |             1.00 |    32.00 |     1.00 |        1.00 |      11.79 |      19.21 |         0.00 | 133186.00 | 307525.00 |       5.00 |     0.00 |
| PostgreSQL-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |       1.43 |       2.67 |         0.00 |  16881.50 |  38971.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-1 |             2.00 |    32.00 |     1.00 |        1.00 |       7.44 |      21.39 |         0.00 | 124506.00 | 286164.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |       1.42 |       2.64 |         0.00 |  17458.00 |  40572.50 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        90.85 |      2.70 |           7.13 |                  7.83 |
| PostgreSQL-1-1-2 |        90.85 |      2.70 |           7.13 |                  7.83 |
| PostgreSQL-1-2-1 |     25726.58 |      2.19 |          10.31 |                 13.93 |
| PostgreSQL-1-2-2 |     25726.58 |      2.19 |          10.31 |                 13.93 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-1 |       259.78 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-2-2 |       259.78 |      0.00 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |     12202.62 |     30.43 |          10.61 |                 13.87 |
| PostgreSQL-1-1-2 |     13345.81 |     31.80 |          11.77 |                 15.37 |
| PostgreSQL-1-2-1 |     11916.65 |     29.52 |          10.33 |                 13.31 |
| PostgreSQL-1-2-2 |     13483.38 |     31.77 |          11.61 |                 15.07 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       401.17 |      1.78 |           1.17 |                  1.17 |
| PostgreSQL-1-1-2 |       401.17 |      0.91 |           1.17 |                  1.17 |
| PostgreSQL-1-2-1 |       371.22 |      1.70 |           0.90 |                  0.90 |
| PostgreSQL-1-2-2 |       371.22 |      0.80 |           0.90 |                  0.90 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                     16.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                     17.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      7.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      4.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |
| PostgreSQL-1-2-1 |                      6.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-2-2 |                      4.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
