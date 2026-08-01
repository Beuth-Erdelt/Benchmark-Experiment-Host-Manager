## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 785s 
* Code: 1785542395
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * Query selection is limited to Q1, Q9, Q14, Q18.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Experiment uses bexhoma version 0.10.9.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 150Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:793083
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785542395

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785542395-85c966d546-9tw4h: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   10 |      499.00 |           1.00 |           16.00 |         77.00 |          400.00 |              8 |           0 |             |                |             0 | False         |               72.14 |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |                4 |         50 |            9.39 |             3842.28 |           2880.00 |           0 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |                4 |         50 |            9.39 |             3842.28 |           2880.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                |   postgresql-1-1-1-1-1 |
|:---------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)      |               10988.66 |
| Product Type Profit Measure (TPC-H Q9) |               10553.28 |
| Promotion Effect Query (TPC-H Q14)     |                2789.09 |
| Large Volume Customer (TPC-H Q18)      |               23826.51 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
