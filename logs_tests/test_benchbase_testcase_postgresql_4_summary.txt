## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1936s 
    Code: 1749129321
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358240476
    datadisk:7963
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358240992
    datadisk:8051
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358241380
    datadisk:8217
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358241172
    datadisk:8331
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358490124
    datadisk:8476
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358491144
    datadisk:8551
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358491472
    datadisk:8712
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358245748
    datadisk:8821
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1749129321

### Execution
                         experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0           0                        856.82                     853.06         0.0                                                      15454.0                                              9325.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0           1                       1650.73                    1635.38         0.0                                                      21337.0                                              9683.50
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0           0                       1144.57                    1133.88         0.0                                                      14775.0                                              6976.50
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0           2                       1488.36                    1466.36         0.0                                                      23439.0                                             10734.75
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0           0                        733.64                     730.11         0.0                                                      21145.0                                             10892.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0           0                       1622.52                    1607.08         0.0                                                      20943.0                                              9848.00
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0           1                       1091.28                    1080.81         0.0                                                      15040.0                                              7317.00
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0           1                       1434.22                    1412.25         0.0                                                      23812.0                                             11140.50

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[4, 2, 2, 1], [2, 4, 2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-1-2      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-1-3      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-1-4      175.0        1.0   4.0         329.142857
PostgreSQL-1-1-1024-2-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-2-2      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-2-3      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-2-4      175.0        1.0   4.0         329.142857

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      329.70     0.76          3.23                 7.68
PostgreSQL-1-1-1024-1-2      691.98     6.95          3.72                 8.37
PostgreSQL-1-1-1024-1-3      448.58     3.44          3.89                 8.68
PostgreSQL-1-1-1024-1-4      727.81     5.49          4.17                 9.10
PostgreSQL-1-1-1024-2-1     2460.89     0.06          6.37                11.45
PostgreSQL-1-1-1024-2-2      631.05     0.00          3.66                 8.72
PostgreSQL-1-1-1024-2-3      349.81     0.00          3.87                 9.06
PostgreSQL-1-1-1024-2-4      545.74     6.33          4.17                 9.50

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      166.09     2.02          0.58                 0.58
PostgreSQL-1-1-1024-1-2      394.05     1.60          1.75                 1.75
PostgreSQL-1-1-1024-1-3      242.09     2.05          1.91                 1.91
PostgreSQL-1-1-1024-1-4      284.79     1.82          2.47                 2.47
PostgreSQL-1-1-1024-2-1       77.49     0.00          0.32                 0.32
PostgreSQL-1-1-1024-2-2      281.63     1.62          1.21                 1.21
PostgreSQL-1-1-1024-2-3      197.94     0.00          1.59                 1.59
PostgreSQL-1-1-1024-2-4      222.02     0.75          1.97                 1.98

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
