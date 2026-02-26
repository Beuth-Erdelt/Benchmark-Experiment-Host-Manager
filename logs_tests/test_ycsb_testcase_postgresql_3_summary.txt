## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 6873s 
    Code: 1749139628
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
    Benchmark is limited to DBMS ['PostgreSQL'].
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
PostgreSQL-64-8-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359045052
    datadisk:2846
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359049596
    datadisk:2853
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359050772
    datadisk:2856
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359225168
    datadisk:2923
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359238984
    datadisk:3046
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359247344
    datadisk:3048
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359247068
    datadisk:3050
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359247796
    datadisk:3052
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
        code:1749139628

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-1024-1-1               1       64    1024          1           0                        1023.49               977047.0            500515                             703.0              499485                               822.0
PostgreSQL-64-8-1024-1-3               1       64    1024          8           0                        1023.68               976894.0            499822                             736.0              500178                               847.0
PostgreSQL-64-8-1024-1-2               1      128    2048          2           0                        2046.08               488745.0            500438                             675.0              499562                               778.0
PostgreSQL-64-8-1024-1-4               1      128    2048         16           0                        2046.67               488620.0            500818                             707.0              499182                               883.0
PostgreSQL-64-8-1024-2-1               2       64    1024          1           0                        1023.51               977030.0            500306                             681.0              499694                               780.0
PostgreSQL-64-8-1024-2-3               2       64    1024          8           0                        1023.68               976913.0            499483                             742.0              500517                               861.0
PostgreSQL-64-8-1024-2-2               2      128    2048          2           0                        2046.10               488748.0            500244                             698.0              499756                               799.0
PostgreSQL-64-8-1024-2-4               2      128    2048         16           0                        2046.71               488605.0            500349                             770.0              499651                               908.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-1024 - Pods [[16, 8, 2, 1], [8, 16, 2, 1]]

#### Planned
DBMS PostgreSQL-64-8-1024 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
