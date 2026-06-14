## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2564s 
* Code: 1781434902
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.12.
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
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102036
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102036
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102038
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102038
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102039
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102039
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102188
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102188
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434902
    * TENANT_BY:database
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781434902-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    3 |      396.00 |           3.00 |            1.00 |        396.00 |         1036.00 |              2 |           0 |               27.27 |
| 1781434902-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    3 |      396.00 |           3.00 |            1.00 |        396.00 |         1036.00 |              2 |           0 |               27.27 |
| 1781434902-PostgreSQL-1-2-0 |                2 | database       | False         |             2 |           0 |    3 |      396.00 |           3.00 |            1.00 |        396.00 |         1036.00 |              2 |           0 |               27.27 |
| 1781434902-PostgreSQL-1-2-1 |                2 | database       | False         |             2 |           1 |    3 |      396.00 |           3.00 |            1.00 |        396.00 |         1036.00 |              2 |           0 |               27.27 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        286 |            5.48 |             1971.88 |            830.77 |           0 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        275 |            6.11 |             1768.41 |            864.00 |           0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        252 |            6.00 |             1799.25 |            942.86 |           1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        239 |            5.78 |             1868.13 |            994.14 |           1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        223 |            3.52 |             3071.97 |           1065.47 |           0 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        226 |            3.72 |             2901.41 |           1051.33 |           0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         51 |            1.51 |             7140.40 |           4658.82 |           1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         51 |            1.55 |             6972.14 |           4658.82 |           1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           2 | 3.00 |               44 |        286 |            5.78 |             1867.37 |           1661.54 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |        252 |            5.89 |             1833.37 |           1885.71 |           1 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           2 | 3.00 |               44 |        226 |            3.62 |             2985.47 |           2102.65 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         51 |            1.53 |             7055.77 |           9317.65 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-1-1-2 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4740.77 |                4754.54 |                5260.80 |                5223.44 |               52839.41 |               50630.08 |                4776.28 |                4875.60 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                8785.13 |                9593.81 |               11452.26 |               11562.26 |               28140.06 |               29204.03 |                1072.10 |                1125.35 |
| Shipping Priority (TPC-H Q3)                        |               12959.14 |               13037.36 |               13034.89 |               12630.13 |               28962.14 |               30351.62 |                1496.45 |                1533.50 |
| Order Priority Checking Query (TPC-H Q4)            |                5527.47 |                6269.20 |                8327.45 |                8545.98 |                6710.23 |                6482.04 |                 837.01 |                 875.54 |
| Local Supplier Volume (TPC-H Q5)                    |               46433.22 |               44221.29 |               31656.20 |               31403.86 |               24973.39 |               24773.60 |                2907.00 |                2590.46 |
| Forecasting Revenue Change (TPC-H Q6)               |                 949.14 |                1151.10 |                1546.46 |                1648.47 |                1644.10 |                1556.19 |                1556.00 |                1603.43 |
| Forecasting Revenue Change (TPC-H Q7)               |               41194.64 |               38153.75 |               27261.79 |               26206.14 |               28901.04 |               28629.66 |                1957.63 |                2275.45 |
| National Market Share (TPC-H Q8)                    |               13121.47 |               11903.16 |               12781.24 |               12367.31 |               16264.66 |               16168.51 |                 981.27 |                1442.70 |
| Product Type Profit Measure (TPC-H Q9)              |               37106.60 |               38703.46 |               33228.32 |               32022.18 |                3809.25 |                3398.62 |                4085.88 |                3119.23 |
| Forecasting Revenue Change (TPC-H Q10)              |                9597.65 |                7908.64 |                7634.82 |                8142.88 |                2231.65 |                1785.15 |                2024.30 |                1973.25 |
| Important Stock Identification (TPC-H Q11)          |                8202.40 |               10895.32 |                8486.05 |                7526.52 |                 635.09 |                 807.34 |                 869.52 |                 967.78 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                6630.86 |                5135.20 |                5168.46 |                7670.72 |                2701.15 |                2536.89 |                2139.20 |                2303.50 |
| Customer Distribution (TPC-H Q13)                   |                1509.09 |                1512.91 |                1344.93 |                1336.10 |                1571.18 |                1959.91 |                1355.19 |                1473.94 |
| Forecasting Revenue Change (TPC-H Q14)              |                1840.23 |                1504.36 |                1729.10 |                2231.98 |                1581.83 |                1557.09 |                2148.52 |                2089.39 |
| Top Supplier Query (TPC-H Q15)                      |                1852.94 |                2057.99 |                1908.91 |                2106.36 |                2041.80 |                2656.02 |                1581.50 |                1548.61 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1126.70 |                1039.47 |                2173.86 |                 722.84 |                1183.23 |                3163.32 |                 531.67 |                 561.29 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               35422.53 |               22313.41 |               31278.88 |               17394.84 |                5539.70 |                7612.61 |                6710.26 |                6681.90 |
| Large Volume Customer (TPC-H Q18)                   |               35594.93 |               30025.93 |               30496.97 |               30851.00 |                6095.68 |                5376.81 |                7556.81 |                7119.53 |
| Discounted Revenue (TPC-H Q19)                      |                 458.31 |                1777.46 |                1121.14 |                 429.87 |                 163.31 |                 150.53 |                 176.36 |                 165.96 |
| Potential Part Promotion (TPC-H Q20)                |                5677.57 |                9288.20 |                4725.51 |                5958.50 |                 993.76 |                 911.29 |                1105.50 |                1221.81 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                4390.27 |               11192.23 |                5508.04 |               11408.68 |                2523.01 |                2775.68 |                2944.20 |                2813.62 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 153.96 |                 218.42 |                 398.36 |                 495.80 |                 152.30 |                 140.17 |                 147.02 |                 151.59 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       395.36 |      2.03 |           0.39 |                 11.71 |
| PostgreSQL-1-1-2-1 |       395.36 |      2.03 |           0.39 |                 11.71 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        67.97 |      0.90 |           0.00 |                  0.16 |
| PostgreSQL-1-1-2-1 |        67.97 |      0.90 |           0.00 |                  0.16 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       229.95 |      1.53 |           0.40 |                 11.44 |
| PostgreSQL-1-1-2-1 |       203.30 |      2.64 |           0.39 |                 11.23 |
| PostgreSQL-1-2-1-1 |       928.14 |      1.41 |           0.37 |                 10.78 |
| PostgreSQL-1-2-2-1 |       187.59 |      4.23 |           0.38 |                 10.20 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        24.73 |      0.25 |           0.26 |                  0.27 |
| PostgreSQL-1-1-2-1 |        24.45 |      0.36 |           0.28 |                  0.28 |
| PostgreSQL-1-2-1-1 |        12.67 |      0.01 |           0.28 |                  0.28 |
| PostgreSQL-1-2-2-1 |        23.06 |      0.01 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                       13.00 |                                    6.00 |
| PostgreSQL-1-1-2-1 |                      2.00 |                                     0.00 |                                             0.00 |                       13.00 |                                    6.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   11.00 |
| PostgreSQL-1-1-2-1 |                      2.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   13.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       11.00 |                                   14.00 |
| PostgreSQL-1-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                   10.00 |

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
