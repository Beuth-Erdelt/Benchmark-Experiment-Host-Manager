## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 711s 
* Code: 1782991797
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 5Gi. Persistent storage is removed at experiment start.
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
  * disk:663085
  * volume_size:5.0G
  * volume_used:312M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782991797
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:663070
  * volume_size:5.0G
  * volume_used:312M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782991797

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782991797-845bc85bc8-s9xpz: 0 0

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
| PostgreSQL-1-1 |                1 | 0.10 |      148.00 |           3.00 |           14.00 |         13.00 |          111.00 |              8 |           0 |             |                |             0 | False         |                2.43 |
| PostgreSQL-1-2 |                2 | 0.10 |      148.00 |           3.00 |           14.00 |         13.00 |          111.00 |              8 |           0 |             |                |             0 | False         |                2.43 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          5 |            0.05 |             7352.22 |           1584.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          8 |            0.08 |             4596.36 |            990.00 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          5 |            0.05 |             7352.22 |           1584.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          8 |            0.08 |             4596.36 |            990.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 255.97 |                2332.46 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  37.60 |                1554.16 |
| Shipping Priority (TPC-H Q3)                        |                  72.46 |                 864.35 |
| Order Priority Checking Query (TPC-H Q4)            |                 100.56 |                 121.69 |
| Local Supplier Volume (TPC-H Q5)                    |                  33.61 |                  38.26 |
| Forecasting Revenue Change (TPC-H Q6)               |                  34.92 |                  35.86 |
| Volume Shipping Query (TPC-H Q7)                    |                  46.40 |                  47.97 |
| National Market Share (TPC-H Q8)                    |                  45.29 |                 125.77 |
| Product Type Profit Measure (TPC-H Q9)              |                 109.98 |                 127.36 |
| Returned Item Reporting Query (TPC-H Q10)           |                  63.51 |                  65.81 |
| Important Stock Identification (TPC-H Q11)          |                  10.59 |                  10.71 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  55.18 |                  55.13 |
| Customer Distribution (TPC-H Q13)                   |                  81.15 |                  94.42 |
| Promotion Effect Query (TPC-H Q14)                  |                  41.44 |                  41.17 |
| Top Supplier Query (TPC-H Q15)                      |                  38.32 |                  36.98 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  67.25 |                  64.57 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  69.16 |                  78.88 |
| Large Volume Customer (TPC-H Q18)                   |                 280.02 |                 286.26 |
| Discounted Revenue (TPC-H Q19)                      |                   8.54 |                   8.93 |
| Potential Part Promotion (TPC-H Q20)                |                  13.18 |                  14.02 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  59.22 |                  56.54 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  19.06 |                  19.97 |

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
