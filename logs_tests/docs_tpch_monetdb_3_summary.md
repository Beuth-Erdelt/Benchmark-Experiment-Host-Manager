## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 1844s 
* Code: 1792703031
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 1000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400352
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400353
  * datadisk:189789
  * volume_size:984G
  * volume_used:186G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792703031

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792703031-7688c97c7d-vn6cz: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              0 |           0 |             | None           |             0 | False         |               88.91 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        501 |            9.59 |            39427.75 |          15808.38 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        285 |            5.54 |            69254.80 |          27789.47 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-1-3-1-1 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |                  22 |        735 |           11.41 |            32645.75 |          10775.51 |          -1 | monetdb-1-1-3-1-1 |
| monetdb-1-1-3-1-2 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |                  22 |        707 |           10.40 |            36170.68 |          11202.26 |          -1 | monetdb-1-1-3-1-2 |
| monetdb-1-1-3-1-3 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |                  22 |        735 |           10.62 |            35256.16 |          10775.51 |          -1 | monetdb-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        501 |            9.59 |            39427.75 |          15808.38 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        285 |            5.54 |            69254.80 |          27789.47 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 100.00 |               66 |                  66 |        735 |           10.80 |            34658.21 |          32326.53 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-3 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-3-1-1 |   monetdb-1-1-3-1-2 |   monetdb-1-1-3-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           123593.19 |            82493.97 |           242477.23 |           280557.77 |           303223.47 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             6166.08 |              756.08 |             2766.08 |              992.89 |             2474.83 |
| Shipping Priority (TPC-H Q3)                        |            27654.10 |             6609.17 |            15377.18 |            11636.23 |             5885.00 |
| Order Priority Checking Query (TPC-H Q4)            |            19151.72 |             9309.01 |            18439.99 |            20870.04 |            19020.08 |
| Local Supplier Volume (TPC-H Q5)                    |             8167.57 |             4000.59 |            15817.75 |             4540.23 |             6139.46 |
| Forecasting Revenue Change (TPC-H Q6)               |             1525.93 |             1329.24 |             2542.73 |             1194.99 |             2097.08 |
| Volume Shipping Query (TPC-H Q7)                    |             9488.60 |             7152.02 |             7087.30 |             8717.71 |             6206.58 |
| National Market Share (TPC-H Q8)                    |            32840.20 |            14784.17 |            57978.51 |            32681.31 |            16441.44 |
| Product Type Profit Measure (TPC-H Q9)              |            10475.01 |             6898.54 |            24990.49 |            25040.02 |            25415.99 |
| Returned Item Reporting Query (TPC-H Q10)           |            16321.02 |             7923.70 |            10270.17 |            11152.60 |            11023.98 |
| Important Stock Identification (TPC-H Q11)          |             1667.69 |              922.72 |             2429.95 |             1843.65 |             2202.92 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1975.03 |             2225.48 |             4158.96 |             4367.67 |             3957.51 |
| Customer Distribution (TPC-H Q13)                   |            64603.70 |            31683.81 |            66565.99 |            62799.55 |            60771.62 |
| Promotion Effect Query (TPC-H Q14)                  |              940.89 |              971.77 |              931.31 |             1612.69 |             1832.51 |
| Top Supplier Query (TPC-H Q15)                      |             3075.77 |             2434.23 |             2343.10 |             4786.99 |             6938.34 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5291.48 |             5157.91 |             5872.79 |             5415.66 |             6151.33 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            32097.47 |             2274.72 |            33909.25 |            34370.92 |            34108.25 |
| Large Volume Customer (TPC-H Q18)                   |            15290.59 |            11607.48 |            22100.82 |            19609.20 |            21624.55 |
| Discounted Revenue (TPC-H Q19)                      |             1625.98 |             3600.20 |             2938.84 |             1980.84 |             2767.66 |
| Potential Part Promotion (TPC-H Q20)                |             5331.31 |             3158.77 |             7611.46 |            11146.84 |             8379.14 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            89302.48 |            59651.82 |           167124.53 |           137456.51 |           166387.15 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4075.50 |             3343.64 |             4413.43 |             7135.58 |             4341.11 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1178.15 |      8.48 |         111.67 |                111.68 |
| monetdb-1-1-2-1 |       827.71 |      6.81 |         178.16 |                178.16 |
| monetdb-1-1-3-1 |      3475.99 |     10.93 |         252.82 |                255.98 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        28.52 |      0.40 |           0.39 |                  0.41 |
| monetdb-1-1-2-1 |        27.22 |      0.40 |           0.40 |                  0.42 |
| monetdb-1-1-3-1 |        88.34 |      1.31 |           0.45 |                  0.46 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: No monitoring metrics missing
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
