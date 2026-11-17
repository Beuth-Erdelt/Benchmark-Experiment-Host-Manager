## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 539s 
* Code: 1794822683
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDBCS'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type nvme and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:906137
  * datadisk:298
  * volume_size:20G
  * volume_used:459M
  * cpu_list:0-255
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794822683
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1390286
  * datadisk:298
  * volume_size:20G
  * volume_used:459M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794822683

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Statistics

### Ingestion
* MariaDBCS-1: 5 of 5 units ok

### SUT Container Restarts
* bexhoma-sut-mariadbcs-1-1794822683-6b87fd794-gvxpn: 0
* bexhoma-sut-mariadbcs-1-1794822683-66769bc89b-m5tdj: 0

### Workflow

#### Actual

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

#### Planned

* DBMS MariaDBCS-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: ssb (1 pods)

### Loading

#### Per Run

| DBMS          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDBCS-1-1 |                1 |    1 |       72.00 |           6.00 |            0.00 |         48.00 |           12.00 |              1 |         0 |             | None           |             0 | False         |               50.00 | False               |
| MariaDBCS-1-2 |                2 |    1 |       72.00 |           6.00 |            0.00 |         48.00 |           12.00 |              1 |         0 |             | None           |             0 | False         |               50.00 | True                |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1-1-1 | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               13 |                  13 |         14 |            0.80 |             4508.99 |           3342.86 |          -1 |
| mariadbcs-1-2-1-1-1 | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               13 |                  13 |          9 |            0.56 |             6393.14 |           5200.00 |          -1 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         14 |            0.80 |             4508.99 |           3342.86 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          9 |            0.56 |             6393.14 |           5200.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| mariadbcs-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| mariadbcs-1-2-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         4.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         4.00 |                |

### Latency of Timer Execution [ms]
| Queries                                                                                |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:---------------------------------------------------------------------------------------|----------------------:|----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               1481.19 |               1065.62 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                212.45 |                167.55 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                250.02 |                206.98 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               1726.05 |               1342.26 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |               1103.21 |                673.43 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                773.51 |                510.95 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               1260.77 |                953.49 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                816.55 |                568.86 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                728.60 |                483.93 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                733.30 |                505.69 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                923.16 |                650.50 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                918.51 |                658.14 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                991.12 |                590.05 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |        72.81 |      1.24 |           4.69 |                  5.18 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 |         1.85 |      0.06 |           0.01 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.25 |           4.65 |                  5.14 |
| mariadbcs-1-2-1-1 | n/a          |      1.29 |           0.26 |                  0.45 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
