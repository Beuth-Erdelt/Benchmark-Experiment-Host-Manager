## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 892s 
* Code: 1794765683
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['MariaDB'].
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
  * disk:1130982
  * datadisk:4478
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794765683

### Ingestion
* MariaDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794765683-85884f795c-fdm4k: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      165.00 |           3.00 |            1.00 |         67.00 |           86.00 |              8 |         0 |             | None           |             0 | False         |               21.82 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        299 |            0.66 |             5567.50 |           1191.97 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        299 |            0.66 |             5567.50 |           1191.97 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               12.02 |
| TPC-DS Q2     |             3914.59 |
| TPC-DS Q3     |               17.91 |
| TPC-DS Q4     |             9160.35 |
| TPC-DS Q5     |             7505.51 |
| TPC-DS Q6     |              814.13 |
| TPC-DS Q7     |             2759.07 |
| TPC-DS Q8     |              292.00 |
| TPC-DS Q9     |             3869.20 |
| TPC-DS Q10    |              104.49 |
| TPC-DS Q11    |             6649.44 |
| TPC-DS Q12    |              227.88 |
| TPC-DS Q13    |              779.72 |
| TPC-DS Q14a+b |            39232.98 |
| TPC-DS Q15    |              131.73 |
| TPC-DS Q16    |             7811.43 |
| TPC-DS Q17    |              637.26 |
| TPC-DS Q18    |             1706.17 |
| TPC-DS Q19    |              294.63 |
| TPC-DS Q20    |              348.97 |
| TPC-DS Q21    |              909.52 |
| TPC-DS Q22    |            14266.50 |
| TPC-DS Q23a+b |            42775.20 |
| TPC-DS Q24a+b |               47.53 |
| TPC-DS Q25    |              164.29 |
| TPC-DS Q26    |              689.16 |
| TPC-DS Q27    |             2634.24 |
| TPC-DS Q28    |             2615.38 |
| TPC-DS Q29    |              102.67 |
| TPC-DS Q30    |               85.42 |
| TPC-DS Q31    |             1178.74 |
| TPC-DS Q32    |               10.02 |
| TPC-DS Q33    |              148.21 |
| TPC-DS Q34    |             2542.69 |
| TPC-DS Q35    |              996.12 |
| TPC-DS Q36    |             2220.82 |
| TPC-DS Q37    |             2971.84 |
| TPC-DS Q38    |             5753.15 |
| TPC-DS Q39a+b |              880.16 |
| TPC-DS Q40    |              135.32 |
| TPC-DS Q41    |              348.12 |
| TPC-DS Q42    |              207.51 |
| TPC-DS Q43    |              792.77 |
| TPC-DS Q44    |                1.20 |
| TPC-DS Q45    |              104.79 |
| TPC-DS Q46    |             2451.52 |
| TPC-DS Q47    |            13468.00 |
| TPC-DS Q48    |              869.20 |
| TPC-DS Q49    |              119.95 |
| TPC-DS Q50    |               26.55 |
| TPC-DS Q51    |             6601.84 |
| TPC-DS Q52    |              170.13 |
| TPC-DS Q53    |              119.60 |
| TPC-DS Q54    |              899.79 |
| TPC-DS Q55    |              163.12 |
| TPC-DS Q56    |              110.91 |
| TPC-DS Q57    |             5088.11 |
| TPC-DS Q58    |             4560.75 |
| TPC-DS Q59    |             6717.47 |
| TPC-DS Q60    |              221.90 |
| TPC-DS Q61    |              251.79 |
| TPC-DS Q62    |             1286.78 |
| TPC-DS Q63    |              352.19 |
| TPC-DS Q64    |              440.30 |
| TPC-DS Q65    |             4331.30 |
| TPC-DS Q66    |              895.15 |
| TPC-DS Q67    |             5221.76 |
| TPC-DS Q68    |             2710.04 |
| TPC-DS Q69    |                1.39 |
| TPC-DS Q70    |             6055.95 |
| TPC-DS Q71    |              391.02 |
| TPC-DS Q72    |              616.09 |
| TPC-DS Q73    |             2102.17 |
| TPC-DS Q74    |             4538.50 |
| TPC-DS Q75    |             4165.49 |
| TPC-DS Q76    |              378.01 |
| TPC-DS Q77    |             5410.07 |
| TPC-DS Q78    |             4506.59 |
| TPC-DS Q79    |             2523.45 |
| TPC-DS Q80    |              402.74 |
| TPC-DS Q81    |              155.67 |
| TPC-DS Q82    |             2939.23 |
| TPC-DS Q83    |              691.34 |
| TPC-DS Q84    |               40.69 |
| TPC-DS Q85    |               97.33 |
| TPC-DS Q86    |              629.35 |
| TPC-DS Q87    |             5373.73 |
| TPC-DS Q88    |             9685.38 |
| TPC-DS Q89    |             1047.48 |
| TPC-DS Q90    |               87.69 |
| TPC-DS Q91    |               10.13 |
| TPC-DS Q92    |                4.28 |
| TPC-DS Q93    |               39.74 |
| TPC-DS Q94    |              441.47 |
| TPC-DS Q95    |              580.72 |
| TPC-DS Q96    |              519.51 |
| TPC-DS Q97    |             4007.83 |
| TPC-DS Q98    |              677.82 |
| TPC-DS Q99    |             2492.48 |

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
