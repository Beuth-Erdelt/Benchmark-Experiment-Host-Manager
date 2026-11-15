## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 593s 
* Code: 1794613466
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1130860
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794613466

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794613466-7488bf9b49-s26lb: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       96.00 |           4.00 |            1.00 |         45.00 |           37.00 |              8 |         0 |             | None           |             0 | False         |               37.50 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        153 |            0.27 |            13149.80 |           2329.41 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        153 |            0.27 |            13149.80 |           2329.41 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 297.77 |
| TPC-DS Q2     |                 180.17 |
| TPC-DS Q3     |                 131.55 |
| TPC-DS Q4     |                5702.87 |
| TPC-DS Q5     |                 356.51 |
| TPC-DS Q6     |               49665.45 |
| TPC-DS Q7     |                 289.05 |
| TPC-DS Q8     |                 101.63 |
| TPC-DS Q9     |                1761.62 |
| TPC-DS Q10    |                 918.77 |
| TPC-DS Q11    |                4020.63 |
| TPC-DS Q12    |                  54.78 |
| TPC-DS Q13    |                 487.63 |
| TPC-DS Q14a+b |                1504.21 |
| TPC-DS Q15    |                 105.33 |
| TPC-DS Q16    |                 163.17 |
| TPC-DS Q17    |                 278.42 |
| TPC-DS Q18    |                 399.01 |
| TPC-DS Q19    |                 132.75 |
| TPC-DS Q20    |                  86.50 |
| TPC-DS Q21    |                 169.27 |
| TPC-DS Q22    |                2646.78 |
| TPC-DS Q23a+b |                4325.52 |
| TPC-DS Q24a+b |                 580.20 |
| TPC-DS Q25    |                 260.61 |
| TPC-DS Q26    |                 198.66 |
| TPC-DS Q27    |                 290.30 |
| TPC-DS Q28    |                 557.33 |
| TPC-DS Q29    |                 279.48 |
| TPC-DS Q30    |                7487.89 |
| TPC-DS Q31    |                1305.57 |
| TPC-DS Q32    |                 145.87 |
| TPC-DS Q33    |                 333.75 |
| TPC-DS Q34    |                  17.91 |
| TPC-DS Q35    |                 966.03 |
| TPC-DS Q36    |                 298.52 |
| TPC-DS Q37    |                 190.71 |
| TPC-DS Q38    |                 811.24 |
| TPC-DS Q39a+b |                1794.10 |
| TPC-DS Q40    |                  98.33 |
| TPC-DS Q41    |                 210.31 |
| TPC-DS Q42    |                  63.78 |
| TPC-DS Q43    |                  21.69 |
| TPC-DS Q44    |                   1.95 |
| TPC-DS Q45    |                  73.33 |
| TPC-DS Q46    |                  28.76 |
| TPC-DS Q47    |                1484.30 |
| TPC-DS Q48    |                 478.22 |
| TPC-DS Q49    |                 324.68 |
| TPC-DS Q50    |                 326.75 |
| TPC-DS Q51    |                1016.97 |
| TPC-DS Q52    |                  69.47 |
| TPC-DS Q53    |                  85.57 |
| TPC-DS Q54    |                  73.63 |
| TPC-DS Q55    |                  63.45 |
| TPC-DS Q56    |                 310.42 |
| TPC-DS Q57    |                 691.13 |
| TPC-DS Q58    |                 299.71 |
| TPC-DS Q59    |                 288.06 |
| TPC-DS Q60    |                 306.97 |
| TPC-DS Q61    |                  99.98 |
| TPC-DS Q62    |                  76.42 |
| TPC-DS Q63    |                  82.14 |
| TPC-DS Q64    |                 509.35 |
| TPC-DS Q65    |                 409.15 |
| TPC-DS Q66    |                 163.17 |
| TPC-DS Q67    |                2935.81 |
| TPC-DS Q68    |                  33.20 |
| TPC-DS Q69    |                  96.45 |
| TPC-DS Q70    |                 282.65 |
| TPC-DS Q71    |                 260.15 |
| TPC-DS Q72    |                 766.91 |
| TPC-DS Q73    |                  23.01 |
| TPC-DS Q74    |                 801.59 |
| TPC-DS Q75    |                 741.77 |
| TPC-DS Q76    |                 168.15 |
| TPC-DS Q77    |                 242.49 |
| TPC-DS Q78    |                1347.81 |
| TPC-DS Q79    |                 111.47 |
| TPC-DS Q80    |                 358.50 |
| TPC-DS Q81    |               33104.74 |
| TPC-DS Q82    |                 184.12 |
| TPC-DS Q83    |                  67.86 |
| TPC-DS Q84    |                  17.83 |
| TPC-DS Q85    |                 230.25 |
| TPC-DS Q86    |                 178.57 |
| TPC-DS Q87    |                 814.18 |
| TPC-DS Q88    |                1956.19 |
| TPC-DS Q89    |                  82.55 |
| TPC-DS Q90    |                  96.37 |
| TPC-DS Q91    |                  69.87 |
| TPC-DS Q92    |                  50.45 |
| TPC-DS Q93    |                 167.26 |
| TPC-DS Q94    |                 131.12 |
| TPC-DS Q95    |                2605.94 |
| TPC-DS Q96    |                  66.98 |
| TPC-DS Q97    |                 280.03 |
| TPC-DS Q98    |                 125.72 |
| TPC-DS Q99    |                 105.16 |

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
