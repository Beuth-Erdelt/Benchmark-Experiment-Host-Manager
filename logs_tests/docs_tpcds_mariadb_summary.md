## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 4037s 
* Code: 1782833902
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:268035
  * datadisk:4543
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782833902

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1782833902-fdb6f66d8-5zpn7: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      585.00 |           0.00 |            0.00 |         66.00 |          512.00 |              8 |           0 |             | None           |             0 | False         |                6.15 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3204 |            0.99 |             3680.65 |            108.99 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3204 |            0.99 |             3680.65 |            108.99 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               21.54 |
| TPC-DS Q2     |             4688.76 |
| TPC-DS Q3     |               19.31 |
| TPC-DS Q4     |            12070.81 |
| TPC-DS Q5     |             8657.12 |
| TPC-DS Q6     |              741.86 |
| TPC-DS Q7     |             4017.22 |
| TPC-DS Q8     |              381.48 |
| TPC-DS Q9     |             3799.48 |
| TPC-DS Q10    |               60.42 |
| TPC-DS Q11    |             8152.01 |
| TPC-DS Q12    |              258.03 |
| TPC-DS Q13    |             1067.62 |
| TPC-DS Q14a+b |            49638.93 |
| TPC-DS Q15    |              175.56 |
| TPC-DS Q16    |            11121.39 |
| TPC-DS Q17    |              707.26 |
| TPC-DS Q18    |             1952.32 |
| TPC-DS Q19    |              309.52 |
| TPC-DS Q20    |              433.49 |
| TPC-DS Q21    |            21572.00 |
| TPC-DS Q22    |            19869.36 |
| TPC-DS Q23a+b |            57465.28 |
| TPC-DS Q24a+b |               32.58 |
| TPC-DS Q25    |              153.86 |
| TPC-DS Q26    |              868.66 |
| TPC-DS Q27    |             1665.35 |
| TPC-DS Q28    |             2837.08 |
| TPC-DS Q29    |               94.89 |
| TPC-DS Q30    |              106.37 |
| TPC-DS Q31    |             1408.80 |
| TPC-DS Q32    |               12.06 |
| TPC-DS Q33    |              158.76 |
| TPC-DS Q34    |             3045.86 |
| TPC-DS Q35    |             1288.52 |
| TPC-DS Q36    |             1771.70 |
| TPC-DS Q37    |             3663.48 |
| TPC-DS Q38    |             7218.75 |
| TPC-DS Q39a+b |             1314.93 |
| TPC-DS Q40    |              179.28 |
| TPC-DS Q41    |              408.73 |
| TPC-DS Q42    |              281.63 |
| TPC-DS Q43    |             1109.11 |
| TPC-DS Q44    |             1198.02 |
| TPC-DS Q45    |              134.35 |
| TPC-DS Q46    |             3230.52 |
| TPC-DS Q47    |            15022.31 |
| TPC-DS Q48    |             1248.50 |
| TPC-DS Q49    |              109.78 |
| TPC-DS Q50    |               35.45 |
| TPC-DS Q51    |             7916.88 |
| TPC-DS Q52    |              314.14 |
| TPC-DS Q53    |              153.86 |
| TPC-DS Q54    |             1086.61 |
| TPC-DS Q55    |              247.21 |
| TPC-DS Q56    |              160.67 |
| TPC-DS Q57    |             6159.56 |
| TPC-DS Q58    |             5881.91 |
| TPC-DS Q59    |             9180.81 |
| TPC-DS Q60    |              663.17 |
| TPC-DS Q61    |              402.53 |
| TPC-DS Q62    |             1681.06 |
| TPC-DS Q63    |              136.88 |
| TPC-DS Q64    |              548.86 |
| TPC-DS Q65    |             5857.24 |
| TPC-DS Q66    |             1228.97 |
| TPC-DS Q67    |             7050.47 |
| TPC-DS Q68    |             3057.05 |
| TPC-DS Q69    |                3.60 |
| TPC-DS Q70    |             8193.80 |
| TPC-DS Q71    |              529.04 |
| TPC-DS Q72    |           403601.33 |
| TPC-DS Q73    |             3509.42 |
| TPC-DS Q74    |             6182.05 |
| TPC-DS Q75    |             5714.65 |
| TPC-DS Q76    |              465.15 |
| TPC-DS Q77    |             6261.85 |
| TPC-DS Q78    |             5726.20 |
| TPC-DS Q79    |             3437.41 |
| TPC-DS Q80    |              548.97 |
| TPC-DS Q81    |              220.27 |
| TPC-DS Q82    |             3659.84 |
| TPC-DS Q83    |              935.74 |
| TPC-DS Q84    |               59.40 |
| TPC-DS Q85    |              146.99 |
| TPC-DS Q86    |              919.30 |
| TPC-DS Q87    |             7199.08 |
| TPC-DS Q88    |            16154.30 |
| TPC-DS Q89    |             1615.79 |
| TPC-DS Q90    |              119.56 |
| TPC-DS Q91    |               24.38 |
| TPC-DS Q92    |                9.40 |
| TPC-DS Q93    |               45.70 |
| TPC-DS Q96    |              807.61 |
| TPC-DS Q97    |             5338.46 |
| TPC-DS Q98    |              875.80 |
| TPC-DS Q99    |             4938.86 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=59) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=59) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
