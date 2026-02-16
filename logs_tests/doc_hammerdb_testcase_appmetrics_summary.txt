## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1314s 
    Code: 1771361129
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:102202
    datadisk:3299
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771361129
PostgreSQL-BHT-16-1-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:103193
    datadisk:4290
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771361129

### Execution
                       experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1     33.83     50.67         0.0  16246.0  37518.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2     33.80     58.61         0.0  19568.5  45451.5         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-16-1 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       94.0        1.0   1.0                 612.765957
PostgreSQL-BHT-16-1-2       94.0        1.0   2.0                 612.765957

### Monitoring

### Loading phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       123.5     1.49          7.16                 7.82
PostgreSQL-BHT-16-1-2       123.5     1.49          7.16                 7.82

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      224.42        0          0.15                 0.15
PostgreSQL-BHT-16-1-2      224.42        0          0.15                 0.15

### Execution phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      329.14     0.79          7.63                 8.46
PostgreSQL-BHT-16-1-2      340.92     0.90          8.06                 9.12

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       59.93     0.14          0.16                 0.16
PostgreSQL-BHT-16-1-2       54.25     0.32          0.16                 0.16

### Application Metrics
                       Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-BHT-16-1-1                             1.0                            13.0                               9.0                                 0.19                                 0.31
PostgreSQL-BHT-16-1-2                             2.0                            15.0                               6.0                                 0.14                                 0.22

### Tests
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
