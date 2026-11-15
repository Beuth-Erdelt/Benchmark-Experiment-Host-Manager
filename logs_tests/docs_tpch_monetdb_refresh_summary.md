## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 319s 
* Code: 1794683398
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1384228
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794683398
* monetdb-1-1-1-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1384228
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794683398
* monetdb-1-1-1-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1384228
  * datadisk:2937
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794683398

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794683398-65cf8f89c-7q2lv: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       61.00 |           3.00 |           18.00 |         15.00 |           20.00 |              8 |         0 |             | None           |             0 | False         |               59.02 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         11 |            0.11 |            33744.24 |           7200.00 |          -1 |
| monetdb-1-1-1-1-2 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         11 |            0.11 |            34046.18 |           7200.00 |          -1 |
| monetdb-1-1-1-1-3 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |         11 |            0.10 |            35937.91 |           7200.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         11 |            0.10 |            34562.64 |          21600.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| monetdb-1-1-1-2-1 | monetdb-1-1-1 | monetdb-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-14 20:14:39 | 2026-11-14 20:14:41 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-1-1-2 |   monetdb-1-1-1-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             1455.87 |             1241.92 |             1318.81 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               32.17 |               31.93 |               24.97 |
| Shipping Priority (TPC-H Q3)                        |               95.23 |               91.47 |              140.48 |
| Order Priority Checking Query (TPC-H Q4)            |              143.04 |              165.59 |              198.73 |
| Local Supplier Volume (TPC-H Q5)                    |               97.34 |               71.93 |               75.13 |
| Forecasting Revenue Change (TPC-H Q6)               |               25.58 |               24.63 |               25.28 |
| Volume Shipping Query (TPC-H Q7)                    |              133.47 |               70.98 |               70.32 |
| National Market Share (TPC-H Q8)                    |              194.06 |              194.69 |              314.34 |
| Product Type Profit Measure (TPC-H Q9)              |               83.00 |              147.62 |              109.96 |
| Returned Item Reporting Query (TPC-H Q10)           |              175.57 |              139.64 |              167.14 |
| Important Stock Identification (TPC-H Q11)          |               18.18 |               19.72 |               21.19 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               54.28 |               47.90 |               50.28 |
| Customer Distribution (TPC-H Q13)                   |              403.71 |              340.12 |              352.92 |
| Promotion Effect Query (TPC-H Q14)                  |               32.84 |               37.84 |               34.76 |
| Top Supplier Query (TPC-H Q15)                      |               35.54 |               43.35 |               43.92 |
| Parts/Supplier Relationship (TPC-H Q16)             |               89.79 |               98.16 |              101.15 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               40.57 |               45.32 |               47.05 |
| Large Volume Customer (TPC-H Q18)                   |              567.51 |              147.88 |              166.15 |
| Discounted Revenue (TPC-H Q19)                      |              164.66 |               69.59 |               61.29 |
| Potential Part Promotion (TPC-H Q20)                |               65.44 |              250.20 |               35.51 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1479.59 |             1527.94 |             1505.55 |
| Global Sales Opportunity Query (TPC-H Q22)          |               45.19 |              122.10 |               98.45 |

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
