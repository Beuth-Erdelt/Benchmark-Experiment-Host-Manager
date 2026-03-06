## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1578s 
    Code: 1772840860
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.1.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-1-1-1024-1 uses docker image pingcap/tidb:v7.1.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:148720
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    sut 1
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    sut 2
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    pd 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:724538
        cpu_list:0-223
    pd 1
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:174949
        cpu_list:0-95
    pd 2
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196808
        cpu_list:0-95
    tikv 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:724539
        cpu_list:0-223
    tikv 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196808
        cpu_list:0-95
    tikv 2
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1334107
        cpu_list:0-255
    eval_parameters
                code:1772840860
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
TiDB-1-1-1024-2 uses docker image pingcap/tidb:v7.1.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:148720
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    sut 0
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    sut 1
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    sut 2
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    pd 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:722552
        cpu_list:0-223
    pd 1
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:174952
        cpu_list:0-95
    pd 2
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196584
        cpu_list:0-95
    tikv 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:722556
        cpu_list:0-223
    tikv 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196585
        cpu_list:0-95
    tikv 2
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1332317
        cpu_list:0-255
    eval_parameters
                code:1772840860
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
TiDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    284.479903                 283.173237         0.0                                                     120500.0                                              56225.0
TiDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    132.453299                 131.119966         0.0                                                     137658.0                                              60372.0
TiDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    134.706630                 133.229964         0.0                                                     136249.0                                              59362.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
TiDB-1-1-1024-1               1         16   16384          1  300.0           0                        284.48                     283.17         0.0                                                     120500.0                                              56225.0
TiDB-1-1-1024-2               1         16   16384          2  300.0           0                        267.16                     264.35         0.0                                                     137658.0                                              59867.0

### Workflow

#### Actual
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
TiDB-1-1-1024-1      245.0        1.0   1.0         235.102041
TiDB-1-1-1024-2      245.0        1.0   2.0         235.102041

### Monitoring

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1599.63     11.2          2.81                 3.07
TiDB-1-1-1024-2     1599.63     11.2          2.81                 3.07

### Loading phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1       76.92     0.36           0.3                  0.3
TiDB-1-1-1024-2       76.92     0.36           0.3                  0.3

### Loading phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1768.17    12.01          9.63                29.16
TiDB-1-1-1024-2     1768.17    12.01          9.63                29.16

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1041.97     9.76          0.38                 0.38
TiDB-1-1-1024-2     1041.97     9.76          0.38                 0.38

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     3394.86    12.09           0.9                 1.15
TiDB-1-1-1024-2     2979.46    11.07           0.9                 1.16

### Execution phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      237.67     0.91          0.31                 0.32
TiDB-1-1-1024-2      231.88     0.92          0.32                 0.32

### Execution phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1289.46     5.25         12.09                31.37
TiDB-1-1-1024-2     1269.16     5.46         13.43                31.93

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      209.87     1.11          0.32                 0.32
TiDB-1-1-1024-2      263.50     0.85          0.32                 0.32

### Application Metrics

#### Loading phase: SUT deployment
                 TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-1-1-1024-1                                 432.95                          19.4
TiDB-1-1-1024-2                                 432.95                          19.4

#### Loading phase: component pd
                 PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-1-1-1024-1                      118                               44
TiDB-1-1-1024-2                      118                               44

#### Loading phase: component tikv
                 TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-1-1-1024-1                 0.18                         68746.15                       13.4                          1.57
TiDB-1-1-1024-2                 0.18                         68746.15                       13.4                          1.57

#### Execution phase: SUT deployment
                 TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-1-1-1024-1                                6799.77                         19.15
TiDB-1-1-1024-2                                4318.23                          3.39

#### Execution phase: component pd
                 PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-1-1-1024-1                      119                               10
TiDB-1-1-1024-2                      122                                0

#### Execution phase: component tikv
                 TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-1-1-1024-1                 0.24                          37575.0                       2.46                          0.73
TiDB-1-1-1024-2                 0.30                          36411.0                       2.77                          0.70

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
