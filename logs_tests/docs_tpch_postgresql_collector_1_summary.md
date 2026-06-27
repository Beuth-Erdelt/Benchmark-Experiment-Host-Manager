## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1304s 
* Code: 1781936763
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type cephcsi and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297521
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781936763
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297513
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781936763
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297513
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781936763
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297515
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781936763
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297513
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781936763
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297513
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781936763

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      325.00 |           1.00 |           22.00 |         88.00 |          211.00 |              8 |           0 |             |                |             0 | False         |               33.23 |
| PostgreSQL-1-2 |                2 |    3 |      325.00 |           1.00 |           22.00 |         88.00 |          211.00 |              8 |           0 |             |                |             0 | False         |               33.23 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.63 |            17216.26 |           9504.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         24 |            0.57 |            19106.25 |           9900.00 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.62 |            17414.47 |           9504.00 |           0 | PostgreSQL-1-1-2-1-2 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        137 |            1.37 |             7885.59 |           1734.31 |           0 | PostgreSQL-1-2-1-1-1 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.62 |            17501.71 |           9504.00 |           0 | PostgreSQL-1-2-2-1-1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.62 |            17434.08 |           9504.00 |           0 | PostgreSQL-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.63 |            17216.26 |           9504.00 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 3.00 |               44 |         25 |            0.59 |            18240.76 |          19008.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        137 |            1.37 |             7885.59 |           1734.31 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 3.00 |               44 |         25 |            0.62 |            17467.87 |          19008.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1647.15 |                1661.82 |                1733.12 |               50884.55 |                1764.28 |                1730.56 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 551.36 |                 532.51 |                 559.45 |               23309.64 |                 526.40 |                 643.84 |
| Shipping Priority (TPC-H Q3)                        |                 578.44 |                 556.64 |                 561.55 |               26269.00 |                 566.39 |                 547.92 |
| Order Priority Checking Query (TPC-H Q4)            |                 244.97 |                 251.67 |                 272.93 |                 269.92 |                 273.97 |                 297.34 |
| Local Supplier Volume (TPC-H Q5)                    |                 547.38 |                 510.80 |                 581.81 |                1287.31 |                 603.32 |                 782.24 |
| Forecasting Revenue Change (TPC-H Q6)               |                 311.68 |                 314.25 |                 303.54 |                 295.46 |                 306.70 |                 596.46 |
| Forecasting Revenue Change (TPC-H Q7)               |                 723.06 |                 708.40 |                 724.90 |                 742.00 |                 896.86 |                 978.48 |
| National Market Share (TPC-H Q8)                    |                 395.91 |                 350.56 |                 345.03 |               10641.88 |                 585.62 |                 389.34 |
| Product Type Profit Measure (TPC-H Q9)              |                1002.44 |                 963.96 |                1015.01 |                4833.17 |                1208.46 |                1115.92 |
| Forecasting Revenue Change (TPC-H Q10)              |                1223.90 |                1172.77 |                1175.42 |                1245.66 |                1175.16 |                1259.75 |
| Important Stock Identification (TPC-H Q11)          |                 189.39 |                 214.63 |                 189.66 |                 192.21 |                 189.35 |                 182.25 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 481.08 |                 491.66 |                 489.63 |                 494.60 |                 529.13 |                 441.36 |
| Customer Distribution (TPC-H Q13)                   |                1983.57 |                2548.29 |                2445.71 |                2654.36 |                2021.08 |                2712.02 |
| Forecasting Revenue Change (TPC-H Q14)              |                 537.82 |                 545.85 |                 539.50 |                 709.60 |                1029.95 |                 555.57 |
| Top Supplier Query (TPC-H Q15)                      |                 419.93 |                 412.79 |                 418.60 |                 477.55 |                 481.13 |                 417.18 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 403.80 |                 394.39 |                 405.32 |                 433.49 |                 441.06 |                 434.73 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1678.46 |                1626.51 |                1724.15 |                1885.74 |                1512.10 |                1467.24 |
| Large Volume Customer (TPC-H Q18)                   |                8459.44 |                8765.12 |                9435.53 |                8035.92 |                7944.65 |                7642.19 |
| Discounted Revenue (TPC-H Q19)                      |                 237.18 |                  87.19 |                 160.95 |                 119.12 |                  86.10 |                  97.02 |
| Potential Part Promotion (TPC-H Q20)                |                 796.92 |                 282.46 |                 716.77 |                 965.96 |                 345.04 |                 323.76 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 736.25 |                 554.57 |                 582.79 |                 522.87 |                 543.17 |                 523.63 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 139.57 |                 136.33 |                 153.00 |                 196.83 |                 143.05 |                 144.56 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        97.08 |      1.18 |           5.16 |                  9.41 |
| PostgreSQL-1-1-2-1 |        97.08 |      1.18 |           5.16 |                  9.41 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        35.30 |      0.55 |           0.00 |                  0.39 |
| PostgreSQL-1-1-2-1 |        35.30 |      0.55 |           0.00 |                  0.39 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        11.43 |      0.36 |           4.34 |                  8.59 |
| PostgreSQL-1-1-2-1 |        85.24 |      3.10 |           5.04 |                  9.29 |
| PostgreSQL-1-2-1-1 |       384.88 |      0.35 |           4.89 |                  9.57 |
| PostgreSQL-1-2-2-1 |        34.93 |      1.19 |           4.93 |                  9.28 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-1-1 |        11.60 |      0.32 |           0.25 |                  0.25 |
| PostgreSQL-1-2-2-1 |        25.11 |      0.00 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    8.00 |
| PostgreSQL-1-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-1-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-1-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
