## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1530s 
    Code: 1748943250
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:328989148
    datadisk:11132
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748943250

### Execution
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         16    8192          1  300.0           0                        112.58                     112.09         0.0                                                     438246.0                                             142078.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      765.0        1.0   1.0          75.294118

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1542.16     2.22         37.43                37.47

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1341.21     3.77          1.33                 1.33

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      436.01     1.81         23.42                27.21

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      167.69     0.59          0.82                 0.82

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
