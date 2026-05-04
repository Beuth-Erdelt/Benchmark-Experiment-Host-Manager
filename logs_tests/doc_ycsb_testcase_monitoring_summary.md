## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 5782s 
* Code: 1775553281
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-64-8-65536-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:157412
  * datadisk:7092
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775553281
* PostgreSQL-64-8-65536-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:158867
  * datadisk:8546
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775553281
* PostgreSQL-64-8-65536-3 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:159849
  * datadisk:9527
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775553281
* PostgreSQL-64-8-65536-4 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:160723
  * datadisk:10402
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1775553281

### Loading

| DBMS                  |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-65536 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                         3328.67 |               901390.00 |           3000000.00 |                             75407.00 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-65536-1 |             1.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                         2769.53 |              1083217.00 |         1500413.00 |                             815.00 |           1499587.00 |                            911359.00 |
| PostgreSQL-64-8-65536-2 |             1.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                         2818.71 |              1071538.00 |         1499635.00 |                             750.00 |           1500365.00 |                            920063.00 |
| PostgreSQL-64-8-65536-3 |             1.00 |     64.00 | 49152.00 |        1.00 |         0.00 |                         2801.92 |              1070694.00 |         1500977.00 |                             753.00 |           1499023.00 |                            901119.00 |
| PostgreSQL-64-8-65536-4 |             1.00 |     64.00 | 49152.00 |        8.00 |         0.00 |                         2813.43 |              1076227.00 |         1499333.00 |                             745.00 |           1500667.00 |                            920575.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-64-8-65536 - Pods [[8, 8, 1, 1]]

#### Planned

* DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-64-8-65536-1 |      1086.22 |      1.15 |           9.82 |                 12.75 |
| PostgreSQL-64-8-65536-2 |      1086.22 |      1.15 |           9.82 |                 12.75 |
| PostgreSQL-64-8-65536-3 |      1086.22 |      1.15 |           9.82 |                 12.75 |
| PostgreSQL-64-8-65536-4 |      1086.22 |      1.15 |           9.82 |                 12.75 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-64-8-65536-1 |       423.45 |      0.50 |           0.11 |                  0.11 |
| PostgreSQL-64-8-65536-2 |       423.45 |      0.50 |           0.11 |                  0.11 |
| PostgreSQL-64-8-65536-3 |       423.45 |      0.50 |           0.11 |                  0.11 |
| PostgreSQL-64-8-65536-4 |       423.45 |      0.50 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-64-8-65536-1 |       964.71 |      1.11 |          10.92 |                 15.12 |
| PostgreSQL-64-8-65536-2 |       900.78 |      0.95 |          11.37 |                 15.99 |
| PostgreSQL-64-8-65536-3 |       908.55 |      0.91 |          11.74 |                 16.00 |
| PostgreSQL-64-8-65536-4 |       920.38 |      0.89 |          12.11 |                 16.00 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-64-8-65536-1 |       259.97 |      0.34 |           0.13 |                  0.13 |
| PostgreSQL-64-8-65536-2 |       259.97 |      0.29 |           0.13 |                  0.13 |
| PostgreSQL-64-8-65536-3 |       260.50 |      0.60 |           0.13 |                  0.13 |
| PostgreSQL-64-8-65536-4 |       262.33 |      0.69 |           0.13 |                  0.13 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
