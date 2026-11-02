## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2361s 
* Code: 1793606617
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29, cl-worker39.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 4 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845869
  * datadisk:58
  * volume_size:49G
  * volume_used:58M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:845869
    * datadisk:15445
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587233
    * datadisk:15422
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:252927
    * datadisk:15448
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:589739
    * datadisk:15446
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793606617
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
    * COLUMNAR:False
* citus-1-1-2-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845870
  * datadisk:58
  * volume_size:49G
  * volume_used:58M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:845870
    * datadisk:15445
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587234
    * datadisk:15422
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:252930
    * datadisk:15448
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:589739
    * datadisk:15446
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793606617
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
    * COLUMNAR:False
* citus-1-2-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845875
  * datadisk:58
  * volume_size:49G
  * volume_used:58M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:845875
    * datadisk:15445
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587236
    * datadisk:15422
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:252931
    * datadisk:15448
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:589740
    * datadisk:15446
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793606617
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
    * COLUMNAR:False
    * ddl_num_worker_shards:48
* citus-1-2-2-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845876
  * datadisk:58
  * volume_size:49G
  * volume_used:58M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:845876
    * datadisk:15445
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587237
    * datadisk:15422
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:252936
    * datadisk:15448
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:589740
    * datadisk:15446
    * volume_size:49G
    * volume_used:16G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793606617
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
    * COLUMNAR:False
    * ddl_num_worker_shards:48

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Citus-1-2

