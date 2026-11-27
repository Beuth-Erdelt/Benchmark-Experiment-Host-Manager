## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 552s 
* Code: 1795631757
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * disk:1248497
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* pgduckdb-1-1-2-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* pgduckdb-1-1-2-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* pgduckdb-1-1-3-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* pgduckdb-1-1-3-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* pgduckdb-1-1-3-1-3 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* pgduckdb-1-1-3-1-4 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248497
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-3-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-3-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-3-1-3 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757
* postgresql-1-1-3-1-4 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1248498
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:1.2T
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
    * code:1795631757

### Ingestion
* PgDuckDB-1: 8 of 8 units ok
* PostgreSQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-pgduckdb-1-1795631757-84fccb858-r2vl2: 0
* bexhoma-sut-postgresql-1-1795631757-f8f54d47f-75c2c: 0

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
| PgDuckDB-1-1   |                1 |    1 |       48.00 |           3.00 |            0.00 |         27.00 |           16.00 |              1 |         0 |             | None           |             0 | False         |               75.00 | False               |
| PostgreSQL-1-1 |                1 |    1 |       57.00 |           3.00 |            0.00 |         33.00 |           19.00 |              1 |         0 |             | None           |             0 | False         |               63.16 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1-1-1   | pgduckdb-1-1-1   | pgduckdb-1-1-1-1   |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         21 |            0.69 |             5232.87 |           3771.43 |          -1 |
| pgduckdb-1-1-2-1-1   | pgduckdb-1-1-2   | pgduckdb-1-1-2-1   |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         28 |            0.95 |             3792.13 |           2828.57 |          -1 |
| pgduckdb-1-1-2-1-2   | pgduckdb-1-1-2   | pgduckdb-1-1-2-1   |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         27 |            0.97 |             3711.01 |           2933.33 |          -1 |
| pgduckdb-1-1-3-1-1   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       1 | 1.00 |               22 |                  22 |         55 |            1.82 |             1975.33 |           1440.00 |          -1 |
| pgduckdb-1-1-3-1-2   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       2 | 1.00 |               22 |                  22 |         57 |            1.76 |             2046.14 |           1389.47 |          -1 |
| pgduckdb-1-1-3-1-3   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       3 | 1.00 |               22 |                  22 |         56 |            1.81 |             1990.02 |           1414.29 |          -1 |
| pgduckdb-1-1-3-1-4   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       4 | 1.00 |               22 |                  22 |         57 |            1.72 |             2089.01 |           1389.47 |          -1 |
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         12 |            0.25 |            14570.41 |           6600.00 |          -1 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         17 |            0.34 |            10494.59 |           4658.82 |          -1 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         17 |            0.33 |            10950.35 |           4658.82 |          -1 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       1 | 1.00 |               22 |                  22 |         30 |            0.50 |             7206.30 |           2640.00 |          -1 |
| postgresql-1-1-3-1-2 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       2 | 1.00 |               22 |                  22 |         32 |            0.56 |             6410.04 |           2475.00 |          -1 |
| postgresql-1-1-3-1-3 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       3 | 1.00 |               22 |                  22 |         32 |            0.56 |             6381.38 |           2475.00 |          -1 |
| postgresql-1-1-3-1-4 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       4 | 1.00 |               22 |                  22 |         35 |            0.61 |             5935.25 |           2262.86 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1   | pgduckdb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.69 |             5232.87 |           3771.43 |          -1 |
| pgduckdb-1-1-2   | pgduckdb-1-1-2   |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         28 |            0.96 |             3751.35 |           5657.14 |          -1 |
| pgduckdb-1-1-3   | pgduckdb-1-1-3   |                1 |        3 |               1 |           4 | 1.00 |               88 |                  88 |         57 |            1.78 |             2024.62 |           5557.89 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         12 |            0.25 |            14570.41 |           6600.00 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         17 |            0.34 |            10720.05 |           9317.65 |          -1 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        3 |               1 |           4 | 1.00 |               88 |                  88 |         35 |            0.56 |             6467.43 |           9051.43 |          -1 |

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
| Pricing Summary Report (TPC-H Q1)                   |              1193.57 |              1611.78 |              1784.63 |              2989.09 |              3607.51 |              3301.39 |              3071.48 |                1146.36 |                2573.57 |                2731.09 |                3511.12 |                3562.01 |                3626.83 |                9175.27 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               346.90 |               391.31 |               370.00 |              1305.07 |               630.21 |              1000.59 |              1198.84 |                 177.02 |                 320.12 |                 212.77 |                 190.92 |                 326.85 |                 220.48 |                 663.63 |
| Shipping Priority (TPC-H Q3)                        |              1175.89 |              1194.01 |               918.24 |              1870.73 |              1831.01 |              1944.71 |              1941.37 |                 253.54 |                 273.69 |                 323.52 |                1137.70 |                1075.10 |                 998.82 |                 758.69 |
| Order Priority Checking Query (TPC-H Q4)            |               689.52 |              1395.90 |              1603.73 |              2160.86 |              2613.15 |              2501.03 |              2313.94 |                 286.38 |                 148.31 |                 232.66 |                 151.54 |                 200.55 |                 181.00 |                 364.46 |
| Local Supplier Volume (TPC-H Q5)                    |              1035.42 |              1499.75 |              1430.82 |              3290.52 |              3026.27 |              2913.10 |              3295.58 |                 296.93 |                 409.70 |                 419.36 |                 461.91 |                 438.45 |                 424.97 |                 651.37 |
| Forecasting Revenue Change (TPC-H Q6)               |               470.92 |               649.35 |               619.48 |               559.08 |              1289.07 |              1288.67 |              1288.60 |                 169.08 |                 300.09 |                 391.30 |                 508.38 |                 508.62 |                 474.95 |                 293.69 |
| Volume Shipping Query (TPC-H Q7)                    |               691.69 |              1523.73 |              1343.18 |              1430.80 |              2681.95 |              1980.22 |              2650.54 |                 274.88 |                 390.70 |                 504.33 |                 557.27 |                 586.79 |                 539.08 |                 722.03 |
| National Market Share (TPC-H Q8)                    |              1466.88 |              1582.88 |              1690.21 |              3567.22 |              3162.01 |              2632.63 |              3061.67 |                 154.86 |                 413.00 |                 174.25 |                 192.92 |                 240.27 |                 240.41 |                 567.46 |
| Product Type Profit Measure (TPC-H Q9)              |              1348.59 |              2125.53 |              2160.42 |              3373.87 |              4591.12 |              4122.41 |              4393.79 |                 365.22 |                 501.86 |                 846.61 |                1549.39 |                1590.48 |                1548.80 |                 683.60 |
| Returned Item Reporting Query (TPC-H Q10)           |               675.61 |               931.34 |               885.64 |              2936.34 |              1573.31 |              2039.48 |              1766.65 |                 206.14 |                 359.67 |                 220.04 |                 741.76 |                 729.77 |                 441.75 |                 859.98 |
| Important Stock Identification (TPC-H Q11)          |               223.50 |               268.75 |               375.04 |               625.92 |              1316.67 |               694.57 |               625.25 |                  61.21 |                  61.71 |                  62.91 |                  52.35 |                  53.52 |                 185.95 |                 255.52 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               661.40 |               872.67 |               849.41 |              1677.75 |              1379.66 |              2409.85 |              2364.67 |                 307.01 |                 529.25 |                 336.54 |                1078.89 |                 617.53 |                 541.56 |                 866.26 |
| Customer Distribution (TPC-H Q13)                   |               269.86 |               411.36 |               350.21 |              1488.30 |               615.25 |               675.70 |               276.72 |                 631.75 |                 716.88 |                 748.75 |                 738.81 |                 952.23 |                1119.37 |                2506.69 |
| Promotion Effect Query (TPC-H Q14)                  |              1083.49 |              1495.99 |              1538.39 |              1478.37 |              3132.79 |              2093.40 |              3048.38 |                 265.70 |                 312.43 |                 386.39 |                 647.99 |                 668.41 |                 623.70 |                1053.75 |
| Top Supplier Query (TPC-H Q15)                      |               784.49 |              1004.60 |               894.22 |              1203.98 |              1304.98 |              2257.42 |              1489.99 |                 198.23 |                 253.61 |                 319.92 |                 572.75 |                 577.36 |                 588.84 |                1597.64 |
| Parts/Supplier Relationship (TPC-H Q16)             |               305.23 |               331.25 |               413.74 |               808.84 |               655.65 |               535.70 |               474.47 |                 160.66 |                 266.00 |                 175.68 |                 308.31 |                 342.79 |                 406.73 |                 582.30 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1342.17 |              2753.84 |              2130.96 |              4150.93 |              4130.16 |              3791.65 |              4054.83 |                 556.89 |                 899.09 |                 701.78 |                1266.93 |                1436.88 |                1437.14 |                1088.05 |
| Large Volume Customer (TPC-H Q18)                   |               538.59 |               886.69 |              1237.14 |              2083.11 |              2475.78 |              1554.52 |              1841.12 |                2993.18 |                4985.78 |                4839.91 |                8164.08 |                8335.75 |                8163.33 |                3801.49 |
| Discounted Revenue (TPC-H Q19)                      |               574.55 |              1178.48 |               973.86 |              1714.36 |              1565.64 |              2338.67 |              2146.48 |                  41.60 |                  41.02 |                  47.97 |                 147.40 |                 102.69 |                 101.44 |                  43.97 |
| Potential Part Promotion (TPC-H Q20)                |               778.75 |               940.15 |              1262.86 |              2676.83 |              1851.47 |              1865.66 |              1679.01 |                 108.68 |                 154.74 |                 141.40 |                 204.54 |                 157.63 |                 158.31 |                 103.05 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |              2455.26 |              2583.75 |              2627.92 |              5807.33 |              5305.79 |              5841.05 |              5605.09 |                 290.86 |                 317.68 |                 357.47 |                 346.17 |                1082.68 |                1078.07 |                 294.65 |
| Global Sales Opportunity Query (TPC-H Q22)          |               214.61 |               194.13 |               253.10 |               713.58 |               204.20 |               405.54 |               269.35 |                  84.05 |                 112.14 |                  70.57 |                 135.33 |                 384.02 |                 383.42 |                  71.71 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   |        13.92 |      0.32 |           0.51 |                  1.72 |
| pgduckdb-1-1-2-1   |        13.92 |      0.32 |           0.51 |                  1.72 |
| pgduckdb-1-1-3-1   |        13.92 |      0.32 |           0.51 |                  1.72 |
| postgresql-1-1-1-1 |        26.20 |      0.40 |           1.73 |                  3.28 |
| postgresql-1-1-2-1 |        26.20 |      0.40 |           1.73 |                  3.28 |
| postgresql-1-1-3-1 |        26.20 |      0.40 |           1.73 |                  3.28 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |         0 |           0.00 |                  0.00 |
| pgduckdb-1-1-2-1   | n/a          |         0 |           0.00 |                  0.00 |
| pgduckdb-1-1-3-1   | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |
| postgresql-1-1-3-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.08 |
| pgduckdb-1-1-2-1   | n/a          |      0.00 |           0.00 |                  0.08 |
| pgduckdb-1-1-3-1   | n/a          |      0.00 |           0.00 |                  0.08 |
| postgresql-1-1-1-1 | n/a          |      0.44 |           0.00 |                  0.65 |
| postgresql-1-1-2-1 | n/a          |      0.44 |           0.00 |                  0.65 |
| postgresql-1-1-3-1 | n/a          |      0.44 |           0.00 |                  0.65 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.61 |           1.75 |                  3.38 |
| pgduckdb-1-1-2-1   | n/a          |      2.10 |           1.83 |                  3.47 |
| pgduckdb-1-1-3-1   | 121.63       |      3.97 |           2.01 |                  3.66 |
| postgresql-1-1-1-1 | n/a          |      0.25 |           1.84 |                  3.47 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           1.89 |                  3.52 |
| postgresql-1-1-3-1 | 7.05         |      0.25 |           2.11 |                  3.74 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           0.31 |                  0.31 |
| pgduckdb-1-1-2-1   | n/a          |      0.00 |           0.33 |                  0.34 |
| pgduckdb-1-1-3-1   | 50.48        |      0.03 |           0.33 |                  0.33 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.28 |                  0.28 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-3-1 | 39.97        |      1.38 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
