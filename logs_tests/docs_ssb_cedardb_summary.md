## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 290s 
* Code: 1794008780
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['CedarDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cedardb-1-1-1-1-1 uses docker image cedardb/cedardb:v2026-10-22
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:871571
  * datadisk:3964
  * volume_size:1.8T
  * volume_used:852G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794008780

### SUT Container Restarts
* bexhoma-sut-cedardb-1-1794008780-d555c4c5b-tv9vt: 0

### Workflow

#### Actual

* DBMS CedarDB-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS CedarDB-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CedarDB-1-1 |                1 |    1 |       63.00 |           3.00 |           22.00 |          3.00 |           27.00 |              8 |           0 |             | None           |             0 | False         |               57.14 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| cedardb-1-1-1-1-1 | CedarDB-1       | cedardb-1-1-1 | cedardb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          4 |            0.02 |           203665.88 |          11700.00 |          -1 | cedardb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| cedardb-1-1-1 | cedardb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          4 |            0.02 |           203665.88 |          11700.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:--------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| cedardb-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   cedardb-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|--------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               53.77 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |               13.05 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |               12.11 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               21.70 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |               17.93 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |               19.30 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               16.33 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |               18.92 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |               17.53 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |               11.23 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |               11.97 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |               20.36 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |               17.37 |

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
