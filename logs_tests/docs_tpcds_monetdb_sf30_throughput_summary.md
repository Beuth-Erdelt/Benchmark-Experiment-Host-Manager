## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3957s 
* Code: 1794679292
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 3000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 900Gi RAM. RAM limit is 1024Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041487
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041501
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041507
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041507
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1041507
  * datadisk:75446
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794679292

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794679292-845c86f48c-ht4pr: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpcds (3 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpcds (3 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              0 |         0 |             | None           |             0 | False         |              109.98 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        814 |            0.88 |           126416.63 |          13135.14 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        726 |            0.74 |           151474.64 |          14727.27 |          -1 |
| monetdb-1-1-3-1-1 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       1 | 30.00 |               99 |                  99 |       1140 |            1.17 |            94355.48 |           9378.95 |          -1 |
| monetdb-1-1-3-1-2 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       2 | 30.00 |               99 |                  99 |       2040 |            0.88 |           128193.48 |           5241.18 |          -1 |
| monetdb-1-1-3-1-3 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       3 | 30.00 |               99 |                  99 |       2084 |            0.87 |           129387.12 |           5130.52 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        814 |            0.88 |           126416.63 |          13135.14 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        726 |            0.74 |           151474.64 |          14727.27 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |       2084 |            0.96 |           116102.45 |          15391.55 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-3 |      3 | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3         | 3/3          | 3/3          | 3/3          | 3/3          | 3/3             | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3             | 3/3             | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3             | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | 3/3          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-3-1-1 |   monetdb-1-1-3-1-2 |   monetdb-1-1-3-1-3 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |             1149.39 |              222.39 |              331.54 |              204.77 |              180.88 |
| TPC-DS Q2     |             4098.29 |             2399.26 |             3992.24 |             4240.45 |             3579.75 |
| TPC-DS Q3     |             2526.82 |              188.52 |              130.48 |              621.85 |              261.11 |
| TPC-DS Q4     |            26296.42 |            17066.69 |            20358.81 |            17489.68 |            21436.64 |
| TPC-DS Q5     |            17989.41 |             2683.29 |             2723.71 |             5092.41 |             1888.42 |
| TPC-DS Q6     |              620.89 |              313.44 |             1204.53 |             1499.28 |             1313.88 |
| TPC-DS Q7     |             4123.94 |              957.50 |             1067.64 |              594.84 |             1233.18 |
| TPC-DS Q8     |             3667.21 |              360.98 |              412.09 |              421.35 |              408.80 |
| TPC-DS Q9     |             1253.40 |              572.36 |             1534.41 |             1741.65 |             1559.92 |
| TPC-DS Q10    |            20032.75 |              541.81 |              641.84 |              371.83 |              636.32 |
| TPC-DS Q11    |             7260.67 |             6633.16 |             7714.30 |             7418.39 |             8634.37 |
| TPC-DS Q12    |              243.21 |              165.07 |              709.46 |              436.30 |               94.10 |
| TPC-DS Q13    |              650.36 |              523.97 |              281.67 |              984.78 |              323.06 |
| TPC-DS Q14a+b |            36384.77 |            34542.22 |            36824.16 |            37557.80 |            36830.24 |
| TPC-DS Q15    |              175.12 |              130.80 |              291.93 |              170.68 |              261.53 |
| TPC-DS Q16    |            49407.70 |            43480.53 |            41105.25 |           152446.03 |           141309.73 |
| TPC-DS Q17    |             4199.07 |             3349.20 |             3935.52 |             2737.31 |             6194.97 |
| TPC-DS Q18    |             2140.05 |             2219.25 |             3168.71 |              972.44 |             3366.62 |
| TPC-DS Q19    |              192.39 |              166.39 |             6520.34 |              254.66 |             1483.46 |
| TPC-DS Q20    |              140.34 |              109.19 |             7300.27 |              135.39 |              120.71 |
| TPC-DS Q21    |             2206.38 |              165.48 |             4169.25 |              117.18 |              103.55 |
| TPC-DS Q22    |             1851.06 |             2215.58 |             4936.64 |             1178.68 |             1270.64 |
| TPC-DS Q23a+b |            53875.75 |            49119.01 |            99026.34 |            58936.57 |            55950.63 |
| TPC-DS Q24a+b |            14693.95 |            16385.50 |             9672.09 |             8123.41 |             9392.61 |
| TPC-DS Q25    |             2460.11 |             2276.47 |             3645.82 |             3663.49 |             3698.39 |
| TPC-DS Q26    |              164.92 |              229.50 |              185.54 |              313.05 |              222.76 |
| TPC-DS Q27    |             1462.95 |             1384.73 |             1862.83 |             1823.32 |             1751.79 |
| TPC-DS Q28    |              832.85 |              645.94 |              708.73 |              621.98 |             1292.59 |
| TPC-DS Q29    |             2192.46 |             2994.26 |             3074.08 |             2677.72 |             3780.36 |
| TPC-DS Q30    |              103.14 |              113.68 |              110.50 |              145.95 |              494.98 |
| TPC-DS Q31    |             2286.92 |             2171.23 |             2198.14 |             1683.16 |             2773.80 |
| TPC-DS Q32    |              184.83 |              168.96 |              107.59 |              237.45 |              180.25 |
| TPC-DS Q33    |              146.96 |              240.13 |              132.24 |              118.34 |              118.60 |
| TPC-DS Q34    |              322.31 |              195.76 |              239.90 |              105.24 |              109.71 |
| TPC-DS Q35    |              802.47 |              824.29 |              714.01 |              730.26 |             1047.36 |
| TPC-DS Q36    |             1431.24 |             1341.62 |             1334.82 |             1684.14 |             1387.60 |
| TPC-DS Q37    |              427.25 |              432.61 |              396.00 |              524.16 |              413.31 |
| TPC-DS Q38    |             3089.72 |             2735.95 |             2478.05 |             2866.13 |             2967.04 |
| TPC-DS Q39a+b |             1193.56 |             1184.14 |             1303.47 |             1294.36 |             1132.69 |
| TPC-DS Q40    |              414.58 |              594.11 |              695.24 |              426.67 |              327.49 |
| TPC-DS Q41    |                6.57 |                6.05 |                5.78 |                5.09 |                5.57 |
| TPC-DS Q42    |              118.55 |              114.15 |               87.99 |               68.37 |               88.44 |
| TPC-DS Q43    |              213.76 |              209.26 |              202.80 |              221.90 |              239.79 |
| TPC-DS Q44    |              247.27 |              352.07 |              225.85 |              244.24 |              239.87 |
| TPC-DS Q45    |              132.07 |              173.90 |              128.58 |              141.56 |              177.45 |
| TPC-DS Q46    |              233.33 |              199.43 |              184.22 |              197.99 |              208.74 |
| TPC-DS Q47    |              941.51 |              892.04 |             1020.62 |             1048.30 |             1046.56 |
| TPC-DS Q48    |              218.16 |              209.70 |              379.98 |              215.13 |              384.65 |
| TPC-DS Q49    |             4295.28 |             1634.39 |             1663.86 |             1566.72 |             1056.68 |
| TPC-DS Q50    |              553.82 |              573.99 |              600.55 |              728.85 |              606.64 |
| TPC-DS Q51    |             2751.18 |             2560.43 |             2940.82 |             3133.39 |             2902.03 |
| TPC-DS Q52    |              122.94 |              113.21 |              176.24 |              115.45 |               85.41 |
| TPC-DS Q53    |               96.48 |               91.63 |               91.27 |              136.64 |              173.43 |
| TPC-DS Q54    |               88.46 |               91.55 |              103.09 |               92.38 |              220.84 |
| TPC-DS Q55    |               72.72 |               87.09 |              567.48 |               78.31 |               94.43 |
| TPC-DS Q56    |              152.63 |              123.40 |              754.51 |              106.98 |              139.82 |
| TPC-DS Q57    |              146.16 |              138.90 |             1652.59 |              161.77 |              203.87 |
| TPC-DS Q58    |              645.67 |              631.84 |             1497.06 |              534.49 |              575.88 |
| TPC-DS Q59    |             1298.21 |             1145.81 |             2101.68 |              639.85 |              819.59 |
| TPC-DS Q60    |              169.81 |              186.76 |             1488.67 |              382.25 |              276.40 |
| TPC-DS Q61    |              167.18 |              171.89 |              412.90 |              344.60 |              162.94 |
| TPC-DS Q62    |              442.43 |              445.91 |             3505.07 |              322.26 |              301.99 |
| TPC-DS Q63    |               93.14 |               91.62 |               95.17 |              120.60 |              115.30 |
| TPC-DS Q64    |             4895.80 |             5521.34 |             7788.78 |             2337.21 |             2794.97 |
| TPC-DS Q65    |             1194.72 |             1111.47 |             2156.08 |             1563.49 |             1164.16 |
| TPC-DS Q66    |             1229.27 |             1300.59 |             1236.84 |              341.30 |              379.16 |
| TPC-DS Q67    |             6008.78 |             6239.05 |             6463.88 |             7729.61 |             6680.92 |
| TPC-DS Q68    |              230.20 |              219.54 |              237.51 |              308.86 |              209.71 |
| TPC-DS Q69    |              373.81 |              394.64 |              414.44 |              245.30 |              319.98 |
| TPC-DS Q70    |             1363.06 |             2301.16 |             1910.34 |             1392.28 |             2254.23 |
| TPC-DS Q71    |              355.79 |              501.88 |              499.70 |              180.92 |              198.46 |
| TPC-DS Q72    |             2287.26 |             2440.33 |             2822.94 |             1055.79 |             1492.78 |
| TPC-DS Q73    |               90.23 |               93.17 |               96.79 |              104.45 |               99.08 |
| TPC-DS Q74    |             1842.48 |             2297.63 |             2523.29 |             3095.26 |             2059.40 |
| TPC-DS Q75    |             7530.87 |             6224.35 |             7718.65 |             6935.77 |             7339.98 |
| TPC-DS Q76    |             2722.48 |             3797.37 |             3394.68 |              168.79 |              192.97 |
| TPC-DS Q77    |             1164.21 |             1260.77 |             1225.51 |              823.67 |             1394.25 |
| TPC-DS Q78    |            13008.62 |            13408.43 |            15091.84 |            15567.01 |            15777.29 |
| TPC-DS Q79    |              204.67 |              222.12 |              213.64 |              222.56 |              251.22 |
| TPC-DS Q80    |             7624.48 |             8157.56 |            11548.96 |             9329.94 |             9420.39 |
| TPC-DS Q81    |              138.62 |              187.36 |              152.87 |              140.64 |              179.04 |
| TPC-DS Q82    |              519.76 |              520.54 |              647.44 |              464.95 |              702.05 |
| TPC-DS Q83    |              240.25 |              279.73 |              236.86 |               41.80 |               40.49 |
| TPC-DS Q84    |               55.48 |               91.26 |               45.11 |               37.23 |               37.02 |
| TPC-DS Q85    |              303.62 |              297.09 |              331.93 |              437.14 |              502.20 |
| TPC-DS Q86    |              311.72 |              417.34 |              342.05 |              568.14 |              271.23 |
| TPC-DS Q87    |             3142.68 |             3180.62 |             3298.18 |             4526.51 |             3766.11 |
| TPC-DS Q88    |              636.79 |              415.95 |             1239.84 |             4593.62 |             7244.82 |
| TPC-DS Q89    |              149.41 |              126.76 |              238.75 |             4866.10 |             1182.02 |
| TPC-DS Q90    |               80.49 |              122.18 |              145.12 |             5308.67 |             2641.44 |
| TPC-DS Q91    |               42.45 |               34.97 |               73.03 |              572.01 |             1460.31 |
| TPC-DS Q92    |              144.83 |              152.49 |              161.55 |             4552.95 |             7583.19 |
| TPC-DS Q93    |             2381.77 |             2114.31 |             2279.27 |             2539.06 |             5488.89 |
| TPC-DS Q94    |            36115.61 |            39463.79 |            40896.94 |           111356.87 |            76512.86 |
| TPC-DS Q95    |           399319.62 |           381848.61 |           621033.50 |          1482120.49 |          1566279.01 |
| TPC-DS Q96    |              768.22 |              747.25 |            30167.79 |              935.21 |               42.34 |
| TPC-DS Q97    |             4009.56 |             4133.86 |            22779.51 |             6489.72 |             3723.90 |
| TPC-DS Q98    |              472.44 |              568.24 |            17245.83 |              579.22 |              150.04 |
| TPC-DS Q99    |              422.85 |              428.18 |            12237.65 |              497.36 |              254.88 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     14080.86 |    166.90 |         979.71 |               1023.95 |
| monetdb-1-1-2-1 |     13123.52 |    188.05 |         967.96 |               1023.98 |
| monetdb-1-1-3-1 |     41891.04 |    187.08 |        1014.89 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        32.78 |      0.26 |           0.35 |                  0.36 |
| monetdb-1-1-2-1 |        30.22 |      0.17 |           0.36 |                  0.37 |
| monetdb-1-1-3-1 |        99.70 |      0.65 |           0.38 |                  0.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-3-1 (bexhoma-metrics-monetdb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-3-1 (bexhoma-metrics-monetdb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MonetDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
 TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
