## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 862s 
* Code: 1795663925
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:627012
  * datadisk:4466
  * volume_size:1.8T
  * volume_used:613G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795663925

### Ingestion
* MariaDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795663925-5c5f98b88c-cz2j9: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      167.00 |           2.00 |            0.00 |         70.00 |           85.00 |              8 |         0 |             | None           |             0 | False         |               21.56 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        318 |            0.66 |             5573.67 |           1120.75 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        318 |            0.66 |             5573.67 |           1120.75 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               15.31 |
| TPC-DS Q2     |             4217.99 |
| TPC-DS Q3     |               16.69 |
| TPC-DS Q4     |             8648.62 |
| TPC-DS Q5     |             6689.09 |
| TPC-DS Q6     |              759.85 |
| TPC-DS Q7     |             2620.08 |
| TPC-DS Q8     |              775.71 |
| TPC-DS Q9     |             3400.15 |
| TPC-DS Q10    |               73.77 |
| TPC-DS Q11    |             6740.60 |
| TPC-DS Q12    |              189.48 |
| TPC-DS Q13    |             1643.16 |
| TPC-DS Q14a+b |            44059.91 |
| TPC-DS Q15    |              130.55 |
| TPC-DS Q16    |             7382.76 |
| TPC-DS Q17    |              593.03 |
| TPC-DS Q18    |             1429.04 |
| TPC-DS Q19    |              168.56 |
| TPC-DS Q20    |              341.19 |
| TPC-DS Q21    |              854.00 |
| TPC-DS Q22    |            13745.41 |
| TPC-DS Q23a+b |            43839.49 |
| TPC-DS Q24a+b |               23.05 |
| TPC-DS Q25    |              116.48 |
| TPC-DS Q26    |              605.35 |
| TPC-DS Q27    |             2452.32 |
| TPC-DS Q28    |             2594.18 |
| TPC-DS Q29    |               65.07 |
| TPC-DS Q30    |               75.80 |
| TPC-DS Q31    |             1058.50 |
| TPC-DS Q32    |                5.87 |
| TPC-DS Q33    |              129.12 |
| TPC-DS Q34    |             2268.53 |
| TPC-DS Q35    |              837.20 |
| TPC-DS Q36    |             2186.00 |
| TPC-DS Q37    |             3289.76 |
| TPC-DS Q38    |             5333.36 |
| TPC-DS Q39a+b |             1252.60 |
| TPC-DS Q40    |              150.65 |
| TPC-DS Q41    |              450.10 |
| TPC-DS Q42    |              166.59 |
| TPC-DS Q43    |              777.94 |
| TPC-DS Q44    |                1.73 |
| TPC-DS Q45    |               92.63 |
| TPC-DS Q46    |             3119.65 |
| TPC-DS Q47    |            12453.77 |
| TPC-DS Q48    |              849.21 |
| TPC-DS Q49    |               96.15 |
| TPC-DS Q50    |               21.43 |
| TPC-DS Q51    |             6319.71 |
| TPC-DS Q52    |              170.47 |
| TPC-DS Q53    |              106.70 |
| TPC-DS Q54    |              904.79 |
| TPC-DS Q55    |              164.97 |
| TPC-DS Q56    |              112.36 |
| TPC-DS Q57    |             5036.64 |
| TPC-DS Q58    |             4688.03 |
| TPC-DS Q59    |             7091.12 |
| TPC-DS Q60    |              542.80 |
| TPC-DS Q61    |              271.98 |
| TPC-DS Q62    |             1323.43 |
| TPC-DS Q63    |              119.70 |
| TPC-DS Q64    |              443.75 |
| TPC-DS Q65    |             5519.51 |
| TPC-DS Q66    |              931.28 |
| TPC-DS Q67    |             6322.63 |
| TPC-DS Q68    |             2399.98 |
| TPC-DS Q69    |                1.87 |
| TPC-DS Q70    |             6289.80 |
| TPC-DS Q71    |              395.80 |
| TPC-DS Q72    |              615.05 |
| TPC-DS Q73    |             2113.40 |
| TPC-DS Q74    |             4831.56 |
| TPC-DS Q75    |             4416.22 |
| TPC-DS Q76    |              345.37 |
| TPC-DS Q77    |             4904.66 |
| TPC-DS Q78    |             4135.71 |
| TPC-DS Q79    |             2399.52 |
| TPC-DS Q80    |              382.24 |
| TPC-DS Q81    |              151.32 |
| TPC-DS Q82    |             2932.95 |
| TPC-DS Q83    |              705.39 |
| TPC-DS Q84    |               43.26 |
| TPC-DS Q85    |               97.09 |
| TPC-DS Q86    |              623.12 |
| TPC-DS Q87    |             5648.93 |
| TPC-DS Q88    |             7385.40 |
| TPC-DS Q89    |             1492.66 |
| TPC-DS Q90    |              318.75 |
| TPC-DS Q91    |               13.00 |
| TPC-DS Q92    |                6.38 |
| TPC-DS Q93    |               33.38 |
| TPC-DS Q94    |              354.79 |
| TPC-DS Q95    |              566.92 |
| TPC-DS Q96    |              489.73 |
| TPC-DS Q97    |             4965.17 |
| TPC-DS Q98    |              694.91 |
| TPC-DS Q99    |             2507.00 |

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
