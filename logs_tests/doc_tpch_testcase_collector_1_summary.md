## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1614s 
* Code: 1778707559
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.7.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197634
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778707559
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197634
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778707559
* PostgreSQL-1-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197634
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778707559
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197635
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778707559
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197635
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778707559
* PostgreSQL-1-2-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197635
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778707559

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      484.00 |           3.00 |           19.00 |        120.00 |          338.00 |              8 |           0 |          |                |             0 | False         |               22.31 |
| PostgreSQL-1-2 |                2 |    3 |      484.00 |           3.00 |           19.00 |        120.00 |          338.00 |              8 |           0 |          |                |             0 | False         |               22.31 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      30.00 |            0.77 |            14018.12 |           7920.00 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.77 |            13970.92 |           8193.10 |
| PostgreSQL-1-1-2-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.77 |            14068.53 |           8193.10 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      90.00 |            1.35 |             7970.50 |           2640.00 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.78 |            13906.69 |           8193.10 |
| PostgreSQL-1-2-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.76 |            14243.48 |           8193.10 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      30.00 |            0.77 |            14018.12 |           7920.00 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.77 |            14019.64 |          16386.21 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      90.00 |            1.35 |             7970.50 |           2640.00 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.77 |            14074.07 |          16386.21 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-1-2-2 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-2-1 |   PostgreSQL-1-2-2-2 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              2528.19 |              2403.91 |              2454.00 |             26432.30 |              2451.12 |              2454.22 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               670.84 |               621.85 |               681.12 |             15605.59 |               716.90 |               700.17 |
| Shipping Priority (TPC-H Q3)                        |              1183.88 |              1164.21 |              1124.71 |             17777.85 |              1135.01 |              1135.50 |
| Order Priority Checking Query (TPC-H Q4)            |               395.52 |               391.07 |               370.61 |               615.73 |               380.87 |               380.85 |
| Local Supplier Volume (TPC-H Q5)                    |               812.32 |               760.38 |               794.72 |              1507.69 |               760.40 |               762.92 |
| Forecasting Revenue Change (TPC-H Q6)               |               457.68 |               459.62 |               438.01 |               650.30 |               442.98 |               429.33 |
| Forecasting Revenue Change (TPC-H Q7)               |               977.26 |               942.08 |               961.41 |              1304.67 |               999.28 |               933.35 |
| National Market Share (TPC-H Q8)                    |               507.91 |               447.78 |               466.79 |              4254.49 |               451.82 |               406.10 |
| Product Type Profit Measure (TPC-H Q9)              |              1337.51 |              1346.22 |              1327.42 |              1481.98 |              1363.55 |              1409.31 |
| Forecasting Revenue Change (TPC-H Q10)              |              1413.84 |              1541.00 |              1402.77 |              1352.01 |              1311.09 |              1403.65 |
| Important Stock Identification (TPC-H Q11)          |               260.90 |               305.01 |               303.50 |               253.93 |               254.94 |               258.21 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               668.25 |               638.54 |               620.01 |               633.16 |               653.04 |               679.49 |
| Customer Distribution (TPC-H Q13)                   |              2495.60 |              3001.83 |              2952.49 |              2486.45 |              2928.74 |              2910.40 |
| Forecasting Revenue Change (TPC-H Q14)              |               766.26 |               729.82 |               719.15 |               730.56 |               744.19 |               763.67 |
| Top Supplier Query (TPC-H Q15)                      |               529.34 |               596.58 |               522.44 |               567.03 |               589.20 |               585.29 |
| Parts/Supplier Relationship (TPC-H Q16)             |               520.66 |               522.79 |               534.19 |               598.86 |               573.89 |               545.81 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1890.30 |              1952.56 |              1915.90 |              1985.18 |              1854.50 |              1956.82 |
| Large Volume Customer (TPC-H Q18)                   |              8645.72 |              8416.40 |              8304.10 |              8221.63 |              8356.49 |              8214.01 |
| Discounted Revenue (TPC-H Q19)                      |               111.17 |               131.87 |               125.91 |               131.21 |               126.85 |               113.13 |
| Potential Part Promotion (TPC-H Q20)                |               407.16 |               456.44 |               425.08 |               435.14 |               443.14 |               358.11 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               786.07 |               689.06 |               731.90 |               840.70 |               773.21 |               759.26 |
| Global Sales Opportunity Query (TPC-H Q22)          |               217.59 |               183.82 |               211.40 |               208.92 |               225.01 |               201.84 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       182.67 |      1.60 |           9.88 |                 14.99 |
| PostgreSQL-1-1-2 |       182.67 |      1.60 |           9.88 |                 14.99 |

### Loading phase: component data generator

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        33.21 |      0.44 |           0.00 |                  0.39 |
| PostgreSQL-1-1-2 |        33.21 |      0.44 |           0.00 |                  0.39 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        85.98 |      2.90 |          16.32 |                 21.12 |
| PostgreSQL-1-1-2 |         0.00 |      0.01 |          10.07 |                 14.87 |
| PostgreSQL-1-2-1 |        44.14 |      0.82 |           9.77 |                 13.76 |
| PostgreSQL-1-2-2 |         0.00 |      0.00 |          10.06 |                 14.44 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        12.44 |      0.00 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2 |         0.02 |      0.00 |           0.26 |                  0.26 |
| PostgreSQL-1-2-1 |        11.76 |      0.39 |           0.26 |                  0.26 |
| PostgreSQL-1-2-2 |         0.04 |      0.00 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    8.00 |
| PostgreSQL-1-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    7.00 |
| PostgreSQL-1-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   10.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
