## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1265s 
* Code: 1773430865
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1262462
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773430865
* YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1263692
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773430865

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| YugabyteDB-1-1-1024-1-1 |                1 |          16 |    16384 |        1 |       1 |    300 |            0 |                        475.947 |                     473.847 |            0 |                                                         81863 |                                                 33609 |
| YugabyteDB-1-1-1024-2-1 |                1 |           8 |     8192 |        2 |       1 |    300 |            0 |                        225.253 |                     224.247 |            0 |                                                         94011 |                                                 35505 |
| YugabyteDB-1-1-1024-2-2 |                1 |           8 |     8192 |        2 |       2 |    300 |            0 |                        214.683 |                     213.59  |            0 |                                                         97092 |                                                 37254 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| YugabyteDB-1-1-1024-1 |                1 |          16 |    16384 |           1 |    300 |            0 |                         475.95 |                      473.85 |            0 |                                                         81863 |                                               33609   |
| YugabyteDB-1-1-1024-2 |                1 |          16 |    16384 |           2 |    300 |            0 |                         439.94 |                      437.84 |            0 |                                                         97092 |                                               36379.5 |

### Workflow

#### Actual

* DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

#### Planned

* DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| YugabyteDB-1-1-1024-1 |         102 |           1 |      1 |             564.706 |
| YugabyteDB-1-1-1024-2 |         102 |           1 |      2 |             564.706 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |      2010.86 |     22.68 |           7.39 |                 16.15 |
| YugabyteDB-1-1-1024-2 |      2508.42 |     22.68 |           7.39 |                 16.15 |

### Loading phase: component yb-master

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        17.84 |      0.21 |           0.34 |                  0.38 |
| YugabyteDB-1-1-1024-2 |        24.18 |      0.21 |           0.36 |                  0.4  |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        75.68 |         0 |           0.25 |                  0.26 |
| YugabyteDB-1-1-1024-2 |        75.68 |         0 |           0.25 |                  0.26 |

### Execution phase: component yb-tserver

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |     10821.6  |     39.06 |          10.15 |                 20.45 |
| YugabyteDB-1-1-1024-2 |      9532.47 |     36.81 |          11.15 |                 22.77 |

### Execution phase: component yb-master

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        13.01 |      0.07 |           0.39 |                  0.43 |
| YugabyteDB-1-1-1024-2 |        17.1  |      0.08 |           0.45 |                  0.49 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |       102.58 |      0.52 |            0.3 |                   0.3 |
| YugabyteDB-1-1-1024-2 |        92.67 |      0.98 |            0.3 |                   0.3 |

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS                  |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:----------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-1-1-1024-1 |                          243.83 |                       0.44 |                       26.87 |                         0 |                         856 |
| YugabyteDB-1-1-1024-2 |                         3048.64 |                       0.44 |                       26.87 |                         0 |                         856 |

#### Loading phase: component yb-master

| DBMS                  |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:----------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-1-1-1024-1 |                               3.05 |                            22.47 |                                0.04 |             5.00068e+08 |                               3.01 |
| YugabyteDB-1-1-1024-2 |                               3.05 |                            22.47 |                                0.04 |             5.00234e+08 |                               3.01 |

#### Execution phase: component yb-tserver

| DBMS                  |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:----------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-1-1-1024-1 |                        16629.5  |                       0.28 |                       11.22 |                         0 |                         599 |
| YugabyteDB-1-1-1024-2 |                         7310.32 |                       0.31 |                        1.19 |                         0 |                         612 |

#### Execution phase: component yb-master

| DBMS                  |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:----------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-1-1-1024-1 |                               3.02 |                             0.44 |                                0.03 |             5.00262e+08 |                               2.99 |
| YugabyteDB-1-1-1024-2 |                               1.11 |                             0.32 |                                0    |             5.01112e+08 |                               1.11 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
