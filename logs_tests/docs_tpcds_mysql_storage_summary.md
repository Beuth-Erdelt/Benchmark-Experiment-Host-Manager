## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 4392s 
* Code: 1795669559
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 150Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'volume': 'mysqltmp', 'field': 'sizeLimit', 'target': 'volume'}, '72Gi'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'sort_buffer_size', 'target': 'container'}, '32M'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'join_buffer_size', 'target': 'container'}, '64M'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'tmp_table_size', 'target': 'container'}, '1G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'max_heap_table_size', 'target': 'container'}, '1G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'temptable_max_ram', 'target': 'container'}, '4G')].
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622538
  * datadisk:45119
  * volume_size:147G
  * volume_used:45G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795669559
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636491
  * datadisk:45119
  * volume_size:147G
  * volume_used:45G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795669559
* mysql-1-1-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636491
  * datadisk:45119
  * volume_size:147G
  * volume_used:45G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795669559

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1795669559-8594fc57f4-kw9bv: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    3 |      848.00 |           3.00 |            1.00 |        188.00 |          648.00 |              8 |         0 |             | None           |             0 | False         |               12.74 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |       1458 |            3.34 |             3251.73 |            733.33 |          -1 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 | 3.00 |               99 |                  99 |       1586 |            2.61 |             4178.02 |            674.15 |          -1 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 | 3.00 |               99 |                  99 |       1588 |            2.68 |             4075.20 |            673.30 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1458 |            3.34 |             3251.73 |            733.33 |          -1 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |       1588 |            2.65 |             4126.29 |           1346.60 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-1-1-2-1-2 |
|:--------------|------------------:|------------------:|------------------:|
| TPC-DS Q1     |            204.73 |            277.84 |             69.97 |
| TPC-DS Q2     |          10748.99 |          14290.61 |          14184.49 |
| TPC-DS Q3     |             30.96 |             43.99 |             56.39 |
| TPC-DS Q4     |         117442.21 |         152320.71 |         153067.10 |
| TPC-DS Q5     |          32083.36 |          46296.55 |          44951.79 |
| TPC-DS Q6     |           4233.21 |           5168.20 |           4634.26 |
| TPC-DS Q7     |           6867.86 |            887.63 |           1289.47 |
| TPC-DS Q8     |           1383.66 |            770.01 |           1012.35 |
| TPC-DS Q9     |          16238.06 |          11955.16 |          11661.88 |
| TPC-DS Q10    |            996.94 |            115.74 |            172.01 |
| TPC-DS Q11    |          73419.38 |          74977.91 |          78257.84 |
| TPC-DS Q12    |            779.83 |            768.20 |            696.45 |
| TPC-DS Q13    |          10938.97 |           3267.88 |           4264.68 |
| TPC-DS Q14a+b |         165357.51 |         223788.09 |         216342.44 |
| TPC-DS Q15    |            431.91 |            493.38 |            450.65 |
| TPC-DS Q16    |           1136.99 |            217.67 |            199.25 |
| TPC-DS Q17    |           1389.83 |           2154.16 |           1718.00 |
| TPC-DS Q18    |           4703.25 |           1311.19 |           1406.50 |
| TPC-DS Q19    |           1072.87 |            994.54 |           1014.53 |
| TPC-DS Q20    |           1348.37 |           1274.87 |           2248.04 |
| TPC-DS Q21    |          87610.89 |          97497.10 |          93988.08 |
| TPC-DS Q22    |          15639.66 |          16427.38 |          15639.02 |
| TPC-DS Q23a+b |         144087.82 |         138374.87 |         140082.97 |
| TPC-DS Q24a+b |          13003.77 |          12507.54 |          13237.87 |
| TPC-DS Q25    |            487.27 |            346.25 |            352.65 |
| TPC-DS Q26    |           1458.66 |            632.76 |            805.23 |
| TPC-DS Q27    |           1139.51 |            749.31 |           1029.38 |
| TPC-DS Q28    |          11182.20 |           8932.79 |           8761.13 |
| TPC-DS Q29    |            335.54 |            189.52 |            192.76 |
| TPC-DS Q30    |           5817.71 |           4373.13 |           4725.23 |
| TPC-DS Q31    |          46386.85 |          35696.04 |          35688.49 |
| TPC-DS Q32    |           2423.62 |           1465.63 |           1624.06 |
| TPC-DS Q33    |           1734.46 |           1611.28 |           1568.76 |
| TPC-DS Q34    |           4946.38 |           2923.83 |           3108.89 |
| TPC-DS Q35    |          74610.14 |          65183.09 |          68517.36 |
| TPC-DS Q36    |          17983.82 |          21424.81 |          21677.31 |
| TPC-DS Q37    |             70.31 |             19.59 |             23.44 |
| TPC-DS Q38    |          20971.86 |          27401.58 |          27663.17 |
| TPC-DS Q39a+b |           4943.60 |           4302.84 |           4331.17 |
| TPC-DS Q40    |            378.02 |            595.35 |            594.22 |
| TPC-DS Q41    |           5440.98 |           5042.25 |           5011.21 |
| TPC-DS Q42    |            269.88 |             39.48 |             41.43 |
| TPC-DS Q43    |          28122.42 |          23061.81 |          23052.60 |
| TPC-DS Q44    |           2343.48 |           2126.98 |           2070.92 |
| TPC-DS Q45    |            652.02 |            485.52 |            455.23 |
| TPC-DS Q46    |           1237.42 |           1375.85 |           1366.06 |
| TPC-DS Q47    |          18895.78 |          21370.60 |          20390.09 |
| TPC-DS Q48    |           3448.06 |           2517.75 |           2500.03 |
| TPC-DS Q49    |            549.66 |            289.89 |            352.89 |
| TPC-DS Q50    |            127.70 |             72.43 |             86.54 |
| TPC-DS Q51    |          15952.63 |          18924.20 |          18905.56 |
| TPC-DS Q52    |             47.20 |             38.04 |             40.30 |
| TPC-DS Q53    |            578.99 |            524.81 |            525.92 |
| TPC-DS Q54    |           7477.71 |           9578.33 |           9732.12 |
| TPC-DS Q55    |            262.68 |             35.82 |             41.97 |
| TPC-DS Q56    |            918.98 |            554.05 |            653.54 |
| TPC-DS Q57    |           8871.27 |           8951.87 |           9089.68 |
| TPC-DS Q58    |          15879.19 |          22933.33 |          23062.69 |
| TPC-DS Q59    |          16458.55 |          18341.78 |          18128.58 |
| TPC-DS Q60    |           1098.97 |            897.44 |            904.53 |
| TPC-DS Q61    |           1303.27 |            748.57 |            773.70 |
| TPC-DS Q62    |           9176.27 |           8735.17 |           8736.14 |
| TPC-DS Q63    |            527.59 |            699.75 |            740.34 |
| TPC-DS Q64    |           1178.17 |           1225.09 |           1224.65 |
| TPC-DS Q65    |          19070.78 |          24819.19 |          24783.61 |
| TPC-DS Q66    |           7301.73 |           5756.03 |           5751.72 |
| TPC-DS Q67    |          24807.19 |          25328.79 |          25254.04 |
| TPC-DS Q68    |            961.06 |            790.84 |            886.20 |
| TPC-DS Q69    |           1925.63 |           1837.94 |           1851.86 |
| TPC-DS Q70    |          39001.54 |          37995.14 |          39131.46 |
| TPC-DS Q71    |           1490.90 |           1206.75 |           1352.61 |
| TPC-DS Q72    |          47595.52 |          79009.56 |          78640.40 |
| TPC-DS Q73    |           4339.64 |           4276.51 |           4229.40 |
| TPC-DS Q74    |          15919.79 |          20039.48 |          20093.68 |
| TPC-DS Q75    |           4118.69 |           5866.83 |           5754.55 |
| TPC-DS Q76    |           1353.71 |           1050.94 |           1306.72 |
| TPC-DS Q77    |          28225.21 |          55871.49 |          54783.86 |
| TPC-DS Q78    |          40644.74 |          41995.75 |          43165.61 |
| TPC-DS Q79    |           3847.76 |           2716.70 |           2902.90 |
| TPC-DS Q80    |          21147.54 |          10138.94 |           9993.46 |
| TPC-DS Q81    |          24647.69 |          21342.33 |          21104.20 |
| TPC-DS Q82    |             42.51 |             40.66 |             32.05 |
| TPC-DS Q83    |           2228.56 |           1984.49 |           2155.97 |
| TPC-DS Q84    |            261.55 |             96.11 |            129.07 |
| TPC-DS Q85    |            449.49 |            593.95 |            323.05 |
| TPC-DS Q86    |           3102.84 |           3325.71 |           3414.80 |
| TPC-DS Q87    |          24785.32 |          26320.60 |          24548.05 |
| TPC-DS Q88    |          11339.09 |           7906.63 |           7793.12 |
| TPC-DS Q89    |            701.24 |            719.12 |            719.86 |
| TPC-DS Q90    |           1272.19 |            867.16 |            928.76 |
| TPC-DS Q91    |            142.10 |             32.77 |             34.40 |
| TPC-DS Q92    |            327.13 |            100.81 |             88.68 |
| TPC-DS Q93    |            420.56 |             94.78 |             97.30 |
| TPC-DS Q94    |           1538.19 |           1005.58 |            993.04 |
| TPC-DS Q95    |          15478.84 |          11222.13 |          10919.68 |
| TPC-DS Q96    |            886.78 |            429.27 |            649.09 |
| TPC-DS Q97    |          17496.49 |          18701.08 |          19190.27 |
| TPC-DS Q98    |           2721.75 |           3414.11 |           3875.62 |
| TPC-DS Q99    |          22003.17 |          16337.02 |          16091.79 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       802.62 |      5.18 |           9.88 |                 16.90 |
| mysql-1-1-2-1 |       802.62 |      5.18 |           9.88 |                 16.90 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mysql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        14.51 |      0.05 |           0.01 |                  2.21 |
| mysql-1-1-2-1 |        14.51 |      0.05 |           0.01 |                  2.21 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1358.79 |      1.02 |          15.45 |                 22.47 |
| mysql-1-1-2-1 |      3100.78 |      2.01 |          17.43 |                 24.45 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        30.08 |      0.44 |           0.37 |                  0.38 |
| mysql-1-1-2-1 |        58.91 |      0.15 |           0.36 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
