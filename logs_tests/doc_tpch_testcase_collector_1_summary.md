## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1653s 
* Code: 1781280659
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
  * disk:921900
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781280659
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921900
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781280659
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921900
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781280659
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921901
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781280659
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921902
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781280659
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921902
  * volume_size:30G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781280659

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      575.00 |           1.00 |           16.00 |        139.00 |          414.00 |              8 |           0 |          |                |             0 | False         |               18.78 |
| PostgreSQL-1-2 |                2 |    3 |      575.00 |           1.00 |           16.00 |        139.00 |          414.00 |              8 |           0 |          |                |             0 | False         |               18.78 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         98 |            2.39 |             4513.25 |           2424.49 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        119 |            3.02 |             3571.61 |           1996.64 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |        118 |            3.04 |             3555.82 |           2013.56 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        190 |            2.52 |             4279.76 |           1250.53 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         54 |            1.55 |             6962.61 |           4400.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         56 |            1.59 |             6812.20 |           4242.86 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         98 |            2.39 |             4513.25 |           2424.49 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |        119 |            3.03 |             3563.70 |           3993.28 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        190 |            2.52 |             4279.76 |           1250.53 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         56 |            1.57 |             6887.00 |           8485.71 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4990.88 |                5212.10 |                5308.99 |               94283.94 |                4490.65 |                4472.00 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                1040.55 |                5955.57 |                6571.31 |               22080.75 |                1491.14 |                1635.98 |
| Shipping Priority (TPC-H Q3)                        |                1568.38 |                5197.63 |                5197.42 |               19803.39 |                1422.88 |                1374.41 |
| Order Priority Checking Query (TPC-H Q4)            |                 796.40 |                1988.29 |                1986.58 |                 881.87 |                 774.26 |                 792.54 |
| Local Supplier Volume (TPC-H Q5)                    |                1584.05 |               10987.88 |               10988.73 |                3099.46 |                2145.48 |                2324.83 |
| Forecasting Revenue Change (TPC-H Q6)               |                1697.13 |                2151.02 |                2238.96 |                1840.04 |                1788.36 |                1862.84 |
| Forecasting Revenue Change (TPC-H Q7)               |               10500.44 |               12509.82 |               12509.08 |                1605.51 |                1857.76 |                1858.45 |
| National Market Share (TPC-H Q8)                    |                4091.95 |                3630.65 |                3631.36 |                4437.69 |                 776.82 |                 773.50 |
| Product Type Profit Measure (TPC-H Q9)              |               23880.16 |               29167.44 |               29127.30 |                5570.73 |                7020.60 |                7010.99 |
| Forecasting Revenue Change (TPC-H Q10)              |                2975.89 |                2860.67 |                2888.71 |                2521.67 |                2695.05 |                2720.31 |
| Important Stock Identification (TPC-H Q11)          |                1264.74 |                2145.49 |                2160.04 |                 532.09 |                 786.05 |                 775.31 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                2925.79 |                2760.94 |                2761.33 |                2791.59 |                2803.09 |                2798.68 |
| Customer Distribution (TPC-H Q13)                   |                2283.61 |                1976.52 |                1977.22 |                1542.48 |                1328.35 |                1331.92 |
| Forecasting Revenue Change (TPC-H Q14)              |                2112.49 |                1878.66 |                1825.19 |                1464.69 |                1909.89 |                1935.20 |
| Top Supplier Query (TPC-H Q15)                      |                2120.59 |                1968.19 |                1609.48 |                2174.96 |                1971.59 |                1926.03 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 546.91 |                 718.84 |                 539.76 |                 500.94 |                 529.42 |                 535.28 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                7515.42 |                5654.26 |                5491.57 |                4870.87 |                3610.62 |                3609.63 |
| Large Volume Customer (TPC-H Q18)                   |                9288.62 |                8721.36 |                7725.77 |                8287.72 |                7839.23 |                8711.61 |
| Discounted Revenue (TPC-H Q19)                      |                1200.68 |                 324.32 |                 460.15 |                 165.88 |                 177.14 |                 166.15 |
| Potential Part Promotion (TPC-H Q20)                |                1690.92 |                2763.41 |                2839.59 |                1490.39 |                1053.65 |                1022.39 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                8655.94 |                6093.31 |                6066.22 |                5786.17 |                4238.47 |                5505.13 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 160.49 |                 155.13 |                 193.32 |                 159.39 |                 154.92 |                 157.65 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       121.44 |      0.63 |           0.28 |                  7.07 |
| PostgreSQL-1-1-2-1 |       121.44 |      0.63 |           0.28 |                  7.07 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        29.68 |      0.41 |           0.00 |                  0.34 |
| PostgreSQL-1-1-2-1 |        29.68 |      0.41 |           0.00 |                  0.34 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        52.19 |      1.29 |           0.26 |                  6.14 |
| PostgreSQL-1-1-2-1 |       202.51 |      3.00 |           0.40 |                  8.49 |
| PostgreSQL-1-2-1-1 |       470.78 |      1.77 |           0.28 |                  5.98 |
| PostgreSQL-1-2-2-1 |       154.70 |      4.25 |           0.34 |                  4.93 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        12.33 |      0.35 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2-1 |        24.48 |      1.31 |           0.27 |                  0.27 |
| PostgreSQL-1-2-1-1 |        12.20 |      0.00 |           0.25 |                  0.25 |
| PostgreSQL-1-2-2-1 |        23.85 |      0.40 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       10.00 |                                    8.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                       10.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    3.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    3.00 |
| PostgreSQL-1-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    6.00 |

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
