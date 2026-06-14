## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2676s 
* Code: 1781434893
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
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102037
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434893
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102037
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434893
    * TENANT_BY:schema
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
    * code:1781434893
    * TENANT_BY:schema
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
    * code:1781434893
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102187
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434893
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102187
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781434893
    * TENANT_BY:schema
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
    * code:1781434893
    * TENANT_BY:schema
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
    * code:1781434893
    * TENANT_BY:schema
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
| 1781434893-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    3 |      412.00 |           5.00 |            3.00 |        412.00 |         1086.00 |              2 |           0 |               26.21 |
| 1781434893-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    3 |      421.00 |           5.00 |            3.00 |        421.00 |         1086.00 |              2 |           0 |               25.65 |
| 1781434893-PostgreSQL-1-2-0 |                2 | schema         | False         |             2 |           0 |    3 |      412.00 |           5.00 |            3.00 |        412.00 |         1086.00 |              2 |           0 |               26.21 |
| 1781434893-PostgreSQL-1-2-1 |                2 | schema         | False         |             2 |           1 |    3 |      421.00 |           5.00 |            3.00 |        421.00 |         1086.00 |              2 |           0 |               25.65 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        300 |            7.36 |             1468.26 |            792.00 |           0 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        326 |            6.18 |             1747.07 |            728.83 |           0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        244 |            6.09 |             1774.04 |            973.77 |           1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        275 |            5.61 |             1925.50 |            864.00 |           1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        194 |            3.26 |             3308.35 |           1224.74 |           0 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        199 |            3.62 |             2986.58 |           1193.97 |           0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         48 |            1.46 |             7412.43 |           4950.00 |           1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         55 |            1.59 |             6792.08 |           4320.00 |           1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           2 | 3.00 |               44 |        326 |            6.74 |             1601.61 |           1457.67 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |        275 |            5.84 |             1848.22 |           1728.00 |           1 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           2 | 3.00 |               44 |        199 |            3.44 |             3143.35 |           2387.94 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         55 |            1.52 |             7095.48 |           8640.00 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-1-1-2 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5324.31 |                5343.18 |                4382.92 |                4328.93 |               58276.22 |               58685.06 |                5371.84 |                5266.86 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               11755.06 |               11759.69 |               14652.14 |               15004.32 |               25475.36 |               21273.74 |                1272.66 |                1369.05 |
| Shipping Priority (TPC-H Q3)                        |               17101.44 |               17086.44 |               16540.90 |               19122.15 |               21817.61 |               25583.88 |                1381.95 |                1725.84 |
| Order Priority Checking Query (TPC-H Q4)            |               11310.89 |               11430.47 |               12690.08 |               12862.28 |                5557.27 |                5114.52 |                1067.45 |                 691.39 |
| Local Supplier Volume (TPC-H Q5)                    |               35125.23 |               36612.44 |               35473.89 |               32693.94 |               25609.60 |               24013.92 |                1952.57 |                2350.82 |
| Forecasting Revenue Change (TPC-H Q6)               |                1705.93 |                1541.27 |                1923.57 |                1627.81 |                1624.56 |                1893.86 |                1839.26 |                1799.63 |
| Forecasting Revenue Change (TPC-H Q7)               |               31089.96 |               40409.53 |               25499.76 |               25578.32 |               13892.50 |               15845.76 |                3032.84 |                2751.90 |
| National Market Share (TPC-H Q8)                    |               20960.34 |               16722.92 |                9640.50 |                9702.82 |                6836.08 |                5892.19 |                 760.74 |                1236.92 |
| Product Type Profit Measure (TPC-H Q9)              |               42972.59 |               82961.26 |               27515.65 |               62841.62 |                3645.18 |                5841.14 |                3470.88 |                6184.75 |
| Forecasting Revenue Change (TPC-H Q10)              |                9649.04 |                7741.87 |                6938.31 |                4611.31 |                1434.69 |                1392.24 |                1392.94 |                1383.68 |
| Important Stock Identification (TPC-H Q11)          |               16603.21 |                4207.08 |               11646.80 |                6626.99 |                 715.56 |                 583.41 |                1004.47 |                 797.91 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               11552.19 |                6666.83 |                6300.74 |                7876.82 |                2414.20 |                2676.94 |                2355.97 |                1974.60 |
| Customer Distribution (TPC-H Q13)                   |                2195.87 |                1684.78 |                1540.30 |                1567.04 |                1525.32 |                1848.13 |                1327.79 |                1994.95 |
| Forecasting Revenue Change (TPC-H Q14)              |                2198.83 |                1942.86 |                1848.27 |                1426.16 |                2023.27 |                2244.85 |                1555.46 |                1771.51 |
| Top Supplier Query (TPC-H Q15)                      |                2195.92 |                1441.80 |                1062.90 |                1341.40 |                2172.14 |                2207.29 |                2248.02 |                1863.68 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1009.91 |                1097.44 |                2261.94 |                 930.69 |                 771.77 |                1643.43 |                 539.09 |                 635.65 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               27092.43 |               41442.33 |               25749.51 |               32058.49 |                7629.60 |                9318.12 |                5865.17 |                8605.42 |
| Large Volume Customer (TPC-H Q18)                   |               30816.52 |               21043.10 |               22823.94 |               21018.99 |                6732.06 |                6150.45 |                5537.69 |                6178.94 |
| Discounted Revenue (TPC-H Q19)                      |                 645.64 |                1696.74 |                 909.08 |                 901.29 |                 139.99 |                 259.31 |                 136.20 |                 172.29 |
| Potential Part Promotion (TPC-H Q20)                |                8243.05 |                4372.50 |                5324.21 |                5261.96 |                1027.48 |                1259.48 |                 881.75 |                1062.47 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                7002.73 |                5928.74 |                6165.43 |                4619.45 |                2682.90 |                3233.84 |                2605.18 |                2643.68 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 928.62 |                 151.54 |                 476.48 |                 227.29 |                 305.52 |                 238.25 |                 162.28 |                 149.99 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       417.00 |      2.03 |           0.39 |                 11.73 |
| PostgreSQL-1-1-2-1 |       417.00 |      2.03 |           0.39 |                 11.73 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        72.33 |      0.68 |           0.00 |                  0.77 |
| PostgreSQL-1-1-2-1 |        72.33 |      0.68 |           0.00 |                  0.77 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       250.65 |      1.96 |           0.36 |                 11.08 |
| PostgreSQL-1-1-2-1 |       215.56 |      1.27 |           0.38 |                 11.21 |
| PostgreSQL-1-2-1-1 |       934.08 |      3.29 |           0.36 |                 10.76 |
| PostgreSQL-1-2-2-1 |        89.77 |      4.78 |           0.28 |                 10.11 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        24.40 |      0.01 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2-1 |        24.18 |      0.68 |           0.27 |                  0.27 |
| PostgreSQL-1-2-1-1 |        24.18 |      0.34 |           0.30 |                  0.30 |
| PostgreSQL-1-2-2-1 |        24.35 |      1.12 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    4.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    4.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    6.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
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
