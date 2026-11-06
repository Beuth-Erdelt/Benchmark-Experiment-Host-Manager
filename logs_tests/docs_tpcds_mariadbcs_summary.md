## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1708s 
* Code: 1793820455
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB', 'MariaDBCS'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type nvme and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 32Gi RAM. RAM limit is 32Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:614198
  * datadisk:4569
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:611695
  * datadisk:4570
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:613073
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:614197
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793820455

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793820455-9fdf78fc5-p5wp8: 0
* bexhoma-sut-mariadb-1-1793820455-6bbc8867c8-srcbx: 0
* bexhoma-sut-mariadbcs-1-1793820455-5796fb4c9f-sbrdm: 0
* bexhoma-sut-mariadbcs-1-1793820455-854dff5c45-7tjdl: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1   |                1 |    1 |      268.00 |           3.00 |            0.00 |        132.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               13.43 | False               |
| MariaDB-1-2   |                2 |    1 |      268.00 |           3.00 |            0.00 |        132.00 |          132.00 |              1 |           0 |             | None           |             0 | False         |               13.43 | True                |
| MariaDBCS-1-1 |                1 |    1 |      188.00 |          19.00 |            0.00 |        128.00 |           33.00 |              1 |           0 |             | None           |             0 | False         |               19.15 | False               |
| MariaDBCS-1-2 |                2 |    1 |      188.00 |          19.00 |            0.00 |        128.00 |           33.00 |              1 |           0 |             | None           |             0 | False         |               19.15 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadb-1-1-1-1-1   | MariaDB-1       | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        357 |            0.78 |             4681.10 |            998.32 |          -1 | mariadb-1-1-1-1-1   |
| mariadb-1-2-1-1-1   | MariaDB-1       | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        322 |            0.70 |             5208.43 |           1106.83 |          -1 | mariadb-1-2-1-1-1   |
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        136 |            0.97 |             3726.42 |           2620.59 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        124 |            0.84 |             4317.79 |           2874.19 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        357 |            0.78 |             4681.10 |            998.32 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        322 |            0.70 |             5208.43 |           1106.83 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        136 |            0.97 |             3726.42 |           2620.59 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        124 |            0.84 |             4317.79 |           2874.19 |          -1 |

#### Query Completion per Phase

