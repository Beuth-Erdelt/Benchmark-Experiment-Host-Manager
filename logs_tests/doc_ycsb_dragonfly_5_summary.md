## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 843s 
* Code: 1774039821
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
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* Dragonfly-64-8-196608-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150080
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:537328
    * volume_size:50G
    * cpu_list:0-223
  * worker 1
    * RAM:540579303424
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-94-generic
    * node:cl-worker22
    * disk:416917
    * volume_size:50G
    * cpu_list:0-127
  * worker 2
    * RAM:540590817280
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-90-generic
    * node:cl-worker23
    * disk:1243305
    * volume_size:50G
    * cpu_list:0-95
  * eval_parameters
    * code:1774039821
    * BEXHOMA_WORKERS:3
* Dragonfly-64-8-196608-2-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150080
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:537321
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-223
  * worker 1
    * RAM:540579303424
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-94-generic
    * node:cl-worker22
    * disk:416920
    * volume_size:50G
    * volume_used:384M
    * cpu_list:0-127
  * worker 2
    * RAM:540590817280
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-90-generic
    * node:cl-worker23
    * disk:1243305
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-95
  * eval_parameters
    * code:1774039821
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        90055.09 |                11444.00 |           1000000.00 |                              1290.75 |

### Execution

| DBMS                      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        64119.42 |               155959.00 |         5001552.00 |                             428.00 |           4998448.00 |                               416.00 |
| Dragonfly-64-8-196608-2-1 |             2.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        64179.50 |               155813.00 |         5001881.00 |                             430.00 |           4998119.00 |                               418.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

### Monitoring

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |        97.49 |      1.46 |           1.14 |                  1.14 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |         0.15 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       582.63 |      4.58 |           1.64 |                  1.64 |
| Dragonfly-64-8-196608-2-1 |       844.10 |      4.63 |           1.74 |                  2.81 |

### Execution phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       558.94 |      4.88 |           0.29 |                  0.29 |
| Dragonfly-64-8-196608-2-1 |       655.12 |      4.85 |           0.29 |                  0.29 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
