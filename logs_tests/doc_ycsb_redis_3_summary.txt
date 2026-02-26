## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 414s 
    Code: 1769094442
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:94800
    datadisk:1
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:384581
        datadisk:717
        cpu_list:0-127
    worker 1
        RAM:540492902400
        CPU:Intel(R) Xeon(R) Gold 6430
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker38
        disk:250672
        datadisk:795
        cpu_list:0-127
    worker 2
        RAM:1081853980672
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:397176
        datadisk:716
        cpu_list:0-127
    worker 3
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:145224
        datadisk:710
        cpu_list:0-95
    worker 4
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:638453
        datadisk:721
        cpu_list:0-223
    worker 5
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:200821
        datadisk:797
        cpu_list:0-95
    worker 6
        node:cl-worker22
    eval_parameters
        code:1769094442
        BEXHOMA_REPLICAS:1
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   36836.051418                27372.0             1000000                             3403.75

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       60827.99               164398.0           5007774                            1383.0             4992226                              1352.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       96.15     3.15          2.65                 2.69

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1           0        0           0.0                  0.0

### Execution phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      425.05     3.29          3.78                 3.79

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      693.18     4.81           0.3                  0.3

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
