## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 13618s 
* Code: 1785541275
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
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.10.9.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765912
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765877
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765779
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765793
  * volume_size:50G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765796
  * volume_size:50G
  * volume_used:5.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765801
  * volume_size:50G
  * volume_used:5.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-2-3-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765813
  * volume_size:50G
  * volume_used:5.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275
* postgresql-1-2-4-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765818
  * volume_size:50G
  * volume_used:5.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541275

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785541275-6d4c688c5-5zf9h: 0 0
* bexhoma-sut-postgresql-1-1785541275-69b9cdcd5-f82ph: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: ycsb (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: ycsb (8 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: ycsb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          123.15 |              1014993.00 |            125000.00 |                            527871.00 | 1.00 |                3.55 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          123.71 |              1010420.00 |            125000.00 |                            528383.00 | 1.00 |                3.56 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          124.09 |              1007326.00 |            125000.00 |                            526847.00 | 1.00 |                3.57 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          123.58 |              1011471.00 |            125000.00 |                            527359.00 | 1.00 |                3.56 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          123.94 |              1008556.00 |            125000.00 |                            526847.00 | 1.00 |                3.57 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          123.21 |              1014524.00 |            125000.00 |                            527359.00 | 1.00 |                3.55 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          123.68 |              1010666.00 |            125000.00 |                            527359.00 | 1.00 |                3.56 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          124.07 |              1007469.00 |            125000.00 |                            527871.00 | 1.00 |                3.57 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |                3.55 |                          989.44 |              1014993.00 |           1000000.00 |                            527487.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|-----------------------------:|--------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                          810.44 |              1233903.00 |             500746 |                             857.00 |               499254 |                           2011135.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                          122.80 |              1017874.00 |              62559 |                             752.00 |                62441 |                           1580031.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                          124.56 |              1003541.00 |              62568 |                             757.00 |                62432 |                           1355775.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                          129.30 |               966720.00 |              62466 |                             740.00 |                62534 |                           1175551.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                          124.20 |              1006458.00 |              62333 |                             759.00 |                62667 |                           1461247.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                          123.08 |              1015595.00 |              62707 |                             763.00 |                62293 |                           1524735.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                          122.15 |              1023373.00 |              62622 |                             757.00 |                62378 |                           1641471.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                          122.31 |              1021980.00 |              62790 |                             766.00 |                62210 |                           1615871.00 |                            0 |                                        0.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                          121.52 |              1028641.00 |              62192 |                             797.00 |                62808 |                           1530879.00 |                            0 |                                        0.00 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                          515.32 |              1940553.00 |             499230 |                             824.00 |               500733 |                           3971071.00 |                           37 |                                 45613055.00 |
| postgresql-1-1-4-1-1 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                           78.34 |              1595659.00 |              62552 |                             821.00 |                62448 |                           3297279.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-2 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                           78.36 |              1595227.00 |              62813 |                             824.00 |                62187 |                           3225599.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-3 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                           78.29 |              1596581.00 |              62616 |                             821.00 |                62384 |                           3160063.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-4 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                           78.32 |              1595939.00 |              62814 |                             831.00 |                62186 |                           3414015.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-5 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                           78.30 |              1596425.00 |              62603 |                             818.00 |                62397 |                           3289087.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-6 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                           78.26 |              1597321.00 |              62393 |                             823.00 |                62607 |                           3207167.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-7 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                           78.32 |              1596008.00 |              62559 |                             812.00 |                62441 |                           3223551.00 |                            0 |                                        0.00 |
| postgresql-1-1-4-1-8 | postgresql-1-1-4 | postgresql-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                           78.26 |              1597306.00 |              62858 |                             820.00 |                62142 |                           3168255.00 |                            0 |                                        0.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                          673.35 |              1485105.00 |             500470 |                             852.00 |               499530 |                           2994175.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                           90.58 |              1379983.00 |              62440 |                             813.00 |                62560 |                           1929215.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                           92.34 |              1353765.00 |              62270 |                             797.00 |                62730 |                           2248703.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                           96.34 |              1297539.00 |              62659 |                             791.00 |                62341 |                           2148351.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                           92.41 |              1352701.00 |              62444 |                             801.00 |                62556 |                           2049023.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                           95.90 |              1303421.00 |              62663 |                             805.00 |                62337 |                           2285567.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                           89.87 |              1390911.00 |              62507 |                             802.00 |                62493 |                           2181119.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                           92.31 |              1354196.00 |              62400 |                             800.00 |                62600 |                           2279423.00 |                            0 |                                        0.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                           92.06 |              1357851.00 |              62428 |                             794.00 |                62572 |                           2224127.00 |                            0 |                                        0.00 |
| postgresql-1-2-3-1-1 | postgresql-1-2-3 | postgresql-1-2-3-1 | PostgreSQL-1    |                2 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                          664.17 |              1505637.00 |             500514 |                             820.00 |               499486 |                           2893823.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-1 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                          126.57 |               987560.00 |              62413 |                             814.00 |                62587 |                           1949695.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-2 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                          127.47 |               980592.00 |              62318 |                             813.00 |                62682 |                           1899519.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-3 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                          128.01 |               976472.00 |              62671 |                             799.00 |                62329 |                           1784831.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-4 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                          127.92 |               977199.00 |              62430 |                             809.00 |                62570 |                           1825791.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-5 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                          126.82 |               985627.00 |              62584 |                             811.00 |                62416 |                           1819647.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-6 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                          127.41 |               981109.00 |              62356 |                             816.00 |                62644 |                           1767423.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-7 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                          127.48 |               980528.00 |              62458 |                             814.00 |                62542 |                           1830911.00 |                            0 |                                        0.00 |
| postgresql-1-2-4-1-8 | postgresql-1-2-4 | postgresql-1-2-4-1 | PostgreSQL-1    |                2 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                          127.13 |               983207.00 |              62520 |                             815.00 |                62480 |                           1901567.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|-----------------------------:|--------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                          810.44 |              1233903.00 |             500746 |                             857.00 |               499254 |                           2011135.00 |                            0 |                                        0.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                          989.92 |              1028641.00 |             500237 |                             797.00 |               499763 |                           1641471.00 |                            0 |                                        0.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                          515.32 |              1940553.00 |             499230 |                             824.00 |               500733 |                           3971071.00 |                           37 |                                 45613055.00 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                          626.45 |              1597321.00 |             501208 |                             831.00 |               498792 |                           3414015.00 |                            0 |                                        0.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        64 |    32768 |               1 |           1 |            0 |                          673.35 |              1485105.00 |             500470 |                             852.00 |               499530 |                           2994175.00 |                            0 |                                        0.00 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        64 |    32768 |               1 |           8 |            0 |                          741.79 |              1390911.00 |             499811 |                             813.00 |               500189 |                           2285567.00 |                            0 |                                        0.00 |
| postgresql-1-2-3 | postgresql-1-2-3 |                2 |        64 |    49152 |               1 |           1 |            0 |                          664.17 |              1505637.00 |             500514 |                             820.00 |               499486 |                           2893823.00 |                            0 |                                        0.00 |
| postgresql-1-2-4 | postgresql-1-2-4 |                2 |        64 |    49152 |               1 |           8 |            0 |                         1018.82 |               987560.00 |             499750 |                             816.00 |               500250 |                           1949695.00 |                            0 |                                        0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
