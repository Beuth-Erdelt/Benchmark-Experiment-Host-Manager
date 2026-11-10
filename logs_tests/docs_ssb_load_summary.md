## Show Summary

### Workload
SSB Data Loading SF=1
* Type: ssb
* Duration: 318s 
* Code: 1794006703
* Load data and do not run a benchmark.
* This imports SSB data sets.
  * Schema is the star schema (-xsv normal).
  * SSB (SF=1) data is loaded.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:873693
  * datadisk:1581
  * volume_size:1.8T
  * volume_used:854G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794006703

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794006703-556f8dbfd6-btszb: 0

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       60.00 |           5.00 |           25.00 |          4.00 |           19.00 |              8 |           0 |             | None           |             0 | False         |               60.00 | False               |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
794005050, 1794005053), (1794005049, 1794005052), (1794005049, 1794005052), (1794005050, 1794005052), (1794005050, 1794005053), (1794005050, 1794005052)]
ClickHouse-1                  : generator timespan (first to last [s]) = 38
ClickHouse-1                  : loader timespan (first to last [s]) = 4
ClickHouse-1                  : total timespan (first to last [s]) = 57
ClickHouse-1                  : loading scripts not in folder, skipped: initindexes-ssb-flat.sql, initstatistics-ssb-flat.sql
ClickHouse-1                  : connect to pod bexhoma-sut-clickhouse-1-1794004854-8594c68996-nd2tp to load scripts
ClickHouse-1                  : start asynch loading scripts of type index
ClickHouse-1                  : is loading
Loop pass                     : took 85.2s (64 kubectl calls 76.8s, 145 API requests 5.9s)
- waiting 30s -               : done
PostgreSQL-1                  : showing loader times (ssb-loader)
PostgreSQL-1                  : generator times (start/end per pod and container) [(1794005097, 1794005113), (1794005094, 1794005113), (1794005089, 1794005114), (1794005113, 1794005113), (1794005103, 1794005114), (1794005109, 1794005113), (1794005107, 1794005114), (1794005101, 1794005113)]
PostgreSQL-1                  : loader times (start/end per pod and container) [(1794005126, 1794005139), (1794005126, 1794005139), (1794005127, 1794005139), (1794005126, 1794005139), (1794005127, 1794005139), (1794005126, 1794005138), (1794005126, 1794005139), (1794005127, 1794005139)]
PostgreSQL-1                  : total times (start/end per pod and container) [(1794005097, 1794005113), (1794005094, 1794005113), (1794005089, 1794005114), (1794005113, 1794005113), (1794005103, 1794005114), (1794005109, 1794005113), (1794005107, 1794005114), (1794005101, 1794005113), (1794005126, 1794005139), (1794005126, 1794005139), (1794005127, 1794005139), (1794005126, 1794005139), (1794005127, 1794005139), (1794005126, 1794005138), (1794005126, 1794005139), (1794005127, 1794005139)]
PostgreSQL-1                  : generator timespan (first to last [s]) = 25
PostgreSQL-1                  : loader timespan (first to last [s]) = 13
PostgreSQL-1                  : total timespan (first to last [s]) = 50
PostgreSQL-1                  : connect to pod bexhoma-sut-postgresql-1-1794004854-697cb777bb-sjnmd to load scripts
PostgreSQL-1                  : start asynch loading scripts of type index
PostgreSQL-1                  : is loading
Experiment                    : Reset experiment counter. This is first run of client number 1.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-1-1-MonetDB-1-1794004854 initialized to 1.
MonetDB-1                     : benchmarks done 0 of 1. This will be client 1
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-1-1-ClickHouse-1-1794004854 initialized to 1.
ClickHouse-1                  : benchmarks done 0 of 1. This will be client 1
monetdb-1-1-1-1               : start benchmarking (benchmark_run=1)
clickhouse-1-1-1-1            : start benchmarking (benchmark_run=1)
MonetDB-1                     : benchmarking results in folder C:\data\benchmarks/1794004854
ClickHouse-1                  : benchmarking results in folder C:\data\benchmarks/1794004854
MonetDB-1                     : submitted benchmarker job in 13.8s (4 kubectl calls 4.8s, 24 API requests 5.9s)
ClickHouse-1                  : submitted benchmarker job in 16.6s (3 kubectl calls 4.0s, 23 API requests 6.0s)
Experiment                    : submitted 2 benchmark rounds in 16.6s (2 at once; 7 kubectl calls 8.8s, 49 API requests 12.0s)
Loop pass                     : took 65.0s (32 kubectl calls 39.5s, 131 API requests 16.3s)
- waiting 30s -               : done
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-1-1-PostgreSQL-1-1794004854 initialized to 1.
PostgreSQL-1                  : benchmarks done 0 of 1. This will be client 1
postgresql-1-1-1-1            : start benchmarking (benchmark_run=1)
PostgreSQL-1                  : benchmarking results in folder C:\data\benchmarks/1794004854
PostgreSQL-1                  : submitted benchmarker job in 6.5s (3 kubectl calls 3.8s, 23 API requests 2.7s)
monetdb-1-1-1-1               : wrote benchmarking_timespans to /data/benchmarks/1794004854/monetdb-1-1-1-1.config
monetdb-1-1-1-1               : showing benchmarker times
monetdb-1-1-1-1               : benchmarker timespan job from 1794005333 to 1794005380
monetdb-1-1-1-1               : benchmarker timespan pods from 1794005348 to 1794005351
monetdb-1-1-1-1               : benchmarker timespan (start to end single container [s]) = 3
monetdb-1-1-1-1               : benchmarker times (start/end per pod and container) = [(1794005348, 1794005351)]
monetdb-1-1-1-1               : found and updated times {'benchmarker': [(1794005348, 1794005351)]}
clickhouse-1-1-1-1            : wrote benchmarking_timespans to /data/benchmarks/1794004854/clickhouse-1-1-1-1.config
clickhouse-1-1-1-1            : showing benchmarker times
clickhouse-1-1-1-1            : benchmarker timespan job from 1794005336 to 1794005380
clickhouse-1-1-1-1            : benchmarker timespan pods from 1794005351 to 1794005353
clickhouse-1-1-1-1            : benchmarker timespan (start to end single container [s]) = 2
clickhouse-1-1-1-1            : benchmarker times (start/end per pod and container) = [(1794005351, 1794005353)]
clickhouse-1-1-1-1            : found and updated times {'benchmarker': [(1794005351, 1794005353)]}
Experiment                    : ended 2 benchmarker jobs in 3.0s (3 at once; 4 kubectl calls 4.9s, 24 API requests 1.1s)
Loop pass                     : took 14.7s (10 kubectl calls 12.3s, 83 API requests 5.2s)
PostgreSQL-1                  : has running benchmarks
MonetDB-1                     : can be stopped
MonetDB-1                     : had 0 restarts at worker bexhoma-sut-monetdb-1-1794004854-54c9bc6879-442kn
ClickHouse-1                  : can be stopped
ClickHouse-1                  : had 0 restarts at worker bexhoma-sut-clickhouse-1-1794004854-8594c68996-nd2tp
Loop pass                     : took 10.3s (6 kubectl calls 6.9s, 70 API requests 2.5s)
- waiting 30s -               : done
postgresql-1-1-1-1            : wrote benchmarking_timespans to /data/benchmarks/1794004854/postgresql-1-1-1-1.config
postgresql-1-1-1-1            : showing benchmarker times
postgresql-1-1-1-1            : benchmarker timespan job from 1794005376 to 1794005427
postgresql-1-1-1-1            : benchmarker timespan pods from 1794005386 to 1794005392
postgresql-1-1-1-1            : benchmarker timespan (start to end single container [s]) = 6
postgresql-1-1-1-1            : benchmarker times (start/end per pod and container) = [(1794005386, 1794005392)]
postgresql-1-1-1-1            : found and updated times {'benchmarker': [(1794005386, 1794005392)]}
Loop pass                     : took 6.4s (4 kubectl calls 4.8s, 30 API requests 1.1s)
PostgreSQL-1                  : can be stopped
PostgreSQL-1                  : had 0 restarts at worker bexhoma-sut-postgresql-1-1794004854-697cb777bb-sjnmd
Loop pass                     : took 5.8s (4 kubectl calls 4.7s, 35 API requests 1.1s)
Experiment                    : ends at 2026-11-06 23:50:36.482880 (228626.0479974) - 581.93s total
Experiment                    : join results...done!
Experiment                    : build evaluation cube...done!
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
SSB Queries SF=1
* Type: ssb
* Duration: 582s 
* Code: 1794004854
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
  * Experiment uses bexhoma version 0.11.13.
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
  * disk:877471
  * datadisk:1613
  * volume_size:1.8T
  * volume_used:857G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794004854
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877471
  * datadisk:2153
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794004854
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:877679
  * datadisk:4470
  * volume_size:1.8T
  * volume_used:858G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794004854

