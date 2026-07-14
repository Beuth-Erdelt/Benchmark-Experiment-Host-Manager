## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 6522s 
* Code: 1784031723
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
  * Database is persisted to disk of type cephcsi and size 1000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199512
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723
* MonetDB-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199623
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723
* MonetDB-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199627
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723
* MonetDB-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199547
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1784031723-8696dddc47-bx4kf: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              0 |           0 |             | None           |             0 | False         |               18.35 |
| MonetDB-1-2 |                2 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              0 |           0 |             | None           |             0 | False         |               18.35 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2555 |           29.30 |            12545.21 |           3099.80 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-1-2-1-1 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |        404 |            4.55 |            87693.30 |          19603.96 |          -1 | MonetDB-1-1-2-1-1 |
| MonetDB-1-2-1-1-1 | MonetDB-1       | MonetDB-1-2-1 | MonetDB-1-2-1-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |       2321 |           25.18 |            14662.83 |           3412.32 |          -1 | MonetDB-1-2-1-1-1 |
| MonetDB-1-2-2-1-1 | MonetDB-1       | MonetDB-1-2-2 | MonetDB-1-2-2-1 |                2 |        2 |               1 |           1 | 100.00 |               22 |        430 |            4.67 |            86100.83 |          18418.60 |          -1 | MonetDB-1-2-2-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2555 |           29.30 |            12545.21 |           3099.80 |          -1 |
| MonetDB-1-1-2 | MonetDB-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |        404 |            4.55 |            87693.30 |          19603.96 |          -1 |
| MonetDB-1-2-1 | MonetDB-1-2-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |       2321 |           25.18 |            14662.83 |           3412.32 |          -1 |
| MonetDB-1-2-2 | MonetDB-1-2-2 |                2 |        2 |               1 |           1 | 100.00 |               22 |        430 |            4.67 |            86100.83 |          18418.60 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |   MonetDB-1-1-2-1-1 |   MonetDB-1-2-1-1-1 |   MonetDB-1-2-2-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           380507.57 |            90166.21 |           343853.46 |            94150.05 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            39231.68 |              503.30 |            38819.07 |              505.91 |
| Shipping Priority (TPC-H Q3)                        |           159098.82 |             5773.04 |           156006.22 |             4681.90 |
| Order Priority Checking Query (TPC-H Q4)            |           146030.20 |             7882.44 |           138574.18 |             8816.53 |
| Local Supplier Volume (TPC-H Q5)                    |            16031.75 |             3267.06 |            11083.36 |             6807.39 |
| Forecasting Revenue Change (TPC-H Q6)               |             1254.08 |             1332.36 |             1124.13 |             1059.84 |
| Volume Shipping Query (TPC-H Q7)                    |             5744.71 |             4260.30 |             5906.07 |             4019.69 |
| National Market Share (TPC-H Q8)                    |           192159.04 |            12041.34 |           180176.18 |            12662.47 |
| Product Type Profit Measure (TPC-H Q9)              |            40472.91 |             5168.41 |            34297.40 |             4148.17 |
| Returned Item Reporting Query (TPC-H Q10)           |            74701.23 |             8165.85 |            61954.80 |             8937.97 |
| Important Stock Identification (TPC-H Q11)          |            11122.38 |              469.77 |             8195.91 |              466.09 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             9910.23 |             1073.95 |             3073.33 |             1390.82 |
| Customer Distribution (TPC-H Q13)                   |           317306.27 |            24164.25 |           263381.00 |            26818.89 |
| Promotion Effect Query (TPC-H Q14)                  |              754.77 |              653.23 |              749.29 |              743.20 |
| Top Supplier Query (TPC-H Q15)                      |            12347.46 |             1537.04 |             7246.03 |             1668.07 |
| Parts/Supplier Relationship (TPC-H Q16)             |             3641.21 |             2854.27 |             4290.91 |             2646.84 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           505277.90 |             1581.20 |           537225.61 |             2117.78 |
| Large Volume Customer (TPC-H Q18)                   |            44862.74 |             7737.06 |            48272.88 |             8162.54 |
| Discounted Revenue (TPC-H Q19)                      |             2725.01 |             3260.81 |             2298.18 |             1276.69 |
| Potential Part Promotion (TPC-H Q20)                |            11586.14 |             3290.00 |            10210.86 |             2633.67 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           546989.89 |           197237.61 |           429840.06 |           212197.41 |
| Global Sales Opportunity Query (TPC-H Q22)          |            10919.43 |             1769.46 |            11616.96 |             2474.70 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       986.35 |      2.51 |         120.22 |                120.22 |
| MonetDB-1-1-2-1 |       857.75 |      7.19 |         181.10 |                181.10 |
| MonetDB-1-2-1-1 |      1871.10 |      5.75 |         136.40 |                136.40 |
| MonetDB-1-2-2-1 |       902.30 |      6.21 |         193.39 |                193.39 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        31.80 |      0.21 |           0.40 |                  0.42 |
| MonetDB-1-1-2-1 |        31.80 |      0.43 |           0.40 |                  0.42 |
| MonetDB-1-2-1-1 |        32.37 |      0.32 |           0.40 |                  0.42 |
| MonetDB-1-2-2-1 |        32.37 |      0.29 |           0.40 |                  0.42 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
