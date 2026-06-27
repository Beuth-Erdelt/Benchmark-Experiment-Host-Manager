## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 817s 
* Code: 1781467828
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:246260
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781467828

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1]]

#### Planned

* DBMS MySQL-1 - Pods [[1]]

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    3 |      284.00 |           1.00 |           24.00 |         54.00 |          201.00 |              8 |           0 |             | None           |             0 | False         |               38.03 |

### Execution

#### Per Connection

|                 | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        169 |            3.33 |             3346.01 |           1405.92 |          -1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        169 |            3.33 |             3346.01 |           1405.92 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          22978.40 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            307.68 |
| Shipping Priority (TPC-H Q3)                        |           4799.50 |
| Order Priority Checking Query (TPC-H Q4)            |           1459.10 |
| Local Supplier Volume (TPC-H Q5)                    |           5006.85 |
| Forecasting Revenue Change (TPC-H Q6)               |           4363.84 |
| Forecasting Revenue Change (TPC-H Q7)               |           2961.28 |
| National Market Share (TPC-H Q8)                    |          10254.50 |
| Product Type Profit Measure (TPC-H Q9)              |           7850.46 |
| Forecasting Revenue Change (TPC-H Q10)              |           4576.51 |
| Important Stock Identification (TPC-H Q11)          |            564.77 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           6342.61 |
| Customer Distribution (TPC-H Q13)                   |          19403.29 |
| Forecasting Revenue Change (TPC-H Q14)              |           4502.62 |
| Top Supplier Query (TPC-H Q15)                      |          44330.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |            996.19 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            868.70 |
| Large Volume Customer (TPC-H Q18)                   |           5139.17 |
| Discounted Revenue (TPC-H Q19)                      |            411.65 |
| Potential Part Promotion (TPC-H Q20)                |            831.02 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          14619.70 |
| Global Sales Opportunity Query (TPC-H Q22)          |            430.94 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       571.85 |      6.85 |          13.14 |                 21.24 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        11.67 |      0.45 |           0.01 |                  0.28 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       142.48 |      1.01 |          13.18 |                 21.29 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        14.07 |      0.02 |           0.31 |                  0.32 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.22 |                     0.01 |                0.04 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.52 |                     0.00 |                0.03 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
