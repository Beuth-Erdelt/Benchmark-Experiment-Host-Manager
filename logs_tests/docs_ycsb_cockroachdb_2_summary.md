## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 3100s 
* Code: 1782146495
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219926
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1337485
    * datadisk:705151
    * volume_size:50G
    * volume_used:1.9G
    * cpu_list:0-255
  * worker 1
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:838172
    * datadisk:704969
    * volume_size:50G
    * volume_used:1.7G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643622
    * datadisk:705029
    * volume_size:50G
    * volume_used:1.7G
    * cpu_list:0-127
  * eval_parameters
    * code:1782146495
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219926
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1337491
    * datadisk:705243
    * volume_size:50G
    * volume_used:2.0G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643621
    * datadisk:705242
    * volume_size:50G
    * volume_used:2.0G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:836553
    * datadisk:705245
    * volume_size:50G
    * volume_used:2.0G
    * cpu_list:0-223
  * worker 3
    * node:cl-worker24
  * eval_parameters
    * code:1782146495
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.83 |               786985.00 |            125000.00 |                            199423.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.66 |               787852.00 |            125000.00 |                            198015.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.92 |               786557.00 |            125000.00 |                            199551.00 | 1.00 |                4.58 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.93 |               786502.00 |            125000.00 |                            199167.00 | 1.00 |                4.58 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.91 |               786585.00 |            125000.00 |                            199295.00 | 1.00 |                4.58 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.81 |               787120.00 |            125000.00 |                            197631.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.64 |               787964.00 |            125000.00 |                            199295.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.85 |               786914.00 |            125000.00 |                            198527.00 | 1.00 |                4.57 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |                4.57 |                         1270.55 |               787964.00 |           1000000.00 |                            198863.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-2-1-1-1 | CockroachDB-1-2-1 | CockroachDB-1-2-1-1 | CockroachDB-1   |                2 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         1269.24 |               787875.00 |             499716 |                           94335.00 |               500284 |                           1576959.00 |
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         1319.68 |               757760.00 |             499571 |                           77887.00 |               500429 |                           1323007.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         1319.68 |               757760.00 |             499571 |                           77887.00 |               500429 |                           1323007.00 |
| CockroachDB-1-2-1 | CockroachDB-1-2-1 |                2 |        64 |    65536 |               1 |           1 |            0 |                         1269.24 |               787875.00 |             499716 |                           94335.00 |               500284 |                           1576959.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     26330.71 |      2.92 |          10.06 |                 23.12 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       142.20 |      0.75 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      3075.07 |      5.85 |           6.88 |                 13.17 |
| CockroachDB-1-2-1-1 |      3674.46 |      5.52 |           6.46 |                 12.35 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |        96.00 |      0.38 |           0.13 |                  0.14 |
| CockroachDB-1-2-1-1 |        95.74 |      0.16 |           0.13 |                  0.13 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
