## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 7051s 
* Code: 1782625813
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 10Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:174612
  * volume_size:10G
  * volume_used:2.4G
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782625813
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:170849
  * volume_size:10G
  * volume_used:2.9G
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782625813

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782625813-797b6c7595-hp4rp: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.84 |              2054437.00 |            125000.00 |                            804863.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.86 |              2053808.00 |            125000.00 |                            804863.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.87 |              2053449.00 |            125000.00 |                            805887.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.84 |              2054502.00 |            125000.00 |                            803839.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.86 |              2053746.00 |            125000.00 |                            806399.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.90 |              2052683.00 |            125000.00 |                            804351.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.84 |              2054721.00 |            125000.00 |                            806911.00 | 1.00 |                1.75 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                           60.87 |              2053557.00 |            125000.00 |                            805887.00 | 1.00 |                1.75 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                1.75 |                          486.89 |              2054721.00 |           1000000.00 |                            805375.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                          517.76 |              1931414.00 |             499132 |                             675.00 |               500868 |                           3633151.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                          477.08 |              2096088.00 |             500345 |                             687.00 |               499655 |                           4354047.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                          517.76 |              1931414.00 |             499132 |                             675.00 |               500868 |                           3633151.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                          477.08 |              2096088.00 |             500345 |                             687.00 |               499655 |                           4354047.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
