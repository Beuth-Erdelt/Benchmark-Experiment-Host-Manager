## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1117s 
    Code: 1770923951
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
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
        disk:898268
        datadisk:291861
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:466964
        datadisk:291679
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:415112
        datadisk:291982
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1770923951
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:898463
        datadisk:292053
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:467124
        datadisk:291839
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:415110
        datadisk:291979
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1770923951
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    312.983331                 311.596665         0.0                                                     103278.0                                              51107.0
CockroachDB-1-1-1024-2-2               1          8    8192       2      1  300.0           0                    127.093312                 126.606646         0.0                                                     132056.0                                              62933.0
CockroachDB-1-1-1024-2-1               1          8    8192       2      2  300.0           0                    121.826654                 121.349987         0.0                                                     132987.0                                              65652.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        312.98                     311.60         0.0                                                     103278.0                                              51107.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        248.92                     247.96         0.0                                                     132987.0                                              64292.5

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      168.0        1.0   1.0         342.857143
CockroachDB-1-1-1024-2      168.0        1.0   2.0         342.857143

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
