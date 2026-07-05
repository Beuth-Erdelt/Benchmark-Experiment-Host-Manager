## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 442s 
* Code: 1782826255
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 5Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* DragonflyCluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * datadisk:1
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:594803
    * datadisk:1
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145307
    * datadisk:1
    * cpu_list:0-95
  * worker 2
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:772228
    * datadisk:1
    * cpu_list:0-127
  * eval_parameters
    * code:1782826255
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1782826255-7794959675-djt9l: 0
* bx-w-dragonfly-ycsb-1-0: 0
* bx-w-dragonfly-ycsb-1-1: 0
* bx-w-dragonfly-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4828.12 |                25890.00 |            125000.00 |                             37823.00 | 1.00 |              139.05 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4892.94 |                25547.00 |            125000.00 |                             37727.00 | 1.00 |              140.92 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4948.14 |                25262.00 |            125000.00 |                             37855.00 | 1.00 |              142.51 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4860.79 |                25716.00 |            125000.00 |                             37823.00 | 1.00 |              139.99 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4529.48 |                27597.00 |            125000.00 |                             37951.00 | 1.00 |              130.45 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4913.33 |                25441.00 |            125000.00 |                             37791.00 | 1.00 |              141.50 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4723.40 |                26464.00 |            125000.00 |                             37887.00 | 1.00 |              136.03 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4748.88 |                26322.00 |            125000.00 |                             37823.00 | 1.00 |              136.77 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              130.45 |                        38445.08 |                27597.00 |           1000000.00 |                             37835.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65496.46 |               152680.00 |            5000064 |                            3409.00 |              4999936 |                              3379.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65496.46 |               152680.00 |            5000064 |                            3409.00 |              4999936 |                              3379.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       372.30 |     10.66 |           5.52 |                  5.52 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |         0.17 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |      1417.89 |     11.17 |           7.50 |                  7.50 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       715.41 |      4.85 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             1780822.00 |                4.06 |                          22447.59 |                     4.82 |                46756.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             8805442.00 |                4.59 |                          62564.37 |                     3.10 |                 1472.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
