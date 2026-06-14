## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1760s 
* Code: 1781434878
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
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102032
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434878
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102034
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434878
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102034
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434878
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102037
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434878
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102038
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434878
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102038
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434878

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      729.00 |           2.00 |           20.00 |        193.00 |          510.00 |              8 |           0 |             |                |             0 | False         |               14.81 |
| PostgreSQL-1-2 |                2 |    3 |      729.00 |           2.00 |           20.00 |        193.00 |          510.00 |              8 |           0 |             |                |             0 | False         |               14.81 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        117 |            2.48 |             4360.02 |           2030.77 |           0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        199 |            4.24 |             2544.44 |           1193.97 |           0 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        199 |            4.18 |             2581.10 |           1193.97 |           0 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        131 |            2.45 |             4401.84 |           1813.74 |           0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         59 |            1.56 |             6931.03 |           4027.12 |           0 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         61 |            1.73 |             6242.87 |           3895.08 |           0 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        117 |            2.48 |             4360.02 |           2030.77 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |        199 |            4.21 |             2562.70 |           2387.94 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        131 |            2.45 |             4401.84 |           1813.74 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         61 |            1.64 |             6577.96 |           7790.16 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5446.01 |                5151.99 |                4900.50 |               39435.20 |                5006.52 |                4914.22 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                1091.01 |                7519.95 |                7721.74 |               17466.20 |                1001.56 |                1308.93 |
| Shipping Priority (TPC-H Q3)                        |                1290.96 |                9192.56 |                9189.24 |               17880.28 |                1795.01 |                1393.09 |
| Order Priority Checking Query (TPC-H Q4)            |                1237.72 |                6850.90 |                6850.55 |                 926.18 |                 811.60 |                 794.29 |
| Local Supplier Volume (TPC-H Q5)                    |                2077.94 |               21023.77 |               21023.89 |                2381.23 |                2275.26 |                2384.90 |
| Forecasting Revenue Change (TPC-H Q6)               |                2040.62 |                1515.17 |                1505.93 |                1763.62 |                1857.72 |                1811.40 |
| Forecasting Revenue Change (TPC-H Q7)               |                2158.15 |               16465.97 |               16472.58 |                2338.01 |                2495.24 |                2411.39 |
| National Market Share (TPC-H Q8)                    |                1990.74 |                7099.77 |                7102.16 |                7101.80 |                 936.99 |                 790.05 |
| Product Type Profit Measure (TPC-H Q9)              |               48040.02 |               67605.81 |               67619.23 |                6254.58 |                6758.67 |                6386.80 |
| Forecasting Revenue Change (TPC-H Q10)              |                3125.60 |                2699.60 |                2657.89 |                3026.19 |                2320.24 |                2885.37 |
| Important Stock Identification (TPC-H Q11)          |                4032.91 |                5894.48 |                5942.47 |                 800.94 |                 573.69 |                1301.64 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                2901.85 |                3033.13 |                3039.71 |                1703.67 |                2288.79 |                2478.99 |
| Customer Distribution (TPC-H Q13)                   |                1843.93 |                1482.29 |                1623.14 |                1528.19 |                1217.51 |                1463.86 |
| Forecasting Revenue Change (TPC-H Q14)              |                2280.87 |                1927.95 |                1943.72 |                1584.50 |                1177.17 |                1910.80 |
| Top Supplier Query (TPC-H Q15)                      |                1838.43 |                1824.06 |                2009.14 |                1253.70 |                2330.11 |                1960.29 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 534.65 |                 811.66 |                 493.64 |                 544.07 |                 550.98 |                 834.84 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                9816.69 |               10157.61 |               10036.19 |                6241.92 |                5732.66 |                5043.87 |
| Large Volume Customer (TPC-H Q18)                   |               10936.27 |                8590.02 |                7897.99 |                8793.34 |                8781.08 |                8652.16 |
| Discounted Revenue (TPC-H Q19)                      |                 921.38 |                 728.05 |                 724.25 |                 172.96 |                 161.25 |                 260.00 |
| Potential Part Promotion (TPC-H Q20)                |                2103.17 |                4106.48 |                4473.81 |                1360.42 |                1015.24 |                1280.49 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                8007.27 |               12505.04 |               12650.91 |                5628.96 |                4998.72 |                5337.76 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 221.73 |                 158.62 |                 162.71 |                 152.50 |                 153.45 |                 139.52 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       126.47 |      0.64 |           0.29 |                  7.25 |
| PostgreSQL-1-1-2-1 |       126.47 |      0.64 |           0.29 |                  7.25 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        32.50 |      0.45 |           0.01 |                  0.39 |
| PostgreSQL-1-1-2-1 |        32.50 |      0.45 |           0.01 |                  0.39 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        95.35 |      1.07 |           0.29 |                  6.20 |
| PostgreSQL-1-1-2-1 |       229.56 |      2.43 |           0.46 |                  8.89 |
| PostgreSQL-1-2-1-1 |       513.16 |      1.70 |           0.23 |                  5.98 |
| PostgreSQL-1-2-2-1 |       118.39 |      4.20 |           0.39 |                  5.47 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        12.98 |      0.43 |           0.29 |                  0.29 |
| PostgreSQL-1-1-2-1 |        25.41 |      0.75 |           0.29 |                  0.29 |
| PostgreSQL-1-2-1-1 |        12.30 |      0.01 |           0.27 |                  0.28 |
| PostgreSQL-1-2-2-1 |        24.31 |      0.92 |           0.29 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       10.00 |                                    8.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                       10.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
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
