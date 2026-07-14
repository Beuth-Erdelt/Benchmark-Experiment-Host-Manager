## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 5775s 
* Code: 1784038339
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
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199550
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199462
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199464
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199464
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199464
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1784038339-7cb6467b-8bnds: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              0 |           0 |             | None           |             0 | False         |               18.35 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2360 |           25.85 |            14292.09 |           3355.93 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-1-2-1-1 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |        409 |            4.32 |            91829.06 |          19364.30 |          -1 | MonetDB-1-1-2-1-1 |
| MonetDB-1-1-3-1-1 | MonetDB-1       | MonetDB-1-1-3 | MonetDB-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |       2521 |           20.09 |            18687.70 |           3141.61 |          -1 | MonetDB-1-1-3-1-1 |
| MonetDB-1-1-3-1-2 | MonetDB-1       | MonetDB-1-1-3 | MonetDB-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |       2561 |           20.48 |            18347.50 |           3092.54 |          -1 | MonetDB-1-1-3-1-2 |
| MonetDB-1-1-3-1-3 | MonetDB-1       | MonetDB-1-1-3 | MonetDB-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |       2583 |           23.95 |            15672.80 |           3066.20 |          -1 | MonetDB-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2360 |           25.85 |            14292.09 |           3355.93 |          -1 |
| MonetDB-1-1-2 | MonetDB-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |        409 |            4.32 |            91829.06 |          19364.30 |          -1 |
| MonetDB-1-1-3 | MonetDB-1-1-3 |                1 |        3 |               1 |           3 | 100.00 |               66 |       2583 |           21.44 |            17515.66 |           9198.61 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |   MonetDB-1-1-2-1-1 |   MonetDB-1-1-3-1-1 |   MonetDB-1-1-3-1-2 |   MonetDB-1-1-3-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           345510.64 |            83581.58 |           432792.46 |           378821.83 |           365983.77 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            37824.54 |              505.99 |              470.61 |             3942.92 |            17136.05 |
| Shipping Priority (TPC-H Q3)                        |           145121.22 |             4339.19 |            44586.97 |            95130.53 |            94589.62 |
| Order Priority Checking Query (TPC-H Q4)            |           150159.15 |             7972.45 |            40322.32 |            39343.29 |            39730.09 |
| Local Supplier Volume (TPC-H Q5)                    |            13639.77 |             2576.59 |            13308.41 |            13211.69 |            13738.45 |
| Forecasting Revenue Change (TPC-H Q6)               |             1588.79 |             1405.06 |             5177.03 |             6929.45 |             5369.13 |
| Volume Shipping Query (TPC-H Q7)                    |             5796.60 |             4632.13 |             8293.63 |             7398.56 |             9809.22 |
| National Market Share (TPC-H Q8)                    |           205834.17 |            12995.63 |           202545.83 |           203563.03 |           202491.55 |
| Product Type Profit Measure (TPC-H Q9)              |            33555.04 |             3745.82 |            30535.53 |            28597.56 |            28434.93 |
| Returned Item Reporting Query (TPC-H Q10)           |            73743.04 |             7570.81 |            39307.30 |            39826.66 |            40103.74 |
| Important Stock Identification (TPC-H Q11)          |             7787.35 |              480.61 |             2673.13 |             2584.45 |             2508.71 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3202.88 |             1356.21 |             3709.38 |             3200.02 |             4097.94 |
| Customer Distribution (TPC-H Q13)                   |           283869.91 |            24407.00 |           225427.59 |           226670.62 |           221943.77 |
| Promotion Effect Query (TPC-H Q14)                  |              594.09 |              743.50 |              468.74 |              774.16 |              748.18 |
| Top Supplier Query (TPC-H Q15)                      |             6460.85 |             2143.70 |             3580.36 |             1818.34 |             6571.20 |
| Parts/Supplier Relationship (TPC-H Q16)             |             3662.20 |             2986.18 |             5686.28 |             5500.22 |             5497.51 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           531005.84 |             1634.87 |           571005.52 |           571663.09 |           571519.36 |
| Large Volume Customer (TPC-H Q18)                   |            58555.41 |             7240.35 |            71217.61 |            73774.63 |            71086.52 |
| Discounted Revenue (TPC-H Q19)                      |             3125.98 |             1207.09 |             4145.76 |             1205.47 |             3916.92 |
| Potential Part Promotion (TPC-H Q20)                |            10407.51 |             3100.78 |            15472.85 |            15281.05 |            15004.89 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           407037.27 |           212794.11 |           771345.24 |           817269.84 |           840518.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |             8983.04 |             1750.74 |             8420.04 |             3403.99 |             1809.50 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1026.48 |      2.98 |         120.02 |                120.02 |
| MonetDB-1-1-2-1 |       822.70 |      4.64 |         192.97 |                192.97 |
| MonetDB-1-1-3-1 |      2823.36 |      5.78 |         253.95 |                255.99 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        31.55 |      0.34 |           0.38 |                  0.39 |
| MonetDB-1-1-2-1 |        31.55 |      0.36 |           0.38 |                  0.39 |
| MonetDB-1-1-3-1 |        71.71 |      0.76 |           0.39 |                  0.40 |

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
