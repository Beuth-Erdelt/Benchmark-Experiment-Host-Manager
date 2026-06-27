## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 739s 
* Code: 1782067395
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:247216
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782067395

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    3 |      854.00 |           1.00 |            1.00 |        375.00 |          471.00 |              8 |           0 |             | None           |             0 | False         |               12.65 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         58 |            0.16 |            71524.20 |          18434.48 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         58 |            0.16 |            71524.20 |          18434.48 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               85.28 |
| TPC-DS Q2     |              240.54 |
| TPC-DS Q3     |               49.83 |
| TPC-DS Q4     |             1900.02 |
| TPC-DS Q5     |              182.26 |
| TPC-DS Q6     |               76.98 |
| TPC-DS Q7     |               78.91 |
| TPC-DS Q8     |               37.30 |
| TPC-DS Q9     |              153.13 |
| TPC-DS Q10    |               63.95 |
| TPC-DS Q11    |              924.75 |
| TPC-DS Q12    |               39.20 |
| TPC-DS Q13    |              149.57 |
| TPC-DS Q14a+b |             8211.41 |
| TPC-DS Q15    |               64.70 |
| TPC-DS Q16    |              242.18 |
| TPC-DS Q17    |              351.47 |
| TPC-DS Q18    |              164.76 |
| TPC-DS Q19    |              107.81 |
| TPC-DS Q20    |               51.52 |
| TPC-DS Q21    |              140.59 |
| TPC-DS Q22    |             2142.98 |
| TPC-DS Q23a+b |             3577.64 |
| TPC-DS Q24a+b |              325.85 |
| TPC-DS Q25    |              212.43 |
| TPC-DS Q26    |               48.23 |
| TPC-DS Q27    |              178.75 |
| TPC-DS Q28    |              135.45 |
| TPC-DS Q29    |              201.98 |
| TPC-DS Q30    |               23.58 |
| TPC-DS Q31    |              327.26 |
| TPC-DS Q32    |               39.63 |
| TPC-DS Q33    |               48.61 |
| TPC-DS Q34    |               66.98 |
| TPC-DS Q35    |              194.14 |
| TPC-DS Q36    |              281.83 |
| TPC-DS Q37    |               62.67 |
| TPC-DS Q38    |              329.34 |
| TPC-DS Q39a+b |             2763.47 |
| TPC-DS Q40    |              155.25 |
| TPC-DS Q41    |                9.57 |
| TPC-DS Q42    |               70.34 |
| TPC-DS Q43    |              172.05 |
| TPC-DS Q44    |              131.21 |
| TPC-DS Q45    |               30.57 |
| TPC-DS Q46    |              121.86 |
| TPC-DS Q47    |              489.21 |
| TPC-DS Q48    |              112.75 |
| TPC-DS Q49    |              285.22 |
| TPC-DS Q50    |              305.51 |
| TPC-DS Q51    |             1043.73 |
| TPC-DS Q52    |               62.76 |
| TPC-DS Q53    |               58.56 |
| TPC-DS Q54    |               66.01 |
| TPC-DS Q55    |               48.83 |
| TPC-DS Q56    |               57.09 |
| TPC-DS Q57    |              175.96 |
| TPC-DS Q58    |              186.18 |
| TPC-DS Q59    |              278.75 |
| TPC-DS Q60    |               60.43 |
| TPC-DS Q61    |              119.25 |
| TPC-DS Q62    |               60.83 |
| TPC-DS Q63    |               56.42 |
| TPC-DS Q64    |              930.71 |
| TPC-DS Q65    |              321.53 |
| TPC-DS Q66    |              293.49 |
| TPC-DS Q67    |              853.66 |
| TPC-DS Q68    |              115.30 |
| TPC-DS Q69    |               89.29 |
| TPC-DS Q70    |              249.40 |
| TPC-DS Q71    |               85.23 |
| TPC-DS Q72    |              327.34 |
| TPC-DS Q73    |               51.38 |
| TPC-DS Q74    |              345.36 |
| TPC-DS Q75    |             1001.13 |
| TPC-DS Q76    |               96.87 |
| TPC-DS Q77    |              165.51 |
| TPC-DS Q78    |             2378.38 |
| TPC-DS Q79    |              119.04 |
| TPC-DS Q80    |             1163.60 |
| TPC-DS Q81    |               69.97 |
| TPC-DS Q82    |               86.09 |
| TPC-DS Q83    |               20.22 |
| TPC-DS Q84    |               23.32 |
| TPC-DS Q85    |              277.86 |
| TPC-DS Q86    |               69.18 |
| TPC-DS Q87    |              471.57 |
| TPC-DS Q88    |              161.67 |
| TPC-DS Q89    |               90.51 |
| TPC-DS Q90    |               22.85 |
| TPC-DS Q91    |               30.50 |
| TPC-DS Q92    |               26.11 |
| TPC-DS Q93    |              258.79 |
| TPC-DS Q94    |               83.38 |
| TPC-DS Q95    |              743.06 |
| TPC-DS Q96    |               29.35 |
| TPC-DS Q97    |              508.77 |
| TPC-DS Q98    |              104.50 |
| TPC-DS Q99    |               93.12 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1012.01 |      3.74 |           6.20 |                  7.72 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        36.40 |      0.13 |           0.01 |                  2.65 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       166.05 |      3.92 |          12.12 |                 13.65 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        18.68 |      0.48 |           0.32 |                  0.32 |

### Tests
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
