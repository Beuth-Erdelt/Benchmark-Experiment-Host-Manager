## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1744s 
* Code: 1778715189
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
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197646
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197646
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197647
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197647
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197647
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197647
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197648
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-2-2-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197648
  * volume_size:30G
  * volume_used:16G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778715189
    * TENANT_BY:database
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
| PostgreSQL-1-1 |                1 |    3 |      734.00 |           8.00 |            0.00 |        299.00 |          425.00 |              2 |           0 |          | database       |             2 | False         |               14.71 |
| PostgreSQL-1-2 |                2 |    3 |      734.00 |           8.00 |            0.00 |        299.00 |          425.00 |              2 |           0 |          | database       |             2 | False         |               14.71 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.74 |            14513.33 |           8193.10 |
| PostgreSQL-1-1-1-2 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.71 |            15229.16 |           8485.71 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.75 |            14393.83 |           8485.71 |
| PostgreSQL-1-1-2-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.75 |            14449.43 |           8485.71 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      88.00 |            1.27 |             8536.18 |           2700.00 |
| PostgreSQL-1-2-1-2 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      93.00 |            1.26 |             8598.28 |           2554.84 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.73 |            14796.53 |           8485.71 |
| PostgreSQL-1-2-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      29.00 |            0.74 |            14665.05 |           8193.10 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.73 |            14866.94 |          16386.21 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        2.00 | 3.00 |            44.00 |      28.00 |            0.75 |            14421.60 |          16971.43 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        2.00 | 3.00 |            44.00 |      93.00 |            1.26 |             8567.17 |           5109.68 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        2.00 | 3.00 |            44.00 |      29.00 |            0.73 |            14730.65 |          16386.21 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-1-2 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-1-2-2 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-1-2 |   PostgreSQL-1-2-2-1 |   PostgreSQL-1-2-2-2 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              2828.96 |              2461.53 |              2380.88 |              2371.56 |             27985.18 |             32789.52 |              2510.04 |              2465.50 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               732.54 |               621.74 |               608.89 |               868.20 |             15313.69 |             16049.95 |               564.92 |               579.18 |
| Shipping Priority (TPC-H Q3)                        |               778.48 |               755.12 |               741.22 |               782.98 |             15502.62 |             14693.20 |               748.87 |               751.86 |
| Order Priority Checking Query (TPC-H Q4)            |               381.96 |               345.77 |               351.44 |               369.74 |               617.86 |               395.56 |               377.95 |               387.46 |
| Local Supplier Volume (TPC-H Q5)                    |               869.04 |               707.43 |               805.84 |               754.24 |              1418.74 |               948.30 |               810.06 |               803.68 |
| Forecasting Revenue Change (TPC-H Q6)               |               482.20 |               446.46 |               461.13 |               420.20 |               451.95 |               487.22 |               442.34 |               463.89 |
| Forecasting Revenue Change (TPC-H Q7)               |               921.26 |               902.04 |               898.31 |               927.11 |              1018.17 |              1030.06 |               980.80 |               993.61 |
| National Market Share (TPC-H Q8)                    |               494.95 |               548.28 |               455.07 |               433.09 |              4499.00 |              5540.48 |               474.41 |               469.17 |
| Product Type Profit Measure (TPC-H Q9)              |              1813.10 |              1413.03 |              1976.19 |              1241.73 |              2042.20 |              1289.06 |              1908.97 |              1393.01 |
| Forecasting Revenue Change (TPC-H Q10)              |               586.67 |               762.52 |               634.12 |               618.39 |               613.83 |               747.17 |               620.05 |               622.66 |
| Important Stock Identification (TPC-H Q11)          |               263.38 |               262.67 |               317.73 |               306.73 |               213.85 |               301.53 |               240.68 |               248.62 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               562.56 |               626.47 |               658.86 |               684.83 |               638.88 |               750.02 |               672.33 |               671.53 |
| Customer Distribution (TPC-H Q13)                   |              2551.66 |              2385.29 |              2574.27 |              3060.35 |              2579.53 |              2612.10 |              2784.73 |              2793.04 |
| Forecasting Revenue Change (TPC-H Q14)              |               594.04 |               634.86 |               721.86 |               736.01 |               665.53 |               703.40 |               700.20 |               761.04 |
| Top Supplier Query (TPC-H Q15)                      |               535.74 |               579.25 |               628.94 |               563.90 |               529.97 |               616.17 |               552.91 |               596.57 |
| Parts/Supplier Relationship (TPC-H Q16)             |               520.22 |               558.61 |               554.39 |               550.29 |               597.08 |               586.28 |               570.33 |               621.11 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              2153.69 |              1910.79 |              2223.12 |              2242.26 |              2033.56 |              2091.37 |              1957.76 |              2002.83 |
| Large Volume Customer (TPC-H Q18)                   |              8739.90 |              8302.78 |              8105.81 |              8227.52 |              8168.57 |              8468.20 |              8301.33 |              9191.07 |
| Discounted Revenue (TPC-H Q19)                      |               122.10 |               111.36 |               130.47 |               132.47 |               135.29 |               132.21 |               126.63 |               133.13 |
| Potential Part Promotion (TPC-H Q20)                |               504.09 |               361.97 |               454.68 |               455.05 |               381.75 |               364.24 |               357.86 |               362.00 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               732.31 |               722.39 |               789.31 |               784.95 |               825.22 |               734.77 |               763.15 |               812.57 |
| Global Sales Opportunity Query (TPC-H Q22)          |               225.72 |               207.79 |               218.86 |               221.60 |               222.63 |               206.31 |               221.54 |               200.90 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       247.28 |      2.98 |          13.74 |                 23.66 |
| PostgreSQL-1-1-2 |       247.28 |      2.98 |          13.74 |                 23.66 |

### Loading phase: component data generator

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        64.61 |      0.75 |           0.01 |                  1.81 |
| PostgreSQL-1-1-2 |        64.61 |      0.75 |           0.01 |                  1.81 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       104.35 |      3.69 |          14.53 |                 24.11 |
| PostgreSQL-1-1-2 |         0.35 |      0.01 |          14.45 |                 24.03 |
| PostgreSQL-1-2-1 |       790.69 |      4.53 |          19.63 |                 28.40 |
| PostgreSQL-1-2-2 |         0.00 |      0.01 |          14.40 |                 23.16 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        24.91 |      0.00 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2 |        22.87 |      0.00 |           0.27 |                  0.27 |
| PostgreSQL-1-2-1 |        23.54 |      0.75 |           0.26 |                  0.26 |
| PostgreSQL-1-2-2 |        24.33 |      1.17 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    6.00 |
| PostgreSQL-1-1-2 |                      2.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    6.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   11.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                       11.00 |                                   10.00 |
| PostgreSQL-1-2-1 |                      2.00 |                                     0.00 |                                             0.00 |                       22.00 |                                   21.00 |
| PostgreSQL-1-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |

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
