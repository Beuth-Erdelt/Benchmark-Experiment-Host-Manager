## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 852s 
* Code: 1785153807
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
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
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808966
  * volume_size:50G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153807
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:810118
  * volume_size:50G
  * volume_used:312M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785153807

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785153807-69ffd6d496-zx9lm: 0 0

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
| PostgreSQL-1-1 |                1 | 0.10 |      139.00 |           1.00 |           19.00 |          2.00 |          113.00 |              8 |           0 |             |                |             0 | False         |                2.59 |
| PostgreSQL-1-2 |                2 | 0.10 |      139.00 |           1.00 |           19.00 |          2.00 |          113.00 |              8 |           0 |             |                |             0 | False         |                2.59 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          3 |            0.04 |            11289.58 |           2640.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          6 |            0.06 |             6392.52 |           1320.00 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          3 |            0.04 |            11289.58 |           2640.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |          6 |            0.06 |             6392.52 |           1320.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 150.24 |                2187.07 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  22.71 |                 638.96 |
| Shipping Priority (TPC-H Q3)                        |                  50.20 |                 986.42 |
| Order Priority Checking Query (TPC-H Q4)            |                  62.66 |                 102.15 |
| Local Supplier Volume (TPC-H Q5)                    |                  26.39 |                  46.15 |
| Forecasting Revenue Change (TPC-H Q6)               |                  22.89 |                  37.81 |
| Volume Shipping Query (TPC-H Q7)                    |                  37.30 |                  57.13 |
| National Market Share (TPC-H Q8)                    |                  32.49 |                 127.10 |
| Product Type Profit Measure (TPC-H Q9)              |                  83.08 |                 107.92 |
| Returned Item Reporting Query (TPC-H Q10)           |                  44.79 |                  40.49 |
| Important Stock Identification (TPC-H Q11)          |                   6.48 |                   6.63 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  31.51 |                  33.88 |
| Customer Distribution (TPC-H Q13)                   |                  56.59 |                  44.07 |
| Promotion Effect Query (TPC-H Q14)                  |                  23.20 |                  23.97 |
| Top Supplier Query (TPC-H Q15)                      |                  21.78 |                  21.38 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  41.98 |                  41.39 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  50.28 |                  45.92 |
| Large Volume Customer (TPC-H Q18)                   |                 205.23 |                 217.58 |
| Discounted Revenue (TPC-H Q19)                      |                   4.66 |                   6.00 |
| Potential Part Promotion (TPC-H Q20)                |                   8.04 |                   8.43 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  35.38 |                  33.68 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  12.26 |                  11.73 |

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