| phase           |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1   |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadb-1-2-1   |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadbcs-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mariadbcs-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         4.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         4.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |        13.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |        13.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:--------------|--------------------:|--------------------:|----------------------:|----------------------:|
| TPC-DS Q1     |               11.94 |              188.99 |               1813.62 |               1897.57 |
| TPC-DS Q2     |             4862.01 |             5348.51 |               4420.18 |               4295.18 |
| TPC-DS Q3     |                7.12 |               12.42 |               1185.00 |               1105.28 |
| TPC-DS Q4     |             9041.50 |             9483.16 |               2154.44 |               1462.74 |
| TPC-DS Q5     |             6920.39 |             7031.27 |               5307.79 |               4350.17 |
| TPC-DS Q6     |              853.34 |              586.57 |               1205.89 |                974.64 |
| TPC-DS Q7     |             2744.20 |             9542.42 |               1710.79 |               1406.01 |
| TPC-DS Q8     |              306.14 |              296.22 |                832.35 |                705.44 |
| TPC-DS Q9     |             3483.26 |             3380.84 |                498.58 |                400.88 |
| TPC-DS Q10    |               44.85 |               64.97 |                948.60 |                813.11 |
| TPC-DS Q11    |             6102.81 |             6146.52 |               1162.05 |                911.74 |
| TPC-DS Q12    |              189.30 |              195.33 |                687.51 |                573.91 |
| TPC-DS Q13    |              842.82 |              836.48 |               1609.24 |               1463.87 |
| TPC-DS Q14a+b |            44086.14 |            42052.22 |               6842.62 |               5901.67 |
| TPC-DS Q15    |              115.50 |              116.70 |                793.93 |                654.16 |
| TPC-DS Q16    |             8363.18 |             8232.55 |                945.06 |                781.23 |
| TPC-DS Q17    |             1162.12 |              528.43 |               1414.63 |               1167.76 |
| TPC-DS Q18    |             2674.80 |             1495.64 |               1733.62 |               1070.89 |
| TPC-DS Q19    |              186.97 |              188.15 |               1001.85 |                727.88 |
| TPC-DS Q20    |              359.46 |              351.63 |                630.55 |                488.53 |
| TPC-DS Q21    |              876.21 |             3790.03 |               1482.28 |               1199.23 |
| TPC-DS Q22    |            13588.25 |             8552.66 |               1769.53 |               1467.53 |
| TPC-DS Q23a+b |            51020.05 |            51614.56 |               3451.83 |               3181.17 |
| TPC-DS Q24a+b |               28.96 |               22.53 |               4482.60 |               5146.02 |
| TPC-DS Q25    |              132.30 |              120.51 |               1252.99 |               1014.68 |
| TPC-DS Q26    |              691.66 |              730.41 |                841.76 |                728.00 |
| TPC-DS Q27    |             2870.27 |             2594.16 |                939.61 |                848.13 |
| TPC-DS Q28    |             2849.70 |             2734.24 |                386.25 |                411.70 |
| TPC-DS Q29    |               87.49 |               77.37 |               1247.30 |               1301.19 |
| TPC-DS Q30    |               30.92 |               34.12 |                866.05 |                846.65 |
| TPC-DS Q31    |             1153.30 |             1048.50 |                841.43 |                859.84 |
| TPC-DS Q32    |                3.89 |                3.20 |                293.02 |                284.98 |
| TPC-DS Q33    |              146.69 |              152.86 |                686.92 |                742.03 |
| TPC-DS Q34    |             2465.21 |             2533.34 |                219.88 |                262.06 |
| TPC-DS Q35    |              944.88 |              948.69 |                831.51 |                820.74 |
| TPC-DS Q36    |             2258.71 |             2203.08 |                642.32 |                655.68 |
| TPC-DS Q37    |             3088.52 |             3109.38 |                385.54 |                388.55 |
| TPC-DS Q38    |             5826.96 |             5474.35 |                794.45 |                714.78 |
| TPC-DS Q39a+b |             1014.09 |              997.35 |               1779.67 |               1786.01 |
| TPC-DS Q40    |              221.23 |              137.15 |                769.21 |                748.91 |
| TPC-DS Q41    |              357.90 |              338.86 |                448.26 |                359.93 |
| TPC-DS Q42    |              189.33 |              179.76 |                367.48 |                380.75 |
| TPC-DS Q43    |              937.63 |              862.68 |                409.70 |                299.79 |
| TPC-DS Q44    |                1.60 |                1.17 |                365.08 |                196.25 |
| TPC-DS Q45    |              116.67 |              100.53 |                581.93 |                465.48 |
| TPC-DS Q46    |             3320.44 |             2829.17 |                405.44 |                312.80 |
| TPC-DS Q47    |            15345.93 |            13073.77 |               1601.87 |               1352.04 |
| TPC-DS Q48    |             1164.88 |              915.71 |               1210.66 |               1107.02 |
| TPC-DS Q49    |              102.86 |               98.98 |                793.05 |                542.39 |
| TPC-DS Q50    |               22.13 |               19.97 |                790.96 |                678.69 |
| TPC-DS Q51    |             7360.81 |             6240.52 |               3494.53 |               2981.28 |
| TPC-DS Q52    |              253.67 |              197.25 |                523.16 |                424.19 |
| TPC-DS Q53    |              143.87 |              121.57 |                701.65 |                586.63 |
| TPC-DS Q54    |             1006.73 |              871.38 |                755.14 |                597.31 |
| TPC-DS Q55    |              204.33 |              172.26 |                413.05 |                414.26 |
| TPC-DS Q56    |              331.12 |              257.12 |                949.53 |                856.30 |
| TPC-DS Q57    |             6381.10 |             5293.93 |               1223.35 |               1150.62 |
| TPC-DS Q58    |             7747.64 |             4473.01 |                718.13 |                593.02 |
| TPC-DS Q59    |             8518.77 |             7055.56 |               1440.12 |               1271.93 |
| TPC-DS Q60    |              372.33 |              294.59 |               1111.50 |                821.64 |
| TPC-DS Q61    |              358.50 |              274.32 |                367.67 |                242.84 |
| TPC-DS Q62    |             1535.87 |             1335.88 |               1212.92 |                888.84 |
| TPC-DS Q63    |              185.33 |              118.29 |                603.78 |                544.83 |
| TPC-DS Q64    |              489.43 |              434.96 |               4010.56 |               3337.16 |
| TPC-DS Q65    |             5294.92 |             4573.20 |                651.42 |                559.23 |
| TPC-DS Q66    |             1003.58 |              912.91 |               1565.93 |               1235.97 |
| TPC-DS Q67    |             5886.39 |             5249.99 |               4688.98 |               4031.68 |
| TPC-DS Q68    |             2573.42 |             2444.88 |                390.34 |                365.04 |
| TPC-DS Q69    |              391.18 |              297.50 |               1097.90 |                835.84 |
| TPC-DS Q70    |             7371.71 |             6214.07 |               1365.36 |               1138.13 |
| TPC-DS Q71    |              689.22 |              389.79 |                712.23 |                605.22 |
| TPC-DS Q72    |             1243.01 |              641.08 |               1787.93 |               1425.05 |
| TPC-DS Q73    |             3936.79 |             2285.60 |                300.45 |                213.31 |
| TPC-DS Q74    |             7720.94 |             4635.00 |               1060.18 |                753.70 |
| TPC-DS Q75    |             6921.24 |             4222.33 |               1344.43 |               1384.81 |
| TPC-DS Q76    |              752.96 |              363.08 |                822.96 |                599.28 |
| TPC-DS Q77    |             9539.58 |             4873.79 |               1170.37 |               1161.33 |
| TPC-DS Q78    |             6625.87 |             4473.00 |               1871.59 |               1685.79 |
| TPC-DS Q79    |             3580.72 |             2739.29 |                917.00 |               1131.59 |
| TPC-DS Q80    |              434.97 |              421.86 |               1431.34 |               1487.49 |
| TPC-DS Q81    |              169.09 |              152.76 |                905.99 |                944.42 |
| TPC-DS Q82    |             4190.50 |             3194.28 |                872.65 |                827.77 |
| TPC-DS Q83    |              756.82 |              775.22 |                877.08 |                908.91 |
| TPC-DS Q84    |               38.90 |               39.59 |                719.84 |                748.24 |
| TPC-DS Q85    |              136.26 |              129.24 |               2889.39 |               2748.12 |
| TPC-DS Q86    |              656.80 |              666.07 |                628.04 |                488.75 |
| TPC-DS Q87    |             5652.67 |             5574.04 |               1033.29 |                889.05 |
| TPC-DS Q88    |            17805.64 |             7320.45 |               1406.33 |                795.14 |
| TPC-DS Q89    |             1164.69 |             1091.34 |                296.96 |                269.29 |
| TPC-DS Q90    |              112.14 |               88.12 |                481.21 |                362.69 |
| TPC-DS Q91    |               18.83 |               11.93 |                968.37 |                824.69 |
| TPC-DS Q92    |                4.90 |                5.09 |                536.90 |                457.71 |
| TPC-DS Q93    |               67.31 |               60.67 |                564.33 |                476.53 |
| TPC-DS Q94    |              393.67 |              377.54 |                923.16 |                760.81 |
| TPC-DS Q95    |              614.67 |              596.15 |               1057.41 |                838.62 |
| TPC-DS Q96    |             1978.26 |              685.95 |                524.58 |                412.91 |
| TPC-DS Q97    |             4273.66 |             4354.91 |                889.50 |                833.45 |
| TPC-DS Q98    |              700.19 |              691.98 |                716.33 |                594.80 |
| TPC-DS Q99    |             2638.00 |             2659.91 |                979.63 |                871.13 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       286.87 |      1.25 |           3.88 |                  3.97 |
| mariadbcs-1-1-1-1 |       249.02 |      1.92 |           5.46 |                  6.23 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |         2.31 |      0.03 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 |         3.35 |      0.04 |           0.01 |                  1.01 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       327.60 |      1.00 |           4.24 |                  4.26 |
| mariadb-1-2-1-1   |       271.84 |      1.00 |           3.61 |                  3.61 |
| mariadbcs-1-1-1-1 |       821.65 |      9.17 |          11.14 |                 11.91 |
| mariadbcs-1-2-1-1 |       790.18 |     11.10 |          10.31 |                 10.50 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |        20.23 |      0.04 |           0.32 |                  0.32 |
| mariadb-1-2-1-1   |        19.70 |      0.47 |           0.31 |                  0.32 |
| mariadbcs-1-1-1-1 |        19.40 |      0.07 |           0.31 |                  0.31 |
| mariadbcs-1-2-1-1 |        19.51 |      0.39 |           0.28 |                  0.29 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-2-1-1 (bexhoma-metrics-mariadbcs-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

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
* TEST passed: Reset scripts ran without errors
