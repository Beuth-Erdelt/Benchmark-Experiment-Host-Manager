## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 585s 
* Code: 1783001511
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 15Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:649421
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783001511

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783001511-574656c78d-6qxs6: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 1.00 |      231.00 |           1.00 |            0.00 |         45.00 |          174.00 |              8 |           0 |             | None           |             0 | False         |               15.58 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        155 |            0.28 |            13413.08 |           2299.35 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        155 |            0.28 |            13413.08 |           2299.35 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  90.44 |
| TPC-DS Q2     |                 195.45 |
| TPC-DS Q3     |                 123.13 |
| TPC-DS Q4     |                6401.93 |
| TPC-DS Q5     |                 370.14 |
| TPC-DS Q6     |               50352.66 |
| TPC-DS Q7     |                 288.01 |
| TPC-DS Q8     |                  48.59 |
| TPC-DS Q9     |                1768.99 |
| TPC-DS Q10    |                 853.76 |
| TPC-DS Q11    |                4023.67 |
| TPC-DS Q12    |                  54.89 |
| TPC-DS Q13    |                 462.85 |
| TPC-DS Q14a+b |                1528.23 |
| TPC-DS Q15    |                  99.73 |
| TPC-DS Q16    |                 156.68 |
| TPC-DS Q17    |                 255.73 |
| TPC-DS Q18    |                 332.06 |
| TPC-DS Q19    |                 126.95 |
| TPC-DS Q20    |                  83.09 |
| TPC-DS Q21    |                 166.65 |
| TPC-DS Q22    |                2736.20 |
| TPC-DS Q23a+b |                4093.47 |
| TPC-DS Q24a+b |                 467.75 |
| TPC-DS Q25    |                 259.24 |
| TPC-DS Q26    |                 191.22 |
| TPC-DS Q27    |                  16.82 |
| TPC-DS Q28    |                 556.03 |
| TPC-DS Q29    |                 267.33 |
| TPC-DS Q30    |                7568.85 |
| TPC-DS Q31    |                1288.15 |
| TPC-DS Q32    |                  76.91 |
| TPC-DS Q33    |                 279.98 |
| TPC-DS Q34    |                  16.74 |
| TPC-DS Q35    |                 978.94 |
| TPC-DS Q36    |                  17.66 |
| TPC-DS Q37    |                 219.55 |
| TPC-DS Q38    |                1041.99 |
| TPC-DS Q39a+b |                1916.40 |
| TPC-DS Q40    |                  99.16 |
| TPC-DS Q41    |                 836.88 |
| TPC-DS Q42    |                  78.75 |
| TPC-DS Q43    |                  20.13 |
| TPC-DS Q44    |                 355.45 |
| TPC-DS Q45    |                  74.21 |
| TPC-DS Q46    |                  24.50 |
| TPC-DS Q47    |                1291.81 |
| TPC-DS Q48    |                 477.99 |
| TPC-DS Q49    |                 337.34 |
| TPC-DS Q50    |                 322.67 |
| TPC-DS Q51    |                 647.80 |
| TPC-DS Q52    |                  64.51 |
| TPC-DS Q53    |                  77.70 |
| TPC-DS Q54    |                  59.66 |
| TPC-DS Q55    |                  60.45 |
| TPC-DS Q56    |                 328.74 |
| TPC-DS Q57    |                 631.76 |
| TPC-DS Q58    |                 314.77 |
| TPC-DS Q59    |                 283.69 |
| TPC-DS Q60    |                 303.22 |
| TPC-DS Q61    |                 103.00 |
| TPC-DS Q62    |                  73.62 |
| TPC-DS Q63    |                  80.76 |
| TPC-DS Q64    |                 470.03 |
| TPC-DS Q65    |                 398.39 |
| TPC-DS Q66    |                 156.18 |
| TPC-DS Q67    |                2285.21 |
| TPC-DS Q68    |                  28.89 |
| TPC-DS Q69    |                 203.61 |
| TPC-DS Q70    |                 315.67 |
| TPC-DS Q71    |                 268.66 |
| TPC-DS Q72    |                 797.64 |
| TPC-DS Q73    |                  20.99 |
| TPC-DS Q74    |                 871.89 |
| TPC-DS Q75    |                 640.75 |
| TPC-DS Q76    |                 151.48 |
| TPC-DS Q77    |                 231.52 |
| TPC-DS Q78    |                1407.08 |
| TPC-DS Q79    |                 146.38 |
| TPC-DS Q80    |                 400.49 |
| TPC-DS Q81    |               31846.33 |
| TPC-DS Q82    |                 283.54 |
| TPC-DS Q83    |                  67.09 |
| TPC-DS Q84    |                  16.57 |
| TPC-DS Q85    |                 224.90 |
| TPC-DS Q86    |                 186.61 |
| TPC-DS Q87    |                 965.92 |
| TPC-DS Q88    |                1928.92 |
| TPC-DS Q89    |                  80.89 |
| TPC-DS Q90    |                  92.20 |
| TPC-DS Q91    |                  70.07 |
| TPC-DS Q92    |                  53.68 |
| TPC-DS Q93    |                 143.70 |
| TPC-DS Q94    |                 151.05 |
| TPC-DS Q95    |                2716.96 |
| TPC-DS Q96    |                  70.52 |
| TPC-DS Q97    |                 282.26 |
| TPC-DS Q98    |                 140.80 |
| TPC-DS Q99    |                 107.29 |

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
