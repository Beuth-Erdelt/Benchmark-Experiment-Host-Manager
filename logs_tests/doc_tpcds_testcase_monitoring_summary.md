## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 755s 
* Code: 1782053765
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
  * disk:224889
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782053765

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    3 |      872.00 |           1.00 |            1.00 |        386.00 |          478.00 |              8 |           0 |             | None           |             0 | False         |               12.39 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         52 |            0.16 |            70009.58 |          20561.54 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         52 |            0.16 |            70009.58 |          20561.54 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               75.62 |
| TPC-DS Q2     |              240.46 |
| TPC-DS Q3     |               74.20 |
| TPC-DS Q4     |             2103.36 |
| TPC-DS Q5     |              202.52 |
| TPC-DS Q6     |               72.99 |
| TPC-DS Q7     |              112.57 |
| TPC-DS Q8     |               54.33 |
| TPC-DS Q9     |              201.19 |
| TPC-DS Q10    |               80.14 |
| TPC-DS Q11    |              924.31 |
| TPC-DS Q12    |               41.53 |
| TPC-DS Q13    |              131.92 |
| TPC-DS Q14a+b |             4542.14 |
| TPC-DS Q15    |               44.33 |
| TPC-DS Q16    |              224.58 |
| TPC-DS Q17    |              392.00 |
| TPC-DS Q18    |              160.38 |
| TPC-DS Q19    |              110.63 |
| TPC-DS Q20    |               55.27 |
| TPC-DS Q21    |              139.88 |
| TPC-DS Q22    |             1689.24 |
| TPC-DS Q23a+b |             4534.19 |
| TPC-DS Q24a+b |              407.95 |
| TPC-DS Q25    |              199.94 |
| TPC-DS Q26    |               56.72 |
| TPC-DS Q27    |              257.26 |
| TPC-DS Q28    |              189.40 |
| TPC-DS Q29    |              306.08 |
| TPC-DS Q30    |               49.86 |
| TPC-DS Q31    |              268.94 |
| TPC-DS Q32    |               33.00 |
| TPC-DS Q33    |               45.06 |
| TPC-DS Q34    |               59.08 |
| TPC-DS Q35    |              153.23 |
| TPC-DS Q36    |              255.98 |
| TPC-DS Q37    |               82.12 |
| TPC-DS Q38    |              354.22 |
| TPC-DS Q39a+b |             2270.67 |
| TPC-DS Q40    |              126.82 |
| TPC-DS Q41    |                7.73 |
| TPC-DS Q42    |               44.18 |
| TPC-DS Q43    |              244.40 |
| TPC-DS Q44    |               65.58 |
| TPC-DS Q45    |               26.84 |
| TPC-DS Q46    |               76.84 |
| TPC-DS Q47    |              303.18 |
| TPC-DS Q48    |               79.03 |
| TPC-DS Q49    |              182.21 |
| TPC-DS Q50    |              226.13 |
| TPC-DS Q51    |              792.46 |
| TPC-DS Q52    |               47.91 |
| TPC-DS Q53    |               51.70 |
| TPC-DS Q54    |               54.71 |
| TPC-DS Q55    |               39.38 |
| TPC-DS Q56    |               44.08 |
| TPC-DS Q57    |              161.88 |
| TPC-DS Q58    |              136.00 |
| TPC-DS Q59    |              259.07 |
| TPC-DS Q60    |               67.12 |
| TPC-DS Q61    |              117.25 |
| TPC-DS Q62    |               71.64 |
| TPC-DS Q63    |               83.25 |
| TPC-DS Q64    |             1022.54 |
| TPC-DS Q65    |              342.85 |
| TPC-DS Q66    |              370.36 |
| TPC-DS Q67    |              991.22 |
| TPC-DS Q68    |              162.76 |
| TPC-DS Q69    |               78.84 |
| TPC-DS Q70    |              304.78 |
| TPC-DS Q71    |              106.16 |
| TPC-DS Q72    |              365.65 |
| TPC-DS Q73    |               65.74 |
| TPC-DS Q74    |              318.86 |
| TPC-DS Q75    |             1027.50 |
| TPC-DS Q76    |              131.57 |
| TPC-DS Q77    |              171.34 |
| TPC-DS Q78    |             1957.76 |
| TPC-DS Q79    |              129.33 |
| TPC-DS Q80    |             1240.21 |
| TPC-DS Q81    |               69.58 |
| TPC-DS Q82    |              120.63 |
| TPC-DS Q83    |               24.47 |
| TPC-DS Q84    |               28.37 |
| TPC-DS Q85    |              266.70 |
| TPC-DS Q86    |               71.90 |
| TPC-DS Q87    |              516.06 |
| TPC-DS Q88    |              160.23 |
| TPC-DS Q89    |              122.50 |
| TPC-DS Q90    |               23.83 |
| TPC-DS Q91    |               43.37 |
| TPC-DS Q92    |               30.18 |
| TPC-DS Q93    |              292.55 |
| TPC-DS Q94    |              101.63 |
| TPC-DS Q95    |              735.84 |
| TPC-DS Q96    |               41.39 |
| TPC-DS Q97    |              554.04 |
| TPC-DS Q98    |              124.57 |
| TPC-DS Q99    |              114.20 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       930.62 |      3.17 |           4.89 |                  6.41 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.06 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        36.82 |      0.11 |           0.01 |                  2.65 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       153.00 |      5.83 |          12.15 |                 13.68 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        16.32 |      0.42 |           0.32 |                  0.32 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
