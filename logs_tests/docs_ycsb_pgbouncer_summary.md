## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 280s 
* Code: 1793709901
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [11].
  * Factors for benchmarking are [11].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 16 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Pooling is fixed to cl-worker38.
  * Database uses ephemeral storage of size 80Gi.
  * Loading is tested with [64] threads, split into [16] pods.
  * Benchmarking is tested with [128] threads, split into [16] pods.
  * Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* pgbouncer-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:811476
  * datadisk:2391
  * volume_size:1.8T
  * volume_used:793G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * pool 0
    * node:cl-worker38
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker38
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 2
    * node:cl-worker38
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 3
    * node:cl-worker38
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793709901

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1793709901-66494d4c66-lll2c: 0
* bexhoma-pool-pgbouncer-1-1793709901-66494d4c66-lmj7c: 0
* bexhoma-pool-pgbouncer-1-1793709901-66494d4c66-r547g: 0
* bexhoma-pool-pgbouncer-1-1793709901-66494d4c66-rw9db: 0
* bexhoma-sut-pgbouncer-1-1793709901-cc865b58f-crvqf: 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| pgbouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         9373.13 |                 6668.00 |             62500.00 |                              1497.00 | 1.00 |              539.89 |
| pgbouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8174.21 |                 7646.00 |             62500.00 |                              1491.00 | 1.00 |              470.83 |
| pgbouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8199.95 |                 7622.00 |             62500.00 |                              1467.00 | 1.00 |              472.32 |
| pgbouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8657.71 |                 7219.00 |             62500.00 |                              1479.00 | 1.00 |              498.68 |
| pgbouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7584.95 |                 8240.00 |             62500.00 |                              1507.00 | 1.00 |              436.89 |
| pgbouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         9328.36 |                 6700.00 |             62500.00 |                              1380.00 | 1.00 |              537.31 |
| pgbouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8482.63 |                 7368.00 |             62500.00 |                              1448.00 | 1.00 |              488.60 |
| pgbouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8122.16 |                 7695.00 |             62500.00 |                              1432.00 | 1.00 |              467.84 |
| pgbouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8502.24 |                 7351.00 |             62500.00 |                              1576.00 | 1.00 |              489.73 |
| pgbouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8304.54 |                 7526.00 |             62500.00 |                              1528.00 | 1.00 |              478.34 |
| pgbouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7920.42 |                 7891.00 |             62500.00 |                              1551.00 | 1.00 |              456.22 |
| pgbouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                        10507.73 |                 5948.00 |             62500.00 |                              1314.00 | 1.00 |              605.25 |
| pgbouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8535.92 |                 7322.00 |             62500.00 |                              1521.00 | 1.00 |              491.67 |
| pgbouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8483.78 |                 7367.00 |             62500.00 |                              1440.00 | 1.00 |              488.67 |
| pgbouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7802.75 |                 8010.00 |             62500.00 |                              1457.00 | 1.00 |              449.44 |
| pgbouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         8827.68 |                 7080.00 |             62500.00 |                              1447.00 | 1.00 |              508.47 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |         0.00 | 1.00 |              436.89 |                       136808.15 |                 8240.00 |           1000000.00 |                              1470.94 |

### Benchmarking

#### Per Connection

| DBMS                 | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1-1-1  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       1 |         8 |    11264 |          16 |            0 |                         9148.13 |                 6832.00 |              62500 |                             989.00 |
| pgbouncer-1-1-1-1-2  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       2 |         8 |    11264 |          16 |            0 |                         9621.31 |                 6496.00 |              62500 |                            1052.00 |
| pgbouncer-1-1-1-1-3  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       3 |         8 |    11264 |          16 |            0 |                         8705.95 |                 7179.00 |              62500 |                            1154.00 |
| pgbouncer-1-1-1-1-4  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       4 |         8 |    11264 |          16 |            0 |                         9221.01 |                 6778.00 |              62500 |                            1012.00 |
| pgbouncer-1-1-1-1-5  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       5 |         8 |    11264 |          16 |            0 |                         8937.51 |                 6993.00 |              62500 |                            1062.00 |
| pgbouncer-1-1-1-1-6  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       6 |         8 |    11264 |          16 |            0 |                         8781.79 |                 7117.00 |              62500 |                            1113.00 |
| pgbouncer-1-1-1-1-7  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       7 |         8 |    11264 |          16 |            0 |                         9278.50 |                 6736.00 |              62500 |                            1004.00 |
| pgbouncer-1-1-1-1-8  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       8 |         8 |    11264 |          16 |            0 |                         9035.71 |                 6917.00 |              62500 |                            1014.00 |
| pgbouncer-1-1-1-1-9  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       9 |         8 |    11264 |          16 |            0 |                         8779.32 |                 7119.00 |              62500 |                            1143.00 |
| pgbouncer-1-1-1-1-10 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      10 |         8 |    11264 |          16 |            0 |                         9329.75 |                 6699.00 |              62500 |                            1112.00 |
| pgbouncer-1-1-1-1-11 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      11 |         8 |    11264 |          16 |            0 |                         9043.55 |                 6911.00 |              62500 |                            1062.00 |
| pgbouncer-1-1-1-1-12 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      12 |         8 |    11264 |          16 |            0 |                         8950.31 |                 6983.00 |              62500 |                            1073.00 |
| pgbouncer-1-1-1-1-13 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      13 |         8 |    11264 |          16 |            0 |                         9431.12 |                 6627.00 |              62500 |                            1022.00 |
| pgbouncer-1-1-1-1-14 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      14 |         8 |    11264 |          16 |            0 |                         9126.75 |                 6848.00 |              62500 |                            1086.00 |
| pgbouncer-1-1-1-1-15 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      15 |         8 |    11264 |          16 |            0 |                         9014.86 |                 6933.00 |              62500 |                             985.00 |
| pgbouncer-1-1-1-1-16 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      16 |         8 |    11264 |          16 |            0 |                         8891.73 |                 7029.00 |              62500 |                            1080.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1 | pgbouncer-1-1-1 |                1 |       128 |   180224 |               1 |          16 |            0 |                       145297.29 |                 7179.00 |            1000000 |                            1154.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
