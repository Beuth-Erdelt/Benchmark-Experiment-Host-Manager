## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 11626s 
* Code: 1782592426
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
  * Database is persisted to disk of type shared and size 5Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1384584
  * volume_size:5.0G
  * volume_used:2.7G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1394798
  * volume_size:5.0G
  * volume_used:2.7G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1398303
  * volume_size:5.0G
  * volume_used:2.9G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1387863
  * volume_size:5.0G
  * volume_used:3.2G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1382797
  * volume_size:5.0G
  * volume_used:4.5G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1388447
  * volume_size:5.0G
  * volume_used:4.5G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1389593
  * volume_size:5.0G
  * volume_used:4.5G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1391685
  * volume_size:5.0G
  * volume_used:4.6G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782592426

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782592426-664dc787f6-nwh67: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: ycsb (16 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: ycsb (16 pods)

### Execution

#### Per Connection

| DBMS                  | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1022.90 |               977616.00 |             499674 |                             524.00 |               500326 |                            193919.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1010.63 |               494741.00 |             250172 |                             501.00 |               249828 |                            176639.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1009.15 |               495466.00 |             249685 |                             521.00 |               250315 |                            178047.00 |
| PostgreSQL-1-1-3-1-7  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.18 |               982882.00 |              62472 |                             502.00 |                62528 |                            194303.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          126.96 |               984590.00 |              62068 |                             486.00 |                62932 |                            182143.00 |
| PostgreSQL-1-1-3-1-8  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.25 |               982310.00 |              62601 |                             520.00 |                62399 |                            177919.00 |
| PostgreSQL-1-1-3-1-6  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.37 |               981412.00 |              62744 |                             486.00 |                62256 |                            188415.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.13 |               983274.00 |              62367 |                             533.00 |                62633 |                            179455.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.21 |               982642.00 |              62530 |                             504.00 |                62470 |                            178175.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          126.92 |               984849.00 |              62695 |                             524.00 |                62305 |                            170367.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          126.90 |               985047.00 |              62509 |                             520.00 |                62491 |                            188799.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          123.14 |               507562.00 |              31324 |                             824.00 |                31176 |                           1961983.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          123.14 |               507542.00 |              31021 |                             800.00 |                31479 |                           1659903.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          123.13 |               507594.00 |              31150 |                             838.00 |                31350 |                           1799167.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          123.30 |               506897.00 |              31383 |                             800.00 |                31117 |                           1776639.00 |
| PostgreSQL-1-1-4-1-16 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          123.07 |               507843.00 |              31203 |                             813.00 |                31297 |                           1502207.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          123.14 |               507554.00 |              30896 |                             818.00 |                31604 |                           1698815.00 |
| PostgreSQL-1-1-4-1-13 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          123.14 |               507566.00 |              31162 |                             763.00 |                31338 |                           1932287.00 |
| PostgreSQL-1-1-4-1-12 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          123.32 |               506791.00 |              31163 |                             828.00 |                31337 |                           1615871.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          123.26 |               507051.00 |              31178 |                             847.00 |                31322 |                           1522687.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          123.15 |               507519.00 |              31220 |                             791.00 |                31280 |                           1753087.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          123.23 |               507182.00 |              31188 |                             827.00 |                31312 |                           1732607.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          123.39 |               506518.00 |              31159 |                             799.00 |                31341 |                           1755135.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          123.18 |               507371.00 |              31440 |                             840.00 |                31060 |                           1927167.00 |
| PostgreSQL-1-1-4-1-11 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          123.03 |               508015.00 |              31394 |                             839.00 |                31106 |                           1776639.00 |
| PostgreSQL-1-1-4-1-15 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          123.50 |               506068.00 |              31181 |                             820.00 |                31319 |                           1793023.00 |
| PostgreSQL-1-1-4-1-14 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          123.28 |               506973.00 |              31202 |                             833.00 |                31298 |                           2015231.00 |
| PostgreSQL-1-2-4-1-9  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                           76.39 |               818206.00 |              31173 |                             617.00 |                31327 |                            874495.00 |
| PostgreSQL-1-2-4-1-8  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                           76.22 |               820025.00 |              31388 |                             640.00 |                31112 |                            938495.00 |
| PostgreSQL-1-2-4-1-5  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                           76.47 |               817325.00 |              31440 |                             615.00 |                31060 |                            880639.00 |
| PostgreSQL-1-2-4-1-4  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                           76.38 |               818280.00 |              31229 |                             584.00 |                31271 |                            829439.00 |
| PostgreSQL-1-2-4-1-15 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                           76.27 |               819410.00 |              31180 |                             603.00 |                31320 |                            761855.00 |
| PostgreSQL-1-2-4-1-2  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                           76.42 |               817873.00 |              31062 |                             620.00 |                31438 |                            892415.00 |
| PostgreSQL-1-2-4-1-10 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                           76.37 |               818379.00 |              31151 |                             645.00 |                31349 |                            891391.00 |
| PostgreSQL-1-2-4-1-14 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                           76.44 |               817646.00 |              31123 |                             616.00 |                31377 |                            831487.00 |
| PostgreSQL-1-2-4-1-7  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                           76.48 |               817237.00 |              31230 |                             606.00 |                31270 |                            784383.00 |
| PostgreSQL-1-2-4-1-1  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                           76.47 |               817298.00 |              31290 |                             609.00 |                31210 |                            783359.00 |
| PostgreSQL-1-2-4-1-6  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                           76.36 |               818519.00 |              31115 |                             605.00 |                31385 |                            806911.00 |
| PostgreSQL-1-2-4-1-13 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                           76.52 |               816772.00 |              31162 |                             642.00 |                31338 |                            762879.00 |
| PostgreSQL-1-2-4-1-11 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                           76.26 |               819511.00 |              31117 |                             612.00 |                31383 |                            793087.00 |
| PostgreSQL-1-2-4-1-16 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                           76.28 |               819350.00 |              31267 |                             635.00 |                31233 |                            762879.00 |
| PostgreSQL-1-2-1-1-1  | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.63 |               976920.00 |             500325 |                             616.00 |               499675 |                            191871.00 |
| PostgreSQL-1-2-2-1-2  | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1000.25 |               499876.00 |             250100 |                             545.00 |               249900 |                            542719.00 |
| PostgreSQL-1-2-2-1-1  | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                          999.46 |               500270.00 |             250130 |                             552.00 |               249870 |                            517119.00 |
| PostgreSQL-1-2-3-1-4  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          116.06 |              1077046.00 |              62636 |                             559.00 |                62364 |                            433407.00 |
| PostgreSQL-1-2-3-1-7  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          115.90 |              1078511.00 |              62189 |                             541.00 |                62811 |                            400895.00 |
| PostgreSQL-1-2-3-1-6  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          116.13 |              1076403.00 |              62532 |                             516.00 |                62468 |                            401407.00 |
| PostgreSQL-1-2-3-1-1  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          115.95 |              1078060.00 |              62621 |                             527.00 |                62379 |                            440575.00 |
| PostgreSQL-1-2-3-1-2  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          116.00 |              1077574.00 |              62664 |                             553.00 |                62336 |                            444927.00 |
| PostgreSQL-1-2-3-1-5  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          116.13 |              1076425.00 |              62563 |                             575.00 |                62437 |                            417023.00 |
| PostgreSQL-1-2-3-1-8  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          115.65 |              1080876.00 |              62406 |                             546.00 |                62594 |                            422143.00 |
| PostgreSQL-1-2-3-1-3  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          115.80 |              1079429.00 |              62289 |                             549.00 |                62711 |                            449791.00 |
| PostgreSQL-1-2-4-1-12 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                           76.28 |               819388.00 |              31219 |                             596.00 |                31281 |                            743935.00 |
| PostgreSQL-1-2-4-1-3  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                           76.25 |               819661.00 |              31250 |                             618.00 |                31250 |                            819199.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1022.90 |               977616.00 |             499674 |                             524.00 |               500326 |                            193919.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       128 |     2048 |               1 |           2 |            0 |                         2019.78 |               495466.00 |             499857 |                             521.00 |               500143 |                            178047.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1016.91 |               985047.00 |             499986 |                             533.00 |               500014 |                            194303.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |       128 |     2048 |               1 |          16 |            0 |                         1971.41 |               508015.00 |             499264 |                             847.00 |               500736 |                           2015231.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1023.63 |               976920.00 |             500325 |                             616.00 |               499675 |                            191871.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       128 |     2048 |               1 |           2 |            0 |                         1999.71 |               500270.00 |             500230 |                             552.00 |               499770 |                            542719.00 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |        64 |     1024 |               1 |           8 |            0 |                          927.61 |              1080876.00 |             499900 |                             575.00 |               500100 |                            449791.00 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |       128 |     2048 |               1 |          16 |            0 |                         1221.85 |               820025.00 |             499396 |                             645.00 |               500604 |                            938495.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
