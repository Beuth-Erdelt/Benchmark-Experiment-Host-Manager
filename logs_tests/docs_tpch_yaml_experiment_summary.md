## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 544s 
* Code: 1795351092
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.2.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL', 'PgDuckDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4] times the number of benchmarking pods.
  * Experiment is run once.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* pgduckdb-1-1-1-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948585
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* pgduckdb-1-1-2-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948585
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* pgduckdb-1-1-2-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948585
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* pgduckdb-1-1-3-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* pgduckdb-1-1-3-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* pgduckdb-1-1-3-1-3 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* pgduckdb-1-1-3-1-4 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948585
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948585
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948585
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-3-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-3-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-3-1-3 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092
* postgresql-1-1-3-1-4 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:948586
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:927G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795351092

### Ingestion
* PgDuckDB-1: 8 of 8 units ok
* PostgreSQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-pgduckdb-1-1795351092-557cfdd5dc-tkbts: 0
* bexhoma-sut-postgresql-1-1795351092-75ff8448db-2vvtj: 0

### Workflow

#### Actual

* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 3: tpch (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: tpch (4 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: tpch (4 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 3: tpch (4 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PgDuckDB-1-1   |                1 |    1 |       64.00 |           2.00 |            0.00 |         40.00 |           15.00 |              1 |         0 |             | None           |             0 | False         |               56.25 | False               |
| PostgreSQL-1-1 |                1 |    1 |       67.00 |           3.00 |            0.00 |         40.00 |           17.00 |              1 |         0 |             | None           |             0 | False         |               53.73 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1-1-1   | pgduckdb-1-1-1   | pgduckdb-1-1-1-1   |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         20 |            0.58 |             6250.63 |           3960.00 |          -1 |
| pgduckdb-1-1-2-1-1   | pgduckdb-1-1-2   | pgduckdb-1-1-2-1   |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         26 |            0.83 |             4339.71 |           3046.15 |          -1 |
| pgduckdb-1-1-2-1-2   | pgduckdb-1-1-2   | pgduckdb-1-1-2-1   |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         25 |            0.78 |             4635.65 |           3168.00 |          -1 |
| pgduckdb-1-1-3-1-1   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       1 | 1.00 |               22 |                  22 |         55 |            1.98 |             1815.77 |           1440.00 |          -1 |
| pgduckdb-1-1-3-1-2   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       2 | 1.00 |               22 |                  22 |         58 |            1.91 |             1888.67 |           1365.52 |          -1 |
| pgduckdb-1-1-3-1-3   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       3 | 1.00 |               22 |                  22 |         58 |            1.96 |             1841.31 |           1365.52 |          -1 |
| pgduckdb-1-1-3-1-4   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       4 | 1.00 |               22 |                  22 |         58 |            1.98 |             1822.20 |           1365.52 |          -1 |
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         23 |            0.25 |            14337.04 |           3443.48 |          -1 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         19 |            0.30 |            12054.45 |           4168.42 |          -1 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         19 |            0.28 |            12650.52 |           4168.42 |          -1 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       1 | 1.00 |               22 |                  22 |         25 |            0.56 |             6483.04 |           3168.00 |          -1 |
| postgresql-1-1-3-1-2 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       2 | 1.00 |               22 |                  22 |         31 |            0.55 |             6519.19 |           2554.84 |          -1 |
| postgresql-1-1-3-1-3 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       3 | 1.00 |               22 |                  22 |         30 |            0.60 |             6028.48 |           2640.00 |          -1 |
| postgresql-1-1-3-1-4 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       4 | 1.00 |               22 |                  22 |         26 |            0.59 |             6059.31 |           3046.15 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1   | pgduckdb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         20 |            0.58 |             6250.63 |           3960.00 |          -1 |
| pgduckdb-1-1-2   | pgduckdb-1-1-2   |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         26 |            0.80 |             4485.24 |           6092.31 |          -1 |
| pgduckdb-1-1-3   | pgduckdb-1-1-3   |                1 |        3 |               1 |           4 | 1.00 |               88 |                  88 |         58 |            1.95 |             1841.77 |           5462.07 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         23 |            0.25 |            14337.04 |           3443.48 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         19 |            0.29 |            12348.89 |           8336.84 |          -1 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        3 |               1 |           4 | 1.00 |               88 |                  88 |         31 |            0.57 |             6268.32 |          10219.35 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| pgduckdb-1-1-1   |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| pgduckdb-1-1-2   |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| pgduckdb-1-1-3   |      4 | 4/4                                 | 4/4                                      | 4/4                            | 4/4                                        | 4/4                                | 4/4                                     | 4/4                                | 4/4                                | 4/4                                      | 4/4                                         | 4/4                                          | 4/4                                             | 4/4                                 | 4/4                                  | 4/4                              | 4/4                                       | 4/4                                        | 4/4                                 | 4/4                              | 4/4                                    | 4/4                                                   | 4/4                                          | yes        |
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-1-3 |      4 | 4/4                                 | 4/4                                      | 4/4                            | 4/4                                        | 4/4                                | 4/4                                     | 4/4                                | 4/4                                | 4/4                                      | 4/4                                         | 4/4                                          | 4/4                                             | 4/4                                 | 4/4                                  | 4/4                              | 4/4                                       | 4/4                                        | 4/4                                 | 4/4                              | 4/4                                    | 4/4                                                   | 4/4                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   pgduckdb-1-1-1-1-1 |   pgduckdb-1-1-2-1-1 |   pgduckdb-1-1-2-1-2 |   pgduckdb-1-1-3-1-1 |   pgduckdb-1-1-3-1-2 |   pgduckdb-1-1-3-1-3 |   pgduckdb-1-1-3-1-4 |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-1-3-1-1 |   postgresql-1-1-3-1-2 |   postgresql-1-1-3-1-3 |   postgresql-1-1-3-1-4 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              1027.87 |              1569.07 |              1656.06 |              3336.86 |              4532.58 |              5265.92 |              5874.14 |                 929.10 |                1533.09 |                1495.48 |                2843.78 |                2818.89 |                8719.80 |                2820.25 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               290.59 |               333.49 |               293.74 |               975.80 |               922.37 |              1317.72 |              1792.05 |                 173.95 |                 174.58 |                 163.44 |                 206.36 |                 205.61 |                 546.63 |                 201.97 |
| Shipping Priority (TPC-H Q3)                        |               604.30 |               904.96 |               908.68 |              1889.71 |              2963.75 |              2418.67 |              2102.38 |                 238.43 |                 227.14 |                 221.49 |                1223.21 |                1215.49 |                 867.89 |                1234.40 |
| Order Priority Checking Query (TPC-H Q4)            |               655.24 |               982.81 |               874.49 |              2992.45 |              2096.25 |              2184.28 |              2285.70 |                 112.51 |                 212.17 |                 211.50 |                 584.72 |                 482.77 |                 361.73 |                 571.29 |
| Local Supplier Volume (TPC-H Q5)                    |              1108.49 |              1504.63 |              1168.59 |              3594.53 |              3891.86 |              4262.11 |              3694.65 |                 238.62 |                 295.86 |                 300.99 |                 207.22 |                 539.86 |                 293.57 |                 539.47 |
| Forecasting Revenue Change (TPC-H Q6)               |               601.54 |              1551.92 |               929.82 |              2672.19 |              2084.84 |              1928.67 |              1645.54 |                 154.87 |                 314.37 |                 311.38 |                 338.06 |                 488.88 |                 521.15 |                 488.67 |
| Volume Shipping Query (TPC-H Q7)                    |               612.22 |              1019.63 |              1751.97 |              1700.64 |              1675.21 |              1815.05 |              1645.87 |                 263.31 |                 350.03 |                 349.79 |                 657.78 |                 563.94 |                 849.09 |                 565.08 |
| National Market Share (TPC-H Q8)                    |               816.13 |              1370.69 |              1181.81 |              3059.62 |              3198.21 |              4026.10 |              3020.99 |                 496.89 |                 112.73 |                 113.22 |                 245.78 |                 283.15 |                 153.71 |                 282.39 |
| Product Type Profit Measure (TPC-H Q9)              |               899.63 |              1543.42 |              1018.58 |              4238.47 |              4548.20 |              3456.90 |              4458.88 |                 584.77 |                 800.30 |                 797.52 |                1125.77 |                2091.54 |                1082.93 |                 769.33 |
| Returned Item Reporting Query (TPC-H Q10)           |               632.72 |               789.60 |               891.05 |              2050.80 |              1604.49 |              1469.74 |              1685.91 |                 238.31 |                 348.60 |                 348.58 |                 338.82 |                 585.02 |                 851.07 |                 827.24 |
| Important Stock Identification (TPC-H Q11)          |               201.09 |               237.05 |               252.27 |               602.64 |               585.75 |              1244.91 |               613.18 |                  72.82 |                  59.95 |                  59.31 |                 416.80 |                  58.97 |                 286.37 |                 476.40 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               663.16 |               891.15 |               700.88 |              1654.04 |              2774.98 |              2071.20 |              2534.87 |                 221.23 |                 520.51 |                 523.37 |                 873.87 |                1760.55 |                 906.31 |                 585.48 |
| Customer Distribution (TPC-H Q13)                   |               242.53 |               263.66 |               357.05 |              1218.10 |               868.25 |               793.26 |               892.84 |                1099.03 |                 601.40 |                 603.05 |                1100.69 |                2062.18 |                2007.44 |                 689.66 |
| Promotion Effect Query (TPC-H Q14)                  |               559.22 |              1017.49 |               839.59 |              2614.07 |              2881.50 |              2744.98 |              2711.74 |                 310.63 |                 349.20 |                 350.17 |                 533.51 |                 594.78 |                 568.55 |                 532.88 |
| Top Supplier Query (TPC-H Q15)                      |               535.32 |              1282.48 |               790.97 |              2797.21 |              1857.54 |              1761.35 |              1895.58 |                 179.84 |                 373.40 |                 373.75 |                 527.16 |                 524.48 |                 578.60 |                 525.84 |
| Parts/Supplier Relationship (TPC-H Q16)             |               189.38 |               266.36 |               229.39 |               525.31 |               404.67 |               585.35 |               473.60 |                 132.45 |                 227.56 |                 145.46 |                 320.45 |                 483.08 |                 873.43 |                 318.98 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               990.88 |              1887.09 |              1527.89 |              4138.13 |              4393.11 |              4335.51 |              4528.35 |                 588.76 |                 505.66 |                 560.76 |                1032.19 |                2570.75 |                2200.91 |                1557.07 |
| Large Volume Customer (TPC-H Q18)                   |               514.71 |               866.48 |               739.78 |              1723.47 |              1865.94 |              1423.58 |              1672.32 |                3033.56 |                3968.95 |                4254.82 |                7799.21 |                6078.87 |                4828.12 |                7405.68 |
| Discounted Revenue (TPC-H Q19)                      |              1274.71 |               849.78 |               776.39 |              1702.63 |              1990.41 |              2346.06 |              1109.55 |                  39.77 |                  43.52 |                  33.81 |                 166.36 |                  40.20 |                  44.48 |                  87.99 |
| Potential Part Promotion (TPC-H Q20)                |               671.58 |              1063.80 |              1012.92 |              2062.18 |              1931.92 |              1871.97 |              2718.65 |                 113.91 |                 105.51 |                  74.24 |                 140.18 |                 117.82 |                 114.27 |                 377.87 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |              1656.53 |              1677.81 |              2452.36 |              5194.13 |              5991.52 |              5681.76 |              6302.79 |                 277.93 |                 598.62 |                 597.15 |                 651.77 |                 472.52 |                 508.33 |                 794.78 |
| Global Sales Opportunity Query (TPC-H Q22)          |               179.86 |               184.40 |               232.01 |               713.44 |               306.11 |               255.27 |               572.86 |                  72.73 |                  70.01 |                  65.24 |                 298.91 |                 107.14 |                 104.79 |                 188.16 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   |        22.93 |      0.37 |           1.68 |                  3.05 |
| pgduckdb-1-1-2-1   |        22.93 |      0.37 |           1.68 |                  3.05 |
| pgduckdb-1-1-3-1   |        22.93 |      0.37 |           1.68 |                  3.05 |
| postgresql-1-1-1-1 |        13.77 |      0.27 |           0.50 |                  1.72 |
| postgresql-1-1-2-1 |        13.77 |      0.27 |           0.50 |                  1.72 |
| postgresql-1-1-3-1 |        13.77 |      0.27 |           0.50 |                  1.72 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| pgduckdb-1-1-2-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| pgduckdb-1-1-3-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-3-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   |         4.07 |      0.00 |           0.00 |                  0.26 |
| pgduckdb-1-1-2-1   |         4.07 |      0.00 |           0.00 |                  0.26 |
| pgduckdb-1-1-3-1   |         4.07 |      0.00 |           0.00 |                  0.26 |
| postgresql-1-1-1-1 |         4.88 |      0.00 |           0.02 |                  0.37 |
| postgresql-1-1-2-1 |         4.88 |      0.00 |           0.02 |                  0.37 |
| postgresql-1-1-3-1 |         4.88 |      0.00 |           0.02 |                  0.37 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           1.75 |                  3.38 |
| pgduckdb-1-1-2-1   | n/a          |      1.55 |           1.85 |                  3.49 |
| pgduckdb-1-1-3-1   | 215.06       |      3.99 |           2.13 |                  3.77 |
| postgresql-1-1-1-1 | n/a          |      0.40 |           1.92 |                  3.55 |
| postgresql-1-1-2-1 | n/a          |      2.04 |           5.28 |                  6.91 |
| postgresql-1-1-3-1 | n/a          |      2.01 |           3.08 |                  4.71 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           0.01 |                  0.01 |
| pgduckdb-1-1-2-1   | n/a          |      0.00 |           0.01 |                  0.01 |
| pgduckdb-1-1-3-1   | 45.76        |      0.73 |           0.29 |                  0.29 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.29 |                  0.29 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.28 |                  0.28 |
| postgresql-1-1-3-1 | n/a          |      0.00 |           0.58 |                  0.58 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
Experiment                    : cleaning up per-connection artefacts
Experiment                    : cleaning up per-connection artefacts completed

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
