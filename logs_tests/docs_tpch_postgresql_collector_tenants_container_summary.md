## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1475s 
* Code: 1781953244
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
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type cephcsi and size 15Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1323482
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1322247
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1322256
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1322168
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1323484
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1322248
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1322168
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1322176
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781953244
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781953244-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    3 |      372.00 |           2.00 |            0.00 |        138.00 |          225.00 |              1 |           0 |               29.03 |
| 1781953244-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    3 |      374.00 |           2.00 |            0.00 |        150.00 |          221.00 |              1 |           0 |               28.88 |
| 1781953244-PostgreSQL-1-2-0 |                2 | container      | False         |             2 |           0 |    3 |      372.00 |           2.00 |            0.00 |        138.00 |          225.00 |              1 |           0 |               29.03 |
| 1781953244-PostgreSQL-2-2-1 |                2 | container      | False         |             2 |           1 |    3 |      374.00 |           2.00 |            0.00 |        150.00 |          221.00 |              1 |           0 |               28.88 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.58 |            18578.40 |           9504.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2    | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         27 |            0.61 |            17607.25 |           8800.00 |           1 | PostgreSQL-2-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         23 |            0.55 |            19625.75 |          10330.43 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2    | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.58 |            18747.01 |           9504.00 |           1 | PostgreSQL-2-1-2-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        135 |            1.33 |             8110.86 |           1760.00 |           0 | PostgreSQL-1-2-1-1-1 |
| PostgreSQL-2-2-1-1-1 | PostgreSQL-2    | PostgreSQL-2-2-1 | PostgreSQL-2-2-1-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        128 |            1.29 |             8353.44 |           1856.25 |           1 | PostgreSQL-2-2-1-1-1 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         24 |            0.57 |            19067.15 |           9900.00 |           0 | PostgreSQL-1-2-2-1-1 |
| PostgreSQL-2-2-2-1-1 | PostgreSQL-2    | PostgreSQL-2-2-2 | PostgreSQL-2-2-2-1 |                2 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.59 |            18216.69 |           9504.00 |           1 | PostgreSQL-2-2-2-1-1 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         25 |            0.58 |            18578.40 |           9504.00 |           0 |
| PostgreSQL-2-1-1_1 | PostgreSQL-2-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         27 |            0.61 |            17607.25 |           8800.00 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |         23 |            0.55 |            19625.75 |          10330.43 |           0 |
| PostgreSQL-2-1-2_1 | PostgreSQL-2-1-2 |                1 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.58 |            18747.01 |           9504.00 |           1 |
| PostgreSQL-1-2-1_0 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        135 |            1.33 |             8110.86 |           1760.00 |           0 |
| PostgreSQL-2-2-1_1 | PostgreSQL-2-2-1 |                2 |        1 |               1 |           1 | 3.00 |               22 |        128 |            1.29 |             8353.44 |           1856.25 |           1 |
| PostgreSQL-1-2-2_0 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         24 |            0.57 |            19067.15 |           9900.00 |           0 |
| PostgreSQL-2-2-2_1 | PostgreSQL-2-2-2 |                2 |        2 |               1 |           1 | 3.00 |               22 |         25 |            0.59 |            18216.69 |           9504.00 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-2-1-1-1-1 |   PostgreSQL-2-1-2-1-1 |   PostgreSQL-2-2-1-1-1 |   PostgreSQL-2-2-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1968.97 |                1636.67 |               55777.73 |                1805.32 |                2125.26 |                1612.48 |               52333.81 |                1774.49 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 567.07 |                 472.12 |               12301.87 |                 539.18 |                 536.51 |                 484.88 |               10331.42 |                 545.20 |
| Shipping Priority (TPC-H Q3)                        |                 510.49 |                 536.96 |               27623.91 |                 505.88 |                 851.31 |                 749.25 |               23700.86 |                 738.85 |
| Order Priority Checking Query (TPC-H Q4)            |                 264.36 |                 257.75 |                 256.87 |                 255.32 |                 281.82 |                 261.78 |                 276.81 |                 237.93 |
| Local Supplier Volume (TPC-H Q5)                    |                 587.23 |                 545.27 |                1422.25 |                 814.95 |                 606.42 |                 547.50 |                1602.47 |                 851.00 |
| Forecasting Revenue Change (TPC-H Q6)               |                 301.22 |                 297.46 |                 561.73 |                 289.57 |                 302.48 |                 301.79 |                 304.82 |                 287.87 |
| Forecasting Revenue Change (TPC-H Q7)               |                 780.30 |                 692.28 |                 978.65 |                 713.90 |                 802.10 |                 726.42 |                 718.88 |                 702.42 |
| National Market Share (TPC-H Q8)                    |                 395.20 |                 345.27 |               11339.85 |                 346.91 |                 476.77 |                 310.72 |               12879.66 |                 336.97 |
| Product Type Profit Measure (TPC-H Q9)              |                1493.63 |                 842.05 |                6100.41 |                 977.22 |                1676.32 |                1228.72 |                7418.94 |                1360.17 |
| Forecasting Revenue Change (TPC-H Q10)              |                 510.78 |                 433.55 |                 730.36 |                 485.23 |                 572.85 |                 517.20 |                 558.50 |                 520.51 |
| Important Stock Identification (TPC-H Q11)          |                 203.14 |                 164.19 |                 163.12 |                 191.34 |                 188.05 |                 178.15 |                 155.63 |                 198.54 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 506.76 |                 419.95 |                 459.31 |                 458.60 |                 512.95 |                 493.45 |                 452.66 |                 442.35 |
| Customer Distribution (TPC-H Q13)                   |                2175.53 |                1872.04 |                1931.04 |                2825.88 |                2120.82 |                2527.83 |                1840.54 |                2546.99 |
| Forecasting Revenue Change (TPC-H Q14)              |                 572.29 |                 749.39 |                 498.44 |                 530.61 |                 579.26 |                 509.41 |                 524.28 |                 539.32 |
| Top Supplier Query (TPC-H Q15)                      |                 436.20 |                 531.25 |                 407.16 |                 402.34 |                 411.80 |                 412.51 |                 420.02 |                 408.08 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 431.02 |                 421.50 |                 412.98 |                 393.55 |                 417.25 |                 387.27 |                 409.02 |                 411.30 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                2085.58 |                1505.43 |                2123.36 |                1613.65 |                2400.66 |                1649.31 |                2632.25 |                1568.42 |
| Large Volume Customer (TPC-H Q18)                   |                8746.78 |                8769.72 |                8395.81 |                8434.65 |                8700.07 |                9211.58 |                8694.64 |                8542.21 |
| Discounted Revenue (TPC-H Q19)                      |                  86.73 |                 179.34 |                 130.41 |                  87.18 |                  88.03 |                  82.97 |                 120.37 |                  86.40 |
| Potential Part Promotion (TPC-H Q20)                |                 373.05 |                 352.49 |                 725.41 |                 330.67 |                 471.46 |                 466.46 |                 942.38 |                 959.30 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 538.34 |                 547.61 |                 833.85 |                1020.25 |                 516.14 |                 749.79 |                 835.90 |                 500.02 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 136.71 |                 131.08 |                 165.97 |                 127.58 |                 127.41 |                 185.68 |                 168.96 |                 128.86 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        56.80 |      0.43 |           4.94 |                  8.73 |
| PostgreSQL-1-1-2-1 |        56.80 |      0.43 |           4.94 |                  8.73 |
| PostgreSQL-2-1-1-1 |        85.63 |      1.13 |           5.18 |                  9.91 |
| PostgreSQL-2-1-2-1 |        85.63 |      1.13 |           5.18 |                  9.91 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-2-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-2-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        29.70 |      0.46 |           0.01 |                  2.19 |
| PostgreSQL-1-1-2-1 |        29.70 |      0.46 |           0.01 |                  2.19 |
| PostgreSQL-2-1-1-1 |        29.41 |      0.55 |           0.00 |                  0.51 |
| PostgreSQL-2-1-2-1 |        29.41 |      0.55 |           0.00 |                  0.51 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        49.48 |      1.34 |           4.90 |                  9.62 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           4.87 |                  9.60 |
| PostgreSQL-1-2-1-1 |        37.33 |      0.58 |           4.61 |                  8.72 |
| PostgreSQL-1-2-2-1 |         0.00 |      0.00 |           4.74 |                  9.07 |
| PostgreSQL-2-1-1-1 |        50.94 |      1.63 |           4.91 |                  9.63 |
| PostgreSQL-2-1-2-1 |         0.00 |      0.00 |           4.87 |                  9.60 |
| PostgreSQL-2-2-1-1 |       286.92 |      0.88 |           4.88 |                  9.66 |
| PostgreSQL-2-2-2-1 |         0.11 |      0.01 |           4.74 |                  9.07 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.52 |      0.50 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.51 |           0.26 |                  0.26 |
| PostgreSQL-1-2-1-1 |        12.76 |      0.38 |           0.25 |                  0.25 |
| PostgreSQL-1-2-2-1 |         0.00 |      0.01 |           0.25 |                  0.25 |
| PostgreSQL-2-1-1-1 |        12.91 |      0.00 |           0.25 |                  0.26 |
| PostgreSQL-2-1-2-1 |         0.00 |      0.00 |           0.25 |                  0.26 |
| PostgreSQL-2-2-1-1 |        13.00 |      0.01 |           0.28 |                  0.28 |
| PostgreSQL-2-2-2-1 |        11.09 |      0.00 |           0.28 |                  0.28 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-2-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-2-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    4.00 |
| PostgreSQL-1-1-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| PostgreSQL-1-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-2-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-2-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    1.00 |
| PostgreSQL-2-2-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    7.00 |
| PostgreSQL-2-2-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    5.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
