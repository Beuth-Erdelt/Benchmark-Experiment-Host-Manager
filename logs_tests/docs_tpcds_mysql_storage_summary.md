## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 4027s 
* Code: 1795534879
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
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
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'volume': 'mysqltmp', 'field': 'sizeLimit', 'target': 'volume'}, '72Gi'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'sort_buffer_size', 'target': 'container'}, '32M'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'join_buffer_size', 'target': 'container'}, '64M'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'tmp_table_size', 'target': 'container'}, '1G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'max_heap_table_size', 'target': 'container'}, '1G'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'temptable_max_ram', 'target': 'container'}, '4G')].
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1086813
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
    * code:1795534879
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1086823
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
    * code:1795534879
* mysql-1-1-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1086823
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
    * code:1795534879

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1795534879-dc845bd66-mf9x8: 0

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
| MySQL-1-1 |                1 |    3 |      879.00 |           2.00 |            1.00 |        177.00 |          692.00 |              8 |         0 |             | None           |             0 | False         |               12.29 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |       1239 |            2.45 |             4443.18 |            862.95 |          -1 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 | 3.00 |               99 |                  99 |       1372 |            2.29 |             4761.19 |            779.30 |          -1 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 | 3.00 |               99 |                  99 |       1358 |            2.33 |             4679.04 |            787.33 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |       1239 |            2.45 |             4443.18 |            862.95 |          -1 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |       1372 |            2.31 |             4719.94 |           1558.60 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-1-1-2-1-2 |
|:--------------|------------------:|------------------:|------------------:|
| TPC-DS Q1     |            354.99 |            145.36 |             53.33 |
| TPC-DS Q2     |          10126.74 |          12240.20 |          11696.35 |
| TPC-DS Q3     |             14.29 |             11.70 |             11.74 |
| TPC-DS Q4     |         111079.26 |         123528.00 |         125176.76 |
| TPC-DS Q5     |          28956.68 |          41762.42 |          40262.15 |
| TPC-DS Q6     |           3660.53 |           2974.06 |           3037.24 |
| TPC-DS Q7     |           6556.17 |            971.40 |           1553.37 |
| TPC-DS Q8     |            987.83 |            968.01 |            715.68 |
| TPC-DS Q9     |          12833.45 |          11456.39 |          12511.80 |
| TPC-DS Q10    |           1189.82 |            113.77 |            149.67 |
| TPC-DS Q11    |          57113.34 |          73643.97 |          64598.27 |
| TPC-DS Q12    |            671.75 |            721.47 |            765.91 |
| TPC-DS Q13    |          10338.82 |           4702.72 |           5141.08 |
| TPC-DS Q14a+b |         144926.37 |         195517.84 |         185622.12 |
| TPC-DS Q15    |            727.78 |            672.14 |           1075.26 |
| TPC-DS Q16    |           1184.33 |            308.80 |            358.37 |
| TPC-DS Q17    |           1277.73 |           1745.18 |           2074.35 |
| TPC-DS Q18    |           4722.47 |           1770.00 |           2282.11 |
| TPC-DS Q19    |            751.86 |           1871.40 |           1364.37 |
| TPC-DS Q20    |           1188.00 |           1725.69 |           3211.31 |
| TPC-DS Q21    |          78025.08 |          77640.22 |          80308.46 |
| TPC-DS Q22    |          12969.37 |          13747.57 |          13983.94 |
| TPC-DS Q23a+b |          93435.39 |         109700.56 |         111379.42 |
| TPC-DS Q24a+b |           3257.66 |           3473.08 |           3484.23 |
| TPC-DS Q25    |            373.54 |            309.30 |            435.83 |
| TPC-DS Q26    |            537.91 |            529.74 |            664.42 |
| TPC-DS Q27    |            692.12 |            675.68 |            714.68 |
| TPC-DS Q28    |           8881.54 |           9207.42 |           9163.35 |
| TPC-DS Q29    |            155.74 |            130.74 |            110.71 |
| TPC-DS Q30    |           4697.16 |           5152.77 |           4809.35 |
| TPC-DS Q31    |          32994.76 |          35910.55 |          35385.56 |
| TPC-DS Q32    |           1512.96 |           1667.47 |           1901.40 |
| TPC-DS Q33    |           1693.10 |           1639.18 |           1427.19 |
| TPC-DS Q34    |           4311.64 |           2806.18 |           2803.32 |
| TPC-DS Q35    |          65342.92 |          69073.93 |          67909.42 |
| TPC-DS Q36    |          17342.52 |          20694.20 |          17529.39 |
| TPC-DS Q37    |             20.91 |             15.77 |             13.60 |
| TPC-DS Q38    |          21373.16 |          23019.00 |          25572.24 |
| TPC-DS Q39a+b |           4622.63 |           4824.00 |           5108.05 |
| TPC-DS Q40    |            377.77 |            385.12 |            452.09 |
| TPC-DS Q41    |           4551.45 |           4964.25 |           5094.86 |
| TPC-DS Q42    |             63.93 |             54.38 |             45.13 |
| TPC-DS Q43    |              2.28 |              2.45 |              1.66 |
| TPC-DS Q44    |           1987.93 |           2025.43 |           1575.21 |
| TPC-DS Q45    |            325.08 |            325.33 |            928.52 |
| TPC-DS Q46    |           3469.97 |           4332.57 |           3160.05 |
| TPC-DS Q47    |          16612.40 |          22805.34 |          19078.93 |
| TPC-DS Q48    |           3086.96 |           2852.03 |           3347.30 |
| TPC-DS Q49    |            385.49 |            288.25 |            331.10 |
| TPC-DS Q50    |             67.34 |             58.38 |             64.22 |
| TPC-DS Q51    |          17086.24 |          18516.84 |          18700.82 |
| TPC-DS Q52    |             38.22 |             38.85 |             38.92 |
| TPC-DS Q53    |            528.05 |            629.60 |            679.12 |
| TPC-DS Q54    |           6277.69 |           8077.36 |           9178.76 |
| TPC-DS Q55    |             23.95 |             28.23 |             24.22 |
| TPC-DS Q56    |            867.96 |           1379.38 |            613.46 |
| TPC-DS Q57    |           9559.51 |          11058.66 |           8885.20 |
| TPC-DS Q58    |          16566.37 |          19840.85 |          19343.31 |
| TPC-DS Q59    |          17630.92 |          18178.24 |          18548.56 |
| TPC-DS Q60    |           1588.48 |            856.88 |            830.95 |
| TPC-DS Q61    |           1062.55 |            751.78 |            752.97 |
| TPC-DS Q62    |          10232.37 |           8861.74 |           8121.44 |
| TPC-DS Q63    |            542.65 |            649.62 |            650.83 |
| TPC-DS Q64    |           1072.70 |            937.46 |            998.41 |
| TPC-DS Q65    |          20054.72 |          26705.20 |          22669.92 |
| TPC-DS Q66    |          10177.82 |           9934.64 |           8120.04 |
| TPC-DS Q67    |          22719.91 |          35957.51 |          31524.66 |
| TPC-DS Q68    |            815.96 |           1683.63 |           1395.74 |
| TPC-DS Q69    |           1400.27 |           1902.73 |           1837.74 |
| TPC-DS Q70    |          39072.34 |          35055.97 |          46334.03 |
| TPC-DS Q71    |           1113.31 |           1378.12 |           1581.87 |
| TPC-DS Q72    |          40911.83 |          44026.95 |          47512.02 |
| TPC-DS Q73    |           4563.89 |           2768.99 |           3576.41 |
| TPC-DS Q74    |          16891.70 |          15507.41 |          14159.25 |
| TPC-DS Q75    |           5077.64 |           4994.85 |           4587.67 |
| TPC-DS Q76    |           1319.82 |           1054.81 |           1233.51 |
| TPC-DS Q77    |          25489.85 |          28002.23 |          27375.13 |
| TPC-DS Q78    |          35323.65 |          36755.44 |          35316.44 |
| TPC-DS Q79    |           2609.46 |           3117.06 |           2662.13 |
| TPC-DS Q80    |          17568.03 |           8855.90 |           9482.76 |
| TPC-DS Q81    |          22894.41 |          22696.38 |          24522.83 |
| TPC-DS Q82    |             16.22 |             15.84 |             14.16 |
| TPC-DS Q83    |           2235.62 |           3271.69 |           2704.61 |
| TPC-DS Q84    |            175.04 |             92.94 |            101.36 |
| TPC-DS Q85    |            404.34 |            289.42 |            281.65 |
| TPC-DS Q86    |           3440.07 |           4144.54 |           2721.39 |
| TPC-DS Q87    |          19686.92 |          22381.03 |          24321.60 |
| TPC-DS Q88    |           9900.05 |           7198.20 |           7854.77 |
| TPC-DS Q89    |            418.73 |            552.09 |            488.35 |
| TPC-DS Q90    |           1070.28 |           1117.04 |           1874.74 |
| TPC-DS Q91    |             36.97 |             30.44 |             31.75 |
| TPC-DS Q92    |            214.68 |            223.22 |            285.14 |
| TPC-DS Q93    |            109.94 |            101.20 |            266.68 |
| TPC-DS Q94    |           2288.44 |           1022.02 |           1292.89 |
| TPC-DS Q95    |          12028.91 |          11160.58 |          10852.74 |
| TPC-DS Q96    |            566.06 |            431.11 |            463.33 |
| TPC-DS Q97    |          15152.90 |          17196.59 |          15494.68 |
| TPC-DS Q98    |           3453.19 |           3134.24 |           3369.33 |
| TPC-DS Q99    |          16978.27 |          13834.05 |          14322.17 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       789.72 |      4.57 |           9.87 |                 16.89 |
| mysql-1-1-2-1 |       789.72 |      4.57 |           9.87 |                 16.89 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mysql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        18.02 |      0.06 |           0.01 |                  2.66 |
| mysql-1-1-2-1 |        18.02 |      0.06 |           0.01 |                  2.66 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1129.11 |      1.01 |          17.41 |                 24.43 |
| mysql-1-1-2-1 |      2633.12 |      2.02 |          21.82 |                 28.84 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        28.79 |      0.04 |           0.36 |                  0.36 |
| mysql-1-1-2-1 |        54.87 |      0.09 |           0.35 |                  0.36 |

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
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
