## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 625s 
* Code: 1782313711
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266128
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782313711

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    1 |      200.00 |           2.00 |           18.00 |         18.00 |          159.00 |              8 |           0 |             | None           |             0 | False         |               18.00 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         51 |            0.98 |             3834.80 |           1552.94 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         51 |            0.98 |             3834.80 |           1552.94 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           8342.62 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            113.67 |
| Shipping Priority (TPC-H Q3)                        |           1360.76 |
| Order Priority Checking Query (TPC-H Q4)            |            462.17 |
| Local Supplier Volume (TPC-H Q5)                    |           1024.24 |
| Forecasting Revenue Change (TPC-H Q6)               |           1141.52 |
| Volume Shipping Query (TPC-H Q7)                    |            750.78 |
| National Market Share (TPC-H Q8)                    |           2858.45 |
| Product Type Profit Measure (TPC-H Q9)              |           1963.78 |
| Returned Item Reporting Query (TPC-H Q10)           |           1000.15 |
| Important Stock Identification (TPC-H Q11)          |            166.90 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1888.96 |
| Customer Distribution (TPC-H Q13)                   |           3356.49 |
| Promotion Effect Query (TPC-H Q14)                  |           1335.93 |
| Top Supplier Query (TPC-H Q15)                      |          12776.72 |
| Parts/Supplier Relationship (TPC-H Q16)             |            390.43 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            274.93 |
| Large Volume Customer (TPC-H Q18)                   |           1704.47 |
| Discounted Revenue (TPC-H Q19)                      |            147.87 |
| Potential Part Promotion (TPC-H Q20)                |            263.45 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           4640.65 |
| Global Sales Opportunity Query (TPC-H Q22)          |            141.84 |

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
