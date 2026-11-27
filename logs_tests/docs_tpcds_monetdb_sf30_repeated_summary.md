## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3502s 
* Code: 1795702762
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 3000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:643772
  * datadisk:76689
  * volume_size:2.9T
  * volume_used:75G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:642168
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:641737
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:639207
  * datadisk:75265
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1795702762

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795702762-9d94b448f-9xdpp: 0
* bexhoma-sut-monetdb-1-1795702762-6dd8db8d9d-5q6md: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (1 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              0 |         0 |             | None           |             0 | False         |               65.02 | True                |
| MonetDB-1-2 |                2 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              0 |         0 |             | None           |             0 | False         |               65.02 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        771 |            0.95 |           117837.71 |          13867.70 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        719 |            0.82 |           136575.06 |          14870.65 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        798 |            1.03 |           108551.75 |          13398.50 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        717 |            0.81 |           138212.18 |          14912.13 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        771 |            0.95 |           117837.71 |          13867.70 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        719 |            0.82 |           136575.06 |          14870.65 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        798 |            1.03 |           108551.75 |          13398.50 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        717 |            0.81 |           138212.18 |          14912.13 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-2-2 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-2-1-1-1 |   monetdb-1-2-2-1-1 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |             1341.55 |              457.58 |             1466.27 |              492.45 |
| TPC-DS Q2     |             3327.24 |             1795.05 |             4345.79 |             2037.65 |
| TPC-DS Q3     |             2372.47 |              173.34 |             2508.90 |              187.09 |
| TPC-DS Q4     |            26658.60 |            19834.84 |            28360.69 |            18496.05 |
| TPC-DS Q5     |            16215.78 |             2001.10 |            19088.98 |             2175.34 |
| TPC-DS Q6     |              673.90 |              367.80 |              622.67 |              307.93 |
| TPC-DS Q7     |             4054.13 |             1221.24 |             4985.37 |             1065.23 |
| TPC-DS Q8     |             3354.97 |              385.98 |             3589.07 |              441.56 |
| TPC-DS Q9     |             1165.48 |              637.42 |             1308.58 |              834.01 |
| TPC-DS Q10    |            17725.51 |              429.41 |            19037.93 |              541.14 |
| TPC-DS Q11    |             6800.44 |             8105.68 |             8608.68 |             6991.31 |
| TPC-DS Q12    |              226.26 |              165.82 |              265.34 |              146.97 |
| TPC-DS Q13    |              432.15 |              569.31 |              492.89 |              551.05 |
| TPC-DS Q14a+b |            33704.96 |            37053.90 |            35515.44 |            33793.78 |
| TPC-DS Q15    |              166.92 |              131.16 |              148.05 |              135.22 |
| TPC-DS Q16    |            47236.20 |            47699.86 |            48986.56 |            45405.35 |
| TPC-DS Q17    |             3849.59 |             4092.80 |             3647.47 |             3043.41 |
| TPC-DS Q18    |             1871.48 |             1940.15 |             2151.98 |             1929.26 |
| TPC-DS Q19    |              172.44 |              162.84 |              171.82 |              150.49 |
| TPC-DS Q20    |              117.20 |              116.97 |              295.35 |              201.11 |
| TPC-DS Q21    |             1959.42 |              173.33 |             2112.45 |              217.82 |
| TPC-DS Q22    |             1794.56 |             2690.07 |             1861.05 |             1771.92 |
| TPC-DS Q23a+b |            49866.66 |            57020.41 |            60009.82 |            60594.55 |
| TPC-DS Q24a+b |            16962.81 |            18471.33 |            17230.67 |            19046.27 |
| TPC-DS Q25    |             2333.17 |             2716.17 |             2704.10 |             2490.68 |
| TPC-DS Q26    |              176.77 |              188.45 |              198.33 |              248.19 |
| TPC-DS Q27    |             1378.83 |             1471.78 |             1368.34 |             1343.16 |
| TPC-DS Q28    |              735.71 |              718.39 |              731.72 |              682.62 |
| TPC-DS Q29    |             2604.81 |             2962.37 |             3015.00 |             2346.12 |
| TPC-DS Q30    |              109.19 |              124.83 |              130.78 |              168.30 |
| TPC-DS Q31    |             2155.48 |             2264.06 |             2330.90 |             2853.49 |
| TPC-DS Q32    |              139.96 |              292.83 |              128.76 |              190.71 |
| TPC-DS Q33    |              136.83 |              179.44 |              529.23 |              165.57 |
| TPC-DS Q34    |              316.06 |              187.14 |              458.31 |              118.44 |
| TPC-DS Q35    |              757.17 |              862.43 |              786.79 |              709.77 |
| TPC-DS Q36    |             1598.95 |             1532.74 |             1343.08 |             1707.02 |
| TPC-DS Q37    |             2719.54 |             2935.28 |             2643.71 |             2198.11 |
| TPC-DS Q38    |             2380.79 |             2590.87 |             3098.64 |             3325.73 |
| TPC-DS Q39a+b |             1384.50 |             1984.19 |             1510.90 |             1423.37 |
| TPC-DS Q40    |              421.32 |              626.37 |              452.23 |              600.99 |
| TPC-DS Q41    |                5.29 |                5.82 |                5.31 |                5.31 |
| TPC-DS Q42    |              121.65 |               93.93 |              107.77 |              114.41 |
| TPC-DS Q43    |              424.10 |              328.03 |              506.25 |              298.11 |
| TPC-DS Q44    |            12716.99 |             8041.71 |             8875.68 |             7020.22 |
| TPC-DS Q45    |              223.55 |              140.39 |              138.93 |              152.83 |
| TPC-DS Q46    |              205.59 |              190.33 |              196.51 |              201.83 |
| TPC-DS Q47    |              885.26 |              841.54 |              875.81 |              930.27 |
| TPC-DS Q48    |              216.69 |              213.44 |              227.78 |              206.97 |
| TPC-DS Q49    |             4942.85 |             1622.64 |             4378.04 |             1574.21 |
| TPC-DS Q50    |              578.53 |              606.88 |              716.37 |              561.23 |
| TPC-DS Q51    |             2431.98 |             2924.44 |             2481.23 |             3123.50 |
| TPC-DS Q52    |               78.72 |              122.31 |              121.19 |              117.48 |
| TPC-DS Q53    |               97.03 |               93.47 |              101.66 |              104.05 |
| TPC-DS Q54    |              110.69 |               94.72 |               95.02 |               92.85 |
| TPC-DS Q55    |               78.47 |               85.60 |               72.80 |               60.95 |
| TPC-DS Q56    |              170.05 |              165.54 |              161.24 |              165.81 |
| TPC-DS Q57    |              146.48 |              141.21 |              133.72 |              134.95 |
| TPC-DS Q58    |              565.49 |              570.51 |              541.22 |              547.10 |
| TPC-DS Q59    |             1131.95 |             1822.94 |             1104.47 |             1622.14 |
| TPC-DS Q60    |              157.22 |              194.21 |              309.44 |              180.55 |
| TPC-DS Q61    |              172.42 |              167.21 |              360.76 |              161.85 |
| TPC-DS Q62    |              428.73 |              438.94 |              488.07 |              398.00 |
| TPC-DS Q63    |               97.05 |              108.67 |              129.82 |              103.59 |
| TPC-DS Q64    |             5527.41 |             5250.18 |             5100.00 |             4968.52 |
| TPC-DS Q65    |             1558.48 |             1098.69 |             1927.09 |             1793.00 |
| TPC-DS Q66    |             1053.24 |             1191.68 |             1138.66 |              786.34 |
| TPC-DS Q67    |             5646.54 |             6126.75 |             6303.18 |             6355.68 |
| TPC-DS Q68    |              226.16 |              220.89 |              216.29 |              231.24 |
| TPC-DS Q69    |              357.69 |              410.72 |              358.09 |              413.99 |
| TPC-DS Q70    |             1474.54 |             1941.71 |             1495.80 |             1439.32 |
| TPC-DS Q71    |              332.01 |              669.27 |              355.53 |              494.77 |
| TPC-DS Q72    |             2193.22 |             2989.87 |             2299.82 |             2384.52 |
| TPC-DS Q73    |              151.09 |               94.00 |              133.17 |               89.06 |
| TPC-DS Q74    |             1977.55 |             1976.69 |             1862.36 |             1960.16 |
| TPC-DS Q75    |             5732.53 |             5664.71 |             6692.33 |             5368.69 |
| TPC-DS Q76    |             6003.63 |             8145.53 |             7236.00 |             8947.07 |
| TPC-DS Q77    |             1147.99 |             1090.03 |             1231.93 |             1094.46 |
| TPC-DS Q78    |            14220.92 |            13961.64 |            15077.46 |            15397.31 |
| TPC-DS Q79    |              238.90 |              838.41 |              236.96 |              227.66 |
| TPC-DS Q80    |             8542.04 |             9035.39 |             8656.02 |            10295.32 |
| TPC-DS Q81    |              337.52 |              196.31 |              148.08 |              304.02 |
| TPC-DS Q82    |              582.28 |              449.08 |              434.97 |              528.29 |
| TPC-DS Q83    |              233.06 |              222.09 |              276.19 |              286.97 |
| TPC-DS Q84    |               49.75 |               45.02 |               50.74 |               51.42 |
| TPC-DS Q85    |              306.90 |              541.34 |              303.50 |              306.63 |
| TPC-DS Q86    |              306.00 |              334.28 |              561.39 |              350.29 |
| TPC-DS Q87    |             3824.84 |             3111.18 |             3239.08 |             3156.44 |
| TPC-DS Q88    |              631.59 |              414.88 |              639.76 |              513.38 |
| TPC-DS Q89    |              141.95 |              157.84 |              243.46 |              216.53 |
| TPC-DS Q90    |               76.05 |               99.97 |              159.59 |              213.05 |
| TPC-DS Q91    |               41.71 |               39.21 |               56.26 |               48.09 |
| TPC-DS Q92    |              141.15 |              137.72 |              146.34 |              140.02 |
| TPC-DS Q93    |             2074.16 |             2472.96 |             2053.36 |             2104.73 |
| TPC-DS Q94    |            37779.85 |            41184.29 |            42187.57 |            42167.14 |
| TPC-DS Q95    |           344096.87 |           326893.35 |           339482.62 |           329777.05 |
| TPC-DS Q96    |              825.21 |              756.14 |              806.36 |              783.42 |
| TPC-DS Q97    |             4489.78 |             4528.22 |             4943.42 |             5092.56 |
| TPC-DS Q98    |              491.55 |              482.09 |              479.94 |              587.42 |
| TPC-DS Q99    |              606.72 |              417.05 |              395.45 |              411.05 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     14053.35 |    190.63 |         955.89 |               1023.98 |
| monetdb-1-1-2-1 |     12287.45 |    170.61 |         961.30 |               1023.99 |
| monetdb-1-2-1-1 |     10997.14 |    134.56 |        1001.81 |               1023.90 |
| monetdb-1-2-2-1 |     11750.81 |    173.82 |        1011.21 |               1023.97 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        32.40 |      0.19 |           0.40 |                  0.41 |
| monetdb-1-1-2-1 |        31.90 |      0.19 |           0.38 |                  0.39 |
| monetdb-1-2-1-1 |        33.52 |      0.35 |           0.38 |                  0.39 |
| monetdb-1-2-2-1 |        31.35 |      0.53 |           0.37 |                  0.37 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
