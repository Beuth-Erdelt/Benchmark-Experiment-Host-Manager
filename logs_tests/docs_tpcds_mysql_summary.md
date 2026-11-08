## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1204s 
* Code: 1794056742
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
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:889509
  * datadisk:37612
  * volume_size:1.8T
  * volume_used:869G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794056742

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794056742-598769b998-7qsnq: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      221.00 |           3.00 |            1.00 |         74.00 |          131.00 |              8 |           0 |             | None           |             0 | False         |               16.29 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        485 |            0.77 |             4769.05 |            734.85 |          -1 | mysql-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        485 |            0.77 |             4769.05 |            734.85 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             53.72 |
| TPC-DS Q2     |           3536.81 |
| TPC-DS Q3     |              9.75 |
| TPC-DS Q4     |          44276.04 |
| TPC-DS Q5     |          14974.10 |
| TPC-DS Q6     |          62675.78 |
| TPC-DS Q7     |           1542.51 |
| TPC-DS Q8     |            316.94 |
| TPC-DS Q9     |           3473.66 |
| TPC-DS Q10    |            268.29 |
| TPC-DS Q11    |          26430.74 |
| TPC-DS Q12    |            231.63 |
| TPC-DS Q13    |           1786.33 |
| TPC-DS Q14a+b |          35019.21 |
| TPC-DS Q15    |            141.35 |
| TPC-DS Q16    |            169.44 |
| TPC-DS Q17    |            913.38 |
| TPC-DS Q18    |           1574.86 |
| TPC-DS Q19    |            330.88 |
| TPC-DS Q20    |            408.30 |
| TPC-DS Q21    |           1374.36 |
| TPC-DS Q22    |           6750.05 |
| TPC-DS Q23a+b |          40156.36 |
| TPC-DS Q24a+b |           1887.95 |
| TPC-DS Q25    |            141.18 |
| TPC-DS Q26    |            491.23 |
| TPC-DS Q27    |            579.42 |
| TPC-DS Q28    |           3439.47 |
| TPC-DS Q29    |             54.20 |
| TPC-DS Q30    |            394.89 |
| TPC-DS Q31    |          10730.40 |
| TPC-DS Q32    |            246.26 |
| TPC-DS Q33    |            573.63 |
| TPC-DS Q34    |           1512.71 |
| TPC-DS Q35    |          12814.67 |
| TPC-DS Q36    |           2353.63 |
| TPC-DS Q37    |              7.01 |
| TPC-DS Q38    |           6450.34 |
| TPC-DS Q39a+b |            942.42 |
| TPC-DS Q40    |            128.47 |
| TPC-DS Q41    |           1051.13 |
| TPC-DS Q42    |             18.21 |
| TPC-DS Q43    |              2.20 |
| TPC-DS Q44    |              5.35 |
| TPC-DS Q45    |            148.17 |
| TPC-DS Q46    |           2101.18 |
| TPC-DS Q47    |           9202.59 |
| TPC-DS Q48    |            603.43 |
| TPC-DS Q49    |            112.94 |
| TPC-DS Q50    |             19.91 |
| TPC-DS Q51    |           6872.68 |
| TPC-DS Q52    |             17.85 |
| TPC-DS Q53    |            171.05 |
| TPC-DS Q54    |           2439.92 |
| TPC-DS Q55    |             11.52 |
| TPC-DS Q56    |            197.55 |
| TPC-DS Q57    |           2522.28 |
| TPC-DS Q58    |           4779.06 |
| TPC-DS Q59    |           4758.80 |
| TPC-DS Q60    |            330.20 |
| TPC-DS Q61    |              2.32 |
| TPC-DS Q62    |           2336.42 |
| TPC-DS Q63    |            180.77 |
| TPC-DS Q64    |            327.51 |
| TPC-DS Q65    |           5369.76 |
| TPC-DS Q66    |           2186.22 |
| TPC-DS Q67    |           7514.10 |
| TPC-DS Q68    |            264.15 |
| TPC-DS Q69    |            399.75 |
| TPC-DS Q70    |          10469.41 |
| TPC-DS Q71    |            373.73 |
| TPC-DS Q72    |          11442.23 |
| TPC-DS Q73    |           1119.06 |
| TPC-DS Q74    |           7894.49 |
| TPC-DS Q75    |           2423.69 |
| TPC-DS Q76    |            533.23 |
| TPC-DS Q77    |          10343.57 |
| TPC-DS Q78    |          20322.83 |
| TPC-DS Q79    |           5398.11 |
| TPC-DS Q80    |          12373.17 |
| TPC-DS Q81    |           3072.73 |
| TPC-DS Q82    |              8.09 |
| TPC-DS Q83    |            855.53 |
| TPC-DS Q84    |             72.06 |
| TPC-DS Q85    |            126.43 |
| TPC-DS Q86    |           1218.65 |
| TPC-DS Q87    |           8506.68 |
| TPC-DS Q88    |           2474.25 |
| TPC-DS Q89    |             93.21 |
| TPC-DS Q90    |            390.75 |
| TPC-DS Q91    |             15.90 |
| TPC-DS Q92    |             57.53 |
| TPC-DS Q93    |             46.67 |
| TPC-DS Q94    |            500.87 |
| TPC-DS Q95    |           4201.58 |
| TPC-DS Q96    |            142.29 |
| TPC-DS Q97    |           9542.70 |
| TPC-DS Q98    |           1335.71 |
| TPC-DS Q99    |          13457.41 |

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
