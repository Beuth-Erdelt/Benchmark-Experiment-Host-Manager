## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 823s 
* Code: 1784568032
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.6.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:495257
  * volume_size:50G
  * volume_used:308M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1784568032
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:495211
  * volume_size:50G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1784568032

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1784568032-86b5b96d8c-jzkb4: 0 0

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
| PostgreSQL-1-1 |                1 | 0.10 |       32.00 |           1.00 |           19.00 |          6.00 |            0.00 |              8 |           0 |             |                |             0 | False         |               11.25 |
| PostgreSQL-1-2 |                2 | 0.10 |      161.00 |           1.00 |           19.00 |          6.00 |          129.00 |              8 |           0 |             |                |             0 | False         |                2.24 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          4 |            0.03 |            11428.35 |           1980.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |         13 |            0.06 |             6828.11 |            609.23 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          4 |            0.03 |            11428.35 |           1980.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |         13 |            0.06 |             6828.11 |            609.23 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 237.42 |                2026.38 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  48.94 |                1995.35 |
| Shipping Priority (TPC-H Q3)                        |                  89.06 |                5661.72 |
| Order Priority Checking Query (TPC-H Q4)            |                 125.04 |                  71.12 |
| Local Supplier Volume (TPC-H Q5)                    |                  23.67 |                  23.09 |
| Forecasting Revenue Change (TPC-H Q6)               |                  20.57 |                  19.89 |
| Volume Shipping Query (TPC-H Q7)                    |                  25.82 |                  29.16 |
| National Market Share (TPC-H Q8)                    |                  24.44 |                  66.56 |
| Product Type Profit Measure (TPC-H Q9)              |                  61.62 |                  73.03 |
| Returned Item Reporting Query (TPC-H Q10)           |                  35.38 |                  37.26 |
| Important Stock Identification (TPC-H Q11)          |                   7.21 |                   7.66 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  27.33 |                  31.03 |
| Customer Distribution (TPC-H Q13)                   |                  50.52 |                  50.71 |
| Promotion Effect Query (TPC-H Q14)                  |                  20.75 |                  21.82 |
| Top Supplier Query (TPC-H Q15)                      |                  18.96 |                  19.96 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  34.40 |                  35.06 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  38.86 |                  41.04 |
| Large Volume Customer (TPC-H Q18)                   |                 190.76 |                 196.61 |
| Discounted Revenue (TPC-H Q19)                      |                   4.43 |                   5.43 |
| Potential Part Promotion (TPC-H Q20)                |                   7.47 |                   8.06 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  30.82 |                  28.41 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  10.40 |                  10.50 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
