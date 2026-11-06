## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 8930s 
    Code: 1748934307
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590004
    datadisk:11132
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748934307
MySQL-1-1-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590184
    datadisk:11165
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748934307

### Execution
                    experiment_run  terminals  target  pod_count  time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1-1               1         16    8192          1  60.0           0                          1.00                       1.23         0.0                                                   47671586.0                                            8847058.0
MySQL-1-1-1024-2-1               2         16    8192          1  60.0           0                          4.52                       4.78         0.0                                                   15558733.0                                            3001960.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1], [1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-2-1     7641.0        1.0   1.0            7.53828

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
