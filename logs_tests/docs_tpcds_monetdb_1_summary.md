## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 1884s 
* Code: 1783005788
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
  * disk:642905
  * volume_size:2.0T
  * volume_used:53G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:1024Gi
  * limits_memory:1024Gi
  * eval_parameters
    * code:1783005788

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1783005788-6674645ddd-nqd6d: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |    SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 30.00 |     1475.00 |           4.00 |            1.00 |        530.00 |          926.00 |              8 |           0 |             | None           |             0 | False         |               73.22 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               95 |        732 |            0.68 |           166879.25 |          14016.39 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               95 |        732 |            0.68 |           166879.25 |          14016.39 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              293.93 |
| TPC-DS Q2     |             1934.26 |
| TPC-DS Q3     |              442.54 |
| TPC-DS Q4     |            16152.60 |
| TPC-DS Q5     |             1368.65 |
| TPC-DS Q6     |              383.03 |
| TPC-DS Q7     |              342.43 |
| TPC-DS Q8     |              306.68 |
| TPC-DS Q9     |              857.80 |
| TPC-DS Q10    |              109.92 |
| TPC-DS Q11    |             6802.43 |
| TPC-DS Q12    |              160.22 |
| TPC-DS Q13    |              496.14 |
| TPC-DS Q14a+b |            34686.66 |
| TPC-DS Q15    |              183.21 |
| TPC-DS Q16    |            40486.93 |
| TPC-DS Q17    |             2397.13 |
| TPC-DS Q18    |              806.73 |
| TPC-DS Q19    |              194.64 |
| TPC-DS Q20    |              143.64 |
| TPC-DS Q21    |              152.05 |
| TPC-DS Q22    |             1069.65 |
| TPC-DS Q23a+b |            53920.76 |
| TPC-DS Q24a+b |            20106.17 |
| TPC-DS Q25    |             2403.08 |
| TPC-DS Q26    |              254.80 |
| TPC-DS Q27    |             1126.26 |
| TPC-DS Q28    |              983.10 |
| TPC-DS Q29    |             2247.58 |
| TPC-DS Q30    |              113.98 |
| TPC-DS Q31    |             2005.23 |
| TPC-DS Q32    |              189.70 |
| TPC-DS Q33    |               93.11 |
| TPC-DS Q34    |              208.59 |
| TPC-DS Q35    |             1015.40 |
| TPC-DS Q36    |             1157.83 |
| TPC-DS Q37    |              515.81 |
| TPC-DS Q38    |             2224.59 |
| TPC-DS Q39a+b |             1307.31 |
| TPC-DS Q40    |              980.92 |
| TPC-DS Q41    |                6.78 |
| TPC-DS Q42    |              132.36 |
| TPC-DS Q43    |              309.21 |
| TPC-DS Q44    |              205.99 |
| TPC-DS Q45    |              156.56 |
| TPC-DS Q46    |              231.80 |
| TPC-DS Q47    |              985.87 |
| TPC-DS Q48    |              230.73 |
| TPC-DS Q49    |             1263.42 |
| TPC-DS Q50    |              611.57 |
| TPC-DS Q51    |             2099.36 |
| TPC-DS Q52    |               75.32 |
| TPC-DS Q53    |               91.36 |
| TPC-DS Q54    |              103.47 |
| TPC-DS Q55    |               96.21 |
| TPC-DS Q56    |              101.52 |
| TPC-DS Q57    |              153.13 |
| TPC-DS Q58    |             5506.27 |
| TPC-DS Q59    |              962.24 |
| TPC-DS Q60    |              117.83 |
| TPC-DS Q61    |              319.80 |
| TPC-DS Q62    |              332.45 |
| TPC-DS Q63    |               87.36 |
| TPC-DS Q64    |             4161.67 |
| TPC-DS Q65    |             1318.94 |
| TPC-DS Q66    |             2011.13 |
| TPC-DS Q67    |             4685.05 |
| TPC-DS Q68    |              532.34 |
| TPC-DS Q69    |               96.04 |
| TPC-DS Q70    |             2206.65 |
| TPC-DS Q71    |              218.54 |
| TPC-DS Q72    |             1231.54 |
| TPC-DS Q73    |               78.67 |
| TPC-DS Q74    |             1864.48 |
| TPC-DS Q75    |             6220.18 |
| TPC-DS Q76    |             1641.90 |
| TPC-DS Q77    |              779.15 |
| TPC-DS Q78    |            11897.88 |
| TPC-DS Q79    |              263.64 |
| TPC-DS Q80    |             7195.21 |
| TPC-DS Q81    |               93.16 |
| TPC-DS Q82    |              482.26 |
| TPC-DS Q83    |               43.09 |
| TPC-DS Q84    |               35.46 |
| TPC-DS Q85    |              912.64 |
| TPC-DS Q86    |              330.66 |
| TPC-DS Q87    |             3183.65 |
| TPC-DS Q88    |              592.07 |
| TPC-DS Q89    |              162.43 |
| TPC-DS Q90    |               94.13 |
| TPC-DS Q91    |               34.80 |
| TPC-DS Q92    |              182.45 |
| TPC-DS Q93    |             1995.47 |
| TPC-DS Q94    |            35202.01 |
| TPC-DS Q95    |           344738.96 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MonetDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |
* TPC-DS Q96
  * MonetDB-1-1-1-1-1: numRun 1: : java.sql.SQLException: Cannot bind column sys.store_sales.ss_sold_time_sk
* TPC-DS Q97
  * MonetDB-1-1-1-1-1: numRun 1: : java.sql.SQLException: Cannot bind column sys.store_sales.ss_sold_date_sk
* TPC-DS Q98
  * MonetDB-1-1-1-1-1: numRun 1: : java.sql.SQLException: Cannot bind column sys.store_sales.ss_item_sk
* TPC-DS Q99
  * MonetDB-1-1-1-1-1: numRun 1: : java.sql.SQLException: Cannot bind column sys.catalog_sales.cs_call_center_sk

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      2280.32 |      5.36 |          52.75 |                 53.46 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       462.46 |      1.11 |           0.01 |                  3.36 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |     11251.02 |    173.16 |         826.52 |                826.53 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        87.84 |      0.63 |           0.64 |                  0.67 |

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
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
