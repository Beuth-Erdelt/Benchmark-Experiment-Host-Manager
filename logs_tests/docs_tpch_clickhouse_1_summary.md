## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 739s 
* Code: 1792777036
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958485
  * datadisk:822
  * volume_size:49G
  * volume_used:822M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792777036
* clickhouse-1-2-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958485
  * datadisk:864
  * volume_size:49G
  * volume_used:864M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * resources_total: 16.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792777036

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: ClickHouse-1-2

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1792777036-5f7588d64c-xjl2q: 0
* bexhoma-sut-clickhouse-1-1792777036-b4f76c66b-4smsw: 0

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
| ClickHouse-1-1 |                1 |    1 |       41.00 |           6.00 |           20.00 |          5.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               87.80 | False               |
| ClickHouse-1-2 |                2 |    1 |       41.00 |           6.00 |           20.00 |          5.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               87.80 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.06 |            74679.86 |           8800.00 |          -1 | clickhouse-1-1-1-1-1 |
| clickhouse-1-2-1-1-1 | ClickHouse-1    | clickhouse-1-2-1 | clickhouse-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          8 |            0.07 |            60955.95 |           9900.00 |          -1 | clickhouse-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          9 |            0.06 |            74679.86 |           8800.00 |          -1 |
| clickhouse-1-2-1 | clickhouse-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |          8 |            0.07 |            60955.95 |           9900.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| clickhouse-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   clickhouse-1-1-1-1-1 |   clickhouse-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 141.84 |                 184.80 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  53.72 |                  97.91 |
| Shipping Priority (TPC-H Q3)                        |                  43.16 |                  79.68 |
| Order Priority Checking Query (TPC-H Q4)            |                 155.03 |                 172.81 |
| Local Supplier Volume (TPC-H Q5)                    |                  44.95 |                  60.96 |
| Forecasting Revenue Change (TPC-H Q6)               |                  16.70 |                  16.03 |
| Volume Shipping Query (TPC-H Q7)                    |                  59.99 |                  60.11 |
| National Market Share (TPC-H Q8)                    |                  44.31 |                  57.70 |
| Product Type Profit Measure (TPC-H Q9)              |                  57.44 |                  60.57 |
| Returned Item Reporting Query (TPC-H Q10)           |                  68.55 |                  88.47 |
| Important Stock Identification (TPC-H Q11)          |                  22.90 |                  31.17 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  30.69 |                  45.63 |
| Customer Distribution (TPC-H Q13)                   |                  41.24 |                  64.50 |
| Promotion Effect Query (TPC-H Q14)                  |                  27.10 |                  30.07 |
| Top Supplier Query (TPC-H Q15)                      |                  33.98 |                  36.43 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  28.90 |                  36.28 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  29.91 |                  32.86 |
| Large Volume Customer (TPC-H Q18)                   |                  61.50 |                  72.04 |
| Discounted Revenue (TPC-H Q19)                      |                  44.94 |                  56.17 |
| Potential Part Promotion (TPC-H Q20)                |                  39.30 |                  38.95 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 371.27 |                 376.58 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  28.66 |                  28.89 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        25.60 |      0.25 |           0.40 |                  1.18 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |         1.42 |      0.00 |           0.04 |                  0.04 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.16 |           0.77 |                  1.58 |
| clickhouse-1-2-1-1 | n/a          |      0.19 |           0.34 |                  0.43 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| clickhouse-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-2-1-1 (bexhoma-metrics-clickhouse-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.23 |                      0.00 |                     0.00 |             37447.64 |                              4.77 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:-------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhouse-1-1-1-1 |                  0.21 |                      0.00 |                     0.00 |             35650.97 |                              4.33 |
| clickhouse-1-2-1-1 |                  0.00 |                      0.00 |                     0.00 |              1397.81 |                              0.04 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST failed: Monitoring metrics missing
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
