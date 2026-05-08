## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1533s 
* Code: 1776768855
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-BHT-2-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247629
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247629
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247629
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247629
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247630
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247630
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247630
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247630
  * datadisk:16353
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776768855
    * TENANT_BY:schema
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-2-1-1-1 |   PostgreSQL-BHT-2-1-1-2 |   PostgreSQL-BHT-2-1-2-1 |   PostgreSQL-BHT-2-1-2-2 |   PostgreSQL-BHT-2-2-1-1 |   PostgreSQL-BHT-2-2-1-2 |   PostgreSQL-BHT-2-2-2-1 |   PostgreSQL-BHT-2-2-2-2 |
|:----------------------------------------------------|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  2522.74 |                  2654.45 |                  2521.04 |                  2513.28 |                 33067.65 |                 38167.95 |                  2496.66 |                  2716.35 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                   653.89 |                   628.14 |                   602.29 |                   615.24 |                 16534.87 |                 17004.12 |                   650.41 |                   651.06 |
| Shipping Priority (TPC-H Q3)                        |                   778.27 |                  1211.69 |                   727.88 |                  1135.34 |                 16205.48 |                 20114.29 |                   702.79 |                  1098.52 |
| Order Priority Checking Query (TPC-H Q4)            |                   339.60 |                   370.67 |                   395.66 |                   382.81 |                   443.62 |                   405.52 |                   344.04 |                   356.42 |
| Local Supplier Volume (TPC-H Q5)                    |                   767.35 |                   814.65 |                   808.18 |                   807.88 |                  1696.87 |                  1132.73 |                   771.50 |                   792.51 |
| Forecasting Revenue Change (TPC-H Q6)               |                   445.32 |                   434.47 |                   513.55 |                   485.67 |                   494.22 |                   493.71 |                   447.91 |                   415.93 |
| Forecasting Revenue Change (TPC-H Q7)               |                   849.68 |                   963.30 |                  1019.62 |                  1027.53 |                  1102.35 |                  1082.48 |                   989.33 |                   940.18 |
| National Market Share (TPC-H Q8)                    |                   464.36 |                   509.89 |                   430.64 |                   455.70 |                  9307.12 |                  6650.06 |                   464.81 |                   448.22 |
| Product Type Profit Measure (TPC-H Q9)              |                  1183.16 |                  1419.73 |                  1243.44 |                  1202.95 |                  1490.78 |                  1451.05 |                  1330.33 |                  1409.97 |
| Forecasting Revenue Change (TPC-H Q10)              |                   598.35 |                   607.82 |                   603.25 |                   591.87 |                   708.42 |                   707.05 |                   582.01 |                   617.28 |
| Important Stock Identification (TPC-H Q11)          |                   246.58 |                   263.74 |                   252.77 |                   260.33 |                   342.46 |                   330.29 |                   262.13 |                   267.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                   694.50 |                   727.50 |                   727.97 |                   726.13 |                   753.23 |                   758.15 |                   684.94 |                   654.91 |
| Customer Distribution (TPC-H Q13)                   |                  2922.01 |                  2947.83 |                  2949.80 |                  2907.05 |                  2722.52 |                  2841.63 |                  2961.42 |                  3118.53 |
| Forecasting Revenue Change (TPC-H Q14)              |                   730.99 |                   767.57 |                   764.80 |                   754.61 |                   751.87 |                   737.21 |                   709.67 |                   827.47 |
| Top Supplier Query (TPC-H Q15)                      |                   575.00 |                   594.84 |                   611.42 |                   591.71 |                   608.69 |                   595.67 |                   580.87 |                   652.56 |
| Parts/Supplier Relationship (TPC-H Q16)             |                   606.98 |                   602.61 |                   588.23 |                   588.06 |                   588.84 |                   600.04 |                   580.08 |                   730.56 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  1984.47 |                  2406.68 |                  2030.55 |                  2006.62 |                  2207.01 |                  2175.57 |                  2089.05 |                  2219.35 |
| Large Volume Customer (TPC-H Q18)                   |                  8513.01 |                  8773.67 |                  9484.94 |                  8586.40 |                  8479.83 |                  9071.95 |                  8707.43 |                  8394.90 |
| Discounted Revenue (TPC-H Q19)                      |                   115.77 |                   129.87 |                   126.15 |                   116.45 |                   125.06 |                   144.84 |                   122.38 |                   122.00 |
| Potential Part Promotion (TPC-H Q20)                |                   380.89 |                   611.85 |                   467.19 |                   496.01 |                   458.11 |                   715.74 |                   408.08 |                   564.50 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                   686.00 |                   732.79 |                   798.45 |                   737.72 |                   808.67 |                   795.24 |                   762.61 |                   799.67 |
| Global Sales Opportunity Query (TPC-H Q22)          |                   209.28 |                   203.24 |                   222.12 |                   214.59 |                   216.45 |                   233.80 |                   221.76 |                   200.20 |

### Loading [s]

