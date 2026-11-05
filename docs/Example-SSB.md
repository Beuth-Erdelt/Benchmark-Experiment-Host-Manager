# Benchmark: SSB

The Star Schema Benchmark (SSB) is a data warehouse benchmark derived from TPC-H: one fact
table `lineorder` (TPC-H's `lineitem` and `orders` combined) and four dimensions `customer`,
`supplier`, `part` and `dates`, queried by 13 queries in four flights. Bexhoma runs it with the
DBMSBenchmarker, like TPC-H and TPC-DS, on PostgreSQL, MonetDB and ClickHouse (the default
set), and on ClickHouseCluster, Citus, PgDuckDB, MySQL, MariaDB, MariaDBCS and CedarDB.

Two options choose what is measured:

| Option | Values | Meaning |
|---|---|---|
| `-xsv` | `normal` (default), `flat` | star schema, or one denormalized table `lineorder_flat` (lineorder joined with customer, supplier and part, as in the ClickHouse and Doris SSB setups) |
| `-xqv` | `spec` (default), `random` | the constants of the specification, or random parameters that keep the filter factor of each query (after Rabl et al., ICPE 2013) |
| `-xdim` | `replicated` (default), `distributed` | multi-node DBMS only (ClickHouseCluster, Citus), star schema: a full copy of every dimension on every node, or the dimensions spread over the nodes like `lineorder` (see [Multi-Node DBMS](#multi-node-dbms)) |

Sources:

* Specification: P. O'Neil, E. O'Neil, X. Chen, S. Revilak: *Star Schema Benchmark*, Revision 3, 2009, <https://www.cs.umb.edu/~poneil/StarSchemaB.PDF>
* Data generator: [eyalroz/ssb-dbgen](https://github.com/eyalroz/ssb-dbgen), commit `ae1e254`, built in the generator image with one fix for chunked generation
* Random parameters: T. Rabl, M. Poess, H.-A. Jacobsen, P. O'Neil, E. O'Neil: *Variations of the Star Schema Benchmark to Test the Effects of Data Skew on Query Performance*, ICPE 2013
* Flat table: ClickHouse docs, *Star Schema Benchmark*; Apache Doris docs, *SSB*

The queries are listed in [Queries-SSB.md](Queries-SSB.md).

**The results are not official benchmark results. The exact performance depends on a collection of parameters.**

## Perform Benchmark

```bash
bexhoma ssb run -ms 1 -dbms PostgreSQL
```

Generates SSB data at scale factor 1 (lineorder: 6 million rows), loads it into PostgreSQL and
runs the 13 queries with the constants of the specification.

A typical run, as in `scripts/test-docs-ssb.sh`:

```bash
bexhoma ssb \
  -dbms PostgreSQL \
  -sf 1 \
  -xii -xic -xis \
  -nlp 8 \
  -xdt \
  -ms 1 \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -ks no \
  run
```

This
* generates and loads SSB data at scale factor 1 (`-sf`) with 8 loader pods (`-nlp`)
* creates indexes, primary and foreign keys and statistics after loading (`-xii -xic -xis`)
* measures the data transfer volume of each query (`-xdt`)
* runs one DBMS at a time (`-ms`), with a timeout of 1200 s per query (`-t`)
* tests the result for errors and mismatches (`-tr`)
* limits and requests 64 GiB RAM for the SUT (`-lr`, `-rr`), with a 50 GiB volume if storage is used (`-rss`)
* removes the SUT at the end (`-ks no`)

The test script also sets PostgreSQL parameters for this run (`--set ... random_page_cost=1.1`,
`shared_buffers=20GB`, `work_mem=1GB`, ...), see `scripts/test-docs-ssb.sh`.

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_postgresql_summary.md" target="_blank" rel="noopener">docs_ssb_postgresql.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 423s 
* Code: 1792953270
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
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PostgreSQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668293
  * datadisk:1581
  * volume_size:1.8T
  * volume_used:653G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792953270

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792953270-747cff779f-7cfk8: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       43.00 |           6.00 |            2.00 |          3.00 |           21.00 |              8 |           0 |             | None           |             0 | False         |               83.72 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          6 |            0.09 |            41975.12 |           7800.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          6 |            0.09 |            41975.12 |           7800.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:-----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   postgresql-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|-----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                 369.59 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  24.00 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                   7.42 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                 155.97 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  70.13 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                   6.94 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                 212.07 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                 141.82 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  41.53 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  35.24 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                 764.93 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                 744.60 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                 108.46 |

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
```

</details>

The summary has the same sections as for TPC-H and TPC-DS: workload, connections, loading
times, per-query latencies, Power@Size, Throughput@Size, errors and warnings (result
mismatches across DBMS) and tests.

## Other DBMS

MonetDB, with the same post-load steps:

```bash
bexhoma ssb -dbms MonetDB -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_monetdb_summary.md" target="_blank" rel="noopener">docs_ssb_monetdb.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 400s 
* Code: 1792953734
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
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['MonetDB'].
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
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668740
  * datadisk:2025
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792953734

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792953734-7f9ddf867f-m45j9: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       66.00 |           5.00 |           21.00 |         16.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               54.55 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          2 |            0.03 |           130355.44 |          23400.00 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          2 |            0.03 |           130355.44 |          23400.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:--------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   monetdb-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|--------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               31.93 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |               12.53 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |               11.72 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               28.11 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |               32.46 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |               27.83 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               26.87 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |               28.30 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |               28.70 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |               38.69 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |               44.07 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |               35.93 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |               34.15 |

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
```

</details>

ClickHouse, which has no secondary indexes, constraints or statistics scripts (the sorting key
is part of the schema):

```bash
bexhoma ssb -dbms ClickHouse -sf 1 -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_clickhouse_summary.md" target="_blank" rel="noopener">docs_ssb_clickhouse.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 395s 
* Code: 1792954170
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['ClickHouse'].
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
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:667205
  * datadisk:486
  * volume_size:1.8T
  * volume_used:652G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792954170

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1792954170-595dd7f8dd-9gwlp: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       35.00 |           3.00 |           15.00 |          4.00 |            4.00 |              8 |           0 |             | None           |             0 | False         |              102.86 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          3 |            0.03 |           130351.72 |          15600.00 |          -1 | clickhouse-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          3 |            0.03 |           130351.72 |          15600.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:-----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   clickhouse-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|-----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                  67.66 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  17.19 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                  16.87 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                  27.28 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  28.44 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                  21.60 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                  43.11 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                  23.68 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  17.71 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  18.64 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                  51.09 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                  32.15 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                  29.87 |

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
```

</details>

PgDuckDB runs PostgreSQL with the pg_duckdb extension and uses PostgreSQL's scripts and loader.
With `-xdfe` the queries run in DuckDB's engine, otherwise in PostgreSQL's:

```bash
bexhoma ssb -dbms PgDuckDB -xdfe -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_pgduckdb_summary.md" target="_blank" rel="noopener">docs_ssb_pgduckdb.log</a></summary>

```markdown
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
```

</details>

MySQL and MariaDB load with `LOAD DATA LOCAL INFILE`. Their tables get the primary keys in the
schema script (InnoDB stores a table in key order, so a key added after the load rebuilds the
table); `-xic` adds the foreign keys. The flat queries have a MySQL variant without
`CAST(... AS INTEGER)`, which MySQL does not know:

```bash
bexhoma ssb -dbms MySQL -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_mysql_summary.md" target="_blank" rel="noopener">docs_ssb_mysql.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 610s 
* Code: 1793208131
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
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['MySQL'].
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
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:660571
  * datadisk:34417
  * volume_size:1.8T
  * volume_used:646G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793208131

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793208131-5f4779f7bd-bnxb6: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |       94.00 |           5.00 |           17.00 |         11.00 |           49.00 |              8 |           0 |             | None           |             0 | False         |               38.30 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         22 |            0.51 |             7147.10 |           2127.27 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         22 |            0.51 |             7147.10 |           2127.27 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   mysql-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |           1177.30 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |             98.05 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |             25.91 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |           2488.97 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |            510.27 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |             43.54 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |           5712.01 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |            654.17 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |            155.14 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |            112.06 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |           4134.77 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |           2640.91 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |           1145.44 |

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
```

</details>

```bash
bexhoma ssb -dbms MariaDB -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_mariadb_summary.md" target="_blank" rel="noopener">docs_ssb_mariadb.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 519s 
* Code: 1793208774
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
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['MariaDB'].
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
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:628165
  * datadisk:1568
  * volume_size:1.8T
  * volume_used:614G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793208774

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793208774-85ddf99d79-vs78r: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |       85.00 |           5.00 |           24.00 |         10.00 |           36.00 |              8 |           0 |             | None           |             0 | False         |               42.35 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         13 |            0.31 |            11824.30 |           3600.00 |          -1 | mariadb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         13 |            0.31 |            11824.30 |           3600.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:--------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   mariadb-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|--------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |              732.99 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |               61.52 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |               14.74 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |              589.33 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |              116.02 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |               15.21 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |             2713.97 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |              877.67 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |              345.48 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |               98.40 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |             3348.39 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |             2215.52 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |              465.01 |

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
```

</details>

## Multi-Node DBMS

ClickHouseCluster (a coordinator and `-nw` shards) and Citus (a coordinator and `-nw` workers)
spread `lineorder` (and `lineorder_flat`) over the nodes by `lo_orderkey`. The loaders write to the
coordinator, which sends the rows to the nodes. For the dimensions there are two placements
(`-xdim`, star schema only):

| `-xdim` | ClickHouseCluster | Citus | Joins |
|---|---|---|---|
| `replicated` (default) | `ReplicatedMergeTree` on every node: the coordinator and all shards are replicas of one table, Keeper (in the coordinator) copies the parts | reference tables | run on every shard against its local copy |
| `distributed` | `Distributed` tables over `<name>_local` on the shards, as for TPC-H | distributed tables | ClickHouse sends the dimension to all shards per query (`GLOBAL`), Citus runs a repartition join |

ClickHouseCluster with replicated dimensions:

```bash
bexhoma ssb -dbms ClickHouseCluster -nw 3 -sf 1 -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_clickhousecluster_summary.md" target="_blank" rel="noopener">docs_ssb_clickhousecluster.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 901s 
* Code: 1793200104
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
  * Experiment uses bexhoma version 0.11.9.
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
  * disk:622971
  * datadisk:228
  * volume_size:1.8T
  * volume_used:609G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:622974
    * datadisk:279
    * volume_size:1.8T
    * volume_used:609G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:561714
    * datadisk:281
    * volume_size:879G
    * volume_used:549G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:500512
    * datadisk:269
    * volume_size:1.8T
    * volume_used:489G
    * cpu_list:0-127
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793200104
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1793200104-75dff9c997-fn892: 0
* bexhoma-worker-clickhousecluster-ssb-1-0: 0
* bexhoma-worker-clickhousecluster-ssb-1-1: 0
* bexhoma-worker-clickhousecluster-ssb-1-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       63.00 |          17.00 |           17.00 |          5.00 |           11.00 |              8 |           0 |             | None           |             0 | False         |               57.14 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          5 |            0.13 |            29496.77 |           9360.00 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          5 |            0.13 |            29496.77 |           9360.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:------------------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   clickhousecluster-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|------------------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                        170.65 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                         50.13 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                         47.77 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                         93.90 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                         84.34 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                         73.03 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                        214.10 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                        140.41 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                        142.04 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                        161.75 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                        193.41 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                        218.62 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                        193.14 |

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
```

</details>

ClickHouseCluster with distributed dimensions:

```bash
bexhoma ssb -dbms ClickHouseCluster -nw 3 -xdim distributed -sf 1 -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_clickhousecluster_distributed_summary.md" target="_blank" rel="noopener">docs_ssb_clickhousecluster_distributed.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 1060s 
* Code: 1793201126
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * Dimensions of ClickHouseCluster are spread over the nodes like lineorder (-xdim distributed).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
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
  * disk:623775
  * datadisk:211
  * volume_size:1.8T
  * volume_used:610G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:623890
    * datadisk:270
    * volume_size:1.8T
    * volume_used:610G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:500517
    * datadisk:272
    * volume_size:1.8T
    * volume_used:489G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:561727
    * datadisk:279
    * volume_size:879G
    * volume_used:549G
    * cpu_list:0-127
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793201126
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1793201126-6c7c6854fc-gbmvc: 0
* bexhoma-worker-clickhousecluster-ssb-distributed-1-0: 0
* bexhoma-worker-clickhousecluster-ssb-distributed-1-1: 0
* bexhoma-worker-clickhousecluster-ssb-distributed-1-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       53.00 |          15.00 |           12.00 |          4.00 |           12.00 |              8 |           0 |             | None           |             0 | False         |               67.92 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         12 |            0.46 |             7835.72 |           3900.00 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         12 |            0.46 |             7835.72 |           3900.00 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:------------------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   clickhousecluster-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|------------------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                        240.04 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                        112.10 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                         77.86 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                        318.90 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                        220.45 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                        201.92 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                        901.72 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                        809.82 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                        744.89 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                       1102.99 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                       1356.16 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                       1245.85 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                       1347.81 |

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
```

</details>

Citus with reference tables:

```bash
bexhoma ssb -dbms Citus -nw 3 -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_citus_summary.md" target="_blank" rel="noopener">docs_ssb_citus.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 892s 
* Code: 1793202939
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * Dimensions of Citus are a full copy on every node (-xdim replicated).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['Citus'].
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
* citus-1-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:624899
  * datadisk:58
  * volume_size:1.8T
  * volume_used:611G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:624899
    * datadisk:800
    * volume_size:1.8T
    * volume_used:611G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:562889
    * datadisk:800
    * volume_size:879G
    * volume_used:550G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:513225
    * datadisk:735
    * volume_size:1.8T
    * volume_used:502G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793202939
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-citus-1-1793202939-96b75f7b9-27p6z: 0
* bexhoma-worker-citus-ssb-1-0: 0
* bexhoma-worker-citus-ssb-1-1: 0
* bexhoma-worker-citus-ssb-1-2: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |    1 |       63.00 |           7.00 |           23.00 |          5.00 |           20.00 |              8 |           0 |             | None           |             0 | False         |               57.14 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| citus-1-1-1-1-1 | Citus-1         | citus-1-1-1 | citus-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          4 |            0.09 |            41691.60 |          11700.00 |          -1 | citus-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          4 |            0.09 |            41691.60 |          11700.00 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| citus-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   citus-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |            124.75 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |             53.38 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |             29.00 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |            158.45 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |            113.60 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |             57.84 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |            143.80 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |             82.57 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |             58.55 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |             55.35 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |            164.63 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |            123.80 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |             94.07 |

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
```

</details>

* With `replicated`, the check script of ClickHouseCluster waits until every node has fetched the dimension parts (`SYSTEM SYNC REPLICA`) and fails if a node holds other rows than the coordinator.
* With `distributed`, Citus gets only the primary keys from `-xic`: a foreign key between distributed tables needs them co-located, and `lineorder` is distributed by its own key.
* The two placements get different volumes (`ssb-<SF>` and `ssb-distributed-<SF>`), so `-rst` never reuses one for the other.
* The scripts of `distributed` are in the subfolder `distributed` of the DBMS folder.

## Data Generation and Loading

Each loader pod runs the generator as an init container, then the loader of its DBMS.

* lineorder is generated in as many chunks as there are loader pods (`dbgen -T l -C <N> -S <k>`); pod 1 also generates the dimensions.
* The files are written to the shared volume `bexhoma-data`, `/data/ssb/SF<SF>/<N>/<k>`, and reused by later experiments with the same scale factor and number of pods.
* Each pod loads the files of its own folder, all pods start loading together.
* The chunks are exactly the data of an unchunked generation, so the data does not depend on `-nlp`.

| Table | Rows |
|---|---|
| `customer` | 30,000 x SF |
| `supplier` | 2,000 x SF |
| `part` | 200,000 x floor(1 + log2 SF) |
| `dates` | 2,557 |
| `lineorder` | about 6,000,000 x SF |

Loading tools: `psql \COPY` (PostgreSQL, PgDuckDB, Citus), `mclient COPY` (MonetDB),
`clickhouse-client INSERT ... FORMAT CSV` (ClickHouse, ClickHouseCluster), `LOAD DATA LOCAL INFILE`
(MySQL, MariaDB). A loader pod fails if a table does not load completely.

`-xlit <table>` loads only one table.

## Flat Table

```bash
bexhoma ssb -dbms PostgreSQL MonetDB ClickHouse -sf 1 -xsv flat -xii -xis -nlp 8 -xdt -ms 10 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

With `-xsv flat` the generator pods build `lineorder_flat.tbl` from their lineorder chunk and
the full customer, supplier and part tables, before loading. The DBMS then ingests only
`lineorder_flat`, in parallel per pod; the join is not part of the measured loading time.

* Columns: the 17 lineorder columns, then all customer, supplier and part columns without their keys. `lo_orderdate` and `lo_commitdate` are `DATE`.
* The join streams: `sort` and `join` for customer, an awk lookup for supplier and part. Memory stays bounded (a 512 MB sort buffer plus supplier and part, about 1 GB at SF 1000); the sorts need temporary disk space on the node of about 6.7x the lineorder chunk (about 2x the flat chunk; SF 10 in 8 chunks: 4.9 GB per pod).
* The file is about 3.4 times the size of the lineorder data and is stored in `/data/ssb/SF<SF>/flat/<N>/<k>`, next to the star schema files. At SF 100 that is about 200 GB on the shared volume.
* A flat experiment gets its own volume label (`ssb-flat-<SF>`), so it never reuses a volume loaded with the star schema.
* `-xic` has no effect: `lineorder_flat` has no keys to constrain.

The flat queries are the star schema queries with predicates on `lo_orderdate` instead of the
date dimension. They return the same results.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_flat_summary.md" target="_blank" rel="noopener">docs_ssb_flat.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 636s 
* Code: 1792954604
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there). The queries read the denormalized table lineorder_flat; year, month and week come from lo_orderdate.
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the flat table lineorder_flat (-xsv flat).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PostgreSQL', 'MonetDB', 'ClickHouse'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:674964
  * datadisk:1617
  * volume_size:1.8T
  * volume_used:660G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792954604
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:674964
  * datadisk:2153
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792954604
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:674964
  * datadisk:4470
  * volume_size:1.8T
  * volume_used:660G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792954604

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1792954604-7f7c94df9d-hxlll: 0
* bexhoma-sut-monetdb-1-1792954604-56d6d765c7-7chmx: 0
* bexhoma-sut-postgresql-1-1792954604-bb6bb6b59-jx7tn: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       60.00 |           4.00 |           33.00 |          3.00 |            8.00 |              8 |           0 |             | None           |             0 | False         |               60.00 | False               |
| MonetDB-1-1    |                1 |    1 |       84.00 |           4.00 |            7.00 |         45.00 |           18.00 |              8 |           0 |             | None           |             0 | False         |               42.86 | False               |
| PostgreSQL-1-1 |                1 |    1 |       90.00 |           6.00 |           28.00 |         10.00 |           30.00 |              8 |           0 |             | None           |             0 | False         |               40.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.04 |            93570.10 |           6685.71 |          -1 | clickhouse-1-1-1-1-1 |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          6 |            0.05 |            79240.82 |           7800.00 |          -1 | monetdb-1-1-1-1-1    |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          5 |            0.07 |            57826.41 |           9360.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.04 |            93570.10 |           6685.71 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          6 |            0.05 |            79240.82 |           7800.00 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          5 |            0.07 |            57826.41 |           9360.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:-----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| monetdb-1-1-1    |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| postgresql-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   clickhouse-1-1-1-1-1 |   monetdb-1-1-1-1-1 |   postgresql-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|-----------------------:|--------------------:|-----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                 159.32 |              345.17 |                 607.87 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  13.47 |             1535.12 |                  43.39 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                  10.44 |               19.78 |                  10.37 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                  32.66 |               20.37 |                 196.06 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  25.60 |               22.14 |                  70.48 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                1999.10 |               23.52 |                  11.37 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                  48.17 |               32.80 |                 384.27 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                  28.77 |               28.30 |                  50.54 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  21.03 |               34.14 |                   8.39 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  12.00 |               27.75 |                   7.52 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                  43.58 |               26.59 |                 289.11 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                  24.33 |               38.77 |                 246.00 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                  29.15 |               34.84 |                  56.34 |

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
```

</details>

## Random Parameters

```bash
bexhoma ssb -dbms PostgreSQL -sf 1 -xqv random -xrcp -ne 1,2 -xii -xic -xis -nlp 8 -xdt -ms 10 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

With `-xqv random` each query draws its constants: a year, month, week, region, nation, city,
category or brand from the whole hierarchy level, ranges over discount and quantity with the
width of the specification. Correlated values are drawn together (two cities of one nation, a
nation of the drawn region). So every query keeps the filter factor of the specification.
Without `-xrcp` all streams use the same parameters, with `-xrcp` each stream draws its own.
The drawn values are in the protocol of the experiment.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_random_summary.md" target="_blank" rel="noopener">docs_ssb_random.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 483s 
* Code: 1792955292
* This includes the 13 queries of the Star Schema Benchmark as templates with random parameters (generalization after Rabl et al., ICPE 2013): every predicate picks a random member of its hierarchy level or moves its range, so each query keeps the filter factor of the specification.
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Queries use random parameters that keep the filter factor of the specification (-xqv random).
  * Query ordering is Q1.1 - Q4.3.
  * All instances use different query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668307
  * datadisk:1581
  * volume_size:1.8T
  * volume_used:653G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792955292
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668307
  * datadisk:1581
  * volume_size:1.8T
  * volume_used:653G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792955292
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668307
  * datadisk:1581
  * volume_size:1.8T
  * volume_used:653G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792955292

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792955292-5df6f64f6-sql4c: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ssb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: ssb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       59.00 |           6.00 |           20.00 |          4.00 |           21.00 |              8 |           0 |             | None           |             0 | False         |               61.02 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.09 |            41705.38 |           6685.71 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.09 |            43377.94 |           6685.71 |          -1 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               13 |                  13 |          8 |            0.09 |            43388.58 |           5850.00 |          -1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          7 |            0.09 |            41705.38 |           6685.71 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               26 |                  26 |          8 |            0.09 |            43383.26 |          11700.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:-----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| postgresql-1-1-2 |      2 | 2/2                                                                      | 2/2                                                                       | 2/2                                                                      | 2/2                                                                                     | 2/2                                                                                | 2/2                                                                  | 2/2                                                                                 | 2/2                                                                               | 2/2                                                                              | 2/2                                                                                  | 2/2                                                                                      | 2/2                                                                           | 2/2                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:---------------------------------------------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                 385.67 |                 380.39 |                 350.13 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  24.55 |                  22.42 |                  21.09 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                   7.09 |                   6.78 |                   6.81 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                 163.64 |                 154.06 |                 140.79 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  43.11 |                  38.92 |                  39.22 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                   6.36 |                   6.28 |                   6.83 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                 234.23 |                 238.02 |                 238.60 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                 164.93 |                 153.18 |                 168.99 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  44.82 |                  44.91 |                  47.11 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  24.86 |                  25.22 |                  25.17 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                 945.65 |                 906.30 |                 885.77 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                 839.86 |                 836.03 |                 886.82 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                 143.54 |                 130.01 |                 123.98 |

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
```

</details>

## Use Persistent Storage

```bash
bexhoma ssb -dbms PostgreSQL -sf 1 -nc 2 -xii -xic -xis -nlp 8 -xdt -ms 10 -t 1200 -tr -lr 64Gi -rr 64Gi -rsr -rss 50Gi -rst <storage class> -ks no run
```

As for TPC-H: the first run loads the data into a persistent volume, the second run (`-nc 2`)
starts the SUT again on that volume and skips loading (see Inherited Loading in the summary).

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_storage_summary.md" target="_blank" rel="noopener">docs_ssb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 756s 
* Code: 1792955824
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
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PostgreSQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:666730
  * datadisk:1581
  * volume_size:49G
  * volume_used:1.6G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792955824
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:666733
  * datadisk:1581
  * volume_size:49G
  * volume_used:1.6G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792955824

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792955824-86d796b4df-vzm4m: 0
* bexhoma-sut-postgresql-1-1792955824-74b67c9c7-wgc8w: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ssb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       60.00 |           8.00 |           18.00 |          3.00 |           23.00 |              8 |           0 |             | None           |             0 | False         |               60.00 | False               |
| PostgreSQL-1-2 |                2 |    1 |       60.00 |           8.00 |           18.00 |          3.00 |           23.00 |              8 |           0 |             | None           |             0 | False         |               60.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          5 |            0.09 |            40775.27 |           9360.00 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         37 |            0.17 |            21974.10 |           1264.86 |          -1 | postgresql-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          5 |            0.09 |            40775.27 |           9360.00 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               13 |                  13 |         37 |            0.17 |            21974.10 |           1264.86 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:-----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| postgresql-1-2-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:---------------------------------------------------------------------------------------|-----------------------:|-----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                 356.73 |               32485.66 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  22.26 |                  39.76 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                   9.57 |                  11.47 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                 177.98 |                 433.68 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  45.29 |                  62.09 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                   6.85 |                   8.38 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                 219.82 |                 260.51 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                 149.62 |                 290.21 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  42.85 |                  69.36 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  35.04 |                  33.93 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                 894.97 |                 914.94 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                 886.10 |                 869.79 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                 120.53 |                 129.36 |

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
```

</details>

## Load Only

```bash
bexhoma ssb -dbms PostgreSQL -sf 1 -xii -xic -xis -nlp 8 -ms 10 -lr 64Gi -rr 64Gi -rss 50Gi -ks no load
```

Mode `load` generates and loads the data and runs the post-load scripts, but no queries.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_load_summary.md" target="_blank" rel="noopener">docs_ssb_load.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Data Loading SF=1
* Type: ssb
* Duration: 396s 
* Code: 1792956624
* Load data and do not run a benchmark.
* This imports SSB data sets.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT pods are stopped after loading.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668317
  * datadisk:1581
  * volume_size:1.8T
  * volume_used:653G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792956624

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792956624-76446f7964-gnk64: 0

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       53.00 |           4.00 |           20.00 |          4.00 |           17.00 |              8 |           0 |             | None           |             0 | False         |               67.92 | False               |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
```

</details>

## Monitoring

With `-m` (SUT) and `-mc` (cluster), bexhoma collects the resource use of the SUT and of the job pods (data generator, loader, benchmarker).
A phase needs at least two scrapes of the monitoring to show up.
At scaling factor 10, loading is long enough for that, while the benchmarking of a single stream is not: its gaps are marked as expected in the tests.
The DBMS run one after another (`-ms 1`), which keeps the metrics of one SUT free of the others.

```bash
bexhoma ssb \
  -dbms PostgreSQL MonetDB ClickHouse \
  -sf 10 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -m \
  -mc \
  -ms 1 \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 100Gi \
  -ks no \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ssb_monitoring.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_monitoring_summary.md" target="_blank" rel="noopener">docs_ssb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 400s 
* Code: 1792953734
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
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['MonetDB'].
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
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:668740
  * datadisk:2025
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792953734

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1792953734-7f9ddf867f-m45j9: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    1 |       66.00 |           5.00 |           21.00 |         16.00 |           16.00 |              8 |           0 |             | None           |             0 | False         |               54.55 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          2 |            0.03 |           130355.44 |          23400.00 |          -1 | monetdb-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          2 |            0.03 |           130355.44 |          23400.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:--------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   monetdb-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|--------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |               31.93 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |               12.53 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |               11.72 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |               28.11 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |               32.46 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |               27.83 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |               26.87 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |               28.30 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |               28.70 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |               38.69 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |               44.07 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |               35.93 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |               34.15 |

### Errors (failed queridone
PostgreSQL-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 16 API requests 0.9s)
- waiting 30s -               : done
PostgreSQL-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.4s (0 kubectl calls 0.0s, 16 API requests 0.5s)
- waiting 30s -               : done
PostgreSQL-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 16 API requests 0.4s)
- waiting 30s -               : done
PostgreSQL-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.4s (0 kubectl calls 0.0s, 16 API requests 0.5s)
- waiting 30s -               : done
PostgreSQL-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 16 API requests 0.4s)
- waiting 30s -               : done
PostgreSQL-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 2.8s (0 kubectl calls 0.0s, 16 API requests 0.5s)
- waiting 30s -               : done
PostgreSQL-1                  : will start now
PostgreSQL-1                  : deployments ['sut']
PostgreSQL-1                  : stateful sets []
PostgreSQL-1                  : pvcs ['sut']
PostgreSQL-1                  : name of SUT pods = bexhoma-sut-postgresql-1-1793810696
PostgreSQL-1                  : name of SUT service = bexhoma-sut-postgresql-1-1793810696
MonetDB-1                     : has to wait - 0 running and 1 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 0 running and 1 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.6s (1 kubectl calls 0.6s, 17 API requests 0.6s)
- waiting 30s -               : done
PostgreSQL-1                  : waits for health check to succeed
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 24 API requests 0.9s)
- waiting 30s -               : done
PostgreSQL-1                  : waits for health check to succeed
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.3s (0 kubectl calls 0.0s, 24 API requests 1.0s)
- waiting 30s -               : done
PostgreSQL-1                  : waits for health check to succeed
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.8s (0 kubectl calls 0.0s, 24 API requests 0.9s)
- waiting 30s -               : done
PostgreSQL-1                  : waits for health check to succeed
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 24 API requests 0.7s)
- waiting 30s -               : done
PostgreSQL-1                  : is not loaded yet
PostgreSQL-1                  : load durability relaxed, scripts ['durability-relaxed.sql', 'restoredurability-relaxed.sql']
PostgreSQL-1                  : connect to pod bexhoma-sut-postgresql-1-1793810696-867c6c8b44-69g49 to load scripts
PostgreSQL-1                  : start asynch loading scripts of type schema
PostgreSQL-1                  : waits for the Schema scripts (schema=True) before starting the loading jobs
PostgreSQL-1                  : Schema scripts done after 4s
PostgreSQL-1                  : is loading
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 11.2s (8 kubectl calls 4.8s, 45 API requests 2.5s)
- waiting 30s -               : done
PostgreSQL-1                  : is loading
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 42 API requests 1.6s)
- waiting 30s -               : done
PostgreSQL-1                  : is loading
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 42 API requests 1.7s)
- waiting 30s -               : done
PostgreSQL-1                  : showing loader times (ssb-loader)
PostgreSQL-1                  : generator times (start/end per pod and container) [(1793812180, 1793812193), (1793812189, 1793812193), (1793812192, 1793812192), (1793812180, 1793812193), (1793812185, 1793812193), (1793812183, 1793812193), (1793812181, 1793812193), (1793812182, 1793812193)]
PostgreSQL-1                  : loader times (start/end per pod and container) [(1793812204, 1793812245), (1793812204, 1793812241), (1793812204, 1793812233), (1793812203, 1793812242), (1793812204, 1793812243), (1793812204, 1793812241), (1793812204, 1793812243), (1793812204, 1793812242)]
PostgreSQL-1                  : total times (start/end per pod and container) [(1793812180, 1793812193), (1793812189, 1793812193), (1793812192, 1793812192), (1793812180, 1793812193), (1793812185, 1793812193), (1793812183, 1793812193), (1793812181, 1793812193), (1793812182, 1793812193), (1793812204, 1793812245), (1793812204, 1793812241), (1793812204, 1793812233), (1793812203, 1793812242), (1793812204, 1793812243), (1793812204, 1793812241), (1793812204, 1793812243), (1793812204, 1793812242)]
PostgreSQL-1                  : generator timespan (first to last [s]) = 13
PostgreSQL-1                  : loader timespan (first to last [s]) = 42
PostgreSQL-1                  : total timespan (first to last [s]) = 65
PostgreSQL-1                  : connect to pod bexhoma-sut-postgresql-1-1793810696-867c6c8b44-69g49 to load scripts
PostgreSQL-1                  : start asynch loading scripts of type index
PostgreSQL-1                  : is loading
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 35.3s (41 kubectl calls 22.6s, 70 API requests 3.1s)
- waiting 30s -               : done
PostgreSQL-1                  : is loading
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 22 API requests 0.8s)
- waiting 30s -               : done
PostgreSQL-1                  : is loading
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 22 API requests 0.9s)
- waiting 30s -               : done
Experiment                    : Reset experiment counter. This is first run of client number 1.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-1-1-PostgreSQL-1-1793810696 initialized to 1.
PostgreSQL-1                  : benchmarks done 0 of 1. This will be client 1
MonetDB-1                     : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 2 running and 0 pending pods: max is 1 pods per cluster
postgresql-1-1-1-1            : start benchmarking (benchmark_run=1)
postgresql-1-1-1-1            : needs monitoring (common metrics) for deployment sut
PostgreSQL-1                  : benchmarking results in folder C:\data\benchmarks/1793810696
PostgreSQL-1                  : submitted benchmarker job in 4.9s (4 kubectl calls 2.6s, 24 API requests 2.2s)
postgresql-1-1-1-1            : needs monitoring (common metrics) for deployment sut
postgresql-1-1-1-1            : collecting loading metrics of SUT at connection postgresql-1-1-1-1
postgresql-1-1-1-1            : collecting metrics of data generator at connection postgresql-1-1-1-1
postgresql-1-1-1-1            : collecting metrics of data injector at connection postgresql-1-1-1-1
postgresql-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)postgresql-1-1793810696(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)postgresql-1-1793810696(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
postgresql-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-loading-postgresql-1-1793810696-1-.+", namespace="perdelt", container="datagenerator"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-loading-postgresql-1-1793810696-1-.+", namespace="perdelt", container="datagenerator"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
postgresql-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-loading-postgresql-1-1793810696-1-.+", namespace="perdelt", container="sensor"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-loading-postgresql-1-1793810696-1-.+", namespace="perdelt", container="sensor"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
postgresql-1-1-1-1            : WARNING metric missing for loader: CPU Throttling Rate [s/s]
postgresql-1-1-1-1            : WARNING metric missing for loader: CPU Throttled Time [s]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: Memory Usage, Working Set [MiB]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: Memory Usage incl. Page Cache [MiB]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: CPU Throttling Rate [s/s]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: CPU Utilization [CPUs]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: CPU System Time [s]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: CPU Utilization Time [s]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: CPU User Time [s]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: CPU Throttled Time [s]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
postgresql-1-1-1-1            : WARNING metric missing for datagenerator: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
postgresql-1-1-1-1            : WARNING metric missing for loading: CPU Throttling Rate [s/s]
postgresql-1-1-1-1            : WARNING metric missing for loading: CPU Throttled Time [s]
Experiment                    : fetched 3 metric sets in 5s (3 at once, 0 repeated, 0 follow-up actions; 5 kubectl calls 11.0s, 0 API requests 0.0s)
Loop pass                     : took 11.9s (11 kubectl calls 14.5s, 52 API requests 3.8s)
- waiting 30s -               : done
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
postgresql-1-1-1-1            : wrote benchmarking_timespans to /data/benchmarks/1793810696/postgresql-1-1-1-1.config
postgresql-1-1-1-1            : showing benchmarker times
postgresql-1-1-1-1            : benchmarker timespan job from 1793812391 to 1793812429
postgresql-1-1-1-1            : benchmarker timespan pods from 1793812401 to 1793812414
postgresql-1-1-1-1            : benchmarker timespan (start to end single container [s]) = 13
postgresql-1-1-1-1            : benchmarker times (start/end per pod and container) = [(1793812401, 1793812414)]
postgresql-1-1-1-1            : found and updated times {'benchmarker': [(1793812401, 1793812414)]}
postgresql-1-1-1-1            : needs monitoring (common metrics) for deployment sut
postgresql-1-1-1-1            : collecting execution metrics of SUT at connection postgresql-1-1-1-1
postgresql-1-1-1-1            : collecting metrics of benchmarker at connection postgresql-1-1-1-1
postgresql-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)postgresql-1-1793810696(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)postgresql-1-1793810696(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
postgresql-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-postgresql-1-1793810696-1-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-postgresql-1-1793810696-1-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
postgresql-1-1-1-1            : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarking: CPU Throttled Time [s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: Memory Usage, Working Set [MiB]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: Memory Usage incl. Page Cache [MiB]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: CPU Utilization [CPUs]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: CPU Throttled Time [s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: CPU Utilization Time [s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: CPU System Time [s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: CPU User Time [s]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
postgresql-1-1-1-1            : WARNING metric missing for benchmarker: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
Experiment                    : fetched 2 metric sets in 5s (2 at once, 0 repeated, 0 follow-up actions; 4 kubectl calls 7.9s, 0 API requests 0.0s)
Loop pass                     : took 9.1s (9 kubectl calls 10.8s, 32 API requests 1.4s)
PostgreSQL-1                  : can be stopped
PostgreSQL-1                  : had 0 restarts at worker bexhoma-sut-postgresql-1-1793810696-867c6c8b44-69g49
MonetDB-1                     : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 3.5s (4 kubectl calls 1.9s, 39 API requests 1.4s)
- waiting 30s -               : done
MonetDB-1                     : will start now
MonetDB-1                     : deployments ['sut']
MonetDB-1                     : stateful sets []
MonetDB-1                     : pvcs ['sut']
MonetDB-1                     : name of SUT pods = bexhoma-sut-monetdb-1-1793810696
MonetDB-1                     : name of SUT service = bexhoma-sut-monetdb-1-1793810696
ClickHouse-1                  : has to wait - 0 running and 1 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.9s (1 kubectl calls 0.5s, 16 API requests 0.5s)
- waiting 30s -               : done
MonetDB-1                     : is not loaded yet
MonetDB-1                     : will start loading but not before 2026-11-04 17:16:01 (that is in 60 secs)
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 23 API requests 0.8s)
- waiting 30s -               : done
MonetDB-1                     : is not loaded yet
MonetDB-1                     : will start loading but not before 2026-11-04 17:16:01
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 0.5s (0 kubectl calls 0.0s, 20 API requests 0.6s)
- waiting 30s -               : done
MonetDB-1                     : is not loaded yet
MonetDB-1                     : load durability relaxed, scripts []
MonetDB-1                     : connect to pod bexhoma-sut-monetdb-1-1793810696-677b54c8d4-kh67x to load scripts
MonetDB-1                     : start asynch loading scripts of type schema
MonetDB-1                     : waits for the Schema scripts (schema=True) before starting the loading jobs
MonetDB-1                     : Schema scripts done after 2s
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 13.2s (5 kubectl calls 2.7s, 40 API requests 2.7s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 41 API requests 1.7s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 41 API requests 1.6s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.7s (0 kubectl calls 0.0s, 41 API requests 1.3s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 41 API requests 1.4s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 15.9s (24 kubectl calls 13.5s, 49 API requests 2.0s)
- waiting 30s -               : done
MonetDB-1                     : showing loader times (ssb-loader)
MonetDB-1                     : generator times (start/end per pod and container) [(1793812595, 1793812612), (1793812612, 1793812612), (1793812602, 1793812612), (1793812593, 1793812612), (1793812605, 1793812613), (1793812594, 1793812612), (1793812610, 1793812612), (1793812599, 1793812612)]
MonetDB-1                     : loader times (start/end per pod and container) [(1793812627, 1793812730), (1793812626, 1793812722), (1793812627, 1793812725), (1793812627, 1793812731), (1793812627, 1793812729), (1793812626, 1793812727), (1793812627, 1793812721), (1793812627, 1793812728)]
MonetDB-1                     : total times (start/end per pod and container) [(1793812595, 1793812612), (1793812612, 1793812612), (1793812602, 1793812612), (1793812593, 1793812612), (1793812605, 1793812613), (1793812594, 1793812612), (1793812610, 1793812612), (1793812599, 1793812612), (1793812627, 1793812730), (1793812626, 1793812722), (1793812627, 1793812725), (1793812627, 1793812731), (1793812627, 1793812729), (1793812626, 1793812727), (1793812627, 1793812721), (1793812627, 1793812728)]
MonetDB-1                     : generator timespan (first to last [s]) = 20
MonetDB-1                     : loader timespan (first to last [s]) = 105
MonetDB-1                     : total timespan (first to last [s]) = 138
MonetDB-1                     : connect to pod bexhoma-sut-monetdb-1-1793810696-677b54c8d4-kh67x to load scripts
MonetDB-1                     : start asynch loading scripts of type index
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 12.2s (14 kubectl calls 9.5s, 53 API requests 2.8s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.5s (0 kubectl calls 0.0s, 21 API requests 1.3s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 21 API requests 1.2s)
- waiting 30s -               : done
MonetDB-1                     : is loading
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 3.8s (0 kubectl calls 0.0s, 21 API requests 0.6s)
- waiting 30s -               : done
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-1-1-MonetDB-1-1793810696 initialized to 1.
MonetDB-1                     : benchmarks done 0 of 1. This will be client 1
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
monetdb-1-1-1-1               : start benchmarking (benchmark_run=1)
monetdb-1-1-1-1               : needs monitoring (common metrics) for deployment sut
MonetDB-1                     : benchmarking results in folder C:\data\benchmarks/1793810696
MonetDB-1                     : submitted benchmarker job in 4.0s (3 kubectl calls 1.7s, 23 API requests 2.2s)
monetdb-1-1-1-1               : needs monitoring (common metrics) for deployment sut
monetdb-1-1-1-1               : collecting loading metrics of SUT at connection monetdb-1-1-1-1
monetdb-1-1-1-1               : collecting metrics of data generator at connection monetdb-1-1-1-1
monetdb-1-1-1-1               : collecting metrics of data injector at connection monetdb-1-1-1-1
monetdb-1-1-1-1               : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)monetdb-1-1793810696(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)monetdb-1-1793810696(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
monetdb-1-1-1-1               : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-loading-monetdb-1-1793810696-1-.+", namespace="perdelt", container="datagenerator"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-loading-monetdb-1-1793810696-1-.+", namespace="perdelt", container="datagenerator"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
monetdb-1-1-1-1               : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-loading-monetdb-1-1793810696-1-.+", namespace="perdelt", container="sensor"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-loading-monetdb-1-1793810696-1-.+", namespace="perdelt", container="sensor"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
monetdb-1-1-1-1               : WARNING metric missing for loading: CPU Throttling Rate [s/s]
monetdb-1-1-1-1               : WARNING metric missing for loading: CPU Throttled Time [s]
monetdb-1-1-1-1               : WARNING metric missing for datagenerator: CPU Throttling Rate [s/s]
monetdb-1-1-1-1               : WARNING metric missing for datagenerator: CPU Utilization [CPUs]
monetdb-1-1-1-1               : WARNING metric missing for datagenerator: CPU Throttled Time [s]
monetdb-1-1-1-1               : WARNING metric missing for datagenerator: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
monetdb-1-1-1-1               : WARNING metric missing for datagenerator: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
monetdb-1-1-1-1               : WARNING metric missing for loader: CPU Throttling Rate [s/s]
monetdb-1-1-1-1               : WARNING metric missing for loader: CPU Throttled Time [s]
Experiment                    : fetched 3 metric sets in 4s (3 at once, 0 repeated, 0 follow-up actions; 5 kubectl calls 9.5s, 0 API requests 0.0s)
Loop pass                     : took 10.7s (10 kubectl calls 12.2s, 50 API requests 3.7s)
- waiting 30s -               : done
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
monetdb-1-1-1-1               : wrote benchmarking_timespans to /data/benchmarks/1793810696/monetdb-1-1-1-1.config
monetdb-1-1-1-1               : showing benchmarker times
monetdb-1-1-1-1               : benchmarker timespan job from 1793812922 to 1793812960
monetdb-1-1-1-1               : benchmarker timespan pods from 1793812932 to 1793812936
monetdb-1-1-1-1               : benchmarker timespan (start to end single container [s]) = 4
monetdb-1-1-1-1               : benchmarker times (start/end per pod and container) = [(1793812932, 1793812936)]
monetdb-1-1-1-1               : found and updated times {'benchmarker': [(1793812932, 1793812936)]}
monetdb-1-1-1-1               : needs monitoring (common metrics) for deployment sut
monetdb-1-1-1-1               : collecting execution metrics of SUT at connection monetdb-1-1-1-1
monetdb-1-1-1-1               : collecting metrics of benchmarker at connection monetdb-1-1-1-1
monetdb-1-1-1-1               : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)monetdb-1-1793810696(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)monetdb-1-1793810696(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
monetdb-1-1-1-1               : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-monetdb-1-1793810696-1-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-monetdb-1-1793810696-1-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: CPU Utilization [CPUs]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: Memory Usage, Working Set [MiB]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: Memory Usage incl. Page Cache [MiB]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: CPU Utilization Time [s]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: CPU User Time [s]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: CPU System Time [s]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: CPU Throttled Time [s]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: Network Rx Total [MiB]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: Network Tx Total [MiB]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
monetdb-1-1-1-1               : WARNING metric missing for benchmarker: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
monetdb-1-1-1-1               : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
monetdb-1-1-1-1               : WARNING metric missing for benchmarking: CPU Throttled Time [s]
Experiment                    : fetched 2 metric sets in 4s (2 at once, 0 repeated, 0 follow-up actions; 4 kubectl calls 6.0s, 0 API requests 0.0s)
Loop pass                     : took 9.1s (9 kubectl calls 9.8s, 31 API requests 1.6s)
MonetDB-1                     : can be stopped
MonetDB-1                     : had 0 restarts at worker bexhoma-sut-monetdb-1-1793810696-677b54c8d4-kh67x
ClickHouse-1                  : has to wait - 1 running and 0 pending pods: max is 1 pods per cluster
Loop pass                     : took 3.2s (3 kubectl calls 1.5s, 38 API requests 1.6s)
- waiting 30s -               : done
ClickHouse-1                  : will start now
ClickHouse-1                  : deployments ['sut']
ClickHouse-1                  : stateful sets []
ClickHouse-1                  : pvcs ['sut']
ClickHouse-1                  : name of SUT pods = bexhoma-sut-clickhouse-1-1793810696
ClickHouse-1                  : name of SUT service = bexhoma-sut-clickhouse-1-1793810696
Loop pass                     : took 1.4s (1 kubectl calls 0.6s, 15 API requests 0.6s)
- waiting 30s -               : done
ClickHouse-1                  : is not loaded yet
ClickHouse-1                  : will start loading but not before 2026-11-04 17:24:52 (that is in 60 secs)
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
ClickHouse-1                  : is not loaded yet
ClickHouse-1                  : will start loading but not before 2026-11-04 17:24:52
Loop pass                     : took 1.4s (0 kubectl calls 0.0s, 19 API requests 1.1s)
- waiting 30s -               : done
ClickHouse-1                  : is not loaded yet
ClickHouse-1                  : load durability relaxed, scripts []
ClickHouse-1                  : connect to pod bexhoma-sut-clickhouse-1-1793810696-576f968c5c-jqqlr to load scripts
ClickHouse-1                  : start asynch loading scripts of type schema
ClickHouse-1                  : waits for the Schema scripts (schema=True) before starting the loading jobs
ClickHouse-1                  : Schema scripts done after 2s
ClickHouse-1                  : is loading
Loop pass                     : took 8.0s (5 kubectl calls 3.3s, 39 API requests 2.7s)
- waiting 30s -               : done
ClickHouse-1                  : is loading
Loop pass                     : took 2.2s (0 kubectl calls 0.0s, 40 API requests 1.9s)
- waiting 30s -               : done
ClickHouse-1                  : is loading
Loop pass                     : took 1.6s (0 kubectl calls 0.0s, 40 API requests 1.7s)
- waiting 30s -               : done
ClickHouse-1                  : showing loader times (ssb-loader)
ClickHouse-1                  : generator times (start/end per pod and container) [(1793813128, 1793813137), (1793813119, 1793813138), (1793813137, 1793813137), (1793813131, 1793813137), (1793813124, 1793813138), (1793813135, 1793813137), (1793813114, 1793813137), (1793813122, 1793813137)]
ClickHouse-1                  : loader times (start/end per pod and container) [(1793813147, 1793813155), (1793813147, 1793813156), (1793813146, 1793813154), (1793813146, 1793813155), (1793813147, 1793813156), (1793813147, 1793813155), (1793813147, 1793813159), (1793813146, 1793813155)]
ClickHouse-1                  : total times (start/end per pod and container) [(1793813128, 1793813137), (1793813119, 1793813138), (1793813137, 1793813137), (1793813131, 1793813137), (1793813124, 1793813138), (1793813135, 1793813137), (1793813114, 1793813137), (1793813122, 1793813137), (1793813147, 1793813155), (1793813147, 1793813156), (1793813146, 1793813154), (1793813146, 1793813155), (1793813147, 1793813156), (1793813147, 1793813155), (1793813147, 1793813159), (1793813146, 1793813155)]
ClickHouse-1                  : generator timespan (first to last [s]) = 24
ClickHouse-1                  : loader timespan (first to last [s]) = 13
ClickHouse-1                  : total timespan (first to last [s]) = 45
ClickHouse-1                  : loading scripts not in folder, skipped: initindexes-ssb.sql, initconstraints-ssb.sql, initstatistics-ssb.sql
ClickHouse-1                  : connect to pod bexhoma-sut-clickhouse-1-1793810696-576f968c5c-jqqlr to load scripts
ClickHouse-1                  : start asynch loading scripts of type index
ClickHouse-1                  : is loading
Loop pass                     : took 23.2s (29 kubectl calls 15.2s, 68 API requests 3.0s)
- waiting 30s -               : done
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-1-1-ClickHouse-1-1793810696 initialized to 1.
ClickHouse-1                  : benchmarks done 0 of 1. This will be client 1
clickhouse-1-1-1-1            : start benchmarking (benchmark_run=1)
clickhouse-1-1-1-1            : needs monitoring (common metrics) for deployment sut
ClickHouse-1                  : benchmarking results in folder C:\data\benchmarks/1793810696
ClickHouse-1                  : submitted benchmarker job in 4.8s (3 kubectl calls 1.8s, 23 API requests 2.9s)
clickhouse-1-1-1-1            : needs monitoring (common metrics) for deployment sut
clickhouse-1-1-1-1            : collecting loading metrics of SUT at connection clickhouse-1-1-1-1
clickhouse-1-1-1-1            : collecting metrics of data generator at connection clickhouse-1-1-1-1
clickhouse-1-1-1-1            : collecting metrics of data injector at connection clickhouse-1-1-1-1
clickhouse-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)clickhouse-1-1793810696(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)clickhouse-1-1793810696(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
clickhouse-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-loading-clickhouse-1-1793810696-1-.+", namespace="perdelt", container="datagenerator"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-loading-clickhouse-1-1793810696-1-.+", namespace="perdelt", container="datagenerator"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
clickhouse-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-loading-clickhouse-1-1793810696-1-.+", namespace="perdelt", container="sensor"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-loading-clickhouse-1-1793810696-1-.+", namespace="perdelt", container="sensor"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: Memory Usage, Working Set [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: CPU Utilization [CPUs]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: Memory Usage incl. Page Cache [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: CPU Throttling Rate [s/s]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: CPU Utilization Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: CPU User Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: CPU Throttled Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: CPU System Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for datagenerator: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for loading: CPU Throttling Rate [s/s]
clickhouse-1-1-1-1            : WARNING metric missing for loading: CPU Throttled Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for loader: CPU Utilization [CPUs]
clickhouse-1-1-1-1            : WARNING metric missing for loader: CPU Throttling Rate [s/s]
clickhouse-1-1-1-1            : WARNING metric missing for loader: Memory Usage, Working Set [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for loader: Memory Usage incl. Page Cache [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for loader: CPU Throttled Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for loader: CPU Utilization Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for loader: CPU User Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for loader: CPU System Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for loader: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for loader: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
Experiment                    : fetched 3 metric sets in 5s (3 at once, 0 repeated, 0 follow-up actions; 5 kubectl calls 11.2s, 0 API requests 0.0s)
Loop pass                     : took 12.1s (10 kubectl calls 13.9s, 49 API requests 4.6s)
- waiting 30s -               : done
clickhouse-1-1-1-1            : wrote benchmarking_timespans to /data/benchmarks/1793810696/clickhouse-1-1-1-1.config
clickhouse-1-1-1-1            : showing benchmarker times
clickhouse-1-1-1-1            : benchmarker timespan job from 1793813255 to 1793813294
clickhouse-1-1-1-1            : benchmarker timespan pods from 1793813261 to 1793813265
clickhouse-1-1-1-1            : benchmarker timespan (start to end single container [s]) = 4
clickhouse-1-1-1-1            : benchmarker times (start/end per pod and container) = [(1793813261, 1793813265)]
clickhouse-1-1-1-1            : found and updated times {'benchmarker': [(1793813261, 1793813265)]}
clickhouse-1-1-1-1            : needs monitoring (common metrics) for deployment sut
clickhouse-1-1-1-1            : collecting execution metrics of SUT at connection clickhouse-1-1-1-1
clickhouse-1-1-1-1            : collecting metrics of benchmarker at connection clickhouse-1-1-1-1
clickhouse-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)clickhouse-1-1793810696(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)clickhouse-1-1793810696(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
clickhouse-1-1-1-1            : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-clickhouse-1-1793810696-1-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-clickhouse-1-1793810696-1-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
clickhouse-1-1-1-1            : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarking: CPU Throttled Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: Memory Usage incl. Page Cache [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: CPU Utilization [CPUs]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: Memory Usage, Working Set [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: CPU Throttled Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: CPU Utilization Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: CPU User Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: CPU System Time [s]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: Filesystem Read Total, Largest Device (RAID Counted Once) [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: Network Rx Total [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: Network Tx Total [MiB]
clickhouse-1-1-1-1            : WARNING metric missing for benchmarker: Filesystem Write Total, Largest Device (RAID Counted Once) [MiB]
Experiment                    : fetched 2 metric sets in 4s (2 at once, 0 repeated, 0 follow-up actions; 4 kubectl calls 6.2s, 0 API requests 0.0s)
Loop pass                     : took 8.5s (9 kubectl calls 8.9s, 30 API requests 1.8s)
ClickHouse-1                  : can be stopped
ClickHouse-1                  : had 0 restarts at worker bexhoma-sut-clickhouse-1-1793810696-576f968c5c-jqqlr
Loop pass                     : took 3.6s (3 kubectl calls 1.4s, 37 API requests 2.0s)
Experiment                    : ends at 2026-11-04 18:28:23.649252 (36496.7211002) - 2606.47s total
Experiment                    : join results...done!
Experiment                    : build evaluation cube...done!
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
SSB Queries SF=10
* Type: ssb
* Duration: 2607s 
* Code: 1793810696
* This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; the specification's text and SQL disagree there).
* This experiment compares run time and resource consumption of SSB queries in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=10) data is loaded and benchmark is executed.
  * Queries use the constants of the specification (-xqv spec).
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL', 'MonetDB', 'ClickHouse'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 1.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:964218
  * datadisk:6809
  * volume_size:1.8T
  * volume_used:942G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810696
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:972295
  * datadisk:14955
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810696
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:865535
  * datadisk:15059
  * volume_size:1.8T
  * volume_used:846G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810696

### Init Scripts Not in Folder
* ClickHouse-1: skipped initconstraints-ssb.sql, initindexes-ssb.sql, initstatistics-ssb.sql

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1793810696-576f968c5c-jqqlr: 0
* bexhoma-sut-monetdb-1-1793810696-677b54c8d4-kh67x: 0
* bexhoma-sut-postgresql-1-1793810696-867c6c8b44-69g49: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |   10 |       47.00 |           1.00 |           24.00 |         13.00 |            1.00 |              8 |           0 |             | None           |             0 | False         |              765.96 | False               |
| MonetDB-1-1    |                1 |   10 |      266.00 |           2.00 |           20.00 |        105.00 |          126.00 |              8 |           0 |             | None           |             0 | False         |              135.34 | False               |
| PostgreSQL-1-1 |                1 |   10 |      153.00 |           3.00 |           13.00 |         42.00 |           85.00 |              8 |           0 |             | None           |             0 | False         |              235.29 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               13 |                  13 |          4 |            0.06 |           593051.00 |         117000.00 |          -1 | clickhouse-1-1-1-1-1 |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 10.00 |               13 |                  13 |          4 |            0.13 |           277382.24 |         117000.00 |          -1 | monetdb-1-1-1-1-1    |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               13 |                  13 |         13 |            0.83 |            43159.87 |          36000.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               13 |                  13 |          4 |            0.06 |           593051.00 |         117000.00 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 10.00 |               13 |                  13 |          4 |            0.13 |           277382.24 |         117000.00 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               13 |                  13 |         13 |            0.83 |            43159.87 |          36000.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)   | Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)   | Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)   | Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)   | Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)   | Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)   | Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)   | Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)   | Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)   | Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)   | Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)   | Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)   | Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)   | complete   |
|:-----------------|-------:|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| monetdb-1-1-1    |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |
| postgresql-1-1-1 |      1 | 1/1                                                                      | 1/1                                                                       | 1/1                                                                      | 1/1                                                                                     | 1/1                                                                                | 1/1                                                                  | 1/1                                                                                 | 1/1                                                                               | 1/1                                                                              | 1/1                                                                                  | 1/1                                                                                      | 1/1                                                                           | 1/1                                                                                  | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                                                                |   clickhouse-1-1-1-1-1 |   monetdb-1-1-1-1-1 |   postgresql-1-1-1-1-1 |
|:---------------------------------------------------------------------------------------|-----------------------:|--------------------:|-----------------------:|
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                 143.65 |               82.76 |                 710.73 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  35.55 |               53.11 |                 644.03 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                  38.50 |               51.39 |                 209.38 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                  55.94 |              125.83 |                1570.77 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  67.61 |              199.99 |                1144.23 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                  47.32 |              147.69 |                 185.99 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                  74.37 |              162.37 |                1208.70 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                  49.60 |              117.57 |                1070.28 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  40.13 |              151.32 |                 939.53 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  45.81 |              117.52 |                1093.56 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                 111.02 |              218.64 |                1371.33 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                  84.29 |              254.77 |                1298.70 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                  68.05 |              186.75 |                1247.43 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 |        63.45 |      1.37 |           7.41 |                  9.27 |
| monetdb-1-1-1-1    |       515.09 |      4.56 |          13.69 |                 14.15 |
| postgresql-1-1-1-1 |       285.66 |      3.03 |           2.72 |                 12.07 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-1-1-1    | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-1-1-1    | 92.04        |      1.20 |           0.00 |                  0.74 |
| postgresql-1-1-1-1 | 56.97        |      1.76 |           0.00 |                  0.74 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.14 |           0.67 |                  7.32 |
| monetdb-1-1-1-1    | n/a          |      1.03 |          13.69 |                 14.14 |
| postgresql-1-1-1-1 | n/a          |      0.27 |           1.02 |                 10.72 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| clickhouse-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-1-1-1    | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Rx Total [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhouse-1-1-1-1 (bexhoma-metrics-clickhouse-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Rx Total [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
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
```

</details>

The section `### Monitoring` lists CPU and memory per phase and component for each DBMS.
See [Monitoring](Monitoring.md) for the metrics and for the tests that mark expected gaps.


## Reset Scripts

With `-ar` a reset runs before each benchmarking round: `VACUUM ANALYZE`, `CHECKPOINT` and a
statistics reset for PostgreSQL and PgDuckDB (Citus: also on every worker), `ANALYZE` for MonetDB,
`ANALYZE TABLE`, a flush of the dirty pages and `FLUSH STATUS` for MySQL and MariaDB, `sync` for
ClickHouse. ClickHouseCluster first sends the rows still held by the Distributed tables, syncs
the replicated dimensions, then runs `sync` on every shard.

## Profiling

```bash
bexhoma ssb -dbms PostgreSQL MonetDB ClickHouse -sf 1 -nlp 8 -xdt -ms 10 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no profiling
```

Runs count, count distinct, minimum and maximum of the key and date columns of each table
instead of the benchmark queries. With `-xsv flat` it profiles `lineorder_flat`.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ssb_profiling_summary.md" target="_blank" rel="noopener">docs_ssb_profiling.log</a></summary>

```markdown
## Show Summary

### Workload
SSB Data Profiling SF=1
* Type: ssb
* Duration: 554s 
* Code: 1792957689
* Row count, count distinct, minimum and maximum of the key and date columns of each table.
* This experiment compares imported SSB data sets in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.9.
  * Experiment is limited to DBMS ['PostgreSQL', 'MonetDB', 'ClickHouse'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:677714
  * datadisk:500
  * volume_size:1.8T
  * volume_used:662G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792957689
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:677714
  * datadisk:862
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792957689
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:677885
  * datadisk:1354
  * volume_size:1.8T
  * volume_used:662G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792957689

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1792957689-56c7bfbb8d-4hsw6: 0
* bexhoma-sut-monetdb-1-1792957689-5f64445dbf-tj9dm: 0
* bexhoma-sut-postgresql-1-1792957689-9cb9f866c-fvlrc: 0

### Workflow

#### Actual

* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: ssb (1 pods)
* DBMS ClickHouse-1 - Experiment 1 Client 1: ssb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       39.00 |           2.00 |           23.00 |          3.00 |            3.00 |              8 |           0 |             | None           |             0 | False         |               92.31 | False               |
| MonetDB-1-1    |                1 |    1 |       52.00 |           2.00 |           21.00 |         17.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |               69.23 | False               |
| PostgreSQL-1-1 |                1 |    1 |      114.00 |           4.00 |           78.00 |          3.00 |            6.00 |              8 |           0 |             | None           |             0 | False         |               31.58 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          2 |            0.03 |           147661.02 |          18000.00 |          -1 | clickhouse-1-1-1-1-1 |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          3 |            0.03 |           135839.85 |          12000.00 |          -1 | monetdb-1-1-1-1-1    |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          7 |            0.13 |            28299.56 |           5142.86 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          2 |            0.03 |           147661.02 |          18000.00 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          3 |            0.03 |           135839.85 |          12000.00 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          7 |            0.13 |            28299.56 |           5142.86 |          -1 |

#### Query Completion per Phase

| phase            |   pods | stats about customer.c_custkey   | stats about supplier.s_suppkey   | stats about part.p_partkey   | stats about dates.d_datekey   | stats about lineorder.lo_orderkey   | stats about lineorder.lo_custkey   | stats about lineorder.lo_partkey   | stats about lineorder.lo_suppkey   | stats about lineorder.lo_orderdate   | stats about lineorder.lo_commitdate   | complete   |
|:-----------------|-------:|:---------------------------------|:---------------------------------|:-----------------------------|:------------------------------|:------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------|:-------------------------------------|:--------------------------------------|:-----------|
| clickhouse-1-1-1 |      1 | 1/1                              | 1/1                              | 1/1                          | 1/1                           | 1/1                                 | 1/1                                | 1/1                                | 1/1                                | 1/1                                  | 1/1                                   | yes        |
| monetdb-1-1-1    |      1 | 1/1                              | 1/1                              | 1/1                          | 1/1                           | 1/1                                 | 1/1                                | 1/1                                | 1/1                                | 1/1                                  | 1/1                                   | yes        |
| postgresql-1-1-1 |      1 | 1/1                              | 1/1                              | 1/1                          | 1/1                           | 1/1                                 | 1/1                                | 1/1                                | 1/1                                | 1/1                                  | 1/1                                   | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                             |   clickhouse-1-1-1-1-1 |   monetdb-1-1-1-1-1 |   postgresql-1-1-1-1-1 |
|:------------------------------------|-----------------------:|--------------------:|-----------------------:|
| stats about customer.c_custkey      |                 212.32 |               19.26 |                  48.94 |
| stats about supplier.s_suppkey      |                   5.30 |                4.09 |                   2.16 |
| stats about part.p_partkey          |                  12.72 |                3.08 |                  23.55 |
| stats about dates.d_datekey         |                  26.92 |                2.42 |                   1.98 |
| stats about lineorder.lo_orderkey   |                 563.79 |              134.94 |                 801.90 |
| stats about lineorder.lo_custkey    |                  14.17 |               63.04 |                 750.65 |
| stats about lineorder.lo_partkey    |                  24.93 |              110.09 |                 967.38 |
| stats about lineorder.lo_suppkey    |                  10.25 |               67.73 |                 752.66 |
| stats about lineorder.lo_orderdate  |                   9.28 |               67.22 |                 691.79 |
| stats about lineorder.lo_commitdate |                  10.17 |               68.40 |                 739.95 |

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
```

</details>

## Adjust Parameters

### Command line

| Option | Meaning |
|---|---|
| `-xsv normal\|flat` | schema variant |
| `-xqv spec\|random` | query variant |
| `-xdim replicated\|distributed` | placement of the dimensions on ClickHouseCluster and Citus |
| `-nw <n>` | number of shards (ClickHouseCluster) or workers (Citus) |
| `-xdfe` | PgDuckDB: run the queries in DuckDB's engine |
| `-xii`, `-xic`, `-xis` | indexes, primary and foreign keys (star schema only), statistics after loading |
| `-xrcp` | with `-xqv random`: new parameters per stream |
| `-xshq` | shuffle the query order per stream |
| `-xaq 1,4,7` | run only these queries (1-based: Q1.1 = 1, Q4.3 = 13) |
| `-xlit <table>` | load only this table |
| `-xdt` | measure the data transfer volume per query |
| `-xve`, `-xse` | print or store EXPLAIN output per query |

Multi-tenancy (`-mtn`) is not supported for SSB yet.

### Files

* Query files and DDL scripts: [`experiments/ssb/`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ssb)
* Images (generator and loaders): [`images/ssb/`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/ssb)
* Job templates: `k8s/jobtemplate-loading-ssb-<DBMS>.yml`
* Script lists: `volumes.ssb` in the cluster config
* Test script with all runs of this page: `scripts/test-docs-ssb.sh` (`.ps1`)
