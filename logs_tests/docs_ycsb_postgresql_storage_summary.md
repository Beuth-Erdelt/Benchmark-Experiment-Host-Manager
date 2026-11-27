## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1074s 
* Code: 1795628325
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222623
  * datadisk:2391
  * volume_size:49G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222623
  * datadisk:2770
  * volume_size:49G
  * volume_used:2.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-1-3-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222614
  * datadisk:2949
  * volume_size:49G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-1-4-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222614
  * datadisk:3272
  * volume_size:49G
  * volume_used:3.2G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222617
  * datadisk:3568
  * volume_size:49G
  * volume_used:3.5G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222617
  * datadisk:3696
  * volume_size:49G
  * volume_used:3.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-2-3-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222617
  * datadisk:3703
  * volume_size:49G
  * volume_used:3.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325
* postgresql-1-2-4-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1222618
  * datadisk:3816
  * volume_size:49G
  * volume_used:3.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795628325

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: fillfactor=100, autovacuum_scale=0.2
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* PostgreSQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795628325-645658bf88-gtjxw: 0
* bexhoma-sut-postgresql-1-1795628325-5b56796cdb-4gw9h: 0

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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| postgresql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8047.90 |                15532.00 |            125000.00 |                               986.00 | 1.00 |              231.78 |
| postgresql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8038.07 |                15551.00 |            125000.00 |                               933.00 | 1.00 |              231.50 |
| postgresql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8042.72 |                15542.00 |            125000.00 |                              1028.00 | 1.00 |              231.63 |
| postgresql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8047.38 |                15533.00 |            125000.00 |                              1114.00 | 1.00 |              231.76 |
| postgresql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8051.01 |                15526.00 |            125000.00 |                              1032.00 | 1.00 |              231.87 |
| postgresql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8044.79 |                15538.00 |            125000.00 |                               995.00 | 1.00 |              231.69 |
| postgresql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8040.65 |                15546.00 |            125000.00 |                              1024.00 | 1.00 |              231.57 |
| postgresql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8047.90 |                15532.00 |            125000.00 |                              1058.00 | 1.00 |              231.78 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |              231.50 |                        64360.43 |                15551.00 |           1000000.00 |                              1021.25 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32407.56 |                30857.00 |             500229 |                             574.00 |               499771 |                              8375.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     4096 |        0 |                         4067.02 |                30735.00 |              62481 |                             558.00 |                62519 |                              6191.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     4096 |        0 |                         4068.61 |                30723.00 |              62701 |                             623.00 |                62299 |                              6091.00 |
| postgresql-1-1-2-1-3 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       3 |         8 |     4096 |        0 |                         4067.82 |                30729.00 |              62509 |                             591.00 |                62491 |                              6507.00 |
| postgresql-1-1-2-1-4 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       4 |         8 |     4096 |        0 |                         4065.97 |                30743.00 |              62314 |                             651.00 |                62686 |                              6431.00 |
| postgresql-1-1-2-1-5 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       5 |         8 |     4096 |        0 |                         4069.54 |                30716.00 |              62642 |                             609.00 |                62358 |                              5991.00 |
| postgresql-1-1-2-1-6 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       6 |         8 |     4096 |        0 |                         4067.69 |                30730.00 |              62199 |                             580.00 |                62801 |                              6303.00 |
| postgresql-1-1-2-1-7 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       7 |         8 |     4096 |        0 |                         4067.55 |                30731.00 |              62665 |                             589.00 |                62335 |                              6283.00 |
| postgresql-1-1-2-1-8 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       8 |         8 |     4096 |        0 |                         4065.83 |                30744.00 |              62894 |                             589.00 |                62106 |                              6327.00 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       1 |        64 |    49152 |        0 |                        40931.60 |                24431.00 |             500338 |                             536.00 |               499662 |                             54207.00 |
| postgresql-1-1-4-1-1 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |     6144 |        0 |                         5136.00 |                24338.00 |              62485 |                             492.00 |                62515 |                             54111.00 |
| postgresql-1-1-4-1-2 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |     6144 |        0 |                         5128.63 |                24373.00 |              62356 |                             493.00 |                62644 |                             56863.00 |
| postgresql-1-1-4-1-3 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |     6144 |        0 |                         5190.17 |                24084.00 |              62932 |                             493.00 |                62068 |                             55327.00 |
| postgresql-1-1-4-1-4 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |     6144 |        0 |                         5134.10 |                24347.00 |              62231 |                             498.00 |                62769 |                             53407.00 |
| postgresql-1-1-4-1-5 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |     6144 |        0 |                         5105.58 |                24483.00 |              62345 |                             494.00 |                62655 |                             52639.00 |
| postgresql-1-1-4-1-6 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |     6144 |        0 |                         5096.42 |                24527.00 |              62563 |                             491.00 |                62437 |                             54111.00 |
| postgresql-1-1-4-1-7 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |     6144 |        0 |                         5178.99 |                24136.00 |              62360 |                             493.00 |                62640 |                             54111.00 |
| postgresql-1-1-4-1-8 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |     6144 |        0 |                         5138.53 |                24326.00 |              62745 |                             495.00 |                62255 |                             55615.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |    32768 |        0 |                        28343.87 |                35281.00 |             499349 |                            1457.00 |               500651 |                             60479.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       1 |         8 |     4096 |        0 |                         4061.74 |                30775.00 |              62476 |                             644.00 |                62524 |                              4847.00 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       2 |         8 |     4096 |        0 |                         4060.81 |                30782.00 |              62501 |                             612.00 |                62499 |                              4519.00 |
| postgresql-1-2-2-1-3 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       3 |         8 |     4096 |        0 |                         4058.18 |                30802.00 |              62377 |                             638.00 |                62623 |                              4735.00 |
| postgresql-1-2-2-1-4 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       4 |         8 |     4096 |        0 |                         4058.44 |                30800.00 |              62494 |                             673.00 |                62506 |                              4651.00 |
| postgresql-1-2-2-1-5 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       5 |         8 |     4096 |        0 |                         4058.57 |                30799.00 |              62423 |                             665.00 |                62577 |                              4687.00 |
| postgresql-1-2-2-1-6 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       6 |         8 |     4096 |        0 |                         4061.74 |                30775.00 |              62298 |                             672.00 |                62702 |                              4703.00 |
| postgresql-1-2-2-1-7 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       7 |         8 |     4096 |        0 |                         4058.57 |                30799.00 |              62397 |                             647.00 |                62603 |                              4723.00 |
| postgresql-1-2-2-1-8 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       8 |         8 |     4096 |        0 |                         4056.86 |                30812.00 |              62665 |                             613.00 |                62335 |                              4647.00 |
| postgresql-1-2-3-1-1 | postgresql-1-2-3 | postgresql-1-2-3-1 |                2 |        3 |               1 |       1 |        64 |    49152 |        0 |                        40230.12 |                24857.00 |             500522 |                             676.00 |               499478 |                             44607.00 |
| postgresql-1-2-4-1-1 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |     6144 |        0 |                         4979.29 |                25104.00 |              62426 |                             624.00 |                62574 |                             48703.00 |
| postgresql-1-2-4-1-2 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |     6144 |        0 |                         5066.68 |                24671.00 |              62568 |                             630.00 |                62432 |                             46239.00 |
| postgresql-1-2-4-1-3 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |     6144 |        0 |                         5168.07 |                24187.00 |              62241 |                             644.00 |                62759 |                             46015.00 |
| postgresql-1-2-4-1-4 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |     6144 |        0 |                         5135.16 |                24342.00 |              62519 |                             655.00 |                62481 |                             46815.00 |
| postgresql-1-2-4-1-5 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |     6144 |        0 |                         5024.52 |                24878.00 |              62678 |                             657.00 |                62322 |                             42239.00 |
| postgresql-1-2-4-1-6 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |     6144 |        0 |                         5186.08 |                24103.00 |              62596 |                             627.00 |                62404 |                             46207.00 |
| postgresql-1-2-4-1-7 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |     6144 |        0 |                         5140.44 |                24317.00 |              62309 |                             654.00 |                62691 |                             46943.00 |
| postgresql-1-2-4-1-8 | postgresql-1-2-4 | postgresql-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |     6144 |        0 |                         5144.24 |                24299.00 |              62692 |                             647.00 |                62308 |                             47871.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32407.56 |                30857.00 |             500229 |                             574.00 |               499771 |                              8375.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           8 |        64 |    32768 |        0 |                        32540.04 |                30744.00 |             500405 |                             651.00 |               499595 |                              6507.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        3 |               1 |           1 |        64 |    49152 |        0 |                        40931.60 |                24431.00 |             500338 |                             536.00 |               499662 |                             54207.00 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        4 |               1 |           8 |        64 |    49152 |        0 |                        41108.43 |                24527.00 |             500017 |                             498.00 |               499983 |                             56863.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 |        64 |    32768 |        0 |                        28343.87 |                35281.00 |             499349 |                            1457.00 |               500651 |                             60479.00 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |        2 |               1 |           8 |        64 |    32768 |        0 |                        32474.92 |                30812.00 |             499631 |                             673.00 |               500369 |                              4847.00 |
| postgresql-1-2-3 | postgresql-1-2-3 |                2 |        3 |               1 |           1 |        64 |    49152 |        0 |                        40230.12 |                24857.00 |             500522 |                             676.00 |               499478 |                             44607.00 |
| postgresql-1-2-4 | postgresql-1-2-4 |                2 |        4 |               1 |           8 |        64 |    49152 |        0 |                        40844.46 |                25104.00 |             500029 |                             657.00 |               499971 |                             48703.00 |

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
