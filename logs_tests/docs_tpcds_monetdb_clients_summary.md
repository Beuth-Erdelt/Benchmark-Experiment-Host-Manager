## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 4740s 
* Code: 1795790763
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
  * System metrics are monitored by a cluster-wide installation for all components.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 3000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 1.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745318
  * datadisk:77057
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795790763
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745312
  * datadisk:76807
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795790763
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745312
  * datadisk:76807
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795790763

### Ingestion
* MonetDB-1: 81 of 81 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795790763-77f6bdcfc9-6zb68: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |     1478.00 |           3.00 |          568.00 |        429.00 |          473.00 |              8 |         0 |             | None           |             0 | False         |               73.07 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        679 |            0.56 |           191802.59 |          15746.69 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |       1026 |            0.83 |           130507.67 |          10421.05 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 30.00 |               99 |                  99 |       1235 |            0.92 |           117479.86 |           8657.49 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        679 |            0.56 |           191802.59 |          15746.69 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 30.00 |              198 |                 198 |       1235 |            0.87 |           123822.55 |          17314.98 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |              299.44 |              345.90 |              210.99 |
| TPC-DS Q2     |             1476.09 |             2354.92 |             2667.97 |
| TPC-DS Q3     |              112.89 |              266.89 |              270.66 |
| TPC-DS Q4     |            15363.74 |            19360.63 |            17297.78 |
| TPC-DS Q5     |             1450.66 |             1558.72 |             3286.88 |
| TPC-DS Q6     |              435.45 |              296.47 |              578.55 |
| TPC-DS Q7     |              189.71 |              728.99 |             1177.75 |
| TPC-DS Q8     |              437.90 |              332.89 |              333.91 |
| TPC-DS Q9     |              516.15 |              909.29 |              784.46 |
| TPC-DS Q10    |              187.52 |              575.92 |              575.81 |
| TPC-DS Q11    |             6747.88 |             6956.54 |             7352.16 |
| TPC-DS Q12    |              161.57 |              427.93 |              250.09 |
| TPC-DS Q13    |              289.26 |              543.74 |              294.24 |
| TPC-DS Q14a+b |            33123.04 |            37807.32 |            37640.69 |
| TPC-DS Q15    |              132.99 |              181.04 |              144.85 |
| TPC-DS Q16    |            43325.60 |            72269.48 |            40858.76 |
| TPC-DS Q17    |             1905.44 |             2132.38 |             6906.90 |
| TPC-DS Q18    |              932.04 |             1187.68 |             2592.51 |
| TPC-DS Q19    |              178.09 |              228.08 |             4553.23 |
| TPC-DS Q20    |              127.94 |              117.16 |             5134.03 |
| TPC-DS Q21    |              111.38 |              118.00 |            11370.26 |
| TPC-DS Q22    |             1095.88 |             1161.06 |             1729.29 |
| TPC-DS Q23a+b |            50097.56 |            52624.30 |            64847.53 |
| TPC-DS Q24a+b |            25717.23 |            26301.59 |            21825.10 |
| TPC-DS Q25    |             2373.71 |             3898.28 |             2569.52 |
| TPC-DS Q26    |              172.07 |              539.54 |              181.90 |
| TPC-DS Q27    |             1501.00 |             2972.15 |             1330.43 |
| TPC-DS Q28    |              534.04 |              713.31 |              882.62 |
| TPC-DS Q29    |             2178.36 |             2470.04 |             3804.41 |
| TPC-DS Q30    |               39.57 |               87.48 |               34.78 |
| TPC-DS Q31    |             1901.45 |             4010.94 |             1789.58 |
| TPC-DS Q32    |              192.00 |              185.70 |              173.20 |
| TPC-DS Q33    |              115.19 |              146.48 |              124.41 |
| TPC-DS Q34    |              100.47 |              150.17 |              161.28 |
| TPC-DS Q35    |              714.09 |              911.82 |              732.99 |
| TPC-DS Q36    |             1235.05 |             1820.63 |             1668.73 |
| TPC-DS Q37    |              427.47 |              467.76 |              453.08 |
| TPC-DS Q38    |             2580.45 |             2467.36 |             2429.21 |
| TPC-DS Q39a+b |             1222.65 |             1181.06 |             1346.41 |
| TPC-DS Q40    |             1010.99 |             5970.21 |             5917.49 |
| TPC-DS Q41    |                5.26 |                6.12 |                8.14 |
| TPC-DS Q42    |              117.27 |               82.26 |               75.74 |
| TPC-DS Q43    |              220.12 |              218.60 |              215.10 |
| TPC-DS Q44    |              203.48 |              233.71 |              217.10 |
| TPC-DS Q45    |              117.54 |              148.36 |              163.83 |
| TPC-DS Q46    |              204.08 |              214.31 |              217.21 |
| TPC-DS Q47    |              803.67 |              931.87 |              878.14 |
| TPC-DS Q48    |              215.37 |              253.33 |              243.96 |
| TPC-DS Q49    |             1170.93 |             1470.23 |             1701.01 |
| TPC-DS Q50    |              577.07 |              618.98 |             1190.60 |
| TPC-DS Q51    |             2344.82 |             3193.76 |             2531.75 |
| TPC-DS Q52    |               98.39 |               97.71 |              119.38 |
| TPC-DS Q53    |              101.07 |              105.06 |               96.33 |
| TPC-DS Q54    |               95.24 |               89.05 |               91.02 |
| TPC-DS Q55    |               85.05 |               78.38 |               69.00 |
| TPC-DS Q56    |              183.37 |              115.79 |              167.73 |
| TPC-DS Q57    |              151.85 |              166.26 |              155.59 |
| TPC-DS Q58    |              570.09 |              555.12 |              586.85 |
| TPC-DS Q59    |              944.19 |             1905.25 |             1239.46 |
| TPC-DS Q60    |              132.87 |              462.02 |              833.37 |
| TPC-DS Q61    |              197.80 |              200.63 |              507.50 |
| TPC-DS Q62    |              262.22 |              831.17 |              931.19 |
| TPC-DS Q63    |              101.79 |              289.19 |              203.70 |
| TPC-DS Q64    |             4541.89 |             2771.75 |             3665.32 |
| TPC-DS Q65    |             1101.03 |             1999.94 |             1256.10 |
| TPC-DS Q66    |              349.63 |             1191.45 |              735.45 |
| TPC-DS Q67    |             5771.28 |             6086.62 |             5849.81 |
| TPC-DS Q68    |              179.33 |              219.36 |              273.56 |
| TPC-DS Q69    |              248.20 |              272.14 |              404.64 |
| TPC-DS Q70    |             1407.29 |             1527.53 |             1508.38 |
| TPC-DS Q71    |              185.26 |              281.36 |              573.00 |
| TPC-DS Q72    |             1208.52 |             2792.06 |             2615.53 |
| TPC-DS Q73    |               99.09 |              165.89 |              241.05 |
| TPC-DS Q74    |             1862.08 |             2888.08 |             2702.17 |
| TPC-DS Q75    |             6243.02 |             7593.94 |             7434.95 |
| TPC-DS Q76    |              396.81 |             8599.01 |             8929.51 |
| TPC-DS Q77    |              810.90 |             1187.75 |             1265.78 |
| TPC-DS Q78    |            12887.06 |            17007.30 |            18317.05 |
| TPC-DS Q79    |              222.48 |              832.38 |              235.02 |
| TPC-DS Q80    |             7893.98 |            10926.31 |             9493.85 |
| TPC-DS Q81    |               73.40 |               95.06 |               94.85 |
| TPC-DS Q82    |              477.77 |              498.02 |              463.52 |
| TPC-DS Q83    |               55.18 |              262.20 |              264.63 |
| TPC-DS Q84    |               32.92 |               84.29 |               85.36 |
| TPC-DS Q85    |              288.88 |              579.94 |              693.01 |
| TPC-DS Q86    |              345.10 |              746.92 |              565.19 |
| TPC-DS Q87    |             2817.96 |             2994.51 |             2945.84 |
| TPC-DS Q88    |              416.48 |              743.04 |              689.96 |
| TPC-DS Q89    |              129.60 |              203.06 |              218.28 |
| TPC-DS Q90    |               78.83 |               68.10 |               98.87 |
| TPC-DS Q91    |               27.36 |               26.98 |               42.63 |
| TPC-DS Q92    |              147.73 |              130.45 |              153.88 |
| TPC-DS Q93    |             1937.13 |             3068.48 |             3333.45 |
| TPC-DS Q94    |            37151.24 |           105021.42 |           143547.25 |
| TPC-DS Q95    |           352010.44 |           550293.75 |           723908.16 |
| TPC-DS Q96    |              766.72 |             1122.51 |              779.20 |
| TPC-DS Q97    |             4305.48 |             6649.95 |             4181.70 |
| TPC-DS Q98    |              492.40 |              825.85 |              571.02 |
| TPC-DS Q99    |              409.04 |              828.10 |              402.74 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      2979.93 |      7.00 |          72.06 |                 73.52 |
| monetdb-1-1-2-1 |      2979.93 |      7.00 |          72.06 |                 73.52 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      4288.69 |      8.00 |           0.02 |                  5.98 |
| monetdb-1-1-2-1 |      4288.69 |      8.00 |           0.02 |                  5.98 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       476.78 |      1.34 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 |       476.78 |      1.34 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     12919.39 |    164.76 |        1011.00 |               1023.99 |
| monetdb-1-1-2-1 |     22180.95 |    157.13 |        1019.76 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        18.26 |      0.02 |           0.35 |                  0.36 |
| monetdb-1-1-2-1 |        36.73 |      0.46 |           0.31 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
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
