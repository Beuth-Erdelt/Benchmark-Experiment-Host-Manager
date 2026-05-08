## Show Summary

### Workload
TPC-H Queries SF=6
* Type: tpch
* Duration: 1694s 
* Code: 1776766994
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=6) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.5.
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
* PostgreSQL-BHT-8-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247626
  * datadisk:16350
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776766994
* PostgreSQL-BHT-8-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247627
  * datadisk:16350
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776766994
* PostgreSQL-BHT-8-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247627
  * datadisk:16350
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776766994
* PostgreSQL-BHT-8-2-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247627
  * datadisk:16350
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776766994
* PostgreSQL-BHT-8-2-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247627
  * datadisk:16350
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776766994
* PostgreSQL-BHT-8-2-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247627
  * datadisk:16350
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776766994

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-8-1-1-1 |   PostgreSQL-BHT-8-1-2-1 |   PostgreSQL-BHT-8-1-2-2 |   PostgreSQL-BHT-8-2-1-1 |   PostgreSQL-BHT-8-2-2-1 |   PostgreSQL-BHT-8-2-2-2 |
|:----------------------------------------------------|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  4119.91 |                  4379.30 |                  4310.78 |                 36692.30 |                  4292.24 |                  4279.99 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  1492.03 |                  1462.74 |                  1514.72 |                 35883.17 |                  1642.51 |                  1645.42 |
| Shipping Priority (TPC-H Q3)                        |                  1573.65 |                  1603.66 |                  1559.84 |                 24288.84 |                  1658.45 |                  1657.08 |
| Order Priority Checking Query (TPC-H Q4)            |                   530.96 |                   565.58 |                   599.03 |                   620.90 |                   565.79 |                   566.30 |
| Local Supplier Volume (TPC-H Q5)                    |                  1853.14 |                  1906.03 |                  1847.66 |                  5002.65 |                  1803.31 |                  1807.94 |
| Forecasting Revenue Change (TPC-H Q6)               |                   695.89 |                   745.90 |                   743.93 |                  1008.54 |                   745.72 |                   742.24 |
| Forecasting Revenue Change (TPC-H Q7)               |                  2124.46 |                  2274.55 |                  2206.37 |                  2251.49 |                  2070.53 |                  2272.51 |
| National Market Share (TPC-H Q8)                    |                   908.48 |                   896.36 |                   789.36 |                 11164.75 |                   842.69 |                   867.60 |
| Product Type Profit Measure (TPC-H Q9)              |                  2234.52 |                  2381.81 |                  2252.64 |                  2616.49 |                  2126.76 |                  2299.89 |
| Forecasting Revenue Change (TPC-H Q10)              |                  2740.12 |                  2572.32 |                  2379.04 |                  2592.74 |                  2674.28 |                  2676.29 |
| Important Stock Identification (TPC-H Q11)          |                   608.77 |                   622.97 |                   550.61 |                   475.19 |                   555.26 |                   506.73 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  1318.54 |                  1289.60 |                  1288.26 |                  1252.81 |                  1249.24 |                  1359.72 |
| Customer Distribution (TPC-H Q13)                   |                  6764.09 |                  6773.53 |                  6501.94 |                  6466.02 |                  6963.48 |                  6476.74 |
| Forecasting Revenue Change (TPC-H Q14)              |                  1175.03 |                  1324.63 |                  1285.54 |                  1171.85 |                  1292.80 |                  1157.91 |
| Top Supplier Query (TPC-H Q15)                      |                  1202.27 |                  1194.31 |                  1204.90 |                  1076.49 |                  1159.24 |                  1089.38 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  1158.11 |                   907.58 |                   983.76 |                   954.53 |                   984.89 |                   918.07 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  3878.40 |                  4483.01 |                  3914.62 |                  3752.56 |                  4403.49 |                  3823.49 |
| Large Volume Customer (TPC-H Q18)                   |                 16573.47 |                 17256.44 |                 17810.98 |                 16953.23 |                 17934.25 |                 17421.15 |
| Discounted Revenue (TPC-H Q19)                      |                   255.09 |                   241.79 |                   210.87 |                   226.28 |                   243.32 |                   220.78 |
| Potential Part Promotion (TPC-H Q20)                |                  1117.99 |                  1089.61 |                   871.46 |                   866.12 |                  1117.98 |                   833.69 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  1744.12 |                  1524.98 |                  1476.88 |                  1541.63 |                  1701.44 |                  1614.88 |
| Global Sales Opportunity Query (TPC-H Q22)          |                   332.28 |                   320.70 |                   331.49 |                   338.08 |                   361.95 |                   367.35 |

### Loading [s]

