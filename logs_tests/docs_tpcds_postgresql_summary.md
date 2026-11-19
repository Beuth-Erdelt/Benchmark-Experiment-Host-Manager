## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 632s 
* Code: 1795120919
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834185
  * datadisk:5787
  * volume_size:1.8T
  * volume_used:815G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120919

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795120919-75ccbbbf57-7prvw: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       94.00 |           2.00 |            1.00 |         49.00 |           33.00 |              8 |         0 |             | None           |             0 | False         |               38.30 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        159 |            0.32 |            11635.11 |           2241.51 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        159 |            0.32 |            11635.11 |           2241.51 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  91.23 |
| TPC-DS Q2     |                 336.94 |
| TPC-DS Q3     |                 112.12 |
| TPC-DS Q4     |                5547.88 |
| TPC-DS Q5     |                 472.97 |
| TPC-DS Q6     |               50039.42 |
| TPC-DS Q7     |                 322.67 |
| TPC-DS Q8     |                  47.33 |
| TPC-DS Q9     |                1872.25 |
| TPC-DS Q10    |                 897.26 |
| TPC-DS Q11    |                3178.72 |
| TPC-DS Q12    |                 118.03 |
| TPC-DS Q13    |                 511.79 |
| TPC-DS Q14a+b |                2182.75 |
| TPC-DS Q15    |                 107.50 |
| TPC-DS Q16    |                 196.30 |
| TPC-DS Q17    |                 259.25 |
| TPC-DS Q18    |                 343.39 |
| TPC-DS Q19    |                 134.81 |
| TPC-DS Q20    |                  85.90 |
| TPC-DS Q21    |                 241.64 |
| TPC-DS Q22    |                2771.96 |
| TPC-DS Q23a+b |                3138.78 |
| TPC-DS Q24a+b |                 730.03 |
| TPC-DS Q25    |                 264.48 |
| TPC-DS Q26    |                 211.67 |
| TPC-DS Q27    |                 315.78 |
| TPC-DS Q28    |                1578.19 |
| TPC-DS Q29    |                 290.79 |
| TPC-DS Q30    |                7329.64 |
| TPC-DS Q31    |                1305.48 |
| TPC-DS Q32    |                 100.67 |
| TPC-DS Q33    |                 302.07 |
| TPC-DS Q34    |                  17.44 |
| TPC-DS Q35    |                 971.32 |
| TPC-DS Q36    |                 287.17 |
| TPC-DS Q37    |                 442.84 |
| TPC-DS Q38    |                 822.42 |
| TPC-DS Q39a+b |                2033.47 |
| TPC-DS Q40    |                 106.69 |
| TPC-DS Q41    |                 714.32 |
| TPC-DS Q42    |                  91.64 |
| TPC-DS Q43    |                  18.13 |
| TPC-DS Q44    |                   1.80 |
| TPC-DS Q45    |                  75.68 |
| TPC-DS Q46    |                  22.82 |
| TPC-DS Q47    |                1276.22 |
| TPC-DS Q48    |                 483.06 |
| TPC-DS Q49    |                 418.94 |
| TPC-DS Q50    |                 395.90 |
| TPC-DS Q51    |                 688.59 |
| TPC-DS Q52    |                  88.69 |
| TPC-DS Q53    |                 118.74 |
| TPC-DS Q54    |                  58.30 |
| TPC-DS Q55    |                  87.13 |
| TPC-DS Q56    |                 258.77 |
| TPC-DS Q57    |                 771.62 |
| TPC-DS Q58    |                 352.62 |
| TPC-DS Q59    |                 410.65 |
| TPC-DS Q60    |                 321.11 |
| TPC-DS Q61    |                 104.74 |
| TPC-DS Q62    |                  83.96 |
| TPC-DS Q63    |                 114.69 |
| TPC-DS Q64    |                 605.55 |
| TPC-DS Q65    |                 499.37 |
| TPC-DS Q66    |                 172.52 |
| TPC-DS Q67    |                2756.78 |
| TPC-DS Q68    |                  29.33 |
| TPC-DS Q69    |                 293.22 |
| TPC-DS Q70    |                 343.35 |
| TPC-DS Q71    |                 248.79 |
| TPC-DS Q72    |                 797.08 |
| TPC-DS Q73    |                  22.14 |
| TPC-DS Q74    |                 911.63 |
| TPC-DS Q75    |                 567.03 |
| TPC-DS Q76    |                 140.67 |
| TPC-DS Q77    |                 274.18 |
| TPC-DS Q78    |                1461.99 |
| TPC-DS Q79    |                 107.12 |
| TPC-DS Q80    |                 364.80 |
| TPC-DS Q81    |               32621.45 |
| TPC-DS Q82    |                 352.45 |
| TPC-DS Q83    |                  70.99 |
| TPC-DS Q84    |                  67.44 |
| TPC-DS Q85    |                 259.63 |
| TPC-DS Q86    |                 186.59 |
| TPC-DS Q87    |                 830.68 |
| TPC-DS Q88    |                1970.19 |
| TPC-DS Q89    |                 128.79 |
| TPC-DS Q90    |                 103.60 |
| TPC-DS Q91    |                 120.18 |
| TPC-DS Q92    |                  57.02 |
| TPC-DS Q93    |                 262.90 |
| TPC-DS Q94    |                 138.06 |
| TPC-DS Q95    |                2634.73 |
| TPC-DS Q96    |                  98.43 |
| TPC-DS Q97    |                 348.82 |
| TPC-DS Q98    |                 426.54 |
| TPC-DS Q99    |                 160.31 |

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
