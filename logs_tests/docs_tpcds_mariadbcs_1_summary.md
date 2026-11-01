## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1671s 
* Code: 1793529751
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:678747
  * datadisk:4586
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793529751
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:680924
  * datadisk:4587
  * volume_size:30G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793529751
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:675709
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793529751
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:675105
  * datadisk:579
  * volume_size:30G
  * volume_used:740M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:32Gi
  * limits_memory:32Gi
  * resources_total: 4.0 CPU, 32.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 32.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793529751

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793529751-56c796c58c-2x6ns: 0
* bexhoma-sut-mariadb-1-1793529751-c4cc56787-4nj5m: 0
* bexhoma-sut-mariadbcs-1-1793529751-775569b975-ct7qj: 0
* bexhoma-sut-mariadbcs-1-1793529751-5f554bd449-n7tdd: 0

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
| MariaDB-1-1   |                1 |    1 |      196.00 |           5.00 |            0.00 |         86.00 |          104.00 |              1 |           0 |             | None           |             0 | False         |               18.37 | False               |
| MariaDB-1-2   |                2 |    1 |      196.00 |           5.00 |            0.00 |         86.00 |          104.00 |              1 |           0 |             | None           |             0 | False         |               18.37 | True                |
| MariaDBCS-1-1 |                1 |    1 |      172.00 |          27.00 |            0.00 |        106.00 |           38.00 |              1 |           0 |             | None           |             0 | False         |               20.93 | False               |
| MariaDBCS-1-2 |                2 |    1 |      172.00 |          27.00 |            0.00 |        106.00 |           38.00 |              1 |           0 |             | None           |             0 | False         |               20.93 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadb-1-1-1-1-1   | MariaDB-1       | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        289 |            0.65 |             5555.85 |           1233.22 |          -1 | mariadb-1-1-1-1-1   |
| mariadb-1-2-1-1-1   | MariaDB-1       | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        321 |            0.71 |             5057.47 |           1110.28 |          -1 | mariadb-1-2-1-1-1   |
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        113 |            0.86 |             4205.32 |           3153.98 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        116 |            0.86 |             4188.79 |           3072.41 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        289 |            0.65 |             5555.85 |           1233.22 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        321 |            0.71 |             5057.47 |           1110.28 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        113 |            0.86 |             4205.32 |           3153.98 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        116 |            0.86 |             4188.79 |           3072.41 |          -1 |

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
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         5.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         7.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |        13.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |        15.00 |                |

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:--------------|--------------------:|--------------------:|----------------------:|----------------------:|
| TPC-DS Q1     |                9.76 |               11.12 |               2264.41 |               2381.79 |
| TPC-DS Q2     |             4262.34 |             3905.36 |               2805.83 |               2851.36 |
| TPC-DS Q3     |               12.08 |              162.48 |               1167.33 |               1177.42 |
| TPC-DS Q4     |             9814.68 |             9882.70 |               1601.13 |               1430.01 |
| TPC-DS Q5     |             7407.51 |             8661.68 |               3819.24 |               3424.23 |
| TPC-DS Q6     |              766.04 |              729.70 |               1162.91 |               1170.60 |
| TPC-DS Q7     |             2744.05 |             8703.33 |               1531.31 |               1529.86 |
| TPC-DS Q8     |              310.59 |              379.14 |                657.01 |                759.93 |
| TPC-DS Q9     |             3413.38 |             4256.59 |                180.12 |                276.49 |
| TPC-DS Q10    |               41.51 |               51.59 |                788.76 |                781.31 |
| TPC-DS Q11    |             6102.49 |             7610.07 |               1116.09 |                985.30 |
| TPC-DS Q12    |              202.09 |              239.94 |                658.69 |                536.68 |
| TPC-DS Q13    |              694.46 |              863.57 |               1530.40 |               1261.82 |
| TPC-DS Q14a+b |            36591.15 |            46296.09 |               5873.43 |               5437.31 |
| TPC-DS Q15    |              119.18 |              145.99 |                584.44 |                595.16 |
| TPC-DS Q16    |             7471.87 |             9402.96 |                670.91 |                708.27 |
| TPC-DS Q17    |              528.65 |              788.45 |               1061.46 |               1181.97 |
| TPC-DS Q18    |             1430.23 |             1870.36 |               1416.68 |               1583.79 |
| TPC-DS Q19    |              190.61 |              200.66 |                807.29 |                838.52 |
| TPC-DS Q20    |              346.96 |              449.29 |                498.84 |                510.61 |
| TPC-DS Q21    |              959.27 |             4826.63 |               1307.61 |               1424.09 |
| TPC-DS Q22    |            14015.32 |            10867.73 |               1079.58 |               1196.85 |
| TPC-DS Q23a+b |            41736.42 |            44231.65 |               3176.01 |               3004.98 |
| TPC-DS Q24a+b |               24.71 |               31.28 |               4318.28 |               4451.39 |
| TPC-DS Q25    |              129.49 |              151.24 |               1096.43 |               1148.39 |
| TPC-DS Q26    |              654.76 |              812.96 |                803.36 |                792.49 |
| TPC-DS Q27    |             2424.83 |             3096.53 |               1033.75 |                946.50 |
| TPC-DS Q28    |             2550.67 |             3264.20 |                478.57 |                398.15 |
| TPC-DS Q29    |               39.86 |               44.68 |               1187.69 |               1163.28 |
| TPC-DS Q30    |               28.99 |               33.54 |                930.65 |                888.21 |
| TPC-DS Q31    |              978.10 |             1180.72 |               1104.65 |               1023.32 |
| TPC-DS Q32    |                4.14 |                4.62 |                568.97 |                596.62 |
| TPC-DS Q33    |              119.63 |              154.13 |               1096.97 |                857.55 |
| TPC-DS Q34    |             2709.66 |             3110.30 |                260.03 |                281.80 |
| TPC-DS Q35    |              832.77 |             1180.65 |                770.72 |                796.42 |
| TPC-DS Q36    |             2233.34 |             2569.62 |                694.16 |                666.35 |
| TPC-DS Q37    |             3363.45 |             4110.71 |                557.58 |                534.64 |
| TPC-DS Q38    |             5420.18 |             6979.23 |                645.25 |                710.39 |
| TPC-DS Q39a+b |             1044.65 |             1268.86 |               1679.16 |               1757.46 |
| TPC-DS Q40    |              137.34 |              174.40 |                750.50 |                899.09 |
| TPC-DS Q41    |              315.28 |              445.49 |                371.97 |                406.38 |
| TPC-DS Q42    |              308.81 |              262.54 |                410.97 |                477.47 |
| TPC-DS Q43    |              828.70 |             1039.02 |                291.08 |                287.42 |
| TPC-DS Q44    |                1.16 |                0.94 |                336.91 |                218.63 |
| TPC-DS Q45    |               98.53 |              125.40 |                652.65 |                548.21 |
| TPC-DS Q46    |             2649.93 |             3392.69 |                286.37 |                256.71 |
| TPC-DS Q47    |             9171.80 |            10051.16 |               1114.41 |               1170.87 |
| TPC-DS Q48    |             1121.36 |              935.47 |                802.50 |                947.08 |
| TPC-DS Q49    |              102.12 |               98.81 |                671.32 |                827.58 |
| TPC-DS Q50    |               21.70 |               17.92 |                700.43 |                753.04 |
| TPC-DS Q51    |             6032.61 |             6725.69 |               1824.96 |               1953.28 |
| TPC-DS Q52    |              220.13 |              200.70 |                430.64 |                442.55 |
| TPC-DS Q53    |              124.91 |              125.24 |                572.57 |                647.42 |
| TPC-DS Q54    |              924.39 |             1031.74 |                603.42 |                593.70 |
| TPC-DS Q55    |              164.92 |              177.74 |                525.87 |                434.00 |
| TPC-DS Q56    |              149.16 |              166.55 |                942.04 |                972.47 |
| TPC-DS Q57    |             4367.94 |             4567.26 |                911.36 |               1069.90 |
| TPC-DS Q58    |             4652.95 |             4551.09 |                825.91 |                836.98 |
| TPC-DS Q59    |             6877.46 |             6896.27 |               1091.02 |               1148.08 |
| TPC-DS Q60    |              280.87 |              215.35 |                973.32 |                982.61 |
| TPC-DS Q61    |              277.04 |              266.59 |                300.72 |                281.26 |
| TPC-DS Q62    |             1348.75 |             1335.40 |               1072.77 |               1143.87 |
| TPC-DS Q63    |              101.33 |              100.00 |                534.07 |                808.24 |
| TPC-DS Q64    |              525.70 |              509.39 |               3168.06 |               3339.63 |
| TPC-DS Q65    |             4767.92 |             4408.83 |                636.83 |                691.00 |
| TPC-DS Q66    |             1005.92 |              939.76 |               1288.39 |               1292.56 |
| TPC-DS Q67    |             5891.42 |             5206.68 |               2885.98 |               2865.09 |
| TPC-DS Q68    |             2795.06 |             2387.15 |                410.20 |                255.91 |
| TPC-DS Q69    |              343.01 |              307.10 |               1021.40 |                853.14 |
| TPC-DS Q70    |             6192.99 |             6089.16 |                973.07 |                991.32 |
| TPC-DS Q71    |              400.23 |              358.04 |                467.65 |                432.57 |
| TPC-DS Q72    |              609.85 |              597.48 |               1239.76 |               1315.26 |
| TPC-DS Q73    |             2152.57 |             2103.66 |                265.26 |                271.30 |
| TPC-DS Q74    |             4589.21 |             4874.39 |                917.08 |                839.16 |
| TPC-DS Q75    |             4274.53 |             4039.88 |               1213.82 |               1356.78 |
| TPC-DS Q76    |              404.32 |              336.56 |                541.83 |                537.46 |
| TPC-DS Q77    |             5108.24 |             4695.13 |               1021.19 |               1195.02 |
| TPC-DS Q78    |             4869.05 |             4532.82 |               1655.94 |               1520.40 |
| TPC-DS Q79    |             2467.27 |             2390.14 |                711.61 |                817.85 |
| TPC-DS Q80    |              421.72 |              411.98 |               1135.21 |               1221.41 |
| TPC-DS Q81    |              155.34 |              154.49 |                872.69 |                816.30 |
| TPC-DS Q82    |             3263.73 |             2958.34 |                652.46 |                558.65 |
| TPC-DS Q83    |              739.57 |              729.35 |                807.13 |                834.87 |
| TPC-DS Q84    |               44.01 |               45.22 |                647.73 |                679.21 |
| TPC-DS Q85    |              125.44 |              112.80 |               2438.72 |               2518.94 |
| TPC-DS Q86    |              640.16 |              641.27 |                525.85 |                537.14 |
| TPC-DS Q87    |             5953.26 |             5443.06 |                730.63 |                778.27 |
| TPC-DS Q88    |            11658.47 |            10751.17 |               1234.77 |               1248.21 |
| TPC-DS Q89    |             1076.82 |             1080.96 |                656.99 |                623.75 |
| TPC-DS Q90    |              279.25 |              108.95 |                460.92 |                472.43 |
| TPC-DS Q91    |               15.79 |               15.79 |                942.82 |                887.72 |
| TPC-DS Q92    |                4.33 |                4.11 |                494.01 |                525.79 |
| TPC-DS Q93    |               34.56 |               32.35 |                491.61 |                515.02 |
| TPC-DS Q94    |              148.54 |              156.85 |               1011.23 |                999.60 |
| TPC-DS Q95    |              600.41 |              621.98 |               1042.58 |               1080.34 |
| TPC-DS Q96    |              632.67 |              500.52 |                528.96 |                522.94 |
| TPC-DS Q97    |             4586.68 |             4098.95 |                620.29 |                611.19 |
| TPC-DS Q98    |              687.49 |              701.37 |                562.94 |                543.23 |
| TPC-DS Q99    |             2520.19 |             2681.73 |               1101.86 |                916.61 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                     |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:--------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| mariadb-1-1-1-1-1   |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| mariadb-1-2-1-1-1   |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| mariadbcs-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       170.69 |      1.16 |           3.89 |                  4.01 |
| mariadbcs-1-1-1-1 |       153.60 |      1.18 |          10.38 |                 11.15 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |         0.99 |      0.02 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 |         1.15 |      0.02 |           0.01 |                  0.01 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |       268.83 |      1.00 |           4.33 |                  4.34 |
| mariadb-1-2-1-1   |       275.92 |      1.00 |           2.67 |                  2.67 |
| mariadbcs-1-1-1-1 |       833.68 |     11.00 |          20.86 |                 21.62 |
| mariadbcs-1-2-1-1 |       729.16 |     12.33 |          12.51 |                 12.70 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |        12.79 |      0.02 |           0.32 |                  0.33 |
| mariadb-1-2-1-1   |        12.80 |      0.34 |           0.30 |                  0.31 |
| mariadbcs-1-1-1-1 |        13.10 |      0.04 |           0.29 |                  0.30 |
| mariadbcs-1-2-1-1 |        12.37 |      0.30 |           0.29 |                  0.29 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* CPU User Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
