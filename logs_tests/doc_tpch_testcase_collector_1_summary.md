## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1614s 
* Code: 1778437166
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
  * disk:197172
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778437166
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197172
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778437166
* PostgreSQL-1-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197172
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778437166
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197218
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778437166
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197173
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778437166
* PostgreSQL-1-2-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197173
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778437166

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      471.00 |           3.00 |            5.00 |        124.00 |          330.00 |              8 |                |             0 | False         |               22.93 |
| PostgreSQL-1-2 |                2 |    3 |      471.00 |           3.00 |            5.00 |        124.00 |          330.00 |              8 |                |             0 | False         |               22.93 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.74 |            14531.68 |           8800.00 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.77 |            14108.75 |           8193.10 |
| PostgreSQL-1-1-2-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.73 |            14706.93 |           8485.71 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      89.00 |            1.40 |             7736.84 |           2669.66 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.75 |            14471.97 |           8485.71 |
| PostgreSQL-1-2-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.73 |            14818.58 |           8485.71 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.74 |            14531.68 |           8800.00 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.75 |            14404.73 |          16386.21 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      89.00 |            1.40 |             7736.84 |           2669.66 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        2.00 | 3.00 |            44.00 |      28.00 |            0.74 |            14644.25 |          16971.43 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-1-2-2 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-2-1 |   PostgreSQL-1-2-2-2 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              2490.85 |              2442.63 |              2371.61 |             29572.83 |              2369.21 |              2313.26 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               637.13 |               640.36 |               652.01 |             15482.19 |               654.31 |               683.28 |
| Shipping Priority (TPC-H Q3)                        |               787.58 |               761.44 |               721.85 |             12208.94 |               752.97 |               729.36 |
| Order Priority Checking Query (TPC-H Q4)            |               389.45 |               350.94 |               351.62 |               612.04 |               370.77 |               338.05 |
| Local Supplier Volume (TPC-H Q5)                    |               805.69 |               777.79 |               736.33 |              1666.63 |               770.50 |               779.29 |
| Forecasting Revenue Change (TPC-H Q6)               |               449.87 |               423.64 |               429.16 |               631.64 |               437.09 |               437.20 |
| Forecasting Revenue Change (TPC-H Q7)               |               934.54 |              1003.81 |               901.86 |              1245.67 |               990.59 |               939.99 |
| National Market Share (TPC-H Q8)                    |               530.74 |               467.39 |               442.22 |              5859.22 |               443.92 |               437.03 |
| Product Type Profit Measure (TPC-H Q9)              |              1237.12 |              1317.66 |              1285.85 |              1508.75 |              1384.27 |              1300.74 |
| Forecasting Revenue Change (TPC-H Q10)              |              1329.79 |              1505.26 |              1416.06 |              1767.16 |              1523.34 |              1390.86 |
| Important Stock Identification (TPC-H Q11)          |               259.11 |               293.32 |               284.73 |               256.76 |               280.94 |               276.77 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               629.55 |               630.79 |               610.32 |               669.86 |               577.91 |               642.93 |
| Customer Distribution (TPC-H Q13)                   |              2331.05 |              2851.64 |              2874.58 |              2380.35 |              2638.35 |              2429.42 |
| Forecasting Revenue Change (TPC-H Q14)              |               643.79 |               768.73 |               651.49 |               757.48 |               657.83 |               654.90 |
| Top Supplier Query (TPC-H Q15)                      |               578.31 |               596.88 |               554.38 |               577.90 |               535.96 |               581.06 |
| Parts/Supplier Relationship (TPC-H Q16)             |               546.87 |               618.22 |               529.65 |               569.69 |               525.84 |               551.52 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1927.72 |              2235.45 |              2023.11 |              1961.81 |              1988.75 |              1957.44 |
| Large Volume Customer (TPC-H Q18)                   |              8270.35 |              8218.37 |              8651.77 |              8035.83 |              8083.75 |              8272.31 |
| Discounted Revenue (TPC-H Q19)                      |               120.24 |               120.64 |               119.41 |               121.45 |               128.56 |               109.81 |
| Potential Part Promotion (TPC-H Q20)                |               394.37 |               454.42 |               432.80 |               700.31 |               416.43 |               376.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               800.59 |               745.60 |               729.13 |               758.63 |               807.58 |               735.61 |
| Global Sales Opportunity Query (TPC-H Q22)          |               216.45 |               194.14 |               197.58 |               211.29 |               214.26 |               215.19 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       153.06 |      1.31 |           9.56 |                 15.53 |
| PostgreSQL-1-1-2 |       153.06 |      1.31 |           9.56 |                 15.53 |

### Loading phase: component data generator

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        30.03 |      0.29 |           0.00 |                  0.34 |
| PostgreSQL-1-1-2 |        30.03 |      0.29 |           0.00 |                  0.34 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           9.52 |                 14.33 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |          10.08 |                 14.89 |
| PostgreSQL-1-2-1 |       527.23 |      1.73 |          10.37 |                 14.90 |
| PostgreSQL-1-2-2 |         0.00 |      0.01 |          10.07 |                 14.49 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        11.24 |      0.00 |           0.29 |                  0.29 |
| PostgreSQL-1-1-2 |         0.02 |      0.00 |           0.29 |                  0.29 |
| PostgreSQL-1-2-1 |        12.01 |      0.00 |           0.26 |                  0.26 |
| PostgreSQL-1-2-2 |         0.03 |      0.00 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-1-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   10.00 |
| PostgreSQL-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
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
