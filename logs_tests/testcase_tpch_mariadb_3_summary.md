## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 2627s 
* Code: 1782334385
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
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-1-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253328
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253328
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385

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
| MariaDB-1-1 |                1 |    1 |     1725.00 |           3.00 |           33.00 |        510.00 |         1172.00 |              8 |           0 |             | None           |             0 | False         |                2.09 |
| MariaDB-1-2 |                2 |    1 |     1725.00 |           3.00 |           33.00 |        510.00 |         1172.00 |              8 |           0 |             | None           |             0 | False         |                2.09 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        103 |            1.08 |             3525.92 |            768.93 |          -1 | MariaDB-1-1-1-1-1 |
| MariaDB-1-1-2-1-1 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        121 |            1.17 |             3264.87 |            654.55 |          -1 | MariaDB-1-1-2-1-1 |
| MariaDB-1-1-2-1-2 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        119 |            1.18 |             3237.13 |            665.55 |          -1 | MariaDB-1-1-2-1-2 |
| MariaDB-1-2-1-1-1 | MariaDB-1       | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.16 |             3324.21 |            740.19 |          -1 | MariaDB-1-2-1-1-1 |
| MariaDB-1-2-2-1-1 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        135 |            1.37 |             2770.37 |            586.67 |          -1 | MariaDB-1-2-2-1-1 |
| MariaDB-1-2-2-1-2 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        134 |            1.43 |             2674.87 |            591.04 |          -1 | MariaDB-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        103 |            1.08 |             3525.92 |            768.93 |          -1 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |        121 |            1.18 |             3250.97 |           1309.09 |          -1 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.16 |             3324.21 |            740.19 |          -1 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |               44 |        135 |            1.40 |             2722.20 |           1173.33 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MariaDB-1-1-2-1-1 |   MariaDB-1-1-2-1-2 |   MariaDB-1-2-1-1-1 |   MariaDB-1-2-2-1-1 |   MariaDB-1-2-2-1-2 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7835.73 |             7460.30 |             7576.32 |             7445.58 |             7798.95 |             7445.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              445.24 |              413.40 |              452.21 |              562.07 |              698.00 |              629.33 |
| Shipping Priority (TPC-H Q3)                        |             1551.76 |             1716.63 |             1743.74 |             1536.82 |             2642.48 |             2428.26 |
| Order Priority Checking Query (TPC-H Q4)            |              339.95 |              350.44 |              357.45 |              351.30 |              398.86 |              386.22 |
| Local Supplier Volume (TPC-H Q5)                    |              966.73 |             1102.55 |             1067.68 |              965.93 |             1496.52 |             1452.50 |
| Forecasting Revenue Change (TPC-H Q6)               |              826.30 |              813.59 |              799.97 |              806.65 |              802.49 |              802.31 |
| Volume Shipping Query (TPC-H Q7)                    |             1078.50 |             1090.08 |             1134.41 |             1098.53 |             1394.57 |             1357.76 |
| National Market Share (TPC-H Q8)                    |             1828.43 |             2211.54 |             2201.69 |             1924.68 |             3119.33 |             3003.46 |
| Product Type Profit Measure (TPC-H Q9)              |             3999.56 |             4395.40 |             4387.79 |             4681.89 |             5739.51 |             5963.52 |
| Returned Item Reporting Query (TPC-H Q10)           |              927.14 |              925.49 |              928.07 |              925.57 |             1174.82 |             1175.41 |
| Important Stock Identification (TPC-H Q11)          |              134.54 |              147.96 |              141.73 |              146.11 |              217.12 |              218.17 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3029.25 |             3415.46 |             3422.66 |             3044.02 |             4549.91 |             4266.76 |
| Customer Distribution (TPC-H Q13)                   |             2995.40 |             3887.61 |             3889.33 |             3221.74 |             4031.94 |             3630.11 |
| Promotion Effect Query (TPC-H Q14)                  |            12074.97 |            14588.29 |            14297.04 |            14396.01 |            18364.82 |            17723.74 |
| Top Supplier Query (TPC-H Q15)                      |             1780.15 |             1809.90 |             1816.64 |             1751.99 |             1732.48 |             2195.46 |
| Parts/Supplier Relationship (TPC-H Q16)             |              220.32 |              221.36 |              206.89 |              213.05 |              234.73 |              226.32 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               69.54 |               61.56 |               65.50 |               75.99 |               62.19 |               61.79 |
| Large Volume Customer (TPC-H Q18)                   |             2930.59 |             3922.40 |             3912.35 |             2979.81 |             3533.70 |             3592.21 |
| Discounted Revenue (TPC-H Q19)                      |               95.73 |              104.56 |              105.85 |              103.57 |               96.93 |              161.23 |
| Potential Part Promotion (TPC-H Q20)                |              206.68 |              235.15 |              220.62 |              242.60 |              218.74 |              385.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            55401.87 |            66972.36 |            65984.58 |            56422.19 |            71639.16 |            71949.04 |
| Global Sales Opportunity Query (TPC-H Q22)          |              113.79 |              115.17 |              139.42 |              144.84 |              158.60 |              159.10 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1541.04 |      2.44 |           5.93 |                  6.04 |
| MariaDB-1-1-2-1 |      1541.04 |      2.44 |           5.93 |                  6.04 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         4.79 |      0.05 |           0.00 |                  0.13 |
| MariaDB-1-1-2-1 |         4.79 |      0.05 |           0.00 |                  0.13 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        69.86 |      0.99 |           5.99 |                  6.09 |
| MariaDB-1-1-2-1 |       205.20 |      2.00 |           6.00 |                  6.10 |
| MariaDB-1-2-1-1 |        92.51 |      1.00 |           3.72 |                  3.75 |
| MariaDB-1-2-2-1 |       224.20 |      2.00 |           3.73 |                  3.76 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        15.09 |      0.17 |           0.30 |                  0.30 |
| MariaDB-1-1-2-1 |        29.66 |      0.21 |           0.33 |                  0.34 |
| MariaDB-1-2-1-1 |        16.76 |      0.46 |           0.34 |                  0.35 |
| MariaDB-1-2-2-1 |        30.93 |      0.24 |           0.34 |                  0.35 |

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
