## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 727s 
* Code: 1782122428
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.18.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219923
  * datadisk:2757
  * volume_size:30G
  * volume_used:2.7G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782122428
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219923
  * datadisk:2757
  * volume_size:30G
  * volume_used:2.7G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782122428

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      178.00 |           1.00 |           23.00 |         26.00 |          125.00 |              8 |           0 |             |                |             0 | False         |               20.22 |
| PostgreSQL-1-2 |                2 |    1 |      178.00 |           1.00 |           23.00 |         26.00 |          125.00 |              8 |           0 |             |                |             0 | False         |               20.22 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.32 |            12024.32 |           5280.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |         35 |            0.54 |             7087.28 |           2262.86 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.32 |            12024.32 |           5280.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |         35 |            0.54 |             7087.28 |           2262.86 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1156.81 |               11210.70 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 265.83 |                5143.92 |
| Shipping Priority (TPC-H Q3)                        |                 331.23 |                3773.82 |
| Order Priority Checking Query (TPC-H Q4)            |                 133.43 |                 198.38 |
| Local Supplier Volume (TPC-H Q5)                    |                 283.41 |                 339.13 |
| Forecasting Revenue Change (TPC-H Q6)               |                 177.66 |                 209.71 |
| Volume Shipping Query (TPC-H Q7)                    |                 365.05 |                 399.37 |
| National Market Share (TPC-H Q8)                    |                 204.26 |                1472.49 |
| Product Type Profit Measure (TPC-H Q9)              |                 577.47 |                 624.11 |
| Returned Item Reporting Query (TPC-H Q10)           |                 600.61 |                 612.29 |
| Important Stock Identification (TPC-H Q11)          |                  86.36 |                  91.02 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 321.20 |                 333.18 |
| Customer Distribution (TPC-H Q13)                   |                1292.86 |                1379.47 |
| Promotion Effect Query (TPC-H Q14)                  |                 222.48 |                 218.09 |
| Top Supplier Query (TPC-H Q15)                      |                 225.85 |                 224.15 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 250.09 |                 248.20 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 654.87 |                 631.71 |
| Large Volume Customer (TPC-H Q18)                   |                2708.36 |                2990.60 |
| Discounted Revenue (TPC-H Q19)                      |                  50.99 |                  56.17 |
| Potential Part Promotion (TPC-H Q20)                |                 150.20 |                 301.68 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 295.46 |                 295.21 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  93.77 |                 101.93 |

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
