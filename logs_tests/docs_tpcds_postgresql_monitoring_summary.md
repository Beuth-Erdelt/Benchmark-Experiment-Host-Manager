## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1106s 
* Code: 1782969611
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 45Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:654135
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782969611

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1782969611-6dfcbdd4d-7bv6w: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    3 |      966.00 |           7.00 |            1.00 |        299.00 |          651.00 |              8 |           0 |             | None           |             0 | False         |               11.18 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         58 |            0.22 |            51182.36 |          18434.48 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         58 |            0.22 |            51182.36 |          18434.48 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               86.56 |
| TPC-DS Q2     |              408.70 |
| TPC-DS Q3     |               98.14 |
| TPC-DS Q4     |             2508.60 |
| TPC-DS Q5     |              271.87 |
| TPC-DS Q6     |              155.05 |
| TPC-DS Q7     |              172.58 |
| TPC-DS Q8     |               72.92 |
| TPC-DS Q9     |              340.07 |
| TPC-DS Q10    |              113.55 |
| TPC-DS Q11    |             1245.74 |
| TPC-DS Q12    |               51.11 |
| TPC-DS Q13    |              219.56 |
| TPC-DS Q14a+b |             6028.01 |
| TPC-DS Q15    |               61.35 |
| TPC-DS Q16    |              277.80 |
| TPC-DS Q17    |              376.44 |
| TPC-DS Q18    |              211.52 |
| TPC-DS Q19    |              180.90 |
| TPC-DS Q20    |               81.29 |
| TPC-DS Q21    |              186.28 |
| TPC-DS Q22    |             2191.72 |
| TPC-DS Q23a+b |             6037.71 |
| TPC-DS Q24a+b |              602.93 |
| TPC-DS Q25    |              397.19 |
| TPC-DS Q26    |              100.18 |
| TPC-DS Q27    |              278.09 |
| TPC-DS Q28    |              266.67 |
| TPC-DS Q29    |              486.53 |
| TPC-DS Q30    |               49.53 |
| TPC-DS Q31    |              447.62 |
| TPC-DS Q32    |               77.62 |
| TPC-DS Q33    |               93.55 |
| TPC-DS Q34    |              120.39 |
| TPC-DS Q35    |              246.50 |
| TPC-DS Q36    |              283.06 |
| TPC-DS Q37    |              165.29 |
| TPC-DS Q38    |              481.28 |
| TPC-DS Q39a+b |             3188.68 |
| TPC-DS Q40    |              205.65 |
| TPC-DS Q41    |               10.73 |
| TPC-DS Q42    |               84.78 |
| TPC-DS Q43    |              201.73 |
| TPC-DS Q44    |              159.42 |
| TPC-DS Q45    |               40.10 |
| TPC-DS Q46    |              163.38 |
| TPC-DS Q47    |              621.12 |
| TPC-DS Q48    |              160.76 |
| TPC-DS Q49    |              411.68 |
| TPC-DS Q50    |              371.79 |
| TPC-DS Q51    |             1132.97 |
| TPC-DS Q52    |               84.98 |
| TPC-DS Q53    |               93.31 |
| TPC-DS Q54    |              106.25 |
| TPC-DS Q55    |               76.81 |
| TPC-DS Q56    |               81.48 |
| TPC-DS Q57    |              269.08 |
| TPC-DS Q58    |              191.56 |
| TPC-DS Q59    |              390.63 |
| TPC-DS Q60    |               90.14 |
| TPC-DS Q61    |              157.88 |
| TPC-DS Q62    |               89.51 |
| TPC-DS Q63    |               88.93 |
| TPC-DS Q64    |              931.17 |
| TPC-DS Q65    |              367.14 |
| TPC-DS Q66    |              361.90 |
| TPC-DS Q67    |              949.10 |
| TPC-DS Q68    |              189.42 |
| TPC-DS Q69    |              141.87 |
| TPC-DS Q70    |              241.12 |
| TPC-DS Q71    |              127.61 |
| TPC-DS Q72    |              420.07 |
| TPC-DS Q73    |               83.64 |
| TPC-DS Q74    |              442.32 |
| TPC-DS Q75    |             1085.68 |
| TPC-DS Q76    |              155.95 |
| TPC-DS Q77    |              196.07 |
| TPC-DS Q78    |             1975.21 |
| TPC-DS Q79    |              162.71 |
| TPC-DS Q80    |             1116.84 |
| TPC-DS Q81    |               86.20 |
| TPC-DS Q82    |              156.12 |
| TPC-DS Q83    |               25.19 |
| TPC-DS Q84    |               27.42 |
| TPC-DS Q85    |              309.50 |
| TPC-DS Q86    |              112.41 |
| TPC-DS Q87    |              674.65 |
| TPC-DS Q88    |              182.59 |
| TPC-DS Q89    |              133.23 |
| TPC-DS Q90    |               28.19 |
| TPC-DS Q91    |               40.63 |
| TPC-DS Q92    |               31.58 |
| TPC-DS Q93    |              367.57 |
| TPC-DS Q94    |              127.15 |
| TPC-DS Q95    |              989.74 |
| TPC-DS Q96    |               37.44 |
| TPC-DS Q97    |              525.77 |
| TPC-DS Q98    |              152.25 |
| TPC-DS Q99    |              148.06 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       617.08 |      3.18 |           5.07 |                  6.60 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        37.53 |      0.18 |           0.01 |                  2.65 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       199.62 |      5.77 |          11.56 |                 13.09 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        15.75 |      0.09 |           0.31 |                  0.32 |

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
