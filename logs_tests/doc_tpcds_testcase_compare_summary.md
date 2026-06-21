## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 4245s 
* Code: 1782049401
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253552
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782049401
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:227914
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782049401
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:258912
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782049401
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:227914
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782049401

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1    |                1 |    1 |      664.00 |           1.00 |            1.00 |         61.00 |          592.00 |              8 |           0 |             | None           |             0 | False         |                5.42 |
| MonetDB-1-1    |                1 |    1 |      422.00 |           1.00 |            1.00 |        138.00 |          274.00 |              8 |           0 |             | None           |             0 | False         |                8.53 |
| MySQL-1-1      |                1 |    1 |      820.00 |           1.00 |            1.00 |         91.00 |          715.00 |              8 |           0 |             | None           |             0 | False         |                4.39 |
| PostgreSQL-1-1 |                1 |    1 |      298.00 |           1.00 |            1.00 |         58.00 |          232.00 |              8 |           0 |             | None           |             0 | False         |               12.08 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3220 |            0.95 |             3836.91 |            108.45 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         29 |            0.06 |            62535.31 |          12041.38 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        529 |            0.85 |             4304.55 |            660.11 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        194 |            0.36 |            10326.60 |           1800.00 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3220 |            0.95 |             3836.91 |            108.45 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         29 |            0.06 |            62535.31 |          12041.38 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        529 |            0.85 |             4304.55 |            660.11 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        194 |            0.36 |            10326.60 |           1800.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:--------------|--------------------:|--------------------:|------------------:|-----------------------:|
| TPC-DS Q1     |               22.80 |               51.20 |             69.99 |                 129.84 |
| TPC-DS Q2     |             4728.70 |               99.04 |           5022.97 |                 314.55 |
| TPC-DS Q3     |               13.97 |               23.87 |             16.20 |                 212.68 |
| TPC-DS Q4     |            11968.93 |              603.97 |          28644.49 |                8694.03 |
| TPC-DS Q5     |             8581.26 |               74.78 |          13003.19 |                 552.85 |
| TPC-DS Q6     |              765.15 |               52.44 |          76134.62 |               56744.91 |
| TPC-DS Q7     |             3456.32 |               40.32 |            764.52 |                 391.47 |
| TPC-DS Q8     |              364.87 |               24.58 |            413.36 |                  67.03 |
| TPC-DS Q9     |             3794.93 |               44.56 |           4465.26 |                2411.42 |
| TPC-DS Q10    |               66.76 |               40.49 |            110.19 |                1198.87 |
| TPC-DS Q11    |             8303.47 |              286.17 |          19239.46 |                5394.96 |
| TPC-DS Q12    |              245.05 |               19.51 |            329.47 |                  68.53 |
| TPC-DS Q13    |             1113.38 |               36.74 |           1592.36 |                 554.97 |
| TPC-DS Q14a+b |            51229.39 |             1619.84 |          53091.93 |                2243.52 |
| TPC-DS Q15    |              167.53 |               21.86 |            218.14 |                 127.37 |
| TPC-DS Q16    |            11096.64 |               29.16 |             40.52 |                 200.08 |
| TPC-DS Q17    |              700.96 |               87.67 |            523.72 |                 319.90 |
| TPC-DS Q18    |             2630.50 |               51.98 |            985.97 |                 448.35 |
| TPC-DS Q19    |              330.03 |               35.66 |            335.08 |                 157.18 |
| TPC-DS Q20    |              715.60 |               25.65 |            590.45 |                 103.47 |
| TPC-DS Q21    |            22746.21 |               91.96 |          28284.38 |                 240.21 |
| TPC-DS Q22    |            19707.55 |              601.45 |           5238.65 |                3281.32 |
| TPC-DS Q23a+b |            48571.27 |              931.47 |          37725.15 |                4409.55 |
| TPC-DS Q24a+b |              113.23 |               96.94 |              7.72 |                  68.51 |
| TPC-DS Q25    |              153.21 |               86.47 |            205.32 |                 329.19 |
| TPC-DS Q26    |              842.92 |               21.74 |           5988.48 |                 255.62 |
| TPC-DS Q27    |             1651.73 |               69.45 |            663.32 |                  37.11 |
| TPC-DS Q28    |             2875.90 |               40.46 |           3832.27 |                 967.51 |
| TPC-DS Q29    |              102.59 |               87.01 |            102.30 |                 432.09 |
| TPC-DS Q30    |              107.28 |               22.42 |            484.51 |                9784.62 |
| TPC-DS Q31    |             1420.79 |               97.25 |          12891.37 |                1590.81 |
| TPC-DS Q32    |               10.50 |               18.83 |             72.97 |                  77.88 |
| TPC-DS Q33    |              172.76 |               37.26 |            280.77 |                 395.37 |
| TPC-DS Q34    |             3059.62 |               23.95 |           1104.95 |                  36.96 |
| TPC-DS Q35    |             1204.32 |               86.97 |          15505.95 |                1269.01 |
| TPC-DS Q36    |             1640.46 |               68.56 |           1447.38 |                  36.33 |
| TPC-DS Q37    |             3748.23 |               51.82 |             17.34 |                 330.60 |
| TPC-DS Q38    |             7278.31 |              100.62 |           8657.44 |                1549.03 |
| TPC-DS Q39a+b |             1324.02 |              994.31 |           2269.52 |                2840.46 |
| TPC-DS Q40    |              182.66 |               60.46 |            191.58 |                 121.62 |
| TPC-DS Q41    |              377.60 |                6.82 |           1642.05 |                 939.19 |
| TPC-DS Q42    |              236.92 |               19.27 |             29.94 |                  93.54 |
| TPC-DS Q43    |             1792.15 |               88.29 |           7439.54 |                 205.02 |
| TPC-DS Q44    |                2.51 |               29.23 |              4.11 |                   3.80 |
| TPC-DS Q45    |              133.03 |               13.30 |            147.83 |                  86.17 |
| TPC-DS Q46    |             3705.35 |               31.29 |           1309.52 |                  47.11 |
| TPC-DS Q47    |            14683.29 |              181.48 |           7752.92 |                1864.55 |
| TPC-DS Q48    |             1286.07 |               33.30 |            960.09 |                 628.72 |
| TPC-DS Q49    |              109.23 |               77.65 |            148.84 |                 469.40 |
| TPC-DS Q50    |               29.97 |               86.06 |             30.40 |                 402.97 |
| TPC-DS Q51    |             7701.86 |              296.95 |           6596.09 |                 848.40 |
| TPC-DS Q52    |              237.62 |               19.88 |             31.46 |                  90.09 |
| TPC-DS Q53    |              165.28 |               32.45 |            274.81 |                 119.58 |
| TPC-DS Q54    |             1075.95 |               23.63 |           2942.52 |                  93.97 |
| TPC-DS Q55    |              222.71 |               47.09 |             20.59 |                  92.94 |
| TPC-DS Q56    |              158.44 |               18.67 |            271.72 |                 382.90 |
| TPC-DS Q57    |             7105.27 |              100.06 |           3663.67 |                 886.70 |
| TPC-DS Q58    |             5900.95 |               71.05 |           6985.48 |                 420.83 |
| TPC-DS Q59    |             9142.01 |               92.86 |           6636.50 |                 438.84 |
| TPC-DS Q60    |              310.15 |               20.14 |            524.71 |                 370.96 |
| TPC-DS Q61    |              403.88 |               29.13 |              4.20 |                 126.37 |
| TPC-DS Q62    |             1688.50 |               32.73 |           3148.78 |                 123.43 |
| TPC-DS Q63    |              136.72 |               24.20 |            241.24 |                 116.66 |
| TPC-DS Q64    |              682.44 |              219.21 |            671.47 |                 794.19 |
| TPC-DS Q65    |             5936.94 |               83.40 |           7804.72 |                 585.48 |
| TPC-DS Q66    |             1262.40 |              118.57 |           2101.13 |                 217.39 |
| TPC-DS Q67    |             7199.29 |              259.66 |           8717.65 |                3031.33 |
| TPC-DS Q68    |             3224.74 |               46.28 |            367.85 |                  51.16 |
| TPC-DS Q69    |                3.41 |               40.05 |              4.36 |                 131.37 |
| TPC-DS Q70    |             8418.86 |               57.43 |          13118.65 |                 379.18 |
| TPC-DS Q71    |              510.77 |               28.27 |            540.13 |                 297.98 |
| TPC-DS Q72    |           401613.46 |              216.85 |          13805.81 |                1171.73 |
| TPC-DS Q73    |             2898.13 |               23.29 |           1111.53 |                  37.33 |
| TPC-DS Q74    |             6217.57 |              274.30 |           5597.28 |                1059.68 |
| TPC-DS Q75    |             5678.97 |              269.92 |           1828.96 |                 935.61 |
| TPC-DS Q76    |              461.37 |               34.35 |            451.22 |                 256.86 |
| TPC-DS Q77    |             6047.25 |               54.89 |           9962.10 |                 349.35 |
| TPC-DS Q78    |             6644.35 |              453.66 |          12574.28 |                1981.67 |
| TPC-DS Q79    |             3078.04 |               41.85 |           5108.32 |                 115.08 |
| TPC-DS Q80    |              555.12 |              291.98 |           9221.61 |                 528.19 |
| TPC-DS Q81    |              215.13 |               30.89 |           2149.25 |               38343.81 |
| TPC-DS Q82    |             4006.40 |               53.82 |             78.20 |                 352.27 |
| TPC-DS Q83    |              921.00 |               12.39 |            884.10 |                 106.52 |
| TPC-DS Q84    |               56.31 |               15.45 |             65.96 |                  35.73 |
| TPC-DS Q85    |              146.61 |              175.42 |            138.74 |                 353.35 |
| TPC-DS Q86    |              897.64 |               32.46 |           1207.67 |                 199.45 |
| TPC-DS Q87    |             7282.65 |              165.23 |           8495.23 |                1357.08 |
| TPC-DS Q88    |            25854.10 |               37.88 |           2003.47 |                2990.34 |
| TPC-DS Q89    |             1628.42 |               33.07 |            138.20 |                 121.76 |
| TPC-DS Q90    |              126.39 |               12.52 |            357.00 |                 131.28 |
| TPC-DS Q91    |               18.28 |               21.23 |             19.59 |                 151.97 |
| TPC-DS Q92    |                9.63 |               10.36 |             44.43 |                  59.74 |
| TPC-DS Q93    |               38.85 |               69.07 |             44.51 |                 224.03 |
| TPC-DS Q96    |             2699.18 |               13.14 |            143.16 |                 102.66 |
| TPC-DS Q97    |             5276.05 |              120.24 |           6358.82 |                 399.82 |
| TPC-DS Q98    |              871.08 |               34.69 |           1154.58 |                 213.02 |
| TPC-DS Q99    |             4969.72 |               42.64 |          12709.88 |                 193.28 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
bexhoma : Traceback (most recent call last):
In C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\scripts\test-docs-tpcds.ps1:25 Zeichen:1
+ bexhoma tpcds `
+ ~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\tpcds.py", line 250, in <module>
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 291, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\dbmsbenchmarker.py", line 120, in 
show_summary
    primary.show_summary(self)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 169, in show_summary
    extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 289, in 
_show_extra_sections
    list_errors = self.evaluator.evaluation.get_error(numQuery)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\dbmsbenchmarker\inspector.py", line 450, in get_error
    return self.benchmarks.getError(numQuery, connection)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\dbmsbenchmarker\benchmarker.py", line 1926, in getError
    return self.protocol['query'][str(query)]['errors']
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
KeyError: 'ariaDB-1-1-1-1-1'
