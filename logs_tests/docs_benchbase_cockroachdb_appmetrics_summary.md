## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1352s 
    Code: 1772842492
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.1.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147811
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173209600
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:702318
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081853952000
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:417146
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081965416448
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1311724
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1772842492
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147809
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173209600
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:702628
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081853952000
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:417451
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081965416448
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1312034
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1772842492
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    514.413285                 512.263285         0.0                                                      72389.0                                              31093.0
CockroachDB-1-1-1024-2-2               1          8    8192       2      1  300.0           0                    253.056659                 251.999992         0.0                                                      74727.0                                              31603.0
CockroachDB-1-1-1024-2-1               1          8    8192       2      2  300.0           0                    242.359930                 241.326597         0.0                                                      82723.0                                              32998.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        514.41                     512.26         0.0                                                      72389.0                                              31093.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        495.42                     493.33         0.0                                                      82723.0                                              32300.5

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      221.0        1.0   1.0         260.633484
CockroachDB-1-1-1024-2      221.0        1.0   2.0         260.633484

### Monitoring

### Loading phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     2163.53    19.11          6.32                 9.84
CockroachDB-1-1-1024-2     2163.53    19.11          6.32                 9.84

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     1356.21    13.52          0.25                 0.25
CockroachDB-1-1-1024-2     1356.21    13.52          0.25                 0.25

### Execution phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     6428.38    24.07          8.94                12.82
CockroachDB-1-1-1024-2     6361.03    22.33          7.80                12.57

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1       250.0     0.92          0.32                 0.32
CockroachDB-1-1-1024-2       250.0     1.70          0.32                 0.32

### Application Metrics

#### Loading phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                    1363.87                  12895218.38                                      0                                        0                                0
CockroachDB-1-1-1024-2                                    1363.87                  12895218.38                                      0                                        0                                0

#### Execution phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                   27334.79                   5029922.02                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-2                                    9909.29                   3968858.30                                    0.0                                      0.0                              0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
