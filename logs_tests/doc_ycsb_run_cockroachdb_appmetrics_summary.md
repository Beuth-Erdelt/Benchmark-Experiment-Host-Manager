## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1712s 
* Code: 1773412876
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:541008474112
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147852
  * cpu_list:0-63
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173209600
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1231409
    * volume_size:1000G
    * volume_used:604G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:481230
    * volume_size:1000G
    * volume_used:604G
    * cpu_list:0-127
  * worker 2
    * RAM:1081965416448
    * Cores:256
    * host:5.15.0-1093-nvidia
    * node:cl-worker27
    * disk:1140135
    * volume_size:1000G
    * volume_used:604G
    * cpu_list:0-255
  * eval_parameters
    * code:1773412876
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                   |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-64-8-65536 |                1 |        64 |    65536 |           8 |            0 |                         20154.1 |                  497161 |                1e+07 |                                11618 |

### Execution

| DBMS                     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-64-8-65536-1 |                1 |        64 |    65536 |           1 |            0 |                         16970.5 |                  589257 |        5.00112e+06 |                               4987 |          4.99888e+06 |                               107583 |

### Workflow

#### Actual

* DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned

* DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-64-8-65536-1 |      15646.4 |     34.83 |          20.68 |                 55.46 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-64-8-65536-1 |       764.58 |      1.88 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-64-8-65536-1 |      18040.8 |     34.44 |          21.87 |                 62.12 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-64-8-65536-1 |       557.24 |      1.01 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:-------------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-64-8-65536-1 |                                     70196.8 |                   5.81254e+07 |                                       0 |                                         0 |                                 0 |

#### Execution phase: component worker

| DBMS                     |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:-------------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-64-8-65536-1 |                                     33441.2 |                   2.26026e+07 |                                       0 |                                         0 |                                 0 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
