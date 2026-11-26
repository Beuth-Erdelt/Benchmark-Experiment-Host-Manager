## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1144s 
* Code: 1795698644
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637000
  * datadisk:12121
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
    * code:1795698644
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637000
  * datadisk:12345
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
    * code:1795698644
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637000
  * datadisk:12345
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
    * code:1795698644
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637001
  * datadisk:10224
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
    * code:1795698644
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637002
  * datadisk:10398
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
    * code:1795698644
* monetdb-1-2-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:637002
  * datadisk:10398
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
    * code:1795698644

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1795698644-ff6465448-c5f4h: 0
* bexhoma-sut-monetdb-1-1795698644-7bc6bf6946-sr88d: 0

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

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MonetDB-1-1 |                1 |    3 |      365.00 |           2.00 |            1.00 |        295.00 |           56.00 |              8 |         0 |             | None           |             0 | False         |               29.59 | False               |
| MonetDB-1-2 |                2 |    3 |      365.00 |           2.00 |            1.00 |        295.00 |           56.00 |              8 |         0 |             | None           |             0 | False         |               29.59 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         34 |            0.09 |           117806.71 |          31447.06 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         32 |            0.09 |           119296.26 |          33412.50 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         33 |            0.09 |           125871.28 |          32400.00 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         64 |            0.11 |            94010.03 |          16706.25 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         49 |            0.08 |           137093.93 |          21820.41 |          -1 |
| monetdb-1-2-2-1-2 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         42 |            0.08 |           132371.56 |          25457.14 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         34 |            0.09 |           117806.71 |          31447.06 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         33 |            0.09 |           122539.68 |          64800.00 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         64 |            0.11 |            94010.03 |          16706.25 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         49 |            0.08 |           134712.05 |          43640.82 |          -1 |

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
| TPC-DS Q1     |              183.70 |               52.40 |              187.95 |              339.08 |               36.28 |              185.55 |
| TPC-DS Q2     |              152.28 |              250.88 |              112.42 |              557.37 |              116.15 |              133.47 |
| TPC-DS Q3     |               32.23 |               58.84 |               33.83 |              793.25 |               38.60 |               26.53 |
| TPC-DS Q4     |             1845.73 |             1298.96 |             1176.34 |             3115.71 |             1169.68 |             1210.02 |
| TPC-DS Q5     |              158.04 |              113.91 |              113.40 |             3098.89 |              120.26 |              107.90 |
| TPC-DS Q6     |               48.25 |               45.81 |               43.38 |              197.61 |               51.08 |               45.22 |
| TPC-DS Q7     |               51.25 |               58.29 |               47.99 |             1617.73 |               56.97 |               52.41 |
| TPC-DS Q8     |               43.49 |               39.60 |               36.49 |               53.48 |               45.88 |               31.45 |
| TPC-DS Q9     |              101.33 |              101.13 |              107.10 |              349.33 |              148.36 |              129.68 |
| TPC-DS Q10    |               27.87 |               28.04 |               36.99 |             5382.62 |               49.25 |               52.95 |
| TPC-DS Q11    |              660.29 |              533.21 |              570.13 |              630.92 |              674.98 |              660.82 |
| TPC-DS Q12    |               22.77 |               25.13 |               30.09 |               46.90 |               29.77 |               28.88 |
| TPC-DS Q13    |               71.71 |               67.64 |               88.25 |               92.16 |               94.74 |               90.73 |
| TPC-DS Q14a+b |             2746.04 |             2258.98 |             2763.90 |             2749.86 |             2172.73 |             2160.95 |
| TPC-DS Q15    |               23.85 |               53.89 |               35.25 |               34.63 |               28.79 |               24.55 |
| TPC-DS Q16    |              115.98 |              205.67 |              149.02 |              362.49 |              122.03 |              122.81 |
| TPC-DS Q17    |              165.43 |              283.18 |              172.42 |              468.69 |              172.28 |              158.59 |
| TPC-DS Q18    |              104.78 |              219.47 |              107.65 |              121.94 |               83.40 |              116.45 |
| TPC-DS Q19    |               54.02 |               84.23 |               49.63 |               58.20 |               61.48 |               59.69 |
| TPC-DS Q20    |               27.96 |               37.33 |               23.84 |               28.61 |               29.17 |               23.58 |
| TPC-DS Q21    |              105.11 |              120.47 |              116.67 |             2241.24 |               99.41 |              112.09 |
| TPC-DS Q22    |              935.29 |              929.38 |              970.07 |             1716.17 |              948.42 |              947.69 |
| TPC-DS Q23a+b |             3016.14 |             2545.62 |             2683.23 |             2618.61 |             3311.36 |             2639.02 |
| TPC-DS Q24a+b |              511.93 |              272.31 |              348.89 |              298.36 |              410.76 |              257.31 |
| TPC-DS Q25    |              311.70 |              185.32 |              187.51 |              190.01 |              191.71 |              193.95 |
| TPC-DS Q26    |               31.80 |               30.90 |               61.16 |               36.33 |               33.91 |               74.48 |
| TPC-DS Q27    |              193.54 |              153.78 |              205.69 |              187.25 |              148.04 |              500.38 |
| TPC-DS Q28    |               86.22 |               97.12 |              142.11 |               87.55 |               87.55 |              194.67 |
| TPC-DS Q29    |              201.40 |              211.51 |              329.28 |              173.77 |              167.37 |              372.62 |
| TPC-DS Q30    |               18.07 |               18.07 |               22.75 |               27.29 |               20.18 |               15.76 |
| TPC-DS Q31    |              169.38 |              421.85 |              344.88 |              163.89 |              154.83 |              131.37 |
| TPC-DS Q32    |               20.23 |               32.36 |               24.43 |               22.61 |               21.18 |               26.59 |
| TPC-DS Q33    |               40.70 |               46.44 |               29.21 |               32.26 |               28.03 |               36.27 |
| TPC-DS Q34    |               36.42 |               51.22 |               56.61 |               41.49 |               39.08 |               44.22 |
| TPC-DS Q35    |               88.97 |              203.90 |               79.48 |               94.12 |               85.32 |               75.59 |
| TPC-DS Q36    |              174.31 |              318.26 |              136.29 |              162.69 |              147.32 |              171.55 |
| TPC-DS Q37    |              138.42 |              139.10 |               79.10 |              136.44 |               78.43 |              105.62 |
| TPC-DS Q38    |              215.54 |              302.70 |              250.74 |              220.64 |              274.29 |              183.30 |
| TPC-DS Q39a+b |             1611.85 |              998.83 |             1012.83 |             1037.51 |              897.14 |              892.91 |
| TPC-DS Q40    |              148.26 |               88.57 |               89.41 |               37.57 |               36.51 |               37.62 |
| TPC-DS Q41    |                8.50 |               10.30 |                4.97 |                3.57 |               10.90 |                6.06 |
| TPC-DS Q42    |               30.77 |               38.05 |               27.64 |               28.64 |               28.45 |               30.71 |
| TPC-DS Q43    |               63.95 |               69.48 |               74.18 |               69.55 |               69.79 |               70.86 |
| TPC-DS Q44    |               48.98 |               49.11 |               52.10 |               49.07 |               48.52 |               49.32 |
| TPC-DS Q45    |               17.44 |               13.10 |               15.14 |               20.45 |               16.44 |               21.74 |
| TPC-DS Q46    |               54.44 |               55.15 |               97.22 |               60.92 |               62.86 |               67.81 |
| TPC-DS Q47    |              219.62 |              210.87 |              208.58 |              204.45 |              188.73 |              204.89 |
| TPC-DS Q48    |               52.26 |               59.53 |               54.30 |               58.03 |               56.69 |               53.08 |
| TPC-DS Q49    |              125.35 |              112.31 |              105.31 |              323.45 |              114.56 |              111.00 |
| TPC-DS Q50    |              131.75 |              148.99 |              165.40 |              153.73 |              135.22 |              144.30 |
| TPC-DS Q51    |              512.55 |              493.41 |              809.67 |              883.55 |              508.64 |              474.22 |
| TPC-DS Q52    |               34.16 |               40.33 |               48.54 |               31.58 |               29.94 |               25.95 |
| TPC-DS Q53    |               36.84 |               29.23 |               48.70 |               35.51 |               30.53 |               33.79 |
| TPC-DS Q54    |               90.57 |               30.00 |               55.87 |               27.36 |               29.71 |               31.87 |
| TPC-DS Q55    |               28.18 |               33.44 |               32.00 |               26.26 |               28.58 |               26.28 |
| TPC-DS Q56    |               47.94 |               27.52 |               51.08 |               57.90 |               31.21 |               30.14 |
| TPC-DS Q57    |              140.84 |               72.58 |               69.84 |               65.61 |              142.17 |               73.63 |
| TPC-DS Q58    |              133.31 |              166.67 |               44.30 |               83.16 |               76.79 |               44.36 |
| TPC-DS Q59    |              184.81 |              211.88 |              123.45 |              127.61 |              118.33 |              126.70 |
| TPC-DS Q60    |               28.43 |               51.09 |               33.68 |               27.19 |               32.20 |               25.73 |
| TPC-DS Q61    |               85.11 |              105.40 |               54.54 |               52.40 |               65.88 |               48.53 |
| TPC-DS Q62    |               34.17 |               34.22 |               33.39 |               32.79 |               28.59 |               27.53 |
| TPC-DS Q63    |               34.22 |               26.09 |               29.48 |               30.46 |               29.87 |               27.51 |
| TPC-DS Q64    |              445.78 |              313.34 |              295.02 |              475.25 |              298.81 |              313.24 |
| TPC-DS Q65    |              124.72 |              116.39 |              117.57 |              116.09 |              140.73 |              134.39 |
| TPC-DS Q66    |               46.85 |               47.18 |               55.52 |               46.26 |               38.49 |               56.92 |
| TPC-DS Q67    |              460.98 |              475.53 |              458.72 |              472.40 |              550.92 |              483.58 |
| TPC-DS Q68    |               70.87 |               84.69 |               86.10 |               61.03 |               63.87 |               74.07 |
| TPC-DS Q69    |               19.67 |               18.79 |               23.23 |               20.76 |               16.65 |               16.29 |
| TPC-DS Q70    |               93.72 |               85.90 |               69.20 |               89.99 |               69.74 |               97.47 |
| TPC-DS Q71    |               40.35 |               46.46 |               47.35 |               51.64 |               45.41 |               42.17 |
| TPC-DS Q72    |              211.61 |              189.66 |              206.65 |              295.70 |              187.80 |              194.34 |
| TPC-DS Q73    |               32.82 |               36.29 |               32.37 |               33.76 |               33.98 |               35.92 |
| TPC-DS Q74    |              178.34 |              169.10 |              166.10 |              143.86 |              175.77 |              155.51 |
| TPC-DS Q75    |              554.76 |              496.50 |              476.49 |              469.80 |              451.59 |             1230.08 |
| TPC-DS Q76    |               69.07 |               57.42 |               49.47 |              620.02 |               54.35 |              104.13 |
| TPC-DS Q77    |               88.72 |               81.25 |               92.38 |               82.09 |               85.70 |               88.69 |
| TPC-DS Q78    |              907.74 |              771.48 |              873.49 |              822.10 |              739.51 |              755.98 |
| TPC-DS Q79    |               60.33 |               73.02 |               67.49 |               56.38 |               62.31 |               67.58 |
| TPC-DS Q80    |              584.46 |              890.68 |             1291.91 |              520.94 |              608.33 |              553.76 |
| TPC-DS Q81    |               31.87 |               31.89 |               28.99 |               32.94 |               42.35 |               26.22 |
| TPC-DS Q82    |              333.53 |              109.77 |              100.66 |              164.13 |              128.96 |               77.40 |
| TPC-DS Q83    |               22.99 |               14.04 |                9.60 |               11.98 |               14.53 |               10.66 |
| TPC-DS Q84    |               53.46 |               19.77 |               10.04 |               37.70 |                9.24 |               10.08 |
| TPC-DS Q85    |               48.17 |               44.89 |               28.61 |               30.25 |               27.50 |               32.11 |
| TPC-DS Q86    |               50.55 |               25.55 |               28.00 |               26.02 |               24.14 |               25.40 |
| TPC-DS Q87    |              267.44 |              224.72 |              222.45 |              203.91 |              202.24 |              200.73 |
| TPC-DS Q88    |               89.05 |               83.05 |               92.73 |              147.24 |               87.53 |               94.89 |
| TPC-DS Q89    |               45.96 |               47.97 |               47.56 |               73.58 |               45.26 |               49.67 |
| TPC-DS Q90    |               10.72 |                9.60 |               11.11 |               15.92 |                8.43 |               10.08 |
| TPC-DS Q91    |               15.71 |               14.09 |               16.35 |               17.54 |               14.03 |               16.09 |
| TPC-DS Q92    |               20.43 |               19.63 |               15.82 |               18.78 |               12.44 |               16.41 |
| TPC-DS Q93    |              137.84 |              134.38 |              139.17 |              139.87 |              132.48 |              109.75 |
| TPC-DS Q94    |               36.06 |               32.14 |               31.36 |               32.14 |               28.21 |               29.35 |
| TPC-DS Q95    |              481.86 |              460.12 |              484.11 |              474.26 |              419.48 |              444.62 |
| TPC-DS Q96    |               15.84 |               20.49 |               20.15 |               14.11 |               13.34 |               12.53 |
| TPC-DS Q97    |              241.26 |              233.05 |              249.85 |              234.99 |              272.12 |              244.61 |
| TPC-DS Q98    |               47.34 |               52.29 |               43.67 |               41.60 |               46.65 |               46.25 |
| TPC-DS Q99    |               41.15 |               47.02 |               44.54 |               38.11 |               36.39 |               39.34 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       298.37 |      1.54 |           7.38 |                  8.38 |
| monetdb-1-1-2-1 |       298.37 |      1.54 |           7.38 |                  8.38 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        32.42 |      0.15 |           0.01 |                  2.65 |
| monetdb-1-1-2-1 |        32.42 |      0.15 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      3.98 |          15.73 |                 17.61 |
| monetdb-1-1-2-1 | n/a          |      2.74 |          19.25 |                 21.13 |
| monetdb-1-2-1-1 | 77.68        |     10.16 |           7.98 |                  7.98 |
| monetdb-1-2-2-1 | 239.50       |      7.88 |          13.97 |                 13.98 |

### Benchmarking phase: component benchmarker

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      0.00 |           0.28 |                  0.28 |
| monetdb-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-2-1-1 | 14.34        |      0.04 |           0.29 |                  0.29 |
| monetdb-1-2-2-1 | 28.56        |      1.17 |           0.31 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
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
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
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
