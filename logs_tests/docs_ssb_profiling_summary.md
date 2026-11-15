## Show Summary

### Workload
SSB Data Profiling SF=1
* Type: ssb
* Duration: 492s 
* Code: 1794598670
* Row count, count distinct, minimum and maximum of the key and date columns of each table.
* This experiment compares imported SSB data sets in different DBMS.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1.1 - Q4.3.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* clickhouse-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1149076
  * datadisk:499
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794598670
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1149086
  * datadisk:862
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794598670
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1149086
  * datadisk:1354
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794598670

### Ingestion
* ClickHouse-1: 12 of 12 units ok
* MonetDB-1: 12 of 12 units ok
* PostgreSQL-1: 12 of 12 units ok

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1794598670-6d6c6c4db8-h4rjj: 0
* bexhoma-sut-monetdb-1-1794598670-68f87755dc-6crm7: 0
* bexhoma-sut-postgresql-1-1794598670-dc65dcd48-w5m8k: 0

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

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouse-1-1 |                1 |    1 |       66.00 |           3.00 |           40.00 |          3.00 |            2.00 |              8 |         0 |             | None           |             0 | False         |               54.55 | False               |
| MonetDB-1-1    |                1 |    1 |       60.00 |           3.00 |           34.00 |         10.00 |            2.00 |              8 |         0 |             | None           |             0 | False         |               60.00 | False               |
| PostgreSQL-1-1 |                1 |    1 |       59.00 |           4.00 |           35.00 |          4.00 |            7.00 |              8 |         0 |             | None           |             0 | False         |               61.02 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1-1-1 | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               10 |                  10 |          2 |            0.03 |           142902.21 |          18000.00 |          -1 |
| monetdb-1-1-1-1-1    | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |       1 | 1.00 |               10 |                  10 |          3 |            0.04 |            90302.01 |          12000.00 |          -1 |
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               10 |                  10 |          8 |            0.19 |            19704.05 |           4500.00 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          2 |            0.03 |           142902.21 |          18000.00 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          3 |            0.04 |            90302.01 |          12000.00 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               10 |                  10 |          8 |            0.19 |            19704.05 |           4500.00 |          -1 |

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
| stats about customer.c_custkey      |                 227.33 |               34.12 |                  57.94 |
| stats about supplier.s_suppkey      |                   7.94 |                3.78 |                   3.59 |
| stats about part.p_partkey          |                  21.86 |                4.91 |                  59.32 |
| stats about dates.d_datekey         |                  41.21 |                2.63 |                   2.17 |
| stats about lineorder.lo_orderkey   |                  36.53 |              348.78 |                1383.64 |
| stats about lineorder.lo_custkey    |                  17.87 |              190.40 |                 931.47 |
| stats about lineorder.lo_partkey    |                  37.10 |              275.46 |                1174.03 |
| stats about lineorder.lo_suppkey    |                  15.28 |               78.17 |                1033.42 |
| stats about lineorder.lo_orderdate  |                  10.34 |               66.27 |                1284.80 |
| stats about lineorder.lo_commitdate |                  16.54 |               64.42 |                 770.34 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
