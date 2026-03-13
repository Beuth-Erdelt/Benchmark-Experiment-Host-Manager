## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 958s 
* Code: 1773429812
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 16 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [1] threads, split into [16] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-16-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:153347
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773429812
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-1-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:153347
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773429812
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-2-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:153347
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773429812
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-2-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:153347
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773429812
    * TENANT_BY:database
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-16-1-1 |   PostgreSQL-BHT-16-1-2 |   PostgreSQL-BHT-16-2-1 |   PostgreSQL-BHT-16-2-2 |
|:----------------------------------------------------|------------------------:|------------------------:|------------------------:|------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 2075.73 |                 2075.88 |                 2072.2  |                 2055.15 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 1047.9  |                 1056.26 |                 1033.03 |                 1032.29 |
| Shipping Priority (TPC-H Q3)                        |                  719.99 |                  713.34 |                  676.67 |                  660.51 |
| Order Priority Checking Query (TPC-H Q4)            |                  340.16 |                  349.34 |                  345.26 |                  337.33 |
| Local Supplier Volume (TPC-H Q5)                    |                  779.85 |                  782.28 |                  783.93 |                  782.21 |
| Forecasting Revenue Change (TPC-H Q6)               |                  455.52 |                  459.35 |                  464.12 |                  462.57 |
| Forecasting Revenue Change (TPC-H Q7)               |                 1636.09 |                 1648.41 |                 1636.67 |                 1622.17 |
| National Market Share (TPC-H Q8)                    |                 1059.22 |                 1070.9  |                 1029.07 |                 1011.42 |
| Product Type Profit Measure (TPC-H Q9)              |                 1873.43 |                 1872.12 |                 1853.41 |                 1808.61 |
| Forecasting Revenue Change (TPC-H Q10)              |                 2168.94 |                 2172.78 |                 2173.06 |                 2150.94 |
| Important Stock Identification (TPC-H Q11)          |                  539.07 |                  537.15 |                  524.07 |                  534.02 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  642.36 |                  643.08 |                  645.39 |                  633.92 |
| Customer Distribution (TPC-H Q13)                   |                 2171.75 |                 2144.46 |                 2084.48 |                 2022.69 |
| Forecasting Revenue Change (TPC-H Q14)              |                  494.46 |                  785.29 |                  492.23 |                  762.79 |
| Top Supplier Query (TPC-H Q15)                      |                  519.93 |                  513.01 |                  515.26 |                  510.43 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  525.42 |                  524.94 |                  527.12 |                  528.19 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 1867.41 |                 1873.87 |                 1835.93 |                 1709.28 |
| Large Volume Customer (TPC-H Q18)                   |                 6933.57 |                 5609.17 |                 5551.28 |                 5493.27 |
| Discounted Revenue (TPC-H Q19)                      |                  115.67 |                  115.86 |                  113.86 |                  111.63 |
| Potential Part Promotion (TPC-H Q20)                |                  317.88 |                  313.39 |                  285.61 |                  262.01 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 1400.07 |                 1404.07 |                 1414.99 |                 1408.33 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  233.69 |                  235.36 |                  211.49 |                  211.7  |

### Loading [s]

| DBMS                  |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-16-1-1 |             48 |              85 |            7 |         439 |        586 |
| PostgreSQL-BHT-16-1-2 |             48 |              85 |            7 |         439 |        586 |
| PostgreSQL-BHT-16-2-1 |             48 |              85 |            7 |         439 |        586 |
| PostgreSQL-BHT-16-2-2 |             48 |              85 |            7 |         439 |        586 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                  |   Geo Times [s] |
|:----------------------|----------------:|
| PostgreSQL-BHT-16-1-1 |            0.84 |
| PostgreSQL-BHT-16-1-2 |            0.85 |
| PostgreSQL-BHT-16-2-1 |            0.82 |
| PostgreSQL-BHT-16-2-2 |            0.82 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                  |   Power@Size [~Q/h] |
|:----------------------|--------------------:|
| PostgreSQL-BHT-16-1-1 |             4290.27 |
| PostgreSQL-BHT-16-1-2 |             4236.31 |
| PostgreSQL-BHT-16-2-1 |             4409.47 |
| PostgreSQL-BHT-16-2-2 |             4392.09 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                |   time [s] |   count |   SF |   Throughput@Size |
|:--------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-16-1 |         30 |       2 |    1 |           5280    |
| PostgreSQL-BHT-16-2 |         28 |       2 |    1 |           5657.14 |

### Workflow

| DBMS                  | orig_name           |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:----------------------|:--------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-16-1-1 | PostgreSQL-BHT-16-1 |    1 |     16 |                1 |            1 |        1773430504 |      1773430533 |
| PostgreSQL-BHT-16-1-2 | PostgreSQL-BHT-16-1 |    1 |     16 |                1 |            1 |        1773430503 |      1773430532 |
| PostgreSQL-BHT-16-2-1 | PostgreSQL-BHT-16-2 |    1 |     16 |                1 |            2 |        1773430655 |      1773430682 |
| PostgreSQL-BHT-16-2-2 | PostgreSQL-BHT-16-2 |    1 |     16 |                1 |            2 |        1773430654 |      1773430682 |

#### Actual

* DBMS PostgreSQL-BHT-16 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-16 - Pods [[2, 2]]

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
