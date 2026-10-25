## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1999s 
* Code: 1792653852
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.7.
  * Experiment is limited to DBMS ['MySQL'].
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
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:1061948
  * datadisk:37664
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792653852
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:1061954
  * datadisk:37664
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792653852
* mysql-1-1-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:1061954
  * datadisk:37664
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792653852

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792653852-fdcbf8b7d-f995s: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      196.00 |           5.00 |            1.00 |         53.00 |          127.00 |              8 |           0 |             | None           |             0 | False         |               18.37 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        470 |            0.69 |             5225.28 |            758.30 |          -1 | mysql-1-1-1-1-1 |
| mysql-1-1-2-1-1 | MySQL-1         | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        518 |            0.74 |             4869.88 |            688.03 |          -1 | mysql-1-1-2-1-1 |
| mysql-1-1-2-1-2 | MySQL-1         | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        518 |            0.74 |             4869.42 |            688.03 |          -1 | mysql-1-1-2-1-2 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        470 |            0.69 |             5225.28 |            758.30 |          -1 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        518 |            0.74 |             4869.65 |           1376.06 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase       | job           |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:------------|:--------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       175.00 |                |
| mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |         6.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-1-1-2-1-2 |
|:--------------|------------------:|------------------:|------------------:|
| TPC-DS Q1     |             66.75 |            235.55 |            192.55 |
| TPC-DS Q2     |           3615.70 |           4522.52 |           3853.62 |
| TPC-DS Q3     |              9.91 |              8.51 |              9.64 |
| TPC-DS Q4     |          53624.59 |          54050.30 |          54390.92 |
| TPC-DS Q5     |          14189.96 |          15511.72 |          15554.24 |
| TPC-DS Q6     |          58905.10 |          59317.18 |          59070.96 |
| TPC-DS Q7     |           1501.27 |            443.01 |            538.88 |
| TPC-DS Q8     |            318.87 |            243.34 |            276.70 |
| TPC-DS Q9     |           3471.79 |           3441.15 |           3461.88 |
| TPC-DS Q10    |            249.65 |             31.74 |             53.19 |
| TPC-DS Q11    |          35366.17 |          34443.09 |          34559.79 |
| TPC-DS Q12    |            246.91 |            271.45 |            242.28 |
| TPC-DS Q13    |           2057.26 |            945.26 |            960.87 |
| TPC-DS Q14a+b |          34675.08 |          39976.62 |          40812.12 |
| TPC-DS Q15    |            157.61 |            141.98 |            128.10 |
| TPC-DS Q16    |            449.78 |            109.78 |             98.09 |
| TPC-DS Q17    |            923.25 |            467.66 |            445.28 |
| TPC-DS Q18    |           1183.19 |            631.14 |            626.73 |
| TPC-DS Q19    |            251.04 |            248.92 |            249.78 |
| TPC-DS Q20    |            413.57 |            469.74 |            473.40 |
| TPC-DS Q21    |           1307.08 |           1534.94 |           1381.73 |
| TPC-DS Q22    |           3736.35 |           3950.34 |           3914.47 |
| TPC-DS Q23a+b |          43793.05 |          47919.77 |          47904.35 |
| TPC-DS Q24a+b |             45.60 |           1153.68 |           1137.60 |
| TPC-DS Q25    |            189.70 |            152.36 |            146.30 |
| TPC-DS Q26    |            435.63 |            428.94 |            428.91 |
| TPC-DS Q27    |            402.82 |            436.38 |            436.01 |
| TPC-DS Q28    |           2730.28 |           2731.91 |           2731.67 |
| TPC-DS Q29    |            110.96 |             80.76 |             91.81 |
| TPC-DS Q30    |            408.16 |            381.09 |            390.32 |
| TPC-DS Q31    |           8871.86 |          11927.42 |          11966.40 |
| TPC-DS Q32    |            240.04 |            304.38 |            306.44 |
| TPC-DS Q33    |            522.63 |            863.17 |            863.05 |
| TPC-DS Q34    |            922.27 |            926.46 |            891.75 |
| TPC-DS Q35    |          11705.23 |          13192.35 |          13310.65 |
| TPC-DS Q36    |           1076.42 |           1222.04 |           1180.36 |
| TPC-DS Q37    |              7.62 |              6.97 |              6.87 |
| TPC-DS Q38    |           5824.73 |           7195.71 |           7137.27 |
| TPC-DS Q39a+b |            905.91 |           1186.24 |           1038.24 |
| TPC-DS Q40    |            689.59 |            123.02 |            141.86 |
| TPC-DS Q41    |           1134.69 |           1129.61 |           1133.92 |
| TPC-DS Q42    |             18.11 |             17.47 |             16.37 |
| TPC-DS Q43    |           6102.46 |           6574.09 |           6637.24 |
| TPC-DS Q44    |              6.93 |              2.41 |              1.62 |
| TPC-DS Q45    |            105.48 |             93.11 |            103.85 |
| TPC-DS Q46    |            886.86 |           1055.06 |           1111.73 |
| TPC-DS Q47    |           9429.69 |          10222.87 |          10234.57 |
| TPC-DS Q48    |           1060.03 |           1549.71 |           1550.40 |
| TPC-DS Q49    |            110.40 |            115.29 |            115.71 |
| TPC-DS Q50    |             21.42 |             21.06 |             21.26 |
| TPC-DS Q51    |           6890.59 |           8355.98 |           8359.60 |
| TPC-DS Q52    |             19.58 |             27.83 |             27.56 |
| TPC-DS Q53    |            184.85 |            242.39 |            240.64 |
| TPC-DS Q54    |           2460.76 |           3250.67 |           3251.23 |
| TPC-DS Q55    |             12.82 |             12.83 |             12.04 |
| TPC-DS Q56    |            206.53 |            278.33 |            277.89 |
| TPC-DS Q57    |           5681.51 |           4673.26 |           4684.17 |
| TPC-DS Q58    |           4867.03 |           6496.93 |           6496.60 |
| TPC-DS Q59    |           4644.42 |           5208.04 |           5206.70 |
| TPC-DS Q60    |            339.97 |            463.47 |            463.51 |
| TPC-DS Q61    |              1.83 |              3.36 |              3.03 |
| TPC-DS Q62    |           2351.78 |           2478.45 |           2490.91 |
| TPC-DS Q63    |            188.48 |            213.80 |            213.65 |
| TPC-DS Q64    |            315.72 |            326.23 |            345.32 |
| TPC-DS Q65    |           5344.46 |           7316.05 |           7316.36 |
| TPC-DS Q66    |           2214.50 |           2625.69 |           2650.50 |
| TPC-DS Q67    |           6647.09 |           7826.67 |           7824.02 |
| TPC-DS Q68    |            253.81 |            384.91 |            385.07 |
| TPC-DS Q69    |              2.23 |              2.67 |              2.49 |
| TPC-DS Q70    |           9106.94 |          11358.49 |          11425.98 |
| TPC-DS Q71    |            394.87 |            348.84 |            385.81 |
| TPC-DS Q72    |           9358.61 |          15318.25 |          15318.02 |
| TPC-DS Q73    |            861.62 |           1238.57 |           1238.34 |
| TPC-DS Q74    |           6708.65 |           8011.58 |           8013.03 |
| TPC-DS Q75    |           1757.93 |           2018.27 |           2005.22 |
| TPC-DS Q76    |            410.61 |            523.99 |            524.00 |
| TPC-DS Q77    |           7163.74 |           9904.95 |           9905.54 |
| TPC-DS Q78    |          13514.87 |          15739.11 |          15607.29 |
| TPC-DS Q79    |           3765.03 |           5152.07 |           5205.14 |
| TPC-DS Q80    |           8119.71 |           8974.00 |           8972.20 |
| TPC-DS Q81    |            342.00 |            346.15 |            346.01 |
| TPC-DS Q82    |             11.21 |             12.15 |             12.48 |
| TPC-DS Q83    |            610.59 |            782.45 |            788.04 |
| TPC-DS Q84    |             50.44 |             62.96 |             62.60 |
| TPC-DS Q85    |            101.08 |            122.66 |            122.48 |
| TPC-DS Q86    |            858.33 |           1083.10 |           1087.37 |
| TPC-DS Q87    |           5891.02 |           7473.12 |           7475.58 |
| TPC-DS Q88    |           1825.06 |           2107.30 |           2108.02 |
| TPC-DS Q89    |            165.93 |            204.41 |            205.39 |
| TPC-DS Q90    |            290.43 |            387.80 |            387.71 |
| TPC-DS Q91    |             13.19 |             17.11 |             17.20 |
| TPC-DS Q92    |             24.92 |             33.68 |             33.61 |
| TPC-DS Q93    |             36.37 |             31.53 |             33.99 |
| TPC-DS Q94    |            394.58 |            368.46 |            387.59 |
| TPC-DS Q95    |           2869.05 |           3170.35 |           3201.29 |
| TPC-DS Q96    |            140.70 |            152.35 |            150.75 |
| TPC-DS Q97    |           6291.02 |           7882.25 |           7914.91 |
| TPC-DS Q98    |            811.58 |           1151.08 |           1155.30 |
| TPC-DS Q99    |           8964.15 |          15608.97 |          15614.31 |

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
* TEST passed: Reset scripts ran without errors
