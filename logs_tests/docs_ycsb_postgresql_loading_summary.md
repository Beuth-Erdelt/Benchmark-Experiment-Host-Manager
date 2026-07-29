## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 605s 
* Code: 1785150902
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
  * Experiment uses bexhoma version 0.10.8.
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
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826020
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822807
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902
* PostgreSQL-3-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826582
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902
* PostgreSQL-4-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825669
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785150902

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785150902-76d6f8f9d4-sddgr: 0 0
* bexhoma-sut-postgresql-2-1785150902-5b89559bd5-4g6dl: 0 0
* bexhoma-sut-postgresql-3-1785150902-7c67d77486-bsvk2: 0 0
* bexhoma-sut-postgresql-4-1785150902-865cd8d87f-vsr6t: 0 0

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
| PostgreSQL-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 |                        16308.42 |                61318.00 |           1000000.00 |                             15543.00 | 1.00 |               58.71 |
| PostgreSQL-2-1-0-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 |                        55367.92 |                18061.00 |           1000000.00 |                              4123.00 | 1.00 |              199.32 |
| PostgreSQL-3-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.48 |                61290.00 |            125000.00 |                             16559.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.05 |                61303.00 |            125000.00 |                             16591.00 | 1.00 |               58.72 |
| PostgreSQL-3-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.22 |                61268.00 |            125000.00 |                             16463.00 | 1.00 |               58.76 |
| PostgreSQL-3-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.45 |                61291.00 |            125000.00 |                             16543.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.15 |                61300.00 |            125000.00 |                             16479.00 | 1.00 |               58.73 |
| PostgreSQL-3-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.15 |                61270.00 |            125000.00 |                             16463.00 | 1.00 |               58.76 |
| PostgreSQL-3-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.55 |                61288.00 |            125000.00 |                             16559.00 | 1.00 |               58.74 |
| PostgreSQL-3-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.05 |                61273.00 |            125000.00 |                             16447.00 | 1.00 |               58.75 |
| PostgreSQL-4-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7190.93 |                17383.00 |            125000.00 |                              5755.00 | 1.00 |              207.10 |
| PostgreSQL-4-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7062.94 |                17698.00 |            125000.00 |                              6111.00 | 1.00 |              203.41 |
| PostgreSQL-4-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7157.58 |                17464.00 |            125000.00 |                              5183.00 | 1.00 |              206.14 |
| PostgreSQL-4-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6998.49 |                17861.00 |            125000.00 |                              5247.00 | 1.00 |              201.56 |
| PostgreSQL-4-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7244.70 |                17254.00 |            125000.00 |                              4935.00 | 1.00 |              208.65 |
| PostgreSQL-4-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7290.33 |                17146.00 |            125000.00 |                              5051.00 | 1.00 |              209.96 |
| PostgreSQL-4-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7051.79 |                17726.00 |            125000.00 |                              5011.00 | 1.00 |              203.09 |
| PostgreSQL-4-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7118.05 |                17561.00 |            125000.00 |                              6067.00 | 1.00 |              205.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |         0.00 | 1.00 |               58.71 |                        16308.42 |                61318.00 |           1000000.00 |                             15543.00 |
| PostgreSQL-2-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 | 1.00 |              199.32 |                        55367.92 |                18061.00 |           1000000.00 |                              4123.00 |
| PostgreSQL-3-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.72 |                        16317.11 |                61303.00 |           1000000.00 |                             16513.00 |
| PostgreSQL-4-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              201.56 |                        57114.81 |                17861.00 |           1000000.00 |                              5420.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32341.53 |                30920.00 |             499746 |                            1659.00 |               500254 |                              8975.00 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 | PostgreSQL-2    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32462.26 |                30805.00 |             500129 |                             645.00 |               499871 |                             11911.00 |
| PostgreSQL-3-1-1-1-1 | PostgreSQL-3-1-1 | PostgreSQL-3-1-1-1 | PostgreSQL-3    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32415.96 |                30849.00 |             500306 |                            1092.00 |               499694 |                              8439.00 |
| PostgreSQL-4-1-1-1-1 | PostgreSQL-4-1-1 | PostgreSQL-4-1-1-1 | PostgreSQL-4    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32464.37 |                30803.00 |             500405 |                             637.00 |               499595 |                             14391.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32341.53 |                30920.00 |             499746 |                            1659.00 |               500254 |                              8975.00 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32462.26 |                30805.00 |             500129 |                             645.00 |               499871 |                             11911.00 |
| PostgreSQL-3-1-1 | PostgreSQL-3-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32415.96 |                30849.00 |             500306 |                            1092.00 |               499694 |                              8439.00 |
| PostgreSQL-4-1-1 | PostgreSQL-4-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32464.37 |                30803.00 |             500405 |                             637.00 |               499595 |                             14391.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
