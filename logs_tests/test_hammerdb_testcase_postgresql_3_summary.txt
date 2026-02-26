## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3091s 
    Code: 1750144214
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394907432
    datadisk:3142
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394903564
    datadisk:3244
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394903164
    datadisk:3755
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394902924
    datadisk:4198
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394895944
    datadisk:4605
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394895792
    datadisk:4680
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393679948
    datadisk:4780
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393680844
    datadisk:4854
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214

### Execution
                        experiment_run  vusers  client  pod_count  efficiency     NOPM       TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1         0.0  11155.0  34338.00         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2         0.0  10683.5  31413.50         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2         0.0   9245.5  29545.50         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4         0.0   9827.0  28375.75         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1         0.0   8843.0  28338.00         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2         0.0   9867.0  29033.50         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2         0.0   8184.0  26391.00         2       0
PostgreSQL-BHT-8-1-2-4               2      32       4          4         0.0   9192.0  26915.75         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[2, 2, 4, 1], [4, 2, 1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      105.0        1.0   1.0                 548.571429
PostgreSQL-BHT-8-1-1-2      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-1-3      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-1-4      105.0        1.0   4.0                 548.571429
PostgreSQL-BHT-8-1-2-1      105.0        1.0   1.0                 548.571429
PostgreSQL-BHT-8-1-2-2      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-2-3      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-2-4      105.0        1.0   4.0                 548.571429

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1    14210.81    61.39          4.88                 7.15
PostgreSQL-BHT-8-1-1-2    16329.58    62.06          5.66                 8.06
PostgreSQL-BHT-8-1-1-3    14599.86    61.88          5.34                 7.81
PostgreSQL-BHT-8-1-1-4    16248.56    62.80          5.90                 8.42
PostgreSQL-BHT-8-1-2-1    62554.21    61.99          9.53                14.73
PostgreSQL-BHT-8-1-2-2    15525.44    62.00          5.87                 8.62
PostgreSQL-BHT-8-1-2-3    15185.24    61.07          5.77                 8.60
PostgreSQL-BHT-8-1-2-4    15832.79    61.88          6.14                 9.03

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       16.73     0.08          0.07                 0.07
PostgreSQL-BHT-8-1-1-2       14.05     0.09          0.21                 0.22
PostgreSQL-BHT-8-1-1-3       22.81     0.07          0.23                 0.23
PostgreSQL-BHT-8-1-1-4       16.87     0.04          0.26                 0.27
PostgreSQL-BHT-8-1-2-1       14.48     0.06          0.09                 0.09
PostgreSQL-BHT-8-1-2-2       14.92     0.04          0.21                 0.22
PostgreSQL-BHT-8-1-2-3       19.10     0.03          0.23                 0.23
PostgreSQL-BHT-8-1-2-4       11.94     0.05          0.26                 0.27

### Tests
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
