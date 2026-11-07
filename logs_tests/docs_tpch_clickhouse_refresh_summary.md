## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 351s 
* Code: 1794003999
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877365
  * datadisk:821
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794003999
* clickhouse-1-1-1-1-2 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877365
  * datadisk:821
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794003999
* clickhouse-1-1-1-1-3 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877365
  * datadisk:821
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794003999

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1794003999-597587d64-2bp22: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       30.00 |           3.00 |           13.00 |          6.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              120.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          5 |            0.06 |            64063.12 |          15840.00 |          -1 | clickhouse-1-1-1-1-1 |
| clickhouse-1-1-1-1-2 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          4 |            0.05 |            66571.64 |          19800.00 |          -1 | clickhouse-1-1-1-1-2 |
| clickhouse-1-1-1-1-3 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          7 |            0.05 |            68221.84 |          11314.29 |          -1 | clickhouse-1-1-1-1-3 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |          7 |            0.05 |            66263.38 |          33942.86 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| clickhouse-1-1-1-2-1 | clickhouse-1-1-1 | clickhouse-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-06 23:31:51 | 2026-11-06 23:31:53 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |   clickhouse-1-1-1-1-2 |   clickhouse-1-1-1-1-3 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 162.68 |                  78.00 |                 159.67 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  59.13 |                  62.32 |                  63.86 |
| Shipping Priority (TPC-H Q3)                        |                  49.53 |                  49.28 |                  62.75 |
| Order Priority Checking Query (TPC-H Q4)            |                 184.63 |                 185.34 |                 171.16 |
| Local Supplier Volume (TPC-H Q5)                    |                  71.61 |                  72.71 |                  42.37 |
| Forecasting Revenue Change (TPC-H Q6)               |                  17.22 |                  18.27 |                  20.90 |
| Volume Shipping Query (TPC-H Q7)                    |                  40.82 |                  50.72 |                  53.90 |
| National Market Share (TPC-H Q8)                    |                  50.53 |                  47.31 |                  54.60 |
| Product Type Profit Measure (TPC-H Q9)              |                  65.58 |                  66.29 |                  63.41 |
| Returned Item Reporting Query (TPC-H Q10)           |                  83.99 |                  85.88 |                  62.51 |
| Important Stock Identification (TPC-H Q11)          |                  47.43 |                  23.36 |                  24.62 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  34.89 |                  31.68 |                  34.21 |
| Customer Distribution (TPC-H Q13)                   |                  42.33 |                  39.09 |                  36.52 |
| Promotion Effect Query (TPC-H Q14)                  |                  30.75 |                  32.16 |                  33.20 |
| Top Supplier Query (TPC-H Q15)                      |                  54.27 |                  38.18 |                  44.13 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  36.05 |                  34.31 |                  33.16 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  30.92 |                  31.14 |                  50.01 |
| Large Volume Customer (TPC-H Q18)                   |                  43.48 |                  44.39 |                  42.37 |
| Discounted Revenue (TPC-H Q19)                      |                  46.70 |                 198.89 |                  42.01 |
| Potential Part Promotion (TPC-H Q20)                |                  43.94 |                  42.36 |                  43.83 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 384.71 |                 392.70 |                 396.14 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  56.50 |                  29.78 |                  29.87 |

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
