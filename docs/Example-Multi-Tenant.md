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
    Duration: 739s 
    Code: 1772193919
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
PostgreSQL-BHT-2-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772193919
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772193919
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772193919
        TENANT_BY:schema
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772193919
        TENANT_BY:schema
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2027.10               2015.58               2003.92               2018.44
Minimum Cost Supplier Query (TPC-H Q2)                             480.79                470.94                448.70                446.29
Shipping Priority (TPC-H Q3)                                       731.24                724.20                685.51                685.21
Order Priority Checking Query (TPC-H Q4)                           357.29                361.93                355.80                355.40
Local Supplier Volume (TPC-H Q5)                                   659.89                639.85                633.84                627.06
Forecasting Revenue Change (TPC-H Q6)                              468.08                461.87                460.73                467.47
Forecasting Revenue Change (TPC-H Q7)                              754.93                745.17                740.77                741.29
National Market Share (TPC-H Q8)                                   433.58                438.48                382.97                382.50
Product Type Profit Measure (TPC-H Q9)                            1029.29               1022.89                982.12                980.78
Forecasting Revenue Change (TPC-H Q10)                             561.22                562.51                569.50                570.01
Important Stock Identification (TPC-H Q11)                         181.95                168.17                166.04                161.59
Shipping Modes and Order Priority (TPC-H Q12)                      646.19                647.15                647.83                652.34
Customer Distribution (TPC-H Q13)                                 2115.44               2197.04               2160.56               2128.04
Forecasting Revenue Change (TPC-H Q14)                             495.01                783.14                503.87                784.12
Top Supplier Query (TPC-H Q15)                                     509.93                509.41                517.14                502.19
Parts/Supplier Relationship (TPC-H Q16)                            566.37                562.25                565.42                555.79
Small-Quantity-Order Revenue (TPC-H Q17)                          1786.90               1739.60               1755.63               1750.54
Large Volume Customer (TPC-H Q18)                                 5501.46               6163.41               6771.44               6327.48
Discounted Revenue (TPC-H Q19)                                     286.42                119.36                116.87                116.56
Potential Part Promotion (TPC-H Q20)                               272.68                267.44                252.84                249.02
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                737.60                732.39                751.49                742.56
Global Sales Opportunity Query (TPC-H Q22)                         222.92                221.57                220.41                219.65

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           1.0          132.0         7.0      236.0     378.0
PostgreSQL-BHT-2-1-2           1.0          132.0         7.0      236.0     378.0
PostgreSQL-BHT-2-2-1           1.0          132.0         7.0      236.0     378.0
PostgreSQL-BHT-2-2-2           1.0          132.0         7.0      236.0     378.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.65
PostgreSQL-BHT-2-1-2           0.63
PostgreSQL-BHT-2-2-1           0.61
PostgreSQL-BHT-2-2-2           0.62

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5573.14
PostgreSQL-BHT-2-1-2            5696.88
PostgreSQL-BHT-2-2-1            5883.71
PostgreSQL-BHT-2-2-2            5814.73

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 24      2  1.0          6600.00
PostgreSQL-BHT-2-2 1.0 1              2                 23      2  1.0          6886.96

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1772194412     1772194435
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1772194412     1772194436
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1772194555     1772194578
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1772194555     1772194577

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
    Duration: 647s 
    Code: 1772794810
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.22.
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
PostgreSQL-BHT-2-1-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772794810
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-1-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772794810
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772794810
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-2-2-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    volume_size:10G
    volume_used:5.4G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772794810
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2-2
Pricing Summary Report (TPC-H Q1)                                 2083.23               2053.38               2065.82               2070.39
Minimum Cost Supplier Query (TPC-H Q2)                             485.37                485.71                442.85                450.54
Shipping Priority (TPC-H Q3)                                       695.08                701.74                658.33                656.33
Order Priority Checking Query (TPC-H Q4)                           337.95                328.42                323.76                337.60
Local Supplier Volume (TPC-H Q5)                                   621.78                606.42                620.54                616.62
Forecasting Revenue Change (TPC-H Q6)                              444.97                439.96                447.80                441.88
Forecasting Revenue Change (TPC-H Q7)                              706.57                709.69                720.74                719.67
National Market Share (TPC-H Q8)                                   404.32                397.71                359.06                345.83
Product Type Profit Measure (TPC-H Q9)                             985.54               1057.29                982.52                999.57
Forecasting Revenue Change (TPC-H Q10)                             532.19                549.31                539.50                534.07
Important Stock Identification (TPC-H Q11)                         167.47                156.83                164.57                169.89
Shipping Modes and Order Priority (TPC-H Q12)                      627.10                620.93                625.84                634.00
Customer Distribution (TPC-H Q13)                                 2055.30               1967.05               2147.13               1990.05
Forecasting Revenue Change (TPC-H Q14)                             483.74                745.39                485.54                764.77
Top Supplier Query (TPC-H Q15)                                     501.67                493.60                501.98                506.52
Parts/Supplier Relationship (TPC-H Q16)                            531.62                542.10                528.38                533.42
Small-Quantity-Order Revenue (TPC-H Q17)                          1942.72               1748.89               1767.79               1805.97
Large Volume Customer (TPC-H Q18)                                 5558.10               5644.78               5680.19               6356.11
Discounted Revenue (TPC-H Q19)                                     115.13                110.46                377.61                113.05
Potential Part Promotion (TPC-H Q20)                               261.24                252.10                229.20                257.10
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                728.95                724.34                722.95                725.74
Global Sales Opportunity Query (TPC-H Q22)                         209.64                213.01                209.57                214.29

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-2-1-1           1.0          118.0         3.0      208.0     333.0
PostgreSQL-BHT-2-1-2           1.0          118.0         3.0      208.0     333.0
PostgreSQL-BHT-2-2-1           1.0          118.0         3.0      208.0     333.0
PostgreSQL-BHT-2-2-2           1.0          118.0         3.0      208.0     333.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-2-1-1           0.60
PostgreSQL-BHT-2-1-2           0.61
PostgreSQL-BHT-2-2-1           0.62
PostgreSQL-BHT-2-2-2           0.61

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-2-1-1            5990.91
PostgreSQL-BHT-2-1-2            5942.13
PostgreSQL-BHT-2-2-1            5798.83
PostgreSQL-BHT-2-2-2            5927.53

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-2-1 1.0 1              1                 24      2  1.0          6600.00
PostgreSQL-BHT-2-2 1.0 1              2                 23      2  1.0          6886.96

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-2-1-1  PostgreSQL-BHT-2-1  1.0     2               1           1       1772795267     1772795290
PostgreSQL-BHT-2-1-2  PostgreSQL-BHT-2-1  1.0     2               1           1       1772795266     1772795289
PostgreSQL-BHT-2-2-1  PostgreSQL-BHT-2-2  1.0     2               1           2       1772795371     1772795393
PostgreSQL-BHT-2-2-2  PostgreSQL-BHT-2-2  1.0     2               1           2       1772795371     1772795394

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
    Duration: 897s 
    Code: 1772195519
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
PostgreSQL-BHT-1-0-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772195519
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-0-2-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772195519
        TENANT_BY:container
        TENANT_NUM:2
