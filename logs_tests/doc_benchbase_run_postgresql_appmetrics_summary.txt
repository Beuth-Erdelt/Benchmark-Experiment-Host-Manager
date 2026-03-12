## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1454s 
    Code: 1773302747
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.3.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152151
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1773302747
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153028
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1773302747
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1        160   16384       1      1  300.0           1                   1938.576442                1922.536444         0.0                                                     286834.0                                              82502.0
PostgreSQL-1-1-1024-2-1               1         80    8192       2      1  300.0           1                    900.036338                 892.773007         0.0                                                     323169.0                                              88870.0
PostgreSQL-1-1-1024-2-2               1         80    8192       2      2  300.0           1                    896.559721                 889.049723         0.0                                                     326932.0                                              89192.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        160   16384          1  300.0           1                       1938.58                    1922.54         0.0                                                     286834.0                                              82502.0
PostgreSQL-1-1-1024-2               1        160   16384          2  300.0           2                       1796.60                    1781.82         0.0                                                     326932.0                                              89031.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      261.0        1.0   1.0         220.689655
PostgreSQL-1-1-1024-2      261.0        1.0   2.0         220.689655

### Monitoring

### Loading phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      717.45     4.32          7.45                 9.04
PostgreSQL-1-1-1024-2      717.45     4.32          7.45                 9.04

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1273.26     9.05          0.26                 0.26
PostgreSQL-1-1-1024-2     1273.26     9.05          0.26                 0.26

### Execution phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2332.28     9.07          9.54                11.72
PostgreSQL-1-1-1024-2     2241.42     8.75         10.20                12.88

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       578.6     2.15          0.77                 0.77
PostgreSQL-1-1-1024-2       578.6     3.07          0.77                 0.77

### Application Metrics

#### Loading phase: SUT deployment
                       Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-1-1-1024-1                       16                                       0                                               0                         17                                     16
PostgreSQL-1-1-1024-2                       16                                       0                                               0                         17                                     16

#### Execution phase: SUT deployment
                       Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-1-1-1024-1                      9.0                                    17.0                                             0.0                      158.0                                  158.0
PostgreSQL-1-1-1024-2                     10.0                                    17.0                                             0.0                      160.0                                  160.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
