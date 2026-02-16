## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 7028s 
    Code: 1749154063
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
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-64-8-1024-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359251792
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-1-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359252284
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-1-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359252544
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-1-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359253064
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359263688
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359264216
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-2-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359264432
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
        code:1749154063
MariaDB-64-8-1024-2-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359272016
    datadisk:1872
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
        code:1749154063

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MariaDB-64-8-1024-1-1               1       64    1024          1           0                        1023.49               977053.0            499413                            1272.0              500587                              1625.0
MariaDB-64-8-1024-1-3               1       64    1024          8           0                        1023.68               976909.0            499256                            1416.0              500744                              1929.0
MariaDB-64-8-1024-1-2               1      128    2048          2           0                        2042.57               489738.0            499938                            3509.0              500062                             10135.0
MariaDB-64-8-1024-1-4               1      128    2048         16           0                        2046.62               488632.0            500884                            2069.0              499116                              6467.0
MariaDB-64-8-1024-2-1               2       64    1024          1           0                        1023.49               977047.0            500393                             998.0              499607                              1111.0
MariaDB-64-8-1024-2-3               2       64    1024          8           0                        1023.67               976904.0            500093                            1350.0              499907                              1698.0
MariaDB-64-8-1024-2-2               2      128    2048          2           0                        2045.51               488912.0            499025                            3107.0              500975                             12247.0
MariaDB-64-8-1024-2-4               2      128    2048         16           0                        2046.64               488614.0            500194                            1833.0              499806                              3201.0

### Workflow

#### Actual
DBMS MariaDB-64-8-1024 - Pods [[8, 16, 2, 1], [16, 1, 8, 2]]

#### Planned
DBMS MariaDB-64-8-1024 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
