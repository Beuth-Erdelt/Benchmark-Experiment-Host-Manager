## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 708s 
* Code: 1782332846
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265547
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782332846

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      367.00 |           1.00 |           25.00 |         36.00 |          302.00 |              8 |           0 |             | None           |             0 | False         |                9.81 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.15 |             3301.61 |            740.19 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.15 |             3301.61 |            740.19 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             8140.58 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              542.66 |
| Shipping Priority (TPC-H Q3)                        |             1629.37 |
| Order Priority Checking Query (TPC-H Q4)            |              372.68 |
| Local Supplier Volume (TPC-H Q5)                    |             1190.27 |
| Forecasting Revenue Change (TPC-H Q6)               |             1298.28 |
| Volume Shipping Query (TPC-H Q7)                    |             1265.87 |
| National Market Share (TPC-H Q8)                    |             2202.44 |
| Product Type Profit Measure (TPC-H Q9)              |             2062.75 |
| Returned Item Reporting Query (TPC-H Q10)           |              896.30 |
| Important Stock Identification (TPC-H Q11)          |              150.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3196.19 |
| Customer Distribution (TPC-H Q13)                   |             3191.68 |
| Promotion Effect Query (TPC-H Q14)                  |            12756.89 |
| Top Supplier Query (TPC-H Q15)                      |             2071.70 |
| Parts/Supplier Relationship (TPC-H Q16)             |              238.70 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               62.08 |
| Large Volume Customer (TPC-H Q18)                   |             3098.08 |
| Discounted Revenue (TPC-H Q19)                      |               97.96 |
| Potential Part Promotion (TPC-H Q20)                |              227.04 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            57943.45 |
| Global Sales Opportunity Query (TPC-H Q22)          |              130.66 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
