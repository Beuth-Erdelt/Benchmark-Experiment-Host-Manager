## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 785s 
* Code: 1783870690
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
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590804992
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-124-generic
  * node:cl-worker24
  * disk:131929
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:131930
    * cpu_list:0-95
  * sut 1
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:582821
    * cpu_list:0-255
  * sut 2
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:940285
    * cpu_list:0-127
  * pd 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:584532
    * cpu_list:0-255
  * pd 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:163405
    * cpu_list:0-95
  * pd 2
    * RAM:2164173213696
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1090603
    * cpu_list:0-223
  * tikv 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:584050
    * cpu_list:0-255
  * tikv 1
    * RAM:2164173213696
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1091017
    * cpu_list:0-223
  * tikv 2
    * RAM:1081853972480
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-134-generic
    * node:cl-worker37
    * disk:539092
    * cpu_list:0-127
  * eval_parameters
    * code:1783870690
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1783870690-8f5675c8-2n8nf: 0
* bexhoma-sut-tidb-1-1783870690-8f5675c8-bkbsl: 0
* bexhoma-sut-tidb-1-1783870690-8f5675c8-fkrdb: 0
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
| TiDB-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1201.87 |               104005.00 |            125000.00 |                             20943.00 | 1.00 |               34.61 |
| TiDB-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1185.96 |               105400.00 |            125000.00 |                             20511.00 | 1.00 |               34.16 |
| TiDB-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1133.36 |               110292.00 |            125000.00 |                             21759.00 | 1.00 |               32.64 |
| TiDB-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1130.41 |               110579.00 |            125000.00 |                             21903.00 | 1.00 |               32.56 |
| TiDB-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1197.34 |               104398.00 |            125000.00 |                             20991.00 | 1.00 |               34.48 |
| TiDB-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1200.51 |               104122.00 |            125000.00 |                             20879.00 | 1.00 |               34.57 |
| TiDB-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1176.07 |               106286.00 |            125000.00 |                             20831.00 | 1.00 |               33.87 |
| TiDB-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1174.41 |               106436.00 |            125000.00 |                             21183.00 | 1.00 |               33.82 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               32.56 |                         9399.93 |               110579.00 |           1000000.00 |                             21125.00 |

### Execution

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1-1-1-1 | TiDB-1-1-1 | TiDB-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                        10834.35 |                92299.00 |             499501 |                            3455.00 |               500499 |                            158207.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1-1 | TiDB-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                        10834.35 |                92299.00 |             499501 |                            3455.00 |               500499 |                            158207.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       960.01 |      9.91 |           3.09 |                  3.42 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       134.18 |      1.17 |           0.26 |                  0.26 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1129.02 |     11.55 |           6.86 |                 17.00 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       127.87 |      1.89 |           0.45 |                  0.46 |

### Execution phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       739.90 |      9.81 |           1.13 |                  1.47 |

### Execution phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |        70.86 |      1.17 |           0.26 |                  0.26 |

### Execution phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |      1200.20 |     16.34 |           8.36 |                 22.16 |

### Execution phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-1-1-1-1 |       183.76 |      2.21 |           0.15 |                  0.15 |

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
