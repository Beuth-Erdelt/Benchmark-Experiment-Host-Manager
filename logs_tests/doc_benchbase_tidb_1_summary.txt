## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1803s 
    Code: 1764165224
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.16.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 1 processes (pods).
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-1-1-1024-1 uses docker image pingcap/tidb:v7.1.0
    RAM:1081742749696
    CPU:AMD EPYC 7502 32-Core Processor
    Cores:128
    host:6.8.0-86-generic
    node:cl-worker29
    disk:1374750
    cpu_list:0-127
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1374751
        cpu_list:0-127
    sut 1
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:639712
        cpu_list:0-223
    sut 2
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1387580
        cpu_list:0-255
    pd 0
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1387571
        cpu_list:0-255
    pd 1
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1374750
        cpu_list:0-127
    pd 2
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:639710
        cpu_list:0-223
    tikv 0
        RAM:1081965486080
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1390278
        cpu_list:0-255
    tikv 1
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1387563
        cpu_list:0-255
    tikv 2
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:639677
        cpu_list:0-223
    eval_parameters
                code:1764165224
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
TiDB-1-1-1024-2 uses docker image pingcap/tidb:v7.1.0
    RAM:1081742749696
    CPU:AMD EPYC 7502 32-Core Processor
    Cores:128
    host:6.8.0-86-generic
    node:cl-worker29
    disk:1374751
    cpu_list:0-127
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    sut 0
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1374751
        cpu_list:0-127
    sut 1
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:637984
        cpu_list:0-223
    sut 2
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1385875
        cpu_list:0-255
    pd 0
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1385871
        cpu_list:0-255
    pd 1
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1374751
        cpu_list:0-127
    pd 2
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:637958
        cpu_list:0-223
    tikv 0
        RAM:1081965486080
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1389018
        cpu_list:0-255
    tikv 1
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1385882
        cpu_list:0-255
    tikv 2
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:637984
        cpu_list:0-223
    eval_parameters
                code:1764165224
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
TiDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    340.073309                 338.459976         0.0                                                     136710.0                                              47037.0
TiDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    148.459978                 146.943312         0.0                                                     143648.0                                              53868.0
TiDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    154.019959                 152.493292         0.0                                                     149166.0                                              51928.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
TiDB-1-1-1024-1               1         16   16384          1  300.0           0                        340.07                     338.46         0.0                                                     136710.0                                              47037.0
TiDB-1-1-1024-2               1         16   16384          2  300.0           0                        302.48                     299.44         0.0                                                     149166.0                                              52898.0

### Workflow

#### Actual
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
TiDB-1-1-1024-1      265.0        1.0   1.0         217.358491
TiDB-1-1-1024-2      265.0        1.0   2.0         217.358491

### Monitoring

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1935.17     9.58           2.4                 3.18
TiDB-1-1-1024-2     1935.17     9.58           2.4                 3.18

### Loading phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1       168.1     0.74          0.28                 0.28
TiDB-1-1-1024-2       168.1     0.74          0.28                 0.28

### Loading phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     2145.26    11.94          9.97                28.01
TiDB-1-1-1024-2     2145.26    11.94          9.97                28.01

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      113.32     0.63          0.67                 0.67
TiDB-1-1-1024-2      113.32     0.63          0.67                 0.67

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     3083.22    11.64          1.87                 2.65
TiDB-1-1-1024-2     2639.94    10.01          3.12                 3.90

### Execution phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      444.65     1.85          0.32                 0.33
TiDB-1-1-1024-2      489.56     1.80          0.33                 0.33

### Execution phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1652.09     6.42         12.40                31.64
TiDB-1-1-1024-2     1564.08     6.41         13.31                32.17

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      172.32     0.69          0.33                 0.33
TiDB-1-1-1024-2      154.84     0.88          0.29                 0.29

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
