## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1435s 
* Code: 1785196488
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
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
  * disk:811054
  * volume_size:50G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785196488
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811055
  * volume_size:50G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785196488

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785196488-55778c77c5-vsv7g: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      477.00 |           2.00 |            1.00 |        167.00 |          298.00 |              8 |           0 |             | None           |             0 | False         |                7.55 |
| PostgreSQL-1-2 |                2 |    1 |      477.00 |           2.00 |            1.00 |        167.00 |          298.00 |              8 |           0 |             | None           |             0 | False         |                7.55 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        175 |            0.30 |            12344.86 |           2036.57 |          -1 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |        220 |            0.39 |             9492.14 |           1620.00 |          -1 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        175 |            0.30 |            12344.86 |           2036.57 |          -1 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |        220 |            0.39 |             9492.14 |           1620.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  93.62 |                7561.26 |
| TPC-DS Q2     |                 176.60 |               12176.55 |
| TPC-DS Q3     |                 140.86 |               18132.04 |
| TPC-DS Q4     |                6308.65 |                8457.55 |
| TPC-DS Q5     |                 359.16 |                2555.33 |
| TPC-DS Q6     |               52932.48 |               54066.11 |
| TPC-DS Q7     |                 299.28 |                4661.85 |
| TPC-DS Q8     |                  51.55 |                 126.47 |
| TPC-DS Q9     |                1700.51 |                2094.08 |
| TPC-DS Q10    |                1662.46 |                2359.01 |
| TPC-DS Q11    |                3953.10 |                4518.14 |
| TPC-DS Q12    |                  53.45 |                  53.82 |
| TPC-DS Q13    |                 469.79 |                 648.91 |
| TPC-DS Q14a+b |                2295.82 |                1531.42 |
| TPC-DS Q15    |                  90.79 |                  90.67 |
| TPC-DS Q16    |                 150.73 |                 416.35 |
| TPC-DS Q17    |                 331.39 |                 282.00 |
| TPC-DS Q18    |                 345.40 |                 319.80 |
| TPC-DS Q19    |                 116.30 |                 117.80 |
| TPC-DS Q20    |                  77.79 |                  77.96 |
| TPC-DS Q21    |                 171.23 |               11606.43 |
| TPC-DS Q22    |                3165.07 |                2916.53 |
| TPC-DS Q23a+b |                4038.67 |                4266.69 |
| TPC-DS Q24a+b |                1493.98 |                 513.82 |
| TPC-DS Q25    |                 265.06 |                 240.51 |
| TPC-DS Q26    |                 202.54 |                 278.22 |
| TPC-DS Q27    |                  21.56 |                  15.95 |
| TPC-DS Q28    |                 561.13 |                 538.30 |
| TPC-DS Q29    |                 270.70 |                 260.74 |
| TPC-DS Q30    |                7835.26 |                7312.17 |
| TPC-DS Q31    |                1430.45 |                1274.53 |
| TPC-DS Q32    |                 194.84 |                 111.94 |
| TPC-DS Q33    |                 820.47 |                 317.82 |
| TPC-DS Q34    |                  23.53 |                  21.06 |
| TPC-DS Q35    |                 941.87 |                 926.92 |
| TPC-DS Q36    |                  16.59 |                  18.93 |
| TPC-DS Q37    |                 238.19 |                 218.00 |
| TPC-DS Q38    |                1016.05 |                1301.66 |
| TPC-DS Q39a+b |                2907.38 |                2061.48 |
| TPC-DS Q40    |                 110.64 |                 121.28 |
| TPC-DS Q41    |                 744.11 |                 810.65 |
| TPC-DS Q42    |                  69.96 |                  64.41 |
| TPC-DS Q43    |                 131.12 |                 123.96 |
| TPC-DS Q44    |                   2.23 |                  85.34 |
| TPC-DS Q45    |                  71.44 |                  74.21 |
| TPC-DS Q46    |                  23.10 |                  23.48 |
| TPC-DS Q47    |                1542.97 |                1315.29 |
| TPC-DS Q48    |                 815.99 |                 457.40 |
| TPC-DS Q49    |                 322.84 |                 332.10 |
| TPC-DS Q50    |                 396.56 |                 322.69 |
| TPC-DS Q51    |                 656.40 |                 830.38 |
| TPC-DS Q52    |                  61.31 |                  81.60 |
| TPC-DS Q53    |                  80.14 |                  77.32 |
| TPC-DS Q54    |                  63.28 |                  62.77 |
| TPC-DS Q55    |                  63.89 |                  57.85 |
| TPC-DS Q56    |                 314.85 |                 303.16 |
| TPC-DS Q57    |                 676.63 |                 630.92 |
| TPC-DS Q58    |                 305.71 |                 294.49 |
| TPC-DS Q59    |                 284.25 |                 286.14 |
| TPC-DS Q60    |                 264.61 |                 262.78 |
| TPC-DS Q61    |                 103.09 |                  97.95 |
| TPC-DS Q62    |                  79.79 |                 179.77 |
| TPC-DS Q63    |                  80.08 |                  74.67 |
| TPC-DS Q64    |                 824.75 |                 485.94 |
| TPC-DS Q65    |                 697.74 |                 407.01 |
| TPC-DS Q66    |                 242.45 |                 700.54 |
| TPC-DS Q67    |                2236.41 |                2588.14 |
| TPC-DS Q68    |                  32.11 |                  31.49 |
| TPC-DS Q69    |                  92.07 |                 193.79 |
| TPC-DS Q70    |                 297.27 |                 280.90 |
| TPC-DS Q71    |                 262.73 |                 273.08 |
| TPC-DS Q72    |                 784.64 |                 758.44 |
| TPC-DS Q73    |                  20.73 |                  20.25 |
| TPC-DS Q74    |                 782.85 |                 746.32 |
| TPC-DS Q75    |                 600.35 |                 981.11 |
| TPC-DS Q76    |                 359.79 |                 268.34 |
| TPC-DS Q77    |                 446.30 |                 424.11 |
| TPC-DS Q78    |                1306.57 |                1018.02 |
| TPC-DS Q79    |                 120.42 |                 115.80 |
| TPC-DS Q80    |                 359.06 |                 359.20 |
| TPC-DS Q81    |               34502.58 |               32038.58 |
| TPC-DS Q82    |                 231.56 |                 229.51 |
| TPC-DS Q83    |                  69.69 |                  72.60 |
| TPC-DS Q84    |                  62.95 |                  68.36 |
| TPC-DS Q85    |                 236.34 |                 352.86 |
| TPC-DS Q86    |                 172.09 |                 204.17 |
| TPC-DS Q87    |                1025.10 |                1149.33 |
| TPC-DS Q88    |                2486.25 |                1923.72 |
| TPC-DS Q89    |                  90.20 |                  88.08 |
| TPC-DS Q90    |                  97.96 |                  87.19 |
| TPC-DS Q91    |                 115.56 |                 112.80 |
| TPC-DS Q92    |                  48.27 |                  45.55 |
| TPC-DS Q93    |                 150.79 |                 133.05 |
| TPC-DS Q94    |                 119.90 |                 204.58 |
| TPC-DS Q95    |                2696.18 |                2816.05 |
| TPC-DS Q96    |                  67.86 |                  91.84 |
| TPC-DS Q97    |                 321.84 |                 310.37 |
| TPC-DS Q98    |                 206.42 |                 157.19 |
| TPC-DS Q99    |                 267.80 |                 105.67 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| PostgreSQL-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
