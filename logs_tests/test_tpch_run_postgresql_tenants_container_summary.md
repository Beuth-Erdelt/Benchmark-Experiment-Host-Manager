## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 1927s 
* Code: 1773422696
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
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-1-0-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1250374
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-0-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1281298
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1281291
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-BHT-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1283094
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-1-0-1-1 |   PostgreSQL-BHT-1-0-2-1 |   PostgreSQL-BHT-1-1-1-1 |   PostgreSQL-BHT-1-1-2-1 |
|:----------------------------------------------------|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  4319.15 |                  4334.56 |                  4336.92 |                  4317.89 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  2443.83 |                  2240    |                  2343.76 |                  2450.72 |
| Shipping Priority (TPC-H Q3)                        |                  1770.97 |                  1634.24 |                  1665.31 |                  1572.43 |
| Order Priority Checking Query (TPC-H Q4)            |                   682.59 |                   660.74 |                   666.87 |                   662.64 |
| Local Supplier Volume (TPC-H Q5)                    |                  1906.8  |                  1921.27 |                  1703.39 |                  1830.61 |
| Forecasting Revenue Change (TPC-H Q6)               |                   742.17 |                   762.12 |                   774.05 |                   765.41 |
| Forecasting Revenue Change (TPC-H Q7)               |                  1495.61 |                  1584.6  |                  1403.14 |                  1584.48 |
| National Market Share (TPC-H Q8)                    |                  1092.45 |                   972.26 |                   988.96 |                  1004.64 |
| Product Type Profit Measure (TPC-H Q9)              |                  4721.04 |                  4784.87 |                  4373.12 |                  4706.72 |
| Forecasting Revenue Change (TPC-H Q10)              |                  1870.05 |                  1891.53 |                  1890.42 |                  1944.94 |
| Important Stock Identification (TPC-H Q11)          |                   775.5  |                   810.17 |                   774.9  |                   733.06 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  1251.32 |                  1274.85 |                  1278.4  |                  1274.82 |
| Customer Distribution (TPC-H Q13)                   |                  6772.36 |                  6428.69 |                  7509.21 |                  6219.9  |
| Forecasting Revenue Change (TPC-H Q14)              |                  1288.87 |                  1272.1  |                  1265.36 |                  1259.48 |
| Top Supplier Query (TPC-H Q15)                      |                  1251.21 |                  1237.44 |                  1242.15 |                  1233.37 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  1043.6  |                  1051.78 |                   999.73 |                   991.78 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  5346.52 |                  5489.68 |                  5499.57 |                  5234    |
| Large Volume Customer (TPC-H Q18)                   |                 22324.9  |                 25265.3  |                 23234.3  |                 23498.1  |
| Discounted Revenue (TPC-H Q19)                      |                   274.93 |                   257.66 |                   240.55 |                   256.97 |
| Potential Part Promotion (TPC-H Q20)                |                  3020.92 |                  3450.41 |                  3069.94 |                  3059.26 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  1758.17 |                  1761.09 |                  1745.94 |                  1744.17 |
| Global Sales Opportunity Query (TPC-H Q22)          |                   374    |                   358.77 |                   368.3  |                   364.12 |

### Loading [s]

| DBMS                   |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-1-0-1-1 |              0 |             701 |            4 |         987 |       1709 |
| PostgreSQL-BHT-1-0-2-1 |              0 |             701 |            4 |         987 |       1709 |
| PostgreSQL-BHT-1-1-1-1 |              0 |             700 |            4 |         975 |       1681 |
| PostgreSQL-BHT-1-1-2-1 |              0 |             700 |            4 |         975 |       1681 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                   |   Geo Times [s] |
|:-----------------------|----------------:|
| PostgreSQL-BHT-1-0-1-1 |            1.74 |
| PostgreSQL-BHT-1-0-2-1 |            1.73 |
| PostgreSQL-BHT-1-1-1-1 |            1.7  |
| PostgreSQL-BHT-1-1-2-1 |            1.7  |

### Power@Size ((3600*SF)/(geo times))

