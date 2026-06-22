## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1093s 
* Code: 1782028616
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:253866
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782028616
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222479
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782028616
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251693
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782028616
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223763
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782028616

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
| MariaDB-1-1    |                1 |    1 |      316.00 |           1.00 |           19.00 |         42.00 |          251.00 |              8 |           0 |             | None           |             0 | False         |               11.39 |
| MonetDB-1-1    |                1 |    1 |      176.00 |           1.00 |           16.00 |         20.00 |          135.00 |              8 |           0 |             | None           |             0 | False         |               20.45 |
| MySQL-1-1      |                1 |    1 |      179.00 |           1.00 |           22.00 |         20.00 |          133.00 |              8 |           0 |             | None           |             0 | False         |               20.11 |
| PostgreSQL-1-1 |                1 |    1 |      166.00 |           2.00 |           18.00 |          8.00 |          135.00 |              8 |           0 |             |                |             0 | False         |               21.69 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |        105 |            1.40 |             2728.15 |            754.29 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |          9 |            0.10 |            42474.94 |           8800.00 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               22 |         53 |            1.07 |             3523.01 |           1494.34 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         16 |            0.32 |            12251.35 |           4950.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |        105 |            1.40 |             2728.15 |            754.29 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |          9 |            0.10 |            42474.94 |           8800.00 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               22 |         53 |            1.07 |             3523.01 |           1494.34 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         16 |            0.32 |            12251.35 |           4950.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             8839.76 |              592.68 |           8516.68 |                1204.42 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              557.04 |               25.67 |            134.28 |                 257.07 |
| Shipping Priority (TPC-H Q3)                        |             1664.01 |               79.08 |           1513.65 |                 317.41 |
| Order Priority Checking Query (TPC-H Q4)            |              329.21 |              128.16 |            444.23 |                 133.77 |
| Local Supplier Volume (TPC-H Q5)                    |              960.44 |               77.25 |           1022.32 |                 299.28 |
| Forecasting Revenue Change (TPC-H Q6)               |              835.14 |               22.11 |           1280.46 |                 205.52 |
| Volume Shipping Query (TPC-H Q7)                    |             1088.89 |               81.21 |           1871.63 |                 320.86 |
| National Market Share (TPC-H Q8)                    |             1899.40 |              143.20 |           2846.74 |                 205.50 |
| Product Type Profit Measure (TPC-H Q9)              |             2019.11 |               99.02 |           2101.36 |                 638.35 |
| Returned Item Reporting Query (TPC-H Q10)           |              878.57 |              173.28 |           1110.20 |                 514.98 |
| Important Stock Identification (TPC-H Q11)          |              123.98 |               19.87 |            167.66 |                  82.32 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3079.49 |               43.61 |           1959.80 |                 286.72 |
| Customer Distribution (TPC-H Q13)                   |             3194.48 |              256.84 |           3522.29 |                1071.28 |
| Promotion Effect Query (TPC-H Q14)                  |             1121.64 |               32.31 |           1462.59 |                 302.96 |
| Top Supplier Query (TPC-H Q15)                      |             1851.27 |               29.36 |          13287.77 |                 206.40 |
| Parts/Supplier Relationship (TPC-H Q16)             |              218.42 |               82.36 |            417.51 |                 241.78 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             8113.62 |               35.16 |            328.34 |                 597.11 |
| Large Volume Customer (TPC-H Q18)                   |             3011.91 |              109.20 |           1731.31 |                2974.97 |
| Discounted Revenue (TPC-H Q19)                      |             2374.88 |               57.96 |            141.32 |                  47.61 |
| Potential Part Promotion (TPC-H Q20)                |              236.65 |              106.54 |            258.95 |                 127.41 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            56735.67 |             2357.74 |           4606.37 |                 273.05 |
| Global Sales Opportunity Query (TPC-H Q22)          |              130.41 |               51.47 |            142.90 |                 100.87 |

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
