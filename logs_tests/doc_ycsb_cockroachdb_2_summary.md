## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 4097s 
    Code: 1770918190
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
CockroachDB-64-8-65536-1-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:896582
        datadisk:291248
        volume_size:50G
        volume_used:1.9G
        cpu_list:0-223
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:464627
        datadisk:291189
        volume_size:50G
        volume_used:1.9G
        cpu_list:0-127
    worker 2
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1349336
        datadisk:291129
        volume_size:50G
        volume_used:1.8G
        cpu_list:0-255
    eval_parameters
        code:1770918190
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3
CockroachDB-64-8-65536-2-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1349336
        datadisk:291048
        volume_size:50G
        volume_used:1.7G
        cpu_list:0-255
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:464628
        datadisk:291049
        volume_size:50G
        volume_used:1.7G
        cpu_list:0-127
    worker 2
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:896583
        datadisk:291052
        volume_size:50G
        volume_used:1.7G
        cpu_list:0-223
    worker 3
        node:cl-worker22
    eval_parameters
        code:1770918190
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                     736.037075              1361805.0             1000000                            510559.0

### Execution
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-2-1               2       64   65536          1           0                         638.85              1565324.0            499948                          187775.0              500052                           4444159.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

### Monitoring

### Loading phase: component worker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1    21699.49     2.03          10.3                23.39

### Loading phase: component loader
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      158.04     0.27          0.11                 0.11

### Execution phase: component worker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      813.03     2.36          6.09                11.81
CockroachDB-64-8-65536-2-1     3127.46     2.52          6.60                12.33

### Execution phase: component benchmarker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1       50.59     0.28          0.13                 0.13
CockroachDB-64-8-65536-2-1      112.39     0.08          0.13                 0.13

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST failed: Workflow not as planned
TEST passed: Execution Phase: contains no FAILED column
