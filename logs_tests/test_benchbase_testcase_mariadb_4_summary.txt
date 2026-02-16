## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 2007s 
    Code: 1748950362
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
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
MariaDB-1-1-1024-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590604
    datadisk:1943
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-1-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590604
    datadisk:1971
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-1-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590612
    datadisk:1995
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-1-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590612
    datadisk:2031
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590612
    datadisk:2071
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317601456
    datadisk:2091
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317546068
    datadisk:2123
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317534032
    datadisk:2147
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1748950362

### Execution
                      experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MariaDB-1-1-1024-1-1               1          8    8192          1  120.0           0                        313.33                     312.02         0.0                                                      15358.0                                              25516.0
MariaDB-1-1-1024-1-2               1         16   16384          2  120.0           0                        345.94                     342.71         0.0                                                      23169.0                                              36029.0
MariaDB-1-1-1024-1-3               1          8    8192          2  120.0           0                        417.55                     413.51         0.0                                                      18344.0                                              19118.5
MariaDB-1-1-1024-1-4               1         16   16384          4  120.0           0                        515.34                     507.25         0.0                                                      27275.0                                              28714.0
MariaDB-1-1-1024-2-1               2          8    8192          1  120.0           0                        315.81                     314.26         0.0                                                      16761.0                                              22922.0
MariaDB-1-1-1024-2-2               2         16   16384          2  120.0           0                        344.72                     341.32         0.0                                                      28206.0                                              38851.0
MariaDB-1-1-1024-2-3               2          8    8192          2  120.0           0                        356.69                     352.91         0.0                                                      17531.0                                              18927.5
MariaDB-1-1-1024-2-4               2         16   16384          4  120.0           0                        422.47                     415.79         0.0                                                      29895.0                                              33430.0

### Workflow

#### Actual
DBMS MariaDB-1-1-1024 - Pods [[2, 2, 4, 1], [4, 1, 2, 2]]

#### Planned
DBMS MariaDB-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                      time_load  terminals  pods  Throughput [SF/h]
MariaDB-1-1-1024-1-1      471.0        1.0   1.0         122.292994
MariaDB-1-1-1024-1-2      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-1-3      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-1-4      471.0        1.0   4.0         122.292994
MariaDB-1-1-1024-2-1      471.0        1.0   1.0         122.292994
MariaDB-1-1-1024-2-2      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-2-3      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-2-4      471.0        1.0   4.0         122.292994

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1-1      118.33     0.97          2.43                 2.74
MariaDB-1-1-1024-1-2      135.25     1.52          2.48                 2.79
MariaDB-1-1-1024-1-3      160.10     2.08          2.53                 2.84
MariaDB-1-1-1024-1-4      284.73     1.27          2.58                 2.89
MariaDB-1-1-1024-2-1      892.33     1.27          5.10                 5.60
MariaDB-1-1-1024-2-2      242.03     1.97          2.64                 2.94
MariaDB-1-1-1024-2-3      122.16     1.21          2.66                 2.96
MariaDB-1-1-1024-2-4      235.28     1.32          2.72                 3.02

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1-1       82.39     0.00          0.44                 0.44
MariaDB-1-1-1024-1-2      102.54     1.02          1.09                 1.09
MariaDB-1-1-1024-1-3      107.54     0.60          1.29                 1.29
MariaDB-1-1-1024-1-4      135.78     0.36          1.70                 1.70
MariaDB-1-1-1024-2-1       67.23     0.00          0.35                 0.35
MariaDB-1-1-1024-2-2      128.95     0.42          1.05                 1.05
MariaDB-1-1-1024-2-3       87.52     0.32          1.32                 1.32
MariaDB-1-1-1024-2-4       73.72     0.51          1.78                 1.78

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
