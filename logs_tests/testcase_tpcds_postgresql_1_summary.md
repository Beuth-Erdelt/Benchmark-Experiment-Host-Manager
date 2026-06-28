## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1037s 
* Code: 1782552070
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
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:1077381271552
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1391288
  * cpu_list:0-255
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782552070

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1782552070-695847f58-fdfqc: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      504.00 |           4.00 |            1.00 |         82.00 |          409.00 |              8 |           0 |             | None           |             0 | False         |                7.14 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        248 |            0.46 |             7992.02 |           1437.10 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        248 |            0.46 |             7992.02 |           1437.10 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 124.57 |
| TPC-DS Q2     |                 359.84 |
| TPC-DS Q3     |                 229.97 |
| TPC-DS Q4     |               10549.67 |
| TPC-DS Q5     |                 672.73 |
| TPC-DS Q6     |               56874.73 |
| TPC-DS Q7     |                 486.99 |
| TPC-DS Q8     |                  81.12 |
| TPC-DS Q9     |                2684.87 |
| TPC-DS Q10    |                1301.89 |
| TPC-DS Q11    |                6665.48 |
| TPC-DS Q12    |                  95.25 |
| TPC-DS Q13    |                 804.45 |
| TPC-DS Q14a+b |                2738.69 |
| TPC-DS Q15    |                 179.81 |
| TPC-DS Q16    |                 280.22 |
| TPC-DS Q17    |                 445.36 |
| TPC-DS Q18    |                 583.33 |
| TPC-DS Q19    |                 274.57 |
| TPC-DS Q20    |                 153.22 |
| TPC-DS Q21    |                 285.06 |
| TPC-DS Q22    |                4279.16 |
| TPC-DS Q23a+b |                6031.94 |
| TPC-DS Q24a+b |                1021.23 |
| TPC-DS Q25    |                 485.61 |
| TPC-DS Q26    |                 385.94 |
| TPC-DS Q27    |                  30.05 |
| TPC-DS Q28    |                 978.31 |
| TPC-DS Q29    |                 516.98 |
| TPC-DS Q30    |               17176.13 |
| TPC-DS Q31    |                2390.55 |
| TPC-DS Q32    |                  95.10 |
| TPC-DS Q33    |                 601.09 |
| TPC-DS Q34    |                  32.98 |
| TPC-DS Q35    |                1459.86 |
| TPC-DS Q36    |                  31.54 |
| TPC-DS Q37    |                 900.87 |
| TPC-DS Q38    |                1874.15 |
| TPC-DS Q39a+b |                3096.16 |
| TPC-DS Q40    |                 192.42 |
| TPC-DS Q41    |                 333.00 |
| TPC-DS Q42    |                 111.92 |
| TPC-DS Q43    |                  32.49 |
| TPC-DS Q44    |                   1.88 |
| TPC-DS Q45    |                 136.40 |
| TPC-DS Q46    |                  43.19 |
| TPC-DS Q47    |                2288.70 |
| TPC-DS Q48    |                 837.74 |
| TPC-DS Q49    |                 602.92 |
| TPC-DS Q50    |                 772.83 |
| TPC-DS Q51    |                1236.34 |
| TPC-DS Q52    |                 118.93 |
| TPC-DS Q53    |                 136.49 |
| TPC-DS Q54    |                  97.60 |
| TPC-DS Q55    |                 114.28 |
| TPC-DS Q56    |                 669.88 |
| TPC-DS Q57    |                1165.56 |
| TPC-DS Q58    |                 601.35 |
| TPC-DS Q59    |                 496.81 |
| TPC-DS Q60    |                 579.08 |
| TPC-DS Q61    |                 169.56 |
| TPC-DS Q62    |                 139.90 |
| TPC-DS Q63    |                 132.85 |
| TPC-DS Q64    |                 857.70 |
| TPC-DS Q65    |                 687.14 |
| TPC-DS Q66    |                 333.55 |
| TPC-DS Q67    |                3873.62 |
| TPC-DS Q68    |                  43.25 |
| TPC-DS Q69    |                 273.79 |
| TPC-DS Q70    |                 532.23 |
| TPC-DS Q71    |                 518.14 |
| TPC-DS Q72    |                1535.14 |
| TPC-DS Q73    |                  33.15 |
| TPC-DS Q74    |                1502.64 |
| TPC-DS Q75    |                1045.67 |
| TPC-DS Q76    |                 289.81 |
| TPC-DS Q77    |                 416.18 |
| TPC-DS Q78    |                1940.28 |
| TPC-DS Q79    |                 143.38 |
| TPC-DS Q80    |                 642.15 |
| TPC-DS Q81    |               72550.22 |
| TPC-DS Q82    |                 407.96 |
| TPC-DS Q83    |                 152.31 |
| TPC-DS Q84    |                 123.65 |
| TPC-DS Q85    |                 405.92 |
| TPC-DS Q86    |                 296.71 |
| TPC-DS Q87    |                1875.36 |
| TPC-DS Q88    |                3031.38 |
| TPC-DS Q89    |                 148.67 |
| TPC-DS Q90    |                 197.72 |
| TPC-DS Q91    |                 208.77 |
| TPC-DS Q92    |                 120.61 |
| TPC-DS Q93    |                 281.55 |
| TPC-DS Q94    |                 254.51 |
| TPC-DS Q95    |                5029.72 |
| TPC-DS Q96    |                 122.94 |
| TPC-DS Q97    |                 485.89 |
| TPC-DS Q98    |                 269.11 |
| TPC-DS Q99    |                 189.39 |

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
