## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 933s 
    Code: 1772643308
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
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Redis-64-8-196608-1-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147524
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:723489
        volume_size:50G
        volume_used:712M
        cpu_list:0-223
    worker 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:337636
        volume_size:50G
        volume_used:792M
        cpu_list:0-55
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1271182
        volume_size:50G
        volume_used:712M
        cpu_list:0-255
    eval_parameters
        code:1772643308
        BEXHOMA_WORKERS:3
Redis-64-8-196608-2-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147524
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:723493
        volume_size:50G
        volume_used:708M
        cpu_list:0-223
    worker 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:337627
        volume_size:50G
        volume_used:768M
        cpu_list:0-55
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1271183
        volume_size:50G
        volume_used:708M
        cpu_list:0-255
    eval_parameters
        code:1772643308
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   24377.495716                41267.0             1000000                              5870.5

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1-1               1      128   65536          1           0                       64127.23               155940.0           4998350                            5487.0             5001650                              5479.0
Redis-64-8-196608-2-1               2      128   65536          1           0                       64207.52               155745.0           4997822                            5755.0             5002178                              5723.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1], [1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1], [1]]

### Monitoring

### Loading phase: component worker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1       83.06     1.17          1.71                 1.72

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1        0.15        0           0.0                  0.0

### Execution phase: component worker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      240.74     2.28          1.81                 1.81
Redis-64-8-196608-2-1      426.51     2.33          2.12                 2.14

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      643.24     4.77          0.29                 0.29
Redis-64-8-196608-2-1      578.85     4.81          0.29                 0.29

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
