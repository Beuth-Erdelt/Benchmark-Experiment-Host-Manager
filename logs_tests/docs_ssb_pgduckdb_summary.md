## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 625s 
* Code: 1793202264
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * PgDuckDB queries are forced through the DuckDB execution engine.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PgDuckDB'].
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
* pgduckdb-1-1-1-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:624990
  * datadisk:1582
  * volume_size:1.8T
  * volume_used:611G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793202264

### SUT Container Restarts
* bexhoma-sut-pgduckdb-1-1793202264-6fd988c8bc-88qpb: 0

### Workflow

#### Actual

* DBMS PgDuckDB-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS PgDuckDB-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|              |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:-------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PgDuckDB-1-1 |                1 |    1 |       86.00 |          15.00 |           21.00 |          6.00 |           30.00 |              8 |           0 |             | None           |             0 | False         |               41.86 | False               |

### Benchmarking

#### Per Connection

| DBMS               | configuration   | phase          | job              |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                |
|:-------------------|:----------------|:---------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:-------------------|
| pgduckdb-1-1-1-1-1 | PgDuckDB-1      | pgduckdb-1-1-1 | pgduckdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.34 |            10822.15 |           6685.71 |          -1 | pgduckdb-1-1-1-1-1 |

#### Per Phase

|                | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1 | pgduckdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.34 |            10822.15 |           6685.71 |          -1 |

#### Query Completion per Phase

| phase          |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:---------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| pgduckdb-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   pgduckdb-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|---------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               283.04 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                91.52 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                50.80 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               682.42 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |               862.99 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |               642.35 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               652.89 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |               612.41 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |               169.18 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                83.41 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |               942.41 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |               502.63 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |               459.07 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
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
