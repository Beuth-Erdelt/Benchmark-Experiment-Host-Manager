## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 7256s 
* Code: 1781304745
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [3].
  * Experiment uses bexhoma version 0.9.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921646
  * volume_size:15G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781304745
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921648
  * volume_size:15G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781304745
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921650
  * volume_size:15G
  * volume_used:5.1G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781304745
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921659
  * volume_size:15G
  * volume_used:5.1G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781304745

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.24 |              1554454.00 |            375000.00 |                            233215.00 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.03 |              1555792.00 |            375000.00 |                            232959.00 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.57 |              1552325.00 |            375000.00 |                            233087.00 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.11 |              1555319.00 |            375000.00 |                            233215.00 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.28 |              1554216.00 |            375000.00 |                            232831.00 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.51 |              1552760.00 |            375000.00 |                            233087.00 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.19 |              1554782.00 |            375000.00 |                            233087.00 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          241.44 |              1553186.00 |            375000.00 |                            233215.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                         1930.37 |              1555792.00 |           3000000.00 |                            233087.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                          950.54 |              1052033.00 |             499868 |                             840.00 |               500132 |                           2619391.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                          109.90 |              1137439.00 |              62469 |                             835.00 |                62531 |                           2680831.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                          111.14 |              1124737.00 |              62569 |                             834.00 |                62431 |                           2738175.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                          109.31 |              1143516.00 |              62395 |                             827.00 |                62605 |                           2564095.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                          110.41 |              1132138.00 |              62803 |                             831.00 |                62197 |                           2777087.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                          107.52 |              1162552.00 |              62105 |                             831.00 |                62895 |                           2697215.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                          106.66 |              1171905.00 |              62416 |                             826.00 |                62584 |                           2748415.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                          109.99 |              1136439.00 |              62507 |                             830.00 |                62493 |                           2701311.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                          115.08 |              1086234.00 |              62471 |                             833.00 |                62529 |                           2682879.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                          723.17 |              1382795.00 |             499539 |                             876.00 |               500461 |                           3334143.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                           99.79 |              1252640.00 |              62458 |                             859.00 |                62542 |                           3250175.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                          100.14 |              1248290.00 |              62299 |                             870.00 |                62701 |                           3078143.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                          100.07 |              1249156.00 |              62201 |                             862.00 |                62799 |                           2947071.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                           99.80 |              1252454.00 |              62208 |                             870.00 |                62792 |                           3119103.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                          100.53 |              1243356.00 |              62373 |                             862.00 |                62627 |                           3117055.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                          100.32 |              1245973.00 |              62344 |                             875.00 |                62656 |                           3223551.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                          100.53 |              1243425.00 |              62639 |                             874.00 |                62361 |                           3164159.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                          100.29 |              1246354.00 |              62427 |                             861.00 |                62573 |                           3102719.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    49152 |               1 |           1 |            0 |                          950.54 |              1052033.00 |             499868 |                             840.00 |               500132 |                           2619391.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    49152 |               1 |           8 |            0 |                          880.01 |              1171905.00 |             499735 |                             835.00 |               500265 |                           2777087.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |    49152 |               1 |           1 |            0 |                          723.17 |              1382795.00 |             499539 |                             876.00 |               500461 |                           3334143.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        64 |    49152 |               1 |           8 |            0 |                          801.48 |              1252640.00 |             498949 |                             875.00 |               501051 |                           3250175.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       491.06 |      0.51 |           0.33 |                  4.72 |
| PostgreSQL-1-1-2-1 |       491.06 |      0.51 |           0.33 |                  4.72 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       352.27 |      1.09 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       352.27 |      1.09 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       183.47 |      0.23 |           0.41 |                  5.14 |
| PostgreSQL-1-1-2-1 |       191.65 |      0.22 |           0.40 |                  5.39 |
| PostgreSQL-1-2-1-1 |       874.55 |      0.20 |           0.34 |                  5.41 |
| PostgreSQL-1-2-2-1 |       190.35 |      0.20 |           0.40 |                  5.47 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        87.81 |      0.28 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2-1 |        87.81 |      0.55 |           0.12 |                  0.13 |
| PostgreSQL-1-2-1-1 |        86.46 |      0.08 |           0.13 |                  0.13 |
| PostgreSQL-1-2-2-1 |        86.46 |      0.49 |           0.12 |                  0.12 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     25.00 |                                     0.00 |                                             0.00 |                       66.00 |                                   64.00 |
| PostgreSQL-1-1-2-1 |                     25.00 |                                     0.00 |                                             0.00 |                       66.00 |                                   64.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-1-2-1 |                      3.00 |                                     0.00 |                                             0.00 |                       65.00 |                                   64.00 |
| PostgreSQL-1-2-1-1 |                     22.00 |                                     0.00 |                                             0.00 |                       66.00 |                                   64.00 |
| PostgreSQL-1-2-2-1 |                     24.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
