## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 656s 
* Code: 1795529289
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1107520
  * datadisk:34809
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529289
    * TENANT_BY:container
    * TENANT_NUM:2
* mysql-1-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1108351
  * datadisk:34809
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529289
    * TENANT_BY:container
    * TENANT_NUM:2
* mysql-2-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1107520
  * datadisk:34825
  * volume_size:49G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529289
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* mysql-2-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1108351
  * datadisk:34825
  * volume_size:49G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795529289
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Ingestion
* MySQL-1: 8 of 8 units ok
* MySQL-2: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1795529289-78df99c8cc-n2bnx: 0
* bexhoma-sut-mysql-2-1795529289-868dd65566-9h8s6: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 2: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                        |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads |   Throughput [SF/h] | loading_inherited   |
|:-----------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|--------------------:|:--------------------|
| 1795529289-MySQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |      123.00 |           3.00 |            0.00 |         56.00 |           52.00 |              1 |         0 |               29.27 | False               |
| 1795529289-MySQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |      113.00 |           2.00 |            0.00 |         57.00 |           53.00 |              1 |         0 |               31.86 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         52 |            0.85 |             4214.34 |           1523.08 |           0 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         45 |            0.74 |             4841.38 |           1760.00 |           0 |
| mysql-2-1-1-1-1 | mysql-2-1-1 | mysql-2-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         52 |            0.99 |             3647.10 |           1523.08 |           1 |
| mysql-2-1-2-1-1 | mysql-2-1-2 | mysql-2-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         47 |            0.82 |             4382.40 |           1685.11 |           1 |

#### Per Phase

| DBMS          | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1_0 | mysql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         52 |            0.85 |             4214.34 |           1523.08 |           0 |
| mysql-1-1-2_0 | mysql-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         45 |            0.74 |             4841.38 |           1760.00 |           0 |
| mysql-2-1-1_1 | mysql-2-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         52 |            0.99 |             3647.10 |           1523.08 |           1 |
| mysql-2-1-2_1 | mysql-2-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |                  22 |         47 |            0.82 |             4382.40 |           1685.11 |           1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mysql-1-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mysql-2-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| mysql-2-1-2 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |   mysql-1-1-2-1-1 |   mysql-2-1-1-1-1 |   mysql-2-1-2-1-1 |
|:----------------------------------------------------|------------------:|------------------:|------------------:|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           7430.64 |           5980.91 |           7646.70 |           5979.31 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             87.07 |             65.21 |             79.39 |             73.41 |
| Shipping Priority (TPC-H Q3)                        |           1638.63 |            861.14 |           1516.47 |           1133.48 |
| Order Priority Checking Query (TPC-H Q4)            |            322.47 |            299.17 |            347.63 |            340.25 |
| Local Supplier Volume (TPC-H Q5)                    |            893.06 |            731.61 |            836.08 |            814.41 |
| Forecasting Revenue Change (TPC-H Q6)               |            810.20 |            784.10 |            885.97 |           1101.43 |
| Volume Shipping Query (TPC-H Q7)                    |            657.29 |            764.55 |           2594.41 |           1742.65 |
| National Market Share (TPC-H Q8)                    |           2270.06 |           2237.96 |           2079.85 |           2138.82 |
| Product Type Profit Measure (TPC-H Q9)              |           5517.81 |           1544.12 |           5909.26 |           1881.79 |
| Returned Item Reporting Query (TPC-H Q10)           |            923.40 |           1436.67 |           1552.98 |            936.98 |
| Important Stock Identification (TPC-H Q11)          |            150.87 |            130.18 |            211.06 |            292.82 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1823.86 |           1176.23 |           1474.66 |           2024.82 |
| Customer Distribution (TPC-H Q13)                   |           2349.99 |           3912.76 |           2557.57 |           2787.78 |
| Promotion Effect Query (TPC-H Q14)                  |            974.90 |           1048.75 |           1204.93 |           1565.32 |
| Top Supplier Query (TPC-H Q15)                      |          15100.64 |          11494.49 |          14262.18 |          10804.16 |
| Parts/Supplier Relationship (TPC-H Q16)             |            228.20 |            219.39 |            412.06 |            252.79 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            219.39 |            194.16 |            231.59 |            191.85 |
| Large Volume Customer (TPC-H Q18)                   |           1190.90 |           1158.41 |           1199.27 |           1787.08 |
| Discounted Revenue (TPC-H Q19)                      |            166.23 |             86.07 |            198.75 |             91.41 |
| Potential Part Promotion (TPC-H Q20)                |            481.61 |            211.80 |            643.12 |            192.51 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           4092.72 |           3773.99 |           3323.88 |           3288.00 |
| Global Sales Opportunity Query (TPC-H Q22)          |             89.31 |            275.30 |             96.22 |             94.44 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
