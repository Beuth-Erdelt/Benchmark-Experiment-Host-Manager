## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 642s 
* Code: 1793781303
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated).
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
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
  * disk:793435
  * datadisk:1390
  * volume_size:49G
  * volume_used:1.4G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:602235
    * datadisk:3585
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605346
    * datadisk:3638
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:793435
    * datadisk:3639
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-223
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793781303
    * BEXHOMA_WORKERS:3
* clickhousecluster-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:793436
  * datadisk:1448
  * volume_size:49G
  * volume_used:1.5G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:602230
    * datadisk:3652
    * volume_size:49G
    * volume_used:3.6G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605345
    * datadisk:3703
    * volume_size:49G
    * volume_used:3.7G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:793436
    * datadisk:3708
    * volume_size:49G
    * volume_used:3.7G
    * cpu_list:0-223
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793781303
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouseCluster-1-2

### Data Parameters of Reused Volumes
* ClickHouseCluster-1: DDL values of the volume: order_orders=key, order_lineitem=key, partition_orders=none, partition_lineitem=none, index_granularity=8192, wide_parts=default, low_cardinality=off, codec=default
* ClickHouseCluster-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1793781303-6486b4d69-c7nzb: 0
* bx-w-clickhousecluster-nvme-tpch-10-0: 0
* bx-w-clickhousecluster-nvme-tpch-10-1: 0
* bx-w-clickhousecluster-nvme-tpch-10-2: 0
* bexhoma-sut-clickhousecluster-1-1793781303-77f7996c84-mwdhd: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouseCluster-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouseCluster-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |   10 |       55.00 |           4.00 |           25.00 |         18.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |              654.55 | False               |
| ClickHouseCluster-1-2 |                2 |   10 |       55.00 |           4.00 |           25.00 |         18.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |              654.55 | True                |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         46 |            0.72 |            62413.74 |          17217.39 |          -1 | clickhousecluster-1-1-1-1-1 |
| clickhousecluster-1-2-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-2-1 | clickhousecluster-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         45 |            0.72 |            58904.07 |          17600.00 |          -1 | clickhousecluster-1-2-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         46 |            0.72 |            62413.74 |          17217.39 |          -1 |
| clickhousecluster-1-2-1 | clickhousecluster-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         45 |            0.72 |            58904.07 |          17600.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhousecluster-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhousecluster-1-1-1-1-1 |   clickhousecluster-1-2-1-1-1 |
|:----------------------------------------------------|------------------------------:|------------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                        318.76 |                        461.70 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                        273.04 |                        276.71 |
| Shipping Priority (TPC-H Q3)                        |                        830.16 |                        852.19 |
| Order Priority Checking Query (TPC-H Q4)            |                       3582.79 |                       3598.60 |
| Local Supplier Volume (TPC-H Q5)                    |                       1216.21 |                       1528.88 |
| Forecasting Revenue Change (TPC-H Q6)               |                        156.54 |                        101.03 |
| Volume Shipping Query (TPC-H Q7)                    |                        727.03 |                        614.77 |
| National Market Share (TPC-H Q8)                    |                       1390.53 |                       1340.63 |
| Product Type Profit Measure (TPC-H Q9)              |                       1906.16 |                       1943.61 |
| Returned Item Reporting Query (TPC-H Q10)           |                        564.26 |                        649.15 |
| Important Stock Identification (TPC-H Q11)          |                         47.97 |                         64.16 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                       4743.12 |                       4677.76 |
| Customer Distribution (TPC-H Q13)                   |                        832.27 |                        829.45 |
| Promotion Effect Query (TPC-H Q14)                  |                        135.26 |                        155.99 |
| Top Supplier Query (TPC-H Q15)                      |                        220.24 |                        213.31 |
| Parts/Supplier Relationship (TPC-H Q16)             |                         67.29 |                        116.04 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                        571.53 |                        630.29 |
| Large Volume Customer (TPC-H Q18)                   |                       2993.06 |                       2607.68 |
| Discounted Revenue (TPC-H Q19)                      |                        270.41 |                        344.05 |
| Potential Part Promotion (TPC-H Q20)                |                        203.28 |                        204.94 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                      17766.56 |                      17527.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |                        162.62 |                        160.71 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        73.05 |      2.22 |           0.72 |                  1.97 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       176.96 |      4.29 |           5.24 |                 12.77 |

### Loading phase: component data generator

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |      1.43 |           1.58 |                  2.51 |

### Benchmarking phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        72.92 |      1.99 |           1.91 |                  3.18 |
| clickhousecluster-1-2-1-1 |         6.62 |      0.54 |           2.39 |                  2.61 |

### Benchmarking phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       246.25 |      7.34 |           7.40 |                 18.06 |
| clickhousecluster-1-2-1-1 |       155.74 |      5.57 |           6.04 |                  8.73 |

### Benchmarking phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        21.11 |      0.00 |           0.40 |                  0.40 |
| clickhousecluster-1-2-1-1 |        18.53 |      0.65 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  0.76 |                      3.00 |                     0.00 |            862148.70 |                            115.07 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.35 |                      6.00 |                     0.00 |          12454578.06 |                            359.17 |
| clickhousecluster-1-2-1-1 |                  0.65 |                      8.00 |                     0.00 |          18172384.55 |                            355.09 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
