## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1135s 
    Code: 1772191469
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-64-8-65536-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146882
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:249967
        cpu_list:0-55
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1080119
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:171801
        cpu_list:0-95
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1772191469
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   25343.635368                40343.0             1000000                              6345.0

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1               1       64   65536          1           0                       64716.12               154521.0           5001448                            1048.0             4998552                              3195.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      555.15     5.98          0.73                 0.76

### Loading phase: component worker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      338.47     4.77          2.86                 5.37

### Loading phase: component loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      122.55        0          0.12                 0.12

### Execution phase: SUT deployment
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1        0.29      0.0          0.53                 0.57

### Execution phase: component worker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     3086.07    26.73          5.54                 9.79

### Execution phase: component benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      753.73     5.26          0.15                 0.15

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
