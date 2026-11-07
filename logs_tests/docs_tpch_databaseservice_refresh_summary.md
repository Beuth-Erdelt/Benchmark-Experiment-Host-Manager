## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 494s 
* Code: 1794045379
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806783
  * datadisk:39
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794045379
* databaseservice-1-1-1-1-2 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806783
  * datadisk:39
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794045379
* databaseservice-1-1-1-1-3 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806783
  * datadisk:39
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794045379

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-tpch.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1794045379-55b9f4cbd8-fwh4q: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| DatabaseService-1-1 |                1 |    1 |       67.00 |           3.00 |           17.00 |          9.00 |           33.00 |              8 |           0 |             | None           |             0 | False         |               53.73 | False               |

### Benchmarking

#### Per Connection

| DBMS                      | configuration     | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                       |
|:--------------------------|:------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------------|
| databaseservice-1-1-1-1-1 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         17 |            0.37 |             9829.56 |           4658.82 |          -1 | databaseservice-1-1-1-1-1 |
| databaseservice-1-1-1-1-2 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         16 |            0.39 |             9244.78 |           4950.00 |          -1 | databaseservice-1-1-1-1-2 |
| databaseservice-1-1-1-1-3 | DatabaseService-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         17 |            0.38 |             9431.78 |           4658.82 |          -1 | databaseservice-1-1-1-1-3 |

#### Per Phase

|                       | phase                 |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------------|:----------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         17 |            0.38 |             9498.93 |          13976.47 |          -1 |

#### Query Completion per Phase

| phase                 |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| databaseservice-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection                | phase                 | job                     |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:--------------------------|:----------------------|:------------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| databaseservice-1-1-1-2-1 | databaseservice-1-1-1 | databaseservice-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-07 11:03:37 | 2026-11-07 11:03:40 |                    3 |

### Latency of Timer Execution [ms]
| Queries                                             |   databaseservice-1-1-1-1-1 |   databaseservice-1-1-1-1-2 |   databaseservice-1-1-1-1-3 |
|:----------------------------------------------------|----------------------------:|----------------------------:|----------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                     1852.31 |                     1505.41 |                     1645.94 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                      218.32 |                      237.02 |                      243.57 |
| Shipping Priority (TPC-H Q3)                        |                      348.88 |                      345.59 |                      409.73 |
| Order Priority Checking Query (TPC-H Q4)            |                      524.83 |                      600.17 |                      548.58 |
| Local Supplier Volume (TPC-H Q5)                    |                      299.05 |                      313.92 |                      343.72 |
| Forecasting Revenue Change (TPC-H Q6)               |                      252.09 |                      229.46 |                      243.00 |
| Volume Shipping Query (TPC-H Q7)                    |                      325.53 |                      413.20 |                      336.64 |
| National Market Share (TPC-H Q8)                    |                      277.15 |                      322.62 |                      277.39 |
| Product Type Profit Measure (TPC-H Q9)              |                      503.02 |                      559.57 |                      539.99 |
| Returned Item Reporting Query (TPC-H Q10)           |                      554.79 |                      558.90 |                      637.13 |
| Important Stock Identification (TPC-H Q11)          |                      103.55 |                      122.51 |                      110.33 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                      403.38 |                      462.13 |                      388.44 |
| Customer Distribution (TPC-H Q13)                   |                      679.13 |                      712.21 |                      745.35 |
| Promotion Effect Query (TPC-H Q14)                  |                      216.60 |                      229.27 |                      209.80 |
| Top Supplier Query (TPC-H Q15)                      |                      228.58 |                      227.80 |                      263.02 |
| Parts/Supplier Relationship (TPC-H Q16)             |                      278.33 |                      345.24 |                      211.24 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                      620.33 |                      623.98 |                      662.97 |
| Large Volume Customer (TPC-H Q18)                   |                     3408.52 |                     2995.54 |                     4029.48 |
| Discounted Revenue (TPC-H Q19)                      |                      289.82 |                      300.22 |                      303.27 |
| Potential Part Promotion (TPC-H Q20)                |                      251.90 |                      262.57 |                      259.81 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                      347.46 |                      388.07 |                      302.72 |
| Global Sales Opportunity Query (TPC-H Q22)          |                       85.81 |                      105.50 |                      109.37 |

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
