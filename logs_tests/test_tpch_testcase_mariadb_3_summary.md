## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 2657s 
* Code: 1782315857
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:224991
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782315857
* MariaDB-1-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:257852
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782315857
* MariaDB-1-1-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:257852
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782315857
* MariaDB-1-2-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:281686
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782315857
* MariaDB-1-2-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:284289
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782315857
* MariaDB-1-2-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:284289
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782315857

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |     1707.00 |           3.00 |           20.00 |        502.00 |         1175.00 |              8 |           0 |             | None           |             0 | False         |                2.11 |
| MariaDB-1-2 |                2 |    1 |     1707.00 |           3.00 |           20.00 |        502.00 |         1175.00 |              8 |           0 |             | None           |             0 | False         |                2.11 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        104 |            1.10 |             3501.59 |            761.54 |          -1 | MariaDB-1-1-1-1-1 |
| MariaDB-1-1-2-1-1 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        124 |            1.18 |             3243.92 |            638.71 |          -1 | MariaDB-1-1-2-1-1 |
| MariaDB-1-1-2-1-2 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        124 |            1.19 |             3231.06 |            638.71 |          -1 | MariaDB-1-1-2-1-2 |
| MariaDB-1-2-1-1-1 | MariaDB-1       | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        177 |            1.23 |             3132.76 |            447.46 |          -1 | MariaDB-1-2-1-1-1 |
| MariaDB-1-2-2-1-1 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        122 |            1.24 |             3107.71 |            649.18 |          -1 | MariaDB-1-2-2-1-1 |
| MariaDB-1-2-2-1-2 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        124 |            1.24 |             3073.18 |            638.71 |          -1 | MariaDB-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        104 |            1.10 |             3501.59 |            761.54 |          -1 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |        124 |            1.18 |             3237.49 |           1277.42 |          -1 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        177 |            1.23 |             3132.76 |            447.46 |          -1 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |               44 |        124 |            1.24 |             3090.40 |           1277.42 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MariaDB-1-1-2-1-1 |   MariaDB-1-1-2-1-2 |   MariaDB-1-2-1-1-1 |   MariaDB-1-2-2-1-1 |   MariaDB-1-2-2-1-2 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7475.20 |             7503.04 |             7418.85 |            74921.73 |             7410.26 |             7712.94 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              438.31 |              494.48 |              541.79 |              528.96 |              442.97 |              582.28 |
| Shipping Priority (TPC-H Q3)                        |             1566.71 |             1717.31 |             1771.33 |             1645.98 |             2061.98 |             2173.56 |
| Order Priority Checking Query (TPC-H Q4)            |              347.36 |              346.47 |              347.80 |              363.11 |              388.57 |              376.00 |
| Local Supplier Volume (TPC-H Q5)                    |              992.87 |             1096.58 |             1123.67 |              987.78 |             1312.63 |             1100.56 |
| Forecasting Revenue Change (TPC-H Q6)               |              843.84 |              840.56 |              842.05 |              849.86 |              851.03 |              849.64 |
| Volume Shipping Query (TPC-H Q7)                    |             1118.22 |             1204.33 |             1214.86 |             1091.23 |             1186.05 |             1402.98 |
| National Market Share (TPC-H Q8)                    |             2152.16 |             2226.39 |             2226.67 |             1981.26 |             2916.02 |             2749.12 |
| Product Type Profit Measure (TPC-H Q9)              |             2295.82 |             2347.08 |             2347.27 |             2040.00 |             2605.69 |             2713.92 |
| Returned Item Reporting Query (TPC-H Q10)           |              875.47 |              939.59 |              941.81 |              885.04 |              941.88 |              984.03 |
| Important Stock Identification (TPC-H Q11)          |              135.12 |              150.30 |              151.75 |              123.90 |              137.40 |              158.47 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3178.64 |             3479.90 |             3486.87 |             3085.02 |             4231.81 |             4051.76 |
| Customer Distribution (TPC-H Q13)                   |             3159.08 |             3672.28 |             3710.61 |             3173.22 |             4792.19 |             4820.50 |
| Promotion Effect Query (TPC-H Q14)                  |            13041.42 |            16149.03 |            16025.37 |            13087.52 |            18361.20 |            19893.03 |
| Top Supplier Query (TPC-H Q15)                      |             1779.14 |             1848.27 |             1901.50 |             1901.38 |             1821.00 |             1869.56 |
| Parts/Supplier Relationship (TPC-H Q16)             |              263.87 |              258.31 |              227.47 |              243.20 |              284.17 |              235.10 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               61.05 |               61.49 |               61.18 |               61.96 |               60.49 |               61.82 |
| Large Volume Customer (TPC-H Q18)                   |             3092.70 |             3655.27 |             3754.21 |             3253.81 |             3070.61 |             3227.97 |
| Discounted Revenue (TPC-H Q19)                      |               99.48 |               97.39 |              101.02 |              109.75 |              103.36 |              100.65 |
| Potential Part Promotion (TPC-H Q20)                |              208.74 |              245.80 |              243.98 |              221.90 |              225.96 |              232.68 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            56255.85 |            71287.37 |            71288.27 |            61629.21 |            63766.99 |            64662.56 |
| Global Sales Opportunity Query (TPC-H Q22)          |              138.98 |              144.69 |              140.23 |              123.52 |              139.10 |              112.37 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1553.72 |      2.04 |           9.11 |                  9.22 |
| MariaDB-1-1-2-1 |      1553.72 |      2.04 |           9.11 |                  9.22 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         4.32 |      0.05 |           0.00 |                  0.13 |
| MariaDB-1-1-2-1 |         4.32 |      0.05 |           0.00 |                  0.13 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       108.15 |      1.17 |           9.16 |                  9.26 |
| MariaDB-1-1-2-1 |       201.20 |      2.00 |           9.16 |                  9.27 |
| MariaDB-1-2-1-1 |        78.30 |      1.00 |           6.99 |                  7.09 |
| MariaDB-1-2-2-1 |       226.48 |      2.00 |           7.00 |                  7.10 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        15.10 |      0.43 |           0.31 |                  0.31 |
| MariaDB-1-1-2-1 |        30.13 |      0.17 |           0.31 |                  0.31 |
| MariaDB-1-2-1-1 |        15.58 |      0.34 |           0.31 |                  0.31 |
| MariaDB-1-2-2-1 |        33.42 |      0.21 |           0.35 |                  0.35 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
