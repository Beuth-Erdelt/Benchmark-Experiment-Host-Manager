## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2127s 
* Code: 1778445920
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
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197186
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197186
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197187
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197186
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197187
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778445920
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      688.00 |           5.00 |            0.00 |        270.00 |          402.00 |              1 | container      |             2 | False         |               15.70 |
| PostgreSQL-1-2 |                2 |    3 |      688.00 |           5.00 |            0.00 |        270.00 |          402.00 |              1 | container      |             2 | False         |               15.70 |
| PostgreSQL-2-1 |                1 |    3 |      670.00 |           4.00 |            0.00 |        272.00 |          393.00 |              1 | container      |             2 | False         |               16.12 |
| PostgreSQL-2-2 |                2 |    3 |      670.00 |           4.00 |            0.00 |        272.00 |          393.00 |              1 | container      |             2 | False         |               16.12 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.74 |            14587.98 |           8485.71 |
| PostgreSQL-2-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.75 |            14364.49 |           8485.71 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.77 |            13964.88 |           8193.10 |
| PostgreSQL-2-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.70 |            15485.91 |           8485.71 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      87.00 |            1.30 |             8280.98 |           2731.03 |
| PostgreSQL-2-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      87.00 |            1.34 |             8038.93 |           2731.03 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.71 |            15149.51 |           8485.71 |
| PostgreSQL-2-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.73 |            14736.00 |           8485.71 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.74 |            14587.98 |           8485.71 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.77 |            13964.88 |           8193.10 |
| PostgreSQL-2-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.75 |            14364.49 |           8485.71 |
| PostgreSQL-2-1-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.70 |            15485.91 |           8485.71 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      87.00 |            1.30 |             8280.98 |           2731.03 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.71 |            15149.51 |           8485.71 |
| PostgreSQL-2-2-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      87.00 |            1.34 |             8038.93 |           2731.03 |
| PostgreSQL-2-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.73 |            14736.00 |           8485.71 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-2-1 |   PostgreSQL-2-1-1-1 |   PostgreSQL-2-1-2-1 |   PostgreSQL-2-2-1-1 |   PostgreSQL-2-2-2-1 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              2548.66 |              2328.47 |             27231.28 |              2481.37 |              2478.05 |              2416.80 |             30665.80 |              2665.08 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               639.16 |               613.68 |             15811.12 |               632.03 |               666.66 |               587.64 |             14504.52 |               639.09 |
| Shipping Priority (TPC-H Q3)                        |               818.86 |               773.37 |             11912.99 |               684.47 |               772.70 |               649.61 |              9936.29 |               738.05 |
| Order Priority Checking Query (TPC-H Q4)            |               379.40 |               381.48 |               584.12 |               341.22 |               326.53 |               340.66 |               589.42 |               358.59 |
| Local Supplier Volume (TPC-H Q5)                    |               830.90 |               767.54 |              1011.24 |               657.31 |               849.33 |               776.52 |              1306.05 |               812.39 |
| Forecasting Revenue Change (TPC-H Q6)               |               444.32 |               487.66 |               492.73 |               411.01 |               447.07 |               434.57 |               471.85 |               403.42 |
| Forecasting Revenue Change (TPC-H Q7)               |              1005.52 |               979.40 |              1057.86 |               870.27 |               934.75 |               949.56 |              1008.55 |               964.15 |
| National Market Share (TPC-H Q8)                    |               494.79 |               423.46 |              5886.78 |               398.56 |               521.07 |               416.27 |              6975.05 |               465.34 |
| Product Type Profit Measure (TPC-H Q9)              |              1960.64 |              1878.18 |              2067.19 |              1846.58 |              1879.11 |              1841.70 |              2036.65 |              1890.42 |
| Forecasting Revenue Change (TPC-H Q10)              |               646.62 |               783.39 |               777.04 |               618.22 |               652.10 |               641.04 |               831.48 |               666.18 |
| Important Stock Identification (TPC-H Q11)          |               231.15 |               357.64 |               308.31 |               264.65 |               312.19 |               249.23 |               320.50 |               280.83 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               620.37 |               700.69 |               682.46 |               627.61 |               634.90 |               617.62 |               723.53 |               582.29 |
| Customer Distribution (TPC-H Q13)                   |              2580.64 |              2867.62 |              2914.98 |              2933.18 |              2704.71 |              2492.81 |              2925.04 |              3078.89 |
| Forecasting Revenue Change (TPC-H Q14)              |               616.15 |               773.20 |               756.97 |               742.29 |               685.64 |               617.74 |               742.49 |               655.96 |
| Top Supplier Query (TPC-H Q15)                      |               589.51 |               612.33 |               578.83 |               568.11 |               552.00 |               531.65 |               554.09 |               535.55 |
| Parts/Supplier Relationship (TPC-H Q16)             |               575.92 |               561.91 |               597.78 |               570.57 |               542.33 |               493.23 |               579.46 |               555.26 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1957.71 |              2139.89 |              2034.41 |              2198.09 |              2166.26 |              1943.88 |              2083.56 |              2023.37 |
| Large Volume Customer (TPC-H Q18)                   |              8304.96 |              8267.13 |              8213.15 |              8111.99 |              8403.73 |              8265.14 |              8128.91 |              8917.75 |
| Discounted Revenue (TPC-H Q19)                      |               127.06 |               128.81 |               147.28 |               115.43 |               131.58 |               118.95 |               158.18 |               122.58 |
| Potential Part Promotion (TPC-H Q20)                |               486.83 |               480.29 |               419.32 |               413.88 |               448.42 |               378.09 |               429.36 |               365.46 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               738.86 |               785.80 |               674.32 |               744.33 |               761.83 |               769.75 |               840.30 |               763.56 |
| Global Sales Opportunity Query (TPC-H Q22)          |               197.81 |               221.29 |               206.54 |               200.59 |               221.42 |               210.60 |               221.52 |               212.24 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       144.71 |      1.59 |           9.62 |                 15.58 |
| PostgreSQL-1-1-2 |       144.71 |      1.59 |           9.62 |                 15.58 |
| PostgreSQL-2-1-1 |       133.83 |      1.76 |           9.63 |                 15.74 |
| PostgreSQL-2-1-2 |       133.83 |      1.76 |           9.63 |                 15.74 |

