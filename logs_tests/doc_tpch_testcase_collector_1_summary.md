## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1317s 
* Code: 1776765494
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
  * disk:247624
  * datadisk:8187
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776765494
* PostgreSQL-BHT-8-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247624
  * datadisk:8187
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776765494
* PostgreSQL-BHT-8-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247624
  * datadisk:8187
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776765494
* PostgreSQL-BHT-8-2-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247625
  * datadisk:8187
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776765494
* PostgreSQL-BHT-8-2-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247625
  * datadisk:8187
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776765494
* PostgreSQL-BHT-8-2-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247625
  * datadisk:8187
  * volume_size:30G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776765494

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-8-1-1-1 |   PostgreSQL-BHT-8-1-2-1 |   PostgreSQL-BHT-8-1-2-2 |   PostgreSQL-BHT-8-2-1-1 |   PostgreSQL-BHT-8-2-2-1 |   PostgreSQL-BHT-8-2-2-2 |
|:----------------------------------------------------|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  2449.22 |                  2578.95 |                  2556.30 |                 31506.67 |                  2498.89 |                  2532.47 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                   611.24 |                   854.03 |                   640.23 |                 17436.76 |                   668.08 |                   692.40 |
| Shipping Priority (TPC-H Q3)                        |                   678.63 |                   815.13 |                   705.52 |                 18244.94 |                   744.96 |                   713.30 |
| Order Priority Checking Query (TPC-H Q4)            |                   344.71 |                   352.13 |                   368.59 |                   419.02 |                   359.06 |                   351.78 |
| Local Supplier Volume (TPC-H Q5)                    |                   743.10 |                   756.71 |                   785.36 |                  1522.38 |                   852.18 |                   810.35 |
| Forecasting Revenue Change (TPC-H Q6)               |                   400.43 |                   460.47 |                   447.98 |                   484.61 |                   461.74 |                   402.89 |
| Forecasting Revenue Change (TPC-H Q7)               |                   875.87 |                   939.63 |                   977.51 |                  1032.73 |                   993.86 |                   887.93 |
| National Market Share (TPC-H Q8)                    |                   537.59 |                   434.04 |                   466.84 |                  7638.39 |                   434.61 |                   415.15 |
| Product Type Profit Measure (TPC-H Q9)              |                  1177.84 |                  1187.22 |                  1246.43 |                  1502.05 |                  1317.38 |                  1206.99 |
| Forecasting Revenue Change (TPC-H Q10)              |                  1342.22 |                  1576.79 |                  1753.49 |                  1840.31 |                  1598.34 |                  1423.66 |
| Important Stock Identification (TPC-H Q11)          |                   230.94 |                   257.50 |                   267.99 |                   417.65 |                   232.20 |                   239.99 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                   661.47 |                   693.84 |                   629.21 |                   753.50 |                   670.22 |                   620.51 |
| Customer Distribution (TPC-H Q13)                   |                  3312.36 |                  2779.26 |                  2602.31 |                  2683.02 |                  3033.57 |                  2999.48 |
| Forecasting Revenue Change (TPC-H Q14)              |                   687.59 |                   725.56 |                   673.27 |                   644.06 |                   686.45 |                   696.86 |
| Top Supplier Query (TPC-H Q15)                      |                   609.85 |                   586.52 |                   592.90 |                   537.75 |                   539.41 |                   584.41 |
| Parts/Supplier Relationship (TPC-H Q16)             |                   645.73 |                   587.11 |                   604.85 |                   603.69 |                   555.76 |                   590.32 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  2365.62 |                  1986.75 |                  2071.45 |                  1926.96 |                  1866.86 |                  1920.16 |
| Large Volume Customer (TPC-H Q18)                   |                  8204.97 |                  8455.24 |                  8842.40 |                  9118.28 |                  8468.39 |                  8360.92 |
| Discounted Revenue (TPC-H Q19)                      |                   117.20 |                   113.39 |                   123.74 |                   118.00 |                   120.67 |                   120.30 |
| Potential Part Promotion (TPC-H Q20)                |                   484.20 |                   388.66 |                   432.13 |                   374.58 |                   391.82 |                   391.13 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                   771.11 |                   778.75 |                   734.10 |                   752.92 |                   806.03 |                   770.44 |
| Global Sales Opportunity Query (TPC-H Q22)          |                   197.70 |                   197.97 |                   194.07 |                   219.83 |                   215.78 |                   223.43 |

### Loading [s]

