## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 1585s 
* Code: 1775750916
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-8-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:178173
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1775750916

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-8-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               13144.15 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                5565.27 |
| Shipping Priority (TPC-H Q3)                        |                4350.74 |
| Order Priority Checking Query (TPC-H Q4)            |                1782.97 |
| Local Supplier Volume (TPC-H Q5)                    |                4500.11 |
| Forecasting Revenue Change (TPC-H Q6)               |                2388.81 |
| Forecasting Revenue Change (TPC-H Q7)               |                4048.80 |
| National Market Share (TPC-H Q8)                    |                2621.38 |
| Product Type Profit Measure (TPC-H Q9)              |               11581.11 |
| Forecasting Revenue Change (TPC-H Q10)              |                4732.76 |
| Important Stock Identification (TPC-H Q11)          |                1721.46 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                3634.37 |
| Customer Distribution (TPC-H Q13)                   |               19292.56 |
| Forecasting Revenue Change (TPC-H Q14)              |                3709.75 |
| Top Supplier Query (TPC-H Q15)                      |                3618.63 |
| Parts/Supplier Relationship (TPC-H Q16)             |                3242.86 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               18402.85 |
| Large Volume Customer (TPC-H Q18)                   |               39040.46 |
| Discounted Revenue (TPC-H Q19)                      |                 571.93 |
| Potential Part Promotion (TPC-H Q20)                |                7703.91 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                5170.12 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 971.56 |

### Loading [s]

| DBMS                 |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-8-1-1 |           4.00 |          401.00 |         1.00 |     1157.00 |    1574.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-8-1-1 |            4.63 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-8-1-1 |             7915.60 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS               |   time [s] |   count |    SF |   Throughput@Size |
|:-------------------|-----------:|--------:|------:|------------------:|
| PostgreSQL-BHT-8-1 |     171.00 |    1.00 | 10.00 |           4631.58 |

### Workflow

| DBMS                 | orig_name          |    SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:---------------------|:-------------------|------:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-8-1-1 | PostgreSQL-BHT-8-1 | 10.00 |      8 |                1 |            1 |        1775752277 |      1775752448 |

#### Actual

* DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |      1416.33 |      2.60 |          20.99 |                 34.83 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |       110.49 |      0.35 |           0.01 |                  1.14 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |       440.95 |      4.36 |          21.11 |                 36.39 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |        17.67 |      0.21 |           0.32 |                  0.33 |

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
