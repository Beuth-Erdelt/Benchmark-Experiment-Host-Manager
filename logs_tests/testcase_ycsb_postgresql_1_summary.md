## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2942s 
* Code: 1782552120
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
  * Import is handled by 4 and 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 5Gi.
  * Loading is tested with [32, 64] threads, split into [4, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:145501
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782552120
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:1081649803264
  * CPU:AMD EPYC 7453 28-Core Processor
  * Cores:56
  * host:6.8.0-111-generic
  * node:cl-worker34
  * disk:330807
  * cpu_list:0-55
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782552120
* PostgreSQL-3-1-1-1 uses docker image postgres:18.3
  * RAM:1077382602752
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-1052-nvidia
  * node:cl-worker28
  * disk:384441
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782552120
* PostgreSQL-4-1-1-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1392951
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782552120

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782552120-5f7f6fc6cb-xtg2v: 0 0
* bexhoma-sut-postgresql-2-1782552120-59796c5bc-m2scp: 0 0
* bexhoma-sut-postgresql-3-1782552120-86bd88959d-5g6j5: 0 0
* bexhoma-sut-postgresql-4-1782552120-865fb556d5-7mqzd: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-4 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-4 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.94 |               976806.00 |            250000.00 |                             65215.00 | 1.00 |                3.69 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.94 |               976807.00 |            250000.00 |                             65183.00 | 1.00 |                3.69 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.94 |               976807.00 |            250000.00 |                             65247.00 | 1.00 |                3.69 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.94 |               976804.00 |            250000.00 |                             66047.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976804.00 |            125000.00 |                              1610.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976801.00 |            125000.00 |                              1675.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976814.00 |            125000.00 |                              1707.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976809.00 |            125000.00 |                              1694.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976806.00 |            125000.00 |                              1627.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976811.00 |            125000.00 |                              1668.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976813.00 |            125000.00 |                              1638.00 | 1.00 |                3.69 |
| PostgreSQL-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976810.00 |            125000.00 |                              1769.00 | 1.00 |                3.69 |
| PostgreSQL-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.92 |               976855.00 |            250000.00 |                             93375.00 | 1.00 |                3.69 |
| PostgreSQL-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.92 |               976855.00 |            250000.00 |                             93311.00 | 1.00 |                3.69 |
| PostgreSQL-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.92 |               976859.00 |            250000.00 |                             93439.00 | 1.00 |                3.69 |
| PostgreSQL-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.92 |               976859.00 |            250000.00 |                             93695.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976850.00 |            125000.00 |                            206207.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.95 |               976958.00 |            125000.00 |                            206207.00 | 1.00 |                3.68 |
| PostgreSQL-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976837.00 |            125000.00 |                            205823.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976841.00 |            125000.00 |                            206463.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976841.00 |            125000.00 |                            207359.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976851.00 |            125000.00 |                            206079.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.96 |               976860.00 |            125000.00 |                            205951.00 | 1.00 |                3.69 |
| PostgreSQL-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.97 |               976821.00 |            125000.00 |                            207231.00 | 1.00 |                3.69 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.69 |                         1023.74 |               976807.00 |           1000000.00 |                             65423.00 |
| PostgreSQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.69 |                         1023.74 |               976814.00 |           1000000.00 |                              1673.50 |
| PostgreSQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.69 |                         1023.69 |               976859.00 |           1000000.00 |                             93455.00 |
| PostgreSQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1023.69 |               976958.00 |           1000000.00 |                            206415.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.64 |               976902.00 |             499751 |                             511.00 |               500249 |                             71999.00 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 | PostgreSQL-2    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.64 |               976903.00 |             499702 |                             591.00 |               500298 |                              1421.00 |
| PostgreSQL-3-1-1-1-1 | PostgreSQL-3-1-1 | PostgreSQL-3-1-1-1 | PostgreSQL-3    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.63 |               976917.00 |             500130 |                             483.00 |               499870 |                            106047.00 |
| PostgreSQL-4-1-1-1-1 | PostgreSQL-4-1-1 | PostgreSQL-4-1-1-1 | PostgreSQL-4    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.64 |               976902.00 |             499298 |                             706.00 |               500702 |                            232831.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.64 |               976902.00 |             499751 |                             511.00 |               500249 |                             71999.00 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.64 |               976903.00 |             499702 |                             591.00 |               500298 |                              1421.00 |
| PostgreSQL-3-1-1 | PostgreSQL-3-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.63 |               976917.00 |             500130 |                             483.00 |               499870 |                            106047.00 |
| PostgreSQL-4-1-1 | PostgreSQL-4-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.64 |               976902.00 |             499298 |                             706.00 |               500702 |                            232831.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
