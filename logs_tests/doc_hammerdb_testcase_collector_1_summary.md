## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2589s 
* Code: 1777967002
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
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-BHT-16-1-1-1 uses docker image postgres:18.3
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
    * code:1777967002
* PostgreSQL-BHT-16-1-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:273497
  * datadisk:23704
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777967002
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
    * code:1777967002
* PostgreSQL-BHT-16-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:273552
  * datadisk:23759
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777967002

### Execution

| DBMS                    |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-BHT-16-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |       1.56 |       2.29 |         0.00 | 412073.00 | 948322.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-1-2 |             1.00 |    16.00 |     2.00 |        2.00 |       1.17 |       1.91 |         0.00 |  39938.00 |  92080.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-2-1 |             2.00 |    16.00 |     1.00 |        1.00 |       1.62 |       2.38 |         0.00 | 388919.00 | 894190.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-2-2 |             2.00 |    16.00 |     2.00 |        2.00 |       1.19 |       1.89 |         0.00 |  40576.00 |  93542.50 |       5.00 |     0.00 |

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
| 1777967002-PostgreSQL-BHT-16-1-1-1 |        77.81 |      1.46 |           7.00 |                  7.70 |
| 1777967002-PostgreSQL-BHT-16-1-1-2 |        77.81 |      1.46 |           7.00 |                  7.70 |
| 1777967002-PostgreSQL-BHT-16-1-2-1 |        87.55 |      2.86 |          13.69 |                 15.51 |
| 1777967002-PostgreSQL-BHT-16-1-2-2 |        87.55 |      2.86 |          13.69 |                 15.51 |

### Loading phase: component loader

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777967002-PostgreSQL-BHT-16-1-1-1 |       115.00 |      0.00 |           0.15 |                  0.15 |
| 1777967002-PostgreSQL-BHT-16-1-1-2 |       115.00 |      0.00 |           0.15 |                  0.15 |
| 1777967002-PostgreSQL-BHT-16-1-2-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-2 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777967002-PostgreSQL-BHT-16-1-1-1 |      4220.60 |     10.47 |          12.53 |                 16.00 |
| 1777967002-PostgreSQL-BHT-16-1-1-2 |      6530.50 |     15.63 |          14.15 |                 16.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-1 |      4262.58 |     10.55 |          12.24 |                 16.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-2 |      6535.32 |     15.62 |          13.04 |                 16.00 |

### Execution phase: component benchmarker

| DBMS                               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777967002-PostgreSQL-BHT-16-1-1-1 |       766.56 |      1.98 |           2.67 |                  2.67 |
| 1777967002-PostgreSQL-BHT-16-1-1-2 |       766.56 |      2.05 |           2.67 |                  2.67 |
| 1777967002-PostgreSQL-BHT-16-1-2-1 |       717.21 |      1.85 |           1.99 |                  1.99 |
| 1777967002-PostgreSQL-BHT-16-1-2-2 |       717.21 |      1.80 |           1.99 |                  1.99 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1777967002-PostgreSQL-BHT-16-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       11.00 |                                    0.00 |
| 1777967002-PostgreSQL-BHT-16-1-1-2 |                     17.00 |                                     0.00 |                                             0.00 |                       11.00 |                                    0.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-2 |                     16.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS                               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1777967002-PostgreSQL-BHT-16-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |
| 1777967002-PostgreSQL-BHT-16-1-1-2 |                     11.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-1 |                     10.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |
| 1777967002-PostgreSQL-BHT-16-1-2-2 |                      5.00 |                                     0.00 |                                             0.00 |                       16.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
