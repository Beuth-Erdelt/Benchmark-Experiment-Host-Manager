## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1339s 
* Code: 1794058579
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:811242
  * datadisk:4462
  * volume_size:1.8T
  * volume_used:793G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794058579
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:811243
  * datadisk:4462
  * volume_size:1.8T
  * volume_used:793G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794058579
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:811243
  * datadisk:4462
  * volume_size:1.8T
  * volume_used:793G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794058579

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794058579-5d4bbbf654-rg5gx: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      173.00 |           4.00 |            1.00 |         64.00 |           96.00 |              8 |           0 |             | None           |             0 | False         |               20.81 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        342 |            0.72 |             4978.18 |           1042.11 |          -1 | mariadb-1-1-1-1-1 |
| mariadb-1-1-2-1-1 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        375 |            0.71 |             5087.26 |            950.40 |          -1 | mariadb-1-1-2-1-1 |
| mariadb-1-1-2-1-2 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        374 |            0.72 |             4989.97 |            952.94 |          -1 | mariadb-1-1-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        342 |            0.72 |             4978.18 |           1042.11 |          -1 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        375 |            0.71 |             5038.38 |           1900.80 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase         | job             |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:--------------|:----------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |         5.00 |                |
| mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |         4.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-1-2-1-1 |   mariadb-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               11.84 |               12.16 |               11.87 |
| TPC-DS Q2     |             3831.26 |             3922.42 |             3920.69 |
| TPC-DS Q3     |                8.87 |                8.05 |                9.07 |
| TPC-DS Q4     |             9058.61 |            10178.85 |             9974.04 |
| TPC-DS Q5     |             8707.98 |             9834.43 |             9480.48 |
| TPC-DS Q6     |              987.07 |              706.28 |              730.71 |
| TPC-DS Q7     |             3197.74 |             3970.85 |             3901.29 |
| TPC-DS Q8     |              335.50 |              322.21 |              329.21 |
| TPC-DS Q9     |             3352.49 |             3872.71 |             3882.39 |
| TPC-DS Q10    |               71.87 |               61.50 |               61.11 |
| TPC-DS Q11    |             7149.19 |             6707.95 |             6790.82 |
| TPC-DS Q12    |              219.34 |              235.55 |              220.06 |
| TPC-DS Q13    |              759.32 |              793.19 |              865.73 |
| TPC-DS Q14a+b |            42183.64 |            46093.65 |            46160.05 |
| TPC-DS Q15    |              123.25 |              138.63 |              145.14 |
| TPC-DS Q16    |             7623.55 |             9344.31 |             9497.84 |
| TPC-DS Q17    |              513.76 |              908.59 |              908.80 |
| TPC-DS Q18    |             1459.79 |             3056.00 |             2660.41 |
| TPC-DS Q19    |              197.48 |              221.16 |              288.38 |
| TPC-DS Q20    |              358.30 |              470.40 |              475.79 |
| TPC-DS Q21    |              934.88 |             1423.65 |             1423.81 |
| TPC-DS Q22    |            14980.45 |            16624.88 |            17024.22 |
| TPC-DS Q23a+b |            48674.68 |            53749.14 |            53018.09 |
| TPC-DS Q24a+b |               27.25 |               24.59 |               25.81 |
| TPC-DS Q25    |              121.64 |              104.91 |              144.07 |
| TPC-DS Q26    |             1225.26 |              571.21 |              682.02 |
| TPC-DS Q27    |             2669.29 |             3175.25 |             3204.39 |
| TPC-DS Q28    |             2621.90 |             2535.97 |             2564.84 |
| TPC-DS Q29    |               79.05 |               55.75 |               68.44 |
| TPC-DS Q30    |               85.72 |               70.33 |               76.24 |
| TPC-DS Q31    |             1010.55 |             1023.22 |             1062.96 |
| TPC-DS Q32    |                4.70 |                5.19 |                5.13 |
| TPC-DS Q33    |              116.61 |              123.19 |              123.52 |
| TPC-DS Q34    |             2305.65 |             3304.58 |             3212.83 |
| TPC-DS Q35    |              869.22 |              879.75 |              947.71 |
| TPC-DS Q36    |             3215.84 |             3356.14 |             3356.44 |
| TPC-DS Q37    |             2980.96 |             3862.88 |             3863.15 |
| TPC-DS Q38    |             6716.02 |             6960.31 |             6961.77 |
| TPC-DS Q39a+b |             1071.38 |             1054.85 |             1057.69 |
| TPC-DS Q40    |              146.16 |              131.86 |              129.11 |
| TPC-DS Q41    |              395.03 |              352.44 |              353.43 |
| TPC-DS Q42    |              236.23 |              233.23 |              233.61 |
| TPC-DS Q43    |              981.64 |              967.55 |              968.53 |
| TPC-DS Q44    |                1.78 |                1.50 |                1.70 |
| TPC-DS Q45    |              119.42 |              245.78 |              121.81 |
| TPC-DS Q46    |             3195.56 |             3237.95 |             3419.90 |
| TPC-DS Q47    |            15374.48 |            14424.37 |            14324.62 |
| TPC-DS Q48    |              990.72 |              998.57 |             1007.63 |
| TPC-DS Q49    |              107.03 |              102.41 |              103.13 |
| TPC-DS Q50    |               30.48 |               21.84 |               24.27 |
| TPC-DS Q51    |             6351.81 |             6995.59 |             6866.23 |
| TPC-DS Q52    |              188.11 |              146.88 |              198.81 |
| TPC-DS Q53    |              109.85 |               97.80 |               99.46 |
| TPC-DS Q54    |             1160.59 |              834.25 |              898.70 |
| TPC-DS Q55    |              307.40 |              162.46 |              196.50 |
| TPC-DS Q56    |              347.82 |              198.61 |              212.72 |
| TPC-DS Q57    |             5713.04 |             4898.74 |             4993.63 |
| TPC-DS Q58    |             5148.66 |             5698.39 |             5689.28 |
| TPC-DS Q59    |             7587.38 |             8110.92 |             8188.77 |
| TPC-DS Q60    |              306.61 |              215.30 |              222.70 |
| TPC-DS Q61    |              387.84 |              233.79 |              263.09 |
| TPC-DS Q62    |             1405.69 |             1610.28 |             1560.51 |
| TPC-DS Q63    |              144.68 |              116.42 |              162.49 |
| TPC-DS Q64    |              632.23 |              446.00 |              452.06 |
| TPC-DS Q65    |             5756.42 |             5977.29 |             5989.37 |
| TPC-DS Q66    |             1200.80 |             1013.45 |             1062.66 |
| TPC-DS Q67    |             6519.91 |             6297.10 |             6256.53 |
| TPC-DS Q68    |             2970.45 |             3154.86 |             3128.11 |
| TPC-DS Q69    |                1.93 |                1.19 |                1.45 |
| TPC-DS Q70    |             7706.34 |             7808.07 |             7847.16 |
| TPC-DS Q71    |              547.62 |              320.90 |              388.26 |
| TPC-DS Q72    |             1010.52 |              820.02 |              819.87 |
| TPC-DS Q73    |             3205.65 |             3195.32 |             3195.57 |
| TPC-DS Q74    |             6297.28 |             5038.50 |             5042.09 |
| TPC-DS Q75    |             5448.64 |             4618.96 |             4620.78 |
| TPC-DS Q76    |              447.30 |              442.53 |              440.77 |
| TPC-DS Q77    |             6272.57 |             6267.86 |             6268.36 |
| TPC-DS Q78    |             5642.29 |             4957.75 |             4967.23 |
| TPC-DS Q79    |             2940.22 |             3143.66 |             3150.37 |
| TPC-DS Q80    |              679.12 |              578.84 |              578.49 |
| TPC-DS Q81    |              174.32 |              179.41 |              179.63 |
| TPC-DS Q82    |             3623.28 |             3618.45 |             3525.80 |
| TPC-DS Q83    |              792.48 |              802.10 |              809.90 |
| TPC-DS Q84    |               43.36 |               34.96 |               38.20 |
| TPC-DS Q85    |              151.66 |               93.36 |               96.82 |
| TPC-DS Q86    |             1243.79 |             1064.34 |              701.56 |
| TPC-DS Q87    |             6730.53 |             6478.97 |             6752.86 |
| TPC-DS Q88    |            11785.09 |            27479.00 |            27259.66 |
| TPC-DS Q89    |             1629.49 |             1068.73 |             1106.84 |
| TPC-DS Q90    |              117.67 |              250.66 |              253.16 |
| TPC-DS Q91    |               20.95 |               12.02 |               12.04 |
| TPC-DS Q92    |                6.34 |                6.25 |                4.77 |
| TPC-DS Q93    |               43.32 |               28.29 |               26.28 |
| TPC-DS Q94    |              404.31 |              359.29 |              369.60 |
| TPC-DS Q95    |              642.15 |              603.98 |              602.24 |
| TPC-DS Q96    |              687.05 |             2409.23 |             2374.15 |
| TPC-DS Q97    |             4526.02 |             5393.08 |             4882.74 |
| TPC-DS Q98    |              698.68 |              842.16 |              992.64 |
| TPC-DS Q99    |             2923.91 |             2842.72 |             2953.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
* TEST passed: Reset scripts ran without errors
