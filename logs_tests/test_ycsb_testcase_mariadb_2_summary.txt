## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 3680s 
    Code: 1749150342
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
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-64-8-1024-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359250416
    datadisk:1871
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749150342
MariaDB-64-8-1024-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359250980
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1749150342

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
MariaDB-64-8-1024               1       64    1024          8           0                    1010.970402               989788.0             1000000                            828287.0

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MariaDB-64-8-1024-1-1               1       64    1024          1           0                        1023.49               977045.0            499394                            1309.0              500606                              1635.0
MariaDB-64-8-1024-2-1               2       64    1024          1           0                        1023.51               977027.0            499688                            1272.0              500312                              1494.0

### Workflow

#### Actual
DBMS MariaDB-64-8-1024 - Pods [[1], [1]]

#### Planned
DBMS MariaDB-64-8-1024 - Pods [[1], [1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
