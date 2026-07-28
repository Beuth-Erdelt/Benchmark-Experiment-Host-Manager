## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1372s 
* Code: 1785194031
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824131
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785194031

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785194031-65d5f7bcb7-sqhfz: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      427.00 |           0.00 |            1.00 |        133.00 |          284.00 |              8 |           0 |             | None           |             0 | False         |               25.29 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        734 |            0.65 |            16838.29 |           1456.68 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        734 |            0.65 |            16838.29 |           1456.68 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 195.35 |
| TPC-DS Q2     |                 467.28 |
| TPC-DS Q3     |                 400.11 |
| TPC-DS Q4     |               18040.64 |
| TPC-DS Q5     |                 761.92 |
| TPC-DS Q6     |              206976.58 |
| TPC-DS Q7     |                 989.82 |
| TPC-DS Q8     |                 101.67 |
| TPC-DS Q9     |                2337.01 |
| TPC-DS Q10    |                1116.31 |
| TPC-DS Q11    |               10068.44 |
| TPC-DS Q12    |                 144.69 |
| TPC-DS Q13    |                1270.97 |
| TPC-DS Q14a+b |                6535.59 |
| TPC-DS Q15    |                 282.16 |
| TPC-DS Q16    |                 399.91 |
| TPC-DS Q17    |                 656.58 |
| TPC-DS Q18    |                 585.07 |
| TPC-DS Q19    |                 402.52 |
| TPC-DS Q20    |                 251.33 |
| TPC-DS Q21    |                 310.85 |
| TPC-DS Q22    |                7219.18 |
| TPC-DS Q23a+b |               11006.14 |
| TPC-DS Q24a+b |                1254.05 |
| TPC-DS Q25    |                 626.01 |
| TPC-DS Q26    |                 435.74 |
| TPC-DS Q27    |                1153.78 |
| TPC-DS Q28    |                1846.05 |
| TPC-DS Q29    |                 730.88 |
| TPC-DS Q30    |               67156.80 |
| TPC-DS Q31    |                3833.71 |
| TPC-DS Q32    |                 149.93 |
| TPC-DS Q33    |                 763.77 |
| TPC-DS Q34    |                  35.09 |
| TPC-DS Q35    |                1213.32 |
| TPC-DS Q36    |                  36.54 |
| TPC-DS Q37    |                 333.39 |
| TPC-DS Q38    |                2848.07 |
| TPC-DS Q39a+b |                4748.58 |
| TPC-DS Q40    |                 425.59 |
| TPC-DS Q41    |                2672.53 |
| TPC-DS Q42    |                 161.92 |
| TPC-DS Q43    |                  52.63 |
| TPC-DS Q44    |                   1.84 |
| TPC-DS Q45    |                 168.58 |
| TPC-DS Q46    |                  53.39 |
| TPC-DS Q47    |                2184.92 |
| TPC-DS Q48    |                1043.56 |
| TPC-DS Q49    |                 644.92 |
| TPC-DS Q50    |                1149.79 |
| TPC-DS Q51    |                2086.48 |
| TPC-DS Q52    |                 154.05 |
| TPC-DS Q53    |                 186.12 |
| TPC-DS Q54    |                  64.13 |
| TPC-DS Q55    |                 150.59 |
| TPC-DS Q56    |                 727.62 |
| TPC-DS Q57    |                1960.78 |
| TPC-DS Q58    |                 727.06 |
| TPC-DS Q59    |                 710.90 |
| TPC-DS Q60    |                 878.03 |
| TPC-DS Q61    |                 104.92 |
| TPC-DS Q62    |                 173.42 |
| TPC-DS Q63    |                 190.57 |
| TPC-DS Q64    |                 850.32 |
| TPC-DS Q65    |                1112.75 |
| TPC-DS Q66    |                 545.22 |
| TPC-DS Q67    |                7656.39 |
| TPC-DS Q68    |                  69.99 |
| TPC-DS Q69    |                 373.90 |
| TPC-DS Q70    |                 701.40 |
| TPC-DS Q71    |                 679.06 |
| TPC-DS Q72    |                2323.13 |
| TPC-DS Q73    |                  37.58 |
| TPC-DS Q74    |                1989.23 |
| TPC-DS Q75    |                3282.63 |
| TPC-DS Q76    |                 357.60 |
| TPC-DS Q77    |                 430.96 |
| TPC-DS Q78    |                4011.82 |
| TPC-DS Q79    |                 262.61 |
| TPC-DS Q80    |                 875.13 |
| TPC-DS Q81    |              292877.99 |
| TPC-DS Q82    |                 447.08 |
| TPC-DS Q83    |                 136.95 |
| TPC-DS Q84    |                  23.43 |
| TPC-DS Q85    |                 279.84 |
| TPC-DS Q86    |                 470.08 |
| TPC-DS Q87    |                2212.85 |
| TPC-DS Q88    |                2446.88 |
| TPC-DS Q89    |                 204.56 |
| TPC-DS Q90    |                 284.55 |
| TPC-DS Q91    |                 145.01 |
| TPC-DS Q92    |                 168.23 |
| TPC-DS Q93    |                 581.52 |
| TPC-DS Q94    |                 309.36 |
| TPC-DS Q95    |                7145.29 |
| TPC-DS Q96    |                 317.96 |
| TPC-DS Q97    |                 719.43 |
| TPC-DS Q98    |                 389.86 |
| TPC-DS Q99    |                 297.96 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       235.12 |      2.11 |           6.32 |                 13.00 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.11 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        23.75 |      0.25 |           0.01 |                  2.21 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       893.62 |      2.54 |           6.97 |                 13.65 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        21.39 |      0.55 |           0.34 |                  0.35 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
