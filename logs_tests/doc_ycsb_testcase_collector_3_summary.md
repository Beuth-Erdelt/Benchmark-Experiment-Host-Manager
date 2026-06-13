## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1106s 
* Code: 1781312056
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
  * disk:926200
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781312056
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:926554
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781312056
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:926200
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781312056
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:926567
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781312056

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8], [1, 8]]

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7951.82 |                47159.00 |            375000.00 |                              4079.00 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7958.40 |                47120.00 |            375000.00 |                              4163.00 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7959.25 |                47115.00 |            375000.00 |                              4015.00 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8014.70 |                46789.00 |            375000.00 |                              4107.00 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7984.84 |                46964.00 |            375000.00 |                              4059.00 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7945.42 |                47197.00 |            375000.00 |                              4065.00 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7922.42 |                47334.00 |            375000.00 |                              4123.00 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8021.91 |                46747.00 |            375000.00 |                              4057.00 |
| PostgreSQL-1-2-0-1-1 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7458.38 |                50279.00 |            375000.00 |                              4747.00 |
| PostgreSQL-1-2-0-1-2 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7216.95 |                51961.00 |            375000.00 |                              4915.00 |
| PostgreSQL-1-2-0-1-3 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7342.86 |                51070.00 |            375000.00 |                              4803.00 |
| PostgreSQL-1-2-0-1-4 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7266.88 |                51604.00 |            375000.00 |                              4867.00 |
| PostgreSQL-1-2-0-1-5 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7471.31 |                50192.00 |            375000.00 |                              4751.00 |
| PostgreSQL-1-2-0-1-6 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7102.68 |                52797.00 |            375000.00 |                              4911.00 |
| PostgreSQL-1-2-0-1-7 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7677.98 |                48841.00 |            375000.00 |                              4683.00 |
| PostgreSQL-1-2-0-1-8 |             2.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7472.50 |                50184.00 |            375000.00 |                              4803.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                        63758.77 |                47334.00 |           3000000.00 |                              4083.50 |
| PostgreSQL-1-2 |             2.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                        59009.54 |                52797.00 |           3000000.00 |                              4810.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        44919.59 |                22262.00 |             500288 |                             671.00 |               499712 |                             21679.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6075.63 |                20574.00 |              62571 |                             646.00 |                62429 |                             25631.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         5993.48 |                20856.00 |              62340 |                             645.00 |                62660 |                             26239.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6026.42 |                20742.00 |              62330 |                             641.00 |                62670 |                             25119.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         5954.08 |                20994.00 |              62405 |                             638.00 |                62595 |                             27103.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         5992.90 |                20858.00 |              62314 |                             647.00 |                62686 |                             25503.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6049.46 |                20663.00 |              62520 |                             649.00 |                62480 |                             25967.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6075.63 |                20574.00 |              62545 |                             646.00 |                62455 |                             26767.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         5945.30 |                21025.00 |              62456 |                             640.00 |                62544 |                             26751.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 | PostgreSQL-1    |                2 |        1 |               1 |       1 |        64 |    49152 |           1 |            0 |                        45821.11 |                21824.00 |             499073 |                             658.00 |               500927 |                             23727.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       1 |         8 |     6144 |           8 |            0 |                         5934.58 |                21063.00 |              62509 |                             610.00 |                62491 |                             21919.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       8 |         8 |     6144 |           8 |            0 |                         5948.13 |                21015.00 |              62445 |                             627.00 |                62555 |                             21743.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       7 |         8 |     6144 |           8 |            0 |                         5946.43 |                21021.00 |              62263 |                             626.00 |                62737 |                             21903.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       5 |         8 |     6144 |           8 |            0 |                         5947.57 |                21017.00 |              62500 |                             644.00 |                62500 |                             21887.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       3 |         8 |     6144 |           8 |            0 |                         5924.45 |                21099.00 |              62532 |                             628.00 |                62468 |                             22623.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6011.35 |                20794.00 |              62314 |                             626.00 |                62686 |                             21647.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6051.22 |                20657.00 |              62566 |                             631.00 |                62434 |                             22031.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 | PostgreSQL-1    |                2 |        2 |               1 |       2 |         8 |     6144 |           8 |            0 |                         5988.31 |                20874.00 |              62398 |                             626.00 |                62602 |                             22479.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    49152 |               1 |           1 |            0 |                        44919.59 |                22262.00 |             500288 |                             671.00 |               499712 |                             21679.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48112.91 |                21025.00 |             499481 |                             649.00 |               500519 |                             27103.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        64 |    49152 |               1 |           1 |            0 |                        45821.11 |                21824.00 |             499073 |                             658.00 |               500927 |                             23727.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        64 |    49152 |               1 |           8 |            0 |                        47752.04 |                21099.00 |             499527 |                             644.00 |               500473 |                             22623.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       286.43 |      5.12 |           0.37 |                  4.75 |
| PostgreSQL-1-1-2-1 |       286.43 |      5.12 |           0.37 |                  4.75 |
| PostgreSQL-1-2-1-1 |       512.41 |      5.41 |           0.40 |                  5.31 |
| PostgreSQL-1-2-2-1 |       512.41 |      5.41 |           0.40 |                  5.31 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       112.14 |      0.00 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       112.14 |      0.00 |           0.11 |                  0.11 |
| PostgreSQL-1-2-1-1 |       194.74 |      5.91 |           0.11 |                  0.11 |
| PostgreSQL-1-2-2-1 |       194.74 |      5.91 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        18.60 |      0.95 |           0.46 |                  4.97 |
| PostgreSQL-1-1-2-1 |        57.01 |      1.70 |           0.48 |                  5.40 |
| PostgreSQL-1-2-1-1 |         0.00 |      0.21 |           0.30 |                  4.74 |
| PostgreSQL-1-2-2-1 |        70.48 |      2.74 |           0.48 |                  5.42 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |        15.77 |      0.00 |           0.10 |                  0.10 |
| PostgreSQL-1-2-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     10.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-1-2-1 |                     10.00 |                                     0.00 |                                             0.00 |                       64.00 |                                   64.00 |
| PostgreSQL-1-2-1-1 |                     49.00 |                                     0.00 |                                             0.00 |                       24.00 |                                   23.00 |
| PostgreSQL-1-2-2-1 |                     49.00 |                                     0.00 |                                             0.00 |                       24.00 |                                   23.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     45.00 |                                     0.00 |                                             0.00 |                       19.00 |                                   19.00 |
| PostgreSQL-1-1-2-1 |                     45.00 |                                     0.00 |                                             0.00 |                       19.00 |                                   19.00 |
| PostgreSQL-1-2-1-1 |                     18.00 |                                     0.00 |                                             0.00 |                       46.00 |                                   47.00 |
| PostgreSQL-1-2-2-1 |                      8.00 |                                     0.00 |                                             0.00 |                       56.00 |                                   56.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
