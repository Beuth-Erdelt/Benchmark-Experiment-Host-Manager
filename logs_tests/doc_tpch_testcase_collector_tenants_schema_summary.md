## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2225s 
* Code: 1781296193
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
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921708
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921708
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921709
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921709
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921710
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921710
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921711
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921711
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781296193
    * TENANT_BY:schema
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |     1035.00 |           2.00 |            1.00 |        257.00 |          774.00 |              2 |           0 |          | schema         |             2 | False         |               10.43 |
| PostgreSQL-1-2 |                2 |    3 |     1035.00 |           2.00 |            1.00 |        257.00 |          774.00 |              2 |           0 |          | schema         |             2 | False         |               10.43 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        218 |            4.14 |             2607.19 |           1089.91 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        184 |            4.88 |             2214.28 |           1291.30 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        213 |            5.38 |             2006.47 |           1115.49 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        213 |            4.99 |             2163.02 |           1115.49 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        208 |            2.53 |             4267.08 |           1142.31 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        209 |            2.93 |             3683.44 |           1136.84 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         48 |            1.44 |             7508.77 |           4950.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         49 |            1.45 |             7471.84 |           4848.98 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           2 | 3.00 |               44 |        218 |            4.49 |             2402.72 |           2179.82 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |        213 |            5.18 |             2083.27 |           2230.99 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           2 | 3.00 |               44 |        209 |            2.72 |             3964.54 |           2273.68 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         49 |            1.44 |             7490.29 |           9697.96 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-1-1-2 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4978.29 |                5036.94 |                4683.98 |                4519.67 |               91574.00 |               91736.93 |                4664.82 |                4548.06 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                6264.01 |                5792.60 |               16422.80 |               16550.93 |               26773.01 |               17580.46 |                1227.79 |                1309.34 |
| Shipping Priority (TPC-H Q3)                        |                5200.22 |                4920.72 |               10436.10 |               11080.78 |               35308.68 |               31518.46 |                1505.22 |                1462.63 |
| Order Priority Checking Query (TPC-H Q4)            |                2530.58 |                2639.38 |                3999.86 |                3519.46 |                 751.40 |                1838.29 |                 791.72 |                 926.45 |
| Local Supplier Volume (TPC-H Q5)                    |               18738.16 |               18127.01 |               13249.72 |               13512.69 |                3067.75 |                4237.79 |                2215.68 |                2604.69 |
| Forecasting Revenue Change (TPC-H Q6)               |                1245.75 |                1039.81 |                1394.93 |                1224.54 |                1392.90 |                6529.02 |                1363.59 |                1247.51 |
| Forecasting Revenue Change (TPC-H Q7)               |               23445.25 |               21282.05 |               12800.15 |               15013.12 |                2115.32 |                2361.32 |                1698.85 |                1940.56 |
| National Market Share (TPC-H Q8)                    |                4834.87 |                5470.87 |                7838.71 |                6503.76 |               10662.23 |               15355.55 |                 712.24 |                 933.02 |
| Product Type Profit Measure (TPC-H Q9)              |               18615.54 |               18061.78 |               14276.78 |               21710.68 |                7442.01 |                7178.88 |                3186.99 |                2853.88 |
| Forecasting Revenue Change (TPC-H Q10)              |                3512.72 |                4191.47 |               11130.56 |                5928.38 |                1352.34 |                1552.53 |                1256.22 |                1389.96 |
| Important Stock Identification (TPC-H Q11)          |                3231.17 |                3163.00 |               29185.22 |               26443.59 |                 631.98 |                 592.60 |                 647.69 |                 652.39 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                4833.35 |                6284.35 |                4510.35 |                4418.24 |                2428.02 |                2551.63 |                2329.94 |                2303.16 |
| Customer Distribution (TPC-H Q13)                   |                1342.45 |                1390.44 |                1852.36 |                2725.87 |                1318.74 |                1314.81 |                1144.19 |                1263.76 |
| Forecasting Revenue Change (TPC-H Q14)              |                2121.31 |                2410.97 |                2573.50 |                1289.41 |                1561.50 |                1588.56 |                2202.19 |                1621.48 |
| Top Supplier Query (TPC-H Q15)                      |                1876.02 |                2392.07 |                1697.88 |                1884.00 |                1599.19 |                1716.75 |                1624.36 |                1976.57 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 784.12 |                 632.46 |                1307.14 |                 962.42 |                 927.59 |                 854.94 |                 551.08 |                 571.13 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               58189.33 |                9305.24 |               19700.90 |               18554.57 |                7012.33 |                8068.28 |                6320.03 |                6749.43 |
| Large Volume Customer (TPC-H Q18)                   |               24199.55 |               41562.53 |               31458.46 |               32377.17 |                5899.03 |                5985.78 |                8162.13 |                7637.19 |
| Discounted Revenue (TPC-H Q19)                      |                 630.51 |                9519.61 |                 347.21 |                 429.69 |                 168.86 |                 173.33 |                 168.14 |                 183.25 |
| Potential Part Promotion (TPC-H Q20)                |                7041.93 |                3862.46 |                8160.26 |                8085.47 |                1123.72 |                1108.29 |                1093.72 |                1173.75 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                4950.52 |                7053.39 |               14253.47 |               14711.79 |                2146.59 |                2639.85 |                2491.91 |                2990.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 264.13 |                2169.35 |                 366.03 |                 166.69 |                 149.62 |                 159.80 |                 369.55 |                 152.55 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       310.70 |      1.59 |           0.39 |                 11.97 |
| PostgreSQL-1-1-2-1 |       310.70 |      1.59 |           0.39 |                 11.97 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        77.84 |      0.89 |           0.01 |                  1.78 |
| PostgreSQL-1-1-2-1 |        77.84 |      0.89 |           0.01 |                  1.78 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       198.92 |      1.45 |           0.36 |                 11.41 |
| PostgreSQL-1-1-2-1 |       198.92 |      1.62 |           0.39 |                 11.36 |
| PostgreSQL-1-2-1-1 |       762.84 |      2.15 |           0.36 |                 10.76 |
| PostgreSQL-1-2-2-1 |        28.25 |      0.76 |           0.31 |                 10.29 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        26.38 |      0.67 |           0.28 |                  0.29 |
| PostgreSQL-1-1-2-1 |        25.22 |      0.42 |           0.29 |                  0.29 |
| PostgreSQL-1-2-1-1 |        24.76 |      0.80 |           0.29 |                  0.29 |
| PostgreSQL-1-2-2-1 |        26.76 |      0.02 |           0.29 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    4.00 |
| PostgreSQL-1-1-2-1 |                      3.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    4.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    6.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    6.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |

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
