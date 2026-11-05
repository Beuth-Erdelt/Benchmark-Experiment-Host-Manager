## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 366s 
* Code: 1793810465
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
  * disk:876395
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
    * code:1793810465
* mariadbcs-1-1-1-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:876395
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
    * code:1793810465
* mariadbcs-1-1-1-1-3 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:876395
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
    * code:1793810465

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1793810465-5b8948c547-6mxq9: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       94.00 |           4.00 |            0.00 |         73.00 |           16.00 |              1 |           0 |             | None           |             0 | False         |               38.30 | False               |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         30 |            0.94 |             3842.03 |           2640.00 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-1-1-1-2 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         30 |            0.89 |             4064.42 |           2640.00 |          -1 | mariadbcs-1-1-1-1-2 |
| mariadbcs-1-1-1-1-3 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         30 |            0.91 |             3958.09 |           2640.00 |          -1 | mariadbcs-1-1-1-1-3 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         30 |            0.91 |             3953.80 |           7920.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mariadbcs-1-1-1-2-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-04 17:46:13 | 2026-11-04 17:46:42 |                   29 |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-1-1-1-2 |   mariadbcs-1-1-1-1-3 |
|:----------------------------------------------------|----------------------:|----------------------:|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               1254.34 |               1259.18 |               1238.46 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               4253.19 |               4317.68 |               4338.24 |
| Shipping Priority (TPC-H Q3)                        |               1614.45 |               1801.81 |               1768.23 |
| Order Priority Checking Query (TPC-H Q4)            |                547.69 |                564.26 |                602.91 |
| Local Supplier Volume (TPC-H Q5)                    |                855.90 |                961.13 |                895.74 |
| Forecasting Revenue Change (TPC-H Q6)               |                 81.23 |                 27.34 |                 52.69 |
| Volume Shipping Query (TPC-H Q7)                    |               1544.45 |               1672.21 |               1472.48 |
| National Market Share (TPC-H Q8)                    |               1078.77 |               1054.23 |               1074.62 |
| Product Type Profit Measure (TPC-H Q9)              |               1589.93 |               1375.67 |               1396.85 |
| Returned Item Reporting Query (TPC-H Q10)           |               1177.16 |                973.69 |               1121.10 |
| Important Stock Identification (TPC-H Q11)          |                936.83 |                900.60 |                903.49 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                494.07 |                532.76 |                584.82 |
| Customer Distribution (TPC-H Q13)                   |               1484.40 |               1492.75 |               1422.75 |
| Promotion Effect Query (TPC-H Q14)                  |                424.51 |                358.27 |                384.18 |
| Top Supplier Query (TPC-H Q15)                      |                709.61 |                717.42 |                705.64 |
| Parts/Supplier Relationship (TPC-H Q16)             |               1520.36 |               1486.05 |               1496.50 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               1011.44 |               1039.40 |               1032.68 |
| Large Volume Customer (TPC-H Q18)                   |                994.02 |                994.83 |                945.91 |
| Discounted Revenue (TPC-H Q19)                      |                595.86 |                573.83 |                591.60 |
| Potential Part Promotion (TPC-H Q20)                |               1289.77 |               1188.80 |               1117.50 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               2093.49 |               2124.93 |               2113.76 |
| Global Sales Opportunity Query (TPC-H Q22)          |                459.04 |                492.68 |                445.15 |

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
