## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1093s 
    Code: 1764160713
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
    Experiment uses bexhoma version 0.8.16.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 8 processes (pods).
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-64-8-16384-1 uses docker image pingcap/tidb:v7.1.0
    RAM:540579323904
    CPU:AMD EPYC 7502 32-Core Processor
    Cores:128
    host:6.8.0-86-generic
    node:cl-worker22
    disk:406027
    cpu_list:0-127
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:540579323904
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker22
        disk:406027
        cpu_list:0-127
    sut 1
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:636776
        cpu_list:0-223
    sut 2
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1395819
        cpu_list:0-127
    pd 0
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:636776
        cpu_list:0-223
    pd 1
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1395819
        cpu_list:0-127
    pd 2
        RAM:1081965486080
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1364527
        cpu_list:0-255
    tikv 0
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:636776
        cpu_list:0-223
    tikv 1
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1383303
        cpu_list:0-255
    tikv 2
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1395819
        cpu_list:0-127
    eval_parameters
        code:1764160713
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
TiDB-64-8-16384               1       64   16384          8           0                    5962.066718               172852.0             1000000                             68887.0

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
TiDB-64-8-16384-1               1       64   16384          1           0                        5963.81               167678.0            500309                            4679.0              499691                            419583.0

### Workflow

#### Actual
DBMS TiDB-64-8-16384 - Pods [[1]]

#### Planned
DBMS TiDB-64-8-16384 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      906.69     5.02          1.15                 1.92

### Loading phase: component pd
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       69.18     0.35          0.26                 0.26

### Loading phase: component tikv
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      670.99     3.77          5.44                15.54

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       83.13     0.46          0.23                 0.23

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      843.71     5.93          1.12                 1.92

### Execution phase: component pd
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       56.87     0.41          0.26                 0.26

### Execution phase: component tikv
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      809.25     5.78          7.24                21.34

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       77.05     0.46          0.14                 0.14

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
