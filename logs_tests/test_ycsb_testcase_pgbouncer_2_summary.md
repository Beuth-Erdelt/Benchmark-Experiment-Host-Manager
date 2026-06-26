## Show Summary

### Workload
YCSB SF=16
* Type: ycsb
* Duration: 2165s 
* Code: 1782220193
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
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PGBouncer'].
  * Import is handled by 16 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [16] pods.
  * Benchmarking is tested with [128] threads, split into [16] pods.
  * Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PGBouncer-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263095
  * datadisk:38196
  * volume_size:100G
  * volume_used:38G
  * cpu_list:0-127
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782220193
* PGBouncer-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263219
  * datadisk:38196
  * volume_size:100G
  * volume_used:38G
  * cpu_list:0-127
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782220193

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)
* DBMS PGBouncer-1 - Experiment 2 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)
* DBMS PGBouncer-1 - Experiment 2 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PGBouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2795.52 |               357715.00 |           1000000.00 |                              1875.00 | 16.00 |              161.02 |
| PGBouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         4413.32 |               226587.00 |           1000000.00 |                              1834.00 | 16.00 |              254.21 |
| PGBouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2776.53 |               360162.00 |           1000000.00 |                              1947.00 | 16.00 |              159.93 |
| PGBouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2767.12 |               361387.00 |           1000000.00 |                              1934.00 | 16.00 |              159.39 |
| PGBouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2798.85 |               357290.00 |           1000000.00 |                              1923.00 | 16.00 |              161.21 |
| PGBouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2777.11 |               360086.00 |           1000000.00 |                              1895.00 | 16.00 |              159.96 |
| PGBouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2787.59 |               358733.00 |           1000000.00 |                              1869.00 | 16.00 |              160.57 |
| PGBouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2748.22 |               363872.00 |           1000000.00 |                              1994.00 | 16.00 |              158.30 |
| PGBouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2765.98 |               361535.00 |           1000000.00 |                              1953.00 | 16.00 |              159.32 |
| PGBouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3456.27 |               289329.00 |           1000000.00 |                              1866.00 | 16.00 |              199.08 |
| PGBouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2783.65 |               359241.00 |           1000000.00 |                              1925.00 | 16.00 |              160.34 |
| PGBouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2760.98 |               362190.00 |           1000000.00 |                              1924.00 | 16.00 |              159.03 |
| PGBouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2768.27 |               361237.00 |           1000000.00 |                              1888.00 | 16.00 |              159.45 |
| PGBouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2759.71 |               362357.00 |           1000000.00 |                              2075.00 | 16.00 |              158.96 |
| PGBouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         2781.32 |               359542.00 |           1000000.00 |                              1937.00 | 16.00 |              160.20 |
| PGBouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3462.72 |               288790.00 |           1000000.00 |                              1999.00 | 16.00 |              199.45 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |         0.00 | 16.00 |              158.30 |                        47403.15 |               363872.00 |          16000000.00 |                              1927.38 |

### Execution

#### Per Connection

