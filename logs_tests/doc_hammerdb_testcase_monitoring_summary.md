## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1381s 
* Code: 1775758495
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-16-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:154262
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775758495
* PostgreSQL-BHT-16-1-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:155513
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775758495

### Execution

| DBMS                  |   experiment_run |   vusers |   client |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |     NOPM |      TPM |   duration |   errors |
|:----------------------|-----------------:|---------:|---------:|------------:|-----------:|-----------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-BHT-16-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |      33.72 |      57.90 |         0.00 | 21080.00 | 48355.00 |       5.00 |     0.00 |
| PostgreSQL-BHT-16-1-2 |             1.00 |    16.00 |     2.00 |        2.00 |      33.83 |      66.89 |         0.00 | 19186.00 | 44117.50 |       5.00 |     0.00 |

* Warehouses: 16

### Workflow

#### Actual

* DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

#### Planned

* DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Imported warehouses [1/h] |
|:----------------------|------------:|------------:|-------:|----------------------------:|
| PostgreSQL-BHT-16-1-1 |       94.00 |        1.00 |   1.00 |                      612.77 |
| PostgreSQL-BHT-16-1-2 |       94.00 |        1.00 |   2.00 |                      612.77 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |       119.61 |      1.39 |           7.13 |                  7.81 |
| PostgreSQL-BHT-16-1-2 |       119.61 |      1.39 |           7.13 |                  7.81 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |       226.55 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-BHT-16-1-2 |       226.55 |      0.00 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |       410.91 |      0.99 |           7.79 |                  8.68 |
| PostgreSQL-BHT-16-1-2 |       359.47 |      0.88 |           8.10 |                  9.23 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |        54.73 |      0.14 |           0.17 |                  0.17 |
| PostgreSQL-BHT-16-1-2 |        54.73 |      0.28 |           0.17 |                  0.17 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
