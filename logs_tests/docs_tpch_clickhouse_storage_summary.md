## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 587s 
* Code: 1793791936
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741613
  * datadisk:11652
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793791936
* clickhouse-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:848574
  * datadisk:11690
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793791936

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouse-1-2

### Data Parameters of Reused Volumes
* ClickHouse-1: DDL values of the volume: order_orders=key, order_lineitem=key, partition_orders=none, partition_lineitem=none, index_granularity=8192, wide_parts=default, low_cardinality=off, codec=default
* ClickHouse-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1793791936-65cf9698b7-d87st: 0
* bexhoma-sut-clickhouse-1-1793791936-5dd8cfc9cf-z6zth: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouse-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS ClickHouse-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |   10 |       49.00 |           2.00 |           23.00 |         18.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              734.69 | False               |
| ClickHouse-1-2 |                2 |   10 |       49.00 |           2.00 |           23.00 |         18.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              734.69 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         21 |            0.22 |           195585.00 |          37714.29 |          -1 | clickhouse-1-1-1-1-1 |
| clickhouse-1-2-1-1-1 | ClickHouse-1    | clickhouse-1-2-1 | clickhouse-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         30 |            0.34 |           145159.34 |          26400.00 |          -1 | clickhouse-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         21 |            0.22 |           195585.00 |          37714.29 |          -1 |
| clickhouse-1-2-1 | clickhouse-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |                  22 |         30 |            0.34 |           145159.34 |          26400.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhouse-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |   clickhouse-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 300.05 |                 789.08 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 120.97 |                 242.15 |
| Shipping Priority (TPC-H Q3)                        |                 158.83 |                 295.95 |
| Order Priority Checking Query (TPC-H Q4)            |                1758.34 |                1802.68 |
| Local Supplier Volume (TPC-H Q5)                    |                 142.99 |                 321.99 |
| Forecasting Revenue Change (TPC-H Q6)               |                  61.89 |                  72.70 |
| Volume Shipping Query (TPC-H Q7)                    |                 163.28 |                 192.26 |
| National Market Share (TPC-H Q8)                    |                 170.19 |                 328.43 |
| Product Type Profit Measure (TPC-H Q9)              |                 263.93 |                 308.22 |
| Returned Item Reporting Query (TPC-H Q10)           |                 205.01 |                 260.86 |
| Important Stock Identification (TPC-H Q11)          |                  47.43 |                  66.97 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 123.70 |                 248.13 |
| Customer Distribution (TPC-H Q13)                   |                 296.53 |                 254.80 |
| Promotion Effect Query (TPC-H Q14)                  |                  86.09 |                  78.16 |
| Top Supplier Query (TPC-H Q15)                      |                 131.15 |                 133.73 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  74.07 |                  88.62 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 104.64 |                 122.55 |
| Large Volume Customer (TPC-H Q18)                   |                 257.79 |                 272.96 |
| Discounted Revenue (TPC-H Q19)                      |                 164.87 |                 309.66 |
| Potential Part Promotion (TPC-H Q20)                |                  93.40 |                 107.22 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                5071.91 |                5311.89 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 163.25 |                 169.98 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        95.99 |      2.72 |           0.82 |                 12.19 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.10 |           0.80 |                 12.18 |
| clickhouse-1-2-1-1 | n/a          |      2.77 |           1.57 |                  3.85 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.35 |                  0.35 |
| clickhouse-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.24 |                      0.00 |                     0.00 |            362580.82 |                             49.06 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.26 |                      0.00 |                     0.00 |           3652961.13 |                            122.50 |
| clickhouse-1-2-1-1 |                  0.04 |                      0.00 |                     0.00 |           2575372.70 |                             65.16 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
