## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 398s 
* Code: 1775817214
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
  * Experiment uses bexhoma version 0.9.5.
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
  * disk:150969
  * datadisk:1
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081965441024
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:5.15.0-1099-nvidia
    * node:cl-worker27
    * disk:1317019
    * datadisk:1
    * cpu_list:0-255
  * worker 1
    * RAM:540591206400
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-107-generic
    * node:cl-worker24
    * disk:149843
    * datadisk:1
    * cpu_list:0-95
  * worker 2
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1166438
    * datadisk:1
    * cpu_list:0-223
  * eval_parameters
    * code:1775817214
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        75876.77 |                14270.00 |           1000000.00 |                              1504.25 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65504.61 |               152661.00 |         4997409.00 |                             311.00 |           5002591.00 |                               299.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |        34.36 |      0.73 |           2.43 |                  2.43 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.15 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       777.11 |      5.45 |           4.92 |                  4.92 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       452.00 |      4.48 |           0.12 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             2000000.00 |                4.59 |                          25843.62 |                     4.34 |                    0.00 |

#### Execution phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             8386902.00 |                4.60 |                          62087.48 |                     3.25 |                 2019.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
