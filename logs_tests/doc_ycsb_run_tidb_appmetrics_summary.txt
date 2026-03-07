## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 648s 
    Code: 1772837896
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.9.1.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 8 processes (pods).
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-64-8-16384-1 uses docker image pingcap/tidb:v7.1.0
    RAM:540590821376
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:6.8.0-90-generic
    node:cl-worker24
    disk:175121
    cpu_list:0-95
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:175122
        cpu_list:0-95
    sut 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1192219
        cpu_list:0-95
    sut 2
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:721213
        cpu_list:0-223
    pd 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:721211
        cpu_list:0-223
    pd 1
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1309450
        cpu_list:0-255
    pd 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:428729
        cpu_list:0-127
    tikv 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:721212
        cpu_list:0-223
    tikv 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1192219
        cpu_list:0-95
    tikv 2
        RAM:1081853952000
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:426855
        cpu_list:0-127
    eval_parameters
        code:1772837896
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
TiDB-64-8-16384               1       64   16384          8           0                   16024.089766                63199.0             1000000                              8425.5

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
TiDB-64-8-16384-1               1       64   16384          1           0                       11916.39                83918.0            499154                            2733.0              500846                            185087.0

### Workflow

#### Actual
DBMS TiDB-64-8-16384 - Pods [[1]]

#### Planned
DBMS TiDB-64-8-16384 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      795.75     9.67          1.93                 2.83

### Loading phase: component pd
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       62.47     0.79          0.35                 0.35

### Loading phase: component tikv
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      356.89     4.71          5.87                15.66

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       24.91        0          0.13                 0.14

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       409.9     6.99          1.09                  2.0

### Execution phase: component pd
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       55.86     0.68          0.35                 0.35

### Execution phase: component tikv
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      398.44     5.65          7.41                20.36

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       17.97        0          0.16                 0.18

### Application Metrics

#### Loading phase: SUT deployment
                   TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-64-8-16384-1                                3883.41                          3.42

#### Loading phase: component pd
                   PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-64-8-16384-1                       63                                6

#### Loading phase: component tikv
                   TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-64-8-16384-1                 0.16                         99786340                       7.16                          1.44

#### Execution phase: SUT deployment
                   TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-64-8-16384-1                                 885.44                          4.09

#### Execution phase: component pd
                   PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-64-8-16384-1                       70                                2

#### Execution phase: component tikv
                   TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-64-8-16384-1                 0.21                                0                       0.22                          0.95

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
