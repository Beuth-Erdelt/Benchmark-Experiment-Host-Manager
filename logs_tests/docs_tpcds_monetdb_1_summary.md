## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 2587s 
* Code: 1785198017
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type shared and size 2000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 1024Gi RAM. RAM limit is 1024Gi.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808966
  * volume_size:2.0T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:1024Gi
  * limits_memory:1024Gi
  * eval_parameters
    * code:1785198017

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1785198017-584964766c-ghvn9: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |   30 |     1680.00 |          19.00 |            1.00 |        611.00 |         1031.00 |              8 |           0 |             | None           |             0 | False         |               64.29 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |       1271 |            0.75 |           149185.98 |           8412.27 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |       1271 |            0.75 |           149185.98 |           8412.27 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              288.11 |
| TPC-DS Q2     |             1979.46 |
| TPC-DS Q3     |              711.46 |
| TPC-DS Q4     |            15593.91 |
| TPC-DS Q5     |             1686.43 |
| TPC-DS Q6     |              517.96 |
| TPC-DS Q7     |              352.82 |
| TPC-DS Q8     |              294.70 |
| TPC-DS Q9     |              813.54 |
| TPC-DS Q10    |              155.84 |
| TPC-DS Q11    |             6191.11 |
| TPC-DS Q12    |              151.86 |
| TPC-DS Q13    |              506.86 |
| TPC-DS Q14a+b |            29041.90 |
| TPC-DS Q15    |              183.92 |
| TPC-DS Q16    |            42886.51 |
| TPC-DS Q17    |             2144.94 |
| TPC-DS Q18    |              919.24 |
| TPC-DS Q19    |              166.74 |
| TPC-DS Q20    |              130.16 |
| TPC-DS Q21    |              141.98 |
| TPC-DS Q22    |             1120.45 |
| TPC-DS Q23a+b |            49711.06 |
| TPC-DS Q24a+b |            25162.45 |
| TPC-DS Q25    |             2616.15 |
| TPC-DS Q26    |              244.52 |
| TPC-DS Q27    |             1278.48 |
| TPC-DS Q28    |              866.44 |
| TPC-DS Q29    |             1519.46 |
| TPC-DS Q30    |               87.40 |
| TPC-DS Q31    |             1926.08 |
| TPC-DS Q32    |              232.75 |
| TPC-DS Q33    |               99.64 |
| TPC-DS Q34    |              203.92 |
| TPC-DS Q35    |              976.48 |
| TPC-DS Q36    |             1143.53 |
| TPC-DS Q37    |              511.73 |
| TPC-DS Q38    |             2628.07 |
| TPC-DS Q39a+b |             1491.78 |
| TPC-DS Q40    |             1022.23 |
| TPC-DS Q41    |                8.27 |
| TPC-DS Q42    |              119.79 |
| TPC-DS Q43    |              288.39 |
| TPC-DS Q44    |              216.70 |
| TPC-DS Q45    |              147.13 |
| TPC-DS Q46    |              233.33 |
| TPC-DS Q47    |              835.90 |
| TPC-DS Q48    |              239.30 |
| TPC-DS Q49    |             1254.03 |
| TPC-DS Q50    |              561.76 |
| TPC-DS Q51    |             2483.18 |
| TPC-DS Q52    |              111.26 |
| TPC-DS Q53    |              101.63 |
| TPC-DS Q54    |              107.02 |
| TPC-DS Q55    |               85.25 |
| TPC-DS Q56    |              111.35 |
| TPC-DS Q57    |              135.91 |
| TPC-DS Q58    |             5326.37 |
| TPC-DS Q59    |             1141.37 |
| TPC-DS Q60    |              184.73 |
| TPC-DS Q61    |              365.66 |
| TPC-DS Q62    |              314.11 |
| TPC-DS Q63    |              113.65 |
| TPC-DS Q64    |             3907.05 |
| TPC-DS Q65    |             1034.50 |
| TPC-DS Q66    |             1770.44 |
| TPC-DS Q67    |             4552.48 |
| TPC-DS Q68    |              405.16 |
| TPC-DS Q69    |              315.45 |
| TPC-DS Q70    |             2349.17 |
| TPC-DS Q71    |              191.91 |
| TPC-DS Q72    |             1143.62 |
| TPC-DS Q73    |               83.45 |
| TPC-DS Q74    |             1749.93 |
| TPC-DS Q75    |             5312.18 |
| TPC-DS Q76    |             1340.61 |
| TPC-DS Q77    |              781.62 |
| TPC-DS Q78    |            12347.74 |
| TPC-DS Q79    |              234.85 |
| TPC-DS Q80    |             7332.41 |
| TPC-DS Q81    |              143.10 |
| TPC-DS Q82    |             1484.97 |
| TPC-DS Q83    |              261.03 |
| TPC-DS Q84    |               36.93 |
| TPC-DS Q85    |              882.09 |
| TPC-DS Q86    |              411.31 |
| TPC-DS Q87    |             2703.99 |
| TPC-DS Q88    |              565.03 |
| TPC-DS Q89    |              145.29 |
| TPC-DS Q90    |               98.36 |
| TPC-DS Q91    |               52.83 |
| TPC-DS Q92    |              194.85 |
| TPC-DS Q93    |             1930.47 |
| TPC-DS Q94    |            34490.63 |
| TPC-DS Q95    |           928120.49 |
| TPC-DS Q96    |             9390.99 |
| TPC-DS Q97    |             1187.65 |
| TPC-DS Q98    |              717.79 |
| TPC-DS Q99    |             1856.50 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      2853.66 |      7.28 |          50.31 |                 51.03 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         1.27 |      0.00 |           0.01 |                  0.01 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       441.11 |      1.09 |           0.03 |                  9.94 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |     41885.59 |    210.86 |         998.57 |               1024.00 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        25.16 |      0.40 |           0.38 |                  0.38 |

### Tests
* TEST passed: No SUT container restarts
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
