## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 2230s 
* Code: 1781474280
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
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:206042
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1359213
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-255
  * worker 1
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1200034
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-223
  * worker 2
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:316911
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-55
  * eval_parameters
    * code:1781474280
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Pods [[1]]

#### Planned

* DBMS CockroachDB-1 - Pods [[1]]

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1446.67 |               864055.00 |           1250000.00 |                             43007.00 | 10.00 |               41.66 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1442.77 |               866390.00 |           1250000.00 |                             43295.00 | 10.00 |               41.55 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1443.44 |               865985.00 |           1250000.00 |                             43135.00 | 10.00 |               41.57 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1445.62 |               864680.00 |           1250000.00 |                             43327.00 | 10.00 |               41.63 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1443.89 |               865715.00 |           1250000.00 |                             42943.00 | 10.00 |               41.58 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1444.84 |               865145.00 |           1250000.00 |                             43039.00 | 10.00 |               41.61 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1444.33 |               865456.00 |           1250000.00 |                             43071.00 | 10.00 |               41.60 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1446.08 |               864408.00 |           1250000.00 |                             42783.00 | 10.00 |               41.65 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               41.55 |                        11557.64 |               866390.00 |          10000000.00 |                             43075.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        10418.33 |               959847.00 |            5001013 |                            6927.00 |              4998987 |                            171263.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        10418.33 |               959847.00 |            5001013 |                            6927.00 |              4998987 |                            171263.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     16674.48 |     24.42 |          20.29 |                 58.18 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       876.34 |      1.87 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     18702.37 |     23.36 |          23.10 |                 66.41 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       689.93 |      0.86 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    43198.22 |                   34637133.52 |                                    0.00 |                                      0.00 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    11465.09 |                    9130677.66 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
