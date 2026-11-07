## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 317s 
* Code: 1794007596
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * Dimensions of ClickHouseCluster are a full copy on every node (-xdim replicated).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* clickhousecluster-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:867996
  * datadisk:157
  * volume_size:1.8T
  * volume_used:848G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:288106
    * datadisk:199
    * volume_size:879G
    * volume_used:282G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:867997
    * datadisk:202
    * volume_size:1.8T
    * volume_used:848G
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716496
    * datadisk:202
    * volume_size:1.8T
    * volume_used:700G
    * cpu_list:0-127
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794007596
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1794007596-7599b844c4-kf6tq: 0
* bx-w-chc-1-1794007596-0: 0
* bx-w-chc-1-1794007596-1: 0
* bx-w-chc-1-1794007596-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       39.00 |           4.00 |           20.00 |          4.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |               92.31 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          4 |            0.12 |            30605.87 |          11700.00 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          4 |            0.12 |            30605.87 |          11700.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:------------------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   clickhousecluster-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|------------------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                        107.96 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                         50.42 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                         52.98 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                         95.68 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                         84.15 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                         82.07 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                        203.07 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                        135.64 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                        130.25 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                        156.03 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                        195.86 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                        217.66 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                        181.43 |

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
