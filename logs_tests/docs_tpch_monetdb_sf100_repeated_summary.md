## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 2177s 
* Code: 1792700729
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
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400114
  * datadisk:192979
  * volume_size:984G
  * volume_used:189G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792700729
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400115
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
    * code:1792700729
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400116
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
    * code:1792700729
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:400117
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
    * code:1792700729

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792700729-5587574c76-7564d: 0
* bexhoma-sut-monetdb-1-1792700729-69dd4b5589-bczzw: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              0 |           0 |             | None           |             0 | False         |               88.91 | True                |
| MonetDB-1-2 |                2 |  100 |     4049.00 |           3.00 |          625.00 |       1516.00 |         1903.00 |              0 |           0 |             | None           |             0 | False         |               88.91 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        523 |            9.80 |            38440.40 |          15143.40 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.56 |            68565.29 |          27310.34 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        495 |            9.84 |            38183.73 |          16000.00 |          -1 | monetdb-1-2-1-1-1 |
| monetdb-1-2-2-1-1 | MonetDB-1       | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.59 |            68493.37 |          27310.34 |          -1 | monetdb-1-2-2-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        523 |            9.80 |            38440.40 |          15143.40 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.56 |            68565.29 |          27310.34 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        495 |            9.84 |            38183.73 |          16000.00 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        290 |            5.59 |            68493.37 |          27310.34 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-2-1-1-1 |   monetdb-1-2-2-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           129158.08 |            81724.98 |           116291.17 |            80236.46 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             5973.25 |              769.55 |             6360.14 |              749.29 |
| Shipping Priority (TPC-H Q3)                        |            31056.22 |             7210.89 |            33344.37 |             6352.36 |
| Order Priority Checking Query (TPC-H Q4)            |            20718.16 |            11677.00 |            19192.29 |             9681.22 |
| Local Supplier Volume (TPC-H Q5)                    |             7524.05 |             3426.95 |             6804.40 |             3386.01 |
| Forecasting Revenue Change (TPC-H Q6)               |             1436.78 |             1247.47 |             1997.99 |             1258.33 |
| Volume Shipping Query (TPC-H Q7)                    |             8798.00 |             7796.90 |             9693.94 |             8170.82 |
| National Market Share (TPC-H Q8)                    |            34117.01 |            14720.91 |            36872.15 |            14659.25 |
| Product Type Profit Measure (TPC-H Q9)              |            12715.11 |             5313.92 |            12565.85 |             7655.70 |
| Returned Item Reporting Query (TPC-H Q10)           |            16307.11 |             7631.41 |            14358.80 |             9163.40 |
| Important Stock Identification (TPC-H Q11)          |             1759.74 |             1211.57 |             1737.07 |              968.44 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2066.97 |             2079.55 |             1916.75 |             2197.20 |
| Customer Distribution (TPC-H Q13)                   |            72758.45 |            30983.30 |            64832.53 |            33840.36 |
| Promotion Effect Query (TPC-H Q14)                  |              959.17 |              934.57 |              961.58 |              939.73 |
| Top Supplier Query (TPC-H Q15)                      |             3461.90 |             2083.27 |             3161.58 |             3524.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5484.16 |             5118.23 |             5340.22 |             5918.79 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            33492.83 |             2044.06 |            31482.94 |             2214.70 |
| Large Volume Customer (TPC-H Q18)                   |            14788.82 |            10128.70 |            14642.92 |            10423.87 |
| Discounted Revenue (TPC-H Q19)                      |             1781.91 |             4265.45 |             2387.13 |             1986.92 |
| Potential Part Promotion (TPC-H Q20)                |             4512.43 |             4439.15 |             4811.18 |             3721.02 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            91620.85 |            62894.24 |            84435.42 |            62242.37 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4021.89 |             3457.70 |             4210.12 |             3602.87 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1314.71 |      5.70 |         104.77 |                104.77 |
| monetdb-1-1-2-1 |       846.62 |      5.82 |         179.83 |                179.83 |
| monetdb-1-2-1-1 |      1307.44 |      6.81 |         111.95 |                111.95 |
| monetdb-1-2-2-1 |       834.35 |      5.37 |         179.80 |                179.80 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        28.51 |      0.41 |           0.37 |                  0.38 |
| monetdb-1-1-2-1 |        28.40 |      0.20 |           0.38 |                  0.39 |
| monetdb-1-2-1-1 |        26.42 |      0.91 |           0.39 |                  0.40 |
| monetdb-1-2-2-1 |        28.58 |      0.27 |           0.38 |                  0.39 |

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
