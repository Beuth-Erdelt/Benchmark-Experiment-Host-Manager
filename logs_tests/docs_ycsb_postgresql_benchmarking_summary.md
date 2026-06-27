## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1094s 
* Code: 1782505177
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Experiment uses bexhoma version 0.10.1.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 5Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:235962
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782505177
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:242249
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782505177
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:245022
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782505177
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:245902
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782505177

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782505177-5f7b89d596-bqd2x: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8046.35 |                15535.00 |            125000.00 |                              4847.00 | 1.00 |              231.73 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8072.85 |                15484.00 |            125000.00 |                              4747.00 | 1.00 |              232.50 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8048.42 |                15531.00 |            125000.00 |                              4459.00 | 1.00 |              231.79 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8052.57 |                15523.00 |            125000.00 |                              4967.00 | 1.00 |              231.91 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8061.40 |                15506.00 |            125000.00 |                              4639.00 | 1.00 |              232.17 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8052.05 |                15524.00 |            125000.00 |                              4823.00 | 1.00 |              231.90 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8064.52 |                15500.00 |            125000.00 |                              4927.00 | 1.00 |              232.26 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8072.33 |                15485.00 |            125000.00 |                              4575.00 | 1.00 |              232.48 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              231.73 |                        64470.47 |                15535.00 |           1000000.00 |                              4748.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32463.32 |                30804.00 |             500203 |                             814.00 |               499797 |                              3105.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4066.10 |                30742.00 |              62302 |                             774.00 |                62698 |                              1275.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4065.04 |                30750.00 |              62473 |                             735.00 |                62527 |                              1297.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4066.23 |                30741.00 |              62506 |                             699.00 |                62494 |                              1253.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4064.38 |                30755.00 |              62491 |                             698.00 |                62509 |                              1187.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4064.38 |                30755.00 |              62603 |                             682.00 |                62397 |                              1238.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4065.57 |                30746.00 |              62650 |                             693.00 |                62350 |                              1188.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4060.16 |                30787.00 |              62717 |                             878.00 |                62283 |                              1421.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4066.63 |                30738.00 |              62308 |                             778.00 |                62692 |                              1337.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48447.27 |                20641.00 |             499232 |                             712.00 |               500768 |                              1033.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6070.32 |                20592.00 |              62516 |                             479.00 |                62484 |                               789.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6078.88 |                20563.00 |              62352 |                             710.00 |                62648 |                               955.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6068.84 |                20597.00 |              62493 |                             580.00 |                62507 |                               893.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6072.38 |                20585.00 |              62806 |                             730.00 |                62194 |                              1014.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6074.74 |                20577.00 |              62554 |                             519.00 |                62446 |                               835.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6074.74 |                20577.00 |              62356 |                             733.00 |                62644 |                              1011.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6073.56 |                20581.00 |              62481 |                             741.00 |                62519 |                              1005.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6070.02 |                20593.00 |              62637 |                             472.00 |                62363 |                               804.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32463.32 |                30804.00 |             500203 |                             814.00 |               499797 |                              3105.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32518.48 |                30787.00 |             500050 |                             878.00 |               499950 |                              1421.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48447.27 |                20641.00 |             499232 |                             712.00 |               500768 |                              1033.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48583.50 |                20597.00 |             500195 |                             741.00 |               499805 |                              1014.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
