## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2032s 
* Code: 1781298543
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
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921716
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921716
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921717
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921717
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921717
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921717
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921718
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921718
  * volume_size:30G
  * volume_used:11G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781298543
    * TENANT_BY:database
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
| PostgreSQL-1-1 |                1 |    3 |     1042.00 |           2.00 |            1.00 |        314.00 |          723.00 |              2 |           0 |          | database       |             2 | False         |               10.36 |
| PostgreSQL-1-2 |                2 |    3 |     1042.00 |           2.00 |            1.00 |        314.00 |          723.00 |              2 |           0 |          | database       |             2 | False         |               10.36 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        152 |            4.22 |             2557.68 |           1563.16 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        158 |            3.83 |             2822.15 |           1503.80 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        151 |            3.87 |             2793.72 |           1573.51 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        163 |            4.33 |             2491.52 |           1457.67 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        151 |            2.41 |             4485.29 |           1573.51 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        154 |            2.54 |             4252.80 |           1542.86 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         48 |            1.47 |             7337.20 |           4950.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         49 |            1.47 |             7324.95 |           4848.98 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           2 | 3.00 |               44 |        158 |            4.02 |             2686.66 |           3007.59 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |        163 |            4.09 |             2638.30 |           2915.34 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           2 | 3.00 |               44 |        154 |            2.47 |             4367.50 |           3085.71 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         49 |            1.47 |             7331.07 |           9697.96 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-1-1-2 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4782.58 |                4997.26 |                5233.71 |                5157.68 |               56424.27 |               56349.26 |                4707.72 |                4633.86 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                4132.07 |                4603.96 |                4385.05 |                5115.44 |               16632.65 |               16063.51 |                1283.34 |                1341.04 |
| Shipping Priority (TPC-H Q3)                        |                4210.48 |                4946.60 |                6189.59 |                5726.62 |               30042.20 |               29728.88 |                2467.55 |                2296.30 |
| Order Priority Checking Query (TPC-H Q4)            |                3377.99 |                3916.94 |                3149.17 |                4244.79 |                 697.75 |                1240.68 |                 850.82 |                 773.64 |
| Local Supplier Volume (TPC-H Q5)                    |               13305.29 |               16807.19 |               21773.74 |               23446.95 |                2920.37 |                3072.91 |                2174.08 |                2309.81 |
| Forecasting Revenue Change (TPC-H Q6)               |                1151.00 |                2102.43 |                1850.12 |                1454.56 |                1639.92 |                1685.28 |                1672.14 |                1640.58 |
| Forecasting Revenue Change (TPC-H Q7)               |               15611.51 |               16626.68 |               14769.28 |               15146.95 |                3104.70 |                3099.54 |                2389.92 |                2235.10 |
| National Market Share (TPC-H Q8)                    |                6158.07 |                9208.78 |                4544.03 |                3977.50 |                5159.74 |                5900.81 |                 937.07 |                 860.22 |
| Product Type Profit Measure (TPC-H Q9)              |               20952.53 |               16787.29 |               13764.25 |               15648.57 |                3518.25 |                3406.58 |                3647.73 |                3810.97 |
| Forecasting Revenue Change (TPC-H Q10)              |                5480.83 |                4831.90 |                4888.45 |                5508.84 |                1511.38 |                1384.44 |                1579.84 |                1524.36 |
| Important Stock Identification (TPC-H Q11)          |                1956.56 |                3074.39 |                4876.63 |                2898.72 |                 669.69 |                 691.91 |                 593.83 |                 621.52 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                6656.49 |                2951.15 |                3921.08 |                3427.96 |                2774.67 |                2461.38 |                2341.96 |                2143.42 |
| Customer Distribution (TPC-H Q13)                   |                1389.76 |                1254.72 |                1262.28 |                1168.81 |                1278.86 |                1323.48 |                1760.85 |                1779.43 |
| Forecasting Revenue Change (TPC-H Q14)              |                1939.10 |                2061.02 |                1543.56 |                1535.66 |                1981.04 |                2041.20 |                1407.69 |                1518.95 |
| Top Supplier Query (TPC-H Q15)                      |                2294.18 |                2316.69 |                1333.77 |                1566.08 |                2104.62 |                2387.91 |                1801.90 |                1996.25 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1273.36 |                 860.35 |                 871.85 |                 542.52 |                 824.28 |                1034.12 |                 502.04 |                 510.98 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               14175.65 |               23052.90 |               13249.11 |               16662.64 |                7350.15 |                8047.76 |                6223.32 |                7197.88 |
| Large Volume Customer (TPC-H Q18)                   |               19745.18 |               27731.32 |               28091.58 |               28672.47 |                5801.36 |                7593.27 |                6169.92 |                6029.80 |
| Discounted Revenue (TPC-H Q19)                      |                 651.63 |                 373.01 |                 416.41 |                1303.98 |                 138.34 |                 163.32 |                 164.12 |                 175.34 |
| Potential Part Promotion (TPC-H Q20)                |               13229.01 |                4062.87 |                5099.00 |                5888.05 |                1213.23 |                1042.63 |                1042.82 |                1001.84 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                7587.21 |                3721.93 |                5778.48 |                9930.28 |                3364.28 |                3090.38 |                2692.56 |                2616.74 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 649.16 |                 201.46 |                 515.80 |                1643.59 |                 157.69 |                 147.29 |                 150.41 |                 149.66 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       376.23 |      2.04 |           0.40 |                 12.52 |
| PostgreSQL-1-1-2-1 |       376.23 |      2.04 |           0.40 |                 12.52 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        75.19 |      0.80 |           0.01 |                  2.18 |
| PostgreSQL-1-1-2-1 |        75.19 |      0.80 |           0.01 |                  2.18 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       196.79 |      1.96 |           0.38 |                 11.45 |
| PostgreSQL-1-1-2-1 |       216.93 |      2.08 |           0.39 |                 11.69 |
| PostgreSQL-1-2-1-1 |       822.79 |      3.18 |           0.36 |                 10.78 |
| PostgreSQL-1-2-2-1 |       181.23 |      4.38 |           0.38 |                 10.57 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        26.79 |      0.82 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2-1 |        25.94 |      0.01 |           0.27 |                  0.27 |
| PostgreSQL-1-2-1-1 |        25.78 |      0.01 |           0.30 |                  0.30 |
| PostgreSQL-1-2-2-1 |        26.59 |      0.02 |           0.30 |                  0.31 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      6.00 |                                     0.00 |                                             0.00 |                       15.00 |                                    7.00 |
| PostgreSQL-1-1-2-1 |                      6.00 |                                     0.00 |                                             0.00 |                       15.00 |                                    7.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   12.00 |
| PostgreSQL-1-1-2-1 |                      2.00 |                                     0.00 |                                             0.00 |                       11.00 |                                   13.00 |
| PostgreSQL-1-2-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   11.00 |
| PostgreSQL-1-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   13.00 |

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
