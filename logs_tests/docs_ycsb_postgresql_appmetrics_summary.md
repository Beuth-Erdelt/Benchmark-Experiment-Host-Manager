## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1051s 
* Code: 1781460454
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209191
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209720
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209816
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209870
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8, 1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8, 1, 8]]

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8147.57 |                46026.00 |            375000.00 |                              4663.00 | 3.00 |              234.65 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8149.69 |                46014.00 |            375000.00 |                              4931.00 | 3.00 |              234.71 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8148.45 |                46021.00 |            375000.00 |                              4807.00 | 3.00 |              234.68 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8148.10 |                46023.00 |            375000.00 |                              4691.00 | 3.00 |              234.67 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8150.76 |                46008.00 |            375000.00 |                              4839.00 | 3.00 |              234.74 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8146.68 |                46031.00 |            375000.00 |                              4815.00 | 3.00 |              234.62 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8150.05 |                46012.00 |            375000.00 |                              4763.00 | 3.00 |              234.72 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8152.35 |                45999.00 |            375000.00 |                              4679.00 | 3.00 |              234.79 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              234.62 |                        65193.66 |                46031.00 |           3000000.00 |                              4773.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32665.15 |                91841.00 |            1499978 |                             656.00 |              1500022 |                              5463.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4084.92 |                91801.00 |             187584 |                             602.00 |               187416 |                              6615.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4081.94 |                91868.00 |             187200 |                             684.00 |               187800 |                              6511.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4085.55 |                91787.00 |             187722 |                             596.00 |               187278 |                              6675.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4085.77 |                91782.00 |             187341 |                             617.00 |               187659 |                              6631.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4085.90 |                91779.00 |             187621 |                             669.00 |               187379 |                              6695.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4085.41 |                91790.00 |             187172 |                             577.00 |               187828 |                              6479.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4085.72 |                91783.00 |             187419 |                             677.00 |               187581 |                              6535.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4086.48 |                91766.00 |             187715 |                             573.00 |               187285 |                              6483.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48922.08 |                61322.00 |            1499514 |                             876.00 |              1500486 |                             12495.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6112.17 |                61353.00 |             187606 |                             577.00 |               187394 |                              4495.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6120.05 |                61274.00 |             187399 |                             574.00 |               187601 |                              4703.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6119.75 |                61277.00 |             187019 |                             564.00 |               187981 |                              4519.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6111.87 |                61356.00 |             187229 |                             608.00 |               187771 |                              4583.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6120.55 |                61269.00 |             187172 |                             582.00 |               187828 |                              4663.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6120.25 |                61272.00 |             187723 |                             597.00 |               187277 |                              4695.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6120.75 |                61267.00 |             187242 |                             591.00 |               187758 |                              4523.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6120.05 |                61274.00 |             187726 |                             573.00 |               187274 |                              4771.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32665.15 |                91841.00 |            1499978 |                             656.00 |              1500022 |                              5463.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32681.70 |                91868.00 |            1499774 |                             684.00 |              1500226 |                              6695.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48922.08 |                61322.00 |            1499514 |                             876.00 |              1500486 |                             12495.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48945.45 |                61356.00 |            1499116 |                             608.00 |              1500884 |                              4771.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       528.77 |      8.53 |           0.40 |                  4.75 |
| PostgreSQL-1-1-2-1 |       528.77 |      8.53 |           0.40 |                  4.75 |
| PostgreSQL-1-1-3-1 |       528.77 |      8.53 |           0.40 |                  4.75 |
| PostgreSQL-1-1-4-1 |       528.77 |      8.53 |           0.40 |                  4.75 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       141.10 |      1.49 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       141.10 |      1.49 |           0.11 |                  0.11 |
| PostgreSQL-1-1-3-1 |       141.10 |      1.49 |           0.11 |                  0.11 |
| PostgreSQL-1-1-4-1 |       141.10 |      1.49 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       580.19 |      7.17 |           0.53 |                  5.46 |
| PostgreSQL-1-1-2-1 |       522.01 |      6.99 |           0.48 |                  5.53 |
| PostgreSQL-1-1-3-1 |       347.03 |     11.17 |           0.48 |                  5.55 |
| PostgreSQL-1-1-4-1 |       314.85 |      8.92 |           0.48 |                  5.60 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       139.96 |      2.12 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2-1 |       177.64 |      5.19 |           0.13 |                  0.13 |
| PostgreSQL-1-1-3-1 |       105.49 |      5.49 |           0.13 |                  0.13 |
| PostgreSQL-1-1-4-1 |       138.63 |      7.67 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |
| PostgreSQL-1-1-2-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |
| PostgreSQL-1-1-3-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |
| PostgreSQL-1-1-4-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     58.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   13.00 |
| PostgreSQL-1-1-2-1 |                     59.00 |                                     0.00 |                                             0.00 |                        9.00 |                                   10.00 |
| PostgreSQL-1-1-3-1 |                     59.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   15.00 |
| PostgreSQL-1-1-4-1 |                     60.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   11.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
