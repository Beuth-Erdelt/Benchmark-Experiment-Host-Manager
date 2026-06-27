## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1930s 
* Code: 1778326643
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.7.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 16 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker21.
  * Loading is tested with [1] threads, split into [16] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-BHT-16-1-1-1 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108972
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-1-1-2 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108972
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-1-2-1 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108972
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-1-2-2 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108972
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-2-1-1 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108973
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-2-1-2 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108973
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-2-2-1 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108974
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-16-2-2-2 uses docker image postgres:18.3
  * RAM:608117161984
  * CPU:AMD EPYC 7542 32-Core Processor
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker21
  * disk:108974
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1778326643
    * TENANT_BY:database
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-BHT-16 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-16 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                     |       code | configuration     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:--------------------|-----------:|:------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-BHT-16-1 | 1778326643 | PostgreSQL-BHT-16 |                1 |    1 |      495.00 |           7.00 |           47.00 |         17.00 |          419.00 |             16 | database       |             2 | False         |                7.27 |
| PostgreSQL-BHT-16-2 | 1778326643 | PostgreSQL-BHT-16 |                2 |    1 |      496.00 |           6.00 |           48.00 |         16.00 |          420.00 |             16 | database       |             2 | False         |                7.26 |

### Execution

#### Per Connection

|                         |       code | configuration     | phase                 | connection              |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size | pod                     |
|:------------------------|-----------:|:------------------|:----------------------|:------------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|:------------------------|
| PostgreSQL-BHT-16-1-1-1 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-1-1 | PostgreSQL-BHT-16-1-1-1 |                1 |        1 |           1 | 1.00 |               22 |         16 |            0.46 |             7855.35 |           4950.00 | PostgreSQL-BHT-16-1-1-1 |
| PostgreSQL-BHT-16-1-1-2 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-1-1 | PostgreSQL-BHT-16-1-1-2 |                1 |        1 |           1 | 1.00 |               22 |         16 |            0.45 |             8004.27 |           4950.00 | PostgreSQL-BHT-16-1-1-2 |
| PostgreSQL-BHT-16-1-2-1 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-1-2 | PostgreSQL-BHT-16-1-2-1 |                1 |        2 |           1 | 1.00 |               22 |         16 |            0.44 |             8114.37 |           4950.00 | PostgreSQL-BHT-16-1-2-1 |
| PostgreSQL-BHT-16-1-2-2 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-1-2 | PostgreSQL-BHT-16-1-2-2 |                1 |        2 |           1 | 1.00 |               22 |         16 |            0.44 |             8268.82 |           4950.00 | PostgreSQL-BHT-16-1-2-2 |
| PostgreSQL-BHT-16-2-1-1 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-2-1 | PostgreSQL-BHT-16-2-1-1 |                2 |        1 |           1 | 1.00 |               22 |         15 |            0.44 |             8099.21 |           5280.00 | PostgreSQL-BHT-16-2-1-1 |
| PostgreSQL-BHT-16-2-1-2 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-2-1 | PostgreSQL-BHT-16-2-1-2 |                2 |        1 |           1 | 1.00 |               22 |         16 |            0.45 |             8061.52 |           4950.00 | PostgreSQL-BHT-16-2-1-2 |
| PostgreSQL-BHT-16-2-2-1 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-2-2 | PostgreSQL-BHT-16-2-2-1 |                2 |        2 |           1 | 1.00 |               22 |         18 |            0.44 |             8127.95 |           4400.00 | PostgreSQL-BHT-16-2-2-1 |
| PostgreSQL-BHT-16-2-2-2 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-2-2 | PostgreSQL-BHT-16-2-2-2 |                2 |        2 |           1 | 1.00 |               22 |         18 |            0.44 |             8101.02 |           4400.00 | PostgreSQL-BHT-16-2-2-2 |

#### Per Phase

