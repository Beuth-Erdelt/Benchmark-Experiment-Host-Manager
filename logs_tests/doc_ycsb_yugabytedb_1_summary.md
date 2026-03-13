## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 957s 
    Code: 1770048432
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96156
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770048432

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8           0                   15398.593486                65177.0             1000000                             43851.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                       15454.59               647057.0           4997636                           59807.0             5002364                             62079.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1891.31    28.05          2.78                 8.13

### Loading phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        5.68     0.07          0.18                 0.22

### Loading phase: component loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       73.94        0          0.11                 0.11

### Execution phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    20703.63     37.1          5.07                16.59

### Execution phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        18.6     0.07          0.19                 0.23

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      523.74     0.99          0.14                 0.14

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
