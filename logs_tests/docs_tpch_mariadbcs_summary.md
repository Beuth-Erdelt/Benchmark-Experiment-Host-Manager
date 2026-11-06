## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 348s 
* Code: 1793710950
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDBCS'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:131397
  * datadisk:512
  * cpu_list:0-95
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793710950

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1793710950-775d9cf8f-hmhgf: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |      113.00 |           2.00 |            0.00 |         97.00 |            6.00 |              1 |           0 |             | None           |             0 | False         |               31.86 | False               |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         16 |            0.52 |             6964.00 |           4950.00 |          -1 | mariadbcs-1-1-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         16 |            0.52 |             6964.00 |           4950.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |
|:----------------------------------------------------|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               1055.29 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               1892.39 |
| Shipping Priority (TPC-H Q3)                        |                787.83 |
| Order Priority Checking Query (TPC-H Q4)            |                613.92 |
| Local Supplier Volume (TPC-H Q5)                    |                451.75 |
| Forecasting Revenue Change (TPC-H Q6)               |                 29.78 |
| Volume Shipping Query (TPC-H Q7)                    |               1004.73 |
| National Market Share (TPC-H Q8)                    |                581.94 |
| Product Type Profit Measure (TPC-H Q9)              |               1065.48 |
| Returned Item Reporting Query (TPC-H Q10)           |                738.23 |
| Important Stock Identification (TPC-H Q11)          |                426.98 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                298.57 |
| Customer Distribution (TPC-H Q13)                   |               1384.98 |
| Promotion Effect Query (TPC-H Q14)                  |                232.98 |
| Top Supplier Query (TPC-H Q15)                      |                160.57 |
| Parts/Supplier Relationship (TPC-H Q16)             |                512.26 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                468.21 |
| Large Volume Customer (TPC-H Q18)                   |                487.14 |
| Discounted Revenue (TPC-H Q19)                      |                258.61 |
| Potential Part Promotion (TPC-H Q20)                |                764.43 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               1374.58 |
| Global Sales Opportunity Query (TPC-H Q22)          |                396.06 |

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
