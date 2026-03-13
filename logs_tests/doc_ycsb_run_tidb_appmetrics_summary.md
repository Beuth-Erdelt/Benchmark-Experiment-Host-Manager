## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 953s 
* Code: 1773414636
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-64-8-16384-1 uses docker image pingcap/tidb:v7.1.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-90-generic
  * node:cl-worker37
  * disk:470827
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:470827
    * cpu_list:0-127
  * sut 1
    * RAM:540579303424
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-94-generic
    * node:cl-worker22
    * disk:387018
    * cpu_list:0-127
  * sut 2
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1241159
    * cpu_list:0-223
  * pd 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1241156
    * cpu_list:0-223
  * pd 1
    * RAM:1081649823744
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-90-generic
    * node:cl-worker34
    * disk:305321
    * cpu_list:0-55
  * pd 2
    * RAM:1081965416448
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:5.15.0-1093-nvidia
    * node:cl-worker27
    * disk:1128780
    * cpu_list:0-255
  * tikv 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1241157
    * cpu_list:0-223
  * tikv 1
    * RAM:540579303424
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-94-generic
    * node:cl-worker22
    * disk:387015
    * cpu_list:0-127
  * tikv 2
    * RAM:1081742741504
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-100-generic
    * node:cl-worker29
    * disk:650970
    * cpu_list:0-127
  * eval_parameters
    * code:1773414636
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Loading

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-64-8-16384 |                1 |        64 |    16384 |           8 |            0 |                         11763.4 |                   85889 |                1e+06 |                                16502 |

### Execution

| DBMS              |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-64-8-16384-1 |                1 |        64 |    16384 |           1 |            0 |                         9747.73 |                  102588 |             500646 |                               3283 |               499354 |                               215551 |

### Workflow

#### Actual

* DBMS TiDB-64-8-16384 - Pods [[1]]

#### Planned

* DBMS TiDB-64-8-16384 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       888.77 |      8.86 |           4.96 |                  5.85 |

### Loading phase: component pd

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        72.65 |      0.56 |           0.28 |                  0.28 |

### Loading phase: component tikv

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       561.69 |      6.14 |            5.5 |                 15.89 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        63.49 |         0 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       448.05 |         7 |           1.45 |                  2.35 |

### Execution phase: component pd

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        61.95 |      0.61 |           0.28 |                  0.28 |

### Execution phase: component tikv

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       473.72 |      7.09 |           6.74 |                 19.26 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        34.04 |         0 |           0.14 |                  0.14 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration [ms] |
|:------------------|----------------------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                                  4023.6 |                           4.77 |

#### Loading phase: component pd

| DBMS              |   PD Cluster Leader Count |   PD Leader Balance Actions [ops] |
|:------------------|--------------------------:|----------------------------------:|
| TiDB-64-8-16384-1 |                        64 |                                14 |

#### Loading phase: component tikv

| DBMS              |   TiKV Store Used [%] |   TiKV Compaction Time Median [s] |   TiKV Compaction Flow [Gi] |   TiKV Compaction Pending [Gi] |
|:------------------|----------------------:|----------------------------------:|----------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                  0.18 |                       9.44679e+07 |                        7.19 |                           1.43 |

#### Execution phase: SUT deployment

| DBMS              |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration [ms] |
|:------------------|----------------------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                                 3330.06 |                           5.37 |

#### Execution phase: component pd

| DBMS              |   PD Cluster Leader Count |   PD Leader Balance Actions [ops] |
|:------------------|--------------------------:|----------------------------------:|
| TiDB-64-8-16384-1 |                        69 |                                 6 |

#### Execution phase: component tikv

| DBMS              |   TiKV Store Used [%] |   TiKV Compaction Time Median [s] |   TiKV Compaction Flow [Gi] |   TiKV Compaction Pending [Gi] |
|:------------------|----------------------:|----------------------------------:|----------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                  0.22 |                                 0 |                        0.35 |                           0.95 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
