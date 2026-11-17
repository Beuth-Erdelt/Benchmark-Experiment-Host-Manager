## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 466s 
* Code: 1794817279
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
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
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:902996
  * datadisk:512
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794817279

### Ingestion
* MariaDBCS-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794817279-7f45847dbf-xmqb8: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |      129.00 |           4.00 |            0.00 |         98.00 |           15.00 |              1 |         0 |             | None           |             0 | False         |               27.91 | False               |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         28 |            0.81 |             4453.60 |           2828.57 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         28 |            0.81 |             4453.60 |           2828.57 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadbcs-1-1-1-1-1 |
|:----------------------------------------------------|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               1243.39 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               3783.25 |
| Shipping Priority (TPC-H Q3)                        |               1604.69 |
| Order Priority Checking Query (TPC-H Q4)            |                604.23 |
| Local Supplier Volume (TPC-H Q5)                    |                961.91 |
| Forecasting Revenue Change (TPC-H Q6)               |                 25.87 |
| Volume Shipping Query (TPC-H Q7)                    |               1495.47 |
| National Market Share (TPC-H Q8)                    |               1123.19 |
| Product Type Profit Measure (TPC-H Q9)              |               1620.30 |
| Returned Item Reporting Query (TPC-H Q10)           |                961.63 |
| Important Stock Identification (TPC-H Q11)          |                943.88 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                521.90 |
| Customer Distribution (TPC-H Q13)                   |               1493.14 |
| Promotion Effect Query (TPC-H Q14)                  |                370.13 |
| Top Supplier Query (TPC-H Q15)                      |                357.18 |
| Parts/Supplier Relationship (TPC-H Q16)             |                903.33 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                750.56 |
| Large Volume Customer (TPC-H Q18)                   |                745.73 |
| Discounted Revenue (TPC-H Q19)                      |                438.47 |
| Potential Part Promotion (TPC-H Q20)                |               1145.20 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               2109.27 |
| Global Sales Opportunity Query (TPC-H Q22)          |                599.13 |

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
