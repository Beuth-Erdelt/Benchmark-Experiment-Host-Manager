## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 378s 
* Code: 1794046827
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated).
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhousecluster-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806763
  * datadisk:260
  * volume_size:49G
  * volume_used:260M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204881
    * datadisk:363
    * volume_size:49G
    * volume_used:363M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:806763
    * datadisk:365
    * volume_size:49G
    * volume_used:365M
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716994
    * datadisk:366
    * volume_size:49G
    * volume_used:366M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794046827
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-1-1-1-2 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806763
  * datadisk:260
  * volume_size:49G
  * volume_used:260M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204881
    * datadisk:363
    * volume_size:49G
    * volume_used:363M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:806763
    * datadisk:365
    * volume_size:49G
    * volume_used:365M
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716994
    * datadisk:366
    * volume_size:49G
    * volume_used:366M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794046827
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-1-1-1-3 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806763
  * datadisk:260
  * volume_size:49G
  * volume_used:260M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204881
    * datadisk:363
    * volume_size:49G
    * volume_used:363M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:806763
    * datadisk:365
    * volume_size:49G
    * volume_used:365M
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716994
    * datadisk:366
    * volume_size:49G
    * volume_used:366M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794046827
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1794046827-65cf5965fb-b2hpz: 0
* bx-w-chc-nvme-tpch-1-0: 0
* bx-w-chc-nvme-tpch-1-1: 0
* bx-w-chc-nvme-tpch-1-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       42.00 |           6.00 |           19.00 |          4.00 |            4.00 |              8 |           0 |             | None           |             0 | False         |               85.71 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         15 |            0.18 |            19585.92 |           5280.00 |          -1 | clickhousecluster-1-1-1-1-1 |
| clickhousecluster-1-1-1-1-2 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         15 |            0.18 |            19784.66 |           5280.00 |          -1 | clickhousecluster-1-1-1-1-2 |
| clickhousecluster-1-1-1-1-3 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         11 |            0.17 |            21765.33 |           7200.00 |          -1 | clickhousecluster-1-1-1-1-3 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         15 |            0.18 |            20355.38 |          15840.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection                  | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:----------------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| clickhousecluster-1-1-1-2-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-07 11:25:48 | 2026-11-07 11:25:52 |                    4 |

### Latency of Timer Execution [ms]
| Queries                                             |   clickhousecluster-1-1-1-1-1 |   clickhousecluster-1-1-1-1-2 |   clickhousecluster-1-1-1-1-3 |
|:----------------------------------------------------|------------------------------:|------------------------------:|------------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                        376.71 |                        350.05 |                        169.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                         58.84 |                         57.51 |                         59.31 |
| Shipping Priority (TPC-H Q3)                        |                        173.43 |                        160.29 |                        190.05 |
| Order Priority Checking Query (TPC-H Q4)            |                        441.88 |                        460.00 |                        497.05 |
| Local Supplier Volume (TPC-H Q5)                    |                        251.26 |                        237.73 |                        239.10 |
| Forecasting Revenue Change (TPC-H Q6)               |                         47.32 |                         41.68 |                         40.30 |
| Volume Shipping Query (TPC-H Q7)                    |                        187.00 |                        179.50 |                        195.26 |
| National Market Share (TPC-H Q8)                    |                        270.96 |                        255.49 |                        286.57 |
| Product Type Profit Measure (TPC-H Q9)              |                        692.45 |                        364.00 |                        337.55 |
| Returned Item Reporting Query (TPC-H Q10)           |                        161.97 |                        196.28 |                        156.98 |
| Important Stock Identification (TPC-H Q11)          |                         43.34 |                         36.17 |                         24.28 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                        721.44 |                        704.82 |                        699.53 |
| Customer Distribution (TPC-H Q13)                   |                        197.80 |                        173.50 |                        160.53 |
| Promotion Effect Query (TPC-H Q14)                  |                         80.34 |                        146.05 |                         66.68 |
| Top Supplier Query (TPC-H Q15)                      |                        103.50 |                        218.87 |                        177.25 |
| Parts/Supplier Relationship (TPC-H Q16)             |                         39.32 |                         45.42 |                         34.52 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                        230.92 |                        228.89 |                        268.67 |
| Large Volume Customer (TPC-H Q18)                   |                        646.33 |                        374.27 |                        570.03 |
| Discounted Revenue (TPC-H Q19)                      |                        134.60 |                        141.74 |                        136.37 |
| Potential Part Promotion (TPC-H Q20)                |                        125.75 |                        146.76 |                        117.44 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                       2656.43 |                       2391.39 |                       2285.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |                         42.02 |                         39.75 |                         38.00 |

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
