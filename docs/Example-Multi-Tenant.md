# Example: Multi-Tenant

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In a multi-tenant architecture, it is assumed that each tenant maintains an isolated dataset and interacts exclusively with this dataset.
Several strategies exist to achieve this separation, including the schema-per-tenant, database-per-tenant, and container-per-tenant approaches.
In the following sections, we present an evaluation of these strategies using bexhoma to compare their performance characteristics.

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
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log &
```

test_tpch_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 623s 
    Code: 1771057520
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 2 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one schema per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771057520
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771057520
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771057520
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771057520
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2238.17               2229.69               2226.96               2236.10
Minimum Cost Supplier Query (TPC-H Q2)                             445.64                451.31                433.60                412.21
Shipping Priority (TPC-H Q3)                                       709.10                710.06                668.14                673.58
Order Priority Checking Query (TPC-H Q4)                           344.10                346.70                336.30                346.59
Local Supplier Volume (TPC-H Q5)                                   617.31                621.71                605.49                594.13
Forecasting Revenue Change (TPC-H Q6)                              454.45                454.70                459.65                455.12
Forecasting Revenue Change (TPC-H Q7)                              714.30                703.74                712.56                695.44
National Market Share (TPC-H Q8)                                   395.72                398.73                358.37                348.65
Product Type Profit Measure (TPC-H Q9)                             999.30               1749.13                994.65               1717.05
Forecasting Revenue Change (TPC-H Q10)                             584.97                582.75                585.98                587.00
Important Stock Identification (TPC-H Q11)                         159.21                160.32                159.25                147.88
Shipping Modes and Order Priority (TPC-H Q12)                      639.14                638.87                640.70                641.52
Customer Distribution (TPC-H Q13)                                 2003.71               2037.44               2029.01               2003.69
Forecasting Revenue Change (TPC-H Q14)                             487.95                495.59                486.22                486.69
Top Supplier Query (TPC-H Q15)                                     504.92                494.10                499.25                497.62
Parts/Supplier Relationship (TPC-H Q16)                            558.92                552.41                547.34                552.27
Small-Quantity-Order Revenue (TPC-H Q17)                          1931.26               1985.30               2031.66               1943.68
Large Volume Customer (TPC-H Q18)                                 6642.07               7221.21               6592.07               5684.46
Discounted Revenue (TPC-H Q19)                                     116.29                115.04                116.54                113.78
Potential Part Promotion (TPC-H Q20)                               248.72                269.35                264.71                231.11
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                733.02                738.96                735.77                739.45
Global Sales Opportunity Query (TPC-H Q22)                         227.00                213.67                211.44                214.32

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           0.0          121.0         3.0      232.0     358.0
PostgreSQL-BHT-2-1-2           0.0          121.0         3.0      232.0     358.0
PostgreSQL-BHT-2-2-1           0.0          121.0         3.0      232.0     358.0
PostgreSQL-BHT-2-2-2           0.0          121.0         3.0      232.0     358.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.61
PostgreSQL-BHT-2-1-2           0.63
PostgreSQL-BHT-2-2-1           0.61
PostgreSQL-BHT-2-2-2           0.61

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5893.01
PostgreSQL-BHT-2-1-2            5706.62
PostgreSQL-BHT-2-2-1            5948.87
PostgreSQL-BHT-2-2-2            5936.28

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 24      2  1.0          6600.00
PostgreSQL-BHT-2-2 1.0 1              2                 23      2  1.0          6886.96

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1771057958     1771057981
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1771057958     1771057982
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1771058061     1771058084
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1771058061     1771058084

#### Actual
DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### Database-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-database-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated database in the same DBMS:
```bash
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log &
```

test_tpch_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 595s 
    Code: 1771058230
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 2 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [2] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-2-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058230
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058230
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058230
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058230
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2321.53               2319.19               2314.00               2315.74
Minimum Cost Supplier Query (TPC-H Q2)                             465.31                434.95                448.34                440.17
Shipping Priority (TPC-H Q3)                                       702.32                704.74                669.32                669.53
Order Priority Checking Query (TPC-H Q4)                           343.77                343.74                339.93                337.49
Local Supplier Volume (TPC-H Q5)                                   639.77                603.93                626.71                618.46
Forecasting Revenue Change (TPC-H Q6)                              453.64                455.69                466.15                464.07
Forecasting Revenue Change (TPC-H Q7)                              731.14                703.73                729.41                725.64
National Market Share (TPC-H Q8)                                   409.48                390.48                381.86                378.11
Product Type Profit Measure (TPC-H Q9)                            1779.86               1007.51               1768.71               1021.34
Forecasting Revenue Change (TPC-H Q10)                             585.51                586.16                592.99                593.95
Important Stock Identification (TPC-H Q11)                         163.43                164.72                165.43                171.21
Shipping Modes and Order Priority (TPC-H Q12)                      632.17                640.52                638.60                638.97
Customer Distribution (TPC-H Q13)                                 1969.80               1992.26               1987.25               1963.51
Forecasting Revenue Change (TPC-H Q14)                             488.44                774.86                501.40                777.18
Top Supplier Query (TPC-H Q15)                                     497.22                502.45                508.63                514.51
Parts/Supplier Relationship (TPC-H Q16)                            535.36                545.07                532.42                547.69
Small-Quantity-Order Revenue (TPC-H Q17)                          1963.43               1876.14               2024.01               1986.85
Large Volume Customer (TPC-H Q18)                                 6908.45               6690.38               5548.01               5286.88
Discounted Revenue (TPC-H Q19)                                     580.64                125.13                121.22                119.37
Potential Part Promotion (TPC-H Q20)                               252.23                233.80                259.33                257.85
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                743.97                750.86                753.69                753.32
Global Sales Opportunity Query (TPC-H Q22)                         212.49                212.73                213.35                213.33

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           0.0          111.0         2.0      198.0     314.0
PostgreSQL-BHT-2-1-2           0.0          111.0         2.0      198.0     314.0
PostgreSQL-BHT-2-2-1           0.0          111.0         2.0      198.0     314.0
PostgreSQL-BHT-2-2-2           0.0          111.0         2.0      198.0     314.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.68
PostgreSQL-BHT-2-1-2           0.62
PostgreSQL-BHT-2-2-1           0.63
PostgreSQL-BHT-2-2-2           0.62

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5306.55
PostgreSQL-BHT-2-1-2            5792.47
PostgreSQL-BHT-2-2-1            5757.72
PostgreSQL-BHT-2-2-2            5808.26

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 25      2  1.0          6336.00
PostgreSQL-BHT-2-2 1.0 1              2                 23      2  1.0          6886.96

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1771058644     1771058669
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1771058644     1771058667
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1771058749     1771058772
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1771058749     1771058771

#### Actual
DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-BHT-2 - Pods [[2, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### Container-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-0-2-tpch-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-tpch-1
```