| DBMS                 | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1-3  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       3 |         8 |    11264 |          16 |            0 |                         3743.50 |               267130.00 |            1000000 |                            2297.00 |
| PGBouncer-1-1-1-1-4  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       4 |         8 |    11264 |          16 |            0 |                         3736.31 |               267644.00 |            1000000 |                            2263.00 |
| PGBouncer-1-2-1-1-6  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       6 |         8 |    11264 |          16 |            0 |                         3092.51 |               323362.00 |            1000000 |                            2639.00 |
| PGBouncer-1-1-1-1-2  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       2 |         8 |    11264 |          16 |            0 |                         3735.62 |               267693.00 |            1000000 |                            2309.00 |
| PGBouncer-1-2-1-1-16 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      16 |         8 |    11264 |          16 |            0 |                         3085.78 |               324067.00 |            1000000 |                            2515.00 |
| PGBouncer-1-1-1-1-11 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      11 |         8 |    11264 |          16 |            0 |                         3731.44 |               267993.00 |            1000000 |                            2343.00 |
| PGBouncer-1-1-1-1-15 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      15 |         8 |    11264 |          16 |            0 |                         3734.94 |               267742.00 |            1000000 |                            2295.00 |
| PGBouncer-1-2-1-1-15 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      15 |         8 |    11264 |          16 |            0 |                         3095.98 |               322999.00 |            1000000 |                            2589.00 |
| PGBouncer-1-1-1-1-6  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       6 |         8 |    11264 |          16 |            0 |                         3728.82 |               268181.00 |            1000000 |                            2331.00 |
| PGBouncer-1-2-1-1-7  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       7 |         8 |    11264 |          16 |            0 |                         3086.66 |               323975.00 |            1000000 |                            2789.00 |
| PGBouncer-1-2-1-1-8  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       8 |         8 |    11264 |          16 |            0 |                         3085.15 |               324133.00 |            1000000 |                            2707.00 |
| PGBouncer-1-1-1-1-14 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      14 |         8 |    11264 |          16 |            0 |                         3739.41 |               267422.00 |            1000000 |                            2327.00 |
| PGBouncer-1-2-1-1-3  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       3 |         8 |    11264 |          16 |            0 |                         3084.11 |               324243.00 |            1000000 |                            2689.00 |
| PGBouncer-1-1-1-1-7  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       7 |         8 |    11264 |          16 |            0 |                         3745.07 |               267018.00 |            1000000 |                            2199.00 |
| PGBouncer-1-2-1-1-13 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      13 |         8 |    11264 |          16 |            0 |                         3085.18 |               324130.00 |            1000000 |                            2679.00 |
| PGBouncer-1-1-1-1-9  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       9 |         8 |    11264 |          16 |            0 |                         3745.42 |               266993.00 |            1000000 |                            2317.00 |
| PGBouncer-1-1-1-1-13 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      13 |         8 |    11264 |          16 |            0 |                         3732.85 |               267892.00 |            1000000 |                            2339.00 |
| PGBouncer-1-2-1-1-1  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       1 |         8 |    11264 |          16 |            0 |                         3084.88 |               324162.00 |            1000000 |                            2675.00 |
| PGBouncer-1-2-1-1-9  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       9 |         8 |    11264 |          16 |            0 |                         3093.10 |               323300.00 |            1000000 |                            2635.00 |
| PGBouncer-1-1-1-1-1  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       1 |         8 |    11264 |          16 |            0 |                         3746.88 |               266889.00 |            1000000 |                            2195.00 |
| PGBouncer-1-2-1-1-2  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       2 |         8 |    11264 |          16 |            0 |                         3084.53 |               324198.00 |            1000000 |                            2757.00 |
| PGBouncer-1-1-1-1-12 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      12 |         8 |    11264 |          16 |            0 |                         3737.83 |               267535.00 |            1000000 |                            2223.00 |
| PGBouncer-1-2-1-1-12 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      12 |         8 |    11264 |          16 |            0 |                         3092.41 |               323372.00 |            1000000 |                            2553.00 |
| PGBouncer-1-1-1-1-10 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      10 |         8 |    11264 |          16 |            0 |                         3733.32 |               267858.00 |            1000000 |                            2363.00 |
| PGBouncer-1-2-1-1-4  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       4 |         8 |    11264 |          16 |            0 |                         3075.83 |               325116.00 |            1000000 |                            2765.00 |
| PGBouncer-1-2-1-1-5  | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |       5 |         8 |    11264 |          16 |            0 |                         3096.53 |               322942.00 |            1000000 |                            2653.00 |
| PGBouncer-1-1-1-1-16 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      16 |         8 |    11264 |          16 |            0 |                         3742.04 |               267234.00 |            1000000 |                            2269.00 |
| PGBouncer-1-1-1-1-5  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       5 |         8 |    11264 |          16 |            0 |                         3734.20 |               267795.00 |            1000000 |                            2323.00 |
| PGBouncer-1-2-1-1-11 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      11 |         8 |    11264 |          16 |            0 |                         3096.34 |               322962.00 |            1000000 |                            2541.00 |
| PGBouncer-1-1-1-1-8  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       8 |         8 |    11264 |          16 |            0 |                         3733.60 |               267838.00 |            1000000 |                            2231.00 |
| PGBouncer-1-2-1-1-14 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      14 |         8 |    11264 |          16 |            0 |                         3097.46 |               322845.00 |            1000000 |                            2655.00 |
| PGBouncer-1-2-1-1-10 | PGBouncer-1-2-1 | PGBouncer-1-2-1-1 | PGBouncer-1     |                2 |        1 |               1 |      10 |         8 |    11264 |          16 |            0 |                         3100.88 |               322489.00 |            1000000 |                            2575.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PGBouncer-1-1-1 | PGBouncer-1-1-1 |                1 |       128 |   180224 |               1 |          16 |            0 |                        59801.23 |               268181.00 |           16000000 |                            2363.00 |
| PGBouncer-1-2-1 | PGBouncer-1-2-1 |                2 |       128 |   180224 |               1 |          16 |            0 |                        49437.34 |               325116.00 |           16000000 |                            2789.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         0.26 |      0.00 |           0.04 |                  0.04 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      2144.32 |      8.21 |          23.98 |                 42.24 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1284.22 |      6.37 |           0.11 |                  0.11 |

### Execution phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         0.08 |      0.00 |           0.04 |                  0.04 |
| PGBouncer-1-2-1-1 |         0.16 |      0.00 |           0.04 |                  0.04 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1607.92 |      8.78 |          26.23 |                 44.49 |
| PGBouncer-1-2-1-1 |      1736.18 |      9.02 |          24.89 |                 43.13 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1105.78 |      7.25 |           0.11 |                  0.11 |
| PGBouncer-1-2-1-1 |      1082.55 |      6.70 |           0.11 |                  0.11 |

### Tests
* TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
