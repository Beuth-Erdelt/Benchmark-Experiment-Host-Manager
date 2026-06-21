## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1032s 
* Code: 1782031322
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 30Gi.
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
  * disk:216139
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782031322
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:216139
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782031322

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
| PostgreSQL-1-1 |                1 |    1 |      244.00 |           2.00 |           20.00 |         56.00 |          162.00 |              8 |           0 |             |                |             0 | False         |               14.75 |
| PostgreSQL-1-2 |                2 |    1 |      244.00 |           2.00 |           20.00 |         56.00 |          162.00 |              8 |           0 |             |                |             0 | False         |               14.75 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         16 |            0.34 |            11346.84 |           4950.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        224 |            1.34 |             2832.75 |            353.57 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         16 |            0.34 |            11346.84 |           4950.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        224 |            1.34 |             2832.75 |            353.57 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1178.57 |               82710.49 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 286.48 |               44147.08 |
| Shipping Priority (TPC-H Q3)                        |                 379.61 |               25273.37 |
| Order Priority Checking Query (TPC-H Q4)            |                 166.66 |                 201.90 |
| Local Supplier Volume (TPC-H Q5)                    |                 329.51 |                2501.81 |
| Forecasting Revenue Change (TPC-H Q6)               |                 209.40 |                 201.48 |
| Volume Shipping Query (TPC-H Q7)                    |                 387.56 |                 444.29 |
| National Market Share (TPC-H Q8)                    |                 212.46 |               35602.88 |
| Product Type Profit Measure (TPC-H Q9)              |                 561.51 |               13193.24 |
| Returned Item Reporting Query (TPC-H Q10)           |                 596.78 |                 690.80 |
| Important Stock Identification (TPC-H Q11)          |                  94.94 |                  98.28 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 304.69 |                 340.14 |
| Customer Distribution (TPC-H Q13)                   |                1145.99 |                1554.82 |
| Promotion Effect Query (TPC-H Q14)                  |                 233.34 |                 259.44 |
| Top Supplier Query (TPC-H Q15)                      |                 244.96 |                 257.45 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 295.69 |                 302.47 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 853.67 |                1309.24 |
| Large Volume Customer (TPC-H Q18)                   |                2709.26 |                3075.81 |
| Discounted Revenue (TPC-H Q19)                      |                  51.27 |                 503.00 |
| Potential Part Promotion (TPC-H Q20)                |                 139.49 |                1426.82 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 290.47 |                 341.68 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  98.20 |                 138.91 |

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
