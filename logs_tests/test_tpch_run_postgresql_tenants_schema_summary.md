## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 565s 
* Code: 1781980444
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225912
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225912
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:233273
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:233273
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781980444-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    1 |       78.00 |           2.00 |            0.00 |         78.00 |          135.00 |              2 |           0 |               46.15 |
| 1781980444-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    1 |       78.00 |           2.00 |            0.00 |         78.00 |          135.00 |              2 |           0 |               46.15 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         14 |            0.33 |            10944.63 |           5657.14 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11496.78 |           6600.00 |           1 | PostgreSQL-1-1-1-1-2 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         12 |            0.33 |            10935.76 |           6600.00 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         15 |            0.36 |             9961.28 |           5280.00 |           1 | PostgreSQL-1-1-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         14 |            0.33 |            10944.63 |           5657.14 |           0 |
| PostgreSQL-1-1-1_1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11496.78 |           6600.00 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         12 |            0.33 |            10935.76 |           6600.00 |           0 |
| PostgreSQL-1-1-2_1 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         15 |            0.36 |             9961.28 |           5280.00 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1222.51 |                1216.25 |                1240.66 |                1237.54 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 247.93 |                 263.77 |                 302.23 |                 357.13 |
| Shipping Priority (TPC-H Q3)                        |                 327.87 |                 338.95 |                 343.23 |                 351.94 |
| Order Priority Checking Query (TPC-H Q4)            |                 140.96 |                 149.93 |                 155.94 |                 163.26 |
| Local Supplier Volume (TPC-H Q5)                    |                 285.46 |                 303.57 |                 343.52 |                 353.58 |
| Forecasting Revenue Change (TPC-H Q6)               |                 192.24 |                 194.15 |                 201.19 |                 203.80 |
| Volume Shipping Query (TPC-H Q7)                    |                 352.66 |                 365.31 |                 424.88 |                 433.53 |
| National Market Share (TPC-H Q8)                    |                 185.14 |                 192.07 |                 204.99 |                 190.92 |
| Product Type Profit Measure (TPC-H Q9)              |                 476.49 |                 796.90 |                 503.22 |                 891.38 |
| Returned Item Reporting Query (TPC-H Q10)           |                 289.12 |                 310.38 |                 313.74 |                 349.90 |
| Important Stock Identification (TPC-H Q11)          |                  89.17 |                  87.04 |                 145.25 |                 148.45 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 293.35 |                 295.85 |                 305.00 |                 309.63 |
| Customer Distribution (TPC-H Q13)                   |                1790.69 |                1014.64 |                1372.90 |                1665.32 |
| Promotion Effect Query (TPC-H Q14)                  |                 372.14 |                 218.00 |                 350.78 |                 224.38 |
| Top Supplier Query (TPC-H Q15)                      |                 266.63 |                 248.55 |                 249.83 |                 256.85 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 318.17 |                 303.08 |                 292.30 |                 322.85 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1188.05 |                 818.27 |                 826.45 |                1256.95 |
| Large Volume Customer (TPC-H Q18)                   |                3810.28 |                3310.75 |                3196.21 |                3885.18 |
| Discounted Revenue (TPC-H Q19)                      |                  68.63 |                  72.48 |                  60.19 |                  67.59 |
| Potential Part Promotion (TPC-H Q20)                |                 186.38 |                 141.42 |                 134.64 |                 205.50 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 339.87 |                 341.59 |                 324.35 |                 380.01 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 118.18 |                 118.67 |                 117.35 |                 108.79 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
