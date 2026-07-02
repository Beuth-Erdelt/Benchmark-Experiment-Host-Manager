## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1462s 
* Code: 1782972290
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:644431
  * volume_size:50G
  * volume_used:3.3G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782972290
* MonetDB-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:644436
  * volume_size:50G
  * volume_used:3.4G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782972290

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1782972290-dfddd8cd4-xh2p5: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    1 |      616.00 |          14.00 |            0.00 |        139.00 |          455.00 |              8 |           0 |             | None           |             0 | False         |                5.84 |
| MonetDB-1-2 |                2 |    1 |      616.00 |          14.00 |            0.00 |        139.00 |          455.00 |              8 |           0 |             | None           |             0 | False         |                5.84 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               89 |         27 |            0.09 |            41357.10 |          11866.67 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-2-1-1-1 | MonetDB-1       | MonetDB-1-2-1 | MonetDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               89 |        130 |            0.11 |            32640.29 |           2464.62 |          -1 | MonetDB-1-2-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               89 |         27 |            0.09 |            41357.10 |          11866.67 |          -1 |
| MonetDB-1-2-1 | MonetDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               89 |        130 |            0.11 |            32640.29 |           2464.62 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |   MonetDB-1-2-1-1-1 |
|:--------------|--------------------:|--------------------:|
| TPC-DS Q1     |               61.72 |              411.04 |
| TPC-DS Q2     |              193.31 |              362.55 |
| TPC-DS Q3     |               70.91 |              875.10 |
| TPC-DS Q5     |              125.26 |             1233.75 |
| TPC-DS Q6     |               70.32 |              266.71 |
| TPC-DS Q7     |               71.89 |             1440.93 |
| TPC-DS Q8     |               56.04 |              129.55 |
| TPC-DS Q9     |              118.09 |              304.44 |
| TPC-DS Q10    |              111.16 |             5993.42 |
| TPC-DS Q12    |               34.18 |               99.85 |
| TPC-DS Q13    |               90.96 |              317.67 |
| TPC-DS Q14a+b |             1980.10 |               72.74 |
| TPC-DS Q15    |               32.69 |               18.39 |
| TPC-DS Q16    |               70.92 |              884.50 |
| TPC-DS Q17    |              155.09 |              182.64 |
| TPC-DS Q18    |              108.92 |              107.99 |
| TPC-DS Q19    |               65.43 |              104.65 |
| TPC-DS Q20    |               34.48 |               19.32 |
| TPC-DS Q21    |              206.71 |             2650.70 |
| TPC-DS Q22    |              804.18 |              213.37 |
| TPC-DS Q24a+b |              486.38 |              731.78 |
| TPC-DS Q25    |              201.82 |               78.03 |
| TPC-DS Q26    |               33.77 |               30.23 |
| TPC-DS Q27    |              105.73 |               45.01 |
| TPC-DS Q28    |               93.53 |               63.78 |
| TPC-DS Q29    |              144.95 |               75.90 |
| TPC-DS Q30    |               38.39 |              134.76 |
| TPC-DS Q31    |              162.19 |              120.82 |
| TPC-DS Q32    |               27.37 |               20.65 |
| TPC-DS Q33    |               55.30 |               55.60 |
| TPC-DS Q34    |               50.54 |               91.15 |
| TPC-DS Q35    |              133.60 |               14.23 |
| TPC-DS Q36    |              101.31 |               38.17 |
| TPC-DS Q37    |              120.27 |              128.80 |
| TPC-DS Q38    |              179.39 |               11.24 |
| TPC-DS Q39a+b |             1456.43 |               17.68 |
| TPC-DS Q41    |               10.05 |              180.28 |
| TPC-DS Q42    |               83.58 |               64.59 |
| TPC-DS Q43    |               72.14 |              193.59 |
| TPC-DS Q44    |               51.40 |               57.88 |
| TPC-DS Q45    |               20.54 |              267.38 |
| TPC-DS Q46    |               61.24 |              167.06 |
| TPC-DS Q47    |              285.20 |              110.48 |
| TPC-DS Q48    |               66.09 |              165.84 |
| TPC-DS Q49    |              178.04 |             3013.84 |
| TPC-DS Q50    |              158.10 |              280.64 |
| TPC-DS Q51    |              470.65 |               29.50 |
| TPC-DS Q52    |               85.81 |               28.93 |
| TPC-DS Q53    |               42.30 |               41.56 |
| TPC-DS Q55    |               26.09 |               24.77 |
| TPC-DS Q56    |               37.92 |               73.15 |
| TPC-DS Q57    |              126.25 |               79.86 |
| TPC-DS Q58    |               51.04 |              171.94 |
| TPC-DS Q59    |               82.10 |               74.65 |
| TPC-DS Q60    |               27.92 |               29.91 |
| TPC-DS Q61    |               48.40 |              122.58 |
| TPC-DS Q62    |               43.19 |              140.32 |
| TPC-DS Q63    |               34.20 |               37.36 |
| TPC-DS Q65    |              121.44 |               59.70 |
| TPC-DS Q66    |              173.55 |              273.57 |
| TPC-DS Q67    |              352.06 |               19.14 |
| TPC-DS Q68    |               64.77 |               68.25 |
| TPC-DS Q69    |               49.06 |             6255.18 |
| TPC-DS Q70    |              104.45 |             3526.95 |
| TPC-DS Q71    |               39.67 |              113.46 |
| TPC-DS Q72    |              303.75 |             1291.05 |
| TPC-DS Q73    |               38.46 |              142.03 |
| TPC-DS Q74    |              176.11 |               44.76 |
| TPC-DS Q75    |              440.99 |              164.52 |
| TPC-DS Q76    |               81.14 |              112.16 |
| TPC-DS Q77    |               86.19 |               71.27 |
| TPC-DS Q79    |               68.13 |               58.71 |
| TPC-DS Q81    |               42.39 |              197.05 |
| TPC-DS Q82    |              136.51 |              127.14 |
| TPC-DS Q83    |               15.13 |               12.12 |
| TPC-DS Q84    |               23.99 |               58.90 |
| TPC-DS Q85    |              254.15 |              283.71 |
| TPC-DS Q86    |               50.98 |               15.49 |
| TPC-DS Q87    |              279.33 |               10.84 |
| TPC-DS Q88    |               85.41 |              139.69 |
| TPC-DS Q89    |               55.80 |               58.68 |
| TPC-DS Q91    |               43.02 |              115.97 |
| TPC-DS Q92    |               16.51 |               15.46 |
| TPC-DS Q94    |               46.03 |               48.51 |
| TPC-DS Q95    |              257.39 |              356.97 |
| TPC-DS Q96    |               20.51 |               14.84 |
| TPC-DS Q97    |              216.50 |               22.63 |
| TPC-DS Q98    |               63.59 |               44.63 |
| TPC-DS Q99    |               93.82 |               44.14 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MonetDB-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        1.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         1.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q4
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q11
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q23a+b
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q40
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q54
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q64
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q78
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q80
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded
* TPC-DS Q90
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: division by zero.
* TPC-DS Q93
  * MonetDB-1-2-1-1-1: numRun 1: : java.sql.SQLException: GDK reported error: GDKextendf: could not extend file: Disk quota exceeded

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MonetDB-1-2-1-1-1 |        0.00 |        0.00 |        1.00 |        0.00 |        1.00 |        1.00 |        1.00 |        0.00 |        1.00 |         1.00 |         0.00 |         1.00 |         1.00 |            1.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |            0.00 |            0.00 |         0.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         0.00 |         1.00 |         0.00 |         1.00 |         1.00 |            1.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         0.00 |         1.00 |         0.00 |         1.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         0.00 |         0.00 |         1.00 |         1.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         0.00 |         1.00 |         0.00 |         1.00 |         0.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
