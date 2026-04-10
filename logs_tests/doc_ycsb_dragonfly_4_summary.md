## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 741s 
* Code: 1775666829
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
  * disk:150958
  * volume_size:50G
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1775666829
* Dragonfly-64-8-196608-2-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150958
  * datadisk:2190
  * volume_size:50G
  * volume_used:2.2G
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1775666829

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        64312.17 |                16678.00 |           1000000.00 |                              1428.62 |

### Execution

| DBMS                      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65500.32 |               152671.00 |         4999903.00 |                             526.00 |           5000097.00 |                               505.00 |
| Dragonfly-64-8-196608-2-1 |             2.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65500.75 |               152670.00 |         5000211.00 |                             514.00 |           4999789.00 |                               493.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       235.31 |      4.33 |           1.62 |                  1.62 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |      1225.01 |      8.71 |           1.62 |                  1.62 |
| Dragonfly-64-8-196608-2-1 |      1091.10 |      9.61 |           1.73 |                  3.02 |

### Execution phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       386.29 |      4.54 |           0.13 |                  0.13 |
| Dragonfly-64-8-196608-2-1 |       580.84 |      4.53 |           0.13 |                  0.13 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
