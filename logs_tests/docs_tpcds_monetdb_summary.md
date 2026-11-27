## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 682s 
* Code: 1795697129
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:649072
  * datadisk:12124
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795697129

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795697129-6648d55c88-vc2k8: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      396.00 |           2.00 |            1.00 |        324.00 |           58.00 |              8 |         0 |             | None           |             0 | False         |               27.27 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         41 |            0.09 |           123928.75 |          26078.05 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         41 |            0.09 |           123928.75 |          26078.05 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               38.54 |
| TPC-DS Q2     |              294.23 |
| TPC-DS Q3     |               47.11 |
| TPC-DS Q4     |             1488.11 |
| TPC-DS Q5     |              143.63 |
| TPC-DS Q6     |               54.51 |
| TPC-DS Q7     |               56.91 |
| TPC-DS Q8     |               40.30 |
| TPC-DS Q9     |              107.29 |
| TPC-DS Q10    |               29.21 |
| TPC-DS Q11    |              528.91 |
| TPC-DS Q12    |               35.93 |
| TPC-DS Q13    |              122.93 |
| TPC-DS Q14a+b |             2552.39 |
| TPC-DS Q15    |               27.06 |
| TPC-DS Q16    |              124.98 |
| TPC-DS Q17    |              196.75 |
| TPC-DS Q18    |              100.22 |
| TPC-DS Q19    |               55.59 |
| TPC-DS Q20    |               64.63 |
| TPC-DS Q21    |              174.46 |
| TPC-DS Q22    |             1152.87 |
| TPC-DS Q23a+b |             1857.30 |
| TPC-DS Q24a+b |              339.46 |
| TPC-DS Q25    |              184.71 |
| TPC-DS Q26    |               29.99 |
| TPC-DS Q27    |              303.52 |
| TPC-DS Q28    |              186.15 |
| TPC-DS Q29    |              363.80 |
| TPC-DS Q30    |               21.56 |
| TPC-DS Q31    |              252.35 |
| TPC-DS Q32    |               25.70 |
| TPC-DS Q33    |               28.09 |
| TPC-DS Q34    |               38.14 |
| TPC-DS Q35    |               78.54 |
| TPC-DS Q36    |              140.84 |
| TPC-DS Q37    |              121.46 |
| TPC-DS Q38    |              217.34 |
| TPC-DS Q39a+b |             1008.98 |
| TPC-DS Q40    |               87.37 |
| TPC-DS Q41    |                9.81 |
| TPC-DS Q42    |               88.43 |
| TPC-DS Q43    |              114.73 |
| TPC-DS Q44    |              163.93 |
| TPC-DS Q45    |               16.18 |
| TPC-DS Q46    |               57.22 |
| TPC-DS Q47    |              193.59 |
| TPC-DS Q48    |               49.49 |
| TPC-DS Q49    |              121.77 |
| TPC-DS Q50    |              132.44 |
| TPC-DS Q51    |              437.61 |
| TPC-DS Q52    |               28.63 |
| TPC-DS Q53    |               32.74 |
| TPC-DS Q54    |               28.50 |
| TPC-DS Q55    |               33.13 |
| TPC-DS Q56    |               36.96 |
| TPC-DS Q57    |               72.26 |
| TPC-DS Q58    |               64.58 |
| TPC-DS Q59    |              125.64 |
| TPC-DS Q60    |               30.36 |
| TPC-DS Q61    |               49.74 |
| TPC-DS Q62    |               26.94 |
| TPC-DS Q63    |               32.71 |
| TPC-DS Q64    |              495.50 |
| TPC-DS Q65    |              114.16 |
| TPC-DS Q66    |               36.65 |
| TPC-DS Q67    |              429.70 |
| TPC-DS Q68    |               64.42 |
| TPC-DS Q69    |               23.43 |
| TPC-DS Q70    |               76.22 |
| TPC-DS Q71    |               39.45 |
| TPC-DS Q72    |              194.67 |
| TPC-DS Q73    |               36.96 |
| TPC-DS Q74    |              178.01 |
| TPC-DS Q75    |              458.79 |
| TPC-DS Q76    |               53.30 |
| TPC-DS Q77    |               92.70 |
| TPC-DS Q78    |              804.05 |
| TPC-DS Q79    |               59.96 |
| TPC-DS Q80    |              537.45 |
| TPC-DS Q81    |               29.70 |
| TPC-DS Q82    |              143.43 |
| TPC-DS Q83    |               15.03 |
| TPC-DS Q84    |               41.00 |
| TPC-DS Q85    |               35.66 |
| TPC-DS Q86    |               34.51 |
| TPC-DS Q87    |              198.40 |
| TPC-DS Q88    |              107.51 |
| TPC-DS Q89    |               45.08 |
| TPC-DS Q90    |                8.86 |
| TPC-DS Q91    |               13.91 |
| TPC-DS Q92    |               13.12 |
| TPC-DS Q93    |              117.46 |
| TPC-DS Q94    |               28.82 |
| TPC-DS Q95    |              450.16 |
| TPC-DS Q96    |               12.63 |
| TPC-DS Q97    |              228.94 |
| TPC-DS Q98    |               46.55 |
| TPC-DS Q99    |               41.88 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
