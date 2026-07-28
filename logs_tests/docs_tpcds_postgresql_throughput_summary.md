## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 885s 
* Code: 1785195502
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
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
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
  * disk:816851
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785195502
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817022
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785195502
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817022
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785195502

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785195502-864dd966b8-4fqrv: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      230.00 |           1.00 |            0.00 |         47.00 |          174.00 |              8 |           0 |             | None           |             0 | False         |               15.65 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        161 |            0.29 |            12740.32 |           2213.66 |          -1 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |        164 |            0.30 |            12297.11 |           2173.17 |          -1 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |        161 |            0.31 |            12127.19 |           2213.66 |          -1 | PostgreSQL-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        161 |            0.29 |            12740.32 |           2213.66 |          -1 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |        164 |            0.30 |            12211.86 |           4346.34 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                 106.18 |                 107.42 |                 103.17 |
| TPC-DS Q2     |                 184.50 |                 182.91 |                 182.88 |
| TPC-DS Q3     |                 139.18 |                 132.11 |                 134.50 |
| TPC-DS Q4     |                6705.71 |                6624.58 |                6521.45 |
| TPC-DS Q5     |                 374.29 |                 371.06 |                 366.61 |
| TPC-DS Q6     |               51964.98 |               54028.23 |               52468.61 |
| TPC-DS Q7     |                 287.65 |                 285.44 |                 301.32 |
| TPC-DS Q8     |                  94.12 |                  91.97 |                  87.91 |
| TPC-DS Q9     |                1720.50 |                1697.48 |                1693.86 |
| TPC-DS Q10    |                 860.98 |                 864.21 |                 857.61 |
| TPC-DS Q11    |                3900.98 |                4756.54 |                4206.76 |
| TPC-DS Q12    |                  55.57 |                  56.82 |                  58.07 |
| TPC-DS Q13    |                 471.63 |                 474.69 |                 490.93 |
| TPC-DS Q14a+b |                2356.39 |                1592.23 |                1657.78 |
| TPC-DS Q15    |                  98.82 |                 100.20 |                  98.97 |
| TPC-DS Q16    |                 153.21 |                 149.33 |                 166.58 |
| TPC-DS Q17    |                 256.80 |                 493.12 |                 267.67 |
| TPC-DS Q18    |                 307.60 |                 397.33 |                 340.31 |
| TPC-DS Q19    |                 136.99 |                 140.54 |                 132.91 |
| TPC-DS Q20    |                  83.11 |                  85.24 |                  86.68 |
| TPC-DS Q21    |                 180.67 |                 171.44 |                 167.90 |
| TPC-DS Q22    |                2618.08 |                2627.61 |                2853.36 |
| TPC-DS Q23a+b |                4000.45 |                5248.84 |                4625.11 |
| TPC-DS Q24a+b |                 485.37 |                 474.16 |                 524.08 |
| TPC-DS Q25    |                 250.69 |                 250.10 |                 259.74 |
| TPC-DS Q26    |                 205.62 |                 184.50 |                 211.95 |
| TPC-DS Q27    |                  20.26 |                  16.61 |                  18.69 |
| TPC-DS Q28    |                 563.38 |                 549.98 |                 574.49 |
| TPC-DS Q29    |                 271.92 |                 263.55 |                 283.31 |
| TPC-DS Q30    |                7574.89 |                8709.46 |                7664.16 |
| TPC-DS Q31    |                1284.96 |                1258.18 |                1541.14 |
| TPC-DS Q32    |                 116.25 |                 111.57 |                 173.54 |
| TPC-DS Q33    |                 326.44 |                 316.42 |                 431.05 |
| TPC-DS Q34    |                  20.14 |                  20.56 |                  21.73 |
| TPC-DS Q35    |                 953.13 |                 960.19 |                 961.27 |
| TPC-DS Q36    |                  16.67 |                  20.83 |                  19.84 |
| TPC-DS Q37    |                 190.20 |                 383.73 |                 189.42 |
| TPC-DS Q38    |                1022.46 |                1375.93 |                1030.78 |
| TPC-DS Q39a+b |                1822.88 |                1838.23 |                2155.70 |
| TPC-DS Q40    |                 108.57 |                 107.57 |                 153.13 |
| TPC-DS Q41    |                 721.27 |                 775.94 |                 762.86 |
| TPC-DS Q42    |                  65.00 |                  63.05 |                  67.97 |
| TPC-DS Q43    |                  21.63 |                  20.76 |                  20.21 |
| TPC-DS Q44    |                 363.74 |                 356.02 |                 411.50 |
| TPC-DS Q45    |                  71.04 |                  71.55 |                  73.99 |
| TPC-DS Q46    |                  25.61 |                  27.40 |                  27.87 |
| TPC-DS Q47    |                1532.01 |                1797.48 |                1170.42 |
| TPC-DS Q48    |                 488.99 |                 479.31 |                 468.33 |
| TPC-DS Q49    |                 334.71 |                 328.72 |                 326.59 |
| TPC-DS Q50    |                 323.77 |                 309.97 |                 375.24 |
| TPC-DS Q51    |                 691.33 |                 646.80 |                 766.26 |
| TPC-DS Q52    |                  66.84 |                  62.71 |                 121.89 |
| TPC-DS Q53    |                  78.92 |                  73.44 |                 163.76 |
| TPC-DS Q54    |                  63.27 |                  62.51 |                 105.44 |
| TPC-DS Q55    |                  63.56 |                  61.18 |                 120.23 |
| TPC-DS Q56    |                 308.41 |                 298.90 |                 428.22 |
| TPC-DS Q57    |                 589.85 |                 649.97 |                 586.46 |
| TPC-DS Q58    |                 319.35 |                 303.87 |                 323.93 |
| TPC-DS Q59    |                 290.96 |                 288.42 |                 282.94 |
| TPC-DS Q60    |                 319.56 |                 307.62 |                 305.75 |
| TPC-DS Q61    |                 102.03 |                  97.53 |                 100.13 |
| TPC-DS Q62    |                  76.15 |                  73.38 |                  77.35 |
| TPC-DS Q63    |                  81.45 |                 123.29 |                  78.20 |
| TPC-DS Q64    |                 442.34 |                1094.73 |                 440.12 |
| TPC-DS Q65    |                 626.57 |                 586.61 |                 408.72 |
| TPC-DS Q66    |                 351.38 |                 172.55 |                 163.65 |
| TPC-DS Q67    |                2436.39 |                2311.29 |                2720.61 |
| TPC-DS Q68    |                  31.67 |                  29.93 |                  41.06 |
| TPC-DS Q69    |                 206.84 |                 200.94 |                 419.69 |
| TPC-DS Q70    |                 279.56 |                 282.03 |                 319.49 |
| TPC-DS Q71    |                 261.06 |                 258.98 |                 254.93 |
| TPC-DS Q72    |                 734.15 |                 743.40 |                 739.32 |
| TPC-DS Q73    |                  22.05 |                  22.01 |                  20.53 |
| TPC-DS Q74    |                 841.81 |                1185.84 |                 781.92 |
| TPC-DS Q75    |                 570.92 |                1415.90 |                 555.30 |
| TPC-DS Q76    |                 189.39 |                 186.56 |                 170.35 |
| TPC-DS Q77    |                 238.20 |                 250.86 |                 234.44 |
| TPC-DS Q78    |                1692.42 |                1409.04 |                1229.87 |
| TPC-DS Q79    |                 113.02 |                 111.79 |                 104.38 |
| TPC-DS Q80    |                 362.75 |                 352.65 |                 760.09 |
| TPC-DS Q81    |               32340.66 |               32888.77 |               34285.62 |
| TPC-DS Q82    |                 242.82 |                 234.56 |                 239.81 |
| TPC-DS Q83    |                  70.44 |                  69.56 |                  68.32 |
| TPC-DS Q84    |                  65.79 |                  69.72 |                  64.37 |
| TPC-DS Q85    |                 238.82 |                 257.74 |                 238.14 |
| TPC-DS Q86    |                 147.66 |                 165.17 |                 150.87 |
| TPC-DS Q87    |                1021.58 |                1045.36 |                1032.90 |
| TPC-DS Q88    |                1909.65 |                2299.74 |                1972.22 |
| TPC-DS Q89    |                 116.30 |                 118.70 |                 114.81 |
| TPC-DS Q90    |                 100.08 |                  88.12 |                  91.91 |
| TPC-DS Q91    |                  75.79 |                  73.01 |                  74.38 |
| TPC-DS Q92    |                  62.16 |                  62.31 |                  64.06 |
| TPC-DS Q93    |                 163.50 |                 159.26 |                 152.83 |
| TPC-DS Q94    |                 124.60 |                 140.77 |                 137.53 |
| TPC-DS Q95    |                2460.48 |                2452.51 |                2629.43 |
| TPC-DS Q96    |                  71.91 |                  72.11 |                  68.50 |
| TPC-DS Q97    |                 277.37 |                 281.39 |                 280.80 |
| TPC-DS Q98    |                 131.31 |                 134.46 |                 140.95 |
| TPC-DS Q99    |                 107.82 |                 107.61 |                 110.10 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| PostgreSQL-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| PostgreSQL-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