PostgreSQL-BHT-1-1-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772195519
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1
PostgreSQL-BHT-1-1-2-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146850
    volume_size:5.0G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772195519
        TENANT_BY:container
        TENANT_NUM:2
        TENANT:1

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-2-1
Pricing Summary Report (TPC-H Q1)                                   2138.53                 2120.55                 2015.43                 2019.14
Minimum Cost Supplier Query (TPC-H Q2)                               463.46                  454.30                  451.09                  399.24
Shipping Priority (TPC-H Q3)                                         713.83                  651.30                  699.60                  645.12
Order Priority Checking Query (TPC-H Q4)                             339.28                  328.89                  325.72                  326.50
Local Supplier Volume (TPC-H Q5)                                     607.20                  614.72                  593.28                  568.50
Forecasting Revenue Change (TPC-H Q6)                                440.57                  457.81                  448.66                  448.17
Forecasting Revenue Change (TPC-H Q7)                                713.36                  735.22                  681.06                  691.12
National Market Share (TPC-H Q8)                                     404.74                  368.00                  397.40                  343.59
Product Type Profit Measure (TPC-H Q9)                              1012.71                 1035.34                  993.01                  991.79
Forecasting Revenue Change (TPC-H Q10)                               551.57                  566.00                  531.98                  541.39
Important Stock Identification (TPC-H Q11)                           168.31                  167.48                  153.72                  152.74
Shipping Modes and Order Priority (TPC-H Q12)                        622.85                  637.76                  633.78                  639.57
Customer Distribution (TPC-H Q13)                                   2016.44                 1984.17                 1992.89                 1960.09
Forecasting Revenue Change (TPC-H Q14)                               487.89                  497.30                  483.27                  489.79
Top Supplier Query (TPC-H Q15)                                       498.08                  506.41                  493.74                  504.90
Parts/Supplier Relationship (TPC-H Q16)                              534.62                  543.14                  531.32                  536.71
Small-Quantity-Order Revenue (TPC-H Q17)                            1813.34                 1737.98                 1717.57                 1715.16
Large Volume Customer (TPC-H Q18)                                   6037.74                 6263.61                 5487.65                 5508.29
Discounted Revenue (TPC-H Q19)                                       118.96                  118.60                  114.15                  116.61
Potential Part Promotion (TPC-H Q20)                                 270.22                  234.85                  248.59                  227.69
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  769.35                  769.66                  739.02                  742.81
Global Sales Opportunity Query (TPC-H Q22)                           219.07                  218.67                  210.25                  209.13

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-0-1-1           0.0           96.0         3.0      235.0     337.0
PostgreSQL-BHT-1-0-2-1           0.0           96.0         3.0      235.0     337.0
PostgreSQL-BHT-1-1-1-1           0.0           93.0         3.0      229.0     327.0
PostgreSQL-BHT-1-1-2-1           0.0           93.0         3.0      229.0     327.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-1-0-1-1           0.61
PostgreSQL-BHT-1-0-2-1           0.60
PostgreSQL-BHT-1-1-1-1           0.59
PostgreSQL-BHT-1-1-2-1           0.58

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-1-0-1-1            5932.70
PostgreSQL-BHT-1-0-2-1            5990.67
PostgreSQL-BHT-1-1-1-1            6135.07
PostgreSQL-BHT-1-1-2-1            6244.74

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-1-0-1 1.0 1              1                 22      1  1.0          3600.00
PostgreSQL-BHT-1-0-2 1.0 1              2                 23      1  1.0          3443.48
PostgreSQL-BHT-1-1-1 1.0 1              1                 21      1  1.0          3771.43
PostgreSQL-BHT-1-1-2 1.0 1              2                 22      1  1.0          3600.00

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-1-0-1-1  PostgreSQL-BHT-1-0-1  1.0     1               1           1       1772196095     1772196117
PostgreSQL-BHT-1-0-2-1  PostgreSQL-BHT-1-0-2  1.0     1               1           2       1772196286     1772196309
PostgreSQL-BHT-1-1-1-1  PostgreSQL-BHT-1-1-1  1.0     1               1           1       1772196094     1772196115
PostgreSQL-BHT-1-1-2-1  PostgreSQL-BHT-1-1-2  1.0     1               1           2       1772196286     1772196308

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
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS_LOADER -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database_multiload.log &
```

test_tpch_run_postgresql_tenants_database_multiload.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 740s 
    Code: 1772796070
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.22.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 16 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [16] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772796070
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-16-1-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772796070
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-16-2-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772796070
        TENANT_BY:database
        TENANT_NUM:2
PostgreSQL-BHT-16-2-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:153301
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1772796070
        TENANT_BY:database
        TENANT_NUM:2

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-16-1-1  PostgreSQL-BHT-16-1-2  PostgreSQL-BHT-16-2-1  PostgreSQL-BHT-16-2-2
Pricing Summary Report (TPC-H Q1)                                  2051.92                2062.91                2055.59                2270.90
Minimum Cost Supplier Query (TPC-H Q2)                             1028.81                1023.25                1005.08                1009.52
Shipping Priority (TPC-H Q3)                                        760.65                 760.26                 689.15                 688.22
Order Priority Checking Query (TPC-H Q4)                            368.96                 363.25                 348.22                 349.54
Local Supplier Volume (TPC-H Q5)                                    780.95                 779.17                 763.43                 778.68
Forecasting Revenue Change (TPC-H Q6)                               471.25                 467.02                 449.31                 461.56
Forecasting Revenue Change (TPC-H Q7)                              1632.58                1648.53                1638.12                1638.04
National Market Share (TPC-H Q8)                                   1121.64                1125.00                1068.27                1071.00
Product Type Profit Measure (TPC-H Q9)                             1891.08                1889.74                1841.29                1846.50
Forecasting Revenue Change (TPC-H Q10)                             1471.37                1507.73                1471.00                1482.50
Important Stock Identification (TPC-H Q11)                          520.44                 528.17                 533.39                 524.64
Shipping Modes and Order Priority (TPC-H Q12)                       656.99                 650.47                 655.92                 646.73
Customer Distribution (TPC-H Q13)                                  2050.24                2053.27                2019.33                2036.26
Forecasting Revenue Change (TPC-H Q14)                              492.50                 818.31                 487.29                 823.37
Top Supplier Query (TPC-H Q15)                                      511.66                 522.40                 508.87                 522.76
Parts/Supplier Relationship (TPC-H Q16)                             532.46                 540.53                 531.13                 530.72
Small-Quantity-Order Revenue (TPC-H Q17)                           1933.98                1878.46                1708.83                1787.69
Large Volume Customer (TPC-H Q18)                                  6772.85                7811.03                6768.05                6896.75
Discounted Revenue (TPC-H Q19)                                      118.38                 118.64                 110.27                 112.74
Potential Part Promotion (TPC-H Q20)                                316.33                 324.35                 275.40                 289.85
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                1431.75                1438.54                1430.48                1447.93
Global Sales Opportunity Query (TPC-H Q22)                          234.58                 234.00                 213.39                 209.83

### Loading [s]
                       timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-16-1-1          52.0           82.0         3.0      342.0     484.0
PostgreSQL-BHT-16-1-2          52.0           82.0         3.0      342.0     484.0
PostgreSQL-BHT-16-2-1          52.0           82.0         3.0      342.0     484.0
PostgreSQL-BHT-16-2-2          52.0           82.0         3.0      342.0     484.0

### Geometric Mean of Medians of Timer Run [s]
                       Geo Times [s]
DBMS                                
PostgreSQL-BHT-16-1-1           0.83
PostgreSQL-BHT-16-1-2           0.86
PostgreSQL-BHT-16-2-1           0.80
PostgreSQL-BHT-16-2-2           0.83

### Power@Size ((3600*SF)/(geo times))
                       Power@Size [~Q/h]
DBMS                                    
PostgreSQL-BHT-16-1-1            4330.00
PostgreSQL-BHT-16-1-2            4194.08
PostgreSQL-BHT-16-2-1            4482.45
PostgreSQL-BHT-16-2-2            4317.04

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                   time [s]  count   SF  Throughput@Size
DBMS                SF  num_experiment num_client                                       
PostgreSQL-BHT-16-1 1.0 1              1                 30      2  1.0          5280.00
PostgreSQL-BHT-16-2 1.0 1              2                 29      2  1.0          5462.07

### Workflow
                                 orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-16-1-1  PostgreSQL-BHT-16-1  1.0    16               1           1       1772796621     1772796650
PostgreSQL-BHT-16-1-2  PostgreSQL-BHT-16-1  1.0    16               1           1       1772796621     1772796651
PostgreSQL-BHT-16-2-1  PostgreSQL-BHT-16-2  1.0    16               1           2       1772796724     1772796752
PostgreSQL-BHT-16-2-2  PostgreSQL-BHT-16-2  1.0    16               1           2       1772796724     1772796753

#### Actual
DBMS PostgreSQL-BHT-16 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-BHT-16 - Pods [[2, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
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
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log &
```

