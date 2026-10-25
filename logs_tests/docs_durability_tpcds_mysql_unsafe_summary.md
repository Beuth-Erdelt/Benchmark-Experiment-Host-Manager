## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1185s 
* Code: 1792614849
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is unsafe (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.7.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
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
  * disk:945750
  * datadisk:37665
  * volume_size:1.8T
  * volume_used:924G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: unsafe
  * eval_parameters
    * code:1792614849

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792614849-85fffd955c-jltn2: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      151.00 |           7.00 |            1.00 |         50.00 |           83.00 |              8 |           0 |             | None           |             0 | False         |               23.84 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        476 |            0.71 |             5084.63 |            748.74 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        476 |            0.71 |             5084.63 |            748.74 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             66.57 |
| TPC-DS Q2     |           3690.70 |
| TPC-DS Q3     |             13.51 |
| TPC-DS Q4     |          54645.20 |
| TPC-DS Q5     |          14430.11 |
| TPC-DS Q6     |          59257.38 |
| TPC-DS Q7     |            627.10 |
| TPC-DS Q8     |            339.76 |
| TPC-DS Q9     |           3909.22 |
| TPC-DS Q10    |             78.56 |
| TPC-DS Q11    |          37022.95 |
| TPC-DS Q12    |            237.55 |
| TPC-DS Q13    |           1099.22 |
| TPC-DS Q14a+b |          40833.56 |
| TPC-DS Q15    |            161.69 |
| TPC-DS Q16    |            108.86 |
| TPC-DS Q17    |            446.61 |
| TPC-DS Q18    |            679.18 |
| TPC-DS Q19    |            254.75 |
| TPC-DS Q20    |            412.03 |
| TPC-DS Q21    |           1524.86 |
| TPC-DS Q22    |           3871.09 |
| TPC-DS Q23a+b |          45934.14 |
| TPC-DS Q24a+b |           1174.97 |
| TPC-DS Q25    |            159.45 |
| TPC-DS Q26    |            477.85 |
| TPC-DS Q27    |            416.55 |
| TPC-DS Q28    |           2784.03 |
| TPC-DS Q29    |             93.00 |
| TPC-DS Q30    |            410.87 |
| TPC-DS Q31    |           8923.79 |
| TPC-DS Q32    |            247.34 |
| TPC-DS Q33    |            554.34 |
| TPC-DS Q34    |            760.38 |
| TPC-DS Q35    |          10995.99 |
| TPC-DS Q36    |            985.53 |
| TPC-DS Q37    |              9.09 |
| TPC-DS Q38    |           5946.91 |
| TPC-DS Q39a+b |            934.23 |
| TPC-DS Q40    |            130.35 |
| TPC-DS Q41    |           1170.28 |
| TPC-DS Q42    |             20.43 |
| TPC-DS Q43    |              2.42 |
| TPC-DS Q44    |           1257.07 |
| TPC-DS Q45    |            109.91 |
| TPC-DS Q46    |            607.20 |
| TPC-DS Q47    |           8570.75 |
| TPC-DS Q48    |           1112.48 |
| TPC-DS Q49    |            133.00 |
| TPC-DS Q50    |             25.19 |
| TPC-DS Q51    |           7755.92 |
| TPC-DS Q52    |             21.65 |
| TPC-DS Q53    |            174.81 |
| TPC-DS Q54    |           2595.46 |
| TPC-DS Q55    |             13.52 |
| TPC-DS Q56    |            226.74 |
| TPC-DS Q57    |           2618.48 |
| TPC-DS Q58    |           5375.85 |
| TPC-DS Q59    |           4990.11 |
| TPC-DS Q60    |            380.28 |
| TPC-DS Q61    |              2.70 |
| TPC-DS Q62    |           2348.74 |
| TPC-DS Q63    |            220.63 |
| TPC-DS Q64    |            398.64 |
| TPC-DS Q65    |           5907.29 |
| TPC-DS Q66    |           1493.48 |
| TPC-DS Q67    |           6903.80 |
| TPC-DS Q68    |            277.09 |
| TPC-DS Q69    |            445.93 |
| TPC-DS Q70    |           9782.91 |
| TPC-DS Q71    |            457.48 |
| TPC-DS Q72    |          10576.98 |
| TPC-DS Q73    |            868.62 |
| TPC-DS Q74    |           7264.86 |
| TPC-DS Q75    |           1907.51 |
| TPC-DS Q76    |            436.46 |
| TPC-DS Q77    |           7637.15 |
| TPC-DS Q78    |          14908.01 |
| TPC-DS Q79    |           4344.13 |
| TPC-DS Q80    |           7195.29 |
| TPC-DS Q81    |           2290.74 |
| TPC-DS Q82    |              7.59 |
| TPC-DS Q83    |            655.18 |
| TPC-DS Q84    |             49.77 |
| TPC-DS Q85    |             88.97 |
| TPC-DS Q86    |            866.44 |
| TPC-DS Q87    |           6413.73 |
| TPC-DS Q88    |           1552.36 |
| TPC-DS Q89    |             48.81 |
| TPC-DS Q90    |            313.27 |
| TPC-DS Q91    |             18.22 |
| TPC-DS Q92    |             64.68 |
| TPC-DS Q93    |             37.73 |
| TPC-DS Q94    |            381.26 |
| TPC-DS Q95    |           3167.39 |
| TPC-DS Q96    |            122.28 |
| TPC-DS Q97    |           6557.97 |
| TPC-DS Q98    |            907.81 |
| TPC-DS Q99    |           9514.53 |

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
