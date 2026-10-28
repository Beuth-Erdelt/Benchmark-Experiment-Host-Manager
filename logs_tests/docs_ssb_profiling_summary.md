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
