## Show Summary

### Workload
Benchbase Workload chbenchmark SF=100
* Type: benchbase
* Duration: 7458s 
* Code: 1792720916
* Benchbase runs the CH-Benchmark benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'chbenchmark'. Scaling factor is 100. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [100] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:975507
  * datadisk:26568
  * volume_size:1.8T
  * volume_used:953G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720916
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:988370
  * datadisk:44712
  * volume_size:1.8T
  * volume_used:966G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720916
    * TENANT_VOL:False
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:967725
  * datadisk:47622
  * volume_size:1.8T
  * volume_used:946G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720916
    * TENANT_VOL:False
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:968738
  * datadisk:48700
  * volume_size:1.8T
  * volume_used:947G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720916
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792720916-68cdccf5d5-8h4mh: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |  100 |     1246.00 |           7.00 |            0.00 |       1232.00 |            7.00 |              1 |           1 |             |                |             0 | False         |              288.92 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1  | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         100 |    16384 |        1 |               1 |       1 |           0 | 1200.00 |          338 |                        1222.23 |                     1216.62 |         0.00 |                                                     262928.00 |                                             159886.00 |
| postgresql-1-1-2-1-1  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          50 |     8192 |        2 |               1 |       1 |           0 | 1200.00 |         1629 |                         188.29 |                      185.61 |         0.00 |                                                     181528.00 |                                             440238.00 |
| postgresql-1-1-2-1-2  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          50 |     8192 |        2 |               1 |       2 |           0 | 1200.00 |         1645 |                         180.90 |                      178.27 |         0.00 |                                                     185743.00 |                                             470533.00 |
| postgresql-1-1-3-1-1  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       1 |           0 | 1200.00 |          613 |                          35.01 |                       34.01 |         0.00 |                                                      56026.00 |                                             945909.00 |
| postgresql-1-1-3-1-2  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       2 |           0 | 1200.00 |          595 |                          35.56 |                       34.56 |         0.00 |                                                      53228.00 |                                             924991.00 |
| postgresql-1-1-3-1-3  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       3 |           0 | 1200.00 |          609 |                          37.18 |                       36.15 |         0.00 |                                                      52895.00 |                                             979108.00 |
| postgresql-1-1-3-1-4  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       4 |           0 | 1200.00 |          640 |                          35.24 |                       34.18 |         0.00 |                                                      59368.00 |                                             972872.00 |
| postgresql-1-1-3-1-5  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |          20 |     3276 |        3 |               1 |       5 |           0 | 1200.00 |          639 |                          36.46 |                       35.41 |         0.00 |                                                      52550.00 |                                             900888.00 |
| postgresql-1-1-4-1-1  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       1 |           0 | 1200.00 |          309 |                           2.83 |                        2.55 |         0.00 |                                                   30019768.00 |                                            5510331.00 |
| postgresql-1-1-4-1-2  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       2 |           0 | 1200.00 |          334 |                           3.06 |                        2.76 |         0.00 |                                                   30018929.00 |                                            5849179.00 |
| postgresql-1-1-4-1-3  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       3 |           0 | 1200.00 |          323 |                           3.55 |                        3.25 |         0.00 |                                                   30016842.00 |                                            4999111.00 |
| postgresql-1-1-4-1-4  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       4 |           0 | 1200.00 |          280 |                           2.74 |                        2.48 |         0.00 |                                                   30021619.00 |                                            6195315.00 |
| postgresql-1-1-4-1-5  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       5 |           0 | 1200.00 |          282 |                           3.08 |                        2.82 |         0.00 |                                                   30018233.00 |                                            5279693.00 |
| postgresql-1-1-4-1-6  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       6 |           0 | 1200.00 |          315 |                           3.22 |                        2.93 |         0.00 |                                                   30016529.00 |                                            4886726.00 |
| postgresql-1-1-4-1-7  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       7 |           0 | 1200.00 |          325 |                           3.88 |                        3.56 |         0.00 |                                                   30015267.00 |                                            4446304.00 |
| postgresql-1-1-4-1-8  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       8 |           0 | 1200.00 |          308 |                           2.95 |                        2.66 |         0.00 |                                                   30019930.00 |                                            5578126.00 |
| postgresql-1-1-4-1-9  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |       9 |           0 | 1200.00 |          335 |                           3.26 |                        2.97 |         0.00 |                                                   30016681.00 |                                            4850482.00 |
| postgresql-1-1-4-1-10 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |          10 |     1638 |        4 |               1 |      10 |           0 | 1200.00 |          268 |                           3.77 |                        3.53 |         0.00 |                                                   30011308.00 |                                            3499069.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         100 |    16384 |               1 |           1 |           0 | 1200.00 |          338 |                        1222.23 |                     1216.62 |         0.00 |                                                     262928.00 |                                             159886.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         100 |    16384 |               1 |           2 |           0 | 1200.00 |         3274 |                         369.19 |                      363.88 |         0.00 |                                                     185743.00 |                                             455385.50 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |         100 |    16380 |               1 |           5 |           0 | 1200.00 |         3096 |                         179.45 |                      174.31 |         0.00 |                                                      59368.00 |                                             944753.60 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |         100 |    16380 |               1 |          10 |           0 | 1200.00 |         3079 |                          32.34 |                       29.53 |         0.00 |                                                   30021619.00 |                                            5109433.60 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
