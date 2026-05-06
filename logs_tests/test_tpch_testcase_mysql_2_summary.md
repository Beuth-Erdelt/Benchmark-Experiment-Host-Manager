## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 21702s 
* Code: 1777891777
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
  * RAM:541008474112
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:213863
  * datadisk:62501
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1777891777

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   MySQL-BHT-8-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           297515.95 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             3704.68 |
| Shipping Priority (TPC-H Q3)                        |            52674.58 |
| Order Priority Checking Query (TPC-H Q4)            |            15958.73 |
| Local Supplier Volume (TPC-H Q5)                    |            46692.27 |
| Forecasting Revenue Change (TPC-H Q6)               |            42538.08 |
| Forecasting Revenue Change (TPC-H Q7)               |            34182.94 |
| National Market Share (TPC-H Q8)                    |           110215.23 |
| Product Type Profit Measure (TPC-H Q9)              |            82494.03 |
| Forecasting Revenue Change (TPC-H Q10)              |            58764.24 |
| Important Stock Identification (TPC-H Q11)          |             7736.26 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            71748.57 |
| Customer Distribution (TPC-H Q13)                   |           290629.72 |
| Forecasting Revenue Change (TPC-H Q14)              |            56599.93 |
| Top Supplier Query (TPC-H Q15)                      |            48145.72 |
| Parts/Supplier Relationship (TPC-H Q16)             |             8209.30 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            13191.89 |
| Large Volume Customer (TPC-H Q18)                   |            60715.58 |
| Discounted Revenue (TPC-H Q19)                      |             4471.10 |
| Potential Part Promotion (TPC-H Q20)                |             9464.34 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           214700.09 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4945.47 |

### Loading [s]

| DBMS              |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| MySQL-BHT-8-1-1-1 |          17.00 |         2439.00 |         3.00 |    19686.00 |   22148.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS              |   Geo Times [s] |
|:------------------|----------------:|
| MySQL-BHT-8-1-1-1 |           34.04 |

### Power@Size ((3600*SF)/(geo times))

| DBMS              |   Power@Size [~Q/h] |
|:------------------|--------------------:|
| MySQL-BHT-8-1-1-1 |             1064.66 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS            |   time [s] |   count |    SF |   Throughput@Size |
|:----------------|-----------:|--------:|------:|------------------:|
| MySQL-BHT-8-1-1 |    1544.00 |    1.00 | 10.00 |            512.95 |

### Workflow

| DBMS              | orig_name       |    SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:------------------|:----------------|------:|-------:|-----------------:|-------------:|------------------:|----------------:|
| MySQL-BHT-8-1-1-1 | MySQL-BHT-8-1-1 | 10.00 |      8 |                1 |            1 |        1777911880 |      1777913424 |

#### Actual

* DBMS MySQL-BHT-8 - Pods [[1]]

#### Planned

* DBMS MySQL-BHT-8 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                       |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777891777-MySQL-BHT-8-1-1 |     19931.39 |      3.72 |          74.22 |                115.09 |

### Loading phase: component data generator

| DBMS                       |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777891777-MySQL-BHT-8-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                       |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777891777-MySQL-BHT-8-1-1 |        30.78 |      0.19 |           0.01 |                  1.31 |

### Execution phase: SUT deployment

| DBMS                       |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777891777-MySQL-BHT-8-1-1 |      3005.25 |      2.03 |          80.50 |                121.85 |

### Execution phase: component benchmarker

| DBMS                       |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------------|-------------:|----------:|---------------:|----------------------:|
| 1777891777-MySQL-BHT-8-1-1 |        21.28 |      0.42 |           0.39 |                  0.39 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
