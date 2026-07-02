## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 1942s 
* Code: 1782973916
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type shared and size 2000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:636767
  * volume_size:2.0T
  * volume_used:53G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:1024Gi
  * limits_memory:1024Gi
  * eval_parameters
    * code:1782973916

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1782973916-bc785fd48-srthn: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |   30 |     1435.00 |          36.00 |            2.00 |        346.00 |         1029.00 |              8 |           0 |             | None           |             0 | False         |               75.26 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |        442 |            0.80 |           139643.82 |          24190.05 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |        442 |            0.80 |           139643.82 |          24190.05 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              268.96 |
| TPC-DS Q2     |             1743.13 |
| TPC-DS Q3     |             1877.89 |
| TPC-DS Q4     |            21483.63 |
| TPC-DS Q5     |             2011.46 |
| TPC-DS Q6     |              649.53 |
| TPC-DS Q7     |              353.08 |
| TPC-DS Q8     |              493.33 |
| TPC-DS Q9     |              783.38 |
| TPC-DS Q10    |              190.56 |
| TPC-DS Q11    |             8402.45 |
| TPC-DS Q12    |              160.95 |
| TPC-DS Q13    |              503.64 |
| TPC-DS Q14a+b |            41366.90 |
| TPC-DS Q15    |              160.74 |
| TPC-DS Q16    |            45606.84 |
| TPC-DS Q17    |             2613.10 |
| TPC-DS Q18    |              960.92 |
| TPC-DS Q19    |              206.41 |
| TPC-DS Q20    |              143.13 |
| TPC-DS Q21    |              167.80 |
| TPC-DS Q22    |             1382.52 |
| TPC-DS Q23a+b |            45821.75 |
| TPC-DS Q24a+b |            24162.32 |
| TPC-DS Q25    |             3114.50 |
| TPC-DS Q26    |              289.04 |
| TPC-DS Q27    |             1487.51 |
| TPC-DS Q28    |              980.75 |
| TPC-DS Q29    |             2818.04 |
| TPC-DS Q30    |               72.79 |
| TPC-DS Q31    |             2251.45 |
| TPC-DS Q32    |              165.22 |
| TPC-DS Q33    |              103.68 |
| TPC-DS Q34    |              244.27 |
| TPC-DS Q35    |             1234.49 |
| TPC-DS Q36    |             1569.94 |
| TPC-DS Q37    |              517.28 |
| TPC-DS Q38    |             2834.53 |
| TPC-DS Q39a+b |             1603.64 |
| TPC-DS Q40    |             1222.29 |
| TPC-DS Q41    |                7.58 |
| TPC-DS Q42    |              112.51 |
| TPC-DS Q43    |              251.62 |
| TPC-DS Q44    |              273.62 |
| TPC-DS Q45    |              157.63 |
| TPC-DS Q46    |              209.76 |
| TPC-DS Q47    |             1072.51 |
| TPC-DS Q48    |              353.60 |
| TPC-DS Q49    |             1590.88 |
| TPC-DS Q50    |              701.24 |
| TPC-DS Q51    |             2941.70 |
| TPC-DS Q52    |               94.62 |
| TPC-DS Q53    |               96.69 |
| TPC-DS Q54    |              122.73 |
| TPC-DS Q55    |               76.83 |
| TPC-DS Q56    |              100.05 |
| TPC-DS Q57    |              164.61 |
| TPC-DS Q58    |             6448.39 |
| TPC-DS Q59    |             1091.47 |
| TPC-DS Q60    |              134.81 |
| TPC-DS Q61    |              222.71 |
| TPC-DS Q62    |              372.24 |
| TPC-DS Q63    |               98.21 |
| TPC-DS Q64    |             6772.62 |
| TPC-DS Q65    |             1412.03 |
| TPC-DS Q66    |             2242.74 |
| TPC-DS Q67    |             7158.08 |
| TPC-DS Q68    |              496.84 |
| TPC-DS Q69    |              102.20 |
| TPC-DS Q70    |             2699.61 |
| TPC-DS Q71    |              233.09 |
| TPC-DS Q72    |             1426.64 |
| TPC-DS Q73    |               96.58 |
| TPC-DS Q74    |             2355.94 |
| TPC-DS Q75    |             7741.86 |
| TPC-DS Q76    |             5393.72 |
| TPC-DS Q77    |             1096.27 |
| TPC-DS Q78    |            18910.63 |
| TPC-DS Q79    |              324.73 |
| TPC-DS Q80    |            15288.44 |
| TPC-DS Q81    |              163.48 |
| TPC-DS Q82    |             1409.14 |
| TPC-DS Q83    |              321.31 |
| TPC-DS Q84    |               43.25 |
| TPC-DS Q85    |             1217.36 |
| TPC-DS Q86    |              533.41 |
| TPC-DS Q87    |             4013.35 |
| TPC-DS Q88    |              968.91 |
| TPC-DS Q89    |              284.76 |
| TPC-DS Q90    |              143.25 |
| TPC-DS Q91    |               44.61 |
| TPC-DS Q92    |              147.50 |
| TPC-DS Q93    |             2529.62 |
| TPC-DS Q94    |            42605.79 |
| TPC-DS Q95    |            46219.09 |
| TPC-DS Q96    |              241.16 |
| TPC-DS Q97    |             5697.41 |
| TPC-DS Q98    |              280.28 |
| TPC-DS Q99    |              331.28 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      2114.76 |     11.97 |          49.86 |                 50.57 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       478.98 |      2.55 |           0.01 |                  3.36 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      7564.32 |     78.75 |         421.12 |                421.13 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        28.65 |      0.15 |           0.43 |                  0.44 |

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
