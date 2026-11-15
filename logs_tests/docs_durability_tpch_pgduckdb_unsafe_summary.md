## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 437s 
* Code: 1794609702
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is unsafe (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PgDuckDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* pgduckdb-1-1-1-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1126693
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: unsafe
  * eval_parameters
    * code:1794609702

### Ingestion
* PgDuckDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-pgduckdb-1-1794609702-7b8fcb6778-m62g9: 0

### Workflow

#### Actual

* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS         |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:-------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PgDuckDB-1-1 |                1 |    1 |       88.00 |           7.00 |           49.00 |          6.00 |           24.00 |              8 |         0 |             | None           |             0 | False         |               40.91 | False               |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1-1-1 | pgduckdb-1-1-1 | pgduckdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |          9 |            0.23 |            15636.48 |           8800.00 |          -1 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1 | pgduckdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.23 |            15636.48 |           8800.00 |          -1 |

#### Query Completion per Phase

| phase          |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:---------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| pgduckdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   pgduckdb-1-1-1-1-1 |
|:----------------------------------------------------|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               665.15 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               180.52 |
| Shipping Priority (TPC-H Q3)                        |               235.98 |
| Order Priority Checking Query (TPC-H Q4)            |               111.12 |
| Local Supplier Volume (TPC-H Q5)                    |               207.83 |
| Forecasting Revenue Change (TPC-H Q6)               |               130.32 |
| Volume Shipping Query (TPC-H Q7)                    |               272.30 |
| National Market Share (TPC-H Q8)                    |               147.05 |
| Product Type Profit Measure (TPC-H Q9)              |               398.66 |
| Returned Item Reporting Query (TPC-H Q10)           |               372.27 |
| Important Stock Identification (TPC-H Q11)          |                60.50 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               196.37 |
| Customer Distribution (TPC-H Q13)                   |               601.26 |
| Promotion Effect Query (TPC-H Q14)                  |               234.90 |
| Top Supplier Query (TPC-H Q15)                      |               148.31 |
| Parts/Supplier Relationship (TPC-H Q16)             |               175.56 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               598.53 |
| Large Volume Customer (TPC-H Q18)                   |              2029.46 |
| Discounted Revenue (TPC-H Q19)                      |                47.20 |
| Potential Part Promotion (TPC-H Q20)                |               297.07 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               329.77 |
| Global Sales Opportunity Query (TPC-H Q22)          |                74.63 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
