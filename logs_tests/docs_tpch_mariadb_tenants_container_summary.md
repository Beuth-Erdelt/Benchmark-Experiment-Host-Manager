## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 684s 
* Code: 1795529977
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1117058
  * datadisk:1993
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529977
    * TENANT_BY:container
    * TENANT_NUM:2
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1117551
  * datadisk:1993
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529977
    * TENANT_BY:container
    * TENANT_NUM:2
* mariadb-2-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1117058
  * datadisk:1993
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529977
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* mariadb-2-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1117551
  * datadisk:1993
  * volume_size:49G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529977
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Ingestion
* MariaDB-1: 8 of 8 units ok
* MariaDB-2: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795529977-6d86496d8c-d2w7w: 0
* bexhoma-sut-mariadb-2-1795529977-6566c889cd-mxvmf: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 2: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-2 - Experiment 1 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                          |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads |   Throughput [SF/h] | loading_inherited   |
|:-------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|--------------------:|:--------------------|
| 1795529977-MariaDB-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |       90.00 |           2.00 |            0.00 |         54.00 |           25.00 |              1 |         0 |               40.00 | False               |
| 1795529977-MariaDB-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |       82.00 |           2.00 |            0.00 |         54.00 |           24.00 |              1 |         0 |               43.90 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         87 |            0.82 |             4365.78 |            910.34 |           0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         91 |            0.87 |             4139.03 |            870.33 |           0 |
| mariadb-2-1-1-1-1 | mariadb-2-1-1 | mariadb-2-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         86 |            0.86 |             4188.66 |            920.93 |           1 |
| mariadb-2-1-2-1-1 | mariadb-2-1-2 | mariadb-2-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         89 |            0.89 |             4047.92 |            889.89 |           1 |

#### Per Phase

| DBMS            | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1_0 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         87 |            0.82 |             4365.78 |            910.34 |           0 |
| mariadb-1-1-2_0 | mariadb-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         91 |            0.87 |             4139.03 |            870.33 |           0 |
| mariadb-2-1-1_1 | mariadb-2-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         86 |            0.86 |             4188.66 |            920.93 |           1 |
| mariadb-2-1-2_1 | mariadb-2-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         89 |            0.89 |             4047.92 |            889.89 |           1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-2-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-2-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-1-2-1-1 |   mariadb-2-1-1-1-1 |   mariadb-2-1-2-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7019.30 |             5802.21 |             6855.00 |             6242.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              341.25 |              342.38 |              362.66 |              816.45 |
| Shipping Priority (TPC-H Q3)                        |             1184.14 |             1969.58 |             1182.39 |             1230.62 |
| Order Priority Checking Query (TPC-H Q4)            |              275.45 |              324.72 |              306.22 |              286.81 |
| Local Supplier Volume (TPC-H Q5)                    |              739.87 |              771.00 |              764.51 |              762.36 |
| Forecasting Revenue Change (TPC-H Q6)               |              880.51 |              789.19 |             2183.89 |             1043.08 |
| Volume Shipping Query (TPC-H Q7)                    |             1849.75 |             1406.95 |              815.59 |             1214.95 |
| National Market Share (TPC-H Q8)                    |             1386.05 |             1383.73 |             1430.83 |             1470.35 |
| Product Type Profit Measure (TPC-H Q9)              |             1339.58 |             1350.49 |             1440.43 |             1380.07 |
| Returned Item Reporting Query (TPC-H Q10)           |              710.69 |              715.38 |              670.03 |             1322.41 |
| Important Stock Identification (TPC-H Q11)          |               94.89 |              158.58 |              121.90 |              106.78 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2669.92 |             3193.09 |             2559.61 |             2976.68 |
| Customer Distribution (TPC-H Q13)                   |             2877.94 |             2644.74 |             2377.87 |             2358.66 |
| Promotion Effect Query (TPC-H Q14)                  |             8451.90 |            10595.68 |             8454.07 |            10909.52 |
| Top Supplier Query (TPC-H Q15)                      |             2486.70 |             1648.15 |             2063.23 |             1641.01 |
| Parts/Supplier Relationship (TPC-H Q16)             |              147.10 |              152.15 |              150.34 |              147.52 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               42.72 |               43.38 |               47.54 |               43.28 |
| Large Volume Customer (TPC-H Q18)                   |             2318.48 |             3503.43 |             2395.89 |             3621.57 |
| Discounted Revenue (TPC-H Q19)                      |               72.95 |               74.03 |              102.93 |               72.85 |
| Potential Part Promotion (TPC-H Q20)                |              158.64 |              167.14 |              215.71 |              161.89 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            49124.80 |            50013.49 |            46789.60 |            48370.59 |
| Global Sales Opportunity Query (TPC-H Q22)          |               91.11 |               95.44 |               91.70 |               91.78 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
