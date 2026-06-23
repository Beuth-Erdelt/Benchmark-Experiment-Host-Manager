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
BEXHOMA_STORAGE_CLASS="shared"

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log
```

test_tpch_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 565s 
* Code: 1781980444
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225912
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225912
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:233273
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:233273
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781980444
    * TENANT_BY:schema
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781980444-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    1 |       78.00 |           2.00 |            0.00 |         78.00 |          135.00 |              2 |           0 |               46.15 |
| 1781980444-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    1 |       78.00 |           2.00 |            0.00 |         78.00 |          135.00 |              2 |           0 |               46.15 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         14 |            0.33 |            10944.63 |           5657.14 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11496.78 |           6600.00 |           1 | PostgreSQL-1-1-1-1-2 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         12 |            0.33 |            10935.76 |           6600.00 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         15 |            0.36 |             9961.28 |           5280.00 |           1 | PostgreSQL-1-1-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         14 |            0.33 |            10944.63 |           5657.14 |           0 |
| PostgreSQL-1-1-1_1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11496.78 |           6600.00 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         12 |            0.33 |            10935.76 |           6600.00 |           0 |
| PostgreSQL-1-1-2_1 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         15 |            0.36 |             9961.28 |           5280.00 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1222.51 |                1216.25 |                1240.66 |                1237.54 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 247.93 |                 263.77 |                 302.23 |                 357.13 |
| Shipping Priority (TPC-H Q3)                        |                 327.87 |                 338.95 |                 343.23 |                 351.94 |
| Order Priority Checking Query (TPC-H Q4)            |                 140.96 |                 149.93 |                 155.94 |                 163.26 |
| Local Supplier Volume (TPC-H Q5)                    |                 285.46 |                 303.57 |                 343.52 |                 353.58 |
| Forecasting Revenue Change (TPC-H Q6)               |                 192.24 |                 194.15 |                 201.19 |                 203.80 |
| Volume Shipping Query (TPC-H Q7)                    |                 352.66 |                 365.31 |                 424.88 |                 433.53 |
| National Market Share (TPC-H Q8)                    |                 185.14 |                 192.07 |                 204.99 |                 190.92 |
| Product Type Profit Measure (TPC-H Q9)              |                 476.49 |                 796.90 |                 503.22 |                 891.38 |
| Returned Item Reporting Query (TPC-H Q10)           |                 289.12 |                 310.38 |                 313.74 |                 349.90 |
| Important Stock Identification (TPC-H Q11)          |                  89.17 |                  87.04 |                 145.25 |                 148.45 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 293.35 |                 295.85 |                 305.00 |                 309.63 |
| Customer Distribution (TPC-H Q13)                   |                1790.69 |                1014.64 |                1372.90 |                1665.32 |
| Promotion Effect Query (TPC-H Q14)                  |                 372.14 |                 218.00 |                 350.78 |                 224.38 |
| Top Supplier Query (TPC-H Q15)                      |                 266.63 |                 248.55 |                 249.83 |                 256.85 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 318.17 |                 303.08 |                 292.30 |                 322.85 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                1188.05 |                 818.27 |                 826.45 |                1256.95 |
| Large Volume Customer (TPC-H Q18)                   |                3810.28 |                3310.75 |                3196.21 |                3885.18 |
| Discounted Revenue (TPC-H Q19)                      |                  68.63 |                  72.48 |                  60.19 |                  67.59 |
| Potential Part Promotion (TPC-H Q20)                |                 186.38 |                 141.42 |                 134.64 |                 205.50 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 339.87 |                 341.59 |                 324.35 |                 380.01 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 118.18 |                 118.67 |                 117.35 |                 108.79 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
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
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log
```

