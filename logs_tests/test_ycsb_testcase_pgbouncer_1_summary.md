## Show Summary

### Workload
YCSB SF=16
* Type: ycsb
* Duration: 1292s 
* Code: 1782218874
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
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [64] threads, split into [16] pods.
  * Benchmarking is tested with [128] threads, split into [16] pods.
  * Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PGBouncer-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:294239
  * datadisk:38200
  * cpu_list:0-127
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782218874

### Workflow

#### Actual

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

#### Planned

* DBMS PGBouncer-1 - Experiment 1 Client 1: ycsb (16 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| PGBouncer-1-1-0-1-1  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         5139.20 |               194583.00 |           1000000.00 |                              1685.00 | 16.00 |              296.02 |
| PGBouncer-1-1-0-1-2  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3398.02 |               294289.00 |           1000000.00 |                              2203.00 | 16.00 |              195.73 |
| PGBouncer-1-1-0-1-3  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3404.60 |               293720.00 |           1000000.00 |                              2203.00 | 16.00 |              196.11 |
| PGBouncer-1-1-0-1-4  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3369.24 |               296803.00 |           1000000.00 |                              2233.00 | 16.00 |              194.07 |
| PGBouncer-1-1-0-1-5  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3440.91 |               290621.00 |           1000000.00 |                              1966.00 | 16.00 |              198.20 |
| PGBouncer-1-1-0-1-6  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3475.15 |               287757.00 |           1000000.00 |                              1937.00 | 16.00 |              200.17 |
| PGBouncer-1-1-0-1-7  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3410.84 |               293183.00 |           1000000.00 |                              2079.00 | 16.00 |              196.46 |
| PGBouncer-1-1-0-1-8  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3383.13 |               295584.00 |           1000000.00 |                              2105.00 | 16.00 |              194.87 |
| PGBouncer-1-1-0-1-9  |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3363.75 |               297287.00 |           1000000.00 |                              1973.00 | 16.00 |              193.75 |
| PGBouncer-1-1-0-1-10 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3419.21 |               292465.00 |           1000000.00 |                              2233.00 | 16.00 |              196.95 |
| PGBouncer-1-1-0-1-11 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         4440.20 |               225215.00 |           1000000.00 |                              2203.00 | 16.00 |              255.76 |
| PGBouncer-1-1-0-1-12 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         4393.34 |               227617.00 |           1000000.00 |                              1867.00 | 16.00 |              253.06 |
| PGBouncer-1-1-0-1-13 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3353.35 |               298209.00 |           1000000.00 |                              2046.00 | 16.00 |              193.15 |
| PGBouncer-1-1-0-1-14 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3406.38 |               293567.00 |           1000000.00 |                              2203.00 | 16.00 |              196.21 |
| PGBouncer-1-1-0-1-15 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         4446.74 |               224884.00 |           1000000.00 |                              1890.00 | 16.00 |              256.13 |
| PGBouncer-1-1-0-1-16 |             1.00 |      4.00 | 11264.00 |       16.00 |         0.00 |                         3413.55 |               292950.00 |           1000000.00 |                              2145.00 | 16.00 |              196.62 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PGBouncer-1-1 |             1.00 |     64.00 | 180224.00 |       16.00 |         0.00 | 16.00 |              193.15 |                        59257.62 |               298209.00 |          16000000.00 |                              2060.69 |

### Execution

#### Per Connection

| DBMS                 | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:---------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PGBouncer-1-1-1-1-3  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       3 |         8 |    11264 |          16 |            0 |                         3132.75 |               319208.00 |            1000000 |                            2723.00 |
| PGBouncer-1-1-1-1-16 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      16 |         8 |    11264 |          16 |            0 |                         3120.01 |               320512.00 |            1000000 |                            2833.00 |
| PGBouncer-1-1-1-1-7  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       7 |         8 |    11264 |          16 |            0 |                         3127.68 |               319726.00 |            1000000 |                            2727.00 |
| PGBouncer-1-1-1-1-5  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       5 |         8 |    11264 |          16 |            0 |                         4081.45 |               245011.00 |            1000000 |                            2093.00 |
| PGBouncer-1-1-1-1-13 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      13 |         8 |    11264 |          16 |            0 |                         3119.80 |               320533.00 |            1000000 |                            2783.00 |
| PGBouncer-1-1-1-1-15 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      15 |         8 |    11264 |          16 |            0 |                         3140.64 |               318406.00 |            1000000 |                            2701.00 |
| PGBouncer-1-1-1-1-11 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      11 |         8 |    11264 |          16 |            0 |                         3134.76 |               319004.00 |            1000000 |                            2645.00 |
| PGBouncer-1-1-1-1-12 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      12 |         8 |    11264 |          16 |            0 |                         3121.76 |               320332.00 |            1000000 |                            2945.00 |
| PGBouncer-1-1-1-1-14 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      14 |         8 |    11264 |          16 |            0 |                         3125.32 |               319967.00 |            1000000 |                            2865.00 |
| PGBouncer-1-1-1-1-6  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       6 |         8 |    11264 |          16 |            0 |                         3131.01 |               319386.00 |            1000000 |                            2761.00 |
| PGBouncer-1-1-1-1-2  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       2 |         8 |    11264 |          16 |            0 |                         3133.46 |               319136.00 |            1000000 |                            2735.00 |
| PGBouncer-1-1-1-1-8  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       8 |         8 |    11264 |          16 |            0 |                         3123.32 |               320172.00 |            1000000 |                            2907.00 |
| PGBouncer-1-1-1-1-9  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       9 |         8 |    11264 |          16 |            0 |                         3120.19 |               320493.00 |            1000000 |                            2947.00 |
| PGBouncer-1-1-1-1-10 | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |      10 |         8 |    11264 |          16 |            0 |                         3122.99 |               320206.00 |            1000000 |                            2925.00 |
| PGBouncer-1-1-1-1-4  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       4 |         8 |    11264 |          16 |            0 |                         3131.40 |               319346.00 |            1000000 |                            2759.00 |
| PGBouncer-1-1-1-1-1  | PGBouncer-1-1-1 | PGBouncer-1-1-1-1 | PGBouncer-1     |                1 |        1 |               1 |       1 |         8 |    11264 |          16 |            0 |                         3126.70 |               319826.00 |            1000000 |                            2861.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|
| PGBouncer-1-1-1 | PGBouncer-1-1-1 |                1 |       128 |   180224 |               1 |          16 |            0 |                        50993.25 |               320533.00 |           16000000 |                            2947.00 |

### Monitoring

### Loading phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         0.16 |      0.00 |           0.04 |                  0.04 |

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      2303.60 |     10.09 |          23.90 |                 42.15 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1301.22 |      8.09 |           0.11 |                  0.11 |

### Execution phase: component pool

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |         0.11 |      0.00 |           0.04 |                  0.04 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1889.83 |      8.88 |          26.73 |                 45.00 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| PGBouncer-1-1-1-1 |      1122.85 |      6.99 |           0.11 |                  0.11 |

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
