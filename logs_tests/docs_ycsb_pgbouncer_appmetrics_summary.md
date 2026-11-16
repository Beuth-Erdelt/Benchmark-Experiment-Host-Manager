## Show Summary

### Workload
YCSB SF=16
* Type: ycsb
* Duration: 736s 
* Code: 1794778724
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'C'.
  * Number of rows to insert is 16000000.
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
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 16 processes (pods).
  * SUT is fixed to cl-worker36.
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
  * disk:1091350
  * datadisk:38200
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * pool 0
    * node:cl-worker37
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker29
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 2
    * node:cl-worker39
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 3
    * node:cl-worker27
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794778724

### Ingestion
* PGBouncer-1: 16 of 16 units ok

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-4zfp4: 0
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-7vpnw: 0
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-dp6bp: 0
* bexhoma-pool-pgbouncer-1-1794778724-8b49548fb-g6jxg: 0
* bexhoma-sut-pgbouncer-1-1794778724-6c797f9857-7d6b7: 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| pgbouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6325.95 |               158079.00 |           1000000.00 |                              1864.00 | 16.00 |              364.37 |
| pgbouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6309.27 |               158497.00 |           1000000.00 |                              2107.00 | 16.00 |              363.41 |
| pgbouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6969.81 |               143476.00 |           1000000.00 |                              2153.00 | 16.00 |              401.46 |
| pgbouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6299.61 |               158740.00 |           1000000.00 |                              2273.00 | 16.00 |              362.86 |
| pgbouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6418.36 |               155803.00 |           1000000.00 |                              1884.00 | 16.00 |              369.70 |
| pgbouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6521.41 |               153341.00 |           1000000.00 |                              1992.00 | 16.00 |              375.63 |
| pgbouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         7406.58 |               135015.00 |           1000000.00 |                              1853.00 | 16.00 |              426.62 |
| pgbouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6480.92 |               154299.00 |           1000000.00 |                              2071.00 | 16.00 |              373.30 |
| pgbouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6365.13 |               157106.00 |           1000000.00 |                              1964.00 | 16.00 |              366.63 |
| pgbouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6364.85 |               157113.00 |           1000000.00 |                              2137.00 | 16.00 |              366.62 |
| pgbouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6316.24 |               158322.00 |           1000000.00 |                              2051.00 | 16.00 |              363.82 |
| pgbouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6447.74 |               155093.00 |           1000000.00 |                              2179.00 | 16.00 |              371.39 |
| pgbouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         7575.93 |               131997.00 |           1000000.00 |                              1964.00 | 16.00 |              436.37 |
| pgbouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         8630.96 |               115862.00 |           1000000.00 |                              1884.00 | 16.00 |              497.14 |
| pgbouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         6278.45 |               159275.00 |           1000000.00 |                              2343.00 | 16.00 |              361.64 |
| pgbouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |     0.00 |                         8150.89 |               122686.00 |           1000000.00 |                              1819.00 | 16.00 |              469.49 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |    SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |     0.00 | 16.00 |              361.64 |                       108862.10 |               159275.00 |          16000000.00 |                              2033.62 |

### Benchmarking

#### Per Connection

| connection           | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1-1-1  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       1 |         8 |    11264 |        0 |                         6840.37 |               146191.00 |            1000000 |                            1444.00 |
| pgbouncer-1-1-1-1-2  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       2 |         8 |    11264 |        0 |                         8777.47 |               113928.00 |            1000000 |                            1186.00 |
| pgbouncer-1-1-1-1-3  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       3 |         8 |    11264 |        0 |                         6714.88 |               148923.00 |            1000000 |                            1511.00 |
| pgbouncer-1-1-1-1-4  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       4 |         8 |    11264 |        0 |                         6829.62 |               146421.00 |            1000000 |                            1469.00 |
| pgbouncer-1-1-1-1-5  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       5 |         8 |    11264 |        0 |                         6816.54 |               146702.00 |            1000000 |                            1413.00 |
| pgbouncer-1-1-1-1-6  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       6 |         8 |    11264 |        0 |                         6802.21 |               147011.00 |            1000000 |                            1505.00 |
| pgbouncer-1-1-1-1-7  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       7 |         8 |    11264 |        0 |                         6795.51 |               147156.00 |            1000000 |                            1433.00 |
| pgbouncer-1-1-1-1-8  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       8 |         8 |    11264 |        0 |                         6920.75 |               144493.00 |            1000000 |                            1337.00 |
| pgbouncer-1-1-1-1-9  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |       9 |         8 |    11264 |        0 |                         6752.15 |               148101.00 |            1000000 |                            1483.00 |
| pgbouncer-1-1-1-1-10 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      10 |         8 |    11264 |        0 |                         6861.30 |               145745.00 |            1000000 |                            1437.00 |
| pgbouncer-1-1-1-1-11 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      11 |         8 |    11264 |        0 |                         6785.46 |               147374.00 |            1000000 |                            1547.00 |
| pgbouncer-1-1-1-1-12 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      12 |         8 |    11264 |        0 |                         8973.92 |               111434.00 |            1000000 |                            1100.00 |
| pgbouncer-1-1-1-1-13 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      13 |         8 |    11264 |        0 |                         6870.40 |               145552.00 |            1000000 |                            1427.00 |
| pgbouncer-1-1-1-1-14 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      14 |         8 |    11264 |        0 |                         8825.58 |               113307.00 |            1000000 |                            1209.00 |
| pgbouncer-1-1-1-1-15 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      15 |         8 |    11264 |        0 |                         6863.23 |               145704.00 |            1000000 |                            1462.00 |
| pgbouncer-1-1-1-1-16 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 |                1 |        1 |               1 |      16 |         8 |    11264 |        0 |                         6808.93 |               146866.00 |            1000000 |                            1488.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1 | pgbouncer-1-1-1 |                1 |        1 |               1 |          16 |       128 |   180224 |        0 |                       115238.31 |               148923.00 |           16000000 |                            1547.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         1.18 |      0.01 |           0.08 |                  0.08 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |      1261.40 |     10.11 |          24.65 |                 42.92 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       744.93 |      6.21 |           0.43 |                  0.44 |

### Benchmarking phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.40 |      0.01 |           0.09 |                  0.09 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       789.08 |      7.70 |          26.74 |                 45.01 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       717.88 |      6.68 |           0.20 |                  0.21 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                 56822.81 |                             0.63 |                                  0.00 |                                     181.00 |                                                       26.79 |

#### Loading phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                               257.00 |                                                0.00 |                                                        0.00 |                                  31.00 |                                              31.00 |

#### Benchmarking phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                 57876.32 |                             0.18 |                                  0.00 |                                      78.00 |                                                       50.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                               257.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |

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
