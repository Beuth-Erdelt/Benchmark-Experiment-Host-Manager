## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 440s 
* Code: 1795443613
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
  * Experiment uses bexhoma version 0.12.3.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:831883
  * datadisk:2392
  * volume_size:1.8T
  * volume_used:813G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795443613
* postgresql-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:833495
  * datadisk:2392
  * volume_size:1.8T
  * volume_used:814G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795443613
* postgresql-3-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:831898
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:813G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795443613
* postgresql-4-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834209
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:815G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795443613

### Ingestion
* PostgreSQL-1: 1 of 1 units ok
* PostgreSQL-2: 1 of 1 units ok
* PostgreSQL-3: 8 of 8 units ok
* PostgreSQL-4: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795443613-5b5b74d4ff-8bh4q: 0
* bexhoma-sut-postgresql-2-1795443613-54d664b7b8-nr5hs: 0
* bexhoma-sut-postgresql-3-1795443613-86997db757-xtjt5: 0
* bexhoma-sut-postgresql-4-1795443613-7df77487cd-pbr46: 0

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
| postgresql-1-1-0-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |     0.00 |                        16280.55 |                61423.00 |           1000000.00 |                               648.00 | 1.00 |               58.61 |
| postgresql-2-1-0-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |     0.00 |                        64057.40 |                15611.00 |           1000000.00 |                               652.00 | 1.00 |              230.61 |
| postgresql-3-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2039.45 |                61291.00 |            125000.00 |                               593.00 | 1.00 |               58.74 |
| postgresql-3-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2039.25 |                61297.00 |            125000.00 |                               595.00 | 1.00 |               58.73 |
| postgresql-3-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2038.05 |                61333.00 |            125000.00 |                               658.00 | 1.00 |               58.70 |
| postgresql-3-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2038.45 |                61321.00 |            125000.00 |                               578.00 | 1.00 |               58.71 |
| postgresql-3-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2038.39 |                61323.00 |            125000.00 |                               635.00 | 1.00 |               58.71 |
| postgresql-3-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2038.15 |                61330.00 |            125000.00 |                               592.00 | 1.00 |               58.70 |
| postgresql-3-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2039.35 |                61294.00 |            125000.00 |                               653.00 | 1.00 |               58.73 |
| postgresql-3-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         2039.42 |                61292.00 |            125000.00 |                               629.00 | 1.00 |               58.74 |
| postgresql-4-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8076.50 |                15477.00 |            125000.00 |                               620.00 | 1.00 |              232.60 |
| postgresql-4-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8081.72 |                15467.00 |            125000.00 |                               636.00 | 1.00 |              232.75 |
| postgresql-4-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8079.11 |                15472.00 |            125000.00 |                               584.00 | 1.00 |              232.68 |
| postgresql-4-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8080.68 |                15469.00 |            125000.00 |                               530.00 | 1.00 |              232.72 |
| postgresql-4-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8079.11 |                15472.00 |            125000.00 |                               587.00 | 1.00 |              232.68 |
| postgresql-4-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8082.24 |                15466.00 |            125000.00 |                               555.00 | 1.00 |              232.77 |
| postgresql-4-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8075.98 |                15478.00 |            125000.00 |                               583.00 | 1.00 |              232.59 |
| postgresql-4-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8078.59 |                15473.00 |            125000.00 |                               532.00 | 1.00 |              232.66 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        1.00 |     0.00 | 1.00 |               58.61 |                        16280.55 |                61423.00 |           1000000.00 |                               648.00 |
| PostgreSQL-2-1 |             1.00 |     64.00 | 65536.00 |        1.00 |     0.00 | 1.00 |              230.61 |                        64057.40 |                15611.00 |           1000000.00 |                               652.00 |
| PostgreSQL-3-1 |             1.00 |     64.00 | 16384.00 |        8.00 |     0.00 | 1.00 |               58.70 |                        16310.52 |                61333.00 |           1000000.00 |                               616.62 |
| PostgreSQL-4-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |              232.59 |                        64633.93 |                15478.00 |           1000000.00 |                               578.38 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32314.35 |                30946.00 |             500902 |                             303.00 |               499098 |                             12983.00 |
| postgresql-2-1-1-1-1 | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32189.53 |                31066.00 |             500292 |                             572.00 |               499708 |                             13703.00 |
| postgresql-3-1-1-1-1 | postgresql-3-1-1 | postgresql-3-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32388.66 |                30875.00 |             499915 |                             300.00 |               500085 |                             10695.00 |
| postgresql-4-1-1-1-1 | postgresql-4-1-1 | postgresql-4-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32231.03 |                31026.00 |             500120 |                             460.00 |               499880 |                              5563.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32314.35 |                30946.00 |             500902 |                             303.00 |               499098 |                             12983.00 |
| postgresql-2-1-1 | postgresql-2-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32189.53 |                31066.00 |             500292 |                             572.00 |               499708 |                             13703.00 |
| postgresql-3-1-1 | postgresql-3-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32388.66 |                30875.00 |             499915 |                             300.00 |               500085 |                             10695.00 |
| postgresql-4-1-1 | postgresql-4-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32231.03 |                31026.00 |             500120 |                             460.00 |               499880 |                              5563.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
