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
