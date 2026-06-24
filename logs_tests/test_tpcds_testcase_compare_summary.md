## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 5589s 
* Code: 1782315025
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
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
  * disk:224991
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782315025
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223911
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782315025
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263208
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782315025
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:229014
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782315025

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
| MariaDB-1-1    |                1 |    1 |      647.00 |           2.00 |            1.00 |         67.00 |          571.00 |              8 |           0 |             | None           |             0 | False         |                5.56 |
| MonetDB-1-1    |                1 |    1 |      276.00 |           2.00 |            1.00 |         84.00 |          183.00 |              8 |           0 |             | None           |             0 | False         |               13.04 |
| MySQL-1-1      |                1 |    1 |      822.00 |           2.00 |            1.00 |         90.00 |          720.00 |              8 |           0 |             | None           |             0 | False         |                4.38 |
| PostgreSQL-1-1 |                1 |    1 |      325.00 |           2.00 |            0.00 |         54.00 |          262.00 |              8 |           0 |             | None           |             0 | False         |               11.08 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3248 |            1.07 |             3379.79 |            107.51 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         23 |            0.07 |            54065.32 |          15182.61 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        520 |            0.86 |             4208.12 |            671.54 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        181 |            0.40 |             9158.95 |           1929.28 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3248 |            1.07 |             3379.79 |            107.51 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         23 |            0.07 |            54065.32 |          15182.61 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        520 |            0.86 |             4208.12 |            671.54 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        181 |            0.40 |             9158.95 |           1929.28 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:--------------|--------------------:|--------------------:|------------------:|-----------------------:|
| TPC-DS Q1     |               20.48 |               57.60 |             67.62 |                 127.76 |
| TPC-DS Q2     |             5352.61 |              100.86 |           5136.17 |                 313.49 |
| TPC-DS Q3     |               21.44 |               23.34 |             15.04 |                 190.27 |
| TPC-DS Q4     |            13034.54 |              649.67 |          26470.71 |                8830.90 |
| TPC-DS Q5     |            11228.31 |               69.64 |          13192.74 |                 529.04 |
| TPC-DS Q6     |             1059.50 |               56.20 |          76860.47 |               51730.42 |
| TPC-DS Q7     |             4264.98 |               44.79 |            838.24 |                 394.68 |
| TPC-DS Q8     |              460.45 |               25.90 |            394.80 |                  66.14 |
| TPC-DS Q9     |             4646.04 |               52.27 |           5853.43 |                2421.21 |
| TPC-DS Q10    |              101.53 |               51.57 |            121.52 |                1203.38 |
| TPC-DS Q11    |             9915.73 |              300.07 |          17615.36 |                5346.71 |
| TPC-DS Q12    |              288.88 |               19.00 |            327.74 |                  74.19 |
| TPC-DS Q13    |             1335.15 |               36.58 |           1082.76 |                 644.82 |
| TPC-DS Q14a+b |            57378.54 |             1339.72 |          54238.20 |                2373.43 |
| TPC-DS Q15    |              207.40 |               22.15 |            282.40 |                 140.62 |
| TPC-DS Q16    |            12067.45 |               29.63 |             25.12 |                 247.19 |
| TPC-DS Q17    |              797.93 |               86.88 |            612.56 |                 394.24 |
| TPC-DS Q18    |             2024.63 |               54.37 |           1079.49 |                 552.69 |
| TPC-DS Q19    |              318.65 |               36.66 |            355.61 |                 198.32 |
| TPC-DS Q20    |              563.67 |               23.77 |            591.05 |                 122.92 |
| TPC-DS Q21    |            22308.51 |               92.74 |          28188.13 |                 287.68 |
| TPC-DS Q22    |            20335.43 |              672.31 |           5318.78 |                3945.24 |
| TPC-DS Q23a+b |            55452.27 |              919.08 |          34635.67 |                4632.19 |
| TPC-DS Q24a+b |               61.47 |              254.06 |           1316.15 |                 686.20 |
| TPC-DS Q25    |              119.93 |              105.86 |            118.49 |                 303.17 |
| TPC-DS Q26    |              853.75 |               22.04 |           5544.53 |                 250.08 |
| TPC-DS Q27    |             1674.05 |               65.28 |            645.59 |                  34.87 |
| TPC-DS Q28    |             2837.76 |               52.89 |           3767.15 |                 866.88 |
| TPC-DS Q29    |              102.60 |              129.34 |             93.49 |                 357.19 |
| TPC-DS Q30    |               44.75 |               16.42 |             82.57 |                 967.43 |
| TPC-DS Q31    |             1479.92 |              120.46 |          12894.10 |                1633.35 |
| TPC-DS Q32    |                9.99 |               15.91 |             36.20 |                  83.54 |
| TPC-DS Q33    |              200.13 |               46.55 |            256.15 |                 419.37 |
| TPC-DS Q34    |             3021.41 |               34.66 |           1091.52 |                  35.30 |
| TPC-DS Q35    |             1226.69 |               80.10 |          16157.84 |                1358.25 |
| TPC-DS Q36    |             3023.23 |              104.65 |           3131.01 |                 395.02 |
| TPC-DS Q37    |             3701.19 |               56.03 |             15.25 |                 341.94 |
| TPC-DS Q38    |             7061.07 |              117.04 |           9908.34 |                1417.16 |
| TPC-DS Q39a+b |             1206.96 |              986.97 |           2083.79 |                2577.82 |
| TPC-DS Q40    |              175.20 |               60.69 |            186.63 |                 124.79 |
| TPC-DS Q41    |              409.08 |               10.44 |           1578.69 |                 949.52 |
| TPC-DS Q42    |              228.19 |               61.56 |             29.20 |                  93.37 |
| TPC-DS Q43    |             1163.98 |               39.11 |              2.35 |                  35.53 |
| TPC-DS Q44    |             1169.99 |               33.89 |           1650.89 |                 503.30 |
| TPC-DS Q45    |              132.01 |               17.25 |            148.53 |                  86.40 |
| TPC-DS Q46    |             3321.08 |               33.86 |            875.24 |                  46.66 |
| TPC-DS Q47    |            11054.11 |              158.55 |           7341.45 |                2054.37 |
| TPC-DS Q48    |             1224.79 |               33.26 |           1681.80 |                 802.06 |
| TPC-DS Q49    |               92.61 |               81.83 |            155.27 |                 534.87 |
| TPC-DS Q50    |               28.83 |               94.93 |             30.50 |                 483.11 |
| TPC-DS Q51    |             7226.52 |              274.83 |           7104.13 |                1208.55 |
| TPC-DS Q52    |              229.83 |               21.39 |             29.57 |                  98.97 |
| TPC-DS Q53    |              133.38 |               24.76 |            253.96 |                 124.30 |
| TPC-DS Q54    |              994.88 |               22.85 |           2946.60 |                 118.34 |
| TPC-DS Q55    |              227.76 |               15.62 |             20.49 |                  97.95 |
| TPC-DS Q56    |              303.97 |               23.65 |            249.64 |                 512.65 |
| TPC-DS Q57    |             6142.73 |              114.77 |           3513.98 |                1124.15 |
| TPC-DS Q58    |             5961.96 |               56.29 |           7114.85 |                 488.01 |
| TPC-DS Q59    |             9225.27 |              115.08 |           6740.61 |                 518.45 |
| TPC-DS Q60    |              369.29 |               30.31 |            551.33 |                 486.84 |
| TPC-DS Q61    |              409.52 |               46.58 |              3.53 |                 199.07 |
| TPC-DS Q62    |             1600.98 |               35.94 |           3069.05 |                 123.41 |
| TPC-DS Q63    |              138.64 |               30.64 |            261.25 |                 124.87 |
| TPC-DS Q64    |              551.57 |              259.80 |            421.87 |                 848.12 |
| TPC-DS Q65    |             5728.92 |               97.88 |           7985.34 |                 730.85 |
| TPC-DS Q66    |             1194.76 |              141.23 |           2294.11 |                 250.71 |
| TPC-DS Q67    |             6960.68 |              277.24 |           8699.30 |                3220.69 |
| TPC-DS Q68    |             3084.19 |               56.04 |            369.73 |                  47.83 |
| TPC-DS Q69    |              395.25 |               57.72 |            560.72 |                 279.06 |
| TPC-DS Q70    |             8250.03 |               91.35 |          13029.15 |                 406.72 |
| TPC-DS Q71    |              471.64 |               40.48 |            545.66 |                 298.22 |
| TPC-DS Q72    |           424654.70 |              266.81 |          13695.37 |                1106.07 |
| TPC-DS Q73    |             2969.96 |               28.73 |            318.60 |                  36.52 |
| TPC-DS Q74    |             6138.38 |              323.96 |           5441.48 |                1063.13 |
| TPC-DS Q75    |             6193.24 |              326.02 |           1794.66 |                 783.01 |
| TPC-DS Q76    |              735.87 |               53.08 |            421.44 |                 232.18 |
| TPC-DS Q77    |             6296.54 |               77.65 |          10000.56 |                 368.29 |
| TPC-DS Q78    |             6153.42 |              516.81 |          12848.67 |                1457.41 |
| TPC-DS Q79    |             3340.31 |               60.01 |           5334.78 |                 185.68 |
| TPC-DS Q80    |              541.50 |              382.32 |           9178.80 |                 479.66 |
| TPC-DS Q81    |              219.63 |               43.03 |           2248.82 |               41407.74 |
| TPC-DS Q82    |             3719.13 |               86.94 |             15.69 |                 354.32 |
| TPC-DS Q83    |              915.28 |               14.21 |            901.14 |                  93.78 |
| TPC-DS Q84    |               55.60 |               20.49 |             66.91 |                  99.82 |
| TPC-DS Q85    |              123.55 |              184.25 |            118.53 |                 359.39 |
| TPC-DS Q86    |              937.07 |               33.86 |           1208.23 |                 190.68 |
| TPC-DS Q87    |             7259.95 |              170.26 |           8543.49 |                1396.46 |
| TPC-DS Q88    |            24745.58 |               56.73 |           2079.77 |                3027.40 |
| TPC-DS Q89    |             1693.89 |               46.82 |             93.56 |                 122.08 |
| TPC-DS Q90    |              127.55 |               21.01 |            382.13 |                 137.32 |
| TPC-DS Q91    |               22.52 |               48.57 |             20.89 |                 163.95 |
| TPC-DS Q92    |               11.10 |               13.38 |             83.13 |                  63.99 |
| TPC-DS Q93    |               42.95 |              101.87 |             45.50 |                 226.49 |
| TPC-DS Q96    |             2732.27 |               18.97 |            152.50 |                  99.51 |
| TPC-DS Q97    |             5253.66 |              138.03 |           6464.00 |                 403.58 |
| TPC-DS Q98    |              877.53 |               53.73 |           1169.17 |                 176.82 |
| TPC-DS Q99    |             4935.45 |               43.63 |          12958.26 |                 174.48 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
bexhoma : Traceback (most recent call last):
In Zeile:1 Zeichen:1
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
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 170, in show_summary
    extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 290, in 
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
