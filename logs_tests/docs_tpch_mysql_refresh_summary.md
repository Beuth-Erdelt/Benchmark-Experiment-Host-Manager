## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 569s 
* Code: 1793810082
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:888071
  * datadisk:34793
  * volume_size:1.8T
  * volume_used:868G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810082
* mysql-1-1-1-1-2 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:888071
  * datadisk:34793
  * volume_size:1.8T
  * volume_used:868G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810082
* mysql-1-1-1-1-3 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:888071
  * datadisk:34793
  * volume_size:1.8T
  * volume_used:868G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793810082

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793810082-6d67b4d94b-qtm95: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |    1 |       74.00 |           2.00 |           22.00 |         16.00 |           29.00 |              8 |           0 |             | None           |             0 | False         |               48.65 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| mysql-1-1-1-1-1 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         51 |            0.83 |             4314.39 |           1552.94 |          -1 | mysql-1-1-1-1-1 |
| mysql-1-1-1-1-2 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         49 |            0.85 |             4253.85 |           1616.33 |          -1 | mysql-1-1-1-1-2 |
| mysql-1-1-1-1-3 | MySQL-1         | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         51 |            0.84 |             4276.59 |           1552.94 |          -1 | mysql-1-1-1-1-3 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         51 |            0.84 |             4281.54 |           4658.82 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| mysql-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| mysql-1-1-1-2-1 | mysql-1-1-1 | mysql-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-04 17:42:51 | 2026-11-04 17:43:00 |                    9 |

### Latency of Timer Execution [ms]
| Queries                                             |   mysql-1-1-1-1-1 |   mysql-1-1-1-1-2 |   mysql-1-1-1-1-3 |
|:----------------------------------------------------|------------------:|------------------:|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           7241.92 |           6886.24 |           7255.07 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             80.55 |             78.01 |             81.09 |
| Shipping Priority (TPC-H Q3)                        |           1727.17 |           1570.48 |           1726.39 |
| Order Priority Checking Query (TPC-H Q4)            |            396.65 |            360.61 |            397.61 |
| Local Supplier Volume (TPC-H Q5)                    |           1243.33 |           1046.44 |           1243.15 |
| Forecasting Revenue Change (TPC-H Q6)               |            847.16 |            843.89 |            873.07 |
| Volume Shipping Query (TPC-H Q7)                    |            756.76 |            653.07 |            764.16 |
| National Market Share (TPC-H Q8)                    |           3229.64 |           3227.68 |           3267.49 |
| Product Type Profit Measure (TPC-H Q9)              |           2143.74 |           2173.71 |           2090.55 |
| Returned Item Reporting Query (TPC-H Q10)           |           1018.05 |           1019.56 |           1039.68 |
| Important Stock Identification (TPC-H Q11)          |            177.02 |            149.78 |            168.89 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1317.28 |           1353.53 |           1379.27 |
| Customer Distribution (TPC-H Q13)                   |           4092.78 |           3946.84 |           4138.00 |
| Promotion Effect Query (TPC-H Q14)                  |           1130.58 |           1139.02 |           1113.34 |
| Top Supplier Query (TPC-H Q15)                      |          16593.67 |          15613.32 |          16549.46 |
| Parts/Supplier Relationship (TPC-H Q16)             |            198.93 |            408.53 |            212.83 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            266.53 |            426.90 |            269.87 |
| Large Volume Customer (TPC-H Q18)                   |           1194.86 |           1470.86 |           1193.96 |
| Discounted Revenue (TPC-H Q19)                      |             82.86 |             78.02 |             84.39 |
| Potential Part Promotion (TPC-H Q20)                |            208.48 |            230.77 |            226.13 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           4794.50 |           3532.38 |           4869.78 |
| Global Sales Opportunity Query (TPC-H Q22)          |             88.37 |             87.30 |             84.02 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
