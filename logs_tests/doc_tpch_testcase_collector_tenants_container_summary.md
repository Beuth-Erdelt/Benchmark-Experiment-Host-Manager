## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 2157s 
* Code: 1778717082
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
  * disk:197650
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197650
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197651
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197651
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197650
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197650
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197651
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:197651
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1778717082
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

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   tenant | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|---------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      654.00 |           4.00 |            0.00 |        242.00 |          398.00 |              1 |           0 |        0 | container      |             2 | False         |               16.51 |
| PostgreSQL-1-2 |                2 |    3 |      654.00 |           4.00 |            0.00 |        242.00 |          398.00 |              1 |           0 |        0 | container      |             2 | False         |               16.51 |
| PostgreSQL-2-1 |                1 |    3 |      646.00 |           4.00 |            0.00 |        247.00 |          394.00 |              1 |           0 |        1 | container      |             2 | False         |               16.72 |
| PostgreSQL-2-2 |                2 |    3 |      646.00 |           4.00 |            0.00 |        247.00 |          394.00 |              1 |           0 |        1 | container      |             2 | False         |               16.72 |

### Execution

#### Per Connection

|                    |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.71 |            15106.06 |           8485.71 |
| PostgreSQL-2-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      30.00 |            0.78 |            13927.25 |           7920.00 |
| PostgreSQL-1-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.70 |            15518.28 |           8485.71 |
| PostgreSQL-2-1-2-1 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.70 |            15442.89 |           8800.00 |
| PostgreSQL-1-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      88.00 |            1.28 |             8436.62 |           2700.00 |
| PostgreSQL-2-2-1-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      86.00 |            1.28 |             8422.34 |           2762.79 |
| PostgreSQL-1-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.71 |            15201.88 |           8800.00 |
| PostgreSQL-2-2-2-1 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      31.00 |            0.75 |            14411.15 |           7664.52 |

#### Per Phase

