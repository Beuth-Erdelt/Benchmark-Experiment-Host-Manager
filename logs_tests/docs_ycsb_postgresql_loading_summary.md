## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 612s 
* Code: 1783808184
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1, 4].
  * Factors for benchmarking are [2].
  * Experiment uses bexhoma version 0.10.4.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 and 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1082809
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808184
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1085032
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808184
* PostgreSQL-3-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1087174
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808184
* PostgreSQL-4-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1079835
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808184

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783808184-c787bb98f-m9684: 0 0
* bexhoma-sut-postgresql-2-1783808184-6ccd546ffd-gsk6j: 0 0
* bexhoma-sut-postgresql-3-1783808184-6c5cdc758c-v5vkq: 0 0
* bexhoma-sut-postgresql-4-1783808184-55846747d4-bzj9w: 0 0

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
| PostgreSQL-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 |                        16241.68 |                61570.00 |           1000000.00 |                             22975.00 | 1.00 |               58.47 |
| PostgreSQL-2-1-0-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 |                        38607.06 |                25902.00 |           1000000.00 |                             16359.00 | 1.00 |              138.99 |
| PostgreSQL-3-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.18 |                61269.00 |            125000.00 |                             16959.00 | 1.00 |               58.76 |
| PostgreSQL-3-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.88 |                61278.00 |            125000.00 |                             16463.00 | 1.00 |               58.75 |
| PostgreSQL-3-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                             16607.00 | 1.00 |               58.75 |
| PostgreSQL-3-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.38 |                61263.00 |            125000.00 |                             16607.00 | 1.00 |               58.76 |
| PostgreSQL-3-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.68 |                61284.00 |            125000.00 |                             16655.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                             16543.00 | 1.00 |               58.75 |
| PostgreSQL-3-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.28 |                61296.00 |            125000.00 |                             16671.00 | 1.00 |               58.73 |
| PostgreSQL-3-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.32 |                61265.00 |            125000.00 |                             16639.00 | 1.00 |               58.76 |
| PostgreSQL-4-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6617.96 |                18888.00 |            125000.00 |                              6659.00 | 1.00 |              190.60 |
| PostgreSQL-4-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6590.39 |                18967.00 |            125000.00 |                              6015.00 | 1.00 |              189.80 |
| PostgreSQL-4-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6623.57 |                18872.00 |            125000.00 |                              6035.00 | 1.00 |              190.76 |
| PostgreSQL-4-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6715.74 |                18613.00 |            125000.00 |                              5375.00 | 1.00 |              193.41 |
| PostgreSQL-4-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6713.57 |                18619.00 |            125000.00 |                              5379.00 | 1.00 |              193.35 |
| PostgreSQL-4-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6574.10 |                19014.00 |            125000.00 |                              5775.00 | 1.00 |              189.33 |
| PostgreSQL-4-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6499.58 |                19232.00 |            125000.00 |                              6435.00 | 1.00 |              187.19 |
| PostgreSQL-4-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6170.40 |                20258.00 |            125000.00 |                              7647.00 | 1.00 |              177.71 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 | 1.00 |               58.47 |                        16241.68 |                61570.00 |           1000000.00 |                             22975.00 |
| PostgreSQL-2-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 | 1.00 |              138.99 |                        38607.06 |                25902.00 |           1000000.00 |                             16359.00 |
| PostgreSQL-3-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.73 |                        16319.64 |                61296.00 |           1000000.00 |                             16643.00 |
| PostgreSQL-4-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              177.71 |                        52505.32 |                20258.00 |           1000000.00 |                              6165.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32398.11 |                30866.00 |             499674 |                            1268.00 |               500326 |                             14207.00 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 | PostgreSQL-2    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32396.01 |                30868.00 |             499534 |                            1505.00 |               500466 |                             14263.00 |
| PostgreSQL-3-1-1-1-1 | PostgreSQL-3-1-1 | PostgreSQL-3-1-1-1 | PostgreSQL-3    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32402.31 |                30862.00 |             499551 |                            2127.00 |               500449 |                             14535.00 |
| PostgreSQL-4-1-1-1-1 | PostgreSQL-4-1-1 | PostgreSQL-4-1-1-1 | PostgreSQL-4    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32436.99 |                30829.00 |             499778 |                            1114.00 |               500222 |                              3647.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32398.11 |                30866.00 |             499674 |                            1268.00 |               500326 |                             14207.00 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32396.01 |                30868.00 |             499534 |                            1505.00 |               500466 |                             14263.00 |
| PostgreSQL-3-1-1 | PostgreSQL-3-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32402.31 |                30862.00 |             499551 |                            2127.00 |               500449 |                             14535.00 |
| PostgreSQL-4-1-1 | PostgreSQL-4-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32436.99 |                30829.00 |             499778 |                            1114.00 |               500222 |                              3647.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
