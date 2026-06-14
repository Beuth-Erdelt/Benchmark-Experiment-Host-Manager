## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2112s 
* Code: 1781434910
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
  * disk:1102034
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102036
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102038
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102039
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102034
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102036
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102039
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102039
  * volume_size:15G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434910
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

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781434910-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    3 |      960.00 |           2.00 |            0.00 |        313.00 |          639.00 |              1 |           0 |               11.25 |
| 1781434910-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    3 |      945.00 |           2.00 |            0.00 |        308.00 |          634.00 |              1 |           0 |               11.43 |
| 1781434910-PostgreSQL-1-2-0 |                2 | container      | False         |             2 |           0 |    3 |      960.00 |           2.00 |            0.00 |        313.00 |          639.00 |              1 |           0 |               11.25 |
| 1781434910-PostgreSQL-2-2-1 |                2 | container      | False         |             2 |           1 |    3 |      945.00 |           2.00 |            0.00 |        308.00 |          634.00 |              1 |           0 |               11.43 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        147 |            4.24 |             2549.34 |           1616.33 |           0 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        160 |            4.17 |             2592.00 |           1485.00 |           1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        148 |            3.88 |             2782.60 |           1605.41 |           0 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        144 |            3.32 |             3252.53 |           1650.00 |           1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        137 |            2.55 |             4241.86 |           1734.31 |           0 |
| PostgreSQL-2-2-1-1-1 | PostgreSQL-2-2-1 | PostgreSQL-2-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        125 |            2.35 |             4591.24 |           1900.80 |           1 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         48 |            1.47 |             7365.11 |           4950.00 |           0 |
| PostgreSQL-2-2-2-1-1 | PostgreSQL-2-2-2 | PostgreSQL-2-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         53 |            1.57 |             6881.85 |           4483.02 |           1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        147 |            4.24 |             2549.34 |           1616.33 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |        148 |            3.88 |             2782.60 |           1605.41 |           0 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        160 |            4.17 |             2592.00 |           1485.00 |           1 |
| PostgreSQL-2-1-2 | PostgreSQL-2-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |        144 |            3.32 |             3252.53 |           1650.00 |           1 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        137 |            2.55 |             4241.86 |           1734.31 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         48 |            1.47 |             7365.11 |           4950.00 |           0 |
| PostgreSQL-2-2-1 | PostgreSQL-2-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        125 |            2.35 |             4591.24 |           1900.80 |           1 |
| PostgreSQL-2-2-2 | PostgreSQL-2-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         53 |            1.57 |             6881.85 |           4483.02 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-2-1-1-1-1 |   PostgreSQL-2-1-2-1-1 |   PostgreSQL-2-2-1-1-1 |   PostgreSQL-2-2-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5413.10 |                5032.65 |               47454.81 |                4741.74 |                5002.03 |                4938.50 |               45433.50 |                5240.82 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                7544.29 |                3707.42 |               16431.35 |                1049.81 |                6502.72 |                5799.67 |               16075.95 |                1034.13 |
| Shipping Priority (TPC-H Q3)                        |               11503.90 |                7288.73 |               19357.85 |                1489.61 |                8520.43 |                5795.33 |               15933.38 |                1413.31 |
| Order Priority Checking Query (TPC-H Q4)            |                9646.09 |                6557.43 |                 606.47 |                 783.93 |                2865.25 |                3897.41 |                 868.80 |                 925.36 |
| Local Supplier Volume (TPC-H Q5)                    |               15271.46 |               16727.20 |                2406.49 |                2349.60 |               19115.46 |               16119.92 |                1552.63 |                2549.76 |
| Forecasting Revenue Change (TPC-H Q6)               |                2160.93 |                1804.67 |                2109.98 |                1864.49 |                1758.12 |                1093.61 |                1543.35 |                1660.31 |
| Forecasting Revenue Change (TPC-H Q7)               |               16320.43 |               21450.23 |                2628.13 |                1583.12 |               27453.73 |               18946.80 |                2270.89 |                2281.68 |
| National Market Share (TPC-H Q8)                    |                5620.69 |                5363.01 |                6744.93 |                 623.54 |                5785.29 |                4943.49 |                5828.51 |                1635.11 |
| Product Type Profit Measure (TPC-H Q9)              |               17846.14 |               18333.68 |                3822.02 |                3709.29 |               22046.54 |               22522.12 |                3455.42 |                3697.31 |
| Forecasting Revenue Change (TPC-H Q10)              |                4113.75 |                4324.79 |                1315.98 |                1711.42 |                5817.32 |                5064.84 |                1496.27 |                1913.16 |
| Important Stock Identification (TPC-H Q11)          |                6465.13 |                3595.62 |                 847.30 |                 669.91 |                3595.16 |                4743.49 |                1227.09 |                 920.40 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                3225.95 |                2433.01 |                2607.17 |                2428.75 |                3314.18 |                2591.78 |                2568.45 |                1919.29 |
| Customer Distribution (TPC-H Q13)                   |                1316.62 |                1518.78 |                2990.00 |                1450.38 |                2127.86 |                1324.43 |                1944.37 |                1383.09 |
| Forecasting Revenue Change (TPC-H Q14)              |                2014.56 |                2411.35 |                1880.75 |                2341.10 |                1602.39 |                1730.18 |                1621.98 |                2172.04 |
| Top Supplier Query (TPC-H Q15)                      |                2337.58 |                2521.38 |                2063.74 |                2401.03 |                2361.81 |                2251.80 |                2292.62 |                2074.66 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 719.00 |                1183.89 |                 988.93 |                 558.90 |                1174.90 |                 526.79 |                 841.43 |                 518.79 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               10502.39 |               15001.68 |                6568.16 |                5656.93 |                9594.85 |               14273.53 |                6832.99 |                5455.07 |
| Large Volume Customer (TPC-H Q18)                   |               13083.63 |               17740.71 |                7532.38 |                6019.42 |               17274.11 |               18923.03 |                5671.51 |                8619.26 |
| Discounted Revenue (TPC-H Q19)                      |                1438.56 |                 636.74 |                 186.22 |                 184.42 |                 880.40 |                 210.10 |                 324.54 |                 178.64 |
| Potential Part Promotion (TPC-H Q20)                |                3202.21 |                3147.04 |                1052.55 |                1043.61 |                6724.39 |                2506.75 |                 879.17 |                1085.90 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                3883.68 |                4303.94 |                3265.44 |                3303.31 |                4989.99 |                3111.93 |                2699.84 |                3192.99 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 270.28 |                 168.20 |                 255.28 |                 177.40 |                 143.93 |                 162.39 |                 156.89 |                 153.51 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       147.14 |      0.91 |           0.28 |                  6.65 |
| PostgreSQL-1-1-2-1 |       147.14 |      0.91 |           0.28 |                  6.65 |
| PostgreSQL-2-1-1-1 |       136.22 |      0.81 |           0.28 |                  6.61 |
| PostgreSQL-2-1-2-1 |       136.22 |      0.81 |           0.28 |                  6.61 |

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
| PostgreSQL-1-1-1-1 |        34.47 |      0.50 |           0.00 |                  0.54 |
| PostgreSQL-1-1-2-1 |        34.47 |      0.50 |           0.00 |                  0.54 |
| PostgreSQL-2-1-1-1 |        35.17 |      0.31 |           0.00 |                  0.90 |
| PostgreSQL-2-1-2-1 |        35.17 |      0.31 |           0.00 |                  0.90 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       101.06 |      1.07 |           0.27 |                  6.07 |
| PostgreSQL-1-1-2-1 |       106.74 |      1.23 |           0.28 |                  6.12 |
| PostgreSQL-1-2-1-1 |        84.95 |      1.46 |           0.23 |                  4.63 |
| PostgreSQL-1-2-2-1 |        56.92 |      1.51 |           0.28 |                  4.70 |
| PostgreSQL-2-1-1-1 |        94.40 |      1.11 |           0.29 |                  6.12 |
| PostgreSQL-2-1-2-1 |        99.29 |      1.14 |           0.28 |                  6.15 |
| PostgreSQL-2-2-1-1 |       375.23 |      1.66 |           0.23 |                  5.98 |
| PostgreSQL-2-2-2-1 |        69.39 |      1.68 |           0.25 |                  4.82 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        12.29 |      0.39 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2-1 |        12.07 |      0.43 |           0.26 |                  0.26 |
| PostgreSQL-1-2-1-1 |        11.98 |      0.39 |           0.26 |                  0.26 |
| PostgreSQL-1-2-2-1 |        12.05 |      0.37 |           0.26 |                  0.26 |
| PostgreSQL-2-1-1-1 |        11.79 |      0.01 |           0.29 |                  0.30 |
| PostgreSQL-2-1-2-1 |        12.70 |      0.75 |           0.29 |                  0.30 |
| PostgreSQL-2-2-1-1 |        12.41 |      0.37 |           0.26 |                  0.26 |
| PostgreSQL-2-2-2-1 |        11.36 |      0.52 |           0.26 |                  0.27 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    2.00 |
| PostgreSQL-2-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    2.00 |
| PostgreSQL-2-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-1-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-2-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-2-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-2-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
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
