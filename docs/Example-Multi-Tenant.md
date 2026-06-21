# Example: Multi-Tenant

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In a multi-tenant architecture, it is assumed that each tenant maintains an isolated dataset and interacts exclusively with this dataset.
Several strategies exist to achieve this separation, including the schema-per-tenant, database-per-tenant, and container-per-tenant approaches.
In the following sections, we present an evaluation of these strategies using bexhoma to compare their performance characteristics, c.f. [1].


[1] [Benchmarking Multi-Tenant Architectures in PostgreSQL](https://doi.org/10.48786/edbt.2026.46)
> Erdelt, P.K., and Rabl T. (2026)
> In: Proceedings 29th International Conference on Extending Database Technology, EDBT 2026
> OpenProceedings.org
> https://doi.org/10.48786/edbt.2026.46

## Background

To make this work, there has to be some preparation.
* In the experiment folders, there are init scripts containing placeholders for the database `{BEXHOMA_DATABASE}` or schema `{BEXHOMA_SCHEMA}`
* The DBMS must have placeholders in the connection parameters - c.f. [DBMS](DBMS.html#postgresql)

Bexhoma contains these preparations for PostgreSQL and MySQL (without the schema-per-tenant option).

## Preparation

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

We set the number of tenants to 2 in the following:
```
BEXHOMA_NUM_TENANTS=2
```

## PostgreSQL

### TPC-H

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-TPC-H-Merger-collector.ipynb).

#### Schema-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-schema-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated schema in the same database:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 10Gi \
  -rst shared \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log
```

test_tpch_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2323s 
* Code: 1773417900
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-2-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219911
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219911
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219912
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219912
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773417900
    * TENANT_BY:schema
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-2-1-1 |   PostgreSQL-BHT-2-1-2 |   PostgreSQL-BHT-2-2-1 |   PostgreSQL-BHT-2-2-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4385.21 |                4358.91 |                4292    |                4402.21 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2384.74 |                2435.03 |                2399.04 |                2256.59 |
| Shipping Priority (TPC-H Q3)                        |                1706.04 |                1770.89 |                1552.63 |                1617.22 |
| Order Priority Checking Query (TPC-H Q4)            |                 712.26 |                 741.89 |                 651.87 |                 674.54 |
| Local Supplier Volume (TPC-H Q5)                    |                2037.55 |                2092.93 |                2005.79 |                1948.2  |
| Forecasting Revenue Change (TPC-H Q6)               |                 792.67 |                 811.99 |                 796.42 |                 804.34 |
| Forecasting Revenue Change (TPC-H Q7)               |                1582.98 |                1612.24 |                1622.64 |                1572.54 |
| National Market Share (TPC-H Q8)                    |                1240.38 |                1237.13 |                1082.55 |                1055.22 |
| Product Type Profit Measure (TPC-H Q9)              |                5167.72 |                5062.05 |                5022.42 |                4965.28 |
| Forecasting Revenue Change (TPC-H Q10)              |                1953.49 |                1957.16 |                1970.79 |                1978.2  |
| Important Stock Identification (TPC-H Q11)          |                 755.85 |                 703.98 |                 767.22 |                 657.7  |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1310.16 |                1291.97 |                1313.09 |                1300.4  |
| Customer Distribution (TPC-H Q13)                   |                6390.39 |                6349.93 |                6569.17 |                6055.44 |
| Forecasting Revenue Change (TPC-H Q14)              |                1267.28 |                1284.83 |                1285.81 |                1273.3  |
| Top Supplier Query (TPC-H Q15)                      |                1237.12 |                1249.33 |                1254.96 |                1248.14 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1049.23 |                1082.12 |                1049.03 |                1065.2  |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                5962.21 |                5354.48 |                6014.36 |                5149.33 |
| Large Volume Customer (TPC-H Q18)                   |               23576    |               23118.3  |               23207.3  |               23060.7  |
| Discounted Revenue (TPC-H Q19)                      |                 279.78 |                 262.96 |                 288.76 |                 285.59 |
| Potential Part Promotion (TPC-H Q20)                |                3671.26 |                3140.37 |                3601.23 |                2999.34 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                1691.9  |                1733.31 |                1695.88 |                1756.25 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 400.2  |                 383.98 |                 402    |                 356.14 |

### Loading [s]

| DBMS                 |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-2-1-1 |              0 |            1149 |            8 |        1740 |       2899 |
| PostgreSQL-BHT-2-1-2 |              0 |            1149 |            8 |        1740 |       2899 |
| PostgreSQL-BHT-2-2-1 |              0 |            1149 |            8 |        1740 |       2899 |
| PostgreSQL-BHT-2-2-2 |              0 |            1149 |            8 |        1740 |       2899 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-2-1-1 |            1.8  |
| PostgreSQL-BHT-2-1-2 |            1.78 |
| PostgreSQL-BHT-2-2-1 |            1.78 |
| PostgreSQL-BHT-2-2-2 |            1.72 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-2-1-1 |             19997.9 |
| PostgreSQL-BHT-2-1-2 |             20234.5 |
| PostgreSQL-BHT-2-2-1 |             20230.9 |
| PostgreSQL-BHT-2-2-2 |             20915   |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS               |   time [s] |   count |   SF |   Throughput@Size |
|:-------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-2-1 |         71 |       2 |   10 |           22309.9 |
| PostgreSQL-BHT-2-2 |         71 |       2 |   10 |           22309.9 |

### Workflow

| DBMS                 | orig_name          |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:---------------------|:-------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-2-1-1 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773419888 |      1773419959 |
| PostgreSQL-BHT-2-1-2 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773419888 |      1773419957 |
| PostgreSQL-BHT-2-2-1 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773420072 |      1773420143 |
| PostgreSQL-BHT-2-2-2 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773420072 |      1773420140 |

#### Actual

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |      1050.92 |      2.22 |          34.47 |                 63.65 |
| PostgreSQL-BHT-2-2 |      1050.92 |      2.22 |          34.47 |                 63.65 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-2-2 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       154.87 |      0.63 |           0.02 |                  6.06 |
| PostgreSQL-BHT-2-2 |       154.87 |      0.63 |           0.02 |                  6.06 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       212.47 |      2.83 |          36.36 |                 68.19 |
| PostgreSQL-BHT-2-2 |       643.04 |      9.62 |          36.26 |                 55.45 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |        18.56 |         0 |           0.26 |                  0.26 |
| PostgreSQL-BHT-2-2 |        18.48 |         0 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         1 |                                        0 |                                                0 |                          17 |                                      16 |
| PostgreSQL-BHT-2-2 |                         1 |                                        0 |                                                0 |                          17 |                                      16 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         0 |                                        0 |                                                0 |                          10 |                                      10 |
| PostgreSQL-BHT-2-2 |                         0 |                                        0 |                                                0 |                          10 |                                      10 |

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
```


#### Database-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-database-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated database in the same DBMS:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 10Gi \
  -rst shared \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log
```

test_tpch_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2247s 
* Code: 1773420332
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-2-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-1-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-BHT-2-2-2 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1219916
  * volume_size:100G
  * volume_used:62G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773420332
    * TENANT_BY:database
    * TENANT_NUM:2

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-2-1-1 |   PostgreSQL-BHT-2-1-2 |   PostgreSQL-BHT-2-2-1 |   PostgreSQL-BHT-2-2-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                4302.73 |                4423.71 |                4310.42 |                4330.76 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2411.65 |                2568.16 |                2344.17 |                2305.32 |
| Shipping Priority (TPC-H Q3)                        |                1668.14 |                1746.71 |                1690.89 |                1570.95 |
| Order Priority Checking Query (TPC-H Q4)            |                 690.19 |                 725.85 |                 707.13 |                 723.72 |
| Local Supplier Volume (TPC-H Q5)                    |                2101.34 |                2043.12 |                2133.01 |                1921.17 |
| Forecasting Revenue Change (TPC-H Q6)               |                 808.49 |                 803.88 |                 807.31 |                 810.93 |
| Forecasting Revenue Change (TPC-H Q7)               |                1587.88 |                1491.45 |                1627.57 |                1626.8  |
| National Market Share (TPC-H Q8)                    |                1251.62 |                1449.04 |                1051.61 |                1237.99 |
| Product Type Profit Measure (TPC-H Q9)              |                4922.11 |                4797.09 |                4941.19 |                4123.63 |
| Forecasting Revenue Change (TPC-H Q10)              |                1859.05 |                1809.69 |                1799.9  |                1901.11 |
| Important Stock Identification (TPC-H Q11)          |                 722.19 |                 719.29 |                 828.14 |                 748.13 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1271.27 |                1281.98 |                1331.26 |                1269.39 |
| Customer Distribution (TPC-H Q13)                   |                7131.42 |                7144.42 |                7262.17 |                7452.36 |
| Forecasting Revenue Change (TPC-H Q14)              |                1248.74 |                1291    |                1221.36 |                1242.35 |
| Top Supplier Query (TPC-H Q15)                      |                1232.45 |                1256.58 |                1253.13 |                1225.53 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1073.43 |                1056.51 |                1063.97 |                1047.72 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                5300.47 |                6059.31 |                5906.99 |                6448.57 |
| Large Volume Customer (TPC-H Q18)                   |               23413.7  |               23714.2  |               23362    |               23633.4  |
| Discounted Revenue (TPC-H Q19)                      |                 289.78 |                 284.89 |                 280.05 |                 292.44 |
| Potential Part Promotion (TPC-H Q20)                |                3195.99 |                3690.39 |                3471.32 |                3522.49 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                1821.16 |                1751.45 |                1806.89 |                1764.4  |
| Global Sales Opportunity Query (TPC-H Q22)          |                 397.39 |                 379.86 |                 387.68 |                 376.18 |

### Loading [s]

| DBMS                 |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-2-1-1 |              2 |            1036 |            8 |        1618 |       2665 |
| PostgreSQL-BHT-2-1-2 |              2 |            1036 |            8 |        1618 |       2665 |
| PostgreSQL-BHT-2-2-1 |              2 |            1036 |            8 |        1618 |       2665 |
| PostgreSQL-BHT-2-2-2 |              2 |            1036 |            8 |        1618 |       2665 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-2-1-1 |            1.78 |
| PostgreSQL-BHT-2-1-2 |            1.82 |
| PostgreSQL-BHT-2-2-1 |            1.79 |
| PostgreSQL-BHT-2-2-2 |            1.78 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-2-1-1 |             20199.2 |
| PostgreSQL-BHT-2-1-2 |             19820.4 |
| PostgreSQL-BHT-2-2-1 |             20056.9 |
| PostgreSQL-BHT-2-2-2 |             20209.4 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS               |   time [s] |   count |   SF |   Throughput@Size |
|:-------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-2-1 |         72 |       2 |   10 |           22000   |
| PostgreSQL-BHT-2-2 |         71 |       2 |   10 |           22309.9 |

### Workflow

| DBMS                 | orig_name          |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:---------------------|:-------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-2-1-1 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773422209 |      1773422278 |
| PostgreSQL-BHT-2-1-2 | PostgreSQL-BHT-2-1 |   10 |      2 |                1 |            1 |        1773422208 |      1773422280 |
| PostgreSQL-BHT-2-2-1 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773422388 |      1773422459 |
| PostgreSQL-BHT-2-2-2 | PostgreSQL-BHT-2-2 |   10 |      2 |                1 |            2 |        1773422388 |      1773422459 |

#### Actual

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       980.19 |      2.15 |          32.82 |                 65.74 |
| PostgreSQL-BHT-2-2 |       980.19 |      2.15 |          32.82 |                 65.74 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-2-2 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       146.68 |      1.11 |           0.01 |                  0.01 |
| PostgreSQL-BHT-2-2 |       146.68 |      1.11 |           0.01 |                  0.01 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |       266.23 |      5.21 |          35.53 |                 67.37 |
| PostgreSQL-BHT-2-2 |       316.43 |      4.48 |          35.5  |                 54.66 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-2-1 |        18.51 |         0 |           0.25 |                  0.25 |
| PostgreSQL-BHT-2-2 |        19.31 |         0 |           0.3  |                  0.3  |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         2 |                                        0 |                                                0 |                          35 |                                      33 |
| PostgreSQL-BHT-2-2 |                         2 |                                        0 |                                                0 |                          35 |                                      33 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-2-1 |                         2 |                                        0 |                                                0 |                          19 |                                      17 |
| PostgreSQL-BHT-2-2 |                         1 |                                        0 |                                                0 |                          16 |                                      16 |

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
```


#### Container-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-0-2-tpch-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated DBMS:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne 1,1 \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 5Gi \
  -rst shared \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log
```

test_tpch_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 1927s 
* Code: 1773422696
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-1-0-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1250374
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-0-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1281298
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-BHT-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1281291
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-BHT-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1283094
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-223
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1773422696
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS                                                |   PostgreSQL-BHT-1-0-1-1 |   PostgreSQL-BHT-1-0-2-1 |   PostgreSQL-BHT-1-1-1-1 |   PostgreSQL-BHT-1-1-2-1 |
|:----------------------------------------------------|-------------------------:|-------------------------:|-------------------------:|-------------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                  4319.15 |                  4334.56 |                  4336.92 |                  4317.89 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  2443.83 |                  2240    |                  2343.76 |                  2450.72 |
| Shipping Priority (TPC-H Q3)                        |                  1770.97 |                  1634.24 |                  1665.31 |                  1572.43 |
| Order Priority Checking Query (TPC-H Q4)            |                   682.59 |                   660.74 |                   666.87 |                   662.64 |
| Local Supplier Volume (TPC-H Q5)                    |                  1906.8  |                  1921.27 |                  1703.39 |                  1830.61 |
| Forecasting Revenue Change (TPC-H Q6)               |                   742.17 |                   762.12 |                   774.05 |                   765.41 |
| Forecasting Revenue Change (TPC-H Q7)               |                  1495.61 |                  1584.6  |                  1403.14 |                  1584.48 |
| National Market Share (TPC-H Q8)                    |                  1092.45 |                   972.26 |                   988.96 |                  1004.64 |
| Product Type Profit Measure (TPC-H Q9)              |                  4721.04 |                  4784.87 |                  4373.12 |                  4706.72 |
| Forecasting Revenue Change (TPC-H Q10)              |                  1870.05 |                  1891.53 |                  1890.42 |                  1944.94 |
| Important Stock Identification (TPC-H Q11)          |                   775.5  |                   810.17 |                   774.9  |                   733.06 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  1251.32 |                  1274.85 |                  1278.4  |                  1274.82 |
| Customer Distribution (TPC-H Q13)                   |                  6772.36 |                  6428.69 |                  7509.21 |                  6219.9  |
| Forecasting Revenue Change (TPC-H Q14)              |                  1288.87 |                  1272.1  |                  1265.36 |                  1259.48 |
| Top Supplier Query (TPC-H Q15)                      |                  1251.21 |                  1237.44 |                  1242.15 |                  1233.37 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  1043.6  |                  1051.78 |                   999.73 |                   991.78 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  5346.52 |                  5489.68 |                  5499.57 |                  5234    |
| Large Volume Customer (TPC-H Q18)                   |                 22324.9  |                 25265.3  |                 23234.3  |                 23498.1  |
| Discounted Revenue (TPC-H Q19)                      |                   274.93 |                   257.66 |                   240.55 |                   256.97 |
| Potential Part Promotion (TPC-H Q20)                |                  3020.92 |                  3450.41 |                  3069.94 |                  3059.26 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  1758.17 |                  1761.09 |                  1745.94 |                  1744.17 |
| Global Sales Opportunity Query (TPC-H Q22)          |                   374    |                   358.77 |                   368.3  |                   364.12 |

### Loading [s]

| DBMS                   |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:-----------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-1-0-1-1 |              0 |             701 |            4 |         987 |       1709 |
| PostgreSQL-BHT-1-0-2-1 |              0 |             701 |            4 |         987 |       1709 |
| PostgreSQL-BHT-1-1-1-1 |              0 |             700 |            4 |         975 |       1681 |
| PostgreSQL-BHT-1-1-2-1 |              0 |             700 |            4 |         975 |       1681 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                   |   Geo Times [s] |
|:-----------------------|----------------:|
| PostgreSQL-BHT-1-0-1-1 |            1.74 |
| PostgreSQL-BHT-1-0-2-1 |            1.73 |
| PostgreSQL-BHT-1-1-1-1 |            1.7  |
| PostgreSQL-BHT-1-1-2-1 |            1.7  |

### Power@Size ((3600*SF)/(geo times))

| DBMS                   |   Power@Size [~Q/h] |
|:-----------------------|--------------------:|
| PostgreSQL-BHT-1-0-1-1 |             20729.6 |
| PostgreSQL-BHT-1-0-2-1 |             20752.2 |
| PostgreSQL-BHT-1-1-1-1 |             21147.1 |
| PostgreSQL-BHT-1-1-2-1 |             21125.9 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS                 |   time [s] |   count |   SF |   Throughput@Size |
|:---------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-1-0-1 |         68 |       1 |   10 |           11647.1 |
| PostgreSQL-BHT-1-0-2 |         70 |       1 |   10 |           11314.3 |
| PostgreSQL-BHT-1-1-1 |         68 |       1 |   10 |           11647.1 |
| PostgreSQL-BHT-1-1-2 |         68 |       1 |   10 |           11647.1 |

### Workflow

| DBMS                   | orig_name            |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:-----------------------|:---------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-1-0-1-1 | PostgreSQL-BHT-1-0-1 |   10 |      1 |                1 |            1 |        1773424159 |      1773424227 |
| PostgreSQL-BHT-1-0-2-1 | PostgreSQL-BHT-1-0-2 |   10 |      1 |                1 |            2 |        1773424433 |      1773424503 |
| PostgreSQL-BHT-1-1-1-1 | PostgreSQL-BHT-1-1-1 |   10 |      1 |                1 |            1 |        1773424159 |      1773424227 |
| PostgreSQL-BHT-1-1-2-1 | PostgreSQL-BHT-1-1-2 |   10 |      1 |                1 |            2 |        1773424432 |      1773424500 |

#### Actual

* DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
* DBMS PostgreSQL-BHT-1 - Pods [[1, 1]]

#### Planned

* DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
* DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |       328.4  |       1.4 |          19.26 |                 35.32 |
| PostgreSQL-BHT-1-0-2 |       328.4  |       1.4 |          19.26 |                 35.32 |
| PostgreSQL-BHT-1-1-1 |       380.89 |       1.4 |          18.66 |                 34.55 |
| PostgreSQL-BHT-1-1-2 |       380.89 |       1.4 |          18.66 |                 34.55 |

### Loading phase: component data generator

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-1-0-2 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-1-1-1 |            0 |         0 |              0 |                     0 |
| PostgreSQL-BHT-1-1-2 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |        74.72 |      0.63 |           0.01 |                  0.01 |
| PostgreSQL-BHT-1-0-2 |        74.72 |      0.63 |           0.01 |                  0.01 |
| PostgreSQL-BHT-1-1-1 |        75.52 |      0.59 |           0.01 |                  0.01 |
| PostgreSQL-BHT-1-1-2 |        75.52 |      0.59 |           0.01 |                  0.01 |

### Execution phase: SUT deployment

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |       269.52 |      4.9  |          57.15 |                 73.09 |
| PostgreSQL-BHT-1-0-2 |       138.32 |      2.23 |          20.65 |                 36.58 |
| PostgreSQL-BHT-1-1-1 |       314.19 |      4.9  |          23.9  |                 39.83 |
| PostgreSQL-BHT-1-1-2 |       133.51 |      2.16 |          20.72 |                 36.65 |

### Execution phase: component benchmarker

| DBMS                 |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-1-0-1 |         9.43 |      0.14 |           0.26 |                  0.27 |
| PostgreSQL-BHT-1-0-2 |         9.31 |      0.16 |           0.26 |                  0.27 |
| PostgreSQL-BHT-1-1-1 |         9.34 |      0.16 |           0.26 |                  0.26 |
| PostgreSQL-BHT-1-1-2 |         9.22 |      0.16 |           0.26 |                  0.26 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:---------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-1-0-1 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-0-2 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-1-1 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-1-2 |                         1 |                                        0 |                                                0 |                           8 |                                       8 |

#### Execution phase: SUT deployment

| DBMS                 |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:---------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-1-0-1 |                         1 |                                        0 |                                                0 |                           6 |                                       7 |
| PostgreSQL-BHT-1-0-2 |                         1 |                                        0 |                                                0 |                           5 |                                       5 |
| PostgreSQL-BHT-1-1-1 |                         0 |                                        0 |                                                0 |                           8 |                                       8 |
| PostgreSQL-BHT-1-1-2 |                         0 |                                        0 |                                                0 |                           7 |                                       7 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST failed: Workflow not as planned
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
```




#### Database-Per-Tenant - Multiple Loaders

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-database-2-tpch-1
```

We set 8 loaders per tenant (2 tenants):
```bash
BEXHOMA_NUM_TENANTS_LOADER = 16
```

Example for power test with 2 tenants, each having a dedicated database in the same DBMS:
```bash
bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 \
  --dbms PostgreSQL \
  -xii -xic -xis \
  -nlp $BEXHOMA_NUM_TENANTS_LOADER -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_database_multiload.log
```

test_tpch_run_postgresql_tenants_database_multiload.log
```markdown
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
```


### TPC-C

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-Benchbase-Merger-collector.ipynb).


#### Schema-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated schema in the same database.
The execution phase is run twice.
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 20Gi \
  -rst shared \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log
```

test_benchbase_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1601s 
* Code: 1773424732
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147853
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773424732
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147853
  * volume_size:20G
  * volume_used:636M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773424732
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-2 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.496667 |                    0.5      |     104.977  |                                                        354187 |                                                136321 |
| PostgreSQL-1-1-1024-1-1 |                1 |          10 |     1024 |        1 |       2 |    300 |            0 |                       0.486667 |                    0.486667 |     102.177  |                                                        345173 |                                                122913 |
| PostgreSQL-1-1-1024-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.503333 |                    0.5      |     104.977  |                                                        132821 |                                                 61155 |
| PostgreSQL-1-1-1024-2-2 |                1 |          10 |     1024 |        2 |       2 |    300 |            0 |                       0.46     |                    0.46     |      96.5785 |                                                        136129 |                                                 62643 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.98 |                        0.99 |            0 |                                                        354187 |                                                129617 |
| PostgreSQL-1-1-1024-2 |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.96 |                        0.96 |            0 |                                                        136129 |                                                 61899 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |         365 |           1 |      2 |             9.86301 |
| PostgreSQL-1-1-1024-2 |         365 |           1 |      2 |             9.86301 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |       139.82 |      0.75 |           5.95 |                  6.21 |
| PostgreSQL-1-1-1024-2 |       139.82 |      0.75 |           5.95 |                  6.21 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |        18.37 |      0.06 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2 |        18.37 |      0.06 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |         6.28 |      0.24 |           6.04 |                  6.29 |
| PostgreSQL-1-1-1024-2 |         6.02 |      0.02 |           6.04 |                  6.29 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |        45.02 |      0.43 |           0.23 |                  0.23 |
| PostgreSQL-1-1-1024-2 |        43.13 |      0.43 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1 |                         1 |                                        0 |                                                0 |                           3 |                                       2 |
| PostgreSQL-1-1-1024-2 |                         1 |                                        0 |                                                0 |                           3 |                                       2 |

#### Execution phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1 |                        21 |                                        0 |                                                0 |                           3 |                                       2 |
| PostgreSQL-1-1-1024-2 |                        21 |                                        0 |                                                0 |                           2 |                                       1 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```


#### Database-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated database in the same DBMS.
The execution phase is run twice.
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 20Gi \
  -rst shared \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log
```

test_benchbase_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1654s 
* Code: 1773426376
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147853
  * volume_size:20G
  * volume_used:648M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773426376
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147853
  * volume_size:20G
  * volume_used:648M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773426376
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1-2 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.449999 |                    0.453332 |      95.1785 |                                                        319897 |                                                132717 |
| PostgreSQL-1-1-1024-1-1 |                1 |          10 |     1024 |        1 |       2 |    300 |            0 |                       0.493333 |                    0.493333 |     103.577  |                                                        359779 |                                                156795 |
| PostgreSQL-1-1-1024-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.513333 |                    0.513333 |     107.776  |                                                         43950 |                                                 17722 |
| PostgreSQL-1-1-1024-2-2 |                1 |          10 |     1024 |        2 |       2 |    300 |            0 |                       0.46     |                    0.463333 |      97.2784 |                                                         75963 |                                                 21255 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-1 |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.94 |                        0.95 |            0 |                                                        359779 |                                              144756   |
| PostgreSQL-1-1-1024-2 |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.97 |                        0.98 |            0 |                                                         75963 |                                               19488.5 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned

* DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-1 |         407 |           1 |      2 |             8.84521 |
| PostgreSQL-1-1-1024-2 |         407 |           1 |      2 |             8.84521 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |       142.14 |      0.63 |           5.98 |                  6.23 |
| PostgreSQL-1-1-1024-2 |       142.14 |      0.63 |           5.98 |                  6.23 |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |         17.9 |      0.08 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-2 |         17.9 |      0.08 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |         9.75 |      0.29 |           6.07 |                  6.33 |
| PostgreSQL-1-1-1024-2 |         9.31 |      0.04 |           6.07 |                  6.33 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-1 |        23.16 |      0.15 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-2 |        22.22 |      0.3  |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1 |                         2 |                                        0 |                                                0 |                           8 |                                       6 |
| PostgreSQL-1-1-1024-2 |                         2 |                                        0 |                                                0 |                           8 |                                       6 |

#### Execution phase: SUT deployment

| DBMS                  |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:----------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-1 |                        21 |                                        1 |                                                0 |                           2 |                                       1 |
| PostgreSQL-1-1-1024-2 |                        23 |                                        0 |                                                0 |                           3 |                                       0 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```


#### Container-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-0-2-benchbase-tpcc-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated DBMS.
The execution phase is run twice.
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -ne 1,1 \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 10Gi \
  -rst shared \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log
```

test_benchbase_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1694s 
* Code: 1773428073
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1024-0-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-0-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:147854
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773428073
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Execution

#### Per Pod

| DBMS                      |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1024-0-1-1 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.5      |                    0.496666 |     104.277  |                                                        121050 |                                                 40628 |
| PostgreSQL-1-1-1024-1-1-1 |                1 |          10 |     1024 |        1 |       1 |    300 |            0 |                       0.503332 |                    0.503332 |     105.676  |                                                         57129 |                                                 21444 |
| PostgreSQL-1-1-1024-0-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.526667 |                    0.53     |     111.275  |                                                        177050 |                                                 50583 |
| PostgreSQL-1-1-1024-1-2-1 |                1 |          10 |     1024 |        2 |       1 |    300 |            0 |                       0.446667 |                    0.446667 |      93.7791 |                                                         37374 |                                                 15766 |

#### Aggregated Parallel

| DBMS   |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| 1-1    |                1 |          20 |     2048 |           2 |    300 |            0 |                           1    |                        1    |            0 |                                                        121050 |                                               31036   |
| 1-2    |                1 |          20 |     2048 |           2 |    300 |            0 |                           0.97 |                        0.98 |            0 |                                                        177050 |                                               33174.5 |

### Workflow

#### Actual

* DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned

* DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
* DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading

| DBMS                    |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:------------------------|------------:|------------:|-------:|--------------------:|
| PostgreSQL-1-1-1024-0-1 |         271 |           1 |      1 |             13.2841 |
| PostgreSQL-1-1-1024-0-2 |         271 |           1 |      1 |             13.2841 |
| PostgreSQL-1-1-1024-1-1 |         224 |           1 |      1 |             16.0714 |
| PostgreSQL-1-1-1024-1-2 |         224 |           1 |      1 |             16.0714 |

### Monitoring

### Loading phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |        70.34 |      0.42 |           5.84 |                  5.98 |
| PostgreSQL-1-1-1024-0-2 |        70.34 |      0.42 |           5.84 |                  5.98 |
| PostgreSQL-1-1-1024-1-1 |        70.83 |      0.41 |           5.85 |                  5.99 |
| PostgreSQL-1-1-1024-1-2 |        70.83 |      0.41 |           5.85 |                  5.99 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |         9.01 |      0.06 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-0-2 |         9.01 |      0.06 |           0.25 |                  0.25 |
| PostgreSQL-1-1-1024-1-1 |         8.28 |      0.05 |           0.24 |                  0.24 |
| PostgreSQL-1-1-1024-1-2 |         8.28 |      0.05 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |         4.47 |      0.02 |           5.89 |                  6.03 |
| PostgreSQL-1-1-1024-0-2 |         3.81 |      0.02 |           5.89 |                  6.03 |
| PostgreSQL-1-1-1024-1-1 |         4.84 |      0.02 |           5.89 |                  6.03 |
| PostgreSQL-1-1-1024-1-2 |         3.88 |      0.02 |           5.89 |                  6.03 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1024-0-1 |        22.69 |      0.23 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-0-2 |        22.99 |      0.07 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-1-1 |        28.53 |      0.33 |           0.11 |                  0.11 |
| PostgreSQL-1-1-1024-1-2 |        28.53 |      0.07 |           0.11 |                  0.11 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                    |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-0-1 |                         1 |                                        0 |                                                0 |                           1 |                                       1 |
| PostgreSQL-1-1-1024-0-2 |                         1 |                                        0 |                                                0 |                           1 |                                       1 |
| PostgreSQL-1-1-1024-1-1 |                         2 |                                        0 |                                                0 |                           2 |                                       1 |
| PostgreSQL-1-1-1024-1-2 |                         2 |                                        0 |                                                0 |                           2 |                                       1 |

#### Execution phase: SUT deployment

| DBMS                    |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:------------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1024-0-1 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |
| PostgreSQL-1-1-1024-0-2 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |
| PostgreSQL-1-1-1024-1-1 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |
| PostgreSQL-1-1-1024-1-2 |                        11 |                                        0 |                                                0 |                           1 |                                       0 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```










## MySQL


### TPC-C

An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/MT-Benchbase-Merger-collector.ipynb).



#### Database-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-mysql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated database in the same DBMS.
The execution phase is run twice.
```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 1 \
  -xsd 5 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst shared \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_database.log
```

test_benchbase_run_mysql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 2706s 
    Code: 1772811599
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.1.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147807
    volume_size:50G
    volume_used:33G
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772811599
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147807
    volume_size:50G
    volume_used:33G
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772811599
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.466667                   0.463333   97.278365                                                     109631.0                                              64847.0
MySQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.470000                   0.470000   98.678068                                                     134946.0                                              56621.0
MySQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.486666                   0.483333  101.477395                                                      39949.0                                              25434.0
MySQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.533333                   0.536666  112.674923                                                     133835.0                                              28955.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.94                       0.93         0.0                                                     134946.0                                              60734.0
MySQL-1-1-1024-2               1         20    2048          2  300.0           0                          1.02                       1.02         0.0                                                     133835.0                                              27194.5

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1     1012.0        1.0   2.0           3.557312
MySQL-1-1-1024-2     1012.0        1.0   2.0           3.557312

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```



#### Container-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-mysql-0-2-benchbase-tpcc-1
kubectl delete pvc bexhoma-storage-mysql-1-2-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated DBMS.
The execution phase is run twice.
```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 1 \
  -xsd 5 \
  -ne 1,1 \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst shared \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_container.log
```

test_benchbase_run_mysql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 2637s 
    Code: 1772814313
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.1.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
MySQL-1-1-1024-0-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147808
    volume_size:50G
    volume_used:33G
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772814313
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-0-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147808
    volume_size:50G
    volume_used:33G
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772814313
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147808
    volume_size:50G
    volume_used:33G
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772814313
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
                TENANT_VOL:False
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147808
    volume_size:50G
    volume_used:33G
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772814313
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
                TENANT_VOL:False

### Execution

#### Per Pod
                      experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                  
MySQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.476667                   0.476667  100.077747                                                     121815.0                                              65837.0
MySQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.463333                   0.466667   97.978200                                                     132437.0                                              50410.0
MySQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.460000                   0.463333   97.278369                                                     133157.0                                              36609.0
MySQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.480000                   0.483333  101.477442                                                      49862.0                                              21001.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.94                       0.94         0.0                                                     132437.0                                              58123.5
1-2               1         20    2048          2  300.0           0                          0.94                       0.95         0.0                                                     133157.0                                              28805.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-0-1      874.0        1.0   1.0           4.118993
MySQL-1-1-1024-0-2      874.0        1.0   1.0           4.118993
MySQL-1-1-1024-1-1      799.0        1.0   1.0           4.505632
MySQL-1-1-1024-1-2      799.0        1.0   1.0           4.505632

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```







