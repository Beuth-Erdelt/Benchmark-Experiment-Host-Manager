## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1060s 
* Code: 1793487653
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB', 'MariaDBCS'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type nvme and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:749051
  * datadisk:1962
  * volume_size:20G
  * volume_used:2.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653
* mariadb-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:546583
  * datadisk:1963
  * volume_size:20G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653
* mariadbcs-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:748673
  * datadisk:512
  * volume_size:20G
  * volume_used:673M
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653
* mariadbcs-1-2-1-1-1 uses docker image mariadb:12.3.3
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:545337
  * datadisk:511
  * volume_size:20G
  * volume_used:673M
  * cpu_list:0-127
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793487653

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: MariaDB-1-2, MariaDBCS-1-2

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: engine=InnoDB, histograms=off
* MariaDB-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics
* MariaDBCS-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793487653-59778bb9cf-lsf5s: 0
* bexhoma-sut-mariadb-1-1793487653-9f7cc4758-tctfz: 0
* bexhoma-sut-mariadbcs-1-1793487653-7764779dc-f6t7q: 0
* bexhoma-sut-mariadbcs-1-1793487653-5d8d5866b-89nk5: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDBCS-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|               |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:--------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1   |                1 |    1 |       84.00 |           6.00 |           12.00 |         20.00 |           36.00 |              8 |           0 |             | None           |             0 | False         |               42.86 | False               |
| MariaDB-1-2   |                2 |    1 |       84.00 |           6.00 |           12.00 |         20.00 |           36.00 |              8 |           0 |             | None           |             0 | False         |               42.86 | True                |
| MariaDBCS-1-1 |                1 |    1 |      100.00 |          10.00 |            0.00 |         65.00 |           19.00 |              1 |           0 |             | None           |             0 | False         |               36.00 | False               |
| MariaDBCS-1-2 |                2 |    1 |      100.00 |          10.00 |            0.00 |         65.00 |           19.00 |              1 |           0 |             | None           |             0 | False         |               36.00 | True                |

### Benchmarking

#### Per Connection

| DBMS                | configuration   | phase           | job               |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                 |
|:--------------------|:----------------|:----------------|:------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:--------------------|
| mariadb-1-1-1-1-1   | MariaDB-1       | mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         94 |            0.99 |             3713.88 |            842.55 |          -1 | mariadb-1-1-1-1-1   |
| mariadb-1-2-1-1-1   | MariaDB-1       | mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         89 |            0.94 |             4121.25 |            889.89 |          -1 | mariadb-1-2-1-1-1   |
| mariadbcs-1-1-1-1-1 | MariaDBCS-1     | mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         24 |            0.71 |             5272.56 |           3300.00 |          -1 | mariadbcs-1-1-1-1-1 |
| mariadbcs-1-2-1-1-1 | MariaDBCS-1     | mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         32 |            0.99 |             3672.97 |           2475.00 |          -1 | mariadbcs-1-2-1-1-1 |

#### Per Phase

|                 | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1   | mariadb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         94 |            0.99 |             3713.88 |            842.55 |          -1 |
| mariadb-1-2-1   | mariadb-1-2-1   |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         89 |            0.94 |             4121.25 |            889.89 |          -1 |
| mariadbcs-1-1-1 | mariadbcs-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         24 |            0.71 |             5272.56 |           3300.00 |          -1 |
| mariadbcs-1-2-1 | mariadbcs-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         32 |            0.99 |             3672.97 |           2475.00 |          -1 |

#### Query Completion per Phase

| phase           |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mariadb-1-1-1   |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadb-1-2-1   |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadbcs-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mariadbcs-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| mariadb-1-1-1   | mariadb-1-1-1-1   |                1 |        1 |               1 |         5.00 |                |
| mariadb-1-2-1   | mariadb-1-2-1-1   |                2 |        1 |               1 |         4.00 |                |
| mariadbcs-1-1-1 | mariadbcs-1-1-1-1 |                1 |        1 |               1 |         5.00 |                |
| mariadbcs-1-2-1 | mariadbcs-1-2-1-1 |                2 |        1 |               1 |         6.00 |                |

