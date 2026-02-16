## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 1585s 
    Code: 1770922331
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 10000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
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
        disk:907492
        datadisk:301035
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081853952000
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:430500
        datadisk:300823
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1361095
        datadisk:301113
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
        code:1770922331
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   22590.094584               443241.0            10000000                              5205.5

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       12541.26               797368.0           5000662                            6147.0             4999338                            136447.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     12861.7    34.12          21.3                55.54

### Loading phase: component loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      748.18     2.13          0.11                 0.11

### Execution phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    18441.31    26.95         26.69                 65.4

### Execution phase: component benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      593.62     0.88          0.13                 0.13

### Application Metrics

#### Loading phase: component worker
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                   71343.93                  68740810.71                                    0.0                                      0.0                              0.0

#### Execution phase: component worker
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                   17213.11                  31282799.76                                    0.0                                      0.0                              0.0

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
