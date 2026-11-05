## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 377s 
* Code: 1793810687
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['PgDuckDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* pgduckdb-1-1-1-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:853213
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:834G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810687
* pgduckdb-1-1-1-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:853213
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:834G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810687
* pgduckdb-1-1-1-1-3 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:853213
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:834G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810687

### SUT Container Restarts
* bexhoma-sut-pgduckdb-1-1793810687-788999774b-mcnh8: 0

### Workflow

#### Actual

* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|              |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:-------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PgDuckDB-1-1 |                1 |    1 |       53.00 |           3.00 |           24.00 |          7.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               67.92 | False               |

### Benchmarking

#### Per Connection

| DBMS               | configuration   | phase          | job              |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                |
|:-------------------|:----------------|:---------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:-------------------|
| pgduckdb-1-1-1-1-1 | PgDuckDB-1      | pgduckdb-1-1-1 | pgduckdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         10 |            0.21 |            17115.48 |           7920.00 |          -1 | pgduckdb-1-1-1-1-1 |
| pgduckdb-1-1-1-1-2 | PgDuckDB-1      | pgduckdb-1-1-1 | pgduckdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.21 |            16847.83 |           8800.00 |          -1 | pgduckdb-1-1-1-1-2 |
| pgduckdb-1-1-1-1-3 | PgDuckDB-1      | pgduckdb-1-1-1 | pgduckdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.21 |            16820.69 |           8800.00 |          -1 | pgduckdb-1-1-1-1-3 |

#### Per Phase

|                | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1 | pgduckdb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         10 |            0.21 |            16927.48 |          23760.00 |          -1 |

#### Query Completion per Phase

| phase          |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:---------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| pgduckdb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| pgduckdb-1-1-1-2-1 | pgduckdb-1-1-1 | pgduckdb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-04 17:49:58 | 2026-11-04 17:50:00 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   pgduckdb-1-1-1-1-1 |   pgduckdb-1-1-1-1-2 |   pgduckdb-1-1-1-1-3 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               651.90 |               656.22 |               666.43 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               153.81 |               155.74 |               176.59 |
| Shipping Priority (TPC-H Q3)                        |               234.76 |               282.00 |               282.10 |
| Order Priority Checking Query (TPC-H Q4)            |               127.72 |               127.33 |               125.88 |
| Local Supplier Volume (TPC-H Q5)                    |               207.83 |               207.97 |               209.85 |
| Forecasting Revenue Change (TPC-H Q6)               |               134.36 |               133.48 |               134.28 |
| Volume Shipping Query (TPC-H Q7)                    |               264.71 |               268.54 |               271.94 |
| National Market Share (TPC-H Q8)                    |               150.54 |               150.67 |               150.20 |
| Product Type Profit Measure (TPC-H Q9)              |               372.35 |               372.72 |               373.26 |
| Returned Item Reporting Query (TPC-H Q10)           |               384.66 |               383.59 |               384.76 |
| Important Stock Identification (TPC-H Q11)          |                58.36 |                54.81 |                55.47 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               212.00 |               213.51 |               201.78 |
| Customer Distribution (TPC-H Q13)                   |               629.14 |               628.26 |               598.21 |
| Promotion Effect Query (TPC-H Q14)                  |               151.93 |               151.50 |               154.60 |
| Top Supplier Query (TPC-H Q15)                      |               158.02 |               156.65 |               157.50 |
| Parts/Supplier Relationship (TPC-H Q16)             |               181.11 |               180.57 |               179.82 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               727.83 |               658.19 |               649.93 |
| Large Volume Customer (TPC-H Q18)                   |              2092.33 |              2049.85 |              2048.71 |
| Discounted Revenue (TPC-H Q19)                      |                40.40 |                42.99 |                41.71 |
| Potential Part Promotion (TPC-H Q20)                |                84.41 |                97.10 |                94.45 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               213.99 |               235.58 |               238.40 |
| Global Sales Opportunity Query (TPC-H Q22)          |                70.52 |                72.98 |                73.54 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
