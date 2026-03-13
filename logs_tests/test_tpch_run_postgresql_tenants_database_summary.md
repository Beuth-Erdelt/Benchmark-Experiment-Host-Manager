## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2247s 
* Code: 1773420332
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-2-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-2-1-1 |   PostgreSQL-BHT-2-1-2 |   PostgreSQL-BHT-2-2-1 |   PostgreSQL-BHT-2-2-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4302.73 |                4423.71 |                4310.42 |                4330.76 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2411.65 |                2568.16 |                2344.17 |                2305.32 |
| Shipping Priority (TPC-H Q3)                        |                1668.14 |                1746.71 |                1690.89 |                1570.95 |
| Order Priority Checking Query (TPC-H Q4)            |                 690.19 |                 725.85 |                 707.13 |                 723.72 |
| Local Supplier Volume (TPC-H Q5)                    |                2101.34 |                2043.12 |                2133.01 |                1921.17 |
| Forecasting Revenue Change (TPC-H Q6)               |                 808.49 |                 803.88 |                 807.31 |                 810.93 |
| Forecasting Revenue Change (TPC-H Q7)               |                1587.88 |                1491.45 |                1627.57 |                1626.8  |
| National Market Share (TPC-H Q8)                    |                1251.62 |                1449.04 |                1051.61 |                1237.99 |
| Product Type Profit Measure (TPC-H Q9)              |                4922.11 |                4797.09 |                4941.19 |                4123.63 |
| Forecasting Revenue Change (TPC-H Q10)              |                1859.05 |                1809.69 |                1799.9  |                1901.11 |
| Important Stock Identification (TPC-H Q11)          |                 722.19 |                 719.29 |                 828.14 |                 748.13 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1271.27 |                1281.98 |                1331.26 |                1269.39 |
| Customer Distribution (TPC-H Q13)                   |                7131.42 |                7144.42 |                7262.17 |                7452.36 |
| Forecasting Revenue Change (TPC-H Q14)              |                1248.74 |                1291    |                1221.36 |                1242.35 |
| Top Supplier Query (TPC-H Q15)                      |                1232.45 |                1256.58 |                1253.13 |                1225.53 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1073.43 |                1056.51 |                1063.97 |                1047.72 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                5300.47 |                6059.31 |                5906.99 |                6448.57 |
| Large Volume Customer (TPC-H Q18)                   |               23413.7  |               23714.2  |               23362    |               23633.4  |
| Discounted Revenue (TPC-H Q19)                      |                 289.78 |                 284.89 |                 280.05 |                 292.44 |
| Potential Part Promotion (TPC-H Q20)                |                3195.99 |                3690.39 |                3471.32 |                3522.49 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                1821.16 |                1751.45 |                1806.89 |                1764.4  |
| Global Sales Opportunity Query (TPC-H Q22)          |                 397.39 |                 379.86 |                 387.68 |                 376.18 |

### Loading [s]

| DBMS                 |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-2-1-1 |              2 |            1036 |            8 |        1618 |       2665 |
| PostgreSQL-BHT-2-1-2 |              2 |            1036 |            8 |        1618 |       2665 |
| PostgreSQL-BHT-2-2-1 |              2 |            1036 |            8 |        1618 |       2665 |
| PostgreSQL-BHT-2-2-2 |              2 |            1036 |            8 |        1618 |       2665 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-2-1-1 |            1.78 |
| PostgreSQL-BHT-2-1-2 |            1.82 |
| PostgreSQL-BHT-2-2-1 |            1.79 |
| PostgreSQL-BHT-2-2-2 |            1.78 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-2-1-1 |             20199.2 |
| PostgreSQL-BHT-2-1-2 |             19820.4 |
| PostgreSQL-BHT-2-2-1 |             20056.9 |
| PostgreSQL-BHT-2-2-2 |             20209.4 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS               |   time [s] |   count |   SF |   Throughput@Size |
|:-------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-2-1 |         72 |       2 |   10 |           22000   |
| PostgreSQL-BHT-2-2 |         71 |       2 |   10 |           22309.9 |

### Workflow

| DBMS                 | orig_name          |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:---------------------|:-------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-2-1-1 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773422209 |      1773422278 |
| PostgreSQL-BHT-2-1-2 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773422208 |      1773422280 |
| PostgreSQL-BHT-2-2-1 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773422388 |      1773422459 |
| PostgreSQL-BHT-2-2-2 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773422388 |      1773422459 |

#### Actual

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       980.19 |      2.15 |          32.82 |                 65.74 |
| PostgreSQL-BHT-2-2 |       980.19 |      2.15 |          32.82 |                 65.74 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-2-2 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       146.68 |      1.11 |           0.01 |                  0.01 |
| PostgreSQL-BHT-2-2 |       146.68 |      1.11 |           0.01 |                  0.01 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       266.23 |      5.21 |          35.53 |                 67.37 |
| PostgreSQL-BHT-2-2 |       316.43 |      4.48 |          35.5  |                 54.66 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |        18.51 |         0 |           0.25 |                  0.25 |
| PostgreSQL-BHT-2-2 |        19.31 |         0 |           0.3  |                  0.3  |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         2 |                                        0 |                                                0 |                          35 |                                      33 |
| PostgreSQL-BHT-2-2 |                         2 |                                        0 |                                                0 |                          35 |                                      33 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         2 |                                        0 |                                                0 |                          19 |                                      17 |
| PostgreSQL-BHT-2-2 |                         1 |                                        0 |                                                0 |                          16 |                                      16 |

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
