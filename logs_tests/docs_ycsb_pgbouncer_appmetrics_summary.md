## Show Summary

### Workload
YCSB SF=16
* Type: ycsb
* Duration: 873s 
* Code: 1792355926
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
  * Experiment uses bexhoma version 0.11.6.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:892848
  * datadisk:38203
  * volume_size:1.8T
  * volume_used:872G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * pool 0
    * node:cl-worker27
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 1
    * node:cl-worker22
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 2
    * node:cl-worker37
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * pool 3
    * node:cl-worker24
    * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1792355926

### SUT Container Restarts
* bexhoma-pool-pgbouncer-1-1792355926-6777dc6489-6vzqf: 0
* bexhoma-pool-pgbouncer-1-1792355926-6777dc6489-whlz5: 0
* bexhoma-pool-pgbouncer-1-1792355926-6777dc6489-zbf4b: 0
* bexhoma-pool-pgbouncer-1-1792355926-6777dc6489-zphcj: 0
* bexhoma-sut-pgbouncer-1-1792355926-558d48fddc-6m67l: 0

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| pgbouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6136.36 |               162963.00 |           1000000.00 |                              2387.00 | 16.00 |              353.45 |
| pgbouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6127.49 |               163199.00 |           1000000.00 |                              2145.00 | 16.00 |              352.94 |
| pgbouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6528.57 |               153173.00 |           1000000.00 |                              1993.00 | 16.00 |              376.05 |
| pgbouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6158.13 |               162387.00 |           1000000.00 |                              2205.00 | 16.00 |              354.71 |
| pgbouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6644.52 |               150500.00 |           1000000.00 |                              1829.00 | 16.00 |              382.72 |
| pgbouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7785.80 |               128439.00 |           1000000.00 |                              1771.00 | 16.00 |              448.46 |
| pgbouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7896.65 |               126636.00 |           1000000.00 |                              1648.00 | 16.00 |              454.85 |
| pgbouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7108.84 |               140670.00 |           1000000.00 |                              1975.00 | 16.00 |              409.47 |
| pgbouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6407.13 |               156076.00 |           1000000.00 |                              2053.00 | 16.00 |              369.05 |
| pgbouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         5989.42 |               166961.00 |           1000000.00 |                              2161.00 | 16.00 |              344.99 |
| pgbouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7689.47 |               130048.00 |           1000000.00 |                              1770.00 | 16.00 |              442.91 |
| pgbouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6936.74 |               144160.00 |           1000000.00 |                              1826.00 | 16.00 |              399.56 |
| pgbouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         7619.57 |               131241.00 |           1000000.00 |                              1989.00 | 16.00 |              438.89 |
| pgbouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6203.01 |               161212.00 |           1000000.00 |                              1994.00 | 16.00 |              357.29 |
| pgbouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6379.67 |               156748.00 |           1000000.00 |                              2395.00 | 16.00 |              367.47 |
| pgbouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         6150.17 |               162597.00 |           1000000.00 |                              2261.00 | 16.00 |              354.25 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |         0.00 | 16.00 |              344.99 |                       107761.53 |               166961.00 |          16000000.00 |                              2025.12 |

### Benchmarking

#### Per Connection

| DBMS                 | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1-1-1  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       1 |         8 |    11264 |          16 |            0 |                         6934.96 |               144197.00 |            1000000 |                            1540.00 |
| pgbouncer-1-1-1-1-2  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       2 |         8 |    11264 |          16 |            0 |                         6947.97 |               143927.00 |            1000000 |                            1525.00 |
| pgbouncer-1-1-1-1-3  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       3 |         8 |    11264 |          16 |            0 |                         6877.63 |               145399.00 |            1000000 |                            1534.00 |
| pgbouncer-1-1-1-1-4  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       4 |         8 |    11264 |          16 |            0 |                         6775.62 |               147588.00 |            1000000 |                            1592.00 |
| pgbouncer-1-1-1-1-5  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       5 |         8 |    11264 |          16 |            0 |                         6910.52 |               144707.00 |            1000000 |                            1505.00 |
| pgbouncer-1-1-1-1-6  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       6 |         8 |    11264 |          16 |            0 |                         6913.53 |               144644.00 |            1000000 |                            1453.00 |
| pgbouncer-1-1-1-1-7  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       7 |         8 |    11264 |          16 |            0 |                         6814.12 |               146754.00 |            1000000 |                            1574.00 |
| pgbouncer-1-1-1-1-8  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       8 |         8 |    11264 |          16 |            0 |                         7049.30 |               141858.00 |            1000000 |                            1396.00 |
| pgbouncer-1-1-1-1-9  | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       9 |         8 |    11264 |          16 |            0 |                         6787.12 |               147338.00 |            1000000 |                            1598.00 |
| pgbouncer-1-1-1-1-10 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      10 |         8 |    11264 |          16 |            0 |                         6860.59 |               145760.00 |            1000000 |                            1525.00 |
| pgbouncer-1-1-1-1-11 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      11 |         8 |    11264 |          16 |            0 |                         6726.17 |               148673.00 |            1000000 |                            1571.00 |
| pgbouncer-1-1-1-1-12 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      12 |         8 |    11264 |          16 |            0 |                         6899.03 |               144948.00 |            1000000 |                            1583.00 |
| pgbouncer-1-1-1-1-13 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      13 |         8 |    11264 |          16 |            0 |                         6854.20 |               145896.00 |            1000000 |                            1521.00 |
| pgbouncer-1-1-1-1-14 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      14 |         8 |    11264 |          16 |            0 |                         6932.70 |               144244.00 |            1000000 |                            1463.00 |
| pgbouncer-1-1-1-1-15 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      15 |         8 |    11264 |          16 |            0 |                         6950.77 |               143869.00 |            1000000 |                            1526.00 |
| pgbouncer-1-1-1-1-16 | pgbouncer-1-1-1 | pgbouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      16 |         8 |    11264 |          16 |            0 |                         6671.16 |               149899.00 |            1000000 |                            1601.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| pgbouncer-1-1-1 | pgbouncer-1-1-1 |                1 |       128 |   180224 |               1 |          16 |            0 |                       109905.36 |               149899.00 |           16000000 |                            1601.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.66 |      0.00 |           0.07 |                  0.07 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |      1188.65 |      8.75 |          24.04 |                 42.32 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       657.26 |      5.33 |           0.38 |                  0.39 |

### Benchmarking phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |         0.24 |      0.00 |           0.08 |                  0.08 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       848.81 |      7.14 |          26.74 |                 45.01 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| pgbouncer-1-1-1-1 |       512.17 |      4.73 |           0.30 |                  0.31 |

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
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolbenchmarking.log)
* CPU Throttling Rate [s/s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgbouncer-1-1-1-1 (bexhoma-metrics-pgbouncer-1-1-1-1-poolloading.log)

### Application Metrics

#### Loading phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                 60236.00 |                             0.33 |                                  0.00 |                                     158.00 |                                                      100.00 |

#### Loading phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                  257 |                                                   0 |                                                           0 |                                     57 |                                                 57 |

#### Benchmarking phase: component pool

| DBMS              |   PgBouncer Query Throughput [queries/s] |   PgBouncer Client Wait Time [s] |   PgBouncer Waiting Clients [clients] |   PgBouncer Idle Connections [connections] |   PgBouncer Pool Utilization, Active Server Connections [%] |
|:------------------|-----------------------------------------:|---------------------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                 55011.05 |                             0.07 |                                  0.00 |                                      67.00 |                                                       50.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| pgbouncer-1-1-1-1 |                                  257 |                                                   0 |                                                           0 |                                      8 |                                                  8 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
