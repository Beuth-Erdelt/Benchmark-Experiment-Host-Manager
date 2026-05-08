## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2606s 
* Code: 1777969641
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.6.
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
* PostgreSQL-BHT-16-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:253074
  * datadisk:3282
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777969641
* PostgreSQL-BHT-16-1-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:261478
  * datadisk:11685
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777969641
* PostgreSQL-BHT-16-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:253091
  * datadisk:3298
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777969641
* PostgreSQL-BHT-16-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:262124
  * datadisk:12331
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777969641

### Execution

| DBMS                    |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-BHT-16-1-1-1 |             1.00 |    32.00 |     1.00 |        1.00 |       7.75 |      23.31 |         0.00 | 113991.00 | 262382.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |       1.46 |       2.67 |         0.00 |  10518.50 |  24289.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-2-1 |             2.00 |    32.00 |     1.00 |        1.00 |      10.32 |      18.35 |         0.00 | 127870.00 | 294706.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |       1.31 |       2.32 |         0.00 |  23794.50 |  54888.50 |       5.00 |     0.00 |

* Warehouses: 16

### Workflow

#### Actual

* DBMS PostgreSQL-BHT-16-1 - Pods [[2, 1], [2, 1]]

#### Planned

* DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2], [1, 2]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Imported warehouses [1/h] |
|:------------------------|------------:|------------:|-------:|----------------------------:|
| PostgreSQL-BHT-16-1-1-1 |       39.00 |        1.00 |   1.00 |                     1476.92 |
| PostgreSQL-BHT-16-1-1-2 |       39.00 |        1.00 |   2.00 |                     1476.92 |
| PostgreSQL-BHT-16-1-2-1 |       39.00 |        1.00 |   1.00 |                     1476.92 |
| PostgreSQL-BHT-16-1-2-2 |       39.00 |        1.00 |   2.00 |                     1476.92 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777969641-PostgreSQL-BHT-16-1-1-1 |        88.09 |      1.74 |           7.00 |                  7.69 |
| 1777969641-PostgreSQL-BHT-16-1-1-2 |        88.09 |      1.74 |           7.00 |                  7.69 |
| 1777969641-PostgreSQL-BHT-16-1-2-1 |        77.90 |      2.44 |           9.79 |                 12.90 |
| 1777969641-PostgreSQL-BHT-16-1-2-2 |        77.90 |      2.44 |           9.79 |                 12.90 |

### Loading phase: component loader

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777969641-PostgreSQL-BHT-16-1-1-1 |        96.00 |      0.00 |           0.15 |                  0.15 |
| 1777969641-PostgreSQL-BHT-16-1-1-2 |        96.00 |      0.00 |           0.15 |                  0.15 |
| 1777969641-PostgreSQL-BHT-16-1-2-1 |       206.12 |      0.00 |           0.15 |                  0.15 |
| 1777969641-PostgreSQL-BHT-16-1-2-2 |       206.12 |      0.00 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777969641-PostgreSQL-BHT-16-1-1-1 |     11630.04 |     28.95 |          10.19 |                 13.07 |
| 1777969641-PostgreSQL-BHT-16-1-1-2 |     13499.66 |     31.88 |          11.21 |                 14.30 |
| 1777969641-PostgreSQL-BHT-16-1-2-1 |     11141.70 |     28.41 |          10.35 |                 13.40 |
| 1777969641-PostgreSQL-BHT-16-1-2-2 |     13206.13 |     31.78 |          11.70 |                 15.25 |

### Execution phase: component benchmarker

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777969641-PostgreSQL-BHT-16-1-1-1 |       334.62 |      1.57 |           0.84 |                  0.84 |
| 1777969641-PostgreSQL-BHT-16-1-1-2 |       334.62 |      0.67 |           0.84 |                  0.84 |
| 1777969641-PostgreSQL-BHT-16-1-2-1 |       370.71 |      1.47 |           1.16 |                  1.16 |
| 1777969641-PostgreSQL-BHT-16-1-2-2 |       370.71 |      0.95 |           1.16 |                  1.16 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1777969641-PostgreSQL-BHT-16-1-1-1 |                        17 |                                        0 |                                                0 |                          14 |                                       0 |
| 1777969641-PostgreSQL-BHT-16-1-1-2 |                        17 |                                        0 |                                                0 |                          14 |                                       0 |
| 1777969641-PostgreSQL-BHT-16-1-2-1 |                        18 |                                        0 |                                                0 |                          14 |                                       0 |
| 1777969641-PostgreSQL-BHT-16-1-2-2 |                        18 |                                        0 |                                                0 |                          14 |                                       0 |

#### Execution phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1777969641-PostgreSQL-BHT-16-1-1-1 |                      7.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |
| 1777969641-PostgreSQL-BHT-16-1-1-2 |                      3.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |
| 1777969641-PostgreSQL-BHT-16-1-2-1 |                      7.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| 1777969641-PostgreSQL-BHT-16-1-2-2 |                      4.00 |                                     0.00 |                                             0.00 |                       32.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