### Data Parameters of Reused Volumes
* Citus-1: DDL values of the volume: num_worker_shards=48, columnar_compression=default
* Citus-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-citus-1-1793606617-c96794cd8-dsz29: 0
* bx-w-citus-nvme-tpch-10-0: 0
* bx-w-citus-nvme-tpch-10-1: 0
* bx-w-citus-nvme-tpch-10-2: 0
* bx-w-citus-nvme-tpch-10-3: 0
* bexhoma-sut-citus-1-1793606617-64c67fb66c-hrgjb: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS Citus-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS Citus-1 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS Citus-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS Citus-1 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |   10 |      195.00 |           4.00 |           21.00 |         97.00 |           66.00 |              8 |           0 |             | None           |             0 | False         |              184.62 | False               |
| Citus-1-2 |                2 |   10 |      195.00 |           4.00 |           21.00 |         97.00 |           66.00 |              8 |           0 |             | None           |             0 | False         |              184.62 | True                |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| citus-1-1-1-1-1 | Citus-1         | citus-1-1-1 | citus-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         70 |            1.10 |            33976.15 |          11314.29 |          -1 | citus-1-1-1-1-1 |
| citus-1-1-2-1-1 | Citus-1         | citus-1-1-2 | citus-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               22 |                  22 |         70 |            1.12 |            33165.08 |          11314.29 |          -1 | citus-1-1-2-1-1 |
| citus-1-2-1-1-1 | Citus-1         | citus-1-2-1 | citus-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |        153 |            1.79 |            20822.00 |           5176.47 |          -1 | citus-1-2-1-1-1 |
| citus-1-2-2-1-1 | Citus-1         | citus-1-2-2 | citus-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               22 |                  22 |         70 |            1.08 |            34159.10 |          11314.29 |          -1 | citus-1-2-2-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         70 |            1.10 |            33976.15 |          11314.29 |          -1 |
| citus-1-1-2 | citus-1-1-2 |                1 |        2 |               1 |           1 | 10.00 |               22 |                  22 |         70 |            1.12 |            33165.08 |          11314.29 |          -1 |
| citus-1-2-1 | citus-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |        153 |            1.79 |            20822.00 |           5176.47 |          -1 |
| citus-1-2-2 | citus-1-2-2 |                2 |        2 |               1 |           1 | 10.00 |               22 |                  22 |         70 |            1.08 |            34159.10 |          11314.29 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| citus-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| citus-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| citus-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| citus-1-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   citus-1-1-1-1-1 |   citus-1-1-2-1-1 |   citus-1-2-1-1-1 |   citus-1-2-2-1-1 |
|:----------------------------------------------------|------------------:|------------------:|------------------:|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            699.68 |            720.15 |           3264.52 |            725.36 |
| Minimum Cost Supplier Query (TPC-H Q2)              |           2577.90 |           2942.86 |          64062.74 |           2302.91 |
| Shipping Priority (TPC-H Q3)                        |           2409.22 |           2575.34 |           3350.42 |           2326.55 |
| Order Priority Checking Query (TPC-H Q4)            |            189.27 |            202.50 |            227.34 |            202.54 |
| Local Supplier Volume (TPC-H Q5)                    |            788.69 |            822.28 |            846.22 |            847.85 |
| Forecasting Revenue Change (TPC-H Q6)               |            165.45 |            165.69 |            267.39 |            144.15 |
| Volume Shipping Query (TPC-H Q7)                    |            651.43 |            680.96 |           1128.75 |            661.23 |
| National Market Share (TPC-H Q8)                    |            697.96 |            655.42 |           1933.00 |            683.42 |
| Product Type Profit Measure (TPC-H Q9)              |           1377.36 |           1329.82 |          16196.77 |           1311.66 |
| Returned Item Reporting Query (TPC-H Q10)           |           1036.65 |           1088.99 |           1049.90 |           1045.25 |
| Important Stock Identification (TPC-H Q11)          |            557.77 |            499.57 |            457.62 |            539.29 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            675.02 |            663.95 |            487.87 |            502.81 |
| Customer Distribution (TPC-H Q13)                   |           7532.11 |           8080.42 |           6601.63 |           6507.05 |
| Promotion Effect Query (TPC-H Q14)                  |            291.95 |            281.91 |            559.89 |            315.54 |
| Top Supplier Query (TPC-H Q15)                      |           1098.48 |           1099.88 |           1790.98 |           1095.64 |
| Parts/Supplier Relationship (TPC-H Q16)             |           1000.12 |           1197.40 |           1194.41 |           1515.55 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |          33014.24 |          30962.81 |          30557.13 |          31298.88 |
| Large Volume Customer (TPC-H Q18)                   |            662.19 |            675.66 |            656.25 |            646.61 |
| Discounted Revenue (TPC-H Q19)                      |            666.62 |            669.94 |            653.93 |            657.85 |
| Potential Part Promotion (TPC-H Q20)                |           1067.01 |           1117.38 |           1513.89 |           1107.66 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            516.98 |            523.64 |            543.58 |            511.97 |
| Global Sales Opportunity Query (TPC-H Q22)          |           7010.23 |           7651.18 |           6684.05 |           7627.79 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                 |   Pricing Summary Report (TPC-H Q1) |   Minimum Cost Supplier Query (TPC-H Q2) |   Shipping Priority (TPC-H Q3) |   Order Priority Checking Query (TPC-H Q4) |   Local Supplier Volume (TPC-H Q5) |   Forecasting Revenue Change (TPC-H Q6) |   Volume Shipping Query (TPC-H Q7) |   National Market Share (TPC-H Q8) |   Product Type Profit Measure (TPC-H Q9) |   Returned Item Reporting Query (TPC-H Q10) |   Important Stock Identification (TPC-H Q11) |   Shipping Modes and Order Priority (TPC-H Q12) |   Customer Distribution (TPC-H Q13) |   Promotion Effect Query (TPC-H Q14) |   Top Supplier Query (TPC-H Q15) |   Parts/Supplier Relationship (TPC-H Q16) |   Small-Quantity-Order Revenue (TPC-H Q17) |   Large Volume Customer (TPC-H Q18) |   Discounted Revenue (TPC-H Q19) |   Potential Part Promotion (TPC-H Q20) |   Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |   Global Sales Opportunity Query (TPC-H Q22) |
|:----------------|------------------------------------:|-----------------------------------------:|-------------------------------:|-------------------------------------------:|-----------------------------------:|----------------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------------:|--------------------------------------------:|---------------------------------------------:|------------------------------------------------:|------------------------------------:|-------------------------------------:|---------------------------------:|------------------------------------------:|-------------------------------------------:|------------------------------------:|---------------------------------:|---------------------------------------:|------------------------------------------------------:|---------------------------------------------:|
| citus-1-1-1-1-1 |                                0.00 |                                     0.00 |                           0.00 |                                       0.00 |                               0.00 |                                    0.00 |                               0.00 |                               0.00 |                                     0.00 |                                        0.00 |                                         0.00 |                                            0.00 |                                0.00 |                                 0.00 |                             0.00 |                                      0.00 |                                       0.00 |                                0.00 |                             0.00 |                                   0.00 |                                                  0.00 |                                         1.00 |
| citus-1-1-2-1-1 |                                0.00 |                                     0.00 |                           0.00 |                                       0.00 |                               0.00 |                                    0.00 |                               0.00 |                               0.00 |                                     0.00 |                                        0.00 |                                         0.00 |                                            0.00 |                                0.00 |                                 0.00 |                             0.00 |                                      0.00 |                                       0.00 |                                0.00 |                             0.00 |                                   0.00 |                                                  0.00 |                                         1.00 |
| citus-1-2-2-1-1 |                                0.00 |                                     0.00 |                           0.00 |                                       0.00 |                               0.00 |                                    0.00 |                               0.00 |                               0.00 |                                     0.00 |                                        0.00 |                                         0.00 |                                            0.00 |                                0.00 |                                 0.00 |                             0.00 |                                      0.00 |                                       0.00 |                                0.00 |                             0.00 |                                   0.00 |                                                  0.00 |                                         1.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       238.89 |      2.94 |           1.70 |                  1.74 |
| citus-1-1-2-1 |       238.89 |      2.94 |           1.70 |                  1.74 |

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      1466.58 |     12.79 |          30.14 |                 84.49 |
| citus-1-1-2-1 |      1466.58 |     12.79 |          30.14 |                 84.49 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| citus-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| citus-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       156.38 |      2.28 |           0.01 |                  1.30 |
| citus-1-1-2-1 |       156.38 |      2.28 |           0.01 |                  1.30 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |        35.51 |      1.00 |           0.79 |                  3.83 |
| citus-1-1-2-1 |        40.00 |      0.93 |           0.65 |                  0.82 |
| citus-1-2-1-1 |        38.13 |      0.94 |           0.78 |                  3.77 |
| citus-1-2-2-1 |        31.27 |      0.82 |           0.78 |                  3.75 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       578.20 |     14.93 |          35.91 |                 96.21 |
| citus-1-1-2-1 |       531.53 |     12.35 |          35.96 |                 96.24 |
| citus-1-2-1-1 |       849.11 |     15.47 |          28.89 |                 52.31 |
| citus-1-2-2-1 |       584.69 |     13.54 |          29.30 |                 52.99 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |        17.56 |      0.11 |           0.36 |                  0.37 |
| citus-1-1-2-1 |        18.04 |      0.15 |           0.39 |                  0.40 |
| citus-1-2-1-1 |        18.74 |      0.41 |           0.38 |                  0.38 |
| citus-1-2-2-1 |        17.03 |      0.53 |           0.35 |                  0.36 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
