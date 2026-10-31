## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 509s 
* Code: 1793466704
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
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
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
  * disk:861719
  * datadisk:5476
  * volume_size:49G
  * volume_used:5.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793466704
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-1-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861719
  * datadisk:5476
  * volume_size:49G
  * volume_used:5.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793466704
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861719
  * datadisk:5476
  * volume_size:49G
  * volume_used:5.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793466704
    * TENANT_BY:schema
    * TENANT_NUM:2
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861719
  * datadisk:5476
  * volume_size:49G
  * volume_used:5.4G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793466704
    * TENANT_BY:schema
    * TENANT_NUM:2

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793466704-585f59b54-tn6th: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793466704-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    1 |       43.00 |           7.00 |            1.00 |         43.00 |           31.00 |              2 |           0 |               83.72 | False               |
| 1793466704-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    1 |       44.00 |           7.00 |            1.00 |         44.00 |           31.00 |              2 |           0 |               81.82 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.20 |            17896.04 |           8800.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-1-1-2 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          8 |            0.20 |            18229.29 |           9900.00 |           1 | postgresql-1-1-1-1-2 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.20 |            18042.66 |           8800.00 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.19 |            18881.43 |           8800.00 |           1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.20 |            17896.04 |           8800.00 |           0 |
| postgresql-1-1-1_1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          8 |            0.20 |            18229.29 |           9900.00 |           1 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.20 |            18042.66 |           8800.00 |           0 |
| postgresql-1-1-2_1 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.19 |            18881.43 |           8800.00 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-1-1-2 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 668.62 |                 669.11 |                 669.67 |                 785.78 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 163.37 |                 172.96 |                 152.71 |                 152.37 |
| Shipping Priority (TPC-H Q3)                        |                 243.51 |                 244.85 |                 229.59 |                 231.43 |
| Order Priority Checking Query (TPC-H Q4)            |                 112.97 |                 112.19 |                 114.29 |                 100.97 |
| Local Supplier Volume (TPC-H Q5)                    |                 209.61 |                 239.64 |                 212.70 |                 177.99 |
| Forecasting Revenue Change (TPC-H Q6)               |                 121.32 |                 136.82 |                 130.97 |                 129.17 |
| Volume Shipping Query (TPC-H Q7)                    |                 280.88 |                 261.37 |                 240.78 |                 247.82 |
| National Market Share (TPC-H Q8)                    |                 138.12 |                 147.30 |                 125.06 |                 125.78 |
| Product Type Profit Measure (TPC-H Q9)              |                 309.35 |                 387.21 |                 377.50 |                 360.27 |
| Returned Item Reporting Query (TPC-H Q10)           |                 197.06 |                 177.91 |                 193.32 |                 191.66 |
| Important Stock Identification (TPC-H Q11)          |                  54.47 |                  53.63 |                  57.98 |                  56.22 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 199.65 |                 189.97 |                 200.68 |                 198.82 |
| Customer Distribution (TPC-H Q13)                   |                 652.07 |                 642.80 |                 676.35 |                 659.23 |
| Promotion Effect Query (TPC-H Q14)                  |                 149.92 |                 150.22 |                 158.67 |                 146.76 |
| Top Supplier Query (TPC-H Q15)                      |                 150.64 |                 152.86 |                 156.99 |                 149.98 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 207.82 |                 128.43 |                 141.82 |                 130.92 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 532.39 |                 539.42 |                 521.15 |                 513.60 |
| Large Volume Customer (TPC-H Q18)                   |                2061.18 |                2060.89 |                2066.72 |                2010.17 |
| Discounted Revenue (TPC-H Q19)                      |                  46.38 |                  38.71 |                  45.13 |                  38.22 |
| Potential Part Promotion (TPC-H Q20)                |                 103.95 |                  93.31 |                 103.65 |                  90.47 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 217.67 |                 224.95 |                 228.59 |                 217.41 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  68.78 |                  65.83 |                  75.69 |                  64.22 |

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
