## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 1490s 
* Code: 1776772217
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
* PostgreSQL-BHT-1-0-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247634
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-0-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247634
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-0-2-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247634
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-0-2-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247635
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247634
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-BHT-1-1-1-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247634
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-BHT-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247635
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-BHT-1-1-2-2-1 uses docker image postgres:18.3
  * RAM:540493398016
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-106-generic
  * node:cl-worker38
  * disk:247635
  * datadisk:8188
  * volume_size:15G
  * volume_used:8.0G
  * cpu_list:0-127
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1776772217
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-1-0-1-1-1 |   PostgreSQL-BHT-1-0-1-2-1 |   PostgreSQL-BHT-1-0-2-1-1 |   PostgreSQL-BHT-1-0-2-2-1 |   PostgreSQL-BHT-1-1-1-1-1 |   PostgreSQL-BHT-1-1-1-2-1 |   PostgreSQL-BHT-1-1-2-1-1 |   PostgreSQL-BHT-1-1-2-2-1 |
|:----------------------------------------------------|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                    2615.95 |                    2661.80 |                   30407.60 |                    2476.80 |                    2768.79 |                    2708.28 |                   28363.40 |                    2530.29 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                     664.59 |                     775.55 |                   16971.50 |                     570.94 |                     672.90 |                     760.63 |                   14599.06 |                     614.43 |
| Shipping Priority (TPC-H Q3)                        |                    1090.42 |                    1231.20 |                   10798.98 |                     988.72 |                     809.83 |                     779.10 |                   12567.72 |                     692.16 |
| Order Priority Checking Query (TPC-H Q4)            |                     322.01 |                     372.92 |                     393.02 |                     377.14 |                     349.02 |                     380.65 |                     383.53 |                     316.82 |
| Local Supplier Volume (TPC-H Q5)                    |                     680.50 |                     843.25 |                    1312.73 |                     730.43 |                     758.14 |                     754.36 |                    1127.38 |                     766.59 |
| Forecasting Revenue Change (TPC-H Q6)               |                     439.26 |                     482.54 |                     509.44 |                     446.90 |                     430.29 |                     427.99 |                     468.62 |                     428.33 |
| Forecasting Revenue Change (TPC-H Q7)               |                     813.32 |                     866.45 |                    1137.22 |                     929.53 |                     865.47 |                     979.30 |                    1022.08 |                     900.36 |
| National Market Share (TPC-H Q8)                    |                     426.56 |                     488.05 |                    5849.91 |                     500.93 |                     467.80 |                     422.15 |                    6029.45 |                     454.83 |
| Product Type Profit Measure (TPC-H Q9)              |                    1085.26 |                    1373.76 |                    1448.94 |                    1386.56 |                    1222.72 |                    1241.79 |                    1516.96 |                    1366.25 |
| Forecasting Revenue Change (TPC-H Q10)              |                     652.58 |                     737.34 |                     874.62 |                     695.55 |                     665.01 |                     686.76 |                     851.03 |                     705.37 |
| Important Stock Identification (TPC-H Q11)          |                     230.79 |                     255.42 |                     304.49 |                     226.67 |                     226.28 |                     263.77 |                     381.68 |                     231.55 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                     687.49 |                     721.15 |                     720.95 |                     684.88 |                     641.29 |                     686.48 |                     727.07 |                     612.13 |
| Customer Distribution (TPC-H Q13)                   |                    2652.20 |                    2552.38 |                    2949.64 |                    2614.63 |                    2664.11 |                    2650.22 |                    3274.26 |                    2610.85 |
| Forecasting Revenue Change (TPC-H Q14)              |                     756.91 |                     728.97 |                     757.14 |                     704.62 |                     690.33 |                     746.27 |                     717.40 |                     689.75 |
| Top Supplier Query (TPC-H Q15)                      |                     596.13 |                     597.41 |                     585.48 |                     592.31 |                     596.65 |                     578.72 |                     583.97 |                     574.24 |
| Parts/Supplier Relationship (TPC-H Q16)             |                     552.99 |                     580.60 |                     621.33 |                     611.36 |                     600.37 |                     571.36 |                     618.38 |                     610.29 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                    1898.33 |                    1849.96 |                    2100.80 |                    1911.96 |                    2016.58 |                    1930.16 |                    2036.66 |                    2060.81 |
| Large Volume Customer (TPC-H Q18)                   |                    8641.77 |                    9241.55 |                    9141.97 |                    9933.50 |                    9212.74 |                    8391.47 |                    8463.62 |                    8366.63 |
| Discounted Revenue (TPC-H Q19)                      |                     131.81 |                     118.70 |                     131.80 |                     123.67 |                     128.31 |                     117.91 |                     124.29 |                     134.07 |
| Potential Part Promotion (TPC-H Q20)                |                     353.56 |                     367.48 |                     408.09 |                     525.13 |                     396.10 |                     373.78 |                     409.16 |                     424.17 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                     742.07 |                     743.50 |                     726.21 |                     840.62 |                     749.17 |                     773.49 |                     732.91 |                     742.78 |
| Global Sales Opportunity Query (TPC-H Q22)          |                     203.97 |                     218.92 |                     209.19 |                     244.84 |                     206.49 |                     214.82 |                     224.64 |                     220.14 |

