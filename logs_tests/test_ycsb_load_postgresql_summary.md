## Show Summary

### Workload
YCSB Data Loading SF=1
    Type: ycsb
    Duration: 329s 
    Code: 1749627711
    Intro: YCSB driver runs the experiment.
    This imports YCSB data sets.
    Workload is 'C'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Target is based on multiples of '16384'.
    Factors for loading are [1].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Experiment is run once.

### Services
PostgreSQL-64-8-16384
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-64-8-16384-1749627711 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389594652
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749627711

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8           0                   16319.503604                61292.0             1000000                            1176.125

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      168.17     2.84          3.87                 4.73

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       50.89        0          3.39                 3.42

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Result contains no FAILED column
