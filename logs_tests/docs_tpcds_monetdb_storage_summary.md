## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1218s 
* Code: 1794672202
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1146791
  * datadisk:12126
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
    * code:1794672202
* monetdb-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146792
  * datadisk:12347
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
    * code:1794672202
* monetdb-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146792
  * datadisk:12347
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
    * code:1794672202
* monetdb-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146788
  * datadisk:10226
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
    * code:1794672202
* monetdb-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146789
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
    * code:1794672202
* monetdb-1-2-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1146789
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
    * code:1794672202

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MonetDB-1-2

### Data Parameters of Reused Volumes
* MonetDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MonetDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1794672202-56b9b78596-wqsql: 0
* bexhoma-sut-monetdb-1-1794672202-669b88d7f4-wmvng: 0

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
| MonetDB-1-1 |                1 |    3 |      394.00 |           5.00 |            1.00 |        316.00 |           64.00 |              8 |         0 |             | None           |             0 | False         |               27.41 | False               |
| MonetDB-1-2 |                2 |    3 |      394.00 |           5.00 |            1.00 |        316.00 |           64.00 |              8 |         0 |             | None           |             0 | False         |               27.41 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1-1-1 | monetdb-1-1-1 | monetdb-1-1-1-1 |                1 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         29 |            0.09 |           125508.57 |          36868.97 |          -1 |
| monetdb-1-1-2-1-1 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         27 |            0.09 |           124088.29 |          39600.00 |          -1 |
| monetdb-1-1-2-1-2 | monetdb-1-1-2 | monetdb-1-1-2-1 |                1 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         32 |            0.08 |           130495.46 |          33412.50 |          -1 |
| monetdb-1-2-1-1-1 | monetdb-1-2-1 | monetdb-1-2-1-1 |                2 |        1 |               1 |       1 | 3.00 |               99 |                  99 |         56 |            0.12 |            89607.54 |          19092.86 |          -1 |
| monetdb-1-2-2-1-1 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       1 | 3.00 |               99 |                  99 |         28 |            0.09 |           124310.61 |          38185.71 |          -1 |
| monetdb-1-2-2-1-2 | monetdb-1-2-2 | monetdb-1-2-2-1 |                2 |        2 |               1 |       2 | 3.00 |               99 |                  99 |         28 |            0.09 |           123857.20 |          38185.71 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| monetdb-1-1-1 | monetdb-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         29 |            0.09 |           125508.57 |          36868.97 |          -1 |
| monetdb-1-1-2 | monetdb-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         32 |            0.08 |           127251.55 |          66825.00 |          -1 |
| monetdb-1-2-1 | monetdb-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               99 |                  99 |         56 |            0.12 |            89607.54 |          19092.86 |          -1 |
| monetdb-1-2-2 | monetdb-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |              198 |                 198 |         28 |            0.09 |           124083.70 |          76371.43 |          -1 |

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
| TPC-DS Q1     |               37.18 |               35.10 |               35.81 |              161.19 |               48.72 |               33.27 |
| TPC-DS Q2     |              258.10 |              145.74 |              123.75 |              619.32 |              104.12 |              126.34 |
| TPC-DS Q3     |               32.55 |               31.93 |               35.88 |              875.35 |               35.42 |               28.13 |
| TPC-DS Q4     |             1224.83 |             1688.29 |             1362.29 |             3099.13 |             1200.90 |             1245.69 |
| TPC-DS Q5     |              139.81 |              217.89 |              251.91 |             2771.03 |              116.09 |              128.96 |
| TPC-DS Q6     |              121.49 |               47.58 |               84.30 |               63.71 |               48.08 |               49.65 |
| TPC-DS Q7     |               76.55 |               57.89 |               62.35 |             1675.95 |               52.23 |               71.11 |
| TPC-DS Q8     |               41.08 |               31.31 |               33.07 |               46.41 |               35.99 |               34.59 |
| TPC-DS Q9     |              104.84 |              112.49 |              124.89 |              367.18 |              104.02 |              111.95 |
| TPC-DS Q10    |               27.95 |               33.86 |               22.83 |             5344.10 |               43.05 |               26.65 |
| TPC-DS Q11    |              545.52 |              530.23 |              546.47 |              531.64 |              619.61 |              577.55 |
| TPC-DS Q12    |               26.17 |               20.98 |               17.05 |               53.79 |               19.32 |               18.09 |
| TPC-DS Q13    |               71.66 |               70.43 |               71.96 |               93.10 |               87.52 |               80.18 |
| TPC-DS Q14a+b |             2781.14 |             2435.95 |             2227.78 |             2625.35 |             2862.70 |             2739.44 |
| TPC-DS Q15    |               22.57 |               23.19 |               24.07 |               24.56 |               36.06 |               24.23 |
| TPC-DS Q16    |              124.36 |              132.40 |              125.88 |              286.75 |              209.05 |              153.19 |
| TPC-DS Q17    |              182.06 |              164.91 |              150.09 |              230.30 |              173.11 |              231.44 |
| TPC-DS Q18    |              105.37 |               80.72 |               78.04 |              106.06 |              101.72 |               90.04 |
| TPC-DS Q19    |               61.06 |               53.23 |               50.64 |               62.00 |               68.81 |               56.21 |
| TPC-DS Q20    |               24.21 |               23.74 |               21.50 |               31.02 |               24.69 |               24.61 |
| TPC-DS Q21    |              128.07 |              123.08 |              119.31 |             2287.06 |              118.20 |              115.68 |
| TPC-DS Q22    |             1000.68 |             1120.40 |             1291.85 |             1642.42 |             1153.87 |             1186.29 |
| TPC-DS Q23a+b |             3183.20 |             3355.05 |             3242.71 |             2642.15 |             3073.66 |             3500.54 |
| TPC-DS Q24a+b |              275.38 |              549.21 |              301.41 |              299.92 |              277.20 |              569.81 |
| TPC-DS Q25    |              209.13 |              191.69 |              202.67 |              193.70 |              190.62 |              219.82 |
| TPC-DS Q26    |               32.95 |               33.56 |               33.81 |               31.77 |               34.10 |               29.63 |
| TPC-DS Q27    |              225.41 |              170.25 |              153.19 |              175.88 |              228.26 |              185.36 |
| TPC-DS Q28    |              106.82 |              105.53 |               96.26 |               86.91 |              163.19 |               98.35 |
| TPC-DS Q29    |              195.85 |              211.58 |              170.73 |              181.10 |              417.33 |              182.42 |
| TPC-DS Q30    |               17.30 |               21.57 |               16.05 |               31.99 |               21.13 |               13.90 |
| TPC-DS Q31    |              330.84 |              205.17 |              143.34 |              185.59 |              305.61 |              176.48 |
| TPC-DS Q32    |               27.12 |               40.02 |               27.59 |               24.71 |               25.11 |               28.08 |
| TPC-DS Q33    |               47.08 |               37.36 |               29.71 |               34.55 |               29.35 |               30.72 |
| TPC-DS Q34    |               38.34 |               38.91 |               37.27 |               39.58 |               37.78 |               39.91 |
| TPC-DS Q35    |               74.98 |               84.41 |               82.10 |              100.45 |               84.19 |               97.29 |
| TPC-DS Q36    |              148.99 |              156.55 |              129.00 |              148.95 |              181.33 |              138.12 |
| TPC-DS Q37    |              131.53 |               81.29 |               72.81 |              173.16 |               66.26 |               65.39 |
| TPC-DS Q38    |              221.97 |              200.26 |              183.82 |              214.36 |              210.50 |              239.55 |
| TPC-DS Q39a+b |             1236.25 |             1151.81 |             1574.89 |             1251.28 |             1210.00 |             1277.11 |
| TPC-DS Q40    |               80.19 |               84.13 |               90.34 |               40.32 |               34.61 |               38.13 |
| TPC-DS Q41    |                4.26 |                8.96 |                5.08 |                6.72 |                7.53 |               10.47 |
| TPC-DS Q42    |               28.19 |               44.82 |               34.32 |               33.77 |               26.28 |               40.14 |
| TPC-DS Q43    |               88.02 |              115.62 |               90.71 |               74.59 |               68.62 |              105.06 |
| TPC-DS Q44    |               89.09 |              151.49 |               85.36 |              713.01 |               86.19 |              174.81 |
| TPC-DS Q45    |               15.84 |               18.56 |               19.56 |               14.77 |               14.84 |               19.64 |
| TPC-DS Q46    |               58.79 |               94.28 |               56.19 |               70.02 |               53.80 |              109.87 |
| TPC-DS Q47    |              179.05 |              260.14 |              183.41 |              192.46 |              406.57 |              369.04 |
| TPC-DS Q48    |               48.16 |               50.46 |               66.88 |               48.30 |               95.63 |               55.75 |
| TPC-DS Q49    |              201.47 |              145.30 |              111.36 |              323.06 |              236.67 |              108.20 |
| TPC-DS Q50    |              198.04 |              142.76 |              141.78 |              146.73 |              217.63 |              151.50 |
| TPC-DS Q51    |              438.04 |              484.35 |              566.46 |              475.78 |              491.37 |              580.12 |
| TPC-DS Q52    |               32.58 |               43.45 |               42.78 |               37.74 |               37.74 |               28.23 |
| TPC-DS Q53    |               35.08 |               26.01 |               43.37 |               35.15 |               28.82 |               34.18 |
| TPC-DS Q54    |               29.34 |               26.96 |               30.53 |               27.33 |               30.42 |               36.34 |
| TPC-DS Q55    |               28.92 |               27.22 |               43.04 |               23.46 |               26.30 |               26.55 |
| TPC-DS Q56    |               30.51 |               25.88 |               33.28 |               50.30 |               28.24 |               29.18 |
| TPC-DS Q57    |               68.73 |               73.46 |               76.41 |               70.49 |               82.99 |               77.11 |
| TPC-DS Q58    |               74.45 |               46.39 |               70.92 |               62.73 |               55.94 |               39.31 |
| TPC-DS Q59    |              123.19 |              140.32 |              139.29 |              128.96 |              134.56 |              127.51 |
| TPC-DS Q60    |               31.32 |               30.77 |               31.16 |               30.46 |               27.01 |               31.04 |
| TPC-DS Q61    |               54.89 |               60.39 |               53.72 |               54.66 |               61.56 |               58.15 |
| TPC-DS Q62    |               30.08 |               26.54 |               26.35 |               30.44 |               32.12 |               27.72 |
| TPC-DS Q63    |               31.51 |               36.92 |               26.46 |               34.79 |               53.89 |               42.71 |
| TPC-DS Q64    |              442.37 |              326.04 |              317.33 |              425.19 |              338.63 |              499.09 |
| TPC-DS Q65    |              134.96 |              116.01 |              139.48 |              135.69 |              304.11 |              129.26 |
| TPC-DS Q66    |               41.69 |               40.61 |               38.54 |               50.58 |               57.55 |               41.40 |
| TPC-DS Q67    |              523.41 |              558.37 |              502.10 |              481.10 |              476.01 |              519.11 |
| TPC-DS Q68    |               69.28 |               95.16 |               71.13 |               69.64 |               59.95 |               78.31 |
| TPC-DS Q69    |               33.57 |               49.22 |               37.49 |               40.76 |               32.31 |               33.10 |
| TPC-DS Q70    |               79.94 |               77.78 |               83.09 |              171.94 |               94.97 |               76.02 |
| TPC-DS Q71    |               37.75 |               41.77 |               37.62 |               68.29 |               41.30 |               41.63 |
| TPC-DS Q72    |              222.96 |              215.50 |              196.42 |              456.50 |              222.00 |              218.95 |
| TPC-DS Q73    |               39.20 |               57.56 |               60.51 |               48.08 |               31.48 |               42.38 |
| TPC-DS Q74    |              158.73 |              150.56 |              354.10 |              297.57 |              154.46 |              170.80 |
| TPC-DS Q75    |              512.72 |              474.20 |              751.81 |              659.65 |              565.25 |              612.98 |
| TPC-DS Q76    |               58.64 |               64.92 |               60.56 |              683.78 |               59.82 |               54.01 |
| TPC-DS Q77    |              160.23 |               90.61 |              154.03 |               92.54 |               88.08 |               91.38 |
| TPC-DS Q78    |              862.31 |              795.43 |              813.15 |              934.29 |             1131.68 |             1133.20 |
| TPC-DS Q79    |               61.87 |               60.14 |               58.32 |               61.28 |              104.83 |               71.08 |
| TPC-DS Q80    |              533.03 |              548.80 |              503.30 |              541.89 |              684.53 |              616.25 |
| TPC-DS Q81    |               25.03 |               41.05 |               15.06 |               27.45 |               21.63 |               17.21 |
| TPC-DS Q82    |              173.51 |              146.44 |               99.01 |              191.57 |               98.00 |               90.91 |
| TPC-DS Q83    |                9.98 |               11.99 |                9.40 |               14.30 |               10.13 |               13.38 |
| TPC-DS Q84    |               50.76 |                9.33 |                8.73 |               45.22 |                9.79 |                9.72 |
| TPC-DS Q85    |               53.37 |               37.30 |               43.42 |               33.44 |               29.19 |               34.16 |
| TPC-DS Q86    |               29.28 |               40.94 |               91.70 |               36.32 |               22.03 |               31.32 |
| TPC-DS Q87    |              237.90 |              505.39 |              394.36 |              221.03 |              245.96 |              226.31 |
| TPC-DS Q88    |              103.29 |              136.04 |              121.51 |               92.66 |              105.56 |              109.79 |
| TPC-DS Q89    |               44.20 |               63.13 |               47.25 |               46.69 |               46.98 |               51.51 |
| TPC-DS Q90    |                9.13 |               12.36 |                9.42 |               10.40 |               10.30 |                9.32 |
| TPC-DS Q91    |               14.30 |               16.44 |               15.74 |               16.76 |               12.72 |               16.51 |
| TPC-DS Q92    |               13.18 |               14.64 |               15.28 |               15.39 |               10.69 |               13.74 |
| TPC-DS Q93    |              130.03 |              134.88 |              110.64 |              140.55 |              134.82 |              192.63 |
| TPC-DS Q94    |               31.45 |               36.37 |               28.96 |               30.79 |               31.07 |               58.86 |
| TPC-DS Q95    |              446.43 |              454.51 |              423.09 |              580.56 |              499.23 |              585.63 |
| TPC-DS Q96    |               13.43 |               12.64 |               13.73 |               17.27 |               31.17 |              119.00 |
| TPC-DS Q97    |              342.32 |              240.63 |              243.16 |              619.91 |              562.72 |              548.24 |
| TPC-DS Q98    |               48.19 |               49.19 |               51.03 |               46.15 |               53.41 |               46.14 |
| TPC-DS Q99    |               42.62 |               68.96 |               37.79 |               37.74 |               67.55 |               63.33 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |       315.13 |      1.42 |           9.30 |                 11.18 |
| monetdb-1-1-2-1 |       315.13 |      1.42 |           9.30 |                 11.18 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 |        38.95 |      0.18 |           0.01 |                  2.65 |
| monetdb-1-1-2-1 |        38.95 |      0.18 |           0.01 |                  2.65 |

### Benchmarking phase: SUT deployment

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      2.63 |          14.49 |                 16.36 |
| monetdb-1-1-2-1 | n/a          |      8.11 |          20.98 |                 22.86 |
| monetdb-1-2-1-1 | 66.08        |      4.16 |           8.65 |                  8.66 |
| monetdb-1-2-2-1 | n/a          |      3.09 |          11.85 |                 11.86 |

### Benchmarking phase: component benchmarker

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| monetdb-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| monetdb-1-1-2-1 | n/a          |      0.00 |           0.30 |                  0.31 |
| monetdb-1-2-1-1 | 12.76        |      0.45 |           0.27 |                  0.28 |
| monetdb-1-2-2-1 | n/a          |      0.00 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection monetdb-1-1-1-1 (bexhoma-metrics-monetdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
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
* CPU Utilization [CPUs] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-1-2-1 (bexhoma-metrics-monetdb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection monetdb-1-2-1-1 (bexhoma-metrics-monetdb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection monetdb-1-2-2-1 (bexhoma-metrics-monetdb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
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
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