### Loading [s]

| DBMS                     |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-------------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-1-0-1-1-1 |           0.00 |          302.00 |         2.00 |      379.00 |     685.00 |
| PostgreSQL-BHT-1-0-1-2-1 |           0.00 |          302.00 |         2.00 |      379.00 |     685.00 |
| PostgreSQL-BHT-1-0-2-1-1 |           0.00 |          302.00 |         2.00 |      379.00 |     685.00 |
| PostgreSQL-BHT-1-0-2-2-1 |           0.00 |          302.00 |         2.00 |      379.00 |     685.00 |
| PostgreSQL-BHT-1-1-1-1-1 |           0.00 |          300.00 |         3.00 |      378.00 |     683.00 |
| PostgreSQL-BHT-1-1-1-2-1 |           0.00 |          300.00 |         3.00 |      378.00 |     683.00 |
| PostgreSQL-BHT-1-1-2-1-1 |           0.00 |          300.00 |         3.00 |      378.00 |     683.00 |
| PostgreSQL-BHT-1-1-2-2-1 |           0.00 |          300.00 |         3.00 |      378.00 |     683.00 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                     |   Geo Times [s] |
|:-------------------------|----------------:|
| PostgreSQL-BHT-1-0-1-1-1 |            0.71 |
| PostgreSQL-BHT-1-0-1-2-1 |            0.76 |
| PostgreSQL-BHT-1-0-2-1-1 |            1.30 |
| PostgreSQL-BHT-1-0-2-2-1 |            0.75 |
| PostgreSQL-BHT-1-1-1-1-1 |            0.72 |
| PostgreSQL-BHT-1-1-1-2-1 |            0.73 |
| PostgreSQL-BHT-1-1-2-1-1 |            1.29 |
| PostgreSQL-BHT-1-1-2-2-1 |            0.72 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                     |   Power@Size [~Q/h] |
|:-------------------------|--------------------:|
| PostgreSQL-BHT-1-0-1-1-1 |            15197.72 |
| PostgreSQL-BHT-1-0-1-2-1 |            14211.46 |
| PostgreSQL-BHT-1-0-2-1-1 |             8280.05 |
| PostgreSQL-BHT-1-0-2-2-1 |            14314.91 |
| PostgreSQL-BHT-1-1-1-1-1 |            14943.38 |
| PostgreSQL-BHT-1-1-1-2-1 |            14799.72 |
| PostgreSQL-BHT-1-1-2-1-1 |             8352.95 |
| PostgreSQL-BHT-1-1-2-2-1 |            15093.65 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                   |   time [s] |   count |   SF |   Throughput@Size |
|:-----------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-1-0-1-1 |      28.00 |    1.00 | 3.00 |           8485.71 |
| PostgreSQL-BHT-1-0-1-2 |      31.00 |    1.00 | 3.00 |           7664.52 |
| PostgreSQL-BHT-1-0-2-1 |      91.00 |    1.00 | 3.00 |           2610.99 |
| PostgreSQL-BHT-1-0-2-2 |      32.00 |    1.00 | 3.00 |           7425.00 |
| PostgreSQL-BHT-1-1-1-1 |      29.00 |    1.00 | 3.00 |           8193.10 |
| PostgreSQL-BHT-1-1-1-2 |      30.00 |    1.00 | 3.00 |           7920.00 |
| PostgreSQL-BHT-1-1-2-1 |      88.00 |    1.00 | 3.00 |           2700.00 |
| PostgreSQL-BHT-1-1-2-2 |      31.00 |    1.00 | 3.00 |           7664.52 |

### Workflow

