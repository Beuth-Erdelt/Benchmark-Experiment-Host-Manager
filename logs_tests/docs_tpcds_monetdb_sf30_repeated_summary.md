## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 3358s 
* Code: 1794675789
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
  * disk:1146783
  * datadisk:76869
  * volume_size:2.9T
  * volume_used:76G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:900Gi
  * limits_memory:1024Gi
  * resources_total: 4.0 CPU, 900.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 900.0 GiB RAM
  * eval_parameters
    * code:1794675789
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146788
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
    * code:1794675789
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1039860
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
    * code:1794675789
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1039856
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
    * code:1794675789

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MonetDB-1

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794675789-58f7d97bb7-lq6mv: 0
* bexhoma-sut-monetdb-1-1794675789-55d8dbd698-2d8md: 0

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
| MonetDB-1-1 |                1 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              0 |         0 |             | None           |             0 | False         |              109.98 | True                |
| MonetDB-1-2 |                2 |   30 |      982.00 |           4.00 |            1.00 |        444.00 |          505.00 |              0 |         0 |             | None           |             0 | False         |              109.98 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        741 |            0.91 |           122877.19 |          14429.15 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        696 |            0.78 |           143633.03 |          15362.07 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 30.00 |               99 |                  99 |        750 |            0.93 |           120342.74 |          14256.00 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 30.00 |               99 |                  99 |        675 |            0.75 |           147519.87 |          15840.00 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        741 |            0.91 |           122877.19 |          14429.15 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        696 |            0.78 |           143633.03 |          15362.07 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 30.00 |               99 |                  99 |        750 |            0.93 |           120342.74 |          14256.00 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           1 | 30.00 |               99 |                  99 |        675 |            0.75 |           147519.87 |          15840.00 |          -1 |

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
| TPC-DS Q1     |             1520.60 |              753.56 |             1498.16 |              467.91 |
| TPC-DS Q2     |             3758.46 |             1948.68 |             3625.04 |             1796.82 |
| TPC-DS Q3     |             2723.16 |              190.88 |             2702.49 |              168.81 |
| TPC-DS Q4     |            25845.06 |            17485.13 |            24105.61 |            16377.45 |
| TPC-DS Q5     |            20301.87 |             1981.75 |            20054.88 |             2173.60 |
| TPC-DS Q6     |              593.81 |              320.14 |              672.25 |              338.27 |
| TPC-DS Q7     |             5552.67 |             1309.56 |             5162.08 |             1084.75 |
| TPC-DS Q8     |             4158.76 |              747.99 |             4152.70 |              371.97 |
| TPC-DS Q9     |             1329.24 |              587.48 |             1303.79 |              583.94 |
| TPC-DS Q10    |            21608.31 |              537.24 |            21097.26 |              515.96 |
| TPC-DS Q11    |             6589.46 |             7585.14 |             6988.97 |             7153.09 |
| TPC-DS Q12    |              232.16 |              189.89 |              247.94 |              165.77 |
| TPC-DS Q13    |              442.69 |              617.10 |              435.04 |              535.71 |
| TPC-DS Q14a+b |            32312.80 |            35696.16 |            31237.11 |            31948.09 |
| TPC-DS Q15    |              177.01 |              138.96 |              191.14 |              129.15 |
| TPC-DS Q16    |            47067.28 |            45981.59 |            46951.03 |            41575.96 |
| TPC-DS Q17    |             3762.53 |             4215.28 |             3834.14 |             3391.36 |
| TPC-DS Q18    |             2237.21 |             2099.96 |             2123.51 |             2192.56 |
| TPC-DS Q19    |              155.34 |              179.92 |              189.81 |              200.37 |
| TPC-DS Q20    |              120.82 |               93.42 |              121.42 |              144.73 |
| TPC-DS Q21    |             2316.78 |              182.44 |             2421.56 |              172.18 |
| TPC-DS Q22    |             1858.85 |             2016.38 |             2041.51 |             1848.72 |
| TPC-DS Q23a+b |            49878.70 |            61993.02 |            56051.27 |            52383.81 |
| TPC-DS Q24a+b |            14649.21 |            16095.33 |            15127.94 |            16586.26 |
| TPC-DS Q25    |             1383.22 |             1846.37 |             1594.89 |             1491.38 |
| TPC-DS Q26    |              166.11 |              179.25 |              172.06 |              181.41 |
| TPC-DS Q27    |             1311.29 |             1450.39 |             1273.45 |             1628.09 |
| TPC-DS Q28    |              612.32 |              662.50 |              628.73 |              879.19 |
| TPC-DS Q29    |             2192.09 |             2940.10 |             2413.55 |             2308.50 |
| TPC-DS Q30    |              100.44 |              114.43 |              115.25 |              114.13 |
| TPC-DS Q31    |             2437.72 |             2371.13 |             2425.69 |             2493.08 |
| TPC-DS Q32    |              182.12 |              139.98 |              130.28 |              421.40 |
| TPC-DS Q33    |              132.50 |              231.94 |              140.73 |              149.80 |
| TPC-DS Q34    |              430.44 |              217.56 |              327.86 |              120.83 |
| TPC-DS Q35    |              791.92 |             1063.91 |              774.33 |             1446.14 |
| TPC-DS Q36    |             1414.32 |             1746.39 |             1592.88 |             1410.01 |
| TPC-DS Q37    |              448.33 |              680.75 |              430.21 |              436.51 |
| TPC-DS Q38    |             2413.78 |             2489.00 |             2584.69 |             2624.39 |
| TPC-DS Q39a+b |             1383.55 |             1409.20 |             1729.79 |             2159.44 |
| TPC-DS Q40    |              417.22 |             1016.85 |              423.98 |              593.51 |
| TPC-DS Q41    |                6.18 |                7.30 |                5.87 |                5.74 |
| TPC-DS Q42    |               93.76 |               68.73 |               88.41 |              112.35 |
| TPC-DS Q43    |              207.46 |              222.41 |              231.86 |              218.55 |
| TPC-DS Q44    |              352.07 |              403.62 |              401.81 |              372.29 |
| TPC-DS Q45    |              131.27 |              138.91 |              133.94 |              138.99 |
| TPC-DS Q46    |              213.27 |              220.86 |              211.85 |              195.68 |
| TPC-DS Q47    |             1240.86 |             1059.69 |              924.56 |              792.56 |
| TPC-DS Q48    |              214.24 |              225.53 |              393.13 |              213.18 |
| TPC-DS Q49    |             4444.50 |             1735.30 |             4520.38 |             1656.74 |
| TPC-DS Q50    |              582.90 |              593.52 |              600.44 |              580.73 |
| TPC-DS Q51    |             2371.52 |             2831.48 |             2547.56 |             2361.98 |
| TPC-DS Q52    |              102.92 |               73.35 |              123.79 |              109.33 |
| TPC-DS Q53    |               98.40 |               93.31 |               88.69 |              229.27 |
| TPC-DS Q54    |               97.63 |               92.47 |               91.61 |               98.68 |
| TPC-DS Q55    |               81.08 |               68.87 |               86.46 |               81.52 |
| TPC-DS Q56    |              217.54 |              111.89 |              150.64 |              152.10 |
| TPC-DS Q57    |              152.03 |              152.60 |              157.61 |              148.39 |
| TPC-DS Q58    |              542.38 |              558.01 |              639.17 |              555.10 |
| TPC-DS Q59    |             1183.12 |             1248.98 |             1208.45 |             1137.45 |
| TPC-DS Q60    |              221.05 |              254.75 |              294.42 |              181.26 |
| TPC-DS Q61    |              205.72 |              172.19 |              170.73 |              163.86 |
| TPC-DS Q62    |              441.41 |              449.45 |              446.59 |              448.58 |
| TPC-DS Q63    |              105.12 |               85.83 |              116.65 |               95.20 |
| TPC-DS Q64    |             5170.89 |             5102.78 |             5372.41 |             5114.38 |
| TPC-DS Q65    |             1089.41 |             1125.06 |             1204.28 |             1043.89 |
| TPC-DS Q66    |             1036.22 |             1085.61 |             1073.02 |             1061.04 |
| TPC-DS Q67    |             5712.38 |             6107.77 |             6251.74 |             5468.87 |
| TPC-DS Q68    |              254.93 |              212.22 |              200.91 |              225.53 |
| TPC-DS Q69    |              461.56 |              371.55 |              543.80 |              421.79 |
| TPC-DS Q70    |             2122.33 |             1439.39 |             1626.18 |             1554.81 |
| TPC-DS Q71    |              372.23 |              537.98 |              337.75 |              493.50 |
| TPC-DS Q72    |             2346.87 |             2464.61 |             2382.61 |             2777.02 |
| TPC-DS Q73    |              103.16 |              171.76 |               87.80 |               95.35 |
| TPC-DS Q74    |             7558.86 |             8550.53 |             7605.52 |             7501.90 |
| TPC-DS Q75    |             6737.16 |             7615.59 |             7033.98 |             6548.43 |
| TPC-DS Q76    |             6326.69 |             7838.32 |             8260.98 |             6575.71 |
| TPC-DS Q77    |             1394.09 |             1281.33 |             1226.03 |             1566.90 |
| TPC-DS Q78    |            13276.33 |            13835.36 |            12753.75 |            14010.89 |
| TPC-DS Q79    |              265.66 |              295.49 |              259.84 |              289.90 |
| TPC-DS Q80    |             7541.55 |             7740.58 |             7504.16 |             7849.43 |
| TPC-DS Q81    |              155.97 |              156.98 |              159.04 |              155.56 |
| TPC-DS Q82    |              462.88 |              455.52 |              490.10 |              455.57 |
| TPC-DS Q83    |              288.23 |              278.88 |              285.50 |              201.57 |
| TPC-DS Q84    |               58.34 |               61.31 |               52.46 |               47.86 |
| TPC-DS Q85    |              303.12 |              299.01 |              695.28 |              314.54 |
| TPC-DS Q86    |              329.24 |              317.55 |              313.71 |              313.37 |
| TPC-DS Q87    |             2738.01 |             3330.32 |             2996.22 |             2718.96 |
| TPC-DS Q88    |              706.70 |              426.35 |              652.17 |              578.13 |
| TPC-DS Q89    |              137.03 |              151.43 |              129.41 |              173.22 |
| TPC-DS Q90    |               81.87 |              121.48 |               81.53 |              135.53 |
| TPC-DS Q91    |               38.84 |               45.03 |               35.73 |               39.28 |
| TPC-DS Q92    |              144.41 |              116.30 |              149.41 |              162.65 |
| TPC-DS Q93    |             1937.97 |             2261.58 |             2154.32 |             1902.04 |
| TPC-DS Q94    |            38996.86 |            40529.56 |            40799.57 |            40739.16 |
| TPC-DS Q95    |           322376.48 |           316144.33 |           322758.33 |           325531.95 |
| TPC-DS Q96    |              810.56 |              753.61 |              749.64 |              794.59 |
| TPC-DS Q97    |             3951.48 |             4109.38 |             4430.46 |             4210.38 |
| TPC-DS Q98    |              469.63 |              472.74 |              482.24 |              476.22 |
| TPC-DS Q99    |              399.97 |              552.01 |              394.35 |              405.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |     11291.41 |    166.87 |        1011.30 |               1023.68 |
| monetdb-1-1-2-1 |     10819.98 |    112.99 |         996.47 |               1023.95 |
| monetdb-1-2-1-1 |     10588.06 |    148.43 |         959.05 |               1023.97 |
| monetdb-1-2-2-1 |     10924.01 |    149.65 |         977.58 |               1023.99 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        31.82 |      0.18 |           0.36 |                  0.36 |
| monetdb-1-1-2-1 |        33.89 |      0.15 |           0.37 |                  0.38 |
| monetdb-1-2-1-1 |        34.05 |      0.46 |           0.38 |                  0.38 |
| monetdb-1-2-2-1 |        32.99 |      0.54 |           0.40 |                  0.40 |

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