test_benchbase_run_postgresql_tenants_schema.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1744s 
    Code: 1772196452
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
    Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one schema per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:20G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772196452
                TENANT_BY:schema
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:20G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772196452
                TENANT_BY:schema
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.456665                   0.453332   95.178547                                                    1985364.0                                             362908.0
PostgreSQL-1-1-1024-1-2               1         10    1024       1      2  300.0         145                      0.480000                   0.000000    0.000000                                                       3320.0                                               2725.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.456667                   0.456667   95.878692                                                    1343523.0                                             571407.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      2  300.0         145                      0.483332                   0.000000    0.000000                                                       3942.0                                               2835.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0         145                          0.94                       0.45         0.0                                                    1985364.0                                             182816.5
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0         145                          0.94                       0.46         0.0                                                    1343523.0                                             287121.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      493.0        1.0   2.0           7.302231
PostgreSQL-1-1-1024-2      493.0        1.0   2.0           7.302231

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
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log &
```

test_benchbase_run_postgresql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1608s 
    Code: 1772198209
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
    Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [10] threads, split into [1] pods.
    Benchmarking is run as [2, 2] times the number of benchmarking pods.
    Number of tenants is 2, one database per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:20G
    volume_used:648M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772198209
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146842
    volume_size:20G
    volume_used:648M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772198209
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-2               1         10    1024       1      1  300.0           0                      0.513333                   0.510000  107.076140                                                      54412.0                                              21786.0
PostgreSQL-1-1-1024-1-1               1         10    1024       1      2  300.0           0                      0.486665                   0.489998  102.876807                                                      62873.0                                              19891.0
PostgreSQL-1-1-1024-2-1               1         10    1024       2      1  300.0           0                      0.483333                   0.483333  101.477396                                                      34613.0                                              16751.0
PostgreSQL-1-1-1024-2-2               1         10    1024       2      2  300.0           0                      0.503333                   0.506667  106.376349                                                      48125.0                                              16763.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         20    2048          2  300.0           0                          1.00                       1.00         0.0                                                      62873.0                                              20838.5
PostgreSQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.99                       0.99         0.0                                                      48125.0                                              16757.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[2, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      366.0        1.0   2.0           9.836066
PostgreSQL-1-1-1024-2      366.0        1.0   2.0           9.836066

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
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log &
```