### Init Scripts Not in Folder
* ClickHouse-1: skipped initindexes-ssb-flat.sql, initstatistics-ssb-flat.sql

### SUT Container Restarts
* bexhoma-sut-clickhouse-1-1794004854-8594c68996-nd2tp: 0
* bexhoma-sut-monetdb-1-1794004854-54c9bc6879-442kn: 0
* bexhoma-sut-postgresql-1-1794004854-697cb777bb-sjnmd: 0

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
| ClickHouse-1-1 |                1 |    1 |       62.00 |           3.00 |           38.00 |          4.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |               58.06 | False               |
| MonetDB-1-1    |                1 |    1 |       96.00 |           3.00 |           39.00 |         28.00 |           15.00 |              8 |           0 |             | None           |             0 | False         |               37.50 | False               |
| PostgreSQL-1-1 |                1 |    1 |       80.00 |           5.00 |           25.00 |         13.00 |           25.00 |              8 |           0 |             | None           |             0 | False         |               45.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| clickhouse-1-1-1-1-1 | ClickHouse-1    | clickhouse-1-1-1 | clickhouse-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          2 |            0.04 |           119059.33 |          23400.00 |          -1 | clickhouse-1-1-1-1-1 |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          3 |            0.03 |           158466.70 |          15600.00 |          -1 | monetdb-1-1-1-1-1    |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          6 |            0.07 |            53755.16 |           7800.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhouse-1-1-1 | clickhouse-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          2 |            0.04 |           119059.33 |          23400.00 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          3 |            0.03 |           158466.70 |          15600.00 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               13 |                  13 |          6 |            0.07 |            53755.16 |           7800.00 |          -1 |

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
| Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)                 |                  60.25 |               34.27 |                 695.03 |
| Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)                |                  10.49 |               11.52 |                  43.07 |
| Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)                 |                   8.94 |               13.61 |                  10.51 |
| Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)  |                  28.77 |               19.90 |                 173.89 |
| Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)       |                  26.04 |               18.32 |                  77.73 |
| Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)                     |                  21.15 |               18.69 |                  10.07 |
| Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)      |                  54.02 |               24.76 |                 405.57 |
| Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)        |                  30.44 |               23.87 |                  51.65 |
| Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)         |                  34.82 |               30.67 |                   8.47 |
| Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)     |                  15.07 |               21.38 |                   6.98 |
| Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1) |                  90.14 |               32.16 |                 277.94 |
| Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)            |                  47.48 |               31.93 |                 406.65 |
| Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)     |                  53.39 |               29.48 |                  90.92 |

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