| DBMS                   |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-8-1-1-1 |          17.00 |          326.00 |         2.00 |      566.00 |     916.00 |
| PostgreSQL-BHT-8-1-2-1 |          17.00 |          326.00 |         2.00 |      566.00 |     916.00 |
| PostgreSQL-BHT-8-1-2-2 |          17.00 |          326.00 |         2.00 |      566.00 |     916.00 |
| PostgreSQL-BHT-8-2-1-1 |          17.00 |          326.00 |         2.00 |      566.00 |     916.00 |
| PostgreSQL-BHT-8-2-2-1 |          17.00 |          326.00 |         2.00 |      566.00 |     916.00 |
| PostgreSQL-BHT-8-2-2-2 |          17.00 |          326.00 |         2.00 |      566.00 |     916.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                   |   Geo Times [s] |
|:-----------------------|----------------:|
| PostgreSQL-BHT-8-1-1-1 |            1.50 |
| PostgreSQL-BHT-8-1-2-1 |            1.50 |
| PostgreSQL-BHT-8-1-2-2 |            1.45 |
| PostgreSQL-BHT-8-2-1-1 |            2.49 |
| PostgreSQL-BHT-8-2-2-1 |            1.51 |
| PostgreSQL-BHT-8-2-2-2 |            1.46 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                   |   Power@Size [~Q/h] |
|:-----------------------|--------------------:|
| PostgreSQL-BHT-8-1-1-1 |            14408.40 |
| PostgreSQL-BHT-8-1-2-1 |            14353.32 |
| PostgreSQL-BHT-8-1-2-2 |            14915.59 |
| PostgreSQL-BHT-8-2-1-1 |             8679.17 |
| PostgreSQL-BHT-8-2-2-1 |            14330.12 |
| PostgreSQL-BHT-8-2-2-2 |            14808.18 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                 |   time [s] |   count |   SF |   Throughput@Size |
|:---------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-8-1-1 |      61.00 |    1.00 | 6.00 |           7790.16 |
| PostgreSQL-BHT-8-1-2 |      59.00 |    2.00 | 6.00 |          16108.47 |
| PostgreSQL-BHT-8-2-1 |     159.00 |    1.00 | 6.00 |           2988.68 |
| PostgreSQL-BHT-8-2-2 |      59.00 |    2.00 | 6.00 |          16108.47 |

### Workflow

| DBMS                   | orig_name            |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-----------------------|:---------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-8-1-1-1 | PostgreSQL-BHT-8-1-1 | 6.00 |      8 |                1 |            1 |        1776767806 |      1776767867 |
| PostgreSQL-BHT-8-1-2-1 | PostgreSQL-BHT-8-1-2 | 6.00 |      8 |                1 |            2 |        1776767950 |      1776768008 |
| PostgreSQL-BHT-8-1-2-2 | PostgreSQL-BHT-8-1-2 | 6.00 |      8 |                1 |            2 |        1776767949 |      1776768006 |
| PostgreSQL-BHT-8-2-1-1 | PostgreSQL-BHT-8-2-1 | 6.00 |      8 |                2 |            1 |        1776768327 |      1776768486 |
| PostgreSQL-BHT-8-2-2-1 | PostgreSQL-BHT-8-2-2 | 6.00 |      8 |                2 |            2 |        1776768573 |      1776768632 |
| PostgreSQL-BHT-8-2-2-2 | PostgreSQL-BHT-8-2-2 | 6.00 |      8 |                2 |            2 |        1776768573 |      1776768630 |

#### Actual

* DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |       395.10 |      1.97 |          14.36 |                 25.75 |
| 1776766994-PostgreSQL-BHT-8-1-2 |       395.10 |      1.97 |          14.36 |                 25.75 |

### Loading phase: component data generator

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776766994-PostgreSQL-BHT-8-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |        74.56 |      1.18 |           0.00 |                  0.78 |
| 1776766994-PostgreSQL-BHT-8-1-2 |        74.56 |      1.18 |           0.00 |                  0.78 |

### Execution phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |       211.14 |      3.70 |          33.69 |                 43.27 |
| 1776766994-PostgreSQL-BHT-8-1-2 |       220.96 |      7.10 |          14.97 |                 24.55 |
| 1776766994-PostgreSQL-BHT-8-2-1 |      1159.54 |      2.34 |          14.55 |                 24.12 |
| 1776766994-PostgreSQL-BHT-8-2-2 |       223.10 |      7.59 |          14.88 |                 23.59 |

### Execution phase: component benchmarker

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |        11.73 |      0.00 |           0.26 |                  0.26 |
| 1776766994-PostgreSQL-BHT-8-1-2 |        24.85 |      0.02 |           0.26 |                  0.27 |
| 1776766994-PostgreSQL-BHT-8-2-1 |        11.80 |      0.38 |           0.25 |                  0.26 |
| 1776766994-PostgreSQL-BHT-8-2-2 |        22.43 |      0.02 |           0.26 |                  0.27 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |                         1 |                                        0 |                                                0 |                           9 |                                       8 |
| 1776766994-PostgreSQL-BHT-8-1-2 |                         1 |                                        0 |                                                0 |                           9 |                                       8 |

#### Execution phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776766994-PostgreSQL-BHT-8-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| 1776766994-PostgreSQL-BHT-8-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   12.00 |
| 1776766994-PostgreSQL-BHT-8-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| 1776766994-PostgreSQL-BHT-8-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   12.00 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
