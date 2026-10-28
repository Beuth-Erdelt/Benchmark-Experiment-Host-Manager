# Benchmark: SSB

The Star Schema Benchmark (SSB) is a data warehouse benchmark derived from TPC-H: one fact
table `lineorder` (TPC-H's `lineitem` and `orders` combined) and four dimensions `customer`,
`supplier`, `part` and `dates`, queried by 13 queries in four flights. Bexhoma runs it with the
DBMSBenchmarker, like TPC-H and TPC-DS, on PostgreSQL, MonetDB and ClickHouse (the default
set), and on ClickHouseCluster, Citus, PgDuckDB, MySQL and MariaDB.

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

MySQL and MariaDB load with `LOAD DATA LOCAL INFILE`. Their tables get the primary keys in the
schema script (InnoDB stores a table in key order, so a key added after the load rebuilds the
table); `-xic` adds the foreign keys. The flat queries have a MySQL variant without
`CAST(... AS INTEGER)`, which MySQL does not know:

```bash
bexhoma ssb -dbms MySQL -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
bexhoma ssb -dbms MariaDB -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

## Multi-Node DBMS

ClickHouseCluster (a coordinator and `-nw` shards) and Citus (a coordinator and `-nw` workers)
spread `lineorder` (and `lineorder_flat`) over the nodes by `lo_orderkey`. The loaders write to the
coordinator, which sends the rows to the nodes. For the dimensions there are two placements
(`-xdim`, star schema only):

| `-xdim` | ClickHouseCluster | Citus | Joins |
|---|---|---|---|
| `replicated` (default) | `ReplicatedMergeTree` on every node: the coordinator and all shards are replicas of one table, Keeper (in the coordinator) copies the parts | reference tables | run on every shard against its local copy |
| `distributed` | `Distributed` tables over `<name>_local` on the shards, as for TPC-H | distributed tables | ClickHouse sends the dimension to all shards per query (`GLOBAL`), Citus runs a repartition join |

```bash
bexhoma ssb -dbms ClickHouseCluster -nw 3 -sf 1 -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
bexhoma ssb -dbms ClickHouseCluster -nw 3 -xdim distributed -sf 1 -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
bexhoma ssb -dbms Citus -nw 3 -sf 1 -xii -xic -xis -nlp 8 -xdt -ms 1 -t 1200 -tr -lr 64Gi -rr 64Gi -rss 50Gi -ks no run
```

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
