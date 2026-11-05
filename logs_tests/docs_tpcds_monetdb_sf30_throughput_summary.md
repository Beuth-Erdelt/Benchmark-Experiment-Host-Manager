## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 1922s 
* Code: 1793890732
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:956544
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956548
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956553
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956553
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:956553
  * datadisk:75380
  * volume_size:2.9T
  * volume_used:74G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1793890732

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793890732-65d46c6948-5lrbb: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |   30 |      941.00 |           2.00 |            1.00 |        420.00 |          499.00 |              0 |           0 |             | None           |             0 | False         |              114.77 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        526 |            0.88 |           128495.99 |          20327.00 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        442 |            0.58 |           199227.02 |          24190.05 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-1-3-1-1 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        624 |            0.98 |           115591.85 |          17134.62 |          -1 | monetdb-1-1-3-1-1 |
| monetdb-1-1-3-1-2 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        717 |            0.75 |           153705.47 |          14912.13 |          -1 | monetdb-1-1-3-1-2 |
| monetdb-1-1-3-1-3 | MonetDB-1       | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |           1 | 30.00 |               99 |                  99 |        696 |            0.85 |           134542.56 |          15362.07 |          -1 | monetdb-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        526 |            0.88 |           128495.99 |          20327.00 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        442 |            0.58 |           199227.02 |          24190.05 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |        717 |            0.86 |           133708.42 |          44736.40 |          -1 |

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
| TPC-DS Q1     |             1730.60 |              171.52 |              156.28 |              265.49 |              263.05 |
| TPC-DS Q2     |             4348.58 |             1279.38 |             1606.98 |             3170.63 |             2619.01 |
| TPC-DS Q3     |             2885.35 |              151.31 |              325.06 |              518.76 |              131.85 |
| TPC-DS Q4     |            26588.76 |            16589.00 |            17274.97 |            19848.55 |            18419.82 |
| TPC-DS Q5     |            19471.89 |             1691.39 |             1428.98 |             1530.38 |             2036.31 |
| TPC-DS Q6     |              604.13 |              310.81 |              500.21 |              277.40 |              336.52 |
| TPC-DS Q7     |             5380.11 |              187.69 |             1570.53 |              436.36 |              154.06 |
| TPC-DS Q8     |             3818.15 |              314.12 |              476.99 |              296.29 |              280.10 |
| TPC-DS Q9     |              734.80 |              533.63 |              659.94 |              887.68 |              580.13 |
| TPC-DS Q10    |            22119.81 |              124.65 |              232.57 |              141.90 |              306.29 |
| TPC-DS Q11    |             7120.58 |             7156.00 |             7535.94 |             8137.51 |             8007.76 |
| TPC-DS Q12    |              259.16 |              195.55 |              118.49 |              210.31 |              529.48 |
| TPC-DS Q13    |              524.70 |              286.18 |              285.03 |              589.51 |              486.63 |
| TPC-DS Q14a+b |            37099.72 |            30876.13 |            32172.15 |            32877.44 |            32436.89 |
| TPC-DS Q15    |              159.41 |              134.66 |              176.36 |              132.24 |              126.82 |
| TPC-DS Q16    |            50168.43 |            44857.42 |            43024.68 |           157812.98 |           133649.61 |
| TPC-DS Q17    |             3392.58 |             2781.61 |             4506.47 |             2602.14 |             8346.70 |
| TPC-DS Q18    |             2140.69 |              939.99 |            12464.75 |             1275.67 |            16269.12 |
| TPC-DS Q19    |              178.54 |              182.91 |             4684.41 |              257.00 |              159.43 |
| TPC-DS Q20    |              136.85 |              113.20 |            33348.68 |              183.03 |              170.34 |
| TPC-DS Q21    |             2341.05 |               99.09 |            22106.63 |              153.84 |              180.33 |
| TPC-DS Q22    |             1878.99 |              975.21 |            17535.60 |             1194.01 |             1244.55 |
| TPC-DS Q23a+b |            54445.99 |            57269.94 |            62973.68 |            65840.02 |            60235.09 |
| TPC-DS Q24a+b |            14043.62 |            16345.81 |             8062.14 |             9998.54 |             6268.13 |
| TPC-DS Q25    |             2346.58 |             2324.78 |             3006.12 |             2706.92 |             3957.40 |
| TPC-DS Q26    |              193.31 |              197.52 |              312.70 |              349.60 |              206.84 |
| TPC-DS Q27    |             1278.65 |             1331.81 |             1536.13 |             1344.30 |             2318.56 |
| TPC-DS Q28    |              605.77 |              521.83 |              648.36 |              644.20 |              991.21 |
| TPC-DS Q29    |             3074.86 |             2706.63 |             2655.41 |             2317.36 |             4124.96 |
| TPC-DS Q30    |              115.81 |               72.55 |               76.81 |               76.66 |               72.28 |
| TPC-DS Q31    |             2294.38 |             1570.12 |             1521.79 |             1892.54 |             2801.78 |
| TPC-DS Q32    |              155.54 |              174.52 |              120.28 |              174.12 |              183.98 |
| TPC-DS Q33    |              167.53 |              130.19 |              116.61 |              113.24 |              280.11 |
| TPC-DS Q34    |              314.55 |              103.82 |              107.96 |              102.61 |              136.43 |
| TPC-DS Q35    |              761.89 |              713.64 |              668.00 |              756.48 |             1035.97 |
| TPC-DS Q36    |             1639.83 |             1686.31 |             2284.08 |             2510.63 |             2134.45 |
| TPC-DS Q37    |             1481.15 |              491.47 |              363.70 |              420.82 |              986.60 |
| TPC-DS Q38    |             2510.38 |             2392.42 |             4282.34 |             2911.35 |             3011.97 |
| TPC-DS Q39a+b |             1370.26 |             1173.68 |             3208.96 |             1251.44 |             1286.13 |
| TPC-DS Q40    |              420.50 |              671.32 |              868.39 |              355.61 |              493.85 |
| TPC-DS Q41    |                5.38 |                7.51 |               81.99 |                9.49 |                6.81 |
| TPC-DS Q42    |              110.87 |               90.73 |              488.03 |               81.04 |              103.63 |
| TPC-DS Q43    |              313.64 |              207.70 |             1167.57 |              204.66 |              322.33 |
| TPC-DS Q44    |              227.91 |              221.17 |              408.42 |              244.55 |              215.78 |
| TPC-DS Q45    |              121.90 |              117.97 |              142.91 |              136.39 |              138.14 |
| TPC-DS Q46    |              215.92 |              199.34 |              812.10 |              225.82 |              238.88 |
| TPC-DS Q47    |              975.37 |             1056.26 |             4294.26 |             1739.29 |             1252.04 |
| TPC-DS Q48    |              217.78 |              213.51 |             3557.61 |              271.36 |              221.46 |
| TPC-DS Q49    |             4466.05 |             1033.19 |             2656.92 |             1736.34 |             1375.73 |
| TPC-DS Q50    |              604.91 |              578.55 |              633.72 |              652.69 |              924.45 |
| TPC-DS Q51    |             2270.52 |             2333.36 |             3082.19 |             2323.08 |             2570.38 |
| TPC-DS Q52    |              118.99 |               79.06 |              759.21 |              120.02 |               87.57 |
| TPC-DS Q53    |              145.09 |               88.03 |              274.84 |               85.09 |               91.85 |
| TPC-DS Q54    |              159.39 |               92.16 |              173.27 |               87.83 |               93.61 |
| TPC-DS Q55    |               97.41 |               71.55 |               92.39 |               80.60 |               87.05 |
| TPC-DS Q56    |              436.97 |              170.14 |              198.20 |              104.44 |              246.13 |
| TPC-DS Q57    |              281.35 |              135.77 |              141.73 |              134.77 |              227.91 |
| TPC-DS Q58    |              569.38 |              565.06 |              560.25 |              513.22 |              825.63 |
| TPC-DS Q59    |              998.43 |             1206.95 |              765.24 |              628.95 |              606.94 |
| TPC-DS Q60    |              166.97 |              136.14 |              120.98 |              194.90 |              132.29 |
| TPC-DS Q61    |              261.16 |              201.50 |              208.94 |              300.55 |              244.77 |
| TPC-DS Q62    |              447.76 |              268.72 |              293.73 |              379.71 |              270.70 |
| TPC-DS Q63    |              101.22 |               96.19 |              101.52 |              109.91 |              185.65 |
| TPC-DS Q64    |             6253.45 |             2464.46 |             3079.45 |             2374.45 |             2439.47 |
| TPC-DS Q65    |             1795.59 |             1714.25 |             1084.98 |             1040.56 |             1128.37 |
| TPC-DS Q66    |             2289.80 |             1682.44 |             1795.17 |             2299.04 |             1053.25 |
| TPC-DS Q67    |             5560.55 |             5594.07 |             5643.89 |             6562.13 |             6091.21 |
| TPC-DS Q68    |              515.00 |              521.21 |              439.44 |              258.64 |              429.43 |
| TPC-DS Q69    |               94.45 |              104.67 |               96.48 |              111.00 |              110.79 |
| TPC-DS Q70    |             1434.57 |             1439.26 |             1486.04 |             2097.38 |             1486.63 |
| TPC-DS Q71    |              353.05 |              183.76 |              178.15 |              182.46 |              872.01 |
| TPC-DS Q72    |             2339.64 |             1475.15 |             1086.45 |             1155.38 |             1033.56 |
| TPC-DS Q73    |               98.87 |               98.61 |               86.12 |               90.62 |              113.27 |
| TPC-DS Q74    |             2520.74 |             1861.18 |             2118.07 |             2094.24 |             2297.78 |
| TPC-DS Q75    |             6487.58 |             5848.43 |             6003.47 |             5578.15 |             6081.12 |
| TPC-DS Q76    |             1993.83 |              320.36 |              189.78 |              170.63 |              160.32 |
| TPC-DS Q77    |             1247.74 |              780.38 |              766.96 |              698.86 |              789.85 |
| TPC-DS Q78    |            12554.74 |            14208.19 |            13210.85 |            15795.93 |            15892.51 |
| TPC-DS Q79    |              267.77 |              248.80 |              257.03 |              248.29 |              235.56 |
| TPC-DS Q80    |             7282.42 |             8103.07 |             7540.67 |             9286.84 |             9356.26 |
| TPC-DS Q81    |              164.00 |              138.99 |              128.36 |              321.56 |              311.18 |
| TPC-DS Q82    |              438.61 |              449.80 |              822.27 |              412.73 |              378.60 |
| TPC-DS Q83    |              251.37 |               60.63 |               39.06 |               41.20 |               43.60 |
| TPC-DS Q84    |               46.78 |               40.50 |               34.38 |               43.41 |               44.49 |
| TPC-DS Q85    |              301.98 |              318.60 |              299.57 |              302.47 |              278.84 |
| TPC-DS Q86    |              308.54 |              333.65 |              346.50 |              280.50 |              285.89 |
| TPC-DS Q87    |             2790.49 |             2829.57 |             3350.04 |             5438.77 |             4050.00 |
| TPC-DS Q88    |              705.45 |              414.10 |              917.75 |            15204.61 |             9447.84 |
| TPC-DS Q89    |              142.73 |              273.12 |              176.95 |             4002.09 |            10594.10 |
| TPC-DS Q90    |               71.47 |               68.37 |               69.67 |              153.11 |              147.99 |
| TPC-DS Q91    |               60.93 |               26.55 |               39.78 |              337.49 |              339.87 |
| TPC-DS Q92    |              134.92 |              158.24 |              133.44 |             3243.37 |             2978.56 |
| TPC-DS Q93    |             2193.92 |             2078.71 |             2557.93 |            17678.94 |            18094.81 |
| TPC-DS Q94    |            40706.17 |            36277.09 |            39039.57 |            98735.00 |            50400.27 |
| TPC-DS Q95    |            49797.92 |            51272.42 |            51891.60 |            65517.21 |            87713.72 |
| TPC-DS Q96    |               34.29 |               61.65 |               86.84 |               39.34 |              345.63 |
| TPC-DS Q97    |             3845.98 |             3119.01 |             7736.77 |             3093.93 |             6243.94 |
| TPC-DS Q98    |              149.20 |              158.14 |            11320.54 |              145.57 |              479.36 |
| TPC-DS Q99    |              275.90 |              321.98 |            31634.47 |              254.64 |              778.45 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      6293.15 |     75.49 |         378.89 |                378.90 |
| monetdb-1-1-2-1 |      6751.14 |     91.66 |         360.63 |                360.64 |
| monetdb-1-1-3-1 |     20408.22 |    146.85 |         510.54 |                510.55 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        80.18 |      0.70 |           0.69 |                  0.73 |
| monetdb-1-1-2-1 |        85.24 |      0.76 |           0.72 |                  0.75 |
| monetdb-1-1-3-1 |       340.74 |      2.74 |           0.73 |                  0.76 |

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
