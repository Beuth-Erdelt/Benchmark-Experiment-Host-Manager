## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 19818s 
* Code: 1777285093
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2].
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-64-8-65536-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:248353
  * datadisk:7091
  * volume_size:15G
  * volume_used:7.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777285093
* PostgreSQL-64-8-65536-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:248359
  * datadisk:8549
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777285093
* PostgreSQL-64-8-65536-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:248364
  * datadisk:9529
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777285093
* PostgreSQL-64-8-65536-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:248370
  * datadisk:9890
  * volume_size:15G
  * volume_used:9.4G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1777285093

### Loading

| DBMS                  |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-65536 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                          789.99 |              3800810.00 |           3000000.00 |                            666239.00 |

### Execution

| DBMS                      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-65536-1-1 |             1.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                          709.71 |              4227107.00 |         1500188.00 |                            1159.00 |           1499812.00 |                           2674687.00 |
| PostgreSQL-64-8-65536-1-2 |             1.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                          824.42 |              3641543.00 |         1500086.00 |                            1110.00 |           1499914.00 |                           2014207.00 |
| PostgreSQL-64-8-65536-2-1 |             2.00 |     64.00 | 32768.00 |        1.00 |         0.00 |                          760.46 |              3944960.00 |         1500795.00 |                            1451.00 |           1499205.00 |                           2848767.00 |
| PostgreSQL-64-8-65536-2-2 |             2.00 |     64.00 | 32768.00 |        8.00 |         0.00 |                          923.93 |              3249867.00 |         1499464.00 |                            1142.00 |           1500536.00 |                           1984511.00 |

### Workflow

#### Actual

* DBMS PostgreSQL-64-8-65536 - Pods [[8, 1], [8, 1]]

#### Planned

* DBMS PostgreSQL-64-8-65536 - Pods [[1, 8], [1, 8]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777285093-PostgreSQL-64-8-65536-1-1 |      1684.35 |      0.92 |           9.88 |                 13.31 |
| 1777285093-PostgreSQL-64-8-65536-1-2 |      1684.35 |      0.92 |           9.88 |                 13.31 |

### Loading phase: component loader

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777285093-PostgreSQL-64-8-65536-1-1 |       485.78 |      0.79 |           0.11 |                  0.11 |
| 1777285093-PostgreSQL-64-8-65536-1-2 |       485.78 |      0.79 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777285093-PostgreSQL-64-8-65536-1-1 |      1537.90 |      1.28 |          10.81 |                 15.03 |
| 1777285093-PostgreSQL-64-8-65536-1-2 |      1388.91 |      1.96 |          11.25 |                 15.90 |
| 1777285093-PostgreSQL-64-8-65536-2-1 |      4631.69 |      1.39 |          11.09 |                 16.00 |
| 1777285093-PostgreSQL-64-8-65536-2-2 |      1458.16 |      1.44 |          11.73 |                 16.00 |

### Execution phase: component benchmarker

| DBMS                                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777285093-PostgreSQL-64-8-65536-1-1 |       272.28 |      0.24 |           0.13 |                  0.13 |
| 1777285093-PostgreSQL-64-8-65536-1-2 |       283.03 |      1.26 |           0.13 |                  0.13 |
| 1777285093-PostgreSQL-64-8-65536-2-1 |       286.10 |      0.26 |           0.13 |                  0.13 |
| 1777285093-PostgreSQL-64-8-65536-2-2 |       285.90 |      0.41 |           0.12 |                  0.12 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1777285093-PostgreSQL-64-8-65536-1-1 |                         5 |                                        0 |                                                0 |                          64 |                                      64 |
| 1777285093-PostgreSQL-64-8-65536-1-2 |                         5 |                                        0 |                                                0 |                          64 |                                      64 |

#### Execution phase: SUT deployment

| DBMS                                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1777285093-PostgreSQL-64-8-65536-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       63.00 |                                   63.00 |
| 1777285093-PostgreSQL-64-8-65536-1-2 |                     15.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| 1777285093-PostgreSQL-64-8-65536-2-1 |                      7.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| 1777285093-PostgreSQL-64-8-65536-2-2 |                     18.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
