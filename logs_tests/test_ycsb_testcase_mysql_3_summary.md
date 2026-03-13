## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 13692s 
    Code: 1748987063
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
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-64-8-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180368
    datadisk:13687
    volume_size:50G
    volume_used:14G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1748987063
MySQL-64-8-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180384
    datadisk:14835
    volume_size:50G
    volume_used:15G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1748987063
MySQL-64-8-1024-1-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180580
    datadisk:15982
    volume_size:50G
    volume_used:16G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1748987063
MySQL-64-8-1024-1-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180600
    datadisk:17129
    volume_size:50G
    volume_used:17G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1748987063
MySQL-64-8-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180796
    datadisk:18278
    volume_size:50G
    volume_used:18G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1748987063
MySQL-64-8-1024-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180816
    datadisk:19424
    volume_size:50G
    volume_used:19G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
        code:1748987063
MySQL-64-8-1024-2-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332180828
    datadisk:20570
    volume_size:50G
    volume_used:21G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
        code:1748987063
MySQL-64-8-1024-2-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332181020
    datadisk:21717
    volume_size:50G
    volume_used:22G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
        code:1748987063

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)  [UPDATE-FAILED].Operations  [UPDATE-FAILED].99thPercentileLatency(us)
MySQL-64-8-1024-1-1               1       64    1024          1           0                         675.56              1480254.0            499883                           37023.0              500117                           3106815.0                           0                                        0.0
MySQL-64-8-1024-1-3               1       64    1024          8           0                         548.57              1825543.0            499801                            1348.0              500199                           4898815.0                           0                                        0.0
MySQL-64-8-1024-1-2               1      128    2048          2           0                         552.69              1809957.0            500001                            1313.0              499999                          13066239.0                           0                                        0.0
MySQL-64-8-1024-1-4               1      128    2048         16           0                         739.11              1357626.0            499515                            1460.0              500473                           9215999.0                          12                                 50823167.0
MySQL-64-8-1024-2-1               2       64    1024          1           0                         610.39              1638291.0            500414                           52735.0              499586                           3760127.0                           0                                        0.0
MySQL-64-8-1024-2-3               2       64    1024          8           0                         678.58              1480195.0            499888                            1332.0              500112                           3872767.0                           0                                        0.0
MySQL-64-8-1024-2-2               2      128    2048          2           0                         810.16              1235485.0            500556                            1214.0              499444                           7942143.0                           0                                        0.0
MySQL-64-8-1024-2-4               2      128    2048         16           0                         622.58              1633727.0            500190                            1468.0              499810                          11698175.0                           0                                        0.0

### Workflow

#### Actual
DBMS MySQL-64-8-1024 - Pods [[16, 8, 2, 1], [16, 8, 2, 1]]

#### Planned
DBMS MySQL-64-8-1024 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST failed: Result contains FAILED column
