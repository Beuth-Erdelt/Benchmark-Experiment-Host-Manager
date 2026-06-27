## Show Summary

### Workload
TPC-H Queries SF=6
* Type: tpch
* Duration: 1618s 
* Code: 1781938146
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=6) data is loaded and benchmark is executed.
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
  * disk:1297683
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781938146
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297694
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781938146
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1297694
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781938146
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1298572
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781938146
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1298581
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781938146
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1298581
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781938146

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
| PostgreSQL-1-1 |                1 |    6 |      627.00 |           1.00 |           19.00 |        178.00 |          425.00 |              8 |           0 |             |                |             0 | False         |               34.45 |
| PostgreSQL-1-2 |                2 |    6 |      627.00 |           1.00 |           19.00 |        178.00 |          425.00 |              8 |           0 |             |                |             0 | False         |               34.45 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 6.00 |               22 |         56 |            1.45 |            14855.57 |           8485.71 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 6.00 |               22 |         56 |            1.34 |            16078.96 |           8485.71 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 6.00 |               22 |         58 |            1.36 |            15896.36 |           8193.10 |           0 | PostgreSQL-1-1-2-1-2 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 6.00 |               22 |        210 |            2.50 |             8649.36 |           2262.86 |           0 | PostgreSQL-1-2-1-1-1 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 6.00 |               22 |         57 |            1.33 |            16223.16 |           8336.84 |           0 | PostgreSQL-1-2-2-1-1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 6.00 |               22 |         57 |            1.33 |            16188.27 |           8336.84 |           0 | PostgreSQL-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 6.00 |               22 |         56 |            1.45 |            14855.57 |           8485.71 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 6.00 |               44 |         58 |            1.35 |            15987.40 |          16386.21 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 6.00 |               22 |        210 |            2.50 |             8649.36 |           2262.86 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 6.00 |               44 |         57 |            1.33 |            16205.71 |          16673.68 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                3016.79 |                4091.84 |                4013.31 |               60828.99 |                3520.24 |                3571.66 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                1561.73 |                1240.14 |                1322.00 |               50708.50 |                1514.80 |                1548.39 |
| Shipping Priority (TPC-H Q3)                        |                1753.05 |                1898.66 |                1739.94 |               31297.06 |                1343.78 |                1263.90 |
| Order Priority Checking Query (TPC-H Q4)            |                 559.98 |                 596.29 |                 677.99 |                 539.80 |                 470.57 |                 432.46 |
| Local Supplier Volume (TPC-H Q5)                    |                1476.87 |                1350.08 |                1458.59 |                2222.72 |                1569.13 |                1569.43 |
| Forecasting Revenue Change (TPC-H Q6)               |                 814.20 |                 737.40 |                 705.72 |                 745.00 |                 718.25 |                 690.46 |
| Forecasting Revenue Change (TPC-H Q7)               |                1817.20 |                1773.69 |                1773.37 |                1840.41 |                2227.21 |                2227.66 |
| National Market Share (TPC-H Q8)                    |                1354.38 |                 704.46 |                 704.58 |               17946.89 |                 700.49 |                 699.93 |
| Product Type Profit Measure (TPC-H Q9)              |                2391.18 |                3173.32 |                2929.13 |                6498.09 |                2502.37 |                2502.50 |
| Forecasting Revenue Change (TPC-H Q10)              |                1488.87 |                1639.54 |                1669.58 |                1582.34 |                1889.91 |                1721.65 |
| Important Stock Identification (TPC-H Q11)          |                 465.53 |                 385.72 |                 434.02 |                 375.09 |                 430.14 |                 470.95 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1114.34 |                1145.46 |                1078.53 |                1013.13 |                1010.14 |                1022.19 |
| Customer Distribution (TPC-H Q13)                   |                4774.35 |                5683.02 |                5655.63 |                3904.57 |                4126.29 |                4201.57 |
| Forecasting Revenue Change (TPC-H Q14)              |                1666.58 |                1120.14 |                1203.65 |                1083.11 |                1713.87 |                1718.61 |
| Top Supplier Query (TPC-H Q15)                      |                1027.90 |                1057.61 |                 965.63 |                 868.89 |                 896.65 |                 884.36 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 660.60 |                 703.46 |                 686.93 |                 694.69 |                 707.20 |                 683.10 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                4320.87 |                3645.67 |                3621.78 |                3339.57 |                3520.88 |                3715.73 |
| Large Volume Customer (TPC-H Q18)                   |               20458.67 |               19819.71 |               21599.11 |               18221.10 |               23183.37 |               21899.78 |
| Discounted Revenue (TPC-H Q19)                      |                 194.59 |                 176.46 |                 189.07 |                 258.66 |                 188.53 |                 191.36 |
| Potential Part Promotion (TPC-H Q20)                |                2095.44 |                2041.92 |                2181.72 |                3592.98 |                2029.31 |                2360.05 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                2011.98 |                1308.63 |                1271.14 |                1243.41 |                1244.47 |                1213.93 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 380.67 |                 249.42 |                 249.04 |                 277.65 |                 255.85 |                 276.32 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       267.80 |      1.85 |           3.41 |                 12.35 |
| PostgreSQL-1-1-2-1 |       267.80 |      1.85 |           3.41 |                 12.35 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        74.43 |      0.80 |           0.01 |                  0.78 |
| PostgreSQL-1-1-2-1 |        74.43 |      0.80 |           0.01 |                  0.78 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        50.35 |      1.66 |           8.65 |                 17.59 |
| PostgreSQL-1-1-2-1 |       438.49 |      8.50 |          16.03 |                 35.03 |
| PostgreSQL-1-2-1-1 |      1057.12 |      2.77 |          15.82 |                 27.65 |
| PostgreSQL-1-2-2-1 |       189.90 |      6.54 |           9.28 |                 17.96 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        12.15 |      0.01 |           0.30 |                  0.30 |
| PostgreSQL-1-1-2-1 |        26.64 |      0.02 |           0.30 |                  0.30 |
| PostgreSQL-1-2-1-1 |        12.14 |      0.01 |           0.26 |                  0.27 |
| PostgreSQL-1-2-2-1 |        26.29 |      0.81 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-2-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-1-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   12.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
