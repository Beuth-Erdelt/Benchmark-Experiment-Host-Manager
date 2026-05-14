## Show Summary

### Workload
TPC-H Queries SF=6
* Type: tpch
* Duration: 1941s 
* Code: 1778711262
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=6) data is loaded and benchmark is executed.
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
  * disk:213989
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778711262
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:213990
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778711262
* PostgreSQL-1-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:213990
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778711262
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:213991
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778711262
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:213991
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778711262
* PostgreSQL-1-2-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:213991
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778711262

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    6 |      416.00 |           2.00 |           22.00 |         38.00 |          351.00 |              8 |           0 |          |                |             0 | False         |               51.92 |
| PostgreSQL-1-2 |                2 |    6 |      403.00 |           2.00 |           20.00 |         36.00 |          343.00 |              8 |           0 |          |                |             0 | False         |               53.60 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 6.00 |            22.00 |      55.00 |            1.47 |            14717.06 |           8640.00 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 6.00 |            22.00 |      54.00 |            1.43 |            15095.94 |           8800.00 |
| PostgreSQL-1-1-2-2 |             1.00 |     2.00 |        1.00 | 6.00 |            22.00 |      54.00 |            1.43 |            15076.05 |           8800.00 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 6.00 |            22.00 |      54.00 |            1.44 |            14950.86 |           8800.00 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 6.00 |            22.00 |      54.00 |            1.46 |            14761.33 |           8800.00 |
| PostgreSQL-1-2-2-2 |             2.00 |     2.00 |        1.00 | 6.00 |            22.00 |      54.00 |            1.44 |            14980.90 |           8800.00 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        1.00 | 6.00 |            22.00 |      55.00 |            1.47 |            14717.06 |           8640.00 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        2.00 | 6.00 |            44.00 |      54.00 |            1.43 |            15085.99 |          17600.00 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        1.00 | 6.00 |            22.00 |      54.00 |            1.44 |            14950.86 |           8800.00 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        2.00 | 6.00 |            44.00 |      54.00 |            1.45 |            14870.71 |          17600.00 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-1-2-2 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-2-1 |   PostgreSQL-1-2-2-2 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              4061.57 |              4326.80 |              4263.55 |              4216.49 |              4105.85 |              4060.45 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              1532.17 |              1500.35 |              1558.33 |              1442.59 |              1546.24 |              1529.60 |
| Shipping Priority (TPC-H Q3)                        |              1538.69 |              1486.61 |              1429.60 |              1509.85 |              1490.11 |              1530.77 |
| Order Priority Checking Query (TPC-H Q4)            |               589.98 |               583.48 |               566.42 |               563.50 |               582.49 |               580.24 |
| Local Supplier Volume (TPC-H Q5)                    |              1864.74 |              1741.78 |              1776.57 |              1759.52 |              1851.45 |              1609.23 |
| Forecasting Revenue Change (TPC-H Q6)               |               783.48 |               736.60 |               685.52 |               776.92 |               706.09 |               733.57 |
| Forecasting Revenue Change (TPC-H Q7)               |              2271.40 |              2184.74 |              2037.16 |              2097.78 |              2248.22 |              2124.57 |
| National Market Share (TPC-H Q8)                    |               941.00 |               796.57 |               854.68 |               884.48 |               810.88 |               849.13 |
| Product Type Profit Measure (TPC-H Q9)              |              2791.59 |              2989.35 |              3086.74 |              2251.59 |              2324.49 |              2280.00 |
| Forecasting Revenue Change (TPC-H Q10)              |              1632.40 |              1716.45 |              1773.47 |              1613.70 |              1567.67 |              1699.51 |
| Important Stock Identification (TPC-H Q11)          |               638.92 |               564.19 |               556.50 |               487.62 |               533.81 |               477.44 |
| Shipping Modes and Order Priority (TPC-H Q12)       |              1304.69 |              1230.55 |              1243.79 |              1223.77 |              1249.09 |              1126.27 |
| Customer Distribution (TPC-H Q13)                   |              6586.88 |              6262.32 |              6546.52 |              6128.83 |              6506.42 |              6433.51 |
| Forecasting Revenue Change (TPC-H Q14)              |              1244.49 |              1260.82 |              1168.79 |              1285.40 |              1154.45 |              1148.32 |
| Top Supplier Query (TPC-H Q15)                      |              1108.94 |              1113.45 |              1151.96 |              1136.45 |              1018.10 |              1137.47 |
| Parts/Supplier Relationship (TPC-H Q16)             |               899.51 |               938.63 |               883.19 |               866.65 |               875.51 |               853.87 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              3934.62 |              3753.82 |              4040.85 |              3635.75 |              3892.62 |              3931.77 |
| Large Volume Customer (TPC-H Q18)                   |             16127.25 |             16507.71 |             16501.04 |             16834.76 |             16090.14 |             16525.70 |
| Discounted Revenue (TPC-H Q19)                      |               239.07 |               234.08 |               234.01 |               226.41 |               234.27 |               214.09 |
| Potential Part Promotion (TPC-H Q20)                |               975.39 |               858.28 |               870.82 |              2166.01 |              2444.59 |              2337.28 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |              1582.99 |              1676.14 |              1608.28 |              1492.45 |              1596.80 |              1655.71 |
| Global Sales Opportunity Query (TPC-H Q22)          |               361.03 |               343.47 |               370.81 |               331.16 |               354.45 |               331.48 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       353.81 |      5.05 |          13.77 |                 22.72 |
| PostgreSQL-1-1-2 |       353.81 |      5.05 |          13.77 |                 22.72 |
| PostgreSQL-1-2-1 |      1087.82 |      3.28 |          14.76 |                 23.70 |
| PostgreSQL-1-2-2 |      1087.82 |      3.28 |          14.76 |                 23.70 |

### Loading phase: component data generator

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        18.44 |      0.16 |           0.00 |                  0.56 |
| PostgreSQL-1-1-2 |        18.44 |      0.16 |           0.00 |                  0.56 |
| PostgreSQL-1-2-1 |        50.05 |      1.78 |           0.00 |                  0.68 |
| PostgreSQL-1-2-2 |        50.05 |      1.78 |           0.00 |                  0.68 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       146.96 |      3.52 |          21.20 |                 30.14 |
| PostgreSQL-1-1-2 |       355.43 |      7.80 |          47.53 |                 56.47 |
| PostgreSQL-1-2-1 |       105.22 |      3.62 |          14.95 |                 23.89 |
| PostgreSQL-1-2-2 |       373.65 |      7.90 |          53.20 |                 62.14 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        12.11 |      0.01 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2 |        22.99 |      0.01 |           0.26 |                  0.26 |
| PostgreSQL-1-2-1 |        12.04 |      0.01 |           0.26 |                  0.26 |
| PostgreSQL-1-2-2 |        24.65 |      0.02 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    3.00 |
| PostgreSQL-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    6.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| PostgreSQL-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    6.00 |
| PostgreSQL-1-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   12.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
