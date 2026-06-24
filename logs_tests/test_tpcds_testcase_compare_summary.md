## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 4408s 
* Code: 1782219800
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
  * disk:262406
  * datadisk:4535
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782219800
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:267892
  * datadisk:3447
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782219800
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263219
  * datadisk:38233
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782219800
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:267892
  * datadisk:5794
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782219800

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
| MariaDB-1-1    |                1 |    1 |      569.00 |           0.00 |            1.00 |         60.00 |          501.00 |              8 |           0 |             | None           |             0 | False         |                6.33 |
| MonetDB-1-1    |                1 |    1 |      350.00 |           0.00 |            1.00 |        123.00 |          219.00 |              8 |           0 |             | None           |             0 | False         |               10.29 |
| MySQL-1-1      |                1 |    1 |      929.00 |           0.00 |            1.00 |        121.00 |          800.00 |              8 |           0 |             | None           |             0 | False         |                3.88 |
| PostgreSQL-1-1 |                1 |    1 |      224.00 |           0.00 |            1.00 |         53.00 |          161.00 |              8 |           0 |             | None           |             0 | False         |               16.07 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3237 |            1.02 |             3550.08 |            107.88 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         20 |            0.06 |            63528.69 |          17460.00 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        551 |            0.83 |             4410.93 |            633.76 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        190 |            0.38 |             9622.23 |           1837.89 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3237 |            1.02 |             3550.08 |            107.88 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         20 |            0.06 |            63528.69 |          17460.00 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        551 |            0.83 |             4410.93 |            633.76 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        190 |            0.38 |             9622.23 |           1837.89 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:--------------|--------------------:|--------------------:|------------------:|-----------------------:|
| TPC-DS Q1     |               26.71 |               53.08 |             81.48 |                 115.80 |
| TPC-DS Q2     |             6948.20 |               96.37 |           7324.95 |                 320.16 |
| TPC-DS Q3     |               21.04 |               24.47 |             25.65 |                 221.67 |
| TPC-DS Q4     |            12312.46 |              609.24 |          33053.88 |                8983.63 |
| TPC-DS Q5     |             8462.02 |               70.41 |          16287.36 |                 479.62 |
| TPC-DS Q6     |              737.95 |               50.67 |          79310.94 |               52953.31 |
| TPC-DS Q7     |             3426.10 |               42.02 |            784.67 |                 395.26 |
| TPC-DS Q8     |              349.52 |               23.52 |            432.16 |                  68.73 |
| TPC-DS Q9     |             3858.53 |               43.84 |           4863.55 |                2476.80 |
| TPC-DS Q10    |               56.90 |               40.70 |             93.52 |                1195.06 |
| TPC-DS Q11    |             8236.48 |              290.42 |          19014.71 |                5368.37 |
| TPC-DS Q12    |              250.67 |               18.19 |            377.84 |                  73.88 |
| TPC-DS Q13    |             1054.78 |               36.65 |           1574.61 |                 658.99 |
| TPC-DS Q14a+b |            55432.85 |             1568.22 |          56555.16 |                2154.85 |
| TPC-DS Q15    |              251.41 |               24.34 |            212.79 |                 128.66 |
| TPC-DS Q16    |            11655.39 |               29.62 |             77.38 |                 215.89 |
| TPC-DS Q17    |              764.10 |               93.45 |            528.85 |                 339.79 |
| TPC-DS Q18    |             1877.22 |               53.90 |            989.17 |                 408.78 |
| TPC-DS Q19    |              232.27 |               34.76 |            363.89 |                 164.27 |
| TPC-DS Q20    |              440.94 |               22.29 |            601.57 |                 112.87 |
| TPC-DS Q21    |            21334.13 |               78.30 |          29082.67 |                 235.19 |
| TPC-DS Q22    |            19858.84 |              637.41 |           5497.97 |                3175.05 |
| TPC-DS Q23a+b |            58761.12 |             1173.89 |          42770.50 |                5555.38 |
| TPC-DS Q24a+b |               83.89 |              100.82 |             64.58 |                 409.51 |
| TPC-DS Q25    |              189.70 |              104.23 |            153.49 |                 327.05 |
| TPC-DS Q26    |              867.27 |               19.37 |           5624.39 |                 267.67 |
| TPC-DS Q27    |             1664.06 |               56.85 |            613.04 |                  35.12 |
| TPC-DS Q28    |             2833.13 |               41.62 |           3775.24 |                 853.99 |
| TPC-DS Q29    |               96.68 |               88.20 |             93.59 |                 355.78 |
| TPC-DS Q30    |              105.77 |               22.97 |            477.37 |                8753.15 |
| TPC-DS Q31    |             1399.05 |              102.37 |          13055.21 |                1522.92 |
| TPC-DS Q32    |               11.42 |               16.97 |            183.61 |                 104.26 |
| TPC-DS Q33    |              184.56 |               25.47 |            294.32 |                 401.91 |
| TPC-DS Q34    |             2993.66 |               25.36 |           1074.68 |                  40.52 |
| TPC-DS Q35    |             1207.55 |               80.12 |          15330.63 |                1642.96 |
| TPC-DS Q36    |             1649.69 |               62.33 |           1457.13 |                  36.74 |
| TPC-DS Q37    |             3745.58 |               48.51 |             13.57 |                 407.41 |
| TPC-DS Q38    |            10393.56 |              102.63 |           9216.57 |                1851.33 |
| TPC-DS Q39a+b |             1173.27 |             1041.05 |           2150.89 |                2776.01 |
| TPC-DS Q40    |              178.32 |               56.10 |            199.56 |                 133.10 |
| TPC-DS Q41    |               33.53 |                7.28 |            125.82 |                 276.57 |
| TPC-DS Q42    |              241.00 |               20.80 |             30.69 |                  95.59 |
| TPC-DS Q43    |             1147.94 |               39.52 |              2.51 |                  36.66 |
| TPC-DS Q44    |             1155.07 |               36.11 |           1634.61 |                 429.43 |
| TPC-DS Q45    |              135.34 |               14.19 |            139.73 |                  91.65 |
| TPC-DS Q46    |             3148.31 |               35.13 |            424.78 |                  48.64 |
| TPC-DS Q47    |            15003.55 |              181.25 |           7935.74 |                1867.39 |
| TPC-DS Q48    |             1247.94 |               32.54 |           1405.70 |                 636.76 |
| TPC-DS Q49    |              110.88 |               75.54 |            145.03 |                 477.90 |
| TPC-DS Q50    |               31.17 |               99.68 |             34.13 |                 443.43 |
| TPC-DS Q51    |             7753.65 |              303.25 |           6750.35 |                 849.60 |
| TPC-DS Q52    |              320.31 |               56.13 |             30.95 |                  94.66 |
| TPC-DS Q53    |              165.01 |               29.08 |            284.03 |                 127.63 |
| TPC-DS Q54    |             1153.94 |               27.30 |           2994.28 |                  81.04 |
| TPC-DS Q55    |              237.46 |               16.80 |             21.66 |                  93.27 |
| TPC-DS Q56    |              177.59 |               20.62 |            247.71 |                 416.98 |
| TPC-DS Q57    |             7205.46 |              108.35 |           3697.34 |                 820.70 |
| TPC-DS Q58    |             5932.96 |               55.26 |           7152.69 |                 497.72 |
| TPC-DS Q59    |             9267.74 |               94.85 |           6763.84 |                 479.91 |
| TPC-DS Q60    |              768.71 |               20.96 |            529.69 |                 501.27 |
| TPC-DS Q61    |              405.86 |               27.51 |              3.28 |                 194.99 |
| TPC-DS Q62    |             2286.94 |               33.32 |           3089.40 |                 141.93 |
| TPC-DS Q63    |              159.64 |               24.34 |            263.09 |                 128.86 |
| TPC-DS Q64    |              588.76 |              220.02 |            402.71 |                 844.53 |
| TPC-DS Q65    |             5929.87 |               88.17 |           8119.52 |                 773.26 |
| TPC-DS Q66    |             1301.97 |              106.78 |           2748.58 |                 262.74 |
| TPC-DS Q67    |             8968.14 |              248.23 |           9086.35 |                3271.20 |
| TPC-DS Q68    |             3274.28 |               34.51 |            368.58 |                  48.21 |
| TPC-DS Q69    |                3.65 |               27.51 |              4.46 |                 120.63 |
| TPC-DS Q70    |             8642.14 |               64.45 |          13258.87 |                 377.98 |
| TPC-DS Q71    |              521.54 |               27.42 |            516.36 |                 306.82 |
| TPC-DS Q72    |           408624.92 |              198.61 |          14078.39 |                1127.51 |
| TPC-DS Q73    |             2851.68 |               23.38 |           1094.42 |                  36.30 |
| TPC-DS Q74    |             6151.54 |               99.88 |           5685.28 |                1383.38 |
| TPC-DS Q75    |             6202.51 |              255.79 |           1751.02 |                1018.62 |
| TPC-DS Q76    |              466.17 |               39.53 |            432.75 |                 231.63 |
| TPC-DS Q77    |             6285.48 |               57.62 |          10025.60 |                 339.91 |
| TPC-DS Q78    |             5738.32 |              433.20 |          12473.94 |                1349.99 |
| TPC-DS Q79    |             3092.40 |               38.95 |           5250.05 |                 111.66 |
| TPC-DS Q80    |              534.10 |              312.03 |           9445.11 |                 477.50 |
| TPC-DS Q81    |              214.21 |               39.79 |           2137.09 |               44464.79 |
| TPC-DS Q82    |             3725.49 |               53.28 |             28.47 |                 357.21 |
| TPC-DS Q83    |              937.42 |               12.69 |            878.78 |                 103.20 |
| TPC-DS Q84    |               64.25 |               15.21 |             64.87 |                  91.21 |
| TPC-DS Q85    |              123.87 |              190.90 |            108.40 |                 345.59 |
| TPC-DS Q86    |              971.41 |               30.17 |           1198.77 |                 210.74 |
| TPC-DS Q87    |            10280.54 |              146.41 |           8568.96 |                1387.98 |
| TPC-DS Q88    |            23723.78 |               41.09 |           2051.35 |                3024.10 |
| TPC-DS Q89    |             1494.23 |               35.49 |             56.66 |                 117.77 |
| TPC-DS Q90    |              360.88 |               14.81 |            375.76 |                 132.84 |
| TPC-DS Q91    |               28.50 |               22.19 |             22.09 |                 111.26 |
| TPC-DS Q92    |                9.64 |               12.05 |             21.00 |                  62.76 |
| TPC-DS Q93    |               44.53 |               68.66 |             44.15 |                 227.99 |
| TPC-DS Q96    |             2682.34 |               13.68 |            193.03 |                 104.89 |
| TPC-DS Q97    |             5202.48 |              132.31 |           8135.01 |                 405.32 |
| TPC-DS Q98    |              863.67 |               36.50 |           1351.19 |                 184.17 |
| TPC-DS Q99    |             4916.78 |               47.03 |          18285.00 |                 178.75 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
Traceback (most recent call last):
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/tpcds.py", line 250, in <module>
    experiment.process()
    ~~~~~~~~~~~~~~~~~~^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/base.py", line 291, in process
    self.show_summary()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/experiments/dbmsbenchmarker.py", line 120, in show_summary
    primary.show_summary(self)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/benchmarks/base.py", line 170, in show_summary
    extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)
  File "/home/perdelt/Git-projects/Benchmark-Experiment-Host-Manager/bexhoma/benchmarks/base.py", line 290, in _show_extra_sections
    list_errors = self.evaluator.evaluation.get_error(numQuery)
  File "/home/perdelt/anaconda3/envs/bexhoma/lib/python3.14/site-packages/dbmsbenchmarker/inspector.py", line 450, in get_error
    return self.benchmarks.getError(numQuery, connection)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/home/perdelt/anaconda3/envs/bexhoma/lib/python3.14/site-packages/dbmsbenchmarker/benchmarker.py", line 1926, in getError
    return self.protocol['query'][str(query)]['errors']
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
KeyError: 'ariaDB-1-1-1-1-1'
