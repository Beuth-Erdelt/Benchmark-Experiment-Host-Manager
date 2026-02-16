## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 2321s 
    Code: 1749021062
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
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-64-8-1024-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332236784
    datadisk:2012
    volume_size:30G
    volume_used:2.0G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749021062
MariaDB-64-8-1024-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332236796
    datadisk:2012
    volume_size:30G
    volume_used:2.0G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749021062

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MariaDB-64-8-1024-1               1       64    1024          1           0                        1023.49               977053.0            499690                            1563.0              500310                              1994.0
MariaDB-64-8-1024-2               1       64    1024          8           0                        1023.66               976914.0            500180                            1849.0              499820                              2299.0

### Workflow

#### Actual
DBMS MariaDB-64-8-1024 - Pods [[8, 1]]

#### Planned
DBMS MariaDB-64-8-1024 - Pods [[1, 8]]

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-64-8-1024-1      275.92     0.71          2.57                 2.81
MariaDB-64-8-1024-2      276.01     0.66          2.58                 2.82

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-64-8-1024-1      208.17     0.22          0.58                 0.59
MariaDB-64-8-1024-2      206.66     0.39          3.03                 3.05

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
