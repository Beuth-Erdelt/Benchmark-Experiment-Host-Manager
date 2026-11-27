## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 5479s 
* Code: 1795772826
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation for all components.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 1.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745327
  * datadisk:192976
  * volume_size:984G
  * volume_used:189G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795772826
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745330
  * datadisk:197881
  * volume_size:984G
  * volume_used:194G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795772826
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745330
  * datadisk:197881
  * volume_size:984G
  * volume_used:194G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795772826

### Ingestion
* MonetDB-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795772826-bffd9fd55-h2q8l: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |  100 |     4176.00 |           2.00 |          778.00 |       1572.00 |         1822.00 |              8 |         0 |             | None           |             0 | False         |               86.21 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 100.00 |               22 |                  22 |        438 |            4.61 |            78057.40 |          18082.19 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 100.00 |               22 |                  22 |        504 |            6.83 |            52702.24 |          15714.29 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 100.00 |               22 |                  22 |        584 |            6.29 |            57279.12 |          13561.64 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |                  22 |        438 |            4.61 |            78057.40 |          18082.19 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 100.00 |               44 |                  44 |        584 |            6.55 |            54943.05 |          27123.29 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-2-1-2 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            75874.25 |           127664.97 |           133185.83 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              446.42 |             1718.65 |              701.80 |
| Shipping Priority (TPC-H Q3)                        |             4662.82 |             8306.07 |             5050.49 |
| Order Priority Checking Query (TPC-H Q4)            |             9130.61 |            12585.16 |             8965.19 |
| Local Supplier Volume (TPC-H Q5)                    |             3296.92 |             5593.65 |            12193.90 |
| Forecasting Revenue Change (TPC-H Q6)               |             3177.48 |             5399.33 |             4117.72 |
| Volume Shipping Query (TPC-H Q7)                    |             5625.78 |             7659.56 |             4742.41 |
| National Market Share (TPC-H Q8)                    |            23672.01 |            19950.29 |            17320.47 |
| Product Type Profit Measure (TPC-H Q9)              |             6407.74 |            11842.74 |            12263.74 |
| Returned Item Reporting Query (TPC-H Q10)           |             9679.83 |            10109.02 |            11094.47 |
| Important Stock Identification (TPC-H Q11)          |              485.71 |              688.77 |              931.06 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1494.01 |             2603.64 |             2658.14 |
| Customer Distribution (TPC-H Q13)                   |            26593.58 |            40948.98 |            42694.69 |
| Promotion Effect Query (TPC-H Q14)                  |              700.00 |             1784.75 |             1466.68 |
| Top Supplier Query (TPC-H Q15)                      |             1633.72 |             2956.26 |             1651.94 |
| Parts/Supplier Relationship (TPC-H Q16)             |             3348.36 |             3615.47 |             3512.44 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             1562.65 |             3491.39 |             3277.52 |
| Large Volume Customer (TPC-H Q18)                   |             8226.99 |            12463.60 |            11108.67 |
| Discounted Revenue (TPC-H Q19)                      |             1295.09 |             1759.81 |             1636.87 |
| Potential Part Promotion (TPC-H Q20)                |             3454.65 |             3733.74 |             5573.33 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           239698.61 |           214580.74 |           294370.68 |
| Global Sales Opportunity Query (TPC-H Q22)          |             3171.60 |             2095.68 |             1749.77 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      8062.50 |      7.91 |         189.03 |                189.04 |
| monetdb-1-1-2-1 |      8062.50 |      7.91 |         189.03 |                189.04 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      5006.24 |      8.00 |           8.06 |                 16.00 |
| monetdb-1-1-2-1 |      5006.24 |      8.00 |           8.06 |                 16.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      1341.04 |      1.95 |           0.01 |                  6.83 |
| monetdb-1-1-2-1 |      1341.04 |      1.95 |           0.01 |                  6.83 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       918.15 |      7.09 |         247.02 |                255.99 |
| monetdb-1-1-2-1 |      1850.95 |     10.77 |         233.33 |                255.99 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        15.24 |      0.02 |           0.28 |                  0.28 |
| monetdb-1-1-2-1 |        29.14 |      0.02 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)

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
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
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
