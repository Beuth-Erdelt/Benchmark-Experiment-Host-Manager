## Show Summary

### Workload
TPC-DS Queries SF=10
* Type: tpcds
* Duration: 7048s 
* Code: 1782595993
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 150Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:1081742745600
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-117-generic
  * node:cl-worker29
  * disk:660803
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782595993

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782595993-7677b5d699-zfm6g: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   10 |     1653.00 |           6.00 |            0.00 |        496.00 |         1142.00 |              8 |           0 |             | None           |             0 | False         |               21.78 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               96 |       5506 |            3.16 |            11477.20 |            627.68 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               96 |       5506 |            3.16 |            11477.20 |            627.68 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q2     |                2473.69 |
| TPC-DS Q3     |                1454.28 |
| TPC-DS Q4     |               98028.18 |
| TPC-DS Q5     |                5054.95 |
| TPC-DS Q7     |                2403.56 |
| TPC-DS Q8     |                1715.23 |
| TPC-DS Q9     |                7782.47 |
| TPC-DS Q10    |                2819.92 |
| TPC-DS Q11    |               58417.79 |
| TPC-DS Q12    |                 594.50 |
| TPC-DS Q13    |                3714.13 |
| TPC-DS Q14a+b |               23174.54 |
| TPC-DS Q15    |                1004.68 |
| TPC-DS Q16    |                2525.16 |
| TPC-DS Q17    |                3268.41 |
| TPC-DS Q18    |                2255.10 |
| TPC-DS Q19    |                2213.33 |
| TPC-DS Q20    |                1063.13 |
| TPC-DS Q21    |                2360.77 |
| TPC-DS Q22    |               48712.96 |
| TPC-DS Q23a+b |               63793.55 |
| TPC-DS Q24a+b |                6047.96 |
| TPC-DS Q25    |                3360.84 |
| TPC-DS Q26    |                1221.89 |
| TPC-DS Q27    |                2566.88 |
| TPC-DS Q28    |                6417.05 |
| TPC-DS Q29    |                3919.92 |
| TPC-DS Q31    |                7771.48 |
| TPC-DS Q32    |                 875.20 |
| TPC-DS Q33    |                4951.72 |
| TPC-DS Q34    |                 340.16 |
| TPC-DS Q35    |                3546.01 |
| TPC-DS Q36    |                 427.48 |
| TPC-DS Q37    |                2715.66 |
| TPC-DS Q38    |               11662.60 |
| TPC-DS Q39a+b |               40993.66 |
| TPC-DS Q40    |                 988.24 |
| TPC-DS Q41    |               61020.81 |
| TPC-DS Q42    |                1226.30 |
| TPC-DS Q43    |                2038.20 |
| TPC-DS Q44    |                   2.10 |
| TPC-DS Q45    |                 681.53 |
| TPC-DS Q46    |                 574.82 |
| TPC-DS Q47    |               11807.07 |
| TPC-DS Q48    |                3609.40 |
| TPC-DS Q49    |                4531.62 |
| TPC-DS Q50    |                7187.90 |
| TPC-DS Q51    |               13219.13 |
| TPC-DS Q52    |                1209.94 |
| TPC-DS Q53    |                1297.56 |
| TPC-DS Q54    |                1008.60 |
| TPC-DS Q55    |                1152.27 |
| TPC-DS Q56    |                4257.17 |
| TPC-DS Q57    |                8388.62 |
| TPC-DS Q58    |                4194.10 |
| TPC-DS Q59    |                3613.69 |
| TPC-DS Q60    |                4830.12 |
| TPC-DS Q61    |                1907.61 |
| TPC-DS Q62    |                 933.52 |
| TPC-DS Q63    |                1344.40 |
| TPC-DS Q64    |                7382.88 |
| TPC-DS Q65    |                8075.58 |
| TPC-DS Q66    |                4374.84 |
| TPC-DS Q67    |               40688.35 |
| TPC-DS Q68    |                 596.04 |
| TPC-DS Q69    |                2265.34 |
| TPC-DS Q70    |                4738.52 |
| TPC-DS Q71    |                4191.63 |
| TPC-DS Q72    |               14392.62 |
| TPC-DS Q73    |                 328.37 |
| TPC-DS Q74    |               12506.90 |
| TPC-DS Q75    |                8205.31 |
| TPC-DS Q76    |                2750.68 |
| TPC-DS Q77    |                3409.65 |
| TPC-DS Q78    |               13398.11 |
| TPC-DS Q79    |                1602.84 |
| TPC-DS Q80    |                5602.13 |
| TPC-DS Q81    |             1093594.34 |
| TPC-DS Q82    |                2769.49 |
| TPC-DS Q83    |                 630.68 |
| TPC-DS Q84    |                 134.30 |
| TPC-DS Q85    |                1106.60 |
| TPC-DS Q86    |                2264.56 |
| TPC-DS Q87    |               10954.12 |
| TPC-DS Q88    |                6770.17 |
| TPC-DS Q89    |                1605.55 |
| TPC-DS Q90    |                 714.22 |
| TPC-DS Q91    |                 334.94 |
| TPC-DS Q92    |                 354.22 |
| TPC-DS Q93    |                3284.99 |
| TPC-DS Q94    |                1465.73 |
| TPC-DS Q95    |               47447.73 |
| TPC-DS Q96    |                1050.60 |
| TPC-DS Q97    |                3918.92 |
| TPC-DS Q98    |                2262.77 |
| TPC-DS Q99    |                1458.33 |

### Errors (failed queries)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| PostgreSQL-1-1-1-1-1 |        1.00 |        0.00 |        0.00 |        0.00 |        0.00 |        1.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q1
  * PostgreSQL-1-1-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
* TPC-DS Q6
  * PostgreSQL-1-1-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
* TPC-DS Q30
  * PostgreSQL-1-1-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2568.70 |      4.41 |          19.59 |                 48.11 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       132.67 |      0.77 |           0.01 |                  2.82 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      7048.38 |      5.58 |          21.33 |                 53.06 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        28.48 |      0.43 |           0.31 |                  0.32 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