|                       |       code | configuration     | phase                 | connection              |   experiment_run |   client |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size | pod   |
|:----------------------|-----------:|:------------------|:----------------------|:------------------------|-----------------:|---------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|:------|
| PostgreSQL-BHT-16-1-1 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-1-1 | PostgreSQL-BHT-16-1-1-2 |                1 |        1 |           2 | 1.00 |               44 |         16 |            0.45 |             7929.46 |           9900.00 | -     |
| PostgreSQL-BHT-16-1-2 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-1-2 | PostgreSQL-BHT-16-1-2-2 |                1 |        2 |           2 | 1.00 |               44 |         16 |            0.44 |             8191.23 |           9900.00 | -     |
| PostgreSQL-BHT-16-2-1 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-2-1 | PostgreSQL-BHT-16-2-1-2 |                2 |        1 |           2 | 1.00 |               44 |         16 |            0.45 |             8080.34 |           9900.00 | -     |
| PostgreSQL-BHT-16-2-2 | 1778326643 | PostgreSQL-BHT-16 | PostgreSQL-BHT-16-2-2 | PostgreSQL-BHT-16-2-2-2 |                2 |        2 |           2 | 1.00 |               44 |         18 |            0.44 |             8114.47 |           8800.00 | -     |

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-16-1-1-1 |   PostgreSQL-BHT-16-1-1-2 |   PostgreSQL-BHT-16-1-2-1 |   PostgreSQL-BHT-16-1-2-2 |   PostgreSQL-BHT-16-2-1-1 |   PostgreSQL-BHT-16-2-1-2 |   PostgreSQL-BHT-16-2-2-1 |   PostgreSQL-BHT-16-2-2-2 |
|:----------------------------------------------------|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|--------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                   1082.08 |                   1078.97 |                   1102.83 |                   1077.43 |                   1099.29 |                   1117.38 |                   1098.26 |                   1103.50 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                    580.86 |                    581.37 |                    543.13 |                    538.11 |                    550.60 |                    557.31 |                    556.45 |                    558.99 |
| Shipping Priority (TPC-H Q3)                        |                    374.90 |                    381.38 |                    351.58 |                    351.81 |                    381.27 |                    387.48 |                    353.57 |                    362.11 |
| Order Priority Checking Query (TPC-H Q4)            |                    199.14 |                    199.88 |                    188.60 |                    189.59 |                    196.50 |                    197.86 |                    191.75 |                    196.58 |
| Local Supplier Volume (TPC-H Q5)                    |                    435.33 |                    438.44 |                    437.60 |                    429.85 |                    435.85 |                    441.54 |                    433.24 |                    436.41 |
| Forecasting Revenue Change (TPC-H Q6)               |                    238.81 |                    236.89 |                    236.90 |                    237.68 |                    245.51 |                    242.52 |                    244.13 |                    246.34 |
| Forecasting Revenue Change (TPC-H Q7)               |                    853.46 |                    855.14 |                    862.58 |                    851.48 |                    860.69 |                    862.08 |                    864.69 |                    866.50 |
| National Market Share (TPC-H Q8)                    |                    631.76 |                    631.63 |                    593.46 |                    594.58 |                    611.54 |                    623.86 |                    589.94 |                    604.35 |
| Product Type Profit Measure (TPC-H Q9)              |                   1022.12 |                   1042.63 |                   1014.56 |                   1007.18 |                   1046.63 |                   1060.15 |                   1038.88 |                   1052.56 |
| Forecasting Revenue Change (TPC-H Q10)              |                   1106.01 |                   1108.75 |                   1126.76 |                   1112.71 |                   1122.19 |                   1142.41 |                   1158.38 |                   1134.07 |
| Important Stock Identification (TPC-H Q11)          |                    281.97 |                    282.84 |                    270.02 |                    275.73 |                    272.36 |                    267.09 |                    273.17 |                    276.20 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                    349.67 |                    349.68 |                    346.49 |                    352.22 |                    345.54 |                    349.33 |                    354.87 |                    354.95 |
| Customer Distribution (TPC-H Q13)                   |                   1160.40 |                   1160.19 |                    956.54 |                   1008.08 |                    904.22 |                    924.99 |                    921.70 |                    962.01 |
| Forecasting Revenue Change (TPC-H Q14)              |                    395.60 |                    256.07 |                    394.73 |                    258.17 |                    258.57 |                    263.57 |                    269.07 |                    272.57 |
| Top Supplier Query (TPC-H Q15)                      |                    261.86 |                    260.53 |                    259.68 |                    261.64 |                    266.44 |                    266.04 |                    275.72 |                    275.08 |
| Parts/Supplier Relationship (TPC-H Q16)             |                    287.37 |                    287.32 |                    290.57 |                    285.08 |                    298.85 |                    297.02 |                    295.85 |                    291.18 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                    917.91 |                    900.87 |                    880.14 |                    894.34 |                    885.06 |                    885.36 |                    942.64 |                    893.25 |
| Large Volume Customer (TPC-H Q18)                   |                   3093.99 |                   3096.48 |                   3077.57 |                   3089.99 |                   3184.40 |                   3132.24 |                   3106.89 |                   3114.51 |
| Discounted Revenue (TPC-H Q19)                      |                     74.24 |                     71.92 |                     74.24 |                     71.57 |                     71.44 |                     72.20 |                     73.32 |                     73.57 |
| Potential Part Promotion (TPC-H Q20)                |                    168.25 |                    168.30 |                    152.83 |                    158.68 |                    170.23 |                    164.45 |                    161.81 |                    156.55 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                    731.23 |                    746.57 |                    731.83 |                    723.26 |                    734.10 |                    744.26 |                    746.32 |                    746.61 |
| Global Sales Opportunity Query (TPC-H Q22)          |                    133.52 |                    134.96 |                    118.93 |                    118.30 |                    135.37 |                    135.24 |                    121.06 |                    122.57 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |        56.47 |      1.77 |           6.69 |                  8.38 |
| PostgreSQL-BHT-16-1-2 |        56.47 |      1.77 |           6.69 |                  8.38 |
| PostgreSQL-BHT-16-2-1 |       322.01 |      1.28 |           8.70 |                 11.05 |
| PostgreSQL-BHT-16-2-2 |       322.01 |      1.28 |           8.70 |                 11.05 |

