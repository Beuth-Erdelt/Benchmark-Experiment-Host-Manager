## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 921s 
* Code: 1782492751
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
  * Database is persisted to disk of type shared and size 1Gi.
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
  * disk:220972
  * volume_size:1.0G
  * volume_used:36M
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782492751

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1782492751-69c78d6c97-2bztt: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| YugabyteDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2284.06 |                54727.00 |            125000.00 |                              9559.00 | 1.00 |               65.78 |
| YugabyteDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2268.23 |                55109.00 |            125000.00 |                              9551.00 | 1.00 |               65.33 |
| YugabyteDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2285.44 |                54694.00 |            125000.00 |                              9631.00 | 1.00 |               65.82 |
| YugabyteDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2284.69 |                54712.00 |            125000.00 |                              9607.00 | 1.00 |               65.80 |
| YugabyteDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2270.79 |                55047.00 |            125000.00 |                              9543.00 | 1.00 |               65.40 |
| YugabyteDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2290.01 |                54585.00 |            125000.00 |                              9599.00 | 1.00 |               65.95 |
| YugabyteDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2281.65 |                54785.00 |            125000.00 |                              9535.00 | 1.00 |               65.71 |
| YugabyteDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2261.50 |                55273.00 |            125000.00 |                              9463.00 | 1.00 |               65.13 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               65.13 |                        18226.37 |                55273.00 |           1000000.00 |                              9561.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1-1-1-1 | YugabyteDB-1-1-1 | YugabyteDB-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        23516.63 |               425231.00 |            4998881 |                           42207.00 |              5001119 |                             52703.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1-1 | YugabyteDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        23516.63 |               425231.00 |            4998881 |                           42207.00 |              5001119 |                             52703.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |      1257.44 |     21.68 |           6.19 |                 13.75 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |         4.97 |      0.04 |           0.22 |                  0.24 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |        88.05 |      1.52 |           0.11 |                  0.11 |

### Execution phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |     12160.06 |     30.42 |          11.91 |                 23.72 |

### Execution phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |        13.15 |      0.07 |           0.23 |                  0.26 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1-1 |       536.50 |      1.70 |           0.14 |                  0.14 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
