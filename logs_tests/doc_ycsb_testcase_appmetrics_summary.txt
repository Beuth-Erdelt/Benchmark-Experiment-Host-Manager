## Show Summary

### Workload
YCSB SF=3
    Type: ycsb
    Duration: 5801s 
    Code: 1771351887
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 3000000.
    Ordering of inserts is hashed.
    Number of operations is 3000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:105993
    datadisk:7090
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1771351887
PostgreSQL-64-8-65536-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:107451
    datadisk:8549
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1771351887
PostgreSQL-64-8-65536-3 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:108433
    datadisk:9530
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1771351887
PostgreSQL-64-8-65536-4 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:109310
    datadisk:10407
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1771351887

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                    3298.366095               909645.0             3000000                             77455.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1           0                        2847.60              1053517.0           1498998                             847.0             1501002                            878591.0
PostgreSQL-64-8-65536-2               1       64   32768          8           0                        2862.28              1057291.0           1499498                             770.0             1500502                            902655.0
PostgreSQL-64-8-65536-3               1       64   49152          1           0                        2838.27              1056983.0           1499484                             756.0             1500516                            879103.0
PostgreSQL-64-8-65536-4               1       64   49152          8           0                        2848.42              1058915.0           1500611                             746.0             1499389                            912895.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8, 8, 1, 1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Monitoring

### Loading phase: SUT deployment
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1055.57     1.13          9.78                12.74
PostgreSQL-64-8-65536-2     1055.57     1.13          9.78                12.74
PostgreSQL-64-8-65536-3     1055.57     1.13          9.78                12.74
PostgreSQL-64-8-65536-4     1055.57     1.13          9.78                12.74

### Loading phase: component loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      432.97     0.51          0.11                 0.11
PostgreSQL-64-8-65536-2      432.97     0.51          0.11                 0.11
PostgreSQL-64-8-65536-3      432.97     0.51          0.11                 0.11
PostgreSQL-64-8-65536-4      432.97     0.51          0.11                 0.11

### Execution phase: SUT deployment
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      970.90     1.11         10.93                15.14
PostgreSQL-64-8-65536-2      897.92     0.94         11.37                15.99
PostgreSQL-64-8-65536-3      907.21     0.92         11.74                16.00
PostgreSQL-64-8-65536-4      912.15     0.90         12.11                16.00

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      271.50     0.28          0.13                 0.13
PostgreSQL-64-8-65536-2      269.54     0.54          0.12                 0.12
PostgreSQL-64-8-65536-3      286.73     0.40          0.13                 0.13
PostgreSQL-64-8-65536-4      264.12     0.50          0.13                 0.13

### Application Metrics

#### Loading phase: SUT deployment
                         Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-64-8-65536-1                             2.0                            64.0                              16.0                                 0.26                                 0.26
PostgreSQL-64-8-65536-2                             2.0                            64.0                              16.0                                 0.26                                 0.26
PostgreSQL-64-8-65536-3                             2.0                            64.0                              16.0                                 0.26                                 0.26
PostgreSQL-64-8-65536-4                             2.0                            64.0                              16.0                                 0.26                                 0.26

#### Execution phase: SUT deployment
                         Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-64-8-65536-1                             1.0                            35.0                              44.0                                 0.07                                 1.71
PostgreSQL-64-8-65536-2                             1.0                            35.0                              47.0                                 0.05                                 2.77
PostgreSQL-64-8-65536-3                             2.0                            33.0                              45.0                                 0.08                                 2.87
PostgreSQL-64-8-65536-4                             1.0                            32.0                              43.0                                 0.07                                 2.48

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
