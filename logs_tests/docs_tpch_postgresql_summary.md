## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 359s 
* Code: 1782120735
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
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222680
  * datadisk:2758
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782120735

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      121.00 |           0.00 |           16.00 |          8.00 |           91.00 |              8 |           0 |             |                |             0 | False         |               29.75 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.33 |            11749.09 |           5280.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.33 |            11749.09 |           5280.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1236.87 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 259.42 |
| Shipping Priority (TPC-H Q3)                        |                 357.31 |
| Order Priority Checking Query (TPC-H Q4)            |                 154.73 |
| Local Supplier Volume (TPC-H Q5)                    |                 328.63 |
| Forecasting Revenue Change (TPC-H Q6)               |                 193.53 |
| Volume Shipping Query (TPC-H Q7)                    |                 343.93 |
| National Market Share (TPC-H Q8)                    |                 192.52 |
| Product Type Profit Measure (TPC-H Q9)              |                 688.55 |
| Returned Item Reporting Query (TPC-H Q10)           |                 527.74 |
| Important Stock Identification (TPC-H Q11)          |                  83.21 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 285.71 |
| Customer Distribution (TPC-H Q13)                   |                1106.00 |
| Promotion Effect Query (TPC-H Q14)                  |                 207.50 |
| Top Supplier Query (TPC-H Q15)                      |                 216.59 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 284.45 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 880.77 |
| Large Volume Customer (TPC-H Q18)                   |                2815.50 |
| Discounted Revenue (TPC-H Q19)                      |                  57.47 |
| Potential Part Promotion (TPC-H Q20)                |                 133.65 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 287.99 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  99.80 |

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
