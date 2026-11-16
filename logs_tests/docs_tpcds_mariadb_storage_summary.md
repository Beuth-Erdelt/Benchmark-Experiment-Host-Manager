## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 2517s 
* Code: 1794767846
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091493
  * datadisk:4474
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767846
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1086019
  * datadisk:4474
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767846
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1086019
  * datadisk:4474
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767846
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1086023
  * datadisk:4475
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767846
* mariadb-1-2-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091166
  * datadisk:4475
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767846
* mariadb-1-2-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091166
  * datadisk:4475
  * volume_size:49G
  * volume_used:4.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767846

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* MariaDB-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794767846-54d8968cfb-ccqd9: 0
* bexhoma-sut-mariadb-1-1794767846-5ff495685f-ghf69: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      208.00 |           5.00 |            1.00 |         85.00 |          107.00 |              8 |         0 |             | None           |             0 | False         |               17.31 | False               |
| MariaDB-1-2 |                2 |    1 |      208.00 |           5.00 |            1.00 |         85.00 |          107.00 |              8 |         0 |             | None           |             0 | False         |               17.31 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        312 |            0.75 |             4895.39 |           1142.31 |          -1 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               99 |                  99 |        336 |            0.74 |             4924.90 |           1060.71 |          -1 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               99 |                  99 |        343 |            0.72 |             5054.78 |           1039.07 |          -1 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        306 |            0.76 |             4781.79 |           1164.71 |          -1 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 | 1.00 |               99 |                  99 |        377 |            0.80 |             4542.08 |            945.36 |          -1 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 | 1.00 |               99 |                  99 |        383 |            0.83 |             4405.96 |            930.55 |          -1 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        312 |            0.75 |             4895.39 |           1142.31 |          -1 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        343 |            0.73 |             4989.42 |           2078.13 |          -1 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        306 |            0.76 |             4781.79 |           1164.71 |          -1 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        383 |            0.82 |             4473.50 |           1861.10 |          -1 |

#### Query Completion per Phase

