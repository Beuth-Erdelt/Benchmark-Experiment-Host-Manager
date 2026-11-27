## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 638s 
* Code: 1795667757
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:667670
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
    * code:1795667757
    * TENANT_BY:container
    * TENANT_NUM:2
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:667671
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
    * code:1795667757
    * TENANT_BY:container
    * TENANT_NUM:2
* mariadb-2-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:667670
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
    * code:1795667757
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* mariadb-2-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:667671
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
    * code:1795667757
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Ingestion
* MariaDB-1: 8 of 8 units ok
* MariaDB-2: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795667757-665d86864c-wdfqf: 0
* bexhoma-sut-mariadb-2-1795667757-7f694fdf98-h96l6: 0

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
| 1795667757-MariaDB-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |       86.00 |           2.00 |            5.00 |         53.00 |           24.00 |              1 |         0 |               41.86 | False               |
| 1795667757-MariaDB-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |       81.00 |           2.00 |            0.00 |         52.00 |           24.00 |              1 |         0 |               44.44 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         89 |            0.91 |             3937.68 |            889.89 |           0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         84 |            0.84 |             4279.59 |            942.86 |           0 |
| mariadb-2-1-1-1-1 | mariadb-2-1-1 | mariadb-2-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         90 |            0.96 |             3768.26 |            880.00 |           1 |
| mariadb-2-1-2-1-1 | mariadb-2-1-2 | mariadb-2-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         85 |            0.84 |             4306.88 |            931.76 |           1 |

#### Per Phase

| DBMS            | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1_0 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         89 |            0.91 |             3937.68 |            889.89 |           0 |
| mariadb-1-1-2_0 | mariadb-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         84 |            0.84 |             4279.59 |            942.86 |           0 |
| mariadb-2-1-1_1 | mariadb-2-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         90 |            0.96 |             3768.26 |            880.00 |           1 |
| mariadb-2-1-2_1 | mariadb-2-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         85 |            0.84 |             4306.88 |            931.76 |           1 |

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
| Pricing Summary Report (TPC-H Q1)                   |             6642.92 |             5666.21 |             6823.98 |             5524.81 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              324.53 |              330.41 |              396.59 |              323.02 |
| Shipping Priority (TPC-H Q3)                        |             2133.27 |             1147.78 |             2248.20 |             1119.70 |
| Order Priority Checking Query (TPC-H Q4)            |              277.04 |              334.85 |              286.26 |              295.38 |
| Local Supplier Volume (TPC-H Q5)                    |              729.10 |              866.43 |              737.66 |              728.52 |
| Forecasting Revenue Change (TPC-H Q6)               |              797.65 |              814.36 |              750.79 |              730.72 |
| Volume Shipping Query (TPC-H Q7)                    |             1147.79 |             1041.26 |             1270.60 |              895.57 |
| National Market Share (TPC-H Q8)                    |             1339.79 |             1861.04 |             1465.23 |             2085.49 |
| Product Type Profit Measure (TPC-H Q9)              |             1334.49 |             1587.37 |             1497.13 |             1359.26 |
| Returned Item Reporting Query (TPC-H Q10)           |             1299.65 |              662.63 |             1292.49 |              690.13 |
| Important Stock Identification (TPC-H Q11)          |              268.84 |              102.43 |              307.95 |               91.94 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2552.00 |             2390.71 |             2572.61 |             2601.33 |
| Customer Distribution (TPC-H Q13)                   |             2614.95 |             2310.17 |             3189.48 |             2276.64 |
| Promotion Effect Query (TPC-H Q14)                  |             9996.62 |             9241.38 |             9032.95 |             8391.29 |
| Top Supplier Query (TPC-H Q15)                      |             1988.96 |             2370.47 |             1642.29 |             1877.84 |
| Parts/Supplier Relationship (TPC-H Q16)             |              164.98 |              156.57 |              267.54 |              320.35 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               44.74 |               43.56 |               56.63 |               70.74 |
| Large Volume Customer (TPC-H Q18)                   |             2966.08 |             2477.02 |             3316.05 |             2360.91 |
| Discounted Revenue (TPC-H Q19)                      |               93.78 |               82.86 |               77.69 |               86.83 |
| Potential Part Promotion (TPC-H Q20)                |              220.39 |              209.94 |              164.11 |              197.81 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            47383.61 |            47574.82 |            47631.78 |            48290.19 |
| Global Sales Opportunity Query (TPC-H Q22)          |               92.04 |              124.22 |               92.11 |               92.40 |

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
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
