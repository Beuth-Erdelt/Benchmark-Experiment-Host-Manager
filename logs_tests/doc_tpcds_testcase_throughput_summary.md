## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 619s 
* Code: 1782054644
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219588
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782054644
* MonetDB-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219591
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782054644
* MonetDB-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219591
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782054644

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    1 |      380.00 |           2.00 |            0.00 |        137.00 |          234.00 |              8 |           0 |             | None           |             0 | False         |                9.47 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |         25 |            0.08 |            48624.24 |          14256.00 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-1-2-1-1 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |         30 |            0.08 |            50508.79 |          11880.00 |          -1 | MonetDB-1-1-2-1-1 |
| MonetDB-1-1-2-1-2 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |         38 |            0.08 |            49841.20 |           9378.95 |          -1 | MonetDB-1-1-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |         25 |            0.08 |            48624.24 |          14256.00 |          -1 |
| MonetDB-1-1-2 | MonetDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |         38 |            0.08 |            50173.88 |          18757.89 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |   MonetDB-1-1-2-1-1 |   MonetDB-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               70.05 |               77.24 |               64.77 |
| TPC-DS Q2     |              100.90 |               92.64 |               92.64 |
| TPC-DS Q3     |               36.65 |               31.98 |               18.40 |
| TPC-DS Q4     |              631.54 |              601.81 |              570.89 |
| TPC-DS Q5     |               70.16 |               61.29 |               68.97 |
| TPC-DS Q6     |               54.76 |               51.86 |               49.45 |
| TPC-DS Q7     |               45.59 |               45.49 |               41.42 |
| TPC-DS Q8     |               26.67 |               25.42 |               25.93 |
| TPC-DS Q9     |               54.69 |               45.49 |               44.93 |
| TPC-DS Q10    |               42.65 |               38.84 |               38.04 |
| TPC-DS Q11    |              328.25 |              271.46 |              260.52 |
| TPC-DS Q12    |               30.32 |               17.04 |               18.15 |
| TPC-DS Q13    |               69.49 |               40.07 |               47.44 |
| TPC-DS Q14a+b |             2083.71 |             1531.06 |             1619.39 |
| TPC-DS Q15    |               39.57 |               22.86 |               21.99 |
| TPC-DS Q16    |               56.47 |               30.46 |               28.41 |
| TPC-DS Q17    |              125.89 |               91.48 |               89.04 |
| TPC-DS Q18    |               72.26 |               52.69 |               49.08 |
| TPC-DS Q19    |               60.94 |               37.97 |               35.84 |
| TPC-DS Q20    |               37.39 |               26.04 |               26.72 |
| TPC-DS Q21    |              168.31 |              135.80 |              114.71 |
| TPC-DS Q22    |              718.35 |              668.81 |              577.51 |
| TPC-DS Q23a+b |             1353.66 |              882.73 |             1020.44 |
| TPC-DS Q24a+b |              194.01 |              107.78 |              178.72 |
| TPC-DS Q25    |              139.47 |               97.61 |              117.97 |
| TPC-DS Q26    |               31.02 |               21.70 |               28.61 |
| TPC-DS Q27    |               72.48 |               58.39 |               77.36 |
| TPC-DS Q28    |               89.13 |               43.38 |               80.90 |
| TPC-DS Q29    |               98.13 |               82.58 |               91.73 |
| TPC-DS Q30    |               32.96 |               25.49 |               31.12 |
| TPC-DS Q31    |              143.48 |               87.56 |              127.51 |
| TPC-DS Q32    |               28.22 |               19.82 |               36.54 |
| TPC-DS Q33    |               32.15 |               21.82 |               29.59 |
| TPC-DS Q34    |               44.30 |               34.17 |               49.03 |
| TPC-DS Q35    |               99.54 |               95.43 |               78.13 |
| TPC-DS Q36    |               75.70 |               73.02 |               77.14 |
| TPC-DS Q37    |               52.94 |               97.15 |              117.69 |
| TPC-DS Q38    |              123.68 |              123.53 |              132.75 |
| TPC-DS Q39a+b |             1024.36 |             1134.53 |             1185.00 |
| TPC-DS Q40    |               63.22 |               65.72 |               66.87 |
| TPC-DS Q41    |                8.32 |                9.70 |                9.34 |
| TPC-DS Q42    |               23.43 |               31.48 |               32.17 |
| TPC-DS Q43    |              112.14 |              120.49 |              124.50 |
| TPC-DS Q44    |               60.41 |               67.65 |               69.19 |
| TPC-DS Q45    |               17.24 |               22.59 |               18.94 |
| TPC-DS Q46    |               41.11 |               51.27 |               51.86 |
| TPC-DS Q47    |              208.61 |              221.32 |              225.12 |
| TPC-DS Q48    |               42.10 |               52.13 |               54.72 |
| TPC-DS Q49    |              101.31 |              111.84 |               93.14 |
| TPC-DS Q50    |              127.47 |              129.23 |              130.78 |
| TPC-DS Q51    |              313.25 |              320.29 |              340.02 |
| TPC-DS Q52    |               61.55 |               38.67 |               33.95 |
| TPC-DS Q53    |               28.05 |               39.59 |               41.13 |
| TPC-DS Q54    |               26.77 |               35.48 |               37.61 |
| TPC-DS Q55    |               19.45 |               29.96 |               23.67 |
| TPC-DS Q56    |               27.70 |               55.29 |               36.19 |
| TPC-DS Q57    |              100.14 |              112.92 |              111.01 |
| TPC-DS Q58    |               57.81 |               50.90 |               62.87 |
| TPC-DS Q59    |              100.28 |              113.95 |              129.68 |
| TPC-DS Q60    |               25.98 |               33.52 |               43.36 |
| TPC-DS Q61    |               39.57 |               53.73 |               59.07 |
| TPC-DS Q62    |               39.73 |               45.50 |               42.62 |
| TPC-DS Q63    |               32.65 |               39.92 |               36.72 |
| TPC-DS Q64    |              276.68 |              289.69 |              301.84 |
| TPC-DS Q65    |              114.98 |              105.09 |              104.49 |
| TPC-DS Q66    |              125.03 |              131.20 |              143.28 |
| TPC-DS Q67    |              271.59 |              279.70 |              281.73 |
| TPC-DS Q68    |               34.71 |               59.11 |               66.92 |
| TPC-DS Q69    |               28.35 |               42.09 |               38.54 |
| TPC-DS Q70    |               64.57 |               79.41 |               76.89 |
| TPC-DS Q71    |               27.35 |               44.40 |               48.14 |
| TPC-DS Q72    |              196.52 |              262.88 |              256.73 |
| TPC-DS Q73    |               21.20 |               32.15 |               35.82 |
| TPC-DS Q74    |               96.43 |              114.38 |              121.47 |
| TPC-DS Q75    |              287.02 |              335.28 |              362.56 |
| TPC-DS Q76    |               51.22 |               51.95 |               51.62 |
| TPC-DS Q77    |               55.12 |               64.97 |               59.65 |
| TPC-DS Q78    |              650.84 |              546.93 |              557.37 |
| TPC-DS Q79    |               70.58 |               60.72 |               65.02 |
| TPC-DS Q80    |              412.65 |              384.02 |              386.06 |
| TPC-DS Q81    |               41.44 |               47.65 |               50.68 |
| TPC-DS Q82    |              102.53 |              117.78 |              115.99 |
| TPC-DS Q83    |               16.58 |               14.82 |               14.56 |
| TPC-DS Q84    |               32.74 |               25.79 |               31.83 |
| TPC-DS Q85    |              200.61 |              189.04 |              202.11 |
| TPC-DS Q86    |               37.75 |               38.32 |               40.67 |
| TPC-DS Q87    |              186.64 |              190.19 |              182.26 |
| TPC-DS Q88    |               64.10 |               64.54 |               65.14 |
| TPC-DS Q89    |               53.13 |               52.89 |               38.29 |
| TPC-DS Q90    |               19.35 |               22.31 |               21.40 |
| TPC-DS Q91    |               40.41 |               37.31 |               28.50 |
| TPC-DS Q92    |               17.06 |               18.28 |               14.81 |
| TPC-DS Q93    |               97.51 |              101.08 |               84.33 |
| TPC-DS Q94    |               39.88 |               26.39 |               27.81 |
| TPC-DS Q95    |              186.37 |              169.31 |              129.16 |
| TPC-DS Q96    |               26.99 |               22.97 |               17.10 |
| TPC-DS Q97    |              188.89 |              169.48 |              154.96 |
| TPC-DS Q98    |               66.50 |               53.69 |               48.75 |
| TPC-DS Q99    |               69.94 |               70.70 |               46.27 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MonetDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MonetDB-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
