## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 779s 
* Code: 1782826724
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
* Dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * volume_size:50G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782826724
* Dragonfly-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * datadisk:2191
  * volume_size:50G
  * volume_used:2.2G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782826724

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1782826724-5c9c9f865b-w7z9w: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Dragonfly-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Dragonfly-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9391.44 |                13310.00 |            125000.00 |                              2515.00 | 1.00 |              270.47 |
| Dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9621.31 |                12992.00 |            125000.00 |                              2525.00 | 1.00 |              277.09 |
| Dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9418.32 |                13272.00 |            125000.00 |                              2487.00 | 1.00 |              271.25 |
| Dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9604.30 |                13015.00 |            125000.00 |                              2503.00 | 1.00 |              276.60 |
| Dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9058.63 |                13799.00 |            125000.00 |                              2791.00 | 1.00 |              260.89 |
| Dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9006.41 |                13879.00 |            125000.00 |                              2709.00 | 1.00 |              259.38 |
| Dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9054.69 |                13805.00 |            125000.00 |                              2485.00 | 1.00 |              260.78 |
| Dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9140.77 |                13675.00 |            125000.00 |                              2707.00 | 1.00 |              263.25 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              259.38 |                        74295.87 |                13879.00 |           1000000.00 |                              2590.25 |

### Execution

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-2-1-1-1 | Dragonfly-1-2-1 | Dragonfly-1-2-1-1 | Dragonfly-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65499.47 |               152673.00 |            4999915 |                            2035.00 |              5000085 |                              1993.00 |
| Dragonfly-1-1-1-1-1 | Dragonfly-1-1-1 | Dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65502.90 |               152665.00 |            4999078 |                            2083.00 |              5000922 |                              2039.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1 | Dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65502.90 |               152665.00 |            4999078 |                            2083.00 |              5000922 |                              2039.00 |
| Dragonfly-1-2-1 | Dragonfly-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65499.47 |               152673.00 |            4999915 |                            2035.00 |              5000085 |                              1993.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       262.30 |      7.26 |           1.69 |                  1.69 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |        14.39 |      0.00 |           0.09 |                  0.10 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |      2176.60 |     15.42 |           1.71 |                  1.71 |
| Dragonfly-1-2-1-1 |      2788.43 |     18.31 |           1.84 |                  2.91 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       677.51 |      4.85 |           0.13 |                  0.13 |
| Dragonfly-1-2-1-1 |       677.51 |      4.85 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             2000000.00 |                1.54 |                           9049.78 |                     5.71 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             8635927.00 |                1.54 |                          30315.84 |                     3.31 |                    0.00 |
| Dragonfly-1-2-1-1 |             9601197.00 |                1.63 |                          33278.43 |                     3.36 |                    0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