test_tpch_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 560s 
* Code: 1781981028
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 2 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [2] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253317
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981028
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253317
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981028
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:256230
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981028
    * TENANT_BY:database
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:256230
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981028
    * TENANT_BY:database
    * TENANT_NUM:2

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781981028-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |       80.00 |           3.00 |            1.00 |         80.00 |          135.00 |              2 |           0 |               45.00 |
| 1781981028-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |       81.00 |           3.00 |            1.00 |         81.00 |          135.00 |              2 |           0 |               44.44 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         13 |            0.35 |            10425.69 |           6092.31 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         13 |            0.34 |            10646.88 |           6092.31 |           1 | PostgreSQL-1-1-1-1-2 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         14 |            0.33 |            10798.62 |           5657.14 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         12 |            0.32 |            11173.35 |           6600.00 |           1 | PostgreSQL-1-1-2-1-2 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         13 |            0.35 |            10425.69 |           6092.31 |           0 |
| PostgreSQL-1-1-1_1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         13 |            0.34 |            10646.88 |           6092.31 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         14 |            0.33 |            10798.62 |           5657.14 |           0 |
| PostgreSQL-1-1-2_1 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         12 |            0.32 |            11173.35 |           6600.00 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1204.80 |                1197.28 |                1220.48 |                1157.29 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 366.88 |                 322.07 |                 291.08 |                 287.97 |
| Shipping Priority (TPC-H Q3)                        |                 354.34 |                 354.73 |                 322.86 |                 338.40 |
| Order Priority Checking Query (TPC-H Q4)            |                 154.74 |                 156.83 |                 152.19 |                 158.71 |
| Local Supplier Volume (TPC-H Q5)                    |                 355.65 |                 358.72 |                 342.97 |                 352.58 |
| Forecasting Revenue Change (TPC-H Q6)               |                 197.90 |                 195.93 |                 197.52 |                 197.64 |
| Volume Shipping Query (TPC-H Q7)                    |                 423.13 |                 437.06 |                 423.64 |                 385.97 |
| National Market Share (TPC-H Q8)                    |                 232.73 |                 223.15 |                 195.43 |                 201.07 |
| Product Type Profit Measure (TPC-H Q9)              |                 575.76 |                 632.58 |                 605.93 |                 590.70 |
| Returned Item Reporting Query (TPC-H Q10)           |                 300.70 |                 302.41 |                 307.18 |                 304.21 |
| Important Stock Identification (TPC-H Q11)          |                 127.37 |                 132.35 |                 130.36 |                 150.32 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 318.87 |                 312.07 |                 302.74 |                 303.22 |
| Customer Distribution (TPC-H Q13)                   |                1626.58 |                1599.12 |                1688.55 |                1442.65 |
| Promotion Effect Query (TPC-H Q14)                  |                 230.40 |                 232.37 |                 226.05 |                 218.42 |
| Top Supplier Query (TPC-H Q15)                      |                 256.14 |                 243.07 |                 250.88 |                 243.84 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 305.31 |                 295.49 |                 297.01 |                 314.29 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 987.82 |                 948.07 |                 977.00 |                 784.28 |
| Large Volume Customer (TPC-H Q18)                   |                3319.69 |                3316.10 |                3344.06 |                3290.09 |
| Discounted Revenue (TPC-H Q19)                      |                  67.75 |                  63.53 |                  61.25 |                  59.14 |
| Potential Part Promotion (TPC-H Q20)                |                 207.29 |                 175.00 |                 170.28 |                 136.93 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 352.25 |                 339.91 |                 342.61 |                 328.41 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 123.30 |                 118.44 |                 133.83 |                 114.83 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
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
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log
```

test_tpch_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 609s 
* Code: 1781981608
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 5Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:218181
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:224797
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
* PostgreSQL-2-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220255
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
* PostgreSQL-2-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:227162
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781981608
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: tpch (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781981608-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |      165.00 |           1.00 |            0.00 |         55.00 |          105.00 |              1 |           0 |               21.82 |
| 1781981608-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |      160.00 |           1.00 |            0.00 |         55.00 |          102.00 |              1 |           0 |               22.50 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11478.56 |           6600.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2    | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11435.20 |           6600.00 |           1 | PostgreSQL-2-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.33 |            11053.82 |           6092.31 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2    | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.34 |            10566.27 |           6092.31 |           1 | PostgreSQL-2-1-2-1-1 |

#### Per Phase

|                    | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1_0 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11478.56 |           6600.00 |           0 |
| PostgreSQL-2-1-1_1 | PostgreSQL-2-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11435.20 |           6600.00 |           1 |
| PostgreSQL-1-1-2_0 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.33 |            11053.82 |           6092.31 |           0 |
| PostgreSQL-2-1-2_1 | PostgreSQL-2-1-2 |                1 |        2 |               1 |           1 | 1.00 |               22 |         13 |            0.34 |            10566.27 |           6092.31 |           1 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-2-1-1-1-1 |   PostgreSQL-2-1-2-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1237.16 |                1232.32 |                1220.50 |                1256.62 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 281.92 |                 306.93 |                 291.62 |                 315.82 |
| Shipping Priority (TPC-H Q3)                        |                 369.27 |                 352.49 |                 358.01 |                 341.07 |
| Order Priority Checking Query (TPC-H Q4)            |                 170.23 |                 156.25 |                 168.54 |                 159.56 |
| Local Supplier Volume (TPC-H Q5)                    |                 336.04 |                 420.53 |                 334.24 |                 334.17 |
| Forecasting Revenue Change (TPC-H Q6)               |                 189.17 |                 199.72 |                 207.66 |                 203.32 |
| Volume Shipping Query (TPC-H Q7)                    |                 396.78 |                 411.15 |                 392.32 |                 410.72 |
| National Market Share (TPC-H Q8)                    |                 221.03 |                 205.64 |                 215.12 |                 194.44 |
| Product Type Profit Measure (TPC-H Q9)              |                 547.66 |                 583.95 |                 538.76 |                 552.07 |
| Returned Item Reporting Query (TPC-H Q10)           |                 313.35 |                 331.30 |                 297.02 |                 301.29 |
| Important Stock Identification (TPC-H Q11)          |                 100.35 |                 143.83 |                 103.38 |                 167.74 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 315.05 |                 310.79 |                 316.32 |                 311.13 |
| Customer Distribution (TPC-H Q13)                   |                1215.78 |                1164.14 |                1213.26 |                1676.85 |
| Promotion Effect Query (TPC-H Q14)                  |                 231.80 |                 224.94 |                 234.79 |                 226.79 |
| Top Supplier Query (TPC-H Q15)                      |                 248.38 |                 241.43 |                 231.85 |                 249.88 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 296.34 |                 305.97 |                 291.90 |                 298.66 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 888.93 |                 793.31 |                 887.80 |                1197.81 |
| Large Volume Customer (TPC-H Q18)                   |                2768.09 |                3254.79 |                3187.04 |                3337.95 |
| Discounted Revenue (TPC-H Q19)                      |                  55.76 |                  60.40 |                  53.01 |                  59.85 |
| Potential Part Promotion (TPC-H Q20)                |                 133.06 |                 133.62 |                 132.74 |                 184.73 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 323.45 |                 332.95 |                 347.23 |                 361.07 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 102.67 |                 111.34 |                 103.31 |                 111.91 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
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
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp $BEXHOMA_NUM_TENANTS_LOADER \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 10Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 1246s 
* Code: 1781982237
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:260043
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781982237
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:242255
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781982237
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781982237-PostgreSQL-1-1-0 |                1 | schema         | False         |             2 |           0 |    1 |      116.00 |           4.00 |            0.00 |        116.00 |          152.00 |              2 |           1 |               31.03 |
| 1781982237-PostgreSQL-1-1-1 |                1 | schema         | False         |             2 |           1 |    1 |      124.00 |           4.00 |            0.00 |        124.00 |          152.00 |              2 |           1 |               29.03 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                      36150.00 |                                              17886.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.48 |                        0.49 |       102.18 |                                                      37472.00 |                                              18054.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.47 |        97.98 |                                                      63778.00 |                                              23085.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.44 |                        0.44 |        93.08 |                                                      40967.00 |                                              20410.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-0 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                      36150.00 |                                              17886.00 |
| PostgreSQL-1-1-1-1 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.48 |                        0.49 |       102.18 |                                                      37472.00 |                                              18054.00 |
| PostgreSQL-1-1-2-0 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.47 |        97.98 |                                                      63778.00 |                                              23085.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.44 |                        0.44 |        93.08 |                                                      40967.00 |                                              20410.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
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
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 1310s 
* Code: 1781983489
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214913
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781983489
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214800
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781983489
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781983489-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |      203.00 |           3.00 |            0.00 |        203.00 |          250.00 |              2 |           1 |               17.73 |
| 1781983489-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |      205.00 |           3.00 |            0.00 |        205.00 |          250.00 |              2 |           1 |               17.56 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.54 |                        0.54 |       114.07 |                                                      81992.00 |                                              26587.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.50 |                        0.49 |       103.58 |                                                      97149.00 |                                              30642.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.45 |        94.48 |                                                      50188.00 |                                              20838.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.28 |                                                      33101.00 |                                              18205.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-0 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.54 |                        0.54 |       114.07 |                                                      81992.00 |                                              26587.00 |
| PostgreSQL-1-1-1-1 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.50 |                        0.49 |       103.58 |                                                      97149.00 |                                              30642.00 |
| PostgreSQL-1-1-2-0 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.45 |        94.48 |                                                      50188.00 |                                              20838.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.28 |                                                      33101.00 |                                              18205.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
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
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Duration: 1312s 
* Code: 1781984804
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214714
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781984804
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214714
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781984804
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214714
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781984804
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214714
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781984804
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: benchbase (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781984804-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |      261.00 |           1.00 |            0.00 |        102.00 |          158.00 |              1 |           1 |               13.79 |
| 1781984804-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |      260.00 |           1.00 |            0.00 |        105.00 |          154.00 |              1 |           1 |               13.85 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.47 |                        0.48 |       100.08 |                                                      51575.00 |                                              22207.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.47 |        97.98 |                                                      82012.00 |                                              24191.00 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                      49885.00 |                                              26393.00 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                      49623.00 |                                              25898.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-0 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.47 |                        0.48 |       100.08 |                                                      51575.00 |                                              22207.00 |
| PostgreSQL-1-1-2-0 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.47 |        97.98 |                                                      82012.00 |                                              24191.00 |
| PostgreSQL-2-1-1-1 | PostgreSQL-2-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                      49885.00 |                                              26393.00 |
| PostgreSQL-2-1-2-1 | PostgreSQL-2-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                      49623.00 |                                              25898.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
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
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Type: benchbase
* Duration: 1689s 
* Code: 1781986123
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214906
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781986123
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214906
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781986123
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                        |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:-----------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781986123-MySQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |      305.00 |           3.00 |            0.00 |        305.00 |          340.00 |              2 |           1 |               11.80 |
| 1781986123-MySQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |      304.00 |           3.00 |            0.00 |        304.00 |          340.00 |              2 |           1 |               11.84 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                     143480.00 |                                              51822.00 |
| MySQL-1-1-1-1-2 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                     124306.00 |                                              50234.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.45 |                        0.45 |        94.48 |                                                     277352.00 |                                              85770.00 |
| MySQL-1-1-2-1-2 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                     188749.00 |                                              83242.00 |

#### Per Phase

| DBMS          | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-0 | MySQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                     143480.00 |                                              51822.00 |
| MySQL-1-1-1-1 | MySQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                     124306.00 |                                              50234.00 |
| MySQL-1-1-2-0 | MySQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.45 |                        0.45 |        94.48 |                                                     277352.00 |                                              85770.00 |
| MySQL-1-1-2-1 | MySQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                     188749.00 |                                              83242.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -rst $BEXHOMA_STORAGE_CLASS \
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
* Type: benchbase
* Duration: 2819s 
* Code: 1781987817
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217663
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781987817
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217663
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781987817
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* MySQL-2-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217663
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781987817
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
    * TENANT_VOL:False
* MySQL-2-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217663
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781987817
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT:1
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 2: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 2: benchbase (1 pods)

### Loading

#### Per Run

|                        |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:-----------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781987817-MySQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |      618.00 |           1.00 |            0.00 |        255.00 |          362.00 |              1 |           1 |                5.83 |
| 1781987817-MySQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |      681.00 |           1.00 |            0.00 |        323.00 |          357.00 |              1 |           1 |                5.29 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                           0.49 |                        0.49 |       103.58 |                                                     142682.00 |                                              63610.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                           0.50 |                        0.50 |       105.68 |                                                     123186.00 |                                              47704.00 |
| MySQL-2-1-1-1-1 | MySQL-2-1-1 | MySQL-2-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      85863.00 |                                              37100.00 |
| MySQL-2-1-2-1-1 | MySQL-2-1-2 | MySQL-2-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                           0.44 |                        0.44 |        93.08 |                                                     125709.00 |                                              65578.00 |

#### Per Phase

| DBMS           | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1--1 | MySQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |          -1 | 300.00 |            0 |                           0.49 |                        0.49 |       103.58 |                                                     142682.00 |                                              63610.00 |
| MySQL-1-1-2--1 | MySQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |          -1 | 300.00 |            0 |                           0.50 |                        0.50 |       105.68 |                                                     123186.00 |                                              47704.00 |
| MySQL-2-1-1--1 | MySQL-2-1-1 |                1 |          10 |     1024 |               1 |           1 |          -1 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      85863.00 |                                              37100.00 |
| MySQL-2-1-2--1 | MySQL-2-1-2 |                1 |          10 |     1024 |               1 |           1 |          -1 | 300.00 |            0 |                           0.44 |                        0.44 |        93.08 |                                                     125709.00 |                                              65578.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```