| DBMS                   |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-8-1-1-1 |          15.00 |          182.00 |         2.00 |      287.00 |     490.00 |
| PostgreSQL-BHT-8-1-2-1 |          15.00 |          182.00 |         2.00 |      287.00 |     490.00 |
| PostgreSQL-BHT-8-1-2-2 |          15.00 |          182.00 |         2.00 |      287.00 |     490.00 |
| PostgreSQL-BHT-8-2-1-1 |          15.00 |          182.00 |         2.00 |      287.00 |     490.00 |
| PostgreSQL-BHT-8-2-2-1 |          15.00 |          182.00 |         2.00 |      287.00 |     490.00 |
| PostgreSQL-BHT-8-2-2-2 |          15.00 |          182.00 |         2.00 |      287.00 |     490.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                   |   Geo Times [s] |
|:-----------------------|----------------:|
| PostgreSQL-BHT-8-1-1-1 |            0.75 |
| PostgreSQL-BHT-8-1-2-1 |            0.76 |
| PostgreSQL-BHT-8-1-2-2 |            0.76 |
| PostgreSQL-BHT-8-2-1-1 |            1.40 |
| PostgreSQL-BHT-8-2-2-1 |            0.75 |
| PostgreSQL-BHT-8-2-2-2 |            0.74 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                   |   Power@Size [~Q/h] |
|:-----------------------|--------------------:|
| PostgreSQL-BHT-8-1-1-1 |            14399.68 |
| PostgreSQL-BHT-8-1-2-1 |            14212.16 |
| PostgreSQL-BHT-8-1-2-2 |            14261.08 |
| PostgreSQL-BHT-8-2-1-1 |             7737.91 |
| PostgreSQL-BHT-8-2-2-1 |            14319.35 |
| PostgreSQL-BHT-8-2-2-2 |            14623.75 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                 |   time [s] |   count |   SF |   Throughput@Size |
|:---------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-8-1-1 |      30.00 |    1.00 | 3.00 |           7920.00 |
| PostgreSQL-BHT-8-1-2 |      30.00 |    2.00 | 3.00 |          15840.00 |
| PostgreSQL-BHT-8-2-1 |     101.00 |    1.00 | 3.00 |           2352.48 |
| PostgreSQL-BHT-8-2-2 |      31.00 |    2.00 | 3.00 |          15329.03 |

### Workflow

| DBMS                   | orig_name            |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-----------------------|:---------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-8-1-1-1 | PostgreSQL-BHT-8-1-1 | 3.00 |      8 |                1 |            1 |        1776766052 |      1776766082 |
| PostgreSQL-BHT-8-1-2-1 | PostgreSQL-BHT-8-1-2 | 3.00 |      8 |                1 |            2 |        1776766154 |      1776766184 |
| PostgreSQL-BHT-8-1-2-2 | PostgreSQL-BHT-8-1-2 | 3.00 |      8 |                1 |            2 |        1776766154 |      1776766184 |
| PostgreSQL-BHT-8-2-1-1 | PostgreSQL-BHT-8-2-1 | 3.00 |      8 |                2 |            1 |        1776766520 |      1776766621 |
| PostgreSQL-BHT-8-2-2-1 | PostgreSQL-BHT-8-2-2 | 3.00 |      8 |                2 |            2 |        1776766705 |      1776766735 |
| PostgreSQL-BHT-8-2-2-2 | PostgreSQL-BHT-8-2-2 | 3.00 |      8 |                2 |            2 |        1776766704 |      1776766734 |

#### Actual

* DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |       154.53 |      1.89 |           9.60 |                 15.75 |
| 1776765494-PostgreSQL-BHT-8-1-2 |       154.53 |      1.89 |           9.60 |                 15.75 |

### Loading phase: component data generator

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776765494-PostgreSQL-BHT-8-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |        32.97 |      0.35 |           0.00 |                  0.39 |
| 1776765494-PostgreSQL-BHT-8-1-2 |        32.97 |      0.35 |           0.00 |                  0.39 |

### Execution phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |        28.32 |      0.91 |           9.86 |                 15.12 |
| 1776765494-PostgreSQL-BHT-8-1-2 |       146.36 |      6.63 |          14.03 |                 18.84 |
| 1776765494-PostgreSQL-BHT-8-2-1 |       503.46 |      0.96 |          10.13 |                 14.87 |
| 1776765494-PostgreSQL-BHT-8-2-2 |        78.27 |      2.29 |          10.32 |                 14.70 |

### Execution phase: component benchmarker

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |        11.82 |      0.00 |           0.29 |                  0.29 |
| 1776765494-PostgreSQL-BHT-8-1-2 |        12.17 |      0.00 |           0.29 |                  0.29 |
| 1776765494-PostgreSQL-BHT-8-2-1 |        11.34 |      0.36 |           0.26 |                  0.26 |
| 1776765494-PostgreSQL-BHT-8-2-2 |         0.02 |      0.00 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |                         1 |                                        0 |                                                0 |                           9 |                                       8 |
| 1776765494-PostgreSQL-BHT-8-1-2 |                         1 |                                        0 |                                                0 |                           9 |                                       8 |

#### Execution phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776765494-PostgreSQL-BHT-8-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |
| 1776765494-PostgreSQL-BHT-8-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |
| 1776765494-PostgreSQL-BHT-8-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| 1776765494-PostgreSQL-BHT-8-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |

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
