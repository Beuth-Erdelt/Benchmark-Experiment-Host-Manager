## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 324s 
* Code: 1794836745
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['MariaDBCS'].
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
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269418
  * datadisk:512
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794836745
* mariadbcs-1-1-1-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269418
  * datadisk:512
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794836745
* mariadbcs-1-1-1-1-3 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269418
  * datadisk:512
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794836745

### Ingestion
* MariaDBCS-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794836745-588794b647-5fjnx: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       83.00 |           4.00 |            0.00 |         64.00 |           13.00 |              1 |         0 |             | None           |             0 | False         |               43.37 | False               |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         49 |            1.35 |             2667.69 |           1616.33 |          -1 |
| mariadbcs-1-1-1-1-2 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         40 |            1.37 |             2624.58 |           1980.00 |          -1 |
| mariadbcs-1-1-1-1-3 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |         40 |            1.34 |             2679.09 |           1980.00 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         49 |            1.35 |             2657.01 |           4848.98 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mariadbcs-1-1-1-2-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-16 14:50:11 | 2026-11-16 14:50:44 |                   33 |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-1-1-1-2 |   mariadbcs-1-1-1-1-3 |
|:----------------------------------------------------|----------------------:|----------------------:|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               1184.68 |               1174.08 |               1202.26 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               3536.83 |               3721.85 |               3681.23 |
| Shipping Priority (TPC-H Q3)                        |               1438.91 |               1465.45 |               1501.46 |
| Order Priority Checking Query (TPC-H Q4)            |               1513.13 |                519.01 |                536.59 |
| Local Supplier Volume (TPC-H Q5)                    |               3096.54 |               4177.24 |               4185.02 |
| Forecasting Revenue Change (TPC-H Q6)               |                577.29 |                609.55 |                630.98 |
| Volume Shipping Query (TPC-H Q7)                    |               3606.63 |               3807.16 |               3781.70 |
| National Market Share (TPC-H Q8)                    |               2027.40 |               2105.09 |               2153.19 |
| Product Type Profit Measure (TPC-H Q9)              |              10034.32 |               4235.13 |               4235.78 |
| Returned Item Reporting Query (TPC-H Q10)           |               9372.67 |               2981.79 |               2907.86 |
| Important Stock Identification (TPC-H Q11)          |               2320.75 |               1832.35 |               1865.52 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                998.17 |                682.91 |                669.87 |
| Customer Distribution (TPC-H Q13)                   |               1311.11 |                644.14 |                577.23 |
| Promotion Effect Query (TPC-H Q14)                  |                730.14 |               1230.44 |               1161.65 |
| Top Supplier Query (TPC-H Q15)                      |                391.53 |               1165.70 |               1117.27 |
| Parts/Supplier Relationship (TPC-H Q16)             |                740.35 |               1462.22 |               1776.61 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                773.17 |                994.00 |                772.99 |
| Large Volume Customer (TPC-H Q18)                   |                644.49 |               1681.21 |               1818.31 |
| Discounted Revenue (TPC-H Q19)                      |                446.30 |                395.17 |                410.91 |
| Potential Part Promotion (TPC-H Q20)                |                906.37 |               1590.65 |               1474.72 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               1311.23 |               1318.59 |               1363.58 |
| Global Sales Opportunity Query (TPC-H Q22)          |                383.45 |                521.35 |                364.64 |

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
