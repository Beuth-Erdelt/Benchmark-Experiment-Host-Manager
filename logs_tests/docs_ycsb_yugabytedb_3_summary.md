## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1131s 
* Code: 1792432953
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
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.7.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker39.
  * Benchmarking is fixed to cl-worker39.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:942085
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:638901
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:331813
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:942087
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:638903
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:942457
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:331974
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792432953

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1792432953-64656d84fb-2fvdn: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2357.20 |                53029.00 |            125000.00 |                             15439.00 | 1.00 |               67.89 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2409.31 |                51882.00 |            125000.00 |                             15495.00 | 1.00 |               69.39 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2423.14 |                51586.00 |            125000.00 |                             15495.00 | 1.00 |               69.79 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2203.85 |                56719.00 |            125000.00 |                             15583.00 | 1.00 |               63.47 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2220.25 |                56300.00 |            125000.00 |                             15551.00 | 1.00 |               63.94 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2279.48 |                54837.00 |            125000.00 |                             15599.00 | 1.00 |               65.65 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2269.34 |                55082.00 |            125000.00 |                             15343.00 | 1.00 |               65.36 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2415.41 |                51751.00 |            125000.00 |                             15367.00 | 1.00 |               69.56 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               63.47 |                        18577.99 |                56719.00 |           1000000.00 |                             15484.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        19315.95 |               517707.00 |            5001221 |                           40511.00 |              4998779 |                             45919.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        19315.95 |               517707.00 |            5001221 |                           40511.00 |              4998779 |                             45919.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1734.89 |     34.31 |           5.73 |                 13.40 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         9.29 |      0.08 |           0.22 |                  0.25 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       117.96 |      3.18 |           0.15 |                  0.15 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     18244.78 |     38.11 |           9.88 |                 21.24 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        23.68 |      0.14 |           0.24 |                  0.27 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1074.26 |      2.55 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
