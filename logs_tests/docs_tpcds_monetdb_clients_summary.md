## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 8165s 
* Code: 1795772856
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
  * disk:745326
  * datadisk:75600
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795772856
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745326
  * datadisk:76836
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
    * code:1795772856
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:745326
  * datadisk:76836
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
    * code:1795772856

### Ingestion
* MonetDB-1: 81 of 81 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795772856-6bff4547b5-q8lx8: 0

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
| MonetDB-1-1 |                1 |   30 |     1576.00 |           2.00 |          563.00 |        491.00 |          517.00 |              8 |         0 |             | None           |             0 | False         |               68.53 | False               |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        355 |            0.54 |           201608.06 |          30118.31 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        398 |            0.66 |           162522.23 |          26864.32 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 30.00 |               99 |                  99 |        421 |            0.57 |           190218.65 |          25396.67 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        355 |            0.54 |           201608.06 |          30118.31 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 30.00 |              198 |                 198 |        421 |            0.61 |           175825.93 |          50793.35 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |              124.01 |              107.95 |              215.88 |
| TPC-DS Q2     |             1461.25 |             1833.90 |             2191.54 |
| TPC-DS Q3     |              105.05 |              108.21 |              101.83 |
| TPC-DS Q4     |            15832.98 |            14752.68 |            15590.25 |
| TPC-DS Q5     |             1425.42 |             1428.07 |             1324.32 |
| TPC-DS Q6     |              446.08 |              773.99 |              747.21 |
| TPC-DS Q7     |              183.42 |              158.86 |              400.40 |
| TPC-DS Q8     |              315.65 |              374.19 |              308.49 |
| TPC-DS Q9     |              500.85 |              825.08 |              671.29 |
| TPC-DS Q10    |              189.13 |              239.59 |              151.34 |
| TPC-DS Q11    |             7210.77 |             6756.72 |             7593.00 |
| TPC-DS Q12    |              149.21 |              113.54 |              171.63 |
| TPC-DS Q13    |              341.36 |              291.30 |              289.71 |
| TPC-DS Q14a+b |            29978.61 |            29917.20 |            31467.36 |
| TPC-DS Q15    |              146.26 |              142.36 |              129.83 |
| TPC-DS Q16    |            44476.90 |            41171.92 |            67929.13 |
| TPC-DS Q17    |             2455.90 |             3681.04 |             2221.02 |
| TPC-DS Q18    |              949.72 |             3810.74 |              955.35 |
| TPC-DS Q19    |              186.11 |            10548.01 |              143.71 |
| TPC-DS Q20    |              129.91 |            11701.91 |              112.51 |
| TPC-DS Q21    |              113.12 |              108.94 |              107.41 |
| TPC-DS Q22    |             1057.05 |             1102.88 |             1021.34 |
| TPC-DS Q23a+b |            53570.09 |            49899.90 |            52353.71 |
| TPC-DS Q24a+b |            14380.13 |            11788.36 |            14540.61 |
| TPC-DS Q25    |             2430.52 |             3347.83 |             3566.38 |
| TPC-DS Q26    |              189.21 |              550.16 |              173.85 |
| TPC-DS Q27    |             1259.54 |             1465.74 |             1935.99 |
| TPC-DS Q28    |              533.24 |             2179.99 |              581.36 |
| TPC-DS Q29    |             2841.34 |             2873.41 |             2963.92 |
| TPC-DS Q30    |               89.98 |              289.88 |               74.86 |
| TPC-DS Q31    |             1590.91 |             2387.99 |             1579.72 |
| TPC-DS Q32    |              164.70 |              184.11 |              179.12 |
| TPC-DS Q33    |              122.69 |              112.00 |              339.04 |
| TPC-DS Q34    |              107.90 |              103.69 |              102.54 |
| TPC-DS Q35    |              727.45 |             1173.29 |              691.12 |
| TPC-DS Q36    |             1996.99 |             2608.11 |             1402.87 |
| TPC-DS Q37    |              454.47 |              422.23 |              546.98 |
| TPC-DS Q38    |             2858.25 |             2639.59 |             2463.81 |
| TPC-DS Q39a+b |             1616.40 |             1188.82 |             1233.98 |
| TPC-DS Q40    |              928.35 |             1293.94 |             1536.99 |
| TPC-DS Q41    |                6.51 |                7.58 |                6.70 |
| TPC-DS Q42    |              106.34 |              114.25 |              135.88 |
| TPC-DS Q43    |              217.36 |              196.00 |              217.52 |
| TPC-DS Q44    |              195.73 |              215.58 |              257.21 |
| TPC-DS Q45    |              127.34 |              123.04 |              131.44 |
| TPC-DS Q46    |              200.72 |              218.18 |              305.26 |
| TPC-DS Q47    |             1591.54 |              830.05 |              982.05 |
| TPC-DS Q48    |              206.33 |              217.15 |              229.16 |
| TPC-DS Q49    |             1044.65 |             1308.48 |             1061.89 |
| TPC-DS Q50    |              615.83 |              554.15 |              573.06 |
| TPC-DS Q51    |             3065.12 |             2815.27 |             3023.40 |
| TPC-DS Q52    |              101.74 |              111.04 |               87.73 |
| TPC-DS Q53    |               90.70 |               92.63 |              165.43 |
| TPC-DS Q54    |               92.85 |               98.92 |              127.24 |
| TPC-DS Q55    |               57.71 |               97.53 |              102.40 |
| TPC-DS Q56    |              140.19 |              157.82 |              122.62 |
| TPC-DS Q57    |              128.84 |              138.80 |              148.83 |
| TPC-DS Q58    |              520.81 |              590.79 |              545.99 |
| TPC-DS Q59    |              998.54 |              693.89 |              754.48 |
| TPC-DS Q60    |              152.37 |              154.67 |              155.66 |
| TPC-DS Q61    |              158.61 |              163.79 |              190.92 |
| TPC-DS Q62    |              259.96 |              270.47 |              309.83 |
| TPC-DS Q63    |              134.65 |              102.48 |               91.90 |
| TPC-DS Q64    |             4539.93 |             2281.65 |             2297.30 |
| TPC-DS Q65    |             1967.58 |             1119.92 |             1207.44 |
| TPC-DS Q66    |              298.08 |              316.89 |              302.19 |
| TPC-DS Q67    |             6026.07 |             6455.00 |             5836.87 |
| TPC-DS Q68    |              212.91 |              221.91 |              224.25 |
| TPC-DS Q69    |              293.96 |              280.99 |              237.49 |
| TPC-DS Q70    |             1531.69 |             1506.37 |             1544.38 |
| TPC-DS Q71    |              294.57 |              206.42 |              184.65 |
| TPC-DS Q72    |             1901.57 |             1081.13 |             1041.38 |
| TPC-DS Q73    |              142.09 |               99.96 |               97.83 |
| TPC-DS Q74    |             1954.28 |             2267.34 |             2370.78 |
| TPC-DS Q75    |             5576.75 |             5351.57 |             5727.89 |
| TPC-DS Q76    |              179.31 |              156.33 |              256.94 |
| TPC-DS Q77    |              734.24 |              753.59 |              686.34 |
| TPC-DS Q78    |            12681.29 |            13356.51 |            13714.74 |
| TPC-DS Q79    |              251.49 |              242.70 |              265.07 |
| TPC-DS Q80    |             7508.01 |             8587.38 |             8665.00 |
| TPC-DS Q81    |              140.01 |              185.09 |              368.25 |
| TPC-DS Q82    |              447.63 |              477.40 |              479.44 |
| TPC-DS Q83    |               65.65 |               44.67 |               36.07 |
| TPC-DS Q84    |               28.97 |               36.19 |               34.19 |
| TPC-DS Q85    |              289.24 |              288.82 |              324.14 |
| TPC-DS Q86    |              307.28 |              299.31 |              293.39 |
| TPC-DS Q87    |             3438.74 |             2637.17 |             2790.67 |
| TPC-DS Q88    |              442.41 |              440.57 |              511.85 |
| TPC-DS Q89    |              138.38 |              169.23 |              167.18 |
| TPC-DS Q90    |               68.83 |               81.24 |               68.01 |
| TPC-DS Q91    |               26.24 |               40.41 |               35.52 |
| TPC-DS Q92    |              104.22 |              162.38 |              156.96 |
| TPC-DS Q93    |             2402.93 |             2285.92 |             1994.42 |
| TPC-DS Q94    |            40927.30 |            36720.13 |            75565.53 |
| TPC-DS Q95    |            42709.70 |            42464.51 |            43327.96 |
| TPC-DS Q96    |               33.78 |             2558.81 |               52.84 |
| TPC-DS Q97    |             3015.74 |            22826.25 |             3209.45 |
| TPC-DS Q98    |              140.90 |              153.54 |              149.49 |
| TPC-DS Q99    |              235.13 |              254.55 |              241.52 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      3087.61 |      6.96 |          73.59 |                 73.60 |
| monetdb-1-1-2-1 |      3087.61 |      6.96 |          73.59 |                 73.60 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      4146.41 |      8.00 |           0.02 |                  5.98 |
| monetdb-1-1-2-1 |      4146.41 |      8.00 |           0.02 |                  5.98 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       468.39 |      1.33 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 |       468.39 |      1.33 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      5728.01 |     73.47 |         419.30 |                419.31 |
| monetdb-1-1-2-1 |     12902.17 |    132.85 |         451.81 |                451.83 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        15.73 |      0.02 |           0.29 |                  0.30 |
| monetdb-1-1-2-1 |        32.53 |      0.95 |           0.30 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
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