Example for power test with 2 tenants, each having a dedicated DBMS:
```bash
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 1 -nlt 1 -nbp 1  -nlt 64 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 5Gi -rsr \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log &
```

test_tpch_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 625s 
    Code: 1771058855
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 5Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-1-0-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058855
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-0-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058855
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058855
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-1-1-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771058855
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-2-1
Pricing Summary Report (TPC-H Q1)                                   2225.51                 2228.06                 2299.51                 2310.38
Minimum Cost Supplier Query (TPC-H Q2)                               436.61                  397.66                  463.11                  441.29
Shipping Priority (TPC-H Q3)                                         692.57                  659.73                  713.67                  660.76
Order Priority Checking Query (TPC-H Q4)                             326.93                  329.07                  340.44                  332.60
Local Supplier Volume (TPC-H Q5)                                     604.47                  578.24                  632.60                  600.96
Forecasting Revenue Change (TPC-H Q6)                                443.62                  450.88                  446.04                  454.63
Forecasting Revenue Change (TPC-H Q7)                                678.46                  699.59                  719.19                  710.16
National Market Share (TPC-H Q8)                                     394.22                  364.31                  401.73                  367.22
Product Type Profit Measure (TPC-H Q9)                               985.02                 1009.11                 1080.77                 1068.12
Forecasting Revenue Change (TPC-H Q10)                               579.51                  584.12                  601.81                  601.80
Important Stock Identification (TPC-H Q11)                           167.87                  158.20                  177.89                  177.03
Shipping Modes and Order Priority (TPC-H Q12)                        630.06                  642.64                  644.53                  649.15
Customer Distribution (TPC-H Q13)                                   2011.78                 1984.22                 2014.57                 2070.84
Forecasting Revenue Change (TPC-H Q14)                               481.82                  489.45                  487.04                  492.26
Top Supplier Query (TPC-H Q15)                                       493.04                  500.00                  519.75                  512.00
Parts/Supplier Relationship (TPC-H Q16)                              554.00                  563.12                  555.70                  558.60
Small-Quantity-Order Revenue (TPC-H Q17)                            1947.57                 1996.49                 2054.51                 2009.15
Large Volume Customer (TPC-H Q18)                                   5339.42                 5421.17                 5727.75                 5561.37
Discounted Revenue (TPC-H Q19)                                       116.36                  114.64                  116.16                  114.57
Potential Part Promotion (TPC-H Q20)                                 289.01                  268.89                  265.03                  256.87
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  729.91                  740.04                  755.82                  747.59
Global Sales Opportunity Query (TPC-H Q22)                           215.13                  212.24                  218.87                  216.99

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0           88.0         1.0      167.0     261.0
PostgreSQL-BHT-1-0-2-1           0.0           88.0         1.0      167.0     261.0
PostgreSQL-BHT-1-1-1-1           0.0           87.0         1.0      164.0     254.0
PostgreSQL-BHT-1-1-2-1           0.0           87.0         1.0      164.0     254.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.60
PostgreSQL-BHT-1-0-2-1           0.60
PostgreSQL-BHT-1-1-1-1           0.62
PostgreSQL-BHT-1-1-2-1           0.61

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5986.11
PostgreSQL-BHT-1-0-2-1            6049.78
PostgreSQL-BHT-1-1-1-1            5810.03
PostgreSQL-BHT-1-1-2-1            5910.20

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 21      1  1.0          3771.43
PostgreSQL-BHT-1-0-2 1.0 1              2                 22      1  1.0          3600.00
PostgreSQL-BHT-1-1-1 1.0 1              1                 22      1  1.0          3600.00
PostgreSQL-BHT-1-1-2 1.0 1              2                 22      1  1.0          3600.00

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1771059267     1771059288
PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-0-2  1.0     1               1           2       1771059389     1771059411
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1771059267     1771059289
PostgreSQL-BHT-1-1-2-1  PostgreSQL-BHT-1-1-2  1.0     1               1           2       1771059389     1771059411

