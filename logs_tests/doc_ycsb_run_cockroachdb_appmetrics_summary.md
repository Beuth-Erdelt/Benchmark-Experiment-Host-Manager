## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 2239s 
* Code: 1780041245
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
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540590825472
  * Cores:96
  * host:6.8.0-117-generic
  * node:cl-worker23
  * disk:1324145
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590825472
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker23
    * disk:1324145
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-95
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:263973
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-55
  * worker 2
    * RAM:1077382602752
    * Cores:256
    * host:6.8.0-1052-nvidia
    * node:cl-worker28
    * disk:313107
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-255
  * eval_parameters
    * code:1780041245
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Pods [[1]]

#### Planned

* DBMS CockroachDB-1 - Pods [[1]]

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-0-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1687.69 |               740659.00 |           1250000.00 |                             12191.00 |
| CockroachDB-1-1-0-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1682.27 |               743045.00 |           1250000.00 |                             12175.00 |
| CockroachDB-1-1-0-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1645.89 |               759469.00 |           1250000.00 |                             12375.00 |
| CockroachDB-1-1-0-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1651.82 |               756741.00 |           1250000.00 |                             12143.00 |
| CockroachDB-1-1-0-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1653.75 |               755858.00 |           1250000.00 |                             12183.00 |
| CockroachDB-1-1-0-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1638.98 |               762670.00 |           1250000.00 |                             12359.00 |
| CockroachDB-1-1-0-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1658.17 |               753844.00 |           1250000.00 |                             12311.00 |
| CockroachDB-1-1-0-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1643.35 |               760640.00 |           1250000.00 |                             12103.00 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 |                        13261.91 |               762670.00 |          10000000.00 |                             12230.00 |

### Execution

#### Per Connection

| DBMS                | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |       1 |        64 |    65536 |           1 |            0 |                         9596.38 |              1042060.00 |            5003662 |                            7483.00 |              4996338 |                            220287.00 |

#### Per Phase

| DBMS              |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 |             1.00 |     64.00 | 65536.00 |        1.00 |         0.00 |                         9596.38 |              1042060.00 |         5003662.00 |                            7483.00 |           4996338.00 |                            220287.00 |

### Monitoring

### Loading phase: component worker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1 |     19566.81 |     30.76 |          20.52 |                 61.28 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1 |       566.45 |      1.12 |           0.26 |                  0.28 |

### Execution phase: component worker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1 |     22633.04 |     25.24 |          24.40 |                 70.21 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1 |       476.27 |      0.60 |           0.13 |                  0.14 |

### Application Metrics

#### Loading phase: component worker

| DBMS              |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1 |                                    47905.56 |                   37968837.01 |                                    0.00 |                                      0.00 |                              0.00 |

#### Execution phase: component worker

| DBMS              |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1 |                                    10882.44 |                    8363784.03 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
