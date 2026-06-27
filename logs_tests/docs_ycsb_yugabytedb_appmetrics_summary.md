## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 950s 
* Code: 1773432301
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
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1294649
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773432301

### Loading

| DBMS                  |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-64-8-65536 |                1 |        64 |    65536 |           8 |            0 |                         19489.3 |                   52544 |                1e+06 |                                 8961 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-64-8-65536-1 |                1 |        64 |    65536 |           1 |            0 |                         34422.5 |                  290508 |        5.00119e+06 |                               7643 |          4.99881e+06 |                                43583 |

### Workflow

#### Actual

* DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned

* DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |      1234.82 |     13.47 |            5.6 |                  13.6 |

### Loading phase: component yb-master

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |         6.87 |      0.04 |           0.24 |                  0.26 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |        38.93 |         0 |           0.11 |                  0.11 |

### Execution phase: component yb-tserver

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |      10378.5 |     39.73 |           9.51 |                 20.76 |

### Execution phase: component yb-master

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |        10.69 |      0.06 |           0.26 |                  0.29 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |       319.68 |      1.25 |           0.14 |                  0.14 |

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS                    |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:------------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-64-8-65536-1 |                         3754.31 |                       0.42 |                        7.06 |                         0 |                         617 |

#### Loading phase: component yb-master

| DBMS                    |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:------------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-64-8-65536-1 |                               0.02 |                             0.54 |                                   0 |               5.017e+08 |                               0.02 |

#### Execution phase: component yb-tserver

| DBMS                    |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:------------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-64-8-65536-1 |                         31676.4 |                       0.67 |                        2.47 |                         0 |                         585 |

#### Execution phase: component yb-master

| DBMS                    |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:------------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-64-8-65536-1 |                               0.01 |                             0.52 |                                   0 |             5.01948e+08 |                               0.01 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
