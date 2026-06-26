## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 585s 
* Code: 1782309137
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:226210
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782309137

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      194.00 |           0.00 |            0.00 |         62.00 |          130.00 |              1 |           0 |             | None           |             0 | False         |               18.56 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        177 |            0.36 |            10054.69 |           2013.56 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        177 |            0.36 |            10054.69 |           2013.56 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 127.73 |
| TPC-DS Q2     |                 312.43 |
| TPC-DS Q3     |                 188.47 |
| TPC-DS Q4     |                8922.19 |
| TPC-DS Q5     |                 530.52 |
| TPC-DS Q6     |               51798.15 |
| TPC-DS Q7     |                 375.14 |
| TPC-DS Q8     |                  69.22 |
| TPC-DS Q9     |                2497.53 |
| TPC-DS Q10    |                1187.07 |
| TPC-DS Q11    |                5421.18 |
| TPC-DS Q12    |                  62.56 |
| TPC-DS Q13    |                 577.65 |
| TPC-DS Q14a+b |                2099.85 |
| TPC-DS Q15    |                 108.23 |
| TPC-DS Q16    |                 182.95 |
| TPC-DS Q17    |                 287.66 |
| TPC-DS Q18    |                 375.59 |
| TPC-DS Q19    |                 166.11 |
| TPC-DS Q20    |                 107.04 |
| TPC-DS Q21    |                 232.32 |
| TPC-DS Q22    |                3949.31 |
| TPC-DS Q23a+b |                5435.30 |
| TPC-DS Q24a+b |                 705.70 |
| TPC-DS Q25    |                 357.89 |
| TPC-DS Q26    |                 263.42 |
| TPC-DS Q27    |                  37.13 |
| TPC-DS Q28    |                 861.96 |
| TPC-DS Q29    |                 355.98 |
| TPC-DS Q30    |                8750.39 |
| TPC-DS Q31    |                1535.26 |
| TPC-DS Q32    |                  77.95 |
| TPC-DS Q33    |                 426.68 |
| TPC-DS Q34    |                  35.09 |
| TPC-DS Q35    |                1366.75 |
| TPC-DS Q36    |                  36.16 |
| TPC-DS Q37    |                 553.56 |
| TPC-DS Q38    |                1381.16 |
| TPC-DS Q39a+b |                2587.64 |
| TPC-DS Q40    |                 131.75 |
| TPC-DS Q41    |                 881.31 |
| TPC-DS Q42    |                 100.36 |
| TPC-DS Q43    |                  34.45 |
| TPC-DS Q44    |                   3.53 |
| TPC-DS Q45    |                  88.03 |
| TPC-DS Q46    |                  43.17 |
| TPC-DS Q47    |                1766.50 |
| TPC-DS Q48    |                 622.78 |
| TPC-DS Q49    |                 482.28 |
| TPC-DS Q50    |                 422.69 |
| TPC-DS Q51    |                 814.58 |
| TPC-DS Q52    |                  93.10 |
| TPC-DS Q53    |                 122.83 |
| TPC-DS Q54    |                  96.51 |
| TPC-DS Q55    |                  94.57 |
| TPC-DS Q56    |                 434.94 |
| TPC-DS Q57    |                 824.05 |
| TPC-DS Q58    |                 421.86 |
| TPC-DS Q59    |                 445.07 |
| TPC-DS Q60    |                 384.17 |
| TPC-DS Q61    |                 172.89 |
| TPC-DS Q62    |                 119.71 |
| TPC-DS Q63    |                 120.33 |
| TPC-DS Q64    |                 670.19 |
| TPC-DS Q65    |                 595.19 |
| TPC-DS Q66    |                 217.19 |
| TPC-DS Q67    |                2897.31 |
| TPC-DS Q68    |                  46.50 |
| TPC-DS Q69    |                 269.83 |
| TPC-DS Q70    |                 383.19 |
| TPC-DS Q71    |                 345.73 |
| TPC-DS Q72    |                 822.10 |
| TPC-DS Q73    |                  37.03 |
| TPC-DS Q74    |                 886.82 |
| TPC-DS Q75    |                1037.75 |
| TPC-DS Q76    |                 162.64 |
| TPC-DS Q77    |                 392.28 |
| TPC-DS Q78    |                1753.25 |
| TPC-DS Q79    |                 179.18 |
| TPC-DS Q80    |                 579.86 |
| TPC-DS Q81    |               38959.51 |
| TPC-DS Q82    |                 806.39 |
| TPC-DS Q83    |                 100.88 |
| TPC-DS Q84    |                  97.10 |
| TPC-DS Q85    |                 347.72 |
| TPC-DS Q86    |                 207.42 |
| TPC-DS Q87    |                1427.97 |
| TPC-DS Q88    |                2984.98 |
| TPC-DS Q89    |                  37.75 |
| TPC-DS Q90    |                 133.71 |
| TPC-DS Q91    |                 154.90 |
| TPC-DS Q92    |                  57.54 |
| TPC-DS Q93    |                 225.38 |
| TPC-DS Q94    |                 169.22 |
| TPC-DS Q95    |                3078.26 |
| TPC-DS Q96    |                 101.50 |
| TPC-DS Q97    |                 384.47 |
| TPC-DS Q98    |                 173.97 |
| TPC-DS Q99    |                 176.20 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        78.34 |      0.87 |           2.17 |                  4.58 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         9.66 |      0.30 |           0.00 |                  0.98 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       240.60 |      2.08 |           3.10 |                  5.79 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.15 |      0.43 |           0.30 |                  0.30 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