#### Actual
DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-BHT-1-0 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-1-1 - Pods [[1, 1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log &
```

test_benchbase_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1392s 
    Code: 1771064549
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one schema per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:632M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771064549
                TENANT_BY:schema
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96805
    volume_size:10G
    volume_used:632M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771064549
                TENANT_BY:schema
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.530000                   0.530000  111.275253                                                     112068.0                                              33437.0
PostgreSQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.446667                   0.446667   93.779159                                                     155759.0                                              38429.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.503333                   0.503333  105.676467                                                      50456.0                                              19023.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.490000                   0.486667  102.177274                                                      53637.0                                              20450.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.98                       0.98         0.0                                                     155759.0                                              35933.0
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.99                       0.99         0.0                                                      53637.0                                              19736.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      322.0        1.0   2.0          11.180124
PostgreSQL-1-1-1024-2      322.0        1.0   2.0          11.180124

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Database-Per-Tenant

At first we remove old storage (or via `-rsr`)
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1
```

Example for run with 2 tenants for 5 minutes, keying and thinking time activated, 1 warehouse and 10 clients per tenant, each having a dedicated database in the same DBMS.
The execution phase is run twice.
```bash
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log &
```

test_benchbase_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1475s 
    Code: 1759406440
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435724660
    datadisk:651
    volume_size:10G
    volume_used:648M
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1759406440
                TENANT_BY:database
                TENANT_NUM:2
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435724664
    datadisk:652
    volume_size:10G
    volume_used:648M
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1759406440
                TENANT_BY:database
                TENANT_NUM:2

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-2               1         10    1024       1      1  300.0           0                      0.499998                   0.499998  104.976352                                                     841162.0                                             233857.0
PostgreSQL-1-1-1024-1-1               1         10    1024       1      2  300.0           0                      0.503332                   0.506665  106.376033                                                     675298.0                                             194761.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      1  300.0           0                      0.469999                   0.473332   99.377606                                                     911456.0                                             250308.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      2  300.0           0                      0.469999                   0.473332   99.377628                                                     895892.0                                             234292.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          1.00                       1.01         0.0                                                     841162.0                                             214309.0
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.94                       0.95         0.0                                                     911456.0                                             242300.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      436.0        1.0   2.0           8.256881
PostgreSQL-1-1-1024-2      436.0        1.0   2.0           8.256881

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 5Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log &
```

test_benchbase_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1492s 
    Code: 1771072762
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 5Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-0-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96806
    volume_size:5.0G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771072762
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-0-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96806
    volume_size:5.0G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771072762
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96806
    volume_size:5.0G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771072762
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
                TENANT:1
PostgreSQL-1-1-1024-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96806
    volume_size:5.0G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771072762
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
                TENANT:1

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.466667                   0.466667   97.978217                                                     342045.0                                             112990.0
PostgreSQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.493333                   0.496667  104.276815                                                     200260.0                                              63424.0
PostgreSQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.510000                   0.506667  106.376354                                                     123989.0                                              49760.0
PostgreSQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.480000                   0.483333  101.477436                                                     265316.0                                              55224.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.96                       0.96         0.0                                                     342045.0                                              88207.0
1-2               1         20    2048          2  300.0           0                          0.99                       0.99         0.0                                                     265316.0                                              52492.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-0-1      313.0        1.0   1.0          11.501597
PostgreSQL-1-1-1024-0-2      313.0        1.0   1.0          11.501597
PostgreSQL-1-1-1024-1-1      377.0        1.0   1.0           9.549072
PostgreSQL-1-1-1024-1-2      377.0        1.0   1.0           9.549072

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_mysql_tenants_database.log &
```

test_benchbase_run_mysql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1136s 
    Code: 1758718431
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:440464384
    datadisk:4669
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758718431
                TENANT_BY:database
                TENANT_NUM:2
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:440474724
    datadisk:4679
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758718431
                TENANT_BY:database
                TENANT_NUM:2

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-2               1         10    1024       1      1  300.0           0                      0.459999                   0.453332   95.178548                                                      76084.0                                              26409.0
MySQL-1-1-1024-1-1               1         10    1024       1      2  300.0           0                      0.539998                   0.543332  114.074327                                                      84308.0                                              28447.0
MySQL-1-1-1024-2-1               1         10    1024       2      1  300.0           0                      0.489999                   0.486665  102.177033                                                      52566.0                                              22908.0
MySQL-1-1-1024-2-2               1         10    1024       2      2  300.0           0                      0.486665                   0.486665  102.176958                                                      74052.0                                              28352.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         20    2048          2  300.0           0                          1.00                       1.00         0.0                                                      84308.0                                              27428.0
MySQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.98                       0.97         0.0                                                      74052.0                                              25630.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1       96.0        1.0   2.0               37.5
MySQL-1-1-1024-2       96.0        1.0   2.0               37.5

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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 5Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_mysql_tenants_container.log &
```

test_benchbase_run_mysql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1400s 
    Code: 1758719572
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
MySQL-1-1-1024-0-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:444749600
    datadisk:4429
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758719572
                TENANT_BY:container
                TENANT_NUM:2
MySQL-1-1-1024-0-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:444763700
    datadisk:4434
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758719572
                TENANT_BY:container
                TENANT_NUM:2
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:444749600
    datadisk:4425
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758719572
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:444763700
    datadisk:4434
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758719572
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1

### Execution

#### Per Pod
                      experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                  
MySQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.440000                   0.440000   92.379445                                                     108783.0                                              30251.0
MySQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.453332                   0.453332   95.178545                                                     156823.0                                              34946.0
MySQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.479999                   0.479999  100.777296                                                      56416.0                                              22940.0
MySQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.473332                   0.476665  100.077439                                                      60623.0                                              23523.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.89                       0.89         0.0                                                     156823.0                                              32598.5
1-2               1         20    2048          2  300.0           0                          0.95                       0.96         0.0                                                      60623.0                                              23231.5

### Workflow

#### Actual
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-0-1      182.0        1.0   1.0           19.78022
MySQL-1-1-1024-0-2      182.0        1.0   1.0           19.78022
MySQL-1-1-1024-1-1      182.0        1.0   1.0           19.78022
MySQL-1-1-1024-1-2      182.0        1.0   1.0           19.78022

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```





