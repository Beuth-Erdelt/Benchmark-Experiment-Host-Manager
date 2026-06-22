## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 609s 
* Code: 1781981608
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 5Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:218181
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:224797
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220255
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:227162
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

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

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781981608-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |      165.00 |           1.00 |            0.00 |         55.00 |          105.00 |              1 |           0 |               21.82 |
| 1781981608-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |      160.00 |           1.00 |            0.00 |         55.00 |          102.00 |              1 |           0 |               22.50 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11478.56 |           6600.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2    | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11435.20 |           6600.00 |           1 | PostgreSQL-2-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.33 |            11053.82 |           6092.31 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2    | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.34 |            10566.27 |           6092.31 |           1 | PostgreSQL-2-1-2-1-1 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11478.56 |           6600.00 |           0 |
| PostgreSQL-2-1-1_1 | PostgreSQL-2-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11435.20 |           6600.00 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.33 |            11053.82 |           6092.31 |           0 |
| PostgreSQL-2-1-2_1 | PostgreSQL-2-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.34 |            10566.27 |           6092.31 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-2-1-1-1-1 |   PostgreSQL-2-1-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1237.16 |                1232.32 |                1220.50 |                1256.62 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 281.92 |                 306.93 |                 291.62 |                 315.82 |
| Shipping Priority (TPC-H Q3)                        |                 369.27 |                 352.49 |                 358.01 |                 341.07 |
| Order Priority Checking Query (TPC-H Q4)            |                 170.23 |                 156.25 |                 168.54 |                 159.56 |
| Local Supplier Volume (TPC-H Q5)                    |                 336.04 |                 420.53 |                 334.24 |                 334.17 |
| Forecasting Revenue Change (TPC-H Q6)               |                 189.17 |                 199.72 |                 207.66 |                 203.32 |
| Volume Shipping Query (TPC-H Q7)                    |                 396.78 |                 411.15 |                 392.32 |                 410.72 |
| National Market Share (TPC-H Q8)                    |                 221.03 |                 205.64 |                 215.12 |                 194.44 |
| Product Type Profit Measure (TPC-H Q9)              |                 547.66 |                 583.95 |                 538.76 |                 552.07 |
| Returned Item Reporting Query (TPC-H Q10)           |                 313.35 |                 331.30 |                 297.02 |                 301.29 |
| Important Stock Identification (TPC-H Q11)          |                 100.35 |                 143.83 |                 103.38 |                 167.74 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 315.05 |                 310.79 |                 316.32 |                 311.13 |
| Customer Distribution (TPC-H Q13)                   |                1215.78 |                1164.14 |                1213.26 |                1676.85 |
| Promotion Effect Query (TPC-H Q14)                  |                 231.80 |                 224.94 |                 234.79 |                 226.79 |
| Top Supplier Query (TPC-H Q15)                      |                 248.38 |                 241.43 |                 231.85 |                 249.88 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 296.34 |                 305.97 |                 291.90 |                 298.66 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 888.93 |                 793.31 |                 887.80 |                1197.81 |
| Large Volume Customer (TPC-H Q18)                   |                2768.09 |                3254.79 |                3187.04 |                3337.95 |
| Discounted Revenue (TPC-H Q19)                      |                  55.76 |                  60.40 |                  53.01 |                  59.85 |
| Potential Part Promotion (TPC-H Q20)                |                 133.06 |                 133.62 |                 132.74 |                 184.73 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 323.45 |                 332.95 |                 347.23 |                 361.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 102.67 |                 111.34 |                 103.31 |                 111.91 |

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