test_benchbase_run_postgresql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 1586s 
    Code: 1772199829
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
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Number of tenants is 2, one container per tenant.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-0-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
    volume_size:10G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772199829
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-0-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
    volume_size:10G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772199829
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
PostgreSQL-1-1-1024-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
    volume_size:10G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772199829
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
                TENANT:1
PostgreSQL-1-1-1024-1-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146850
    volume_size:10G
    volume_used:328M
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772199829
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
                TENANT:1

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.493332                   0.486665  102.176959                                                     151694.0                                              53610.0
PostgreSQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.493333                   0.493333  103.576963                                                      38235.0                                              15204.0
PostgreSQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.483333                   0.486667  102.177288                                                     362720.0                                             122960.0
PostgreSQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.443333                   0.446667   93.779151                                                      27949.0                                              14859.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.99                       0.98         0.0                                                     151694.0                                              34407.0
1-2               1         20    2048          2  300.0           0                          0.93                       0.93         0.0                                                     362720.0                                              68909.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024-0 - Pods [[1, 1]]
DBMS PostgreSQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-0-1      249.0        1.0   1.0          14.457831
PostgreSQL-1-1-1024-0-2      249.0        1.0   1.0          14.457831
PostgreSQL-1-1-1024-1-1      260.0        1.0   1.0          13.846154
PostgreSQL-1-1-1024-1-2      260.0        1.0   1.0          13.846154

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
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_mysql_tenants_database.log &
```

test_benchbase_run_mysql_tenants_database.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 3130s 
    Code: 1772201428
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
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
    disk:146843
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
                code:1772201428
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
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
                code:1772201428
                TENANT_BY:database
                TENANT_NUM:2
                TENANT_VOL:False

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1         10    1024       1      1  300.0           0                      0.486667                   0.480000  100.777588                                                     747035.0                                             234830.0
MySQL-1-1-1024-1-2               1         10    1024       1      2  300.0           0                      0.436667                   0.440000   92.379462                                                    4543211.0                                             496056.0
MySQL-1-1-1024-2-2               1         10    1024       2      1  300.0           0                      0.500000                   0.496667  104.276807                                                     164983.0                                              55657.0
MySQL-1-1-1024-2-1               1         10    1024       2      2  300.0           0                      0.480000                   0.476666  100.077685                                                     136146.0                                              40417.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         20    2048          2  300.0           0                          0.92                       0.92         0.0                                                    4543211.0                                             365443.0
MySQL-1-1-1024-2               1         20    2048          2  300.0           0                          0.98                       0.97         0.0                                                     164983.0                                              48037.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[2, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1     1284.0        1.0   2.0           2.803738
MySQL-1-1-1024-2     1284.0        1.0   2.0           2.803738

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
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/test_benchbase_run_mysql_tenants_container.log &
```

