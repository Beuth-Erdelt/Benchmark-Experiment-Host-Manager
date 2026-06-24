## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 991s 
* Code: 1782218791
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:257486
  * datadisk:2105
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782218791
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225232
  * datadisk:2209
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782218791
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:294248
  * datadisk:35543
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782218791
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:226003
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782218791

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1    |                1 |    1 |      277.00 |           0.00 |           14.00 |         38.00 |          221.00 |              8 |           0 |             | None           |             0 | False         |               13.00 |
| MonetDB-1-1    |                1 |    1 |      139.00 |           1.00 |           19.00 |         21.00 |           95.00 |              8 |           0 |             | None           |             0 | False         |               25.90 |
| MySQL-1-1      |                1 |    1 |      141.00 |           0.00 |           20.00 |         19.00 |           99.00 |              8 |           0 |             | None           |             0 | False         |               25.53 |
| PostgreSQL-1-1 |                1 |    1 |      158.00 |           1.00 |           25.00 |          6.00 |          123.00 |              8 |           0 |             |                |             0 | False         |               22.78 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |        111 |            1.19 |             3243.50 |            713.51 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |          7 |            0.09 |            45483.66 |          11314.29 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               22 |         54 |            1.09 |             3453.26 |           1466.67 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.33 |            11731.82 |           5280.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |        111 |            1.19 |             3243.50 |            713.51 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |          7 |            0.09 |            45483.66 |          11314.29 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               22 |         54 |            1.09 |             3453.26 |           1466.67 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.33 |            11731.82 |           5280.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             9410.23 |              600.40 |           8486.49 |                1143.17 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              496.57 |               24.62 |            123.07 |                 266.38 |
| Shipping Priority (TPC-H Q3)                        |             1607.02 |               73.80 |           1688.02 |                 370.30 |
| Order Priority Checking Query (TPC-H Q4)            |              354.87 |              124.35 |            503.11 |                 166.53 |
| Local Supplier Volume (TPC-H Q5)                    |             1012.69 |               75.50 |           1076.80 |                 304.04 |
| Forecasting Revenue Change (TPC-H Q6)               |             1350.33 |               20.63 |           1303.66 |                 181.89 |
| Volume Shipping Query (TPC-H Q7)                    |             1402.60 |               73.69 |           2124.21 |                 342.41 |
| National Market Share (TPC-H Q8)                    |             1997.77 |              145.08 |           3007.50 |                 202.50 |
| Product Type Profit Measure (TPC-H Q9)              |             2155.24 |               99.77 |           2231.08 |                 908.93 |
| Returned Item Reporting Query (TPC-H Q10)           |              954.31 |              167.71 |           1027.85 |                 527.60 |
| Important Stock Identification (TPC-H Q11)          |              170.90 |               19.32 |            183.62 |                  74.38 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3485.41 |               40.27 |           1961.50 |                 278.61 |
| Customer Distribution (TPC-H Q13)                   |             3313.35 |              253.28 |           3382.60 |                 771.75 |
| Promotion Effect Query (TPC-H Q14)                  |            13727.58 |               31.14 |           1467.40 |                 206.72 |
| Top Supplier Query (TPC-H Q15)                      |             1874.13 |               28.21 |          13328.29 |                 231.78 |
| Parts/Supplier Relationship (TPC-H Q16)             |              230.49 |               79.98 |            405.83 |                 293.15 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               58.97 |               35.50 |            292.00 |                 755.48 |
| Large Volume Customer (TPC-H Q18)                   |             3085.11 |              105.68 |           1749.95 |                3188.04 |
| Discounted Revenue (TPC-H Q19)                      |              100.70 |               55.12 |            138.36 |                  55.10 |
| Potential Part Promotion (TPC-H Q20)                |              296.01 |               88.74 |            270.32 |                 140.95 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            58885.47 |             1268.10 |           5166.55 |                 331.03 |
| Global Sales Opportunity Query (TPC-H Q22)          |              126.34 |               47.89 |            143.43 |                 107.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
