## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1037s 
* Code: 1773436667
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:160902
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773436667

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS          |   MonetDB-BHT-8-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               54.13 |
| TPC-DS Q2     |              637.42 |
| TPC-DS Q3     |               54.91 |
| TPC-DS Q4     |             4148.1  |
| TPC-DS Q5     |              312.42 |
| TPC-DS Q6     |              254.49 |
| TPC-DS Q7     |               89.96 |
| TPC-DS Q8     |              106.09 |
| TPC-DS Q9     |              179.09 |
| TPC-DS Q10    |               76.65 |
| TPC-DS Q11    |             2018.26 |
| TPC-DS Q12    |               34.47 |
| TPC-DS Q13    |              153.59 |
| TPC-DS Q14a+b |             7290.79 |
| TPC-DS Q15    |               41.68 |
| TPC-DS Q16    |              306.83 |
| TPC-DS Q17    |              391.75 |
| TPC-DS Q18    |              258.37 |
| TPC-DS Q19    |               83    |
| TPC-DS Q20    |               48.03 |
| TPC-DS Q21    |               96.28 |
| TPC-DS Q22    |             2556.07 |
| TPC-DS Q23a+b |             9043.16 |
| TPC-DS Q24a+b |              860.43 |
| TPC-DS Q25    |              376.37 |
| TPC-DS Q26    |               67.9  |
| TPC-DS Q27    |              310.08 |
| TPC-DS Q28    |              201.81 |
| TPC-DS Q29    |              341.09 |
| TPC-DS Q30    |               29.29 |
| TPC-DS Q31    |              510.87 |
| TPC-DS Q32    |               38.74 |
| TPC-DS Q33    |               46.44 |
| TPC-DS Q34    |               56.09 |
| TPC-DS Q35    |              209.47 |
| TPC-DS Q36    |              258.11 |
| TPC-DS Q37    |              127.71 |
| TPC-DS Q38    |              599.06 |
| TPC-DS Q39a+b |             3810.77 |
| TPC-DS Q40    |              221.62 |
| TPC-DS Q41    |                7.2  |
| TPC-DS Q42    |               36.09 |
| TPC-DS Q43    |              141.85 |
| TPC-DS Q44    |               88.16 |
| TPC-DS Q45    |               23.24 |
| TPC-DS Q46    |               86.02 |
| TPC-DS Q47    |              574.29 |
| TPC-DS Q48    |               97.36 |
| TPC-DS Q49    |              284.76 |
| TPC-DS Q50    |              239.52 |
| TPC-DS Q51    |             1389.58 |
| TPC-DS Q52    |               35.91 |
| TPC-DS Q53    |               53.27 |
| TPC-DS Q54    |               58.66 |
| TPC-DS Q55    |               34.32 |
| TPC-DS Q56    |               61.98 |
| TPC-DS Q57    |              173.99 |
| TPC-DS Q58    |              191.72 |
| TPC-DS Q59    |              258.88 |
| TPC-DS Q60    |               86.63 |
| TPC-DS Q61    |               76.57 |
| TPC-DS Q62    |               47.74 |
| TPC-DS Q63    |               47.59 |
| TPC-DS Q64    |             1319.18 |
| TPC-DS Q65    |              416.54 |
| TPC-DS Q66    |              326.22 |
| TPC-DS Q67    |             1459.46 |
| TPC-DS Q68    |               89.06 |
| TPC-DS Q69    |               41.42 |
| TPC-DS Q70    |              266.85 |
| TPC-DS Q71    |               69.02 |
| TPC-DS Q72    |              259.12 |
| TPC-DS Q73    |               37.61 |
| TPC-DS Q74    |              545.97 |
| TPC-DS Q75    |             1751.65 |
| TPC-DS Q76    |              151.73 |
| TPC-DS Q77    |              169.5  |
| TPC-DS Q78    |             3260.6  |
| TPC-DS Q79    |               86.43 |
| TPC-DS Q80    |             2580.9  |
| TPC-DS Q81    |               51.05 |
| TPC-DS Q82    |              373.66 |
| TPC-DS Q83    |               29.43 |
| TPC-DS Q84    |              130.39 |
| TPC-DS Q85    |               55.68 |
| TPC-DS Q86    |               68.62 |
| TPC-DS Q87    |              745.21 |
| TPC-DS Q88    |              173.53 |
| TPC-DS Q89    |               73.74 |
| TPC-DS Q90    |               17.95 |
| TPC-DS Q91    |               22.99 |
| TPC-DS Q92    |               21.88 |
| TPC-DS Q93    |              431.48 |
| TPC-DS Q94    |               71.08 |
| TPC-DS Q95    |             1111.68 |
| TPC-DS Q96    |               23.05 |
| TPC-DS Q97    |              909.67 |
| TPC-DS Q98    |               83.7  |
| TPC-DS Q99    |               97.34 |

### Loading [s]

| DBMS              |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| MonetDB-BHT-8-1-1 |              1 |             267 |           11 |         666 |        954 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS              |   Geo Times [s] |
|:------------------|----------------:|
| MonetDB-BHT-8-1-1 |            0.18 |

### Power@Size ((3600*SF)/(geo times))

| DBMS              |   Power@Size [~Q/h] |
|:------------------|--------------------:|
| MonetDB-BHT-8-1-1 |             63365.3 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS            |   time [s] |   count |   SF |   Throughput@Size |
|:----------------|-----------:|--------:|-----:|------------------:|
| MonetDB-BHT-8-1 |         68 |       1 |    3 |           15723.5 |

### Workflow

| DBMS              | orig_name       |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:------------------|:----------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| MonetDB-BHT-8-1-1 | MonetDB-BHT-8-1 |    3 |      8 |                1 |            1 |        1773437542 |      1773437610 |

#### Actual

* DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned

* DBMS MonetDB-BHT-8 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-BHT-8-1 |       724.45 |      3.19 |           1.91 |                 11.64 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-BHT-8-1 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-BHT-8-1 |        43.55 |      0.21 |           0.01 |                  2.65 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-BHT-8-1 |        86.18 |      1.67 |           6.47 |                 15.14 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-BHT-8-1 |        15.79 |         0 |           0.36 |                  0.36 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
