## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1779s 
    Code: 1769437461
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95723
    datadisk:4307
    volume_size:30G
    volume_used:4.3G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1769437461
                TENANT_VOL:False
PostgreSQL-1-1-1024-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95723
    datadisk:4470
    volume_size:30G
    volume_used:4.4G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1769437461
                TENANT_VOL:False

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-1-1-1               1        160   16384       1      1  300.0           1                    357.013305                 354.759972         0.0                                                    2130851.0                                             447939.0
PostgreSQL-1-1-1024-2-1-1               2        160   16384       1      1  300.0           0                    357.849976                 355.299976         0.0                                                    1998059.0                                             446722.0

#### Aggregated Parallel
                         experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1        160   16384          1  300.0           1                        357.01                     354.76         0.0                                                    2130851.0                                             447939.0
PostgreSQL-1-1-1024-2-1               2        160   16384          1  300.0           0                        357.85                     355.30         0.0                                                    1998059.0                                             446722.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      626.0        1.0   1.0           92.01278
PostgreSQL-1-1-1024-2-1      626.0        1.0   1.0           92.01278

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
