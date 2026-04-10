## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 497s 
* Code: 1774190325
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
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Dragonfly-64-8-196608-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:152282
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1774190325

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        54919.96 |                18773.00 |           1000000.00 |                              1548.25 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65499.04 |               152674.00 |         5001346.00 |                             534.00 |           4998654.00 |                               513.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       308.22 |      3.92 |           1.68 |                  1.68 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.14 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |      1299.60 |      8.81 |           1.68 |                  1.68 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       485.00 |      4.49 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             2000001.00 |                1.53 |                           9990.22 |                     6.31 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             8673876.00 |                1.53 |                          24921.94 |                     3.94 |                    0.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
