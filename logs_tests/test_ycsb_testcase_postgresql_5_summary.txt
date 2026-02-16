## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 2342s 
    Code: 1749147910
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359249228
    datadisk:2752
    volume_size:50G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749147910
PostgreSQL-64-8-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359249624
    datadisk:2754
    volume_size:50G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749147910

### Execution
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-1024-1               1       64    1024          1           0                        1023.48               977059.0            499742                             690.0              500258                               814.0
PostgreSQL-64-8-1024-2               1       64    1024          8           0                        1023.69               976880.0            500373                             722.0              499627                               852.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-1024 - Pods [[8, 1]]

#### Planned
DBMS PostgreSQL-64-8-1024 - Pods [[1, 8]]

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-1024-1      233.34     0.26          4.05                 5.60
PostgreSQL-64-8-1024-2      220.71     0.24          4.01                 5.58

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-1024-1      229.65     0.35          0.57                 0.57
PostgreSQL-64-8-1024-2      227.59     0.25          2.48                 2.50

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
