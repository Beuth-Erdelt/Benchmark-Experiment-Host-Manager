## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 642s 
* Code: 1792690450
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
  * Experiment uses bexhoma version 0.11.8.
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
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:953456
  * datadisk:2392
  * volume_size:1.8T
  * volume_used:932G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792690450
* postgresql-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:953456
  * datadisk:2392
  * volume_size:1.8T
  * volume_used:932G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792690450
* postgresql-3-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:952772
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:931G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792690450
* postgresql-4-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:952772
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:931G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792690450

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792690450-595f9455cf-6s88g: 0
* bexhoma-sut-postgresql-2-1792690450-58f775446d-dpgjv: 0
* bexhoma-sut-postgresql-3-1792690450-7696d7f6b5-g74nx: 0
* bexhoma-sut-postgresql-4-1792690450-59d5c968cd-plwwp: 0

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
| postgresql-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 |                        16289.30 |                61390.00 |           1000000.00 |                               783.00 | 1.00 |               58.64 |
| postgresql-2-1-0-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 |                        64069.71 |                15608.00 |           1000000.00 |                               581.00 | 1.00 |              230.65 |
| postgresql-3-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.92 |                61307.00 |            125000.00 |                               844.00 | 1.00 |               58.72 |
| postgresql-3-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.95 |                61306.00 |            125000.00 |                               864.00 | 1.00 |               58.72 |
| postgresql-3-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.35 |                61294.00 |            125000.00 |                               781.00 | 1.00 |               58.73 |
| postgresql-3-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.79 |                61311.00 |            125000.00 |                               858.00 | 1.00 |               58.72 |
| postgresql-3-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.82 |                61310.00 |            125000.00 |                               763.00 | 1.00 |               58.72 |
| postgresql-3-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.75 |                61282.00 |            125000.00 |                               877.00 | 1.00 |               58.74 |
| postgresql-3-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.52 |                61289.00 |            125000.00 |                               821.00 | 1.00 |               58.74 |
| postgresql-3-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2038.79 |                61311.00 |            125000.00 |                               849.00 | 1.00 |               58.72 |
| postgresql-4-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8047.90 |                15532.00 |            125000.00 |                               580.00 | 1.00 |              231.78 |
| postgresql-4-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8041.69 |                15544.00 |            125000.00 |                               583.00 | 1.00 |              231.60 |
| postgresql-4-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8034.97 |                15557.00 |            125000.00 |                               576.00 | 1.00 |              231.41 |
| postgresql-4-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8034.97 |                15557.00 |            125000.00 |                               536.00 | 1.00 |              231.41 |
| postgresql-4-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8036.00 |                15555.00 |            125000.00 |                               667.00 | 1.00 |              231.44 |
| postgresql-4-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8054.64 |                15519.00 |            125000.00 |                               575.00 | 1.00 |              231.97 |
| postgresql-4-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8036.52 |                15554.00 |            125000.00 |                               599.00 | 1.00 |              231.45 |
| postgresql-4-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8024.65 |                15577.00 |            125000.00 |                               606.00 | 1.00 |              231.11 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 | 1.00 |               58.64 |                        16289.30 |                61390.00 |           1000000.00 |                               783.00 |
| PostgreSQL-2-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 | 1.00 |              230.65 |                        64069.71 |                15608.00 |           1000000.00 |                               581.00 |
| PostgreSQL-3-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.72 |                        16312.88 |                61311.00 |           1000000.00 |                               832.12 |
| PostgreSQL-4-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              231.11 |                        64311.34 |                15577.00 |           1000000.00 |                               590.25 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32178.14 |                31077.00 |             500785 |                             500.00 |               499215 |                              8231.00 |
| postgresql-2-1-1-1-1 | postgresql-2-1-1 | postgresql-2-1-1-1 | PostgreSQL-2    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32308.09 |                30952.00 |             500201 |                             504.00 |               499799 |                              6671.00 |
| postgresql-3-1-1-1-1 | postgresql-3-1-1 | postgresql-3-1-1-1 | PostgreSQL-3    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32189.53 |                31066.00 |             500441 |                             505.00 |               499559 |                              2649.00 |
| postgresql-4-1-1-1-1 | postgresql-4-1-1 | postgresql-4-1-1-1 | PostgreSQL-4    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32216.49 |                31040.00 |             500085 |                             511.00 |               499915 |                              2767.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32178.14 |                31077.00 |             500785 |                             500.00 |               499215 |                              8231.00 |
| postgresql-2-1-1 | postgresql-2-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32308.09 |                30952.00 |             500201 |                             504.00 |               499799 |                              6671.00 |
| postgresql-3-1-1 | postgresql-3-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32189.53 |                31066.00 |             500441 |                             505.00 |               499559 |                              2649.00 |
| postgresql-4-1-1 | postgresql-4-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32216.49 |                31040.00 |             500085 |                             511.00 |               499915 |                              2767.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
