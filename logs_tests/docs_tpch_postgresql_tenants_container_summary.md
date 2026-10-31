## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 493s 
* Code: 1793468428
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861914
  * datadisk:2758
  * volume_size:49G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793468428
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861914
  * datadisk:2758
  * volume_size:49G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793468428
    * TENANT_BY:container
    * TENANT_NUM:2
* postgresql-2-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861914
  * datadisk:2758
  * volume_size:49G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793468428
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* postgresql-2-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861914
  * datadisk:2758
  * volume_size:49G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793468428
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793468428-7cf4f55844-fqmfb: 0
* bexhoma-sut-postgresql-2-1793468428-7f9b85d678-2kl2s: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793468428-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |      100.00 |           9.00 |            0.00 |         40.00 |           18.00 |              1 |           0 |               36.00 | False               |
| 1793468428-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |       69.00 |          10.00 |            0.00 |         41.00 |           17.00 |              1 |           0 |               52.17 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.23 |            15915.40 |           7920.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.22 |            16096.19 |           5657.14 |           0 | postgresql-1-1-2-1-1 |
| postgresql-2-1-1-1-1 | PostgreSQL-2    | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.22 |            16384.77 |           7920.00 |           1 | postgresql-2-1-1-1-1 |
| postgresql-2-1-2-1-1 | PostgreSQL-2    | postgresql-2-1-2 | postgresql-2-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.23 |            15804.22 |           5657.14 |           1 | postgresql-2-1-2-1-1 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.23 |            15915.40 |           7920.00 |           0 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.22 |            16096.19 |           5657.14 |           0 |
| postgresql-2-1-1_1 | postgresql-2-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.22 |            16384.77 |           7920.00 |           1 |
| postgresql-2-1-2_1 | postgresql-2-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.23 |            15804.22 |           5657.14 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-2-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-2-1-1-1-1 |   postgresql-2-1-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 914.65 |                 989.24 |                 755.03 |                1000.59 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 180.51 |                 212.63 |                 172.99 |                 222.10 |
| Shipping Priority (TPC-H Q3)                        |                 246.64 |                 246.99 |                 251.61 |                 246.86 |
| Order Priority Checking Query (TPC-H Q4)            |                 103.81 |                 109.91 |                 113.82 |                 119.86 |
| Local Supplier Volume (TPC-H Q5)                    |                 269.11 |                 212.37 |                 218.83 |                 228.05 |
| Forecasting Revenue Change (TPC-H Q6)               |                 270.89 |                 137.72 |                 130.38 |                 138.16 |
| Volume Shipping Query (TPC-H Q7)                    |                 325.78 |                 261.67 |                 302.05 |                 286.76 |
| National Market Share (TPC-H Q8)                    |                 124.32 |                 123.96 |                 191.17 |                 116.79 |
| Product Type Profit Measure (TPC-H Q9)              |                 569.97 |                 751.51 |                 601.37 |                 701.49 |
| Returned Item Reporting Query (TPC-H Q10)           |                 242.08 |                 214.56 |                 223.73 |                 204.82 |
| Important Stock Identification (TPC-H Q11)          |                  64.31 |                  58.59 |                  79.23 |                  72.38 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 206.86 |                 185.77 |                 236.85 |                 203.92 |
| Customer Distribution (TPC-H Q13)                   |                 605.06 |                 620.13 |                 651.82 |                 685.74 |
| Promotion Effect Query (TPC-H Q14)                  |                 137.55 |                 150.34 |                 146.66 |                 146.45 |
| Top Supplier Query (TPC-H Q15)                      |                 167.07 |                 151.03 |                 145.02 |                 148.89 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 153.95 |                 133.17 |                 136.39 |                 136.17 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 801.09 |                 583.73 |                 627.02 |                 561.16 |
| Large Volume Customer (TPC-H Q18)                   |                2264.79 |                2828.37 |                2651.56 |                3014.38 |
| Discounted Revenue (TPC-H Q19)                      |                  43.65 |                  44.35 |                  43.34 |                  43.81 |
| Potential Part Promotion (TPC-H Q20)                |                 102.76 |                 110.65 |                 102.70 |                 107.01 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 223.28 |                 236.12 |                 221.18 |                 239.42 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  70.58 |                 143.85 |                  68.92 |                 128.99 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
