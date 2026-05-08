## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1531s 
* Code: 1776770536
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
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-BHT-2-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247631
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247631
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247631
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247631
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247632
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247632
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247632
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2-2 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247632
  * datadisk:16368
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776770536
    * TENANT_BY:database
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-2-1-1-1 |   PostgreSQL-BHT-2-1-1-2 |   PostgreSQL-BHT-2-1-2-1 |   PostgreSQL-BHT-2-1-2-2 |   PostgreSQL-BHT-2-2-1-1 |   PostgreSQL-BHT-2-2-1-2 |   PostgreSQL-BHT-2-2-2-1 |   PostgreSQL-BHT-2-2-2-2 |
|:----------------------------------------------------|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  2636.12 |                  2620.34 |                  2651.48 |                  2638.93 |                 29210.01 |                 30645.89 |                  2609.41 |                  2535.28 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                   636.39 |                   653.60 |                   661.30 |                   664.07 |                 17255.55 |                 17742.65 |                   823.73 |                   600.62 |
| Shipping Priority (TPC-H Q3)                        |                   808.26 |                   769.96 |                   788.08 |                   781.91 |                 16775.57 |                 15738.77 |                   684.59 |                   661.84 |
| Order Priority Checking Query (TPC-H Q4)            |                   366.16 |                   400.99 |                   386.38 |                   374.72 |                   433.23 |                   404.39 |                   314.02 |                   325.83 |
| Local Supplier Volume (TPC-H Q5)                    |                   800.97 |                   819.09 |                   846.34 |                   794.86 |                  1000.64 |                  1127.90 |                   742.68 |                   747.08 |
| Forecasting Revenue Change (TPC-H Q6)               |                   468.86 |                   434.88 |                   440.08 |                   480.26 |                   492.03 |                   484.23 |                   428.46 |                   450.66 |
| Forecasting Revenue Change (TPC-H Q7)               |                   972.48 |                  1012.00 |                   991.70 |                   982.16 |                  1085.68 |                  1080.72 |                  1003.75 |                   975.30 |
| National Market Share (TPC-H Q8)                    |                   500.17 |                   541.33 |                   453.17 |                   435.46 |                  6168.07 |                  5784.37 |                   500.36 |                   466.41 |
| Product Type Profit Measure (TPC-H Q9)              |                  1335.07 |                  1281.05 |                  1259.45 |                  1272.71 |                  1475.89 |                  1338.12 |                  1283.84 |                  1218.38 |
| Forecasting Revenue Change (TPC-H Q10)              |                   643.07 |                   626.95 |                   689.56 |                   786.35 |                   781.99 |                   805.68 |                   691.74 |                   670.81 |
| Important Stock Identification (TPC-H Q11)          |                   259.93 |                   249.76 |                   303.50 |                   367.87 |                   331.76 |                   312.84 |                   256.60 |                   259.94 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                   677.65 |                   680.68 |                   696.91 |                   659.92 |                   754.32 |                   752.68 |                   684.11 |                   676.73 |
| Customer Distribution (TPC-H Q13)                   |                  3177.56 |                  3189.57 |                  3106.81 |                  3408.27 |                  3155.55 |                  3525.59 |                  2899.69 |                  2792.17 |
| Forecasting Revenue Change (TPC-H Q14)              |                   784.77 |                   823.23 |                   677.61 |                   712.36 |                   769.13 |                   754.38 |                   758.64 |                   693.34 |
| Top Supplier Query (TPC-H Q15)                      |                   609.56 |                   640.43 |                   576.07 |                   624.49 |                   603.23 |                   589.76 |                   605.80 |                   550.67 |
| Parts/Supplier Relationship (TPC-H Q16)             |                   604.40 |                   696.88 |                   567.05 |                   694.06 |                   637.75 |                   599.53 |                   611.31 |                   589.18 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  2004.82 |                  2023.72 |                  2023.74 |                  2321.61 |                  2065.39 |                  1928.66 |                  2300.19 |                  1951.62 |
| Large Volume Customer (TPC-H Q18)                   |                  9670.73 |                  8491.50 |                  8408.32 |                  8919.23 |                  8536.17 |                  8599.45 |                  9230.37 |                  8535.41 |
| Discounted Revenue (TPC-H Q19)                      |                   119.30 |                   117.95 |                   127.19 |                   119.73 |                   124.28 |                   135.38 |                   115.35 |                   112.48 |
| Potential Part Promotion (TPC-H Q20)                |                   397.06 |                   512.95 |                   420.99 |                   542.29 |                   445.81 |                   710.50 |                   432.91 |                   518.08 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                   798.28 |                   783.08 |                   777.57 |                   770.74 |                   740.39 |                   781.54 |                   716.10 |                   746.95 |
| Global Sales Opportunity Query (TPC-H Q22)          |                   200.57 |                   204.91 |                   213.09 |                   217.86 |                   215.89 |                   219.62 |                   216.64 |                   227.73 |

### Loading [s]