| DBMS                     | orig_name              |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-------------------------|:-----------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-1-0-1-1-1 | PostgreSQL-BHT-1-0-1-1 | 3.00 |      1 |                1 |            1 |        1776772875 |      1776772903 |
| PostgreSQL-BHT-1-0-1-2-1 | PostgreSQL-BHT-1-0-1-2 | 3.00 |      1 |                1 |            2 |        1776773019 |      1776773050 |
| PostgreSQL-BHT-1-0-2-1-1 | PostgreSQL-BHT-1-0-2-1 | 3.00 |      1 |                2 |            1 |        1776773428 |      1776773519 |
| PostgreSQL-BHT-1-0-2-2-1 | PostgreSQL-BHT-1-0-2-2 | 3.00 |      1 |                2 |            2 |        1776773614 |      1776773646 |
| PostgreSQL-BHT-1-1-1-1-1 | PostgreSQL-BHT-1-1-1-1 | 3.00 |      1 |                1 |            1 |        1776772874 |      1776772903 |
| PostgreSQL-BHT-1-1-1-2-1 | PostgreSQL-BHT-1-1-1-2 | 3.00 |      1 |                1 |            2 |        1776773019 |      1776773049 |
| PostgreSQL-BHT-1-1-2-1-1 | PostgreSQL-BHT-1-1-2-1 | 3.00 |      1 |                2 |            1 |        1776773428 |      1776773516 |
| PostgreSQL-BHT-1-1-2-2-1 | PostgreSQL-BHT-1-1-2-2 | 3.00 |      1 |                2 |            2 |        1776773614 |      1776773645 |

#### Actual

* DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1], [1, 1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |       145.66 |      1.22 |           9.76 |                 15.66 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |       145.66 |      1.22 |           9.76 |                 15.66 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |       143.47 |      1.49 |           9.78 |                 15.70 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |       143.47 |      1.49 |           9.78 |                 15.70 |

### Loading phase: component data generator

| DBMS                              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |        31.53 |      0.31 |           0.00 |                  1.04 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |        31.53 |      0.31 |           0.00 |                  1.04 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |        32.74 |      0.29 |           0.01 |                  1.87 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |        32.74 |      0.29 |           0.01 |                  1.87 |

### Execution phase: SUT deployment

| DBMS                              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |        66.69 |      2.20 |          11.61 |                 16.42 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |        75.17 |      3.13 |          12.59 |                 17.40 |
| 1776772217-PostgreSQL-BHT-1-0-2-1 |        79.42 |      1.21 |          10.13 |                 14.51 |
| 1776772217-PostgreSQL-BHT-1-0-2-2 |       105.36 |      3.43 |          10.11 |                 14.50 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |         0.00 |      0.01 |           9.52 |                 14.72 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |         0.00 |      0.01 |          10.07 |                 14.88 |
| 1776772217-PostgreSQL-BHT-1-1-2-1 |       394.30 |      1.20 |          10.09 |                 14.90 |
| 1776772217-PostgreSQL-BHT-1-1-2-2 |        26.02 |      0.63 |          10.12 |                 14.50 |

### Execution phase: component benchmarker

| DBMS                              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------------------|-------------:|----------:|---------------:|----------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |         0.00 |      0.01 |           0.00 |                  0.00 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |        12.02 |      0.35 |           0.29 |                  0.30 |
| 1776772217-PostgreSQL-BHT-1-0-2-1 |        11.94 |      0.36 |           0.26 |                  0.26 |
| 1776772217-PostgreSQL-BHT-1-0-2-2 |        11.96 |      0.37 |           0.29 |                  0.29 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |        11.35 |      0.00 |           0.26 |                  0.26 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |        11.77 |      0.00 |           0.26 |                  0.26 |
| 1776772217-PostgreSQL-BHT-1-1-2-1 |        12.40 |      0.01 |           0.28 |                  0.29 |
| 1776772217-PostgreSQL-BHT-1-1-2-2 |        11.87 |      0.01 |           0.28 |                  0.29 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                              |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS                              |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| 1776772217-PostgreSQL-BHT-1-0-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| 1776772217-PostgreSQL-BHT-1-0-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    4.00 |
| 1776772217-PostgreSQL-BHT-1-0-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    7.00 |
| 1776772217-PostgreSQL-BHT-1-0-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    5.00 |
| 1776772217-PostgreSQL-BHT-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| 1776772217-PostgreSQL-BHT-1-1-1-2 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |
| 1776772217-PostgreSQL-BHT-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        7.00 |                                    7.00 |
| 1776772217-PostgreSQL-BHT-1-1-2-2 |                      0.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |

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
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
