## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 425s 
* Code: 1781947318
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217100
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781947318

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10544.07 |                11855.00 |            125000.00 |                              1765.00 | 1.00 |              303.67 |
| Dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9939.57 |                12576.00 |            125000.00 |                              2012.00 | 1.00 |              286.26 |
| Dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10401.07 |                12018.00 |            125000.00 |                              1935.00 | 1.00 |              299.55 |
| Dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10303.33 |                12132.00 |            125000.00 |                              2059.00 | 1.00 |              296.74 |
| Dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9921.42 |                12599.00 |            125000.00 |                              1833.00 | 1.00 |              285.74 |
| Dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10830.01 |                11542.00 |            125000.00 |                              1730.00 | 1.00 |              311.90 |
| Dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9906.48 |                12618.00 |            125000.00 |                              1841.00 | 1.00 |              285.31 |
| Dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10382.92 |                12039.00 |            125000.00 |                              1948.00 | 1.00 |              299.03 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              285.31 |                        82228.88 |                12618.00 |           1000000.00 |                              1890.38 |

### Execution

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1-1-1 | Dragonfly-1-1-1 | Dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65502.04 |               152667.00 |            5001040 |                            1877.00 |              4998960 |                              1831.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1 | Dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65502.04 |               152667.00 |            5001040 |                            1877.00 |              4998960 |                              1831.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       269.94 |      8.13 |           1.69 |                  1.69 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |      1799.35 |     15.46 |           1.76 |                  1.76 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       751.53 |      5.15 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             2000000.00 |                1.54 |                           9930.00 |                     6.27 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             8584639.00 |                1.54 |                          30387.49 |                     3.20 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
