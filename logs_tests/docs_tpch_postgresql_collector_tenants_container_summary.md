## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1523s 
* Code: 1793589652
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Each query is repeated 3 times.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685317
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685315
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-2-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685317
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685315
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-2-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685316
  * datadisk:8188
  * volume_size:49G
  * volume_used:8.0G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793589652
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2, PostgreSQL-2-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* PostgreSQL-2: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-2: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793589652-f45bcf47-pp922: 0
* bexhoma-sut-postgresql-1-1793589652-7cccf94664-2z92d: 0
* bexhoma-sut-postgresql-2-1793589652-6dbccd459c-fz7md: 0
* bexhoma-sut-postgresql-2-1793589652-685dff56d6-8qfpd: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793589652-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    3 |      164.00 |           3.00 |            0.00 |        100.00 |           47.00 |              1 |           0 |               65.85 | False               |
| 1793589652-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    3 |      148.00 |           4.00 |            0.00 |        101.00 |           41.00 |              1 |           0 |               72.97 | False               |
| 1793589652-PostgreSQL-1-2-0 |                2 | container      | False         |             2 |           0 |    3 |      164.00 |           3.00 |            0.00 |        100.00 |           47.00 |              1 |           0 |               65.85 | True                |
| 1793589652-PostgreSQL-2-2-1 |                2 | container      | False         |             2 |           1 |    3 |      148.00 |           4.00 |            0.00 |        101.00 |           41.00 |              1 |           0 |               72.97 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.55 |            19770.00 |           9504.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.58 |            18616.59 |           9504.00 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         70 |            0.49 |            21977.43 |          10182.86 |           0 | postgresql-1-2-1-1-1 |
| postgresql-1-2-2-1-1 | PostgreSQL-1    | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.49 |            21993.84 |          11137.50 |           0 | postgresql-1-2-2-1-1 |
| postgresql-2-1-1-1-1 | PostgreSQL-2    | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         73 |            0.54 |            20155.28 |           9764.38 |           1 | postgresql-2-1-1-1-1 |
| postgresql-2-1-2-1-1 | PostgreSQL-2    | postgresql-2-1-2 | postgresql-2-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.58 |            18677.36 |           9632.43 |           1 | postgresql-2-1-2-1-1 |
| postgresql-2-2-1-1-1 | PostgreSQL-2    | postgresql-2-2-1 | postgresql-2-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.54 |            20151.14 |           9632.43 |           1 | postgresql-2-2-1-1-1 |
| postgresql-2-2-2-1-1 | PostgreSQL-2    | postgresql-2-2-2 | postgresql-2-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.53 |            20428.08 |          11137.50 |           1 | postgresql-2-2-2-1-1 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.55 |            19770.00 |           9504.00 |           0 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         75 |            0.58 |            18616.59 |           9504.00 |           0 |
| postgresql-1-2-1_0 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         70 |            0.49 |            21977.43 |          10182.86 |           0 |
| postgresql-1-2-2_0 | postgresql-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.49 |            21993.84 |          11137.50 |           0 |
| postgresql-2-1-1_1 | postgresql-2-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         73 |            0.54 |            20155.28 |           9764.38 |           1 |
| postgresql-2-1-2_1 | postgresql-2-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.58 |            18677.36 |           9632.43 |           1 |
| postgresql-2-2-1_1 | postgresql-2-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |                  66 |         74 |            0.54 |            20151.14 |           9632.43 |           1 |
| postgresql-2-2-2_1 | postgresql-2-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |                  66 |         64 |            0.53 |            20428.08 |          11137.50 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-2-1-1-1 |   postgresql-1-2-2-1-1 |   postgresql-2-1-1-1-1 |   postgresql-2-1-2-1-1 |   postgresql-2-2-1-1-1 |   postgresql-2-2-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                2007.84 |                1876.49 |                2612.66 |                1586.57 |                1919.04 |                1873.12 |                2650.72 |                1610.05 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 483.79 |                 453.74 |                1002.96 |                 405.08 |                 442.50 |                 459.69 |                1048.96 |                 474.99 |
| Shipping Priority (TPC-H Q3)                        |                 695.75 |                 511.68 |                 871.45 |                 482.71 |                 492.27 |                 508.37 |                 876.17 |                 504.29 |
| Order Priority Checking Query (TPC-H Q4)            |                 272.56 |                 250.14 |                 213.58 |                 231.95 |                 406.63 |                 253.71 |                 232.75 |                 241.55 |
| Local Supplier Volume (TPC-H Q5)                    |                 550.41 |                 541.77 |                 499.78 |                 524.00 |                 500.93 |                 535.52 |                 552.30 |                 536.01 |
| Forecasting Revenue Change (TPC-H Q6)               |                 304.81 |                 619.98 |                 272.64 |                 275.96 |                 287.24 |                 557.57 |                 296.09 |                 296.48 |
| Volume Shipping Query (TPC-H Q7)                    |                 781.06 |                 753.40 |                 561.94 |                 645.02 |                 892.83 |                 792.42 |                 661.39 |                 677.22 |
| National Market Share (TPC-H Q8)                    |                 304.47 |                 381.53 |                1277.79 |                 319.48 |                 340.26 |                 373.40 |                1352.42 |                 315.96 |
| Product Type Profit Measure (TPC-H Q9)              |                1096.93 |                1087.23 |                1100.55 |                 880.17 |                1424.19 |                1320.25 |                1345.38 |                1202.69 |
| Returned Item Reporting Query (TPC-H Q10)           |                 543.07 |                 555.67 |                 480.05 |                 533.36 |                 513.80 |                 523.12 |                 516.60 |                 520.58 |
| Important Stock Identification (TPC-H Q11)          |                 168.03 |                 174.55 |                 175.17 |                 155.80 |                 162.71 |                 169.37 |                 151.30 |                 173.46 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 473.51 |                 711.61 |                 420.52 |                 447.74 |                 522.55 |                 684.42 |                 461.55 |                 706.50 |
| Customer Distribution (TPC-H Q13)                   |                2419.29 |                1974.60 |                1774.16 |                2144.32 |                2020.53 |                1915.64 |                1848.96 |                1900.63 |
| Promotion Effect Query (TPC-H Q14)                  |                 523.54 |                 537.64 |                 443.93 |                 509.81 |                 600.63 |                 535.52 |                 491.75 |                 513.99 |
| Top Supplier Query (TPC-H Q15)                      |                 394.07 |                 407.07 |                 364.90 |                 399.58 |                 392.44 |                 407.06 |                 390.57 |                 396.44 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 435.71 |                 435.68 |                 350.23 |                 375.24 |                 352.72 |                 383.65 |                 381.57 |                 407.89 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                2100.31 |                1929.58 |                1462.54 |                1620.38 |                1922.89 |                1737.33 |                1641.60 |                1584.56 |
| Large Volume Customer (TPC-H Q18)                   |                9275.18 |                9170.14 |                7655.75 |                7964.89 |                8929.59 |                9118.33 |                7697.06 |                7567.51 |
| Discounted Revenue (TPC-H Q19)                      |                  97.59 |                  80.58 |                  69.43 |                  84.85 |                  78.68 |                  78.59 |                  84.34 |                  72.48 |
| Potential Part Promotion (TPC-H Q20)                |                 326.25 |                 279.82 |                 242.89 |                 308.73 |                 337.73 |                 314.68 |                 320.80 |                 341.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 618.77 |                 718.80 |                 458.32 |                 482.16 |                 545.14 |                 586.35 |                 507.18 |                 491.24 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 127.49 |                 213.90 |                 132.59 |                 124.71 |                 126.15 |                 300.56 |                 132.50 |                 130.63 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        56.04 |      0.81 |           4.61 |                  8.84 |
| postgresql-1-1-2-1 |        56.04 |      0.81 |           4.61 |                  8.84 |
| postgresql-2-1-1-1 |        91.35 |      1.69 |           5.18 |                  9.91 |
| postgresql-2-1-2-1 |        91.35 |      1.69 |           5.18 |                  9.91 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        32.24 |      0.46 |           0.01 |                  0.84 |
| postgresql-1-1-2-1 |        32.24 |      0.46 |           0.01 |                  0.84 |
| postgresql-2-1-1-1 |        32.89 |      0.42 |           0.00 |                  1.56 |
| postgresql-2-1-2-1 |        32.89 |      0.42 |           0.00 |                  1.56 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       227.73 |      3.54 |           6.16 |                 11.39 |
| postgresql-1-1-2-1 |       236.09 |      4.26 |           5.84 |                 11.50 |
| postgresql-1-2-1-1 |       179.77 |      3.05 |           8.21 |                 12.54 |
| postgresql-1-2-2-1 |       208.19 |      3.95 |           9.51 |                 13.84 |
| postgresql-2-1-1-1 |       134.96 |      3.65 |           5.00 |                  9.80 |
| postgresql-2-1-2-1 |       245.63 |      3.53 |           8.38 |                 13.19 |
| postgresql-2-2-1-1 |       146.20 |      2.84 |           5.83 |                 10.17 |
| postgresql-2-2-2-1 |       126.33 |      3.54 |           4.86 |                  9.19 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        13.60 |      0.42 |           0.28 |                  0.29 |
| postgresql-1-1-2-1 |        15.04 |      0.03 |           0.33 |                  0.34 |
| postgresql-1-2-1-1 |        13.20 |      0.02 |           0.30 |                  0.30 |
| postgresql-1-2-2-1 |        12.87 |      0.02 |           0.26 |                  0.26 |
| postgresql-2-1-1-1 |        13.52 |      0.82 |           0.30 |                  0.30 |
| postgresql-2-1-2-1 |        13.21 |      0.02 |           0.28 |                  0.28 |
| postgresql-2-2-1-1 |        14.22 |      0.65 |           0.36 |                  0.36 |
| postgresql-2-2-2-1 |        13.70 |      0.03 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-1-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-2-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-2-2-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   5.00 |                                               5.00 |
| postgresql-2-2-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   4.00 |                                               4.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
