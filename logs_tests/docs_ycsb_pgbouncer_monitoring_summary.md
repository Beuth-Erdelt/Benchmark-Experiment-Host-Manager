## Show Summary

### Workload
YCSB SF=32
* Type: ycsb
* Duration: 869s 
* Code: 1794849659
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 32000000.
  * Ordering of inserts is hashed.
  * Number of operations is 16000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [11].
  * Factors for benchmarking are [11].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
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
  * disk:1396173
  * datadisk:71058
  * volume_size:1.8T
  * volume_used:1.4T
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
    * code:1794849659

### Ingestion
* PGBouncer-1: 16 of 16 units ok

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1794849659-df56d9678-5mq6l: 0
* bexhoma-pool-pgbouncer-1-1794849659-df56d9678-8ctnb: 0
* bexhoma-pool-pgbouncer-1-1794849659-df56d9678-dnjft: 0
* bexhoma-pool-pgbouncer-1-1794849659-df56d9678-lhdz2: 0
* bexhoma-sut-pgbouncer-1-1794849659-86cf4579cf-46qw4: 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| pgbouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5325.25 |               375569.00 |           2000000.00 |                              2179.00 | 32.00 |              306.73 |
| pgbouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5293.75 |               377804.00 |           2000000.00 |                              2411.00 | 32.00 |              304.92 |
| pgbouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5291.41 |               377971.00 |           2000000.00 |                              2433.00 | 32.00 |              304.79 |
| pgbouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5264.54 |               379900.00 |           2000000.00 |                              2283.00 | 32.00 |              303.24 |
| pgbouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5300.34 |               377334.00 |           2000000.00 |                              2175.00 | 32.00 |              305.30 |
| pgbouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5307.73 |               376809.00 |           2000000.00 |                              2427.00 | 32.00 |              305.73 |
| pgbouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5303.00 |               377145.00 |           2000000.00 |                              1986.00 | 32.00 |              305.45 |
| pgbouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5320.88 |               375878.00 |           2000000.00 |                              2089.00 | 32.00 |              306.48 |
| pgbouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5303.72 |               377094.00 |           2000000.00 |                              2355.00 | 32.00 |              305.49 |
| pgbouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5307.52 |               376824.00 |           2000000.00 |                              2403.00 | 32.00 |              305.71 |
| pgbouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5302.52 |               377179.00 |           2000000.00 |                              2593.00 | 32.00 |              305.43 |
| pgbouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5321.27 |               375850.00 |           2000000.00 |                              2037.00 | 32.00 |              306.51 |
| pgbouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5308.60 |               376747.00 |           2000000.00 |                              2245.00 | 32.00 |              305.78 |
| pgbouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5319.04 |               376008.00 |           2000000.00 |                              2243.00 | 32.00 |              306.38 |
| pgbouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         5318.26 |               376063.00 |           2000000.00 |                              2355.00 | 32.00 |              306.33 |
| pgbouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         8487.63 |               235637.00 |           2000000.00 |                              1895.00 | 32.00 |              488.89 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |    SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |     0.00 | 32.00 |              303.24 |                        88075.46 |               379900.00 |          32000000.00 |                              2256.81 |

### Benchmarking

#### Per Connection

| connection           | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1-1-1  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       1 |         8 |    11264 |        0 |                         9756.29 |               102498.00 |            1000000 |                            1215.00 |
| pgbouncer-1-1-1-1-2  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       2 |         8 |    11264 |        0 |                         9725.92 |               102818.00 |            1000000 |                            1236.00 |
| pgbouncer-1-1-1-1-3  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       3 |         8 |    11264 |        0 |                         9740.42 |               102665.00 |            1000000 |                            1197.00 |
| pgbouncer-1-1-1-1-4  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       4 |         8 |    11264 |        0 |                         9763.91 |               102418.00 |            1000000 |                            1232.00 |
| pgbouncer-1-1-1-1-5  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       5 |         8 |    11264 |        0 |                         9688.98 |               103210.00 |            1000000 |                            1229.00 |
| pgbouncer-1-1-1-1-6  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       6 |         8 |    11264 |        0 |                         9787.90 |               102167.00 |            1000000 |                            1220.00 |
| pgbouncer-1-1-1-1-7  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       7 |         8 |    11264 |        0 |                         9776.89 |               102282.00 |            1000000 |                            1271.00 |
| pgbouncer-1-1-1-1-8  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       8 |         8 |    11264 |        0 |                         9766.29 |               102393.00 |            1000000 |                            1262.00 |
| pgbouncer-1-1-1-1-9  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       9 |         8 |    11264 |        0 |                         9750.20 |               102562.00 |            1000000 |                            1226.00 |
| pgbouncer-1-1-1-1-10 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      10 |         8 |    11264 |        0 |                         9765.34 |               102403.00 |            1000000 |                            1219.00 |
| pgbouncer-1-1-1-1-11 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      11 |         8 |    11264 |        0 |                         9700.73 |               103085.00 |            1000000 |                            1242.00 |
| pgbouncer-1-1-1-1-12 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      12 |         8 |    11264 |        0 |                         9829.07 |               101739.00 |            1000000 |                            1248.00 |
| pgbouncer-1-1-1-1-13 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      13 |         8 |    11264 |        0 |                         9781.48 |               102234.00 |            1000000 |                            1182.00 |
| pgbouncer-1-1-1-1-14 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      14 |         8 |    11264 |        0 |                         9752.77 |               102535.00 |            1000000 |                            1251.00 |
| pgbouncer-1-1-1-1-15 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      15 |         8 |    11264 |        0 |                         9774.88 |               102303.00 |            1000000 |                            1221.00 |
| pgbouncer-1-1-1-1-16 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      16 |         8 |    11264 |        0 |                         9823.18 |               101800.00 |            1000000 |                            1241.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1 | pgbouncer-1-1-1 |                1 |        1 |               1 |          16 |       128 |   180224 |        0 |                       156184.26 |               103210.00 |           16000000 |                            1271.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.42 |      0.00 |           0.01 |                  0.01 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |      2625.68 |     10.53 |          44.38 |                 64.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |      1901.97 |      6.98 |           0.30 |                  0.30 |

### Benchmarking phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.05 |      0.00 |           0.01 |                  0.01 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       540.15 |      7.26 |          49.58 |                 64.00 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       836.11 |      9.06 |           0.10 |                  0.11 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
