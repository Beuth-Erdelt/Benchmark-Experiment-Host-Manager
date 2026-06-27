## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1409s 
* Code: 1781946415
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type cephcsi and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1300639
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1300639
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1300724
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1300724
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324146
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324146
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324145
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1324145
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781946415
    * TENANT_BY:schema
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781946415-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    3 |      221.00 |           2.00 |            0.00 |        221.00 |          317.00 |              2 |           0 |               48.87 |
| 1781946415-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    3 |      222.00 |           2.00 |            0.00 |        222.00 |          317.00 |              2 |           0 |               48.65 |
| 1781946415-PostgreSQL-1-2-0 |                2 | schema         | False         |             2 |           0 |    3 |      221.00 |           2.00 |            0.00 |        221.00 |          317.00 |              2 |           0 |               48.87 |
| 1781946415-PostgreSQL-1-2-1 |                2 | schema         | False         |             2 |           1 |    3 |      222.00 |           2.00 |            0.00 |        222.00 |          317.00 |              2 |           0 |               48.65 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.61 |            17796.40 |           9504.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.58 |            18481.64 |           9504.00 |           1 | PostgreSQL-1-1-1-1-2 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         24 |            0.60 |            17971.05 |           9900.00 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         26 |            0.62 |            17375.50 |           9138.46 |           1 | PostgreSQL-1-1-2-1-2 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        148 |            1.45 |             7431.15 |           1605.41 |           0 | PostgreSQL-1-2-1-1-1 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        137 |            1.38 |             7810.68 |           1734.31 |           1 | PostgreSQL-1-2-1-1-2 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         26 |            0.59 |            18246.61 |           9138.46 |           0 | PostgreSQL-1-2-2-1-1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         26 |            0.61 |            17816.00 |           9138.46 |           1 | PostgreSQL-1-2-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.61 |            17796.40 |           9504.00 |           0 |
| PostgreSQL-1-1-1_1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.58 |            18481.64 |           9504.00 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |         24 |            0.60 |            17971.05 |           9900.00 |           0 |
| PostgreSQL-1-1-2_1 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |         26 |            0.62 |            17375.50 |           9138.46 |           1 |
| PostgreSQL-1-2-1_0 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        148 |            1.45 |             7431.15 |           1605.41 |           0 |
| PostgreSQL-1-2-1_1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        137 |            1.38 |             7810.68 |           1734.31 |           1 |
| PostgreSQL-1-2-2_0 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         26 |            0.59 |            18246.61 |           9138.46 |           0 |
| PostgreSQL-1-2-2_1 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         26 |            0.61 |            17816.00 |           9138.46 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-1-1-2 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1644.04 |                1659.15 |                1667.47 |                1848.05 |               55315.25 |               49534.45 |                2400.98 |                2236.90 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 571.40 |                 575.31 |                 639.45 |                 595.63 |               13936.73 |               12711.18 |                 549.97 |                 504.47 |
| Shipping Priority (TPC-H Q3)                        |                 557.08 |                 532.85 |                 554.61 |                 511.54 |               29146.50 |               26001.50 |                 505.71 |                 486.94 |
| Order Priority Checking Query (TPC-H Q4)            |                 256.10 |                 461.39 |                 283.83 |                 264.29 |                 279.53 |                 275.71 |                 262.42 |                 266.32 |
| Local Supplier Volume (TPC-H Q5)                    |                 651.91 |                1089.53 |                 623.11 |                 590.65 |                1520.06 |                1439.71 |                 622.09 |                 633.93 |
| Forecasting Revenue Change (TPC-H Q6)               |                 632.96 |                 313.45 |                 308.13 |                 317.62 |                 678.81 |                 296.70 |                 297.74 |                 298.14 |
| Forecasting Revenue Change (TPC-H Q7)               |                1022.98 |                 714.56 |                 769.81 |                1428.28 |                 918.85 |                 774.51 |                1009.86 |                1088.71 |
| National Market Share (TPC-H Q8)                    |                 441.31 |                 377.04 |                 466.69 |                 466.92 |               16618.29 |               15073.18 |                 386.43 |                 463.23 |
| Product Type Profit Measure (TPC-H Q9)              |                1574.08 |                 991.37 |                1867.90 |                1048.14 |                8302.11 |                9898.93 |                1511.17 |                1033.80 |
| Forecasting Revenue Change (TPC-H Q10)              |                 585.27 |                 496.28 |                 563.75 |                 514.94 |                 548.88 |                 616.59 |                 553.09 |                 473.49 |
| Important Stock Identification (TPC-H Q11)          |                 196.41 |                 185.55 |                 235.51 |                 214.64 |                 174.62 |                 176.30 |                 209.43 |                 210.07 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 464.07 |                 459.11 |                 482.39 |                 516.54 |                 448.62 |                 496.46 |                 468.61 |                 464.43 |
| Customer Distribution (TPC-H Q13)                   |                1998.42 |                1978.59 |                2132.47 |                2146.06 |                2968.52 |                2152.63 |                2824.41 |                2704.48 |
| Forecasting Revenue Change (TPC-H Q14)              |                 547.84 |                 550.35 |                 571.69 |                 563.73 |                 693.52 |                 547.20 |                 553.78 |                 610.33 |
| Top Supplier Query (TPC-H Q15)                      |                 409.29 |                 413.81 |                 421.92 |                 414.93 |                 576.80 |                 421.51 |                 416.18 |                 409.89 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 388.62 |                 393.46 |                 402.46 |                 396.95 |                 537.19 |                 443.21 |                 402.05 |                 432.04 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                2436.79 |                2716.62 |                2368.86 |                2793.07 |                2021.09 |                2891.68 |                1722.53 |                1714.97 |
| Large Volume Customer (TPC-H Q18)                   |                8119.42 |                8368.80 |                8417.36 |                8777.32 |               10132.72 |               10358.28 |                9421.13 |                9223.45 |
| Discounted Revenue (TPC-H Q19)                      |                  93.71 |                  87.83 |                  94.34 |                  84.37 |                 158.85 |                 221.63 |                  94.85 |                 163.38 |
| Potential Part Promotion (TPC-H Q20)                |                 344.76 |                 324.08 |                 349.02 |                 305.59 |                 717.36 |                 897.41 |                 307.95 |                 440.51 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 533.19 |                 522.11 |                 537.01 |                 966.23 |                 513.90 |                 558.98 |                 530.80 |                 529.55 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 135.86 |                 135.81 |                 134.89 |                 211.09 |                 138.13 |                 141.62 |                 142.60 |                 140.57 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       183.25 |      3.15 |          10.14 |                 19.56 |
| PostgreSQL-1-1-2-1 |       183.25 |      3.15 |          10.14 |                 19.56 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        76.60 |      0.62 |           0.01 |                  1.59 |
| PostgreSQL-1-1-2-1 |        76.60 |      0.62 |           0.01 |                  1.59 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        68.22 |      1.89 |           9.61 |                 19.03 |
| PostgreSQL-1-1-2-1 |        30.12 |      1.07 |           9.52 |                 18.93 |
| PostgreSQL-1-2-1-1 |       578.21 |      1.30 |           9.38 |                 18.94 |
| PostgreSQL-1-2-2-1 |         0.05 |      0.01 |           9.08 |                 17.73 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-2-1-1 |        27.50 |      1.14 |           0.27 |                  0.27 |
| PostgreSQL-1-2-2-1 |        13.21 |      0.01 |           0.27 |                  0.27 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    8.00 |
| PostgreSQL-1-2-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                       14.00 |                                   14.00 |
| PostgreSQL-1-2-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    2.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
