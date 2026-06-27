## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 8027s 
    Code: 1750090720
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392960236
    datadisk:10860
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750090720

### Execution
                 experiment_run  vusers  client  pod_count  efficiency    NOPM     TPM  duration  errors
MySQL-BHT-8-1-1               1      16       1          1         0.0  1288.0  3024.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1     6604.0        1.0   1.0                   8.721987

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      869.56     0.44         37.45                 45.5

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      361.33      0.2           0.1                  0.1

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      194.44     1.47         22.97                32.18

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        8.52     0.06          0.07                 0.07

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
