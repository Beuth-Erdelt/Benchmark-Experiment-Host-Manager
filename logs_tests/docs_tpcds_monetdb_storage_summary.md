## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1181s 
* Code: 1793948768
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
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
  * disk:838033
  * datadisk:12125
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793948768
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838925
  * datadisk:12346
  * volume_size:49G
  * volume_used:13G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793948768
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838925
  * datadisk:12346
  * volume_size:49G
  * volume_used:13G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793948768
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:842663
  * datadisk:10225
  * volume_size:49G
  * volume_used:10G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793948768
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845256
  * datadisk:10400
  * volume_size:49G
  * volume_used:11G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793948768
* monetdb-1-2-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:845256
  * datadisk:10400
  * volume_size:49G
  * volume_used:11G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793948768

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1793948768-6fb867fd84-xd8p5: 0
* bexhoma-sut-monetdb-1-1793948768-84dcddbcf-mnlzc: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      416.00 |           5.00 |            1.00 |        345.00 |           56.00 |              8 |           0 |             | None           |             0 | False         |               25.96 | False               |
| MonetDB-1-2 |                2 |    3 |      416.00 |           5.00 |            1.00 |        345.00 |           56.00 |              8 |           0 |             | None           |             0 | False         |               25.96 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| monetdb-1-1-1-1-1 | MonetDB-1       | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         39 |            0.09 |           121568.58 |          27415.38 |          -1 | monetdb-1-1-1-1-1 |
| monetdb-1-1-2-1-1 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               99 |                  99 |         51 |            0.09 |           121251.98 |          20964.71 |          -1 | monetdb-1-1-2-1-1 |
| monetdb-1-1-2-1-2 | MonetDB-1       | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               99 |                  99 |         54 |            0.09 |           122596.54 |          19800.00 |          -1 | monetdb-1-1-2-1-2 |
| monetdb-1-2-1-1-1 | MonetDB-1       | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         57 |            0.11 |            96131.64 |          18757.89 |          -1 | monetdb-1-2-1-1-1 |
| monetdb-1-2-2-1-1 | MonetDB-1       | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               99 |                  99 |         34 |            0.08 |           129330.27 |          31447.06 |          -1 | monetdb-1-2-2-1-1 |
| monetdb-1-2-2-1-2 | MonetDB-1       | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               99 |                  99 |         35 |            0.08 |           127182.32 |          30548.57 |          -1 | monetdb-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         39 |            0.09 |           121568.58 |          27415.38 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         54 |            0.09 |           121922.40 |          39600.00 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         57 |            0.11 |            96131.64 |          18757.89 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         35 |            0.08 |           128251.80 |          61097.14 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| monetdb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |
| monetdb-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-2-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   monetdb-1-1-1-1-1 |   monetdb-1-1-2-1-1 |   monetdb-1-1-2-1-2 |   monetdb-1-2-1-1-1 |   monetdb-1-2-2-1-1 |   monetdb-1-2-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               37.99 |               37.81 |               36.74 |              167.00 |               36.13 |               37.47 |
| TPC-DS Q2     |              205.57 |              111.20 |              109.98 |              595.91 |              103.44 |              120.87 |
| TPC-DS Q3     |               42.82 |               58.82 |               41.16 |              848.59 |               45.03 |               53.82 |
| TPC-DS Q4     |             1317.15 |             1239.77 |             1473.43 |             3118.19 |             1123.17 |             1140.00 |
| TPC-DS Q5     |              143.14 |              249.15 |              180.27 |             2822.93 |              129.11 |              120.88 |
| TPC-DS Q6     |               56.49 |               68.87 |               65.12 |               73.43 |               47.96 |               50.08 |
| TPC-DS Q7     |               53.19 |               73.93 |               74.42 |             1692.13 |               50.84 |               73.61 |
| TPC-DS Q8     |               39.82 |               36.31 |               37.09 |               49.17 |               36.32 |               35.41 |
| TPC-DS Q9     |              134.25 |              142.97 |              142.81 |               98.87 |              104.33 |              106.64 |
| TPC-DS Q10    |               28.82 |               32.49 |               28.12 |             5469.60 |               38.32 |               25.12 |
| TPC-DS Q11    |              503.55 |              517.06 |              500.25 |              758.30 |              549.04 |              532.17 |
| TPC-DS Q12    |               29.26 |               24.24 |               23.19 |               43.53 |               30.74 |               28.86 |
| TPC-DS Q13    |               77.33 |               70.96 |               78.71 |               88.19 |               86.19 |               68.73 |
| TPC-DS Q14a+b |             2350.86 |             2707.34 |             2546.45 |             2455.66 |             2295.49 |             2824.02 |
| TPC-DS Q15    |               29.00 |               21.26 |               26.09 |               20.07 |               31.57 |               32.74 |
| TPC-DS Q16    |              140.96 |              210.69 |              180.60 |              301.99 |              188.30 |              123.90 |
| TPC-DS Q17    |              314.01 |              159.00 |              173.10 |              242.40 |              270.61 |              164.42 |
| TPC-DS Q18    |              107.94 |               89.31 |              109.21 |              116.66 |               88.17 |               96.47 |
| TPC-DS Q19    |              139.85 |               83.30 |               85.89 |               61.48 |               62.03 |               56.03 |
| TPC-DS Q20    |               30.26 |               28.34 |               33.43 |               34.35 |               24.06 |               29.78 |
| TPC-DS Q21    |              118.10 |              146.84 |              167.20 |             2319.98 |              102.58 |              115.85 |
| TPC-DS Q22    |             1058.51 |             1024.19 |             1004.76 |             1679.80 |              986.08 |              976.19 |
| TPC-DS Q23a+b |             2804.84 |             3417.90 |             3432.31 |             2527.19 |             2449.41 |             2512.69 |
| TPC-DS Q24a+b |              269.34 |              373.11 |              363.18 |              297.94 |              264.99 |              286.19 |
| TPC-DS Q25    |              204.70 |              247.15 |              214.43 |              188.27 |              183.91 |              188.85 |
| TPC-DS Q26    |               30.63 |               48.84 |               53.42 |               27.50 |               31.19 |               32.93 |
| TPC-DS Q27    |              403.73 |              147.77 |              159.19 |              150.17 |              171.21 |              158.80 |
| TPC-DS Q28    |              104.64 |              114.33 |              114.93 |               81.48 |               85.77 |              116.37 |
| TPC-DS Q29    |              192.58 |              380.13 |              417.50 |              176.80 |              170.25 |              173.84 |
| TPC-DS Q30    |               14.20 |               21.66 |               23.02 |               22.55 |               14.50 |               12.77 |
| TPC-DS Q31    |              158.28 |              157.74 |              163.45 |              150.57 |              158.15 |              153.36 |
| TPC-DS Q32    |               31.96 |               34.85 |               24.83 |               38.39 |               24.83 |               35.55 |
| TPC-DS Q33    |               27.82 |               36.30 |               29.16 |               30.90 |               36.72 |               39.25 |
| TPC-DS Q34    |               45.17 |               37.59 |               34.89 |               40.85 |               40.18 |               39.44 |
| TPC-DS Q35    |               84.71 |               75.54 |               74.62 |               93.76 |               80.66 |               94.99 |
| TPC-DS Q36    |              214.85 |              155.65 |              140.27 |              165.37 |              157.45 |              143.21 |
| TPC-DS Q37    |              122.36 |              110.66 |               95.71 |               77.09 |              103.15 |               76.15 |
| TPC-DS Q38    |              434.27 |              224.09 |              219.29 |              185.71 |              204.62 |              209.73 |
| TPC-DS Q39a+b |             1153.16 |             1194.59 |             1182.03 |             1082.10 |             1095.23 |             1050.84 |
| TPC-DS Q40    |               84.84 |               75.97 |               99.42 |               42.23 |               35.62 |               37.10 |
| TPC-DS Q41    |                5.89 |                6.11 |                6.50 |                4.61 |                6.12 |                4.88 |
| TPC-DS Q42    |               31.65 |               34.07 |               44.32 |               30.66 |               32.26 |               31.99 |
| TPC-DS Q43    |              117.62 |               92.59 |               73.77 |               67.52 |               72.44 |               74.14 |
| TPC-DS Q44    |               81.28 |               47.96 |               69.33 |               48.56 |               51.61 |               53.33 |
| TPC-DS Q45    |               15.42 |               23.60 |               14.72 |               22.57 |               17.44 |               20.72 |
| TPC-DS Q46    |               61.25 |               56.18 |               63.76 |               74.56 |               56.19 |               54.42 |
| TPC-DS Q47    |              228.73 |              220.82 |              209.53 |              210.74 |              215.67 |              217.17 |
| TPC-DS Q48    |               51.30 |               48.81 |               55.19 |               66.89 |               50.64 |               47.72 |
| TPC-DS Q49    |              126.16 |              130.47 |              116.35 |              376.44 |              102.38 |              112.24 |
| TPC-DS Q50    |              138.96 |              135.38 |              152.06 |              143.12 |              229.32 |              222.32 |
| TPC-DS Q51    |              470.90 |              463.03 |              739.46 |              431.43 |              461.35 |              449.38 |
| TPC-DS Q52    |               34.93 |               38.41 |               35.17 |               41.62 |               61.34 |               50.90 |
| TPC-DS Q53    |               36.96 |               28.98 |               32.36 |               38.54 |               28.65 |               29.56 |
| TPC-DS Q54    |               28.41 |               41.91 |               38.64 |               26.78 |               32.40 |               33.19 |
| TPC-DS Q55    |               28.29 |               30.22 |               28.65 |               26.17 |               29.73 |               29.93 |
| TPC-DS Q56    |               26.03 |               40.94 |               31.23 |               35.46 |               29.17 |               26.63 |
| TPC-DS Q57    |               62.33 |               67.71 |               68.99 |               68.39 |               59.01 |               62.85 |
| TPC-DS Q58    |              138.19 |               72.86 |               47.07 |               41.38 |               73.34 |               40.11 |
| TPC-DS Q59    |              187.63 |              139.10 |              124.54 |              115.78 |              129.83 |              203.75 |
| TPC-DS Q60    |               39.96 |               31.28 |               33.82 |               30.96 |               39.40 |               30.11 |
| TPC-DS Q61    |               48.68 |               50.05 |               54.93 |               51.76 |               48.17 |               52.00 |
| TPC-DS Q62    |               30.95 |               38.41 |               30.08 |               41.49 |               43.23 |               52.21 |
| TPC-DS Q63    |               34.89 |               36.04 |               28.61 |               32.18 |               36.11 |               33.08 |
| TPC-DS Q64    |              454.00 |              384.85 |              337.36 |              436.89 |              466.86 |              584.00 |
| TPC-DS Q65    |              136.87 |              121.29 |              124.67 |              157.32 |              290.99 |              282.22 |
| TPC-DS Q66    |               39.15 |               40.54 |               36.62 |               57.59 |               57.85 |               58.13 |
| TPC-DS Q67    |              501.06 |              426.70 |             1065.14 |              462.58 |              508.80 |              456.78 |
| TPC-DS Q68    |               65.31 |               71.07 |               73.54 |               68.83 |               85.26 |               91.53 |
| TPC-DS Q69    |               34.10 |               33.13 |               33.05 |               57.23 |               37.92 |               28.52 |
| TPC-DS Q70    |               78.00 |               75.14 |               85.84 |               99.45 |               71.47 |               69.48 |
| TPC-DS Q71    |               36.31 |               72.02 |               47.18 |               44.21 |               44.94 |               37.58 |
| TPC-DS Q72    |              377.45 |              360.57 |              208.61 |              266.96 |              275.28 |              275.31 |
| TPC-DS Q73    |               33.86 |               46.18 |               48.45 |               35.27 |               83.68 |               79.84 |
| TPC-DS Q74    |              588.26 |              606.95 |              552.70 |              540.18 |              533.73 |              537.80 |
| TPC-DS Q75    |              494.79 |              459.88 |              460.44 |              473.94 |              441.81 |              476.17 |
| TPC-DS Q76    |               66.39 |               62.18 |               56.24 |              642.49 |               76.31 |               60.18 |
| TPC-DS Q77    |              102.41 |              108.51 |               92.65 |               90.57 |               96.09 |               97.36 |
| TPC-DS Q78    |              985.26 |              833.10 |             1032.54 |              802.77 |              782.95 |              845.56 |
| TPC-DS Q79    |               54.02 |               68.29 |              103.44 |               58.15 |               79.13 |               65.17 |
| TPC-DS Q80    |              578.04 |              524.72 |              650.84 |              566.66 |              535.30 |              506.40 |
| TPC-DS Q81    |               25.90 |               29.24 |               23.32 |               31.06 |               29.32 |               27.88 |
| TPC-DS Q82    |              186.94 |               71.36 |               69.76 |              176.17 |               64.22 |               92.72 |
| TPC-DS Q83    |               10.93 |                8.96 |               10.39 |               12.95 |                8.75 |               15.50 |
| TPC-DS Q84    |               41.03 |                9.82 |               12.45 |               40.44 |                9.17 |               12.39 |
| TPC-DS Q85    |               29.30 |               43.83 |               32.56 |               32.41 |               27.99 |               34.63 |
| TPC-DS Q86    |               31.19 |               50.48 |               30.63 |               32.34 |               33.17 |               26.96 |
| TPC-DS Q87    |              209.99 |              354.34 |              508.56 |              201.29 |              191.23 |              200.52 |
| TPC-DS Q88    |               88.84 |              151.10 |              143.67 |               83.77 |              105.00 |               96.94 |
| TPC-DS Q89    |               46.34 |               48.66 |               59.93 |               44.19 |               50.22 |               52.87 |
| TPC-DS Q90    |                9.04 |               10.55 |               11.49 |               12.53 |               15.16 |               11.74 |
| TPC-DS Q91    |               16.65 |               19.79 |               22.95 |               17.14 |               21.22 |               17.04 |
| TPC-DS Q92    |               14.47 |               11.99 |               16.30 |               14.82 |               14.44 |               20.30 |
| TPC-DS Q93    |              140.60 |              126.30 |              130.31 |              146.19 |              105.62 |              116.95 |
| TPC-DS Q94    |               27.86 |               29.91 |               30.41 |               39.60 |               31.12 |               34.34 |
| TPC-DS Q95    |              446.83 |              530.42 |              433.20 |              433.88 |              458.36 |              427.35 |
| TPC-DS Q96    |               17.40 |               19.65 |               12.88 |               12.05 |               16.90 |               25.36 |
| TPC-DS Q97    |              232.47 |              406.65 |              222.70 |              234.22 |              227.85 |              451.57 |
| TPC-DS Q98    |               51.75 |               46.25 |               64.77 |              156.63 |               48.48 |               62.07 |
| TPC-DS Q99    |               35.32 |               39.81 |               41.22 |               43.71 |               49.39 |               57.92 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       307.72 |      1.03 |           5.91 |                  7.86 |
| monetdb-1-1-2-1 |       307.72 |      1.03 |           5.91 |                  7.86 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        40.79 |      0.17 |           0.01 |                  2.65 |
| monetdb-1-1-2-1 |        40.79 |      0.17 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        33.61 |      1.00 |          13.53 |                 15.41 |
| monetdb-1-1-2-1 |       298.67 |      6.17 |          20.27 |                 22.15 |
| monetdb-1-2-1-1 |        97.81 |      9.62 |           8.27 |                  8.28 |
| monetdb-1-2-2-1 |       167.03 |      6.00 |          13.55 |                 13.56 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        13.58 |      0.50 |           0.31 |                  0.32 |
| monetdb-1-1-2-1 |        28.48 |      0.86 |           0.31 |                  0.31 |
| monetdb-1-2-1-1 |        11.66 |      0.42 |           0.27 |                  0.28 |
| monetdb-1-2-2-1 |        27.04 |      1.35 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
