## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 846s 
* Code: 1779625885
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.8.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540590804992
  * Cores:96
  * host:6.8.0-111-generic
  * node:cl-worker23
  * disk:1231906
  * cpu_list:0-95
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1779625885

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1]]

#### Planned

* DBMS MySQL-1 - Pods [[1]]

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    1 |      443.00 |           1.00 |            8.00 |         90.00 |          325.00 |              8 |           0 |          | None           |             0 | False         |                8.13 |

### Execution

#### Per Connection

|               |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:--------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| MySQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 1.00 |            22.00 |      79.00 |            1.66 |             2248.82 |           1002.53 |

#### Per Phase

|             |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| MySQL-1-1-1 |             1.00 |     1.00 |        1.00 | 1.00 |            22.00 |      79.00 |            1.66 |             2248.82 |           1002.53 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1 |
|:----------------------------------------------------|----------------:|
| Pricing Summary Report (TPC-H Q1)                   |        13173.30 |
| Minimum Cost Supplier Query (TPC-H Q2)              |          188.91 |
| Shipping Priority (TPC-H Q3)                        |         2061.15 |
| Order Priority Checking Query (TPC-H Q4)            |          791.56 |
| Local Supplier Volume (TPC-H Q5)                    |         1951.46 |
| Forecasting Revenue Change (TPC-H Q6)               |         2373.51 |
| Forecasting Revenue Change (TPC-H Q7)               |         1345.30 |
| National Market Share (TPC-H Q8)                    |         4485.11 |
| Product Type Profit Measure (TPC-H Q9)              |         3221.55 |
| Forecasting Revenue Change (TPC-H Q10)              |         1812.60 |
| Important Stock Identification (TPC-H Q11)          |          235.92 |
| Shipping Modes and Order Priority (TPC-H Q12)       |         3548.38 |
| Customer Distribution (TPC-H Q13)                   |         5511.38 |
| Forecasting Revenue Change (TPC-H Q14)              |         2815.40 |
| Top Supplier Query (TPC-H Q15)                      |        19024.32 |
| Parts/Supplier Relationship (TPC-H Q16)             |          556.26 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |          486.70 |
| Large Volume Customer (TPC-H Q18)                   |         3218.41 |
| Discounted Revenue (TPC-H Q19)                      |          235.03 |
| Potential Part Promotion (TPC-H Q20)                |          422.04 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |         7978.46 |
| Global Sales Opportunity Query (TPC-H Q22)          |          277.28 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Workflow as planned
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