| DBMS                   |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-2-1-1-1 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-1-1-2 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-1-2-1 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-1-2-2 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-2-1-1 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-2-1-2 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-2-2-1 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |
| PostgreSQL-BHT-2-2-2-2 |           1.00 |          439.00 |         2.00 |      533.00 |     977.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                   |   Geo Times [s] |
|:-----------------------|----------------:|
| PostgreSQL-BHT-2-1-1-1 |            0.75 |
| PostgreSQL-BHT-2-1-1-2 |            0.76 |
| PostgreSQL-BHT-2-1-2-1 |            0.75 |
| PostgreSQL-BHT-2-1-2-2 |            0.78 |
| PostgreSQL-BHT-2-2-1-1 |            1.33 |
| PostgreSQL-BHT-2-2-1-2 |            1.35 |
| PostgreSQL-BHT-2-2-2-1 |            0.75 |
| PostgreSQL-BHT-2-2-2-2 |            0.72 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                   |   Power@Size [~Q/h] |
|:-----------------------|--------------------:|
| PostgreSQL-BHT-2-1-1-1 |            14375.18 |
| PostgreSQL-BHT-2-1-1-2 |            14118.39 |
| PostgreSQL-BHT-2-1-2-1 |            14429.86 |
| PostgreSQL-BHT-2-1-2-2 |            13761.42 |
| PostgreSQL-BHT-2-2-1-1 |             8135.97 |
| PostgreSQL-BHT-2-2-1-2 |             7982.87 |
| PostgreSQL-BHT-2-2-2-1 |            14495.36 |
| PostgreSQL-BHT-2-2-2-2 |            14978.59 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                 |   time [s] |   count |   SF |   Throughput@Size |
|:---------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-2-1-1 |      30.00 |    2.00 | 3.00 |          15840.00 |
| PostgreSQL-BHT-2-1-2 |      31.00 |    2.00 | 3.00 |          15329.03 |
| PostgreSQL-BHT-2-2-1 |      95.00 |    2.00 | 3.00 |           5002.11 |
| PostgreSQL-BHT-2-2-2 |      31.00 |    2.00 | 3.00 |          15329.03 |

### Workflow

| DBMS                   | orig_name            |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-----------------------|:---------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-2-1-1-1 | PostgreSQL-BHT-2-1-1 | 3.00 |      2 |                1 |            1 |        1776771307 |      1776771337 |
| PostgreSQL-BHT-2-1-1-2 | PostgreSQL-BHT-2-1-1 | 3.00 |      2 |                1 |            1 |        1776771307 |      1776771336 |
| PostgreSQL-BHT-2-1-2-1 | PostgreSQL-BHT-2-1-2 | 3.00 |      2 |                1 |            2 |        1776771409 |      1776771438 |
| PostgreSQL-BHT-2-1-2-2 | PostgreSQL-BHT-2-1-2 | 3.00 |      2 |                1 |            2 |        1776771409 |      1776771440 |
| PostgreSQL-BHT-2-2-1-1 | PostgreSQL-BHT-2-2-1 | 3.00 |      2 |                2 |            1 |        1776771779 |      1776771874 |
| PostgreSQL-BHT-2-2-1-2 | PostgreSQL-BHT-2-2-1 | 3.00 |      2 |                2 |            1 |        1776771779 |      1776771874 |
| PostgreSQL-BHT-2-2-2-1 | PostgreSQL-BHT-2-2-2 | 3.00 |      2 |                2 |            2 |        1776771960 |      1776771991 |
| PostgreSQL-BHT-2-2-2-2 | PostgreSQL-BHT-2-2-2 | 3.00 |      2 |                2 |            2 |        1776771960 |      1776771989 |

#### Actual

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2], [2, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |       252.22 |      4.70 |          13.25 |                 23.45 |
| 1776770536-PostgreSQL-BHT-2-1-2 |       252.22 |      4.70 |          13.25 |                 23.45 |

### Loading phase: component data generator

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776770536-PostgreSQL-BHT-2-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |        67.20 |      0.63 |           0.01 |                  1.56 |
| 1776770536-PostgreSQL-BHT-2-1-2 |        67.20 |      0.63 |           0.01 |                  1.56 |

### Execution phase: SUT deployment

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |         6.30 |      1.72 |          13.53 |                 24.95 |
| 1776770536-PostgreSQL-BHT-2-1-2 |       137.51 |      3.75 |          16.58 |                 26.16 |
| 1776770536-PostgreSQL-BHT-2-2-1 |       795.93 |      1.59 |          14.47 |                 24.07 |
| 1776770536-PostgreSQL-BHT-2-2-2 |         0.00 |      0.02 |          14.40 |                 23.16 |

### Execution phase: component benchmarker

| DBMS                            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |        23.54 |      0.00 |           0.28 |                  0.28 |
| 1776770536-PostgreSQL-BHT-2-1-2 |         0.02 |      0.00 |           0.28 |                  0.28 |
| 1776770536-PostgreSQL-BHT-2-2-1 |        24.68 |      1.04 |           0.27 |                  0.27 |
| 1776770536-PostgreSQL-BHT-2-2-2 |        23.80 |      0.01 |           0.27 |                  0.27 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |                         3 |                                        0 |                                                0 |                           9 |                                       6 |
| 1776770536-PostgreSQL-BHT-2-1-2 |                         3 |                                        0 |                                                0 |                           9 |                                       6 |

#### Execution phase: SUT deployment

| DBMS                            |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:--------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776770536-PostgreSQL-BHT-2-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   14.00 |
| 1776770536-PostgreSQL-BHT-2-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                       11.00 |                                   11.00 |
| 1776770536-PostgreSQL-BHT-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                       16.00 |                                   17.00 |
| 1776770536-PostgreSQL-BHT-2-2-2 |                      3.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    9.00 |

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
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
