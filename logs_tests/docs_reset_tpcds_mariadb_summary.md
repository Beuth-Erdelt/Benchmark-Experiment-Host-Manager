## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 6308s 
* Code: 1792656017
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.7.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:1028769
  * datadisk:4466
  * volume_size:1.8T
  * volume_used:1005G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792656017
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:912548
  * datadisk:4466
  * volume_size:1.8T
  * volume_used:892G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792656017
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:912548
  * datadisk:4466
  * volume_size:1.8T
  * volume_used:892G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792656017

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1792656017-59b944bb78-zcb5l: 0

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
| MariaDB-1-1 |                1 |    1 |      173.00 |           5.00 |            1.00 |         67.00 |           88.00 |              8 |           0 |             | None           |             0 | False         |               20.81 | False               |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |                  97 |       2725 |            0.69 |             5230.74 |            128.15 |          -1 | mariadb-1-1-1-1-1 |
| mariadb-1-1-2-1-1 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               97 |                  97 |       2759 |            0.70 |             5133.81 |            126.57 |          -1 | mariadb-1-1-2-1-1 |
| mariadb-1-1-2-1-2 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               97 |                  97 |       2759 |            0.69 |             5231.67 |            126.57 |          -1 | mariadb-1-1-2-1-2 |

These totals cover 97 of 99 active queries: only queries that succeeded in every connection of this experiment count, so the others are left out of every row (Q94 failed in 3 of 3 connections; Q95 failed in 3 of 3 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |                  97 |       2725 |            0.69 |             5230.74 |            128.15 |          -1 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              194 |                 194 |       2759 |            0.69 |             5182.51 |            253.14 |          -1 |

These totals cover 97 of 99 active queries: only queries that succeeded in every connection of this experiment count, so the others are left out of every row (Q94 failed in 3 of 3 connections; Q95 failed in 3 of 3 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 0/1          | 0/1          | 1/1          | 1/1          | 1/1          | 1/1          | no         |
| mariadb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 0/2          | 0/2          | 2/2          | 2/2          | 2/2          | 2/2          | no         |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Per Phase (Complete Phases Only)

Only the 0 of 2 phases in which every pod completed every active query; each row covers all 99 active queries, so the rows are comparable with each other. Left out: mariadb-1-1-1, mariadb-1-1-2 - see Query Completion per Phase.

#### Reset

| phase         | job             |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:--------------|:----------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |         7.00 |                |
| mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |         4.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-1-2-1-1 |   mariadb-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               11.94 |               14.34 |               14.50 |
| TPC-DS Q2     |             3602.86 |             3694.34 |             3713.22 |
| TPC-DS Q3     |               15.46 |               14.40 |               10.04 |
| TPC-DS Q4     |             9718.81 |            11118.31 |            11598.79 |
| TPC-DS Q5     |             6696.23 |             7245.70 |             7282.47 |
| TPC-DS Q6     |              596.06 |              642.74 |              566.97 |
| TPC-DS Q7     |             2633.82 |             3524.45 |             3479.77 |
| TPC-DS Q8     |              252.66 |              267.59 |              243.72 |
| TPC-DS Q9     |             3346.63 |             3326.37 |             3319.16 |
| TPC-DS Q10    |               42.23 |               23.35 |               20.20 |
| TPC-DS Q11    |             6749.47 |             6809.16 |             6722.07 |
| TPC-DS Q12    |              192.67 |              191.97 |              190.93 |
| TPC-DS Q13    |              730.51 |              689.21 |              664.80 |
| TPC-DS Q14a+b |            39693.08 |            49554.77 |            48935.56 |
| TPC-DS Q15    |              120.26 |              152.33 |              152.01 |
| TPC-DS Q16    |             7032.45 |             8770.89 |             8771.08 |
| TPC-DS Q17    |              508.20 |              742.57 |              742.43 |
| TPC-DS Q18    |             1427.93 |             2047.62 |             2047.95 |
| TPC-DS Q19    |              169.62 |              227.66 |              227.09 |
| TPC-DS Q20    |              340.12 |              413.32 |              414.82 |
| TPC-DS Q21    |              904.98 |             1607.10 |             1606.98 |
| TPC-DS Q22    |            15089.41 |            23857.22 |            24043.78 |
| TPC-DS Q23a+b |            46566.85 |            59604.35 |            60398.24 |
| TPC-DS Q24a+b |               26.58 |               22.46 |               21.82 |
| TPC-DS Q25    |              149.16 |              114.45 |              101.39 |
| TPC-DS Q26    |              769.06 |              620.46 |              598.48 |
| TPC-DS Q27    |             2906.54 |             3167.42 |             3141.21 |
| TPC-DS Q28    |             2960.66 |             2551.35 |             2528.04 |
| TPC-DS Q29    |               70.18 |               59.56 |               62.04 |
| TPC-DS Q30    |               33.86 |               29.46 |               26.04 |
| TPC-DS Q31    |             1185.65 |             1030.98 |             1038.97 |
| TPC-DS Q32    |                9.57 |                7.85 |                8.15 |
| TPC-DS Q33    |              148.70 |              124.48 |              109.95 |
| TPC-DS Q34    |             2687.67 |             2606.36 |             2599.92 |
| TPC-DS Q35    |              925.09 |              800.88 |              818.51 |
| TPC-DS Q36    |             2355.93 |             2984.77 |             2976.05 |
| TPC-DS Q37    |             3427.43 |             3258.52 |             3247.45 |
| TPC-DS Q38    |             6601.00 |             6443.19 |             6412.84 |
| TPC-DS Q39a+b |             1142.14 |              991.05 |             1000.57 |
| TPC-DS Q40    |              155.36 |              133.50 |              127.34 |
| TPC-DS Q41    |              469.20 |              392.82 |              398.16 |
| TPC-DS Q42    |              233.16 |              164.36 |              157.65 |
| TPC-DS Q43    |             1443.08 |             1266.01 |             1239.83 |
| TPC-DS Q44    |                1.47 |                1.26 |                1.47 |
| TPC-DS Q45    |              114.69 |               96.75 |               93.10 |
| TPC-DS Q46    |             2587.76 |             2923.29 |             3089.89 |
| TPC-DS Q47    |            13355.19 |            14827.06 |            14685.52 |
| TPC-DS Q48    |              824.91 |              837.16 |              787.77 |
| TPC-DS Q49    |               92.56 |               95.47 |               80.06 |
| TPC-DS Q50    |               18.97 |               18.71 |               17.93 |
| TPC-DS Q51    |             6164.16 |             6729.24 |             6697.84 |
| TPC-DS Q52    |              157.34 |              156.53 |              150.01 |
| TPC-DS Q53    |              120.84 |              120.90 |              120.93 |
| TPC-DS Q54    |              835.70 |              853.91 |              830.09 |
| TPC-DS Q55    |              159.27 |              154.68 |              167.33 |
| TPC-DS Q56    |              117.31 |              113.62 |              108.93 |
| TPC-DS Q57    |             6299.07 |             6400.36 |             6398.49 |
| TPC-DS Q58    |             4462.50 |             5059.89 |             5491.39 |
| TPC-DS Q59    |             6818.67 |             8231.27 |             8015.72 |
| TPC-DS Q60    |              313.40 |              314.45 |              302.12 |
| TPC-DS Q61    |              258.47 |              264.84 |              256.71 |
| TPC-DS Q62    |             1324.49 |             1582.38 |             1443.29 |
| TPC-DS Q63    |              130.63 |              140.08 |              153.16 |
| TPC-DS Q64    |              442.10 |              432.81 |              419.72 |
| TPC-DS Q65    |             4315.01 |             5590.30 |             5513.34 |
| TPC-DS Q66    |              949.18 |              950.18 |              923.06 |
| TPC-DS Q67    |             6185.14 |             6744.56 |             6765.05 |
| TPC-DS Q68    |             2409.65 |             2808.07 |             2893.78 |
| TPC-DS Q69    |              270.60 |              264.77 |              256.42 |
| TPC-DS Q70    |             6601.17 |             7907.00 |             7836.19 |
| TPC-DS Q71    |              436.54 |              308.06 |              308.21 |
| TPC-DS Q72    |             8854.21 |             8485.93 |             8358.99 |
| TPC-DS Q73    |             2831.55 |             2505.73 |             2487.50 |
| TPC-DS Q74    |             6002.44 |             4877.53 |             4861.99 |
| TPC-DS Q75    |             4930.42 |             4194.06 |             4196.99 |
| TPC-DS Q76    |              827.60 |              638.51 |              648.03 |
| TPC-DS Q77    |             5912.41 |             5652.05 |             5636.88 |
| TPC-DS Q78    |             4188.88 |             4415.45 |             4389.38 |
| TPC-DS Q79    |             2709.66 |             3009.81 |             3082.38 |
| TPC-DS Q80    |              419.02 |              440.61 |              382.05 |
| TPC-DS Q81    |              165.31 |              160.84 |              161.85 |
| TPC-DS Q82    |             2926.19 |             3136.90 |             3134.29 |
| TPC-DS Q83    |              703.63 |              697.29 |              704.95 |
| TPC-DS Q84    |               38.64 |               38.59 |               36.56 |
| TPC-DS Q85    |              124.57 |               96.89 |               89.22 |
| TPC-DS Q86    |              744.50 |              748.60 |              878.85 |
| TPC-DS Q87    |             5585.70 |             6577.55 |             6460.03 |
| TPC-DS Q88    |             5383.67 |             6253.42 |             6248.11 |
| TPC-DS Q89    |             1037.42 |             1103.58 |             1038.98 |
| TPC-DS Q90    |               85.22 |               78.42 |               78.26 |
| TPC-DS Q91    |               10.43 |               10.34 |               10.21 |
| TPC-DS Q92    |                3.10 |                3.43 |                3.76 |
| TPC-DS Q93    |               24.25 |               24.66 |               23.22 |
| TPC-DS Q96    |              559.35 |              587.39 |              472.66 |
| TPC-DS Q97    |             4043.39 |             4911.54 |             4838.84 |
| TPC-DS Q98    |              678.13 |              823.59 |              824.13 |
| TPC-DS Q99    |             3855.87 |             4396.77 |             4322.26 |

These totals cover 97 of 99 active queries: only queries that succeeded in every connection of this experiment count, so the others are left out of every row (Q94 failed in 3 of 3 connections; Q95 failed in 3 of 3 connections). See Query Completion per Phase for where, and Per Phase (Complete Phases Only) for the phases that completed every query.

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| mariadb-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| mariadb-1-1-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| mariadb-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * mariadb-1-1-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=124) Query was interrupted: execution time limit 1200.0 sec exceeded
  * mariadb-1-1-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=125) Query was interrupted: execution time limit 1200.0 sec exceeded
  * mariadb-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=69) Query was interrupted: execution time limit 1200.0 sec exceeded
* TPC-DS Q95
  * mariadb-1-1-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=124) Query was interrupted: execution time limit 1200.0 sec exceeded
  * mariadb-1-1-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=125) Query was interrupted: execution time limit 1200.0 sec exceeded
  * mariadb-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=69) Query was interrupted: execution time limit 1200.0 sec exceeded

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST failed: Some active queries missing from the totals (see Per Phase table's num_of_queries column)
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
