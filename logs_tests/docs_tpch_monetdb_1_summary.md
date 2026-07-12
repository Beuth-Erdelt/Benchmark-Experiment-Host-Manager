## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 6028s 
* Code: 1783873656
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1104242
  * volume_size:1000G
  * volume_used:189G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:256Gi
  * limits_memory:256Gi
  * eval_parameters
    * code:1783873656

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1783873656-7c6765b7bc-hs8c4: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |     7283.00 |          21.00 |           22.00 |       2060.00 |         5176.00 |              8 |           0 |             | None           |             0 | False         |               49.43 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |        607 |            7.22 |            54225.20 |          13047.78 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |        607 |            7.22 |            54225.20 |          13047.78 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           171023.57 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             2746.62 |
| Shipping Priority (TPC-H Q3)                        |             6799.19 |
| Order Priority Checking Query (TPC-H Q4)            |             8005.93 |
| Local Supplier Volume (TPC-H Q5)                    |             5576.96 |
| Forecasting Revenue Change (TPC-H Q6)               |             3156.81 |
| Volume Shipping Query (TPC-H Q7)                    |             1444.33 |
| National Market Share (TPC-H Q8)                    |            42135.10 |
| Product Type Profit Measure (TPC-H Q9)              |            14017.73 |
| Returned Item Reporting Query (TPC-H Q10)           |             9673.67 |
| Important Stock Identification (TPC-H Q11)          |              785.20 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2882.65 |
| Customer Distribution (TPC-H Q13)                   |            45957.93 |
| Promotion Effect Query (TPC-H Q14)                  |             3915.06 |
| Top Supplier Query (TPC-H Q15)                      |             2745.12 |
| Parts/Supplier Relationship (TPC-H Q16)             |             3010.96 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             4816.47 |
| Large Volume Customer (TPC-H Q18)                   |             7774.84 |
| Discounted Revenue (TPC-H Q19)                      |             2276.29 |
| Potential Part Promotion (TPC-H Q20)                |             2887.31 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           243732.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |             1625.90 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      9200.84 |      5.65 |         184.82 |                184.83 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1587.06 |      1.08 |           0.04 |                 13.31 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      7682.34 |     69.25 |         246.76 |                246.76 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        31.28 |      0.25 |           0.40 |                  0.41 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
