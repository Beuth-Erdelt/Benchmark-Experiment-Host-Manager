## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2094s 
* Code: 1782315238
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223912
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782315238
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220626
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782315238
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220626
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782315238
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225205
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782315238
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:224991
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782315238
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:224991
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782315238

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
| PostgreSQL-1-1 |                1 |   10 |     1008.00 |           2.00 |           19.00 |        277.00 |          705.00 |              8 |           0 |             |                |             0 | False         |               35.71 |
| PostgreSQL-1-2 |                2 |   10 |     1008.00 |           2.00 |           19.00 |        277.00 |          705.00 |              8 |           0 |             |                |             0 | False         |               35.71 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        101 |            2.63 |            14113.38 |           7841.58 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               22 |         99 |            2.55 |            14541.44 |           8000.00 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               22 |         99 |            2.54 |            14596.84 |           8000.00 |           0 | PostgreSQL-1-1-2-1-2 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |        240 |            4.03 |             9166.49 |           3300.00 |           0 | PostgreSQL-1-2-1-1-1 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               22 |         97 |            2.47 |            15098.62 |           8164.95 |           0 | PostgreSQL-1-2-2-1-1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               22 |         96 |            2.45 |            15072.55 |           8250.00 |           0 | PostgreSQL-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        101 |            2.63 |            14113.38 |           7841.58 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 10.00 |               44 |         99 |            2.54 |            14569.11 |          16000.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |        240 |            4.03 |             9166.49 |           3300.00 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 10.00 |               44 |         97 |            2.46 |            15085.58 |          16329.90 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                7265.35 |                6883.17 |                6356.98 |               58163.00 |                6383.05 |                6454.54 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2942.27 |                3407.16 |                2728.04 |               53573.19 |                2558.33 |                2454.21 |
| Shipping Priority (TPC-H Q3)                        |                3679.87 |                2528.13 |                2475.11 |               28619.98 |                2560.64 |                2387.51 |
| Order Priority Checking Query (TPC-H Q4)            |                1183.94 |                 970.40 |                1041.30 |                1161.51 |                 898.46 |                 984.96 |
| Local Supplier Volume (TPC-H Q5)                    |                2579.37 |                2646.60 |                2487.81 |                4344.24 |                2486.40 |                2563.60 |
| Forecasting Revenue Change (TPC-H Q6)               |                1439.99 |                1262.17 |                1258.57 |                1491.26 |                1290.07 |                1290.45 |
| Volume Shipping Query (TPC-H Q7)                    |                2332.35 |                2420.15 |                2363.83 |                2539.08 |                2326.79 |                2309.48 |
| National Market Share (TPC-H Q8)                    |                1515.84 |                1298.86 |                1238.07 |               11476.68 |                1233.08 |                1248.30 |
| Product Type Profit Measure (TPC-H Q9)              |                5741.53 |                5980.13 |                5806.17 |                6081.35 |                5965.30 |                5878.13 |
| Returned Item Reporting Query (TPC-H Q10)           |                2578.71 |                2480.86 |                2438.25 |                2383.17 |                2266.10 |                2383.57 |
| Important Stock Identification (TPC-H Q11)          |                 962.44 |                 930.30 |                 994.12 |                 783.09 |                 949.85 |                 911.59 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                2236.54 |                2033.97 |                2132.50 |                1983.06 |                2008.84 |                1884.45 |
| Customer Distribution (TPC-H Q13)                   |               14578.32 |               12999.88 |               11892.73 |               13663.58 |               12661.67 |               12302.55 |
| Promotion Effect Query (TPC-H Q14)                  |                2034.84 |                2107.32 |                1958.95 |                2041.19 |                1971.53 |                1926.86 |
| Top Supplier Query (TPC-H Q15)                      |                1965.43 |                1962.46 |                1994.31 |                1975.47 |                1908.92 |                1978.26 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1439.91 |                1485.18 |                1774.10 |                1657.61 |                1426.37 |                1520.09 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                6977.52 |                7655.93 |                7889.10 |                7015.79 |                7412.76 |                7570.10 |
| Large Volume Customer (TPC-H Q18)                   |               25332.67 |               25586.93 |               26858.73 |               26489.26 |               25373.60 |               25407.28 |
| Discounted Revenue (TPC-H Q19)                      |                 318.59 |                 312.46 |                 332.33 |                 318.35 |                 315.32 |                 310.90 |
| Potential Part Promotion (TPC-H Q20)                |                3830.77 |                3902.83 |                4358.24 |                3863.18 |                3868.55 |                4126.25 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                2641.82 |                2977.68 |                2968.99 |                2707.53 |                2823.34 |                2823.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 474.38 |                 475.94 |                 456.73 |                 472.57 |                 510.52 |                 490.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       747.58 |      2.46 |           6.11 |                 24.06 |
| PostgreSQL-1-1-2-1 |       747.58 |      2.46 |           6.11 |                 24.06 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       126.80 |      1.03 |           0.01 |                  1.30 |
| PostgreSQL-1-1-2-1 |       126.80 |      1.03 |           0.01 |                  1.30 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       311.06 |      5.79 |          16.96 |                 33.88 |
| PostgreSQL-1-1-2-1 |       600.38 |     11.63 |          18.66 |                 36.58 |
| PostgreSQL-1-2-1-1 |      1790.69 |      3.51 |          15.78 |                 31.29 |
| PostgreSQL-1-2-2-1 |       601.35 |     12.14 |          16.69 |                 31.92 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        16.98 |      0.14 |           0.36 |                  0.37 |
| PostgreSQL-1-1-2-1 |        34.73 |      1.15 |           0.36 |                  0.37 |
| PostgreSQL-1-2-1-1 |        17.41 |      0.15 |           0.36 |                  0.37 |
| PostgreSQL-1-2-2-1 |        34.85 |      1.00 |           0.36 |                  0.37 |

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
