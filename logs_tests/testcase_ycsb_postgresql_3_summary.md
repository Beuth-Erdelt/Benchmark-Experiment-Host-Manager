## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 24081s 
* Code: 1782632881
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
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:178701
  * volume_size:10G
  * volume_used:3.0G
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:161399
  * volume_size:10G
  * volume_used:3.0G
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:167246
  * volume_size:10G
  * volume_used:4.3G
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:167758
  * volume_size:10G
  * volume_used:4.7G
  * cpu_list:0-95
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1393138
  * volume_size:10G
  * volume_used:5.0G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1396241
  * volume_size:10G
  * volume_used:5.0G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1413952
  * volume_size:10G
  * volume_used:5.0G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1383878
  * volume_size:10G
  * volume_used:5.0G
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782632881

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782632881-5df5b978db-k8skm: 0 0

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
| PostgreSQL-1-1-1-1-1  | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                          409.08 |              2444507.00 |             500518 |                             694.00 |               499482 |                           5558271.00 |
| PostgreSQL-1-1-2-1-2  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                          204.22 |              2448343.00 |             249625 |                            1272.00 |               250375 |                          14630911.00 |
| PostgreSQL-1-1-2-1-1  | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                          203.04 |              2462554.00 |             250589 |                            1267.00 |               249411 |                          14581759.00 |
| PostgreSQL-1-1-3-1-1  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                           47.51 |              2631037.00 |              62690 |                             686.00 |                62310 |                           5517311.00 |
| PostgreSQL-1-1-3-1-6  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                           47.61 |              2625729.00 |              62662 |                             631.00 |                62338 |                           5804031.00 |
| PostgreSQL-1-1-3-1-8  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                           47.35 |              2640020.00 |              63043 |                             639.00 |                61957 |                           5799935.00 |
| PostgreSQL-1-1-3-1-3  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                           47.59 |              2626391.00 |              62717 |                             657.00 |                62283 |                           5648383.00 |
| PostgreSQL-1-1-3-1-7  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                           47.27 |              2644274.00 |              62604 |                             616.00 |                62396 |                           5480447.00 |
| PostgreSQL-1-1-3-1-2  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                           47.26 |              2645004.00 |              62616 |                             679.00 |                62384 |                           5304319.00 |
| PostgreSQL-1-1-3-1-4  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                           47.58 |              2627348.00 |              62389 |                             691.00 |                62611 |                           5459967.00 |
| PostgreSQL-1-1-3-1-5  | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                           47.58 |              2627366.00 |              62489 |                             659.00 |                62511 |                           5582847.00 |
| PostgreSQL-1-1-4-1-9  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                           26.83 |              2329350.00 |              31430 |                            1251.00 |                31070 |                          14270463.00 |
| PostgreSQL-1-1-4-1-1  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                           25.74 |              2428147.00 |              31171 |                            1215.00 |                31329 |                          13180927.00 |
| PostgreSQL-1-1-4-1-2  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                           25.74 |              2428251.00 |              31245 |                            1262.00 |                31255 |                          14041087.00 |
| PostgreSQL-1-1-4-1-12 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                           25.75 |              2427551.00 |              31277 |                            1242.00 |                31223 |                          12746751.00 |
| PostgreSQL-1-1-4-1-13 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                           25.75 |              2427478.00 |              31434 |                            1263.00 |                31066 |                          14163967.00 |
| PostgreSQL-1-1-4-1-11 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                           26.45 |              2362761.00 |              31153 |                            1240.00 |                31347 |                          13877247.00 |
| PostgreSQL-1-1-4-1-5  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                           26.35 |              2372150.00 |              31182 |                            1252.00 |                31318 |                          13221887.00 |
| PostgreSQL-1-1-4-1-4  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                           24.95 |              2505089.00 |              30954 |                            1223.00 |                31546 |                          13484031.00 |
| PostgreSQL-1-1-4-1-3  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                           25.91 |              2412041.00 |              31168 |                            1208.00 |                31332 |                          13721599.00 |
| PostgreSQL-1-1-4-1-10 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                           26.21 |              2385031.00 |              31157 |                            1235.00 |                31343 |                          13148159.00 |
| PostgreSQL-1-1-4-1-6  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                           25.46 |              2454429.00 |              31178 |                            1215.00 |                31322 |                          13811711.00 |
| PostgreSQL-1-1-4-1-14 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                           25.67 |              2435068.00 |              31253 |                            1239.00 |                31247 |                          15745023.00 |
| PostgreSQL-1-1-4-1-16 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                           25.75 |              2427155.00 |              31391 |                            1232.00 |                31109 |                          14540799.00 |
| PostgreSQL-1-1-4-1-15 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                           25.28 |              2472055.00 |              31007 |                            1229.00 |                31493 |                          14401535.00 |
| PostgreSQL-1-1-4-1-8  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                           25.44 |              2457206.00 |              31160 |                            1244.00 |                31340 |                          14352383.00 |
| PostgreSQL-1-1-4-1-7  | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                           26.94 |              2320320.00 |              31419 |                            1229.00 |                31081 |                          14131199.00 |
| PostgreSQL-1-2-4-1-12 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                           31.23 |              2001503.00 |              31090 |                             922.00 |                31410 |                          12017663.00 |
| PostgreSQL-1-2-4-1-2  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                           30.96 |              2019013.00 |              31098 |                             946.00 |                31402 |                          11911167.00 |
| PostgreSQL-1-2-4-1-16 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                           30.73 |              2033755.00 |              31395 |                             915.00 |                31105 |                          12967935.00 |
| PostgreSQL-1-2-4-1-6  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                           30.76 |              2031871.00 |              31317 |                             952.00 |                31183 |                          13271039.00 |
| PostgreSQL-1-2-4-1-15 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                           31.54 |              1981363.00 |              31070 |                             959.00 |                31430 |                          12337151.00 |
| PostgreSQL-1-2-4-1-8  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                           30.73 |              2033902.00 |              31079 |                             966.00 |                31421 |                          13336575.00 |
| PostgreSQL-1-2-4-1-14 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                           31.09 |              2009972.00 |              31089 |                             925.00 |                31411 |                          11952127.00 |
| PostgreSQL-1-2-4-1-5  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                           31.13 |              2007880.00 |              31192 |                             909.00 |                31308 |                          12754943.00 |
| PostgreSQL-1-2-4-1-1  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                           31.45 |              1987359.00 |              31317 |                             959.00 |                31183 |                          11460607.00 |
| PostgreSQL-1-2-4-1-11 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                           31.13 |              2007546.00 |              31233 |                             992.00 |                31267 |                          12976127.00 |
| PostgreSQL-1-2-4-1-13 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                           30.72 |              2034498.00 |              31362 |                             961.00 |                31138 |                          12525567.00 |
| PostgreSQL-1-2-4-1-10 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                           31.19 |              2003693.00 |              31226 |                             926.00 |                31274 |                          11616255.00 |
| PostgreSQL-1-2-4-1-9  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                           31.35 |              1993781.00 |              31256 |                             961.00 |                31244 |                          12296191.00 |
| PostgreSQL-1-2-4-1-3  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                           31.14 |              2007356.00 |              31252 |                             947.00 |                31248 |                          12287999.00 |
| PostgreSQL-1-2-1-1-1  | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                          293.80 |              3403654.00 |             500362 |                             550.00 |               499638 |                           6004735.00 |
| PostgreSQL-1-2-2-1-1  | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                          194.12 |              2575755.00 |             249767 |                             973.00 |               250233 |                          13049855.00 |
| PostgreSQL-1-2-2-1-2  | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                          192.69 |              2594816.00 |             250075 |                             976.00 |               249925 |                          13762559.00 |
| PostgreSQL-1-2-3-1-8  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                           47.44 |              2634641.00 |              62675 |                             536.00 |                62325 |                           5615615.00 |
| PostgreSQL-1-2-3-1-5  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                           47.23 |              2646444.00 |              62631 |                             555.00 |                62369 |                           5484543.00 |
| PostgreSQL-1-2-3-1-2  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                           50.45 |              2477686.00 |              62650 |                             571.00 |                62350 |                           5505023.00 |
| PostgreSQL-1-2-3-1-3  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                           49.98 |              2501034.00 |              62716 |                             536.00 |                62284 |                           5603327.00 |
| PostgreSQL-1-2-3-1-7  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                           48.39 |              2583337.00 |              62631 |                             526.00 |                62369 |                           5476351.00 |
| PostgreSQL-1-2-3-1-6  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                           51.43 |              2430276.00 |              62580 |                             546.00 |                62420 |                           5427199.00 |
| PostgreSQL-1-2-3-1-1  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                           47.90 |              2609558.00 |              62552 |                             540.00 |                62448 |                           5595135.00 |
| PostgreSQL-1-2-3-1-4  | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                           49.77 |              2511498.00 |              62489 |                             548.00 |                62511 |                           5779455.00 |
| PostgreSQL-1-2-4-1-7  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                           31.51 |              1983676.00 |              31276 |                             960.00 |                31224 |                          12287999.00 |
| PostgreSQL-1-2-4-1-4  | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                           31.45 |              1987123.00 |              31319 |                             923.00 |                31181 |                          11968511.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                          409.08 |              2444507.00 |             500518 |                             694.00 |               499482 |                           5558271.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       128 |     2048 |               1 |           2 |            0 |                          407.26 |              2462554.00 |             500214 |                            1272.00 |               499786 |                          14630911.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |     1024 |               1 |           8 |            0 |                          379.74 |              2645004.00 |             501210 |                             691.00 |               498790 |                           5804031.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |       128 |     2048 |               1 |          16 |            0 |                          414.20 |              2505089.00 |             499579 |                            1263.00 |               500421 |                          15745023.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                          293.80 |              3403654.00 |             500362 |                             550.00 |               499638 |                           6004735.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       128 |     2048 |               1 |           2 |            0 |                          386.81 |              2594816.00 |             499842 |                             976.00 |               500158 |                          13762559.00 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |        64 |     1024 |               1 |           8 |            0 |                          392.60 |              2646444.00 |             500924 |                             571.00 |               499076 |                           5779455.00 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |       128 |     2048 |               1 |          16 |            0 |                          498.11 |              2034498.00 |             499571 |                             992.00 |               500429 |                          13336575.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
