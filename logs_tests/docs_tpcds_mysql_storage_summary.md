## Show Summary

### Workload
TPC-DS Queries SF=10
* Type: tpcds
* Duration: 30839s 
* Code: 1794263841
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * Experiment is run 2 times.
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
  * disk:883946
  * datadisk:78490
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794263841
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:883307
  * datadisk:78490
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794263841
* mysql-1-1-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:883307
  * datadisk:78490
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794263841
* mysql-1-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:881185
  * datadisk:78494
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794263841
* mysql-1-2-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:880529
  * datadisk:78494
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
bexhoma : C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py:733: 
PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, 
which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a 
de-fragmented frame, use `newframe = frame.copy()`
In C:\Users\Patrick\AppData\Local\Temp\claude\c--Users-Patrick-eclipse-workspace-Benchmark-Experiment-Host-Manager\9113
4c7f-b6e2-48e3-a81b-1c6e59515939\scratchpad\t_11.ps1:9 Zeichen:1
+ bexhoma tpcds `
+ ~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (C:\Users\Patric...= frame.copy()`:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  df_matrix['complete'] = complete.map({True: 'yes', False: 'no'})
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794263841
* mysql-1-2-2-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:880529
  * datadisk:78494
  * volume_size:147G
  * volume_used:77G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem', '--sort_buffer_size=32M', '--join_buffer_size=64M', '--tmp_table_size=1G', '--max_heap_table_size=1G', '--temptable_max_ram=4G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794263841

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MySQL-1-2

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794263841-7db785776f-f2hfk: 0
* bexhoma-sut-mysql-1-1794263841-5d5d5d9fb9-kff4f: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   10 |     2522.00 |           3.00 |            1.00 |        319.00 |         2191.00 |              8 |           0 |             | None           |             0 | False         |               14.27 | False               |
| MySQL-1-2 |                2 |   10 |     2522.00 |           3.00 |            1.00 |        319.00 |         2191.00 |              8 |           0 |             | None           |             0 | False         |               14.27 | True                |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               99 |                  99 |       5864 |            9.39 |             3848.57 |            607.78 |          -1 | mysql-1-1-1-1-1 |
| mysql-1-1-2-1-1 | MySQL-1         | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               99 |                  99 |       7372 |           11.32 |             3190.44 |            483.45 |          -1 | mysql-1-1-2-1-1 |
| mysql-1-1-2-1-2 | MySQL-1         | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               99 |                  99 |       7372 |           10.98 |             3293.77 |            483.45 |          -1 | mysql-1-1-2-1-2 |
| mysql-1-2-1-1-1 | MySQL-1         | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               99 |                  99 |       6477 |            9.96 |             3623.93 |            550.25 |          -1 | mysql-1-2-1-1-1 |
| mysql-1-2-2-1-1 | MySQL-1         | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               99 |                  99 |       7617 |           11.59 |             3115.08 |            467.90 |          -1 | mysql-1-2-2-1-1 |
| mysql-1-2-2-1-2 | MySQL-1         | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               99 |                  99 |       7617 |           11.55 |             3127.43 |            467.90 |          -1 | mysql-1-2-2-1-2 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               99 |                  99 |       5864 |            9.39 |             3848.57 |            607.78 |          -1 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 | 10.00 |              198 |                 198 |       7372 |           11.15 |             3241.69 |            966.90 |          -1 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               99 |                  99 |       6477 |            9.96 |             3623.93 |            550.25 |          -1 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 | 10.00 |              198 |                 198 |       7617 |           11.57 |             3121.25 |            935.80 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |
| mysql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-2-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-1-1-2-1-2 |   mysql-1-2-1-1-1 |   mysql-1-2-2-1-1 |   mysql-1-2-2-1-2 |
|:--------------|------------------:|------------------:|------------------:|------------------:|------------------:|------------------:|
| TPC-DS Q1     |             54.98 |             54.78 |            146.14 |            114.70 |             66.22 |            169.17 |
| TPC-DS Q2     |          32813.61 |          37615.06 |          37725.87 |          56566.55 |          69020.98 |          67361.05 |
| TPC-DS Q3     |            150.05 |             79.93 |             94.50 |            759.53 |             88.53 |            110.70 |
| TPC-DS Q4     |         462269.74 |         524243.70 |         524617.57 |         806636.72 |         551119.29 |         550560.97 |
| TPC-DS Q5     |         114160.37 |         138724.39 |         136361.34 |         120693.83 |         133034.70 |         134380.74 |
| TPC-DS Q6     |          11507.17 |          11840.33 |          11261.28 |          12119.45 |          11177.68 |          11120.76 |
| TPC-DS Q7     |         122860.89 |         107306.78 |         108288.49 |         126706.25 |         141706.89 |         141701.31 |
| TPC-DS Q8     |         154599.00 |         202115.13 |         202474.56 |         161273.64 |         199327.75 |         202980.61 |
| TPC-DS Q9     |          39322.89 |          38712.87 |          38519.81 |          42598.29 |          43139.47 |          39012.73 |
| TPC-DS Q10    |           9479.39 |           7385.01 |           9107.67 |           9215.80 |          10159.38 |          10609.96 |
| TPC-DS Q11    |         274718.59 |         329097.34 |         329743.92 |         321719.41 |         344021.93 |         344893.74 |
| TPC-DS Q12    |           2605.20 |           3042.30 |           3354.83 |           2470.54 |           3230.57 |           3237.67 |
| TPC-DS Q13    |          78681.07 |          70333.28 |          69565.76 |          64058.58 |          72651.14 |          72402.05 |
| TPC-DS Q14a+b |         386763.99 |         485076.11 |         486163.19 |         386068.89 |         472299.64 |         469599.81 |
| TPC-DS Q15    |           2796.98 |           1831.66 |           1801.02 |           1806.53 |           1737.35 |           2190.35 |
| TPC-DS Q16    |              2.82 |              4.81 |              2.66 |              4.40 |              2.94 |              5.63 |
| TPC-DS Q17    |          83605.78 |          89222.32 |          88221.23 |          69506.02 |          78845.58 |          77793.68 |
| TPC-DS Q18    |          20662.42 |          15177.50 |          14934.91 |          14761.87 |          12254.03 |          16031.70 |
| TPC-DS Q19    |           4676.02 |           5062.62 |           5062.32 |           4257.97 |           5616.47 |           5621.70 |
| TPC-DS Q20    |           4349.17 |           6258.40 |           6330.50 |           3968.08 |           6540.62 |           6048.31 |
| TPC-DS Q21    |         408367.84 |         616646.67 |         616540.16 |         511542.04 |         634746.97 |         635847.39 |
| TPC-DS Q22    |          56525.62 |          60874.52 |          61043.00 |          57707.84 |          57489.16 |          57203.86 |
| TPC-DS Q23a+b |         536877.93 |         619407.51 |         619311.03 |         557001.60 |         639871.64 |         640163.53 |
| TPC-DS Q24a+b |          28781.00 |          40776.79 |          40775.72 |          27197.97 |          41060.87 |          41063.36 |
| TPC-DS Q25    |           2235.58 |          19690.57 |          19689.93 |           1510.67 |          17967.99 |          17968.50 |
| TPC-DS Q26    |          69505.46 |         184113.94 |         184112.84 |          62268.28 |         146130.01 |         146131.94 |
| TPC-DS Q27    |          26590.39 |          34592.13 |          35135.97 |          24766.14 |          41198.60 |          42637.12 |
| TPC-DS Q28    |          31932.62 |          29371.29 |          29387.15 |          29683.63 |          29621.40 |          30910.36 |
| TPC-DS Q29    |           1768.11 |           2769.78 |           2607.22 |           1834.33 |           2419.94 |           1695.88 |
| TPC-DS Q30    |          59118.44 |          60629.39 |          62425.75 |          55412.29 |          64770.98 |          63928.62 |
| TPC-DS Q31    |         151971.37 |         203125.68 |         187563.35 |         157079.70 |         197520.42 |         210547.76 |
| TPC-DS Q32    |            698.15 |            699.28 |            764.96 |            704.68 |            784.43 |            720.16 |
| TPC-DS Q33    |           2286.10 |           2044.97 |           2343.45 |           2231.10 |           2352.88 |           2146.25 |
| TPC-DS Q34    |              4.41 |              2.10 |              3.76 |              4.40 |              5.74 |              2.26 |
| TPC-DS Q35    |          47137.17 |          42405.82 |          55803.41 |          44459.16 |          58925.56 |          44924.51 |
| TPC-DS Q36    |          25445.93 |          35207.39 |          35446.29 |          24117.58 |          34067.48 |          34066.91 |
| TPC-DS Q37    |             67.69 |             70.74 |             47.48 |             65.20 |             81.28 |             82.05 |
| TPC-DS Q38    |          42761.39 |          57718.99 |          56501.09 |          40953.56 |          56729.19 |          56719.81 |
| TPC-DS Q39a+b |          13551.68 |          16260.70 |          16541.11 |          13021.11 |          16841.08 |          16235.00 |
| TPC-DS Q40    |          48770.85 |          61520.07 |          62133.50 |          41696.50 |          61979.78 |          62661.18 |
| TPC-DS Q41    |          26166.85 |          24485.30 |          24840.09 |          23501.14 |          24622.02 |          24971.90 |
| TPC-DS Q42    |           3477.28 |           3687.81 |           3603.04 |           3106.96 |           2850.24 |           2601.80 |
| TPC-DS Q43    |          49614.29 |          61639.37 |          62434.00 |          47972.73 |          88170.13 |          86655.83 |
| TPC-DS Q44    |             11.89 |             17.95 |              1.97 |              9.12 |              3.45 |             13.54 |
| TPC-DS Q45    |           1436.34 |           1350.05 |           1235.52 |           3243.01 |           1595.34 |           1955.74 |
| TPC-DS Q46    |              2.07 |              4.10 |              1.80 |              3.77 |              2.38 |              4.36 |
| TPC-DS Q47    |          82600.65 |         105332.52 |          93179.06 |          81836.63 |         108113.03 |         107286.26 |
| TPC-DS Q48    |          55935.10 |          63073.87 |          63512.75 |          54872.70 |          60151.40 |          60395.55 |
| TPC-DS Q49    |          35236.90 |          36502.54 |          46763.53 |          36472.42 |          44461.09 |          45835.52 |
| TPC-DS Q50    |            281.59 |            400.27 |            400.94 |            335.21 |            415.25 |            415.68 |
| TPC-DS Q51    |          39097.24 |          55734.69 |          59132.85 |          51131.65 |          69487.35 |          67191.12 |
| TPC-DS Q52    |           2599.05 |           2431.91 |           2805.68 |           2897.79 |           3694.56 |           2433.56 |
| TPC-DS Q53    |          70003.28 |          84338.51 |          81860.70 |          66796.17 |          85037.65 |          80965.86 |
| TPC-DS Q54    |          21558.00 |          32584.97 |          30751.45 |          21753.63 |          31134.58 |          28753.89 |
| TPC-DS Q55    |           2287.40 |           2611.79 |           2667.34 |           2610.45 |           2391.35 |           2773.38 |
| TPC-DS Q56    |           2267.53 |           2128.89 |           2314.34 |           2749.38 |           2060.37 |           2919.80 |
| TPC-DS Q57    |          52178.10 |          65960.65 |          66120.27 |          52227.14 |          56843.36 |          66067.05 |
| TPC-DS Q58    |          49899.87 |          69753.17 |          74248.55 |          49161.26 |          76044.11 |          76718.94 |
| TPC-DS Q59    |          64803.11 |          77620.11 |          76853.44 |          64652.28 |          77572.25 |          81398.15 |
| TPC-DS Q60    |           4989.84 |           4718.24 |           4430.20 |           4861.53 |           5829.75 |           5307.01 |
| TPC-DS Q61    |          92585.39 |         109447.33 |         111407.89 |          90325.82 |         111714.71 |         111266.82 |
| TPC-DS Q62    |          29723.59 |          14378.04 |          34116.31 |          27763.78 |          15106.77 |          35568.24 |
| TPC-DS Q63    |          70159.77 |          84725.32 |          85772.17 |          70499.53 |          86280.85 |          85013.06 |
| TPC-DS Q64    |           4294.01 |         120383.97 |         114974.11 |           4068.95 |         114953.35 |         111798.26 |
| TPC-DS Q65    |          33639.62 |          36945.31 |          35105.74 |          37888.77 |          37852.98 |          36202.59 |
| TPC-DS Q66    |          12778.02 |          12809.23 |          10204.93 |          13110.87 |          14832.81 |          10565.57 |
| TPC-DS Q67    |         109861.40 |         123666.49 |         122096.78 |         111679.24 |         123485.54 |         126311.94 |
| TPC-DS Q68    |              2.13 |              2.95 |              2.59 |              3.59 |              2.24 |              2.01 |
| TPC-DS Q69    |            834.39 |            568.19 |            485.54 |            908.50 |            559.21 |            466.52 |
| TPC-DS Q70    |         136936.52 |         160991.80 |         162936.45 |         133602.80 |         167454.70 |         176397.57 |
| TPC-DS Q71    |           5391.70 |           6513.61 |           4851.02 |           5975.64 |           8196.29 |           6010.92 |
| TPC-DS Q72    |         239786.66 |         555684.85 |         540356.26 |         268101.42 |         595171.24 |         570785.47 |
| TPC-DS Q73    |              2.05 |              1.97 |              2.08 |              2.03 |              2.60 |              2.61 |
| TPC-DS Q74    |          55915.31 |          76732.93 |          76480.55 |          61057.45 |          84087.62 |          84093.71 |
| TPC-DS Q75    |          14051.94 |          17792.50 |          17664.22 |          15636.09 |          17532.83 |          18093.50 |
| TPC-DS Q76    |           5704.30 |           6343.60 |           6541.60 |           5979.42 |           7201.31 |           7048.89 |
| TPC-DS Q77    |          92345.19 |         126436.66 |         126650.68 |         115923.28 |         134260.08 |         130060.67 |
| TPC-DS Q78    |         136448.00 |         176972.75 |         176371.27 |         151287.10 |         178011.92 |         176597.45 |
| TPC-DS Q79    |          69914.01 |          89019.83 |          87890.17 |          69090.69 |          87433.25 |          87064.08 |
| TPC-DS Q80    |         196346.67 |         289525.23 |         290808.29 |         198104.10 |         309707.87 |         315810.54 |
| TPC-DS Q81    |         246153.09 |           7741.30 |           7739.77 |         258277.90 |           6850.34 |           6856.95 |
| TPC-DS Q82    |            140.03 |            131.48 |            136.57 |            136.34 |            144.68 |            146.18 |
| TPC-DS Q83    |            477.67 |            891.15 |            890.88 |            482.58 |            834.71 |            840.30 |
| TPC-DS Q84    |            671.41 |            624.15 |            623.34 |            530.61 |            624.12 |            620.92 |
| TPC-DS Q85    |           1233.19 |           1368.22 |           1368.37 |           1324.14 |           1380.37 |           1381.60 |
| TPC-DS Q86    |           9965.34 |          11803.04 |          11795.77 |          10607.37 |          12134.77 |          12158.94 |
| TPC-DS Q87    |          37631.00 |          53858.77 |          54291.40 |          41153.36 |          57727.97 |          57717.50 |
| TPC-DS Q88    |          74017.41 |          90707.01 |          93397.22 |          79082.25 |          95041.27 |          97987.13 |
| TPC-DS Q89    |          69160.73 |          86546.51 |          85929.84 |          70390.32 |          79918.14 |          79557.80 |
| TPC-DS Q90    |           4605.60 |           6140.36 |           5184.85 |           4695.90 |           5094.68 |           5359.79 |
| TPC-DS Q91    |            180.59 |           1144.62 |            384.83 |            181.13 |           1488.56 |            149.73 |
| TPC-DS Q92    |            761.88 |            908.36 |           1098.24 |            786.54 |            810.28 |            779.24 |
| TPC-DS Q93    |            393.11 |            507.56 |            271.80 |            411.64 |            454.36 |            266.48 |
| TPC-DS Q94    |           3795.27 |           9870.57 |           8773.69 |           5322.29 |           9212.23 |           8238.72 |
| TPC-DS Q95    |          40747.40 |          43698.95 |          44518.94 |          41244.65 |          43622.00 |          43302.47 |
| TPC-DS Q96    |           9405.39 |          11037.93 |          10519.30 |           9083.80 |          11033.77 |          11253.63 |
| TPC-DS Q97    |          35684.95 |          65845.33 |          66005.08 |          37076.97 |          64935.53 |          64512.27 |
| TPC-DS Q98    |           8110.88 |          12283.24 |          12172.56 |           8833.67 |          16815.95 |          16167.45 |
| TPC-DS Q99    |          60631.77 |          76901.66 |          77351.04 |          71673.93 |          86829.76 |          87910.30 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      2898.41 |      6.31 |          30.77 |                 59.79 |
| mysql-1-1-2-1 |      2898.41 |      6.31 |          30.77 |                 59.79 |

### Loading phase: component data generator

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mysql-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        33.93 |      0.41 |           0.01 |                  2.83 |
| mysql-1-1-2-1 |        33.93 |      0.41 |           0.01 |                  2.83 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      5335.85 |      1.02 |          52.01 |                 81.04 |
| mysql-1-1-2-1 |     12959.32 |      2.02 |          68.95 |                 97.97 |
| mysql-1-2-1-1 |      5580.80 |      1.02 |          57.45 |                 57.46 |
| mysql-1-2-2-1 |     13570.38 |      2.02 |          66.68 |                 66.69 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |        41.41 |      0.15 |           0.42 |                  0.43 |
| mysql-1-1-2-1 |        84.86 |      0.76 |           0.42 |                  0.43 |
| mysql-1-2-1-1 |        42.86 |      0.13 |           0.43 |                  0.44 |
| mysql-1-2-2-1 |        87.13 |      0.26 |           0.40 |                  0.41 |

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
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
