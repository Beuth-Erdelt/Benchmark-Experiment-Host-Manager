## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1250s 
* Code: 1782971750
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
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:645226
  * volume_size:30G
  * volume_used:2.7G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782971750
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:645550
  * volume_size:30G
  * volume_used:2.7G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782971750

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782971750-5c7bd5c765-jxzvg: 0 0

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
| PostgreSQL-1-1 |                1 |    1 |      403.00 |           8.00 |           21.00 |         31.00 |          340.00 |              8 |           0 |             |                |             0 | False         |                8.93 |
| PostgreSQL-1-2 |                2 |    1 |      403.00 |           8.00 |           21.00 |         31.00 |          340.00 |              8 |           0 |             |                |             0 | False         |                8.93 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         13 |            0.28 |            13747.85 |           6092.31 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |         39 |            0.51 |             7580.85 |           2030.77 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         13 |            0.28 |            13747.85 |           6092.31 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |         39 |            0.51 |             7580.85 |           2030.77 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1372.11 |               14411.37 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 174.33 |                5870.25 |
| Shipping Priority (TPC-H Q3)                        |                 316.82 |                5893.84 |
| Order Priority Checking Query (TPC-H Q4)            |                 143.05 |                 227.09 |
| Local Supplier Volume (TPC-H Q5)                    |                 274.64 |                 459.63 |
| Forecasting Revenue Change (TPC-H Q6)               |                 191.44 |                 232.47 |
| Volume Shipping Query (TPC-H Q7)                    |                 326.05 |                 528.30 |
| National Market Share (TPC-H Q8)                    |                 168.83 |                1595.87 |
| Product Type Profit Measure (TPC-H Q9)              |                 432.56 |                 747.50 |
| Returned Item Reporting Query (TPC-H Q10)           |                 468.60 |                 427.57 |
| Important Stock Identification (TPC-H Q11)          |                  54.56 |                  52.24 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 250.14 |                 252.28 |
| Customer Distribution (TPC-H Q13)                   |                 555.09 |                 561.92 |
| Promotion Effect Query (TPC-H Q14)                  |                 269.95 |                 235.59 |
| Top Supplier Query (TPC-H Q15)                      |                 176.55 |                 151.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 200.05 |                 179.09 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 552.53 |                 562.63 |
| Large Volume Customer (TPC-H Q18)                   |                2709.68 |                2504.55 |
| Discounted Revenue (TPC-H Q19)                      |                  61.65 |                  56.24 |
| Potential Part Promotion (TPC-H Q20)                |                 158.95 |                 326.36 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 268.92 |                 236.70 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  86.95 |                  81.34 |

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
