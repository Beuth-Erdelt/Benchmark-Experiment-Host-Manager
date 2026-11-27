## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 414s 
* Code: 1795626465
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
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 and 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1239252
  * datadisk:2392
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795626465
* postgresql-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1237570
  * datadisk:2396
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795626465
* postgresql-3-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1238849
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795626465
* postgresql-4-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1237172
  * datadisk:2390
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795626465

### Ingestion
* PostgreSQL-1: 1 of 1 units ok
* PostgreSQL-2: 1 of 1 units ok
* PostgreSQL-3: 8 of 8 units ok
* PostgreSQL-4: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795626465-754b9cbdb9-bn7v9: 0
* bexhoma-sut-postgresql-2-1795626465-669df49994-h5fhl: 0
* bexhoma-sut-postgresql-3-1795626465-5c7c4895c5-7jjfd: 0
* bexhoma-sut-postgresql-4-1795626465-9b6f99cb4-bd5bd: 0

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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |     0.00 |                        16234.03 |                61599.00 |           1000000.00 |                               841.00 | 1.00 |               58.44 |
| postgresql-2-1-0-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |     0.00 |                        63199.14 |                15823.00 |           1000000.00 |                              1136.00 | 1.00 |              227.52 |
| postgresql-3-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2040.62 |                61256.00 |            125000.00 |                               691.00 | 1.00 |               58.77 |
| postgresql-3-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2040.48 |                61260.00 |            125000.00 |                               685.00 | 1.00 |               58.77 |
| postgresql-3-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2041.55 |                61228.00 |            125000.00 |                               687.00 | 1.00 |               58.80 |
| postgresql-3-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2041.58 |                61227.00 |            125000.00 |                               699.00 | 1.00 |               58.80 |
| postgresql-3-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2040.75 |                61252.00 |            125000.00 |                               683.00 | 1.00 |               58.77 |
| postgresql-3-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2040.52 |                61259.00 |            125000.00 |                               736.00 | 1.00 |               58.77 |
| postgresql-3-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2040.22 |                61268.00 |            125000.00 |                               673.00 | 1.00 |               58.76 |
| postgresql-3-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2040.85 |                61249.00 |            125000.00 |                               667.00 | 1.00 |               58.78 |
| postgresql-4-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8079.63 |                15471.00 |            125000.00 |                              1066.00 | 1.00 |              232.69 |
| postgresql-4-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8021.56 |                15583.00 |            125000.00 |                              1001.00 | 1.00 |              231.02 |
| postgresql-4-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8077.02 |                15476.00 |            125000.00 |                              1050.00 | 1.00 |              232.62 |
| postgresql-4-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8083.29 |                15464.00 |            125000.00 |                              1057.00 | 1.00 |              232.80 |
| postgresql-4-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8074.94 |                15480.00 |            125000.00 |                              1053.00 | 1.00 |              232.56 |
| postgresql-4-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8080.16 |                15470.00 |            125000.00 |                              1073.00 | 1.00 |              232.71 |
| postgresql-4-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8083.81 |                15463.00 |            125000.00 |                              1062.00 | 1.00 |              232.81 |
| postgresql-4-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8075.46 |                15479.00 |            125000.00 |                              1079.00 | 1.00 |              232.57 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |     0.00 | 1.00 |               58.44 |                        16234.03 |                61599.00 |           1000000.00 |                               841.00 |
| PostgreSQL-2-1 |             1.00 |     64.00 | 65536.00 |        1.00 |     0.00 | 1.00 |              227.52 |                        63199.14 |                15823.00 |           1000000.00 |                              1136.00 |
| PostgreSQL-3-1 |             1.00 |     64.00 | 16384.00 |        8.00 |     0.00 | 1.00 |               58.76 |                        16326.56 |                61268.00 |           1000000.00 |                               690.12 |
| PostgreSQL-4-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |              231.02 |                        64575.87 |                15583.00 |           1000000.00 |                              1055.12 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32192.64 |                31063.00 |             499953 |                             593.00 |               500047 |                             22511.00 |
| postgresql-2-1-1-1-1 | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32157.44 |                31097.00 |             498995 |                             475.00 |               501005 |                              3713.00 |
| postgresql-3-1-1-1-1 | postgresql-3-1-1 | postgresql-3-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32357.22 |                30905.00 |             499906 |                             413.00 |               500094 |                             19695.00 |
| postgresql-4-1-1-1-1 | postgresql-4-1-1 | postgresql-4-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32218.57 |                31038.00 |             500245 |                             334.00 |               499755 |                              5563.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32192.64 |                31063.00 |             499953 |                             593.00 |               500047 |                             22511.00 |
| postgresql-2-1-1 | postgresql-2-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32157.44 |                31097.00 |             498995 |                             475.00 |               501005 |                              3713.00 |
| postgresql-3-1-1 | postgresql-3-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32357.22 |                30905.00 |             499906 |                             413.00 |               500094 |                             19695.00 |
| postgresql-4-1-1 | postgresql-4-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32218.57 |                31038.00 |             500245 |                             334.00 |               499755 |                              5563.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
