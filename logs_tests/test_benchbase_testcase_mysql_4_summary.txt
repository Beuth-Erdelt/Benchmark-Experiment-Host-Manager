## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 2183s 
    Code: 1748944810
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
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
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590204
    datadisk:11187
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590204
    datadisk:11220
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590208
    datadisk:11256
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590208
    datadisk:11308
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590216
    datadisk:11339
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590216
    datadisk:11374
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590220
    datadisk:11458
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590396
    datadisk:11489
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1748944810

### Execution
                    experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1-1               1          8    8192          1  120.0           0                         36.02                      35.85         0.0                                                     610937.0                                            220741.00
MySQL-1-1-1024-1-2               1         16   16384          2  120.0           0                         39.64                      39.47         0.0                                                     820427.0                                            285537.50
MySQL-1-1-1024-1-3               1          8    8192          2  120.0           0                         69.92                      69.46         0.0                                                     394377.0                                            114272.50
MySQL-1-1-1024-1-4               1         16   16384          4  120.0           0                         37.22                      36.94         0.0                                                    1876083.0                                            429714.25
MySQL-1-1-1024-2-1               2          8    8192          1  120.0           0                         45.04                      44.85         0.0                                                     500014.0                                            177493.00
MySQL-1-1-1024-2-2               2         16   16384          2  120.0           0                        106.22                     105.62         0.0                                                     483418.0                                            150073.00
MySQL-1-1-1024-2-3               2          8    8192          2  120.0           0                         39.84                      39.67         0.0                                                     952677.0                                            200600.50
MySQL-1-1-1024-2-4               2         16   16384          4  120.0           0                         49.48                      49.02         0.0                                                     940977.0                                            213649.25

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1, 2, 2, 4], [4, 2, 2, 1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-1-2     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-1-3     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-1-4     7641.0        1.0   4.0            7.53828
MySQL-1-1-1024-2-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-2-2     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-2-3     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-2-4     7641.0        1.0   4.0            7.53828

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1-1       50.42     0.79         37.96                45.81
MySQL-1-1-1024-1-2       78.16     0.28         38.17                46.08
MySQL-1-1-1024-1-3       86.48     0.10         38.23                46.20
MySQL-1-1-1024-1-4       49.59     0.73         38.27                46.26
MySQL-1-1-1024-2-1       51.82     0.00         37.95                45.98
MySQL-1-1-1024-2-2      112.04     1.48         38.17                46.30
MySQL-1-1-1024-2-3      100.06     0.47         38.21                46.40
MySQL-1-1-1024-2-4      123.16     1.35         38.26                46.51

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1-1       33.15     0.00          0.28                 0.28
MySQL-1-1-1024-1-2       61.65     0.00          0.80                 0.80
MySQL-1-1-1024-1-3       33.28     0.00          1.19                 1.19
MySQL-1-1-1024-1-4       38.84     0.08          1.45                 1.45
MySQL-1-1-1024-2-1       35.98     0.00          0.30                 0.30
MySQL-1-1-1024-2-2       87.11     0.37          0.97                 0.97
MySQL-1-1-1024-2-3       35.98     0.07          1.18                 1.18
MySQL-1-1-1024-2-4      117.93     0.51          4.46                 4.47

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
