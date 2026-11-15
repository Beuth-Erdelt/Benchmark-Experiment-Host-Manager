## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 725s 
* Code: 1794670484
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1181103
  * datadisk:12129
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794670484

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794670484-7667447b4d-rzpb9: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      439.00 |           2.00 |            1.00 |        367.00 |           61.00 |              8 |         0 |             | None           |             0 | False         |               24.60 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         25 |            0.09 |           124434.42 |          42768.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         25 |            0.09 |           124434.42 |          42768.00 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               37.61 |
| TPC-DS Q2     |              136.78 |
| TPC-DS Q3     |               34.20 |
| TPC-DS Q4     |             1148.98 |
| TPC-DS Q5     |              125.32 |
| TPC-DS Q6     |               49.93 |
| TPC-DS Q7     |               52.21 |
| TPC-DS Q8     |               35.46 |
| TPC-DS Q9     |              101.16 |
| TPC-DS Q10    |               25.78 |
| TPC-DS Q11    |              523.77 |
| TPC-DS Q12    |               24.47 |
| TPC-DS Q13    |               73.80 |
| TPC-DS Q14a+b |             2635.56 |
| TPC-DS Q15    |               20.24 |
| TPC-DS Q16    |              116.58 |
| TPC-DS Q17    |              180.64 |
| TPC-DS Q18    |              108.55 |
| TPC-DS Q19    |               57.60 |
| TPC-DS Q20    |               29.93 |
| TPC-DS Q21    |              132.29 |
| TPC-DS Q22    |             1130.18 |
| TPC-DS Q23a+b |             2577.24 |
| TPC-DS Q24a+b |              297.26 |
| TPC-DS Q25    |              194.84 |
| TPC-DS Q26    |               29.70 |
| TPC-DS Q27    |              160.72 |
| TPC-DS Q28    |               93.53 |
| TPC-DS Q29    |              191.20 |
| TPC-DS Q30    |               20.43 |
| TPC-DS Q31    |              282.19 |
| TPC-DS Q32    |               21.77 |
| TPC-DS Q33    |               35.30 |
| TPC-DS Q34    |               49.97 |
| TPC-DS Q35    |              146.36 |
| TPC-DS Q36    |              304.90 |
| TPC-DS Q37    |              100.68 |
| TPC-DS Q38    |              334.01 |
| TPC-DS Q39a+b |             1273.27 |
| TPC-DS Q40    |               78.88 |
| TPC-DS Q41    |                6.24 |
| TPC-DS Q42    |               35.37 |
| TPC-DS Q43    |               67.32 |
| TPC-DS Q44    |               52.35 |
| TPC-DS Q45    |               15.14 |
| TPC-DS Q46    |               60.27 |
| TPC-DS Q47    |              194.24 |
| TPC-DS Q48    |               46.14 |
| TPC-DS Q49    |              122.59 |
| TPC-DS Q50    |              143.70 |
| TPC-DS Q51    |              439.98 |
| TPC-DS Q52    |               38.75 |
| TPC-DS Q53    |               35.58 |
| TPC-DS Q54    |               27.44 |
| TPC-DS Q55    |               17.49 |
| TPC-DS Q56    |               74.77 |
| TPC-DS Q57    |              108.10 |
| TPC-DS Q58    |              132.58 |
| TPC-DS Q59    |              198.70 |
| TPC-DS Q60    |               42.88 |
| TPC-DS Q61    |               70.42 |
| TPC-DS Q62    |               33.17 |
| TPC-DS Q63    |               57.45 |
| TPC-DS Q64    |              754.42 |
| TPC-DS Q65    |              136.45 |
| TPC-DS Q66    |               40.32 |
| TPC-DS Q67    |              426.82 |
| TPC-DS Q68    |               75.63 |
| TPC-DS Q69    |               23.68 |
| TPC-DS Q70    |               73.13 |
| TPC-DS Q71    |               36.53 |
| TPC-DS Q72    |              197.88 |
| TPC-DS Q73    |               36.44 |
| TPC-DS Q74    |              179.51 |
| TPC-DS Q75    |              495.31 |
| TPC-DS Q76    |               61.60 |
| TPC-DS Q77    |               82.66 |
| TPC-DS Q78    |              784.36 |
| TPC-DS Q79    |               63.51 |
| TPC-DS Q80    |              553.74 |
| TPC-DS Q81    |               34.07 |
| TPC-DS Q82    |              190.27 |
| TPC-DS Q83    |               24.81 |
| TPC-DS Q84    |               74.16 |
| TPC-DS Q85    |               32.67 |
| TPC-DS Q86    |               26.40 |
| TPC-DS Q87    |              283.36 |
| TPC-DS Q88    |               86.13 |
| TPC-DS Q89    |               48.40 |
| TPC-DS Q90    |                9.88 |
| TPC-DS Q91    |               14.49 |
| TPC-DS Q92    |               15.00 |
| TPC-DS Q93    |              131.11 |
| TPC-DS Q94    |               33.53 |
| TPC-DS Q95    |              427.35 |
| TPC-DS Q96    |               15.13 |
| TPC-DS Q97    |              238.72 |
| TPC-DS Q98    |               48.24 |
| TPC-DS Q99    |               40.33 |

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
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
