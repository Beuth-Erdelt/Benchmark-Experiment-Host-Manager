## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 3586s 
* Code: 1783879748
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [2] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:2164173213696
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1116355
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783879748

### SUT Container Restarts
* bexhoma-sut-mysql-1-1783879748-85cd8f4cc4-6d8x6: 0 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 | 3.00 |     1852.00 |           0.00 |            0.00 |        227.00 |         1622.00 |              2 |           0 |             | None           |             0 | False         |                5.83 |

### Execution

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |       1524 |            2.47 |             4404.45 |            701.57 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |       1524 |            2.47 |             4404.45 |            701.57 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MySQL-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             78.40 |
| TPC-DS Q2     |          13692.97 |
| TPC-DS Q3     |             23.98 |
| TPC-DS Q4     |         115304.79 |
| TPC-DS Q5     |          30681.82 |
| TPC-DS Q6     |         271783.80 |
| TPC-DS Q7     |           1325.94 |
| TPC-DS Q8     |            862.64 |
| TPC-DS Q9     |          11744.90 |
| TPC-DS Q10    |            913.63 |
| TPC-DS Q11    |          72910.96 |
| TPC-DS Q12    |            835.39 |
| TPC-DS Q13    |           3785.18 |
| TPC-DS Q14a+b |         119243.75 |
| TPC-DS Q15    |            537.02 |
| TPC-DS Q16    |            372.68 |
| TPC-DS Q17    |           1271.80 |
| TPC-DS Q18    |           1420.20 |
| TPC-DS Q19    |            868.80 |
| TPC-DS Q20    |           1544.70 |
| TPC-DS Q21    |          68402.65 |
| TPC-DS Q22    |          10988.92 |
| TPC-DS Q23a+b |         154354.14 |
| TPC-DS Q24a+b |           3005.38 |
| TPC-DS Q25    |            424.24 |
| TPC-DS Q26    |           1625.22 |
| TPC-DS Q27    |            952.77 |
| TPC-DS Q28    |           9833.14 |
| TPC-DS Q29    |            428.40 |
| TPC-DS Q30    |           4206.57 |
| TPC-DS Q31    |          33402.23 |
| TPC-DS Q32    |            991.75 |
| TPC-DS Q33    |            693.03 |
| TPC-DS Q34    |           1674.20 |
| TPC-DS Q35    |           7120.16 |
| TPC-DS Q36    |           3884.16 |
| TPC-DS Q37    |             20.33 |
| TPC-DS Q38    |          24734.98 |
| TPC-DS Q39a+b |           5254.09 |
| TPC-DS Q40    |            462.91 |
| TPC-DS Q41    |           5554.08 |
| TPC-DS Q42    |           1224.59 |
| TPC-DS Q43    |              2.63 |
| TPC-DS Q44    |              2.62 |
| TPC-DS Q45    |            572.31 |
| TPC-DS Q46    |           3907.38 |
| TPC-DS Q47    |          12765.31 |
| TPC-DS Q48    |           3671.38 |
| TPC-DS Q49    |           4306.05 |
| TPC-DS Q50    |             84.74 |
| TPC-DS Q51    |          17169.02 |
| TPC-DS Q52    |            801.73 |
| TPC-DS Q53    |            927.97 |
| TPC-DS Q54    |           7409.39 |
| TPC-DS Q55    |            997.23 |
| TPC-DS Q56    |            655.08 |
| TPC-DS Q57    |           9084.60 |
| TPC-DS Q58    |          19703.14 |
| TPC-DS Q59    |          20165.00 |
| TPC-DS Q60    |           1557.74 |
| TPC-DS Q61    |           2088.12 |
| TPC-DS Q62    |           8449.80 |
| TPC-DS Q63    |            918.79 |
| TPC-DS Q64    |           1170.43 |
| TPC-DS Q65    |          22724.26 |
| TPC-DS Q66    |           6335.36 |
| TPC-DS Q67    |          26202.02 |
| TPC-DS Q68    |            845.31 |
| TPC-DS Q69    |              2.44 |
| TPC-DS Q70    |          37176.09 |
| TPC-DS Q71    |           1336.15 |
| TPC-DS Q72    |          36807.20 |
| TPC-DS Q73    |            840.35 |
| TPC-DS Q74    |          15149.67 |
| TPC-DS Q75    |           6154.93 |
| TPC-DS Q76    |           1225.58 |
| TPC-DS Q77    |          28219.03 |
| TPC-DS Q78    |          33955.47 |
| TPC-DS Q79    |           2744.97 |
| TPC-DS Q80    |          23906.21 |
| TPC-DS Q81    |          20819.57 |
| TPC-DS Q82    |             22.19 |
| TPC-DS Q83    |           1962.47 |
| TPC-DS Q84    |             98.34 |
| TPC-DS Q85    |            268.41 |
| TPC-DS Q86    |           3018.81 |
| TPC-DS Q87    |          24237.59 |
| TPC-DS Q88    |          32229.34 |
| TPC-DS Q89    |           5739.63 |
| TPC-DS Q90    |            993.20 |
| TPC-DS Q91    |             50.74 |
| TPC-DS Q92    |            314.65 |
| TPC-DS Q93    |            113.53 |
| TPC-DS Q94    |           1272.14 |
| TPC-DS Q95    |          11390.68 |
| TPC-DS Q96    |           2780.83 |
| TPC-DS Q97    |          16793.11 |
| TPC-DS Q98    |           2863.12 |
| TPC-DS Q99    |          14961.96 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      2936.43 |      6.92 |          27.45 |                 52.96 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         7.18 |      0.12 |           0.01 |                  2.88 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1480.38 |      1.02 |          31.80 |                 57.33 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        27.15 |      0.05 |           0.43 |                  0.44 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.01 |                     0.00 |                0.03 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       0.82 |                     0.00 |                0.03 |                    0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
