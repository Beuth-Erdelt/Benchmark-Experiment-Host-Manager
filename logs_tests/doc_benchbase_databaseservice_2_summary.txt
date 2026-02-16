## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 928s 
    Code: 1770025008
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is skipped.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1770025008
DBS-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1770025008

### Execution

#### Per Pod
                  experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                              
DBS-1-1-1024-1-1               1         16   16384       1      1  300.0           0                   4236.779164                4218.015834         0.0                                                       8145.0                                               3774.0
DBS-1-1-1024-2-1               1          8    8192       2      1  300.0           3                   1947.856369                1928.746372         0.0                                                       9277.0                                               4103.0
DBS-1-1-1024-2-2               1          8    8192       2      2  300.0           2                   1959.836444                1940.699779         0.0                                                       9306.0                                               4078.0

#### Aggregated Parallel
                experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DBS-1-1-1024-1               1         16   16384          1  300.0           0                       4236.78                    4218.02         0.0                                                       8145.0                                               3774.0
DBS-1-1-1024-2               1         16   16384          2  300.0           5                       3907.69                    3869.45         0.0                                                       9306.0                                               4090.5

### Workflow

#### Actual
DBMS DBS-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS DBS-1-1-1024 - Pods [[1, 2]]

### Loading
                time_load  terminals  pods  Throughput [SF/h]
DBS-1-1-1024-1          0          1     1                inf
DBS-1-1-1024-2          0          1     2                inf

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