test_benchbase_run_mysql_tenants_container.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 3330s 
    Code: 1772204569
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
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
    disk:146843
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
                code:1772204569
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-0-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
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
                code:1772204569
                TENANT_BY:container
                TENANT_NUM:2
                TENANT_VOL:False
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
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
                code:1772204569
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
                TENANT_VOL:False
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146843
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
                code:1772204569
                TENANT_BY:container
                TENANT_NUM:2
                TENANT:1
                TENANT_VOL:False

### Execution

#### Per Pod
                      experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                  
MySQL-1-1-1024-0-1-1               1         10    1024       1      1  300.0           0                      0.496665                   0.493332  103.576654                                                      93356.0                                             310717.0
MySQL-1-1-1024-1-1-1               1         10    1024       1      1  300.0           0                      0.443333                   0.440000   92.379464                                                    1659868.0                                             602605.0
MySQL-1-1-1024-0-2-1               1         10    1024       2      1  300.0           0                      0.496667                   0.500000  104.976648                                                      37928.0                                              17323.0
MySQL-1-1-1024-1-2-1               1         10    1024       2      1  300.0           0                      0.520000                   0.520000  109.175728                                                     546839.0                                             133408.0

#### Aggregated Parallel
     experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
1-1               1         20    2048          2  300.0           0                          0.94                       0.93         0.0                                                    1659868.0                                             456661.0
1-2               1         20    2048          2  300.0           0                          1.02                       1.02         0.0                                                     546839.0                                              75365.5

### Workflow

#### Actual
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

#### Planned
DBMS MySQL-1-1-1024-0 - Pods [[1, 1]]
DBMS MySQL-1-1-1024-1 - Pods [[1, 1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-0-1     1255.0        1.0   1.0           2.868526
MySQL-1-1-1024-0-2     1255.0        1.0   1.0           2.868526
MySQL-1-1-1024-1-1     1025.0        1.0   1.0           3.512195
MySQL-1-1-1024-1-2     1025.0        1.0   1.0           3.512195

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```







