## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 3428s 
    Code: 1749002427
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
    Benchmark is limited to DBMS ['MySQL'].
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
MySQL-64-8-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332181244
    datadisk:23020
    volume_size:50G
    volume_used:23G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749002427
MySQL-64-8-1024-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332181256
    datadisk:24167
    volume_size:50G
    volume_used:24G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749002427

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MySQL-64-8-1024-1               1       64    1024          1           0                         787.67              1269573.0            499911                           41503.0              500089                           2619391.0
MySQL-64-8-1024-2               1       64    1024          8           0                         584.61              1719106.0            500708                            1340.0              499292                           3885055.0

### Workflow

#### Actual
DBMS MySQL-64-8-1024 - Pods [[8, 1]]

#### Planned
DBMS MySQL-64-8-1024 - Pods [[1, 8]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-1024-1     1432.25     1.34         39.21                48.23
MySQL-64-8-1024-2     1822.88     1.20         39.23                49.40

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-1024-1      292.69     0.29          0.62                 0.63
MySQL-64-8-1024-2      292.69     0.21          4.73                 4.77

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