| DBMS                   |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-2-1-1-1 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-1-1-2 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-1-2-1 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-1-2-2 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-2-1-1 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-2-1-2 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-2-2-1 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |
| PostgreSQL-BHT-2-2-2-2 |           1.00 |          440.00 |         2.00 |      535.00 |     979.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                   |   Geo Times [s] |
|:-----------------------|----------------:|
| PostgreSQL-BHT-2-1-1-1 |            0.71 |
| PostgreSQL-BHT-2-1-1-2 |            0.78 |
| PostgreSQL-BHT-2-1-2-1 |            0.75 |
| PostgreSQL-BHT-2-1-2-2 |            0.75 |
| PostgreSQL-BHT-2-2-1-1 |            1.38 |
| PostgreSQL-BHT-2-2-1-2 |            1.40 |
| PostgreSQL-BHT-2-2-2-1 |            0.73 |
| PostgreSQL-BHT-2-2-2-2 |            0.78 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                   |   Power@Size [~Q/h] |
|:-----------------------|--------------------:|
| PostgreSQL-BHT-2-1-1-1 |            15168.62 |
| PostgreSQL-BHT-2-1-1-2 |            13825.46 |
| PostgreSQL-BHT-2-1-2-1 |            14395.33 |
| PostgreSQL-BHT-2-1-2-2 |            14325.80 |
| PostgreSQL-BHT-2-2-1-1 |             7804.80 |
| PostgreSQL-BHT-2-2-1-2 |             7731.92 |
| PostgreSQL-BHT-2-2-2-1 |            14822.92 |
| PostgreSQL-BHT-2-2-2-2 |            13928.05 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                 |   time [s] |   count |   SF |   Throughput@Size |
|:---------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-2-1-1 |      30.00 |    2.00 | 3.00 |          15840.00 |
| PostgreSQL-BHT-2-1-2 |      32.00 |    2.00 | 3.00 |          14850.00 |
| PostgreSQL-BHT-2-2-1 |     110.00 |    2.00 | 3.00 |           4320.00 |
| PostgreSQL-BHT-2-2-2 |      30.00 |    2.00 | 3.00 |          15840.00 |

### Workflow

| DBMS                   | orig_name            |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-----------------------|:---------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-2-1-1-1 | PostgreSQL-BHT-2-1-1 | 3.00 |      2 |                1 |            1 |        1776769625 |      1776769654 |
| PostgreSQL-BHT-2-1-1-2 | PostgreSQL-BHT-2-1-1 | 3.00 |      2 |                1 |            1 |        1776769625 |      1776769655 |
| PostgreSQL-BHT-2-1-2-1 | PostgreSQL-BHT-2-1-2 | 3.00 |      2 |                1 |            2 |        1776769738 |      1776769770 |
| PostgreSQL-BHT-2-1-2-2 | PostgreSQL-BHT-2-1-2 | 3.00 |      2 |                1 |            2 |        1776769738 |      1776769769 |
| PostgreSQL-BHT-2-2-1-1 | PostgreSQL-BHT-2-2-1 | 3.00 |      2 |                2 |            1 |        1776770114 |      1776770217 |
| PostgreSQL-BHT-2-2-1-2 | PostgreSQL-BHT-2-2-1 | 3.00 |      2 |                2 |            1 |        1776770113 |      1776770223 |
| PostgreSQL-BHT-2-2-2-1 | PostgreSQL-BHT-2-2-2 | 3.00 |      2 |                2 |            2 |        1776770307 |      1776770335 |
| PostgreSQL-BHT-2-2-2-2 | PostgreSQL-BHT-2-2-2 | 3.00 |      2 |                2 |            2 |        1776770306 |      1776770336 |

#### Actual

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2], [2, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |       269.88 |      3.23 |          13.73 |                 25.42 |
| 1776768855-PostgreSQL-BHT-2-1-2 |       269.88 |      3.23 |          13.73 |                 25.42 |

### Loading phase: component data generator

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776768855-PostgreSQL-BHT-2-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |        66.22 |      0.53 |           0.01 |                  2.02 |
| 1776768855-PostgreSQL-BHT-2-1-2 |        66.22 |      0.53 |           0.01 |                  2.02 |

### Execution phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |       178.14 |      7.12 |          28.28 |                 38.02 |
| 1776768855-PostgreSQL-BHT-2-1-2 |        46.72 |      1.42 |          14.65 |                 24.22 |
| 1776768855-PostgreSQL-BHT-2-2-1 |       791.63 |      1.53 |          14.45 |                 24.03 |
| 1776768855-PostgreSQL-BHT-2-2-2 |        66.18 |      2.08 |          14.62 |                 23.37 |

### Execution phase: component benchmarker

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |        24.11 |      0.00 |           0.26 |                  0.26 |
| 1776768855-PostgreSQL-BHT-2-1-2 |        22.56 |      1.05 |           0.29 |                  0.30 |
| 1776768855-PostgreSQL-BHT-2-2-1 |        24.16 |      0.01 |           0.28 |                  0.29 |
| 1776768855-PostgreSQL-BHT-2-2-2 |        11.84 |      0.61 |           0.28 |                  0.29 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |                         1 |                                        0 |                                                0 |                           3 |                                       2 |
| 1776768855-PostgreSQL-BHT-2-1-2 |                         1 |                                        0 |                                                0 |                           3 |                                       2 |

#### Execution phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776768855-PostgreSQL-BHT-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       11.00 |                                   10.00 |
| 1776768855-PostgreSQL-BHT-2-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   10.00 |
| 1776768855-PostgreSQL-BHT-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                       14.00 |                                   14.00 |
| 1776768855-PostgreSQL-BHT-2-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   10.00 |

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
