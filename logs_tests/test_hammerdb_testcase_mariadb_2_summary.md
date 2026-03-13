## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1133s 
    Code: 1750103774
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MariaDB'].
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
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392980272
    datadisk:1640
    volume_size:30G
    volume_used:1.6G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750103774

### Execution
                   experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
MariaDB-BHT-8-1-1               1      16       1          1         0.0  11051.0  25616.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MariaDB-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8-1 - Pods [[1]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
MariaDB-BHT-8-1-1      345.0        1.0   1.0                 166.956522

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      520.42     2.12          2.56                 2.59

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      358.21     1.06          0.09                  0.1

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      753.47     2.14          2.73                 2.76

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1       70.66     0.16          0.07                 0.07

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
