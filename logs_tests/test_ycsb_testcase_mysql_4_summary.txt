## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1470s 
    Code: 1749000927
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'E'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-64-8-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332181224
    datadisk:22864
    volume_size:50G
    volume_used:23G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749000927

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)  [INSERT-FAILED].Operations  [INSERT-FAILED].99thPercentileLatency(us)
MySQL-64-8-1024-1               1       64    1024          8           0                         904.85              1107041.0               49677                            989183.0            950081                          104383.0                         242                                    31743.0

### Workflow

#### Actual
DBMS MySQL-64-8-1024 - Pods [[8]]

#### Planned
DBMS MySQL-64-8-1024 - Pods [[8]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST failed: Result contains FAILED column
