## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 724s 
* Code: 1783004125
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
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:653629
  * volume_size:5.0G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783004125
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:656438
  * volume_size:5.0G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783004125

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783004125-76dc769f6b-qbfzc: 0 0

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
| PostgreSQL-1-1 |                1 | 0.10 |      137.00 |           1.00 |           18.00 |          3.00 |          111.00 |              8 |           0 |             |                |             0 | False         |                2.63 |
| PostgreSQL-1-2 |                2 | 0.10 |      137.00 |           1.00 |           18.00 |          3.00 |          111.00 |              8 |           0 |             |                |             0 | False         |                2.63 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          2 |            0.03 |            11752.52 |           3960.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          8 |            0.06 |             6752.96 |            990.00 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          2 |            0.03 |            11752.52 |           3960.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          8 |            0.06 |             6752.96 |            990.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 156.57 |                3002.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  21.30 |                1247.31 |
| Shipping Priority (TPC-H Q3)                        |                  42.53 |                1054.96 |
| Order Priority Checking Query (TPC-H Q4)            |                  72.26 |                  73.90 |
| Local Supplier Volume (TPC-H Q5)                    |                  27.38 |                  26.29 |
| Forecasting Revenue Change (TPC-H Q6)               |                  24.67 |                  20.62 |
| Volume Shipping Query (TPC-H Q7)                    |                  30.30 |                  32.50 |
| National Market Share (TPC-H Q8)                    |                  25.56 |                  97.64 |
| Product Type Profit Measure (TPC-H Q9)              |                  63.80 |                  78.22 |
| Returned Item Reporting Query (TPC-H Q10)           |                  40.88 |                  41.44 |
| Important Stock Identification (TPC-H Q11)          |                   7.34 |                   7.03 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  34.13 |                  32.99 |
| Customer Distribution (TPC-H Q13)                   |                  56.03 |                  61.79 |
| Promotion Effect Query (TPC-H Q14)                  |                  24.01 |                  22.83 |
| Top Supplier Query (TPC-H Q15)                      |                  23.13 |                  22.40 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  35.30 |                  35.22 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  45.51 |                  48.86 |
| Large Volume Customer (TPC-H Q18)                   |                 176.76 |                 192.21 |
| Discounted Revenue (TPC-H Q19)                      |                   4.73 |                   5.12 |
| Potential Part Promotion (TPC-H Q20)                |                   8.08 |                  10.62 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  40.53 |                  34.34 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  10.35 |                  13.25 |

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