### Latency of Timer Execution [ms]
| Queries                                             |   mariadb-1-1-1-1-1 |   mariadb-1-2-1-1-1 |   mariadbcs-1-1-1-1-1 |   mariadbcs-1-2-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|----------------------:|----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             6696.95 |             7779.54 |                982.33 |               1435.12 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              398.59 |              438.20 |               2748.69 |               3029.67 |
| Shipping Priority (TPC-H Q3)                        |             2403.78 |             1403.04 |               1244.10 |               1572.55 |
| Order Priority Checking Query (TPC-H Q4)            |              315.58 |              414.60 |                445.11 |                955.26 |
| Local Supplier Volume (TPC-H Q5)                    |              802.55 |              840.57 |                675.43 |                877.49 |
| Forecasting Revenue Change (TPC-H Q6)               |              776.85 |              853.83 |                 46.60 |                 65.75 |
| Volume Shipping Query (TPC-H Q7)                    |             1432.54 |              978.74 |               1391.23 |               1361.85 |
| National Market Share (TPC-H Q8)                    |             1498.65 |             1578.94 |                841.08 |                949.96 |
| Product Type Profit Measure (TPC-H Q9)              |             1766.16 |             1576.30 |               1054.60 |               1493.85 |
| Returned Item Reporting Query (TPC-H Q10)           |              707.92 |              712.54 |                842.14 |               1387.22 |
| Important Stock Identification (TPC-H Q11)          |              103.56 |              106.50 |                754.39 |                943.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3069.94 |             2503.49 |                415.11 |               1042.15 |
| Customer Distribution (TPC-H Q13)                   |             2641.26 |             2416.61 |               1112.14 |               2175.47 |
| Promotion Effect Query (TPC-H Q14)                  |            10447.27 |             9623.03 |                300.90 |                659.25 |
| Top Supplier Query (TPC-H Q15)                      |             2441.82 |             1754.10 |                392.21 |                492.35 |
| Parts/Supplier Relationship (TPC-H Q16)             |              471.55 |              159.33 |                739.61 |                931.59 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               49.36 |               44.80 |                692.49 |               1094.92 |
| Large Volume Customer (TPC-H Q18)                   |             2500.83 |             2466.37 |                747.91 |               1088.62 |
| Discounted Revenue (TPC-H Q19)                      |               85.27 |               73.41 |                436.88 |                558.38 |
| Potential Part Promotion (TPC-H Q20)                |              215.13 |              169.96 |               1375.86 |               1140.60 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            51258.72 |            47935.68 |               1268.81 |               1891.17 |
| Global Sales Opportunity Query (TPC-H Q22)          |              126.85 |              180.47 |                384.89 |                685.14 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   |        93.59 |      2.38 |           1.68 |                  1.69 |
| mariadbcs-1-1-1-1 |        77.75 |      1.49 |           3.65 |                  4.28 |

### Loading phase: component data generator

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | n/a          |      0.00 |           0.01 |                  0.01 |
| mariadbcs-1-1-1-1 | 1.07         |      0.02 |           0.01 |                  0.73 |

### Benchmarking phase: SUT deployment

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | 87.10        |      1.00 |           2.04 |                  2.05 |
| mariadb-1-2-1-1   | 72.30        |      1.00 |           1.88 |                  1.88 |
| mariadbcs-1-1-1-1 | n/a          |      0.17 |           5.20 |                  5.90 |
| mariadbcs-1-2-1-1 | n/a          |      2.17 |           4.28 |                  4.47 |

### Benchmarking phase: component benchmarker

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1   | 11.46        |      0.35 |           0.30 |                  0.30 |
| mariadb-1-2-1-1   | 15.37        |      0.10 |           0.32 |                  0.32 |
| mariadbcs-1-1-1-1 | n/a          |      0.00 |           0.35 |                  0.35 |
| mariadbcs-1-2-1-1 | n/a          |      0.41 |           0.32 |                  0.32 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection mariadbcs-1-1-1-1 (bexhoma-metrics-mariadbcs-1-1-1-1-datagenerator.log, expected: data pre-existing)
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
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
* TEST passed: Reset scripts ran without errors
