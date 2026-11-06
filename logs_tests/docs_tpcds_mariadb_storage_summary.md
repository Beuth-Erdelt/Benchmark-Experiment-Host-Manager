## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 2307s 
* Code: 1793873688
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:944580
  * datadisk:4502
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
    * code:1793873688
* mariadb-1-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:947579
  * datadisk:4502
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
    * code:1793873688
* mariadb-1-1-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:947579
  * datadisk:4502
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
    * code:1793873688
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:954341
  * datadisk:4503
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
    * code:1793873688
* mariadb-1-2-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:951737
  * datadisk:4503
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
    * code:1793873688
* mariadb-1-2-2-1-2 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:951737
  * datadisk:4503
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
    * code:1793873688

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793873688-6d44cbbd48-fb8n5: 0
* bexhoma-sut-mariadb-1-1793873688-7d8fd78447-bw82v: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |    1 |      198.00 |           1.00 |            1.00 |         82.00 |          105.00 |              8 |           0 |             | None           |             0 | False         |               18.18 | False               |
| MariaDB-1-2 |                2 |    1 |      198.00 |           1.00 |            1.00 |         82.00 |          105.00 |              8 |           0 |             | None           |             0 | False         |               18.18 | True                |

### Benchmarking

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| mariadb-1-1-1-1-1 | MariaDB-1       | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        360 |            0.69 |             5293.02 |            990.00 |          -1 | mariadb-1-1-1-1-1 |
| mariadb-1-1-2-1-1 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        381 |            0.72 |             5062.63 |            935.43 |          -1 | mariadb-1-1-2-1-1 |
| mariadb-1-1-2-1-2 | MariaDB-1       | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        383 |            0.71 |             5153.04 |            930.55 |          -1 | mariadb-1-1-2-1-2 |
| mariadb-1-2-1-1-1 | MariaDB-1       | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        342 |            0.73 |             5032.36 |           1042.11 |          -1 | mariadb-1-2-1-1-1 |
| mariadb-1-2-2-1-1 | MariaDB-1       | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        365 |            0.71 |             5170.21 |            976.44 |          -1 | mariadb-1-2-2-1-1 |
| mariadb-1-2-2-1-2 | MariaDB-1       | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        365 |            0.71 |             5141.68 |            976.44 |          -1 | mariadb-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        360 |            0.69 |             5293.02 |            990.00 |          -1 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        383 |            0.71 |             5107.63 |           1861.10 |          -1 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        342 |            0.73 |             5032.36 |           1042.11 |          -1 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        365 |            0.71 |             5155.93 |           1952.88 |          -1 |

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
| TPC-DS Q1     |               12.21 |               13.93 |               15.35 |               28.48 |               13.03 |               13.96 |
| TPC-DS Q2     |             3845.20 |             3625.71 |             3637.00 |            12590.57 |             3936.34 |             4050.29 |
| TPC-DS Q3     |                5.52 |                7.76 |                7.74 |              237.05 |                5.23 |                4.88 |
| TPC-DS Q4     |             8917.70 |             9625.30 |             9904.03 |            10105.94 |            10190.22 |            10233.54 |
| TPC-DS Q5     |             7563.07 |             8673.96 |             9288.37 |             7911.35 |             8478.16 |             8543.11 |
| TPC-DS Q6     |              620.38 |              800.55 |              568.90 |              943.30 |              662.92 |              656.32 |
| TPC-DS Q7     |             2738.51 |             3698.66 |             3697.41 |             2752.12 |             3934.59 |             3936.18 |
| TPC-DS Q8     |              262.85 |              412.36 |              306.65 |              264.40 |              304.79 |              305.69 |
| TPC-DS Q9     |             3645.74 |             3418.79 |             3359.48 |             3316.98 |             3882.09 |             3746.26 |
| TPC-DS Q10    |               48.73 |               41.59 |               21.99 |               32.45 |               19.01 |               24.08 |
| TPC-DS Q11    |             7093.05 |             6245.17 |             6145.63 |             6298.79 |             7121.65 |             6632.17 |
| TPC-DS Q12    |              187.68 |              185.89 |              182.42 |              195.04 |              186.54 |              183.76 |
| TPC-DS Q13    |              722.66 |              766.98 |              727.36 |              728.44 |              669.78 |              709.52 |
| TPC-DS Q14a+b |            71653.43 |            51736.16 |            52411.30 |            39988.65 |            47186.16 |            44716.88 |
| TPC-DS Q15    |              125.92 |              130.06 |              116.89 |              118.63 |              121.80 |              125.92 |
| TPC-DS Q16    |             8345.55 |             8329.56 |             8469.42 |             7375.62 |             7739.87 |             8705.27 |
| TPC-DS Q17    |              517.23 |              573.35 |              466.56 |              497.90 |              484.55 |              576.28 |
| TPC-DS Q18    |             1458.24 |             1589.44 |             1583.52 |             1399.15 |             1399.00 |             1402.88 |
| TPC-DS Q19    |              177.55 |              175.26 |              169.41 |              172.41 |              173.84 |              193.01 |
| TPC-DS Q20    |              350.94 |              347.23 |              362.70 |              394.35 |              362.11 |              342.29 |
| TPC-DS Q21    |              905.72 |              853.36 |              867.42 |             2752.85 |              836.90 |              842.13 |
| TPC-DS Q22    |            14746.57 |            16233.80 |            15832.48 |            20567.11 |            14996.99 |            15516.90 |
| TPC-DS Q23a+b |            50089.00 |            58697.62 |            59547.36 |            48641.30 |            55678.43 |            57458.38 |
| TPC-DS Q24a+b |               48.78 |               51.53 |               45.22 |               48.87 |               58.04 |               45.40 |
| TPC-DS Q25    |              115.13 |              116.71 |              101.17 |              114.43 |              117.77 |               91.91 |
| TPC-DS Q26    |              606.26 |              605.70 |              593.75 |              720.62 |              676.91 |              606.47 |
| TPC-DS Q27    |             2571.62 |             3030.53 |             3002.22 |             2566.80 |             3524.91 |             3473.49 |
| TPC-DS Q28    |             2592.61 |             2561.38 |             2561.38 |             2556.16 |             2581.97 |             2788.73 |
| TPC-DS Q29    |               69.11 |               67.06 |               65.70 |               65.96 |               70.16 |              181.93 |
| TPC-DS Q30    |               28.17 |               27.98 |               25.11 |               28.16 |               42.82 |               74.92 |
| TPC-DS Q31    |             1366.32 |              991.73 |              986.72 |              988.53 |             1751.05 |             1424.63 |
| TPC-DS Q32    |               15.36 |                5.53 |                5.33 |                5.04 |                5.52 |                5.27 |
| TPC-DS Q33    |              435.47 |              137.31 |              134.08 |              136.14 |              136.08 |              118.14 |
| TPC-DS Q34    |             2313.34 |             2678.74 |             2670.45 |             2587.84 |             2920.50 |             3471.56 |
| TPC-DS Q35    |              935.74 |              832.86 |             1013.85 |              846.93 |             1017.31 |              765.09 |
| TPC-DS Q36    |             3215.90 |             3861.34 |             4206.33 |             2210.71 |             3076.15 |             3060.59 |
| TPC-DS Q37    |             4192.74 |             4635.31 |             3661.16 |             3005.04 |             3465.21 |             3362.12 |
| TPC-DS Q38    |             5490.15 |             7746.44 |             8372.97 |             5639.19 |             6674.92 |             6548.99 |
| TPC-DS Q39a+b |             2092.76 |              969.98 |              967.85 |              984.94 |             1407.91 |             1944.29 |
| TPC-DS Q40    |              133.20 |              158.05 |              126.82 |              133.24 |              133.29 |              177.38 |
| TPC-DS Q41    |              363.63 |              363.16 |              359.44 |              353.46 |              369.49 |              349.87 |
| TPC-DS Q42    |              166.70 |              164.65 |              146.44 |              164.50 |              194.37 |              159.71 |
| TPC-DS Q43    |              792.57 |              763.46 |              758.03 |              764.19 |              824.30 |              768.43 |
| TPC-DS Q44    |                1.53 |                1.36 |                1.02 |                1.24 |                1.11 |                1.23 |
| TPC-DS Q45    |              100.06 |               97.27 |               95.92 |               95.87 |               96.98 |               92.83 |
| TPC-DS Q46    |             2730.53 |             2933.51 |             4345.33 |             3560.20 |             3064.61 |             3235.59 |
| TPC-DS Q47    |            15179.13 |            16436.18 |            15688.84 |            15787.83 |            15265.81 |            15408.96 |
| TPC-DS Q48    |              873.67 |              947.36 |              836.57 |             1240.74 |              812.00 |              769.64 |
| TPC-DS Q49    |               94.86 |               84.63 |               81.10 |              284.79 |               84.60 |               79.39 |
| TPC-DS Q50    |               20.87 |               17.82 |               18.96 |               17.48 |               16.63 |               16.35 |
| TPC-DS Q51    |             7335.35 |             7875.41 |             7866.13 |             7083.63 |             7144.51 |             6687.01 |
| TPC-DS Q52    |              187.01 |              160.86 |              165.18 |              155.51 |              156.62 |              145.87 |
| TPC-DS Q53    |              105.95 |              103.66 |              105.28 |              103.95 |              103.57 |              125.55 |
| TPC-DS Q54    |              912.94 |              863.27 |              853.31 |              842.21 |              863.04 |              839.61 |
| TPC-DS Q55    |              170.03 |              157.74 |              170.91 |              158.79 |              150.69 |              155.22 |
| TPC-DS Q56    |              116.79 |              115.79 |              200.65 |              107.02 |              109.36 |              105.23 |
| TPC-DS Q57    |             4783.85 |             5660.04 |             6005.47 |             5175.57 |             4638.28 |             4628.28 |
| TPC-DS Q58    |             4412.76 |             6949.13 |             6907.75 |             4790.29 |             5126.47 |             5291.17 |
| TPC-DS Q59    |             8181.77 |             9098.57 |             8887.92 |             7304.29 |             8422.86 |             8304.75 |
| TPC-DS Q60    |              354.75 |              240.40 |              610.55 |              316.73 |              227.34 |              213.60 |
| TPC-DS Q61    |              299.37 |              288.67 |              275.47 |              287.86 |              262.85 |              260.21 |
| TPC-DS Q62    |             1293.05 |             2147.83 |             1458.06 |             1301.97 |             1349.24 |             1408.31 |
| TPC-DS Q63    |              108.32 |              222.99 |              175.25 |              108.41 |              123.69 |              180.75 |
| TPC-DS Q64    |              441.04 |              518.38 |              487.06 |              450.57 |              429.27 |              593.01 |
| TPC-DS Q65    |             5238.87 |             6880.98 |             6851.30 |             5118.62 |             6141.12 |             6127.95 |
| TPC-DS Q66    |              908.88 |              941.43 |              942.20 |             1289.45 |             1611.90 |             1317.58 |
| TPC-DS Q67    |             6951.27 |             5967.06 |             5977.07 |             6458.09 |             6658.62 |             6289.58 |
| TPC-DS Q68    |             2399.37 |             3154.95 |             3154.41 |             3410.14 |             2929.10 |             2963.04 |
| TPC-DS Q69    |              269.81 |              322.42 |              254.98 |              285.14 |              343.85 |              256.68 |
| TPC-DS Q70    |             6314.31 |             8253.03 |             8329.92 |             6464.80 |             8075.36 |             8551.48 |
| TPC-DS Q71    |              334.87 |              401.90 |              331.79 |              348.76 |              625.60 |              355.93 |
| TPC-DS Q72    |              586.38 |              619.61 |              583.30 |              601.12 |              741.10 |              580.98 |
| TPC-DS Q73    |             2116.92 |             2656.20 |             2643.01 |             2144.91 |             2630.59 |             2610.99 |
| TPC-DS Q74    |             4757.09 |             4717.66 |             4811.81 |             4761.45 |             5645.58 |             5460.05 |
| TPC-DS Q75    |             4243.01 |             4175.79 |             4232.64 |             4341.33 |             4273.95 |             4114.48 |
| TPC-DS Q76    |              341.47 |              380.91 |              781.79 |              342.97 |              333.07 |              337.89 |
| TPC-DS Q77    |             4557.05 |             5990.54 |             5830.71 |             4766.43 |             5829.28 |             5821.83 |
| TPC-DS Q78    |             4073.36 |             4306.94 |             4371.22 |             4612.22 |             4477.99 |             4426.91 |
| TPC-DS Q79    |             2459.34 |             2783.96 |             2794.56 |             2414.28 |             3079.32 |             3089.98 |
| TPC-DS Q80    |              383.81 |              512.44 |              383.13 |              382.31 |              471.87 |              471.72 |
| TPC-DS Q81    |              154.07 |              156.23 |              157.85 |              149.27 |              164.21 |              158.28 |
| TPC-DS Q82    |             3008.29 |             3684.59 |             3402.26 |             3299.82 |             3782.24 |             3780.48 |
| TPC-DS Q83    |              782.40 |              696.20 |              865.63 |              687.23 |              900.00 |              901.15 |
| TPC-DS Q84    |               39.21 |               39.40 |               41.40 |               38.48 |               56.40 |               55.01 |
| TPC-DS Q85    |               97.70 |              102.95 |               98.11 |              105.46 |               96.35 |               94.06 |
| TPC-DS Q86    |              638.32 |              815.79 |              851.90 |              628.68 |              791.35 |              785.88 |
| TPC-DS Q87    |             6170.63 |             6580.98 |             6334.77 |             5631.45 |             6482.95 |             6469.96 |
| TPC-DS Q88    |            19712.38 |            25596.42 |            25800.47 |            18723.99 |            23413.98 |            24051.24 |
| TPC-DS Q89    |             1117.10 |             1151.08 |             1143.40 |             1099.60 |             1110.53 |             1072.92 |
| TPC-DS Q90    |              243.23 |              287.01 |              249.82 |              243.69 |              245.41 |              234.47 |
| TPC-DS Q91    |               10.40 |               12.59 |               10.41 |               14.91 |               13.45 |                9.36 |
| TPC-DS Q92    |                4.78 |                4.81 |                4.67 |                4.45 |                4.40 |                5.22 |
| TPC-DS Q93    |               27.18 |               32.68 |               27.54 |               34.16 |               25.49 |               27.17 |
| TPC-DS Q94    |              141.81 |              154.12 |              150.68 |              140.10 |              136.92 |              143.07 |
| TPC-DS Q95    |              573.19 |              606.40 |              585.38 |              590.78 |              591.77 |              797.17 |
| TPC-DS Q96    |             1910.17 |             1907.76 |             1981.28 |             2279.50 |             2495.68 |             2171.15 |
| TPC-DS Q97    |             3994.38 |             4374.46 |             4685.65 |             4146.24 |             4734.05 |             4680.97 |
| TPC-DS Q98    |              673.06 |              858.55 |              974.54 |              741.38 |              661.72 |              667.72 |
| TPC-DS Q99    |             2643.62 |             2940.90 |             2523.05 |             3067.95 |             2836.92 |             2809.68 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       256.39 |      3.71 |           3.91 |                  4.04 |
| mariadb-1-1-2-1 |       256.39 |      3.71 |           3.91 |                  4.04 |

### Loading phase: component data generator

| DBMS            | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |
| mariadb-1-1-2-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |         2.40 |      0.05 |           0.01 |                  0.76 |
| mariadb-1-1-2-1 |         2.40 |      0.05 |           0.01 |                  0.76 |

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       332.42 |      1.00 |           4.88 |                  4.90 |
| mariadb-1-1-2-1 |       730.47 |      2.00 |           4.35 |                  4.36 |
| mariadb-1-2-1-1 |       295.34 |      1.75 |           2.73 |                  2.74 |
| mariadb-1-2-2-1 |       637.79 |      2.00 |           3.04 |                  3.05 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |        19.17 |      0.44 |           0.30 |                  0.31 |
| mariadb-1-1-2-1 |        41.83 |      0.51 |           0.32 |                  0.32 |
| mariadb-1-2-1-1 |        20.09 |      0.04 |           0.30 |                  0.31 |
| mariadb-1-2-2-1 |        41.35 |      1.66 |           0.33 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
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