### Loading phase: component data generator

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-2-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-2-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        27.66 |      0.35 |           0.01 |                  1.79 |
| PostgreSQL-1-1-2 |        27.66 |      0.35 |           0.01 |                  1.79 |
| PostgreSQL-2-1-1 |        28.24 |      0.35 |           0.00 |                  0.90 |
| PostgreSQL-2-1-2 |        28.24 |      0.35 |           0.00 |                  0.90 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        26.89 |      1.58 |           9.90 |                 14.71 |
| PostgreSQL-1-1-2 |        76.28 |      3.28 |          13.72 |                 18.53 |
| PostgreSQL-1-2-1 |        73.23 |      1.11 |          10.15 |                 14.53 |
| PostgreSQL-1-2-2 |        37.77 |      1.94 |          10.16 |                 14.55 |
| PostgreSQL-2-1-1 |        72.03 |      2.21 |          12.82 |                 17.62 |
| PostgreSQL-2-1-2 |        10.11 |      0.34 |          10.18 |                 14.98 |
| PostgreSQL-2-2-1 |        78.31 |      1.42 |          10.12 |                 14.50 |
| PostgreSQL-2-2-2 |        61.72 |      2.02 |          10.11 |                 14.49 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        11.53 |      0.34 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2 |        12.00 |      0.39 |           0.29 |                  0.29 |
| PostgreSQL-1-2-1 |        11.68 |      0.40 |           0.25 |                  0.26 |
| PostgreSQL-1-2-2 |        11.47 |      0.41 |           0.30 |                  0.30 |
| PostgreSQL-2-1-1 |        12.04 |      0.00 |           0.28 |                  0.28 |
| PostgreSQL-2-1-2 |         0.02 |      0.00 |           0.28 |                  0.28 |
| PostgreSQL-2-2-1 |        11.99 |      0.31 |           0.25 |                  0.25 |
| PostgreSQL-2-2-2 |        11.69 |      0.00 |           0.25 |                  0.25 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| PostgreSQL-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-2-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    1.00 |
| PostgreSQL-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-1-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-2-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-2-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-2-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
