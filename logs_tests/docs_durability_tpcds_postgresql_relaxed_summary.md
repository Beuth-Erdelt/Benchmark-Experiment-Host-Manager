## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 704s 
* Code: 1792612601
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.7.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:913888
  * datadisk:5792
  * volume_size:1.8T
  * volume_used:893G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792612601

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792612601-558b675759-w7w2x: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |      110.00 |           8.00 |            1.00 |         50.00 |           42.00 |              8 |           0 |             | None           |             0 | False         |               32.73 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        166 |            0.27 |            13292.85 |           2146.99 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        166 |            0.27 |            13292.85 |           2146.99 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  92.04 |
| TPC-DS Q2     |                 188.73 |
| TPC-DS Q3     |                 128.82 |
| TPC-DS Q4     |                6419.94 |
| TPC-DS Q5     |                 372.95 |
| TPC-DS Q6     |               48698.63 |
| TPC-DS Q7     |                 308.51 |
| TPC-DS Q8     |                  91.21 |
| TPC-DS Q9     |                1714.51 |
| TPC-DS Q10    |                 887.44 |
| TPC-DS Q11    |                4044.29 |
| TPC-DS Q12    |                  51.72 |
| TPC-DS Q13    |                 497.51 |
| TPC-DS Q14a+b |                1517.36 |
| TPC-DS Q15    |                  94.02 |
| TPC-DS Q16    |                 147.40 |
| TPC-DS Q17    |                 249.56 |
| TPC-DS Q18    |                 320.41 |
| TPC-DS Q19    |                 131.82 |
| TPC-DS Q20    |                  81.28 |
| TPC-DS Q21    |                 177.86 |
| TPC-DS Q22    |                2600.73 |
| TPC-DS Q23a+b |                3415.77 |
| TPC-DS Q24a+b |                 579.19 |
| TPC-DS Q25    |                 255.06 |
| TPC-DS Q26    |                 199.54 |
| TPC-DS Q27    |                  15.88 |
| TPC-DS Q28    |                 555.07 |
| TPC-DS Q29    |                 268.74 |
| TPC-DS Q30    |                7652.61 |
| TPC-DS Q31    |                1288.98 |
| TPC-DS Q32    |                 116.56 |
| TPC-DS Q33    |                 314.17 |
| TPC-DS Q34    |                  21.44 |
| TPC-DS Q35    |                 986.29 |
| TPC-DS Q36    |                  18.77 |
| TPC-DS Q37    |                 235.28 |
| TPC-DS Q38    |                1020.98 |
| TPC-DS Q39a+b |                1774.37 |
| TPC-DS Q40    |                 104.17 |
| TPC-DS Q41    |                 855.63 |
| TPC-DS Q42    |                  70.43 |
| TPC-DS Q43    |                  21.67 |
| TPC-DS Q44    |                 361.64 |
| TPC-DS Q45    |                  76.17 |
| TPC-DS Q46    |                  24.41 |
| TPC-DS Q47    |                1307.77 |
| TPC-DS Q48    |                 473.58 |
| TPC-DS Q49    |                 332.85 |
| TPC-DS Q50    |                 305.62 |
| TPC-DS Q51    |                 651.47 |
| TPC-DS Q52    |                  66.37 |
| TPC-DS Q53    |                  80.00 |
| TPC-DS Q54    |                  64.26 |
| TPC-DS Q55    |                  63.36 |
| TPC-DS Q56    |                 284.70 |
| TPC-DS Q57    |                 585.94 |
| TPC-DS Q58    |                 306.82 |
| TPC-DS Q59    |                 290.74 |
| TPC-DS Q60    |                 279.15 |
| TPC-DS Q61    |                  90.86 |
| TPC-DS Q62    |                  81.08 |
| TPC-DS Q63    |                  81.52 |
| TPC-DS Q64    |                 497.00 |
| TPC-DS Q65    |                 419.26 |
| TPC-DS Q66    |                 162.69 |
| TPC-DS Q67    |                2243.95 |
| TPC-DS Q68    |                  30.52 |
| TPC-DS Q69    |                 201.80 |
| TPC-DS Q70    |                 284.01 |
| TPC-DS Q71    |                 242.29 |
| TPC-DS Q72    |                 784.01 |
| TPC-DS Q73    |                  22.42 |
| TPC-DS Q74    |                 838.14 |
| TPC-DS Q75    |                 578.09 |
| TPC-DS Q76    |                 118.29 |
| TPC-DS Q77    |                 244.46 |
| TPC-DS Q78    |                1252.39 |
| TPC-DS Q79    |                  83.95 |
| TPC-DS Q80    |                 335.86 |
| TPC-DS Q81    |               33522.24 |
| TPC-DS Q82    |                 241.15 |
| TPC-DS Q83    |                  79.20 |
| TPC-DS Q84    |                  19.16 |
| TPC-DS Q85    |                 245.07 |
| TPC-DS Q86    |                 150.51 |
| TPC-DS Q87    |                1018.83 |
| TPC-DS Q88    |                1937.55 |
| TPC-DS Q89    |                  90.52 |
| TPC-DS Q90    |                  95.19 |
| TPC-DS Q91    |                 118.73 |
| TPC-DS Q92    |                  40.85 |
| TPC-DS Q93    |                 181.85 |
| TPC-DS Q94    |                 139.27 |
| TPC-DS Q95    |                2558.10 |
| TPC-DS Q96    |                  74.81 |
| TPC-DS Q97    |                 293.76 |
| TPC-DS Q98    |                 148.66 |
| TPC-DS Q99    |                 108.17 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
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
