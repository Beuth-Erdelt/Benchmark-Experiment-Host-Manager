## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 471s 
* Code: 1793467256
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
  * Number of tenants is 2, one database per tenant.
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
  * disk:861721
  * datadisk:5507
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
    * code:1793467256
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-1-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861721
  * datadisk:5507
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
    * code:1793467256
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861721
  * datadisk:5507
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
    * code:1793467256
    * TENANT_BY:database
    * TENANT_NUM:2
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861721
  * datadisk:5507
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
    * code:1793467256
    * TENANT_BY:database
    * TENANT_NUM:2

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793467256-97b767db9-xwtbp: 0

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
| 1793467256-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |       33.00 |           6.00 |            1.00 |         33.00 |           30.00 |              2 |           0 |              109.09 | False               |
| 1793467256-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |       32.00 |           6.00 |            1.00 |         32.00 |           30.00 |              2 |           0 |              112.50 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.22 |            16270.33 |           7920.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-1-1-1-2 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.22 |            16143.28 |           7920.00 |           1 | postgresql-1-1-1-1-2 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.22 |            16357.95 |           6092.31 |           0 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.22 |            16000.95 |           6092.31 |           1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1_0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.22 |            16270.33 |           7920.00 |           0 |
| postgresql-1-1-1_1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.22 |            16143.28 |           7920.00 |           1 |
| postgresql-1-1-2_0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.22 |            16357.95 |           6092.31 |           0 |
| postgresql-1-1-2_1 | postgresql-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         13 |            0.22 |            16000.95 |           6092.31 |           1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-1-1-2 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 697.30 |                 839.70 |                 724.71 |                 691.09 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 183.54 |                 179.86 |                 170.68 |                 164.45 |
| Shipping Priority (TPC-H Q3)                        |                 257.32 |                 296.17 |                 232.37 |                 233.90 |
| Order Priority Checking Query (TPC-H Q4)            |                 121.40 |                 119.60 |                 105.43 |                 107.58 |
| Local Supplier Volume (TPC-H Q5)                    |                 274.44 |                 227.13 |                 217.08 |                 293.04 |
| Forecasting Revenue Change (TPC-H Q6)               |                 134.45 |                 130.09 |                 128.52 |                 225.76 |
| Volume Shipping Query (TPC-H Q7)                    |                 264.94 |                 267.55 |                 371.15 |                 334.59 |
| National Market Share (TPC-H Q8)                    |                 138.31 |                 152.56 |                 214.40 |                 124.75 |
| Product Type Profit Measure (TPC-H Q9)              |                 428.92 |                 430.37 |                 485.13 |                 416.21 |
| Returned Item Reporting Query (TPC-H Q10)           |                 205.29 |                 192.53 |                 250.02 |                 198.77 |
| Important Stock Identification (TPC-H Q11)          |                  62.19 |                  61.00 |                  64.15 |                  62.15 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 191.63 |                 302.74 |                 195.27 |                 191.44 |
| Customer Distribution (TPC-H Q13)                   |                 761.89 |                 822.03 |                 682.64 |                 620.27 |
| Promotion Effect Query (TPC-H Q14)                  |                 154.72 |                 261.76 |                 153.26 |                 232.53 |
| Top Supplier Query (TPC-H Q15)                      |                 171.45 |                 154.51 |                 147.54 |                 158.68 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 162.25 |                 141.12 |                 138.80 |                 288.58 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 564.38 |                 578.47 |                 558.40 |                 560.82 |
| Large Volume Customer (TPC-H Q18)                   |                2485.08 |                2516.90 |                3320.22 |                3170.05 |
| Discounted Revenue (TPC-H Q19)                      |                  71.09 |                  40.50 |                  51.21 |                  43.33 |
| Potential Part Promotion (TPC-H Q20)                |                 124.76 |                 105.54 |                  96.66 |                  93.66 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 230.45 |                 227.32 |                 230.54 |                 219.37 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  72.62 |                  70.22 |                  74.26 |                  68.80 |

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