| phase         |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:--------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |
| mariadb-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-2-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-1-2-1-1 |   mariadb-1-1-2-1-2 |   mariadb-1-2-1-1-1 |   mariadb-1-2-2-1-1 |   mariadb-1-2-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               13.98 |               13.48 |               13.35 |               39.18 |               12.38 |               12.23 |
| TPC-DS Q2     |             4248.82 |             3478.19 |             3447.24 |             9142.27 |             3809.72 |             3701.34 |
| TPC-DS Q3     |                6.38 |                6.51 |                5.79 |               22.48 |                5.79 |                6.65 |
| TPC-DS Q4     |            10194.10 |             8935.50 |             8954.20 |             9511.79 |             9542.89 |             9532.54 |
| TPC-DS Q5     |             8296.98 |             7401.73 |             7555.41 |             8171.50 |             8685.09 |             8639.08 |
| TPC-DS Q6     |              755.58 |              880.34 |              711.84 |              731.61 |              844.56 |              823.72 |
| TPC-DS Q7     |             3132.27 |             2743.40 |             2628.64 |             2778.28 |             3895.01 |             3807.57 |
| TPC-DS Q8     |              376.84 |              245.55 |              237.95 |              255.99 |              257.25 |              235.61 |
| TPC-DS Q9     |             3815.42 |             3245.61 |             3245.02 |             3336.82 |             3259.50 |             3247.84 |
| TPC-DS Q10    |              143.62 |               49.32 |               42.93 |              969.54 |               53.70 |               42.41 |
| TPC-DS Q11    |             6844.99 |             6034.35 |             6076.21 |             6026.37 |             7221.48 |             7220.95 |
| TPC-DS Q12    |              190.23 |              182.92 |              261.37 |              205.80 |              247.52 |              245.29 |
| TPC-DS Q13    |             1334.50 |              803.87 |              692.24 |              909.03 |              892.38 |              892.09 |
| TPC-DS Q14a+b |            43903.89 |            41159.80 |            40456.53 |            39916.32 |            53474.76 |            53467.51 |
| TPC-DS Q15    |              124.26 |              127.04 |              114.33 |              117.31 |              141.19 |              145.31 |
| TPC-DS Q16    |             8036.54 |             8393.73 |             8005.94 |             8209.77 |             9535.29 |             9234.61 |
| TPC-DS Q17    |              585.92 |              490.15 |              472.35 |             1407.57 |              560.83 |              734.55 |
| TPC-DS Q18    |             1448.57 |             1455.88 |             1415.46 |             1608.34 |             1902.36 |             1926.71 |
| TPC-DS Q19    |              167.60 |              169.39 |              162.51 |              163.32 |              162.85 |              178.37 |
| TPC-DS Q20    |              333.93 |              341.56 |              352.55 |              331.51 |              395.90 |              393.15 |
| TPC-DS Q21    |              907.36 |              904.86 |              969.19 |             1240.96 |             1071.89 |             1174.74 |
| TPC-DS Q22    |            13329.66 |            16154.44 |            15235.43 |            13375.42 |            19397.71 |            18960.73 |
| TPC-DS Q23a+b |            50605.41 |            56824.86 |            55973.25 |            47816.09 |            63063.09 |            63473.84 |
| TPC-DS Q24a+b |             1911.17 |             1636.55 |             1589.18 |             1411.74 |             1810.87 |             1760.12 |
| TPC-DS Q25    |              158.14 |              116.14 |               94.18 |              111.88 |               86.38 |              104.49 |
| TPC-DS Q26    |              788.99 |              624.53 |              563.33 |              621.26 |              603.82 |              659.09 |
| TPC-DS Q27    |             2547.80 |             3236.09 |             3189.14 |             2419.62 |             3830.55 |             3849.91 |
| TPC-DS Q28    |             2513.95 |             2555.47 |             2530.42 |             2642.16 |             2949.51 |             2859.14 |
| TPC-DS Q29    |               44.93 |               39.45 |               36.12 |               39.16 |               48.70 |               55.97 |
| TPC-DS Q30    |               79.24 |               75.31 |               73.87 |               74.46 |               70.56 |              115.63 |
| TPC-DS Q31    |             1082.61 |              978.36 |              941.39 |              989.87 |              980.47 |             1061.83 |
| TPC-DS Q32    |                3.99 |                3.72 |                3.84 |                4.04 |                3.22 |                3.82 |
| TPC-DS Q33    |              126.68 |              111.75 |              103.25 |              109.67 |               89.61 |              106.38 |
| TPC-DS Q34    |             2198.49 |             2758.84 |             2751.31 |             2167.50 |             3196.76 |             2933.91 |
| TPC-DS Q35    |             1042.09 |              840.56 |              814.58 |              844.42 |              807.45 |             1033.34 |
| TPC-DS Q36    |             2330.44 |             2792.17 |             2852.85 |             2152.81 |             3185.50 |             3173.06 |
| TPC-DS Q37    |             2961.26 |             3141.08 |             3099.69 |             2928.78 |             3840.47 |             3710.60 |
| TPC-DS Q38    |             5423.89 |             6470.26 |             6421.74 |             5278.39 |             6864.70 |             7585.96 |
| TPC-DS Q39a+b |              974.57 |             1049.38 |             1041.06 |              975.83 |             1123.71 |             1188.97 |
| TPC-DS Q40    |              133.18 |              130.72 |              127.17 |              134.68 |              136.74 |              133.48 |
| TPC-DS Q41    |              343.73 |              344.60 |              346.02 |              345.42 |              356.58 |              329.26 |
| TPC-DS Q42    |              166.32 |              163.81 |              159.98 |              162.85 |              164.46 |              157.13 |
| TPC-DS Q43    |              949.89 |              808.60 |              770.34 |              761.52 |              825.41 |             1569.60 |
| TPC-DS Q44    |             1024.52 |             1114.38 |             1126.30 |             1060.12 |             1400.97 |             1261.25 |
| TPC-DS Q45    |              109.86 |              110.42 |               93.41 |               98.90 |              121.40 |               97.45 |
| TPC-DS Q46    |             2430.12 |             2724.65 |             3078.68 |             2403.66 |             2737.11 |             3548.09 |
| TPC-DS Q47    |            13272.64 |            15184.99 |            14770.98 |            13489.43 |            16421.18 |            17771.29 |
| TPC-DS Q48    |              874.64 |              813.12 |              789.29 |              863.90 |              964.94 |              808.44 |
| TPC-DS Q49    |              107.49 |               83.81 |               79.79 |              100.03 |               92.87 |               98.55 |
| TPC-DS Q50    |               20.47 |               19.41 |               19.79 |               21.26 |               19.99 |               21.03 |
| TPC-DS Q51    |             6692.38 |             6904.93 |             6955.42 |             6772.31 |             7221.83 |             7132.00 |
| TPC-DS Q52    |              168.28 |              163.69 |              158.40 |              164.91 |              177.77 |              168.90 |
| TPC-DS Q53    |              105.31 |              105.04 |              105.85 |              105.80 |              105.89 |              104.99 |
| TPC-DS Q54    |              920.02 |              879.83 |              849.83 |              899.21 |              882.66 |              989.82 |
| TPC-DS Q55    |              168.29 |              213.65 |              182.00 |              170.20 |              169.83 |              187.21 |
| TPC-DS Q56    |              126.88 |              123.53 |              134.28 |              129.62 |              130.52 |              133.09 |
| TPC-DS Q57    |             4492.12 |             4568.75 |             4618.32 |             4615.31 |             4702.54 |             5595.88 |
| TPC-DS Q58    |             4285.69 |             4828.89 |             5598.56 |             4264.57 |             5137.81 |             5499.27 |
| TPC-DS Q59    |             7053.68 |             8556.73 |             8094.73 |             6814.73 |             9467.93 |             9200.63 |
| TPC-DS Q60    |              220.09 |              213.17 |              211.01 |              213.23 |              248.89 |              216.31 |
| TPC-DS Q61    |              267.18 |              263.71 |              260.09 |              260.68 |              297.23 |              265.66 |
| TPC-DS Q62    |             1287.69 |             1522.87 |             1580.38 |             1424.93 |             2402.69 |             1578.57 |
| TPC-DS Q63    |              123.80 |              155.99 |              161.59 |              122.39 |              152.57 |              160.03 |
| TPC-DS Q64    |              473.18 |              437.53 |              437.00 |              431.40 |              434.80 |              432.46 |
| TPC-DS Q65    |             4326.18 |             6055.93 |             6306.00 |             4317.86 |             4890.43 |             6906.14 |
| TPC-DS Q66    |              966.83 |              935.35 |              918.64 |             1365.53 |              965.26 |              963.39 |
| TPC-DS Q67    |             5453.27 |             5994.04 |             5279.63 |             5221.33 |             8224.67 |             5603.91 |
| TPC-DS Q68    |             2395.72 |             2395.61 |             3157.79 |             2459.84 |             2728.90 |             4469.53 |
| TPC-DS Q69    |              282.42 |              290.60 |              257.53 |              260.34 |              372.81 |              319.22 |
| TPC-DS Q70    |             6076.35 |             7745.19 |             6937.43 |             5982.71 |            10139.52 |             9398.40 |
| TPC-DS Q71    |              337.71 |              320.07 |              315.39 |              318.67 |              555.90 |              343.11 |
| TPC-DS Q72    |              626.12 |              572.39 |              568.04 |              584.83 |              660.67 |              576.79 |
| TPC-DS Q73    |             2091.19 |             2094.59 |             2153.20 |             2091.32 |             3277.89 |             2894.55 |
| TPC-DS Q74    |             4310.71 |             4563.48 |             4496.93 |             4396.15 |             5687.85 |             5911.17 |
| TPC-DS Q75    |             4120.59 |             4124.56 |             4015.13 |             3945.30 |             5462.55 |             5135.82 |
| TPC-DS Q76    |              336.81 |              349.67 |              366.09 |              344.05 |              410.00 |              385.46 |
| TPC-DS Q77    |             4564.31 |             5240.22 |             5301.93 |             4681.04 |             5241.65 |             5856.78 |
| TPC-DS Q78    |             4100.86 |             4330.88 |             4348.52 |             4221.56 |             4968.93 |             5048.52 |
| TPC-DS Q79    |             2469.14 |             2585.34 |             2502.47 |             2414.97 |             2870.22 |             3153.88 |
| TPC-DS Q80    |              446.93 |              478.85 |              381.02 |              382.53 |              402.34 |              469.82 |
| TPC-DS Q81    |              154.78 |              158.21 |              151.81 |              152.47 |              155.85 |              153.69 |
| TPC-DS Q82    |             3153.45 |             2884.49 |             3011.57 |             2926.66 |             3431.19 |             3118.77 |
| TPC-DS Q83    |              708.58 |              709.52 |              856.09 |              706.86 |              711.68 |              961.59 |
| TPC-DS Q84    |               41.09 |               44.15 |               39.34 |               44.85 |               40.95 |               38.73 |
| TPC-DS Q85    |               96.38 |              281.67 |               97.26 |               97.06 |              111.11 |              178.24 |
| TPC-DS Q86    |              630.32 |              630.37 |              816.16 |              623.58 |              640.66 |              771.49 |
| TPC-DS Q87    |             5411.91 |             5597.48 |             5344.26 |             5298.00 |             6332.07 |             6144.98 |
| TPC-DS Q88    |             7363.97 |             7606.21 |             7417.53 |             7395.54 |             8480.28 |             8431.50 |
| TPC-DS Q89    |             1075.23 |             1130.86 |             1200.26 |             1036.18 |             1721.28 |             1036.99 |
| TPC-DS Q90    |              262.10 |              256.32 |              232.92 |              246.80 |              264.80 |              249.08 |
| TPC-DS Q91    |               12.92 |               14.33 |               13.74 |               16.12 |               15.65 |               15.55 |
| TPC-DS Q92    |                4.61 |                4.86 |                5.22 |                4.67 |                5.15 |                5.25 |
| TPC-DS Q93    |               28.76 |               27.31 |               28.79 |               27.71 |               34.22 |               30.94 |
| TPC-DS Q94    |              345.66 |              367.68 |              354.22 |              353.18 |              377.78 |             1085.76 |
| TPC-DS Q95    |              563.79 |              595.97 |              599.46 |              574.71 |              599.97 |              697.65 |
| TPC-DS Q96    |              761.88 |              504.13 |              475.66 |              506.53 |              496.05 |              512.84 |
| TPC-DS Q97    |             4490.07 |             4022.18 |             4323.74 |             4094.75 |             4445.97 |             5175.05 |
| TPC-DS Q98    |              658.93 |              674.50 |              658.96 |              661.82 |              791.63 |              693.97 |
| TPC-DS Q99    |             2667.89 |             2827.63 |             2524.26 |             2487.64 |             3246.37 |             3222.51 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       278.56 |      5.30 |           4.26 |                  4.27 |
| mariadb-1-1-2-1 |       278.56 |      5.30 |           4.26 |                  4.27 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mariadb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |         5.37 |      0.05 |           0.01 |                  0.76 |
| mariadb-1-1-2-1 |         5.37 |      0.05 |           0.01 |                  0.76 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       280.84 |      1.00 |           4.33 |                  4.35 |
| mariadb-1-1-2-1 |       581.80 |      2.00 |           5.19 |                  5.21 |
| mariadb-1-2-1-1 |       258.98 |      1.00 |           2.70 |                  2.71 |
| mariadb-1-2-2-1 |       702.55 |      2.00 |           2.97 |                  2.97 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        19.88 |      0.40 |           0.30 |                  0.31 |
| mariadb-1-1-2-1 |        42.06 |      1.01 |           0.34 |                  0.34 |
| mariadb-1-2-1-1 |        19.22 |      0.46 |           0.29 |                  0.29 |
| mariadb-1-2-2-1 |        37.90 |      0.06 |           0.33 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
