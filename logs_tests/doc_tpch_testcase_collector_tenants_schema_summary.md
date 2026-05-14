## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1736s 
* Code: 1778713322
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
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197643
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197643
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197644
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197644
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197644
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197644
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197645
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197645
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778713322
    * TENANT_BY:schema
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      750.00 |           8.00 |            1.00 |        303.00 |          437.00 |              2 |           0 |          | schema         |             2 | False         |               14.40 |
| PostgreSQL-1-2 |                2 |    3 |      750.00 |           8.00 |            1.00 |        303.00 |          437.00 |              2 |           0 |          | schema         |             2 | False         |               14.40 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.74 |            14553.77 |           8800.00 |
| PostgreSQL-1-1-1-2 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.75 |            14310.19 |           8193.10 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      30.00 |            0.73 |            14885.96 |           7920.00 |
| PostgreSQL-1-1-2-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      32.00 |            0.77 |            13962.22 |           7425.00 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      87.00 |            1.29 |             8395.03 |           2731.03 |
| PostgreSQL-1-2-1-2 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      89.00 |            1.32 |             8190.77 |           2669.66 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.70 |            15507.59 |           8800.00 |
| PostgreSQL-1-2-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.78 |            13832.72 |           8193.10 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.75 |            14431.46 |          16386.21 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        2.00 | 3.00 |            44.00 |      32.00 |            0.75 |            14416.69 |          14850.00 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        2.00 | 3.00 |            44.00 |      89.00 |            1.30 |             8292.27 |           5339.33 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.74 |            14646.23 |          16386.21 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-1-2 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-1-2-2 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-1-2 |   PostgreSQL-1-2-2-1 |   PostgreSQL-1-2-2-2 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              2556.74 |              2503.98 |              2444.13 |              2488.02 |             28688.90 |             29856.02 |              2442.82 |              2671.01 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               649.86 |               675.94 |               674.30 |               677.66 |             14278.78 |             15446.61 |               579.16 |               670.95 |
| Shipping Priority (TPC-H Q3)                        |               766.69 |              1173.59 |               671.25 |              1125.94 |             13300.65 |             13406.03 |               673.90 |              1072.03 |
| Order Priority Checking Query (TPC-H Q4)            |               387.22 |               416.04 |               370.72 |               388.68 |               615.64 |               418.85 |               373.62 |               402.21 |
| Local Supplier Volume (TPC-H Q5)                    |               817.26 |               781.17 |               758.07 |               823.63 |              1172.80 |              1039.92 |               707.15 |               803.10 |
| Forecasting Revenue Change (TPC-H Q6)               |               470.30 |               432.17 |               424.61 |               467.80 |               512.92 |               518.03 |               418.64 |               406.27 |
| Forecasting Revenue Change (TPC-H Q7)               |               961.01 |               953.34 |               930.45 |              1001.39 |              1108.45 |              1131.87 |               991.77 |               993.96 |
| National Market Share (TPC-H Q8)                    |               554.03 |               531.22 |               428.60 |               485.60 |              5204.04 |              5044.91 |               464.21 |               490.45 |
| Product Type Profit Measure (TPC-H Q9)              |              1348.21 |              1872.21 |              1312.92 |              1928.29 |              1532.95 |              2108.93 |              1283.80 |              2020.87 |
| Forecasting Revenue Change (TPC-H Q10)              |               736.37 |               679.40 |               670.34 |               671.47 |               882.34 |               846.51 |               659.73 |               714.50 |
| Important Stock Identification (TPC-H Q11)          |               238.61 |               256.55 |               284.84 |               301.12 |               293.63 |               284.23 |               233.29 |               305.69 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               674.32 |               654.26 |               658.37 |               637.13 |               725.93 |               635.91 |               622.55 |               638.21 |
| Customer Distribution (TPC-H Q13)                   |              3008.07 |              3077.30 |              2960.98 |              3034.59 |              2950.35 |              2844.58 |              2639.00 |              2965.44 |
| Forecasting Revenue Change (TPC-H Q14)              |               691.99 |               629.15 |               682.03 |               772.91 |               653.58 |               855.54 |               676.74 |               727.02 |
| Top Supplier Query (TPC-H Q15)                      |               600.78 |               577.45 |               551.95 |               603.56 |               557.96 |               653.64 |               529.15 |               626.52 |
| Parts/Supplier Relationship (TPC-H Q16)             |               571.87 |               566.36 |               578.24 |               601.89 |               582.00 |               751.03 |               585.35 |               639.36 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1843.28 |              1882.90 |              2056.12 |              2024.70 |              1915.52 |              2276.24 |              1925.11 |              2078.02 |
| Large Volume Customer (TPC-H Q18)                   |              8152.18 |              8139.02 |              8761.88 |              9118.60 |              8461.64 |              8319.55 |              8438.51 |              8404.35 |
| Discounted Revenue (TPC-H Q19)                      |               125.96 |               115.73 |               130.78 |               124.57 |               119.37 |               124.93 |               113.20 |               130.70 |
| Potential Part Promotion (TPC-H Q20)                |               373.28 |               384.99 |               403.36 |               377.74 |               362.41 |               438.27 |               361.46 |               378.74 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               788.70 |               755.68 |               750.85 |               713.82 |               808.95 |               676.71 |               786.05 |               761.87 |
| Global Sales Opportunity Query (TPC-H Q22)          |               219.76 |               207.70 |               215.08 |               193.88 |               214.08 |               203.61 |               202.43 |               219.29 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       286.84 |      3.22 |          13.70 |                 25.95 |
| PostgreSQL-1-1-2 |       286.84 |      3.22 |          13.70 |                 25.95 |

### Loading phase: component data generator

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        60.69 |      0.63 |           0.01 |                  1.64 |
| PostgreSQL-1-1-2 |        60.69 |      0.63 |           0.01 |                  1.64 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       168.74 |      5.41 |          26.68 |                 36.26 |
| PostgreSQL-1-1-2 |       102.67 |      3.34 |          14.57 |                 24.14 |
| PostgreSQL-1-2-1 |       774.57 |      1.98 |          14.42 |                 24.00 |
| PostgreSQL-1-2-2 |         0.00 |      0.01 |          14.39 |                 23.14 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        23.90 |      0.00 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2 |        24.58 |      0.00 |           0.27 |                  0.27 |
| PostgreSQL-1-2-1 |        24.90 |      0.01 |           0.28 |                  0.29 |
| PostgreSQL-1-2-2 |         0.02 |      0.01 |           0.28 |                  0.29 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       11.00 |                                   10.00 |
| PostgreSQL-1-1-2 |                      2.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    1.00 |
| PostgreSQL-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                       14.00 |                                   14.00 |
| PostgreSQL-1-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |

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
