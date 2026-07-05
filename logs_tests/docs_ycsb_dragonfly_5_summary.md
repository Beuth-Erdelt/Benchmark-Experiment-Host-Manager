## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 787s 
* Code: 1782827530
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
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
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
  * disk:263492
  * datadisk:1
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
    * disk:596940
    * volume_size:50G
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145308
    * volume_size:50G
    * cpu_list:0-95
  * worker 2
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:685580
    * volume_size:50G
    * cpu_list:0-127
  * eval_parameters
    * code:1782827530
    * BEXHOMA_WORKERS:3
* DragonflyCluster-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266867
  * datadisk:1
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
    * disk:592122
    * datadisk:356
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145453
    * datadisk:386
    * volume_size:50G
    * volume_used:384M
    * cpu_list:0-95
  * worker 2
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:685657
    * datadisk:355
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-127
  * eval_parameters
    * code:1782827530
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1782827530-7876f9c4b6-v6mcg: 0
* bx-w-dragonfly-ycsb-1-0: 0
* bx-w-dragonfly-ycsb-1-1: 0
* bx-w-dragonfly-ycsb-1-2: 0

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
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9203.36 |                13582.00 |            125000.00 |                              2873.00 | 1.00 |              265.06 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8873.43 |                14087.00 |            125000.00 |                              2875.00 | 1.00 |              255.55 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9780.91 |                12780.00 |            125000.00 |                              2819.00 | 1.00 |              281.69 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9202.68 |                13583.00 |            125000.00 |                              2797.00 | 1.00 |              265.04 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9115.44 |                13713.00 |            125000.00 |                              2885.00 | 1.00 |              262.52 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9268.18 |                13487.00 |            125000.00 |                              2925.00 | 1.00 |              266.92 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9049.45 |                13813.00 |            125000.00 |                              2735.00 | 1.00 |              260.62 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9123.42 |                13701.00 |            125000.00 |                              2987.00 | 1.00 |              262.75 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              255.55 |                        73616.86 |                14087.00 |           1000000.00 |                              2862.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-2-1-1-1 | DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1-1 | DragonflyCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64241.75 |               155662.00 |            4998467 |                            2815.00 |              5001533 |                              2787.00 |
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64252.07 |               155637.00 |            4997231 |                            2801.00 |              5002769 |                              2775.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64252.07 |               155637.00 |            4997231 |                            2801.00 |              5002769 |                              2775.00 |
| DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        64241.75 |               155662.00 |            4998467 |                            2815.00 |              5001533 |                              2787.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       146.70 |      4.58 |           1.67 |                  1.67 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |         0.16 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |      1256.92 |      9.07 |           2.37 |                  2.37 |
| DragonflyCluster-1-2-1-1 |      1644.04 |      9.61 |           2.52 |                  3.59 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       651.07 |      5.16 |           0.29 |                  0.29 |
| DragonflyCluster-1-2-1-1 |       651.07 |      5.63 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             1924690.00 |                1.49 |                           8189.88 |                     5.59 |                    0.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             8824841.00 |                1.60 |                          31519.89 |                     3.06 |                    0.00 |
| DragonflyCluster-1-2-1-1 |             9214551.00 |                1.69 |                          32466.51 |                     3.28 |                    0.00 |

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
