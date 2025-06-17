## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3178s 
    Code: 1750104975
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MariaDB'].
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
MariaDB-BHT-8-1-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392980956
    datadisk:1725
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-1-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392981692
    datadisk:1782
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-1-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393277240
    datadisk:1823
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-1-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393283676
    datadisk:1867
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393286676
    datadisk:1903
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393287036
    datadisk:1947
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-2-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393286988
    datadisk:1992
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975
MariaDB-BHT-8-1-2-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393287596
    datadisk:2036
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750104975

### Execution
                     experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
MariaDB-BHT-8-1-1-1               1      16       1          1         0.0  11854.0  27681.0         2       0
MariaDB-BHT-8-1-1-2               1      32       2          2         0.0   9138.0  21218.0         2       0
MariaDB-BHT-8-1-1-3               1      16       3          2         0.0   8589.0  19906.0         2       0
MariaDB-BHT-8-1-1-4               1      32       4          4         0.0   7608.0  17744.0         2       0
MariaDB-BHT-8-1-2-1               2      16       1          1         0.0  11327.0  26492.0         2       0
MariaDB-BHT-8-1-2-2               2      32       2          2         0.0   8274.0  19100.0         2       0
MariaDB-BHT-8-1-2-3               2      16       3          2         0.0  10246.0  23647.0         2       0
MariaDB-BHT-8-1-2-4               2      32       4          4         0.0   8605.0  19909.0         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS MariaDB-BHT-8-1 - Pods [[4, 2, 2, 1], [1, 2, 2, 4]]

#### Planned
DBMS MariaDB-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                     time_load  terminals  pods  Imported warehouses [1/h]
MariaDB-BHT-8-1-1-1      345.0        1.0   1.0                 166.956522
MariaDB-BHT-8-1-1-2      345.0        1.0   2.0                 166.956522
MariaDB-BHT-8-1-1-3      345.0        1.0   2.0                 166.956522
MariaDB-BHT-8-1-1-4      345.0        1.0   4.0                 166.956522
MariaDB-BHT-8-1-2-1      345.0        1.0   1.0                 166.956522
MariaDB-BHT-8-1-2-2      345.0        1.0   2.0                 166.956522
MariaDB-BHT-8-1-2-3      345.0        1.0   2.0                 166.956522
MariaDB-BHT-8-1-2-4      345.0        1.0   4.0                 166.956522

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1-1      497.61     2.38          2.42                 2.71
MariaDB-BHT-8-1-1-2     1092.93     2.06          2.56                 2.84
MariaDB-BHT-8-1-1-3      386.03     1.93          2.60                 2.88
MariaDB-BHT-8-1-1-4      840.76     3.91          2.68                 2.97
MariaDB-BHT-8-1-2-1     2910.91     2.18          4.99                 5.46
MariaDB-BHT-8-1-2-2      741.47     2.58          2.59                 2.93
MariaDB-BHT-8-1-2-3      430.79     1.91          2.64                 2.98
MariaDB-BHT-8-1-2-4      607.57     1.96          2.73                 3.07

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1-1       42.65     0.19          0.07                 0.07
MariaDB-BHT-8-1-1-2       42.65     0.08          0.21                 0.22
MariaDB-BHT-8-1-1-3       31.65     0.09          0.23                 0.24
MariaDB-BHT-8-1-1-4       34.10     0.05          0.26                 0.27
MariaDB-BHT-8-1-2-1       42.49     0.18          0.09                 0.09
MariaDB-BHT-8-1-2-2       42.50     0.11          0.21                 0.22
MariaDB-BHT-8-1-2-3       36.74     0.07          0.23                 0.23
MariaDB-BHT-8-1-2-4       35.29     0.06          0.26                 0.27

### Tests
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