| DBMS                   |   Power@Size [~Q/h] |
|:-----------------------|--------------------:|
| PostgreSQL-BHT-1-0-1-1 |             20729.6 |
| PostgreSQL-BHT-1-0-2-1 |             20752.2 |
| PostgreSQL-BHT-1-1-1-1 |             21147.1 |
| PostgreSQL-BHT-1-1-2-1 |             21125.9 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                 |   time [s] |   count |   SF |   Throughput@Size |
|:---------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-1-0-1 |         68 |       1 |   10 |           11647.1 |
| PostgreSQL-BHT-1-0-2 |         70 |       1 |   10 |           11314.3 |
| PostgreSQL-BHT-1-1-1 |         68 |       1 |   10 |           11647.1 |
| PostgreSQL-BHT-1-1-2 |         68 |       1 |   10 |           11647.1 |

### Workflow

| DBMS                   | orig_name            |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-----------------------|:---------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-1-0-1-1 | PostgreSQL-BHT-1-0-1 |   10 |      1 |                1 |            1 |        1773424159 |      1773424227 |
| PostgreSQL-BHT-1-0-2-1 | PostgreSQL-BHT-1-0-2 |   10 |      1 |                1 |            2 |        1773424433 |      1773424503 |
| PostgreSQL-BHT-1-1-1-1 | PostgreSQL-BHT-1-1-1 |   10 |      1 |                1 |            1 |        1773424159 |      1773424227 |
| PostgreSQL-BHT-1-1-2-1 | PostgreSQL-BHT-1-1-2 |   10 |      1 |                1 |            2 |        1773424432 |      1773424500 |

#### Actual

* DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
* DBMS PostgreSQL-BHT-1 - Pods [[1, 1]]

#### Planned

* DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
* DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |       328.4  |       1.4 |          19.26 |                 35.32 |
| PostgreSQL-BHT-1-0-2 |       328.4  |       1.4 |          19.26 |                 35.32 |
| PostgreSQL-BHT-1-1-1 |       380.89 |       1.4 |          18.66 |                 34.55 |
| PostgreSQL-BHT-1-1-2 |       380.89 |       1.4 |          18.66 |                 34.55 |

### Loading phase: component data generator

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-1-0-2 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-1-1-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-1-1-2 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |        74.72 |      0.63 |           0.01 |                  0.01 |
| PostgreSQL-BHT-1-0-2 |        74.72 |      0.63 |           0.01 |                  0.01 |
| PostgreSQL-BHT-1-1-1 |        75.52 |      0.59 |           0.01 |                  0.01 |
| PostgreSQL-BHT-1-1-2 |        75.52 |      0.59 |           0.01 |                  0.01 |

### Execution phase: SUT deployment

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |       269.52 |      4.9  |          57.15 |                 73.09 |
| PostgreSQL-BHT-1-0-2 |       138.32 |      2.23 |          20.65 |                 36.58 |
| PostgreSQL-BHT-1-1-1 |       314.19 |      4.9  |          23.9  |                 39.83 |
| PostgreSQL-BHT-1-1-2 |       133.51 |      2.16 |          20.72 |                 36.65 |

### Execution phase: component benchmarker

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |         9.43 |      0.14 |           0.26 |                  0.27 |
| PostgreSQL-BHT-1-0-2 |         9.31 |      0.16 |           0.26 |                  0.27 |
| PostgreSQL-BHT-1-1-1 |         9.34 |      0.16 |           0.26 |                  0.26 |
| PostgreSQL-BHT-1-1-2 |         9.22 |      0.16 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:---------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-1-0-1 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-0-2 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-1-1 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-1-2 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |

#### Execution phase: SUT deployment

| DBMS                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:---------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-1-0-1 |                         1 |                                        0 |                                                0 |                           6 |                                       7 |
| PostgreSQL-BHT-1-0-2 |                         1 |                                        0 |                                                0 |                           5 |                                       5 |
| PostgreSQL-BHT-1-1-1 |                         0 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-1-2 |                         0 |                                        0 |                                                0 |                           7 |                                       7 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST failed: Workflow not as planned
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
