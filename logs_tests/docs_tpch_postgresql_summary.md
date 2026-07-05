## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 434s 
* Code: 1783001522
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 15Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:649421
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783001522

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783001522-76db7486b6-2bmv6: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 1.00 |      156.00 |           1.00 |           22.00 |          8.00 |          118.00 |              8 |           0 |             |                |             0 | False         |               23.08 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.20 |            19327.25 |           7200.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.20 |            19327.25 |           7200.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 668.55 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 152.70 |
| Shipping Priority (TPC-H Q3)                        |                 201.36 |
| Order Priority Checking Query (TPC-H Q4)            |                  85.99 |
| Local Supplier Volume (TPC-H Q5)                    |                 170.13 |
| Forecasting Revenue Change (TPC-H Q6)               |                 120.28 |
| Volume Shipping Query (TPC-H Q7)                    |                 212.08 |
| National Market Share (TPC-H Q8)                    |                 101.43 |
| Product Type Profit Measure (TPC-H Q9)              |                 311.23 |
| Returned Item Reporting Query (TPC-H Q10)           |                 250.23 |
| Important Stock Identification (TPC-H Q11)          |                  58.50 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 178.36 |
| Customer Distribution (TPC-H Q13)                   |                 607.31 |
| Promotion Effect Query (TPC-H Q14)                  |                 133.93 |
| Top Supplier Query (TPC-H Q15)                      |                 143.46 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 168.53 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 577.68 |
| Large Volume Customer (TPC-H Q18)                   |                2353.17 |
| Discounted Revenue (TPC-H Q19)                      |                  37.28 |
| Potential Part Promotion (TPC-H Q20)                |                 113.62 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 197.48 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  62.02 |

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
