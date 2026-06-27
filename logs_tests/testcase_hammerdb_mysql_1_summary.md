## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1229s 
    Code: 1750089430
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
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
    disk:403932404
    datadisk:10864
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750089430

### Execution
                 experiment_run  vusers  client  pod_count  efficiency    NOPM     TPM  duration  errors
MySQL-BHT-8-1-1               1      16       1          1         0.0  2499.0  5772.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1      375.0        1.0   1.0                      153.6

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