|                  |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |
|:-----------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|
| PostgreSQL-1-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.71 |            15106.06 |           8485.71 |
| PostgreSQL-1-1-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      28.00 |            0.70 |            15518.28 |           8485.71 |
| PostgreSQL-2-1-1 |             1.00 |     1.00 |        1.00 | 3.00 |            22.00 |      30.00 |            0.78 |            13927.25 |           7920.00 |
| PostgreSQL-2-1-2 |             1.00 |     2.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.70 |            15442.89 |           8800.00 |
| PostgreSQL-1-2-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      88.00 |            1.28 |             8436.62 |           2700.00 |
| PostgreSQL-1-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      27.00 |            0.71 |            15201.88 |           8800.00 |
| PostgreSQL-2-2-1 |             2.00 |     1.00 |        1.00 | 3.00 |            22.00 |      86.00 |            1.28 |             8422.34 |           2762.79 |
| PostgreSQL-2-2-2 |             2.00 |     2.00 |        1.00 | 3.00 |            22.00 |      31.00 |            0.75 |            14411.15 |           7664.52 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1 |   PostgreSQL-1-1-2-1 |   PostgreSQL-1-2-1-1 |   PostgreSQL-1-2-2-1 |   PostgreSQL-2-1-1-1 |   PostgreSQL-2-1-2-1 |   PostgreSQL-2-2-1-1 |   PostgreSQL-2-2-2-1 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              2413.78 |              2462.88 |             27642.06 |              2413.98 |              2494.69 |              2506.44 |             29761.43 |              2446.23 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               664.72 |               617.82 |             16067.42 |               632.34 |               817.81 |               601.99 |             15000.39 |               619.11 |
| Shipping Priority (TPC-H Q3)                        |               755.33 |               705.52 |             13830.70 |               743.50 |               840.69 |               700.84 |             11390.01 |               630.66 |
| Order Priority Checking Query (TPC-H Q4)            |               386.17 |               373.11 |               409.06 |               353.20 |               409.49 |               350.61 |               581.54 |               342.37 |
| Local Supplier Volume (TPC-H Q5)                    |               771.11 |               846.72 |              1045.77 |               855.10 |               784.09 |               785.05 |              1101.12 |               834.07 |
| Forecasting Revenue Change (TPC-H Q6)               |               453.31 |               472.99 |               490.52 |               445.83 |               475.91 |               469.59 |               426.58 |               418.26 |
| Forecasting Revenue Change (TPC-H Q7)               |               950.04 |               943.84 |              1044.63 |              1027.67 |              1077.35 |               861.06 |               980.52 |              1026.00 |
| National Market Share (TPC-H Q8)                    |               551.31 |               442.27 |              5813.01 |               458.78 |               573.39 |               419.45 |              4423.90 |               476.79 |
| Product Type Profit Measure (TPC-H Q9)              |              1321.12 |              1198.21 |              1520.28 |              1296.64 |              1423.73 |              1248.10 |              1481.63 |              1413.94 |
| Forecasting Revenue Change (TPC-H Q10)              |               690.05 |               697.61 |               858.49 |               634.99 |               700.24 |               657.39 |               822.77 |               683.48 |
| Important Stock Identification (TPC-H Q11)          |               280.46 |               229.61 |               322.35 |               268.91 |               305.17 |               233.91 |               384.14 |               266.84 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               608.30 |               711.05 |               754.39 |               698.60 |               657.70 |               598.38 |               714.95 |               607.47 |
| Customer Distribution (TPC-H Q13)                   |              2557.73 |              2429.03 |              3101.24 |              2733.81 |              2534.01 |              2476.01 |              2988.84 |              3712.36 |
| Forecasting Revenue Change (TPC-H Q14)              |               517.89 |               500.79 |               538.37 |               494.29 |               697.28 |               731.39 |               750.59 |               757.89 |
| Top Supplier Query (TPC-H Q15)                      |               543.27 |               556.14 |               572.75 |               529.48 |               567.58 |               575.36 |               563.40 |               640.54 |
| Parts/Supplier Relationship (TPC-H Q16)             |               568.11 |               580.07 |               585.78 |               616.61 |               546.71 |               577.28 |               597.01 |               659.64 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1967.77 |              1832.00 |              2205.87 |              2043.99 |              2080.38 |              1839.45 |              2091.59 |              2368.77 |
| Large Volume Customer (TPC-H Q18)                   |              8176.67 |              9512.45 |              8137.32 |              8347.02 |              9011.96 |              8049.58 |              9166.25 |             10564.02 |
| Discounted Revenue (TPC-H Q19)                      |               121.04 |               107.32 |               129.15 |               118.23 |               162.08 |               119.14 |               118.68 |               122.77 |
| Potential Part Promotion (TPC-H Q20)                |               389.94 |               373.69 |               417.14 |               376.23 |               437.10 |               335.52 |               442.30 |               388.94 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |               748.49 |               712.30 |               779.22 |               718.75 |               745.00 |               815.79 |               721.21 |               779.99 |
| Global Sales Opportunity Query (TPC-H Q22)          |               200.95 |               192.79 |               218.29 |               201.92 |               211.53 |               232.67 |               215.05 |               181.06 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |       137.89 |      1.24 |           9.81 |                 15.76 |
| PostgreSQL-1-1-2 |       137.89 |      1.24 |           9.81 |                 15.76 |
| PostgreSQL-2-1-1 |       127.77 |      1.71 |           9.54 |                 15.69 |
| PostgreSQL-2-1-2 |       127.77 |      1.71 |           9.54 |                 15.69 |

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
| PostgreSQL-1-1-1 |        28.86 |      0.39 |           0.01 |                  1.26 |
| PostgreSQL-1-1-2 |        28.86 |      0.39 |           0.01 |                  1.26 |
| PostgreSQL-2-1-1 |        27.96 |      0.37 |           0.01 |                  1.50 |
| PostgreSQL-2-1-2 |        27.96 |      0.37 |           0.01 |                  1.50 |

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |         1.15 |      0.08 |           9.61 |                 14.42 |
| PostgreSQL-1-1-2 |         0.06 |      0.01 |          10.07 |                 14.88 |
| PostgreSQL-1-2-1 |        50.51 |      1.21 |           9.85 |                 13.99 |
| PostgreSQL-1-2-2 |        17.88 |      0.67 |          10.15 |                 14.54 |
| PostgreSQL-2-1-1 |        61.59 |      1.45 |          10.10 |                 14.91 |
| PostgreSQL-2-1-2 |         9.29 |      0.35 |          10.17 |                 14.98 |
| PostgreSQL-2-2-1 |        52.96 |      1.11 |           9.90 |                 14.03 |
| PostgreSQL-2-2-2 |        23.31 |      0.88 |          10.15 |                 14.54 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1 |        12.03 |      0.38 |           0.29 |                  0.29 |
| PostgreSQL-1-1-2 |         0.18 |      0.39 |           0.29 |                  0.29 |
| PostgreSQL-1-2-1 |        12.65 |      0.41 |           0.26 |                  0.26 |
| PostgreSQL-1-2-2 |         4.10 |      0.22 |           0.26 |                  0.26 |
| PostgreSQL-2-1-1 |        12.00 |      0.00 |           0.29 |                  0.29 |
| PostgreSQL-2-1-2 |        12.21 |      0.00 |           0.30 |                  0.30 |
| PostgreSQL-2-2-1 |        11.63 |      0.00 |           0.25 |                  0.26 |
| PostgreSQL-2-2-2 |         0.02 |      0.00 |           0.25 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-2-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS             |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-----------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    5.00 |
| PostgreSQL-1-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| PostgreSQL-1-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |
| PostgreSQL-2-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |
| PostgreSQL-2-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-2-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |

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
