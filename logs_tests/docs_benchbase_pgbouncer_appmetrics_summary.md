## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1738s 
    Code: 1772843882
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.9.1.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PGBouncer'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Pooling is done with [2] pods having [32] inbound and [32] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
pgb-1-2-32-32-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152117
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772843882
pgb-1-2-32-32-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152392
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772843882

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
pgb-1-2-32-32-1-1               1         32   16384       1      1  600.0           2                   1419.373316                 467.336661         0.0                                                      42104.0                                              22541.0
pgb-1-2-32-32-2-1               1         16    8192       2      1  600.0           1                    595.639960                 445.091637         0.0                                                      52955.0                                              26854.0
pgb-1-2-32-32-2-2               1         16    8192       2      2  600.0           0                    615.298234                 445.133261         0.0                                                      52476.0                                              25996.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
pgb-1-2-32-32-1               1         32   16384          1  600.0           2                       1419.37                     467.34         0.0                                                      42104.0                                              22541.0
pgb-1-2-32-32-2               1         32   16384          2  600.0           1                       1210.94                     890.22         0.0                                                      52955.0                                              26425.0

### Workflow

#### Actual
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

#### Planned
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
pgb-1-2-32-32-1      152.0        1.0   1.0         378.947368
pgb-1-2-32-32-2      152.0        1.0   2.0         378.947368

### Monitoring

### Loading phase: component pool
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1        0.41      0.0          0.04                 0.04
pgb-1-2-32-32-2        0.41      0.0          0.04                 0.04

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1      705.11     7.79          4.71                 6.34
pgb-1-2-32-32-2      705.11     7.79          4.71                 6.34

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1     1271.66    12.76          0.26                 0.26
pgb-1-2-32-32-2     1271.66    12.76          0.26                 0.26

### Execution phase: component pool
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1        1.18      0.0          0.04                 0.04
pgb-1-2-32-32-2        1.12      0.0          0.04                 0.04

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1     2161.66     4.05          5.01                 6.91
pgb-1-2-32-32-2     3957.94     8.22          5.51                 7.83

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1    12049.58    24.20          0.48                 0.48
pgb-1-2-32-32-2    12049.58    23.12          0.48                 0.48

### Application Metrics

#### Loading phase: component pool
                 PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-1-2-32-32-1                                  224.53                           0.19                                    0                                        48                             100.0
pgb-1-2-32-32-2                                  224.53                           0.19                                    0                                        48                             100.0

#### Loading phase: SUT deployment
                 Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-1-2-32-32-1                       65                                       0                                               0                         15                                     14
pgb-1-2-32-32-2                       65                                       0                                               0                         15                                     14

#### Execution phase: component pool
                 PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-1-2-32-32-1                                 9640.80                           0.35                                    0                                        56                             100.0
pgb-1-2-32-32-2                                18880.11                           0.09                                    0                                        55                             100.0

#### Execution phase: SUT deployment
                 Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-1-2-32-32-1                       65                                      21                                               0                         19                                     18
pgb-1-2-32-32-2                       65                                      21                                               0                         17                                     17

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
