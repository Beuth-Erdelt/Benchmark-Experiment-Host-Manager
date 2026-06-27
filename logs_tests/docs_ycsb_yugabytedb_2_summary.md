## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 530s 
* Code: 1782462251
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.10.1.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is skipped.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-1-1-1-1 uses docker image postgres:15.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220937
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782462251

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1-1-1-1 | YugabyteDB-1-1-1 | YugabyteDB-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        33938.69 |               294649.00 |            5000255 |                           21535.00 |              4999745 |                             35231.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1-1 | YugabyteDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        33938.69 |               294649.00 |            5000255 |                           21535.00 |              4999745 |                             35231.00 |

### Monitoring

### Execution phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |      9794.97 |     36.50 |          12.85 |                 22.22 |

### Execution phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |        10.31 |      0.10 |           0.25 |                  0.28 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |       522.41 |      2.12 |           0.14 |                  0.14 |

### Tests
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
