## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 494s 
* Code: 1793715774
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:131939
  * datadisk:2937
  * volume_size:49G
  * volume_used:2.9G
  * cpu_list:0-95
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793715774
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:131779
  * datadisk:1417
  * volume_size:49G
  * volume_used:1.4G
  * cpu_list:0-95
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793715774

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793715774-58d649c877-bsnxz: 0
* bexhoma-sut-monetdb-1-1793715774-7d97987947-7wbt8: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       57.00 |           1.00 |           27.00 |          9.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               63.16 | False               |
| MonetDB-1-2 |                2 |    1 |       57.00 |           1.00 |           27.00 |          9.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               63.16 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.08 |            57485.56 |           3771.43 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         34 |            0.07 |            65513.36 |           2329.41 |          -1 | monetdb-1-2-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.08 |            57485.56 |           3771.43 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         34 |            0.07 |            65513.36 |           2329.41 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:--------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| monetdb-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   monetdb-1-1-1-1-1 |   monetdb-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              718.36 |              724.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               19.09 |               17.87 |
| Shipping Priority (TPC-H Q3)                        |               53.56 |               58.25 |
| Order Priority Checking Query (TPC-H Q4)            |              108.71 |              105.18 |
| Local Supplier Volume (TPC-H Q5)                    |               42.27 |               36.60 |
| Forecasting Revenue Change (TPC-H Q6)               |               17.90 |               13.50 |
| Volume Shipping Query (TPC-H Q7)                    |               48.39 |               39.39 |
| National Market Share (TPC-H Q8)                    |              284.56 |              244.40 |
| Product Type Profit Measure (TPC-H Q9)              |               48.88 |               42.33 |
| Returned Item Reporting Query (TPC-H Q10)           |               84.10 |               84.62 |
| Important Stock Identification (TPC-H Q11)          |               16.10 |                8.80 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               34.24 |               27.31 |
| Customer Distribution (TPC-H Q13)                   |              274.31 |              248.81 |
| Promotion Effect Query (TPC-H Q14)                  |               23.65 |               18.06 |
| Top Supplier Query (TPC-H Q15)                      |               21.66 |               18.59 |
| Parts/Supplier Relationship (TPC-H Q16)             |               43.73 |               45.11 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               38.50 |               32.12 |
| Large Volume Customer (TPC-H Q18)                   |              151.81 |              119.45 |
| Discounted Revenue (TPC-H Q19)                      |               56.85 |               46.90 |
| Potential Part Promotion (TPC-H Q20)                |               28.90 |               33.11 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |             1165.84 |             1122.92 |
| Global Sales Opportunity Query (TPC-H Q22)          |               26.04 |               23.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
