## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 976s 
* Code: 1781949630
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
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* DragonflyCluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214909
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1344408
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1416354
    * cpu_list:0-255
  * worker 2
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:306121
    * cpu_list:0-55
  * eval_parameters
    * code:1781949630
    * BEXHOMA_WORKERS:3
* DragonflyCluster-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214909
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1416324
    * cpu_list:0-255
  * worker 1
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:306122
    * cpu_list:0-55
  * worker 2
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1325025
    * cpu_list:0-223
  * eval_parameters
    * code:1781949630
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8567.51 |                14590.00 |            125000.00 |                              3641.00 | 1.00 |              246.74 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8138.02 |                15360.00 |            125000.00 |                              3619.00 | 1.00 |              234.38 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7978.55 |                15667.00 |            125000.00 |                              3643.00 | 1.00 |              229.78 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8039.62 |                15548.00 |            125000.00 |                              3969.00 | 1.00 |              231.54 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8938.79 |                13984.00 |            125000.00 |                              3293.00 | 1.00 |              257.44 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8536.50 |                14643.00 |            125000.00 |                              3753.00 | 1.00 |              245.85 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8782.41 |                14233.00 |            125000.00 |                              3747.00 | 1.00 |              252.93 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8407.88 |                14867.00 |            125000.00 |                              3991.00 | 1.00 |              242.15 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              229.78 |                        67389.29 |                15667.00 |           1000000.00 |                              3707.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64652.94 |               154672.00 |            4996223 |                            1054.00 |              5003777 |                              1023.00 |
| DragonflyCluster-1-2-1-1-1 | DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1-1 | DragonflyCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64602.82 |               154792.00 |            5001172 |                            2549.00 |              4998828 |                              2513.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64652.94 |               154672.00 |            4996223 |                            1054.00 |              5003777 |                              1023.00 |
| DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        64602.82 |               154792.00 |            5001172 |                            2549.00 |              4998828 |                              2513.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       140.77 |      4.14 |           1.63 |                  1.63 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |        15.19 |      0.00 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       682.13 |      4.90 |           1.64 |                  1.64 |
| DragonflyCluster-1-2-1-1 |       796.22 |      5.27 |           1.78 |                  2.85 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       694.90 |      5.57 |           0.29 |                  0.29 |
| DragonflyCluster-1-2-1-1 |       682.41 |      7.07 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             2001604.00 |                1.52 |                          10984.24 |                     6.17 |                    0.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             9166322.00 |                1.52 |                          27099.77 |                     3.43 |                    0.00 |
| DragonflyCluster-1-2-1-1 |             8597893.00 |                1.62 |                          31789.52 |                     3.21 |                    0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
