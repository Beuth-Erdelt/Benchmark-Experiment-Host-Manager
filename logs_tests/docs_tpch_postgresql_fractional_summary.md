## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 871s 
* Code: 1785541498
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Experiment uses bexhoma version 0.10.9.
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
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765871
  * volume_size:50G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541498
* postgresql-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:765872
  * volume_size:50G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785541498

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785541498-79bc8c45d5-2hq5r: 0 0
* bexhoma-sut-postgresql-1-1785541498-6784646458-rp84m: 0 0

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
| PostgreSQL-1-1 |                1 | 0.10 |      160.00 |           2.00 |           18.00 |          5.00 |          130.00 |              8 |           0 |             |                |             0 | False         |                2.25 |
| PostgreSQL-1-2 |                2 | 0.10 |      160.00 |           2.00 |           18.00 |          5.00 |          130.00 |              8 |           0 |             |                |             0 | False         |                2.25 |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          3 |            0.03 |            13133.36 |           2640.00 |           0 | postgresql-1-1-1-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          9 |            0.05 |             7571.59 |            880.00 |           0 | postgresql-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          3 |            0.03 |            13133.36 |           2640.00 |           0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          9 |            0.05 |             7571.59 |            880.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 146.19 |                2854.35 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  20.73 |                 940.98 |
| Shipping Priority (TPC-H Q3)                        |                  39.79 |                 971.05 |
| Order Priority Checking Query (TPC-H Q4)            |                  56.42 |                  61.84 |
| Local Supplier Volume (TPC-H Q5)                    |                  20.40 |                  20.50 |
| Forecasting Revenue Change (TPC-H Q6)               |                  18.65 |                  19.54 |
| Volume Shipping Query (TPC-H Q7)                    |                  24.02 |                  26.06 |
| National Market Share (TPC-H Q8)                    |                  23.66 |                 164.29 |
| Product Type Profit Measure (TPC-H Q9)              |                  63.29 |                  64.23 |
| Returned Item Reporting Query (TPC-H Q10)           |                  38.60 |                  37.29 |
| Important Stock Identification (TPC-H Q11)          |                   5.40 |                   5.85 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  32.82 |                  33.53 |
| Customer Distribution (TPC-H Q13)                   |                  43.14 |                  43.20 |
| Promotion Effect Query (TPC-H Q14)                  |                  23.48 |                  23.43 |
| Top Supplier Query (TPC-H Q15)                      |                  21.57 |                  20.28 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  34.17 |                  34.79 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  34.73 |                  40.38 |
| Large Volume Customer (TPC-H Q18)                   |                 176.05 |                 169.34 |
| Discounted Revenue (TPC-H Q19)                      |                   5.17 |                   4.72 |
| Potential Part Promotion (TPC-H Q20)                |                   9.01 |                   8.00 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  29.65 |                  29.74 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  10.71 |                  11.08 |

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
