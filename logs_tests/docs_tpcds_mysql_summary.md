## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1082s 
* Code: 1795665856
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['MySQL'].
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:660165
  * datadisk:37628
  * volume_size:1.8T
  * volume_used:645G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795665856

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1795665856-99bd6f98-kktrs: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      194.00 |           2.00 |            1.00 |         57.00 |          126.00 |              8 |         0 |             | None           |             0 | False         |               18.56 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        432 |            0.75 |             4848.82 |            825.00 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        432 |            0.75 |             4848.82 |            825.00 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |            213.08 |
| TPC-DS Q2     |           3773.76 |
| TPC-DS Q3     |             37.95 |
| TPC-DS Q4     |          50604.77 |
| TPC-DS Q5     |          16744.60 |
| TPC-DS Q6     |            920.87 |
| TPC-DS Q7     |           1681.65 |
| TPC-DS Q8     |            335.21 |
| TPC-DS Q9     |           4381.61 |
| TPC-DS Q10    |            288.26 |
| TPC-DS Q11    |          27444.34 |
| TPC-DS Q12    |            232.12 |
| TPC-DS Q13    |           2023.82 |
| TPC-DS Q14a+b |          39460.28 |
| TPC-DS Q15    |            164.77 |
| TPC-DS Q16    |            381.67 |
| TPC-DS Q17    |            894.60 |
| TPC-DS Q18    |           1210.14 |
| TPC-DS Q19    |            235.38 |
| TPC-DS Q20    |            423.46 |
| TPC-DS Q21    |           1378.53 |
| TPC-DS Q22    |           6648.30 |
| TPC-DS Q23a+b |          43110.61 |
| TPC-DS Q24a+b |           1229.07 |
| TPC-DS Q25    |            468.55 |
| TPC-DS Q26    |            848.42 |
| TPC-DS Q27    |            425.02 |
| TPC-DS Q28    |           2838.38 |
| TPC-DS Q29    |            104.40 |
| TPC-DS Q30    |             58.66 |
| TPC-DS Q31    |           9405.99 |
| TPC-DS Q32    |            316.54 |
| TPC-DS Q33    |            830.35 |
| TPC-DS Q34    |           1226.70 |
| TPC-DS Q35    |          13300.68 |
| TPC-DS Q36    |           2584.77 |
| TPC-DS Q37    |             10.49 |
| TPC-DS Q38    |           7039.64 |
| TPC-DS Q39a+b |            932.77 |
| TPC-DS Q40    |            127.33 |
| TPC-DS Q41    |           1053.19 |
| TPC-DS Q42    |             59.06 |
| TPC-DS Q43    |              2.58 |
| TPC-DS Q44    |              7.30 |
| TPC-DS Q45    |            112.19 |
| TPC-DS Q46    |           1939.15 |
| TPC-DS Q47    |           9829.14 |
| TPC-DS Q48    |           1114.26 |
| TPC-DS Q49    |            125.38 |
| TPC-DS Q50    |             25.29 |
| TPC-DS Q51    |           8199.64 |
| TPC-DS Q52    |             59.82 |
| TPC-DS Q53    |            193.51 |
| TPC-DS Q54    |           3083.88 |
| TPC-DS Q55    |              9.50 |
| TPC-DS Q56    |            209.49 |
| TPC-DS Q57    |           3727.67 |
| TPC-DS Q58    |           5207.82 |
| TPC-DS Q59    |           4727.13 |
| TPC-DS Q60    |            479.04 |
| TPC-DS Q61    |              3.10 |
| TPC-DS Q62    |           2438.30 |
| TPC-DS Q63    |            172.55 |
| TPC-DS Q64    |            359.72 |
| TPC-DS Q65    |           5786.58 |
| TPC-DS Q66    |           2957.16 |
| TPC-DS Q67    |           8762.27 |
| TPC-DS Q68    |            283.07 |
| TPC-DS Q69    |            457.85 |
| TPC-DS Q70    |          11645.62 |
| TPC-DS Q71    |            563.15 |
| TPC-DS Q72    |          10966.86 |
| TPC-DS Q73    |            293.95 |
| TPC-DS Q74    |           5717.65 |
| TPC-DS Q75    |           1817.44 |
| TPC-DS Q76    |            473.42 |
| TPC-DS Q77    |           8432.43 |
| TPC-DS Q78    |          14760.25 |
| TPC-DS Q79    |           3840.62 |
| TPC-DS Q80    |           9680.46 |
| TPC-DS Q81    |           1931.32 |
| TPC-DS Q82    |              7.86 |
| TPC-DS Q83    |            648.64 |
| TPC-DS Q84    |             99.84 |
| TPC-DS Q85    |             70.39 |
| TPC-DS Q86    |            981.20 |
| TPC-DS Q87    |           7030.71 |
| TPC-DS Q88    |           2302.70 |
| TPC-DS Q89    |              8.60 |
| TPC-DS Q90    |            313.67 |
| TPC-DS Q91    |             14.44 |
| TPC-DS Q92    |             43.39 |
| TPC-DS Q93    |             37.86 |
| TPC-DS Q94    |            399.25 |
| TPC-DS Q95    |           3742.43 |
| TPC-DS Q96    |            247.72 |
| TPC-DS Q97    |           7344.13 |
| TPC-DS Q98    |            872.90 |
| TPC-DS Q99    |          12385.51 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

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
