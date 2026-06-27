## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1546s 
* Code: 1781462191
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:212915
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781462191

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      493.00 |           1.00 |            0.00 |        141.00 |          344.00 |              8 |           0 |             | None           |             0 | False         |               21.91 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        906 |            1.38 |             7882.93 |           1180.13 |          -1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        906 |            1.38 |             7882.93 |           1180.13 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 356.27 |
| TPC-DS Q2     |                1901.93 |
| TPC-DS Q3     |                 640.71 |
| TPC-DS Q4     |               32464.23 |
| TPC-DS Q5     |                3303.09 |
| TPC-DS Q6     |              224696.05 |
| TPC-DS Q7     |                1379.57 |
| TPC-DS Q8     |                 169.15 |
| TPC-DS Q9     |                8249.72 |
| TPC-DS Q10    |                2307.15 |
| TPC-DS Q11    |               19756.81 |
| TPC-DS Q12    |                 294.36 |
| TPC-DS Q13    |                1797.06 |
| TPC-DS Q14a+b |               13304.64 |
| TPC-DS Q15    |                 666.30 |
| TPC-DS Q16    |                 664.19 |
| TPC-DS Q17    |                1666.29 |
| TPC-DS Q18    |                1282.87 |
| TPC-DS Q19    |                 983.46 |
| TPC-DS Q20    |                 638.78 |
| TPC-DS Q21    |                1095.31 |
| TPC-DS Q22    |               11111.22 |
| TPC-DS Q23a+b |               28278.35 |
| TPC-DS Q24a+b |                2572.52 |
| TPC-DS Q25    |                1449.86 |
| TPC-DS Q26    |                 930.07 |
| TPC-DS Q27    |                  63.71 |
| TPC-DS Q28    |                4970.23 |
| TPC-DS Q29    |                1638.26 |
| TPC-DS Q30    |               75398.08 |
| TPC-DS Q31    |                5634.18 |
| TPC-DS Q32    |                 640.84 |
| TPC-DS Q33    |                1956.82 |
| TPC-DS Q34    |                  60.85 |
| TPC-DS Q35    |                2640.06 |
| TPC-DS Q36    |                1134.99 |
| TPC-DS Q37    |                 930.04 |
| TPC-DS Q38    |                3574.83 |
| TPC-DS Q39a+b |                9181.49 |
| TPC-DS Q40    |                 502.69 |
| TPC-DS Q41    |                2786.31 |
| TPC-DS Q42    |                 617.03 |
| TPC-DS Q43    |                  80.45 |
| TPC-DS Q44    |                   4.07 |
| TPC-DS Q45    |                 395.27 |
| TPC-DS Q46    |                  96.70 |
| TPC-DS Q47    |                4970.10 |
| TPC-DS Q48    |                1898.82 |
| TPC-DS Q49    |                2024.72 |
| TPC-DS Q50    |                1116.72 |
| TPC-DS Q51    |                3239.74 |
| TPC-DS Q52    |                 600.97 |
| TPC-DS Q53    |                 731.19 |
| TPC-DS Q54    |                1211.63 |
| TPC-DS Q55    |                 603.27 |
| TPC-DS Q56    |                1746.17 |
| TPC-DS Q57    |                2077.95 |
| TPC-DS Q58    |                1637.61 |
| TPC-DS Q59    |                2352.65 |
| TPC-DS Q60    |                1577.40 |
| TPC-DS Q61    |                 176.33 |
| TPC-DS Q62    |                 540.78 |
| TPC-DS Q63    |                 675.32 |
| TPC-DS Q64    |                2051.97 |
| TPC-DS Q65    |                2414.51 |
| TPC-DS Q66    |                 979.45 |
| TPC-DS Q67    |                8691.14 |
| TPC-DS Q68    |                  85.82 |
| TPC-DS Q69    |                1199.45 |
| TPC-DS Q70    |                1791.87 |
| TPC-DS Q71    |                1659.26 |
| TPC-DS Q72    |                3030.50 |
| TPC-DS Q73    |                  57.26 |
| TPC-DS Q74    |                6658.89 |
| TPC-DS Q75    |                4975.60 |
| TPC-DS Q76    |                 844.95 |
| TPC-DS Q77    |                1455.01 |
| TPC-DS Q78    |                3294.85 |
| TPC-DS Q79    |                 846.92 |
| TPC-DS Q80    |                1523.61 |
| TPC-DS Q81    |              318326.04 |
| TPC-DS Q82    |                1246.06 |
| TPC-DS Q83    |                 270.36 |
| TPC-DS Q84    |                 172.34 |
| TPC-DS Q85    |                 691.58 |
| TPC-DS Q86    |                 460.38 |
| TPC-DS Q87    |                4085.21 |
| TPC-DS Q88    |                6132.60 |
| TPC-DS Q89    |                 706.66 |
| TPC-DS Q90    |                 700.33 |
| TPC-DS Q91    |                 281.37 |
| TPC-DS Q92    |                 342.69 |
| TPC-DS Q93    |                 825.32 |
| TPC-DS Q94    |                 619.32 |
| TPC-DS Q95    |                8948.80 |
| TPC-DS Q96    |                 583.19 |
| TPC-DS Q97    |                1983.87 |
| TPC-DS Q98    |                 896.92 |
| TPC-DS Q99    |                1106.04 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       415.46 |      5.17 |           0.49 |                  8.82 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        21.77 |      0.26 |           0.01 |                  2.21 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1253.75 |      2.45 |           0.59 |                 10.45 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        20.46 |      0.06 |           0.32 |                  0.32 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    7.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    5.00 |

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
