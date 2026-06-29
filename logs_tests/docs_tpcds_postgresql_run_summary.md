## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 549s 
* Code: 1782732822
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:269230
  * datadisk:5747
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782732822

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      196.00 |           1.00 |            0.00 |         61.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               18.37 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        180 |            0.36 |            10101.22 |           1980.00 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        180 |            0.36 |            10101.22 |           1980.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 156.58 |
| TPC-DS Q2     |                 314.42 |
| TPC-DS Q3     |                 191.80 |
| TPC-DS Q4     |                8868.43 |
| TPC-DS Q5     |                 496.68 |
| TPC-DS Q6     |               52884.13 |
| TPC-DS Q7     |                 386.10 |
| TPC-DS Q8     |                  69.72 |
| TPC-DS Q9     |                2538.50 |
| TPC-DS Q10    |                1204.19 |
| TPC-DS Q11    |                5301.77 |
| TPC-DS Q12    |                  71.63 |
| TPC-DS Q13    |                 637.11 |
| TPC-DS Q14a+b |                2083.80 |
| TPC-DS Q15    |                 119.24 |
| TPC-DS Q16    |                 210.36 |
| TPC-DS Q17    |                 320.69 |
| TPC-DS Q18    |                 441.67 |
| TPC-DS Q19    |                 164.51 |
| TPC-DS Q20    |                 111.88 |
| TPC-DS Q21    |                 228.09 |
| TPC-DS Q22    |                3486.12 |
| TPC-DS Q23a+b |                5475.90 |
| TPC-DS Q24a+b |                  69.09 |
| TPC-DS Q25    |                 332.17 |
| TPC-DS Q26    |                 265.65 |
| TPC-DS Q27    |                  35.78 |
| TPC-DS Q28    |                 860.33 |
| TPC-DS Q29    |                 357.66 |
| TPC-DS Q30    |                8799.76 |
| TPC-DS Q31    |                1574.81 |
| TPC-DS Q32    |                  98.17 |
| TPC-DS Q33    |                 416.25 |
| TPC-DS Q34    |                  36.18 |
| TPC-DS Q35    |                1697.73 |
| TPC-DS Q36    |                  36.69 |
| TPC-DS Q37    |                 314.84 |
| TPC-DS Q38    |                1843.75 |
| TPC-DS Q39a+b |                3000.19 |
| TPC-DS Q40    |                 138.17 |
| TPC-DS Q41    |                 816.26 |
| TPC-DS Q42    |                  96.10 |
| TPC-DS Q43    |                  35.90 |
| TPC-DS Q44    |                   3.27 |
| TPC-DS Q45    |                  96.50 |
| TPC-DS Q46    |                  43.53 |
| TPC-DS Q47    |                1638.26 |
| TPC-DS Q48    |                 657.10 |
| TPC-DS Q49    |                 488.88 |
| TPC-DS Q50    |                 496.86 |
| TPC-DS Q51    |                 828.76 |
| TPC-DS Q52    |                  95.67 |
| TPC-DS Q53    |                 127.38 |
| TPC-DS Q54    |                  95.76 |
| TPC-DS Q55    |                  93.88 |
| TPC-DS Q56    |                 382.90 |
| TPC-DS Q57    |                 849.61 |
| TPC-DS Q58    |                 422.68 |
| TPC-DS Q59    |                 444.00 |
| TPC-DS Q60    |                 449.66 |
| TPC-DS Q61    |                 113.07 |
| TPC-DS Q62    |                 116.52 |
| TPC-DS Q63    |                 118.67 |
| TPC-DS Q64    |                 694.34 |
| TPC-DS Q65    |                 582.49 |
| TPC-DS Q66    |                 222.89 |
| TPC-DS Q67    |                2969.22 |
| TPC-DS Q68    |                  49.39 |
| TPC-DS Q69    |                 286.52 |
| TPC-DS Q70    |                 388.63 |
| TPC-DS Q71    |                 309.09 |
| TPC-DS Q72    |                 989.17 |
| TPC-DS Q73    |                  36.33 |
| TPC-DS Q74    |                1338.85 |
| TPC-DS Q75    |                 986.15 |
| TPC-DS Q76    |                 166.71 |
| TPC-DS Q77    |                 402.34 |
| TPC-DS Q78    |                1646.83 |
| TPC-DS Q79    |                 182.27 |
| TPC-DS Q80    |                 569.04 |
| TPC-DS Q81    |               39619.65 |
| TPC-DS Q82    |                 597.08 |
| TPC-DS Q83    |                 101.16 |
| TPC-DS Q84    |                  94.59 |
| TPC-DS Q85    |                 363.29 |
| TPC-DS Q86    |                 191.79 |
| TPC-DS Q87    |                1471.58 |
| TPC-DS Q88    |                3002.34 |
| TPC-DS Q89    |                 129.67 |
| TPC-DS Q90    |                 126.16 |
| TPC-DS Q91    |                  98.50 |
| TPC-DS Q92    |                  55.46 |
| TPC-DS Q93    |                 216.40 |
| TPC-DS Q94    |                 172.84 |
| TPC-DS Q95    |                3064.01 |
| TPC-DS Q96    |                  92.19 |
| TPC-DS Q97    |                 387.90 |
| TPC-DS Q98    |                 195.47 |
| TPC-DS Q99    |                 168.06 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       105.72 |      1.53 |           2.81 |                  5.50 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         6.64 |      0.22 |           0.00 |                  0.61 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       252.87 |      2.22 |           3.00 |                  5.68 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.64 |      0.02 |           0.28 |                  0.28 |

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
