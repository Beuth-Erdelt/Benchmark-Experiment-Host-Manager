## Show Summary

### Workload
Benchbase Workload tpcc SF=128
    Type: benchbase
    Duration: 9376s 
    Code: 1772245192
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-1-1-1024-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146846
    volume_size:100.0G
    volume_used:40.0M
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
        disk:297743
        volume_size:100.0G
        volume_used:6.3G
        cpu_list:0-55
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1084221
        volume_size:100.0G
        volume_used:6.3G
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:381108
        volume_size:100.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:172614
        volume_size:100.0G
        volume_used:6.3G
        cpu_list:0-95
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
                code:1772245192
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146846
    volume_size:100.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:297748
        volume_size:100.0G
        volume_used:9.2G
        cpu_list:0-55
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1084228
        volume_size:100.0G
        volume_used:7.0G
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:381111
        volume_size:100.0G
        volume_used:6.4G
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:172610
        volume_size:100.0G
        volume_used:7.4G
        cpu_list:0-95
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
                code:1772245192
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-3 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146846
    volume_size:100.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:297745
        volume_size:100.0G
        volume_used:9.2G
        cpu_list:0-55
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1084245
        volume_size:100.0G
        volume_used:7.0G
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:381115
        volume_size:100.0G
        volume_used:6.4G
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:172613
        volume_size:100.0G
        volume_used:7.4G
        cpu_list:0-95
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
                code:1772245192
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-4 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146846
    volume_size:100.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:297756
        volume_size:100.0G
        volume_used:12.2G
        cpu_list:0-55
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1084245
        volume_size:100.0G
        volume_used:8.8G
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:381118
        volume_size:100.0G
        volume_used:7.9G
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:172618
        volume_size:100.0G
        volume_used:8.9G
        cpu_list:0-95
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
                code:1772245192
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                 
Citus-1-1-1024-1-1               1         64   16384       1      1  1200.0           0                    379.985815                 378.292482         0.0                                                     689527.0                                             168395.0
Citus-1-1-1024-2-1               1         32    8192       2      1  1200.0           0                    167.215821                 166.161654         0.0                                                     809496.0                                             191310.0
Citus-1-1-1024-2-2               1         32    8192       2      2  1200.0           0                    167.513323                 166.522490         0.0                                                     808014.0                                             190991.0
Citus-1-1-1024-3-4               1         16    4096       3      1  1200.0           2                     64.218328                  63.666661         0.0                                                    1069727.0                                             249069.0
Citus-1-1-1024-3-3               1         16    4096       3      2  1200.0           1                     64.500832                  63.968332         0.0                                                    1075186.0                                             248025.0
Citus-1-1-1024-3-1               1         16    4096       3      3  1200.0           1                     63.514166                  63.015832         0.0                                                    1080208.0                                             251851.0
Citus-1-1-1024-3-2               1         16    4096       3      4  1200.0           0                     64.279989                  63.782489         0.0                                                    1073335.0                                             248770.0
Citus-1-1-1024-4-1               1          8    2048       4      1  1200.0           0                     24.930829                  24.715830         0.0                                                    1290364.0                                             320441.0
Citus-1-1-1024-4-6               1          8    2048       4      2  1200.0           0                     24.044999                  23.839999         0.0                                                    1345406.0                                             332389.0
Citus-1-1-1024-4-4               1          8    2048       4      3  1200.0           0                     24.794996                  24.584996         0.0                                                    1268360.0                                             322328.0
Citus-1-1-1024-4-7               1          8    2048       4      4  1200.0           0                     24.617498                  24.399998         0.0                                                    1291460.0                                             324554.0
Citus-1-1-1024-4-5               1          8    2048       4      5  1200.0           0                     23.527494                  23.294161         0.0                                                    1343290.0                                             339460.0
Citus-1-1-1024-4-8               1          8    2048       4      6  1200.0           0                     23.969994                  23.746660         0.0                                                    1352663.0                                             333206.0
Citus-1-1-1024-4-2               1          8    2048       4      7  1200.0           1                     24.656662                  24.418329         0.0                                                    1310620.0                                             324153.0
Citus-1-1-1024-4-3               1          8    2048       4      8  1200.0           0                     25.194162                  24.979162         0.0                                                    1262385.0                                             317346.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         64   16384          1  1200.0           0                        379.99                     378.29         0.0                                                     689527.0                                            168395.00
Citus-1-1-1024-2               1         64   16384          2  1200.0           0                        334.73                     332.68         0.0                                                     809496.0                                            191150.50
Citus-1-1-1024-3               1         64   16384          4  1200.0           4                        256.51                     254.43         0.0                                                    1080208.0                                            249428.75
Citus-1-1-1024-4               1         64   16384          8  1200.0           1                        195.74                     193.98         0.0                                                    1352663.0                                            326734.62

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
Citus-1-1-1024-1     2785.0        1.0   1.0          165.45781
Citus-1-1-1024-2     2785.0        1.0   2.0          165.45781
Citus-1-1-1024-3     2785.0        1.0   4.0          165.45781
Citus-1-1-1024-4     2785.0        1.0   8.0          165.45781

### Monitoring

### Loading phase: SUT deployment
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     4030.64     2.24          0.99                 1.02
Citus-1-1-1024-2     4030.64     2.24          0.99                 1.02
Citus-1-1-1024-3     4030.64     2.24          0.99                 1.02
Citus-1-1-1024-4     4030.64     2.24          0.99                 1.02

### Loading phase: component worker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     4142.05     2.62         14.79                44.28
Citus-1-1-1024-2     4142.05     2.62         14.79                44.28
Citus-1-1-1024-3     4142.05     2.62         14.79                44.28
Citus-1-1-1024-4     4142.05     2.62         14.79                44.28

### Loading phase: component loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     8679.02    12.24           0.3                  0.3
Citus-1-1-1024-2     8679.02    12.24           0.3                  0.3
Citus-1-1-1024-3     8679.02    12.24           0.3                  0.3
Citus-1-1-1024-4     8679.02    12.24           0.3                  0.3

### Execution phase: SUT deployment
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     3936.25     4.81          0.83                 0.90
Citus-1-1-1024-2     3340.04     4.31          0.83                 0.91
Citus-1-1-1024-3     2471.61     4.36          0.83                 0.93
Citus-1-1-1024-4     1762.46     2.49          0.83                 0.93

### Execution phase: component worker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     3361.10     3.91         17.34                51.55
Citus-1-1-1024-2     3198.11     3.68         17.76                53.30
Citus-1-1-1024-3     2298.78     3.11         17.98                54.02
Citus-1-1-1024-4     1713.80     2.28         18.10                54.27

### Execution phase: component benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1      745.87     0.82          0.38                 0.38
Citus-1-1-1024-2      745.87     0.86          0.38                 0.38
Citus-1-1-1024-3      730.88     0.81          0.33                 0.33
Citus-1-1-1024-4      628.17     1.28          0.29                 0.29

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
