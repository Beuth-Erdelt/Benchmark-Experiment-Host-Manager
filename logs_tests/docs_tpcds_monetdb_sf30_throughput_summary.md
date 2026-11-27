## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 2686s 
* Code: 1795706405
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
  * disk:643805
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
    * code:1795706405
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:639984
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
    * code:1795706405
* monetdb-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:645548
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
    * code:1795706405
* monetdb-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:645548
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
    * code:1795706405
* monetdb-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:645548
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
    * code:1795706405

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795706405-b4967bc7-l7975: 0

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
| MonetDB-1-1 |                1 |   30 |     1661.00 |           3.00 |          717.00 |        409.00 |          527.00 |              0 |         0 |             | None           |             0 | False         |               65.02 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        586 |            0.91 |           124029.69 |          18245.73 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        469 |            0.59 |           195900.16 |          22797.44 |          -1 |
| monetdb-1-1-3-1-1 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       1 | 30.00 |               99 |                  99 |       1319 |            0.99 |           115285.95 |           8106.14 |          -1 |
| monetdb-1-1-3-1-2 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       2 | 30.00 |               99 |                  99 |        807 |            0.87 |           127683.25 |          13249.07 |          -1 |
| monetdb-1-1-3-1-3 | monetdb-1-1-3 | monetdb-1-1-3-1 |                1 |        3 |               1 |       3 | 30.00 |               99 |                  99 |       1297 |            0.84 |           133534.09 |           8243.64 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        586 |            0.91 |           124029.69 |          18245.73 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        469 |            0.59 |           195900.16 |          22797.44 |          -1 |
| monetdb-1-1-3 | monetdb-1-1-3 |                1 |        3 |               1 |           3 | 30.00 |              297 |                 297 |       1319 |            0.90 |           125266.27 |          24318.42 |          -1 |

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
| TPC-DS Q1     |             1645.35 |              273.54 |              380.22 |              251.66 |              370.66 |
| TPC-DS Q2     |             3903.88 |             1304.30 |             2405.47 |             2214.67 |             3253.38 |
| TPC-DS Q3     |             2801.76 |              102.73 |              161.59 |              296.76 |              751.11 |
| TPC-DS Q4     |            26666.79 |            15832.68 |            17428.28 |            19769.40 |            20219.14 |
| TPC-DS Q5     |            20011.86 |             1338.21 |             1972.81 |             2379.15 |             1497.47 |
| TPC-DS Q6     |              582.26 |              322.24 |             1881.25 |              358.90 |              582.30 |
| TPC-DS Q7     |             5468.17 |              156.34 |              212.73 |              170.69 |              163.40 |
| TPC-DS Q8     |             3898.33 |              452.18 |              502.99 |              313.21 |             1426.66 |
| TPC-DS Q9     |             2055.07 |              780.75 |              667.31 |              579.37 |              661.46 |
| TPC-DS Q10    |            20023.43 |              263.34 |              307.50 |              150.93 |              125.08 |
| TPC-DS Q11    |             7899.54 |             7215.97 |             8509.99 |             8931.45 |             9460.57 |
| TPC-DS Q12    |              199.59 |              123.29 |              129.86 |              234.97 |              170.36 |
| TPC-DS Q13    |              712.69 |              290.08 |              314.83 |              297.51 |              323.34 |
| TPC-DS Q14a+b |            33103.83 |            37379.67 |            37968.19 |            35963.21 |            31181.96 |
| TPC-DS Q15    |              159.25 |              115.85 |              122.59 |              271.02 |              724.24 |
| TPC-DS Q16    |            54392.79 |            44198.13 |            68219.98 |            38602.28 |           115060.74 |
| TPC-DS Q17    |             3511.94 |             1945.84 |             2650.81 |             2983.99 |             1965.36 |
| TPC-DS Q18    |             2492.88 |              895.06 |             2059.55 |             1177.61 |             1870.40 |
| TPC-DS Q19    |              162.06 |              147.51 |             9739.66 |             1853.71 |              515.61 |
| TPC-DS Q20    |              141.74 |               98.48 |             4163.64 |             4628.49 |              210.50 |
| TPC-DS Q21    |             2417.29 |               97.70 |            13075.72 |             7062.53 |              157.03 |
| TPC-DS Q22    |             1748.29 |             1022.27 |             3769.80 |             4676.51 |             2070.71 |
| TPC-DS Q23a+b |            43521.62 |            40745.92 |            56824.29 |            54378.96 |            54443.68 |
| TPC-DS Q24a+b |            16408.96 |            15867.02 |             6422.72 |             7412.16 |             9843.29 |
| TPC-DS Q25    |             2374.24 |             3299.29 |             3071.41 |             3266.83 |             3329.82 |
| TPC-DS Q26    |              201.12 |              178.13 |              152.79 |              230.33 |              236.40 |
| TPC-DS Q27    |             1424.44 |             1362.44 |             1699.40 |             1922.11 |             1792.36 |
| TPC-DS Q28    |              841.73 |              915.04 |             1064.02 |              613.15 |              596.80 |
| TPC-DS Q29    |             2198.98 |             2305.96 |             4034.69 |             2695.66 |             2309.93 |
| TPC-DS Q30    |               79.77 |               33.61 |               81.22 |               67.04 |               36.22 |
| TPC-DS Q31    |             2222.65 |             1559.56 |             3675.19 |             1811.92 |             1726.32 |
| TPC-DS Q32    |              131.45 |              170.19 |              101.26 |              161.23 |              274.06 |
| TPC-DS Q33    |              283.27 |              294.86 |              108.29 |              150.24 |              187.13 |
| TPC-DS Q34    |              562.47 |              199.60 |              103.89 |              106.18 |              180.44 |
| TPC-DS Q35    |              853.32 |             1135.12 |             1332.15 |             1023.68 |             1266.19 |
| TPC-DS Q36    |             1740.72 |             1365.59 |             2294.18 |             1433.29 |             1393.72 |
| TPC-DS Q37    |              493.85 |              404.17 |              484.19 |              398.07 |              471.75 |
| TPC-DS Q38    |             2565.12 |             3591.71 |             2966.03 |             2616.26 |             3699.51 |
| TPC-DS Q39a+b |             1527.72 |             1006.96 |             2205.56 |             1346.52 |             1382.88 |
| TPC-DS Q40    |              757.05 |              320.46 |              394.36 |              376.37 |              372.17 |
| TPC-DS Q41    |                9.46 |                4.73 |                6.50 |                8.90 |                6.19 |
| TPC-DS Q42    |               77.29 |              106.61 |               88.88 |              243.64 |              102.00 |
| TPC-DS Q43    |              226.43 |              211.51 |              220.03 |              267.09 |              225.87 |
| TPC-DS Q44    |              210.15 |              206.47 |              216.81 |              300.88 |              255.28 |
| TPC-DS Q45    |              114.25 |              126.39 |              124.77 |              148.09 |              468.87 |
| TPC-DS Q46    |              212.04 |              427.63 |              184.45 |              325.52 |              327.57 |
| TPC-DS Q47    |             1770.76 |             1567.64 |             1661.68 |             1585.53 |             1189.33 |
| TPC-DS Q48    |              217.30 |              217.69 |              228.83 |              222.13 |              227.02 |
| TPC-DS Q49    |             4220.23 |             1068.95 |             1027.50 |             1072.10 |             1151.30 |
| TPC-DS Q50    |              788.73 |              559.92 |              794.58 |              595.93 |             1587.23 |
| TPC-DS Q51    |             3051.08 |             2402.60 |             3460.45 |             3041.54 |             3592.43 |
| TPC-DS Q52    |               70.44 |              101.55 |              108.00 |              105.52 |               98.04 |
| TPC-DS Q53    |              105.25 |               88.60 |              165.12 |               95.74 |               99.18 |
| TPC-DS Q54    |               91.52 |               93.96 |              212.95 |               89.30 |              104.16 |
| TPC-DS Q55    |               81.46 |              126.98 |               99.58 |               69.58 |              109.05 |
| TPC-DS Q56    |              226.53 |              346.56 |              129.03 |              126.53 |              132.11 |
| TPC-DS Q57    |              150.57 |              149.10 |              156.60 |              144.11 |              143.01 |
| TPC-DS Q58    |              567.36 |              553.42 |              890.14 |              512.42 |              544.73 |
| TPC-DS Q59    |             1771.96 |             1100.28 |              800.02 |             1350.37 |             1012.20 |
| TPC-DS Q60    |              192.71 |              146.10 |              357.38 |              248.91 |              228.11 |
| TPC-DS Q61    |              169.02 |              162.27 |              170.24 |              162.72 |              175.63 |
| TPC-DS Q62    |              434.24 |              255.74 |              300.02 |              294.38 |              280.63 |
| TPC-DS Q63    |               93.79 |               94.60 |              113.27 |              104.81 |               96.91 |
| TPC-DS Q64    |             6294.05 |             2098.46 |             2465.25 |             2239.46 |             1998.91 |
| TPC-DS Q65    |             1074.66 |             1513.63 |             1591.66 |             2459.38 |             1397.31 |
| TPC-DS Q66    |             1377.92 |              465.52 |              563.10 |             1438.66 |              309.60 |
| TPC-DS Q67    |             5366.73 |             6589.77 |             7359.14 |             9172.77 |             6557.15 |
| TPC-DS Q68    |              202.29 |              225.25 |              255.66 |             1141.14 |              225.55 |
| TPC-DS Q69    |              393.05 |              291.61 |              254.47 |              738.23 |              272.32 |
| TPC-DS Q70    |             1612.28 |             1530.74 |             2067.41 |             3620.04 |             2045.11 |
| TPC-DS Q71    |              369.18 |              206.37 |              187.57 |              762.26 |              177.09 |
| TPC-DS Q72    |             2458.17 |             1257.39 |             1128.52 |             1241.27 |             1243.45 |
| TPC-DS Q73    |              110.11 |              106.28 |              124.88 |               90.47 |              127.54 |
| TPC-DS Q74    |             1929.06 |             2163.57 |             2885.84 |             2913.32 |             8064.88 |
| TPC-DS Q75    |             7144.33 |             5107.53 |             6155.60 |             7314.37 |            10287.90 |
| TPC-DS Q76    |             7605.38 |              338.85 |             6750.61 |              349.96 |             3119.89 |
| TPC-DS Q77    |             1312.48 |              850.09 |              988.38 |              724.70 |             1430.54 |
| TPC-DS Q78    |            14103.03 |            14352.84 |            15856.57 |            15829.34 |            18335.19 |
| TPC-DS Q79    |              458.44 |              207.36 |             8405.20 |              248.26 |             9115.69 |
| TPC-DS Q80    |             9461.90 |             7142.30 |            12800.06 |            11171.75 |            32766.41 |
| TPC-DS Q81    |              169.87 |              139.93 |             2381.76 |              216.04 |              194.63 |
| TPC-DS Q82    |              454.92 |              427.72 |             3939.07 |              469.03 |              776.38 |
| TPC-DS Q83    |              278.93 |               37.54 |              708.05 |               44.69 |               50.31 |
| TPC-DS Q84    |               45.67 |               31.12 |              564.49 |               33.32 |               35.32 |
| TPC-DS Q85    |              294.45 |              288.95 |            14797.58 |              349.04 |              382.69 |
| TPC-DS Q86    |              321.41 |              326.83 |             1912.14 |              462.14 |              442.97 |
| TPC-DS Q87    |             3062.27 |             2704.27 |             5082.77 |             3350.51 |             4247.65 |
| TPC-DS Q88    |              922.43 |              420.11 |              598.47 |              447.82 |              578.42 |
| TPC-DS Q89    |              274.59 |              144.19 |              197.53 |              158.48 |              197.49 |
| TPC-DS Q90    |              112.24 |              161.76 |               88.54 |               69.18 |              100.81 |
| TPC-DS Q91    |               43.50 |               37.74 |               35.07 |               25.16 |               34.69 |
| TPC-DS Q92    |              138.95 |              149.68 |              199.24 |              167.10 |              164.39 |
| TPC-DS Q93    |             1937.95 |             1958.77 |             2650.99 |             2017.23 |             5881.83 |
| TPC-DS Q94    |            40344.93 |            39050.91 |            58848.42 |            43032.19 |            82239.04 |
| TPC-DS Q95    |           154901.75 |           144690.75 |           846252.94 |           371377.03 |           774551.96 |
| TPC-DS Q96    |               34.71 |               35.19 |               40.28 |            22004.81 |             1232.27 |
| TPC-DS Q97    |             3038.02 |             3939.22 |             4022.85 |            24152.03 |             7738.19 |
| TPC-DS Q98    |              155.67 |              162.58 |              153.01 |            12873.86 |              706.29 |
| TPC-DS Q99    |              264.11 |              259.22 |              328.48 |             9354.10 |              898.75 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |      8934.28 |     90.22 |         854.20 |                854.21 |
| monetdb-1-1-2-1 |      7939.16 |    102.68 |         813.03 |                813.04 |
| monetdb-1-1-3-1 |     24374.84 |    121.34 |        1005.09 |               1024.00 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        30.96 |      0.31 |           0.38 |                  0.39 |
| monetdb-1-1-2-1 |        31.41 |      0.26 |           0.35 |                  0.36 |
| monetdb-1-1-3-1 |        88.25 |      1.02 |           0.79 |                  0.80 |

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
