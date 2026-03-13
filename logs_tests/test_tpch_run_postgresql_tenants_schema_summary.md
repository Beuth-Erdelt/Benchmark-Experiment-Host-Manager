## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2323s 
* Code: 1773417900
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
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-2-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219911
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219911
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219912
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219912
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-2-1-1 |   PostgreSQL-BHT-2-1-2 |   PostgreSQL-BHT-2-2-1 |   PostgreSQL-BHT-2-2-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4385.21 |                4358.91 |                4292    |                4402.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2384.74 |                2435.03 |                2399.04 |                2256.59 |
| Shipping Priority (TPC-H Q3)                        |                1706.04 |                1770.89 |                1552.63 |                1617.22 |
| Order Priority Checking Query (TPC-H Q4)            |                 712.26 |                 741.89 |                 651.87 |                 674.54 |
| Local Supplier Volume (TPC-H Q5)                    |                2037.55 |                2092.93 |                2005.79 |                1948.2  |
| Forecasting Revenue Change (TPC-H Q6)               |                 792.67 |                 811.99 |                 796.42 |                 804.34 |
| Forecasting Revenue Change (TPC-H Q7)               |                1582.98 |                1612.24 |                1622.64 |                1572.54 |
| National Market Share (TPC-H Q8)                    |                1240.38 |                1237.13 |                1082.55 |                1055.22 |
| Product Type Profit Measure (TPC-H Q9)              |                5167.72 |                5062.05 |                5022.42 |                4965.28 |
| Forecasting Revenue Change (TPC-H Q10)              |                1953.49 |                1957.16 |                1970.79 |                1978.2  |
| Important Stock Identification (TPC-H Q11)          |                 755.85 |                 703.98 |                 767.22 |                 657.7  |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1310.16 |                1291.97 |                1313.09 |                1300.4  |
| Customer Distribution (TPC-H Q13)                   |                6390.39 |                6349.93 |                6569.17 |                6055.44 |
| Forecasting Revenue Change (TPC-H Q14)              |                1267.28 |                1284.83 |                1285.81 |                1273.3  |
| Top Supplier Query (TPC-H Q15)                      |                1237.12 |                1249.33 |                1254.96 |                1248.14 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1049.23 |                1082.12 |                1049.03 |                1065.2  |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                5962.21 |                5354.48 |                6014.36 |                5149.33 |
| Large Volume Customer (TPC-H Q18)                   |               23576    |               23118.3  |               23207.3  |               23060.7  |
| Discounted Revenue (TPC-H Q19)                      |                 279.78 |                 262.96 |                 288.76 |                 285.59 |
| Potential Part Promotion (TPC-H Q20)                |                3671.26 |                3140.37 |                3601.23 |                2999.34 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                1691.9  |                1733.31 |                1695.88 |                1756.25 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 400.2  |                 383.98 |                 402    |                 356.14 |

### Loading [s]

| DBMS                 |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-2-1-1 |              0 |            1149 |            8 |        1740 |       2899 |
| PostgreSQL-BHT-2-1-2 |              0 |            1149 |            8 |        1740 |       2899 |
| PostgreSQL-BHT-2-2-1 |              0 |            1149 |            8 |        1740 |       2899 |
| PostgreSQL-BHT-2-2-2 |              0 |            1149 |            8 |        1740 |       2899 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-2-1-1 |            1.8  |
| PostgreSQL-BHT-2-1-2 |            1.78 |
| PostgreSQL-BHT-2-2-1 |            1.78 |
| PostgreSQL-BHT-2-2-2 |            1.72 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-2-1-1 |             19997.9 |
| PostgreSQL-BHT-2-1-2 |             20234.5 |
| PostgreSQL-BHT-2-2-1 |             20230.9 |
| PostgreSQL-BHT-2-2-2 |             20915   |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS               |   time [s] |   count |   SF |   Throughput@Size |
|:-------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-2-1 |         71 |       2 |   10 |           22309.9 |
| PostgreSQL-BHT-2-2 |         71 |       2 |   10 |           22309.9 |

### Workflow

| DBMS                 | orig_name          |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:---------------------|:-------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-2-1-1 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773419888 |      1773419959 |
| PostgreSQL-BHT-2-1-2 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773419888 |      1773419957 |
| PostgreSQL-BHT-2-2-1 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773420072 |      1773420143 |
| PostgreSQL-BHT-2-2-2 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773420072 |      1773420140 |

#### Actual

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |      1050.92 |      2.22 |          34.47 |                 63.65 |
| PostgreSQL-BHT-2-2 |      1050.92 |      2.22 |          34.47 |                 63.65 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-2-2 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       154.87 |      0.63 |           0.02 |                  6.06 |
| PostgreSQL-BHT-2-2 |       154.87 |      0.63 |           0.02 |                  6.06 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       212.47 |      2.83 |          36.36 |                 68.19 |
| PostgreSQL-BHT-2-2 |       643.04 |      9.62 |          36.26 |                 55.45 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |        18.56 |         0 |           0.26 |                  0.26 |
| PostgreSQL-BHT-2-2 |        18.48 |         0 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         1 |                                        0 |                                                0 |                          17 |                                      16 |
| PostgreSQL-BHT-2-2 |                         1 |                                        0 |                                                0 |                          17 |                                      16 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         0 |                                        0 |                                                0 |                          10 |                                      10 |
| PostgreSQL-BHT-2-2 |                         0 |                                        0 |                                                0 |                          10 |                                      10 |

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
