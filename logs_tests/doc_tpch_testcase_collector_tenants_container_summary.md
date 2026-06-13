## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1885s 
* Code: 1781300697
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921721
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921673
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:923552
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:925123
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921711
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921675
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921678
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:925347
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781300697
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   tenant | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|---------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      835.00 |           2.00 |            0.00 |        290.00 |          537.00 |              1 |           0 |        0 | container      |             2 | False         |               12.93 |
| PostgreSQL-1-2 |                2 |    3 |      835.00 |           2.00 |            0.00 |        290.00 |          537.00 |              1 |           0 |        0 | container      |             2 | False         |               12.93 |
| PostgreSQL-2-1 |                1 |    3 |      842.00 |           1.00 |            0.00 |        292.00 |          547.00 |              1 |           0 |        1 | container      |             2 | False         |               12.83 |
| PostgreSQL-2-2 |                2 |    3 |      842.00 |           1.00 |            0.00 |        292.00 |          547.00 |              1 |           0 |        1 | container      |             2 | False         |               12.83 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        115 |            3.06 |             3533.59 |           2066.09 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        115 |            3.38 |             3191.77 |           2066.09 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         94 |            2.41 |             4479.14 |           2527.66 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         85 |            2.29 |             4719.86 |           2795.29 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        107 |            1.92 |             5610.82 |           2220.56 |
| PostgreSQL-2-2-1-1-1 | PostgreSQL-2-2-1 | PostgreSQL-2-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        115 |            2.25 |             4800.41 |           2066.09 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         45 |            1.44 |             7486.04 |           5280.00 |
| PostgreSQL-2-2-2-1-1 | PostgreSQL-2-2-2 | PostgreSQL-2-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         50 |            1.49 |             7237.24 |           4752.00 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        115 |            3.06 |             3533.59 |           2066.09 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |         94 |            2.41 |             4479.14 |           2527.66 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        115 |            3.38 |             3191.77 |           2066.09 |
| PostgreSQL-2-1-2 | PostgreSQL-2-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |         85 |            2.29 |             4719.86 |           2795.29 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        107 |            1.92 |             5610.82 |           2220.56 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         45 |            1.44 |             7486.04 |           5280.00 |
| PostgreSQL-2-2-1 | PostgreSQL-2-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        115 |            2.25 |             4800.41 |           2066.09 |
| PostgreSQL-2-2-2 | PostgreSQL-2-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         50 |            1.49 |             7237.24 |           4752.00 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-2-1-1-1-1 |   PostgreSQL-2-1-2-1-1 |   PostgreSQL-2-2-1-1-1 |   PostgreSQL-2-2-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5010.44 |                4836.61 |               35034.58 |                5167.51 |                4940.62 |                4926.79 |               33865.94 |                5032.64 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2877.31 |                8461.01 |               13600.34 |                1217.02 |                2203.04 |                5433.52 |               15962.14 |                1219.78 |
| Shipping Priority (TPC-H Q3)                        |               18258.60 |                5472.37 |               12497.13 |                1712.83 |               17824.88 |                7975.93 |               22155.04 |                1747.55 |
| Order Priority Checking Query (TPC-H Q4)            |                2134.16 |                2726.70 |                 788.89 |                 650.69 |                2111.55 |                2119.41 |                 870.14 |                 703.92 |
| Local Supplier Volume (TPC-H Q5)                    |                7309.85 |               10772.09 |                2120.53 |                2192.88 |               10168.46 |               11508.18 |                2245.27 |                1709.35 |
| Forecasting Revenue Change (TPC-H Q6)               |                1383.65 |                1576.41 |                1671.21 |                1492.43 |                1462.01 |                2007.78 |                1026.94 |                1701.18 |
| Forecasting Revenue Change (TPC-H Q7)               |                7431.82 |               11329.05 |                1521.27 |                2144.52 |                8926.54 |               14130.64 |                2112.05 |                2716.60 |
| National Market Share (TPC-H Q8)                    |                7471.24 |                2268.68 |                4381.43 |                1684.45 |                8013.72 |                4397.16 |                4793.64 |                1162.20 |
| Product Type Profit Measure (TPC-H Q9)              |               12620.20 |               14657.90 |                3052.62 |                2797.63 |               10005.90 |                3338.28 |                3157.66 |                3300.39 |
| Forecasting Revenue Change (TPC-H Q10)              |                2542.99 |                1617.85 |                1472.65 |                1848.26 |                3320.34 |                1935.01 |                1369.02 |                1854.33 |
| Important Stock Identification (TPC-H Q11)          |                2700.12 |                 598.39 |                 617.40 |                 806.64 |                2402.15 |                 584.78 |                 704.10 |                 704.36 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                2662.37 |                2693.39 |                1836.69 |                1681.48 |                2874.07 |                2607.18 |                2200.13 |                2506.01 |
| Customer Distribution (TPC-H Q13)                   |                1442.61 |                2339.91 |                1263.51 |                1400.17 |                1618.26 |                1311.68 |                1250.43 |                1342.30 |
| Forecasting Revenue Change (TPC-H Q14)              |                2075.46 |                1926.17 |                 990.60 |                1584.12 |                2063.91 |                1910.79 |                1172.20 |                1882.20 |
| Top Supplier Query (TPC-H Q15)                      |                1238.38 |                2469.97 |                1201.89 |                1470.20 |                1820.91 |                1652.58 |                2531.10 |                1901.07 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 519.69 |                 780.41 |                 729.44 |                1051.15 |                 527.21 |                 887.17 |                1357.09 |                 531.47 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                6216.68 |                6589.81 |                5975.61 |                3396.21 |                5780.02 |                5828.96 |                6486.92 |                7020.62 |
| Large Volume Customer (TPC-H Q18)                   |               13036.32 |                6080.04 |                5866.86 |                6150.62 |               17198.45 |                6339.61 |                6093.91 |                6219.71 |
| Discounted Revenue (TPC-H Q19)                      |                 503.73 |                 148.19 |                 158.18 |                 151.97 |                1502.79 |                 181.86 |                 164.24 |                 160.00 |
| Potential Part Promotion (TPC-H Q20)                |               10378.27 |                1101.32 |                1145.71 |                1268.46 |                3314.66 |                1026.12 |                1443.90 |                1072.45 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                4145.27 |                2927.13 |                3265.45 |                2647.79 |                4641.83 |                3129.50 |                2682.29 |                2957.81 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 191.90 |                 151.42 |                 140.25 |                 149.51 |                 601.85 |                 159.79 |                 270.90 |                 157.65 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       103.38 |      0.55 |           0.29 |                  7.15 |
| PostgreSQL-1-1-2-1 |       103.38 |      0.55 |           0.29 |                  7.15 |
| PostgreSQL-2-1-1-1 |       120.00 |      0.75 |           0.29 |                  7.20 |
| PostgreSQL-2-1-2-1 |       120.00 |      0.75 |           0.29 |                  7.20 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-2-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-2-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        39.85 |      0.40 |           0.01 |                  1.56 |
| PostgreSQL-1-1-2-1 |        39.85 |      0.40 |           0.01 |                  1.56 |
| PostgreSQL-2-1-1-1 |        38.12 |      0.41 |           0.01 |                  1.53 |
| PostgreSQL-2-1-2-1 |        38.12 |      0.41 |           0.01 |                  1.53 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        94.92 |      0.99 |           0.27 |                  6.48 |
| PostgreSQL-1-1-2-1 |        63.79 |      0.90 |           0.28 |                  6.24 |
| PostgreSQL-1-2-1-1 |       325.94 |      0.83 |           0.25 |                  5.98 |
| PostgreSQL-1-2-2-1 |        20.35 |      0.69 |           0.23 |                  4.73 |
| PostgreSQL-2-1-1-1 |        71.84 |      1.13 |           0.26 |                  6.46 |
| PostgreSQL-2-1-2-1 |        79.34 |      1.47 |           0.24 |                  6.25 |
| PostgreSQL-2-2-1-1 |        89.43 |      1.72 |           0.27 |                  4.70 |
| PostgreSQL-2-2-2-1 |        86.75 |      2.06 |           0.27 |                  4.83 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        12.77 |      0.49 |           0.26 |                  0.27 |
| PostgreSQL-1-1-2-1 |        13.00 |      0.52 |           0.28 |                  0.28 |
| PostgreSQL-1-2-1-1 |        12.82 |      0.00 |           0.24 |                  0.25 |
| PostgreSQL-1-2-2-1 |        12.96 |      0.39 |           0.29 |                  0.29 |
| PostgreSQL-2-1-1-1 |        12.70 |      0.41 |           0.26 |                  0.27 |
| PostgreSQL-2-1-2-1 |        13.36 |      0.01 |           0.26 |                  0.27 |
| PostgreSQL-2-2-1-1 |        13.09 |      0.43 |           0.27 |                  0.27 |
| PostgreSQL-2-2-2-1 |        13.00 |      0.01 |           0.28 |                  0.29 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    2.00 |
| PostgreSQL-2-1-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    2.00 |
| PostgreSQL-2-1-2-1 |                      2.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-1-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-1-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-2-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-2-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-2-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-2-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |

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
