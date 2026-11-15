## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 2182s 
* Code: 1794668223
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:575865
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:584558
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:573372
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:573372
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:573372
  * datadisk:195342
  * volume_size:984G
  * volume_used:191G
  * cpu_list:0-127
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1794668223

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794668223-868c9d6698-mcgb5: 0

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

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     3963.00 |           5.00 |           22.00 |       1753.00 |         2179.00 |              0 |         0 |             | None           |             0 | False         |               90.84 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 100.00 |               22 |                  22 |        668 |           12.18 |            30614.54 |          11856.29 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 100.00 |               22 |                  22 |        339 |            6.18 |            61674.11 |          23362.83 |          -1 |
| monetdb-1-1-3-1-1 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       1 | 100.00 |               22 |                  22 |        893 |           14.97 |            24810.40 |           8868.98 |          -1 |
| monetdb-1-1-3-1-2 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       2 | 100.00 |               22 |                  22 |        853 |           13.27 |            28236.90 |           9284.88 |          -1 |
| monetdb-1-1-3-1-3 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       3 | 100.00 |               22 |                  22 |        883 |           15.46 |            24712.46 |           8969.42 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        668 |           12.18 |            30614.54 |          11856.29 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |                  22 |        339 |            6.18 |            61674.11 |          23362.83 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 100.00 |               66 |                  66 |        893 |           14.53 |            25869.56 |          26606.94 |          -1 |

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
| Pricing Summary Report (TPC-H Q1)                   |           154045.20 |           108857.02 |           356690.13 |           385596.16 |           369442.43 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            11194.49 |              873.83 |             4200.71 |              812.21 |             8098.29 |
| Shipping Priority (TPC-H Q3)                        |            36067.75 |             7410.09 |            38733.65 |            12735.95 |            21417.69 |
| Order Priority Checking Query (TPC-H Q4)            |            24287.67 |            10598.70 |            14173.51 |            16881.08 |            16390.00 |
| Local Supplier Volume (TPC-H Q5)                    |            12147.91 |             5402.49 |            10400.92 |             9357.54 |            10013.62 |
| Forecasting Revenue Change (TPC-H Q6)               |             1391.62 |             2232.63 |             5649.61 |             5495.35 |             5313.60 |
| Volume Shipping Query (TPC-H Q7)                    |             6564.15 |             5819.48 |            12174.28 |            10590.92 |            13018.51 |
| National Market Share (TPC-H Q8)                    |            69531.56 |            18536.40 |            55704.21 |            56368.33 |            54384.78 |
| Product Type Profit Measure (TPC-H Q9)              |            18688.47 |             5136.99 |            24809.34 |            25747.92 |            24914.46 |
| Returned Item Reporting Query (TPC-H Q10)           |            21279.34 |            13546.32 |            13077.47 |            13507.67 |            16062.81 |
| Important Stock Identification (TPC-H Q11)          |             2527.30 |             1078.84 |             3436.18 |             2554.70 |              956.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             2973.70 |             1992.39 |             5431.99 |             5696.83 |             6107.58 |
| Customer Distribution (TPC-H Q13)                   |           100139.20 |            33828.70 |            95869.63 |            98526.28 |            91777.43 |
| Promotion Effect Query (TPC-H Q14)                  |              849.85 |             1347.30 |             2272.35 |             3247.22 |             2264.52 |
| Top Supplier Query (TPC-H Q15)                      |             3454.18 |             3148.02 |             5842.88 |             3873.65 |             9300.24 |
| Parts/Supplier Relationship (TPC-H Q16)             |             5783.66 |             5692.48 |             6959.53 |             7207.31 |             7378.18 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            37248.35 |             2518.00 |            43250.75 |            42158.81 |            42879.06 |
| Large Volume Customer (TPC-H Q18)                   |            16672.61 |            12614.35 |            23322.11 |            26683.48 |            22801.29 |
| Discounted Revenue (TPC-H Q19)                      |             2399.61 |             1726.48 |             3501.65 |             3485.62 |             3747.26 |
| Potential Part Promotion (TPC-H Q20)                |             7238.10 |             4297.67 |            13829.20 |             9923.88 |            15059.59 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           110983.94 |            69695.95 |           133333.23 |            89799.88 |           120567.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |             4984.14 |             3683.31 |             3146.32 |             6407.67 |             4477.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1599.04 |      7.16 |         113.97 |                113.97 |
| monetdb-1-1-2-1 |       948.98 |      6.12 |         195.87 |                195.87 |
| monetdb-1-1-3-1 |      4181.35 |     14.44 |         255.55 |                256.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        27.41 |      0.33 |           0.39 |                  0.40 |
| monetdb-1-1-2-1 |        27.97 |      0.19 |           0.46 |                  0.47 |
| monetdb-1-1-3-1 |        87.70 |      1.71 |           0.40 |                  0.41 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
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
