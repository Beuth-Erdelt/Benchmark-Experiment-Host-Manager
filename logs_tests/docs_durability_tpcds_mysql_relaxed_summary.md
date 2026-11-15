## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1133s 
* Code: 1794614153
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1110798
  * datadisk:37580
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794614153

### Ingestion
* MySQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794614153-6d87447b64-q62bb: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |      222.00 |           4.00 |            1.00 |         77.00 |          130.00 |              8 |         0 |             | None           |             0 | False         |               16.22 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        436 |            0.76 |             4767.73 |            817.43 |          -1 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        436 |            0.76 |             4767.73 |            817.43 |          -1 |

#### Query Completion per Phase

| phase       |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mysql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mysql-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |            193.63 |
| TPC-DS Q2     |           3797.10 |
| TPC-DS Q3     |             13.35 |
| TPC-DS Q4     |          47844.39 |
| TPC-DS Q5     |          15574.53 |
| TPC-DS Q6     |            874.32 |
| TPC-DS Q7     |           1557.96 |
| TPC-DS Q8     |            734.30 |
| TPC-DS Q9     |           3571.15 |
| TPC-DS Q10    |            458.25 |
| TPC-DS Q11    |          28014.07 |
| TPC-DS Q12    |            361.55 |
| TPC-DS Q13    |           2199.28 |
| TPC-DS Q14a+b |          43997.64 |
| TPC-DS Q15    |            162.72 |
| TPC-DS Q16    |            297.65 |
| TPC-DS Q17    |           1039.44 |
| TPC-DS Q18    |           1182.41 |
| TPC-DS Q19    |            276.43 |
| TPC-DS Q20    |            413.25 |
| TPC-DS Q21    |           1377.19 |
| TPC-DS Q22    |           6476.02 |
| TPC-DS Q23a+b |          43448.41 |
| TPC-DS Q24a+b |             48.89 |
| TPC-DS Q25    |            192.33 |
| TPC-DS Q26    |            378.52 |
| TPC-DS Q27    |            416.71 |
| TPC-DS Q28    |           3090.26 |
| TPC-DS Q29    |             97.88 |
| TPC-DS Q30    |            382.92 |
| TPC-DS Q31    |           9734.60 |
| TPC-DS Q32    |             55.57 |
| TPC-DS Q33    |            664.51 |
| TPC-DS Q34    |           1702.17 |
| TPC-DS Q35    |          16959.85 |
| TPC-DS Q36    |           3510.80 |
| TPC-DS Q37    |              7.96 |
| TPC-DS Q38    |           7640.58 |
| TPC-DS Q39a+b |           1932.31 |
| TPC-DS Q40    |            182.78 |
| TPC-DS Q41    |           1305.44 |
| TPC-DS Q42    |             18.49 |
| TPC-DS Q43    |              2.54 |
| TPC-DS Q44    |           1735.63 |
| TPC-DS Q45    |            135.87 |
| TPC-DS Q46    |            579.44 |
| TPC-DS Q47    |          10246.93 |
| TPC-DS Q48    |            989.51 |
| TPC-DS Q49    |            124.99 |
| TPC-DS Q50    |             32.65 |
| TPC-DS Q51    |           7483.85 |
| TPC-DS Q52    |             20.44 |
| TPC-DS Q53    |            166.08 |
| TPC-DS Q54    |           3217.83 |
| TPC-DS Q55    |              8.82 |
| TPC-DS Q56    |            234.14 |
| TPC-DS Q57    |           4423.45 |
| TPC-DS Q58    |           5426.96 |
| TPC-DS Q59    |           4554.75 |
| TPC-DS Q60    |            792.93 |
| TPC-DS Q61    |              3.49 |
| TPC-DS Q62    |           3173.81 |
| TPC-DS Q63    |            258.57 |
| TPC-DS Q64    |            514.57 |
| TPC-DS Q65    |           5387.19 |
| TPC-DS Q66    |           2759.51 |
| TPC-DS Q67    |           8643.10 |
| TPC-DS Q68    |            264.67 |
| TPC-DS Q69    |            437.12 |
| TPC-DS Q70    |          10917.54 |
| TPC-DS Q71    |            427.42 |
| TPC-DS Q72    |          10215.96 |
| TPC-DS Q73    |           1027.18 |
| TPC-DS Q74    |           6069.39 |
| TPC-DS Q75    |           1851.03 |
| TPC-DS Q76    |            410.03 |
| TPC-DS Q77    |           7746.59 |
| TPC-DS Q78    |          14606.84 |
| TPC-DS Q79    |           3787.94 |
| TPC-DS Q80    |           9356.37 |
| TPC-DS Q81    |            338.14 |
| TPC-DS Q82    |              9.40 |
| TPC-DS Q83    |            615.78 |
| TPC-DS Q84    |             63.18 |
| TPC-DS Q85    |             78.49 |
| TPC-DS Q86    |            902.47 |
| TPC-DS Q87    |           5904.54 |
| TPC-DS Q88    |           2474.55 |
| TPC-DS Q89    |            230.00 |
| TPC-DS Q90    |            312.13 |
| TPC-DS Q91    |             14.17 |
| TPC-DS Q92    |             20.59 |
| TPC-DS Q93    |             37.79 |
| TPC-DS Q94    |            390.11 |
| TPC-DS Q95    |           3376.57 |
| TPC-DS Q96    |            197.35 |
| TPC-DS Q97    |           7720.88 |
| TPC-DS Q98    |            872.76 |
| TPC-DS Q99    |          11219.63 |

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
