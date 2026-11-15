## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1758s 
* Code: 1794655623
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1394132
  * datadisk:37564
  * volume_size:1.8T
  * volume_used:1.4T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794655623

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794655623-5cd8cf6474-nbshf: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      330.00 |          38.00 |            1.00 |        112.00 |          170.00 |              8 |         0 |             | None           |             0 | False         |               10.91 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        936 |            1.05 |             3474.47 |            380.77 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        936 |            1.05 |             3474.47 |            380.77 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             57.65 |
| TPC-DS Q2     |           9747.50 |
| TPC-DS Q3     |             56.63 |
| TPC-DS Q4     |         150431.73 |
| TPC-DS Q5     |          87076.73 |
| TPC-DS Q6     |           1206.26 |
| TPC-DS Q7     |           2721.15 |
| TPC-DS Q8     |           1513.70 |
| TPC-DS Q9     |          17729.39 |
| TPC-DS Q10    |           1230.65 |
| TPC-DS Q11    |         113988.58 |
| TPC-DS Q12    |            941.79 |
| TPC-DS Q13    |           5349.16 |
| TPC-DS Q14a+b |         145006.56 |
| TPC-DS Q15    |           1107.97 |
| TPC-DS Q16    |           1407.54 |
| TPC-DS Q17    |           4652.49 |
| TPC-DS Q18    |           6347.85 |
| TPC-DS Q19    |           2874.45 |
| TPC-DS Q20    |           1355.99 |
| TPC-DS Q21    |           3356.81 |
| TPC-DS Q22    |          54565.37 |
| TPC-DS Q23a+b |          80488.57 |
| TPC-DS Q24a+b |           1941.19 |
| TPC-DS Q25    |            210.96 |
| TPC-DS Q26    |            602.52 |
| TPC-DS Q27    |            562.58 |
| TPC-DS Q28    |           3487.84 |
| TPC-DS Q29    |             60.67 |
| TPC-DS Q30    |            445.55 |
| TPC-DS Q31    |          13247.53 |
| TPC-DS Q32    |            244.61 |
| TPC-DS Q33    |            592.18 |
| TPC-DS Q34    |           1484.85 |
| TPC-DS Q35    |          15477.08 |
| TPC-DS Q36    |           3289.66 |
| TPC-DS Q37    |             11.40 |
| TPC-DS Q38    |           7177.63 |
| TPC-DS Q39a+b |           1207.98 |
| TPC-DS Q40    |            128.35 |
| TPC-DS Q41    |           1006.00 |
| TPC-DS Q42    |             70.28 |
| TPC-DS Q43    |              1.78 |
| TPC-DS Q44    |              5.56 |
| TPC-DS Q45    |            166.58 |
| TPC-DS Q46    |            538.59 |
| TPC-DS Q47    |           9597.35 |
| TPC-DS Q48    |           1438.56 |
| TPC-DS Q49    |            146.02 |
| TPC-DS Q50    |             25.02 |
| TPC-DS Q51    |           7951.54 |
| TPC-DS Q52    |             60.28 |
| TPC-DS Q53    |            167.53 |
| TPC-DS Q54    |           2693.72 |
| TPC-DS Q55    |             35.11 |
| TPC-DS Q56    |            423.60 |
| TPC-DS Q57    |           5050.61 |
| TPC-DS Q58    |           5871.62 |
| TPC-DS Q59    |           5754.25 |
| TPC-DS Q60    |            410.17 |
| TPC-DS Q61    |              2.26 |
| TPC-DS Q62    |           2738.29 |
| TPC-DS Q63    |            213.33 |
| TPC-DS Q64    |            765.71 |
| TPC-DS Q65    |           7272.32 |
| TPC-DS Q66    |           2434.93 |
| TPC-DS Q67    |           8677.36 |
| TPC-DS Q68    |            557.78 |
| TPC-DS Q69    |              3.11 |
| TPC-DS Q70    |          12373.32 |
| TPC-DS Q71    |            687.79 |
| TPC-DS Q72    |          12187.04 |
| TPC-DS Q73    |            842.27 |
| TPC-DS Q74    |           6705.65 |
| TPC-DS Q75    |           2254.26 |
| TPC-DS Q76    |            479.70 |
| TPC-DS Q77    |           8855.17 |
| TPC-DS Q78    |          15438.24 |
| TPC-DS Q79    |           4110.23 |
| TPC-DS Q80    |           9818.36 |
| TPC-DS Q81    |           1895.91 |
| TPC-DS Q82    |             27.54 |
| TPC-DS Q83    |            622.01 |
| TPC-DS Q84    |             60.07 |
| TPC-DS Q85    |             81.54 |
| TPC-DS Q86    |           1330.92 |
| TPC-DS Q87    |           7237.69 |
| TPC-DS Q88    |           2413.87 |
| TPC-DS Q89    |            186.71 |
| TPC-DS Q90    |            334.40 |
| TPC-DS Q91    |             17.82 |
| TPC-DS Q92    |             50.15 |
| TPC-DS Q93    |             51.63 |
| TPC-DS Q94    |            418.57 |
| TPC-DS Q95    |           3640.85 |
| TPC-DS Q96    |            166.50 |
| TPC-DS Q97    |           7452.24 |
| TPC-DS Q98    |            982.53 |
| TPC-DS Q99    |          10532.52 |

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
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
