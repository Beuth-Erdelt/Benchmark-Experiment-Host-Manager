## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 25192s 
* Code: 1784006384
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
  * Database is persisted to disk of type cephcsi and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1198794
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784006384

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1784006384-5c45c8fbb4-v77jt: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              8 |           0 |             | None           |             0 | False         |               18.35 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               21 |       5373 |            8.28 |            47743.39 |           1407.04 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               21 |       5373 |            8.28 |            47743.39 |           1407.04 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           309827.03 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              547.05 |
| Shipping Priority (TPC-H Q3)                        |             6249.89 |
| Local Supplier Volume (TPC-H Q5)                    |           879691.18 |
| Forecasting Revenue Change (TPC-H Q6)               |             1518.85 |
| Volume Shipping Query (TPC-H Q7)                    |             4982.96 |
| National Market Share (TPC-H Q8)                    |            75733.41 |
| Product Type Profit Measure (TPC-H Q9)              |             7399.30 |
| Returned Item Reporting Query (TPC-H Q10)           |            11360.79 |
| Important Stock Identification (TPC-H Q11)          |              713.93 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1591.71 |
| Customer Distribution (TPC-H Q13)                   |            34001.50 |
| Promotion Effect Query (TPC-H Q14)                  |              833.30 |
| Top Supplier Query (TPC-H Q15)                      |             1995.43 |
| Parts/Supplier Relationship (TPC-H Q16)             |             4567.27 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             3689.23 |
| Large Volume Customer (TPC-H Q18)                   |             9213.20 |
| Discounted Revenue (TPC-H Q19)                      |             1831.63 |
| Potential Part Promotion (TPC-H Q20)                |             3653.47 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           391298.27 |
| Global Sales Opportunity Query (TPC-H Q22)          |             2270.00 |

### Errors (failed queries)

|                   |   Pricing Summary Report (TPC-H Q1) |   Minimum Cost Supplier Query (TPC-H Q2) |   Shipping Priority (TPC-H Q3) |   Order Priority Checking Query (TPC-H Q4) |   Local Supplier Volume (TPC-H Q5) |   Forecasting Revenue Change (TPC-H Q6) |   Volume Shipping Query (TPC-H Q7) |   National Market Share (TPC-H Q8) |   Product Type Profit Measure (TPC-H Q9) |   Returned Item Reporting Query (TPC-H Q10) |   Important Stock Identification (TPC-H Q11) |   Shipping Modes and Order Priority (TPC-H Q12) |   Customer Distribution (TPC-H Q13) |   Promotion Effect Query (TPC-H Q14) |   Top Supplier Query (TPC-H Q15) |   Parts/Supplier Relationship (TPC-H Q16) |   Small-Quantity-Order Revenue (TPC-H Q17) |   Large Volume Customer (TPC-H Q18) |   Discounted Revenue (TPC-H Q19) |   Potential Part Promotion (TPC-H Q20) |   Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |   Global Sales Opportunity Query (TPC-H Q22) |
|:------------------|------------------------------------:|-----------------------------------------:|-------------------------------:|-------------------------------------------:|-----------------------------------:|----------------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------------:|--------------------------------------------:|---------------------------------------------:|------------------------------------------------:|------------------------------------:|-------------------------------------:|---------------------------------:|------------------------------------------:|-------------------------------------------:|------------------------------------:|---------------------------------:|---------------------------------------:|------------------------------------------------------:|---------------------------------------------:|
| MonetDB-1-1-1-1-1 |                                0.00 |                                     0.00 |                           0.00 |                                       1.00 |                               0.00 |                                    0.00 |                               0.00 |                               0.00 |                                     0.00 |                                        0.00 |                                         0.00 |                                            0.00 |                                0.00 |                                 0.00 |                             0.00 |                                      0.00 |                                       0.00 |                                0.00 |                             0.00 |                                   0.00 |                                                  0.00 |                                         0.00 |
* Order Priority Checking Query (TPC-H Q4)
  * MonetDB-1-1-1-1-1: numRun 1: : java.sql.SQLNonTransientConnectionException: connection timed out

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      8738.85 |      5.95 |         181.43 |                181.43 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1589.01 |      1.07 |           0.03 |                 13.29 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1607.63 |      5.98 |         234.98 |                234.98 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        34.36 |      0.26 |           0.36 |                  0.37 |

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
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
