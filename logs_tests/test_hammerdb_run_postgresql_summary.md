## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
    Type: tpcc
    Duration: 798s 
    Code: 1749630540
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749630540 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387041208
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749630540

### Execution
                      experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-1-1-1               1      64       1          1         0.0  19670.0  53038.0         5       0

Warehouses: 1

### Workflow

#### Actual
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       31.0        1.0   1.0                 116.129032

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        3.46        0          2.41                 2.47

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       12.11        0          0.02                 0.02

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1    10120.59     23.8          3.49                 3.91

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        88.8     0.22          0.19                 0.19

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
