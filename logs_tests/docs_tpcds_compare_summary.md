## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1308s 
* Code: 1794055305
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:896286
  * datadisk:4474
  * volume_size:1.8T
  * volume_used:876G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:890647
  * datadisk:5472
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:896286
  * datadisk:37644
  * volume_size:1.8T
  * volume_used:876G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:890647
  * datadisk:5794
  * volume_size:1.8T
  * volume_used:870G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794055305-7c59c75f95-gt4ld: 0
* bexhoma-sut-monetdb-1-1794055305-655cf6db5b-z77sf: 0
* bexhoma-sut-mysql-1-1794055305-7f775d78b-sbhhg: 0
* bexhoma-sut-postgresql-1-1794055305-68cbc8c9f8-ncr44: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1    |                1 |    1 |      180.00 |           4.00 |            1.00 |         66.00 |           99.00 |              8 |           0 |             | None           |             0 | False         |               20.00 | False               |
| MonetDB-1-1    |                1 |    1 |      161.00 |           3.00 |            1.00 |        118.00 |           27.00 |              8 |           0 |             | None           |             0 | False         |               22.36 | False               |
| MySQL-1-1      |                1 |    1 |      212.00 |           4.00 |            1.00 |         60.00 |          137.00 |              8 |           0 |             | None           |             0 | False         |               16.98 | False               |
| PostgreSQL-1-1 |                1 |    1 |      100.00 |           5.00 |            1.00 |         40.00 |           43.00 |              8 |           0 |             | None           |             0 | False         |               36.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| mariadb-1-1-1-1-1    | MariaDB-1       | mariadb-1-1-1    | mariadb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        339 |            0.74 |             4923.82 |           1051.33 |          -1 | mariadb-1-1-1-1-1    |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         17 |            0.04 |           100748.75 |          20964.71 |          -1 | monetdb-1-1-1-1-1    |
| mysql-1-1-1-1-1      | MySQL-1         | mysql-1-1-1      | mysql-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        489 |            0.70 |             5215.27 |            728.83 |          -1 | mysql-1-1-1-1-1      |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        180 |            0.31 |            11901.53 |           1980.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1    | mariadb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        339 |            0.74 |             4923.82 |           1051.33 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         17 |            0.04 |           100748.75 |          20964.71 |          -1 |
| mysql-1-1-1      | mysql-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        489 |            0.70 |             5215.27 |            728.83 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        180 |            0.31 |            11901.53 |           1980.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1    |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-1    |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-1      |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   monetdb-1-1-1-1-1 |   mysql-1-1-1-1-1 |   postgresql-1-1-1-1-1 |
|:--------------|--------------------:|--------------------:|------------------:|-----------------------:|
| TPC-DS Q1     |               15.71 |              158.86 |            197.62 |                 170.50 |
| TPC-DS Q2     |             3981.12 |               53.29 |           3539.43 |                 322.88 |
| TPC-DS Q3     |               12.46 |               12.05 |             35.78 |                 246.75 |
| TPC-DS Q4     |            10104.53 |              342.64 |          51482.47 |                6639.13 |
| TPC-DS Q5     |             9273.21 |               49.33 |          16253.15 |                 370.50 |
| TPC-DS Q6     |              584.51 |               26.59 |          62857.27 |               65443.20 |
| TPC-DS Q7     |             3452.69 |               32.92 |           1754.30 |                 329.58 |
| TPC-DS Q8     |              308.75 |               40.89 |            316.85 |                  61.19 |
| TPC-DS Q9     |             3578.81 |               40.28 |           4214.68 |                2773.55 |
| TPC-DS Q10    |               58.46 |               23.29 |            295.42 |                1086.88 |
| TPC-DS Q11    |             6693.94 |              398.59 |          26564.06 |                3952.04 |
| TPC-DS Q12    |              206.54 |               16.58 |            240.49 |                  55.98 |
| TPC-DS Q13    |              774.18 |               36.26 |           1938.93 |                 517.99 |
| TPC-DS Q14a+b |            50670.07 |              898.35 |          36160.62 |                1563.59 |
| TPC-DS Q15    |              138.20 |                9.94 |            162.44 |                  88.81 |
| TPC-DS Q16    |             9950.05 |               20.60 |            379.68 |                 155.92 |
| TPC-DS Q17    |              596.00 |               56.97 |           1025.14 |                 235.32 |
| TPC-DS Q18    |             2438.47 |               47.83 |           1196.80 |                 397.15 |
| TPC-DS Q19    |              177.37 |               19.06 |            307.91 |                 123.65 |
| TPC-DS Q20    |              329.93 |               12.19 |            408.64 |                 197.94 |
| TPC-DS Q21    |             3529.87 |               62.48 |           1826.96 |                 286.47 |
| TPC-DS Q22    |             9180.91 |              355.14 |           6272.58 |                2644.35 |
| TPC-DS Q23a+b |            51118.25 |              819.56 |          52292.89 |                4927.96 |
| TPC-DS Q24a+b |               23.67 |               84.68 |              6.73 |                  43.17 |
| TPC-DS Q25    |              100.60 |               57.40 |            181.08 |                 251.74 |
| TPC-DS Q26    |              605.34 |                9.30 |            516.58 |                 211.27 |
| TPC-DS Q27    |             2448.00 |               48.39 |            593.49 |                 314.46 |
| TPC-DS Q28    |             2529.64 |               30.19 |           4180.76 |                 595.62 |
| TPC-DS Q29    |               44.70 |               53.52 |             74.58 |                 249.06 |
| TPC-DS Q30    |               31.19 |               13.07 |             81.36 |                 817.05 |
| TPC-DS Q31    |              995.59 |               49.67 |          14233.84 |                1837.44 |
| TPC-DS Q32    |                6.14 |               14.02 |            143.50 |                  95.21 |
| TPC-DS Q33    |              135.06 |               14.52 |            576.21 |                 299.70 |
| TPC-DS Q34    |             2721.48 |               16.81 |            971.67 |                  22.60 |
| TPC-DS Q35    |              877.48 |               41.36 |          12358.20 |                 992.68 |
| TPC-DS Q36    |             2216.57 |               57.72 |           2591.92 |                 320.88 |
| TPC-DS Q37    |             2936.60 |               40.34 |             16.02 |                 192.13 |
| TPC-DS Q38    |             6287.24 |               65.40 |           6885.72 |                 854.68 |
| TPC-DS Q39a+b |              988.16 |             1026.28 |           1104.01 |                2525.55 |
| TPC-DS Q40    |              141.11 |               28.19 |            129.41 |                 106.32 |
| TPC-DS Q41    |              950.14 |                4.78 |           1084.03 |                 845.84 |
| TPC-DS Q42    |              245.28 |               13.10 |             71.17 |                  66.73 |
| TPC-DS Q43    |              810.00 |               22.15 |              9.74 |                  22.88 |
| TPC-DS Q44    |             1102.44 |               34.04 |           1862.12 |                 332.01 |
| TPC-DS Q45    |              120.28 |                8.19 |             97.17 |                  74.82 |
| TPC-DS Q46    |             2709.90 |               19.68 |            946.04 |                  30.89 |
| TPC-DS Q47    |            13063.19 |               87.73 |           7805.31 |                2056.39 |
| TPC-DS Q48    |              853.24 |               24.30 |            927.52 |                 534.33 |
| TPC-DS Q49    |              105.20 |               42.45 |            112.66 |                 348.20 |
| TPC-DS Q50    |               21.63 |               45.50 |             24.77 |                 433.06 |
| TPC-DS Q51    |             6885.97 |              153.42 |           7593.59 |                 810.09 |
| TPC-DS Q52    |              262.60 |               11.25 |             20.53 |                  64.96 |
| TPC-DS Q53    |              151.70 |               14.58 |            169.54 |                  81.17 |
| TPC-DS Q54    |              988.62 |              188.67 |           2437.91 |                  67.66 |
| TPC-DS Q55    |              164.78 |                9.15 |             12.94 |                  66.98 |
| TPC-DS Q56    |              127.78 |               10.78 |            182.24 |                 307.47 |
| TPC-DS Q57    |             4791.77 |               32.94 |           2548.57 |                1093.60 |
| TPC-DS Q58    |             5565.69 |               15.18 |           5577.65 |                 282.55 |
| TPC-DS Q59    |             8687.18 |               50.23 |           4421.85 |                 369.97 |
| TPC-DS Q60    |              277.12 |               12.37 |            306.65 |                 334.95 |
| TPC-DS Q61    |              276.08 |               16.10 |              2.37 |                 111.76 |
| TPC-DS Q62    |             1495.41 |               12.71 |           3471.02 |                  79.17 |
| TPC-DS Q63    |              270.24 |               14.94 |            180.44 |                  82.03 |
| TPC-DS Q64    |             1086.93 |              120.21 |            314.10 |                 545.65 |
| TPC-DS Q65    |             5338.74 |               29.53 |           5414.62 |                 453.77 |
| TPC-DS Q66    |             1099.02 |               21.39 |           1844.25 |                 313.98 |
| TPC-DS Q67    |             6096.94 |              125.87 |           7043.32 |                2872.70 |
| TPC-DS Q68    |             2700.47 |               34.52 |            248.21 |                  29.98 |
| TPC-DS Q69    |                2.04 |                8.18 |              3.19 |                  95.17 |
| TPC-DS Q70    |             6113.41 |               30.52 |           9901.53 |                 304.16 |
| TPC-DS Q71    |              410.63 |               14.81 |            412.00 |                 393.55 |
| TPC-DS Q72    |              641.45 |               98.57 |           8967.76 |                 969.91 |
| TPC-DS Q73    |             2167.50 |               17.00 |            213.69 |                  22.59 |
| TPC-DS Q74    |             5365.64 |               57.43 |           7650.60 |                 878.91 |
| TPC-DS Q75    |             5438.40 |              177.31 |           1860.57 |                 728.57 |
| TPC-DS Q76    |              852.82 |               21.24 |            409.59 |                 120.18 |
| TPC-DS Q77    |             5914.83 |               20.34 |           8635.90 |                 261.08 |
| TPC-DS Q78    |             4215.16 |              259.95 |          16112.44 |                2219.18 |
| TPC-DS Q79    |             2600.76 |               25.54 |           3766.14 |                 142.86 |
| TPC-DS Q80    |              416.15 |              172.87 |           8662.73 |                 328.97 |
| TPC-DS Q81    |              156.90 |               16.36 |           1780.81 |               37426.92 |
| TPC-DS Q82    |             3274.36 |               53.64 |              7.94 |                 235.66 |
| TPC-DS Q83    |             1032.02 |               10.84 |            619.03 |                  67.78 |
| TPC-DS Q84    |               46.16 |               23.34 |             59.73 |                  21.36 |
| TPC-DS Q85    |              193.79 |               78.99 |             83.87 |                 252.97 |
| TPC-DS Q86    |              657.58 |               24.53 |            909.55 |                 149.32 |
| TPC-DS Q87    |             6343.37 |              161.35 |           5865.20 |                 840.50 |
| TPC-DS Q88    |             8105.92 |               55.01 |           1867.24 |                2829.95 |
| TPC-DS Q89    |             1020.03 |               21.80 |              7.54 |                  23.16 |
| TPC-DS Q90    |              121.67 |               10.12 |            308.43 |                  93.83 |
| TPC-DS Q91    |               18.73 |               13.30 |             12.61 |                 151.08 |
| TPC-DS Q92    |                5.09 |                8.82 |             52.39 |                  71.12 |
| TPC-DS Q93    |               35.61 |               42.37 |             36.29 |                 199.70 |
| TPC-DS Q94    |              379.84 |               10.12 |            383.66 |                 139.11 |
| TPC-DS Q95    |              578.72 |               97.49 |           3188.02 |                3043.83 |
| TPC-DS Q96    |              559.07 |                6.46 |            139.04 |                  71.90 |
| TPC-DS Q97    |             4216.73 |               75.21 |           6422.60 |                 426.99 |
| TPC-DS Q98    |              723.45 |               19.96 |            810.87 |                 131.00 |
| TPC-DS Q99    |             2738.94 |               23.33 |          10328.17 |                 109.35 |

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