### Loading phase: component data generator

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-1-2 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-2-2 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |         0.71 |      0.01 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-1-2 |         0.71 |      0.01 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-2-1 |         0.95 |      0.01 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-2-2 |         0.95 |      0.01 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |         0.16 |      0.01 |           8.34 |                 10.70 |
| PostgreSQL-BHT-16-1-2 |         0.00 |      0.01 |           8.70 |                 11.05 |
| PostgreSQL-BHT-16-2-1 |         0.16 |      0.01 |           8.34 |                 10.70 |
| PostgreSQL-BHT-16-2-2 |         0.00 |      0.01 |           8.70 |                 11.06 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-16-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-1-2 |         0.03 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-BHT-16-2-2 |         0.03 |      0.00 |           0.00 |                  0.00 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-16-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                       22.00 |                                   19.00 |
| PostgreSQL-BHT-16-1-2 |                      3.00 |                                     0.00 |                                             0.00 |                       22.00 |                                   19.00 |
| PostgreSQL-BHT-16-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                       21.00 |                                   20.00 |
| PostgreSQL-BHT-16-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                       21.00 |                                   20.00 |

#### Execution phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-16-1-1 |                      0.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   13.00 |
| PostgreSQL-BHT-16-1-2 |                      0.00 |                                     0.00 |                                             0.00 |                        0.00 |                                    0.00 |
| PostgreSQL-BHT-16-2-1 |                      0.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    2.00 |
| PostgreSQL-BHT-16-2-2 |                      1.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
