## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 826s 
* Code: 1783892810
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
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590841856
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-117-generic
  * node:cl-worker25
  * disk:170557
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:170609
    * cpu_list:0-95
  * sut 1
    * RAM:540597907456
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:320592
    * cpu_list:0-255
  * sut 2
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:592162
    * cpu_list:0-255
  * pd 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:597940
    * cpu_list:0-255
  * pd 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:133836
    * cpu_list:0-95
  * pd 2
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:170647
    * cpu_list:0-95
  * tikv 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:592155
    * cpu_list:0-255
  * tikv 1
    * RAM:1077381287936
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1392000
    * cpu_list:0-255
  * tikv 2
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:170586
    * cpu_list:0-95
  * eval_parameters
    * code:1783892810
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1783892810-6749979d78-jp74c: 0
* bexhoma-sut-tidb-1-1783892810-6749979d78-lh57n: 0
* bexhoma-sut-tidb-1-1783892810-6749979d78-sq9bz: 0
* bexhoma-pd-tidb-ycsb-1-0: 0
* bexhoma-pd-tidb-ycsb-1-1: 0
* bexhoma-pd-tidb-ycsb-1-2: 0
* bexhoma-tikv-tidb-ycsb-1-0: 0
* bexhoma-tikv-tidb-ycsb-1-1: 0
* bexhoma-tikv-tidb-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| TiDB-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          706.97 |               176810.00 |            125000.00 |                             78911.00 | 1.00 |               20.36 |
| TiDB-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          707.59 |               176655.00 |            125000.00 |                             77823.00 | 1.00 |               20.38 |
| TiDB-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          707.37 |               176712.00 |            125000.00 |                             80255.00 | 1.00 |               20.37 |
| TiDB-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          706.94 |               176818.00 |            125000.00 |                             79615.00 | 1.00 |               20.36 |
| TiDB-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          720.36 |               173524.00 |            125000.00 |                             77439.00 | 1.00 |               20.75 |
| TiDB-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          708.83 |               176346.00 |            125000.00 |                             78975.00 | 1.00 |               20.41 |
| TiDB-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          707.69 |               176632.00 |            125000.00 |                             78463.00 | 1.00 |               20.38 |
| TiDB-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                          710.32 |               175978.00 |            125000.00 |                             77887.00 | 1.00 |               20.46 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               20.36 |                         5676.07 |               176818.00 |           1000000.00 |                             78671.00 |

### Execution

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1-1-1-1 | TiDB-1-1-1 | TiDB-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                         4162.68 |               240230.00 |             500772 |                            7891.00 |               499228 |                            331519.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1-1 | TiDB-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                         4162.68 |               240230.00 |             500772 |                            7891.00 |               499228 |                            331519.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1208.31 |      8.29 |           2.88 |                  3.22 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       122.25 |      0.85 |           0.28 |                  0.28 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1184.00 |      8.60 |           7.03 |                 17.83 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       120.75 |      0.89 |           0.23 |                  0.23 |

### Execution phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1146.49 |      8.73 |           1.28 |                  1.63 |

### Execution phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       136.37 |      0.93 |           0.27 |                  0.27 |

### Execution phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1332.57 |      9.86 |           9.05 |                 22.55 |

### Execution phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |        85.94 |      0.75 |           0.14 |                  0.14 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration [ms] |
|:-------------|----------------------------------------:|-------------------------------:|
| TiDB-1-1-1-1 |                                 3446.56 |                          10.77 |

#### Loading phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [ops] |
|:-------------|--------------------------:|----------------------------------:|
| TiDB-1-1-1-1 |                     64.00 |                             12.00 |

#### Loading phase: component tikv

| DBMS         |   TiKV Store Used [%] |   TiKV Compaction Time Median [s] |   TiKV Compaction Flow [Gi] |   TiKV Compaction Pending [Gi] |
|:-------------|----------------------:|----------------------------------:|----------------------------:|-------------------------------:|
| TiDB-1-1-1-1 |                  0.18 |                      104429564.00 |                        6.22 |                           1.44 |

#### Execution phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration [ms] |
|:-------------|----------------------------------------:|-------------------------------:|
| TiDB-1-1-1-1 |                                 1553.79 |                          12.37 |

#### Execution phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [ops] |
|:-------------|--------------------------:|----------------------------------:|
| TiDB-1-1-1-1 |                     70.00 |                              0.00 |

#### Execution phase: component tikv

| DBMS         |   TiKV Store Used [%] |   TiKV Compaction Time Median [s] |   TiKV Compaction Flow [Gi] |   TiKV Compaction Pending [Gi] |
|:-------------|----------------------:|----------------------------------:|----------------------------:|-------------------------------:|
| TiDB-1-1-1-1 |                  0.26 |                       56219681.00 |                        2.26 |                           1.42 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
